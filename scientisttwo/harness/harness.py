"""The locked evaluation harness (CLAUDE.md: metrics come only from it; U-INT-4).

Setup, once per run: the task's `harness/` (split inputs, labels, metric) is copied into the run
and a sha256 manifest is written. Then, for every evaluation of a codebase version on a split:

  1. verify the manifest; any changed, added or removed file stops the run (`HarnessTampered`);
  2. copy the split's INPUTS (never its labels) into a fresh directory;
  3. per seed, run the task's entrypoint in the version's workspace, inside the sandbox: the
     workspace and the harness are read-only, the run's harness copy cannot even be read, only
     the evaluation directory is writable, and there is no network;
  4. score each predictions file in the ENGINE's process with the task's own `metric.score`;
  5. write one result file: per-seed scores, mean, standard deviation, status, log tail.

A crash, a timeout or a missing prediction is a `failed` result, which the critic judges; it is
never retried silently.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Optional

from ..runtime.store import atomic_write_json, read_json
from ..task import Task
from . import sandbox as sbx


class HarnessTampered(RuntimeError):
    pass


# numpy 2.2 with Apple Accelerate on M4 warns on every matmul although the results are exact
# (numpy PR #29235, fixed in 2.3.1; measured 2026-10-02). Critics would read them as overflows.
QUIET_WARNINGS = ",".join(f"ignore:{m} encountered in matmul:RuntimeWarning"
                          for m in ("divide by zero", "overflow", "invalid value"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_of(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): sha256_file(p) for p in sorted(root.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}


def tail(text: str, n: int = 3000) -> str:
    return text if len(text) <= n else "[...]\n" + text[-n:]


class Harness:
    def __init__(self, task: Task, run_dir: Path, allow_unsandboxed: bool = False,
                 python: str = sys.executable):
        self.task = task
        self.run_dir = Path(run_dir)
        self.root = self.run_dir / sbx.LOCKED_DIRNAME  # the locked copy: denied to every agent
        self.locked = self.root / "files"
        self.public = self.run_dir / "public_data"     # what training code may read
        self.results = self.run_dir / "results"
        self.allow_unsandboxed = allow_unsandboxed
        self.python = python
        self._metric = None

    # ---- setup ----------------------------------------------------------------------------------
    def install(self) -> dict[str, str]:
        """Copy the task's harness and public data into the run, once, and pin them by hash."""
        manifest_path = self.root / "manifest.json"
        if manifest_path.exists():
            self.verify()
            return read_json(manifest_path)["files"]
        if self.locked.exists():
            shutil.rmtree(self.locked)
        shutil.copytree(self.task.harness_dir, self.locked,
                        ignore=shutil.ignore_patterns("__pycache__"))
        if not self.public.exists():
            shutil.copytree(self.task.public_data_dir, self.public)
        files = manifest_of(self.locked)
        public = manifest_of(self.public)
        atomic_write_json(manifest_path, {"files": files, "public": public,
                                          "source": str(self.task.harness_dir)})
        for p in [*self.locked.rglob("*"), *self.public.rglob("*")]:
            if p.is_file():
                os.chmod(p, 0o444)
        return files

    def verify(self) -> None:
        recorded = read_json(self.root / "manifest.json")
        for label, root, files in (("harness", self.locked, recorded["files"]),
                                   ("public data", self.public, recorded.get("public", {}))):
            now = manifest_of(root)
            if now != files:
                changed = sorted(set(now.items()) ^ set(files.items()))
                raise HarnessTampered(f"{label} changed since the run started: {changed[:5]}")

    def _path(self, rel: str) -> Path:
        # task paths are relative to the task folder and start with harness/
        rel_path = Path(rel)
        parts = rel_path.parts[1:] if rel_path.parts and rel_path.parts[0] == "harness" else rel_path.parts
        return self.locked.joinpath(*parts)

    def metric(self):
        if self._metric is None:
            spec = importlib.util.spec_from_file_location("task_metric", self._path(self.task.metric_module))
            module = importlib.util.module_from_spec(spec)            # type: ignore[arg-type]
            spec.loader.exec_module(module)                           # type: ignore[union-attr]
            self._metric = module
        return self._metric

    def integrity(self) -> dict:
        """The sandbox rules every process of this run gets, agents and evaluated code alike:
        the task's own folder and its declared extra paths are unreadable, the run directory is
        never writable, and, when runs share a `runs/` folder, other runs are unreadable."""
        denied = [self.root, self.task.root, *self.task.deny_read]
        rules: dict = {"denied": denied, "protected": [self.run_dir]}
        if self.run_dir.parent.name == "runs":
            rules.update(hidden=[self.run_dir.parent], visible=[self.run_dir])
        return rules

    def reject(self, key: str, workspace: Path, split: str, reason: str, commit: str = "") -> dict:
        """A version that breaks a checkable rule is never run: its result is `failed`, with why."""
        out_file = self.results / f"{key}.json"
        if out_file.exists():
            return read_json(out_file)
        result = {"key": key, "split": split, "workspace": workspace.name, "commit": commit,
                  "status": "failed", "error": f"rejected before running: {reason}",
                  "metric": self.task.metric_name, "direction": self.task.direction,
                  "seeds": list(self.task.splits[split].seeds), "scores": [], "mean": None, "std": None,
                  "n_seeds": 0, "seconds": 0.0, "log_tail": f"The harness did not run this version: {reason}"}
        atomic_write_json(out_file, result)
        return result

    # ---- one evaluation -------------------------------------------------------------------------
    def evaluate(self, key: str, workspace: Path, split: str, commit: str = "") -> dict[str, Any]:
        """Evaluate a codebase version on a split. Memoised by `key` in results/."""
        out_file = self.results / f"{key}.json"
        if out_file.exists():
            return read_json(out_file)
        self.verify()
        s = self.task.splits[split]
        eval_dir = self.run_dir / "evals" / key
        shutil.rmtree(eval_dir, ignore_errors=True)
        eval_dir.mkdir(parents=True)
        # a neutral name: the code cannot tell which split it is labelling
        inputs = eval_dir / ("inputs" + Path(s.inputs).suffix)
        shutil.copyfile(self._path(s.inputs), inputs)
        policy = sbx.SandboxPolicy.build(writable=[eval_dir], readonly=[workspace, self.public],
                                         network=False, **self.integrity())
        scores, logs, status, error = [], [], "ok", None
        started = time.time()
        for seed in s.seeds:
            pred = eval_dir / f"pred_seed{seed}.npy"
            cmd = self.task.entrypoint.format(python=_shq(self.python), train_dir=_shq(str(self.public)),
                                              inputs=_shq(str(inputs)), out=_shq(str(pred)), seed=seed)
            rc, output, timed_out = self._run(cmd, workspace, eval_dir, policy)
            (eval_dir / f"log_seed{seed}.txt").write_text(output)
            logs.append(f"--- seed {seed} (exit {rc}{', TIMEOUT' if timed_out else ''}) ---\n{output}")
            if timed_out or rc != 0:
                status, error = "failed", (f"seed {seed}: timed out after {self.task.eval_timeout_s}s"
                                           if timed_out else f"seed {seed}: exit code {rc}")
                break
            try:
                score = self.metric().score(str(pred), str(self._path(s.labels)))
                scores.append({"seed": seed, **{k: _num(v) for k, v in score.items()}})
            except Exception as e:                                   # noqa: BLE001 - any metric error
                status, error = "failed", f"seed {seed}: scoring failed: {type(e).__name__}: {e}"
                break
        primary = [x["primary"] for x in scores if isinstance(x.get("primary"), (int, float))]
        result = {"key": key, "split": split, "workspace": workspace.name, "commit": commit,
                  "status": status, "error": error, "metric": self.task.metric_name,
                  "direction": self.task.direction, "seeds": list(s.seeds), "scores": scores,
                  "mean": _mean(primary) if status == "ok" else None,
                  "std": _std(primary) if status == "ok" else None,
                  "n_seeds": len(primary), "seconds": round(time.time() - started, 2),
                  "log_tail": tail("\n".join(logs))}
        atomic_write_json(out_file, result)
        return result

    def _run(self, cmd: str, cwd: Path, eval_dir: Path, policy: sbx.SandboxPolicy) -> tuple[int, str, bool]:
        from ..runtime.backends.claude_cli import child_env
        env = child_env(self.python)
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "MPLBACKEND": "Agg", "HOME": str(eval_dir),
                    "TMPDIR": str(eval_dir), "PYTHONWARNINGS": QUIET_WARNINGS})
        argv = sbx.wrap(["/bin/sh", "-c", cmd], policy, self.allow_unsandboxed)
        proc = subprocess.Popen(argv, cwd=str(cwd), env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, start_new_session=True)
        try:
            out, _ = proc.communicate(timeout=self.task.eval_timeout_s)
            return proc.returncode, tail(out, 20000), False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            out, _ = proc.communicate()
            return -9, tail(out or "", 20000), True


