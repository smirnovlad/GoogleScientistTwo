"""The budget guard and the cost ledger (CLAUDE.md: cost is bounded and recorded).

On the subscription a call costs nothing per call, but it spends the usage windows. The ledger
holds one line per ATTEMPT, written and fsync'd before the unit is stored: the agent, model,
outcome, seconds, the API-equivalent cost the CLI reports (`null` when it reports none: unknown,
never zero), and the usage windows after the call. Retries and failures spend too, so they count.

Each attempt is journalled BEFORE its call (`attempt_started`), so an engine killed during a call
leaves a record: the next start counts that attempt as `interrupted`, with an unknown cost, and
the caps keep it (Codex review 2026-10-02, P2). Attempt numbers run on across resumes, per unit.

The guard stops a run before it passes any cap of its profile: attempts, coding sessions, hours
of RUNNING time (paused time does not count), API-equivalent dollars, or a usage window above its
ceiling. A stop raises `BudgetExceeded`, a `RunPaused`: the orchestrator records a resumable
`paused` run.
"""
from __future__ import annotations

import json
import logging
import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

log = logging.getLogger("scientisttwo")


class RunPaused(RuntimeError):
    """The run must stop now and can be resumed later, at `resume_after` if known."""

    def __init__(self, message: str, resume_after: Optional[float] = None):
        super().__init__(message)
        self.resume_after = resume_after


class BudgetExceeded(RunPaused):
    pass


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
        unknown = set(d) - set(Caps.__dataclass_fields__)
        if unknown:
            raise ValueError(f"unknown budget caps {sorted(unknown)}")
        return Caps(**{k: d.get(k) for k in Caps.__dataclass_fields__})


@dataclass
class Totals:
    agent_calls: int = 0                 # attempts: every call that reached the backend
    coding_sessions: int = 0
    seconds: float = 0.0
    equiv_usd: float = 0.0
    unknown_cost_calls: int = 0
    by_agent: dict = field(default_factory=dict)
    by_outcome: dict = field(default_factory=dict)


CODING_KINDS = ("coding", "writer", "readonly")


def running_hours(run_dir: Path, now: Optional[float] = None) -> float:
    """Hours the run has spent in status `running`, from run.json's history."""
    try:
        history = json.loads((Path(run_dir) / "run.json").read_text()).get("history", [])
    except (OSError, json.JSONDecodeError):
        return 0.0
    now = time.time() if now is None else now
    total, since = 0.0, None
    for h in history:
        if h.get("status") == "running":
            if since is None:
                since = h["time"]
        elif since is not None:
            total += max(0.0, h["time"] - since)
            since = None
    if since is not None:
        total += max(0.0, now - since)
    return total / 3600


def repair_ledger(path: Path) -> Optional[str]:
    """A crash mid-append can leave a partial last line: cut it, and say what was cut."""
    if not path.exists():
        return None
    data = path.read_bytes()
    if not data or data.endswith(b"\n"):
        return None
    cut = data.rfind(b"\n") + 1
    with open(path, "r+b") as f:
        f.truncate(cut)
        f.flush()
        os.fsync(f.fileno())
    return data[cut:].decode("utf-8", "replace")[:200]


