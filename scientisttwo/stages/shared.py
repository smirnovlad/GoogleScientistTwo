"""Steps more than one stage takes: the specification filter, A_FullEng with its guarded update,
and a fan-out of code variants. They live here so that no stage imports another stage."""
from __future__ import annotations

from typing import Any, Callable

from ..harness.harness import gain, strictly_better, summarize
from ..state import Core
from .common import Ctx


def spec_check(ctx: Ctx, key: str, idea: dict, ws: str) -> tuple[bool, str]:
    """The specification filter: does the solution obey the task's rules? (§4.2)"""
    if not ctx.cfg.get("integrity", {}).get("spec_filter", True):
        return True, "specification filter disabled by the profile"
    o = ctx.think(key, "spec_filter", {"task_title": ctx.task.title, "rules": ctx.task.rules_text,
                                       "idea": idea, "diff": ctx.diff(ws)}, workdir=ctx.ws.path(ws))
    if o.get("compliant"):
        return True, ""
    return False, "specification filter: " + "; ".join(
        f"{v.get('rule')}: {v.get('evidence')}" for v in o.get("violations", []))


def full_set_refine(ctx: Ctx, core: Core, feedback: str, key: str) -> Core:
    """A_FullEng (§3.4, §3.6): refine h_best and C_best from feedback, evaluate on `full`, and
    check the rules when the result would be admitted."""
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
    """The guarded update (§3.4, §3.6, A-ABL-3): strictly better on validation, within the rules."""
    return new.compliant and strictly_better(new.result, best.result, ctx.min_delta)


def run_variants(ctx: Ctx, tag: str, core: Core, items: list[dict], prefix: str, agent: str,
                 variables: Callable[[dict], dict[str, Any]]) -> list[dict]:
    """One coding unit per item, each on a copy of C_best, each scored on `full`, in parallel.

    The ablation pass (§3.4) and the rebuttal experiments (§3.5) share this shape. Each variant
    stays a version of its own, so the export can ship it beside C+ (U-ABL-3, U-PEER-2)."""
    def one(i_item: tuple[int, dict]) -> dict:
        i, item = i_item
        vid = f"{prefix}{i + 1}"
        name = f"{core.id}.{tag.replace('/', '-')}.{vid}"
        _, err = ctx.code(f"{tag}/{vid}/code", agent, variables(item), core.ws, name)
        result = ctx.evaluate(f"{tag}/{vid}/eval", name, "full")
        return {"id": vid, "item": item, "ws": name, "result": summarize(result),
                "delta_vs_full_method": gain(result, core.result), "agent_error": err}

    return ctx.map(one, list(enumerate(items)))
