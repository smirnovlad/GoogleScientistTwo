"""The whole engine, end to end, for $0: the real orchestrator, harness, sandbox and stores, with
the mock backend standing in for `claude -p`. Each test drives one branch of analysis §4.3."""
import json
import time

import pytest

from conftest import params
from scientisttwo.config import apply_overrides, load_profile
from scientisttwo.orchestrator import RunLocked, close, prepare, run
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
    # the test split was evaluated only at export, once per version: the baseline, the proposed
    # method and each final variant; every decision in the loop read validation splits (U-TOP-5)
    splits = {str(f.relative_to(ctx.run_dir / "results")): read_json(f)["split"]
              for f in (ctx.run_dir / "results").rglob("*.json")}
    on_test = sorted(k for k, s in splits.items() if s == "test")
    assert on_test == ["export/test/A1.json", "export/test/A2.json", "export/test/baseline.json",
                       "export/test/proposed.json"]
    assert [v["id"] for v in result["test"]["variants"]] == ["A1", "A2"]
    assert sorted(f.name for f in (out / "variants").iterdir()) == ["A1.patch", "A2.patch"]
    assert ("test_reporter", "export/test_report") in backend.calls       # the text reports the test
    assert result["final_checks"]["unverified_numbers"] == []
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



# ---- the reviews of 2026-10-02 -----------------------------------------------------------------
MAIN = (r"\documentclass{article}\begin{document}" "\n" r"\section{Results}" "\n{prose}\n"
        r"\input{results}" "\n" r"\end{document}" "\n")
BIB = "@misc{mock2026, title = {A mock reference}, author = {Mock, A.}, year = {2026}}\n"


def prompt(ctx, key):
    return read_json(ctx.run_dir / "prompts" / f"{key}.json")["user"]


def set_task(toy_task, **fields):
    d = json.loads((toy_task / "task.json").read_text())
    d.update(fields)
    (toy_task / "task.json").write_text(json.dumps(d))


def test_a_baseline_that_misses_the_reported_number_ends_the_run(tmp_path, toy_task):
    """U-BASE-2: a weaker baseline would inflate every gain (integrity review, finding 3)."""
    set_task(toy_task, baseline_check={"split": "full", "expected": 0.95, "tolerance": 0.02})
    rec, ctx, backend = go(tmp_path, toy_task, [GOOD_IDEA])
    assert rec["status"] == "baseline_failed" and "U-BASE-2" in rec["reason"]
    assert not any(a == "subset_coder" for a, _ in backend.calls)


def test_the_ablation_critic_reads_the_baseline(tmp_path, toy_task):
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT])
    text = prompt(ctx, "abl/p0/critic/0")
    base_mean = read_json(ctx.run_dir / "results" / "base/eval/full.json")["mean"]
    assert "<baseline_result>" in text and f"{base_mean}" in text
    assert "<reject_share>\n0.5\n</reject_share>" in text


def test_a_rebuttal_plan_reads_the_results_already_reported(tmp_path, toy_task):
    low = {"agent": "peer_reviewer", "key": "^write/p0/review/0$", "output": {"score": 3}}
    rec, ctx, backend = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, low])
    assert rec["status"] == "done", rec.get("reason")
    text = prompt(ctx, "write/p0/rebut0/plan")
    assert '"ablations"' in text and '"A1"' in text
    assert ("paper_enhancer", "write/p0/enhance/0") in backend.calls
    result = read_json(ctx.run_dir / "export" / "results.json")
    assert [r["id"] for r in result["rebuttals"]] == ["rebut0-R1"]
    assert "S1" in [v["id"] for v in result["test"]["variants"]]


def test_a_reference_whose_search_failed_is_kept(tmp_path, toy_task):
    refs = {"agent": "reference_checker", "output": {"entries": [
        {"key": "mock2026", "status": "unchecked", "evidence": "the search tool failed"},
        {"key": "ghost2020", "status": "not_found", "evidence": "searched twice"}]}}
    rec, ctx, backend = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, refs])
    audit = read_json(ctx.run_dir / "export" / "audit.json")
    assert audit["unchecked"] == ["mock2026"] and audit["repaired"] is True
    repair = prompt(ctx, "audit/p0/repair")
    problems = repair.split('"problems"')[1].split('"report"')[0]
    assert "ghost2020" in problems and "mock2026" not in problems


