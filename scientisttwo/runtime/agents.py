"""The agent runtime: an agent is data (prompt, schema, route); this runs it as one unit of work.

`AgentRuntime.run(key, agent, variables)`:
  1. a finished unit at `key` returns from the store, with no call (resume);
  2. the budget guard may stop the run first;
  3. the backend is called, with retries: a transient error twice, an invalid output once (the
     error is shown to the agent), a usage limit waited out up to `max_wait_minutes`, else the
     run pauses;
  4. the output is validated against the agent's schema;
  5. `on_done` runs (a coding unit finalises its workspace here), then the unit is stored and
     the ledger written, in that order, so a stored unit always has its side effects.
A unit that fails for good is stored as failed and raises `UnitFailed`, now and on resume.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

from ..harness.sandbox import SandboxPolicy
from .backends.base import (AgentCall, AgentFailed, AgentResult, AgentTimeout, Backend,
                            InvalidOutput, RateLimited, TransientError)
from .budget import Budget, BudgetExceeded
from .store import RunStore

log = logging.getLogger("scientisttwo")
AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"
_PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")

try:                                     # the CLI validates too; this is the engine's own check
    import jsonschema
except ImportError:                      # pragma: no cover
    jsonschema = None


class UnitFailed(RuntimeError):
    def __init__(self, key: str, error: str):
        super().__init__(f"{key}: {error}")
        self.key = key
        self.error = error


@dataclass(frozen=True)
class AgentSpec:
    name: str
    kind: str
    tools: tuple[str, ...]
    paper_ref: str
    description: str
    variables: tuple[str, ...]
    system: str
    prompt: str
    schema: dict

    @staticmethod
    def load(folder: Path) -> "AgentSpec":
        meta = json.loads((folder / "agent.json").read_text())
        spec = AgentSpec(name=meta["name"], kind=meta["kind"], tools=tuple(meta.get("tools", [])),
                         paper_ref=meta.get("paper_ref", ""), description=meta.get("description", ""),
                         variables=tuple(meta.get("variables", [])),
                         system=(folder / "system.md").read_text(),
                         prompt=(folder / "prompt.md").read_text(),
                         schema=json.loads((folder / "schema.json").read_text()))
        found = set(_PLACEHOLDER.findall(spec.prompt))
        if found != set(spec.variables):
            raise ValueError(f"{spec.name}: prompt placeholders {sorted(found)} differ from "
                             f"agent.json variables {sorted(spec.variables)}")
        return spec

    def render(self, variables: dict[str, Any]) -> str:
        missing = [v for v in self.variables if v not in variables]
        if missing:
            raise KeyError(f"{self.name}: missing template variables {missing}")

        def sub(m: re.Match) -> str:
            value = variables[m.group(1)]
            if isinstance(value, str):
                return value
            return json.dumps(value, indent=1, ensure_ascii=False, default=str)

        return _PLACEHOLDER.sub(sub, self.prompt)


def load_specs(folder: Optional[Path] = None) -> dict[str, AgentSpec]:
    """Every agent in `folder`: by default the engine's own, or $SCIENTISTTWO_AGENTS_DIR."""
    import os
    folder = Path(folder or os.environ.get("SCIENTISTTWO_AGENTS_DIR") or AGENTS_DIR)
    specs = {}
    for d in sorted(p for p in folder.iterdir() if (p / "agent.json").exists()):
        spec = AgentSpec.load(d)
        specs[spec.name] = spec
    return specs


@dataclass
class Route:
    model: str
    effort: Optional[str]
    timeout_s: int


class Routing:
    """Model, effort and timeout per agent: config/routing.json, then the profile's overrides."""

    def __init__(self, data: dict):
        self.data = data

    def route(self, spec: AgentSpec) -> Route:
        d = dict(self.data.get("default", {}))
        d.update(self.data.get("by_kind", {}).get(spec.kind, {}))
        d.update(self.data.get("agents", {}).get(spec.name, {}))
        timeout = int(d.get("timeout_s") or self.data.get("timeouts_s", {}).get(spec.kind, 1800))
        return Route(model=d.get("model", "sonnet"), effort=d.get("effort"), timeout_s=timeout)


