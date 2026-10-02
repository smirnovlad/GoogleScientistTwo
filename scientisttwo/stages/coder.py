"""§3.2: the baseline, and the Idea Implementer A_Coder (docs/paper/stages/02-evaluating-ideas.md).

    reproduce_baseline:  version "task" (G's code) → baseline_coder → version "base"
                         E_base on subset and full, by the harness             (A-BASE-1: once)

    a_coder(h):                                                                 [§3.2, Eq. 2]
        for level in (subset, full):                                            one function, two levels
            coder(h) on a copy of the previous version; harness on the level's split
            run_stage(critic = level critic(E, E_base) → Good | Engineer | Bad,
                      refine = level engineer + harness, limit N_eng, discard)
            not Good → Trace(h, Bad), ended at this level
        filter:  spec_filter, read-only, on the diff against "base"             [§4.2]
        → Trace(h, E, C, Good | Bad, feedback)                                  [P-STATE-7]

An agent that fails for good inside A_Coder makes the idea `Bad` with the error as its feedback;
the run goes on. Only a pause (budget, usage window) or a tampered harness stops it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from ..harness.harness import gain, summarize
from ..primitive import StageOutcome, StageParams, run_stage
from ..runtime.agents import UnitFailed
from ..state import Baseline, Trace
from .common import Ctx, RunEnded
from .roles import verdict_map, verdict_of
from .shared import spec_check


def reproduce_baseline(ctx: Ctx) -> Baseline:
    t = ctx.task
    ctx.ws.init_from(t.code_dir, "task", "the task's codebase, as released")
    ctx.task_commit = ctx.ws.commit("task")
    out, err = ctx.code("base/coder", "baseline_coder",
                        {"task_title": t.title, "paper": t.paper_text, "rules": t.rules_text,
                         "entrypoint": ctx.entrypoint_text()}, parent="task", name="base")
    ctx.base_commit = ctx.ws.commit("base")
    subset = ctx.evaluate("base/eval/subset", "base", "subset")
    full = ctx.evaluate("base/eval/full", "base", "full")
    ctx.event("baseline", subset=_fmt(subset), full=_fmt(full), agent_error=err or "")
    if subset["status"] != "ok" or full["status"] != "ok":
        # U-BASE-2 (engine.md §8): no idea can be judged against a baseline that does not run
        raise RunEnded("baseline_failed", f"the reproduced baseline does not run: "
                                          f"{subset.get('error') or full.get('error')}")
    check_baseline(ctx, {"subset": subset, "full": full})
    return Baseline("base", subset, full)


def check_baseline(ctx: Ctx, results: dict) -> None:
    """U-BASE-2: the reproduced baseline must score what the task reports, within its tolerance.
    Every reported gain is measured against it, so a weaker baseline would inflate them all
    (integrity review 2026-10-02, finding 3). A better one fails too: it is not the paper's."""
    check = ctx.task.baseline_check
    if not check:
        ctx.event("baseline_unchecked", reason="the task declares no baseline_check")
        return
    r = results[check["split"]]
    off = r["mean"] - float(check["expected"])
    ctx.event("baseline_check", split=check["split"], mean=r["mean"], expected=check["expected"],
              tolerance=check["tolerance"], ok=abs(off) <= float(check["tolerance"]))
    if abs(off) > float(check["tolerance"]):
        raise RunEnded("baseline_failed",
                       f"the reproduced baseline scores {r['mean']:.4f} on {check['split']}; the task "
                       f"reports {check['expected']} ± {check['tolerance']} (U-BASE-2)")


@dataclass(frozen=True)
class Level:
    """One evaluation level of A_Coder: its split, its agents and its engineering limit."""
    split: str                 # subset | full: also the key segment and the stage's settings
    tag: str                   # version suffix: sub | full
    coder: str
    critic: str
    engineer: str
    limit: str


SUBSET = Level("subset", "sub", "subset_coder", "subset_critic", "subset_engineer", "n_eng_subset")
FULL = Level("full", "full", "full_set_coder", "full_set_critic", "full_set_engineer", "n_eng_full")


def run_level(ctx: Ctx, k: str, idea_id: str, lvl: Level, idea: dict, parent: str,
              coder_vars: Callable[[dict], dict], critic_vars: Callable[[dict], dict],
              engineer_vars: Callable[[dict, Any], dict], history: list) -> StageOutcome:
    """The level's first implementation, then its critic–engineer loop, as one primitive."""
    name = f"{idea_id}.{lvl.tag}0"
    _, err = ctx.code(f"{k}/{lvl.split}/code", lvl.coder, coder_vars(idea), parent, name)
    start = {"idea": idea, "ws": name, "agent_error": err,
             "result": ctx.evaluate(f"{k}/{lvl.split}/eval0", name, lvl.split)}

    def critic(st: dict, i: int) -> tuple[str, str]:
        o = ctx.think(f"{k}/{lvl.split}/critic/{i}", lvl.critic, critic_vars(st))
        history.append((lvl.split, i, verdict_of(lvl.critic, o), o["feedback"]))
        return verdict_of(lvl.critic, o), o["feedback"]

    def refine(st: dict, feedback: Any, i: int) -> dict:
        new = f"{idea_id}.{lvl.tag}{i + 1}"
        out, err = ctx.code(f"{k}/{lvl.split}/engineer/{i}", lvl.engineer, engineer_vars(st, feedback),
                            st["ws"], new)
        return {"idea": (out or {}).get("idea") or st["idea"], "ws": new, "agent_error": err,
                "result": ctx.evaluate(f"{k}/{lvl.split}/eval{i + 1}", new, lvl.split)}

    cfg = ctx.stage(lvl.split)
    return run_stage(start, StageParams(
        lvl.split, critic, refine, verdict_map(lvl.critic), limit=ctx.L(lvl.limit),
        counting=cfg.get("counting", "refinements"), exhaustion=cfg.get("exhaustion", "discard")))


