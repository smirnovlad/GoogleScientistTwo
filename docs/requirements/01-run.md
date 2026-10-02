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

- **Requirement.** G reaches the engine as a task manifest and a read-only task package. The manifest is pinned before the task's first run by a hash registered in the repository, outside the run; a change makes a new version, and every result names the version it was computed under [ours]. The manifest names [ours]:
  - G's paper, and its code at a pinned commit, which is the baseline row (task 6's IR-4) [§4.1] [ours];
  - the task rules that the specification filter checks [§4.2];
  - the data roles, fit, search and report, each a hashed index file built when the task is packaged, with the screening subset a named part of search (IR-10; U-TOP-5) [§3.2] [ours];
  - the published reference numbers, labelled as published, and the baseline tolerance (R-STG-3) [Tab. 1] [ours];
  - the comparison rule (R-RUN-6) [ours];
  - the evaluation entry points that the harness runs (U-INT-4) [App. B] [Tab. 15] [ours];
  - the compute envelope that bounds every row, the baseline's included [ours].

  The engine and the harness are task-generic: a new task is a manifest and a package, never code [ours]. The subset and the full benchmark are chosen when the task is packaged, never by an agent, and the harness scores every setting the manifest lists (IR-9) [§3.2] [§4.1] [ours]. The manifest's schema is task 3's (U-TOP-1, A-TOP-4) [ours].
- **Traces.** P-STATE-1 [§3, Eq. 1]; P-STATE-2 [App. B] [Tab. 15]; P-BENCH-2 [§4.1].
- **Why ours.** The paper never says what a task contains (U-TOP-1), and in its one trace the agent decided what the full set covered and left out a setting it had run [p. 40] [p. 46] (image). A field the decisions read must not be an agent's to change, and a hash recorded only inside the run can be changed with it unseen (EI-16) [ours].
- **Decides.** U-BASE-1 [ours].
- **Depends on.** U-TOP-1 and A-TOP-4, task 3, the manifest's schema; U-TOP-5 and U-INT-4, task 6, the data roles and the harness [ours].
- **Test.** Logic: a manifest missing any field above fails to load before any spend, and the message names the field; a second fixture task, added as a manifest and a package only, runs end to end with no code change [ours]. Enforcement, on the toy task: a coding agent scripted to drop one setting of the full benchmark from its own run changes nothing reported, since the harness scores every listed setting, while in the twin whose harness takes the agent's list the setting disappears; a manifest edited after its hash was registered makes the next harness job refuse to run [ours].

### R-RUN-3 · A run's output can be the next run's task

- **Requirement.** An export (P+, C+) can become the G of a later run, through one documented conversion [§4.3] [Tab. 9]. The conversion carries no number of the report role into the next G, so that no link of a chain searches on a test result (U-TOP-5, IR-14), and the chain's record counts every link's test event [ours]. Which parts of an export enter the next G is task 3's (A-TOP-4, U-TOP-1) [ours].
- **Traces.** P-TOP-6 [§4.3] [Tab. 9].
- **Why ours.** After the final fill, P+ holds test numbers beside validation ones (IR-17); passed on whole, they would steer the next link's search with the data it is scored on (EI-14) [ours].
- **Depends on.** A-TOP-4 and U-TOP-1, task 3; U-TOP-5, task 6 [ours].
- **Test.** Logic, in mock mode: the export of one run, after the conversion, loads as the manifest of a second run, which completes; a scan of every input of the second run finds no value tagged with the report role; the chain's record counts two test events [ours].

### R-RUN-4 · The run is a sequence of stages, held as data, in the paper's order

