# Closure check: system-architect, the requirements revision of TODO task 2 (2026-10-02)

- **Checked:** `docs/requirements.md` and `docs/requirements/01-run.md` to `08-operation.md` on `claude/requirements` at `c2ad177`. I checked them against my review of `ff1faaa` (`docs/reviews/requirements-2026-10-02/system-architect.md`, SA-1 to SA-17) and against the dispositions in `fix-list.md` beside it.
- **Lens:** what the next change costs, and whether task 3 can start rank 1, the primitive's parameters.
- **Mode:** read-only.
  - I created, edited and deleted no file. I ran no git command that changes state, and I read other branches with `GIT_OPTIONAL_LOCKS=0 git show`.
  - While I worked, another session added an untracked file, `docs/reviews/requirements-2026-10-02/codex-review.md`, at 14:59. I read it, and cite it where it found the same defect. Two of its P1 findings are outside this lens: R-INT-3's test against the sealed baseline check, and R-MEAS-1's fixture for an ablation reject.
- **Voices:**
  - *Paper* is arXiv:2609.19644v1, quoted from `docs/paper/source/`.
  - *Requirements* are the files at `c2ad177`, cited as `file:line` and quoted verbatim.
  - *Elsewhere* is another branch, cited as `branch:path:line` and read on 2026-10-02.
  - *Proposal* is mine, and is never a decision.
- **Paths** are relative to the repository root.
- **The checker** ran on 2026-10-02 at 14:53 (+04), with `-B`, so it wrote no bytecode.
  - `python3 playground/paper/requirement_coverage.py` exits 0. Its last line is `0 problem(s)`. The two lines before it read `requirements: 82 (RUN 8, PRIM 10, STG 13, AGT 9, STATE 10, INT 10, MEAS 10, OPS 12); leave-out decisions: 5` and `task-2 register rows: 33; decided by a requirement: 33; in the decisions table: 15 confirmed, 18 refined`.
  - `--selftest` exits 0, with 40 cases, all `ok`. Its last line is `ok   --write fills the column: before ['column'], after no problem, identical to the clean file: True`. Each defect is planted beside a clean twin, so the zero above can fail.
  - The Codex gate found two checker defects that the self-test does not plant: a truncated table row raises `IndexError`, and a zero-padded range endpoint passes. Both are outside this lens.
  - `git status --porcelain` was empty before and after both runs.

## Summary

- **Both blockers are resolved in substance.**
  - R-PRIM-2 is now a floor of behaviours.
  - Every row of the stage table, the TAIL row included, can be expressed under that floor, with one exception: the ablation's undo of a promotion (NEW-2).
  - The run's sequence is data, and each stage that can end the run declares its outcome.
  - The meta restart is one behaviour, stated twice in the same terms.
- **SA-1 to SA-17:** 13 are closed and 4 are partly closed (SA-1, SA-2, SA-4 and SA-11). None is open, and none regressed.
- **New findings: six majors and five minors.**
  - Two majors are contradictions between requirements whose tests cannot both pass:
    - the ablation's undo against R-STATE-3 (NEW-2), which the Codex gate also found;
    - resuming after a budget stop against R-STATE-7 (NEW-4).
  - Two majors are definitions that rank 1 or rank 2 would otherwise settle silently in code:
    - the primitive's vocabulary of outcomes, with a failure value for only three groups of roles (NEW-1);
    - what a "unit of work" is (NEW-3).
  - Two majors are documents on other branches that have moved under the requirements:
    - task 6's reviewed fix list, which moves the BASE row and the gates (NEW-5);
    - the engine branch's contract, which already builds the primitive that SA-1 rejected (NEW-6).
- **Verdict:**
  - Task 3 can start rank 1 now.
  - NEW-1 and NEW-2 must be fixed before rank 1 closes, and NEW-3 and NEW-4 before rank 2.
  - NEW-5 and NEW-6 are decisions for the coordinating session. They should be taken while rank 1 is drafted, not after it.

## 1. SA-1 to SA-17: status

