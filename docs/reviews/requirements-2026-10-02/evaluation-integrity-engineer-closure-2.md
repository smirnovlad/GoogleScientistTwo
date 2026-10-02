# Closure check of the evaluation-integrity review, continued

*The second half of `evaluation-integrity-engineer-closure.md`, split at "### Minors" to keep each file under 600 lines. The text below is verbatim.*

### Minors

**NEW-11 · minor · R-STG-3: the refusal of a changed C_base has no control of its own, and repackaging is unbounded**
- **Where:**
  - "a copy whose code differs from the pinned commit is refused" (`03-stages.md:60`).
  - Its test: "a Baseline Coding Agent scripted to weaken the code it copies is refused, and E_base and every gain are unchanged; in the twin that scores the agent's copy as E_base, every gain grows by the weakening" (`03-stages.md:70`).
  - "a person may repackage the task as a new manifest version, and every attempt is reported (IR-15)" (`03-stages.md:62`).
- **(a) The twin proves IR-4, not the refusal.**
  - The twin shows that E_base comes from the pinned code. Once it does, a weakened C_base only handicaps the ideas.
  - The attack the refusal actually stops is a strengthened copy, for example with EMA added. Every idea would inherit it, and be credited with it against E_base.
  - Control: plant a strengthened copy.
    - Under the guard: refused, and a null idea's gain is unchanged.
    - Twin that accepts the copy: the null idea's subset gain grows by the strengthening, and passes the veto.
- **(b) Repackaging can select the report split.**
  - Each repackaging reads the report role through the sealed check.
  - The roles are built when a task is packaged (IR-10), so a new version may re-draw the report split.
  - Repackaging until the check passes selects a split on which the baseline reproduces. Every model scored on that split shares its luck, which inflates each gain against the published number (R-MEAS-2).
  - Guard:
    - at most k attempts, fixed before the first, with packaging iterating on search (F-6);
    - a new version keeps its task's role index files, so only the baseline's packaging diff may change.
  - Control: a planted packaging loop that re-carves the report split.
    - Under the guard: refused after k attempts, with the role hashes unchanged.
    - Twin, unbounded: the final split's baseline score sits in the upper tail of what re-carving produces.

**NEW-12 · minor · People can choose which runs finish, after seeing their results**
- **Where:**
  - R-OPS-4: "Each coding session and each task has a budget, fixed before the task's first run". Yet a task that cannot afford its next unit "resumes from its record once the budget is raised" (`08-operation.md:36`).
  - R-RUN-8: "a person may resume a stopped or paused run from its record" (`01-run.md:108`).
  - R-RUN-3's chained runs (`01-run.md:35`).
- **Attack:**
  - A budget is raised, or a stopped run resumed, only where its search records look promising.
  - A chain's next link starts only after the previous link's test event went well.
  - IR-18 bars selection on report numbers, not on search numbers (`blocking-decisions.md:135`).
  - A link registered after its predecessor's test event is exactly what F-10's new control refuses.
- **Guard:**
  - Budget raises and resumptions follow a rule fixed before the first run, applied to every run of their class, and recorded.
  - A raise or resumption outside the rule flags the report.
  - A chain's links, and how many there are, are registered before the first link's test event.
- **Control:** two runs stopped at their budget, one holding an idea that is `Good` on search.
  - A raise for that run alone flags the report.
  - Twin: only the promising run completes, unflagged.

**NEW-13 · minor · A run that reaches its test event and then fails its gates has no place in the report**
- **Where:**
  - R-RUN-5's outcomes (`01-run.md:59-68`) include *manuscript gate failed*, but no end state "test event done, not exported". F-5 adds one.
  - R-MEAS-2 and R-MEAS-3 compute gains from test-event records (`07-measurement.md:24`, `:33`), but do not say those records are reported whatever the outcome.
- **Attack:**
  - The tail's writer has read every frozen row's report numbers.
  - Suppose a run that fails a gate after its test event counts at U-EVAL-1's convention for failed tasks, not at its measured gain.
  - Then a failed gate can replace a negative measured gain in the mean that includes failures.
- **Guard:**
  - R-RUN-5 adds F-5's end state.
  - A run's test-event records are reported whatever its outcome.
  - The mean that includes failures counts a run with a measured gain at no more than that gain.
