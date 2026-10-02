"""The locked harness and the sandbox: integrity enforced by the setup (CLAUDE.md)."""
import json
import os
import shutil
from pathlib import Path

import pytest

from scientisttwo.harness import sandbox as sbx
from scientisttwo.harness.harness import Harness, HarnessTampered, gain, strictly_better
from scientisttwo.task import TaskError, load_task
from scientisttwo.workspace import Workspaces

needs_sandbox = pytest.mark.skipif(not sbx.available(), reason="sandbox-exec is macOS only")


def probe(op: str, indent: str = "") -> str:
    """Python lines that run `op` and print whether the sandbox denied it. A test asserts the
    child got this far, so a sandbox that failed to start (`sandbox_apply: Operation not
    permitted`, as in Codex's review environment) never passes for one that denied the operation
    (Codex review 2026-10-02, P2)."""
    lines = ["print('PROBE-REACHED', flush=True)", "try:", f"    {op}", "    print('PROBE-ALLOWED', flush=True)",
             "except PermissionError as e:", "    print('PROBE-DENIED', e, flush=True)", "    raise SystemExit(3)"]
    return "".join(f"{indent}{line}\n" for line in lines)


def denied(text: str) -> bool:
    return "PROBE-REACHED" in text and "PROBE-DENIED" in text and "PROBE-ALLOWED" not in text


def setup(toy_task, tmp_path):
    task = load_task(toy_task)
    run = tmp_path / "run"
    h = Harness(task, run)
    h.install()
    ws = Workspaces(run)
    ws.init_from(task.code_dir, "base", "base")
    return task, run, h, ws