| SA | Status | Evidence | What remains |
|---|---|---|---|
| SA-1 · blocker | partly closed; no longer a blocker | R-PRIM-2 is a floor: "A stage configuration can express at least the behaviours below. This is a floor" (`02-primitive.md:23`). One assessor list now holds "a choice among options" and "a nested stage, A_Coder" (`:27`). The floor adds the precondition (`:28`), aggregation (`:29`), append (`:30`), counter scope (`:32`), stop tests (`:33`), hooks (`:35`) and declared outcomes (`:36`). The out-of-domain cells are rewritten (`03-stages.md:23-34`). Rank 1 is named in full (`requirements.md:192`) | Three lists are closed again, and four cells sit outside them (NEW-7). No list can express ABL's undo (NEW-2). The floor lacks the failure value per role, which R-PRIM-10 makes data (NEW-1) |
| SA-2 · blocker | partly closed; the blocker is resolved | "The run's sequence of stages is data." (`01-run.md:43`). The test inserts a toy stage, and ends a run with a toy stage's own outcome (`:55`). The restart is stated once as behaviour, with "How this is built is task 3's (A-NOTE-1)" (`:50`), and R-STG-12 repeats it in the same terms (`03-stages.md:178`). The outcomes are a union of declarations (`01-run.md:59`) | R-PRIM-8's test still picks the nested mechanism (`02-primitive.md:99`). R-RUN-4's step 4 nests the opposite way to the META row (`01-run.md:47` against `03-stages.md:33`). See NEW-8 |
| SA-3 · major | closed | Hook points are "declared in data by the kind of step, not by stage, in a stated order" (`06-integrity.md:107`). Each failure is mapped and each repair bounded (`:111`). "with no list to edit" (`:47`). Compile is a manuscript hook (`03-stages.md:154`) | The repair counter's scope, the re-check rule after a later repair, and two output checks with no hook (NEW-9) |
| SA-4 · major | partly closed | Harness jobs are units, and keys come from each unit's place. Units in doubt are reconciled. Resume starts from the recorded input snapshot, configuration and ledger (`05-state.md:60-64`). The test kills the run at every unit boundary (`:70`). "Afford" is defined (`08-operation.md:36`) | R-OPS-4's resume "once the budget is raised" contradicts R-STATE-7's recorded configuration (NEW-4). "Unit of work" now has two definitions (NEW-3) |
| SA-5 · major | closed | A failure after retries maps "onto the primitive's own outcomes, per role, as data", and unparsable output "never maps to accept or `Good`" (`02-primitive.md:118-123`), with tests (`:128-130`). R-OPS-7 defers to it (`08-operation.md:60`) | Done as I proposed. But my proposal named three groups of roles, and 15 roles and the tail's four steps still have no value (NEW-1) |
| SA-6 · major | closed for the Codex contracts | RJ, BA, VT and the runtime integration are mapped to the requirements they refine. RJ-1, RJ-4, BA-3 and BA-5 are folded in (`requirements.md:120-133`) | The engine branch's `docs/architecture/engine.md`, a larger second home that landed after my review, is missing from that table (NEW-6). BA's "session" is not R-OPS-4's (NEW-10) |
| SA-7 · major | closed | The presumed rows are listed, each open in its task (`requirements.md:178-190`). R-STG-6 is cut to "at least its verdict and its feedback" (`03-stages.md:98`). R-OPS-9's cuts are left to task 3 (`08-operation.md:76`) | U-ART-15's row is not the register's proposal (NEW-11) |
| SA-8 · major | closed | "Each agent role has one access policy, as data ... A stage may only narrow it" (`08-operation.md:68`). Within one subset stage the coder writes and the filter is refused, beside a twin with one policy per stage (`:72`). The roster entry names its access role (`04-agents.md:10`) | R-AGT-4 keeps "permissions" in the adapter's configuration. It should say that the adapter translates the role's policy (NEW-10) |
| SA-9 · major | closed | R-STATE-10 (`05-state.md:88-94`). Each manuscript version names its code and table versions (`:45`). R-INT-3 states the invariant only (`06-integrity.md:39`). The tail is R-RUN-7 (`01-run.md:91-104`) and a row of the table (`03-stages.md:34`) | The TAIL row omits the export that R-RUN-7 places in the tail (NEW-8) |
| SA-10 · major | closed | Routing by stage and agent, tested (`04-agents.md:18`, `:27`). "a new task is a manifest and a package, never code", tested (`01-run.md:26`, `:31`). Inputs as references, tested (`04-agents.md:10`, `:14`). Backend settings only in the adapter, with a static check (`:39`, `:43`) | See section 2.4 |
| SA-11 · major | partly closed | The listed tests are replaced (`02-primitive.md:16-19`, `:99-100`, `:114`; `08-operation.md:56`; `04-agents.md:27`, `:68`, `:90`; `01-run.md:9`) | The R-STG-12 case I proposed passes on an engine that never resets its counters. Nothing spends N_abl in the first pass, so the second pass may refine anyway (`03-stages.md:187`; found by the Codex gate, P2). **Fix:** in pass one, script `Refine`, guard accepts, `Refine`, which spends N_abl; then a `Refine` in pass two must bring one more A_FullEng call. Do the same for N_peer, with three reviews below 8 in pass one |
| SA-12 · major | closed | Two test tiers, each enforcement test beside a twin with its guard off (`requirements.md:28-30`). The five tests I named now run in the enforcement tier (`05-state.md:14`; `06-integrity.md:21-27`, `:35`, `:103`; `08-operation.md:72`) | Nothing in this lens |
| SA-13 · minor | closed | "one entry per gate, each with its own margin and defaulting to the task's" (`01-run.md:81`), tested (`:89`) | Nothing |
| SA-14 · minor | closed | 15 judged refinements, so 16 rounds (`02-primitive.md:47`; `03-stages.md:23`, `:40`). The test expects "16 Extractor calls and 16 Verifier calls" (`:45`) | Nothing |
| SA-15 · minor | closed | The load check is dropped, and the run-alone branch has its test (`03-stages.md:108`, `:111`; `requirements.md:96`) | Nothing |
| SA-16 · minor | closed | Every artifact "resolves from the run's record by ID and hash; where it is stored is task 3's" (`05-state.md:74`) | Nothing. This fix now pays off: task 6's task-scoped baseline records (NEW-5) can be referenced from a run's record |
| SA-17 · minor | closed | There is one record per unit, from which "The stage records, the ledger, the log and every query derive" (`08-operation.md:44`). R-PRIM-9 and R-MEAS-8 write into it (`02-primitive.md:104`; `07-measurement.md:73`) | Its subject, the "unit of work", is defined two ways (NEW-3) |

## 2. The five questions

### 2.1 Can task 3 start rank 1 from R-PRIM-1 to R-PRIM-10, the stage table and R-RUN-4?

**Yes.**
- One contradiction is left in these inputs (NEW-2).
- Two gaps would otherwise be closed silently by the parameter cut (NEW-1, NEW-7).

The table below repeats SA-1's test, row by row, against R-PRIM-2's floor (`02-primitive.md:23-36`).

| Row | Holds under R-PRIM-2? | What is left |
|---|---|---|
| LIM | Yes: one agent generates, the Extractor refines, the assessor is an LLM verdict, and at the limit it keeps the last set, flagged | Its failure value lies outside R-PRIM-10's three groups: an empty set ends the run (R-STG-1's test, `03-stages.md:45`). See NEW-1 |
| SEED | Yes: append, a score with no verdict, and a count stop | Its at-limit cell, "keep the whole pool, sorted by score, descending" (`03-stages.md:24`), is none of R-PRIM-4's five values. R-PRIM-4 closes that list with "The at-limit value is one of these" (NEW-7) |
| BASE | Yes: a sequence of a harness job and an agent, a deterministic check, and a declared outcome | "fail → stop the run, *baseline not reproduced*" (`03-stages.md:25`) lies outside "a verdict map onto accept, refine and reject" (`02-primitive.md:29`) (NEW-7). Task 6's accepted F-6 moves the row out of the run (NEW-5) |
| SUB, FULL | Yes: an LLM verdict behind a precondition, and "a `Good` the precondition blocks → `Engineer`" | The engineer's component-list refusal (`03-stages.md:77`) is a check that neither the floor nor R-INT-10 names (NEW-9) |
| A_Coder | Yes: a sequence in which the full set runs only after a subset `Good`, aggregated into one trace (R-STG-6, `03-stages.md:98`) | It has no row, although R-PRIM-1's test loads it from data (NEW-8) |
| EVO | Yes: deterministic draws plus A_Evolve; A_Coder nested in a fan-out; a count of `Good`; append; K and S tested at the end of each round; keep the accepted items, or end with *no Good idea* | Nothing |
| SEL | Yes: "a choice among options" behind a precondition that "narrows the options a choice may pick" (`02-primitive.md:28`) | Its failure ends a run whose band entry already names a leader (NEW-1) |
| ABL | Partly. The plan-then-execute sequence, the fan-out, the precondition, the guard and the restart all hold | "`Reject` → stop the run, *ablation reject*, or undo a promotion of this pass" (`03-stages.md:30`) is an effect that depends on run state. No list holds the undo, and R-STATE-3 forbids it. A `Reject` of the meta stage's candidate falls in neither branch (NEW-2) |
| DRAFT | Yes, except its assessor | "none; the manuscript hooks run after it" (`03-stages.md:31`) is not in the list that R-PRIM-7 closes (NEW-7) |
| PEER | Yes: a score against a threshold, a sequence with a fan-out as the refiner, and keep the last | A rebuttal task "that names any other data is refused" (`03-stages.md:164`), but no effect of that refusal is stated, and the check has no home (NEW-9) |
| META | Yes: the downstream pass is the generator, the judged object differs from the refined one, there is a guard, counters are fresh by per-invocation scope, and it keeps the last outputs, marked unapproved | The row and R-PRIM-8's test pick the nested mechanism, which R-RUN-4 leaves to task 3 (NEW-8) |
| TAIL | Yes: a sequence of deterministic steps and one agent, no assessor, and hooks after it | Its assessor is "none" (NEW-7). The export, R-RUN-7's step 4, is missing from the row (NEW-8). Its steps have no failure values (NEW-1) |
| The run's sequence | Yes (`01-run.md:43`, tested at `:55`) | It has no row (NEW-8) |
| Hook points | Yes (`06-integrity.md:107-111`) | See NEW-9 |
| Failure after retries | Partly | See NEW-1 |
| Counter scope (U-META-1) | Yes: "its scope, per invocation by default" (`02-primitive.md:32`) | R-STG-12's test does not yet show it (SA-11) |