- **Control:** a fixture run with a negative test gain, whose tail writer is scripted to fail a gate twice.
  - Under the guard: its gain enters the mean.
  - Twin: it counts at the failure convention, and the mean rises.

**NEW-14 · minor · Three report reads against CLAUDE.md's "used once, at the end", unflagged**
- **Where:**
  - `CLAUDE.md:45`: "The test set is used once, at the end."
  - R-INT-3: "The report role is scored only in task 6's three kinds of report job: the sealed baseline check, the one test event after the freeze, and the audit's re-run (IR-14, IR-15; U-TOP-5)" (`06-integrity.md:39`).
  - R-STG-3's sealed check (`03-stages.md:61`).
- **The point:**
  - The sealed check reads the report split before the search; the audit reads it after export.
  - Task 6's review lists both, together with F-30's correction event, as "proposed exceptions awaiting Vlad's confirmation" (F-46).
  - The requirements adopt them as provisional IR- rules, without saying that they depart from a rule that binds (`docs/requirements.md:26`).
  - CLAUDE.md asks that an INCONSISTENT statement be flagged, never resolved silently.
- **Risk:**
  - Small for the numbers: the sealed check releases one bit, its selection is bounded by NEW-11 (b), and the audit reaches no run.
  - Larger for the record: a binding rule is relaxed without its owner's word.
- **Fix:** R-INT-3 says that the three report jobs depart from CLAUDE.md's wording, cites F-46, and stays provisional until that is resolved. This is bookkeeping, so it needs no control.

**NEW-15 · minor · Bookkeeping: the checker, the fix list and four texts**
- **The checker misses IR- citations.**
  - Its integrity-dependency rule matches words (`playground/paper/requirement_coverage.py:87-88`), not IR- citations.
  - R-MEAS-5 (citing IR-29) should depend on A-INT-3. R-MEAS-9 and R-OPS-2 (citing IR-18) should depend on U-TOP-5.
  - Add a rule that an IR- citation implies its row under *Depends on*, with a self-test case.
- **The checker checks no test tier.** Add the rule that a *Test* field starts with *Logic* or *Enforcement*, and that an enforcement test states a twin for each clause (NEW-10). Add self-test cases.
- **Two entries in the fix list are inaccurate:**
  - Its EI-1 row counts R-INT-4 among the enforcement tests. R-INT-4's test is "Logic, in mock mode" (`06-integrity.md:56`). That is the right tier for an LLM check whose miss rate IR-31 measures.
  - Its EI-9 row cites IR-9 for "every setting and metric". IR-9 covers settings only (`blocking-decisions.md:45`).
- **R-INT-5's and R-INT-6's logic tests** (`06-integrity.md:65`, `:74`) flag planted defects with mocks scripted to flag. Unlike R-INT-4, they do not say that the real detection rate is IR-31's.
- **R-INT-7's account of what is ours** (`06-integrity.md:78`) omits IR-23's re-training of every reported row, and IR-24's ledger checks.
  - ScientistOne's I1 compares the paper's score with "scores obtained by re-running the submitted solution on the golden evaluator" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:25).
  - F-13 marks the re-training as ours.
- **Two texts state task 6's matter as their own:** R-MEAS-1's "is positive" (`07-measurement.md:14`) and R-MEAS-2's two references (`07-measurement.md:24`) belong to A-EVAL-1 and U-EVAL-1. Write each as "as task 6 decides (row)".

## 4. What task 6's fix list and the Codex review already move

Task 6's fix list is at 04522df, F-0 to F-46, and none is declined. "Moved" means a scheduled change to a task 6 rule settles the point; the requirements then follow it.

