"""The claude -p backend against a fake CLI, and the agent runtime against the mock backend."""
import json
import os
import stat
import time
from pathlib import Path

import pytest

from scientisttwo.harness.sandbox import SandboxPolicy, SandboxUnavailable, child_env
from scientisttwo.runtime.agents import AgentRuntime, AgentSpec, InputsChanged, Routing, UnitFailed
from scientisttwo.runtime.backends import make_backend
from scientisttwo.runtime.backends.base import (AgentCall, AgentFailed, AgentTimeout, EnvironmentFault,
                                                InvalidOutput, RateLimited, TransientError)
from scientisttwo.runtime.backends.claude_cli import QUIET_ENV, ClaudeCLIBackend, _reset_at
from scientisttwo.runtime.backends.mock import MockBackend, synth
from scientisttwo.runtime.budget import Budget, BudgetExceeded, Caps, RunPaused
from scientisttwo.runtime.store import RunStore

FAKE = Path(__file__).parent / "fake_claude.py"
SCHEMA = {"type": "object", "properties": {"verdict": {"type": "string", "enum": ["Good", "Bad"]},
                                           "feedback": {"type": "string"}},
          "required": ["verdict", "feedback"], "additionalProperties": False}
TMP = Path(os.environ.get("TMPDIR", "/tmp"))


@pytest.fixture
def fake(tmp_path):
    os.chmod(FAKE, os.stat(FAKE).st_mode | stat.S_IXUSR)
    # these tests check how the backend reads the CLI, not the sandbox (tests/test_harness.py)
    return ClaudeCLIBackend(claude_bin=str(FAKE), allow_unsandboxed=True)


def call(scenario="success", kind="reasoning", timeout=20, transcript=None, sandbox=None):
    return AgentCall(agent="critic", kind=kind, system="SYSTEM", user=f"hello\nSCENARIO={scenario}\n",
                     schema=SCHEMA, model="sonnet", effort="medium", tools=(), cwd=None, sandbox=sandbox,
                     timeout_s=timeout, transcript=transcript, key="t/1")


def last_call() -> dict:
    return json.loads((TMP / "fake_claude_last_call.json").read_text())


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
    assert not any(k.startswith("ANTHROPIC") for k in env)
    # the only Claude Code variables are the engine's own switches: none of the launching session's
    assert {k for k in env if k.startswith("CLAUDE_CODE")} == {k for k in QUIET_ENV if k.startswith("CLAUDE_CODE")}
    assert env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] == "1" and env["DISABLE_AUTOUPDATER"] == "1"
    assert (tmp_path / "t.jsonl").read_text().count("\n") == 3


def test_the_proxy_and_the_unit_tmpdir_reach_the_cli(fake, tmp_path):
    sb = SandboxPolicy.build(network="proxy", proxy_port=4321)
    c = AgentCall(agent="critic", kind="reasoning", system="S", user="SCENARIO=success\n", schema=SCHEMA,
                  model="sonnet", effort=None, tools=(), cwd=None, sandbox=sb, timeout_s=20,
                  transcript=None, key="t/1", tmpdir=tmp_path)
    fake.allow_unsandboxed = True
    env = fake.env(c)
    assert env["HTTPS_PROXY"] == "http://127.0.0.1:4321" and env["TMPDIR"] == str(tmp_path)
    assert env["NO_PROXY"] == ""                 # nothing bypasses the proxy


def test_no_policy_no_process():
    b = ClaudeCLIBackend(claude_bin=str(FAKE))
    with pytest.raises(SandboxUnavailable):
        b.call(call())


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
                                            ("noschema", InvalidOutput), ("usage", AgentFailed),
                                            ("eperm", EnvironmentFault), ("context", TransientError)])
def test_failures_are_classified(fake, scenario, error):
    """`context` once read as a usage limit ("limit reached"), `eperm` as an argument error
    (infrastructure review 2026-10-02, I10)."""
    with pytest.raises(error):
        fake.call(call(scenario))


