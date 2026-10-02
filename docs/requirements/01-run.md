# Requirements 1 · The run: one task in, one paper and codebase out

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
This file covers what the engine takes, what it returns, the sequence of its stages, the one rule
its numeric gates read, and how a run ends [§3] [ours].

### R-RUN-1 · One task in, one paper and one codebase out, or a recorded failure

- **Requirement.** From one task G the engine returns an improved paper P+ and an improved codebase C+, or no export and an outcome record that says why [§3, Eq. 1] [§3.6]. Whether P+ addresses a bottleneck of G, and whether C+ implements the idea with a measurable gain, is measured after the run, on the report role (R-MEAS-1, R-MEAS-5; U-TOP-5), never asserted by the run itself [§3, Eq. 1] [ours].
- **Traces.** P-TOP-1 [§3, Eq. 1]; P-STATE-17 [§3.6].
- **Why ours.** Those two clauses of Eq. 1 are judgements that no test of the engine can make, so they move to measurement (the architect's review, SA-11) [ours].
- **Depends on.** U-TOP-5, task 6 [ours].
- **Test.** Logic, in mock mode: a scenario scripted to succeed exports a manuscript, a codebase snapshot and an outcome record; a scenario scripted to find no `Good` idea exports nothing, and its outcome record names the stage and the reason [ours].

### R-RUN-2 · A task is a manifest and a read-only package, pinned before its first run

- **Requirement.** G reaches the engine as a task manifest and a read-only task package. The manifest is pinned before the task's admission by a hash registered in the repository, outside the run; a change makes a new version, and every result names the version it was computed under [ours]. The manifest names at least [ours]:
  - G's paper, and its code at a pinned commit, which is the baseline row, with the packaging diff that a person signs off (task 6's IR-4.1) [§4.1] [ours];
  - the task rules that the specification filter checks [§4.2];
  - the data roles, fit, search and report, each a hashed index file built when the task is packaged, with the screening subset a named part of search (IR-10; U-TOP-5) [§3.2] [ours];
  - one seed list per role, which no agent chooses (task 6's IR-9.3, IR-10.2); and whether the method is declared deterministic, a field of ours, so that R-MEAS-7's seed flag does not fire on a method meant to be deterministic [ours];
  - the settings a rebuttal task may declare, registered in advance (R-STG-11) [ours];
  - the published reference numbers, labelled as published, and the baseline tolerance (R-STG-3) [Tab. 1] [ours];
  - the comparison rule (R-RUN-6) [ours];
  - the evaluation entry points that the harness runs (U-INT-4) [App. B] [Tab. 15] [ours];
  - the compute envelope that bounds every row, the baseline's included: a job that exceeds it is stopped and released as failed, and the row's aggregate is invalid (IR-33.4, IR-9.4) [ours].

  The engine and the harness are task-generic: a new task is a manifest and a package, never code [ours]. The subset and the full benchmark are chosen when the task is packaged, never by an agent, and the harness scores every setting the manifest lists (IR-9) [§3.2] [§4.1] [ours]. The manifest's schema is task 3's (U-TOP-1, A-TOP-4) [ours].
- **Traces.** P-STATE-1 [§3, Eq. 1]; P-STATE-2 [App. B] [Tab. 15]; P-BENCH-2 [§4.1]; P-ROSTER-32 [Fig. 3] (image).
- **Why ours.** The paper never says what a task contains (U-TOP-1), and in its one trace the agent decided what the full set covered and left out a setting it had run [p. 40] [p. 46] (image). A field the decisions read must not be an agent's to change, and a hash recorded only inside the run can be changed with it unseen (EI-16). Other requirements read the seed lists, the registered rebuttal settings and the determinism declaration from the manifest, so it must hold them (MISS-21) [ours].
- **Decides.** U-BASE-1 [ours].
- **Depends on.** U-TOP-1 and A-TOP-4, task 3, the manifest's schema; U-TOP-5 and U-INT-4, task 6, the data roles and the harness [ours].
- **Test.** Logic: a manifest missing any field above, a seed list included, fails to load before any spend, and the message names the field; a second fixture task, added as a manifest and a package only, runs end to end with no code change [ours]. Enforcement, on the toy task [ours]:
  - a coding agent scripted to drop one setting of the full benchmark from its own run changes nothing reported, since the harness scores every listed setting; in the twin whose harness takes the agent's list, the setting disappears [ours];
  - a manifest edited after its hash was registered makes the next harness job refuse to run; in the twin that checks no registered hash, the job runs under the edited manifest [ours];
  - a row whose job exceeds the compute envelope is stopped and released as failed, no gate passes, and a resume does not run it again; in the twin with no envelope, its result enters the next decision [ours].

### R-RUN-3 · A run's output can be the next run's task

- **Requirement.** An export (P+, C+) can become the G of a later run, through one documented conversion [§4.3] [Tab. 9]. The conversion carries no number of the report role into the next G as a number to search on, so that no link of a chain searches on a test result (U-TOP-5, IR-14): the parent's report-role results become the child's published numbers, labelled and sealed as published [ours]. A chain's links, and how many there are, are registered before the first link's test event, and the chain's record counts every link's test event [ours]. Which parts of an export enter the next G is task 3's (A-TOP-4, U-TOP-1) [ours].
- **Traces.** P-TOP-6 [§4.3] [Tab. 9].
- **Why ours.** After the final fill, P+ holds test numbers beside validation ones (IR-17); passed on whole, they would steer the next link's search with the data it is scored on (EI-14). A link started only after its predecessor's test event went well selects on test numbers too (the integrity closure, NEW-12) [ours].
- **Depends on.** A-TOP-4 and U-TOP-1, task 3; U-TOP-5, task 6 [ours].
- **Test.** Logic, in mock mode: the export of one run, after the conversion, loads as the manifest of a second run, which completes; a scan of every input an agent of the second run reads finds no report-role value, and the parent's report results appear only as sealed published numbers; the chain's record counts two test events; a link registered after the first link's test event is refused [ours].

### R-RUN-4 · The run is a sequence of stages, held as data, in the paper's order

- **Requirement.** The run's sequence of stages is data, and each stage declares its scope, the task or the run. The default sequence runs [§3] [ours]:
  1. at the task's admission, once per task: the baseline, whose records every run of the task shares (R-STG-3) [§3.2] [ours];
  2. finding limitations, then seed ideas [§3.1];
  3. the idea rounds, A_Coder per candidate, then selection [§3.3];
  4. the meta stage, which runs a downstream pass, ablation, drafting and peer review, and then asks the Meta-Reviewer [§3.4] [§3.5] [§3.6] [ours];
  5. the tail, which ends in the export (R-RUN-7) [ours].

  When the meta-review's guard accepts a refinement, a new downstream pass starts at ablation planning, the ablation critic included, with fresh budgets, and the Meta-Reviewer is asked again at its end; nothing before ablation planning runs again [§3.6] [Fig. 7] (image) [ours]. How this is built is task 3's (A-NOTE-1). Each stage that can end the run declares its outcome in its configuration (R-RUN-5) [ours].
- **Traces.** P-TOP-4 [§3] [§3.6].
- **Why ours.** The paper states the restart in prose and in a figure, and the first draft gave it three mechanisms (SA-2). A sequence held as data makes a new stage, such as the tail, an insertion rather than new code [§3.6] [Fig. 7] (image). Task 6's second version runs the baseline's fits, its search scoring and its sealed check at the task's admission (IR-4.2, IR-15), so the baseline's scope is the task, not the run [ours].
- **Decides.** A-META-1, the re-entry point and what runs again [ours].
- **Depends on.** A-NOTE-1, task 3 [ours].
- **Test.** Logic, in mock mode: the stage records of two runs of one task list the stages in this order, and the baseline's records appear once, at admission, named by both runs; with the Meta-Reviewer scripted to `Refine` and the guard to accept, the second pass starts at ablation planning, and no limitation, seed, baseline, idea-round or selection call follows it; a toy stage inserted between SEL and the meta stage by data alone runs in its place; a toy stage that declares its own outcome ends a scripted run with that outcome [ours].

### R-RUN-5 · Every task ends with exactly one outcome record, and an outcome is final

- **Requirement.** Every task, and every run of it, ends with one outcome, from the union of the outcomes the stages declare and the operational ones [ours]:
  - an accepted export [§3.6];
  - an unapproved export, at the meta limit or after a refinement the guard rejects [§3.6] [ours];
  - no `Good` idea, with the number of results the specification filter discarded [§3.3] [§4.2];
  - an ablation reject [App. B];
  - a manuscript gate failed: before the freeze, no manuscript version passes its hooks within their repairs (R-INT-10; A-INT-1) [ours];
  - the test event done, not exported: after the test event, the tail's gates fail within their repairs, and the test-event records are reported all the same (task 6's IR-39.3; A-INT-1) [ours];
  - not admitted: at the task's admission, the baseline is not reproduced, or its preparation fails after retries, and no run starts (R-STG-3; task 6's IR-15.7) [ours];
  - an integrity halt: the setup itself failed, by a hash mismatch, a record its writer did not write, or a read of the report role that could feed a decision (IR-6.5, IR-14.6, IR-35.1; U-INT-4) [ours];
  - an error after retries: an agent's failure at a role whose failure stops the run (R-PRIM-10; U-TOP-2) [ours];
  - a frozen artifact lost: a frozen row's code or artifact is missing from its store and cannot be restored, with no agent write to explain it, and the run ends as a failure with that cause (task 6's IR-35, its tail stage) [ours];
  - abandoned: a suspended run ended under R-RUN-8's rule [ours].

  The record gives the stage, the reason, the last valid core state, the cost and, for a failure, the key of the failing unit [§3.3] [§3.6] [§4.2] [ours]. An outcome is final: a run with an outcome never resumes, and a failed task stays in every count and ledger. A suspended run has not ended (R-RUN-8) [ours].
