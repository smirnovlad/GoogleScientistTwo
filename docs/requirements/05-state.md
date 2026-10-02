# Requirements 5 · Run state: what is kept, who may change it, and resuming

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
`docs/paper/analysis.md` section 8 lists the seventeen objects that a run keeps, with their producers,
consumers and lifetimes; these requirements fix who may change each one, and how a run that stops
picks up again [§3] [ours]. Where each object is stored is task 3's [ours].

### R-STATE-1 · The task's inputs are read-only for the whole run

- **Requirement.** Nothing in a run writes to the task G: its paper, its code at the pinned commit, its rules, its reference numbers and its evaluation protocol. Each agent works on a copy, and R-INT-2 adds a hash check on the evaluation protocol [§3, Eq. 1] [App. B] [ours].
- **Traces.** P-STATE-1 [§3, Eq. 1]; P-STATE-2 [App. B] [Tab. 15].
- **Why ours.** The paper forbids changing the protocol by audit only; CLAUDE.md enforces integrity by the setup, never by a prompt [Tab. 15] [ours].
- **Test.** In mock mode, an agent scripted to write into the task's files fails with a permission error, and the hashes of the task's files are the same after the run as before it [ours].

### R-STATE-2 · Some records only grow

- **Requirement.** These records are appended to and never rewritten [§3.1] [§3.3] [§3.5] [ours]:
  - the set of limitations, fixed once its stage ends [§3.1];
  - the seed pool, fixed once sorted, and its record of the seeds already run, append-only [§3.1] [§3.3];
  - the traces of every idea, `Good` and `Bad` [§3.3, Eq. 3];
  - every review, kept in the record although the loop reads only the last [§3.5] [ours].
- **Traces.** P-STATE-3 [§3.1]; P-STATE-4 [§3.1] [§3.3]; P-STATE-7 [§3.3, Eq. 3]; P-STATE-13 [§3.5].
- **Test.** In mock mode, a write that changes an existing trace entry is refused, and after a run with two review rounds the record holds all three reviews [ours].

### R-STATE-3 · The core state changes only through the selection and the guard

- **Requirement.** h_best, E_best and C_best are set by the selection, and replaced only by a refinement that the guard accepts; every refinement candidate is recorded as promoted or discarded [§3.3, Eq. 4] [§3.4] [§3.6].
- **Traces.** P-STATE-9 [§3.3, Eq. 4] [§3.4]; P-STATE-11 [§3.4] [§3.6].
- **Test.** In mock mode, a write to the core state from anywhere but the selection or a guard that accepted is refused, and every A_FullEng result in the record is marked promoted or discarded [ours].

### R-STATE-4 · Every code version is a snapshot, and work happens on copies

- **Requirement.** Each code version is a snapshot with an ID and a hash, never edited in place: C_base, each idea's subset and full-set code, C_best, each C_new, each ablation and rebuttal variant, and C+. C+ ships the method together with the scripts behind every reported number [§3.2] [§3.4] [§3.6] [ours].
- **Traces.** P-STATE-5 [§3.2]; P-STATE-6 [§3.2]; P-STATE-16 [§3.2] [§3.4] [§3.6].
- **Why ours.** The paper keeps the previous best outputs after a failed refinement, which needs copies; and whether ablation and rebuttal code reaches C+ is open, while every reported number must be re-runnable [§3.6] [Tab. 7] [ours].
- **Depends on.** U-ABL-3, U-CODER-1, task 3: where auxiliary code lives, and the trace of a pruned idea [ours].
- **Test.** After a mock run, every code version that a record names exists and matches its recorded hash; C_base's hash is unchanged; every script behind a number in the verified results table is in C+ [ours].

### R-STATE-5 · Each pass, round and revision leaves its own record

- **Requirement.** These records are fixed once made [§3.3] [§3.4] [§3.5] [§3.6] [ours]:
  - a round's candidates, fixed when the round starts [§3.3];
  - one ablation record per pass: plans, results, verdict and feedback [§3.4];
  - one manuscript version per revision, numbered in order [§3.5];
  - one rebuttal record per cycle: tasks and results [§3.5];
  - the meta decision and its feedback, once per pass [§3.6].
- **Traces.** P-STATE-8 [§3.3]; P-STATE-10 [§3.4]; P-STATE-12 [§3.5]; P-STATE-14 [§3.5]; P-STATE-15 [§3.6].
- **Test.** In mock mode, a run with a meta restart leaves two ablation records, manuscript versions numbered in order across both passes, and one meta decision per pass [ours].

### R-STATE-6 · The export is fixed, and marked

- **Requirement.** At export, P+ and C+ are hashed and become read-only, and the export record carries the last meta verdict, so that an unapproved export is never counted as an accepted one [§3.6] [ours].
- **Traces.** P-STATE-17 [§3, Eq. 1] [§3.6].
- **Decides.** A-TOP-3 [ours].
- **Test.** In mock mode, a write to an export is refused; an export after a guard rejection carries the verdict `Refine` and the mark *unapproved*, and the success report counts it apart (R-MEAS-1) [ours].

### R-STATE-7 · A stopped run resumes, and never pays twice for finished work

- **Requirement.** Every finished unit of work is written to disk before the next starts. After a crash, the run resumes from the last finished unit, and a retry never repeats a unit that finished [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md requires long runs to resume. The paper's runs last 2.51 days on average, and most of the time and cost is spent inside A_Coder, so the unit that resumes sits inside it [Fig. 10] (image) [ours].
- **Depends on.** U-CFG-2 and U-TOP-2, task 3: the unit of work, and the failure policy [ours].
- **Test.** A mock run killed inside A_Coder after k finished units, then restarted, finishes with the same records as an uninterrupted run, and the mock's call counter shows each finished unit called once [ours].

### R-STATE-8 · A run has a declared layout on disk

- **Requirement.** Each task's run writes to one directory with a declared layout: code versions, harness results, stage records, manuscript versions and the ledger. Every file a record names is inside it [pp. 40–55] [ours].
- **Traces.** P-ART-11 [pp. 40–55].
- **Why ours.** The one layout the paper shows is one task's, and its reports were written by the scripts they report on [p. 42] (image) [ours].
- **Depends on.** U-ART-10, task 3: the layout and the record format [ours].
- **Test.** After a mock run, the run directory validates against the declared layout, and every path that a record names exists [ours].
