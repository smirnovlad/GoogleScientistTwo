# Record: `system-architect` closure check (2026-10-02)

- **Reviewed:** the second version (`adc3484`) against this reviewer's own wave-1 findings.
- **Record:** the reviewer's final message, verbatim below, unchanged.

---

# Closure check: system-architect, second version (adc3484)

**What I checked:** my own wave-1 findings, and nothing else. I read:
- the index, `docs/integrity/blocking-decisions.md`;
- the four files in `docs/integrity/decisions/`;
- `docs/reviews/integrity-blockers-2026-10-02/fix-list.md`, including the amendments A1 to A6 and the contested points in section 5;
- the updated `docs/integrity/README.md`.

**Verdict:** all 30 of my findings and tensions are fixed. The blocker's substance is fixed. Two findings carry a one-line residual: B1, where an optional fresh start leaves a bounded re-roll, and M3, where IR-5.3 and IR-41.2 re-open the scope of E_base's records. The coordinator accepted the owner's three contested points that touch my findings (1, 4 and 5), and I accept them too.

Task 3 can now write the contracts of the scoring runner and of the audit without re-deciding any of the four questions, with one narrow exception. The fixes introduced five new defects, all MINOR. The first of them, the correction event, is that exception.

## 1. My findings

| Finding | Verdict | Where | Remaining |
|---|---|---|---|
| B1: one use counted as jobs; no resume | fixed | index IR-32, IR-33.1–33.5, IR-34, IR-35, IR-36; U-TOP-5 IR-14.5, IR-15.5; A-INT-1 IR-24 (b)(e) | Part (a): a fresh start for a listed cause is still optional (IR-34.2, IR-18.4), which leaves a bounded re-roll. See N5. |
| M1: the freeze's contents, *ours*, and the baseline in the test event | fixed | U-TOP-5 IR-14.2, IR-14.3, IR-14.4; U-INT-4 IR-8.1 | none |
| M2: the gates on the primitive; the tail as a stage | fixed | index IR-39 (pseudocode, a failure table for every step, end state IR-39.3, termination table IR-39.4), IR-40, IR-40.1–40.2; A-INT-1 IR-21.1, IR-21.6; A-NOTE-1, A-TOP-2 and U-TOP-2 added to the constraint tables | none. Contested point 4 (G4 and G5 nested, not filters) is right, and the sketch now matches the table. |
| M3: per-task events and their scope; the race between parallel runs | fixed | Terms (admission, baseline key, stores and ledgers); U-INT-4 IR-4.2; U-TOP-5 IR-15.1, IR-15.2, IR-15.5, and the ⛔ WHY NOT "before round 0" | The correction path re-opens the scope of E_base's records. See N1. |
| M4: the audit's results landing in engine stores | fixed | U-INT-4 IR-5.3, IR-5.6; U-TOP-5 IR-14.6; A-INT-1 IR-22.4; A-INT-3 IR-30.2 | The reporter's identity is not stated. See N3. |
| M5: one name for the enforcer and what it enforces | fixed | Terms (scoring runner, scoring items); U-INT-4 IR-6.1, IR-6.3, IR-6.4, and the ⛔ WHY NOT "a harness per task" | The baseline key omits the runner's version. See N2. |
| M6: "mock, $0" testing the mock | fixed | index IR-37, the fixtures list, the IR-37 control; every Mode column | none |
| M7: no configuration key | fixed | Terms (configuration hash, campaign record); U-TOP-5 IR-18.1–18.6; A-INT-3 IR-29.2, IR-29.6 | none |
| m1: bundled IDs; G-IDs duplicating rules | fixed | index section 2 (sub-IDs), the gate names; A-INT-1 IR-21.5 | none |
| m2: the fixer counted as an author; IR-27's inputs | fixed | A-INT-3 IR-26, IR-27.1 | none |
| m3: the literal scope of IR-1 and IR-17 | fixed | U-INT-4 IR-1 (its scope bullet); U-TOP-5 IR-17.1, where G3 to G5 are named as the exception (contested point 1, accepted) | none |
| m4: what a change of routing sets off | fixed | A-INT-3 IR-27.4, IR-29.3, IR-29.6, IR-31.4 | none |
| m5: G3 fixing the interface of drafting | fixed | A-INT-1 IR-21.2 (the invariant, the mechanism, figures) and the ⛔ WHY NOT against evidence tags; the U-DRAFT-1, U-PEER-4 and A-INT-2 constraint row | none |
| m6: IR-7's precondition as data | fixed, as changed | U-INT-4 IR-7.1; the fail mapping goes to task 2 under U-SUB-1, as the fix list decided | none |
| m7: a cut of what a model reads, with no owner | fixed | U-INT-4 IR-5.4; U-TOP-5 IR-11.4 | none |
| m8: the reporter, the reported table and the run registry undefined | fixed | Terms | The reporter's identity against IR-29.1. See N3. |
| m9: C_base without a contract | fixed | U-INT-4 IR-4.3, with A5's hash check | none |
| m10: no way to correct a locked item | fixed | U-TOP-5 IR-41; U-INT-4 IR-5.6; index section 7 | Its scope against admission is open. See N1. |

