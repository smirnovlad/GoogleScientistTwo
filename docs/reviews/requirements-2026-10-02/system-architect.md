# Review: system-architect, the requirements draft of TODO task 2 (2026-10-02)

- **Reviewed:** `docs/requirements.md`, `docs/requirements/01-run.md` to `08-operation.md`, and `playground/paper/requirement_coverage.py` only where it bears on the boundary check. The change is `git diff claude/paper-analysis...HEAD` on `claude/requirements` at `ff1faaa`.
- **Lens:** what the next change costs; whether the stage primitive and its parameters hold as data; whether task 3 can design components from these requirements.
- **Mode:** read-only. I edited no file and changed no git state.
  - `python3 -B playground/paper/requirement_coverage.py` reports 0 problems: 177 elements, 71 requirements, and 33 task-2 rows decided.
  - Its `--selftest` passes every planted defect, so that zero can fail.
  - The worktree was unchanged after both runs.
- **Four voices, kept apart:**
  - *Paper* is arXiv:2609.19644v1, quoted from `docs/paper/source/` and checked on 2026-10-02.
  - *Draft* is the files under review, cited by file, requirement ID and line.
  - *Proposal* is mine, and is never a decision.
  - *Elsewhere* is files outside the reviewed diff, read-only on 2026-10-02 and cited by branch.
- **Paths** are relative to the repository root.

## Summary

- **The primitive's parameter list is too narrow (SA-1).** The stage table is the right instrument. But the parameter list closes four of its value domains too narrowly (R-PRIM-2, R-PRIM-4, R-PRIM-7, R-PRIM-8), and then cannot hold the table's own rows.
  - EVO's rounds, SEL's choice, the SUB and FULL veto, A_Coder, ABL's plan-then-execute, PEER's rebuttal cycle and META's downstream pass would each become stage-specific code.
  - So R-PRIM-1 cannot be met as written.
- **The meta restart is stated three incompatible ways, and the run's stage order is not data (SA-2).** So "a new stage is a change of data only" has no requirement behind it.
- **Rank 2, the unit of work and its failure, is too weak for a multi-day run (SA-4, SA-5).** It also has a second home in committed Codex code (SA-6).
- **Only two of task 3's five routine changes are close to one component or only data:** a new loop limit (for the eleven table rows) and a new coding backend. A new model for one stage, a new task and a new agent are not required to be (SA-10).
- **Several tests would pass on a broken engine,** R-PRIM-1's among them (SA-11). The enforcement tests run against mocks of the enforcement (SA-12).
- **Verdict:** task 3 cannot start rank 1 from this draft. SA-1 and SA-2 must change first, and both are small changes of text. SA-4 to SA-6 must change before rank 2.

## What holds

- **The default stage configuration is one table.** Each value is tagged as the paper's or ours, and a value no task has set refuses to load (R-STG-13). A changed limit is one cell, and an unknown is never silently a default.
- **R-PRIM-3 keeps Listing 1's counting as a value** that no default uses, so the paper's literal convention stays a data change away.
- **R-PRIM-6 replaces the Result Comparison Agent's preference with one deterministic rule** over harness results. ABL and META share the rule, and the agent's reading is recorded.
- **R-PRIM-8 requires order independence,** and its test can fail.
- **R-OPS-3's static check can fail:** a provider's library may be imported only inside its adapter.
- **The coverage checker plants each defect beside a clean twin.** It enforces the *Decides* and *Depends on* boundary at the level of those fields.

## Findings

### SA-1 · blocker · The primitive's parameter list cannot hold the draft's own stage table

- **Location.**
  - `docs/requirements/02-primitive.md`: R-PRIM-2 (lines 20–29), R-PRIM-4 (44–48), R-PRIM-7 (71) and R-PRIM-8 (77).
  - `docs/requirements/03-stages.md`, the default stage configuration (17–29).
  - `docs/requirements.md` line 138.
- **Draft.**
  - R-PRIM-1 (line 12): "No stage has a loop of its own in code".
  - R-PRIM-2: "A stage configuration sets these parameters, and the primitive honours each one". Its domains are closed:
    - the assessor is "of one kind: an LLM verdict, a numeric threshold on a score, a score with no verdict, a deterministic check, or none" (line 23);
    - the verdict map maps "onto accept, refine and reject" (24).
  - R-PRIM-4 allows four at-limit values: discard, keep the last, keep the current best, and stop the run.
  - R-PRIM-8: "A stage's generator or refiner can be another stage configuration".
- **Paper.**
  - Table 1 gives idea evolution the critic *Idea experiment* (tables/overview.tex:19), so A_Coder is that stage's assessor.
  - The rounds stop on a count of `Good` summed over all rounds (sections/3_new_method.tex:84–86).
  - After a promotion, the ablation stage "re-executes the ablation planning phase on the updated candidate" (3_new_method.tex:113).
  - After an accepted meta refinement, the engine "re-executes downstream ablation planning, ablation execution, manuscript re-drafting, and simulated peer-review cycles" (3_new_method.tex:149).
- **Problem.** The draft's own table needs more than these domains allow, and two domains contradict each other.
  - R-PRIM-2's assessor kinds include "none" and not "a choice". R-PRIM-7's include "a choice" and not "none". No default stage uses "none", and SEL needs "a choice".
  - "Of one kind" excludes two of the table's own assessors:
    - SUB's and FULL's "LLM verdict under a numeric veto";
    - SEL's "the task's validation metric ranks …; the Selector, an LLM, chooses".

  The table below answers the brief's question 1, behaviour by behaviour.

