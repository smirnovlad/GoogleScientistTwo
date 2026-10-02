# Requirements 5 · Run state: what is kept, who may change it, and resuming

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
`docs/paper/analysis.md` section 8 lists the seventeen objects that a run keeps, with their producers,
consumers and lifetimes; these requirements fix who may change each one, and how a run that stops
picks up again [§3] [ours]. Where each object is stored is task 3's [ours].

### R-STATE-1 · The task's inputs are read-only for the whole run, and checked at every use

- **Requirement.** Nothing in a run writes to the task G: its paper, its code at the pinned commit, its rules, its published numbers and its evaluation entry points. Each agent works on a copy, and no agent can read the index files or labels of the search and report roles (task 6's IR-11; U-TOP-5). The harness checks the hashes it depends on at the start of every job, not after the run (IR-6; U-INT-4) [§3, Eq. 1] [App. B] [ours].
- **Traces.** P-STATE-1 [§3, Eq. 1]; P-STATE-2 [App. B] [Tab. 15].
- **Why ours.** The paper forbids changing the protocol by audit only; CLAUDE.md enforces integrity by the setup, never by a prompt [Tab. 15] [ours]. A comparison of hashes after the run misses an edit restored before it ends (EI-16) [ours].
- **Depends on.** U-TOP-5 and U-INT-4, task 6 [ours].
- **Test.** Enforcement, on the toy task: an agent scripted to write into the task's files, and one scripted to open a label file, both fail on the real sandbox; a task file edited and restored between two harness jobs makes the second job refuse to run. In the twin with a writable mount and a hash check only after the run, the edit changes the next decision and the final check passes [ours].

### R-STATE-2 · Some records only grow

- **Requirement.** These records are appended to and never rewritten [§3.1] [§3.3] [§3.5] [ours]:
  - the set of limitations, fixed once its stage ends [§3.1];
  - the seed pool, fixed once sorted, and its record of the seeds already run, append-only [§3.1] [§3.3];
  - the traces of every idea, `Good` and `Bad` [§3.3, Eq. 3];
  - every review, kept in the record although the loop reads only the last [§3.5] [ours].
- **Traces.** P-STATE-3 [§3.1]; P-STATE-4 [§3.1] [§3.3]; P-STATE-7 [§3.3, Eq. 3]; P-STATE-13 [§3.5].
- **Test.** Logic, in mock mode: a write that changes an existing trace entry is refused, and after a run with two review rounds the record holds all three reviews [ours].

### R-STATE-3 · The core state changes only through the selection and the guard

- **Requirement.** h_best, E_best and C_best are set by the selection, and replaced only by a refinement that the guard accepts; every refinement candidate is recorded as promoted or discarded, and every change of the core state leaves an audit row with its cause [§3.3, Eq. 4] [§3.4] [§3.6] [ours].
- **Traces.** P-STATE-9 [§3.3, Eq. 4] [§3.4]; P-STATE-11 [§3.4] [§3.6].
- **Test.** Logic, in mock mode: a write to the core state from anywhere but the selection or a guard that accepted is refused; every A_FullEng result in the record is marked promoted or discarded; each change of the core state has its audit row [ours].

### R-STATE-4 · Every code version is a snapshot, and work happens on copies

- **Requirement.** Each code version that a result, a verdict or a record names is a snapshot with an ID and a hash, never edited in place: C_base, each idea's subset and full-set code, C_best, each C_new, each ablation and rebuttal variant, and C+. C+ holds the code of every row of the freeze, so that the audit can re-run each (task 6's constraint on U-ABL-3); where auxiliary code lives, and the trace of a pruned idea, are task 3's (U-ABL-3, U-CODER-1) [§3.2] [§3.4] [§3.6] [ours].
- **Traces.** P-STATE-5 [§3.2]; P-STATE-6 [§3.2]; P-STATE-16 [§3.2] [§3.4] [§3.6].
- **Why ours.** The paper keeps the previous best outputs after a failed refinement, which needs copies; a verdict bound to a hash cannot be about other code than the code the harness ran (EI-21) [§3.6] [Tab. 7] [ours].
- **Depends on.** U-ABL-3 and U-CODER-1, task 3 [ours].
- **Test.** Logic: after a mock run, every code version that a record names exists and matches its recorded hash; C_base's hash is unchanged; C+ holds the code of every row of the freeze [ours].

### R-STATE-5 · Each pass, round and revision leaves its own record

- **Requirement.** These records are fixed once made [§3.3] [§3.4] [§3.5] [§3.6] [ours]:
  - a round's candidates, fixed when the round starts [§3.3];
  - one ablation record per pass: plans, the control, results, verdict and feedback [§3.4] [ours];
  - one manuscript version per revision, numbered in order, with the IDs of the code version and the table version it was written from [§3.5] [ours];
  - one rebuttal record per cycle: tasks and results [§3.5];
  - the meta decision and its feedback, once per pass [§3.6].
- **Traces.** P-STATE-8 [§3.3]; P-STATE-10 [§3.4]; P-STATE-12 [§3.5]; P-STATE-14 [§3.5]; P-STATE-15 [§3.6].
- **Test.** Logic, in mock mode: a run with a meta restart leaves two ablation records, manuscript versions numbered in order across both passes, each naming its code and table versions, and one meta decision per pass [ours].

### R-STATE-6 · The export is fixed, and marked