### 2.2 Is the meta restart stated once, as behaviour, with no mechanism? Is the run's sequence data?

- **The behaviour holds, in one form.**
  - R-RUN-4: "When the meta-review's guard accepts a refinement, a new downstream pass starts at ablation planning, the ablation critic included, with fresh budgets, and the Meta-Reviewer is asked again at its end; nothing before ablation planning runs again" (`01-run.md:50`).
  - R-STG-12 says the same (`03-stages.md:178`). So does A-META-1's decision: "the behaviour is required, and its mechanism is task 3's" (`requirements.md:78`).
  - It is written twice, but never differently.
  - It matches the paper, whose engine "re-executes downstream ablation planning, ablation execution, manuscript re-drafting, and simulated peer-review cycles" (`sections/3_new_method.tex:149`).
- **Two places leave the mechanism to task 3, and a third picks it.**
  - Left to task 3: "How this is built is task 3's (A-NOTE-1)" (`01-run.md:50`), and "task 3 may build the same behaviour another way (A-NOTE-1)" (`03-stages.md:13-14`).
  - Picked: R-PRIM-8's test requires "the downstream pass nested in the meta stage, both from data" (`02-primitive.md:99`).
  - The texts also nest in opposite directions:
    - R-RUN-4's step 4 reads "a downstream pass: ablation, drafting, peer review, then meta-review" (`01-run.md:47`), which puts META inside the pass;
    - the META row's generator is "the downstream pass, ablation to peer review" (`03-stages.md:33`), which puts the pass inside META.
  - NEW-8 fixes both, in two lines.
- **The sequence is data.**
  - "The run's sequence of stages is data." (`01-run.md:43`).
  - Its test inserts a toy stage between SEL and the downstream pass by data alone, and ends a run with a toy stage's own outcome (`:55`).
  - Each stage that can end the run declares its outcome (`:50`; `02-primitive.md:36`). R-RUN-5's list is "the union of the outcomes the stages declare and the operational ones" (`01-run.md:59`).
  - So a new stage is an insertion. Its new outcome changes R-RUN-5's text and its test's count of nine (`:75`), and never code.

### 2.3 Do the hooks, the failure mapping, resume, the budget, access and the one record hold together?

Five pairs hold. Four specify one thing in two ways, and two are ambiguous.

| Requirements | What they share | Do they hold together? |
|---|---|---|
| R-STATE-7, R-OPS-4 | units in doubt | Yes. A unit starts only if the budget, "net of the reservations of units in flight and units in doubt", covers it (`08-operation.md:36`), tested at `:40`. R-STATE-7 reconciles such units (`05-state.md:62`) |
| R-STATE-7, R-OPS-7 | a retry after a timeout | Yes: "a unit in doubt is reconciled before any retry (R-STATE-7)" (`08-operation.md:60`) |
| R-OPS-5, R-PRIM-9, R-MEAS-8 | the record of a unit | Yes. R-PRIM-9 records "in the one record per unit of work (R-OPS-5)" (`02-primitive.md:104`), and the ledger is "derived from the one record per unit of work" (`07-measurement.md:73`) |
| R-OPS-8, R-INT-9, R-OPS-5 | access | Yes. The judges' read-only rule constrains the role policies, and "the policy in force is in each unit's record" (`08-operation.md:68`) |
| R-INT-10, R-INT-4, R-RUN-7 | where the checks run | Yes: one mechanism, by the kind of step, with the tail's revision included (`06-integrity.md:47`, `:109`; `01-run.md:96`) |
| R-PRIM-4, R-PRIM-5, R-PRIM-10, R-INT-4, R-INT-10, R-AGT-6 | what a failed or exhausted step does | **No.** "The primitive's own outcomes" is cited three times and defined nowhere, and the five lists differ (NEW-1) |
| R-OPS-5 against R-STATE-7, R-OPS-4, R-OPS-7 | what a unit of work is | **No.** A stage and a run are units in one, and only leaves are units in the others (NEW-3) |
| R-OPS-4 against R-STATE-7, with R-OPS-2, R-RUN-5 and R-RUN-8 | resuming after a budget stop | **No.** The raised budget is a file that resume must ignore (NEW-4) |
| R-PRIM-10 and R-INT-4 against R-OPS-7 | how often an item is re-run | **No.** Two requirements fix "one re-run by a fresh session", R-OPS-7 gives the retry values to task 3, and R-STG-13's list of values holds neither (NEW-1) |
| R-OPS-8 and R-OPS-4 against R-AGT-4 | a session's access and limits | Ambiguous. The adapter holds "its tools, permissions and turn limits" (`04-agents.md:39`) (NEW-10) |
| R-OPS-7 against R-INT-1 | a harness job whose agent code fails | Ambiguous. R-OPS-7 retries every unit, while R-INT-1 says "A code version with no runnable entry point yields no result" (`06-integrity.md:16`) (NEW-3) |

### 2.4 Do the five routine changes each touch one component, or only data?

The requirements now require all five to, each with a test. What is left is small.