class Budget:
    def __init__(self, run_dir: Path, caps: Caps, started_at: float,
                 hours: Optional[Callable[[], float]] = None):
        self.caps = caps
        self.started_at = started_at
        self.run_dir = Path(run_dir)
        self.ledger_path = self.run_dir / "ledger.jsonl"
        self.hours = hours or (lambda: running_hours(self.run_dir))
        self.totals = Totals()
        self.windows: dict[str, Any] = {}
        self.attempts: dict[str, int] = {}                   # per unit key, every attempt so far
        self._lock = threading.Lock()
        cut = repair_ledger(self.ledger_path)
        if cut is not None:
            log.warning("ledger: removed a partial last line left by a crash: %r", cut)
            self.record_event({"type": "ledger_repaired", "removed": cut})
        if self.ledger_path.exists():                      # resume: count what was already spent
            started: dict[str, dict] = {}
            for line in self.ledger_path.read_text().splitlines():
                if line.strip():
                    entry = json.loads(line)
                    if entry.get("type") == "attempt_started":
                        started[entry["attempt_id"]] = entry
                    else:
                        started.pop(entry.get("attempt_id"), None)
                        self._count(entry)
            for entry in started.values():                 # cut off by the end of an engine
                self.record({k: entry.get(k) for k in ("key", "agent", "kind", "attempt", "attempt_id")}
                            | {"outcome": "interrupted", "seconds": None, "equiv_usd": None,
                               "error": "the engine stopped during this call; what it spent is unknown"})

    def _count(self, entry: dict) -> None:
        if entry.get("type") != "agent":
            return
        t = self.totals
        t.agent_calls += 1
        if entry.get("key"):
            self.attempts[entry["key"]] = self.attempts.get(entry["key"], 0) + 1
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
        outcome = entry.get("outcome", "ok")
        t.by_outcome[outcome] = t.by_outcome.get(outcome, 0) + 1
        if entry.get("rate_limit"):
            self.windows = {**entry["rate_limit"], "observed_at": entry.get("time")}

    def check(self, kind: str) -> None:
        """Raise BudgetExceeded if one more call of this kind would pass a cap."""
        c, t = self.caps, self.totals
        with self._lock:
            if c.max_agent_calls is not None and t.agent_calls >= c.max_agent_calls:
                raise BudgetExceeded(f"agent-call cap reached ({t.agent_calls}/{c.max_agent_calls})")
            if (kind in CODING_KINDS and c.max_coding_sessions is not None
                    and t.coding_sessions >= c.max_coding_sessions):
                raise BudgetExceeded(f"coding-session cap reached ({t.coding_sessions}/{c.max_coding_sessions})")
            if c.max_hours is not None:
                hours = self.hours()
                if hours >= c.max_hours:
                    raise BudgetExceeded(f"running-time cap reached ({hours:.1f} h / {c.max_hours} h)")
            if c.max_equiv_usd is not None and t.equiv_usd >= c.max_equiv_usd:
                raise BudgetExceeded(f"API-equivalent cost cap reached (${t.equiv_usd:.2f})")
            self._check_windows()

    def _check_windows(self) -> None:
        windows = (self.windows or {}).get("unifiedWindows") or {}
        now = time.time()
        for name, cap in (("five_hour", self.caps.max_five_hour_utilization),
                          ("seven_day", self.caps.max_seven_day_utilization)):
            w = windows.get(name) or {}
            util, reset = w.get("utilization"), w.get("resetsAt")
            if cap is None or not isinstance(util, (int, float)) or util < cap:
                continue
            # ⛔ WHY NOT block on a window with no known reset time: no call could then run to
            # refresh the reading, and the run would pause forever (infrastructure review, I10).
            # The CLI itself refuses a call when the window is really spent.
            if isinstance(reset, (int, float)) and reset > now:
                raise BudgetExceeded(f"subscription {name} window at {util:.0%} (ceiling {cap:.0%})",
                                     resume_after=float(reset))

    def _append(self, entry: dict) -> None:
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def started(self, entry: dict) -> None:
        """An attempt is about to call the backend (`entry` names it by `attempt_id`)."""
        with self._lock:
            self._append({"type": "attempt_started", "time": time.time(), **entry})

    def attempts_of(self, key: str) -> int:
        with self._lock:
            return self.attempts.get(key, 0)

    def record(self, entry: dict) -> None:
        """One attempt: written and fsync'd before its unit is stored."""
        entry = {"type": "agent", "time": time.time(), **entry}
        with self._lock:
            self._append(entry)
            self._count(entry)

    def record_event(self, entry: dict) -> None:
        with self._lock:
            self._append({"time": time.time(), **entry})

    def summary(self) -> dict:
        t = self.totals
        return {"agent_calls": t.agent_calls, "coding_sessions": t.coding_sessions,
                "agent_seconds": round(t.seconds, 1), "equiv_usd": round(t.equiv_usd, 4),
                # copies: a summary stored earlier must not change with later calls (run 2's
                # export said 40 calls and 42 outcomes)
                "unknown_cost_calls": t.unknown_cost_calls, "by_outcome": dict(t.by_outcome),
                "running_hours": round(self.hours(), 3),
                "wall_hours": round((time.time() - self.started_at) / 3600, 3),
                "by_agent": {k: dict(v) for k, v in t.by_agent.items()},
                "usage_windows": (self.windows or {}).get("unifiedWindows")}
