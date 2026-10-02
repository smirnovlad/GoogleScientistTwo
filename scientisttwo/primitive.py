"""The stage primitive (analysis §3.4–3.5): Listing 1, with its fixed choices made parameters.

Listing 1 fixes one setting [Lst. 1]: a critic reading the candidate, three verdicts, no guard,
a limit counting critic calls, discard at the limit. The paper's stages each set some of these
differently (analysis §3.4), so each is a parameter, and each stage's values are data.

    run_stage(candidate, p):
        rounds = 0
        loop:
            verdict, feedback = p.critic(candidate, rounds)          # an agent, or a number
            outcome = p.verdict_map[verdict]                          # accept | refine | reject
            accept -> return candidate                                [accepted]
            reject -> return None                                     [rejected]
            refine:
                if the limit is spent -> exhaustion policy             [exhausted]
                new = p.refine(candidate, feedback, rounds)
                if p.guard and not p.guard(new, best):                 [guard_failed]
                    return best                                       (§3.4, §3.6: keep the best)
                if p.guard: best = new; new = p.after_guard(new)
                candidate = new; rounds += 1

Every outcome carries `last`, the last candidate the critic judged, and `best`, so a caller never
needs a closure to learn what a rejected or discarded candidate was.

Counting (A-TOP-2): "refinements" allows `limit` judged refinements, so `limit + 1` critic calls
(App. A.2's wording for N_eng, N_abl, N_peer, N_meta); "critic_calls" allows `limit` critic calls
and refines after each, as Listing 1 does (the 16 limitation rounds).
Exhaustion (A-TOP-1, U-TOP-7): "discard" returns None, "keep_last" the last candidate,
"keep_best" the best one: the last the guard admitted, or, for a stage without a guard, the
highest by `rank` (peer review's score, U-TOP-7's other reading). "keep_best" with neither is
refused: it used to return the first candidate silently.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

ACCEPT, REFINE, REJECT = "accept", "refine", "reject"
COUNTING = ("refinements", "critic_calls")
EXHAUSTION = ("discard", "keep_last", "keep_best")


@dataclass
class StageParams:
    name: str
    critic: Callable[[Any, int], tuple[str, Any]]
    refine: Callable[[Any, Any, int], Any]
    verdict_map: dict[str, str]
    limit: int
    counting: str = "refinements"
    exhaustion: str = "discard"
    guard: Optional[Callable[[Any, Any], bool]] = None
    after_guard: Optional[Callable[[Any, int], Any]] = None
    rank: Optional[Callable[[Any], float]] = None     # keep_best without a guard: higher is better

    def __post_init__(self) -> None:
        if self.counting not in COUNTING:
            raise ValueError(f"{self.name}: counting must be one of {COUNTING}")
        if self.exhaustion not in EXHAUSTION:
            raise ValueError(f"{self.name}: exhaustion must be one of {EXHAUSTION}")
        if self.limit < 0:
            raise ValueError(f"{self.name}: limit must be >= 0")
        if self.exhaustion == "keep_best" and self.guard is None and self.rank is None:
            raise ValueError(f"{self.name}: keep_best needs a guard or a rank to say what is best")
        if self.guard is not None and self.rank is not None:
            raise ValueError(f"{self.name}: give a guard or a rank, not both")
        bad = {v for v in self.verdict_map.values()} - {ACCEPT, REFINE, REJECT}
        if bad:
            raise ValueError(f"{self.name}: unknown outcomes {bad}")


@dataclass
class StageOutcome:
    candidate: Any                 # what the stage passes on; None when rejected or discarded
    status: str                    # accepted | rejected | exhausted | guard_failed
    critic_calls: int
    refinements: int
    history: list = field(default_factory=list)   # (round, verdict, feedback)
    last_feedback: Any = None
    last: Any = None               # the last candidate the critic judged
    best: Any = None               # the guard's best, or the rank's


def run_stage(candidate: Any, p: StageParams) -> StageOutcome:
    best = candidate
    history: list = []
    calls = refinements = 0

    def done(kept: Any, status: str, feedback: Any = None) -> StageOutcome:
        return StageOutcome(kept, status, calls, refinements, history, feedback, candidate, best)

    while True:
        if p.counting == "critic_calls" and calls >= p.limit:
            return done(_kept(p, candidate, best), "exhausted")
        verdict, feedback = p.critic(candidate, calls)
        calls += 1
        history.append((calls - 1, verdict, feedback))
        outcome = p.verdict_map.get(verdict)
        if outcome is None:
            raise ValueError(f"{p.name}: verdict {verdict!r} not in {sorted(p.verdict_map)}")
        if outcome == ACCEPT:
            return done(candidate, "accepted", feedback)
        if outcome == REJECT:
            return done(None, "rejected", feedback)
        if p.counting == "refinements" and refinements >= p.limit:
            return done(_kept(p, candidate, best), "exhausted", feedback)
        new = p.refine(candidate, feedback, refinements)
        refinements += 1
        if p.guard is not None:
            if not p.guard(new, best):
                candidate = new
                return done(best, "guard_failed", feedback)
            best = new
            if p.after_guard is not None:
                new = p.after_guard(new, refinements)
                best = new
        elif p.rank is not None and p.rank(new) > p.rank(best):
            best = new
        candidate = new


def _kept(p: StageParams, candidate: Any, best: Any) -> Any:
    return {"discard": None, "keep_last": candidate, "keep_best": best}[p.exhaustion]
