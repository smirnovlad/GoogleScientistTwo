"""§3.6: the meta-review, whose refinement restarts the downstream pass
(docs/paper/stages/06-meta-review.md).

    downstream(core): ablation (§3.4) → drafting and review (§3.5) → audit (§4.2)
    run_stage(downstream(core_0),
        critic      = meta_reviewer(P_new, R_new) → Accept | Refine
        refine      = full_set_refine(h_best, C_best, r_meta)                    A_FullEng
        guard       = strictly superior on validation, and within the rules      "strictly superior"
        after_guard = downstream(new core)                                       restart, A-META-1
        limit N_meta = 1, keep the best pass)
    A failed guard exports the previous pass, which the meta-reviewer had sent back (A-TOP-3); the
    run records whether the exported manuscript was accepted.

An ablation `Reject` on the first pass ends the run (A-ABL-1, App. B). On a restarted pass it ends
only the restart: the refined core's gain is not the idea's, so the previous pass, whose ablation
the critic accepted, is exported (engine.md §8).
"""
from __future__ import annotations

from ..primitive import StageParams, run_stage
from ..state import Baseline, Core
from .ablation import ablation_stage
from .common import Ctx, RunEnded
from .manuscript import manuscript_text
from .roles import verdict_map, verdict_of
from .shared import admits, full_set_refine
from .writing import audit, writing_stage


class RestartRejected(Exception):
    """A restarted pass whose ablation the critic rejected."""


def downstream(ctx: Ctx, base: Baseline, core: Core, limitations: list[dict],
               references: list[dict], pass_i: int) -> dict:
    core, abl, abl_status, abl_feedback = ablation_stage(ctx, base, core, pass_i)
    if abl_status == "rejected" and ctx.stage("ablation").get("reject_ends_run", True):
        if pass_i == 0:
            raise RunEnded("ablation_rejected", "the Ablation Critic attributes the gain to generic "
                           f"controls, not the idea (App. B): {abl_feedback}")
        raise RestartRejected(abl_feedback)
    written = writing_stage(ctx, base, core, abl, limitations, references, pass_i)
    written, report = audit(ctx, base, core, abl, written, pass_i)
    ctx.event("downstream", pass_i=pass_i, version=written["version"],
              score=int(written["review"]["score"]))
    return {"pass": pass_i, "core": core, "ablations": abl, "ablation_status": abl_status,
            "version": written["version"], "review": written["review"],
            "rebuttals": written["rebuttals"], "review_status": written["status"], "audit": report}


def meta_stage(ctx: Ctx, base: Baseline, core: Core, limitations: list[dict],
               references: list[dict]) -> dict:
    assert ctx.papers is not None
    passes = [downstream(ctx, base, core, limitations, references, 0)]

    def critic(c: dict, i: int) -> tuple[str, str]:
        o = ctx.think(f"meta/review/{i}", "meta_reviewer", {
            "manuscript": manuscript_text(ctx.papers.path(c["version"])), "review": c["review"]})
        c["meta"] = o
        return verdict_of("meta_reviewer", o), o["feedback"]

    def refine(c: dict, feedback: str, i: int) -> dict:
        return {**c, "core": full_set_refine(ctx, c["core"], feedback, f"meta/refine/{i}")}

    def after_guard(c: dict, i: int) -> dict:
        passes.append(downstream(ctx, base, c["core"], limitations, references, i))
        return passes[-1]

    cfg = ctx.stage("meta")
    try:
        outcome = run_stage(passes[0], StageParams(
            "meta", critic, refine, verdict_map("meta_reviewer"), limit=ctx.L("n_meta"),
            counting=cfg.get("counting", "refinements"), exhaustion=cfg.get("exhaustion", "keep_best"),
            guard=lambda new, best: admits(ctx, new["core"], best["core"]), after_guard=after_guard))
        final, status = outcome.candidate or passes[0], outcome.status
    except RestartRejected as e:
        final, status = passes[-1], "restart_rejected"
        ctx.event("restart_rejected", reason=str(e)[:200], kept_pass=final["pass"])
    final["meta_status"] = status
    final["meta_accepted"] = status == "accepted"
    ctx.event("meta", status=status, accepted=final["meta_accepted"], pass_i=final["pass"])
    return final