| Change | What it touches, as the requirements state it | One component, or only data? | What is left |
|---|---|---|---|
| A new reasoning agent | A roster entry, with its inputs as references, its output's destination, its prompt, schema and access role (`04-agents.md:10`). A routing rule, unless a default covers it (`:18`). The stage cell that names it (`03-stages.md`). A golden set, if it chooses a branch (`04-agents.md:80`) | Only data, tested by a toy agent (`04-agents.md:14`) | R-AGT-1's test checks that "each of its 27 entries validates against the entry schema" (`04-agents.md:14`), so the test changes with every new agent. "At least the paper's 27" would not |
| A new coding backend | One adapter, its configuration, and a mock that passes the same contract tests (`04-agents.md:39`; `08-operation.md:28`), with R-OPS-12's check before dispatch (`08-operation.md:99`). One routing value | One component, tested by a swap and a static check (`04-agents.md:43`) | The adapter must translate the role's access and the session's budget, never hold values of its own (NEW-10). R-OPS-12 forbids Table 8's Antigravity from running for real, and no departure records this (NEW-10) |
| A new task | A manifest and a read-only package, with the manifest's hash registered in the repository (`01-run.md:17-26`), and an entry in the task list (`07-measurement.md:81`) | Only data, tested by a second fixture task (`01-run.md:31`) | Once task 6's F-6 lands, admitting a task runs per-task jobs whose records have task scope. The engine needs that scope once (NEW-5) |
| A new loop limit | One cell of the stage table, or one value of R-STG-13 (`03-stages.md:193`), as R-OPS-2's test shows (`08-operation.md:24`) | Only data, for every limit in the table and in R-STG-13 | The fresh-session re-run count (`02-primitive.md:119`; `06-integrity.md:50`) and the retry counts (`08-operation.md:60`) are in neither (NEW-1) |
| A new model for one stage | One rule of the routing file, scoped to the stage (`04-agents.md:18`) | Only data, tested on A_FullEng in META alone (`04-agents.md:27`) | Nothing |

### 2.5 What did the revision introduce that would make a later change expensive?

- **The vocabulary of outcomes** is split across five lists, and only three groups of roles have a failure value (NEW-1). This came from SA-5's fix, whose list was mine, and incomplete.
- **The ablation's undo of a promotion** contradicts R-STATE-3 (NEW-2). It came from A-ABL-1's refinement, made for Q-11.
- **"Unit of work" is defined two ways** (NEW-3). This came from SA-17's fix, which merged the log into the unit's record.
- **Resuming after a budget stop** contradicts R-STATE-7 (NEW-4). It came from the decision on Q-8.
- **Task 6 is cited as unreviewed,** although its review had landed with 47 accepted fixes, and several of them move rank-1 rows (NEW-5).
- **The engine branch's contract is not mapped** (NEW-6), although `DEVELOPMENT_PROCESS.md` says that the requirements record where it differs.

## 3. New findings

### NEW-1 · major · "The primitive's own outcomes" are cited three times and defined nowhere, and only three groups of roles have a failure value

- **Location.**
  - `02-primitive.md`: R-PRIM-4 (`:55-60`), R-PRIM-5 (`:73`), R-PRIM-10 (`:118-123`), and the floor (`:24-36`).
  - `06-integrity.md`: R-INT-4 (`:48-51`) and R-INT-10 (`:111`).
  - `04-agents.md`: R-AGT-6 (`:56`).
  - `08-operation.md`: R-OPS-7 (`:60`).
  - `03-stages.md`: the table header (`:21`) and R-STG-13 (`:193`).
- **Requirements.**
  - R-PRIM-10: "then maps onto the primitive's own outcomes, per role, as data" (`02-primitive.md:118`).
  - R-INT-10: "Each check's failure maps onto the primitive's outcomes: reject the candidate, fail a refinement into its guard's failure branch, drop an item, or repair." (`06-integrity.md:111`).
  - R-OPS-7: "a unit that still fails after its retries maps onto the primitive's outcomes by its role (R-PRIM-10)" (`08-operation.md:60`).
- **Problem.**
  - **One vocabulary appears as six partial lists:**
    - R-PRIM-4's five at-limit values;
    - R-PRIM-5's failure branch;
    - R-PRIM-10's three: drop the item "after one re-run by a fresh session", reject the candidate, and "stop the run with *error after retries*, for the baseline, the selection or the draft";
    - R-INT-10's four, which add "fail a refinement into its guard's failure branch" and "repair";
    - R-INT-4's four effects of the filter;
    - R-AGT-6's "a score that cannot be computed is recorded as unknown, never as zero", after which the run goes on.
  - **R-PRIM-10 assigns values to three groups of roles:** ablation plans and rebuttal tasks, ideas, and the baseline, selection and draft.
  - **15 roles have no value,** counting A_FullEng once in each of its two stages:
    - the Limitation Extractor and the Limitation Verifier (R-STG-1's test decides the Extractor's case, outside R-PRIM-10);
    - the Idea Generator and A_Evolve;
    - the Ablation Planner, the Ablation Critic and the Result Comparison Agent;
    - A_FullEng in ablation and in meta-review;
    - the Peer Reviewer, the Rebuttal Planner and the Paper Enhancer;
    - the Meta-Reviewer;
    - the reference checker and the alignment checker, when the checker itself fails rather than the check.
  - **The tail's four steps** (the freeze, the test event, the fill and the writer) have no value either.
  - **Nothing makes these values data.** The floor (`02-primitive.md:24-36`) lists no failure value per role, and the stage table has no column for one. So R-STG-13's load check ("the configuration refuses to load", `03-stages.md:193`) never reaches them.
  - **The re-run count has two owners.** It is fixed text twice: "after one re-run by a fresh session" (`02-primitive.md:119`) and "re-run once by a fresh session" (`06-integrity.md:50`). Yet R-OPS-7 makes the retry values task 3's, and R-STG-13 lists neither.
  - **One value that is set costs more than it needs to.** SEL's failure ends a run that holds ranked `Good` ideas, although R-STG-8's band entry names a leader without the Selector: "If one leads by more than the band's margin, it is h_best" (`03-stages.md:115`).
- **Cost of change.**
  - The effects would become three enumerations in three components: the primitive, the hook runner and the failure policy. Every new effect then touches all three, and two are already coming: task 6's "released as failed" (F-3) and its new end state for the tail (F-5).
  - Each role without a value gets decided in code during the build, where nobody sees the decision.