def gain(new: dict, ref: dict) -> Optional[float]:
    """Signed improvement of new over ref, in the metric's direction. None if either failed."""
    if new.get("status") != "ok" or ref.get("status") != "ok":
        return None
    d = new["mean"] - ref["mean"]
    return d if new.get("direction", "max") == "max" else -d


def strictly_better(new: dict, best: dict, min_delta: float = 0.0) -> bool:
    """The guarded update of §3.4 and §3.6, as a numeric test (A-ABL-3)."""
    g = gain(new, best)
    return g is not None and g > min_delta


def summarize(result: dict) -> dict:
    """What a critic reads: no log, numbers only."""
    keys = ("split", "status", "error", "metric", "direction", "mean", "std", "n_seeds", "scores")
    return {k: result.get(k) for k in keys}


def _shq(s: str) -> str:
    return "'" + s.replace("'", "'\"'\"'") + "'"


def _num(v: Any) -> Any:
    try:
        import numpy as np  # noqa: F401
        if hasattr(v, "item"):
            return v.item()
    except ImportError:
        pass
    return v


def _mean(xs: list[float]) -> Optional[float]:
    return sum(xs) / len(xs) if xs else None


def _std(xs: list[float]) -> Optional[float]:
    if len(xs) < 2:
        return 0.0 if xs else None
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
