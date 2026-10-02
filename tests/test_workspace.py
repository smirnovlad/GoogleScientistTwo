"""Versions are what the engine reads, commits and exports OUTSIDE the sandbox, so nothing an agent
leaves in one may lead the engine to a file outside it (Codex review 2026-10-02, P1)."""
import os
import subprocess

from scientisttwo.stages.manuscript import (manuscript_text, read_regular, tables_edited,
                                            write_results)
from scientisttwo.workspace import Workspaces, unsafe_entries


def version(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "run.py").write_text("print('hi')\n")
    ws = Workspaces(tmp_path / "run")
    ws.init_from(src, "base", "base")
    return ws


def tracked(ws, name):
    out = subprocess.run(["git", "-C", str(ws.path(name)), "ls-files"], capture_output=True, text=True)
    return set(out.stdout.split())


def test_finalize_removes_what_leads_outside_and_keeps_the_rest(tmp_path):
    ws = version(tmp_path)
    secret = tmp_path / "secret.txt"
    secret.write_text("SECRET")
    tmp = ws.fresh("base", "v1")
    os.symlink(secret, tmp / "absolute")                       # absolute: leaves the version
    os.symlink("../../../secret.txt", tmp / "relative")        # relative, but resolves outside
    os.symlink("run.py", tmp / "inside")                       # stays inside: harmless, kept
    os.link(secret, tmp / "hard")                              # shares the outside file's contents
    os.mkfifo(tmp / "fifo")                                    # reading it would block the engine
    (tmp / "sub").mkdir()
    os.symlink("..", tmp / "sub" / "up")                       # the version's own root: kept
    found = {e["path"]: e["kind"] for e in unsafe_entries(tmp)}
    assert found == {"absolute": "symlink", "relative": "symlink", "hard": "hardlink", "fifo": "special"}
    ws.finalize(tmp, "v1", "v1")
    v1 = ws.path("v1")
    assert not any(os.path.lexists(v1 / p) for p in found)    # removed: the links, not their targets
    assert secret.read_text() == "SECRET"
    assert {"run.py", "inside", "sub/up"} <= tracked(ws, "v1") and not tracked(ws, "v1") & set(found)
    assert "Removed by the engine" in subprocess.run(
        ["git", "-C", str(v1), "log", "-1", "--format=%B"], capture_output=True, text=True).stdout
    assert unsafe_entries(v1) == []


def test_the_export_is_the_commit_not_the_working_tree(tmp_path):
    ws = version(tmp_path)
    tmp = ws.fresh("base", "v1")
    (tmp / "run.py").write_text("print('committed')\n")
    ws.finalize(tmp, "v1", "v1")
    v1 = ws.path("v1")
    (v1 / "run.py").write_text("print('written after the commit')\n")   # never scored
    (v1 / "untracked.txt").write_text("x")
    (v1 / "__pycache__").mkdir()
    (v1 / "__pycache__" / "run.cpython.pyc").write_bytes(b"\0")
    os.symlink(tmp_path / "src", v1 / "link-added-later")
    ws.export("v1", tmp_path / "out")
    assert sorted(p.name for p in (tmp_path / "out").iterdir()) == ["run.py"]
    assert (tmp_path / "out" / "run.py").read_text() == "print('committed')\n"


def test_the_engine_neither_writes_nor_reads_through_a_writers_link(tmp_path):
    folder, victim, secret = tmp_path / "paper", tmp_path / "victim.txt", tmp_path / "secret.txt"
    folder.mkdir()
    victim.write_text("VICTIM")
    secret.write_text("SECRET")
    os.symlink(victim, folder / "results.tex")
    os.symlink(secret, folder / "references.bib")
    p = {"metric": "accuracy", "direction": "max", "main": [], "gain_over_baseline": None,
         "ablations": [], "rebuttal": []}
    assert tables_edited(folder, p)                            # a link where the tables go is an edit
    write_results(folder, p)
    assert victim.read_text() == "VICTIM"                      # the link was replaced, not followed
    assert not os.path.islink(folder / "results.tex") and "tabular" in (folder / "results.tex").read_text()
    assert not tables_edited(folder, p)
    (folder / "main.tex").write_text("\\input{results}\n")
    text = manuscript_text(folder, tables="TABLES")
    assert "TABLES" in text and "SECRET" not in text
    os.unlink(folder / "main.tex")
    os.symlink(secret, folder / "main.tex")
    assert "SECRET" not in manuscript_text(folder, tables="TABLES")
    assert read_regular(folder / "main.tex") is None
