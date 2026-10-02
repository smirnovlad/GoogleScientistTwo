"""The budget guard and the cost ledger (CLAUDE.md: cost is bounded and recorded).

On the subscription a call costs nothing per call, but it spends the usage windows. The ledger
records, per unit: the agent, model, seconds, the API-equivalent cost the CLI reports (`null`
when the CLI reports none: unknown, never zero), and the usage windows after the call.

The guard stops a run before it passes any cap of its profile: agent calls, coding sessions,
wall-clock hours, API-equivalent dollars, or a usage window above its ceiling. A stop is a
`BudgetExceeded`, which the orchestrator turns into a resumable `paused` run.
"""
from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


class BudgetExceeded(RuntimeError):
    def __init__(self, message: str, resume_after: Optional[float] = None):
        super().__init__(message)
        self.resume_after = resume_after


@dataclass
class Caps:
    max_agent_calls: Optional[int] = None
    max_coding_sessions: Optional[int] = None
    max_hours: Optional[float] = None
    max_equiv_usd: Optional[float] = None
    # usage-window ceilings (0..1): above them the run pauses until the window resets
    max_five_hour_utilization: Optional[float] = None
    max_seven_day_utilization: Optional[float] = None

    @staticmethod
    def from_dict(d: dict) -> "Caps":
        return Caps(**{k: d.get(k) for k in Caps.__dataclass_fields__})


@dataclass
class Totals:
    agent_calls: int = 0
    coding_sessions: int = 0
    seconds: float = 0.0
    equiv_usd: float = 0.0
    unknown_cost_calls: int = 0
    by_agent: dict = field(default_factory=dict)


CODING_KINDS = ("coding", "writer", "readonly")


class Budget:
    def __init__(self, run_dir: Path, caps: Caps, started_at: float):
        self.caps = caps
        self.started_at = started_at
        self.ledger_path = Path(run_dir) / "ledger.jsonl"
        self.totals = Totals()
        self.windows: dict[str, Any] = {}
        self._lock = threading.Lock()
        if self.ledger_path.exists():                      # resume: count what was already spent
            for line in self.ledger_path.read_text().splitlines():
                if line.strip():
                    self._count(json.loads(line))

    def _count(self, entry: dict) -> None:
        if entry.get("type") != "agent":
            return
        t = self.totals
        t.agent_calls += 1
        if entry.get("kind") in CODING_KINDS:
            t.coding_sessions += 1
        t.seconds += float(entry.get("seconds") or 0)
        cost = entry.get("equiv_usd")
        if cost is None:
            t.unknown_cost_calls += 1
        else:
            t.equiv_usd += float(cost)
        a = t.by_agent.setdefault(entry.get("agent", "?"), {"calls": 0, "seconds": 0.0, "equiv_usd": 0.0})
        a["calls"] += 1
        a["seconds"] += float(entry.get("seconds") or 0)
        a["equiv_usd"] += float(cost or 0)
        if entry.get("rate_limit"):
            self.windows = entry["rate_limit"]

    def check(self, kind: str) -> None:
        """Raise BudgetExceeded if one more call of this kind would pass a cap."""
        c, t = self.caps, self.totals
        with self._lock:
            if c.max_agent_calls is not None and t.agent_calls >= c.max_agent_calls:
                raise BudgetExceeded(f"agent-call cap reached ({t.agent_calls}/{c.max_agent_calls})")
            if (kind in CODING_KINDS and c.max_coding_sessions is not None
                    and t.coding_sessions >= c.max_coding_sessions):
                raise BudgetExceeded(f"coding-session cap reached ({t.coding_sessions}/{c.max_coding_sessions})")
            hours = (time.time() - self.started_at) / 3600
            if c.max_hours is not None and hours >= c.max_hours:
                raise BudgetExceeded(f"wall-clock cap reached ({hours:.1f} h / {c.max_hours} h)")
            if c.max_equiv_usd is not None and t.equiv_usd >= c.max_equiv_usd:
                raise BudgetExceeded(f"API-equivalent cost cap reached (${t.equiv_usd:.2f})")
            self._check_windows()

    def _check_windows(self) -> None:
        windows = (self.windows or {}).get("unifiedWindows") or {}
        for name, cap in (("five_hour", self.caps.max_five_hour_utilization),
                          ("seven_day", self.caps.max_seven_day_utilization)):
            w = windows.get(name) or {}
            util, reset = w.get("utilization"), w.get("resetsAt")
            if cap is None or not isinstance(util, (int, float)):
                continue
            if util >= cap and (not isinstance(reset, (int, float)) or reset > time.time()):
                raise BudgetExceeded(f"subscription {name} window at {util:.0%} (ceiling {cap:.0%})",
                                     resume_after=float(reset) if isinstance(reset, (int, float)) else None)

    def record(self, entry: dict) -> None:
        entry = {"type": "agent", "time": time.time(), **entry}
        with self._lock:
            with open(self.ledger_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
            self._count(entry)

    def record_event(self, entry: dict) -> None:
        with self._lock:
            with open(self.ledger_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"time": time.time(), **entry}, default=str) + "\n")

    def summary(self) -> dict:
        t = self.totals
        return {"agent_calls": t.agent_calls, "coding_sessions": t.coding_sessions,
                "agent_seconds": round(t.seconds, 1), "equiv_usd": round(t.equiv_usd, 4),
                "unknown_cost_calls": t.unknown_cost_calls,
                "wall_hours": round((time.time() - self.started_at) / 3600, 3),
                "by_agent": t.by_agent, "usage_windows": (self.windows or {}).get("unifiedWindows")}
