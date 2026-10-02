"""The mock backend: the whole engine for $0 (CLAUDE.md: every external dependency has a mock).

An output is built in three layers, the first that matches wins:
1. a scripted rule: `{"agent": name, "key": regex, "output": {...}, "edits": {path: text},
   "raise": "transient" | "rate_limit" | "timeout" | "failed"}`, matched against the unit key;
2. a semantic default for the agents whose output the engine acts on (verdicts, plans, files);
3. an instance synthesised from the agent's own schema, so the mock always fits the data.

Coding agents act on their working directory as a real session would: scripted `edits` are
written there; otherwise a notes file is appended, so every coding unit leaves a diff.
"""
from __future__ import annotations

import json
import re
import threading
import time
from pathlib import Path
from typing import Any, Callable, Optional

from .base import (AgentCall, AgentFailed, AgentResult, AgentTimeout, Backend, InvalidOutput,
                   RateLimited, TransientError)


def synth(schema: dict, name: str = "x") -> Any:
    """A minimal instance that satisfies `schema` (the subset of JSON Schema agents use)."""
    if "anyOf" in schema:
        return synth(schema["anyOf"][0], name)
    if "oneOf" in schema:
        return synth(schema["oneOf"][0], name)
    if "enum" in schema:
        return schema["enum"][0]
    if "const" in schema:
        return schema["const"]
    kind = schema.get("type")
    if isinstance(kind, list):
        kind = next((k for k in kind if k != "null"), kind[0])
    if kind == "object":
        props = schema.get("properties", {})
        return {k: synth(v, k) for k, v in props.items()}
    if kind == "array":
        n = max(1, int(schema.get("minItems", 1)))
        if "maxItems" in schema:
            n = min(n, int(schema["maxItems"]))
        return [synth(schema.get("items", {"type": "string"}), f"{name}{i + 1}") for i in range(n)]
    if kind == "integer":
        lo = schema.get("minimum", 0)
        hi = schema.get("maximum", lo)
        return int(max(lo, min(hi, lo)))
    if kind == "number":
        return float(schema.get("minimum", 0.0))
    if kind == "boolean":
        return True
    if kind == "null":
        return None
    return f"mock {name}"


_MAIN_TEX = r"""\documentclass{article}
\usepackage{booktabs}
\title{Mock manuscript}
\begin{document}
\maketitle
\begin{abstract}A mock manuscript written by the mock backend.\end{abstract}
\section{Method}The method is described here.
\section{Results}
\input{results}
\bibliographystyle{plain}
\bibliography{references}
\end{document}
"""
_BIB = "@misc{mock2026,\n  title = {A mock reference},\n  author = {Mock, A.},\n  year = {2026}\n}\n"


def _n(call: AgentCall, name: str, default: int) -> int:
    try:
        return int(call.meta.get(name, default))
    except (TypeError, ValueError):
        return default


class MockBackend(Backend):
    name = "mock"

    def __init__(self, script: Optional[dict] = None, schemas: Optional[dict[str, dict]] = None):
        self.rules: list[dict] = list((script or {}).get("rules", []))
        self.schemas = schemas or {}
        self.calls: list[tuple[str, str]] = []           # (agent, key), for tests
        self._fired: dict[int, int] = {}                 # rule index -> times used
        self._lock = threading.Lock()
        self.semantic: dict[str, Callable[[AgentCall, dict], dict]] = {
            "limitation_verifier": lambda c, o: {**o, "verdict": "sufficient"},
            "subset_critic": lambda c, o: {**o, "verdict": "Good"},
            "full_set_critic": lambda c, o: {**o, "verdict": "Good"},
            "ablation_critic": lambda c, o: {**o, "verdict": "Good"},
            "meta_reviewer": lambda c, o: {**o, "decision": "Accept"},
            "peer_reviewer": lambda c, o: {**o, "score": 8},
            "spec_filter": lambda c, o: {**o, "compliant": True, "violations": []},
            "method_code_auditor": lambda c, o: {**o, "consistent": True, "issues": []},
            "ablation_planner": self._plans,
            "rebuttal_planner": self._rebuttal_tasks,
            "novelty_checker": lambda c, o: {**o, "novelty_score": 6},
        }

    def describe(self) -> dict[str, Any]:
        return {"backend": self.name, "rules": len(self.rules)}

    # ---- semantic defaults ----------------------------------------------------------------------
    def _plans(self, call: AgentCall, out: dict) -> dict:
        n = _n(call, "n_plans", 2)
        item = (out.get("plans") or [{}])[0]
        return {**out, "plans": [{**item, "id": f"A{i + 1}", "component": f"component {i + 1}"}
                                 for i in range(n)]}

    def _rebuttal_tasks(self, call: AgentCall, out: dict) -> dict:
        n = _n(call, "n_tasks", 1)
        item = (out.get("tasks") or [{}])[0]
        return {**out, "tasks": [{**item, "id": f"R{i + 1}"} for i in range(n)]}

    # ---- the call ---------------------------------------------------------------------------------
    def _rule(self, call: AgentCall) -> Optional[dict]:
        with self._lock:
            for i, rule in enumerate(self.rules):
                if rule.get("agent") not in (None, call.agent):
                    continue
                if rule.get("key") and not re.search(rule["key"], call.key):
                    continue
                limit = rule.get("times")
                if limit is not None and self._fired.get(i, 0) >= limit:
                    continue
                self._fired[i] = self._fired.get(i, 0) + 1
                return rule
        return None

    def call(self, call: AgentCall) -> AgentResult:
        with self._lock:
            self.calls.append((call.agent, call.key))
        rule = self._rule(call) or {}
        failure = rule.get("raise")
        if failure == "transient":
            raise TransientError(f"mock transient failure for {call.key}")
        if failure == "rate_limit":
            raise RateLimited(f"mock usage limit for {call.key}", reset_at=time.time() + 1)
        if failure == "timeout":
            raise AgentTimeout(f"mock timeout for {call.key}")
        if failure == "failed":
            raise AgentFailed(f"mock failure for {call.key}")
        if failure == "invalid":
            raise InvalidOutput(f"mock invalid output for {call.key}")

        schema = call.schema or self.schemas.get(call.agent) or {"type": "object"}
        output = synth(schema, call.agent)
        if call.agent in self.semantic and isinstance(output, dict):
            output = self.semantic[call.agent](call, output)
        if "output" in rule:
            output = {**output, **rule["output"]} if isinstance(output, dict) else rule["output"]

        if call.cwd is not None and call.kind in ("coding", "writer"):
            self._act(call, rule.get("edits"))
        if call.transcript is not None:
            call.transcript.write_text(json.dumps({"mock": True, "agent": call.agent,
                                                   "key": call.key, "output": output}) + "\n")
        return AgentResult(output=output, text=json.dumps(output), cost_usd=0.0, duration_s=0.0,
                           raw={"model": f"mock:{call.model}", "api_key_source": "none"})

    def _act(self, call: AgentCall, edits: Optional[dict]) -> None:
        cwd = Path(call.cwd)  # type: ignore[arg-type]
        if edits:
            for rel, text in edits.items():
                target = cwd / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
            return
        if call.kind == "writer":
            main = cwd / "main.tex"
            if not main.exists():
                main.write_text(_MAIN_TEX)
                (cwd / "references.bib").write_text(_BIB)
            else:
                main.write_text(main.read_text().replace(
                    r"\end{document}", f"% revised by {call.agent} ({call.key})\n\\end{{document}}"))
            return
        with open(cwd / "MOCK_NOTES.md", "a", encoding="utf-8") as f:
            f.write(f"- {call.agent} at {call.key}\n")
