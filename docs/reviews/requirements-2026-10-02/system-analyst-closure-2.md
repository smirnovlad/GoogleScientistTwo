# Narrow closure check: task 2's requirements at fd9bcf9, against my closure of c2ad177

Read-only. I edited no file in the repository and changed no git state; `git status` is still clean. I planted the defects only in `git archive` copies under my session scratchpad, and deleted each copy after its run. Requirement files are cited without `docs/requirements/`.

## 1. The checker runs, and the new rules fire on real files

On the real tree, `python3 playground/paper/requirement_coverage.py` exits 0. It reports:
- `total 177 172 29 5`
- `requirements: 82 (RUN 8, PRIM 10, STG 13, AGT 9, STATE 10, INT 10, MEAS 10, OPS 12); leave-out decisions: 5`
- `task-2 register rows: 33; … 15 confirmed, 18 refined`
- `0 problem(s)`

`--selftest` passes 52 of 52 cases, and exits 0. `check_citations.py` gives `27 file(s) checked, 0 problem(s)`. An unmutated copy in scratch also gives 0.

I planted one defect per new rule in a copy of a real file. Every one gives exit 1 and names the right rule:

| Rule | Planted in a copy | Result |
|---|---|---|
| test-tier | R-RUN-1's Test changed from "Logic, in mock mode: …" to "In mock mode: …" | `test-tier: 01-run.md:7 R-RUN-1: the Test field opens with neither Logic nor Enforcement`, 1 problem |
| task-attribution | R-RUN-1's "U-TOP-5, task 6" changed to "task 5" | `task-attribution: … gives U-TOP-5 to task 5; the register gives it to task 6`, 1 problem |
| IR- citation | R-OPS-12's *Depends on* line (A-INT-3) deleted; its text still cites IR-29.4 | `integrity-dependency: 08-operation.md:106 R-OPS-12: cites IR-29 and depends on none of A-INT-1, A-INT-3, U-INT-4, U-TOP-5`, 1 problem |
| loose U-/A- ID, dash | `U–TOP–5` under R-RUN-1's *Depends on* | `malformed-id: … writes 'U–TOP–5'`, plus the knock-on `integrity-dependency` |
| loose U-/A- ID, padding | `U-BASE-01` under R-RUN-2's *Decides* | `malformed-id`, plus the knock-ons `undecided` and `decision-table` (5 problems) |
| HTML comment, trace | R-STG-2's `P-SEED-1 … 4` wrapped in `<!-- -->` | `unmapped: P-SEED-1`, `unmapped: P-SEED-4`, and 3 `column` problems |
| HTML comment, *Depends on* | `<!-- U-TOP-5, task 6 -->` under R-RUN-1 | `integrity-dependency` (the hidden row no longer counts) |

Both defects my previous closure showed passing at exit 0 now fail: a trace hidden in a comment, and an en-dash ID under *Depends on*. One limit remains: the task-attribution rule checks only a clause that says "task N", so a clause that names no task is never compared with the register.

## 2. Status of the items checked

