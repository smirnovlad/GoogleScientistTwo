"""§3.2: the baseline, and the Idea Implementer A_Coder (docs/paper/stages/02-evaluating-ideas.md).

    reproduce_baseline:  version "task" (G's code) → baseline_coder → version "base"
                         E_base on subset and full, by the harness             (A-BASE-1: once)

    a_coder(h):                                                                 [§3.2, Eq. 2]
        subset:  subset_coder(h) on a copy of "base"; harness on subset
                 run_stage(critic = subset_critic(E, E_base) → Good | Engineer | Bad,
                           refine = subset_engineer + harness, limit N_eng, discard)
        full:    full_set_coder on a copy of the subset version; harness on full
                 run_stage(critic = full_set_critic(E, E_base_full, reported) …,
                           refine = full_set_engineer + harness, limit N_eng_full, discard)
        filter:  spec_filter, read-only, on the diff against "base"             [§4.2]
        → Trace(h, E, C, Good | Bad, feedback)                                  [P-STATE-7]

An agent that fails for good inside A_Coder makes the idea `Bad` with the error as its feedback;
the run goes on. Only a pause (budget, usage window) or a tampered harness stops it.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from ..harness.harness import gain, summarize
from ..primitive import ACCEPT, REFINE, REJECT, StageParams, run_stage
from ..runtime.agents import UnitFailed
from .common import Ctx, RunEnded, gain_text

VERDICTS = {"Good": ACCEPT, "Engineer": REFINE, "Bad": REJECT}


@dataclass
class Baseline:
    ws: str
    subset: dict
    full: dict


@dataclass
class Trace:
    id: str
    idea: dict
    verdict: str                      # Good | Bad
    level: str                        # where it ended: subset | full | spec | error
    feedback: str
    ws: str
    subset: Optional[dict] = None
    full: Optional[dict] = None
    history: list = field(default_factory=list)

    def view(self) -> dict:
        """What the Idea Evolver and the Selector read (P-STATE-7)."""
        last = self.full or self.subset or {}
        v = {"id": self.id, "idea": self.idea, "verdict": self.verdict, "ended_at": self.level,
             "feedback": self.feedback,
             "subset_result": summarize(self.subset) if self.subset else None,
             "full_result": summarize(self.full) if self.full else None}
        if self.verdict == "Bad" and last.get("log_tail"):
            v["diagnostic_log_tail"] = last["log_tail"][-2000:]
        return v

    def to_dict(self) -> dict:
        return asdict(self)


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
        raise RunEnded("baseline_failed", f"the reproduced baseline does not run: "
                                          f"{subset.get('error') or full.get('error')}")
    return Baseline("base", subset, full)


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

    # ---- subset level -------------------------------------------------------------------------
    name = f"{idea_id}.sub0"
    _, err = ctx.code(f"{k}/subset/code", "subset_coder", {**common, "idea": idea}, "base", name)
    state = {"idea": idea, "ws": name, "result": ctx.evaluate(f"{k}/subset/eval0", name, "subset"),
             "agent_error": err}
    last = {"state": state}

    def sub_critic(st: dict, i: int) -> tuple[str, str]:
        o = ctx.think(f"{k}/subset/critic/{i}", "subset_critic", {
            "task_title": t.title, "metric": t.metric_info, "idea": st["idea"],
            "baseline_result": summarize(base.subset), "idea_result": summarize(st["result"]),
            "gain": gain_text(st["result"], base.subset, t), "log_tail": _log(st),
            "diff_summary": ctx.diff(st["ws"])})
        history.append(("subset", i, o["verdict"], o["feedback"]))
        return o["verdict"], o["feedback"]

    def sub_refine(st: dict, feedback: str, i: int) -> dict:
        new = f"{idea_id}.sub{i + 1}"
        out, err = ctx.code(f"{k}/subset/engineer/{i}", "subset_engineer", {
            **common, "idea": st["idea"], "feedback": feedback,
            "idea_result": summarize(st["result"]), "log_tail": _log(st)}, st["ws"], new)
        revised = out.get("idea") if out else None
        nxt = {"idea": revised or st["idea"], "ws": new, "agent_error": err,
               "result": ctx.evaluate(f"{k}/subset/eval{i + 1}", new, "subset")}
        last["state"] = nxt
        return nxt

    sub_cfg = ctx.stage("subset")
    outcome = run_stage(state, StageParams(
        "subset", sub_critic, sub_refine, VERDICTS, limit=ctx.L("n_eng_subset"),
        counting=sub_cfg.get("counting", "refinements"), exhaustion=sub_cfg.get("exhaustion", "discard")))
    st = last["state"]
    if outcome.status != "accepted":
        ctx.event("idea", id=idea_id, verdict="Bad", level="subset", gain=_g(st["result"], base.subset))
        return Trace(idea_id, st["idea"], "Bad", "subset", str(outcome.last_feedback or ""), st["ws"],
                     subset=st["result"], history=history)
    subset_result = outcome.candidate["result"]
    st = outcome.candidate

    # ---- full level ---------------------------------------------------------------------------
    name = f"{idea_id}.full0"
    _, err = ctx.code(f"{k}/full/code", "full_set_coder", {
        **common, "idea": st["idea"], "subset_result": summarize(subset_result)}, st["ws"], name)
    fstate = {"idea": st["idea"], "ws": name, "result": ctx.evaluate(f"{k}/full/eval0", name, "full"),
              "agent_error": err}
    flast = {"state": fstate}

    def full_critic(s: dict, i: int) -> tuple[str, str]:
        o = ctx.think(f"{k}/full/critic/{i}", "full_set_critic", {
            "task_title": t.title, "metric": t.metric_info, "idea": s["idea"],
            "baseline_result": summarize(base.full), "idea_result": summarize(s["result"]),
            "gain": gain_text(s["result"], base.full, t), "reported": t.reported, "log_tail": _log(s)})
        history.append(("full", i, o["verdict"], o["feedback"]))
        return o["verdict"], o["feedback"]

    def full_refine(s: dict, feedback: str, i: int) -> dict:
        new = f"{idea_id}.full{i + 1}"
        out, err = ctx.code(f"{k}/full/engineer/{i}", "full_set_engineer", {
            **common, "idea": s["idea"], "feedback": feedback,
            "best_result": summarize(base.full)}, s["ws"], new)
        nxt = {"idea": (out or {}).get("idea") or s["idea"], "ws": new, "agent_error": err,
               "result": ctx.evaluate(f"{k}/full/eval{i + 1}", new, "full")}
        flast["state"] = nxt
        return nxt

    full_cfg = ctx.stage("full")
    outcome = run_stage(fstate, StageParams(
        "full", full_critic, full_refine, VERDICTS, limit=ctx.L("n_eng_full"),
        counting=full_cfg.get("counting", "refinements"), exhaustion=full_cfg.get("exhaustion", "discard")))
    fs = flast["state"]
    if outcome.status != "accepted":
        ctx.event("idea", id=idea_id, verdict="Bad", level="full", gain=_g(fs["result"], base.full))
        return Trace(idea_id, fs["idea"], "Bad", "full", str(outcome.last_feedback or ""), fs["ws"],
                     subset=subset_result, full=fs["result"], history=history)
    fs = outcome.candidate

    # ---- specification filter, §4.2: an in-run gate, read-only (A-INT-1, A-INT-3) -------------
    ok, why = spec_check(ctx, f"{k}/spec", fs["idea"], fs["ws"])
    if not ok:
        ctx.event("idea", id=idea_id, verdict="Bad", level="spec")
        return Trace(idea_id, fs["idea"], "Bad", "spec", why, fs["ws"], subset=subset_result,
                     full=fs["result"], history=history)
    ctx.event("idea", id=idea_id, verdict="Good", level="full", gain=_g(fs["result"], base.full))
    return Trace(idea_id, fs["idea"], "Good", "full", str(outcome.last_feedback or ""), fs["ws"],
                 subset=subset_result, full=fs["result"], history=history)


def spec_check(ctx: Ctx, key: str, idea: dict, ws: str) -> tuple[bool, str]:
    """The specification filter: does the solution obey the task's rules? (§4.2)"""
    if not ctx.cfg.get("integrity", {}).get("spec_filter", True):
        return True, "specification filter disabled by the profile"
    o = ctx.think(key, "spec_filter", {"task_title": ctx.task.title, "rules": ctx.task.rules_text,
                                       "idea": idea, "diff": ctx.diff(ws)}, readonly=ctx.ws.path(ws))
    if o.get("compliant"):
        return True, ""
    return False, "specification filter: " + "; ".join(
        f"{v.get('rule')}: {v.get('evidence')}" for v in o.get("violations", []))


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
