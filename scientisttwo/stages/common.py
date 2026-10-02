"""What every stage shares: the run context, sandbox policies, coding units and evaluations."""
from __future__ import annotations

import json
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

from ..harness.harness import Harness, gain, summarize
from ..harness.sandbox import SandboxPolicy
from ..runtime.agents import AgentRuntime, UnitFailed
from ..task import Task
from ..workspace import Workspaces

log = logging.getLogger("scientisttwo")
DIFF_CAP = 200_000
DATA_SUFFIXES = {".npz", ".npy", ".csv", ".tsv", ".gz", ".zip", ".bz2", ".xz", ".tar", ".pkl",
                 ".pickle", ".joblib", ".pt", ".pth", ".ckpt", ".h5", ".hdf5", ".parquet",
                 ".feather", ".arrow", ".mat", ".bin", ".safetensors", ".onnx"}
MAX_ADDED_BYTES = 1_000_000              # no added file this large is code (our choice, 2026-10-02)


class RunEnded(Exception):
    """A branch of analysis §4.3 that ends the run early, e.g. no idea succeeded."""

    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


@dataclass
class Ctx:
    task: Task
    cfg: dict
    rt: AgentRuntime
    harness: Harness
    ws: Workspaces
    run_dir: Path
    papers: Optional[Workspaces] = None      # manuscript versions, beside the code versions
    task_commit: str = ""                    # G's code as released: what every check compares with
    base_commit: str = ""
    overview: str = ""
    _events_lock: threading.Lock = field(default_factory=threading.Lock)

    # ---- configuration --------------------------------------------------------------------------
    def L(self, name: str) -> int:
        return int(self.cfg["limits"][name])

    def stage(self, name: str) -> dict:
        return self.cfg.get("stages", {}).get(name, {})

    @property
    def min_delta(self) -> float:
        """The noise floor of "strictly better": the task's, else the profile's."""
        if self.task.min_delta is not None:
            return float(self.task.min_delta)
        return float(self.cfg.get("guard", {}).get("min_delta", 0.0))

    # ---- events ---------------------------------------------------------------------------------
    def event(self, kind: str, **fields: Any) -> None:
        entry = {"time": round(time.time(), 3), "event": kind, **fields}
        with self._events_lock:
            with open(self.run_dir / "events.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        brief = " ".join(f"{k}={v}" for k, v in fields.items() if isinstance(v, (str, int, float)))
        log.info("%-22s %s", kind, brief[:200])

    # ---- sandbox policies -----------------------------------------------------------------------
    def _rules(self) -> dict:
        return self.harness.integrity()

    def policy_reasoning(self) -> SandboxPolicy:
        return SandboxPolicy.build(writable=[self.scratch], readonly=[self.harness.public],
                                   claude_state=True, **self._rules())

    def policy_coding(self, workdir: Path) -> SandboxPolicy:
        return SandboxPolicy.build(writable=[workdir], readonly=[self.harness.public],
                                   claude_state=True, **self._rules())

    def policy_readonly(self, workdir: Path) -> SandboxPolicy:
        # A-INT-3: an auditor reads, never writes, what it audits
        return SandboxPolicy.build(writable=[self.scratch], readonly=[workdir, self.harness.public],
                                   claude_state=True, **self._rules())

    @property
    def scratch(self) -> Path:
        p = self.run_dir / "scratch"
        p.mkdir(exist_ok=True)
        return p

    # ---- units ----------------------------------------------------------------------------------
    def think(self, key: str, agent: str, variables: dict, cwd: Optional[Path] = None,
              readonly: Optional[Path] = None) -> dict:
        """A reasoning (or read-only) unit. Raises UnitFailed if the agent fails for good."""
        if readonly is not None:
            return self.rt.run(key, agent, variables, cwd=readonly, sandbox=self.policy_readonly(readonly))
        return self.rt.run(key, agent, variables, cwd=cwd or self.scratch, sandbox=self.policy_reasoning())

    def code(self, key: str, agent: str, variables: dict, parent: str, name: str,
             on: Optional[Workspaces] = None) -> tuple[Optional[dict], Optional[str]]:
        """A coding unit: the agent edits a fresh copy of version `parent`, which becomes `name`.

        Returns (output, None) on success, (None, error) on failure. Either way the version
        exists afterwards, holding whatever the agent left, so the harness can judge it.
        """
        ws = on or self.ws
        record = self.rt.store.get(key)
        if record is not None and ws.exists(name):
            return (record.get("output"), None) if record.get("status") == "ok" else (None, record.get("error"))
        if record is not None:
            # the version this unit made is gone (removed by hand): its record alone cannot replay it
            log.warning("%s: version %s is missing; the unit runs again", key, name)
            self.rt.store.delete(key)
        tmp = ws.fresh(parent, name)

        def done(output: Optional[dict], error: Optional[str]) -> None:
            ws.finalize(tmp, name, f"{key}: {agent}" + (" (failed)" if error else ""))

        try:
            return self.rt.run(key, agent, variables, cwd=tmp, sandbox=self.policy_coding(tmp),
                               on_done=done), None
        except UnitFailed as e:
            if not ws.exists(name):
                ws.finalize(tmp, name, f"{key}: {agent} (failed)")
            return None, e.error

    def evaluate(self, key: str, name: str, split: str) -> dict:
        """The harness's result for version `name` on `split`, after the deterministic checks."""
        path, commit = self.ws.path(name), self.ws.commit(name)
        reason = self.check_change(name)
        if reason:
            self.event("rejected", version=name, reason=reason[:160])
            return self.harness.reject(key, path, split, reason, commit)
        return self.harness.evaluate(key, path, split, commit=commit)

    def check_change(self, name: str) -> Optional[str]:
        """Checkable task rules, applied by code before anything runs: the change may not add a
        forbidden string (a dataset loader, a URL …), nor a data file unless the task allows it."""
        if not self.task_commit:
            return None
        lines, files = self.ws.added(name, self.task_commit)
        low = lines.lower()
        for s in self.task.forbidden_in_diff:
            if s.lower() in low:
                return f"the change adds {s!r}, which the task forbids (rules.md)"
        if not self.task.allow_data_files:
            for f in files:
                if f["binary"] or Path(f["path"]).suffix.lower() in DATA_SUFFIXES or f["bytes"] > MAX_ADDED_BYTES:
                    return (f"the change adds the data file {f['path']} ({f['bytes']} bytes); "
                            "data may come only from the training split")
        return None

    def map(self, fn: Callable[[Any], Any], items: Iterable[Any]) -> list:
        """Run independent units in parallel (U-TOP-4), keeping order. Errors propagate."""
        items = list(items)
        workers = max(1, int(self.cfg.get("parallel", 1)))
        if workers == 1 or len(items) <= 1:
            return [fn(x) for x in items]
        with ThreadPoolExecutor(max_workers=min(workers, len(items))) as pool:
            futures = [pool.submit(fn, x) for x in items]
            return [f.result() for f in futures]

    # ---- what agents read -----------------------------------------------------------------------
    def entrypoint_text(self) -> str:
        t = self.task
        files = ", ".join(sorted(p.name for p in self.harness.public.iterdir())) if self.harness.public.exists() else ""
        return (
            "The engine's locked harness evaluates your code by running this command from the "
            f"codebase root, once per seed:\n  {t.entrypoint}\n"
            "where {python} is the engine's Python, {train_dir} is the public training data "
            f"directory {self.harness.public} (read-only; files: {files}), {{inputs}} is a file "
            "with the split's inputs and no labels, {out} is the predictions file the command must "
            "write, and {seed} is the seed.\n"
            "During evaluation the codebase is read-only and there is no network: write nothing "
            "but {out} (temporary files go to $TMPDIR). Validation and test labels are never "
            "readable; for self-checks, hold out part of the training data yourself. "
            f"Each run must finish within {t.eval_timeout_s} seconds.")

    def diff(self, name: str, stat_only: bool = False) -> str:
        # Critics and auditors judge the whole change. ⛔ WHY NOT no cap at all: an agent that
        # commits a data file would make every later prompt too long to send. Cap, our choice
        # (2026-10-02): DIFF_CAP characters, about 50k tokens; it loses the tail of such a diff.
        return self.ws.diff(name, self.base_commit, stat_only=stat_only, max_chars=DIFF_CAP)

    def result_view(self, result: dict, ref: Optional[dict] = None) -> dict:
        view = summarize(result)
        if ref is not None:
            view["gain_over_reference"] = gain(result, ref)
        return view


def gain_text(new: dict, ref: dict, task: Task) -> str:
    g = gain(new, ref)
    if g is None:
        return "not computable: at least one evaluation failed"
    sign = "an improvement" if g > 0 else ("no change" if g == 0 else "a regression")
    return (f"{g:+.6f} in {task.metric_name} ({sign}; {task.metric_info['better']}); "
            f"new mean {new['mean']:.6f} ± {new['std']:.6f} over {new['n_seeds']} seed(s), "
            f"reference mean {ref['mean']:.6f} ± {ref['std']:.6f} over {ref['n_seeds']} seed(s)")