- **Requirement.** At export, P+ and C+ are hashed and become read-only, and the export record carries the last meta verdict, so that an unapproved export is never counted as an accepted one [§3.6] [ours].
- **Traces.** P-STATE-17 [§3, Eq. 1] [§3.6].
- **Decides.** A-TOP-3 [ours].
- **Test.** Logic, in mock mode: a write to an export is refused; an export after a guard rejection carries the verdict `Refine` and the mark *unapproved*, and the success report counts it apart (R-MEAS-1) [ours].

### R-STATE-7 · A stopped run resumes, and never pays twice for finished work

- **Requirement.** Every unit of work, an agent call, a coding session or a harness job, has a key derived from its place in the run: stage path, pass, round, item and attempt. Its record is written to disk before the next unit that depends on it starts [ours]. On resume [ours]:
  - a finished unit is never run again, and a unit with a harness result reuses that result on any retry (U-INT-4) [ours];
  - a unit whose call may have finished is in doubt, and is reconciled before any retry, never retried blind [ours];
  - a resumed unit starts from its recorded input snapshot, never from a half-edited workspace [ours];
  - the run reads the configuration versions and the ledger its record names, never the files as they now are on disk [ours].

  The unit of work and the failure policy are task 3's (U-CFG-2, U-TOP-2) [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md requires long runs to resume, and a retry never to spend twice. The paper's runs last 2.51 days on average, and most of the time and cost is spent inside A_Coder, so the unit that resumes sits inside it [Fig. 10] (image). After a timeout the engine cannot know whether a paid call finished, and a retry after a poor result would re-draw it (SA-4, EI-21) [ours].
- **Depends on.** U-CFG-2 and U-TOP-2, task 3; U-INT-4, task 6, the harness's records [ours].
- **Test.** Logic, in mock mode: the run is killed at every unit boundary, inside a fan-out, inside the second downstream pass, during a harness job, and between a paid call's return and its durable record. After each restart, every finished unit has been called once, the unit in flight at most once more, the records equal an uninterrupted run's, and configuration files edited on disk in the meantime are ignored [ours].

### R-STATE-8 · A run's parts resolve from its record, each with its own writers

- **Requirement.** Every artifact a record names, code versions, harness results, stage records, manuscript versions, the verified table and the ledger, resolves from the run's record by ID and hash; where it is stored is task 3's (U-ART-10) [pp. 40–55] [ours]. The parts have separate write permissions: an agent writes only its declared outputs, and only engine code and the harness write results, records, verdicts and the ledger (task 6's IR-5 and IR-30; U-INT-4); no agent writes a behaviour file (R-OPS-2) [ours].
- **Traces.** P-ART-11 [pp. 40–55].
- **Why ours.** The one layout the paper shows is one task's, its reports written by the scripts they report on [p. 42] (image), and its auditor's verdict saved inside the task it audited [p. 47]. A single writable run directory lets a session write a result or a verdict that the next decision reads (EI-4) [ours].
- **Depends on.** U-ART-10, task 3; U-INT-4, task 6 [ours].
- **Test.** Logic: after a mock run, every artifact that a record names resolves and matches its hash [ours]. Enforcement, on the toy task: a coding session scripted to write a result record, a stage record holding a verdict, and a margin in a behaviour file is refused all three times, and the next decision is unchanged; in the twin with the run directory writable, each write changes the next decision [ours].

### R-STATE-9 · Every idea has a decision trail that one query returns

- **Requirement.** For any idea, one query over the run's records returns its whole trail: its origin, a seed's rank or the traces it evolved from; its novelty score with its references; every verdict with its feedback and the harness records the judge read; every engineering step with its code version; and, if chosen, the Selector's reason. A pruned idea's trail ends at the verdict that pruned it. The record format is task 3's (U-ART-10), and the records the judges read are the harness's (U-INT-4) [§3.1] [§3.2] [§3.3] [ours].
- **Traces.** none.
- **Why ours.** A_Evolve reads the failure logs of `Bad` ideas, and CLAUDE.md keeps run history as data that can be queried; the paper prints no verdict at all [§3.3] [pp. 34–71] [ours].
- **Depends on.** U-ART-10, task 3; U-INT-4, task 6 [ours].
- **Test.** Logic: after a mock run, for every idea ID, one query returns a trail with each of the parts above, and a pruned idea's trail ends at its `Bad` [ours].

### R-STATE-10 · The verified results table is run state that only engine code writes

- **Requirement.** The verified results table, which the writers, the Meta-Reviewer and the export read, is written only by engine code from the harness's result records (U-INT-4). It is versioned and append-only; each entry cites its records by ID and hash and carries its row's role, its split role, its metric and direction, and its seed count (U-TOP-5); a result the specification filter discarded never enters it, and its discard is recorded. Its form, and the consistency check before export, are task 6's (A-ART-7); what the drafter reads from it is task 3's (U-DRAFT-1) [§3.5] [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md lets the manuscript writer see only verified results. Four stages and the export read one table that no requirement had defined (SA-9), and a number without its role can be quoted as another row's (EI-5) [§3.5] [ours].
- **Depends on.** U-INT-4, U-TOP-5 and A-ART-7, task 6; U-DRAFT-1, task 3 [ours].
- **Test.** Logic, in mock mode: after a run, every entry of every table version resolves to harness records with matching hashes and carries its roles; a result the filter discarded is absent, and its discard is in the record; an attempt by an agent to write an entry is refused [ours].
