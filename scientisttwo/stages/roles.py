"""Each critic's verdict field, and how its verdicts map onto the primitive's outcomes.

One table, checked against every critic's schema when the agents load (`check_roles`), so a map
and an enum can never disagree at run time, after the critic's call is paid for and stored
(architecture review 2026-10-02, finding 3).
"""
from __future__ import annotations

from typing import Any

from ..primitive import ACCEPT, REFINE, REJECT

CRITICS: dict[str, tuple[str, dict[str, str]]] = {
    "limitation_verifier": ("verdict", {"sufficient": ACCEPT, "insufficient": REFINE}),     # §3.1
    "subset_critic": ("verdict", {"Good": ACCEPT, "Engineer": REFINE, "Bad": REJECT}),      # §3.2
    "full_set_critic": ("verdict", {"Good": ACCEPT, "Engineer": REFINE, "Bad": REJECT}),    # §3.2
    "ablation_critic": ("verdict", {"Good": ACCEPT, "Refine": REFINE, "Reject": REJECT}),   # §3.4, A-ABL-1
    "meta_reviewer": ("decision", {"Accept": ACCEPT, "Refine": REFINE}),                    # §3.6
}


def verdict_map(agent: str) -> dict[str, str]:
    return CRITICS[agent][1]


def verdict_of(agent: str, output: dict[str, Any]) -> str:
    return output[CRITICS[agent][0]]


def check_roles(specs: dict) -> None:
    """Refuse to start a run whose critic schemas and verdict maps disagree."""
    problems = []
    for agent, (field, vmap) in CRITICS.items():
        spec = specs.get(agent)
        if spec is None:
            problems.append(f"{agent}: no such agent")
            continue
        enum = (spec.schema.get("properties", {}).get(field) or {}).get("enum")
        if enum is None:
            problems.append(f"{agent}: its schema has no enum for {field!r}")
        elif set(enum) != set(vmap):
            problems.append(f"{agent}: schema enum {sorted(enum)} differs from the verdict map {sorted(vmap)}")
    if problems:
        raise ValueError("agent roles disagree with their schemas: " + "; ".join(problems))