def test_baseline_is_scored_by_the_harness(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    r = h.evaluate("base-full", ws.path("base"), "full")
    assert r["status"] == "ok" and r["n_seeds"] == 2
    assert 0.7 < r["mean"] < 0.9                     # threshold 0.5 on labels x > 0.3
    assert h.evaluate("base-full", ws.path("base"), "full") == r      # memoised by key


def test_a_better_version_gains(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    base = h.evaluate("b", ws.path("base"), "full")
    tmp = ws.fresh("base", "idea")
    (tmp / "params.json").write_text(json.dumps({"threshold": 0.3}))
    ws.finalize(tmp, "idea", "idea")
    new = h.evaluate("i", ws.path("idea"), "full")
    assert new["mean"] == 1.0
    assert gain(new, base) > 0.1 and strictly_better(new, base)
    assert not strictly_better(base, new)


def test_a_crash_is_a_failed_result(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    tmp = ws.fresh("base", "broken")
    (tmp / "run.py").write_text("raise SystemExit('boom')\n")
    ws.finalize(tmp, "broken", "broken")
    r = h.evaluate("x", ws.path("broken"), "subset")
    assert r["status"] == "failed" and "exit code" in r["error"] and "boom" in r["log_tail"]
    assert gain(r, r) is None


def test_tampering_with_the_labels_stops_the_run(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    label = h.locked / "labels" / "full.npz"
    os.chmod(label, 0o644)
    label.write_bytes(label.read_bytes() + b"\0")
    with pytest.raises(HarnessTampered):
        h.evaluate("y", ws.path("base"), "full")


@needs_sandbox
def test_agent_code_cannot_read_the_labels(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    tmp = ws.fresh("base", "cheat")
    target = h.locked / "labels" / "full.npz"
    (tmp / "run.py").write_text(
        "import argparse, numpy as np\n"
        "ap = argparse.ArgumentParser(); [ap.add_argument(a) for a in ('--train-dir','--inputs','--out','--seed')]\n"
        "a = ap.parse_args()\n"
        + probe(f"y = np.load({str(target)!r})['y']") +
        "np.save(a.out, y)\n")
    ws.finalize(tmp, "cheat", "cheat")
    r = h.evaluate("c", ws.path("cheat"), "full")
    assert r["status"] == "failed" and denied(r["log_tail"])


@needs_sandbox
@pytest.mark.parametrize("target", ["forged_result", "other_version", "home"])
def test_agent_code_cannot_forge_results_or_write_outside(toy_task, tmp_path, target):
    """The run lives under a temp root here, as tmp_path does: the run directory is still protected."""
    task, run, h, ws = setup(toy_task, tmp_path)
    path = {"forged_result": run / "results" / "future-eval.json",
            "other_version": ws.path("base") / "params.json",
            "home": Path.home() / ".scientisttwo_sandbox_probe"}[target]
    tmp = ws.fresh("base", "escape")
    (tmp / "run.py").write_text(
        "import argparse, os\n"
        "ap = argparse.ArgumentParser(); [ap.add_argument(a) for a in ('--train-dir','--inputs','--out','--seed')]\n"
        "a = ap.parse_args()\n"
        + probe(f"os.makedirs(os.path.dirname({str(path)!r}), exist_ok=True); "
                f"open({str(path)!r}, 'w').write('{{\"mean\": 1.0}}')"))
    ws.finalize(tmp, "escape", "escape")
    before = path.read_text() if path.exists() else None
    r = h.evaluate("e", ws.path("escape"), "subset")
    assert r["status"] == "failed" and denied(r["log_tail"])
    assert (path.read_text() if path.exists() else None) == before


@needs_sandbox
def test_agent_code_cannot_reach_the_network(tmp_path):
    pol = sbx.SandboxPolicy.build(writable=[tmp_path], readable=python_read_paths(), network="none")
    out = run_in(pol, "import socket\n" + probe("socket.create_connection(('1.1.1.1', 443), timeout=3)"), tmp_path)
    assert denied(out.stdout)


def test_unsandboxed_is_refused_unless_allowed(monkeypatch):
    monkeypatch.setattr(sbx, "available", lambda: False)
    pol = sbx.SandboxPolicy.build(writable=["/tmp"])
    with pytest.raises(sbx.SandboxUnavailable):
        sbx.wrap(["true"], pol)
    assert sbx.wrap(["true"], pol, allow_unsandboxed=True) == ["true"]


def test_task_validation(toy_task):
    task = load_task(toy_task)
    assert task.splits["full"].seeds == (0, 1) and task.direction == "max"
    d = json.loads((toy_task / "task.json").read_text())
    d["splits"]["test"]["labels"] = "data/public/train.npz"          # labels outside harness/
    (toy_task / "task.json").write_text(json.dumps(d))
    with pytest.raises(TaskError):
        load_task(toy_task)


def test_a_test_seed_is_never_a_search_seed(toy_task):
    """Task 6, blocker B1: shared seeds carry the selection's training luck into the test number."""
    d = json.loads((toy_task / "task.json").read_text())
    d["splits"]["test"]["seeds"] = [1, 7]                            # 1 is a `full` seed
    (toy_task / "task.json").write_text(json.dumps(d))
    with pytest.raises(TaskError, match=r"shared: \[1\]"):
        load_task(toy_task)
    d["splits"]["test"]["seeds"] = [7, 8]
    (toy_task / "task.json").write_text(json.dumps(d))
    assert load_task(toy_task).splits["test"].seeds == (7, 8)


# ---- the holes the digits task's builder found (2026-10-02), each closed by mechanism ----------
CHEAT = ("import argparse, numpy as np\n"
         "ap = argparse.ArgumentParser(); [ap.add_argument(a) for a in ('--train-dir','--inputs','--out','--seed')]\n"
         "a = ap.parse_args()\n"
         + probe("y = np.load({path!r})['y']") +
         "np.save(a.out, y)\n")


def cheat_run(h, ws, name, path):
    tmp = ws.fresh("base", name)
    (tmp / "run.py").write_text(CHEAT.format(path=str(path)))
    ws.finalize(tmp, name, name)
    return h.evaluate(name, ws.path(name), "full")


@needs_sandbox
def test_the_tasks_own_labels_are_unreadable(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    r = cheat_run(h, ws, "own", toy_task / "harness" / "labels" / "full.npz")
    assert r["status"] == "failed" and denied(r["log_tail"])


@needs_sandbox
def test_another_runs_locked_labels_are_unreadable(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    other = Harness(task, tmp_path / "other-run")
    other.install()
    r = cheat_run(h, ws, "other", other.locked / "labels" / "full.npz")
    assert r["status"] == "failed" and denied(r["log_tail"])


@needs_sandbox
def test_sibling_runs_are_hidden_in_a_runs_folder(toy_task, tmp_path):
    task = load_task(toy_task)
    runs = tmp_path / "runs"
    sibling = runs / "earlier"
    (sibling / "export").mkdir(parents=True)
    leak = sibling / "export" / "results.npz"
    import numpy as np
    np.savez(leak, y=np.zeros(300, dtype=np.int64))
    h = Harness(task, runs / "now")
    h.install()
    ws = Workspaces(runs / "now")
    ws.init_from(task.code_dir, "base", "base")
    r = cheat_run(h, ws, "sib", leak)
    assert r["status"] == "failed" and denied(r["log_tail"])
    assert h.evaluate("ok", ws.path("base"), "full")["status"] == "ok"      # its own run still works


@needs_sandbox
def test_declared_extra_paths_are_unreadable(toy_task, tmp_path):
    """The stand-in for scikit-learn's bundled digits, which hold every evaluation label."""
    vault = tmp_path / "site-packages-copy"
    vault.mkdir()
    import numpy as np
    np.savez(vault / "digits.npz", y=np.zeros(300, dtype=np.int64))
    d = json.loads((toy_task / "task.json").read_text())
    d["deny_read"] = [str(vault)]
    (toy_task / "task.json").write_text(json.dumps(d))
    task, run, h, ws = setup(toy_task, tmp_path)
    r = cheat_run(h, ws, "vault", vault / "digits.npz")
    assert r["status"] == "failed" and denied(r["log_tail"])


def _ctx_for_checks(toy_task, tmp_path, **task_fields):
    from scientisttwo.stages.common import Ctx
    d = json.loads((toy_task / "task.json").read_text())
    d.update(task_fields)
    (toy_task / "task.json").write_text(json.dumps(d))
    task, run, h, ws = setup(toy_task, tmp_path)
    ctx = Ctx(task=task, cfg={"limits": {}}, rt=None, harness=h, ws=ws, run_dir=run)  # type: ignore[arg-type]
    ws.init_from(task.code_dir, "task", "task")
    ctx.task_commit = ws.commit("task")
    return ctx, ws


def test_a_forbidden_string_is_rejected_before_running(toy_task, tmp_path):
    ctx, ws = _ctx_for_checks(toy_task, tmp_path, forbidden_in_diff=["load_digits"])
    tmp = ws.fresh("task", "loader")
    (tmp / "run.py").write_text((tmp / "run.py").read_text() + "\n# from sklearn.datasets import load_digits\n")
    ws.finalize(tmp, "loader", "loader")
    r = ctx.evaluate("loader", "loader", "full")
    assert r["status"] == "failed" and "load_digits" in r["error"] and r["seconds"] == 0.0
    assert ctx.evaluate("clean", "task", "full")["status"] == "ok"


def test_an_added_data_file_is_rejected(toy_task, tmp_path):
    ctx, ws = _ctx_for_checks(toy_task, tmp_path)
    tmp = ws.fresh("task", "data")
    import numpy as np
    np.save(tmp / "lookup.npy", np.arange(10))
    ws.finalize(tmp, "data", "data")
    r = ctx.evaluate("data", "data", "full")
    assert r["status"] == "failed" and "lookup.npy" in r["error"]


# ---- the integrity and infrastructure reviews of 2026-10-02, each hole closed by mechanism -----
import subprocess
import sys
import time
import uuid

from scientisttwo.harness.egress import EgressProxy, host_allowed
from scientisttwo.harness.policies import RunRules, python_read_paths
from scientisttwo.runtime.procs import ProcRegistry, TreeWatcher, kill_groups, run_tree, started


def run_in(policy, code: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(sbx.wrap([sys.executable, "-c", code], policy), cwd=str(cwd),
                          capture_output=True, text=True, timeout=60)


@needs_sandbox
def test_a_dataset_copy_under_home_is_unreadable_unless_allowlisted(toy_task, tmp_path):
    """The review read one of 9 un-denied copies of the digits data in conda environments."""
    vault = Path.home() / ".cache" / f"scientisttwo-test-{uuid.uuid4().hex}"
    vault.mkdir(parents=True)
    try:
        import numpy as np
        np.savez(vault / "digits.npz", y=np.zeros(300, dtype=np.int64))
        task, run, h, ws = setup(toy_task, tmp_path)
        r = cheat_run(h, ws, "homecopy", vault / "digits.npz")
        assert r["status"] == "failed" and denied(r["log_tail"])
        assert h.evaluate("fine", ws.path("base"), "full")["status"] == "ok"    # Python itself still runs
    finally:
        shutil.rmtree(vault, ignore_errors=True)


@needs_sandbox
def test_a_deny_pattern_hides_every_copy_anywhere(toy_task, tmp_path):
    copy = tmp_path / "elsewhere" / "pkg" / "vault-data"
    copy.mkdir(parents=True)
    import numpy as np
    np.savez(copy / "labels.npz", y=np.zeros(300, dtype=np.int64))
    d = json.loads((toy_task / "task.json").read_text())
    d["deny_patterns"] = ["/vault-data(/|$)"]
    (toy_task / "task.json").write_text(json.dumps(d))
    task, run, h, ws = setup(toy_task, tmp_path)
    policy = sbx.SandboxPolicy.build(readable=[tmp_path, *python_read_paths()], deny_patterns=task.deny_patterns)
    out = run_in(policy, probe(f"open({str(copy / 'labels.npz')!r}, 'rb').read()"), tmp_path)
    assert denied(out.stdout)
    ok = run_in(policy, probe(f"open({str(toy_task / 'paper.md')!r}).read()"), tmp_path)
    assert ok.returncode == 0 and "PROBE-ALLOWED" in ok.stdout


@needs_sandbox
def test_evaluation_runs_the_commit_not_the_working_tree(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    tmp = ws.fresh("base", "v1")
    (tmp / "params.json").write_text(json.dumps({"threshold": 0.3}))
    ws.finalize(tmp, "v1", "v1")
    # after the commit, something rewrites the working tree (a stray process, by hand)
    (ws.path("v1") / "params.json").write_text(json.dumps({"threshold": 0.9}))
    r = h.evaluate("v1", ws.path("v1"), "full", commit=ws.commit("v1"))
    assert r["mean"] == 1.0
    # and a copy for the next version starts from the commit too
    child = ws.fresh("v1", "v2")
    assert json.loads((child / "params.json").read_text())["threshold"] == 0.3


@needs_sandbox
def test_one_seed_cannot_read_what_another_left(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    tmp = ws.fresh("base", "seedleak")
    (tmp / "run.py").write_text(
        "import argparse, os, pathlib, numpy as np\n"
        "ap = argparse.ArgumentParser(); [ap.add_argument(a) for a in ('--train-dir','--inputs','--out','--seed')]\n"
        "a = ap.parse_args()\n"
        "out = pathlib.Path(a.out)\n"
        "if a.seed == '1':\n"
        + probe("print(open(out.parent.parent / 'seed0' / 'note.txt').read())", indent="    ") +
        "(out.parent / 'note.txt').write_text('left by seed 0')\n"
        "np.save(a.out, np.zeros(len(np.load(a.inputs)['X']), dtype=np.int64))\n")
    ws.finalize(tmp, "seedleak", "seedleak")
    r = h.evaluate("sl", ws.path("seedleak"), "full")
    assert r["status"] == "failed" and "seed 1" in r["error"] and denied(r["log_tail"])


def _rules(tmp_path, port=0) -> RunRules:
    return RunRules(run_dir=tmp_path / "run", denied=(), deny_patterns=(), public=tmp_path / "public",
                    python=tuple(python_read_paths()), api_proxy_port=port, open_proxy_port=port)


@needs_sandbox
def test_a_coding_agent_cannot_write_its_versions_git(tmp_path):
    work = tmp_path / "run" / "workspaces" / "v.tmp"
    (work / ".git").mkdir(parents=True)
    pol = _rules(tmp_path, 1).agent("coding", ("Bash",), tmp_path / "run" / "tmp", tmp_path / "run" / "scratch", work)
    out = run_in(pol, probe("open('.git/index.lock', 'w')"), work)
    assert denied(out.stdout)
    assert run_in(pol, "open('model.py', 'w').write('x = 1')", work).returncode == 0
    assert (work / "model.py").read_text() == "x = 1"


@needs_sandbox
def test_no_agent_can_write_the_users_claude_setup_or_read_its_history(tmp_path):
    """settings, hooks and CLAUDE.md there run in the user's own, unsandboxed sessions."""
    work = tmp_path / "run" / "workspaces" / "v.tmp"
    work.mkdir(parents=True)
    pol = _rules(tmp_path, 1).agent("coding", ("Bash",), tmp_path / "run" / "tmp", tmp_path / "run" / "scratch", work)
    target = Path.home() / ".claude" / f"scientisttwo-probe-{uuid.uuid4().hex}"
    out = run_in(pol, probe(f"open({str(target)!r}, 'w')"), work)
    assert denied(out.stdout) and not target.exists()
    projects = Path.home() / ".claude" / "projects"
    if projects.exists():
        out = run_in(pol, "import os\n" + probe(f"print(os.listdir({str(projects)!r}))"), work)
        assert denied(out.stdout)


@needs_sandbox
def test_an_agent_reaches_the_proxy_and_nothing_else(tmp_path):
    proxy = EgressProxy(allow=("api.anthropic.com",), log_path=tmp_path / "egress.jsonl")
    port = proxy.start()
    try:
        work = tmp_path / "run" / "workspaces" / "v.tmp"
        work.mkdir(parents=True)
        pol = _rules(tmp_path, port).agent("coding", ("Bash",), tmp_path / "run" / "tmp",
                                           tmp_path / "run" / "scratch", work)
        direct = run_in(pol, "import socket\n" + probe("socket.create_connection(('1.1.1.1', 443), timeout=3)"), work)
        assert denied(direct.stdout)
        refused = run_in(pol, (
            "import socket; s = socket.create_connection(('127.0.0.1', %d), timeout=5);"
            "s.sendall(b'CONNECT archive.ics.uci.edu:443 HTTP/1.1\\r\\n\\r\\n');"
            "print(s.recv(100).decode())") % port, work)
        assert refused.returncode == 0 and "403" in refused.stdout
        log = [json.loads(l) for l in (tmp_path / "egress.jsonl").read_text().splitlines()]
        assert log[-1] == {**log[-1], "host": "archive.ics.uci.edu", "allowed": False}
    finally:
        proxy.stop()


@needs_sandbox
def test_a_child_that_never_ran_is_not_a_denial(tmp_path):
    """The check behind every test above can fail: a sandbox that stops the child before it
    starts prints "Operation not permitted" too, and is not taken for a denied operation."""
    out = subprocess.run(["sandbox-exec", "-p", "(version 1)(deny default)", sys.executable, "-c",
                          probe("open('/etc/hosts').read()")], capture_output=True, text=True, timeout=60)
    assert out.returncode != 0 and not denied(out.stdout + out.stderr)
    assert "PROBE-REACHED" not in out.stdout


def test_the_allowlist_matches_hosts_not_suffixes():
    allow = ("api.anthropic.com", "*.claude.ai")
    assert host_allowed("api.anthropic.com", allow) and host_allowed("x.claude.ai", allow)
    assert not host_allowed("evil-api.anthropic.com.example", allow)
    assert not host_allowed("claude.ai.example.com", allow) and not host_allowed("notclaude.ai", allow)


def test_a_hung_child_holding_the_output_cannot_hang_the_harness(tmp_path):
    """A detached grandchild kept the pipe open, and the engine waited for its whole life (I6)."""
    script = ("import subprocess, sys, time\n"
              "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'], start_new_session=True)\n"
              "time.sleep(60)\n")
    started_at = time.time()
    rc, timed_out = run_tree([sys.executable, "-c", script], cwd=tmp_path, env=dict(os.environ),
                             timeout=1.5, output=tmp_path / "log.txt", key="hang", grace=0.5)
    assert timed_out and time.time() - started_at < 10


def test_a_group_that_outlived_its_leader_is_reaped_on_resume(tmp_path):
    """Codex review, P1: a shell exits and leaves its child running in the shell's group. The
    resume looked for the group's leader, found none, and dropped the record of a live process."""
    reg = ProcRegistry(tmp_path)
    shell = subprocess.Popen(["/bin/sh", "-c", f"{sys.executable} -c 'import time; time.sleep(60)' & sleep 1; exit 0"],
                             start_new_session=True)
    watcher = TreeWatcher(shell.pid, interval=0.1,
                          on_new=lambda w: reg.record(shell.pid, "unit/c", w.groups, w.members, "no-marker")).start()
    try:
        shell.wait(timeout=5)                                   # the leader is gone; its child is not
        time.sleep(0.3)
        child = next(p for p in watcher.members if p != shell.pid)
        assert os.getpgid(child) == shell.pid
        watcher._stop.set()                                     # the engine "crashes" here
        reaped = ProcRegistry(tmp_path).reap_orphans()
        assert [r["key"] for r in reaped] == ["unit/c"]
        deadline = time.time() + 5
        while time.time() < deadline:
            try:
                os.kill(child, 0)
                time.sleep(0.05)
            except ProcessLookupError:
                break
        else:
            raise AssertionError("the orphaned child survived the resume")
    finally:
        kill_groups([shell.pid], grace=0.2)


def test_orphans_of_a_crashed_engine_are_killed_on_resume_and_only_they(tmp_path):
    victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], start_new_session=True)
    bystander = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], start_new_session=True)
    try:
        time.sleep(0.2)
        reg = ProcRegistry(tmp_path)
        reg.record(victim.pid, "unit/a", {victim.pid: started(victim.pid)})
        reg.record(bystander.pid, "unit/b", {bystander.pid: "Thu Jan  1 00:00:00 1970"})   # pid reused since
        reaped = ProcRegistry(tmp_path).reap_orphans()
        assert [r["key"] for r in reaped] == ["unit/a"]
        assert victim.wait(timeout=5) is not None and bystander.poll() is None
    finally:
        kill_groups([bystander.pid, victim.pid], grace=0.2)



def test_a_rejection_never_replays_another_commits_result(toy_task, tmp_path):
    """Codex review 2, P2: a version regenerated on resume inherited the old version's result."""
    from scientisttwo.harness.harness import StaleResult
    task, run, h, ws = setup(toy_task, tmp_path)
    h.reject("k", ws.path("base"), "full", "a rule", commit="a" * 40)
    assert h.reject("k", ws.path("base"), "full", "a rule", commit="a" * 40)["status"] == "failed"
    with pytest.raises(StaleResult):
        h.reject("k", ws.path("base"), "full", "a rule", commit="b" * 40)