def a_coder(ctx: Ctx, idea_id: str, idea: dict, base: Baseline, round_tag: str) -> Trace:
    k = f"evo/{round_tag}/{idea_id}"
    try:
        return _a_coder(ctx, k, idea_id, idea, base)
    except UnitFailed as e:
        ctx.event("idea_error", idea=idea_id, error=e.error[:200])
        return Trace(idea_id, idea, "Bad", "error", f"an agent failed: {e.error}", "base")


def _a_coder(ctx: Ctx, k: str, idea_id: str, idea: dict, base: Baseline) -> Trace:
    t = ctx.task
    common = {"task_title": t.title, "rules": t.rules_text, "entrypoint": ctx.entrypoint_text()}
    history: list = []

    sub = run_level(
        ctx, k, idea_id, SUBSET, idea, "base",
        coder_vars=lambda h: {**common, "idea": h},
        critic_vars=lambda st: {
            "task_title": t.title, "metric": t.metric_info, "idea": st["idea"],
            "baseline_result": summarize(base.subset), "idea_result": summarize(st["result"]),
            "gain": ctx.gain_text(st["result"], base.subset), "log_tail": _log(st),
            "diff_summary": ctx.diff(st["ws"])},
        engineer_vars=lambda st, fb: {
            **common, "idea": st["idea"], "feedback": fb, "idea_result": summarize(st["result"]),
            "log_tail": _log(st)},
        history=history)
    if sub.candidate is None:
        st = sub.last
        ctx.event("idea", id=idea_id, verdict="Bad", level="subset", gain=_g(st["result"], base.subset))
        return Trace(idea_id, st["idea"], "Bad", "subset", str(sub.last_feedback or ""), st["ws"],
                     subset=st["result"], history=history)
    subset_result = sub.candidate["result"]

    full = run_level(
        ctx, k, idea_id, FULL, sub.candidate["idea"], sub.candidate["ws"],
        coder_vars=lambda h: {**common, "idea": h, "subset_result": summarize(subset_result)},
        critic_vars=lambda st: {
            "task_title": t.title, "metric": t.metric_info, "idea": st["idea"],
            "baseline_result": summarize(base.full), "idea_result": summarize(st["result"]),
            "gain": ctx.gain_text(st["result"], base.full), "reported": t.reported,
            "log_tail": _log(st)},
        engineer_vars=lambda st, fb: {
            **common, "idea": st["idea"], "feedback": fb, "best_result": summarize(base.full)},
        history=history)
    if full.candidate is None:
        fs = full.last
        ctx.event("idea", id=idea_id, verdict="Bad", level="full", gain=_g(fs["result"], base.full))
        return Trace(idea_id, fs["idea"], "Bad", "full", str(full.last_feedback or ""), fs["ws"],
                     subset=subset_result, full=fs["result"], history=history)
    fs = full.candidate

    # ---- specification filter, §4.2: an in-run gate, read-only (A-INT-1, A-INT-3) -------------
    ok, why = spec_check(ctx, f"{k}/spec", fs["idea"], fs["ws"])
    if not ok:
        ctx.event("idea", id=idea_id, verdict="Bad", level="spec")
        return Trace(idea_id, fs["idea"], "Bad", "spec", why, fs["ws"], subset=subset_result,
                     full=fs["result"], history=history)
    ctx.event("idea", id=idea_id, verdict="Good", level="full", gain=_g(fs["result"], base.full))
    return Trace(idea_id, fs["idea"], "Good", "full", str(full.last_feedback or ""), fs["ws"],
                 subset=subset_result, full=fs["result"], history=history)


def _log(state: dict) -> str:
    parts = []
    if state.get("agent_error"):
        parts.append(f"The coding agent's session failed: {state['agent_error']}")
    parts.append(state["result"].get("log_tail") or "")
    return "\n".join(parts)


def _fmt(r: dict) -> str:
    if r.get("status") != "ok":
        return f"failed ({r.get('error')})"
    return f"{r['mean']:.4f}±{r['std']:.4f}"


def _g(new: dict, ref: dict) -> Any:
    g = gain(new, ref)
    return "n/a" if g is None else f"{g:+.4f}"
