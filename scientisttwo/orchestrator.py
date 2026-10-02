"""The engine: (P+, C+) = A(G) [§3, Eq. 1], as analysis §4's control flow.

    L      = find_limitations(G)                    §3.1
    H_0    = generate_seeds(G, L)                   §3.1
    base   = reproduce_baseline(G)                  §3.2
    traces = idea_rounds(H_0, base)                 §3.2–3.3
    core   = select_best(traces)                    §3.3   (no Good idea → ends "no_success")
    final  = meta_stage(core)                       §3.4–3.6, §4.2
    export(final)                                   test split once, P+, C+

Every call is a unit in the run store, so `resume` re-runs this function from the top and every
finished unit returns from disk. The run ends in one status of analysis §4.3, recorded in run.json:
done | no_success | ablation_rejected | baseline_failed | paused (resumable) | error.
"""
from __future__ import annotations

import json
import logging
import platform
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Optional

from .config import load_routing
from .harness.harness import Harness, HarnessTampered
from .runtime.agents import AgentRuntime, Routing, load_specs
from .runtime.backends.base import Backend
from .runtime.budget import Budget, BudgetExceeded, Caps
from .runtime.store import RunStore, atomic_write_json, read_json
from .stages.coder import reproduce_baseline
from .stages.common import Ctx, RunEnded
from .stages.evolution import idea_rounds, select_best
from .stages.export import export
from .stages.limitations import find_limitations, generate_seeds
from .stages.meta import meta_stage
from .task import code_overview, load_task
from .workspace import Workspaces

log = logging.getLogger("scientisttwo")
ENGINE_ROOT = Path(__file__).resolve().parent.parent


def engine_commit() -> str:
    try:
        r = subprocess.run(["git", "-C", str(ENGINE_ROOT), "rev-parse", "HEAD"], capture_output=True,
                           text=True, timeout=10)
        dirty = subprocess.run(["git", "-C", str(ENGINE_ROOT), "status", "--porcelain", "--", "scientisttwo"],
                               capture_output=True, text=True, timeout=10).stdout.strip()
        return r.stdout.strip() + ("+dirty" if dirty else "")
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def prepare(run_dir: Path, task_path: Optional[Path], profile: Optional[dict], backend: Backend,
            allow_unsandboxed: bool = False, sleep=time.sleep) -> Ctx:
    """Create a run directory, or open an existing one to resume it."""
    run_dir = Path(run_dir).expanduser().resolve()
    manifest = run_dir / "run.json"
    if manifest.exists():
        rec = read_json(manifest)
        task_path = Path(rec["task_path"])
        profile = rec["profile"]
        allow_unsandboxed = rec.get("allow_unsandboxed", allow_unsandboxed)
    else:
        if task_path is None or profile is None:
            raise ValueError("a new run needs a task and a profile")
        run_dir.mkdir(parents=True, exist_ok=True)
        rec = {"run_id": run_dir.name, "task_path": str(Path(task_path).resolve()), "profile": profile,
               "routing": load_routing(profile), "allow_unsandboxed": allow_unsandboxed,
               "backend": backend.describe(), "engine_commit": engine_commit(),
               "python": sys.version.split()[0], "platform": platform.platform(),
               "created_at": time.time(), "status": "created", "history": []}
        atomic_write_json(manifest, rec)
    task = load_task(task_path)                                       # type: ignore[arg-type]
    store = RunStore(run_dir)
    caps = Caps.from_dict(profile.get("budget", {}))                  # type: ignore[union-attr]
    budget = Budget(run_dir, caps, started_at=rec["created_at"])
    routing = Routing(rec.get("routing") or load_routing(profile))    # type: ignore[arg-type]
    rt = AgentRuntime(backend, store, budget, routing, run_dir, specs=load_specs(),
                      retries_transient=int(profile.get("retries", {}).get("transient", 2)),
                      retries_invalid=int(profile.get("retries", {}).get("invalid_output", 1)),
                      max_wait_minutes=float(profile.get("rate_limit", {}).get("max_wait_minutes", 0)),
                      sleep=sleep)
    harness = Harness(task, run_dir, allow_unsandboxed=allow_unsandboxed)
    harness.install()
    ctx = Ctx(task=task, cfg=profile, rt=rt, harness=harness, ws=Workspaces(run_dir),
              run_dir=run_dir, papers=Workspaces(run_dir, "manuscripts"),
              overview=code_overview(task.code_dir))                  # type: ignore[arg-type]
    if ctx.ws.exists("task"):
        ctx.task_commit = ctx.ws.commit("task")
    if ctx.ws.exists("base"):
        ctx.base_commit = ctx.ws.commit("base")
    return ctx


def _set_status(run_dir: Path, status: str, **extra) -> dict:
    rec = read_json(run_dir / "run.json")
    rec["status"] = status
    rec.update(extra)
    rec.setdefault("history", []).append({"time": time.time(), "status": status,
                                          **{k: v for k, v in extra.items() if isinstance(v, (str, int, float))}})
    atomic_write_json(run_dir / "run.json", rec)
    return rec


def scientist_two(ctx: Ctx) -> dict:
    limitations = find_limitations(ctx)
    seeds = generate_seeds(ctx, limitations)
    base = reproduce_baseline(ctx)
    traces = idea_rounds(ctx, seeds, base, limitations)
    atomic_write_json(ctx.run_dir / "traces.json", [t.to_dict() for t in traces])
    core = select_best(ctx, traces, base)
    references = [r for s in seeds for r in s["novelty"].get("references", [])]
    final = meta_stage(ctx, base, core, limitations, references)
    return export(ctx, base, final, traces, limitations, seeds, ctx.rt.budget.summary())


def run(ctx: Ctx) -> dict:
    run_dir = ctx.run_dir
    _set_status(run_dir, "running", started_at=time.time())
    ctx.event("run", status="running", task=ctx.task.id, profile=ctx.cfg.get("name"))
    try:
        record = scientist_two(ctx)
        return _set_status(run_dir, "done", finished_at=time.time(), final=_brief(record),
                           budget=ctx.rt.budget.summary())
    except BudgetExceeded as e:
        ctx.event("paused", reason=str(e))
        return _set_status(run_dir, "paused", reason=str(e), resume_after=e.resume_after,
                           budget=ctx.rt.budget.summary())
    except RunEnded as e:
        ctx.event("ended", status=e.status, reason=str(e))
        return _set_status(run_dir, e.status, reason=str(e), finished_at=time.time(),
                           budget=ctx.rt.budget.summary())
    except HarnessTampered as e:
        ctx.event("tampered", reason=str(e))
        return _set_status(run_dir, "error", reason=f"harness tampered: {e}", budget=ctx.rt.budget.summary())
    except Exception as e:                                              # noqa: BLE001 - recorded, then re-raised
        _set_status(run_dir, "error", reason=f"{type(e).__name__}: {e}",
                    traceback=traceback.format_exc()[-4000:], budget=ctx.rt.budget.summary())
        raise


def _brief(record: dict) -> dict:
    return {"idea": record["idea"].get("title"), "validation_gain": record["validation"]["gain"],
            "test_gain": record["test"]["gain"], "meta_accepted": record["meta_accepted"],
            "review_score": record["review"].get("score"),
            "final_judge": (record.get("final_judge") or {}).get("score")}
