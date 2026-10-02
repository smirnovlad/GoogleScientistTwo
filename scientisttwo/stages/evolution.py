"""§3.3: idea evolution and selection (docs/paper/stages/03-refining-ideas.md).

    H_0 = top N_0 seeds                                        round 0           (A-EVO-1: N_0 = 2)
    loop:
        R_k = [A_Coder(h) for h in H_k]       in parallel (U-TOP-4)          [§3.3, Eq. 3]
        traces += R_k
        stop if #Good >= S or k == K          tested at the end of a round    (U-EVO-1, A-EVO-2)
        k += 1
        H_k = idea_evolver(all traces) × N_k  +  next N_e unevaluated seeds    [§3.3]
    no Good idea → the run ends ("terminates the entire process")             [§3.3]
    selector(Good tuples) → (h_best, E_best, C_best)                          [§3.3, Eq. 4]
"""
from __future__ import annotations

from ..harness.harness import gain, summarize
from ..state import Baseline, Core, Trace
from .coder import a_coder
from .common import Ctx, RunEnded


def idea_rounds(ctx: Ctx, seeds: list[dict], base: Baseline, limitations: list[dict]) -> list[Trace]:
    used: set[str] = set()

    def next_seeds(n: int) -> list[tuple[str, dict]]:
        picks = [s for s in seeds if s["id"] not in used][:n]
        used.update(s["id"] for s in picks)
        return [(s["id"], s["idea"]) for s in picks]

    traces: list[Trace] = []
    candidates = next_seeds(ctx.L("n0"))
    k, evolved = 0, 0
    S, K = ctx.L("S"), ctx.L("K")
    while candidates:
        tag = f"r{k}"
        traces += ctx.map(lambda c: a_coder(ctx, c[0], c[1], base, tag), candidates)
        n_good = sum(t.verdict == "Good" for t in traces)
        ctx.event("round", k=k, evaluated=len(candidates), good_total=n_good)
        if n_good >= S or k >= K:
            break
        k += 1
        new: list[tuple[str, dict]] = []
        for j in range(ctx.L("n_k")):
            out = ctx.think(f"evo/r{k}/evolve/{j}", "idea_evolver", {
                "task_title": ctx.task.title, "limitations": limitations,
                "traces": [t.view() for t in traces]})
            evolved += 1
            new.append((f"e{evolved}", out["idea"]))
        candidates = new + next_seeds(ctx.L("n_e"))
    return traces


def select_best(ctx: Ctx, traces: list[Trace], base: Baseline) -> Core:
    goods = [t for t in traces if t.verdict == "Good"]
    if not goods:
        raise RunEnded("no_success", f"no idea was judged Good after {len(traces)} ideas "
                                     "(§3.3: ScientistTwo terminates the entire process)")
    if len(goods) == 1:
        # ⛔ WHY NOT call the Selector on one candidate: there is nothing to choose (our decision)
        choice, why = goods[0], "the only Good idea"
    else:
        candidates = [{"id": t.id, "idea": t.idea, "full_result": summarize(t.full or {}),
                       "gain_over_baseline": gain(t.full or {}, base.full),
                       "diff_stat": ctx.diff(t.ws, stat_only=True)} for t in goods]
        out = ctx.think("select", "selector", {"task_title": ctx.task.title,
                                               "metric": ctx.task.metric_info, "candidates": candidates})
        by_id = {t.id: t for t in goods}
        choice = by_id.get(str(out.get("choice")).strip())
        why = out.get("rationale", "")
        if choice is None:
            # an id the selector made up: fall back to the largest validated gain, and say so
            choice = max(goods, key=lambda t: gain(t.full or {}, base.full) or float("-inf"))
            why = f"the selector chose {out.get('choice')!r}, not a candidate; fell back to the largest gain"
    ctx.event("selected", id=choice.id, gain=gain(choice.full or {}, base.full), why=why[:160])
    return Core(choice.id, choice.idea, choice.ws, choice.full or {}, True, [f"selected:{choice.id}"])