| Item | Status | Evidence | What remains |
|---|---|---|---|
| NEW-1 · attribution never established | **closed** | ABL row and Ablation Critic row: `03-stages.md:31,55`. R-STG-9: `03-stages.md:162`, tests at `:174,:177`. R-MEAS-1's third reading and its test: `07-measurement.md:15,23-24`. A-EVAL-1 added to the presumed-proposals table: `requirements.md:219` | Minor, skipped: which mark applies when a pass-k `Reject` restores pass k−1. |
| NEW-2 · last repair unchecked | **closed** | After any repair, every check of the hook runs again: `06-integrity.md:122`. Test with a twin: `:129` | none |
| NEW-3 · failure map | **partly closed** | Failure table: `03-stages.md:37-61`. Harness and machine faults suspend: `02-primitive.md:122`, `08-operation.md:63` | **Gap 1:** the table has no row for the Subset Critic, the Full-Set Critic, the Result Comparison Agent or the Initial Idea Generator (P-ROSTER-8, 11, 19, 3). Yet R-PRIM-10's test expects a failed critic to take "its configured branch" (`02-primitive.md:128`). Nothing at load checks the table against the roster. **Gap 2:** only half closed; outages of the LLM provider, of tools and of search still become research outcomes (C-2). **Gap 3:** open. "A session that reaches its budget is stopped and recorded" (`08-operation.md:36`) still has no next step (C-1). |
| NEW-4 · stop, resume, one outcome | **closed** | Outcomes are final: `01-run.md:76`. Suspension and amendments: `:124`. A resume is refused after an outcome: `:81`. Audit row for a resume or amendment: `05-state.md:30,33` | Two new defects in the suspended state itself (C-3). |
| NEW-5 · budget unit | **partly closed** | Named resources, and dollars only for a metered charge: `08-operation.md:36`. Test, including the dollar-validation case: `:40` | No test case for machine-hours. Budgets are not among the values whose absence stops the configuration loading (`03-stages.md:230` omits U-COST-1), so a configuration with no budget loads. |
| NEW-6 · threshold 8 | **partly closed** | 8 belongs to the paper profile and its ScholarPeer reviewer: `03-stages.md:200,230`. Departures: `:203,232`. A missing calibration record fails to load: `:207,235` | The claim "a value another task owns has no default, and the configuration refuses to load" (`:230`) is not true as written. Budgets (U-COST-1), the reconciliation bound for units in doubt, and the guardrail bounds and aggregation that `01-run.md:91` gives to task 5 are all missing from the list. Wall-clock bounds have two owners (C-1). |
| NEW-7 · units in doubt | **partly closed** | Settled as spent within a bound, then run once more: `05-state.md:66`. Test: `:74` | The test still allows "the unit in flight at most once more" when the run is killed between a call's return and its record. A blind retry therefore passes. No case shows a unit whose result *can* be recovered being reconciled with zero further calls. The bound has no value and no owner. |
| MISS-20 · duplicates and attempts | **closed** | `03-stages.md:24,29,76,81,135,140,230` (M = 3 × N_seed; 3 attempts per round for A_Evolve) | Minor: the duplicate rule is given to task 3 under U-SEED-2 (`:76`), a row about the score's scale and query, and it is not in the presumed-proposals table. |
| CONT-11 · the supersede sentence | **closed** | `requirements.md:28` | none |
| CONT-19 · the ablation's exit | **closed** | Same evidence as NEW-1 | none |
| U-EVO-4 flag | **partly closed** | *abandoned*: `01-run.md:74`. The failing unit's key: `:76`. A budget stop becomes a suspension: `:124`. A unit in doubt is settled: `05-state.md:66` | "Dependency unavailable", one of the flag's five asks, is still handled only for the harness (C-2). |
| CHK-6 · bare leave-out | **closed in substance** | X- decisions gain *Depends on*, checked against their *Why* (`requirement_coverage.py`, `X_FIELDS`), with a self-test case | Neither a decider nor a date is a field. The file header (`requirements.md:3`) dates every decision and gives it to task 2. The disposition (`fix-list.md:79`) is silent on both; a one-line "declined" would settle it. |
| NEW-15 · bookkeeping | **closed** | All 17 questions, each with a *Where* cell: `requirements.md:105-127`. Q-16 is now at `:126`. The cell at `fix-list.md:64` is corrected. CHK-6 and CHK-9 are disposed at `fix-list.md:79` | `DEVELOPMENT_PROCESS.md:582` still says "ten decisions", but it is the c2ad177 narrative and was true then. |

## 3. New major contradictions and omissions in this revision

### C-1 · Which bound suspends a run is stated three ways, and one reading reintroduces a re-roll

- **The texts:**
  - R-RUN-8 (`01-run.md:124`): "a budget, a wall-clock bound, … suspends the run".
  - R-OPS-7 (`08-operation.md:60`) gives "each session, harness job and task" a wall-clock bound.
  - A harness job's own timeout is a released result, never re-run. R-PRIM-10 (`02-primitive.md:121`) says so, citing task 6's IR-33.4, which reads "a timeout against the manifest's limit" (`blocking-decisions.md:119` at adc3484).
  - R-RUN-2 says a job beyond the compute envelope "has no result" (`01-run.md:26,36`). A released *failed* result counts against its row, and "no result" does not.
  - R-OPS-7's test (`08-operation.md:69`) says only that the job is "stopped and recorded".
  - A session's budget stop has no next step (`08-operation.md:36`). A session timeout, by contrast, is an agent failure, mapped through the role table (`02-primitive.md:120`).
- **Why it matters:** read as R-RUN-8 reads, a job that times out suspends the run. On resume, R-STATE-7 re-runs "one stopped before it released a result … under the same identity" (`05-state.md:65`). That is exactly the re-roll IR-33.4 forbids.
- **Owner conflict:** R-STG-13 gives the wall-clock bounds to task 3, U-TOP-2 (`03-stages.md:230`). R-OPS-4 makes wall-clock time a budget resource whose budgets are task 5's, U-COST-1 (`08-operation.md:36`).
- **Fix:** one table of each level (agent call, session, harness job, task) against each bound (budget, wall-clock), with its outcome:
  - harness job: a released result;
  - session: an agent failure mapped by role, or a named row of its own;
  - task: suspended.
  Give it one owner.
- **Test:** agent code that times out is released and never runs again after a resume. A Subset Coding Agent session stopped at its budget ends in that row's outcome.

### C-2 · "Infrastructure" has two definitions, and outages still become research outcomes