- **Requirement.** The run's sequence of stages is data. The default sequence runs [§3] [ours]:
  1. finding limitations, then seed ideas [§3.1];
  2. the baseline, once per task [§3.2];
  3. the idea rounds, A_Coder per candidate, then selection [§3.3];
  4. a downstream pass: ablation, drafting, peer review, then meta-review [§3.4] [§3.5] [§3.6];
  5. the tail, which ends in the export (R-RUN-7) [ours].

  When the meta-review's guard accepts a refinement, a new downstream pass starts at ablation planning, the ablation critic included, with fresh budgets, and the Meta-Reviewer is asked again at its end; nothing before ablation planning runs again [§3.6] [Fig. 7] (image) [ours]. How this is built is task 3's (A-NOTE-1). Each stage that can end the run declares its outcome in its configuration (R-RUN-5) [ours].
- **Traces.** P-TOP-4 [§3] [§3.6].
- **Why ours.** The paper states the restart in prose and in a figure, and the first draft gave it three mechanisms (SA-2). A sequence held as data makes a new stage, such as the tail, an insertion rather than new code [§3.6] [Fig. 7] (image) [ours].
- **Decides.** A-META-1, the re-entry point and what runs again [ours].
- **Depends on.** A-NOTE-1, task 3 [ours].
- **Test.** Logic, in mock mode: the stage records of a run list the stages in this order; with the Meta-Reviewer scripted to `Refine` and the guard to accept, the second pass starts at ablation planning, and no limitation, seed, baseline, idea-round or selection call follows it; a toy stage inserted between SEL and the downstream pass by data alone runs in its place; a toy stage that declares its own outcome ends a scripted run with that outcome [ours].

### R-RUN-5 · Every task ends with exactly one outcome record

- **Requirement.** Every task ends with one outcome, from the union of the outcomes the stages declare and the operational ones [ours]:
  - an accepted export [§3.6];
  - an unapproved export, at the meta limit or after a refinement the guard rejects [§3.6] [ours];
  - no `Good` idea, with the number of results the specification filter discarded [§3.3] [§4.2];
  - the baseline not reproduced (R-STG-3) [ours];
  - an ablation reject [App. B];
  - a manuscript gate failed: the repairs of a check on the manuscript are spent (IR-21, R-INT-10; A-INT-1) [ours];
  - an integrity halt: the setup itself failed, by a hash mismatch or a record its writer did not write (IR-6, IR-20; U-INT-4) [ours];
  - the budget exhausted (R-OPS-4) [ours];
  - an error after retries, under the retry policy (R-OPS-7; U-TOP-2) [ours].

  The record gives the stage, the reason, the last valid core state and the cost, and a failed task stays in every count and ledger [§3.3] [§3.6] [§4.2] [ours]. A run paused at a usage window of the subscription has not ended (R-OPS-12) [ours].
- **Traces.** P-TOP-5 [§3.3] [§3.6] [§4.2]; P-BENCH-4 [Tab. 3].
- **Why ours.** The paper ends a failed task without a record and names 1 of its 21 failures [§3.3] [Tab. 3] [App. B]. The last five outcomes come from our own guards: task 6's gates and setup checks, the budget guard and the retry policy [ours].
- **Decides.** U-EVO-4 [ours].
- **Depends on.** U-TOP-2, task 3, the retry policy; A-INT-1 and U-INT-4, task 6, the gates and the setup checks [ours].
- **Test.** Logic, in mock mode: one scenario per outcome, nine in all, each ends with exactly that outcome, its stage and its cost; the failed scenarios appear in the ledger and count as failures in the success report (R-MEAS-1) [ours].

### R-RUN-6 · One comparison rule per task serves every numeric gate

- **Requirement.** Each task's manifest holds one comparison rule, which every decision reads by its hash [ours]:
  - its metric fields: the primary metric, the settings, the direction, and how settings, metrics and seeds aggregate [§4.1] [ours];
  - one entry per gate, each with its own margin and defaulting to the task's: the subset and full-set vetoes, the Selector's near-tie band, the ablation's mechanism control, the guards of ablation and meta-review [§3.2] [§3.3] [§3.4] [§3.6] [ours];
  - guardrail metrics, each with a non-inferiority bound, compute among them, read from the compute the harness records with each result (IR-5; U-INT-4) [ours];
  - completeness: a result that lacks a setting of the rule, or holds an invalid or non-finite value, passes no gate (IR-9) [ours].

  The configuration refuses a margin below k times the baseline's measured run-to-run spread on the same role, where k and the number of runs are task 6's (U-ART-12, U-EVAL-4) [ours]. Every decision record names the rule's hash and the manifest's. The reported gain reads the same metric fields under the formula of U-EVAL-1, task 6's, and every value of the rule is task 5's, set before the task's first run [ours].