- **Traces.** P-TOP-5 [§3.3] [§3.6] [§4.2]; P-BENCH-4 [Tab. 3].
- **Why ours.** The paper ends a failed task without a record and names 1 of its 21 failures [§3.3] [Tab. 3] [App. B]. The last seven outcomes come from our own guards: task 6's gates, setup checks, tail and admission, the retry policy and the suspended state. A run that failed a gate after its test event would otherwise vanish from the report while its writer had read every frozen row's test numbers (the integrity closure, NEW-13) [ours].
- **Decides.** U-EVO-4 [ours].
- **Depends on.** U-TOP-2, task 3, the retry policy; A-INT-1 and U-INT-4, task 6, the gates and the setup checks [ours].
- **Test.** Logic, in mock mode: one scenario per outcome, eleven in all, each ends with exactly that outcome, its stage, its cost and, for a failure, the failing unit's key; the failed scenarios appear in the ledger and count as failures in the success report (R-MEAS-1); a resume requested for a run that has its outcome is refused [ours].

### R-RUN-6 · One comparison rule per task serves every numeric gate

- **Requirement.** Each task's manifest holds one comparison rule, which every decision reads by its hash [ours]:
  - its metric fields: the primary metric, the settings, the direction, and how settings, metrics and seeds aggregate; every metric the evaluation entry points emit is recorded beside the primary one [§4.1] [ours];
  - one entry per gate, each with its own margin, defaulting to the task's, and its reference: the subset and full-set vetoes, against E_base; the Selector's near-tie band, against the leader; the ablation's mechanism control, against C_best's released search records, a filter only, since attribution is measured at the test event (R-STG-9, R-MEAS-1); the guards of ablation and meta-review, against the kept result [§3.2] [§3.3] [§3.4] [§3.6] [ours];
  - guardrail metrics, each with a non-inferiority bound against the same reference, compute among them, read from the compute the harness records for every attempt of the row (IR-5; U-INT-4) [ours];
  - completeness: a result that lacks a setting or a seed of the manifest's lists, or holds an invalid or non-finite value, passes no gate (IR-9.2, IR-9.4) [ours].

  **The noise floor.** At the task's admission the harness measures the baseline's spread across the manifest's search seeds, each a separate fit, on the settings and aggregate that each gate's entry reads (IR-4.2; U-TOP-5). Each gate's margin is derived, never chosen: the smallest that keeps that gate's false-pass rate for a change that does nothing, given the number of scorings the loop allows it (IR-13.4) and computed from a 95% upper confidence bound on the spread across the s seeds, at most α_gate, whose default is 0.05; a run whose floor cannot be computed does not start. α_gate bounds a gate's false passes, and is not task 6's α, which belongs to its success test (A-EVAL-1). The gates' values are task 2's (IR-7.1); how run-to-run variance is estimated, and the number of repeated runs, are task 6's (U-EVAL-4, U-ART-12), and the seed floor task 5's (IR-9.3) [ours]. Every decision record names the rule's hash and the manifest's. The reported gain reads the same metric fields under the formula of U-EVAL-1, task 6's, and the rule's other values, the guardrails' bounds and the aggregation, are task 5's, set before the task's admission [ours].
