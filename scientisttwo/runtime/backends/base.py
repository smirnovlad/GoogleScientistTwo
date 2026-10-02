"""The backend interface: one agent call in, one result out.

Every agent the engine runs goes through a Backend. Two implementations exist: `claude_cli`, the
real one, which runs `claude -p` on the user's subscription, and `mock`, which runs the whole
engine for $0 in tests (docs/architecture/engine.md, section 2). A backend that starts a process
derives from `SubprocessBackend`, whose `spawn` always applies the call's sandbox and records the
process, so a new backend cannot forget either (architecture review 2026-10-02, finding 1).
"""
from __future__ import annotations

import abc
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ...harness import sandbox as sbx
from ...harness.sandbox import SandboxPolicy
from ..procs import MARKER, ProcRegistry, TreeWatcher, kill_groups, marked, new_marker

KINDS = ("reasoning", "coding", "writer", "readonly")


@dataclass(frozen=True)
class AgentCall:
    """Everything a backend needs to run one agent once."""

    agent: str
    kind: str                      # one of KINDS
    system: str                    # system.md: replaces (reasoning) or extends (others) the CLI's
    user: str                      # the rendered prompt.md
    schema: Optional[dict]         # the output JSON schema, or None for free text
    model: str
    effort: Optional[str]
    tools: tuple[str, ...]         # () means no tools at all
    cwd: Optional[Path]            # the agent's working directory
    sandbox: Optional[SandboxPolicy]
    timeout_s: int
    transcript: Optional[Path]     # where the backend writes the session's stream, if it can
    key: str = ""                  # the unit key: where in the run this call sits
    meta: dict = field(default_factory=dict, compare=False)  # the template variables, for mocks and logs
    tmpdir: Optional[Path] = None  # the unit's own TMPDIR
    attempt: int = 1

    def __post_init__(self) -> None:
        if self.kind not in KINDS:
            raise ValueError(f"unknown agent kind {self.kind!r}")


@dataclass
class AgentResult:
    output: Optional[dict]         # the structured output, validated against the schema
    text: str                      # the final message as text
    cost_usd: Optional[float]      # API-equivalent cost the CLI reports; None means unknown
    duration_s: float
    tokens: dict = field(default_factory=dict)
    session_id: Optional[str] = None
    raw: dict = field(default_factory=dict)


class BackendError(Exception):
    """Base of every backend failure. `cost_usd` and `tokens`: what the call reported spending
    before it failed, if it got that far (None: unknown, never zero)."""
    cost_usd: Optional[float] = None
    tokens: Optional[dict] = None
    rate_limit: Optional[dict] = None             # the usage windows the call observed


class TransientError(BackendError):
    """Worth retrying: a network blip, an overloaded model, a crashed CLI."""


class RateLimited(BackendError):
    """The subscription's usage window is spent. `reset_at` is a unix time, or None if unknown."""

    def __init__(self, message: str, reset_at: Optional[float] = None):
        super().__init__(message)
        self.reset_at = reset_at


class AgentTimeout(BackendError):
    """The call ran past its timeout and was killed."""


class InvalidOutput(BackendError):
    """The call finished but returned no output that fits the schema."""


class AgentFailed(BackendError):
    """The call failed in a way a retry will not fix."""


class EnvironmentFault(BackendError):
    """The machine, not the agent, failed (no space left, a permission the engine needs): the run
    pauses for a person, rather than failing a unit that would replay as failed for good."""


class Backend(abc.ABC):
    name: str = "abstract"

    @abc.abstractmethod
    def call(self, call: AgentCall) -> AgentResult:
        """Run one agent call. Raises a BackendError subclass on failure."""

    def describe(self) -> dict[str, Any]:
        """What the run manifest records about this backend."""
        return {"backend": self.name}

    def sandbox_reads(self) -> list[Path]:
        """What the backend's own process must read under $HOME (its binary, its login)."""
        return []

    def attach(self, registry: Optional[ProcRegistry]) -> None:
        """Called once per run: where to record the processes this backend starts."""


class SubprocessBackend(Backend):
    """A backend that runs each call as a process tree."""

    allow_unsandboxed: bool = False
    registry: Optional[ProcRegistry] = None

    def attach(self, registry: Optional[ProcRegistry]) -> None:
        self.registry = registry

    def spawn(self, call: AgentCall, argv: list[str], env: dict[str, str]) -> "Spawned":
        """Start argv inside the call's sandbox, in its own session, watched and recorded.

        The sandbox is not optional here: without a policy the start is refused, unless the run
        was explicitly started with --allow-unsandboxed."""
        wrapped = sbx.wrap(argv, call.sandbox, self.allow_unsandboxed)
        marker = new_marker(call.key)
        env = {**env, MARKER: marker}
        proc = subprocess.Popen(wrapped, cwd=str(call.cwd) if call.cwd else None, env=env,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
        registry = self.registry
        on_new = ((lambda w: registry.record(proc.pid, call.key, w.groups, w.members, marker))
                  if registry else None)
        return Spawned(proc, TreeWatcher(proc.pid, on_new=on_new).start(), registry, marker)


class Spawned:
    """A started process tree; `finish` kills whatever of it is still alive and forgets it."""

    def __init__(self, proc: subprocess.Popen, watcher: TreeWatcher, registry: Optional[ProcRegistry],
                 marker: str):
        self.proc, self.watcher, self.registry, self.marker = proc, watcher, registry, marker

    def kill_now(self) -> None:
        """Kill the whole tree at once (a timeout), not only the CLI's group: a descendant in a
        session of its own can hold the output pipe open (Codex review 2026-10-02, P1)."""
        self.watcher.sample()
        kill_groups(self.watcher.live_groups() | {self.proc.pid} | {g for _, g in marked(self.marker)},
                    grace=0)

    def finish(self, grace: float = 3.0) -> None:
        groups = self.watcher.stop() | {self.proc.pid} | {g for _, g in marked(self.marker)}
        kill_groups(groups, grace=grace)
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass
        if self.registry is not None:
            self.registry.forget(self.proc.pid)