- **Fix.**
  1. Define the vocabulary once, in R-PRIM-2: pass on; discard the candidate; drop the item; keep the last, flagged; keep the current best (the guard's failure branch); keep the accepted items; repair, within a bound; record as unknown and go on; stop the run with a declared outcome. R-PRIM-4, R-PRIM-5, R-PRIM-10, R-INT-4 and R-INT-10 each cite it and choose from it.
  2. Add one column to the stage table, "on failure after retries", with one value per role, the tail's steps and the hooks' checkers included. R-STG-13's load check then covers it.
  3. Make the fresh-session re-run count a value of R-STG-13, beside the 2 repairs per manuscript hook.
  4. Proposal: SEL's failure value is "keep the band's leader", not "stop the run".

### NEW-2 · major · An ablation `Reject` undoes a promotion, which R-STATE-3 forbids, and a `Reject` of the meta stage's candidate has no branch

- **Location.**
  - `03-stages.md`: the ABL row (`:30`), R-STG-9 (`:133`) and R-STG-9's test (`:148`).
  - `05-state.md`: R-STATE-3 (`:28`) and its test (`:30`).
  - `requirements.md:76`, A-ABL-1's decision.
  - `02-primitive.md`: the floor (`:26`) and R-PRIM-5 (`:73`).
- **Requirements.**
  - R-STG-9: "of a candidate promoted in this downstream pass, it undoes the promotion, and the flow goes on as when the guard rejects" (`03-stages.md:133`).
  - R-STATE-3: h_best, E_best and C_best are "replaced only by a refinement that the guard accepts" (`05-state.md:28`). Its test: "a write to the core state from anywhere but the selection or a guard that accepted is refused" (`:30`).
- **Problem.**
  1. **The two tests cannot both pass.** The undo writes the core state, and its cause is a critic's verdict. R-STATE-3's test refuses that write, while R-STG-9's test requires it: "`Reject` after a promotion leads to drafting with the idea as it was before it" (`03-stages.md:148`). The Codex gate found the same contradiction (P1, on `05-state.md:28-30`).
  2. **The primitive cannot express it.** R-PRIM-2's floor has no behaviour that restores the kept candidate, and R-PRIM-5 only replaces it.
  3. **One case has no branch.** In a second downstream pass, the meta stage's guard promoted the candidate before the pass started (`01-run.md:50`). A `Reject` of that candidate is neither "the selected idea" nor a candidate "promoted in this downstream pass".
  4. **The paper does not settle it.** It gives the ablation critic no reject at all: "$d_{\mathrm{abl}} \in \{\mathrm{Good}, \mathrm{Refine}\}$" (`sections/3_new_method.tex:106`).
- **Cost of change.**
  - The binding of the kept candidate is a rank-1 decision (`02-primitive.md:26`).
  - If it is built single-valued, as R-STATE-3 reads, the undo becomes ablation-specific code that reaches into run state.
  - The meta case then becomes a special case across stages, which rank 6, the restarts, must reopen.
- **Fix.**
  - **R-STATE-3** gains a third transition: "restored to its value before the last promotion when a judge rejects the promoted candidate (R-STG-9), with an audit row that names the verdict".
  - **R-PRIM-2** gains a behaviour: "a verdict may restore the kept candidate to its value before the stage's last promotion".
  - **R-STG-9** decides the meta case, with a test for the branch it picks. Two options:
    - a `Reject` in a pass that a meta promotion opened undoes that promotion, and the tail runs with the previous pass's outputs, unapproved, as when the meta guard fails (`03-stages.md:33`);
    - or the task ends with *ablation reject*.

### NEW-3 · major · "Unit of work" has two definitions, and a harness job's failure has no class

- **Location.**
  - `08-operation.md`: R-OPS-5 (`:44`), R-OPS-4 (`:36`) and R-OPS-7 (`:60`).
  - `05-state.md:60`, R-STATE-7.
  - `requirements.md:184`.
  - `06-integrity.md:16`, R-INT-1.
- **Requirements.**
  - R-OPS-5: "Each unit of work, a stage, an agent call, a coding session, a harness job (U-INT-4) or a run, has one record that holds its key, inputs, outputs, cost, timing and outcome."
  - R-STATE-7: "Every unit of work, an agent call, a coding session or a harness job, has a key derived from its place in the run".
  - R-OPS-4: "A unit of work, an agent call, a coding session or a harness job (U-INT-4), starts only if".
  - The presumed rows: "the unit of work sits below a stage, inside A_Coder" (`requirements.md:184`).
- **Elsewhere.** `codex/run-journal:docs/requirements/run-journal.md`: "The unit recorded here is **one external operation**, which may be a child of a stage ... A parent stage later aggregates child outcomes."
- **Problem.**
  - **The two definitions disagree on stages and runs.**
    - Under R-OPS-5's list, a stage and a run are units. Then R-OPS-7 gives each of them "a timeout and a retry policy", and R-STATE-7's "a finished unit is never run again" applies to them.
    - Under the other three requirements, and the journal contract, units are leaves only.
  - **R-OPS-7 does not say which harness-job failures are retried.** It retries "Each unit of work, harness jobs included", and a harness job can fail in two different ways:
    - the machine fails: re-run the same code;
    - the agent's code fails: that failure is a result, which the candidate is judged on.
  - **Only one case of the second kind is classified.** R-INT-1 places a version with no runnable entry point in the second class: it "yields no result" (`06-integrity.md:16`), and its idea is `Bad`. A crash or a timeout of agent code has no class.
  - **Task 6's accepted F-3 decides it:** "What agent code produces (an invalid output, a failure, a timeout against the manifest's limit) is a released result and is never re-run".
- **Cost of change.**
  - Rank 2 is "the unit of work, and what happens when it fails" (`docs/paper/unspecified.md:55`).
  - Designed against R-OPS-5, the journal carries reservations, in-doubt states and retries for composites that need none. Designed against R-STATE-7, R-OPS-5's tests break.
  - A retried crash of agent code draws a new result, which EI-21 forbids. Changing the class later reopens the journal's contract, which every stage writes through.
- **Fix.**
  - Use two terms:
    - a **unit of work** is a leaf (an agent call, a coding session or a harness job), and is the thing that is admitted, reconciled, retried and resumed;
    - a **composite** is a stage invocation, a pass or the run. It has a record keyed the same way, which aggregates its units' records, and it is never retried as a whole.
  - R-OPS-5 then says "each unit of work and each composite has one record".
  - R-OPS-7 adds: "a harness job fails either in the infrastructure, and is retried under the same identity, or in the agent's code, which is a result that is recorded, judged and never re-run (task 6's F-3, pending)".

### NEW-4 · major · Resuming after a budget stop contradicts R-STATE-7, the budget's own fixing rule, and "exactly one outcome record"

