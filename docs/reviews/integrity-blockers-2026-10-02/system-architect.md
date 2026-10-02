# Record: `system-architect` review, wave 1 (2026-10-02)

- **Reviewed:** `docs/integrity/blocking-decisions.md` at commit `a2e7eb0`, against its brief,
  `docs/integrity/README.md`.
- **Lens:** what does the next change cost, and does a crashed multi-day run resume?
- **Record:** the reviewer's final message, verbatim below, unchanged. It names scratchpad
  scripts by file name only; those that a fix cites are copied into `playground/integrity/`.

---

# Review: system-architect, `docs/integrity/blocking-decisions.md` at a2e7eb0

**Lens:** what the next change costs, and whether a crashed multi-day run resumes.

**What I read:**
- The brief, `docs/integrity/README.md`, and the document itself.
- `CLAUDE.md`, and TODO task 3.
- `docs/paper/analysis.md`, sections 3.1–3.5, 4–4.3, 8, 9 and 10.1.
- `docs/paper/stages/07-integrity.md`.
- The register rows in `docs/paper/unspecified.md`, with its "How to read a row" convention.
- My task-1 review and its closure check.
- The paper's TeX: §3.2–§3.6, §4.2 with fn. 2, App. A.2, App. B with Tables 15–16, Table 7 and Listing 1. Also p. 62 of the PDF text.
- ScientistOne's `05_coe_audit.tex`, `06a_setup.tex`, `06b_integrity.tex` and `04.5_system_claim_writer.tex`.

## 1. Verdict

The document is not yet ready for task 3, for one reason, and that reason is cheap to fix. The rules count harness jobs and events, not released results, and they define no way to resume. So a crash in the test event, in a search scoring or in the audit cannot be told apart from a second use (B1).

Once B1 and seven MAJOR findings are fixed (most need a sentence or two each), task 3 can write the harness and audit contracts from these rules. Their core is sound:
- the harness computes every number;
- scoring is independent of the coding backend;
- one read table covers every kind of job;
- three layers, with a separate writer for each.

## 2. Requirements R2, R8, R10

**R2: partly met.**
- **Met:** the IDs are stable (IR-1 to IR-31, G1 to G7), and no rule says only "should" or "ensure".
- **Gap (a), bundled clauses:** several IDs each hold 5 to 8 invariants (IR-3, IR-5, IR-6, IR-11, IR-14, IR-18, IR-29), so task 2 cannot cite one clause with one test.
- **Gap (b), duplicate IDs:** G1, G6 and G7 restate IR-6, IR-14 and IR-17 under a second ID.
- **Gap (c), clauses about people:** a few clauses bind people and the setup cannot check them: "seen its verdicts", "written apart", "no prompt was developed on".
- **Gap (d), tensions between rules:**

