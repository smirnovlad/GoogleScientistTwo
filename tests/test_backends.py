"""The claude -p backend against a fake CLI, and the agent runtime against the mock backend."""
import json
import os
import stat
import time
from pathlib import Path

import pytest

from scientisttwo.runtime.agents import AgentRuntime, AgentSpec, Routing, UnitFailed
from scientisttwo.runtime.backends.base import (AgentCall, AgentFailed, AgentTimeout, InvalidOutput,
                                                RateLimited, TransientError)
from scientisttwo.runtime.backends.claude_cli import ClaudeCLIBackend, child_env
from scientisttwo.runtime.backends.mock import MockBackend, synth
from scientisttwo.runtime.budget import Budget, BudgetExceeded, Caps
from scientisttwo.runtime.store import RunStore

FAKE = Path(__file__).parent / "fake_claude.py"
SCHEMA = {"type": "object", "properties": {"verdict": {"type": "string", "enum": ["Good", "Bad"]},
                                           "feedback": {"type": "string"}},
          "required": ["verdict", "feedback"], "additionalProperties": False}


@pytest.fixture
def fake(tmp_path):
    os.chmod(FAKE, os.stat(FAKE).st_mode | stat.S_IXUSR)
    return ClaudeCLIBackend(claude_bin=str(FAKE))


def call(scenario="success", kind="reasoning", timeout=20, transcript=None):
    return AgentCall(agent="critic", kind=kind, system="SYSTEM", user=f"hello\nSCENARIO={scenario}\n",
                     schema=SCHEMA, model="sonnet", effort="medium", tools=(), cwd=None, sandbox=None,
                     timeout_s=timeout, transcript=transcript, key="t/1")


def last_call() -> dict:
    return json.loads((Path(os.environ.get("TMPDIR", "/tmp")) / "fake_claude_last_call.json").read_text())


def test_success_and_isolation_flags(fake, tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-must-not-leak")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://example.invalid")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "parent-session")
    r = fake.call(call(transcript=tmp_path / "t.jsonl"))
    assert r.output == {"verdict": "Good", "feedback": "fine"} and r.cost_usd == 0.0123
    assert r.raw["api_key_source"] == "none" and r.raw["rate_limit"]["status"] == "allowed"
    argv, env = last_call()["argv"], last_call()["env"]
    assert "--bare" not in argv
    for flag in ("-p", "--setting-sources", "--strict-mcp-config", "--disable-slash-commands",
                 "--no-session-persistence", "--json-schema", "--system-prompt"):
        assert flag in argv
    assert argv[argv.index("--setting-sources") + 1] == "" and argv[argv.index("--tools") + 1] == ""
    assert not any(k.startswith("ANTHROPIC") or k.startswith("CLAUDE_CODE") for k in env)
    assert (tmp_path / "t.jsonl").read_text().count("\n") == 3


def test_coding_agents_keep_the_cli_prompt_and_bypass_inside_the_sandbox(fake):
    fake.call(call(kind="coding"))
    argv = last_call()["argv"]
    assert "--append-system-prompt" in argv and "--system-prompt" not in argv
    assert argv[argv.index("--permission-mode") + 1] == "bypassPermissions"


def test_api_key_auth_is_refused(fake):
    started = time.time()
    with pytest.raises(AgentFailed, match="bill the API"):
        fake.call(call("apikey"))
    assert time.time() - started < 4          # killed at the init event, before any result


@pytest.mark.parametrize("scenario,error", [("ratelimit", RateLimited), ("error429", RateLimited),
                                            ("overloaded", TransientError), ("crash", TransientError),
                                            ("noschema", InvalidOutput)])
def test_failures_are_classified(fake, scenario, error):
    with pytest.raises(error):
        fake.call(call(scenario))


def test_rate_limit_carries_the_reset_time(fake):
    with pytest.raises(RateLimited) as e:
        fake.call(call("ratelimit"))
    assert e.value.reset_at and e.value.reset_at > time.time()


def test_timeout_kills_the_call(fake):
    with pytest.raises(AgentTimeout):
        fake.call(call("slow", timeout=1))


