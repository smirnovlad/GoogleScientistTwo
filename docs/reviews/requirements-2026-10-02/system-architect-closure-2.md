# Closure check of the third revision (fd9bcf9), system-architect lens

I checked commit fd9bcf9 in read-only mode. All paths below are relative to the repository root.

**What I read:**
- Task 6's rules at adc3484: `git show adc3484:docs/integrity/blocking-decisions.md`, cited as `bd.md:line`.
- The engine branch:
  - `claude/engine` is local only, at **c1850a5** (2026-10-02 16:33). That is newer than the cba39df that `requirements.md:149` says it read.
  - `origin/claude/engine` is still at 7e3f0c3.
  - I cite c1850a5's files as `engine.md:line` and `orchestrator.py:line`.

**The checker:** `python3 -B playground/paper/requirement_coverage.py` ends with `0 problem(s)`. It checks the stage-table keys (`requirement_coverage.py:94`) but not the table of failures after retries. `git status --porcelain` was empty, and I edited nothing.

## 1. Status of the eight findings

| ID | Status | Evidence | What remains |
|---|---|---|---|
| NEW-1 · outcome vocabulary, failure values | **partly closed** | One vocabulary at `02-primitive.md:38`. A table of failures after retries at `03-stages.md:37-61`, which R-PRIM-10 points to (`02-primitive.md:120`). The re-run count is now a value (`03-stages.md:230`). A failed Selector keeps the band's leader (`03-stages.md:52`) | (a) Three judges have no row in the table: the Subset Critic, the Full-Set Critic and the Result Comparison Agent (which still runs in the paper profile, `02-primitive.md:81`). R-PRIM-10's test expects a critic to take "its configured branch" (`02-primitive.md:128`), and A_Coder's two critics have none. (b) Nothing refuses to load a role that has no row: neither R-STG-13's test (`03-stages.md:235`) nor the checker. A new agent's failure value is therefore still decided in code. (c) R-INT-10 keeps its own four-word list, "reject the candidate, fail a refinement into its guard's failure branch, drop an item, or repair" (`06-integrity.md:122`), and "repair" is not in the vocabulary. Several cells of the table describe effects ("as a `Refine` that cannot be acted on", "the round runs its seed alone", `03-stages.md:51,55`) instead of naming a vocabulary term |
| NEW-2 · `Reject` against R-STATE-3; the meta case | **closed** (one leftover moved to N3-1) | R-STATE-3 now allows a restore, with an audit row, and refuses a restore to a state never held (`05-state.md:30,33`). R-PRIM-5 has the restore and its test (`02-primitive.md:75,77`). The meta case has its branch (`03-stages.md:163,215`) and a test (`03-stages.md:224`). The two tests no longer contradict each other | How the restore travels from the ablation stage to the stage that made the promotion (N3-1) |
| NEW-3 · two meanings of "unit of work"; harness failures unclassified | **partly closed** | R-STATE-7 now says "A unit of work is a leaf … A stage, a pass or a run is a composite" (`05-state.md:63`). Harness failures are classified: agent code gives a released result, and a machine failure is retried under the same identity, then suspends the run (`02-primitive.md:121-122`; `08-operation.md:61-63`; `05-state.md:65`) | R-OPS-5 still reads "Each unit of work, a stage, an agent call, a coding session, a harness job (U-INT-4) or a run, has one record" (`08-operation.md:44`). Two definitions therefore still stand. One-line fix: "each unit of work and each composite has one record" |
| NEW-4 · budget stop against resume and a single outcome | **closed** | One suspended state, with its reasons (`01-run.md:124`). "An outcome is final … A suspended run has not ended" (`01-run.md:76`). A raise is an amendment, made under a rule fixed before admission (`01-run.md:124`; `08-operation.md:36`). Amendments get audit rows (`05-state.md:30`). The tests are at `01-run.md:81,130` and `08-operation.md:40` | Two of the five reasons for suspension have nothing that lifts them (N3-2) |
| NEW-5 · task 6's review moves rank-1 rows | **partly closed** | The requirements cite adc3484 (`06-integrity.md:8`). BASE runs at admission with task scope (`03-stages.md:25,85,97`). Each stage declares its scope (`01-run.md:48-49`). *Baseline not reproduced* means the task is not admitted (`01-run.md:71`). The gates are R-INT-10's filters, to which a stage may add and never remove (`06-integrity.md:118`; `02-primitive.md:35`) | The unit key is still "derived from its place in the run: stage path, pass, round, item and attempt" (`05-state.md:63`). BASE's agent call and its fits happen before any run exists, and two runs share them (the test at `03-stages.md:97`), so a key from a place in the run cannot name them. Harness jobs also carry IR-32.1's content identity (scope, key, manifest hash, row, code hash, arguments, seed, setting; no attempt; `bd.md:113`), and the requirements never say how the two keys relate. My proposal 3 was not taken. It decides the shape of the rank-2 journal |
| NEW-6 · the engine's contract is a second home | **partly closed** | The contracts table now maps `claude/engine`, and *The engine as built* lists departures (`requirements.md:143-157`) | See the details below the table |
| SA-4 · resume, units, in-doubt units | **partly closed** | In-doubt units now have a bound (`05-state.md:66`). Resume reads the record and its amendments (`05-state.md:68`; `01-run.md:124`) | NEW-3's line in R-OPS-5, NEW-5's key, and N3-2 |
| SA-11 · tests that pass on a broken engine | **closed** | R-STG-12's test now spends N_abl and N_peer in pass one before checking the reset (`03-stages.md:223`). R-PRIM-8's test names no mechanism (`02-primitive.md:101`). The static check covers CODER and TAIL (`02-primitive.md:19`) | Nothing |

