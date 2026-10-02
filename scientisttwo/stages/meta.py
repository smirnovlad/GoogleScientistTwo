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
"""
from __future__ import annotations

from ..primitive import ACCEPT, REFINE, StageParams, run_stage
from .ablation import ablation_stage, admits, full_set_refine
from .coder import Baseline
from .common import Ctx
from .evolution import Core
from .manuscript import manuscript_text
from .writing import audit, writing_stage


def downstream(ctx: Ctx, base: Baseline, core: Core, limitations: list[dict],
               references: list[dict], pass_i: int) -> dict:
    core, abl, abl_status = ablation_stage(ctx, core, pass_i)
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
    first = downstream(ctx, base, core, limitations, references, 0)

    def critic(c: dict, i: int) -> tuple[str, str]:
        o = ctx.think(f"meta/review/{i}", "meta_reviewer", {
            "manuscript": manuscript_text(ctx.papers.path(c["version"])), "review": c["review"]})
        c["meta"] = o
        return o["decision"], o["feedback"]

    def refine(c: dict, feedback: str, i: int) -> dict:
        return {**c, "core": full_set_refine(ctx, c["core"], feedback, f"meta/refine/{i}")}

    def after_guard(c: dict, i: int) -> dict:
        return downstream(ctx, base, c["core"], limitations, references, i)

    cfg = ctx.stage("meta")
    outcome = run_stage(first, StageParams(
        "meta", critic, refine, {"Accept": ACCEPT, "Refine": REFINE}, limit=ctx.L("n_meta"),
        counting=cfg.get("counting", "refinements"), exhaustion=cfg.get("exhaustion", "keep_best"),
        guard=lambda new, best: admits(ctx, new["core"], best["core"]), after_guard=after_guard))
    final = outcome.candidate or first
    final["meta_status"] = outcome.status
    final["meta_accepted"] = outcome.status == "accepted"
    ctx.event("meta", status=outcome.status, accepted=final["meta_accepted"], pass_i=final["pass"])
    return final
