"""The sandbox: what a process may read, write and reach, enforced by the OS.

On macOS this is `sandbox-exec` with a generated profile. Rules are "last match wins", which the
profile below relies on.

Reads under $HOME are an ALLOWLIST. The home directory holds every copy of every dataset the user
has (conda environments, package caches, other worktrees, other runs), and a denylist of them
cannot be complete: the integrity review of 2026-10-02 read one of 9 un-denied copies of the
digits data from inside the evaluation sandbox and scored 1.0 on the test split. Outside $HOME
the system is readable, minus the task's deny patterns.

⛔ WHY NOT trust a prompt ("do not read the labels"): CLAUDE.md requires integrity enforced by the
setup. ⛔ WHY NOT deny `file-read*` under $HOME: resolving a path stats every parent directory,
so metadata stays readable and only file CONTENTS (`file-read-data`, which includes listing a
directory) are denied outside the allowlist.
"""
from __future__ import annotations

import os
import platform
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence


class SandboxUnavailable(RuntimeError):
    pass


# Secrets no process needs. Denied for reading and writing, even if an allowlist names a parent.
SENSITIVE_HOME_DIRS = (".ssh", ".aws", ".gnupg", ".config/gh", ".netrc", ".docker", ".kube")

# Every run keeps its locked harness in a directory of this name. Every profile denies all of
# them, any run's, so an agent of one run cannot read the labels pinned by another.
LOCKED_DIRNAME = ".locked-harness"
LOCKED_PATTERN = "/" + LOCKED_DIRNAME.replace(".", "\\.") + "(/|$)"

# Shared temporary directories: every process may write there, so evaluated code must not read
# from them, or a result could depend on a file outside its commit (infrastructure review, I11).
TEMP_ROOTS = (Path("/private/tmp"), Path("/private/var/folders"))
NETWORK_MODES = ("none", "proxy", "open")


@dataclass(frozen=True)
class SandboxPolicy:
    """What a sandboxed process may touch. Later rules win, in this order:

    reads:    everything outside $HOME → under $HOME, only `readable` and `writable`
              → not the temp roots when `temp_read` is off, except `readable` and `writable`
    writes:   /dev → the temp roots when `temp_write` → not `protected` (e.g. the run directory,
              even under a temp root) → `writable` → not `readonly` (e.g. a workspace's .git)
    never:    `denied`, the sensitive home directories, and any path matching `deny_patterns`
    network:  "none"; "proxy", only to the egress proxy on 127.0.0.1:`proxy_port`; or "open"
    """
    writable: tuple[Path, ...] = ()
    readable: tuple[Path, ...] = ()
    readonly: tuple[Path, ...] = ()
    protected: tuple[Path, ...] = ()
    denied: tuple[Path, ...] = ()
    deny_patterns: tuple[str, ...] = ()
    network: str = "none"
    proxy_port: int = 0
    temp_read: bool = True
    temp_write: bool = True
    home: Optional[Path] = None

    def __post_init__(self) -> None:
        if self.network not in NETWORK_MODES:
            raise ValueError(f"network must be one of {NETWORK_MODES}, not {self.network!r}")
        if self.network == "proxy" and not self.proxy_port:
            raise ValueError("network 'proxy' needs the proxy's port")
        for p in self.deny_patterns:
            if '"' in p or "\n" in p:
                raise ValueError(f"a deny pattern cannot hold a quote or a newline: {p!r}")

    @staticmethod
    def build(writable: Iterable[Path] = (), readable: Iterable[Path] = (),
              readonly: Iterable[Path] = (), protected: Iterable[Path] = (),
              denied: Iterable[Path] = (), deny_patterns: Iterable[str] = (),
              network: str = "none", proxy_port: int = 0, temp_read: bool = True,
              temp_write: bool = True, home: Optional[Path] = None) -> "SandboxPolicy":
        r = lambda ps: tuple(dict.fromkeys(_real(p) for p in ps))          # noqa: E731
        return SandboxPolicy(r(writable), r(readable), r(readonly), r(protected), r(denied),
                             tuple(deny_patterns), network, proxy_port, temp_read, temp_write,
                             _real(home) if home else None)


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