- **Location.**
  - `08-operation.md`: R-OPS-4 (`:36`) and its test (`:40`); R-OPS-2 (`:20`).
  - `05-state.md`: R-STATE-7 (`:64`) and its test (`:70`).
  - `01-run.md`: R-RUN-5 (`:57`), R-RUN-8 (`:108`) and R-RUN-8's test (`:111`).
  - `requirements.md:115`, Q-8.
- **Requirements.**
  - R-OPS-4: "Each coding session and each task has a budget, fixed before the task's first run", and a task that cannot afford its next unit "resumes from its record once the budget is raised".
  - R-OPS-2: "model routes, budgets and profiles live in versioned data files".
  - R-STATE-7: "the run reads the configuration versions and the ledger its record names, never the files as they now are on disk". Its test: "configuration files edited on disk in the meantime are ignored".
  - R-RUN-5's heading: "Every task ends with exactly one outcome record".
  - R-RUN-8: "Every stop, whether a guard, a budget or an error, ends the run with its outcome record ... a person may resume a stopped or paused run from its record (R-STATE-7)".
- **Problem.**
  1. **A budget "fixed before the task's first run" cannot be "raised".**
  2. **The resume tests cannot pass together.** A raised budget is an edited configuration file, which resume must ignore under R-STATE-7's rule and test. So R-OPS-4's and R-RUN-8's resume tests (`08-operation.md:40`; `01-run.md:111`) cannot pass beside R-STATE-7's.
  3. **One task gets two outcome records.** A run that wrote *budget exhausted*, then resumes and exports, ends with a second outcome record.
  4. **Resuming after a guard's stop is void, or a re-draw.** R-RUN-8 lets a person resume a run that a guard stopped. Replayed from its records, the run reaches the same guard again.
  5. **Three stop-and-continue paths have two meanings.** A usage window and a billing-environment fault pause the run (R-OPS-12, `08-operation.md:99`), while a budget stop ends it.
- **Elsewhere.** `claude/engine` already treats `BudgetExceeded` as `paused` (`scientisttwo/orchestrator.py:129-131`).
- **Cost of change.**
  - Rank 2, resume, and the outcome record, which carries rank 1's declared outcomes, both depend on whether a stop is final.
  - As written, raising the budget becomes a special path in resume, which reads a file the rule says to ignore. The success report must also choose which of two outcome records counts.
- **Fix.**
  - **One suspended state,** with its reason: a budget, a usage window, or the billing environment. A suspended run has no final outcome.
  - **A raise is an amendment.** It is appended to the run's record as a new budget version, with who made it, when and why, and resume reads it. R-OPS-4 then reads "fixed before the first run, and changed only by a recorded amendment, which the report flags", which answers EI-14's concern.
  - ***Budget exhausted*** is the outcome only of a suspended run that is abandoned.
  - **R-RUN-8 names which stops can be resumed:** suspensions, and never an outcome that a guard declared.
  - **Tests:**
    - a budget raised on disk without an amendment is ignored;
    - with an amendment, the run resumes, and the report flags it.

### NEW-5 · major · Task 6's review has landed and moves two rank-1 rows, while the requirements still cite task 6 as unreviewed

- **Location.**
  - `06-integrity.md:8`.
  - `requirements.md:27` and `:190`.
  - `fix-list.md:17-18`.
  - `03-stages.md:25` and `:58`.
  - `01-run.md:45` and `:63`.
  - `06-integrity.md:107`; `08-operation.md:60`; `05-state.md:60`.
- **Requirements.**
  - "`docs/integrity/blocking-decisions.md` on its own branch, not yet reviewed, states rules IR-1 to IR-31" (`06-integrity.md:8`).
  - "task 6's first version, IR-1 to IR-31, before its review" (`requirements.md:190`).
- **Elsewhere.**
  - `claude/integrity-blockers` is at `04522df`, committed at 14:16 (+04), before `c2ad177` at 14:51.
  - Its file `docs/reviews/integrity-blockers-2026-10-02/fix-list.md` holds fixes F-0 to F-46 and says "**None is declined.**" (`:13`).
  - `blocking-decisions.md` is unchanged since `d5d0d61`. So the fixes are accepted, and not yet applied.
