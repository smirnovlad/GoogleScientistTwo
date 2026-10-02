"""§3.1: finding limitations, then seed ideas (docs/paper/stages/01-seed-ideas.md).

Limitations, one use of the primitive:
    L = extractor(G)
    run_stage(L, critic = verifier → sufficient | insufficient,
                 refine = extractor(G, L, feedback),
                 limit = 16 critic calls (App. A.2), counting as Listing 1, keep the last set)

Seeds, a different shape (analysis §3.3): a scoring critic and a count stop.
    h0 = initial_idea_generator(G, L); score it                       # novelty_checker, 2 papers
    while |pool| < N_seed: h = idea_generator(G, L, pool); score it
    pool sorted by novelty score, descending
"""
from __future__ import annotations

from ..primitive import ACCEPT, REFINE, StageParams, run_stage
from .common import Ctx


def find_limitations(ctx: Ctx) -> list[dict]:
    t = ctx.task
    base = {"task_title": t.title, "paper": t.paper_text, "code_overview": ctx.overview,
            "rules": t.rules_text}
    first = ctx.think("lim/extract/0", "limitation_extractor",
                      {**base, "current_limitations": "none yet", "feedback": "none yet"})

    def critic(limitations: list, i: int) -> tuple[str, str]:
        out = ctx.think(f"lim/verify/{i}", "limitation_verifier",
                        {"task_title": t.title, "paper": t.paper_text, "limitations": limitations})
        return out["verdict"], out["feedback"]

    def refine(limitations: list, feedback: str, i: int) -> list:
        out = ctx.think(f"lim/extract/{i + 1}", "limitation_extractor",
                        {**base, "current_limitations": limitations, "feedback": feedback})
        return out["limitations"]

    cfg = ctx.stage("limitations")
    outcome = run_stage(first["limitations"], StageParams(
        name="limitations", critic=critic, refine=refine,
        verdict_map={"sufficient": ACCEPT, "insufficient": REFINE},
        limit=ctx.L("limitation_rounds"), counting=cfg.get("counting", "critic_calls"),
        exhaustion=cfg.get("exhaustion", "keep_last")))
    limitations = outcome.candidate if outcome.candidate is not None else first["limitations"]
    ctx.event("limitations", status=outcome.status, n=len(limitations), critic_calls=outcome.critic_calls)
    return limitations


def generate_seeds(ctx: Ctx, limitations: list[dict]) -> list[dict]:
    """The seed pool H_0, sorted by novelty score. Each seed: {id, idea, novelty}."""
    t = ctx.task
    base = {"task_title": t.title, "paper": t.paper_text, "code_overview": ctx.overview,
            "rules": t.rules_text, "limitations": limitations}
    pool: list[dict] = []
    n_seed = ctx.L("n_seed")
    for i in range(n_seed):
        if i == 0:
            idea = ctx.think("seeds/0/generate", "initial_idea_generator", base)["idea"]
        else:
            view = [{"idea": s["idea"], "novelty_score": s["novelty"]["novelty_score"]} for s in pool]
            idea = ctx.think(f"seeds/{i}/generate", "idea_generator", {**base, "pool": view})["idea"]
        novelty = ctx.think(f"seeds/{i}/novelty", "novelty_checker", {"task_title": t.title, "idea": idea})
        pool.append({"id": f"s{i + 1}", "idea": idea, "novelty": novelty, "order": i})
    pool.sort(key=lambda s: (-int(s["novelty"]["novelty_score"]), s["order"]))
    ctx.event("seeds", n=len(pool), ranking=",".join(s["id"] for s in pool))
    return pool