| Finding | Task 6's fix list | Left for task 2 |
|---|---|---|
| NEW-1 | Moved by F-1: each frozen row is re-trained with report seeds disjoint from the search seeds, and the baseline uses the same report fit | R-RUN-7 cites F-1 once it is applied. R-INT-3's twin plants training noise and states its expected values |
| NEW-2 | Not moved. F-5 and F-27 leave the exhaustion values and the mapping of verdicts to task 2 | All of it |
| NEW-3 | Partly: F-16's per-seed pairs make a paired re-fit natural | What the precondition compares against |
| NEW-4 | Not moved. Switches are task 2's. U-SUB-2's tuned baseline is task 6's (`blocking-decisions.md:93`, `:203`) | All of it, and the tuned baseline once it lands |
| NEW-5 | Not moved. F-26 makes G3 bind a number to its cell, not to a claim. Task 6's list of attacks it does not stop includes "The words around a bound number" (`blocking-decisions.md:417`) | The invariant in R-INT-8. G3's mechanism is task 6's |
| NEW-6 | Partly: F-6 runs the baseline's fits and search scoring at admission, and F-16 sets one seed list per role and a seed floor | R-RUN-6's definition of the spread, per gate, with the number of scorings each gate gets |
| NEW-7 | Largely: F-11 runs the null "through the engine's own loop", with at least 100 replications and ±3 SE, and adds a null control on the false-success rate | R-MEAS-10's definition, its test, and the twin that turns off the floor |
| NEW-8 | Largely: F-3 says what agent code produces "is a released result and is never re-run", and F-16 says "A failed seed invalidates its row" | R-OPS-7, R-STATE-7 and R-RUN-6 follow; the compute of every attempt |
| NEW-9 | Partly: F-25 computes IR-29's family check per run, from the recorded routing; F-22 turns clauses about people into records or process rules | The scope of R-OPS-12; R-MEAS-5's comparison with the authors, its held-out prompt, and the transfer control |
| NEW-10 | Partly: F-9 requires that a setup control run "against the production sandbox ... a control run against a mock of the component it tests does not count" | Twins or positive controls per clause |
| NEW-11 | Partly: F-6 allows at most k attempts, with packaging iterating on search; F-15 scores C_base as a row | The refusal's own control; role files fixed across versions |
| NEW-12 | Partly: F-10 allows retries only for causes on a list written in advance, and refuses a run registered after the others' test events | Budget raises and resumptions by rule; chain registration in R-RUN-3 |
| NEW-13 | Moved by F-5, which adds the end state and how it counts | R-RUN-5, R-MEAS-2 and R-MEAS-3 follow |
| NEW-14 | Moved by F-46, which states the three reads as exceptions awaiting Vlad's confirmation | R-INT-3 flags the departure meanwhile |
| NEW-15 | Partly: F-13 marks I1's re-training as ours, and F-12 replaces "is positive" | The checker rules, and the remaining text fixes |
| EI-2, EI-13, EI-17, EI-20 remainders | F-2 narrows the public-label path; F-7 and F-13 cover EI-13; F-6 covers EI-17; F-16 covers EI-20 | Follow each when applied |

**The Codex review, within this lens.** I concur with six of its findings:
- **P1, R-INT-10's repairs:** check 1, and EI-5.
- **P1, R-INT-3's test against the sealed check:** check 1, and EI-3.
- **P1, R-MEAS-1's fixture:** EI-3 (a), which I found independently.
- **P2, R-STATE-1's edit-and-restore clause:** EI-16.
- **P2, R-INT-9's twin:** check 3.
- **P2, R-MEAS-10's zero margin:** NEW-7.

Its other findings are outside this lens:
- **P1, the rollback after a `Reject` (R-STATE-3):** it bears on integrity only because the rollback must leave an audit row, as R-STATE-3 requires for every change.
- **The checker's indexing and padding defects.**
- **The budget-reset test.**

## 5. Verdict

**Close, and most of the design can start now.**

What is closed:
- The cores of the four blockers are closed.
  - Test labels are absent from every agent sandbox, and agent code runs only in harness jobs, without network (EI-2).
  - Agents and their code cannot write results, verdicts, the ledger or behaviour files, each proven by an enforcement twin (EI-4).
  - The requirements state invariants, and leave the timing of the test split to task 6 (EI-3).
  - Every test names its tier, and the setup guards run for real beside twins (EI-1).
- No requirement decides one of task 6's blocking rows.

What task 3 can design now, against these files: the harness boundary, the access policies, the stores and their writers, the hook points, the records, and the tail as a stage.

What it should not yet design against: the numeric gates and measurement controls this revision added. As written, they do not do what they claim.
- The ablation precondition decides nothing, re-reads a selected record, and trusts a switch its author scopes (NEW-2 to NEW-4).
- The noise floor and the null control can pass without measuring anything; both use my own first-review words (NEW-6, NEW-7).
- Agent code can choose its draws by failing on purpose (NEW-8).
- The reporting judge cannot be held out on the subscription, and nothing measures what that costs (NEW-9).
- The tail, as task 6's first version sets it, carries the winner's seed luck into every reported test gain, while R-INT-3's twin can stay green (NEW-1). Task 6's own review has already accepted the fix, as F-1.

