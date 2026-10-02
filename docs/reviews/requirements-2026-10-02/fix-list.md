# Fix list for the requirements' first draft (commit ff1faaa)

Every finding of the review gate, merged, with what was done about it. The sources, all in this
folder, verbatim:
- `system-analyst-elicitation.md`, the independent inventory made before the draft was read
  (labels MISS, CONT, ORPH, CHK, Q);
- `system-architect.md` (labels SA);
- `evaluation-integrity-engineer.md` (labels EI).

Dispositions:
- **accepted**: fixed as proposed, or with the change named;
- **declined**: with the reason;
- **decided here**: a question the review raised for Vlad. His instruction to the coordinating
  session, recorded on `claude/engine`, is not to ask him anything, so task 2 decides it, with its
  reason, in `docs/requirements.md`, section *Decided here, not asked*;
- **covered by task 6**: answered by a rule of task 6's first version
  (`docs/integrity/blocking-decisions.md`, IR-1 to IR-31, on `claude/integrity-blockers` at
  d5d0d61). It arrived while this list was being written, and it is not yet reviewed. The
  requirement cites the rule by its IR- ID, lists the row under *Depends on*, and decides nothing
  of it.

## From the elicitation

The draft was written before the elicitation arrived, so the table compares the two: what the draft
already covered, and what it missed.

