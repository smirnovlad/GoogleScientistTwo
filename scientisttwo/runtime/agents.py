"""The agent runtime: an agent is data (prompt, schema, route); this runs it as one unit of work.

`AgentRuntime.run(key, agent, variables)`:
  1. a finished unit at `key` returns from the store, with no call (resume), once its recorded
     inputs hash is checked against the inputs it would be sent now: a replay never answers a
     different question (infrastructure review 2026-10-02, I1);
  2. the budget guard may stop the run first;
  3. the backend is called, with retries. Every attempt is journalled before its call, and writes
     one ledger line after it (I2), numbered on from the unit's attempts in earlier processes:
     - a transient error is retried twice with backoff, then the RUN PAUSES (the idea is not at
       fault, and a half-recorded unit must not exist);
     - an invalid output is retried once, with the error shown to the agent;
     - a usage limit is waited out up to `max_wait_minutes`, at most `max_waits` times, else the
       run pauses;
     - a fault of the machine (no space, a permission the engine needs) pauses the run;
     - a timeout is retried `retries_timeout` times from a clean start, then fails the unit;
     - a final refusal fails the unit;
  4. the output is validated against the agent's schema;
  5. the unit is stored, THEN `on_done` runs (a coding unit finalises its workspace here). A crash
     between the two leaves a stored unit and the agent's working copy, which the caller turns
     into the version on resume, so a finished, paid call is never made again (Codex review
     2026-10-02, P1). ⛔ WHY NOT `on_done` first: a crash after it lost the paid result.
A unit that fails for good is stored as failed and raises `UnitFailed`, now and on resume, unless
the run stopped on it (the orchestrator then clears it, so the resume tries it again).
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

from ..harness.sandbox import SandboxPolicy
from .backends.base import (AgentCall, AgentFailed, AgentResult, AgentTimeout, Backend,
                            EnvironmentFault, InvalidOutput, RateLimited, TransientError)
from .budget import Budget, BudgetExceeded, RunPaused
from .store import RunStore

log = logging.getLogger("scientisttwo")
AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"
_PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")

try:                                     # the CLI validates too; this is the engine's own check
    import jsonschema
except ImportError:                      # pragma: no cover
    jsonschema = None


class InputsChanged(RuntimeError):
    """A finished unit would now be sent other inputs than the ones it answered."""


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
        # ⛔ WHY NOT drop a variable the agent does not declare: the stage passed it for the model
        # to read, so a silent drop is a cut on model-bound content that nobody chose
        extra = [v for v in variables if v not in self.variables]
        if extra:
            raise KeyError(f"{self.name}: variables {extra} are passed but not declared in agent.json")

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
    backend: str = "default"


class Routing:
    """Backend, model, effort and timeout per agent: config/routing.json, then the profile's."""

    def __init__(self, data: dict):
        self.data = data

    def route(self, spec: AgentSpec) -> Route:
        d = dict(self.data.get("default", {}))
        d.update(self.data.get("by_kind", {}).get(spec.kind, {}))
        d.update(self.data.get("agents", {}).get(spec.name, {}))
        timeout = int(d.get("timeout_s") or self.data.get("timeouts_s", {}).get(spec.kind, 1800))
        return Route(model=d.get("model", "sonnet"), effort=d.get("effort"), timeout_s=timeout,
                     backend=d.get("backend", "default"))


def _outcome(e: Exception) -> str:
    return {RateLimited: "rate_limited", TransientError: "transient", InvalidOutput: "invalid_output",
            AgentTimeout: "timeout", AgentFailed: "failed", EnvironmentFault: "environment"}.get(type(e), "error")