def test_rate_limit_carries_the_reset_time(fake):
    with pytest.raises(RateLimited) as e:
        fake.call(call("ratelimit"))
    assert e.value.reset_at and e.value.reset_at > time.time()


def test_the_reset_comes_from_the_spent_window():
    now = time.time()
    windows = {"five_hour": {"utilization": 1.0, "resetsAt": now + 3600},
               "seven_day": {"utilization": 0.6, "resetsAt": now + 5 * 86400}}
    # a warning about the 7-day window, while the 5-hour one is the one spent
    assert abs(_reset_at({"status": "allowed_warning", "rateLimitType": "seven_day",
                          "resetsAt": now + 5 * 86400, "unifiedWindows": windows}) - (now + 3600)) < 1
    assert abs(_reset_at({"status": "rejected", "resetsAt": now + 7200, "unifiedWindows": windows}) - (now + 7200)) < 1


def test_timeout_kills_the_call(fake):
    with pytest.raises(AgentTimeout):
        fake.call(call("slow", timeout=1))


def _holder_pid(path: Path) -> int:
    deadline = time.time() + 5
    while not path.exists() and time.time() < deadline:
        time.sleep(0.05)
    return int(path.read_text())


def _dead(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return False
    except ProcessLookupError:
        return True


def test_a_timeout_kills_a_descendant_that_holds_the_output(fake, tmp_path):
    """Codex review, P1: the timeout killed only the CLI's group, and the reader waited for the
    descendant holding the pipe, for its whole life (30 s here)."""
    pid_file = tmp_path / "holder.pid"
    c = call("holder", timeout=1)
    started = time.time()
    with pytest.raises(AgentTimeout):
        fake.call(AgentCall(**{**c.__dict__, "user": c.user + f"PIDFILE={pid_file}\n"}))
    assert time.time() - started < 8
    holder = _holder_pid(pid_file)
    deadline = time.time() + 3
    while not _dead(holder) and time.time() < deadline:
        time.sleep(0.05)
    assert _dead(holder)


def test_the_reader_is_bounded_even_when_a_holder_escapes_every_kill(fake, tmp_path, monkeypatch):
    """A descendant that left the tree and the unit's environment holds the pipe: the call still
    ends DRAIN_S after the kill, never at that process's exit."""
    import scientisttwo.runtime.backends.claude_cli as cli
    monkeypatch.setattr(cli, "DRAIN_S", 1.0)
    pid_file = tmp_path / "holder.pid"
    c = call("escaped_holder", timeout=2)
    started = time.time()
    try:
        with pytest.raises(AgentTimeout):
            fake.call(AgentCall(**{**c.__dict__, "user": c.user + f"PIDFILE={pid_file}\n"}))
        assert time.time() - started < 8          # 2 s timeout, 1 s drain, the clean-up
    finally:
        try:
            os.kill(_holder_pid(pid_file), 9)
        except (ProcessLookupError, ValueError, FileNotFoundError):
            pass


def test_a_delivered_result_survives_a_lingering_cli(fake):
    started = time.time()
    r = fake.call(call("linger", timeout=3))
    assert r.output == {"verdict": "Good", "feedback": "fine"}
    assert time.time() - started < 6           # not the CLI's 30 s, and not a timeout


def test_the_whole_process_tree_dies_with_the_call(fake, tmp_path):
    beat = tmp_path / "beat.txt"
    c = call("orphan")
    fake.call(AgentCall(**{**c.__dict__, "user": c.user + f"BEAT={beat}\n"}))
    assert beat.exists() and beat.stat().st_size > 0           # the child ran (Codex review 2, P2)
    time.sleep(0.6)
    size = beat.stat().st_size
    time.sleep(0.8)
    assert beat.stat().st_size == size, "a detached child outlived its call"


def test_child_env_is_an_allowlist(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    env = child_env("/usr/bin/python3")
    assert set(env) <= {"HOME", "USER", "LOGNAME", "SHELL", "LANG", "TERM", "PATH", "TMPDIR"}


def test_the_registry_resumes_a_run_on_the_backend_it_recorded(tmp_path):
    b = make_backend("claude_cli", claude_bin=str(FAKE))
    assert isinstance(b, ClaudeCLIBackend) and b.claude_bin == os.path.realpath(FAKE)
    assert isinstance(make_backend("mock"), MockBackend)
    with pytest.raises(ValueError):
        make_backend("gemini")
    # the CLI updated since and deleted the pinned version: the current binary takes over
    gone = make_backend("claude_cli", claude_bin=str(tmp_path / "versions" / "2.1.0"))
    assert isinstance(gone, ClaudeCLIBackend) and gone.claude_bin != str(tmp_path / "versions" / "2.1.0")


# ---- the runtime, on the mock backend ---------------------------------------------------------
SPEC = AgentSpec(name="critic", kind="reasoning", tools=(), paper_ref="test", description="",
                 variables=("x",), system="sys", prompt="judge {{x}}", schema=SCHEMA)


def runtime(tmp_path, script=None, caps=None, max_wait=0.0, strict=True, spec=SPEC):
    backend = MockBackend(script)
    sleeps: list = []
    rt = AgentRuntime(backend, RunStore(tmp_path), Budget(tmp_path, caps or Caps(), time.time()),
                      Routing({"default": {"model": "sonnet"}}), tmp_path, specs={"critic": spec},
                      max_wait_minutes=max_wait, sleep=sleeps.append, strict_replay=strict)
    return rt, backend, sleeps


def ledger(tmp_path) -> list[dict]:
    return [json.loads(l) for l in (tmp_path / "ledger.jsonl").read_text().splitlines()
            if json.loads(l).get("type") == "agent"]


def test_a_finished_unit_is_never_paid_twice(tmp_path):
    rt, backend, _ = runtime(tmp_path)
    first = rt.run("a/1", "critic", {"x": 1})
    rt2, backend2, _ = runtime(tmp_path)                     # a resumed process
    assert rt2.run("a/1", "critic", {"x": 1}) == first and backend2.calls == []
    assert (tmp_path / "prompts" / "a" / "1.json").exists()  # what was asked, in full


def test_a_replay_with_other_inputs_is_refused(tmp_path):
    rt, _, _ = runtime(tmp_path)
    rt.run("a/1", "critic", {"x": 1})
    rt2, backend2, _ = runtime(tmp_path)
    with pytest.raises(InputsChanged):
        rt2.run("a/1", "critic", {"x": 2})
    rt3, backend3, _ = runtime(tmp_path, strict=False)       # resume --allow-changed: replayed, logged
    rt3.run("a/1", "critic", {"x": 2})
    assert backend3.calls == []


def test_unknown_variables_are_refused(tmp_path):
    rt, _, _ = runtime(tmp_path)
    with pytest.raises(KeyError, match="not declared"):
        rt.run("a/1", "critic", {"x": 1, "y": 2})


def test_transient_errors_are_retried_and_each_attempt_is_in_the_ledger(tmp_path):
    rt, backend, sleeps = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "transient", "times": 2}]})
    assert rt.run("a/1", "critic", {"x": 1})["verdict"] in ("Good", "Bad")
    assert len(backend.calls) == 3 and len(sleeps) == 2
    assert [e["outcome"] for e in ledger(tmp_path)] == ["transient", "transient", "ok"]