| # | Rule against rule | Fixed in |
|---|---|---|
| T1 | IR-14 "except the baseline" against IR-8 (a) "the baseline included" | M1 |
| T2 | IR-13's cap and IR-24 (e) against G2's retry ("the author gets the rule ID") | M2 |
| T3 | IR-21 "the task ends without export" against §3.6 U-INT-1 "whether the idea becomes `Bad` or the task ends is task 2's" | M2 |
| T4 | IR-14, IR-20 and IR-24 (b) against `CLAUDE.md`'s resume rule and the register's U-TOP-2 decision | B1 |
| T5 | IR-15 "Every attempt is a ledger entry" against IR-14 "once per task … The harness refuses any other" | B1 |
| T6 | IR-18's retry after an infrastructure failure against IR-20, where a hash mismatch is an integrity failure | B1 |
| T7 | IR-5 and IR-14 (the audit re-run is a harness record, counted in the run's ledger) against IR-29 and IR-30 | M4 |
| T8 | IR-26: the author includes the fixer, yet "no session holds two roles" | m2 |
| T9 | IR-17 "no decision with a branch runs" against G4 and G5, which block export after the final fill | m3 |
| T10 | Table 2.2 and §2.7 "its rows enter the freeze" against §2.8 "the cited rebuttal rows" | M1 |
| T11 | IR-1 "Every number that a decision in the loop reads" against ScholarPeer's score tested against 8, and the novelty sort | m3 |
| T12 | The Terms entry, ledger = "the run's", against the per-task events of IR-4 and IR-15 | M3 |

**R8: partly met.**
- **Met:** most rules state guarantees and leave components open, and no rule adds a component that the paper and our requirements do not need.
- **Not met, things task 3 would have to decide again:** before it can write the harness's failure modes or the audit contract, task 3 would have to re-decide four questions that belong to these rows:
  - what one "use" of the report split is when a job crashes (B1);
  - what the freeze holds, and which row is *ours* (M1);
  - which events are per task, and where they are recorded (M3);
  - which identity an audit re-run runs under, and which store it writes to (M4).
- **Not met, mechanisms fixed without need:** G3's insertion by engine code (m5), and the toy task's make-up, which belongs to task 7 (M6).

The five routine changes, under these rules as written:

| Change | What it touches | Verdict |
|---|---|---|
| A new reasoning agent | its prompt, schema and routing entry; if it gates on performance, a numeric precondition (IR-7, form not set); if it is an LLM check, an IR-31 measurement for its configuration | one data folder, once IR-7's precondition is declared as data (m6) |
| A new coding backend | the backend adapter and its routing; the IR-29 family check; for IR-31, new corpus items written by the new author model, and every LLM check measured again | one component plus data. Scoring is untouched, thanks to IR-2 and IR-3. |
| A new research task | the task package (manifest, roles, index files, labels, scoring items, baseline diff, rules, image), plus the admission jobs of IR-10 and IR-15 | one data folder, only if the scoring runner is engine code (M5) and admission runs the per-task jobs (M3) |
| A different loop limit | one value; IR-13's cap derives from it | under IR-18, the new runs join the old per-task aggregate, and the freeze of a final-test task does not cover limits (M7) |
| A new model for one stage | one routing value; the IR-29 family flag; an IR-31 re-measurement if the stage writes or checks | IR-29 can retire the reporting auditor, and that cost is not recorded (m4) |

The stores the rules name:

| Store | Who writes | Who reads | Consistent? |
|---|---|---|---|
| result records | the harness only (IR-5) | engine code, which hands search records to sessions; the verified-table renderer; the audit (IR-24 c); the reporter | no: the audit's re-runs are written here (M4), and the baseline's records have no run (M3) |
| ledger | engine code and the harness | engine code; G2, through engine code; the audit | no: it is defined per run but counts per-task events (M3), and it counts the audit's own jobs (M4) |
| freeze record | engine code | the harness, the final fill, the audit | its row set and the rule for *ours* are not stated (M1) |
| audit store | the audit's identity only | "the reporter", which is never defined | yes, apart from m8 |
| run registry | not named | the reporter | its key is not stated (M7) |

**Can the engine run end to end in mock mode for $0?** Yes, for LLM spend, but only if "mock" means scripted agents running over the production setup. M6 covers this.

**R10: partly met.**
- **Met:** 419 lines by `wc -l`, under the 600 cap, and a table for every control, gate and role.
- **Not met:** the document adds a tail after the meta-review: the freeze, the test event, the final fill, G3 to G5, and export. That tail is prose scattered over IR-14, IR-17, IR-21 and IR-22. It has no pseudocode and no failure branch for any step. `CLAUDE.md` asks for both: "Give pseudocode … and the failure branch of every step." The fixes below add about 80 lines and stay under the cap.

## 3. Findings

### BLOCKER

**B1 · IR-13, IR-14, IR-15, IR-18, IR-20, IR-22 and IR-24 (b)(e): uses are counted as jobs, and nothing resumes.**

**The problem.** The rules count jobs and events. IR-14 says "The harness refuses any other, and the ledger counts them". IR-24 requires "(b) exactly one test event" and "(e) each candidate's search scorings stay within its limits". IR-22 says the audit "runs once per exported task". IR-18 says "a retry after an infrastructure failure is allowed only for a run that never reached its freeze". IR-20 halts the run as an integrity failure on "a report job outside IR-14".

The document never uses the words crash, resume or idempotent. "Attempt" appears only in IR-15 and in a quote from ScientistOne.

**What a crash leads to.** Say a node dies halfway through the test event. The rules define two outcomes, and both are wrong:
- Re-scoring the unfinished rows is a further report job. IR-20 then halts the run as an integrity failure, which stays in every denominator.
- Not re-scoring them means "a run that ended without a test event counts as a failure".

The same holds elsewhere:
- **A search scoring that dies:** its retry pushes the ledger's count past IR-13's cap, and IR-24 (e) then fails the task's integrity.
- **The audit:** it is either run a second time, or left unfinished.

So, under these rules a crash cannot be told from a second use.

**What it contradicts.** `CLAUDE.md` says "a crash resumes from the last finished stage. A retry never spends twice for the same work". The register's U-TOP-2 decision says "resume from the last finished unit". Yet §3.6 constrains U-TOP-2 only with failure reasons.

**Three more problems.**
- **(a) A restart is a re-roll.** IR-18's "retry" follows ScientistOne's practice of runs "re-attempted with fresh state" (`.cache/refs/2605.26340v1/src/sections/06a_setup.tex:29`). Whoever chooses which failed runs to restart can see their search trajectory. So "the best of several runs" (§2.3) is stopped only for report numbers.
- **(b) Inconsistent attempt rules.** IR-15 already records and reports every attempt, but IR-14 refuses any second attempt (T5).
- **(c) A fault reads as tampering.** A corrupted read or a torn append is a hash mismatch, and so an integrity failure under IR-6 and IR-20, while IR-18 treats infrastructure faults as retryable. Nobody is named to classify which it was (T6).

**What it makes expensive:** every infrastructure fault after the freeze. That costs the whole multi-day run, and the run is reported as a failure or as cheating. The audit re-fits every reported row (IR-23), and it has no restart rule either.

**The fix, as rules:**
1. **Every harness job and every gate verdict has an identity.**
   - A job's identity: the event kind, its scope (task, run or audit), the manifest hash, the freeze hash where there is one, the row, the seed and the setting.
   - A verdict's identity: the check, the hashes of its inputs, and its configuration hash.
   - A *use* is a released result, meaning a record the harness has written. At most one result is released per identity.
   - Asking again for an identity that already has a result returns that result.
2. **An attempt that ends without a released result is re-run.** Such attempts are a runner crash, a preemption or a torn write. The re-run uses the same identity and the same frozen artifact, and every attempt is logged with its cause.
   - What agent code produces (an invalid output, a failure, a timeout against the manifest's limit) is a released result, and is never re-run.
   - The manifest bounds the attempts per identity. At the bound, the identity is released as failed.
   - The harness writes no value anywhere before it writes the record.
3. **IR-13, IR-14, IR-15 and IR-24 (b)(e) count released results per identity,** and report the attempts beside them.
4. **IR-18: an infrastructure failure resumes the run from its last finished stage,** before or after the freeze, with the same run ID, state and seeds.
   - No registered run restarts with fresh state.
   - A fresh start is a new registered run. The old one stays in the denominator as a failure, with its cause.
5. **IR-6 and IR-20: a halt records which class of cause it had.**
   - **Integrity:** a write by an agent identity, or a mismatch that the write log does not explain. This halt is terminal.
   - **Infrastructure:** the item verifies again from its pinned source and no agent identity wrote it, or an append was torn. This halt resumes.
   - Add the line: ⛔ WHY NOT treat every mismatch as integrity: then a disk fault costs a run and counts as cheating. Or keep that rule, and record what it costs.
6. **IR-22: the audit's identity is (bundle hash, configuration hash).**
   - Its units (check × row × re-run) are released once, and resume after a crash.
   - An audit run under a new configuration, after anyone has seen its verdicts, is reported beside the first audit, never in its place. IR-25 already applies this rule to a person's review.

**Control:** mock LLM, the real harness, $0. Kill the harness halfway through the toy task's test event.
- With the rule removed, the run halts as an integrity failure, or ends without a test event.
- With the rule in place, each frozen identity has exactly one released result, the attempt log shows the kill, and asking again for a released identity returns the same record.

### MAJOR

**M1 · IR-14, IR-8 (a), Table 2.2, §2.7 and §2.8: what the freeze holds, and which row is *ours*.**

**The problem:**
- **(a) Which row is *ours*.** IR-14 binds "the role *ours*, bound to one row", but does not say which row. The attack that §2.3 claims to stop is ScientistOne's writer, which "selects the most favorable score from ablation-stage nodes rather than the score of the node whose code is used as the final solution". It is stopped only if *ours* is the row whose code is exported as C+. Nothing says so, and the IR-14 control tests rebinding after the test event, not the choice made at the freeze.
- **(b) Which rows the freeze lists.** This is not stated either, and two places disagree (T10): "its rows enter the freeze" (§2.2, §2.7) against "the cited rebuttal rows" (§2.8). If only cited rows are frozen, the writer's choice of what to cite decides what gets test-scored.
- **(c) The baseline in the test event (T1).** For a time metric, IR-8 (a) requires the baseline to be timed in the same job as the rows it is compared with. IR-14 skips the baseline in the test event. And IR-15's sealed time is not comparable with a time measured in another job.

**What it makes expensive:** the contract of the freeze record, the cost of the test event, and the IR-24 (c) check. All three wait for task 3 to settle a question that belongs to U-TOP-5.

**The fix:**
- **Who is *ours*:** "*ours* is the row of C_best in the run state when the freeze is written, which is the code exported as C+."
- **What the freeze lists:** exactly these rows and no others:
  - *ours*;
  - the baseline;
  - every row the last downstream pass produced: its ablation rows, its A_FullEng refinement if there is one, and its rebuttal rows;
  - the controls and diagnostics that task 6 registers in advance.

  This rule is computed from the run state, with no reading of the manuscript and no choice left to the writer.
- **The baseline:** "for a metric under IR-8 (a), the test event measures the baseline again in the same job; IR-15's values stand only for metrics that are functions of predictions."

**M2 · IR-21's gate table, IR-13, IR-27, §2.8 and §3.7: the gates set the stage primitive without saying how, and the tail is a new stage that the document never records as one.**

**The problem:**
- **(a) The gates do not map onto the primitive.** The register's convention is that "Where a decision sets the stage primitive, it names a parameter value of the one primitive that analysis.md sections 3.4 and 3.5 describe, never a loop of its own". Three kinds of gate each add a check-and-fix loop between the generator (or refiner) and the assessor:
  - G2: "the author gets the rule ID";
  - G3: "the manuscript is blocked until the writer fixes it";
  - G4 and G5, with their fixer.

  The parameter set in analysis.md §3.5 has only "an optional guard with its failure branch", which is the guard on updates after a refinement. It has no slot for a validity filter that runs before the assessor. If this stays unrecorded, task 3 will write G2 by hand into five stages (subset, full set, A_FullEng, ablation, rebuttal), and G3 into three (initial drafting, each enhancement, the tail). That is one copy per stage.
- **(b) G2 retries break the scoring cap (T2).** IR-13 caps scorings at "1 + N_eng". A G2 retry is a new unit of work, so it brings a new scoring. The count goes past the cap, and IR-24 (e) then fails the task's integrity.
- **(c) IR-21 decides what §3.6 leaves to task 2 (T3).** IR-21 ends the task when a gate's retries run out, while §3.6 leaves the choice between `Bad` and ending the task to task 2.
- **(d) The tail is a new stage, recorded only as a cost.** It appears in two places only: "one more stage at the end of every run" (§2.8) and "the gates add a stage after the test event" (§3.7).
  - It has no parameter row and no failure branches.
  - No register row of rank 5 (the shape of the stage graph) receives it.
  - It changes the termination branches of analysis.md §4.3, and adds a new end state: the test event is done, but nothing is exported. How that state counts under IR-18 and U-EVAL-1 is not stated.

**What it makes expensive:** each new gate, or a gate on one more stage, becomes code in that stage, and a new loop limit no longer bounds the scorings on its own.

**The fix:**
- **A table "Gates on the primitive":**

| Gate or rule | Where it sits on the primitive |
|---|---|
| G2, G3 | a new parameter, *filters*: checks run on each new candidate before the assessor, each with its class, where the rule ID goes, its retry and its exhaustion value |
| G4, G5 | a nested instance of the primitive: the checker is its critic, and the fixer (text only) its refine step |
| IR-7 | the assessor's rule: a numeric precondition, and the LLM verdict |
| IR-13 | the output of a refine step: one scoring per unit of work |
| IR-15 | the guard of the baseline row |
| G1, G6, G7 | invariants of the harness and of the run state, not stage parameters |

- **One counter per candidate:** "a candidate's scorings and refinements are bounded by one counter, the stage's limit; a G2 retry, if task 2 allows one, uses up a refinement". The alternative is that G2 discards without a retry, as §4.2's filter does. Leave the exhaustion value to task 2.
- **Record the tail as a stage,** with an updated termination table and this sketch:
  ```
  F = write_freeze(run_state)            # M1's rule; atomic, content-hashed; on a crash, rewrite (same hash)
  for i in report_identities(F):         # (freeze hash, row, seed, setting), plus the baseline's timing rows
      if released(i): continue           # a resume never scores twice
      harness.report(i)                  # crash: no record, the attempt is logged, re-run on resume (B1)
  P = final_fill(F)                      # engine code, from the verified table; deterministic
  P = stage(P, filters=[G3, G4, G5], refine=writer_text_only, limit=task2_bound)
  if P is None: end(run, "gate unresolved after the test event")   # how it counts: IR-18
  export(P, F)                           # bundle hash; the run's ledger closes here
  ```
- **Add these rows to the constraint tables:**
  - A-NOTE-1 (task 3, rank 1) gains the *filters* parameter and the tail's row;
  - A-TOP-2 (task 2, rank 1) sets IR-13's cap;
  - A-BASE-1 (task 2, rank 5) is decided by IR-4 for E_base: once per task;
  - U-TOP-2 (task 3, rank 2) receives B1's rule on resume.

**M3 · The Terms entry for the ledger, IR-4, IR-5, IR-15, and §2.7's U-BASE-2 row: per-task events have nowhere to live, and parallel runs race for them.**

**The problem.** Three per-task events have no per-task home:
- IR-4: the baseline "is fitted and scored like every row, once per task, before any candidate is scored".
- IR-15: the sealed check runs "once per task (that is, per manifest hash)".

Yet the ledger is "the run's append-only record", and each result record holds a "run ID". With IR-18's several runs per task, the count "once per task" has nowhere to live. Where these events happen is also left open: "at admission or before round 0".
- **The race.** Nothing makes runs of one task wait for each other. If the per-task jobs happen before round 0, a second run started at the same time hits IR-14's "The harness refuses any other", and IR-20 halts it as an integrity failure.
- **Edits re-read the report split.** Counting "per manifest hash" means that any edit to the manifest (the wording of a task rule, the citation of a published number) triggers a new sealed check, which reads the report split again, although the baseline's score cannot change.

**What it makes expensive:** admitting a new task, every edit to a manifest, and running a task's runs in parallel.

**The fix:**
- **Decide "at admission".** The baseline's fit jobs, its search scoring and the sealed check all run when the task is packaged, before any run can be registered.
- **Give their records and ledger entries task scope.** Runs refer to them by ID and never write them.
- **Narrow the key.** Count "once per task" over the fields that can change the baseline's score: the scoring items, the index files and labels, the baseline's code and diff, the image, the seeds and the settings.
- **Widen the audit.** IR-24 (a) reads the task-scope entries as well.
- ⛔ WHY NOT before round 0: parallel runs would race for a job the harness allows only once.

**M4 · IR-5, IR-14, IR-22, IR-23, IR-29 and IR-30: the audit's results land in engine stores.**

**The problem.** The harness serves two identities, the engine and the audit, but the rules give it only the engine's stores (T7):
- IR-5 lists "audit re-run" as a kind of result record, and says "Only the harness writes a result".
- IR-14 counts the audit's re-run in the run's ledger, which the engine can read.
- IR-30, by contrast, puts verdicts in "an audit store that only the audit's identity can write and that no engine job can read".
- IR-29 says "nothing it writes reaches a run".

So I1's re-run values sit beside the reported values in a store the engine can read, and I1's verdict can be worked out from them. The audit's own jobs are also appended to the ledger it audits.

**What it makes expensive:** the reporting auditor stays held out only as long as nobody reads an engine store. A builder who reads it has "seen its verdicts", and under IR-29 that retires the auditor.

**The fix:**
- **A harness job runs under the identity that asked for it,** and writes to that identity's store.
- **Jobs the audit asks for** write their records to the audit store, or to an area of audit scope with the same read rule, and are counted in an audit ledger.
- **The run's ledger closes at export.**
- **Move both entries to the audit side:** IR-5's "audit re-run" kind and IR-14's count of it.

**M5 · The Terms entry for "the harness", and IR-6: one name covers the code that enforces and the code that is enforced upon.**

**The problem.** The Terms define the harness as "a task's locked evaluation: the code that loads a split, runs agent code's predict step, validates its output and computes the metric". IR-6 hashes "the harness code (scoring data loaders, output schema, metric, aggregation)" in the manifest, and says "The harness checks every hash it depends on". Read literally, each task ships its own harness, and the code that checks the hashes is among the code it checks.

**What it makes expensive:** a new task, and any fix to the harness.
- If the code enforcing IR-5, IR-11, IR-14 and the IR-6 check sits in each task, every new task re-implements the part that integrity rests on, and that part must be re-verified per task.
- If that code is instead hashed in each manifest, a fix to it changes every manifest's hash, and IR-15 then re-reads the report split for every task.

**The fix: split the term into two.**
- **The scoring runner:** engine code at the run's pinned commit, the same for every task. It enforces IR-5, the IR-6 check, IR-9's validation, IR-11, IR-13 and IR-14.
- **A task's scoring items:** the loaders, output schema, metric, aggregation, environment and judge configuration. They are hashed in the manifest, and the runner runs them.

State two rules:
- IR-6's check is made by the runner, never by an item it checks.
- A change to the runner is a change of engine version (IR-18), never a change of manifest.

**M6 · The Mode column of §1.3, §2.4, §3.3 and §4.4, and the Terms entry for the toy task: "mock, $0" can test the mock instead of the guard.**

**The problem.** The setup controls test permissions, mounts, identities and stores: IR-2 and IR-3, IR-6, IR-11, IR-14, IR-22, IR-28, IR-29 and IR-30. `CLAUDE.md` puts every external dependency behind an interface with a mock, and lists sandboxes among the things that will have several implementations. So mock mode will include a mock sandbox and in-memory stores. A setup control run in that mode passes without testing the guard.

**The toy task's definition** ("a few hundred synthetic items in the three roles, a pinned baseline and a metric, run on a CPU in seconds, with mock agents that emit scripted code (task 7)") fixes task 7's fixture in advance. It also leaves out what the controls need:
- a mock judge, for IR-8 (b);
- a toy environment, for IR-8 (c);
- a timing workload that sleeps, for IR-8 (a);
- scripted adversaries: one that claims numbers in its logs, one that reads labels, one that ignores the seed, and one that hides its hack after reading the checker's reasoning;
- two identities, and canary strings.

**What it makes expensive:** a new sandbox implementation would pass every setup control without being tested.

**The fix:**
- **Change the Mode column** to "scripted agents, production setup, CPU, $0".
- **Add a rule:** a control of a setup guard runs against the production sandbox, mounts, identities, stores and runner; only the LLM, the coding agent and external APIs are mocked. A control run against a mock of the component it tests does not count.
- **Replace the definition of the toy task** with the list of fixtures above, as requirements on task 7.

**M7 · IR-18, IR-29 and IR-31: no configuration key for the runs a reported number covers.**

**The problem:**
- **(a) Runs of different configurations are pooled.** IR-18 takes the aggregate "over all registered runs". So a run with a different loop limit, or with a new model for one stage, joins the same per-task number.
- **(b) The final-test freeze does not cover limits.** It covers only "an engine version (code, prompts, routing)". Loop limits, budgets and schemas, which `CLAUDE.md` makes data, fall outside it. A different loop limit can therefore change a final-test task's engine after its first run.
- **(c) Two of IR-29's clauses have no record to point to:** "hashed before the reported runs start", and the clause that retires the auditor.

**What it makes expensive:** two of the five routine changes silently change what a reported number averages.

**The fix:**
- **Widen the configuration hash** to every versioned file a run reads: code, prompts, schemas, routing, limits and budgets.
- **Aggregate per configuration.** Take the aggregate over the runs of one (manifest hash, configuration hash). A run under another configuration starts a new set.
- **Optionally, a reporting-campaign record,** written before the first reported run. It holds:
  - the configuration hash;
  - the reporting auditor's configuration hash;
  - the final-test tasks, with their manifest hashes;
  - the aggregate, registered in advance.

  IR-18's freeze, IR-29's hashing and retirement clause, and IR-31's rates would all point to it.

### MINOR

- **m1 · The granularity of R2.**
  - **The problem:** IR-3, IR-5, IR-6, IR-11, IR-14, IR-18 and IR-29 each hold 5 to 8 invariants. IR-5, for example, holds: append-only; the fields; consumers reject records the harness did not write; no write path for agents; refused writes are logged; agents see aggregates only.
  - **The fix:** give sub-IDs (IR-5.1 and so on), so that task 2 can cite one invariant with one test. Make G1, G6 and G7 names of hooks that point to IR-6, IR-14 and IR-17, rather than second IDs.
- **m2 · IR-26 and IR-27: the roles.**
  - **The author includes the fixer (T8).** "The author (every session that writes code or the manuscript)" covers the fixer, "the writer that repairs references and the method text". The fix: exclude the fixer from the author role.
  - **IR-27's input list fits G2 only.** IR-27 says "The checker reads the code and the task rules". But G5 also reads the manuscript, and G4's judge reads the bibliography and the lookup records. The fix: list each check's own inputs.
- **m3 · Two rules read too widely.**
  - **IR-1 (T11):** it covers ScholarPeer's score tested against 8 and the novelty sort. Change it to "every number about a row's performance".
  - **IR-17 (T9):** it covers G4 and G5. Change it to "no decision of analysis.md section 4.2".
- **m4 · IR-27, IR-29 and IR-31: what a change of routing sets off.**
  - **The corpus depends on the author model.** IR-31's corpus includes "hacks that the author's model writes when asked to hide one". So a new author model means new corpus items, and every LLM check measured again.
  - **The checker may follow the author's backend.** IR-27 says "it may be the author's backend". Say whether the routing names a concrete model or "the same as the author". Otherwise a change of backend silently changes the checker, and voids its measured miss rate.
  - **IR-29:** compute its family check per run, from the recorded routing, and define "seen its verdicts".
  - **§4.7:** record what retiring the reporting auditor costs.
- **m5 · G3 fixes the interface of drafting.**
  - **The problem:** "inserted by engine code from a verified-table cell the writer names" fixes the writer's output format. That constrains U-DRAFT-1, U-PEER-4 and A-INT-2, and none of them is listed with this constraint.
  - **The fix:**
    - State the invariant: every measured number is bound to a cell and equals it.
    - Keep insertion as the mechanism, with a ⛔ WHY NOT against the alternative. ScientistOne's Ground step instead validates evidence tags (`.cache/refs/2605.26340v1/src/sections/04.5_system_claim_writer.tex:7`).
    - Say how figures are covered.
- **m6 · IR-7's precondition should be data.**
  - **The problem:** "whose rule task 2 sets per gate" leaves the precondition's form open.
  - **The fix:**
    - Make it a value of the assessor parameter, written over harness records (metric, settings, margin, seeds), so a new agent that judges performance is a data row.
    - State what a three-verdict critic does when the precondition fails: `Good` becomes `Engineer` while budget remains, and `Bad` after that.
- **m7 · A bound on what a model reads, without its owner.**
  - **The problem:** IR-5 ("aggregates per setting and seed, never per-item outputs") and IR-11 ("search inputs: none") cut the register's default of "everything" (U-EVO-2, U-SEL-2, U-ABL-6). `CLAUDE.md` requires such a cut to say "on the same line who chose it and what it loses".
  - **The fix:** add both. Task 6 chose it; the critics lose per-item error analysis on search, and keep it on the validation part of fit.
- **m8 · Actors and records that are never defined.**
  - **The problem:** three terms are used without a definition:
    - "the reporter", in the controls of IR-25 and IR-30;
    - "the reported table", in IR-29;
    - the run registry, in IR-18.
  - **The fix:** add them to the Terms, with who may read and write each.
- **m9 · IR-4 leaves the Baseline Coding Agent without a contract.**
  - **The problem:** "may still prepare C_base … but E_base never comes from it". Any change the agent makes to C_base is inherited by every idea, and credited to it against the pinned E_base.
  - **The fix:** either C_base is the pinned code plus the packaging diff and nothing else, or C_base is scored as a row of its own.
- **m10 · No way to correct a locked item.**
  - **The problem:** a defect in the harness found after a test event can only be fixed by a further report job, which IR-14 refuses. The only remedy left is to re-run whole runs.
  - **The fix:** record this as open, or allow a correction event that re-scores the frozen identities and is reported beside the original values, never in their place.

## 4. What is right, and must not be lost in the fixes

- **IR-2 and IR-3.** Agent code hands over a code tree at a content hash, and only fit jobs that engine code runs produce scored artifacts. Scoring is therefore independent of the coding backend, so a new backend never touches scoring.
- **IR-11.** One read table covers every kind of job, with the same paths in every job, and the setup enforces it.
- **IR-13.** The scoring cap is derived from the stage's limits. Keep it derived, never a second number.
- **IR-7.** "An LLM can only be stricter" composes cleanly as the assessor's rule.
- **IR-14.** The freeze is a hashed record of references: code hash, artifact hash and seeds.
- **IR-15.** It already records and reports every attempt. It is the model that B1 extends.
- **IR-20 and IR-30.** Three layers, each with its own writer and store. The audit never feeds a run, and the checker returns data while engine code writes the verdict.
- **IR-23 with IR-24 (c).** I1 extracts numbers from the paper independently of the provenance links, and the ledger check compares the two paths.
- **IR-26 and IR-27.**
  - The development and reporting auditors are two configurations of one audit.
  - The checker's model is a routing value.
- **Section 6.** The attacks these rules do not stop are listed honestly.
