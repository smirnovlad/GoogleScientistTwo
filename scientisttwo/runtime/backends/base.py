"""The backend interface: one agent call in, one result out.

Every agent the engine runs goes through a Backend. Two implementations exist: `claude_cli`, the
real one, which runs `claude -p` on the user's subscription, and `mock`, which runs the whole
engine for $0 in tests (docs/architecture/engine.md, section 2).
"""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ...harness.sandbox import SandboxPolicy

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
    """Base of every backend failure."""


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


class Backend(abc.ABC):
    name: str = "abstract"

    @abc.abstractmethod
    def call(self, call: AgentCall) -> AgentResult:
        """Run one agent call. Raises a BackendError subclass on failure."""

    def describe(self) -> dict[str, Any]:
        """What the run manifest records about this backend."""
        return {"backend": self.name}
