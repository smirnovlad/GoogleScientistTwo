"""The export: P+ ← P_new, C+ ← C_best [§3.6], and the run's verified record.

    1. the test split, ONCE, after every decision: the reproduced baseline, C_best, and each final
       ablation and supplementary variant (`export.test_variants`), so every claim the paper makes
       on validation has its held-out number too                        (U-TOP-5; CLAUDE.md)
    2. a manuscript version whose results.tex adds the test table; the test_reporter (writer) puts
       the test results into the text; the engine regenerates its own files over whatever the
       writer left                                                       (engine.md §8, U-TOP-5)
    3. the final judge, a held-out reviewer, reads it once                (never the loop's reviewer)
    4. export/: paper/ (tex, bib, pdf), code/ (C+), changes.patch, variants/ (one patch per
       ablation and supplementary experiment, against C+), results.json, audit.json, report.md
"""
from __future__ import annotations

import json
import os
import shutil
from collections import Counter
from pathlib import Path
from typing import Optional

from ..harness.harness import gain, summarize
from ..runtime.agents import UnitFailed
from ..runtime.store import atomic_write_json
from ..state import Baseline, Trace
from .common import Ctx
from .manuscript import (payload, read_regular_bytes, tables_edited, unverified_numbers,
                         write_regular, write_results)
from .writing import _refresh_results, build, read


def _variants(final: dict) -> list[dict]:
    """The final pass's ablation and supplementary variants, each with a label and its version."""
    out = [{"id": a["id"], "label": a["plan"].get("component", ""), "ws": a.get("ws"),
            "validation": a["result"]} for a in final["ablations"]]
    out += [{"id": f"S{i}", "label": r["task"].get("experiment", ""), "ws": r.get("ws"),
             "validation": r["result"]} for i, r in enumerate(final["rebuttals"], 1)]
    return [v for v in out if v["ws"]]