- **Problem.** Four of the accepted fixes move inputs of rank 1 and rank 2.
  - **F-6** (`fix-list.md:38`): "The baseline's fits, its search scoring and the sealed check all run at admission, with records and ledger entries of task scope that runs only refer to."
    - Its decision: "a baseline that fails is never admitted, so no run starts".
    - The review's road not taken (M3) reads "WHY NOT before round 0: parallel runs would race for a job the harness allows only once" (`system-architect.md:236` there).
    - It moves the BASE row's "once per task, before round 0" (`03-stages.md:25`), R-STG-3 (`:58`), R-RUN-4's step 2 (`01-run.md:45`), and R-RUN-5's run outcome *the baseline not reproduced* (`:63`).
  - **F-5** (`fix-list.md:37`): "Add the table "Gates on the primitive" (a *filters* parameter for G2 and G3; G4 and G5 as a nested primitive)". It also adds the tail's end state "test event done, not exported".
    - F-35 (`:72`) adds A-NOTE-1 to task 6's constrained rows: "(the *filters* parameter and the tail's row)".
    - A list of *filters* per stage conflicts with R-INT-10's hooks, which are "declared in data by the kind of step, not by stage" (`06-integrity.md:107`). It is the very list that R-INT-4 removed ("with no list to edit", `:47`): a new code-producing stage that omits G2 would run unfiltered.
  - **F-3** (`fix-list.md:30`) moves R-STATE-7's place key (`05-state.md:60`) and R-OPS-7's retry of harness jobs (`08-operation.md:60`). It brings three rules:
    - **a content identity for every harness job:** "the event kind, its scope (task, run or audit), the manifest hash, the freeze hash where there is one, the row, the seed and the setting" (the review's B1, `:125` there);
    - **agent-code failures are released results,** never re-run;
    - **resume runs "from its last finished stage, before or after the freeze".**
  - **F-15** (`fix-list.md:47`): "C_base is scored as a row and frozen as a control". This adds a second harness job to BASE.
- **Cost of change.**
  - Suppose task 3 fixes rank 1 with BASE as a run stage and the hooks by kind of step, and task 6 then writes BASE as an admission step and the gates as a stage parameter. Two rows are then redesigned.
  - The mapping of gates onto the primitive also gets a second home: task 6's table beside R-INT-10. That is SA-6's pattern again.
- **Fix.**
  1. **Update the citations.** The requirements cite `04522df`, and mark these as changing under task 6's F-3, F-5 and F-6:
     - the BASE row and R-STG-3;
     - R-RUN-4's step 2, and R-RUN-5's *baseline not reproduced*;
     - R-INT-10 and R-OPS-7;
     - R-STATE-7's key.
  2. **One home for the gate mapping.** Task 6's "Gates on the primitive" points to R-INT-10, and *filters* is R-INT-10's list of hooks by the kind of step. A stage may extend that list, and never shorten it.
  3. **Proposal, for task 3:**
     - a stage configuration carries its scope, task admission or run, so that BASE moves by data;
     - a harness job's content identity is its key for idempotence, and the place key points to it, so that per-task jobs are shared across runs.

### NEW-6 · major · The engine branch's contract is a second home, not mapped, and it decides rank 1 against the requirements

- **Location.**
  - `requirements.md:120-133`, the table of contracts written elsewhere.
  - `DEVELOPMENT_PROCESS.md:521-523`.
- **Elsewhere.** `claude/engine` at `7e3f0c3`, committed 2026-10-02 13:54, after the draft I reviewed. Its rank-1 shape:
  - the orchestrator: "The orchestrator is analysis §4's control flow as plain Python" (`docs/architecture/engine.md:12-13`), and it calls the stages in code (`scientisttwo/orchestrator.py:109-117`);
  - the stages: "one module per paper section, each a use of the primitive" (`engine.md:22-23`), and the idea rounds are a loop of their own, `while candidates:` (`scientisttwo/stages/evolution.py:50`);
  - the primitive's parameters: "generator, critic, refiner, verdict map, guard, limit, exhaustion policy" (`engine.md:49`), the narrow set of SA-1.

  Its other decisions:
  - "`Reject` ends the run with "no contribution"" (`:218`), with no undo;
  - "The Result Comparison Agent (P-ROSTER-19) is a numeric test, not an agent" (`:197`);
  - "The `test` split is scored once, at export" (`:114`);
  - the budget's "caps per run: agent calls, coding sessions, wall-clock hours, equivalent USD" (`:44`);
  - `agent.json` holds "kind, tools, paper reference" (`:162`);
  - the run's end states, "done | no_success | ablation_rejected | baseline_failed | paused (resumable) | error" (`orchestrator.py:13`).
- **Requirements it contradicts.**
  - R-PRIM-1 and its static check (`02-primitive.md:12`, `:19`).
  - R-RUN-4 (`01-run.md:43`).
  - R-PRIM-2's floor (`02-primitive.md:23-36`).
  - R-RUN-5's list (`01-run.md:59-68`).
  - R-PRIM-6: "The Result Comparison Agent still runs" (`02-primitive.md:79`).
  - R-STG-9's undo (`03-stages.md:133`).
  - R-RUN-7's freeze before the test event (`01-run.md:93-97`).
  - R-AGT-4: "roster entries hold engine-level session settings only" (`04-agents.md:39`).
  - R-MEAS-8: a subscription estimate is "a diagnostic and never as a bill" (`07-measurement.md:73`). BA-5 adds that a subscription operation "cannot reserve `usd_spend`".
- **Problem.**
  - `DEVELOPMENT_PROCESS.md:521-523` says of this engine: "Its decisions on the register mostly match the ones taken here; where they differ, the requirements say so."
  - Yet no requirement file names `claude/engine` or `engine.md`. The table of contracts written elsewhere lists only the four Codex contracts.
  - `engine.md` also sits in `docs/architecture/`, which is task 3's output folder.
- **Cost of change.** This is the largest cost in the project today.
  - Each stage built on `claude/engine` is stage-specific code that rank 1 removes.
  - Every change to a stage is made twice, in a stage module and in a configuration, until one side yields.
  - A new coding backend touches every `agent.json`, since the tools sit in the roster.
  - Task 3's rank-1 document and `engine.md` will collide in one folder on merge.
- **Fix.**
  1. Add `engine.md` to the table with the status *diverges*, listing each requirement it contradicts (the list above).
  2. Correct `DEVELOPMENT_PROCESS.md:521-523`.
  3. Before task 3 writes rank 1 into `docs/architecture/`, the coordinating session decides one of two ways. This is not task 3's decision.
     - `claude/engine` moves onto task 3's primitive, and its stage modules become configurations.
     - Or task 3 starts from `engine.md`, and the requirements record each departure.

### NEW-7 · minor · Three lists are still closed, and four cells sit outside them

- **Location.**
  - `02-primitive.md`: `:55`, `:89` and `:29`.
  - `03-stages.md`: `:24`, `:25`, `:30`, `:31` and `:34`.
- **Requirements.** Three closed lists:
  - R-PRIM-4: "The at-limit value is one of these" (`02-primitive.md:55`);
  - R-PRIM-7: each assessor kind comes "from the list of R-PRIM-2" (`:89`);
  - R-PRIM-2: "a verdict map onto accept, refine and reject" (`:29`).
- **Problem.**
  - SA-1's fix made R-PRIM-2 a floor, but R-PRIM-4 and R-PRIM-7 close their lists again.
  - The merged assessor list dropped the first draft's "none", which DRAFT and TAIL now use (`03-stages.md:31`, `:34`).
  - The verdict map's range has no "stop the run", which BASE uses (`:25`), and no undo, which ABL uses (`:30`).
  - SEED keeps "the whole pool, sorted by score, descending" (`:24`), which is not one of R-PRIM-4's values.
- **Cost of change.** One value per list. But a strict reading, by task 3 or by a schema check, would reject four of the default cells.
- **Fix.**
  - R-PRIM-4 reads "at least these".
  - R-PRIM-2's list of assessors adds "none: the generator's output passes on".
  - The verdict map reads "onto accept, refine, reject, or an outcome from the vocabulary of NEW-1".
  - SEED's cell reads "keep the accepted items: every idea, ranked by the assessor's score".

### NEW-8 · minor · The table lacks the rows that R-PRIM-1 loads, and one test still picks the meta mechanism

- **Location.**
  - `02-primitive.md`: `:12`, `:16` and `:99`.
  - `03-stages.md`: `:21-34` and `:33`.
  - `01-run.md`: `:47`, `:48`, `:50` and `:97`.
- **Problem.**
  - **No rows for two loaded configurations.** R-PRIM-1's test loads "A_Coder, the tail and the run's sequence from data" (`02-primitive.md:16`), but no row states the values of A_Coder or of the sequence. So the coverage checker cannot check them, as it now checks the TAIL row.
  - **The TAIL row lacks the export.** It omits R-RUN-7's step 4, "the export (R-STATE-6)" (`01-run.md:97`), which R-RUN-4 also places in the tail (`:48`).
  - **A test picks the mechanism.** R-PRIM-8's test requires "the downstream pass nested in the meta stage, both from data" (`02-primitive.md:99`), against R-RUN-4's "How this is built is task 3's (A-NOTE-1)" (`01-run.md:50`).
  - **The nesting is opposite.** R-RUN-4's step 4 (`:47`) and the META row (`03-stages.md:33`) nest in opposite directions (section 2.2).
- **Cost of change.** Small, but the test would fail a design that task 3 is told it may choose.
- **Fix.**
  - Add an A_Coder row and a row for the run's sequence, or put the sequence as a list beside the table.
  - Add the export to the TAIL row.
  - R-PRIM-8's test reads "the downstream pass re-run after a meta promotion, from data, gives the call counts of R-STG-12".
  - R-RUN-4's step 4 reads "a downstream pass of ablation, drafting and peer review, then meta-review".

### NEW-9 · minor · The hooks' repair loop has an ambiguous counter and a re-check rule of its own, and two output checks have no home

- **Location.**
  - `06-integrity.md:111`.
  - `05-state.md:45`.
  - `03-stages.md`: `:77` and `:164`.
- **Problem.**
  1. **The counter may never bind.** The bound is "at most 2 repairs per hook and manuscript version" (`06-integrity.md:111`), and R-STATE-5 makes "one manuscript version per revision" (`05-state.md:45`). If a repair is a revision, the counter resets with every repair, and the bound never binds.
  2. **The re-check rule is special.** "A repair does not start the sequence over; only the compile check runs again after the last hook" (`06-integrity.md:111`) is a rule that singles out one kind of check. The Codex gate (P1, on this line) shows that an alignment repair can add a typed number or a fabricated citation after those checks have passed.
  3. **Two deterministic checks on a step's output have no home.** Neither sits in a hook or in a behaviour of the floor.
     - The engineer's "step that changes the idea's component list is refused and counted" (`03-stages.md:77`). What the refusal counts against is unstated.
     - A rebuttal task "that names any other data is refused" (`03-stages.md:164`). What follows the refusal is unstated.
- **Cost of change.** Each new manuscript check needs its own decision about what re-triggers it, and each new output check becomes code in its stage.
- **Fix.**
  - One nested instance of the primitive per hook point:
    - its assessor is the ordered list of checks, all re-run after any repair;
    - its bound counts once per hook invocation, the per-invocation scope that R-PRIM-2 already defaults to (`02-primitive.md:32`).
  - Add two entries to R-INT-10's list, each with its effect taken from NEW-1's vocabulary:
    - after a code-producing step by an engineer, the component-list check;
    - after a planning step, the registered-settings check.

### NEW-10 · minor · Backend settings, session budgets and the second backend

- **Location.**
  - `04-agents.md:39`, R-AGT-4.
  - `08-operation.md`: R-OPS-4 (`:36`) and its test (`:40`), R-OPS-8 (`:68`), R-OPS-12 (`:99`).
  - `07-measurement.md:77`.
  - `codex/budget-admission:docs/requirements/budget-admission.md`.
- **Problem.**
  1. **A role's access could live in two places.** R-AGT-4 puts "its tools, permissions and turn limits" in the adapter's configuration, while R-OPS-8 holds each role's access and R-OPS-4 each session's budget. Unless the adapter translates them, every new backend re-encodes every role.
  2. **The budget names no resource.** Under R-OPS-12 every call bills zero: R-MEAS-8's test expects "a billed amount of zero" (`07-measurement.md:77`). So a budget in dollars never binds, and R-OPS-4's own test needs "a task budget below the scenario's cost" (`08-operation.md:40`). BA-5 already counts `claude_calls`.
  3. **"Session" means two things.** R-OPS-4 means a coding session. In BA, a session's gate is "shared by every task/run root in that session".
  4. **The second backend cannot run for real.** R-AGT-4 requires a second backend "as Table 8 runs it with Antigravity" (`04-agents.md:39`), which R-OPS-12 forbids from running for real. No *Departs from* records P-ROSTER-49, and the checker lists no such departure.
- **Fix.**
  - R-AGT-4 adds: "the adapter translates the role's access policy (R-OPS-8) and the session's budget (R-OPS-4) into its backend's permissions and limits, and holds no value per role".
  - R-OPS-4 names its resources: calls, tokens, wall-clock time, machine-hours, and dollars for metered work only. It also writes "coding session".
  - R-AGT-4 departs from P-ROSTER-49. The second backend that runs for real is one that bills the subscription, such as the Agent SDK, and Antigravity runs only as a mock.

### NEW-11 · minor · U-ART-15's presumed row is not the register's proposal

- **Location.**
  - `requirements.md:178-179` and `:188`.
  - `docs/paper/unspecified.md:134`.
- **Requirements.**
  - "Some requirement texts presume a register proposal of another task" (`requirements.md:178`).
  - "| U-ART-15 (3) | access is declared per agent role, and a stage may only narrow it [ours] | R-OPS-8 |" (`:188`).
  - The register proposes "A sandbox policy per stage for installs, network and GPUs, with the evaluation protocol read-only to every agent [ours]" (`unspecified.md:134`).
- **Problem.** R-OPS-8 replaces the register's proposal; it does not presume it. Task 3 reads the register first, and will see "per stage".
- **Fix.** Mark the row as replacing the register's proposal: per stage becomes per role (SA-8). Task 3 then reads the requirement's choice as the one that stands, and remains free to decide otherwise and revise R-OPS-8.

## 4. Verdict

Task 3 can start rank 1 from this revision.
- **SA-1 and SA-2 are resolved in substance.** R-PRIM-2 is a floor that holds every row of the stage table, the TAIL row included, except ABL's undo of a promotion. The run's sequence is data, with a test that can fail. Each stage that can end the run declares its outcome. The meta restart is one behaviour, stated consistently.
- **Before rank 1 closes, two findings must land.**
  - NEW-1: one vocabulary of outcomes, with a failure value for every role as a column of the table.
  - NEW-2: the undo, which contradicts R-STATE-3, and the case of the meta stage's candidate.
  - Each is a few sentences of requirement text, and each shapes the parameter cut. NEW-7 and NEW-8 can land in the same edit.
- **Rank 2 waits on two findings.** NEW-3 fixes what a unit of work is and how a harness job fails. NEW-4 decides whether a budget stop suspends the run or ends it.
- **Two decisions belong to the coordinating session.** Take them while rank 1 is drafted, because each changes what rank 1 must express.
  - NEW-5: whether the requirements take in task 6's reviewed fix list now. It moves BASE to task admission, and gives the gates a stage parameter.
  - NEW-6: what `claude/engine`'s `engine.md` is to task 3. It already builds the primitive that SA-1 rejected, in the folder task 3 writes to.
