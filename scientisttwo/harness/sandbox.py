"""The sandbox: what a process may read and write, enforced by the OS.

On macOS this is `sandbox-exec` with a generated profile. Rules are "last match wins", which the
profile below relies on: deny all writes, allow the writable paths, then deny the read-only and
the denied paths again (checked 2026-10-02, DEVELOPMENT_PROCESS.md).

⛔ WHY NOT trust a prompt ("do not read the labels"): CLAUDE.md requires integrity enforced by the
setup. A probe showed a coding agent inside this profile gets "Operation not permitted" on the
labels and on writes outside its workspace, while still running on the subscription.
"""
from __future__ import annotations

import os
import platform
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence


class SandboxUnavailable(RuntimeError):
    pass


# Secrets an agent never needs. Denied to every sandboxed process, for reading and writing.
SENSITIVE_HOME_DIRS = (".ssh", ".aws", ".gnupg", ".config/gh", ".netrc", ".docker", ".kube")


# Every run keeps its locked harness in a directory of this name. Every profile denies all of
# them, any run's, so an agent of one run cannot read the labels pinned by another.
LOCKED_DIRNAME = ".locked-harness"


@dataclass(frozen=True)
class SandboxPolicy:
    """What a sandboxed process may touch. Later rules win, in this order:

    writes:  temp roots → `protected` (none, even under a temp root) → `writable` (re-opened
             inside a protected path) → `readonly` (never written)
    reads:   everything → `hidden` (not read) → `visible` (re-opened inside a hidden path)
    both:    `denied`, the sensitive home directories and every run's LOCKED_DIRNAME: never
             read, never written
    """
    writable: tuple[Path, ...] = ()
    readonly: tuple[Path, ...] = ()
    denied: tuple[Path, ...] = ()
    protected: tuple[Path, ...] = ()      # e.g. the run directory: its store and results
    hidden: tuple[Path, ...] = ()         # e.g. the directory holding every run
    visible: tuple[Path, ...] = ()        # e.g. this run, inside it
    network: bool = True
    claude_state: bool = False            # allow writes to Claude Code's own state (agent sessions)

    @staticmethod
    def build(writable: Iterable[Path] = (), readonly: Iterable[Path] = (),
              denied: Iterable[Path] = (), network: bool = True, claude_state: bool = False,
              protected: Iterable[Path] = (), hidden: Iterable[Path] = (),
              visible: Iterable[Path] = ()) -> "SandboxPolicy":
        r = lambda ps: tuple(_real(p) for p in ps)          # noqa: E731
        return SandboxPolicy(r(writable), r(readonly), r(denied), r(protected), r(hidden),
                             r(visible), network, claude_state)


def _real(p: Path | str) -> Path:
    # sandbox-exec matches resolved paths: /tmp is /private/tmp on macOS
    return Path(os.path.realpath(os.path.expanduser(str(p))))


def _q(p: Path | str) -> str:
    s = str(p)
    if "\n" in s:
        raise ValueError(f"path with a newline cannot go into a sandbox profile: {s!r}")
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def available() -> bool:
    return platform.system() == "Darwin" and shutil.which("sandbox-exec") is not None


def _subpaths(paths: Iterable[Path]) -> str:
    return " ".join(f"(subpath {_q(p)})" for p in paths)


def profile(policy: SandboxPolicy) -> str:
    home = _real(Path.home())
    temp_roots = [Path("/private/tmp"), Path("/private/var/folders"), Path("/dev")]
    lines = ["(version 1)", "(allow default)", "(deny file-write*)"]
    extra = ""
    if policy.claude_state:
        # Claude Code writes its state, its config file and caches; OAuth goes through securityd
        claude_json = re.escape(str(home / ".claude.json"))
        extra = (f" (subpath {_q(home / '.claude')}) (regex #\"^{claude_json}\")"
                 f" (subpath {_q(home / 'Library' / 'Caches')})")
    lines.append(f"(allow file-write* {_subpaths(temp_roots)}{extra})")
    if policy.protected:
        lines.append(f"(deny file-write* {_subpaths(policy.protected)})")
    if policy.writable:
        lines.append(f"(allow file-write* {_subpaths(policy.writable)})")
    if policy.readonly:
        lines.append(f"(deny file-write* {_subpaths(policy.readonly)})")
    if policy.hidden:
        lines.append(f"(deny file-read* {_subpaths(policy.hidden)})")
        if policy.visible:
            lines.append(f"(allow file-read* {_subpaths(policy.visible)})")
    denied = [*policy.denied, *(home / d for d in SENSITIVE_HOME_DIRS)]
    locked = "/" + LOCKED_DIRNAME.replace(".", "\\.")          # only the dot needs escaping
    lines.append(f"(deny file-read* file-write* {_subpaths(denied)} (regex #\"{locked}(/|$)\"))")
    if not policy.network:
        lines.append("(deny network*)")
    return "\n".join(lines)


def wrap(argv: Sequence[str], policy: SandboxPolicy | None, allow_unsandboxed: bool = False) -> list[str]:
    """Prefix argv with sandbox-exec. Without a sandbox, refuse unless explicitly allowed."""
    if policy is None:
        return list(argv)
    if not available():
        if allow_unsandboxed:
            return list(argv)
        raise SandboxUnavailable(
            "sandbox-exec is not available on this machine; the harness cannot lock the labels. "
            "Pass --allow-unsandboxed to run anyway (integrity is then NOT enforced).")
    return ["sandbox-exec", "-p", profile(policy), *argv]