- **Traces.** none.
- **Why ours.** In the paper, LLM agents make every comparison: the critics, the Selector and the Result Comparison Agent [§3.2] [§3.3] [§3.4] [§3.6]. The first draft's four gates each named a rule fixed in advance, with nothing tying them together (MISS-9); one margin cannot fit gates of different noise (SA-13); a rule that ignores a missing setting, a second metric or compute passes a result that drops its losing setting or scales its compute (EI-9, EI-10) [App. B] [ours]. The first revision's floor read a run-to-run spread that is about 0 when seeds come from a fixed list, and did not exist when the configuration loaded; a change that does nothing passes a subset veto of margin 0 in about 0.75 of runs when the loop allows three scorings (the integrity closure, NEW-6, model A, n = 200,000) [ours].
- **Depends on.** U-EVAL-1, U-ART-12 and U-EVAL-4, task 6; U-INT-4 and U-TOP-5, task 6, the records the rule reads and the role they come from [ours].
- **Test.** Logic, with fixture result records [ours]:
  - changing the subset entry's margin changes the subset veto and leaves the Selector's band unchanged [ours];
  - a result better on the primary metric that omits its losing setting, lacks one seed, holds a NaN, or breaks a guardrail's bound, compute of its failed attempts included, passes no gate, while its twin under a rule with no completeness check and no guardrails passes [ours];
  - a toy baseline that is deterministic given its seed has a same-seed spread of 0 and a cross-seed spread σ: the floor reads σ, a margin of 0 is refused, and the margin computed for α_gate loads; admission records without the spread stop the run before it starts [ours];
  - every decision record names both hashes [ours].

