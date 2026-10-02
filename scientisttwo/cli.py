"""python -m scientisttwo run | resume | status | agents

    run     --task tasks/digits [--profile quick|paper|file.json] [--run-dir runs/<id>]
            [--backend claude|mock] [--mock-script rules.json] [--set limits.K=2 ...]
            [--parallel N] [--allow-unsandboxed] [--wait [--max-wait-hours H]]
    resume  <run-dir> [--allow-changed] [--wait [--max-wait-hours H]]
                             continue a paused or crashed run; finished units are not re-run.
                             A unit whose inputs changed since it ran (new prompts, new engine
                             code) stops the resume, unless --allow-changed replays it as recorded.
            --wait           when the run pauses on a subscription usage window, sleep until the
                             window resets and go on, until the run ends; a pause with no known
                             reset, or one further away than --max-wait-hours (24), still stops.
    status  <run-dir>        the run's status, budget and last events
    agents                   list the agents, their kind, model and paper reference

The default backend is `claude`: `claude -p` on the logged-in subscription, never the API.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

from .config import apply_overrides, load_profile, load_routing
from .orchestrator import prepare, run
from .runtime.agents import InputsChanged, Routing, load_specs
from .runtime.backends import BACKENDS, make_backend
from .runtime.store import read_json


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m scientisttwo", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="start a run")
    r.add_argument("--task", required=True)
    r.add_argument("--profile", default="quick")
    r.add_argument("--run-dir")
    r.add_argument("--backend", choices=BACKENDS, default="claude")
    r.add_argument("--mock-script")
    r.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    r.add_argument("--parallel", type=int)
    r.add_argument("--allow-unsandboxed", action="store_true")
    s = sub.add_parser("resume", help="continue a run")
    s.add_argument("run_dir")
    s.add_argument("--backend", choices=BACKENDS)
    s.add_argument("--mock-script")
    s.add_argument("--allow-changed", action="store_true")
    for p in (r, s):
        p.add_argument("--wait", action="store_true", help="sleep through usage-window pauses")
        p.add_argument("--max-wait-hours", type=float, default=24.0)
    st = sub.add_parser("status", help="show a run's status")
    st.add_argument("run_dir")
    sub.add_parser("agents", help="list the agents")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")

    if a.cmd == "agents":
        routing = Routing(load_routing(load_profile("paper")))
        for spec in load_specs().values():
            route = routing.route(spec)
            print(f"{spec.name:24s} {spec.kind:9s} {route.model:7s} {spec.paper_ref}")
        return 0
    if a.cmd == "status":
        rec = read_json(Path(a.run_dir) / "run.json")
        print(json.dumps({k: rec.get(k) for k in ("run_id", "status", "reason", "resume_after", "final", "budget")},
                         indent=1, default=str))
        events = Path(a.run_dir) / "events.jsonl"
        if events.exists():
            for line in events.read_text().splitlines()[-12:]:
                print(line)
        return 0
    if a.cmd == "run":
        profile = apply_overrides(load_profile(a.profile), a.set)
        if a.parallel:
            profile["parallel"] = a.parallel
        run_dir = Path(a.run_dir or f"runs/{Path(a.task).name}-{time.strftime('%Y%m%d-%H%M%S')}")
        backend = make_backend(a.backend, allow_unsandboxed=a.allow_unsandboxed, mock_script=a.mock_script)
        ctx = prepare(run_dir, Path(a.task), profile, backend, a.allow_unsandboxed)
    else:
        rec = read_json(Path(a.run_dir) / "run.json")
        recorded = rec.get("backend", {})
        name = a.backend or recorded.get("backend", "claude")
        backend = make_backend(name, allow_unsandboxed=rec.get("allow_unsandboxed", False),
                               mock_script=a.mock_script, claude_bin=recorded.get("claude_bin"))
        try:
            ctx = prepare(Path(a.run_dir), None, None, backend, allow_changed=a.allow_changed)
        except InputsChanged as e:
            print(f"not resumed: {e}", file=sys.stderr)
            return 1
    print(f"run directory: {ctx.run_dir}", file=sys.stderr)
    rec = run(ctx)
    if a.wait:
        allow = bool(getattr(a, "allow_changed", False))
        rec = wait_and_resume(rec, lambda: run(prepare(ctx.run_dir, None, None, backend, allow_changed=allow)),
                              a.max_wait_hours)
    print(json.dumps({k: rec.get(k) for k in ("status", "reason", "resume_after", "final")}, indent=1, default=str))
    return 0 if rec["status"] in ("done", "no_success", "ablation_rejected") else (3 if rec["status"] == "paused" else 1)


RESUME_MARGIN_S = 120.0       # after a window's reset, before the next call
_sleep = time.sleep


def wait_and_resume(rec: dict, resume, max_wait_hours: float, sleep=None) -> dict:
    """While the run is paused on a usage window with a known reset, sleep until it and resume.
    The subscription's windows make a long run pause every few hours; without this, each pause
    waits for a person. ⛔ WHY NOT wait on any pause: a cap or a persisting error needs a person."""
    while rec.get("status") == "paused":
        reset = rec.get("resume_after")
        wait = None if not reset else max(60.0, float(reset) - time.time() + RESUME_MARGIN_S)
        if wait is None or wait > max_wait_hours * 3600:
            why = "it has no known reset time" if wait is None else f"its reset is {wait / 3600:.1f} h away"
            print(f"paused, and not waiting: {why} ({rec.get('reason')})", file=sys.stderr)
            return rec
        print(f"paused ({rec.get('reason')}); resuming at "
              f"{time.strftime('%H:%M', time.localtime(time.time() + wait))}", file=sys.stderr)
        (sleep or _sleep)(wait)
        rec = resume()
    return rec


if __name__ == "__main__":
    sys.exit(main())