def export(ctx: Ctx, base: Baseline, final: dict, traces: list[Trace], limitations: list[dict],
           seeds: list[dict]) -> dict:
    assert ctx.papers is not None
    core = final["core"]
    integ = ctx.cfg.get("integrity", {})

    # ---- 1. the test split, once -----------------------------------------------------------------
    test_base = ctx.evaluate("export/test/baseline", base.ws, "test")
    test_best = ctx.evaluate("export/test/proposed", core.ws, "test")
    variants = _variants(final) if ctx.cfg.get("export", {}).get("test_variants", True) else []
    for v in variants:
        v["test"] = summarize(ctx.evaluate(f"export/test/{v['id']}", v["ws"], "test"))
    test = {"baseline": summarize(test_base), "proposed": summarize(test_best),
            "gain": gain(test_best, test_base),
            "variants": [{"id": v["id"], "label": v["label"], **v["test"]} for v in variants]}
    ctx.event("test_set", baseline=test_base.get("mean"), proposed=test_best.get("mean"), gain=test["gain"],
              variants=len(variants))

    # ---- 2. the final manuscript ---------------------------------------------------------------
    p = payload(ctx.task, base, core, final["ablations"], final["rebuttals"], test=test)
    staged = "final.results"
    if not ctx.papers.exists(staged):
        tmp = ctx.papers.fresh(final["version"], staged)
        write_results(tmp, p)
        ctx.papers.finalize(tmp, staged, "the held-out test table, added by the engine")
    written, report_error = staged, None
    if integ.get("test_report", True):
        validation = {"baseline": summarize(base.full), "proposed": summarize(core.result),
                      "gain": gain(core.result, base.full),
                      "variants": [{"id": v["id"], "label": v["label"], **v["validation"]} for v in variants]}
        _, report_error = ctx.code("export/test_report", "test_reporter", {
            "task_title": ctx.task.title, "metric": ctx.task.metric_info,
            "test_results": json.dumps(test, indent=1, default=str),
            "validation_results": json.dumps(validation, indent=1, default=str)},
            staged, "final.reported", on=ctx.papers)
        if report_error is None:
            written = "final.reported"
        else:
            ctx.event("test_report_failed", error=report_error[:200])
    edited = tables_edited(ctx.papers.path(written), p)
    name = _refresh_results(ctx, written, "final", p)    # the engine's files, over any writer's edit
    pdf = build(ctx, name, p)
    context = ctx.task.paper_text + "\n" + json.dumps(core.idea)
    checks = {"tables_edited_by_writer": edited, "test_report_error": report_error,
              "unverified_numbers": unverified_numbers(ctx.papers.path(name), p, context)}

    # ---- 3. the final judge -------------------------------------------------------------------
    judge: Optional[dict] = None
    if integ.get("final_judge", True):
        try:
            judge = ctx.think("export/final_judge", "final_judge", {"manuscript": read(ctx, name, p)})
        except UnitFailed as e:
            judge = {"error": e.error}

    # ---- 4. the files ------------------------------------------------------------------------
    out = ctx.run_dir / "export"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    ctx.papers.export(name, out / "paper")              # the committed version, no link followed
    data = read_regular_bytes(Path(pdf["pdf"])) if pdf.get("ok") else None
    if data is not None:                                # never through a link the build left
        write_regular(out / "paper" / "main.pdf", data)
    elif os.path.isdir(out / "paper" / "main.pdf") and not os.path.islink(out / "paper" / "main.pdf"):
        shutil.rmtree(out / "paper" / "main.pdf")       # a writer's own PDF is not the paper's
    elif os.path.lexists(out / "paper" / "main.pdf"):
        os.unlink(out / "paper" / "main.pdf")
    ctx.ws.export(core.ws, out / "code")
    # the whole change: ctx.diff caps what a model reads, a patch must apply (Codex review 2)
    (out / "changes.patch").write_text(ctx.ws.diff(core.ws, ctx.base_commit))
    core_commit = ctx.ws.commit(core.ws)
    if variants:
        (out / "variants").mkdir()
        for v in variants:
            (out / "variants" / f"{v['id']}.patch").write_text(ctx.ws.diff(v["ws"], core_commit))

    record = {
        "task": ctx.task.id, "metric": ctx.task.metric_info,
        "validation": {"baseline": summarize(base.full), "proposed": summarize(core.result),
                       "gain": gain(core.result, base.full)},
        "test": test, "idea": core.idea, "core_lineage": core.lineage,
        "meta_accepted": final.get("meta_accepted"), "meta_status": final.get("meta_status"),
        "meta": final.get("meta"), "review": final["review"], "ablations": final["ablations"],
        "ablation_status": final.get("ablation_status"), "rebuttals": final["rebuttals"],
        "final_judge": judge, "pdf": pdf.get("ok"), "final_checks": checks,
        "ideas": [{"id": t.id, "title": t.idea.get("title"), "verdict": t.verdict, "ended_at": t.level,
                   "full_gain": gain(t.full, base.full) if t.full else None} for t in traces],
        # after the test reporter and the final judge, so the export counts its own calls too
        "egress": egress_summary(ctx), "budget": ctx.rt.budget.summary()}
    atomic_write_json(out / "results.json", record)
    atomic_write_json(out / "audit.json", {**(final.get("audit") or {}), "final_checks": checks})
    (out / "report.md").write_text(report_md(ctx, record, limitations, final.get("audit") or {}))
    ctx.event("exported", path=str(out), pdf=pdf.get("ok"))
    return record


def egress_summary(ctx: Ctx) -> dict:
    """Which hosts the agents reached, and which they were refused (egress.jsonl)."""
    path = ctx.run_dir / "egress.jsonl"
    allowed, refused = Counter(), Counter()
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            (allowed if e.get("allowed") else refused)[str(e.get("host") or e.get("request", "?"))] += 1
    return {"allowed": dict(allowed), "refused": dict(refused)}


def _num(x: Optional[float]) -> str:
    return "n/a" if x is None else f"{x:.4f}"


