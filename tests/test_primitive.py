"""The stage primitive: every branch of analysis §3.4's parameter table."""
import pytest

from scientisttwo.primitive import ACCEPT, REFINE, REJECT, StageParams, run_stage

V = {"Good": ACCEPT, "Engineer": REFINE, "Bad": REJECT}


def scripted(verdicts):
    calls = []

    def critic(c, i):
        calls.append((c, i))
        return verdicts[min(i, len(verdicts) - 1)], f"fb{i}"

    return critic, calls


def test_accept_first():
    critic, calls = scripted(["Good"])
    out = run_stage(0, StageParams("s", critic, lambda c, f, i: c + 1, V, limit=2))
    assert (out.candidate, out.status, out.critic_calls, out.refinements) == (0, "accepted", 1, 0)


def test_refine_then_accept():
    critic, _ = scripted(["Engineer", "Engineer", "Good"])
    out = run_stage(0, StageParams("s", critic, lambda c, f, i: c + 1, V, limit=2))
    assert (out.candidate, out.status, out.critic_calls, out.refinements) == (2, "accepted", 3, 2)


def test_reject_discards():
    critic, _ = scripted(["Engineer", "Bad"])
    out = run_stage(0, StageParams("s", critic, lambda c, f, i: c + 1, V, limit=2))
    assert (out.candidate, out.status) == (None, "rejected")


@pytest.mark.parametrize("exhaustion,expected", [("discard", None), ("keep_last", 2), ("keep_best", 1)])
def test_refinement_counting_allows_n_plus_one_critic_calls(exhaustion, expected):
    critic, calls = scripted(["Engineer"])
    rank = (lambda c: -abs(c - 1)) if exhaustion == "keep_best" else None   # candidates 0, 1, 2: 1 is best
    out = run_stage(0, StageParams("s", critic, lambda c, f, i: c + 1, V, limit=2, exhaustion=exhaustion,
                                   rank=rank))
    assert out.status == "exhausted"
    assert (out.critic_calls, out.refinements) == (3, 2)        # A-TOP-2 reading 2
    assert out.candidate == expected


def test_critic_call_counting_is_listing_1():
    """Listing 1: max_rounds critic calls; the last refinement is never judged (the 16 rounds)."""
    critic, calls = scripted(["Engineer"])
    out = run_stage(0, StageParams("s", critic, lambda c, f, i: c + 1, V, limit=3,
                                   counting="critic_calls", exhaustion="keep_last"))
    assert (out.critic_calls, out.refinements, out.candidate) == (3, 3, 3)
    assert [i for _, i in calls] == [0, 1, 2]


def test_guard_failure_keeps_best():
    critic, _ = scripted(["Engineer"])
    out = run_stage(10, StageParams("s", critic, lambda c, f, i: c - 1, V, limit=3,
                                    guard=lambda new, best: new > best))
    assert (out.candidate, out.status, out.refinements) == (10, "guard_failed", 1)


def test_guard_success_runs_after_guard_and_keeps_best_at_limit():
    critic, _ = scripted(["Engineer"])
    seen = []

    def after(c, i):
        seen.append((c, i))
        return c + 100

    out = run_stage(0, StageParams("s", critic, lambda c, f, i: c + 1, V, limit=1, exhaustion="keep_best",
                                   guard=lambda new, best: new > best, after_guard=after))
    assert seen == [(1, 1)]
    assert (out.candidate, out.status) == (101, "exhausted")


def test_unknown_verdict_is_an_error():
    with pytest.raises(ValueError):
        run_stage(0, StageParams("s", lambda c, i: ("Maybe", ""), lambda c, f, i: c, V, limit=1))


def test_bad_parameters_are_refused():
    with pytest.raises(ValueError):
        StageParams("s", lambda c, i: ("Good", ""), lambda c, f, i: c, V, limit=-1)
    with pytest.raises(ValueError):
        StageParams("s", lambda c, i: ("Good", ""), lambda c, f, i: c, V, limit=1, exhaustion="keep_some")


def test_keep_best_needs_a_guard_or_a_rank():
    """It used to return the first candidate silently (architecture review 2026-10-02, finding 2)."""
    with pytest.raises(ValueError):
        StageParams("s", lambda c, i: ("Good", ""), lambda c, f, i: c, V, limit=1, exhaustion="keep_best")
    with pytest.raises(ValueError):
        StageParams("s", lambda c, i: ("Good", ""), lambda c, f, i: c, V, limit=1, exhaustion="keep_best",
                    guard=lambda n, b: True, rank=lambda c: c)


def test_every_outcome_says_what_was_judged_last():
    critic, _ = scripted(["Engineer", "Bad"])
    out = run_stage(0, StageParams("s", critic, lambda c, f, i: c + 1, V, limit=2))
    assert (out.candidate, out.last, out.status) == (None, 1, "rejected")
    critic, _ = scripted(["Engineer"])
    out = run_stage(10, StageParams("s", critic, lambda c, f, i: c - 1, V, limit=3,
                                    guard=lambda new, best: new > best))
    assert (out.candidate, out.last, out.best, out.status) == (10, 9, 10, "guard_failed")
