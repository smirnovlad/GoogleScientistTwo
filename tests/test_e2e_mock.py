"""The whole engine, end to end, for $0: the real orchestrator, harness, sandbox and stores, with
the mock backend standing in for `claude -p`. Each test drives one branch of analysis §4.3."""
import json
import time

import pytest

from conftest import params
from scientisttwo.config import apply_overrides, load_profile
from scientisttwo.orchestrator import prepare, run
from scientisttwo.runtime.backends.mock import MockBackend
from scientisttwo.runtime.store import read_json

GOOD_IDEA = {"agent": "subset_coder", "key": "^evo/r0/s1/", "edits": {"params.json": params(0.3)}}
BAD_IDEA = {"agent": "subset_coder", "key": "^evo/r0/s2/", "edits": {"params.json": params(0.9)}}
BAD_VERDICT = {"agent": "subset_critic", "key": "^evo/r0/s2/", "output": {"verdict": "Bad"}}


def profile(**overrides):
    p = load_profile("quick")
    p = apply_overrides(p, [f"{k}={json.dumps(v)}" for k, v in overrides.items()])
    p["parallel"] = 2
    return p


def go(tmp_path, toy_task, rules, prof=None, backend=None):
    backend = backend or MockBackend({"rules": rules})
    ctx = prepare(tmp_path / "run", toy_task, prof or profile(), backend, sleep=lambda s: None)
    return run(ctx), ctx, backend


def test_a_full_run_exports_a_paper_and_code(tmp_path, toy_task):
    rec, ctx, backend = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT])
    assert rec["status"] == "done", rec.get("reason")
    out = ctx.run_dir / "export"
    result = read_json(out / "results.json")
    assert result["validation"]["gain"] == pytest.approx(result["validation"]["proposed"]["mean"]
                                                         - result["validation"]["baseline"]["mean"])
    assert result["validation"]["proposed"]["mean"] == 1.0 and result["validation"]["gain"] > 0.1
    assert result["test"]["gain"] > 0.1                                  # the test split, once
    assert {i["id"]: i["verdict"] for i in result["ideas"]} == {"s1": "Good", "s2": "Bad"}
    assert (out / "code" / "params.json").read_text() == params(0.3)     # C+ is the winning code
    tex = (out / "paper" / "results.tex").read_text()
    assert "Held-out test set" in tex and "1.0000" in tex                # engine-written numbers
    assert "\\input{results}" in (out / "paper" / "main.tex").read_text()
    assert (out / "report.md").exists() and (out / "changes.patch").read_text()
    # the test split was evaluated exactly twice, at export; every decision in the loop read
    # validation splits only (U-TOP-5)
    splits = {str(f.relative_to(ctx.run_dir / "results")): read_json(f)["split"]
              for f in (ctx.run_dir / "results").rglob("*.json")}
    assert sorted(k for k, s in splits.items() if s == "test") == ["export/test/baseline.json",
                                                                  "export/test/proposed.json"]
    agents = {a for a, _ in backend.calls}
    for a in ("limitation_extractor", "limitation_verifier", "initial_idea_generator", "novelty_checker",
              "idea_generator", "baseline_coder", "subset_coder", "subset_critic", "full_set_coder",
              "full_set_critic", "spec_filter", "ablation_planner", "ablation_coder", "ablation_critic",
              "initial_drafter", "peer_reviewer", "meta_reviewer", "reference_checker",
              "method_code_auditor", "final_judge"):
        assert a in agents, a


def test_no_good_idea_ends_the_run(tmp_path, toy_task):
    rules = [{"agent": "subset_critic", "output": {"verdict": "Bad"}}]
    rec, ctx, backend = go(tmp_path, toy_task, rules)
    assert rec["status"] == "no_success"
    assert not (ctx.run_dir / "export").exists()
    assert ("idea_evolver" in {a for a, _ in backend.calls})              # K = 1: one evolution round


def test_engineering_rounds_then_success(tmp_path, toy_task):
    rules = [{"agent": "subset_coder", "key": "^evo/r0/s1/", "edits": {"run.py": "raise SystemExit(3)\n"}},
             {"agent": "subset_critic", "key": "^evo/r0/s1/subset/critic/0", "output": {"verdict": "Engineer"}},
             {"agent": "subset_engineer", "key": "^evo/r0/s1/",
              "edits": {"run.py": open(toy_task / "code" / "run.py").read(), "params.json": params(0.3)}},
             BAD_IDEA, BAD_VERDICT]
    rec, ctx, backend = go(tmp_path, toy_task, rules)
    assert rec["status"] == "done", rec.get("reason")
    first = read_json(ctx.run_dir / "results" / "evo/r0/s1/subset/eval0.json")
    assert first["status"] == "failed"                                    # the crash was judged
    assert read_json(ctx.run_dir / "export" / "results.json")["validation"]["proposed"]["mean"] == 1.0


def test_ablation_reject_ends_with_no_contribution(tmp_path, toy_task):
    rules = [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, {"agent": "ablation_critic", "output": {"verdict": "Reject"}}]
    rec, ctx, _ = go(tmp_path, toy_task, rules)
    assert rec["status"] == "ablation_rejected"


def test_meta_refinement_that_is_not_better_exports_the_previous_pass(tmp_path, toy_task):
    rules = [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, {"agent": "meta_reviewer", "output": {"decision": "Refine"}}]
    rec, ctx, backend = go(tmp_path, toy_task, rules)
    assert rec["status"] == "done"
    result = read_json(ctx.run_dir / "export" / "results.json")
    assert result["meta_accepted"] is False                               # A-TOP-3: marked, not hidden
    assert ("full_set_engineer", "meta/refine/0/code") in backend.calls
    assert not any(k.startswith("abl/p1") for _, k in backend.calls)      # guard failed: no restart


def test_a_spec_violation_makes_the_idea_bad(tmp_path, toy_task):
    rules = [GOOD_IDEA, BAD_IDEA, BAD_VERDICT,
             {"agent": "spec_filter", "key": "^evo/r0/s1/", "output": {"compliant": False,
              "violations": [{"rule": "no test data", "evidence": "run.py:1"}]}}]
    rec, ctx, _ = go(tmp_path, toy_task, rules)
    traces = {t["id"]: t for t in read_json(ctx.run_dir / "traces.json")}
    assert (traces["s1"]["verdict"], traces["s1"]["level"]) == ("Bad", "spec")
    assert "no test data" in traces["s1"]["feedback"]
    # the rounds go on (K = 1: an evolved idea and the next seed), and s1's code is never exported
    assert rec["status"] == "done", rec.get("reason")
    assert {"e1", "s3"} <= set(traces)
    assert read_json(ctx.run_dir / "export" / "results.json")["core_lineage"][0] != "selected:s1"


def test_a_paused_run_resumes_without_paying_twice(tmp_path, toy_task):
    pause = {"agent": "ablation_planner", "raise": "rate_limit"}
    backend1 = MockBackend({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, pause]})
    prof = profile()
    prof["rate_limit"]["max_wait_minutes"] = 0
    rec, ctx, _ = go(tmp_path, toy_task, None, prof, backend1)
    assert rec["status"] == "paused"
    finished = set(ctx.rt.store.keys())
    backend2 = MockBackend({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]})
    ctx2 = prepare(ctx.run_dir, None, None, backend2, sleep=lambda s: None)
    rec2 = run(ctx2)
    assert rec2["status"] == "done", rec2.get("reason")
    repaid = {k for _, k in backend2.calls} & finished
    assert repaid == set(), f"units paid twice: {sorted(repaid)[:5]}"