def test_transient_errors_that_persist_pause_the_run_and_store_nothing(tmp_path):
    rt, backend, _ = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "transient"}]})
    with pytest.raises(RunPaused):
        rt.run("a/1", "critic", {"x": 1})
    assert not RunStore(tmp_path).has("a/1") and len(ledger(tmp_path)) == 3


def test_a_machine_fault_pauses(tmp_path):
    rt, _, _ = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "environment"}]})
    with pytest.raises(RunPaused, match="machine"):
        rt.run("a/1", "critic", {"x": 1})


def test_persistent_failure_is_stored_and_replayed(tmp_path):
    rt, backend, _ = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "failed"}]})
    with pytest.raises(UnitFailed):
        rt.run("a/1", "critic", {"x": 1})
    rt2, backend2, _ = runtime(tmp_path)
    with pytest.raises(UnitFailed):
        rt2.run("a/1", "critic", {"x": 1})
    assert backend2.calls == []


def test_a_timeout_is_retried_once_then_fails(tmp_path):
    rt, backend, _ = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "timeout", "times": 1}]})
    rt.run("a/1", "critic", {"x": 1})
    assert len(backend.calls) == 2
    rt, backend, _ = runtime(tmp_path / "b", {"rules": [{"agent": "critic", "raise": "timeout"}]})
    with pytest.raises(UnitFailed):
        rt.run("a/1", "critic", {"x": 1})
    assert len(backend.calls) == 2


