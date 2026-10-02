"""The backends agents can run on, by name (architecture review 2026-10-02, finding 1).

A run records the backend it started with in run.json, and `resume` rebuilds it from there by the
same name. A second real backend is one more entry here, plus a `backend` key in routing.json for
the agents it should serve; the stages do not change.
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Optional

from .base import Backend

log = logging.getLogger("scientisttwo")

BACKENDS = ("claude", "mock")
_ALIASES = {"claude": "claude", "claude_cli": "claude", "mock": "mock"}


def canonical(name: str) -> str:
    if name not in _ALIASES:
        raise ValueError(f"unknown backend {name!r}; known: {', '.join(BACKENDS)}")
    return _ALIASES[name]


def make_backend(name: str, *, allow_unsandboxed: bool = False, mock_script: Optional[str] = None,
                 claude_bin: Optional[str] = None) -> Backend:
    name = canonical(name)
    if name == "mock":
        from .mock import MockBackend
        script = json.loads(Path(mock_script).read_text()) if mock_script else None
        return MockBackend(script)
    from .claude_cli import ClaudeCLIBackend
    if claude_bin and not os.path.exists(claude_bin):
        # the CLI's updater keeps a few versions and deletes older ones: a resume days later finds
        # the pinned binary gone. The current one takes over; the history entry of this start
        # records its path and version. ⛔ WHY NOT refuse: the run could then never finish.
        log.warning("the run's claude binary %s is gone (updated since); using the current one", claude_bin)
        claude_bin = None
    return ClaudeCLIBackend(claude_bin=claude_bin, allow_unsandboxed=allow_unsandboxed)