**What remains for NEW-6:**
- **The reading is out of date.** It was made "against cba39df and its uncommitted fixes" (`requirements.md:149`), and the branch has since moved to c1850a5.
- **The departures are undercounted.** The table records one departure, and `requirements.md:221` tells task 3 to start "from the engine as built, whose one departure is listed above". At c1850a5 I find at least these further departures:
  - **R-RUN-5's finality.**
    - The engine's end states include "`error` (resumable)" (`orchestrator.py:13`).
    - "A unit failure that stopped the run is cleared, so the resume tries it again" (`engine.md:350-354`).
    - `baseline_failed` is a state of the run, not a refusal at admission.
    - The engine has no *abandoned*, no *integrity halt*, no *manuscript gate failed* and no *test event done, not exported*.
  - **R-STG-9.** "`Reject` ends the run" (`engine.md:308`). Only the meta restart is handled (`:319`), and there is no restore after a promotion inside the same pass. The table's row calling this "aligned" is half true.
  - **R-OPS-4 and R-MEAS-8.** The engine caps "per run … equivalent USD" (`engine.md:54`). The requirements ask for a budget per session and per task, in named resources, with dollars only for metered charges.
  - **R-AGT-4.** `agent.json` holds "kind, tools" (`engine.md:251`).
  - **R-OPS-7 and R-PRIM-10.** A transient error is "retried twice with backoff, then the run pauses" (`engine.md:106-108`). The requirements route it through the table of failures for its role.
  - **R-PRIM-2.** The engine's primitive is "generator, critic, refiner, verdict map, guard, limit, exhaustion policy" and returns "the kept candidate, or `None`" (`engine.md:60,122-140`). It has no precondition, no vocabulary of outcomes and no restore. The table's one departure row covers only the seed and evolution loops.
- **Cost:** task 3 starts from a design it is told has one gap, and has six or more.

## 2. New defects at blocker or major level

### N3-1 · major · The vocabulary of outcomes does not combine with the restore or with suspension, so each needs a second code path

**Suspension is listed as something a stage ends in.**
- "a stage ends in one of the primitive's own outcomes … or the run suspended (R-RUN-8)" (`02-primitive.md:38`), and the test checks that "each stage's record ends in one outcome of the vocabulary" (`:42`).
- But a suspended run "has not ended" (`01-run.md:76`), and it resumes by replaying units from their records (`05-state.md:63-68`).
- If a stage's record ends in *suspended*, which R-STATE-5 then fixes, resuming needs a path that reopens the stage. Replay alone needs no such path.
- **Fix:** suspension is an interruption, not an outcome. A suspended stage has no record that ends it, and its record is derived from its units' records (`05-state.md:63`).

**The restore has no outcome that reaches the stage that made the promotion.**
- The ABL cell maps one verdict onto outcomes that depend on run state: "`Reject` → stop the run, *ablation reject*, or restore the candidate kept before a promotion" (`03-stages.md:31`).
- R-PRIM-2 maps a verdict onto *an* outcome (`02-primitive.md:29`).
- In the meta case, the ablation stage's `Reject` must skip drafting, peer review and the meta-review of pass k, and send pass k−1's outputs to the tail (`03-stages.md:163,215`). The vocabulary has no term that tells META its promotion was undone, so the build would put code in the ablation stage that reaches into META.
- **One rule covers both cases, and I checked it against the table.** A `Reject` of a candidate whose promotion is still open restores the state from before that promotion. It then ends the promoting stage in that stage's own guard-failure branch:
  - inside the same pass, the promoting stage is ABL, whose branch is "drafting with the unchanged h_best" (`03-stages.md:31`);
  - in the meta case, it is META, whose branch is "the tail with the previous outputs, unapproved" (`03-stages.md:34`). That matches R-STG-12 (`03-stages.md:215`).
