"""Which sandbox each kind of process gets, in one place.

An agent's rights follow its KIND (agent.json), not the arguments of the call that starts it
(A-INT-3; architecture review 2026-10-02, finding 8):

| process | writes | reads under $HOME (besides the rules' common reads) | network |
|---|---|---|---|
| reasoning agent | scratch, its TMPDIR | the backend's own files | the Anthropic API; any host, logged, if it has WebFetch |
| read-only agent | scratch, its TMPDIR | + the version it audits (never writable) | the Anthropic API |
| coding / writer agent | its version but not its `.git`, its TMPDIR | + the public training data | the Anthropic API, plus the task's `network_allow` hosts |
| evaluated code | its seed's directory only | the version's commit, the split's inputs, the public data, Python | none |
| LaTeX build | its build directory only | the manuscript version | none |

Every process: the run directory is never writable (results, units, ledger), and the locked
harness, the task's own folder, its `deny_read` paths and its `deny_patterns` are never readable.
"""
from __future__ import annotations

import site
import sys
import sysconfig
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .sandbox import SandboxPolicy

AGENT_KINDS = ("reasoning", "readonly", "coding", "writer")
PYTHON_SUBDIRS = ("bin", "lib", "include", "share", "ssl", "etc", "conda-meta")


def python_read_paths(python: str = sys.executable) -> list[Path]:
    """What a Python process needs to read to run with its installed packages, and no more: the
    interpreter's prefix subdirectories, never the whole prefix (a conda prefix also holds `envs/`
    and `pkgs/`, each with more copies of every dataset that ships inside a package)."""
    paths: list[Path] = [Path(python).resolve().parent]
    for prefix in dict.fromkeys([sys.prefix, sys.base_prefix, sys.exec_prefix]):
        for sub in PYTHON_SUBDIRS:
            p = Path(prefix) / sub
            if p.exists():
                paths.append(p)
    for key in ("stdlib", "platstdlib", "purelib", "platlib"):
        p = sysconfig.get_paths().get(key)
        if p and Path(p).exists():
            paths.append(Path(p))
    user_site = site.getusersitepackages() if hasattr(site, "getusersitepackages") else None
    if user_site and Path(user_site).exists():
        paths.append(Path(user_site))
    return list(dict.fromkeys(paths))


@dataclass(frozen=True)
class RunRules:
    """The run-wide facts every policy is built from."""
    run_dir: Path
    denied: tuple[Path, ...]                 # the locked harness, the task folder, task deny_read
    deny_patterns: tuple[str, ...]           # the task's, e.g. a dataset directory name anywhere
    public: Path                             # the public training data
    python: tuple[Path, ...]                 # python_read_paths()
    backend_reads: tuple[Path, ...] = ()     # what the agent CLI itself must read (its binary, auth)
    api_proxy_port: int = 0                  # the egress proxy for the Anthropic API (+ task hosts)
    open_proxy_port: int = 0                 # the logged egress for agents with WebFetch
    extra: dict = field(default_factory=dict)

    def _base(self, **kw) -> SandboxPolicy:
        return SandboxPolicy.build(protected=[self.run_dir], denied=self.denied,
                                   deny_patterns=self.deny_patterns, **kw)

    def _network(self, tools: tuple[str, ...]) -> dict:
        port = self.open_proxy_port if "WebFetch" in tools else self.api_proxy_port
        return {"network": "proxy", "proxy_port": port} if port else {"network": "open"}

    def agent(self, kind: str, tools: tuple[str, ...], tmpdir: Path, scratch: Path,
              workdir: Optional[Path] = None) -> SandboxPolicy:
        if kind not in AGENT_KINDS:
            raise ValueError(f"unknown agent kind {kind!r}")
        reads = [*self.backend_reads, *self.python, self.public]
        if kind == "reasoning":
            return self._base(writable=[scratch, tmpdir], readable=reads, **self._network(tools))
        if workdir is None:
            raise ValueError(f"a {kind} agent needs the version it works on")
        if kind == "readonly":
            return self._base(writable=[scratch, tmpdir], readable=[*reads, workdir],
                              readonly=[workdir], **self._network(tools))
        return self._base(writable=[workdir, tmpdir], readable=reads, readonly=[workdir / ".git"],
                          **self._network(tools))

    def evaluation(self, code: Path, seed_dir: Path, inputs: Path) -> SandboxPolicy:
        """`code`: the version's commit, exported; `seed_dir`: this seed's own directory."""
        return self._base(writable=[seed_dir], readable=[code, inputs, self.public, *self.python],
                          readonly=[code, inputs, self.public], network="none",
                          temp_read=False, temp_write=False)

    def build(self, folder: Path, build_dir: Path) -> SandboxPolicy:
        return self._base(writable=[build_dir], readable=[folder], readonly=[folder],
                          network="none", temp_read=False, temp_write=False)