| Tension | Verdict | Where |
|---|---|---|
| T1: IR-14 against IR-8 (a) | fixed | IR-14.4, IR-8.1, the `time_baseline_with` step of IR-39 |
| T2: IR-13's cap against G2 retries | fixed | IR-13.3, IR-40.1, IR-21.1 |
| T3: IR-21 against the U-INT-1 row | fixed | IR-21.1, IR-21.6, IR-40.2 |
| T4: no resume | fixed | IR-33, IR-34 |
| T5: IR-15's attempts against IR-14's refusal | fixed | IR-15.5, IR-33.3 |
| T6: a retry against IR-20's halt | fixed | IR-35.1–35.3, IR-20.2 |
| T7: audit records against IR-29 and IR-30 | fixed | IR-5.3, IR-14.6, IR-30.2 |
| T8: the author against the fixer | fixed | IR-26 |
| T9: IR-17 against G4 and G5 | fixed | IR-17.1 |
| T10: the rows of the freeze | fixed | IR-14.3; the U-TOP-5 decision table |
| T11: IR-1 against ScholarPeer's score and the novelty sort | fixed | IR-1's scope bullet |
| T12: the ledger per run against per-task events | fixed | the stores and ledgers term; IR-5.3 |

## 2. Requirements

- **R2: met.**
  - Every bundled rule now has sub-IDs, each one invariant.
  - The hooks G1, G6 and G7 are names that point to their rules, not second IDs.
  - The clauses about people are marked as process rules, recorded but not enforced: IR-15.6, IR-29.5 and IR-31.5. IR-29.6 makes "seen its verdicts" checkable against an access log.
  - I found no tension left among the rules I checked, apart from N1, N3 and N4 below.
- **R8: met, with one narrow gap.**
  - **The runner's contract** can be written from these rules as they stand:
    - job identity: IR-32;
    - release and attempts: IR-33;
    - the read table: IR-11;
    - the four kinds of job that read report: IR-14.6;
    - hashing: IR-6.3, IR-6.5;
    - stores by scope: IR-5.3;
    - halts by class: IR-35.
  - **The audit's contract** can be written from these rules as they stand:
    - its identity and resume: IR-36;
    - its inputs: IR-22.1;
    - its outputs and stores: IR-22.4, IR-30.2;
    - its checks: IR-23, IR-24;
    - what it does to what we report: IR-25.
  - **What IR-33.3 leaves open** is what exhausted attempts do. That belongs to U-TOP-2's owner, which is task 3 itself, so it is not a re-decision of the four questions.
  - **The gap:** the correction event (N1). Task 3 would have to decide whether a correction re-admits the task, and in which scope E_base's corrected records live.
  - **Over-reach:** no rule fixes a component boundary it does not need. The fixtures are now requirements on task 7, not a design.