def test_invalid_output_is_retried_with_the_error(tmp_path):
    rt, backend, _ = runtime(tmp_path, {"rules": [{"agent": "critic", "output": {"verdict": "Maybe"}, "times": 1}]})
    assert rt.run("a/1", "critic", {"x": 1})["verdict"] == "Good"
    assert len(backend.calls) == 2
    assert [e["outcome"] for e in ledger(tmp_path)] == ["invalid_output", "ok"]


def test_usage_limit_waits_when_short_and_pauses_when_long(tmp_path):
    rt, backend, sleeps = runtime(tmp_path / "a", {"rules": [{"agent": "critic", "raise": "rate_limit", "times": 1}]},
                                  max_wait=10)
    rt.run("a/1", "critic", {"x": 1})
    assert len(sleeps) == 1 and len(backend.calls) == 2
    rt, backend, sleeps = runtime(tmp_path / "b", {"rules": [{"agent": "critic", "raise": "rate_limit"}]})
    with pytest.raises(BudgetExceeded):
        rt.run("a/1", "critic", {"x": 1})
    assert not RunStore(tmp_path / "b").has("a/1")           # nothing half-written: resumable


def test_usage_limit_waits_are_capped(tmp_path):
    rt, backend, sleeps = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "rate_limit"}]}, max_wait=10)
    with pytest.raises(BudgetExceeded):
        rt.run("a/1", "critic", {"x": 1})
    assert len(sleeps) == 3 and len(backend.calls) == 4


def test_budget_caps_stop_before_the_call(tmp_path):
    rt, backend, _ = runtime(tmp_path, caps=Caps(max_agent_calls=1))
    rt.run("a/1", "critic", {"x": 1})
    with pytest.raises(BudgetExceeded):
        rt.run("a/2", "critic", {"x": 2})
    assert len(backend.calls) == 1


def test_retries_count_against_the_caps(tmp_path):
    """Three backend calls once counted as one (infrastructure review 2026-10-02, I2)."""
    rt, backend, _ = runtime(tmp_path, {"rules": [{"agent": "critic", "raise": "transient", "times": 1}]},
                             caps=Caps(max_agent_calls=2))
    rt.run("a/1", "critic", {"x": 1})
    with pytest.raises(BudgetExceeded):
        rt.run("a/2", "critic", {"x": 2})
    assert len(backend.calls) == 2


def test_usage_window_ceiling_pauses(tmp_path):
    b = Budget(tmp_path, Caps(max_five_hour_utilization=0.5), time.time())
    b.record({"agent": "x", "kind": "reasoning", "seconds": 1, "equiv_usd": None,
              "rate_limit": {"unifiedWindows": {"five_hour": {"utilization": 0.6, "resetsAt": time.time() + 99}}}})
    with pytest.raises(BudgetExceeded) as e:
        b.check("reasoning")
    assert e.value.resume_after and b.summary()["unknown_cost_calls"] == 1