| Behaviour | Holds under R-PRIM-2? | What is missing | Parameter that would avoid stage-specific code (proposal, for task 3) |
|---|---|---|---|
| EVO, the population loop | no | A_Coder as the assessor (R-PRIM-8 nests only generators and refiners). Per-candidate verdicts folded into one stage verdict ("`Good` → counted" is not accept, refine or reject). A population that grows, where Listing 1 replaces one candidate. The next unevaluated seed drawn by a cursor, which no agent does. At the limit, "with at least one `Good`, go to selection; with none, stop the run", which is none of R-PRIM-4's four values | any role may be a nested stage; a rule that aggregates a fan-out's outcomes, with its test point; an update that replaces or appends; a role may be a named deterministic operation (top-k, next-n by cursor); an at-limit value "keep the accepted items" |
| SEED, the count stop | yes, with two conventions | what decides when the assessor gives no verdict; how a new idea joins the pool | state that the stop tests decide, and refine otherwise; append, as EVO also needs |
| BASE, the deterministic check | yes, once "stop the run" names its outcome | "outside → stop the run" is outside the verdict map's range. Encoded as refine, a limit of 0 and "stop the run" at the limit, it fits, but R-PRIM-4's "stop the run" names no outcome | an outcome name for each stage that can end the run |
| SUB and FULL, the numeric veto | no | two assessor kinds in one stage | a deterministic precondition over harness records that an LLM accept must pass, so the LLM can only be stricter |
| SEL, the choice | no | R-PRIM-2 has no "choice"; ranking plus an LLM choice is two kinds | the same precondition, narrowing the options the LLM chooses among |
| ABL, the restart after a promotion | partly | R-PRIM-5's restart holds. The generator is a plan followed by one coding session per plan. That is a sequence, which R-PRIM-8 does not allow | sequence composition, fanning out over the previous step's items |
| PEER, the rebuttal cycle | no | the refiner is plan → N_t sessions → Enhancer | as for ABL |
| A_Coder (R-STG-6), not a table row | no | a conditional sequence: SUB, then FULL only after a subset `Good`, returning one trace | sequence composition, with a continuation for each outcome |
| META, the nested downstream pass | no, and contradictory | see SA-2 | see SA-2 |
| ABL and META keep the run's core state | partly | the kept candidate is run state (h_best, E_best, C_best), not local to the stage | bindings: a role's inputs and the kept candidate are references to named run-state objects |
| Fresh N_abl and N_peer per pass (U-META-1) | no | counter scope is not a parameter | counter scope: per invocation (the default) or per run |
| The integrity hooks | no | see SA-3 | see SA-3 |

- **Cost of change.** Under the draft, seven behaviours become stage-specific code beside the primitive: EVO's round loop, A_Coder, ABL's plan-and-execute, the rebuttal cycle, the downstream pass, the vetoes, and SEL's pre-selection.
  - Every later change to one of them is a code change in its own path.
  - The nearest such change is already drafted elsewhere: task 6's in-progress `docs/integrity/blocking-decisions.md` (IR-7, untracked on `claude/integrity-blockers`).
  - IR-7 gives every performance gate, the ablation's "clean breakdown" included, "a numeric precondition over harness records, whose rule task 2 sets per gate".
  - Under R-PRIM-2 that is new code in each gate. Under a precondition parameter it is one cell per stage.
- **How this happened.**
  - The columns of `docs/paper/analysis.md` §3.4 still stand, as this persona's task-1 closure check said ("Its columns are the full parameter set").
  - The draft then closed four of those domains too narrowly: assessor, verdict map, at-limit and nesting.
  - It also moved the specification filter to "points that no stage owns", although §3.4 had put it in the SUB row's guard cell (analysis.md:128).
  - My closure check never tested the columns against the EVO and META cells. Counter scope, and appending against replacing, have no column there either.
- **Fix.**
  1. Make R-PRIM-2's lists a floor ("at least"), and leave the parameter design to A-NOTE-1, which task 3 owns (SA-7). The behaviours in the table above become what the primitive must express, each with a mock test.
  2. Merge R-PRIM-2's and R-PRIM-7's assessor kinds into one list.
  3. Rewrite the out-of-domain cells in the revised vocabulary:
     - EVO's verdict map and its at-limit value;
     - BASE's and ABL's "stop the run";
     - the SUB, FULL and SEL assessors;
     - META's generator and nesting.
  4. Replace R-PRIM-1's test with the conformance test in SA-11.
  5. In `docs/requirements.md` line 138, rank 1 is R-PRIM-1 to R-PRIM-9 and the table, not "R-PRIM-3 to R-PRIM-6".
  6. Optionally, `requirement_coverage.py` could check that the table's columns and R-PRIM-2's parameters are one list. Today R-PRIM-2 names nine parameters and the table has eight parameter columns: "stop tests" is folded into "Limit".

### SA-2 · blocker · The run's composition is not data, and the meta restart is specified three ways

- **Location.**
  - `01-run.md`: R-RUN-4 (lines 38–49) and R-RUN-5 (53).
  - `02-primitive.md`: R-PRIM-1 (12) and R-PRIM-5 (56).
  - `03-stages.md`: the META row (29) and R-STG-12 (143–146).
  - `docs/paper/unspecified.md` line 101, A-META-1's decision.
  - `docs/paper/traceability.md` line 207, P-META-5's component.
