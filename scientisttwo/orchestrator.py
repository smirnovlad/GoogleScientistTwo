"""The engine: (P+, C+) = A(G) [§3, Eq. 1], as analysis §4's control flow.

    L      = find_limitations(G)                    §3.1
    H_0    = generate_seeds(G, L)                   §3.1
    base   = reproduce_baseline(G)                  §3.2   (checked against the task's numbers)
    traces = idea_rounds(H_0, base)                 §3.2–3.3
    core   = select_best(traces)                    §3.3   (no Good idea → ends "no_success")
    final  = meta_stage(core)                       §3.4–3.6, §4.2
    export(final)                                   test split once, P+, C+

Every call is a unit in the run store, so `resume` re-runs this function from the top and every
finished unit returns from disk. The run ends in one status of analysis §4.3, recorded in run.json:
done | no_success | ablation_rejected | baseline_failed | paused (resumable) | error (resumable).

What a run directory holds for itself, so that it never depends on the engine's working tree:
the profile and routing (run.json), a copy of every agent's prompt and schema (agents/), and the
locked harness. A resume uses those copies, and records the engine commit and the CLI version it
ran with in run.json's history.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Optional

from .config import load_routing, validate_profile
from .harness.egress import DEFAULT_ALLOW, EgressProxy
from .harness.harness import Harness, HarnessTampered, StaleResult
from .runtime.agents import AGENTS_DIR, AgentRuntime, InputsChanged, Routing, UnitFailed, load_specs
from .runtime.backends.base import Backend
from .runtime.budget import Budget, Caps, RunPaused
from .runtime.procs import ProcRegistry
from .runtime.store import RunStore, atomic_write_json, read_json
from .stages.coder import reproduce_baseline
from .stages.common import Ctx, RunEnded
from .stages.evolution import idea_rounds, select_best
from .stages.export import export
from .stages.limitations import find_limitations, generate_seeds
from .stages.meta import meta_stage
from .stages.roles import check_roles
from .task import code_overview, load_task, read_manifest
from .workspace import Workspaces

log = logging.getLogger("scientisttwo")
ENGINE_ROOT = Path(__file__).resolve().parent.parent


class RunLocked(RuntimeError):
    pass


def engine_commit() -> str:
    try:
        r = subprocess.run(["git", "-C", str(ENGINE_ROOT), "rev-parse", "HEAD"], capture_output=True,
                           text=True, timeout=10)
        dirty = subprocess.run(["git", "-C", str(ENGINE_ROOT), "status", "--porcelain", "--", "scientisttwo"],
                               capture_output=True, text=True, timeout=10).stdout.strip()
        return r.stdout.strip() + ("+dirty" if dirty else "")
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def tree_sha256(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            h.update(str(p.relative_to(root)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def _lock(run_dir: Path) -> int:
    """One engine process per run: two resumes of one run would pay twice for the same units."""
    fd = os.open(run_dir / "run.lock", os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(fd)
        raise RunLocked(f"another engine process is running {run_dir}") from None
    os.ftruncate(fd, 0)
    os.write(fd, str(os.getpid()).encode())
    return fd


def prepare(run_dir: Path, task_path: Optional[Path], profile: Optional[dict], backend: Backend,
            allow_unsandboxed: bool = False, sleep=time.sleep, allow_changed: bool = False) -> Ctx:
    """Create a run directory, or open an existing one to resume it."""
    run_dir = Path(run_dir).expanduser().resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    lock_fd = _lock(run_dir)
    try:
        return _prepare(run_dir, task_path, profile, backend, allow_unsandboxed, sleep, allow_changed, lock_fd)
    except BaseException:
        os.close(lock_fd)
        raise


def _prepare(run_dir: Path, task_path: Optional[Path], profile: Optional[dict], backend: Backend,
             allow_unsandboxed: bool, sleep, allow_changed: bool, lock_fd: int) -> Ctx:
    manifest = run_dir / "run.json"
    agents_dir = run_dir / "agents"
    resumed = manifest.exists()
    if resumed:
        _close_crash(run_dir)                       # we hold the lock: no engine runs it now
        rec = read_json(manifest)
        task_path = Path(rec["task_path"])
        profile = rec["profile"]
        allow_unsandboxed = rec.get("allow_unsandboxed", allow_unsandboxed)
    else:
        if task_path is None or profile is None:
            raise ValueError("a new run needs a task and a profile")
        validate_profile(profile)
        source = Path(os.environ.get("SCIENTISTTWO_AGENTS_DIR") or AGENTS_DIR)
        shutil.copytree(source, agents_dir, ignore=shutil.ignore_patterns("__pycache__"),
                        dirs_exist_ok=True)
        rec = {"run_id": run_dir.name, "task_path": str(Path(task_path).resolve()), "profile": profile,
               "routing": load_routing(profile), "allow_unsandboxed": allow_unsandboxed,
               "backend": backend.describe(), "engine_commit": engine_commit(),
               "agents_sha256": tree_sha256(agents_dir), "python": sys.version.split()[0],
               "platform": platform.platform(), "created_at": time.time(), "status": "created",
               "history": []}
        atomic_write_json(manifest, rec)
    validate_profile(profile)                                         # type: ignore[arg-type]
    if agents_dir.exists():
        specs = load_specs(agents_dir)
    else:                                       # a run made before agents were copied into runs
        log.warning("this run has no copy of its agents; using the engine's current ones")
        specs = load_specs()
    check_roles(specs)
    task = load_task(task_path, manifest=_pinned_manifest(run_dir, rec, task_path, allow_changed))


    procs = ProcRegistry(run_dir)
    reaped = procs.reap_orphans(log=log.warning)
    egress = run_dir / "egress.jsonl"
    api_proxy = EgressProxy(allow=(*DEFAULT_ALLOW, *task.network_allow), log_path=egress)
    open_proxy = EgressProxy(allow=("*",), log_path=egress, ports=(80, 443))
    api_proxy.start()
    open_proxy.start()

    store = RunStore(run_dir)
    caps = Caps.from_dict(profile.get("budget", {}))                  # type: ignore[union-attr]
    budget = Budget(run_dir, caps, started_at=rec["created_at"])
    routing = Routing(rec.get("routing") or load_routing(profile))    # type: ignore[arg-type]
    retries = profile.get("retries", {})                              # type: ignore[union-attr]
    rate = profile.get("rate_limit", {})                              # type: ignore[union-attr]
    backend.attach(procs)
    rt = AgentRuntime(backend, store, budget, routing, run_dir, specs=specs,
                      retries_transient=int(retries.get("transient", 2)),
                      retries_invalid=int(retries.get("invalid_output", 1)),
                      retries_timeout=int(retries.get("timeout", 1)),
                      max_wait_minutes=float(rate.get("max_wait_minutes", 0)),
                      max_waits=int(rate.get("max_waits", 3)), sleep=sleep,
                      strict_replay=not allow_changed)
    harness = Harness(task, run_dir, allow_unsandboxed=allow_unsandboxed)
    harness.procs = procs
    harness.configure(backend_reads=tuple(backend.sandbox_reads()), api_proxy_port=api_proxy.port,
                      open_proxy_port=open_proxy.port)
    harness.install()
    ctx = Ctx(task=task, cfg=profile, rt=rt, harness=harness, ws=Workspaces(run_dir),  # type: ignore[arg-type]
              run_dir=run_dir, papers=Workspaces(run_dir, "manuscripts"),
              overview=code_overview(task.code_dir))
    ctx.services = [api_proxy, open_proxy]
    ctx.lock_fd = lock_fd
    if ctx.ws.exists("task"):
        ctx.task_commit = ctx.ws.commit("task")
    if ctx.ws.exists("base"):
        ctx.base_commit = ctx.ws.commit("base")
    described = backend.describe()
    _history(run_dir, "resumed" if resumed else "prepared", engine_commit=engine_commit(),
             cli_version=described.get("claude_version"), claude_bin=described.get("claude_bin"),
             allow_changed=allow_changed, orphans_killed=len(reaped))
    return ctx


def _pinned_manifest(run_dir: Path, rec: dict, task_path, allow_changed: bool) -> dict:
    """The task settings this run started with (seeds, timeouts, checks, deny lists). A resume
    uses them, never the task folder's current task.json, so a run never mixes evaluation
    protocols: results already on disk are replayed by key and commit, and their seeds are not
    part of either (Codex review 2026-10-02, P1). A changed manifest stops the resume unless
    `--allow-changed`, which records what changed. A run made before pinning pins at this resume."""
    current = read_manifest(task_path)
    pinned = rec.get("task_manifest")
    if pinned is not None and pinned != current:
        changed = sorted(k for k in {*pinned, *current} if pinned.get(k) != current.get(k))
        if not allow_changed:
            raise InputsChanged(f"the task's settings changed since this run started ({', '.join(changed)}). "
                                "Start a new run, or resume with --allow-changed to use the new ones.")
        log.warning("the task's settings changed (%s); --allow-changed uses the new ones", changed)
        _history(run_dir, "task_changed", keys=changed)
    if pinned != current:
        if pinned is None and rec.get("history"):
            _history(run_dir, "task_pinned", note="the run predates pinning; pinned at this resume")
        fresh = read_json(run_dir / "run.json")
        fresh["task_manifest"] = current
        atomic_write_json(run_dir / "run.json", fresh)
    return current


HEARTBEAT_S = 30.0


class Heartbeat:
    """`<run>/heartbeat` holds the last time the engine was alive, rewritten every HEARTBEAT_S
    seconds while a run runs: after a hard crash, the running time ends there, not at the resume
    (Codex review 2026-10-02, P2: a quick run stopped overnight by a crash passed its 12-hour
    cap without doing more work)."""

    def __init__(self, run_dir: Path, every: float = HEARTBEAT_S):
        self.path, self.every = run_dir / "heartbeat", every
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True, name="heartbeat")

    def start(self) -> "Heartbeat":
        self.beat()
        self._thread.start()
        return self

    def beat(self) -> None:
        atomic_write_json(self.path, {"time": time.time()})

    def _loop(self) -> None:
        while not self._stop.wait(self.every):
            self.beat()

    def stop(self) -> None:
        self._stop.set()


def _last_alive(run_dir: Path, rec: dict) -> float:
    """The last time a dead engine left a trace: its heartbeat, or a later ledger or event line."""
    times = [h["time"] for h in rec.get("history", []) if isinstance(h.get("time"), (int, float))]
    try:
        times.append(float(read_json(run_dir / "heartbeat")["time"]))
    except (OSError, ValueError, KeyError, TypeError):
        pass
    for name in ("ledger.jsonl", "events.jsonl"):
        try:
            lines = (run_dir / name).read_text().splitlines()
            if lines:
                times.append(float(json.loads(lines[-1])["time"]))
        except (OSError, ValueError, KeyError, TypeError):
            pass
    return max(times) if times else time.time()


def _close_crash(run_dir: Path) -> None:
    """A run whose status is still `running` when its lock is free was ended by a crash: close
    its running interval at its last sign of life, so the downtime is not running time."""
    rec = read_json(run_dir / "run.json")
    if rec.get("status") != "running":
        return
    at = _last_alive(run_dir, rec)
    rec["status"] = "crashed"
    rec.setdefault("history", []).append({"time": at, "status": "crashed",
                                          "note": "the engine stopped without recording a status; "
                                                  "running time ends at its last heartbeat"})
    atomic_write_json(run_dir / "run.json", rec)
    log.warning("the previous engine of this run stopped without a status: closing its running "
                "time at its last heartbeat")


def _history(run_dir: Path, what: str, **fields) -> None:
    rec = read_json(run_dir / "run.json")
    rec.setdefault("history", []).append({"time": time.time(), "event": what, **fields})
    atomic_write_json(run_dir / "run.json", rec)


def _set_status(run_dir: Path, status: str, **extra) -> dict:
    rec = read_json(run_dir / "run.json")
    rec["status"] = status
    for stale in ("reason", "resume_after", "retry_on_resume", "traceback"):
        rec.pop(stale, None)                        # the previous status's; its history keeps them
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
    return export(ctx, base, final, traces, limitations, seeds)


def run(ctx: Ctx) -> dict:
    run_dir = ctx.run_dir
    _set_status(run_dir, "running", started_at=time.time(), engine_commit=engine_commit())
    ctx.services.append(Heartbeat(run_dir).start())
    ctx.event("run", status="running", task=ctx.task.id, profile=ctx.cfg.get("name"))
    try:
        record = scientist_two(ctx)
        return _set_status(run_dir, "done", finished_at=time.time(), final=_brief(record),
                           budget=ctx.rt.budget.summary())
    except RunPaused as e:
        ctx.event("paused", reason=str(e))
        return _set_status(run_dir, "paused", reason=str(e), resume_after=e.resume_after,
                           budget=ctx.rt.budget.summary())
    except RunEnded as e:
        ctx.event("ended", status=e.status, reason=str(e))
        return _set_status(run_dir, e.status, reason=str(e), finished_at=time.time(),
                           budget=ctx.rt.budget.summary())
    except UnitFailed as e:
        # a failure no stage absorbs stops the run; the resume tries that unit again rather than
        # replaying its failure forever (architecture review 2026-10-02, finding 4)
        ctx.rt.forget(e.key)
        ctx.event("stopped", unit=e.key, error=e.error[:300])
        return _set_status(run_dir, "error", reason=f"unit {e.key} failed: {e.error[:500]}",
                           retry_on_resume=e.key, budget=ctx.rt.budget.summary())
    except (HarnessTampered, InputsChanged, StaleResult) as e:
        ctx.event("stopped", reason=f"{type(e).__name__}: {e}"[:300])
        return _set_status(run_dir, "error", reason=f"{type(e).__name__}: {e}", budget=ctx.rt.budget.summary())
    except Exception as e:                                              # noqa: BLE001 - recorded, then re-raised
        _set_status(run_dir, "error", reason=f"{type(e).__name__}: {e}",
                    traceback=traceback.format_exc()[-4000:], budget=ctx.rt.budget.summary())
        raise
    finally:
        close(ctx)


def close(ctx: Ctx) -> None:
    """Stop the run's services and release its lock."""
    for s in getattr(ctx, "services", []):
        s.stop()
    fd = getattr(ctx, "lock_fd", None)
    if fd is not None:
        try:
            os.close(fd)
        except OSError:
            pass
        ctx.lock_fd = None


def _brief(record: dict) -> dict:
    return {"idea": record["idea"].get("title"), "validation_gain": record["validation"]["gain"],
            "test_gain": record["test"]["gain"], "meta_accepted": record["meta_accepted"],
            "review_score": record["review"].get("score"),
            "final_judge": (record.get("final_judge") or {}).get("score")}