class AgentRuntime:
    def __init__(self, backend: Backend | dict[str, Backend], store: RunStore, budget: Budget,
                 routing: Routing, run_dir: Path, specs: Optional[dict[str, AgentSpec]] = None,
                 retries_transient: int = 2, retries_invalid: int = 1, retries_timeout: int = 1,
                 max_wait_minutes: float = 0.0, max_waits: int = 3,
                 sleep: Callable[[float], None] = time.sleep, strict_replay: bool = True):
        self.backends = backend if isinstance(backend, dict) else {"default": backend}
        if "default" not in self.backends:
            raise ValueError("the runtime needs a 'default' backend")
        self.store = store
        self.budget = budget
        self.routing = routing
        self.run_dir = Path(run_dir)
        self.specs = specs if specs is not None else load_specs()
        self.retries_transient = retries_transient
        self.retries_invalid = retries_invalid
        self.retries_timeout = retries_timeout
        self.max_wait_s = max_wait_minutes * 60
        self.max_waits = max_waits
        self.sleep = sleep
        self.strict_replay = strict_replay
        self._lock = threading.Lock()

    @property
    def backend(self) -> Backend:
        return self.backends["default"]

    def spec(self, agent: str) -> AgentSpec:
        if agent not in self.specs:
            raise KeyError(f"no agent {agent!r} among this run's agents")
        return self.specs[agent]

    def _backend_for(self, route: Route) -> Backend:
        if route.backend not in self.backends:
            raise KeyError(f"routing names backend {route.backend!r}, which this run has not started")
        return self.backends[route.backend]

    def inputs_sha(self, spec: AgentSpec, route: Route, user: str) -> str:
        return hashlib.sha256(json.dumps([spec.system, user, route.model, route.effort, route.backend],
                                         default=str).encode()).hexdigest()

    def recorded(self, key: str, agent: str, variables: dict[str, Any]) -> Optional[dict]:
        """The finished unit at `key`, checked against the inputs it would be sent now; None if
        the unit has not run. For callers that must look before `run` (a coding unit checks its
        version exists first), so no replay skips the check."""
        record = self.store.get(key)
        if record is not None:
            spec = self.spec(agent)
            route = self.routing.route(spec)
            self._check_replay(key, record, self.inputs_sha(spec, route, spec.render(variables)))
        return record

    def run(self, key: str, agent: str, variables: dict[str, Any], *, cwd: Optional[Path] = None,
            sandbox: Optional[SandboxPolicy] = None, tmpdir: Optional[Path] = None,
            on_done: Optional[Callable[[Optional[dict], Optional[str]], None]] = None,
            before_attempt: Optional[Callable[[int], None]] = None) -> dict:
        spec = self.spec(agent)
        route = self.routing.route(spec)
        user = spec.render(variables)
        inputs_sha = self.inputs_sha(spec, route, user)

        record = self.store.get(key)
        if record is not None:
            self._check_replay(key, record, inputs_sha)
            if record.get("status") == "failed":
                raise UnitFailed(key, record.get("error", "failed"))
            return record["output"]

        backend = self._backend_for(route)
        self._log_prompt(key, spec, route, user, inputs_sha)
        meta = {k: v for k, v in variables.items() if isinstance(v, (int, float, str)) and len(str(v)) < 200}
        text, transient, invalid, timeouts, waits, attempt = user, 0, 0, 0, 0, 0
        prior = self.budget.attempts_of(key)              # this unit's attempts in earlier processes
        started = time.time()
        while True:
            self.budget.check(spec.kind)
            attempt += 1
            number, attempt_id = prior + attempt, uuid.uuid4().hex
            if before_attempt is not None:
                before_attempt(attempt)
            self.budget.started({"key": key, "agent": agent, "kind": spec.kind, "attempt": number,
                                 "attempt_id": attempt_id})
            call = AgentCall(agent=agent, kind=spec.kind, system=spec.system, user=text,
                             schema=spec.schema, model=route.model, effort=route.effort,
                             tools=spec.tools, cwd=cwd, sandbox=sandbox, timeout_s=route.timeout_s,
                             transcript=self._transcript(key, number), key=key, meta=meta,
                             tmpdir=tmpdir, attempt=number)
            t0 = time.time()
            result: Optional[AgentResult] = None
            try:
                result = backend.call(call)
                self._validate(spec, result)
            except (RateLimited, TransientError, InvalidOutput, AgentTimeout, AgentFailed,
                    EnvironmentFault) as e:
                self._ledger(key, agent, spec, route, number, attempt_id, _outcome(e), t0, result,
                             str(e), failure=e)
                if isinstance(e, RateLimited):
                    waits += 1
                    wait = (e.reset_at - time.time() + 60) if e.reset_at else None
                    if wait is not None and 0 < wait <= self.max_wait_s and waits <= self.max_waits:
                        log.warning("%s: usage limit, waiting %.0f min for the reset", key, wait / 60)
                        self.budget.record_event({"type": "rate_limit_wait", "key": key, "seconds": wait})
                        self.sleep(wait)
                        continue
                    raise BudgetExceeded(f"subscription usage limit: {e}", resume_after=e.reset_at) from e
                if isinstance(e, EnvironmentFault):
                    raise RunPaused(f"{key}: the machine failed, not the agent: {e}") from e
                if isinstance(e, TransientError):
                    transient += 1
                    if transient > self.retries_transient:
                        raise RunPaused(f"{key}: transient errors persisted over {transient} attempts: {e}") from e
                    log.warning("%s: transient error (%s), retry %d", key, e, transient)
                    self.sleep(min(60.0, 5.0 * 2 ** transient))
                    continue
                if isinstance(e, AgentTimeout):
                    timeouts += 1
                    if timeouts <= self.retries_timeout:
                        log.warning("%s: timed out, retry %d from a clean start", key, timeouts)
                        continue
                if isinstance(e, InvalidOutput):
                    invalid += 1
                    if invalid > self.retries_invalid:
                        self._fail(key, agent, spec, route, f"invalid output: {e}", started, inputs_sha, on_done)
                    text = (user + "\n\n---\nYour previous answer was rejected: " + str(e)[:1500] +
                            "\nAnswer again, as the required structured output.")
                    continue
                self._fail(key, agent, spec, route, f"{type(e).__name__}: {e}", started, inputs_sha, on_done)
            self._ledger(key, agent, spec, route, number, attempt_id, "ok", t0, result, None)
            break

        assert result is not None
        self.store.put(key, {"status": "ok", "agent": agent, "kind": spec.kind, "model": route.model,
                             "effort": route.effort, "backend": route.backend, "inputs_sha256": inputs_sha,
                             "attempts": attempt, "output": result.output, "text": result.text[-4000:],
                             "equiv_usd": result.cost_usd, "seconds": round(time.time() - started, 2),
                             "session_id": result.session_id, "finished_at": time.time()})
        if on_done is not None:
            on_done(result.output, None)
        return result.output  # type: ignore[return-value]

    # ---- records --------------------------------------------------------------------------------
    def _check_replay(self, key: str, record: dict, inputs_sha: str) -> None:
        recorded = record.get("inputs_sha256")
        if recorded is None or recorded == inputs_sha:
            return
        msg = (f"{key}: this unit's inputs changed since it ran (prompt, variables, model or "
               f"backend). Start a new run, or resume with --allow-changed to replay its recorded output.")
        if self.strict_replay:
            raise InputsChanged(msg)
        log.warning("%s", msg)
        self.budget.record_event({"type": "replayed_changed_inputs", "key": key,
                                  "recorded": recorded, "now": inputs_sha})

    def _transcript(self, key: str, attempt: int) -> Path:
        name = f"{key}.jsonl" if attempt == 1 else f"{key}.attempt{attempt}.jsonl"
        path = self.run_dir / "transcripts" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _log_prompt(self, key: str, spec: AgentSpec, route: Route, user: str, inputs_sha: str) -> None:
        """What the agent is asked, in full: a run's history is data, not only hashes."""
        from .store import atomic_write_json
        atomic_write_json(self.run_dir / "prompts" / f"{key}.json", {
            "key": key, "agent": spec.name, "kind": spec.kind, "model": route.model,
            "effort": route.effort, "backend": route.backend, "tools": list(spec.tools),
            "inputs_sha256": inputs_sha, "system_sha256": hashlib.sha256(spec.system.encode()).hexdigest(),
            "user": user})

    def _ledger(self, key: str, agent: str, spec: AgentSpec, route: Route, attempt: int,
                attempt_id: str, outcome: str, t0: float, result: Optional[AgentResult],
                error: Optional[str], failure: Optional[Exception] = None) -> None:
        raw = result.raw if result is not None else {}
        # a failure the backend raised still carries what the call reported spending
        cost = result.cost_usd if result is not None else getattr(failure, "cost_usd", None)
        tokens = result.tokens if result is not None else getattr(failure, "tokens", None)
        self.budget.record({"key": key, "agent": agent, "kind": spec.kind, "attempt": attempt,
                            "attempt_id": attempt_id, "outcome": outcome, "backend": route.backend,
                            "model": raw.get("model") or route.model,
                            "seconds": round(time.time() - t0, 2),
                            "equiv_usd": cost, "tokens": tokens,
                            "rate_limit": raw.get("rate_limit"), "api_key_source": raw.get("api_key_source"),
                            "cli_version": raw.get("cli_version"),
                            **({"error": error[:500]} if error else {})})

    def _validate(self, spec: AgentSpec, result: AgentResult) -> None:
        if result.output is None:
            raise InvalidOutput("no structured output")
        if jsonschema is not None:
            try:
                jsonschema.validate(result.output, spec.schema)
            except jsonschema.ValidationError as e:
                raise InvalidOutput(f"schema violation at {list(e.absolute_path)}: {e.message}") from e

    def _fail(self, key: str, agent: str, spec: AgentSpec, route: Route, error: str, started: float,
              inputs_sha: str, on_done: Optional[Callable[[Optional[dict], Optional[str]], None]]) -> None:
        self.store.put(key, {"status": "failed", "agent": agent, "kind": spec.kind,
                             "model": route.model, "backend": route.backend, "inputs_sha256": inputs_sha,
                             "error": error[:4000], "seconds": round(time.time() - started, 2),
                             "finished_at": time.time()})
        if on_done is not None:
            on_done(None, error)
        raise UnitFailed(key, error)