### R-RUN-7 · The run ends in a tail that freezes, scores the test split once, and exports

- **Requirement.** Once the last decision that can change code or rows has been made, when meta-review ends with `Accept`, with N_meta spent or with a refinement discarded, the run's sequence ends in a tail stage, run once [§3.6] [ours]:
  1. the freeze, the one test event and the final fill, as task 6 sets them: at the test event every frozen row but E_base is fitted again from its code hash, with its job arguments, at each report seed, disjoint from the search seeds, and the report split is scored once; E_base's report results are those of its admission, except for a time or throughput metric, for which E_base is timed again in the same job as the frozen rows (IR-8.1, IR-14.4, IR-15.1, IR-17; U-TOP-5) [ours];
  2. one revision of the text by the writer, with no change to code, rows or roles (IR-17) [ours];
  3. the manuscript gates on the final version, each check run again after any repair, with at most 2 repairs per hook invocation; when they are spent, the run ends with *test event done, not exported* (R-INT-10; task 6's IR-21.6, IR-39.3; A-INT-1) [ours];
  4. the export (R-STATE-6), whose record lists every frozen row whose search and report gains differ in sign; when the method's own row is one of them, the export is marked *not confirmed on test* [§3.6] [ours].

  Nothing in the tail branches on a measured result: no critic, Selector, guard, review threshold or meta verdict runs in it (IR-17) [ours].
- **Traces.** P-META-2 [§3.6].
- **Departs from.** P-META-2: P+ is the reviewed P_new after the final fill and a revision of its text, not P_new itself [§3.6] [ours].
- **Why ours.** CLAUDE.md uses the test set once, at the end, and the paper's export has no such step. Task 6 decides what the tail holds; this requirement makes it a stage of the run's sequence, configured like the others (SA-9) [ours]. Scoring the searched artifact on the report split removes the evaluation's luck but keeps the fit's: with 20 candidates that do nothing, the winner keeps 1.33 of a 2.64 search gain on report (the integrity closure, NEW-1, model C, n = 20,000; task 6's first review found the same, which IR-14.4 now fixes) [ours]. A test number that contradicts a claim written from search numbers must be visible in the export (MISS-1) [ours].
- **Depends on.** U-TOP-5 and A-INT-1, task 6 [ours].
- **Test.** Logic, in mock mode [ours]:
  - an accepted run, an unapproved run and a run whose meta refinement is discarded each end with one freeze, one test event and one export, in that order; no critic, Selector or guard call follows the freeze [ours];
  - a writer scripted to ask for an experiment after the test event is refused [ours];
  - a tail writer scripted to fail the reference check three times ends the run with *test event done, not exported*, and its test-event records are in the report [ours];
  - a fixture whose method row gains on search and loses on report is exported marked *not confirmed on test*, and the row is listed [ours].

  Enforcement, on the toy task, whose models depend on their training seed: a search over 20 candidates that do nothing picks a winner, and over at least 100 seeded runs its reported test gain is 0 within ±3 SE; in the twin that scores the searched artifact on the report split without fitting it again, the reported gain is about half the search gain when the fit's noise equals the evaluation's, as stated before the run [ours]. For a time metric, E_base's timing in the test event's job, not its admission timing, enters the gain [ours].

### R-RUN-8 · No person decides anything between launch and export

- **Requirement.** Between launch and export no person makes a decision about a run, and no run is restarted, re-seeded or dropped because of a result (task 6's IR-18.4; U-TOP-5) [Abstract] [ours]. Every bound and fault falls in one class, by its level [ours]:

  | Level | Bound or fault | What it does | What lifts it |
  |---|---|---|---|
  | agent call or session | an error, a timeout, a malformed output, or the session's budget | an agent failure, retried, then mapped by its role (R-PRIM-10) [ours] | nothing: it is final for that step [ours] |
  | harness job | agent code's failure, its time or memory limit, or the compute envelope | a released failed result, never run again (IR-33.4) [ours] | nothing: it is the row's result [ours] |
  | harness job | a fault of the harness or the machine, past the manifest's attempts | the run suspended (IR-33.3) [ours] | an amendment recording the repair, which grants new attempts under the same identity, every attempt reported (IR-33.5) [ours] |
  | outside system | the LLM backend, a coding backend, search, bibliographic lookup or the drafting system unreachable past its retries | the run suspended [ours] | the system answering a probe again [ours] |
  | subscription | a usage-limit answer, or a failed billing check | the run suspended (R-OPS-12) [ours] | the window's reset, or the environment fixed [ours] |
  | task | its budget, or its wall-clock bound | the run suspended (R-OPS-4) [ours] | a raise, by an amendment under the rule [ours] |

  A suspended run resumes from its record (R-STATE-7), and suspended time counts toward no bound. Resuming, raising a budget or a bound, and abandoning a run follow a rule fixed before the task's admission, applied to every run of its class, each recorded as an amendment appended to the run's record; a resume, a raise or an abandonment outside the rule flags the report. A run still suspended when a report is computed counts as a failure in every denominator, flagged as suspended [ours]. The values of the bounds are task 5's (U-COST-1), and the retry policy task 3's (U-TOP-2) [ours].
- **Traces.** none.
- **Why ours.** The paper's engine runs "without human intervention" [Abstract]; a stop that waited for a person would make that untestable, and Vlad asked for an engine that delivers on its own (DEVELOPMENT_PROCESS.md, 2026-10-02) [ours]. A budget raised, a run resumed or a run abandoned only where its search records look promising selects runs by their results (the integrity closure, NEW-12; the analyst's second closure, C-3). A bound that suspended a run at one level and released a result at another let a resume re-run agent code that had timed out, and an outage of an outside system turned ideas `Bad` or lost a run after its one test event (the analyst's second closure, C-1, C-2; the architect's, N3-2). The amendment that grants new attempts is our reading of IR-33.3, which task 6 confirmed on 2026-10-02: no value is written before its record (IR-33.2), so a new attempt is never a re-roll [ours].
- **Depends on.** U-TOP-5, task 6; U-COST-1, task 5; U-TOP-2, task 3 [ours].
- **Test.** Logic, in mock mode [ours]:
  - the run log of every outcome scenario holds no human-input event between launch and export [ours];
  - a run suspended at its budget resumes from its record once the budget is raised under the rule, and the amendment is in its record; a raise, or an abandonment, for one run of a class outside the rule flags the report [ours];
  - a run suspended at a mock usage window resumes when the window resets, and the suspended time counts toward no wall-clock bound [ours];
  - agent code that times out is released as failed, and a resume does not run it again; a Subset Coding Agent session stopped at its budget ends in that role's outcome [ours];
  - the backend scripted to refuse connections through a coding agent's retries suspends the run, and no idea becomes `Bad`; the bibliographic lookup unreachable in the tail suspends the run, which after the resume exports with one test event [ours];
  - a harness fault past its attempts suspends the run, and an amendment recording the repair lets it resume with the attempts reported [ours];
  - a report computed while one run is suspended counts it as a failure, flagged; a suspended run abandoned under the rule has the outcome *abandoned* [ours].
