"""The command line, on the mock backend."""
import json

from scientisttwo import cli
from scientisttwo.runtime.store import read_json
from test_e2e_mock import BAD_IDEA, BAD_VERDICT, GOOD_IDEA


def test_wait_sleeps_through_a_usage_window_and_finishes_the_run(tmp_path, toy_task, monkeypatch):
    sleeps = []
    monkeypatch.setattr(cli, "_sleep", sleeps.append)
    rules = tmp_path / "rules.json"
    rules.write_text(json.dumps({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT,
                                           {"agent": "ablation_planner", "raise": "rate_limit", "times": 1}]}))
    run_dir = tmp_path / "run"
    code = cli.main(["run", "--task", str(toy_task), "--run-dir", str(run_dir), "--backend", "mock",
                     "--mock-script", str(rules), "--set", "rate_limit.max_wait_minutes=0", "--wait"])
    rec = read_json(run_dir / "run.json")
    assert code == 0 and rec["status"] == "done", rec.get("reason")
    assert len(sleeps) == 1 and 60 <= sleeps[0] <= 60 + cli.RESUME_MARGIN_S + 5
    assert [h.get("status") for h in rec["history"] if h.get("status")].count("paused") == 1


def test_wait_does_not_wait_for_a_pause_without_a_reset():
    sleeps = []
    rec = cli.wait_and_resume({"status": "paused", "reason": "agent-call cap reached"}, resume=None,
                              max_wait_hours=24, sleep=sleeps.append)
    assert rec["status"] == "paused" and sleeps == []


# ---- what the guide's checks found (2026-10-02) -------------------------------------------------
def _paused_run(tmp_path, toy_task):
    rules = tmp_path / "rules.json"
    rules.write_text(json.dumps({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT,
                                           {"agent": "ablation_planner", "raise": "rate_limit"}]}))
    run_dir = tmp_path / "run"
    code = cli.main(["run", "--task", str(toy_task), "--run-dir", str(run_dir), "--backend", "mock",
                     "--mock-script", str(rules), "--set", "rate_limit.max_wait_minutes=0"])
    assert code == 3 and read_json(run_dir / "run.json")["status"] == "paused"
    return run_dir


def test_run_refuses_an_existing_run_and_resume_changes_only_caps_on_the_record(tmp_path, toy_task):
    run_dir = _paused_run(tmp_path, toy_task)
    before = (run_dir / "run.json").read_text()
    assert cli.main(["run", "--task", str(toy_task), "--run-dir", str(run_dir), "--profile", "paper"]) == 1
    assert (run_dir / "run.json").read_text() == before                  # not silently resumed
    assert cli.main(["resume", str(run_dir), "--backend", "mock", "--set", "limits.K=3"]) == 1
    from scientisttwo.orchestrator import close, prepare
    from scientisttwo.runtime.backends.mock import MockBackend
    held = prepare(run_dir, None, None, MockBackend())
    try:
        assert cli.main(["resume", str(run_dir), "--backend", "mock"]) == 1    # locked: no traceback
    finally:
        close(held)
    rules = tmp_path / "ok.json"
    rules.write_text(json.dumps({"rules": [GOOD_IDEA, BAD_IDEA, BAD_VERDICT]}))
    assert cli.main(["resume", str(run_dir), "--backend", "mock", "--mock-script", str(rules),
                     "--set", "budget.max_agent_calls=999"]) == 0
    rec = read_json(run_dir / "run.json")
    changed = [h for h in rec["history"] if h.get("event") == "budget_changed"]
    assert rec["status"] == "done" and changed[0]["after"]["max_agent_calls"] == 999


def test_a_mistyped_cap_leaves_no_run_behind(tmp_path, toy_task):
    import pytest
    run_dir = tmp_path / "run"
    with pytest.raises(ValueError):
        cli.main(["run", "--task", str(toy_task), "--run-dir", str(run_dir), "--backend", "mock",
                  "--set", "budget.max_agent_cals=5"])
    assert not run_dir.exists()


def test_a_new_status_drops_the_last_finish(tmp_path):
    from scientisttwo.orchestrator import _set_status
    from scientisttwo.runtime.store import atomic_write_json
    atomic_write_json(tmp_path / "run.json", {"status": "done", "final": {"idea": "x"}, "history": []})
    assert "final" not in _set_status(tmp_path, "error", reason="later")


def test_a_resume_after_a_wait_takes_the_current_claude_when_the_pinned_one_is_gone(tmp_path):
    from scientisttwo.runtime.backends.claude_cli import ClaudeCLIBackend
    b = ClaudeCLIBackend(claude_bin=str(tmp_path / "versions" / "2.1.0"))
    assert cli._current(b) is not b and cli._current(b).claude_bin != b.claude_bin
    live = ClaudeCLIBackend()
    assert cli._current(live) is live


# ---- the fourth Codex pass (2026-10-02) ---------------------------------------------------------
def test_a_cap_must_be_a_number_and_a_bad_one_changes_nothing(tmp_path, toy_task):
    run_dir = _paused_run(tmp_path, toy_task)
    before = read_json(run_dir / "run.json")["profile"]
    assert cli.main(["resume", str(run_dir), "--backend", "mock", "--set", "budget.max_agent_calls=\"typo\""]) == 1
    assert cli.main(["resume", str(run_dir), "--backend", "mock", "--set", "budget.max_five_hour_utilization=3"]) == 1
    assert read_json(run_dir / "run.json")["profile"] == before


def test_run_refuses_an_existing_run_named_with_a_tilde(tmp_path, toy_task, monkeypatch):
    run_dir = _paused_run(tmp_path, toy_task)
    monkeypatch.setenv("HOME", str(tmp_path))
    assert cli.main(["run", "--task", str(toy_task), "--run-dir", f"~/{run_dir.name}"]) == 1


def test_a_resume_refused_after_the_wait_is_not_reported_as_a_pause():
    from scientisttwo.orchestrator import RunLocked

    def taken():
        raise RunLocked("another engine process is running it")

    rec = cli.wait_and_resume({"status": "paused", "resume_after": 1.0, "reason": "window"}, taken, 24,
                              sleep=lambda s: None)
    assert rec["status"] == "refused"
