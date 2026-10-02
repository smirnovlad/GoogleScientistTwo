"""The export: P+ ← P_new, C+ ← C_best [§3.6], and the run's verified record.

    1. the test split, ONCE: the reproduced baseline and C_best              (U-TOP-5; CLAUDE.md)
    2. a final manuscript version whose results.tex adds the held-out test table
    3. the final judge, a held-out reviewer, reads it once                   (never the loop's reviewer)
    4. export/: paper/ (tex, bib, pdf), code/ (C+), changes.patch, results.json, audit.json, report.md
"""
from __future__ import annotations

import json
import shutil
from typing import Optional

from ..harness.harness import gain, summarize
from ..runtime.agents import UnitFailed
from ..runtime.store import atomic_write_json
from .coder import Baseline, Trace
from .common import Ctx
from .manuscript import manuscript_text, payload, write_results
from .writing import build


def export(ctx: Ctx, base: Baseline, final: dict, traces: list[Trace], limitations: list[dict],
           seeds: list[dict], budget_summary: dict) -> dict:
    assert ctx.papers is not None
    core = final["core"]
    test_base = ctx.evaluate("export/test/baseline", base.ws, "test")
    test_best = ctx.evaluate("export/test/proposed", core.ws, "test")
    test = {"baseline": summarize(test_base), "proposed": summarize(test_best),
            "gain": gain(test_best, test_base)}
    ctx.event("test_set", baseline=test_base.get("mean"), proposed=test_best.get("mean"), gain=test["gain"])

    p = payload(ctx.task, base, core, final["ablations"], final["rebuttals"], test=test)
    name = "final"
    if not ctx.papers.exists(name):
        tmp = ctx.papers.fresh(final["version"], name)
        write_results(tmp, p)
        ctx.papers.finalize(tmp, name, "final: the held-out test table added by the engine")
    pdf = build(ctx, name)

    judge: Optional[dict] = None
    if ctx.cfg.get("integrity", {}).get("final_judge", True):
        try:
            judge = ctx.think("export/final_judge", "final_judge",
                              {"manuscript": manuscript_text(ctx.papers.path(name))})
        except UnitFailed as e:
            judge = {"error": e.error}

    out = ctx.run_dir / "export"
    if out.exists():
        shutil.rmtree(out)
    (out / "paper").mkdir(parents=True)
    paper_dir = ctx.papers.path(name)
    for f in paper_dir.iterdir():
        if f.is_file() and f.name != ".gitignore":
            shutil.copy2(f, out / "paper" / f.name)
    if pdf.get("ok"):
        shutil.copy2(pdf["pdf"], out / "paper" / "main.pdf")
    ctx.ws.export(core.ws, out / "code")
    (out / "changes.patch").write_text(ctx.diff(core.ws))

    record = {
        "task": ctx.task.id, "metric": ctx.task.metric_info,
        "validation": {"baseline": summarize(base.full), "proposed": summarize(core.result),
                       "gain": gain(core.result, base.full)},
        "test": test, "idea": core.idea, "core_lineage": core.lineage,
        "meta_accepted": final.get("meta_accepted"), "meta": final.get("meta"),
        "review": final["review"], "ablations": final["ablations"], "rebuttals": final["rebuttals"],
        "final_judge": judge, "pdf": pdf.get("ok"),
        "ideas": [{"id": t.id, "title": t.idea.get("title"), "verdict": t.verdict, "ended_at": t.level,
                   "full_gain": gain(t.full, base.full) if t.full else None} for t in traces],
        "budget": budget_summary}
    atomic_write_json(out / "results.json", record)
    atomic_write_json(out / "audit.json", final.get("audit") or {})
    (out / "report.md").write_text(report_md(ctx, record, limitations, seeds))
    ctx.event("exported", path=str(out), pdf=pdf.get("ok"))
    return record


def _num(x: Optional[float]) -> str:
    return "n/a" if x is None else f"{x:.4f}"


def report_md(ctx: Ctx, r: dict, limitations: list[dict], seeds: list[dict]) -> str:
    v, t = r["validation"], r["test"]
    lines = [f"# Run report: {ctx.task.title}", "",
             f"**Idea:** {r['idea'].get('title')}. {r['idea'].get('summary', '')}", "",
             "## Results (computed by the locked harness)", "",
             f"| Split | Baseline (reproduced) | Proposed | Gain ({ctx.task.metric_info['better']}) |",
             "|---|---|---|---|",
             f"| validation (`full`) | {_num(v['baseline'].get('mean'))} ± {_num(v['baseline'].get('std'))} "
             f"| {_num(v['proposed'].get('mean'))} ± {_num(v['proposed'].get('std'))} | {_num(v['gain'])} |",
             f"| test, evaluated once at export | {_num(t['baseline'].get('mean'))} ± {_num(t['baseline'].get('std'))} "
             f"| {_num(t['proposed'].get('mean'))} ± {_num(t['proposed'].get('std'))} | {_num(t['gain'])} |",
             "", "## Decisions", "",
             f"- In-loop review score: {r['review'].get('score')} (threshold {ctx.L('review_threshold')}).",
             f"- Meta-review accepted the exported manuscript: {r['meta_accepted']}.",
             f"- Final judge (held-out, read once): "
             + (f"{r['final_judge'].get('score')} / 10, {r['final_judge'].get('decision')}"
                if r.get("final_judge") and "score" in r["final_judge"] else str(r.get("final_judge"))),
             "", "## Ideas tried", "", "| Idea | Verdict | Ended at | Gain on `full` |", "|---|---|---|---|"]
    for i in r["ideas"]:
        lines.append(f"| {i['id']}: {i['title']} | {i['verdict']} | {i['ended_at']} | {_num(i['full_gain'])} |")
    lines += ["", f"## Limitations found ({len(limitations)})", ""]
    lines += [f"- **{l.get('id')}** {l.get('title')}" for l in limitations]
    b = r["budget"]
    lines += ["", "## Cost", "",
              f"- {b['agent_calls']} agent calls, {b['coding_sessions']} of them sessions with tools; "
              f"{b['agent_seconds']} s of agent time; {b['wall_hours']} h wall-clock.",
              f"- API-equivalent cost reported by the CLI: ${b['equiv_usd']} "
              f"({b['unknown_cost_calls']} calls with unknown cost). On the subscription, nothing is billed per call.",
              "", "Files: `paper/` (P+), `code/` (C+), `changes.patch`, `results.json`, `audit.json`."]
    return "\n".join(lines) + "\n"