def _paths(paths: Iterable[Path]) -> str:
    """A path matches itself and everything under it; a file is matched literally."""
    out = []
    for p in paths:
        out.append(f"(subpath {_q(p)})" if not p.is_file() else f"(literal {_q(p)})")
    return " ".join(out)


def profile(policy: SandboxPolicy) -> str:
    home = policy.home or _real(Path.home())
    lines = ["(version 1)", "(allow default)"]
    reads = [*policy.readable, *policy.writable]
    lines.append(f"(deny file-read-data (subpath {_q(home)}))")
    if reads:
        lines.append(f"(allow file-read-data {_paths(reads)})")
    if not policy.temp_read:
        lines.append(f"(deny file-read-data {_paths(TEMP_ROOTS)})")
        if reads:
            lines.append(f"(allow file-read-data {_paths(reads)})")
    lines.append("(deny file-write*)")
    lines.append(f"(allow file-write* {_paths([Path('/dev'), *(TEMP_ROOTS if policy.temp_write else ())])})")
    if policy.protected:
        lines.append(f"(deny file-write* {_paths(policy.protected)})")
    if policy.writable:
        lines.append(f"(allow file-write* {_paths(policy.writable)})")
    if policy.readonly:
        lines.append(f"(deny file-write* {_paths(policy.readonly)})")
    denied = [*policy.denied, *(home / d for d in SENSITIVE_HOME_DIRS)]
    patterns = " ".join(f'(regex #"{p}")' for p in (LOCKED_PATTERN, *policy.deny_patterns))
    # `file-read-data` by name: a wildcard deny does not override a specific allow of the same
    # operation (probe of 2026-10-02: a deny pattern inside an allowed Python prefix still read)
    lines.append(f"(deny file-read* file-read-data file-write* {_paths(denied)} {patterns})")
    if policy.network == "none":
        lines.append("(deny network*)")
    elif policy.network == "proxy":
        lines.append("(deny network-outbound)")
        lines.append(f'(allow network-outbound (remote ip "localhost:{int(policy.proxy_port)}"))')
    return "\n".join(lines)


def wrap(argv: Sequence[str], policy: SandboxPolicy | None, allow_unsandboxed: bool = False) -> list[str]:
    """Prefix argv with sandbox-exec. Without a sandbox, refuse unless explicitly allowed."""
    if policy is None:
        if allow_unsandboxed:
            return list(argv)
        raise SandboxUnavailable("a process was about to start with no sandbox policy")
    if not available():
        if allow_unsandboxed:
            return list(argv)
        raise SandboxUnavailable(
            "sandbox-exec is not available on this machine; the harness cannot lock the labels. "
            "Pass --allow-unsandboxed to run anyway (integrity is then NOT enforced).")
    return ["sandbox-exec", "-p", profile(policy), *argv]


def child_env(python: str, extra: Optional[dict[str, str]] = None) -> dict[str, str]:
    """The allowlisted environment of every sandboxed process: nothing of the launching
    session's environment passes except these names (no API key, no base URL, no proxy)."""
    home = str(Path.home())
    path = [str(Path(python).parent), str(Path(home) / ".local" / "bin"), "/opt/homebrew/bin",
            "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin", "/Library/TeX/texbin"]
    env = {"HOME": home, "USER": os.environ.get("USER", ""), "LOGNAME": os.environ.get("USER", ""),
           "SHELL": "/bin/zsh" if Path("/bin/zsh").exists() else "/bin/sh",
           "LANG": os.environ.get("LANG", "en_US.UTF-8"), "TERM": "xterm-256color",
           "PATH": os.pathsep.join(dict.fromkeys(path))}
    if os.environ.get("TMPDIR"):
        env["TMPDIR"] = os.environ["TMPDIR"]
    env.update(extra or {})
    return env