def test_a_writer_cannot_change_the_numbers_a_reviewer_reads(tmp_path, toy_task):
    """Integrity review, finding 5: the drafter edits the engine's table."""
    forged = {"agent": "initial_drafter", "edits": {
        "main.tex": MAIN.replace("{prose}", "We report our results."),
        "references.bib": BIB, "results.tex": "Proposed & 0.9999 \\\\\n"}}
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, forged])
    review = prompt(ctx, "write/p0/review/0")
    assert "0.9999" not in review and "1.0000" in review           # the engine's table, regenerated
    audit = read_json(ctx.run_dir / "export" / "audit.json")
    assert audit["tables_edited"] is True and audit["repaired"] is True


def test_a_number_in_the_prose_that_no_result_holds_is_flagged(tmp_path, toy_task):
    """Integrity review, finding 4."""
    invented = {"agent": "initial_drafter", "edits": {
        "main.tex": MAIN.replace("{prose}", "Our method reaches an accuracy of 0.4242 on average."),
        "references.bib": BIB}}
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, invented])
    audit = read_json(ctx.run_dir / "export" / "audit.json")
    assert audit["unverified_numbers"] == ["0.4242"] and audit["repaired"] is True


def test_a_restart_the_ablation_critic_rejects_keeps_the_previous_pass(tmp_path, toy_task):
    """Architecture review, finding 6: a Reject on a restarted pass used to end the run."""
    near = {"agent": "subset_coder", "key": "^evo/r0/s1/", "edits": {"params.json": params(0.35)}}
    refine = {"agent": "meta_reviewer", "key": "^meta/review/0$", "output": {"decision": "Refine"}}
    better = {"agent": "full_set_engineer", "key": "^meta/refine/0", "edits": {"params.json": params(0.3)}}
    reject = {"agent": "ablation_critic", "key": "^abl/p1/", "output": {"verdict": "Reject"}}
    rec, ctx, backend = go(tmp_path, toy_task, [near, BAD_IDEA, BAD_VERDICT, refine, better, reject])
    assert rec["status"] == "done", rec.get("reason")
    result = read_json(ctx.run_dir / "export" / "results.json")
    assert result["meta_status"] == "restart_rejected" and result["meta_accepted"] is False
    assert result["validation"]["proposed"]["mean"] < 1.0               # pass 0's core, not the restart's


def test_a_failure_that_stops_the_run_is_retried_on_resume(tmp_path, toy_task):
    """Architecture review, finding 4: a stored failure used to replay on every resume."""
    broken = {"agent": "peer_reviewer", "key": "^write/p0/review/0$", "raise": "failed"}
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, broken])
    assert rec["status"] == "error" and rec["retry_on_resume"] == "write/p0/review/0"
    ctx2 = prepare(ctx.run_dir, None, None, MockBackend({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]}),
                   sleep=lambda s: None)
    assert run(ctx2)["status"] == "done"


def test_one_engine_per_run(tmp_path, toy_task):
    ctx = prepare(tmp_path / "run", toy_task, profile(), MockBackend(), sleep=lambda s: None)
    try:
        with pytest.raises(RunLocked):
            prepare(tmp_path / "run", None, None, MockBackend(), sleep=lambda s: None)
    finally:
        close(ctx)
    close(prepare(tmp_path / "run", None, None, MockBackend(), sleep=lambda s: None))   # released


def test_a_run_keeps_its_own_prompts_and_refuses_a_changed_one(tmp_path, toy_task):
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT])
    coder = ctx.run_dir / "agents" / "subset_coder" / "prompt.md"       # a coding unit replays too
    coder.write_text(coder.read_text() + "\nAnother instruction.\n")
    rec1 = run(prepare(ctx.run_dir, None, None, MockBackend(), sleep=lambda s: None))
    assert rec1["status"] == "error" and "InputsChanged" in rec1["reason"] and "subset/code" in rec1["reason"]
    snapshot = ctx.run_dir / "agents" / "limitation_extractor" / "prompt.md"
    assert snapshot.exists() and read_json(ctx.run_dir / "run.json")["agents_sha256"]
    snapshot.write_text(snapshot.read_text() + "\nA new instruction.\n")
    rec2 = run(prepare(ctx.run_dir, None, None, MockBackend(), sleep=lambda s: None))
    assert rec2["status"] == "error" and "InputsChanged" in rec2["reason"]
    rec3 = run(prepare(ctx.run_dir, None, None, MockBackend({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]}),
                       sleep=lambda s: None, allow_changed=True))
    assert rec3["status"] == "done", rec3.get("reason")