def test_a_window_with_no_reset_time_does_not_block_forever(tmp_path):
    b = Budget(tmp_path, Caps(max_five_hour_utilization=0.5), time.time())
    b.record({"agent": "x", "kind": "reasoning", "seconds": 1, "equiv_usd": 0.0,
              "rate_limit": {"unifiedWindows": {"five_hour": {"utilization": 0.9}}}})
    b.check("reasoning")


def test_a_partial_ledger_line_is_repaired(tmp_path):
    b = Budget(tmp_path, Caps(), time.time())
    b.record({"agent": "x", "kind": "reasoning", "seconds": 1, "equiv_usd": 0.5})
    with open(tmp_path / "ledger.jsonl", "a") as f:
        f.write('{"type": "agent", "agent": "x", "equiv_')       # a crash mid-append
    b2 = Budget(tmp_path, Caps(), time.time())
    assert b2.totals.agent_calls == 1 and b2.totals.equiv_usd == 0.5


def test_paused_time_does_not_count_as_running(tmp_path):
    from scientisttwo.runtime.budget import running_hours
    now = time.time()
    (tmp_path / "run.json").write_text(json.dumps({"history": [
        {"time": now - 10 * 3600, "status": "running"}, {"time": now - 9 * 3600, "status": "paused"},
        {"time": now - 2 * 3600, "status": "running"}]}))
    assert abs(running_hours(tmp_path, now) - 3.0) < 1e-6
    b = Budget(tmp_path, Caps(max_hours=4), now - 10 * 3600)
    b.check("reasoning")                                       # 3 h running of a 10 h-old run


def test_synth_fits_its_schema():
    import jsonschema
    jsonschema.validate(synth(SCHEMA), SCHEMA)


# ---- the Codex review of 2026-10-02 ------------------------------------------------------------
def test_a_failed_result_keeps_the_cost_it_reported(fake, tmp_path):
    """P2: a result reporting $12.30 was counted as unknown, and a $1 cap let the next call run."""
    with pytest.raises(AgentFailed) as e:
        fake.call(call("costly_error"))
    assert e.value.cost_usd == pytest.approx(12.30) and e.value.tokens["input_tokens"] == 900

    class Costly(MockBackend):
        def call(self, c):
            self.calls.append((c.agent, c.key))
            err = AgentFailed("error_max_turns")
            err.cost_usd = 12.30
            raise err

    rt = AgentRuntime(Costly(), RunStore(tmp_path), Budget(tmp_path, Caps(max_equiv_usd=1.0), time.time()),
                      Routing({"default": {"model": "sonnet"}}), tmp_path, specs={"critic": SPEC},
                      sleep=lambda s: None)
    with pytest.raises(UnitFailed):
        rt.run("a/1", "critic", {"x": 1})
    assert ledger(tmp_path)[0]["equiv_usd"] == pytest.approx(12.30)
    with pytest.raises(BudgetExceeded):
        rt.run("a/2", "critic", {"x": 2})


def test_an_attempt_cut_off_by_the_engines_end_is_counted_and_numbered_on(tmp_path):
    """P2: an attempt was journalled only after its call, so a kill during a call erased it from
    the caps; and numbering restarted at 1, overwriting the earlier transcript."""
    class Dies(MockBackend):
        def call(self, c):
            c.transcript.write_text("the first attempt's evidence")
            raise KeyboardInterrupt                         # the engine is killed mid-call

    rt = AgentRuntime(Dies(), RunStore(tmp_path), Budget(tmp_path, Caps(max_agent_calls=5), time.time()),
                      Routing({"default": {"model": "sonnet"}}), tmp_path, specs={"critic": SPEC},
                      sleep=lambda s: None)
    with pytest.raises(KeyboardInterrupt):
        rt.run("a/1", "critic", {"x": 1})
    assert ledger(tmp_path) == []                              # only the journal line so far
    rt2, backend2, _ = runtime(tmp_path)                       # the next engine process
    assert ledger(tmp_path)[0]["outcome"] == "interrupted" and ledger(tmp_path)[0]["equiv_usd"] is None
    assert rt2.budget.totals.agent_calls == 1 and rt2.budget.totals.unknown_cost_calls == 1
    rt2.run("a/1", "critic", {"x": 1})
    assert [e["attempt"] for e in ledger(tmp_path)] == [1, 2]
    transcripts = tmp_path / "transcripts" / "a"
    assert (transcripts / "1.jsonl").read_text() == "the first attempt's evidence"
    assert (transcripts / "1.attempt2.jsonl").exists()