What has to happen first:
1. Fix NEW-1 to NEW-10.
2. Resolve the four contradictions of check 1.
3. Apply task 6's F-0 to F-46, and re-check the eleven provisional rows.

Until then, task 3 should mark these as pending in its contracts: R-STG-9's precondition, R-RUN-6's floor, R-MEAS-10, R-RUN-7's test event, and R-MEAS-5.

## Appendix: the simulation behind models A to C

Run inline on 2026-10-02. It is not saved in the repository, because this check is read-only; save it under `playground/` so the numbers can be re-run.

The model:
- Every candidate's true gain is 0.
- Each harness scoring is one draw of unit variance.
- E_base is one draw per task.
- A gate passes when the record minus its reference is at least the margin m.
- Margins are in units of one scoring's standard deviation.
- "Up to 3 scorings" is a subset or full-set loop with the critic scripted to `Good` and N_eng = 2.

```python
# Closure-check simulations (2026-10-02). Model: true gain 0 for every candidate; each harness scoring
# is a unit-variance draw; E_base is one draw per task; a gate passes when record - reference >= m.
import random, statistics as st
random.seed(12345)
g = random.gauss

def veto(base, m, tries):                     # blocked Good -> Engineer: up to `tries` scorings
    for _ in range(tries):
        x = g(0, 1)
        if x - base >= m:
            return x
    return None

N = 200_000
print("A  null idea, subset veto: pass rate")
for m in (0, 1, 2):
    one = sum(veto(g(0, 1), m, 1) is not None for _ in range(N)) / N
    three = sum(veto(g(0, 1), m, 3) is not None for _ in range(N)) / N
    print(f"   margin {m}: 1 scoring {one:.3f}, up to 3 scorings {three:.3f}  (n={N})")

print("B  ablation precondition for a null idea that passed the full-set veto (ablation margin = veto margin)")
for m in (1, 2):
    a = b = c = n = 0
    while n < 50_000:
        base = g(0, 1); best = veto(base, m, 3)
        if best is None:
            continue
        n += 1
        a += best - base >= m                   # control reproduces E_base exactly (same seeds, same code path)
        b += best - g(0, 1) >= m                # control is an independent fresh draw
        c += g(0, 1) - g(0, 1) >= m             # fresh re-fit of C_best vs fresh control, independent noise
    print(f"   margin {m}: vs E_best, control = E_base {a/n:.3f}; vs E_best, fresh control {b/n:.3f}; "
          f"fresh re-fit vs fresh control {c/n:.3f}  (n={n})")

print("C  20 null candidates, winner chosen on search, scored on report with the same fitted artifact")
for sf in (1.0, 0.0):
    s, r = [], []
    for _ in range(20_000):
        cands = [(g(0, sf), g(0, 1), g(0, 1)) for _ in range(20)]   # (fit noise, search eval, report eval)
        f, es, er = max(cands, key=lambda c: c[0] + c[1])
        s.append(f + es); r.append(f + er)
    print(f"   fit sd {sf}, eval sd 1: search gain {st.mean(s):.2f}, report gain {st.mean(r):.2f}  (n=20000)")
```

Output:

```
A  null idea, subset veto: pass rate
   margin 0: 1 scoring 0.498, up to 3 scorings 0.749  (n=200000)
   margin 1: 1 scoring 0.239, up to 3 scorings 0.447  (n=200000)
   margin 2: 1 scoring 0.079, up to 3 scorings 0.177  (n=200000)
B  ablation precondition for a null idea that passed the full-set veto (ablation margin = veto margin)
   margin 1: vs E_best, control = E_base 1.000; vs E_best, fresh control 0.515; fresh re-fit vs fresh control 0.240  (n=50000)
   margin 2: vs E_best, control = E_base 1.000; vs E_best, fresh control 0.323; fresh re-fit vs fresh control 0.077  (n=50000)
C  20 null candidates, winner chosen on search, scored on report with the same fitted artifact
   fit sd 1.0, eval sd 1: search gain 2.64, report gain 1.33  (n=20000)
   fit sd 0.0, eval sd 1: search gain 1.87, report gain -0.01  (n=20000)
```