# ---- the Codex review of 2026-10-02 ------------------------------------------------------------
def test_the_meta_reviewer_reads_the_verified_tables(tmp_path, toy_task):
    """P1: the audit's repair is a writer session too, and its edited tables reached the meta-review."""
    forged = {"agent": "initial_drafter", "edits": {
        "main.tex": MAIN.replace("{prose}", "We report our results."),
        "references.bib": BIB, "results.tex": "Proposed & 0.9999 \\\\\n"}}
    forged_repair = {"agent": "paper_enhancer", "key": "^audit/p0/repair$", "edits": {
        "main.tex": MAIN.replace("{prose}", "We report our results."),
        "results.tex": "Proposed & 0.9999 \\\\\n"}}
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, forged, forged_repair])
    assert rec["status"] == "done", rec.get("reason")
    assert "0.9999" in (ctx.papers.path("audit/p0.repaired") / "results.tex").read_text()
    meta = prompt(ctx, "meta/review/0")
    assert "0.9999" not in meta and "1.0000" in meta


def test_a_crash_between_storing_a_unit_and_making_its_version_does_not_pay_twice(tmp_path, toy_task, monkeypatch):
    """P1: the version used to be made before the unit was stored, so a crash between the two
    lost a finished, paid call; now the resume makes the version from what the agent left."""
    from scientisttwo.workspace import Workspaces
    real, crashed = Workspaces.finalize, []

    def crash_once(self, tmp, name, message):
        if name == "write/p0.draft" and not crashed:
            crashed.append(name)
            raise RuntimeError("the machine died here")
        return real(self, tmp, name, message)

    monkeypatch.setattr(Workspaces, "finalize", crash_once)
    with pytest.raises(RuntimeError, match="the machine died"):
        go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT])
    run_dir = tmp_path / "run"
    assert (run_dir / "units" / "write" / "p0" / "draft.json").exists()        # stored first
    assert (run_dir / "manuscripts" / "write" / "p0.draft.tmp").is_dir()       # the agent's work
    backend2 = MockBackend({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]})
    rec = run(prepare(run_dir, None, None, backend2, sleep=lambda s: None))
    assert rec["status"] == "done", rec.get("reason")
    assert ("initial_drafter", "write/p0/draft") not in backend2.calls       # not paid twice
    assert (run_dir / "manuscripts" / "write" / "p0.draft" / "main.tex").exists()


def test_a_resume_keeps_the_task_settings_the_run_started_with(tmp_path, toy_task):
    """P1: a resume used to reload task.json, mixing seeds of two protocols in one run."""
    pause = {"agent": "ablation_planner", "raise": "rate_limit"}
    prof = profile()
    prof["rate_limit"]["max_wait_minutes"] = 0
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, pause], prof)
    assert rec["status"] == "paused"
    assert read_json(ctx.run_dir / "run.json")["task_manifest"]["splits"]["full"]["seeds"] == [0, 1]
    d = json.loads((toy_task / "task.json").read_text())
    d["splits"]["full"]["seeds"] = [7, 8]
    (toy_task / "task.json").write_text(json.dumps(d))
    from scientisttwo.runtime.agents import InputsChanged
    with pytest.raises(InputsChanged, match="splits"):
        prepare(ctx.run_dir, None, None, MockBackend(), sleep=lambda s: None)
    rules = {"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]}
    ctx2 = prepare(ctx.run_dir, None, None, MockBackend(rules), sleep=lambda s: None, allow_changed=True)
    assert ctx2.task.splits["full"].seeds == (7, 8)
    close(ctx2)
    history = read_json(ctx.run_dir / "run.json")["history"]
    assert any(h.get("event") == "task_changed" and h["keys"] == ["splits"] for h in history)


def test_the_ablation_planner_reads_the_selected_version_and_cannot_write_it(tmp_path, toy_task):
    """Codex review, P2: declared a reasoning agent, the planner ran in the scratch directory with
    no read access to the code it was told to read."""
    seen = []

    class Spy(MockBackend):
        def call(self, call):
            if call.agent == "ablation_planner":
                seen.append(call)
            return super().call(call)

    rules = [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]
    rec, ctx, _ = go(tmp_path, toy_task, rules, backend=Spy({"rules": rules}))
    assert rec["status"] == "done", rec.get("reason")
    good = [t for t in read_json(ctx.run_dir / "traces.json") if t["verdict"] == "Good"]
    selected = ctx.ws.path(good[0]["ws"])                     # s1, the only Good idea
    c = seen[0]
    assert c.kind == "readonly" and c.cwd == selected and (selected / "params.json").exists()
    assert selected in c.sandbox.readable and selected in c.sandbox.readonly
    assert selected not in c.sandbox.writable


def test_downtime_after_a_crash_is_not_running_time(tmp_path, toy_task):
    """P2: a crash left the status `running`, so the whole stop until the resume counted against
    the running-time cap. Also: a finished run keeps no stale pause reason."""
    from scientisttwo.runtime.budget import running_hours
    from scientisttwo.runtime.store import atomic_write_json
    pause = {"agent": "ablation_planner", "raise": "rate_limit"}
    prof = profile()
    prof["rate_limit"]["max_wait_minutes"] = 0
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT, pause], prof)
    assert rec["status"] == "paused" and rec["resume_after"]
    # the next engine starts, runs for a minute, and is killed: its status stays `running`. The
    # resume comes ten hours later
    run_json = ctx.run_dir / "run.json"
    before = running_hours(ctx.run_dir)
    r = read_json(run_json)
    t = time.time() + 1
    r["status"] = "running"
    r["history"].append({"time": t, "status": "running"})
    atomic_write_json(run_json, r)
    atomic_write_json(ctx.run_dir / "heartbeat", {"time": t + 60})
    assert running_hours(ctx.run_dir, now=t + 36000) - before > 9.9           # what it used to count
    ctx2 = prepare(ctx.run_dir, None, None, MockBackend({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]}),
                   sleep=lambda s: None)
    assert read_json(run_json)["history"][-2]["status"] == "crashed"
    assert running_hours(ctx.run_dir, now=t + 36000) - before == pytest.approx(60 / 3600, abs=1e-3)
    rec2 = run(ctx2)
    assert rec2["status"] == "done" and "resume_after" not in rec2 and "reason" not in rec2