- **R10: met.**
  - Every file is under 600 lines: the index is 286, and the decision files are 208, 158, 152 and 116.
  - Each decision file stands alone, citing the index's terms rather than splitting one subject in half.
  - The new stage, the tail (IR-39), has pseudocode and a failure branch for every step.

## 3. New defects the fixes introduced

All five are MINOR. There is no BLOCKER and no MAJOR.

**N1 · MINOR · IR-41.2 against IR-5.3, IR-6.4, IR-14.5, IR-15.1 and IR-15.5: the correction event has no consistent scope.**
- **Evidence:**
  - IR-41.2 re-runs "with the corrected item (a new manifest version)", and says "E_base's identities are corrected in the same event".
  - IR-5.3 puts correction events in run scope.
  - IR-6.4 says a change to a scoring item "changes the baseline key", and IR-15.1 requires an admission for each baseline key. That admission includes a sealed check, which counts against IR-15.5's "at most k attempts".
  - IR-14.5 also says the runner "refuses a report job whose identity the freeze does not list", while IR-41.4 gives corrections "identities of their own".
- **What it makes expensive:** with N runs of a task, E_base would be corrected N times, in run scope, possibly with N different values. A correction either triggers a re-admission, which can exhaust k and so block the correction, or it contradicts IR-15.1. The scope of correction records is part of the runner's contract, so task 3 must settle this.
- **Fix:**
  - E_base's corrected records are task scope, released once per (new baseline key, identity), and every run refers to them.
  - A correction's manifest version inherits the task's admission with no new sealed check, and is not counted against k.
  - IR-14.5 names the correction kind (IR-14.6) as the exception.

**N2 · MINOR · IR-6.4 and the baseline key: a change to the runner can silently unpair comparisons with E_base.**
- **Evidence:**
  - IR-6.4 says "A change to the runner is a change of engine version … never of a manifest".
  - The baseline key, in the Terms and IR-15.2, omits the runner's version, so E_base's admission records, scored by the old runner, stand for runs scored by the new one.
- **What it makes expensive:** a fix to the runner that moves values, for example in validation or in input ordering, mixes the two versions inside every gain.
- **Fix:** on a change to the runner, re-score E_base on search under the new runner and compare it with the admission record, with no read of report. Keep the admission records only if the two agree within the seed noise. Otherwise the change is value-changing, and the task is admitted again.

**N3 · MINOR · The reporter's term against IR-29.1 and IR-30.2: the reporter is engine code that reads the audit store.**
- **Evidence:**
  - The Terms define the reporter as "engine code that computes every reported table … from released records, the audit store and the run registry".
  - IR-29.1 puts the reporting auditor's verdicts "outside everything that any engine job or engine agent can read".
  - IR-30.2 says the audit store is one that "no engine job reads".
- **Fix:** give the reporter an identity of its own, which runs outside every run, and whose output never reaches a run. Then define "engine job" as a job of a run.

**N4 · MINOR · IR-5.6 against IR-29.1: only exported runs close their ledger.**
- **Evidence:**
  - IR-5.6 says "The run ledger closes at export".
  - Runs that end without a freeze, or in IR-39.3's end state, never export.
  - IR-29.1 has the auditor read "the closed ledgers".
- **Fix:** the run ledger closes when the run ends, whatever its end state.

**N5 · MINOR · IR-34.2 and IR-18.4: a fresh start for a listed cause is optional (the residual of B1 (a)).**
- **Evidence:** a fresh start is "allowed only for a cause on the campaign's list and within its bound". A person can therefore spend that allowance only on runs whose search went badly. The old run still counts as a failure, but the new run adds a chance of success that a well-going run never gets.
- **This is not contested point 5.** Point 5, accepted by the coordinator, settled when a late fresh start is allowed. It did not settle whether a fresh start, once its cause occurs, is optional.
- **Fix:** for a listed cause, a fresh start is mandatory, exactly once per halted run. Or: a listed cause gives no fresh start at all. Either way, nobody chooses.