- **Paper.**
  - The engine "re-executes downstream ablation planning, ablation execution, manuscript re-drafting, and simulated peer-review cycles" (3_new_method.tex:149).
  - The loop repeats "for a maximum of N_meta iterations or until d_meta = Accept" (3_new_method.tex:151).
- **Draft.** It gives one behaviour three mechanisms:
  1. **A re-entry at run level.** A new pass "starts … at the ablation stage" (R-RUN-4, line 46). A-META-1's adopted decision calls this "a value of the stage graph".
  2. **Nesting in the refiner.** "Its refine nests a whole downstream pass" (the META row's last cell). `traceability.md` line 207 repeats it: "the ABL, DRAFT and PEER configs inside its refine".
  3. **R-PRIM-5's generic restart.** An accepted refinement makes "the stage restart on it".
     - For ABL this re-runs planning, as the table says.
     - META's generator, though, is "the peer stage's last P_new and R_new": a binding, with nothing to re-run.
- **Problem.**
  - R-PRIM-1 says "a new stage … is a change of data only". Yet R-RUN-4 fixes the stage order as a requirement, and no requirement makes the order data.
  - R-RUN-5's outcomes come "from a fixed list".
- **Cost of change.** Each mechanism needs a different component:
  1. a stage-graph component, with edges and counters scoped per pass;
  2. a sequence nested in a refiner, with the first pass held outside META;
  3. a generator for META that can be re-run.
  - The tests of R-RUN-4 and R-STG-12 pass under all three, so whichever one task 3 builds goes undocumented.
  - With the order and the outcomes in code, each new stage touches both the run driver and the outcome list.
  - Task 6's in-progress draft already plans two such changes:
    - IR-14 and IR-17 add a freeze, a test event and a final fill before export;
    - IR-6 adds an integrity-failure outcome to U-EVO-4's list.
- **Fix.**
  - State the behaviour once in R-RUN-4 and R-STG-12, without naming a mechanism: what re-runs, what never does, fresh counters, and the Meta-Reviewer asked again.
  - Add a requirement that the run's stage sequence is data, with a test. A toy stage inserted between SEL and META by data alone runs in order. A toy stage that declares its own stop outcome ends a scripted run with that outcome.
  - Each stage that can end the run declares its outcome. R-RUN-5's list is then the union of the default configuration's declarations and the two operational outcomes.
- **Proposal, for task 3.** One mechanism serves all three readings.
  - The run is a sequence of stage configurations: LIM, SEED, BASE, EVO (with A_Coder nested for each candidate), SEL, META, then the tail of SA-9.
  - META's generator is the sequence ABL, DRAFT, PEER.
  - R-PRIM-5's restart re-runs a guarded stage's generator, for ABL and META alike.
  - Counters live per invocation, so U-META-1 holds without a rule of its own.
  - A failed guard and META's limit both exit keeping the current outputs, flagged unapproved where R-STG-12 says so.
  - No graph edges are needed, and a new stage is an insertion into a sequence.

### SA-3 · major · The integrity and manuscript checks sit outside the primitive, and their repair loops have no limit

- **Location.**
  - `03-stages.md`: lines 12–15, the DRAFT row (27) and R-STG-10 (125).
  - `06-integrity.md`: R-INT-4 (36–39), R-INT-5 (48) and R-INT-6 (57).
  - `08-operation.md`: R-OPS-7 (56).
- **Paper.** Both checks are coding sessions (sections/4_experiment.tex:43):
  - the filter is "a validation filter that uses the Coding Agent to detect and discard rule-violating solutions immediately after experimentation";
  - "the Coding Agent audits the repository against the manuscript to produce an audit report, which the Writer Agent then uses to rectify any discrepancies in the method section".
- **Draft.**
  - **No hook points.** "Three checks run at points that no stage owns" (lines 12–13). No parameter of R-PRIM-2 declares a hook point, so no stage configuration can say where a check runs.
  - **The filter's scope is a list of stages.** R-INT-4 defines "every experiment" by listing stages, and the baseline is not in the list. A new result-producing step inherits the filter only if someone edits the list. U-SUB-2's baseline tuning is one such step, and the BASE row leaves it to task 6.
  - **The filter's effects are not declared.**
    - Its three discard effects are the primitive's own outcomes: an idea `Bad`, a refinement discarded, an item dropped. The draft does not declare them as such.
    - A SUB engineering round discarded after a valid first result fits none of them.
  - **The compile check.**
    - The compile-and-format check runs "after the draft and after every revision" (R-STG-10), but it is missing from the list of cross-cutting checks.
    - Its failure goes to R-OPS-7. So a manuscript that will not compile ends the task as *error after retries*: a content failure recorded as an infrastructure failure, and DRAFT's behaviour lives outside its configuration.
  - **The triggers disagree.**
    - R-INT-5 runs its check "after the draft, after every enhancement and every re-draft, and once more before export"; R-STG-10 runs "after every revision".
    - The writer's corrections are revisions, so whether they re-trigger the checks is open.
    - Each check → correct pair is a judge → refine loop with no limit and no at-limit value. That is a loop of its own in code, against R-PRIM-1.
    - No order is given among the three checks at one point.
- **Cost of change.** Each hook becomes a call written into each stage's path, or a special case inside the primitive.
  - A new check then touches every path. Task 6's in-progress IR-7 adds one: it matches every number in a critic's rationale against harness records.
  - So does a new result-producing stage.
- **Fix.**
  - Declare the hook points as data, by the kind of step rather than by stage:
    - after a code-producing step: harness scoring, then the specification filter;
    - after a manuscript-producing step: compile, references, then the method–code audit, in a stated order;
    - before export.
  - Give each check's failure an effect in the primitive's vocabulary: reject the candidate, fail the refinement into the guard's failure branch, drop the item, or repair.
  - Make each repair an instance of the primitive, with a limit and an at-limit value.
  - State that a hook's own correction does not re-trigger that hook.
  - **Test.** A toy result-producing stage added by data has its results filtered, with no code change. An unfixable planted citation ends at the repair limit, with the declared outcome.

### SA-4 · major · Resume and the unit of work are too weak for a run of 2.5 days

- **Location.**
  - `05-state.md`: R-STATE-7 (59–63).
  - `08-operation.md`: R-OPS-4 (33), R-OPS-5 (41) and R-OPS-7 (56).
  - `07-measurement.md`: R-MEAS-8 (72).
- **Draft.**
  - R-STATE-7: "Every finished unit of work is written to disk before the next starts. After a crash, the run resumes from the last finished unit, and a retry never repeats a unit that finished".
  - Its test kills the run once, "inside A_Coder after k finished units".
- **Problem.**
  1. **Harness jobs are not units of work.**
     - R-OPS-5 logs "each stage, agent call and run". R-OPS-4 budgets "each coding session and each task".
     - R-MEAS-8 prices machine-hours per call, stage and task, and names no harness job.
     - The full-benchmark evaluations, likely the longest GPU jobs of a run, have no timeout, retry, budget or resume requirement.
  2. **There is no in-doubt state.** After a timeout the engine cannot know whether a paid call finished. R-OPS-7 retries it as failed, so "never pays twice" cannot be kept as worded.
  3. **A resumed unit's starting point is unstated.** It must start from its recorded input snapshot, never from a half-edited workspace. R-STATE-4 makes code versions snapshots, but does not tie resume to them.
  4. **Resume must use the recorded configuration versions and the recorded ledger,** and neither is required. A resumed run could pick up a prompt edited during the crash, or start with a fresh budget.
  5. **Units have no stable identity.** With parallel fan-out (R-PRIM-8), a resumed run must map each record to its unit by a key derived from the unit's place (stage path, pass, round, item, attempt), not by completion order.
  6. **The test has one kill point.** A kill inside A_Coder passes on an engine that checkpoints only there. ABL's and PEER's fan-outs, the second downstream pass and harness jobs go untested.
  7. **"Afford" is undefined.** R-OPS-4's "a task never starts a unit of work it cannot afford" needs a reservation for each unit, which no requirement provides.
- **Cost of change.** Met during a run, each gap costs GPU-days or a double spend. Met after task 3, it reopens the journal's contract, which every stage writes through.
- **Fix.**
  - Name harness jobs as units of work in R-OPS-4, R-OPS-5, R-OPS-7 and R-STATE-7.
  - Add four rules:
    - an in-doubt outcome, reconciled before any retry;
    - a resumed unit starts from its recorded input snapshot;
    - resume reads the recorded configuration versions and the recorded ledger;
    - unit keys derive from each unit's place.
  - Define "afford": the remaining budget, net of unresolved reservations, is at least the unit's declared reservation.
  - **Test.** Kill the run at every unit boundary: inside a fan-out, inside the second downstream pass, during a harness job, and between a paid call's return and its durable record. After the restart:
    - each finished unit is called once;
    - the unit in flight is called at most once more;
    - configuration files edited on disk in the meantime are ignored.

### SA-5 · major · A unit that fails after its retries ends the task, whatever it was

- **Location.**
  - `08-operation.md`: R-OPS-7 (56–60).
  - `06-integrity.md`: R-INT-4 (39).
  - `04-agents.md`: R-AGT-8 (63–67).
  - `02-primitive.md`: R-PRIM-7.
- **Draft.**
  - R-OPS-7: "a unit that still fails after its retries ends the task with *error after retries*".
  - R-INT-4: a rule-breaking ablation or rebuttal result "is dropped … and the discard is recorded", and the critic reads the others.
  - No requirement says what a judge's malformed output does: a word outside its verdict vocabulary, or an output that fails its schema. R-AGT-8 tests only that mock outputs validate.
- **Problem.**
  - One of the N_p ablation sessions that keeps crashing ends a run that already has a selected idea. The same item, had it broken a rule, would only have been dropped.
  - An implementation that maps an unknown verdict to accept passes every test.
- **Cost of change.**
  - The failure policy (U-TOP-2, task 3, rank 2) inherits two contradictory rules.
  - Resolved as stage-specific code, each new fan-out stage adds a branch.
  - Resolved as one global rule, it wastes days of a run.
- **Fix.**
  - Failure after retries maps onto the primitive's own outcomes, per role, as data:
    - drop the item: an ablation plan or a rebuttal task;
    - reject the candidate: an idea becomes `Bad`, with the reason *error*;
    - end the run: BASE, SEL or DRAFT.
  - A malformed judge output is a failed attempt of that unit. It is retried, and never maps to accept.
  - **Test.** An ablation session scripted to fail every time is dropped and recorded, and the critic reads the rest. A critic that returns an unknown word is retried, then takes its configured branch, never accept.

### SA-6 · major · Rank 2's requirements have a second home, already in code

- **Location.** `docs/requirements.md` lines 124–138, the table of rows left to other tasks, names none of the following.
- **Elsewhere.** These are outside the reviewed diff and none is merged into `claude/requirements`:
  - `codex/run-journal:docs/requirements/run-journal.md`, RJ-1 to RJ-7, with `scientist_two/run_journal/` and its tests;
  - `codex/budget-admission:docs/requirements/budget-admission.md`, BA-1 to BA-6, with `scientist_two/budget/`;
  - `docs/requirements/verified-results-tables.md`, VT-1 to VT-5, untracked in the worktree of `codex/verified-tables`, with `scientist_two/reporting/`.
- **Problem.** Under their own IDs, these files define what R-STATE-7, R-OPS-4, R-OPS-5, R-MEAS-8 and R-INT-8 require:
  - a work key that identifies one operation (RJ-1). This is the question of U-CFG-2, a task 3 row at rank 2;
  - "A transport exception is **InDoubt**, not a confirmed failure" (RJ-4);
  - limits that "count settled actual usage plus unresolved reservations" (BA-3);
  - a billing mode, subscription calls or metered USD (BA-5), which R-MEAS-8's "the tokens times their price" does not admit;
  - the results table's reading rules (VT-1 to VT-5).

  Some of these rules are stronger than the draft: RJ-4 and BA-3 answer SA-4's points 2 and 7. Others decide rows that the draft leaves to tasks 3 and 6.
- **Cost of change.**
  - The journal, the budget and the results table each get two sources of truth.
  - Task 3 designs from one source, and the other drifts.
  - Every change to the unit of work then touches two requirement files and two codebases.
- **Fix.**
  - `docs/requirements.md` names the three files and their status: either adopted or superseded.
  - If adopted, each RJ, BA and VT row is traced to the R- requirement it refines, and RJ-4 and BA-3 are folded into R-STATE-7 and R-OPS-4.
  - R-MEAS-8 records a billing mode beside each cost. Task 5 decides the billing.
  - Until then, task 3 treats rank 2 as contested.

### SA-7 · major · Requirement texts decide rows that task 3 owns, and the checker cannot see it

- **Location.** `playground/paper/requirement_coverage.py` lines 264–274 check the *Decides* field only, so the checker cannot see a decision made in a requirement's text. The cases:

| Requirement | States as required | Row it decides: owner, priority |
|---|---|---|
| R-PRIM-2 (02-primitive.md 20–29) | the parameter list | A-NOTE-1: task 3, blocks 1 |
| R-OPS-4, R-OPS-7, R-STATE-7 | a budget guard per session and per task; a retry and timeout policy per unit; resume from the last finished unit | U-TOP-2: task 3, blocks 2 |
| R-STG-6 (03-stages.md 80) | a pruned idea's trace keeps "its verdict, its feedback, its subset results and its code version" | U-CODER-1: task 3, blocks 4 |
| R-STATE-4 (05-state.md 33) | versions are "never edited in place"; C+ "ships the method together with the scripts behind every reported number" | U-ABL-3: task 3, blocks 4 |
| R-OPS-8 (08-operation.md 64) | a sandbox policy per stage | U-ART-15: task 3, blocks 4 |
| R-RUN-2, R-RUN-3 | G is a paper with its code at a commit, and an export can become G | A-TOP-4 and U-TOP-1: task 3, blocks 7 |
| R-OPS-9 | an agent reads everything by default; any cut is a recorded decision | U-EVO-2, U-SEL-2 and U-ABL-6: task 3, later |
| R-INT-3 (06-integrity.md 28) | the test split is scored "after the export" | U-TOP-5: task 6, blocks 3 |

  Each requirement lists its row under *Depends on*, "pending there", while its own text states that row's register proposal as a requirement.
- **Cost of change.**
  - Task 3 cannot tell which of its rows are open.
  - If task 3 decides one of them differently, it contradicts a requirement silently.
  - The fix then touches three places: the requirement, the register and the design.
- **Fix.**
  - For each row, either move it to task 2 and decide it there, or cut the requirement to its testable minimum and mark the rest "the register's proposal, open in task 3". U-CODER-1 and A-TOP-4 ask what, not how, so they suit the first option.
  - List these rows in `docs/requirements.md` as presumed and pending.
  - For R-INT-3, see SA-9.

### SA-8 · major · Access is declared per stage in one requirement and per role in another

- **Location.**
  - `08-operation.md`: R-OPS-8 (64), "declared per stage".
  - `06-integrity.md`: R-INT-9 (81).
  - `04-agents.md`: R-AGT-1 (10), "a tool policy" in each roster entry.
- **Paper.** The filter "uses the Coding Agent", and "the Coding Agent audits the repository" (sections/4_experiment.tex:43). Both checks are therefore coding sessions.
- **Draft.**
  - R-INT-9 makes every judge read-only, "the filter or an auditor" included.
  - R-OPS-8 declares the sandbox policy per stage.
  - R-AGT-1 gives each roster entry its own tool policy.
- **Problem.** A per-stage policy cannot give two sessions of one stage different access.
  - In SUB, the coder and the engineer must write code, while the filter, a session in the same stage, must not.
  - The method–code auditor runs beside the Enhancer, a Claude Code session that edits files.
  - The roster's tool policy and the stage's sandbox policy have no stated precedence.
- **Cost of change.**
  - Rank 4, who may write what, is task 3's next blocking decision after the harness.
  - A sandbox contract built per stage must be redone when the first judge runs as a session.
  - A new agent touches both the roster and every stage's policy.
- **Fix.**
  - One access policy per agent role, as data. It covers read and write sets over named run-state objects, network access, package installs and GPUs.
  - A stage may only narrow a role's policy.
  - The evaluation protocol is read-only in every policy.
  - **Test.** Within SUB, the coder's write succeeds, and the filter's write to the same workspace fails.

### SA-9 · major · The verified results table and the run's tail have no state requirement

- **Location.**
  - `06-integrity.md`: R-INT-3 (28) and R-INT-8 (73).
  - `05-state.md`: R-STATE-5 and R-STATE-6 (52).
  - `03-stages.md`: R-STG-10 (125) and R-STG-12 (144).
  - `07-measurement.md`: R-MEAS-2 (24).
- **Draft: the verified results table.** The Drafter, the Enhancer, the Meta-Reviewer and the export check all read it, and "the harness builds" it (R-INT-8). Nothing says:
  - when it grows: at selection, each ablation pass, each rebuttal cycle, or a promotion;
  - that results the filter discards are excluded;
  - whether its entries refer to result files by ID and hash, or copy the numbers;
  - which table version and code version a manuscript version was written from. R-INT-6's audit and R-INT-8's trace check both need this.
- **Draft: the tail of the run.**
  - R-INT-3 scores the test split "after the export", and R-STATE-6 hashes P+ and makes it read-only at export. So P+ can carry only validation numbers.
  - R-MEAS-2's reported gain, though, comes from the test split.
  - No requirement says that P+ carries validation numbers, or places a step between the last decision and the export.
- **Elsewhere.** Task 6's in-progress draft puts "One test event per run, after the freeze", and then a final fill of the manuscript's numbers, before export (IR-14, IR-17). That is the opposite order to R-INT-3's.
- **Cost of change.**
  - The stage sequence has an unknown last stage.
  - The table is the one object that four stages and the export read. A store designed before its versioning is known will be designed twice.
- **Fix.**
  - Add an R-STATE requirement for the verified results table:
    - only the harness writes it;
    - it is versioned and append-only;
    - its entries cite results by ID and hash;
    - it excludes discarded results and records each discard;
    - each manuscript version records the IDs of its code version and its table version.
  - Replace R-INT-3's "after the export" with "after the last decision that can change code or results".
  - Add a tail step to R-RUN-4: freeze, test scoring, export. Its content is pending U-TOP-5 (task 6), and the table of pending rows lists it.

### SA-10 · major · Three of task 3's five routine changes are not required to touch one component or only data

- **Location.**
  - `04-agents.md`: R-AGT-1 (10), R-AGT-2 (18–22) and R-AGT-4 (34).
  - `08-operation.md`: R-OPS-3 (26).
  - `01-run.md`: R-RUN-2 (15–29).
- **A new model for one stage.**
  - **Problem.**
    - Routing is per agent (R-AGT-2), and three agents serve several stages:
      - A_FullEng serves FULL, ABL and META;
      - the Result Comparison Agent serves ABL and META;
      - the Novelty Checker serves SEED and the re-scoring of R-STG-7 and R-STG-9.
    - Changing the model in one of those stages needs a copied roster entry.
    - The route also has two homes: the entry's "model route" (R-AGT-1) and the routing file (R-AGT-2).
  - **Fix.** Route by stage and agent, falling back to the agent's default, in the routing file only. Each call record names the rule that matched.
  - **Test.** Override A_FullEng's model in META only; the FULL and ABL calls keep the default.
- **A new task.**
  - **Problem.** R-OPS-3 reaches "tasks" through an interface with an adapter, which implies code for each task. No requirement says that a task is data, or that the harness is task-generic.
  - **Fix.** A new task is a manifest plus a read-only task package, holding its evaluation entry points, data roles, rules and result format. The engine and the harness are task-generic.
  - **Test.** A second fixture task, added as data, runs end to end with no code change.
- **A new agent.**
  - **Problem.** R-AGT-1 lists "inputs" and "outputs", but does not require them to be references to named run-state objects that generic code resolves. Without that, each agent brings its own context assembly, in code.
  - **Fix.** Each roster entry names its inputs as references and its output's destination.
  - **Test.** Extend R-AGT-1's toy-agent test: the toy agent reads an existing state object (the traces) and writes a declared record, with no code change.
  - Access is covered by SA-8.
- **A new coding backend** is already close to one component: one adapter (R-AGT-4, R-OPS-3).
  - **Problem.** The register's U-CFG-1 names "Claude Code's tools, permissions and turn limits". These must not land in stage data.
  - **Fix.** Stage configurations and roster entries hold engine-level session settings only, and the adapter translates them.
  - **Test.** A static check finds no backend-specific key outside the adapter's own configuration.
- **Cost of change.** These are TODO task 3's done-when. Unless the requirements ask for them, task 3's design can pass its review without them.

### SA-11 · major · Several tests would pass on a broken engine

| Requirement and test | Why a wrong engine passes | A test that can fail (proposal) |
|---|---|---|
| R-PRIM-1 (line 16): a toy stage runs from a configuration file | an engine with eleven hand-written stage loops beside one generic path passes | every stage of the default configuration, A_Coder and the run sequence load from data and run through the one primitive; changing a stage's limit, verdict map or at-limit value in data changes its recorded calls; a static check finds no stage name in engine code |
| R-PRIM-8 (80): fan-out order | nesting, half the requirement, has no test | A_Coder nested in EVO's fan-out and the downstream pass nested in META, both from data, give the call counts of R-STG-7 and R-STG-12 |
| R-PRIM-9 (94): replaying the records rebuilds the control path | rebuilding a sequence from records that list that sequence is circular | re-execute with a mock that answers every agent call from the records: the same stage records, and no call left unanswered |
| R-OPS-6 (52): re-run from the record | in mock mode the re-run reads the same files from disk | edit every configuration file after the run; the re-run still reproduces, using the versions the record names |
| R-AGT-2 (22) and R-AGT-7 (59): "is a one-line change", "is a configuration change" | a property of a file, not something a run checks | apply the one-line change; the next mock run's records show the new model or drafting system, for that agent only |
| R-AGT-9 (79): golden sets against the mock judge | a scripted mock passes by construction | a pass rule per golden set for the real model, recorded with its n and date; the mock run checks only that the sets run |
| R-STG-12 (150–154): "with fresh counters" | no listed case observes a reset | script a `Refine` from the Ablation Critic in the second pass: one more A_FullEng call follows |
| R-RUN-1 (11): P+ addresses a bottleneck, and C+ shows a measurable gain | neither clause is tested | test the gain through the harness (the export's validation gain over the reproduced baseline exceeds the margin), or move both clauses to R-MEAS as measured quantities |

- **Cost of change.** A green test suite that cannot see stage-specific code is how a monolith ships. R-PRIM-1's test is the one that should see it.

### SA-12 · major · The enforcement tests run against mocks of the enforcement

- **Location.**
  - `docs/requirements.md` line 26: "a mock harness that returns fixture results".
  - `08-operation.md` R-OPS-1 (11), which mocks "the sandbox and the harness".
  - The tests of R-STATE-1 (13), R-INT-1 (16), R-INT-2 (24), R-INT-9 (85) and R-OPS-8 (68).
- **Problem.** These tests run "in mock mode".
  - A permission error raised by a mock sandbox proves nothing about the real one.
  - With a harness that returns fixtures, R-INT-1's fabricated-score test passes even if the real harness reads the agent's own results file.
  - CLAUDE.md enforces integrity "by the setup", and no test exercises the setup.
- **Cost of change.** A later change to the sandbox or the harness adapter can switch enforcement off while every test stays green.
- **Fix.** Name two test tiers in `docs/requirements.md`:
  - **Logic tests** mock everything, and check control flow and counts.
  - **Enforcement tests** mock only the agents and the paid services. The sandbox, file permissions, hashing and the harness run for real, on a toy CPU task.
  - The five tests above run in the second tier. R-OPS-1 keeps the sandbox and the harness mockable for the first tier only.

### SA-13 · minor · One margin serves three gates

- **Location.** R-STG-4 (03-stages.md 62), R-STG-8 (97) and R-PRIM-6 (02-primitive.md 62). Each reads "the task's margin" from R-RUN-2's comparison rule.
- **Cost of change.** The gates have different needs: subset noise differs from full-set noise, and a near-tie band differs from a promotion threshold. A different value for one gate is a manifest schema change plus code. Task 6's in-progress IR-7 already asks for a rule "per gate".
- **Fix.** One named rule per gate in the configuration, each defaulting to the manifest's margin.

### SA-14 · minor · The limitation stage's default runs 17 extraction rounds, against App. A.2's 16

- **Location.** R-STG-1's test (03-stages.md 40): "17 Extractor calls, 17 Verifier calls". R-PRIM-3's *Why ours* (02-primitive.md 38).
- **Paper.** "We extract limitations for a maximum of 16 rounds" (sections/appendix.tex:155). The register's D-4 verdict: "the limitation loop and the peer-review loop count rounds" (unspecified.md 289).
- **Problem.** R-PRIM-3's reasons cover the three limits stated as refinements, Table 5 and Figure 9; none covers the limitation loop. R-STG-1's *Why ours* does not record the departure.
- **Cost of change.** One value.
- **Fix.** Either set 16 extraction rounds (15 judged refinements), or record the departure.

### SA-15 · minor · U-EVO-3 has two mechanisms, and one of them can never run

- **Location.** R-STG-2 (03-stages.md 44) refuses at load an N_seed below N_0 + K·N_e. R-STG-7 (88) runs "the evolved idea alone" once the seeds run out.
- **Problem.**
  - Under the load check, the runtime branch is unreachable, and no test covers it.
  - The check is itself a rule across two stages' parameters (SEED's N_seed against EVO's N_0, K and N_e), which makes it a stage-specific validation.
- **Cost of change.** A change to K or N_e also forces a change to N_seed and to the cross-stage rule.
- **Fix.** Keep only one mechanism:
  - the runtime branch, as data (EVO's draw takes what is left), with a test; or
  - the load check, written as a declared constraint between named parameters.

### SA-16 · minor · "One directory" designs the store

- **Location.** R-STATE-8 (05-state.md 67): "Every file a record names is inside it".
- **Problem.** This rules out a content-addressed store shared across runs, which chained runs (R-RUN-3) could use to reuse C_base and datasets. That choice belongs to task 3 (U-ART-10).
- **Fix.** "Every artifact a record names resolves from the run's record by ID and hash."

### SA-17 · minor · Five records are each required to hold the same facts about a unit of work

- **Location.** Five requirements ask for part of the same facts:
  - R-PRIM-9: the stage records;
  - R-OPS-5: the log;
  - R-MEAS-8: the ledger;
  - R-STATE-7: the resume record;
  - R-OPS-6: the reproduction record.

  R-OPS-5's test compares three of them.
- **Cost of change.** A new field on a unit of work has five writers.
- **Fix.** Require one record per unit of work as the single source. The stage records, the ledger and queries are computed from it, and the five tests read it.

## The five routine changes (question 2)

| Change | What the draft requires it to touch | One component, or only data? | What is missing | Finding |
|---|---|---|---|---|
| A new reasoning agent | a roster entry, a prompt, a schema, a routing line, and the stage configuration that names it; a golden set if it judges | only data, except its context assembly and its access, which are not required to be data | inputs as named references; one home for access | SA-10, SA-8 |
| A new coding backend | one adapter with its mock and contract tests; one routing value | one component, provided no backend setting leaks into stage data | engine-level session settings only, in stage and roster data | SA-10 |
| A new task | a manifest (R-RUN-2); by R-OPS-3, also a task adapter; the harness's per-task part is unstated | not required; possibly two components, the task adapter and the harness | a task as a manifest and a package; a task-generic harness; a test | SA-10 |
| A new loop limit | one cell of the stage table, for the eleven rows (R-OPS-2's test) | only data, for those rows | limits on the loops outside the primitive (the repairs, and DRAFT's compile repair); counter scope; the cross-stage seed rule | SA-1, SA-3, SA-15 |
| A new model for one stage | the agent's routing line, which moves every stage that agent serves | no, for A_FullEng (3 stages), the Result Comparison Agent (2) and the Novelty Checker (3) | routing by stage and agent | SA-10 |

## The five questions, answered by finding

1. **One primitive as data:** SA-1 (its behaviour table), SA-2 and SA-3.
2. **Change cost:** the table above, SA-10 and SA-8.
3. **Testability:** SA-11 and SA-12, and the tests inside SA-4 and SA-5.
4. **Boundary with task 3:** SA-7, SA-6 and SA-16, and the ranks below.
5. **Contradictions and gaps:** SA-2, SA-4, SA-5, SA-8, SA-9, SA-13, SA-14 and SA-15.

## What task 3 needs, rank by rank

| Rank | What task 3 needs first | Does the draft provide it? | Findings |
|---|---|---|---|
| 1 | the primitive's parameters | no: the parameter list contradicts the table, and composition and hooks are missing | SA-1, SA-2, SA-3, SA-11 |
| 2 | the unit of work, and what happens when it fails | partly: no harness jobs, no in-doubt state, two failure rules that contradict each other, and a second home in code | SA-4, SA-5, SA-6 |
| 3 | who produces the results, and on which data | this is task 6's, still uncommitted; R-INT-3 pre-decides its timing | SA-7, SA-9, SA-12 |
| 4 | code versions, and who may write them | contradictory: per stage against per role, and three task 3 rows are presumed | SA-8, SA-7 |
| 5 | the shape of the stage graph | no: the order is not data, and the tail is unknown | SA-2, SA-9 |
| 6 | restarts, and whether counters reset | contradictory: three mechanisms, and no counter scope | SA-2, SA-1 |
| 7 | what a task contains | partly: the manifest's fields hold; a new task is not required to be data; one margin serves three gates | SA-10, SA-13, SA-7 |
| 8 | where the integrity checks hook in | no: no hook points, and the repair loops are unbounded | SA-3 |

## Verdict

- **Task 3 cannot start rank 1 from this draft.** Its first decision is the primitive's parameters.
  - Three parts of the draft define them: R-PRIM-2's list, R-PRIM-4's four values and R-PRIM-8's nesting rule.
  - Together they cannot express EVO, SEL, the vetoes, A_Coder, the rebuttal cycle or the downstream pass, all of which the draft's own table and stage requirements require.
  - So R-PRIM-1 cannot be met, and its test would not notice.
- **What must change first, in this order:**
  1. **SA-1.**
     - Make the parameter lists a floor.
     - Hand their design to A-NOTE-1, with the behaviour table as its acceptance cases.
     - Merge R-PRIM-2's and R-PRIM-7's assessor kinds, and rewrite the out-of-domain cells.
  2. **SA-2.** State the meta restart once, make the run's sequence data, and have each stage declare its own outcomes.
  3. **SA-11's first row.** Replace R-PRIM-1's test with the conformance test.

  Together these are a few hundred words of requirement text, not a redesign.
- **Before task 3 closes rank 2:** SA-4, SA-5 and SA-6. The status of the Codex journal and budget work is for the coordinating session to decide, not task 3.
- **The rest** (SA-3, SA-7 to SA-10, and SA-12 to SA-17) can land in the same revision. Each must land before task 3 closes the rank that the table above names for it.
- **What task 3 can start now:** the LLM-provider and coding-backend interfaces with their mocks (R-AGT-4, R-OPS-3). No finding touches them beyond SA-10's note on backend settings.
- **Still blocked:** the harness and audit contracts, which wait on task 6's four decisions. On 2026-10-02 those decisions are drafted but uncommitted.
