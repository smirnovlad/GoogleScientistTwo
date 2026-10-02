"""The engine's state between stages: the baseline, an idea's trace and the core state.

They live here, not in the stage that first makes them, so that a stage imports the state it
reads and nothing else (architecture review 2026-10-02, finding 8).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Optional

from .harness.harness import summarize


@dataclass
class Baseline:
    """E_base: the reproduced baseline's version and its results (§3.2, A-BASE-1)."""
    ws: str
    subset: dict
    full: dict


@dataclass
class Trace:
    """One idea's record through A_Coder (P-STATE-7)."""
    id: str
    idea: dict
    verdict: str                      # Good | Bad
    level: str                        # where it ended: subset | full | spec | error
    feedback: str
    ws: str
    subset: Optional[dict] = None
    full: Optional[dict] = None
    history: list = field(default_factory=list)

    def view(self) -> dict:
        """What the Idea Evolver and the Selector read (P-STATE-7)."""
        last = self.full or self.subset or {}
        v = {"id": self.id, "idea": self.idea, "verdict": self.verdict, "ended_at": self.level,
             "feedback": self.feedback,
             "subset_result": summarize(self.subset) if self.subset else None,
             "full_result": summarize(self.full) if self.full else None}
        if self.verdict == "Bad" and last.get("log_tail"):
            # ⛔ WHY NOT the whole log: the evolver reads every trace at once. The last 2000
            # characters (our choice, 2026-10-02) hold the error; what is lost is the run's start.
            v["diagnostic_log_tail"] = last["log_tail"][-2000:]
        return v

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Core:
    """The core state (h_best, E_best, C_best), P-STATE-9."""
    id: str
    idea: dict
    ws: str
    result: dict                     # E_best: the harness result on `full`
    compliant: bool = True
    lineage: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"id": self.id, "idea": self.idea, "ws": self.ws, "result": self.result,
                "compliant": self.compliant, "lineage": self.lineage}
