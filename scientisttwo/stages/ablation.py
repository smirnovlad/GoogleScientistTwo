"""§3.4: the ablation study, and A_FullEng (docs/paper/stages/04-ablation.md).

    ablation_pass(core):  plans = ablation_planner(h_best)[:N_p]            reads C_best, read-only
                          E_abl = run_variants(ablation_coder, plans)       in parallel, on `full`
    run_stage({core, E_abl},
        critic      = ablation_critic(h_best, E_abl, E_base) → Good | Refine | Reject  (A-ABL-1: Reject, App. B)
                      E_base: the gain must be attributable to the mechanism (P-ABL-7, Tab. 15)
        refine      = full_set_refine(core, feedback)                           A_FullEng
        guard       = the new full-set mean strictly beats E_best, and the spec filter passes (A-ABL-3)
        after_guard = a new ablation pass on the new h_best                     [§3.4]
        limit N_abl, keep the best; a failed guard goes on to drafting          (A-ABL-2, Figure 7)

The stage returns its status; the caller decides what a `Reject` ends (meta.downstream): the run,
on the first pass; the restarted pass, on a later one.
"""
from __future__ import annotations

from ..harness.harness import summarize
from ..primitive import StageParams, run_stage
from ..runtime.agents import UnitFailed
from ..state import Baseline, Core
from .common import Ctx
from .roles import verdict_map, verdict_of
from .shared import admits, full_set_refine, run_variants


def ablation_pass(ctx: Ctx, core: Core, tag: str) -> list[dict]:
    t = ctx.task
    n = ctx.L("n_p")
    out = ctx.think(f"{tag}/plan", "ablation_planner", {
        "task_title": t.title, "idea": core.idea, "best_result": summarize(core.result),
        "n_plans": n, "diff_summary": ctx.diff(core.ws)}, workdir=ctx.ws.path(core.ws))
    plans = out["plans"][:n]
    if len(out["plans"]) != n:
        ctx.event("plan_count", key=f"{tag}/plan", asked=n, got=len(out["plans"]))
    ablations = run_variants(ctx, tag, core, plans, "A", "ablation_coder", lambda plan: {
        "task_title": t.title, "rules": t.rules_text, "entrypoint": ctx.entrypoint_text(),
        "idea": core.idea, "plan": plan})
    for a in ablations:
        a["plan"] = a.pop("item")
    ctx.event("ablation_pass", tag=tag, plans=len(ablations))
    return ablations


def ablation_stage(ctx: Ctx, base: Baseline, core: Core, pass_i: int) -> tuple[Core, list[dict], str, str]:
    """Returns (core, E_abl, status, the critic's last feedback)."""
    t = ctx.task
    root = f"abl/p{pass_i}"
    try:
        start = {"core": core, "abl": ablation_pass(ctx, core, f"{root}/a0")}
    except UnitFailed as e:
        ctx.event("ablation_error", error=e.error[:200])
        return core, [], "error", e.error

    def critic(c: dict, i: int) -> tuple[str, str]:
        o = ctx.think(f"{root}/critic/{i}", "ablation_critic", {
            "task_title": t.title, "metric": t.metric_info, "idea": c["core"].idea,
            "best_result": summarize(c["core"].result), "baseline_result": summarize(base.full),
            "gain": ctx.gain_text(c["core"].result, base.full),
            "ablations": [{k: a[k] for k in ("id", "plan", "result", "delta_vs_full_method", "agent_error")}
                          for a in c["abl"]],
            # App. B: `Reject` when a variant without the idea's own mechanism keeps more than
            # this share of the gain ("primarily driven by general training controls")
            "reject_share": float(ctx.stage("ablation").get("reject_share", 0.5))})
        return verdict_of("ablation_critic", o), o["feedback"]

    def refine(c: dict, feedback: str, i: int) -> dict:
        return {"core": full_set_refine(ctx, c["core"], feedback, f"{root}/refine/{i}"), "abl": c["abl"]}

    def after_guard(c: dict, i: int) -> dict:
        return {"core": c["core"], "abl": ablation_pass(ctx, c["core"], f"{root}/a{i}")}

    cfg = ctx.stage("ablation")
    try:
        outcome = run_stage(start, StageParams(
            "ablation", critic, refine, verdict_map("ablation_critic"),
            limit=ctx.L("n_abl"), counting=cfg.get("counting", "refinements"),
            exhaustion=cfg.get("exhaustion", "keep_best"),
            guard=lambda new, best: admits(ctx, new["core"], best["core"]), after_guard=after_guard))
    except UnitFailed as e:
        ctx.event("ablation_error", error=e.error[:200])
        return core, start["abl"], "error", e.error
    feedback = str(outcome.last_feedback or "")
    if outcome.status == "rejected":
        ctx.event("ablation", status="rejected", best=core.ws)
        return core, start["abl"], "rejected", feedback
    kept = outcome.candidate or start
    ctx.event("ablation", status=outcome.status, best=kept["core"].ws)
    return kept["core"], kept["abl"], outcome.status, feedback