def test_the_exported_budget_counts_the_exports_own_calls(tmp_path, toy_task):
    """P2: the budget was taken before the test reporter and the final judge ran."""
    rec, ctx, _ = go(tmp_path, toy_task, [GOOD_IDEA, BAD_IDEA, BAD_VERDICT])
    exported = read_json(ctx.run_dir / "export" / "results.json")["budget"]
    assert exported["agent_calls"] == rec["budget"]["agent_calls"] == sum(exported["by_outcome"].values())
    assert exported["by_agent"]["final_judge"]["calls"] == 1
    early = ctx.rt.budget.summary()
    ctx.rt.budget.record({"key": "x/1", "agent": "final_judge", "kind": "reasoning", "outcome": "ok",
                          "seconds": 1, "equiv_usd": 0.0})
    assert early["by_outcome"] == exported["by_outcome"]       # a stored summary does not move


def test_the_exported_patch_is_the_whole_change(tmp_path, toy_task):
    """Codex review 2, P2: the patch was cut at the cap on what a model reads, and did not apply."""
    import subprocess
    big = {"agent": "subset_coder", "key": "^evo/r0/s1/",
           "edits": {"params.json": params(0.3), "notes.py": "# note\n" * 40000}}       # 280 kB
    rec, ctx, _ = go(tmp_path, toy_task, [big, BAD_IDEA, BAD_VERDICT])
    assert rec["status"] == "done", rec.get("reason")
    patch = ctx.run_dir / "export" / "changes.patch"
    assert patch.stat().st_size > 280000
    base = tmp_path / "base-copy"
    ctx.ws.export("base", base)
    subprocess.run(["git", "init", "-q", str(base)], check=True)
    check = subprocess.run(["git", "-C", str(base), "apply", "--check", str(patch)], capture_output=True, text=True)
    assert check.returncode == 0, check.stderr


def test_every_coding_session_gets_the_tasks_timeout(tmp_path, toy_task):
    """Codex review 3: the D7 test called the runtime directly and never went through Ctx.code."""
    seen = {}

    class Spy(MockBackend):
        def call(self, call):
            if call.kind in ("coding", "writer"):
                seen.setdefault(call.agent, call.timeout_s)
            return super().call(call)

    rules = [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]
    rec, ctx, _ = go(tmp_path, toy_task, rules, backend=Spy({"rules": rules}))
    assert rec["status"] == "done" and seen and set(seen.values()) == {60}     # the toy task's 60 s