- **Traces.** none.
- **Why ours.** In the paper, LLM agents make every comparison: the critics, the Selector and the Result Comparison Agent [§3.2] [§3.3] [§3.4] [§3.6]. The first draft's four gates each named a rule fixed in advance, with nothing tying them together (MISS-9); one margin cannot fit gates of different noise (SA-13); a margin below the noise passes a change that does nothing (EI-8); and a rule that ignores a missing setting, a second metric or compute passes a result that drops its losing setting or scales its compute (EI-9, EI-10) [App. B] [ours].
- **Depends on.** U-EVAL-1, U-ART-12 and U-EVAL-4, task 6; U-INT-4, task 6, the records the rule reads [ours].
- **Test.** Logic, with fixture result records: changing the subset entry's margin changes the subset veto and leaves the Selector's band unchanged; a result better on the primary metric that omits its losing setting, holds a NaN, or breaks a guardrail's bound, compute included, passes no gate, while its twin under a rule with no completeness check and no guardrails passes; a margin below k times the fixture spread fails to load; every decision record names both hashes [ours].

### R-RUN-7 · The run ends in a tail that freezes, scores the test split once, and exports

- **Requirement.** Once the last decision that can change code or rows has been made, when meta-review ends with `Accept`, with N_meta spent or with a refinement discarded, the run's sequence ends in a tail stage, run once [§3.6] [ours]:
  1. the freeze, the one test event and the final fill, as task 6 sets them (IR-14, IR-17; U-TOP-5) [ours];
  2. one revision of the text by the writer, with no change to code, rows or roles (IR-17) [ours];
  3. the manuscript gates, each repaired within its bound (R-INT-10; A-INT-1) [ours];
  4. the export (R-STATE-6) [§3.6].

  Nothing in the tail branches on a result: no critic, Selector, guard, review threshold or meta verdict runs in it (IR-17) [ours].
- **Traces.** P-META-2 [§3.6].
- **Departs from.** P-META-2: P+ is the reviewed P_new after the final fill and a revision of its text, not P_new itself [§3.6] [ours].
- **Why ours.** CLAUDE.md uses the test set once, at the end, and the paper's export has no such step. Task 6 decides what the tail holds; this requirement makes it a stage of the run's sequence, configured like the others (SA-9) [ours].
- **Depends on.** U-TOP-5 and A-INT-1, task 6 [ours].
- **Test.** Logic, in mock mode: an accepted run, an unapproved run and a run whose meta refinement is discarded each end with one freeze, one test event and one export, in that order; a writer scripted to ask for an experiment after the test event is refused; no critic, Selector or guard call follows the freeze [ours].

### R-RUN-8 · No person acts between launch and export

- **Requirement.** Between launch and export the run needs no person. Every stop, whether a guard, a budget or an error, ends the run with its outcome record, and a usage window of the subscription pauses it; a person may resume a stopped or paused run from its record (R-STATE-7) [Abstract] [ours].
- **Traces.** none.
- **Why ours.** The paper's engine runs "without human intervention" [Abstract]; a stop that waited for a person would make that untestable, and Vlad asked for an engine that delivers on its own (DEVELOPMENT_PROCESS.md, 2026-10-02) [ours].
- **Test.** Logic, in mock mode: the run log of every outcome scenario holds no human-input event between launch and export; a run stopped by its budget resumes from its record once the budget is raised, and a run paused at a mock usage window resumes when the window resets [ours].