| Item | What it asks | Disposition, and where |
|---|---|---|
| MISS-1, CONT-2, Q-1 | The test split is scored once at the end; what P+ then reports, and what happens when a test number contradicts a claim written from validation numbers | Covered by task 6: the freeze, one test event, the final fill of both columns by engine code, and text-only changes afterwards (IR-14, IR-16, IR-17). New requirement R-RUN-7 makes that tail a stage of the run's sequence, and departs from P-META-2 |
| CONT-1 | The in-loop "full benchmark" puts test numbers in front of agents | Accepted: in the loop the full benchmark is every setting of the full grid, on its validation side (R-RUN-2, R-STG-3, R-STG-5) |
| CONT-3, Q-2 | Chained runs show the parent's test numbers to the child's agents | Decided here, with EI-14: the conversion of an export into the next G carries no report-role number, and every link's test event is counted (R-RUN-3, provisional on U-TOP-5) |
| CONT-4, Q-3 | U-BASE-2's tolerance against published numbers would score test before the search | Covered by task 6, which decides it the other way: IR-15's sealed check reads the test split once per task, before any candidate, and releases only pass or fail. R-STG-3 adopts it, and keeps U-BASE-2's branch, which is task 2's |
| CONT-5, MISS-8, Q-4 | ScholarPeer has no published implementation (task 4); the threshold 8 is on its own scale | Accepted: a reviewer contract; the threshold stored with the reviewer's version and derived by a recorded calibration rule (A-EVAL-3, task 6); the in-loop reviewer runs on the subscription, so R-AGT-5 departs from P-ROSTER-21 and P-ROSTER-46. Which reviewer is task 4's (U-PEER-3) |
| MISS-3 | Every step needs a failure branch; a malformed verdict must never map to accept | Accepted, new requirement R-PRIM-10, fail closed |
| MISS-4, CONT-6, Q-5 | Resume at a finer grain than a stage; CLAUDE.md says "stage" | Accepted: R-STATE-7 resumes from the last finished unit of work, and reconciles units in doubt. Decided here: a finer grain meets CLAUDE.md's rule as written, which stays unchanged |
| MISS-5 | A queryable decision trail per idea | Accepted, new requirement R-STATE-9 |
| MISS-6 | An audit row per core-state change and per paid call | Accepted: R-STATE-3 and R-MEAS-8 |
| MISS-7, Q-8 | The budget guard counts spend in flight; an unknown cost reads as at least X; the branch at the limit | Accepted: R-OPS-4 counts reservations and units in doubt. Decided here: at the limit the run stops with its record and no export, and resumes from it once the budget is raised; a subscription's usage window pauses the run instead (R-OPS-12) |
| MISS-9, CONT-7, Q-6 | One comparison rule per task for every numeric gate and the reported gain | Accepted, new requirement R-RUN-6: one rule in the manifest, read by hash. Decided here: the gates' entries are task 2's (A-ABL-3, U-SUB-1, U-SEL-1, U-ABL-5), the reported gain's formula task 6's (U-EVAL-1), the values task 5's, set before the task's first run |
| MISS-10, Q-10 | Reproducible, defined so it can fail | Accepted: R-OPS-6 requires both replay and re-execution |
| MISS-11 | Mock mode with no unknown ledger entry | Accepted: R-OPS-1 |
| MISS-12, CONT-13, Q-13 | Inputs larger than a model's context | Accepted: R-OPS-9 fails loudly or applies a recorded bound, never truncates silently |
| MISS-13, CONT-15 | Named profiles, the paper profile equal to App. A.2 | Accepted: R-STG-13 and R-OPS-2 |
| MISS-14 | One conformance test for all eleven stages and Listing 1 | Accepted: R-PRIM-1's test |
| MISS-15 | Swap a backend, a provider or a reviewer by configuration | Accepted: R-OPS-3's test |
| MISS-16 | Least privilege, and the policy in force in the record | Accepted: R-OPS-8 |
| MISS-17 | The export maps every number in P+ to a harness result | Accepted: R-INT-8 |
| MISS-18 | Run artifacts carry no secret, e-mail address or local path | Accepted, new requirement R-OPS-10 |
| MISS-19, CONT-14, Q-9 | Which human steps may happen between launch and export | Decided here, new requirement R-RUN-8: none; every stop ends or pauses the run with its record, and a person may resume it |
| MISS-20 | Generation loops are bounded, and reject duplicates | Accepted: R-STG-2 and R-STG-7 |
| MISS-21 | The task is validated before any spend | Accepted: R-RUN-2's test |
| MISS-22 | Wall-clock bounds per session, harness job and task | Accepted: R-OPS-7 |
| MISS-23 | Parallel results in a deterministic order | Already in R-PRIM-8; its test now checks the traces and A_Evolve's inputs |
| MISS-24 | A score that cannot be computed is unknown, not zero | Accepted: R-AGT-6 |
| MISS-25, Q-17 | Novelty retrieval excludes G's own paper and records dates | Accepted: R-AGT-6. Decided here: no date cut-off; each reference's date is recorded, so that a cut-off can be applied later |
| MISS-26 | Every agent has a success test | Accepted: R-AGT-9 covers every agent, judges with a pass rule |
| MISS-27 | Concurrent runs share GPUs safely | Accepted, new requirement R-OPS-11 |
| Summary 10, CONT-8 | The integrity hooks add sessions that analysis.md §9 does not count | Accepted: said in R-INT-4 to R-INT-6, and in the section on what is left to task 5 |
| ORPH-1, CONT-9, Q-7 | `codex/run-journal` holds a second requirements file (RJ-1 to RJ-7) and engine code, untracked | Decided here, with SA-6: `docs/requirements.md` is the one home of requirements. RJ, BA and VT are component contracts that refine named requirements, mapped in *Component contracts written elsewhere*; on merge they move beside their components. The checker fails on a file in `docs/requirements/` that defines no requirement |
| ORPH-2, CONT-11 | traceability.md's component column contradicts the register in four cells | Accepted: `docs/requirements.md` says that the requirements supersede the candidates where they differ; the column is task 3's to update |
| ORPH-3 | U-ART-11's score feeds no decision | Already decided as a record only (R-STG-7, R-STG-9) |
| ORPH-4 | A-ART-5 has no detector and no branch | Accepted: R-STG-4 compares the idea's component list, and a step that changes it is refused and counted |
| A-TOP-1 flags, CONT-19 | An empty limitation set at the limit; the ablation's exit is not marked | Accepted: R-STG-1 fails an empty set; R-STG-9 records the ablation exit, which R-MEAS-1's third reading reads |
| A-TOP-2 flag, CONT-10, Q-12 | 16 verifier calls or 16 judged expansions | Kept: 16 rounds of extraction, the first included, so 15 judged refinements, counted like Table 5's and Figure 9's rounds; the reason is now in R-STG-1 (corrected in the third revision: this cell read 16 judged refinements) |
| U-BASE-2 flag | One failed reproduction ends the task | Changed by task 6: no agent edits the baseline (IR-4), and the check releases no gap (IR-15), so no repair loop is possible. The task ends with *baseline not reproduced*; a person may repackage the task as a new manifest version, and every attempt is reported (R-STG-3) |
| A-ABL-1 flag, Q-11 | A `Reject` in a re-ablation or in the meta pass | Accepted: a `Reject` of a promoted candidate undoes the promotion, and the flow continues as when the guard rejects it; a `Reject` of the selected idea ends the task (R-STG-9) |
| U-INT-1 flag | The filter's own failure | Accepted: fail closed after the retries, as a discard (R-INT-4) |
| U-INT-3 flag | A repair that fails | Changed by task 6: a gate whose retries are spent ends the task without export (IR-21). R-INT-10 sets the bound, two repairs per hook and manuscript version, and R-RUN-5 adds *manuscript gate failed* |
| U-EVO-4 flag | Human abort; the failing unit's ID; reasons for success branches | Accepted: R-RUN-5 |
| U-SEL-1 flag | Order of the inputs | Accepted: R-STG-8's test shuffles them |
| U-META-2, U-ABL-5, U-SEED-3 flags | Golden cases with a pass rule | Accepted: R-AGT-9 |
| Part 4.1, Q-15 | Ten leave-out candidates | Five left out (X-1 to X-5). Declined for the other five, which carry real requirements: P-CFG-17 (the roster's size), P-ROSTER-50 (the held-out judge), P-ART-11 (the run layout), P-BENCH-1 and P-BENCH-3 (task selection) |
| Part 4.1, *replaces* | A third status for departures from the paper | Accepted: a *Departs from* field; traceability.md's column marks a departure |
| Part 5 | Eleven group names carry a decision owned elsewhere | Accepted: each also traces to the requirement that carries the decision |
| P-TOP-1 | Its first clause cannot be tested in the engine | Accepted: R-RUN-1 marks it as judged at evaluation (R-MEAS-5) |
| CONT-16 | CLAUDE.md's rules began as the note's proposals | Accepted: one line in *How to read* |
| CONT-17, Q-16 | Where task 2 files a gap it finds | Decided here: as a requirement with its reason in `docs/requirements.md`, or as a row pending in its owning task; the register stays task 1's |
| Q-14 | Is matching the paper's numbers part of the goal | Decided here: no; the fair targets are traceability.md's Part 3, the mechanics and the planted behaviours |
| Part 6 | The checker's defects | Already caught: CHK-2 to CHK-5, 7, 8, 10 to 14, 18 to 20 and 22. Added: placeholders in a field (CHK-1), split pairs (CHK-15), the stage table (CHK-16), malformed IDs (CHK-17), a file with no requirement (CHK-21), and printing the pending rows and departures. The self-test moved to its own module, to keep both files under 600 lines. Added in the third revision: CHK-6, an X- decision now has a *Depends on* field for the rows it rests on, checked like a requirement's; an X- decision's decider and date stay in the file's header, which dates every decision and gives it to task 2, so no field is added for them; CHK-9 declined, since a check of a reason's content would only test its wording, and the analyst's scan found a source named in all 19 untraced requirements |

## From the system-architect review

| Finding | What it asks | Disposition, and where |
|---|---|---|
| SA-1 · blocker | R-PRIM-2's closed lists cannot hold the draft's own stage table: EVO's population loop, the vetoes, SEL's choice, A_Coder, the plan-then-execute generators, META's nested pass | Accepted: R-PRIM-2 becomes a floor of behaviours the primitive must express, with SA-1's table as its acceptance cases, and the parameter design stays with A-NOTE-1 (task 3). The assessor kinds become one list. The out-of-domain cells of the stage table are rewritten: EVO's verdict map and at-limit value, the outcomes of BASE and ABL, the SUB, FULL and SEL assessors as an LLM judgement behind a deterministic precondition, META's generator |
| SA-2 · blocker | The meta restart is stated three ways, and the run's order is not data | Accepted: R-RUN-4 states the behaviour once, with no mechanism, and requires the run's sequence as data; each stage that can end a run declares its outcome, and R-RUN-5's list is their union with the operational outcomes. A-META-1's status becomes refined: the behaviour adopted, the mechanism left to task 3 |
| SA-3 · major | The integrity and manuscript checks sit outside the primitive, by a list of stages, and their repairs have no limit | Accepted: hook points declared as data by the kind of step (after code, after a manuscript, before export), in a stated order; each failure mapped onto the primitive's outcomes; each repair a bounded instance of the primitive; a hook's own repair does not re-trigger it (new R-INT-10). The compile check joins the manuscript hooks |
| SA-4 · major | Resume and the unit of work are too weak for a 2.5-day run | Accepted: R-STATE-7 adds harness jobs as units, an in-doubt state reconciled before any retry, resume from the recorded input snapshot, configuration and ledger, unit keys from each unit's place, and a kill at every unit boundary. The policy itself stays U-TOP-2's and U-CFG-2's (task 3) |
| SA-5 · major | A unit failing after its retries ends the task, whatever it was | Accepted: R-PRIM-10 maps a failure after retries onto the primitive's outcomes per role, as data: drop the item, reject the candidate, or end the run; a malformed judge output is a failed attempt, never accept |
| SA-6 · major | Rank 2 has a second home in committed Codex code: RJ, BA, VT | Accepted: `docs/requirements.md` names those files and maps their IDs to the requirements they refine. RJ-4's in-doubt state and BA-3's reservations are folded into R-STATE-7 and R-OPS-4, and BA-5's billing mode into R-MEAS-8. Adopting or superseding the files is left to whoever integrates the engine |
| SA-7 · major | Requirement texts decide rows that task 3 owns, which the checker cannot see | Accepted: each such requirement is cut to its testable minimum, and *What the requirements leave to other tasks* lists the register proposals the requirements presume, each pending in its task |
| SA-8 · major | Access per stage in one requirement, per role in another | Accepted: one access policy per agent role, as data, which a stage may only narrow (R-OPS-8) |
| SA-9 · major | The verified results table and the run's tail have no state requirement; R-INT-3 scores the test split after the export | Accepted: new R-STATE-10 for the table; R-INT-3 states the invariant only (EI-3); R-RUN-4's sequence ends with the tail (new R-RUN-7: the freeze, the test event, the final fill, the text revision, the gates, the export), whose content is task 6's IR-14 to IR-17 |
| SA-10 · major | Three of task 3's five routine changes are not required to touch one component or only data | Accepted: routing by stage and agent, with a fallback to the agent (R-AGT-2); a new task as a manifest and a read-only package, with a task-generic engine and harness (R-RUN-2); roster inputs as references to named run-state objects (R-AGT-1); backend settings only in the adapter (R-AGT-4) |
| SA-11 · major | Several tests pass on a broken engine | Accepted: every listed test replaced as proposed (R-PRIM-1, R-PRIM-8, R-PRIM-9, R-OPS-6, R-AGT-2, R-AGT-7, R-AGT-9, R-STG-12); R-RUN-1's untestable clause moves to measurement |
| SA-12 · major | The enforcement tests run against mocks of the enforcement | Accepted: two test tiers in *How to read*, logic tests and enforcement tests; the enforcement tests run the sandbox, permissions, hashing and the harness for real, on a toy CPU task |
| SA-13 · minor | One margin serves three gates | Accepted: R-RUN-6's rule names one entry per gate, each defaulting to the task's margin |
| SA-14 · minor | The limitation default runs 17 extraction rounds against App. A.2's 16 | Accepted: 16 extraction rounds, so 15 judged refinements. A.2 counts its rounds of extraction with the first included, and no table or figure places a round 0 outside the count, as Table 5 and Figure 9 do for the review and idea rounds. A-TOP-2's status becomes refined |
| SA-15 · minor | U-EVO-3 has two mechanisms, one unreachable | Accepted: the load check is dropped; the round's draw takes the seeds that are left, with a test |
| SA-16 · minor | "One directory" designs the store | Accepted: every artifact a record names resolves from the run's record by ID and hash (R-STATE-8) |
| SA-17 · minor | Five records hold the same facts about a unit of work | Accepted: one record per unit of work, from which the stage records, the ledger and the log derive (R-OPS-5) |

## From the evaluation-integrity-engineer review

| Finding | What it asks | Disposition, and where |
|---|---|---|
| EI-1 · blocker | The integrity tests prove the plumbing, never the guard | Accepted: two test tiers in *How to read*, logic and enforcement (with SA-12). Each enforcement test runs the real guard on the toy task beside a twin with the guard off, in which the planted attack succeeds: R-STATE-1, R-INT-1, R-INT-2, R-INT-3, R-INT-8, R-INT-9, R-OPS-8 (corrected in the third revision: this cell also listed R-INT-4, whose test is a logic test, the right tier for an LLM check whose rates IR-31 measures) |
| EI-2 · blocker | The test split is read-only, not unreachable | Covered by task 6: three data roles with hashed index files, built at packaging (IR-10); agent sessions read the fit role only, and predict steps run without network (IR-11). R-RUN-2, R-INT-2 and R-OPS-8 state the invariant and cite them |
| EI-3 · blocker | R-INT-3 and R-STATE-6 decide when the test split is scored, and P+ reports unlabelled validation numbers | Accepted: R-INT-3 states the invariant only; the timing is task 6's freeze and test event (IR-14), the labels its final fill (IR-16, IR-17); R-STATE-6 says nothing of timing |
| EI-4 · blocker | Nothing keeps agents and agent code away from results, verdicts and rules | Accepted, with task 6's IR-5, IR-11 and IR-30: R-INT-1's test plants EI-4's four attacks, each with its twin; R-STATE-8 gives the parts of a run separate write permissions; R-OPS-8 makes behaviour files read-only to every agent |
| EI-5 · major | The manuscript can launder an ablation's, a rebuttal's or another idea's number as the method's | Accepted in part: R-INT-8 requires each measurement in a manuscript to be inserted by engine code from a verified-table entry that carries its role (task 6's G3); the Enhancer's sandbox holds the manuscript, the table and read-only code, never the run directory; figures are rendered by engine code from entries (R-STG-10). The words around a bound number stay detection only, as task 6's section 6 records. The test plants EI-5's three drafts, with the value-only twin |
| EI-6 · major | The rebuttal picks its own datasets, caps and metrics | Accepted: R-STG-11: a rebuttal task declares its evaluation from settings the manifest registers, scored on the search role; every rebuttal row enters the verified table whatever its sign; the export record lists the rows the manuscript leaves out. The extra settings are task 5's (U-PEER-1) |
| EI-7 · major | Attribution rests on one LLM verdict over ablations the pipeline chooses, codes and can drop | Accepted: the idea's code declares its mechanism as switches when first implemented (R-STG-4); every ablation pass has a mechanism-off control that the harness runs from those switches; the ablation `Good` stands only if that control loses at least the rule's ablation margin (R-STG-9, IR-7's precondition for a clean breakdown); a discarded or failed ablation item is re-run once by a fresh session, then listed to the critic, and a missing control bars `Good`; R-INT-6's audit checks each switch and variant against its plan; R-STG-9 and R-MEAS-2 name U-SUB-2 |
| EI-8 · major | No control shows that the numeric guards stop noise | Accepted: R-RUN-6 refuses a margin below k times the baseline's measured run-to-run spread on the same role (k and the number of runs are task 6's, U-ART-12 and U-EVAL-4); the count of search scorings per idea is task 6's IR-13; new R-MEAS-10 runs a null idea end to end as configuration, and the report gives the measured false-pass rate beside every success rate |
| EI-9 · major | The comparison rule can be gamed through what it does not read | Accepted: R-RUN-6: a result missing a setting of the rule, or holding an invalid or non-finite value, passes no gate; the rule carries guardrail metrics with non-inferiority bounds, whose values are task 5's; the harness records every setting (IR-9), and, since the third revision, R-RUN-6 records every metric the entry points emit (corrected: this cell credited IR-9 with every metric, which it does not cover) |
| EI-10 · major | Compute scaling passes every guard | Accepted: compute is a guardrail of R-RUN-6, read from the compute the harness records with each result (IR-5); the manifest bounds it (R-RUN-2); R-STG-2's content rule stays a prompt, and is not counted as a guard |
| EI-11 · major | Judges read what the judged agent wrote, and no detection rate gates a run | Accepted in part: IR-7 lets an LLM only be stricter than the numbers, which bounds what a swayed critic can pass; R-AGT-9's golden sets hold each case beside a twin with text addressed to the judge, whose verdicts must agree, and each judge's recorded pass rate goes with the reported run. The gating threshold is task 7's (U-TOP-6); the integrity checks' rates are task 6's (IR-31) |
| EI-12 · major | The reported judge is kept apart from one reviewer, by an exact match, with nothing during development | Accepted: R-MEAS-5 compares the reporting judge with every in-loop judge of the manuscript by system, model family and prompt lineage, and flags the report when, on the subscription alone, no other family is available; every query to it is logged with its purpose, and one outside a final evaluation flags the report; in-loop judges' numbers are reported only as in-distribution (R-MEAS-6), which settles R-AGT-5 against R-MEAS-6 |
| EI-13 · major | The post-hoc audit is kept apart from the wrong agent | Covered by task 6 (IR-22 to IR-31). R-INT-7 cites them, and records which parts follow ScientistOne and which are ours. The proposal to hand-check a random sample of passes is left to task 6 (U-NOTE-4) |
| EI-14 · major | "Used once" has neither a refusal nor a ledger | Covered by task 6: three kinds of report job, every other refused and every one counted (IR-14); runs registered, an aggregate fixed in advance, and retries only before the freeze (IR-18). R-RUN-3 carries no report-role number into a chained run's G; R-OPS-4 fixes budgets before a task's first run |
| EI-15 · major | Development-time overfitting | Covered by task 6's IR-18: development and final-test tasks, and the engine frozen before a final-test task's first run. R-MEAS-9 keeps a task removed after the first run in the report, with its reason; R-OPS-2 hashes every behaviour file, and every reported number names the configuration's hash |
| EI-16 · major | The manifest and the evaluator are pinned by a hash checked after the fact, against itself | Accepted: R-RUN-2 pins the manifest before the task's first run, by a hash registered outside the run; a change makes a new version; every decision record names the manifest's and the rule's hashes (R-RUN-6); the hashes are checked at the start of every harness job (IR-6), not after the run (R-STATE-1, R-INT-2) |
| EI-17 · major | The baseline is agent-written, unfiltered, unaudited, and checked on an unnamed split | Covered by task 6: E_base is the pinned code's harness score (IR-4), checked once per task on the report role, sealed (IR-15). Task 2's part, U-BASE-2's branch: a baseline weaker than the reference by more than the tolerance ends the task, a stronger one passes and is recorded, and no agent repairs it; C_base runs the pinned code unchanged (R-STG-3) |
| EI-18 · major | Task 6's blocking rows are missing where requirements rest on them, and six decisions are marked final | Accepted: the *Depends on* fields are completed; A-FULL-1, U-BASE-1, U-BASE-2, U-INT-1, U-INT-3 and A-ABL-3 are marked provisional on task 6 in the decisions table; the checker fails a requirement whose text names the harness, a data role, a gain or the verified table and whose *Depends on* lists neither U-INT-4 nor U-TOP-5, with a self-test case |
| EI-19 · minor | Requirement texts adopt task 6's proposals, which the boundary check cannot see | Accepted: every row under *Depends on* is named in the Requirement text beside the clause that rests on it, and the checker enforces it; a clause that states a task 6 rule cites it by its IR- ID |
| EI-20 · minor | Seeds are the agent's to choose | Covered by task 6's IR-3: seeds from the manifest's list, and a flag on identical results across seeds. R-MEAS-7 cites it |
| EI-21 · minor | Verdicts are not bound to the code the harness ran, and a failure after a result can re-roll it | Accepted: R-INT-4 binds every filter verdict and result to its snapshot's hash, and a decision reads a result only when they match; R-STATE-7 reuses a unit's harness result on a retry |
| EI-22 · minor | The Selector's band is never tested against an out-of-band choice | Accepted: R-STG-8's test adds a third idea outside the band, which a Selector scripted to choose it cannot take, and the override is recorded |
| EI-23 · minor | The in-loop reference check is weaker than ScientistOne's I3 | Accepted: R-INT-5 resolves each entry and compares its title, authors, venue and year with the record it resolves to |
| EI-24 · minor | Nothing shows that a gain can be re-run, or traces a reported number to its file | Accepted: R-MEAS-2's gain code is committed before the first reported run, and a test re-runs it from the stored result records in a fresh environment with identical numbers; every reported number names its result record, its hash, the harness commit and the manifest's hash |

## The third revision: after the closure checks

Four more sources arrived after the second revision, c2ad177, all saved verbatim in this folder:
- `codex-review.md`, the Codex gate on c2ad177 (labels P1, P2);
- `system-analyst-closure.md` and `system-architect-closure.md` (labels NEW-n, and the earlier IDs);
- `evaluation-integrity-engineer-closure.md` and its second half, `-closure-2.md` (labels NEW-n,
  check 1 to check 3; its simulations are `playground/requirements/closure_sims.py`).

Task 6's second version, adc3484, landed during the round. It applies F-0 to F-46 and the
coordinating session's amendments A1 to A6 as rules IR-1 to IR-41, so the requirements now cite its
rules, never its fix list, and stay provisional on its next review. Every disposition below is
*accepted* unless it says otherwise.

### From the Codex review of c2ad177

| Finding | What it asks | Disposition, and where |
|---|---|---|
| P1 · R-STATE-3 | a `Reject` must undo a promotion, which R-STATE-3 forbade | R-STATE-3 gains a restore, to a state the core state has held, with an audit row naming both hashes, cause, inputs and rule hash |
| P1 · R-INT-10 | an alignment repair can type a number after the provenance check | every check of a hook runs again after any repair; all gates pass on the final version (R-INT-10, R-RUN-7) |
| P1 · R-INT-3 | its test forbade the sealed check | the test scans only what agents, prompts and manuscripts read, allows the sealed check, and plants a candidate's report job |
| P1 · R-MEAS-1 | an ablation reject has no test gain | reading two is *not measured*, counted as a failure; the readings follow the register's A-EVAL-1 |
| P2 · checker | truncated table rows crash the checker | row-width guards, with three self-test cases |
| P2 · checker | a padded range endpoint passes | range endpoints validated, with two self-test cases |
| P2 · R-STATE-1 | an edit restored between jobs cannot be seen | the second job runs while the file is changed |
| P2 · R-STG-12 | the reset test passes without a reset | pass one spends N_abl and N_peer first |
| P2 · R-INT-9 | one twin for two guards | a permission twin and a provenance twin |
| P2 · R-MEAS-10 | a zero margin cannot load | the floor-off twin is a guard-off build, never reportable (IR-38) |

### From the architect's closure

| Finding | Disposition, and where |
|---|---|
| NEW-1 · outcomes undefined, three role groups | R-PRIM-2 defines the primitive's outcome vocabulary; 03-stages.md gains a table of failures after retries for every role; the re-run count is a value of R-STG-13; a failed Selector keeps the band's leader |
| NEW-2 · `Reject` against R-STATE-3, the meta case | the restore of R-STATE-3; a `Reject` in a pass the meta stage started restores the previous pass, whose outputs go to the tail unapproved (R-STG-9, R-STG-12) |
| NEW-3 · two units of work, harness failures unclassed | a unit is a leaf, a stage a composite (R-STATE-7); agent-code failures are released results (IR-33.4), harness failures are retried under the same identity, then suspend (IR-33.3) (R-PRIM-10, R-OPS-7) |
| NEW-4 · budget stop against resume and one outcome | one suspended state for budget, wall-clock, usage window, billing and infrastructure; resumes and raises by a rule fixed before admission, as amendments; *abandoned*; outcomes final (R-RUN-5, R-RUN-8, R-OPS-4) |
| NEW-5 · task 6's review moves rank-1 rows | requirements cite the second version; BASE runs at admission with task scope (IR-4.2, IR-15); *baseline not reproduced* refuses admission; the gates are R-INT-10's *filters*, which a stage may add to, never remove from (IR-40) |
| NEW-6 · the engine's contract is a second home | the contracts table maps `claude/engine`, and *The engine as built* lists its departures, as the coordinating session read them |
| NEW-7 · closed lists | R-PRIM-2 and R-PRIM-4 are floors; an assessor of no kind; verdict maps onto declared outcomes; SEED keeps the accepted items |
| NEW-8 · missing rows, a mechanism in a test | the stage table gains CODER and the checker requires it; TAIL includes the export; R-RUN-4 lists the sequence with the meta stage; R-PRIM-8's test names no mechanism |
| NEW-9 · the hooks' counter, two homeless checks | one counter per hook invocation; the component-list and registered-settings checks join the code hook (R-INT-10) |
| NEW-10 · backend settings, budgets, second backend | adapters translate the role's access and the session's budget (R-AGT-4); budgets in named resources (R-OPS-4); R-AGT-4 departs from P-ROSTER-49 |
| NEW-11 · U-ART-15's presumed row | the presumed-proposals table says the requirement replaces the register's proposal |

### From the analyst's closure

| Finding | Disposition, and where |
|---|---|
| NEW-1 · attribution never established, exported unmarked | the export is marked *attribution not established*, and reading three reads the mark (R-STG-9, R-MEAS-1) |
| NEW-2 · last repair unchecked | as Codex's P1 on R-INT-10 |
| NEW-3 · five roles mapped | as the architect's NEW-1 and NEW-3 |
| NEW-4 · stop, resume and one outcome | as the architect's NEW-4 |
| NEW-5 · no budget unit on the subscription | R-OPS-4's named resources; dollars only for metered charges |
| NEW-6 · the threshold 8 guessed | 8 is the paper profile's, bound to ScholarPeer; the subscription profile needs a calibration record (A-EVAL-3); R-STG-11 departs from P-PEER-1, P-PEER-2, P-CFG-9, R-STG-13 from P-CFG-9; R-STG-13 refuses every value another task owns |
| NEW-7 · units in doubt unbounded | settled as spent within a bound, then run once more, the duplicate recorded (R-STATE-7) |
| NEW-8 · the baseline belongs to the task | as the architect's NEW-5 |
| NEW-9 · departures R-OPS-12 forces | R-AGT-6 departs from P-ROSTER-47, R-AGT-7 from P-ROSTER-45 where PaperOrchestra cannot run on the subscription. Declined for P-ROSTER-6: the Baseline Coding Agent still prepares C_base, as §3.2 has it |
| NEW-10 · presumed proposals unlisted | X- decisions name their rows under *Depends on*; the presumed table adds A-EVAL-1 and U-EVAL-1, and U-TOP-2's suspension |
| NEW-11 · a chained run's sealed check | the parent's report results become the child's sealed published numbers (R-RUN-3) |
| NEW-12 · `Reject` in pass two | as the architect's NEW-2 |
| NEW-13 · published numbers in the manuscript | table entries come from harness records or the manifest, labelled; each rendered row from its own entries (R-STATE-10, R-INT-8) |
| NEW-14 · tests that cannot settle | stated bounds in R-MEAS-10 and R-INT-3; R-OPS-12 gains a no-cost enforcement case with the real CLI adapter |
| NEW-15 · bookkeeping | line 64 corrected above; all 17 questions listed; CHK-6 and CHK-9 disposed above |
| NEW-16 · checker defects | HTML comments stripped; U- and A- IDs matched loosely and reported, with self-test cases |
| NEW-17 · task 6's review moves rules | as the architect's NEW-5 |
| MISS-1 · a test number against a claim | the export lists rows whose search and report gains differ in sign, and marks *not confirmed on test* when the method's own row is one (R-RUN-7) |
| MISS-5, MISS-6 · trail and audit row | R-STATE-9's trail and R-STATE-3's audit row as asked |
| MISS-18 · addresses in the task package | verbatim task-package content is allowed by the package's hash (R-OPS-10) |
| MISS-20 · duplicates and attempts | a duplicate rule with M = 3 × N_seed attempts for the pool and 3 per round for A_Evolve, ours (R-STG-2, R-STG-7, R-STG-13) |
| MISS-21 · manifest fields | seed lists per role, the determinism declaration, registered rebuttal settings and the packaging diff (R-RUN-2) |
| MISS-22 · wall-clock outcome | a wall-clock bound suspends, and suspended time counts toward no bound (R-RUN-8, R-OPS-7) |
| MISS-24 · unknown novelty | sorts last (R-AGT-6, SEED) |
| MISS-26 · acceptance cases | every roster entry has some; the Meta-Reviewer gains App. D's do-no-harm case (R-AGT-9) |
| CONT-11 · the supersede sentence | added to *How to read* |
| ORPH-4 · the component list's source | the declared switches; the full-set engineer gets a refusal case (R-STG-4, R-STG-5) |
| U-BASE-2 flag · the tolerance's owner | task 5's, with IR-15.3's formula (R-STG-3, R-STG-13) |
| Part 5 · two traces | P-ROSTER-32 traced by R-RUN-2, P-ROSTER-33 by R-STG-9 |

### From the integrity closure

| Finding | Disposition, and where |
|---|---|
| NEW-1 · blocker · seed luck survives the tail | task 6's IR-14.4 fits every frozen row again at the report seeds; R-RUN-7 cites it, and its enforcement test plants seed-dependent training noise with the expected values stated |
| NEW-2 · the precondition decides nothing exported | the export mark *attribution not established*, read by R-MEAS-1. ⛔ The alternative, an unmet precondition at the limit as `Reject`, declined: it would end tasks that Figure 7 sends to drafting |
| NEW-3 · the precondition re-reads E_best | paired fresh fits of C_best and the control in one job (R-STG-9) |
| NEW-4 · the author scopes the switch | a scope check at the code hook, before any veto, against the description recorded before scoring; a floor against E_base; a text edit never repairs a switch finding (R-STG-4, R-STG-9, R-INT-6); the planted corpus is task 6's (IR-31); corrected in the fourth revision: IR-31.1 does not list this check, so task 6 is asked to extend it |
| NEW-5 · prose binds any cell after the test event | numbers in the text bind only to *ours* or a reference row; other rows only in rendered tables (R-INT-8) |
| NEW-6 · the floor measures nothing | spread across search seeds at admission; margins derived from α per gate, given its scorings; α's default 0.05, ours under IR-7.1 (R-RUN-6) |
| NEW-7 · the null is empty | the null redraws its randomness, runs through the loop, and states its rate beforehand (R-MEAS-10) |
| NEW-8 · failing on purpose | agent-code failures are released and never retried (IR-33.4); completeness names seeds; compute of every attempt (R-OPS-7, R-RUN-6) |
| NEW-9 · the reporting judge on the authors' family | R-OPS-12 states its scope; the judge and auditor need another family on a subscription (IR-29.4); R-MEAS-5 compares with the authors, hides its prompt, and reports a transfer control |
| NEW-10 · one twin per test | a twin or a positive control per clause, in *How to read* and in R-INT-1, R-INT-2, R-INT-3, R-INT-8, R-OPS-8, R-RUN-2 |
| NEW-11 · C_base's refusal, repackaging | a strengthened-copy control; at most k attempts, the roles fixed across versions (R-STG-3) |
| NEW-12 · people choose which runs finish | raises and resumes by a rule fixed before admission (R-RUN-8); chain links registered before the first test event (R-RUN-3); IR-18.4 |
| NEW-13 · a test event with no export | *test event done, not exported* (R-RUN-5); such a run counts at no more than its gain (R-MEAS-3) |
| NEW-14 · three reads against CLAUDE.md | task 6 decided it in place (its amendments A1 and A6, section 7); R-INT-3 records that reading and the flag to the coordinating session |
| NEW-15 · bookkeeping | the checker requires a task-6 row beside an IR- citation and a tier on every test, with self-test cases; R-MEAS-5, R-MEAS-9 and R-OPS-2 gain their rows; R-INT-5 and R-INT-6 point to IR-31's rates; R-INT-7 names the re-fits and ledger checks as ours; R-MEAS-1 and R-MEAS-2 defer to task 6's rows; the two fix-list cells corrected above |
| check 1 · four contradictions | R-INT-10 and R-INT-3 as above; R-INT-3's first sentence rewritten; R-STATE-7's test counts identities (IR-33) |
| EI-2 remainder | R-INT-2 names the two paths that stay detection only |
| EI-9 remainder | every metric recorded; each entry states its reference (R-RUN-6) |
| EI-10 remainder | the harness stops a job at the envelope, with a test (R-RUN-2) |
| EI-20 remainder | the seed floor replaces the single-run mark (R-MEAS-7) |

### From task 6's second version, and the coordinating session

| Source | Disposition, and where |
|---|---|
| IR-4.3, IR-14.3 · C_base as a row unless its hash equals E_base's | R-STG-3: C_base is the pinned code, and the equality is its setup check |
| IR-14.4 · E_base is not fitted at the test event | R-RUN-7: E_base's report results come from admission (IR-15.1) |
| IR-15.5 and section 10 · k, the seed floor and the attempt bound are task 5's | R-STG-3, R-STG-13 |
| IR-7.1, IR-21.1 · values left to task 2 | decided in R-RUN-6, R-STG-4, R-STG-9, R-INT-4 and R-INT-10, listed at the end of `docs/requirements.md` |
| IR-34 · resume from the last finished stage | R-STATE-7's finer grain meets it, as Q-5 decided |
| the coordinating session · task 3 starts from engine.md, departures recorded | *The engine as built*; R-PRIM-6's agent becomes optional by profile, which brings it into line |
| the coordinating session · F-46 decided without asking Vlad | relayed to task 6, which decided it in place (A1, A6); R-INT-3 records it |

## The fourth revision: after the narrow closure checks

The narrow closure checks of fd9bcf9 and the second Codex review, all saved verbatim in this folder:
`codex-review-2.md`, `system-analyst-closure-2.md`, `system-architect-closure-2.md` and
`evaluation-integrity-engineer-closure-3.md`. Every disposition is *accepted* unless it says
otherwise.

| Finding | Source | Disposition, and where |
|---|---|---|
| the ablation's fresh fits are E_best's released records | Codex P1; integrity ND-1, NEW-3 | the in-loop precondition is a filter, its bias stated; attribution is measured at the test event from *ours* and its frozen control, paired per report seed, under a pre-registered test (R-STG-9, R-MEAS-1). ⛔ A third seed list declined: it changes IR-9.3 and IR-10.2, and the test event already gives undecided draws |
| the sealed check once per manifest version | Codex P1; integrity §3 | once per baseline key (IR-15.2); roles fixed after the first attempt; an unchanged-key test case (R-STG-3) |
| a time metric needs E_base timed again | Codex P1 | E_base is timed in the test event's job for a time metric (R-RUN-7, IR-8.1, IR-14.4) |
| a post-test failure still counted a success | Codex P1 | the tail's end state, a lost artifact, abandonment and suspension fail every reading, with a fixture (R-MEAS-1) |
| the writable-mount twin cannot succeed | Codex P1 | the twin asserts the write while the hash check still refuses; a second twin turns both off (R-INT-2) |
| critics missing from the failure table | Codex P2; architect NEW-1; analyst NEW-3 | rows for both critics, the Result Comparison Agent and the initial idea; every cell names a vocabulary term; a role with no row fails to load (03-stages.md, R-PRIM-10) |
| row width checked only up to the needed columns | Codex P2 | every row must match its header's width, with a self-test case |
| one-digit task numbers in attribution | Codex P2 | any task number, with a self-test case |
| suspension listed as a stage outcome; no outcome for an undone promotion | architect N3-1 | suspension interrupts a stage; *promotion undone* travels up to the promoting stage, which restores and takes its failure branch (R-PRIM-2, R-STG-9, R-STG-12, R-STATE-3) |
| bounds classed three ways; two suspensions with no lift | architect N3-2; analyst C-1 | R-RUN-8's table of bounds by level, each with what it does and what lifts it; a job's limits release a failure; a harness fault past its attempts is lifted by an amendment, which task 6 is asked to confirm |
| an item's re-run spends its parent's refinement | architect N3-3 | the item has its own counter, limit one re-run, as IR-40.1's one counter per candidate (R-INT-4) |
| two definitions of a unit | architect NEW-3 | R-OPS-5 gives units and composites one record each |
| keys from a place in the run | architect NEW-5 | keys by scope: task, run or audit; a harness job keyed by IR-32.1's identity (R-STATE-7) |
| the engine read at cba39df, one departure | architect NEW-6 | re-read at c1850a5: six more departures listed, and the index no longer says one |
| outages of outside systems become research outcomes | analyst C-2 | an outside system unreachable past its retries suspends the run, with tests (R-PRIM-10, R-RUN-8) |
| a suspended run has no exit | analyst C-3; integrity's minor | abandonment under the rule, flagged outside it; a run suspended at report time counts as a failure, flagged (R-RUN-8, R-MEAS-3) |
| a lost frozen artifact has no outcome; admission failures | analyst C-4 | an eleventh outcome, *frozen artifact lost*; *not admitted* covers both admission failures (R-RUN-5) |
| no budget unit tested; refusal list incomplete | analyst NEW-5, NEW-6 | a machine-hours case (R-OPS-4); R-STG-13 refuses without budgets, wall-clock bounds, guardrail bounds and the reconciliation bound |
| a blind retry passes R-STATE-7's test | analyst NEW-7 | a recoverable unit is reconciled with no further call, with a case; the bound is task 3's (R-STATE-7) |
| the duplicate rule's owner | analyst MISS-20 | presumed as task 3's, in the presumed-proposals table |
| the switch-scope check's error rate | integrity NEW-4 | measured as IR-31 measures task 6's checks, which task 6 is asked to extend; the bundled description stated as detection only (R-STG-4) |
| the scan reports a zero with no positive control | integrity NEW-10 | a planted report value in a copy of the run is found (R-INT-3) |
| α collides with task 6's | integrity §3 | renamed α_gate (R-RUN-6, R-STG-13) |
| the margin from a point estimate of σ | integrity NEW-6 | an upper 95% bound on the spread (R-RUN-6) |
| the determinism exemption cited to IR-9.3 | integrity §3 | marked as ours (R-RUN-2, R-MEAS-7) |
| R-MEAS-3 cited IR-39.3 for its cap | integrity §3 | cited as a presumption on U-EVAL-1 |
| the envelope's "no result" | integrity §3 | released as failed (R-RUN-2) |
| the judge's prompt hidden from development | integrity NEW-9 | a process rule, as IR-29.5 (R-MEAS-5) |
| "about half" assumes equal noises | integrity NEW-1 | stated (R-RUN-7) |
| the end-to-end null rate has no test of its own | integrity NEW-7 | declined for now: R-STG-9's and R-RUN-7's nulls cover two gates, and task 6's null control (its U-TOP-5 file) covers the loop |
| clauses are not counted against twins by the checker | integrity NEW-10 | declined: a clause count would read wording, not guards; the narrow reviews read them |
