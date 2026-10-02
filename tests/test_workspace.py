"""Versions are what the engine reads, commits and exports OUTSIDE the sandbox, so nothing an agent
leaves in one may lead the engine to a file outside it (Codex review 2026-10-02, P1)."""
import os
import shutil
import subprocess
import sys
import time

import pytest

from scientisttwo.harness import sandbox as sbx
from scientisttwo.harness.policies import RunRules, python_read_paths
from scientisttwo.stages import manuscript
from scientisttwo.stages.manuscript import (compile_pdf, manuscript_text, read_regular, tables_edited,
                                            write_results)
from scientisttwo.workspace import IGNORE, PAPER_IGNORE, Workspaces, unsafe_entries


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
    os.unlink(folder / "main.tex")
    (folder / "main.tex").mkdir()                              # a directory in its place
    assert read_regular(folder / "main.tex") is None and "missing" in manuscript_text(folder, tables="T")



# ---- the PDF build ------------------------------------------------------------------------------
PAPER = (r"\documentclass{article}\begin{document}" "\n"
         r"Results in Table~\ref{tab:main}, after \cite{knuth1984}." "\n"
         r"\input{results}" "\n" r"\bibliographystyle{plain}\bibliography{references}" "\n"
         r"\end{document}" "\n")
BIBTEX = "@book{knuth1984, title={The TeXbook}, author={Knuth, Donald E.}, year={1984}, publisher={Addison-Wesley}}\n"


@pytest.mark.skipif(not sbx.available() or shutil.which("latexmk") is None
                    and not os.path.exists("/Library/TeX/texbin/latexmk"), reason="needs sandbox-exec and latexmk")
def test_a_paper_with_a_bibliography_builds_in_the_sandbox(tmp_path):
    """Run 2's every PDF failed: bibtex writes beside its sources, and the build could write only
    to a separate directory ("Not writing to /Use.bbl"). The build now compiles a copy."""
    src = tmp_path / "run" / "builds" / "v1"
    src.mkdir(parents=True)
    (src / "main.tex").write_text(PAPER)
    (src / "references.bib").write_text(BIBTEX)
    (src / "results.tex").write_text("\\begin{table}\\caption{Main}\\label{tab:main}x\\end{table}\n")
    # a writer's latexmkrc is Perl that latexmk would run: here it swaps the PDF for a link
    (src / ".latexmkrc").write_text("END { system('rm -f main.pdf; ln -s /etc/hosts main.pdf'); }\n")
    rules = RunRules(run_dir=tmp_path / "run", denied=(), deny_patterns=(), public=tmp_path / "public",
                     python=tuple(python_read_paths()))
    report = compile_pdf(src, rules.build(src), allow_unsandboxed=False)
    assert report["ok"], report.get("error")
    assert "Knuth" in (src / "main.bbl").read_text()
    assert not os.path.islink(src / "main.pdf")                # -norc: the rc file never ran


def test_a_pdf_the_build_left_as_a_link_is_not_a_pdf(tmp_path, monkeypatch):
    """Codex review 2, P1: the engine copied main.pdf outside the sandbox, following a link."""
    secret = tmp_path / "secret.txt"
    secret.write_text("SECRET")
    fake = tmp_path / "latexmk"
    fake.write_text(f"#!/bin/sh\nln -s {secret} main.pdf\nexit 0\n")
    fake.chmod(0o755)
    monkeypatch.setattr(manuscript.shutil, "which", lambda name: str(fake))
    src = tmp_path / "build"
    src.mkdir()
    assert compile_pdf(src, None, allow_unsandboxed=True)["ok"] is False


def test_a_hung_build_dies_with_its_whole_tree(tmp_path, monkeypatch):
    """Codex review, P2: `subprocess.run(timeout=)` killed only latexmk, never the TeX it started."""
    beat, tex = tmp_path / "beat.txt", tmp_path / "tex.py"
    tex.write_text("import time\nwhile True:\n"
                   f"    open({str(beat)!r}, 'a').write('b')\n    time.sleep(0.1)\n")
    fake = tmp_path / "latexmk"
    fake.write_text(f"#!{sys.executable}\nimport os, subprocess, sys, time\n"
                    f"subprocess.Popen([sys.executable, {str(tex)!r}], start_new_session=True)\n"
                    f"while not os.path.exists({str(beat)!r}):\n    time.sleep(0.05)\n"   # it runs
                    "time.sleep(30)\n")
    fake.chmod(0o755)
    monkeypatch.setattr(manuscript.shutil, "which", lambda name: str(fake))
    src = tmp_path / "build"
    src.mkdir()
    started = time.time()
    report = compile_pdf(src, None, allow_unsandboxed=True, timeout=5.0)
    assert report == {"ok": False, "error": "latexmk timed out"} and time.time() - started < 15
    size = beat.stat().st_size
    time.sleep(0.5)
    assert beat.stat().st_size == size                       # the detached TeX stand-in is dead



def test_a_paper_version_keeps_latexs_outputs_out(tmp_path):
    """Run 3 exported a writer's main.aux, main.bbl, main.log and main.out; run 2 a writer's PDF."""
    src = tmp_path / "seed"
    src.mkdir()
    (src / "main.tex").write_text("x")
    papers = Workspaces(tmp_path / "run", "manuscripts", ignore=IGNORE + PAPER_IGNORE)
    papers.init_from(src, "p0", "p0")
    tmp = papers.fresh("p0", "p1")
    for name in ("main.aux", "main.bbl", "main.log", "main.out", "main.pdf"):
        (tmp / name).write_text("built")
    (tmp / "figures").mkdir()
    (tmp / "figures" / "plot.pdf").write_text("a figure")
    papers.finalize(tmp, "p1", "p1")
    papers.export("p1", tmp_path / "out")
    assert sorted(str(p.relative_to(tmp_path / "out")) for p in (tmp_path / "out").rglob("*") if p.is_file()) \
        == ["figures/plot.pdf", "main.tex"]
