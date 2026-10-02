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