def _ms(row: dict) -> str:
    if row.get("status") != "ok":
        return "failed"
    return f"{_num(row.get('mean'))} ± {_num(row.get('std'))}"


def report_md(ctx: Ctx, r: dict, limitations: list[dict], audit: dict) -> str:
    v, t = r["validation"], r["test"]
    lines = [f"# Run report: {ctx.task.title}", "",
             f"**Idea:** {r['idea'].get('title')}. {r['idea'].get('summary', '')}", "",
             "## Results (computed by the locked harness)", "",
             f"| Split | Baseline (reproduced) | Proposed | Gain ({ctx.task.metric_info['better']}) |",
             "|---|---|---|---|",
             f"| validation (`full`) | {_ms(v['baseline'])} | {_ms(v['proposed'])} | {_num(v['gain'])} |",
             f"| test, evaluated once at export | {_ms(t['baseline'])} | {_ms(t['proposed'])} | {_num(t['gain'])} |"]
    if t.get("variants"):
        lines += ["", "Ablation and supplementary variants on the test split, evaluated once at export:", "",
                  "| Variant | Test |", "|---|---|"]
        lines += [f"| {x['id']}: {x['label'][:100]} | {_ms(x)} |" for x in t["variants"]]
    judge = r.get("final_judge") or {}
    lines += ["", "## Decisions", "",
              f"- Ablation critic: {r.get('ablation_status')}.",
              f"- In-loop review score: {r['review'].get('score')} (threshold {ctx.L('review_threshold')}).",
              f"- Meta-review: {r.get('meta_status')}; it accepted the exported manuscript: {r['meta_accepted']}.",
              "- Final judge (held-out, read once): "
              + (f"{judge.get('score')} / 10, {judge.get('decision')}" if "score" in judge else str(judge or "not run"))]
    refs = Counter(e.get("status") for e in ((audit.get("references") or {}).get("entries") or []))
    mc = audit.get("method_code") or {}
    checks = r.get("final_checks") or {}
    egress = r.get("egress") or {}
    lines += ["", "## Integrity", "",
              f"- References: {dict(refs) or 'none checked'}"
              + (f"; unchecked (search failed): {', '.join(audit['unchecked'])}" if audit.get("unchecked") else ""),
              f"- Method–code audit: consistent={mc.get('consistent')}, {len(mc.get('issues') or [])} issue(s); "
              f"repaired: {audit.get('repaired')}.",
              f"- Numbers in the final text found in no result: {checks.get('unverified_numbers') or 'none'}.",
              f"- A writer edited the engine's tables: {checks.get('tables_edited_by_writer')} "
              "(readers always get them regenerated from the result files).",
              f"- Network: agents reached {sorted(egress.get('allowed', {}))}; refused "
              f"{sum(egress.get('refused', {}).values())} request(s) to {sorted(egress.get('refused', {}))}."]
    lines += ["", "## Ideas tried", "", "| Idea | Verdict | Ended at | Gain on `full` |", "|---|---|---|---|"]
    for i in r["ideas"]:
        lines.append(f"| {i['id']}: {i['title']} | {i['verdict']} | {i['ended_at']} | {_num(i['full_gain'])} |")
    lines += ["", f"## Limitations found ({len(limitations)})", ""]
    lines += [f"- **{l.get('id')}** {l.get('title')}" for l in limitations]
    b = r["budget"]
    lines += ["", "## Cost", "",
              f"- {b['agent_calls']} agent calls (every attempt counts), {b['coding_sessions']} of them "
              f"sessions with tools; {b['agent_seconds']} s of agent time; {b.get('running_hours')} h running.",
              f"- API-equivalent cost reported by the CLI: ${b['equiv_usd']} "
              f"({b['unknown_cost_calls']} calls with unknown cost). On the subscription, nothing is billed per call.",
              "", "Files: `paper/` (P+), `code/` (C+), `changes.patch`, `variants/`, `results.json`, "
              "`audit.json`."]
    return "\n".join(lines) + "\n"
