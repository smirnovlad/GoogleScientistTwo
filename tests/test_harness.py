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
        f"y = np.load({str(target)!r})['y']\n"
        "np.save(a.out, y)\n")
    ws.finalize(tmp, "cheat", "cheat")
    r = h.evaluate("c", ws.path("cheat"), "full")
    assert r["status"] == "failed"
    assert "Operation not permitted" in r["log_tail"] or "PermissionError" in r["log_tail"]


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
        f"os.makedirs(os.path.dirname({str(path)!r}), exist_ok=True)\n"
        f"open({str(path)!r}, 'w').write('{{\"mean\": 1.0}}')\n")
    ws.finalize(tmp, "escape", "escape")
    before = path.read_text() if path.exists() else None
    r = h.evaluate("e", ws.path("escape"), "subset")
    assert r["status"] == "failed" and "Operation not permitted" in r["log_tail"]
    assert (path.read_text() if path.exists() else None) == before


@needs_sandbox
def test_agent_code_cannot_reach_the_network(tmp_path):
    pol = sbx.SandboxPolicy.build(writable=[tmp_path], network=False)
    import subprocess
    out = subprocess.run(sbx.wrap(["/usr/bin/curl", "-s", "-m", "5", "https://example.com"], pol),
                         capture_output=True, text=True)
    assert out.returncode != 0


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


# ---- the holes the digits task's builder found (2026-10-02), each closed by mechanism ----------
CHEAT = ("import argparse, numpy as np\n"
         "ap = argparse.ArgumentParser(); [ap.add_argument(a) for a in ('--train-dir','--inputs','--out','--seed')]\n"
         "a = ap.parse_args()\n"
         "y = np.load({path!r})['y']\n"
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
    assert r["status"] == "failed" and "Operation not permitted" in r["log_tail"]


@needs_sandbox
def test_another_runs_locked_labels_are_unreadable(toy_task, tmp_path):
    task, run, h, ws = setup(toy_task, tmp_path)
    other = Harness(task, tmp_path / "other-run")
    other.install()
    r = cheat_run(h, ws, "other", other.locked / "labels" / "full.npz")
    assert r["status"] == "failed" and "Operation not permitted" in r["log_tail"]


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
    assert r["status"] == "failed" and "Operation not permitted" in r["log_tail"]
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
    assert r["status"] == "failed" and "Operation not permitted" in r["log_tail"]


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
