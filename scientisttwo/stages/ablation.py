"""§3.4: the ablation study, and A_FullEng (docs/paper/stages/04-ablation.md).

    ablation_pass(core):  plans = ablation_planner(h_best)[:N_p]            reads C_best, read-only
                          E_abl = [harness(ablation_coder(C_best, p)) for p in plans]   in parallel
    run_stage({core, E_abl},
        critic      = ablation_critic(h_best, E_abl) → Good | Refine | Reject   (A-ABL-1: Reject, App. B)
        refine      = full_set_refine(core, feedback)                           A_FullEng
        guard       = the new full-set mean strictly beats E_best, and the spec filter passes (A-ABL-3)
        after_guard = a new ablation pass on the new h_best                     [§3.4]
        limit N_abl, keep the best; a failed guard goes on to drafting          (A-ABL-2, Figure 7)

`full_set_refine` is also §3.6's refinement: the Full-Set Engineering Agent applied to C_best.
"""
from __future__ import annotations

from typing import Optional

from ..harness.harness import gain, strictly_better, summarize
from ..primitive import ACCEPT, REFINE, REJECT, StageParams, run_stage
from ..runtime.agents import UnitFailed
from .coder import spec_check
from .common import Ctx, RunEnded
from .evolution import Core


def full_set_refine(ctx: Ctx, core: Core, feedback: str, key: str) -> Core:
    """A_FullEng: refine h_best and C_best from feedback; evaluate on `full`; check the rules."""
    t = ctx.task
    name = f"{core.id}.{key.replace('/', '-')}"
    out, err = ctx.code(f"{key}/code", "full_set_engineer", {
        "task_title": t.title, "rules": t.rules_text, "entrypoint": ctx.entrypoint_text(),
        "idea": core.idea, "feedback": feedback, "best_result": summarize(core.result)}, core.ws, name)
    idea = (out or {}).get("idea") or core.idea
    result = ctx.evaluate(f"{key}/eval", name, "full")
    compliant = True
    if result.get("status") == "ok" and strictly_better(result, core.result, ctx.min_delta):
        compliant, _ = spec_check(ctx, f"{key}/spec", idea, name)
    new = Core(core.id, idea, name, result, compliant, [*core.lineage, key])
    ctx.event("refined", key=key, gain_vs_best=gain(result, core.result), compliant=compliant,
              agent_error=err or "")
    return new


def admits(ctx: Ctx, new: Core, best: Core) -> bool:
    """The guarded update: strictly better on validation, and within the rules."""
    return new.compliant and strictly_better(new.result, best.result, ctx.min_delta)


def ablation_pass(ctx: Ctx, core: Core, tag: str) -> list[dict]:
    t = ctx.task
    n = ctx.L("n_p")
    out = ctx.think(f"{tag}/plan", "ablation_planner", {
        "task_title": t.title, "idea": core.idea, "best_result": summarize(core.result),
        "n_plans": n, "diff_summary": ctx.diff(core.ws)}, readonly=ctx.ws.path(core.ws))
    plans = out["plans"][:n]

    def run(i_plan: tuple[int, dict]) -> dict:
        i, plan = i_plan
        pid = f"A{i + 1}"
        name = f"{core.id}.{tag.replace('/', '-')}.{pid}"
        _, err = ctx.code(f"{tag}/{pid}/code", "ablation_coder", {
            "task_title": t.title, "rules": t.rules_text, "entrypoint": ctx.entrypoint_text(),
            "idea": core.idea, "plan": plan}, core.ws, name)
        result = ctx.evaluate(f"{tag}/{pid}/eval", name, "full")
        return {"id": pid, "plan": plan, "result": summarize(result),
                "delta_vs_full_method": gain(result, core.result), "agent_error": err, "ws": name}

    ablations = ctx.map(run, list(enumerate(plans)))
    ctx.event("ablation_pass", tag=tag, plans=len(ablations))
    return ablations


def ablation_stage(ctx: Ctx, core: Core, pass_i: int) -> tuple[Core, list[dict], str]:
    """Returns (core, E_abl, status). A Reject ends the run when the profile says so (App. B)."""
    t = ctx.task
    root = f"abl/p{pass_i}"
    start = {"core": core, "abl": ablation_pass(ctx, core, f"{root}/a0")}

    def critic(c: dict, i: int) -> tuple[str, str]:
        o = ctx.think(f"{root}/critic/{i}", "ablation_critic", {
            "task_title": t.title, "metric": t.metric_info, "idea": c["core"].idea,
            "best_result": summarize(c["core"].result),
            "ablations": [{k: a[k] for k in ("id", "plan", "result", "delta_vs_full_method", "agent_error")}
                          for a in c["abl"]]})
        return o["verdict"], o["feedback"]

    def refine(c: dict, feedback: str, i: int) -> dict:
        return {"core": full_set_refine(ctx, c["core"], feedback, f"{root}/refine/{i}"), "abl": c["abl"]}

    def after_guard(c: dict, i: int) -> dict:
        return {"core": c["core"], "abl": ablation_pass(ctx, c["core"], f"{root}/a{i}")}

    cfg = ctx.stage("ablation")
    try:
        outcome = run_stage(start, StageParams(
            "ablation", critic, refine, {"Good": ACCEPT, "Refine": REFINE, "Reject": REJECT},
            limit=ctx.L("n_abl"), counting=cfg.get("counting", "refinements"),
            exhaustion=cfg.get("exhaustion", "keep_best"),
            guard=lambda new, best: admits(ctx, new["core"], best["core"]), after_guard=after_guard))
    except UnitFailed as e:
        ctx.event("ablation_error", error=e.error[:200])
        return core, start["abl"], "error"
    if outcome.status == "rejected":
        if cfg.get("reject_ends_run", True):
            raise RunEnded("ablation_rejected", "the Ablation Critic attributes the gain to generic "
                           f"controls, not the idea (App. B): {outcome.last_feedback}")
        return core, start["abl"], "rejected"
    kept = outcome.candidate or start
    ctx.event("ablation", status=outcome.status, best=kept["core"].ws)
    return kept["core"], kept["abl"], outcome.status