- **Fix:** add *promotion undone* to the vocabulary, carried up through nested stages to the stage that made the promotion. The ABL cell then reads "`Reject` → *promotion undone* if a promotion is open, else stop the run, *ablation reject*". This fixes how rank 1 binds the kept candidate.

### N3-2 · major · Two of the five reasons for suspension have nothing that lifts them, and time bounds are classified three ways

**The lift conditions.**
- R-RUN-8 suspends a run for a budget, a wall-clock bound, a usage window, a billing check, or an infrastructure failure that outlasts its retries (`01-run.md:124`).
- What lifts a suspension is stated for three of the five:
  - the budget: a raise under the rule (`08-operation.md:36`);
  - the usage window: its reset (`08-operation.md:108`);
  - billing: the environment is fixed (`08-operation.md:108`).
- Nothing is stated for the wall-clock bound or for exhausted infrastructure retries. The tests stop at "suspends the run" (`02-primitive.md:130`; `05-state.md:74`).

**Exhausted retries cannot be raised by data.**
- The attempt bound is the manifest's (IR-33.3, `bd.md:118`; `03-stages.md:230`).
- The manifest's hash is part of every identity in run scope (`bd.md:113`).
- So raising the bound in the manifest re-keys every job. Leaving it unchanged makes the resume suspend again at once.

**Time bounds are classified three ways.**
- A job's time limit is the manifest's, and running past it is a released failure (IR-33.4, `bd.md:119`; `02-primitive.md:121`).
- The compute envelope "stops a job … and the row has no result" (`01-run.md:26`).
- A harness job's wall-clock bound "is stopped and recorded" (`08-operation.md:60,69`), and a wall-clock bound suspends the run (`01-run.md:124`).
- If the harness job's bound counts as a suspension, a job that always overruns loops: resume, the same identity, overrun, suspend again. A multi-day run never finishes and never ends.

**Fix:** one small table. For each bound, give its owner and its class:
- job-level limits are released results of the row;
- the run's and the task's wall-clock bounds suspend.

For each reason for suspension, give the event that lifts it. Wall-clock bounds and attempt bounds are copied into the run's record at admission, so an amendment can raise them without changing the manifest's hash.

### N3-3 · major · A re-run of one item spends its parent stage's refinement, so a limit counts two things across a nesting boundary

**The conflict.**
- "a discarded ablation or rebuttal item is re-run once by a fresh session, which uses up a refinement of its stage (IR-40.1)" (`06-integrity.md:58`; `bd.md:212`).
- But R-PRIM-3 says "a limit N counts refinements, and every refinement is judged" (`02-primitive.md:49`), and R-PRIM-2 gives a limit "what it counts … and its scope" (`02-primitive.md:32`).
- The same re-run after an agent failure spends nothing (`03-stages.md:54`).

**What it costs.**
- A fan-out item nested inside the ablation or peer stage writes to its parent's counter.
- With N_abl = 1, a single filter discard of one plan removes the A_FullEng refinement, and a test that never mentions it changes outcome.
- This is rank 1's decision on the shape of the counter.

**Fix:** choose one of these.
- (a) A limit counts a set of events declared in data, which may include a nested item's re-runs. Apply it to the row at `03-stages.md:54` too, and make R-PRIM-3 say so.
- (b) An item's re-runs are bounded only by R-STG-13's "1 re-run by a fresh session". Ask task 6 to narrow IR-40.1 to the candidate's own refinements.

## 3. Verdict

Task 3 can start rank 1 now, with one condition: first correct the engine's departures, because task 3 is told to start from `engine.md` (`requirements.md:221`).
- **Before rank 1 starts:** re-read *The engine as built* against c1850a5 and list the six or more departures above, the primitive's narrow set of parameters among them. Then remove "whose one departure" from `requirements.md:221`. This is a short documentation edit.
- **Before rank 1 closes:**
  - N3-1: take *suspended* out of the stage vocabulary and add *promotion undone*;
  - N3-3: decide what a limit counts across nesting;
  - NEW-1's remainder: rows for the Subset Critic, the Full-Set Critic and the Result Comparison Agent, a check at load time that every role a stage names has a failure value, and R-INT-10 citing the vocabulary.
- **Before rank 2:**
  - NEW-3's one line in R-OPS-5;
  - NEW-5's key, scoped to task, run or audit, with a harness job keyed by IR-32.1's identity;
  - N3-2's table of bounds and of what lifts each suspension.

None of these is a blocker. Each is a few sentences of requirement text.