- **The texts:**
  - R-RUN-8 suspends on "an infrastructure failure that outlasts its retries".
  - R-PRIM-10, R-OPS-7 and the preamble of the failure table (`03-stages.md:41-42`) limit that to "the harness or the machine".
  - R-PRIM-10 lists "an outage of a tool" among the step failures mapped by role (`02-primitive.md:120`).
- **What follows:** an outage of the Claude backend that is not a usage-limit answer, of Claude Code, of the novelty search or of the bibliographic lookup goes through the role table:
  - coding agents: the idea becomes `Bad`, with the reason *error*, and A_Evolve learns from it (`03-stages.md:50`);
  - Initial Drafter: *error after retries*, which is final (`:57`);
  - the reference check in the tail: a failed check that no repair can fix, so *test event done, not exported*, final (`03-stages.md:61`, `06-integrity.md:122`). This loses a run whose one test event, under IR-14, cannot be repeated.
- **Fix:** an outage of an outside system suspends, as a harness fault does. The role table covers only failures of agent output.
- **Test:**
  - the backend scripted to refuse connections through a Subset Coding Agent's retries suspends the run, and no idea becomes `Bad`;
  - the bibliographic search unreachable in the tail suspends the run; after the resume the run exports, and the report-job count stays at 1.

### C-3 · A suspended run has no exit, and abandoning one follows no rule

- **The contradiction:** R-RUN-8 says "a person may end a suspended run" (`01-run.md:124`), with no rule. Q-9 says "a resume, a budget raise and an abandonment follow a rule fixed in advance" (`requirements.md:119`).
- **What is missing:** nothing bounds how long a run may stay suspended. `07-measurement.md` never mentions a suspended or abandoned run (grep: 0 hits). A run left suspended therefore has no outcome and drops out of every denominator, so R-RUN-5's "every task … ends with one outcome" cannot be tested for it.
- **Why it matters:** abandoning a run before its test event, chosen by how its search records look, puts it at U-EVAL-1's value for a failed task. R-MEAS-3's "no more than that gain" (`07-measurement.md:40`) caps only runs that have a measured gain, so that value can exceed what the run would have measured. This is the integrity closure's NEW-13 mechanism, on the other side of the freeze.
- **Fix:** abandonment falls under the rule fixed before admission, applied to a whole class of runs. The report either counts a run still suspended at report time as a failure in every denominator, or refuses to compute while any registered run is suspended.
- **Test:**
  - an abandonment outside the rule flags the report;
  - a report built with one run still suspended counts it, or refuses.

### C-4 · R-RUN-5's ten outcomes are not the union it claims

- **What is missing:**
  - Task 6 ends a run when a frozen artifact cannot be restored: "the run ends as a failure with that cause" (`blocking-decisions.md:177`). This can happen after the test event, and none of the ten outcomes fits it.
  - The Baseline Coding Agent's failure gives "not admitted, *error after retries*" (`03-stages.md:49`). R-RUN-5 defines that outcome for a run (`01-run.md:73`), and at admission no run exists yet.
- **Why it matters:** the test of "ten in all" (`01-run.md:81`, `requirements.md:93`) stays green while a post-test-event ending goes unrecorded.
- **Fix:** add the unrestorable-artifact ending, or map it explicitly to an existing outcome. State which outcome a failure at admission gives.

## Verdict

Of the items checked, 6 are closed (NEW-1, NEW-2, NEW-4, MISS-20, CONT-11, CONT-19), CHK-6 is closed in substance, and NEW-15's bookkeeping is complete: all 17 questions are answered, each with its pointer. NEW-3, NEW-5, NEW-6, NEW-7 and the U-EVO-4 flag are partly closed. None regressed.

The checker is sound. It exits 0 with 52 of 52 self-test cases passing, and each of the five new rules fires on a mutated copy of a real file.

The revision brought in a coherent suspended state, but where it meets the failure model it still leaves four major defects:
- **C-1:** whether a wall-clock or budget bound suspends the run depends on which file you read, and one reading re-rolls agent code;
- **C-2:** outages of outside systems other than the harness still become `Bad` ideas or final outcomes, after the one test event included;
- **C-3:** a suspended run can wait forever, or be abandoned with no rule, and leave the denominators;
- **C-4:** the "ten in all" outcome list misses one ending task 6 defines.

Each is a local edit of a sentence or a table row, plus a test case. I would not close task 2 until C-1 to C-3 are fixed, together with the critic rows missing from the failure table and the refusal to load without a budget. C-4, NEW-7's stricter test, and the minors can be ticked into `TODO.md`.

Relevant files:
- `docs/requirements/01-run.md`
- `docs/requirements/02-primitive.md`
- `docs/requirements/03-stages.md`
- `docs/requirements/05-state.md`
- `docs/requirements/08-operation.md`
- `docs/requirements.md`
- `playground/paper/requirement_coverage.py`
