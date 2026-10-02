"""Codebase versions: C_base, C_sub^h, C_full^h, C_best, C_new … (analysis §8, P-STATE-16).

Each version is a directory under `<run>/workspaces/`, a full copy of its parent with the git
history, so every change an agent made is a commit and a diff. A version is never edited in
place: a coding unit works in `<name>.tmp`, and `finalize` commits and renames it, so a crash
mid-session leaves no half-made version, and the next attempt starts from a fresh copy.

A version IS its commit. A copy is reset to its parent's commit, and the harness evaluates an
export of the commit, so nothing left in a working tree after its commit (a stray process still
writing, an uncommitted file) reaches a later version or a result (infrastructure review, I5).
Agents cannot write a version's `.git` (policies.py), so a git failure here is the machine's.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional

GIT = ["git", "-c", "user.name=scientisttwo", "-c", "user.email=engine@localhost",
       "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
IGNORE = "__pycache__/\n*.pyc\n.ipynb_checkpoints/\n"


def archive_commit(repo: Path, commit: str, dest: Path) -> None:
    """The files of `commit`, and nothing else, into `dest` (made fresh)."""
    import io
    import tarfile
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)
    r = subprocess.run([*GIT, "-C", str(repo), "archive", "--format=tar", commit], capture_output=True)
    if r.returncode != 0:
        raise WorkspaceError(f"git archive {commit} in {repo}: {r.stderr.decode(errors='replace')}")
    with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tar:
        tar.extractall(dest, filter="data")


class WorkspaceError(RuntimeError):
    """A git operation on a version failed: the machine's fault, since no agent can write `.git`."""


class Workspaces:
    def __init__(self, run_dir: Path, sub: str = "workspaces"):
        self.root = Path(run_dir) / sub
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, name: str) -> Path:
        return self.root / name

    def exists(self, name: str) -> bool:
        return (self.root / name / ".git").is_dir()

    def _git(self, ws: Path, *args: str, check: bool = True) -> str:
        r = subprocess.run([*GIT, "-C", str(ws), *args], capture_output=True, text=True)
        if check and r.returncode != 0:
            raise WorkspaceError(f"git {' '.join(args)} in {ws}: {r.stderr.strip()}")
        return r.stdout

    def init_from(self, source: Path, name: str, message: str) -> Path:
        """The first version: the task's code, as one commit."""
        if self.exists(name):
            return self.path(name)
        tmp = self.root / f"{name}.tmp"
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.copytree(source, tmp, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        (tmp / ".gitignore").write_text(IGNORE)
        self._git(tmp, "init", "-q")
        self._git(tmp, "add", "-A")
        self._git(tmp, "commit", "-q", "-m", message)
        tmp.rename(self.path(name))
        return self.path(name)

    def fresh(self, parent: str, name: str) -> Path:
        """A writable copy of `parent`, to become version `name` once finalised."""
        if not self.exists(parent):
            raise FileNotFoundError(f"no workspace {parent!r}")
        tmp = self.root / f"{name}.tmp"
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.copytree(self.path(parent), tmp, symlinks=True)
        self._git(tmp, "reset", "-q", "--hard", "HEAD")      # exactly the parent's commit
        self._git(tmp, "clean", "-q", "-fdx")
        return tmp

    def finalize(self, tmp: Path, name: str, message: str) -> str:
        """Commit everything in `tmp` and make it version `name`. Returns the commit."""
        self._git(tmp, "add", "-A")
        self._git(tmp, "commit", "-q", "--allow-empty", "-m", message)
        sha = self._git(tmp, "rev-parse", "HEAD").strip()
        final = self.path(name)
        shutil.rmtree(final, ignore_errors=True)
        tmp.rename(final)
        return sha

    def commit(self, name: str) -> str:
        return self._git(self.path(name), "rev-parse", "HEAD").strip()

    def diff(self, name: str, base_commit: str, stat_only: bool = False,
             max_chars: Optional[int] = None) -> str:
        args = ["diff", "--stat"] if stat_only else ["diff"]
        out = self._git(self.path(name), *args, base_commit, "HEAD", "--", ".", ":(exclude).gitignore")
        if max_chars is not None and len(out) > max_chars:
            out = out[:max_chars] + f"\n[... diff truncated, {len(out) - max_chars} more characters]"
        return out

    def added(self, name: str, base_commit: str) -> tuple[str, list[dict]]:
        """What version `name` adds since `base_commit`: the added lines, and the added or changed
        files with their size and whether git sees them as binary."""
        ws = self.path(name)
        lines = [l[1:] for l in self._git(ws, "diff", "-U0", base_commit, "HEAD").splitlines()
                 if l.startswith("+") and not l.startswith("+++")]
        files = []
        for row in self._git(ws, "diff", "--numstat", "--diff-filter=AM", base_commit, "HEAD").splitlines():
            added, _, path = row.split("\t", 2)
            target = ws / path
            files.append({"path": path, "binary": added == "-",
                          "bytes": target.stat().st_size if target.exists() else 0})
        return "\n".join(lines), files

    def archive(self, name: str, commit: str, dest: Path) -> None:
        archive_commit(self.path(name), commit, dest)

    def export(self, name: str, dest: Path) -> None:
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(self.path(name), dest, ignore=shutil.ignore_patterns(".git", "__pycache__"))