class AgentRuntime:
    def __init__(self, backend: Backend, store: RunStore, budget: Budget, routing: Routing,
                 run_dir: Path, specs: Optional[dict[str, AgentSpec]] = None,
                 retries_transient: int = 2, retries_invalid: int = 1,
                 max_wait_minutes: float = 0.0, sleep: Callable[[float], None] = time.sleep):
        self.backend = backend
        self.store = store
        self.budget = budget
        self.routing = routing
        self.run_dir = Path(run_dir)
        self.specs = specs if specs is not None else load_specs()
        self.retries_transient = retries_transient
        self.retries_invalid = retries_invalid
        self.max_wait_s = max_wait_minutes * 60
        self.sleep = sleep
        self._lock = threading.Lock()

    def spec(self, agent: str) -> AgentSpec:
        if agent not in self.specs:
            raise KeyError(f"no agent {agent!r} in {AGENTS_DIR}")
        return self.specs[agent]

    def run(self, key: str, agent: str, variables: dict[str, Any], *, cwd: Optional[Path] = None,
            sandbox: Optional[SandboxPolicy] = None,
            on_done: Optional[Callable[[Optional[dict], Optional[str]], None]] = None) -> dict:
        record = self.store.get(key)
        if record is not None:
            if record.get("status") == "failed":
                raise UnitFailed(key, record.get("error", "failed"))
            return record["output"]

        spec = self.spec(agent)
        route = self.routing.route(spec)
        user = spec.render(variables)
        inputs_sha = hashlib.sha256(json.dumps([spec.system, user, route.model, route.effort],
                                               default=str).encode()).hexdigest()
        transcript = self.run_dir / "transcripts" / f"{key}.jsonl"
        transcript.parent.mkdir(parents=True, exist_ok=True)
        meta = {k: v for k, v in variables.items() if isinstance(v, (int, float, str)) and len(str(v)) < 200}

        def make_call(text: str) -> AgentCall:
            return AgentCall(agent=agent, kind=spec.kind, system=spec.system, user=text,
                             schema=spec.schema, model=route.model, effort=route.effort,
                             tools=spec.tools, cwd=cwd, sandbox=sandbox, timeout_s=route.timeout_s,
                             transcript=transcript, key=key, meta=meta)

        text, transient, invalid = user, 0, 0
        started = time.time()
        while True:
            self.budget.check(spec.kind)
            try:
                result = self.backend.call(make_call(text))
                self._validate(spec, result)
                break
            except RateLimited as e:
                wait = (e.reset_at - time.time() + 60) if e.reset_at else None
                if wait is not None and 0 < wait <= self.max_wait_s:
                    log.warning("%s: usage limit, waiting %.0f min for the reset", key, wait / 60)
                    self.budget.record_event({"type": "rate_limit_wait", "key": key, "seconds": wait})
                    self.sleep(wait)
                    continue
                raise BudgetExceeded(f"subscription usage limit: {e}", resume_after=e.reset_at) from e
            except TransientError as e:
                transient += 1
                if transient > self.retries_transient:
                    raise UnitFailed(key, f"transient errors persisted: {e}") from e
                log.warning("%s: transient error (%s), retry %d", key, e, transient)
                self.sleep(min(60.0, 5.0 * 2 ** transient))
            except InvalidOutput as e:
                invalid += 1
                if invalid > self.retries_invalid:
                    self._fail(key, agent, spec, route, f"invalid output: {e}", started, on_done)
                text = (user + "\n\n---\nYour previous answer was rejected: " + str(e)[:1500] +
                        "\nAnswer again, as the required structured output.")
            except (AgentTimeout, AgentFailed) as e:
                self._fail(key, agent, spec, route, f"{type(e).__name__}: {e}", started, on_done)

        if on_done is not None:
            on_done(result.output, None)
        self.store.put(key, {"status": "ok", "agent": agent, "kind": spec.kind, "model": route.model,
                             "effort": route.effort, "inputs_sha256": inputs_sha,
                             "output": result.output, "text": result.text[-4000:],
                             "equiv_usd": result.cost_usd, "seconds": round(time.time() - started, 2),
                             "session_id": result.session_id, "finished_at": time.time()})
        self.budget.record({"key": key, "agent": agent, "kind": spec.kind, "model": result.raw.get("model") or route.model,
                            "seconds": round(time.time() - started, 2), "equiv_usd": result.cost_usd,
                            "tokens": result.tokens, "rate_limit": result.raw.get("rate_limit"),
                            "api_key_source": result.raw.get("api_key_source")})
        return result.output  # type: ignore[return-value]

    def _validate(self, spec: AgentSpec, result: AgentResult) -> None:
        if result.output is None:
            raise InvalidOutput("no structured output")
        if jsonschema is not None:
            try:
                jsonschema.validate(result.output, spec.schema)
            except jsonschema.ValidationError as e:
                raise InvalidOutput(f"schema violation at {list(e.absolute_path)}: {e.message}") from e

    def _fail(self, key: str, agent: str, spec: AgentSpec, route: Route, error: str, started: float,
              on_done: Optional[Callable[[Optional[dict], Optional[str]], None]]) -> None:
        if on_done is not None:
            on_done(None, error)
        self.store.put(key, {"status": "failed", "agent": agent, "kind": spec.kind,
                             "model": route.model, "error": error[:4000],
                             "seconds": round(time.time() - started, 2), "finished_at": time.time()})
        self.budget.record({"key": key, "agent": agent, "kind": spec.kind, "model": route.model,
                            "seconds": round(time.time() - started, 2), "equiv_usd": None,
                            "failed": error[:500]})
        raise UnitFailed(key, error)