# ---- the second Codex review of 2026-10-02 ------------------------------------------------------
def test_parallel_calls_cannot_pass_a_cap_together(tmp_path):
    """P1: two workers checked a cap of one before either call was counted."""
    import threading

    class Slow(MockBackend):
        def call(self, c):
            time.sleep(0.3)
            return super().call(c)

    backend = Slow()
    rt = AgentRuntime(backend, RunStore(tmp_path), Budget(tmp_path, Caps(max_agent_calls=1), time.time()),
                      Routing({"default": {"model": "sonnet"}}), tmp_path, specs={"critic": SPEC},
                      sleep=lambda s: None)
    errors = []

    def one(i):
        try:
            rt.run(f"a/{i}", "critic", {"x": i})
        except BudgetExceeded as e:
            errors.append(e)

    threads = [threading.Thread(target=one, args=(i,)) for i in range(2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert len(backend.calls) == 1 and len(errors) == 1


def test_a_unit_finished_but_not_stored_is_rebuilt_without_a_second_call(tmp_path, monkeypatch):
    """P1: a crash after the success line and before the store write paid for the unit twice."""
    rt, backend, _ = runtime(tmp_path)
    real = RunStore.put

    def dies(self, key, record):
        raise KeyboardInterrupt                                   # the engine dies here

    monkeypatch.setattr(RunStore, "put", dies)
    with pytest.raises(KeyboardInterrupt):
        rt.run("a/1", "critic", {"x": 1})
    monkeypatch.setattr(RunStore, "put", real)
    rt2, backend2, _ = runtime(tmp_path)                          # the next engine process
    rt2.run("a/1", "critic", {"x": 1})
    assert backend2.calls == [] and RunStore(tmp_path).has("a/1")
    rt2.forget("a/1")                                             # forgotten for good: runs again
    rt3, backend3, _ = runtime(tmp_path)
    rt3.run("a/1", "critic", {"x": 1})
    assert len(backend3.calls) == 1


def test_a_changed_schema_does_not_replay(tmp_path):
    """P2: the replay fingerprint ignored the output schema and the tools."""
    rt, _, _ = runtime(tmp_path)
    rt.run("a/1", "critic", {"x": 1})
    changed = AgentSpec(**{**SPEC.__dict__, "schema": {**SCHEMA, "required": ["verdict"]}})
    rt2, _, _ = runtime(tmp_path, spec=changed)
    with pytest.raises(InputsChanged):
        rt2.run("a/1", "critic", {"x": 1})


def test_a_failed_call_keeps_its_usage_windows(fake):
    with pytest.raises(AgentFailed) as e:
        fake.call(call("costly_error"))
    assert e.value.rate_limit["unifiedWindows"]["five_hour"]["utilization"] == 0.4


def test_a_coding_session_gets_the_tasks_timeout_unless_its_route_sets_one(tmp_path):
    seen = []

    class Spy(MockBackend):
        def call(self, c):
            seen.append(c.timeout_s)
            return super().call(c)

    for routing, expected in (({"default": {"model": "sonnet"}}, 60),
                              ({"default": {"model": "sonnet"}, "agents": {"critic": {"timeout_s": 99}}}, 99)):
        rt = AgentRuntime(Spy(), RunStore(tmp_path / str(expected)), Budget(tmp_path / str(expected), Caps(), time.time()),
                          Routing(routing), tmp_path / str(expected), specs={"critic": SPEC}, sleep=lambda s: None)
        rt.run("a/1", "critic", {"x": 1}, timeout_s=60)
        assert seen[-1] == expected