def test_child_env_is_an_allowlist(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    env = child_env()
    assert set(env) <= {"HOME", "USER", "LOGNAME", "SHELL", "LANG", "TERM", "PATH", "TMPDIR"}


# ---- the runtime, on the mock backend ---------------------------------------------------------
SPEC = AgentSpec(name="critic", kind="reasoning", tools=(), paper_ref="test", description="",
                 variables=("x",), system="sys", prompt="judge {{x}}", schema=SCHEMA)


def runtime(tmp_path, script=None, caps=None, max_wait=0.0):
    backend = MockBackend(script)
    sleeps: list = []
    rt = AgentRuntime(backend, RunStore(tmp_path), Budget(tmp_path, caps or Caps(), time.time()),
                      Routing({"default": {"model": "sonnet"}}), tmp_path, specs={"critic": SPEC},
                      max_wait_minutes=max_wait, sleep=sleeps.append)
    return rt, backend, sleeps


def test_a_finished_unit_is_never_paid_twice(tmp_path):
    rt, backend, _ = runtime(tmp_path)
    first = rt.run("a/1", "critic", {"x": 1})
    rt2, backend2, _ = runtime(tmp_path)                     # a resumed process
    assert rt2.run("a/1", "critic", {"x": 1}) == first and backend2.calls == []


def test_transient_errors_are_retried(tmp_path):
    rt, backend, sleeps = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "transient", "times": 2}]})
    assert rt.run("a/1", "critic", {"x": 1})["verdict"] in ("Good", "Bad")
    assert len(backend.calls) == 3 and len(sleeps) == 2


def test_persistent_failure_is_stored_and_replayed(tmp_path):
    rt, backend, _ = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "failed"}]})
    with pytest.raises(UnitFailed):
        rt.run("a/1", "critic", {"x": 1})
    rt2, backend2, _ = runtime(tmp_path)
    with pytest.raises(UnitFailed):
        rt2.run("a/1", "critic", {"x": 1})
    assert backend2.calls == []


def test_invalid_output_is_retried_with_the_error(tmp_path):
    rt, backend, _ = runtime(tmp_path, {"rules": [{"agent": "critic", "output": {"verdict": "Maybe"}, "times": 1}]})
    assert rt.run("a/1", "critic", {"x": 1})["verdict"] == "Good"
    assert len(backend.calls) == 2


def test_usage_limit_waits_when_short_and_pauses_when_long(tmp_path):
    rt, backend, sleeps = runtime(tmp_path / "a", {"rules": [{"agent": "critic", "raise": "rate_limit", "times": 1}]},
                                  max_wait=10)
    rt.run("a/1", "critic", {"x": 1})
    assert len(sleeps) == 1 and len(backend.calls) == 2
    rt, backend, sleeps = runtime(tmp_path / "b", {"rules": [{"agent": "critic", "raise": "rate_limit"}]})
    with pytest.raises(BudgetExceeded):
        rt.run("a/1", "critic", {"x": 1})
    assert not RunStore(tmp_path / "b").has("a/1")           # nothing half-written: resumable


def test_budget_caps_stop_before_the_call(tmp_path):
    rt, backend, _ = runtime(tmp_path, caps=Caps(max_agent_calls=1))
    rt.run("a/1", "critic", {"x": 1})
    with pytest.raises(BudgetExceeded):
        rt.run("a/2", "critic", {"x": 2})
    assert len(backend.calls) == 1


def test_usage_window_ceiling_pauses(tmp_path):
    b = Budget(tmp_path, Caps(max_five_hour_utilization=0.5), time.time())
    b.record({"agent": "x", "kind": "reasoning", "seconds": 1, "equiv_usd": None,
              "rate_limit": {"unifiedWindows": {"five_hour": {"utilization": 0.6, "resetsAt": time.time() + 99}}}})
    with pytest.raises(BudgetExceeded) as e:
        b.check("reasoning")
    assert e.value.resume_after and b.summary()["unknown_cost_calls"] == 1


def test_synth_fits_its_schema():
    import jsonschema
    jsonschema.validate(synth(SCHEMA), SCHEMA)
