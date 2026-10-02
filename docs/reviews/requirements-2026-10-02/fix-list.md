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
| A-TOP-2 flag, CONT-10, Q-12 | 16 verifier calls or 16 judged expansions | Kept: 16 judged refinements, counted like Table 5's and Figure 9's rounds; the reason is now in R-STG-1 |
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
| Part 6 | The checker's defects | Already caught: CHK-2 to CHK-5, 7, 8, 10 to 14, 18 to 20 and 22. Added: placeholders in a field (CHK-1), split pairs (CHK-15), the stage table (CHK-16), malformed IDs (CHK-17), a file with no requirement (CHK-21), and printing the pending rows and departures. The self-test moved to its own module, to keep both files under 600 lines |

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
| EI-1 · blocker | The integrity tests prove the plumbing, never the guard | Accepted: two test tiers in *How to read*, logic and enforcement (with SA-12). Each enforcement test runs the real guard on the toy task beside a twin with the guard off, in which the planted attack succeeds: R-STATE-1, R-INT-1, R-INT-2, R-INT-3, R-INT-4, R-INT-8, R-INT-9, R-OPS-8 |
| EI-2 · blocker | The test split is read-only, not unreachable | Covered by task 6: three data roles with hashed index files, built at packaging (IR-10); agent sessions read the fit role only, and predict steps run without network (IR-11). R-RUN-2, R-INT-2 and R-OPS-8 state the invariant and cite them |
| EI-3 · blocker | R-INT-3 and R-STATE-6 decide when the test split is scored, and P+ reports unlabelled validation numbers | Accepted: R-INT-3 states the invariant only; the timing is task 6's freeze and test event (IR-14), the labels its final fill (IR-16, IR-17); R-STATE-6 says nothing of timing |
| EI-4 · blocker | Nothing keeps agents and agent code away from results, verdicts and rules | Accepted, with task 6's IR-5, IR-11 and IR-30: R-INT-1's test plants EI-4's four attacks, each with its twin; R-STATE-8 gives the parts of a run separate write permissions; R-OPS-8 makes behaviour files read-only to every agent |
| EI-5 · major | The manuscript can launder an ablation's, a rebuttal's or another idea's number as the method's | Accepted in part: R-INT-8 requires each measurement in a manuscript to be inserted by engine code from a verified-table entry that carries its role (task 6's G3); the Enhancer's sandbox holds the manuscript, the table and read-only code, never the run directory; figures are rendered by engine code from entries (R-STG-10). The words around a bound number stay detection only, as task 6's section 6 records. The test plants EI-5's three drafts, with the value-only twin |
| EI-6 · major | The rebuttal picks its own datasets, caps and metrics | Accepted: R-STG-11: a rebuttal task declares its evaluation from settings the manifest registers, scored on the search role; every rebuttal row enters the verified table whatever its sign; the export record lists the rows the manuscript leaves out. The extra settings are task 5's (U-PEER-1) |
| EI-7 · major | Attribution rests on one LLM verdict over ablations the pipeline chooses, codes and can drop | Accepted: the idea's code declares its mechanism as switches when first implemented (R-STG-4); every ablation pass has a mechanism-off control that the harness runs from those switches; the ablation `Good` stands only if that control loses at least the rule's ablation margin (R-STG-9, IR-7's precondition for a clean breakdown); a discarded or failed ablation item is re-run once by a fresh session, then listed to the critic, and a missing control bars `Good`; R-INT-6's audit checks each switch and variant against its plan; R-STG-9 and R-MEAS-2 name U-SUB-2 |
| EI-8 · major | No control shows that the numeric guards stop noise | Accepted: R-RUN-6 refuses a margin below k times the baseline's measured run-to-run spread on the same role (k and the number of runs are task 6's, U-ART-12 and U-EVAL-4); the count of search scorings per idea is task 6's IR-13; new R-MEAS-10 runs a null idea end to end as configuration, and the report gives the measured false-pass rate beside every success rate |
| EI-9 · major | The comparison rule can be gamed through what it does not read | Accepted: R-RUN-6: a result missing a setting of the rule, or holding an invalid or non-finite value, passes no gate; the rule carries guardrail metrics with non-inferiority bounds, whose values are task 5's; the harness records every setting and metric (IR-9) |
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
