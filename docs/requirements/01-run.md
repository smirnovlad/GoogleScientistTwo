# Requirements 1 · The run: one task in, one paper and codebase out

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
This file covers what the engine takes, what it returns, the order of its stages, and how a run
ends [§3] [ours].

### R-RUN-1 · One task in, one paper and one codebase out, or a recorded failure

- **Requirement.** From one task G the engine returns an improved paper P+ and an improved codebase C+, or no export and an outcome record that says why; P+ must address a bottleneck of G, and C+ must implement the idea reproducibly and with a measurable gain [§3, Eq. 1] [§3.6].
- **Traces.** P-TOP-1 [§3, Eq. 1]; P-STATE-17 [§3.6].
- **Test.** In mock mode, a scenario scripted to succeed exports a manuscript and a codebase snapshot with an outcome record; a scenario scripted to find no `Good` idea exports nothing, and its outcome record names the stage and the reason [ours].

### R-RUN-2 · A task is a manifest, fixed before the run

- **Requirement.** G reaches the engine as a versioned task manifest, fixed before the run. It names [ours]:
  - G's paper, and its code at a commit [§4.1];
  - the task rules the specification filter checks [§4.2];
  - the screening subset and the full benchmark [§3.2];
  - the reference numbers, published and reproduced, with a tolerance [Tab. 1] [App. B] [ours];
  - the comparison rule: primary metric, datasets, direction, aggregation and margin [ours];
  - the evaluation protocol, read-only [App. B] [Tab. 15];
  - the compute [ours].

  The subset and the full benchmark are chosen by us when the task is packaged, never by an agent, and the harness reports every setting of the full benchmark [§3.2] [§4.1] [§4.2] [ours].
- **Traces.** P-STATE-1 [§3, Eq. 1]; P-STATE-2 [App. B] [Tab. 15]; P-BENCH-2 [§4.1].
- **Why ours.** The paper never says what a task contains (U-TOP-1), and in its one trace the agent decided what the full set covered and left out a setting it had run [p. 40] [p. 46] (image). A field the decisions read must not be an agent's to change [ours].
- **Decides.** U-BASE-1 [ours].
- **Depends on.** U-TOP-1 and A-TOP-4, task 3, the manifest's schema; U-TOP-5 and U-INT-4, task 6, the splits and the harness the manifest points to. Task 5 fills one manifest per task [ours].
- **Test.** A manifest without one of the fields above fails to load, and the message names the field. In mock mode, a coding agent scripted to drop one dataset of the full benchmark from its own run changes nothing reported: the harness scores the manifest's full benchmark and reports every one of its settings [ours].

### R-RUN-3 · A run's output can be the next run's task

- **Requirement.** An export (P+, C+) can become the G of a later run, so the output and the task manifest share one schema, or one documented conversion [§4.3] [Tab. 9].
- **Traces.** P-TOP-6 [§4.3] [Tab. 9].
- **Depends on.** A-TOP-4 and U-TOP-1, task 3: which parts of an export enter the next G [ours].
- **Test.** In mock mode, the export of one run, after the documented conversion if there is one, loads as the manifest of a second run, which completes [ours].

### R-RUN-4 · The stages run in the paper's order

- **Requirement.** A run executes:
  1. finding limitations, then seed ideas [§3.1];
  2. the baseline, once per task [§3.2];
  3. the idea rounds, A_Coder per candidate, then selection [§3.3];
  4. a downstream pass: ablation, drafting, peer review, meta-review [§3.4] [§3.5] [§3.6].

  A meta-review refinement that its guard accepts starts a new downstream pass at the ablation stage, and nothing before the ablation stage runs again [§3.6] [Fig. 7] (image).
- **Traces.** P-TOP-4 [§3] [§3.6].
- **Decides.** A-META-1, the re-entry point [ours].
- **Test.** In mock mode, the stage records of a run list the stages in this order; in a scenario where the meta-reviewer returns `Refine` and the guard accepts the refinement, the second pass starts at ablation planning, and no limitation, seed, baseline, idea-round or selection call follows it [ours].

### R-RUN-5 · Every task ends with exactly one outcome record

- **Requirement.** Every task ends with one outcome, from a fixed list [ours]:
  - an accepted export [§3.6];
  - an unapproved export, at the meta limit or after a refinement the guard rejects [§3.6] [ours];
  - no `Good` idea, with the number of results the specification filter discarded [§3.3] [§4.2];
  - the baseline not reproduced [ours];
  - an ablation reject [App. B];
  - the budget exhausted [ours];
  - an error after retries [ours].

  The record gives the stage, the reason, the last valid core state and the cost, and a failed task stays in every count and ledger [§3.3] [§3.6] [§4.2] [ours].
- **Traces.** P-TOP-5 [§3.3] [§3.6] [§4.2]; P-BENCH-4 [Tab. 3].
- **Why ours.** The paper ends a failed task without a record and names 1 of its 21 failures [§3.3] [Tab. 3] [App. B]. The last two outcomes are ours, from the budget guard (R-OPS-4) and the retry policy (R-OPS-7) [ours].
- **Decides.** U-EVO-4 [ours].
- **Depends on.** U-TOP-2, task 3, the retry policy behind the last outcome [ours].
- **Test.** In mock mode, one scenario per outcome, seven in all, each ends with exactly that outcome, its stage and its cost; the failed scenarios appear in the ledger and count as failures in the success report (R-MEAS-1) [ours].
