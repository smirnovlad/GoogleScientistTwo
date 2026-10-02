"""What every stage shares: the run context, agent units, coding units and evaluations."""
from __future__ import annotations

import json
import logging
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

from ..harness.checks import change_violation
from ..harness.harness import Harness, gain
from ..harness.sandbox import SandboxPolicy
from ..runtime.agents import AgentRuntime, UnitFailed
from ..task import Task
from ..workspace import Workspaces, remove_unsafe

log = logging.getLogger("scientisttwo")
DIFF_CAP = 200_000


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
    services: list = field(default_factory=list)  # what the run started and stops at its end
    lock_fd: Optional[int] = None                 # the run lock, held for the process's life
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

    def gain_text(self, new: dict, ref: dict) -> str:
        return gain_text(new, ref, self.task, self.min_delta)

    # ---- events ---------------------------------------------------------------------------------
    def event(self, kind: str, **fields: Any) -> None:
        entry = {"time": round(time.time(), 3), "event": kind, **fields}
        with self._events_lock:
            with open(self.run_dir / "events.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        brief = " ".join(f"{k}={v}" for k, v in fields.items() if isinstance(v, (str, int, float)))
        log.info("%-22s %s", kind, brief[:200])

    # ---- sandboxes ------------------------------------------------------------------------------
    @property
    def scratch(self) -> Path:
        p = self.run_dir / "scratch"
        p.mkdir(exist_ok=True)
        return p

    def tmpdir(self, key: str) -> Path:
        """A unit's own TMPDIR, empty when it starts: no unit reads another's temporary files."""
        p = self.run_dir / "tmp" / key.replace("/", "__")
        shutil.rmtree(p, ignore_errors=True)
        p.mkdir(parents=True)
        return p

    def policy(self, agent: str, tmpdir: Path, workdir: Optional[Path] = None) -> SandboxPolicy:
        """The agent's sandbox, from its kind (A-INT-3): an auditor can never write what it reads."""
        spec = self.rt.spec(agent)
        return self.harness.rules.agent(spec.kind, spec.tools, tmpdir, self.scratch, workdir)

    # ---- units ----------------------------------------------------------------------------------
    def think(self, key: str, agent: str, variables: dict, workdir: Optional[Path] = None) -> dict:
        """A reasoning unit, or a read-only one on `workdir`. Raises UnitFailed if the agent fails
        for good."""
        kind = self.rt.spec(agent).kind
        if kind in ("coding", "writer"):
            raise TypeError(f"{agent} is a {kind} agent: run it with code(), on a version of its own")
        if kind == "readonly" and workdir is None:
            raise TypeError(f"{agent} is read-only: it needs the version it reads")
        tmp = self.tmpdir(key)
        cwd = workdir if kind == "readonly" else self.scratch
        return self.rt.run(key, agent, variables, cwd=cwd, tmpdir=tmp,
                           sandbox=self.policy(agent, tmp, workdir))

    def code(self, key: str, agent: str, variables: dict, parent: str, name: str,
             on: Optional[Workspaces] = None) -> tuple[Optional[dict], Optional[str]]:
        """A coding unit: the agent edits a fresh copy of version `parent`, which becomes `name`.

        Returns (output, None) on success, (None, error) on failure. Either way the version
        exists afterwards, holding whatever the agent left, so the harness can judge it.
        """
        kind = self.rt.spec(agent).kind
        if kind not in ("coding", "writer"):
            raise TypeError(f"{agent} is a {kind} agent: run it with think()")
        ws = on or self.ws
        record = self.rt.recorded(key, agent, variables)
        if record is not None and not ws.exists(name):
            left = ws.pending(name)
            if left is not None:
                # the unit finished and was stored, and the engine stopped before making its
                # version: make it now from what the agent left, never by calling it again
                self._seal(ws, left, key, agent, name, failed=record.get("status") != "ok")
            else:
                # the version this unit made is gone (removed by hand): its record alone cannot replay it
                log.warning("%s: version %s is missing; the unit runs again", key, name)
                self.rt.store.delete(key)
                record = None
        if record is not None:
            return (record.get("output"), None) if record.get("status") == "ok" else (None, record.get("error"))
        tmp = ws.fresh(parent, name)
        unit_tmp = self.tmpdir(key)

        def attempt(n: int) -> None:
            # every retry starts from the parent again, never from a failed attempt's edits
            if n > 1:
                ws.fresh(parent, name)
                self.tmpdir(key)

        def done(output: Optional[dict], error: Optional[str]) -> None:
            self._seal(ws, tmp, key, agent, name, failed=error is not None)

        try:
            return self.rt.run(key, agent, variables, cwd=tmp, tmpdir=unit_tmp,
                               sandbox=self.policy(agent, unit_tmp, tmp), on_done=done,
                               before_attempt=attempt), None
        except UnitFailed as e:
            if not ws.exists(name):
                self._seal(ws, tmp, key, agent, name, failed=True)
            return None, e.error

    def _seal(self, ws: Workspaces, tmp: Path, key: str, agent: str, name: str, failed: bool) -> None:
        """Make the agent's working copy version `name`, logging what the engine must not follow."""
        removed = remove_unsafe(tmp)
        if removed:
            self.event("unsafe_entries", key=key, version=name, removed=removed)
        ws.finalize(tmp, name, f"{key}: {agent}" + (" (failed)" if failed else ""))

    def evaluate(self, key: str, name: str, split: str) -> dict:
        """The harness's result for version `name` on `split`, after the deterministic checks."""
        path, commit = self.ws.path(name), self.ws.commit(name)
        reason = change_violation(self.ws, self.task, self.task_commit, name)
        if reason:
            self.event("rejected", version=name, reason=reason[:160])
            return self.harness.reject(key, path, split, reason, commit)
        return self.harness.evaluate(key, path, split, commit=commit)

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


def gain_text(new: dict, ref: dict, task: Task, min_delta: float = 0.0) -> str:
    """The gain as the critics read it, with the margin the numeric guard applies to it, so that
    the LLM gates and the guard judge noise by one threshold."""
    g = gain(new, ref)
    if g is None:
        return "not computable: at least one evaluation failed"
    sign = "an improvement" if g > 0 else ("no change" if g == 0 else "a regression")
    return (f"{g:+.6f} in {task.metric_name} ({sign}; {task.metric_info['better']}); "
            f"new mean {new['mean']:.6f} ± {new['std']:.6f} over {new['n_seeds']} seed(s), "
            f"reference mean {ref['mean']:.6f} ± {ref['std']:.6f} over {ref['n_seeds']} seed(s); "
            f"the engine counts a gain as real only above its margin of {min_delta:g}, and this one "
            f"is {'above' if g > min_delta else 'not above'} it")
