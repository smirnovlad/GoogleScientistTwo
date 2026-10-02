# Requirements 2 · The stage primitive

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The paper abstracts every stage with one pseudocode, Listing 1, and task 1 concluded that every way a
stage departs from it is a parameter value of one primitive (`docs/paper/analysis.md` sections 3.4
and 3.5) [§3] [Lst. 1] [ours]. These requirements state that primitive's behaviour, parameter by
parameter; [03-stages.md](03-stages.md) gives each stage's values as data [ours]. How the primitive
is built is task 3's [ours].

### R-PRIM-1 · Every Table 1 stage is a configuration of one primitive

- **Requirement.** Each of Table 1's eleven stages runs as one generic primitive with a stage configuration that is data. No stage has a loop of its own in code, and a new stage, or a changed limit, verdict or at-limit policy, is a change of data only [§3] [Tab. 1] [ours].
- **Traces.** P-TOP-3 [Tab. 1] [§3].
- **Why ours.** The paper claims the abstraction, and analysis.md section 3.5 shows that it holds once the parameters below exist; CLAUDE.md makes behaviour data, run by generic code [§3] [ours].
- **Depends on.** A-NOTE-1, task 3, which confirms the primitive as a component [ours].
- **Test.** In mock mode, a toy stage defined only in a configuration file runs with no code change: its own verdict names, a limit of 3 and the keep-last policy. Its record shows exactly the calls its configuration implies [ours].

### R-PRIM-2 · The primitive's parameters

- **Requirement.** A stage configuration sets these parameters, and the primitive honours each one [Tab. 1] [Lst. 1] [ours]:
  - the generator [Tab. 1];
  - the judged object, and the refiner with the object it refines [Tab. 1] [§3.2];
  - the assessor, of one kind: an LLM verdict, a numeric threshold on a score, a score with no verdict, a deterministic check, or none [§3.1] [§3.5] [ours];
  - the verdict map, onto accept, refine and reject [Lst. 1];
  - an optional guard, with its failure branch [§3.4] [§3.6];
  - the limit: what it counts, and its value [App. A.2];
  - the stop tests: a count stop, a round limit, and when each is tested [§3.1] [§3.3];
  - the at-limit policy [Lst. 1] [§3.5];
  - nesting, and fan-out [§3.2, Eq. 2] [§3.4].
- **Traces.** P-TOP-2 [Lst. 1]; P-TOP-3 [Tab. 1].
- **Why ours.** The split into parameters is task 1's reading, not the paper's (analysis.md section 3.4); Listing 1 is one set of values: a critic that reads only the candidate, three verdicts, no guard, a limit on critic calls, and discard at the limit [Lst. 1] [ours].
- **Test.** In mock mode, with Listing 1's values and a scripted critic: an accept on the first call returns the candidate; a reject returns nothing; a critic that always asks for refinement makes `max_rounds` critic calls and `max_rounds` refinements, the last one never judged, and returns nothing [Lst. 1] [ours].

### R-PRIM-3 · A limit counts judged refinements

- **Requirement.** In every default stage configuration, a limit N counts refinements, and every refinement is judged: a stage makes at most N refinements and N + 1 assessor calls, and the verdict on the last refinement applies. Listing 1's convention, a limit on critic calls, stays available as a value, and no default stage uses it [Lst. 1] [App. A.2] [ours].
- **Traces.** P-TOP-2 [Lst. 1]; P-LIM-4 [§3.1]; P-SUB-4 [§3.2]; P-ABL-6 [§3.4]; P-PEER-6 [§3.5]; P-META-7 [§3.6].
- **Why ours.** App. A.2 states three of its limits as refinements, Table 5 counts review rounds 0, 1 and 2 under a limit of 2, and Figure 9 counts four rounds after the initial one; and under Listing 1's convention the last refinement is made and never judged [App. A.2] [Tab. 5] [Fig. 9] (image) [Lst. 1] [ours].
- **Decides.** A-TOP-2 [ours].
- **Test.** In mock mode, an assessor scripted to ask for refinement every time, under a limit of 2: 2 refinements, 3 assessor calls, and the third verdict decides. Under a limit of 0: 1 assessor call and no refinement [ours].

### R-PRIM-4 · What a stage keeps at its limit is one value per stage

- **Requirement.** The at-limit policy takes one of four values, set per stage in [03-stages.md](03-stages.md) [Lst. 1] [§3.5] [ours]:
  - discard: nothing passes on, as Listing 1 does [Lst. 1];
  - keep the last candidate, flagged as having reached the limit [§3.5];
  - keep the current best, the candidate the guard last accepted [§3.4] [§3.6];
  - stop the run [§3.3].
- **Traces.** P-TOP-2 [Lst. 1]; P-SUB-4 [§3.2]; P-PEER-6 [§3.5]; P-META-7 [§3.6].
- **Why ours.** Listing 1 discards at the limit, §3.5 keeps the last manuscript, and §3.4 and §3.6 imply keeping (the register's D-5); one value per stage settles it, last or best included [Lst. 1] [§3.4] [§3.5] [§3.6] [ours].
- **Decides.** A-TOP-1, with its aliases U-TOP-7, A-LIM-1 and U-ABL-4 [ours].
- **Test.** In mock mode, one scripted stage per value, each run to its limit. Discard: no candidate passes on. Keep the last: the last refinement passes on, flagged. Keep the current best: the guard's last accepted candidate passes on, not the last refinement. Stop the run: the run ends with its outcome record [ours].

### R-PRIM-5 · A guarded refinement replaces the kept candidate only when the guard accepts it

- **Requirement.** In a guarded stage, a refinement replaces the kept candidate, and the stage restarts on it, only when the guard accepts the refinement; otherwise the kept candidate stays and the stage's failure branch runs [§3.4] [§3.6].
- **Traces.** P-ABL-5 [§3.4]; P-META-4, P-META-5, P-META-6 [§3.6]; P-STATE-9 [§3.4].
- **Test.** In mock mode, a guard scripted to accept: the core state is replaced, and the stage runs again from its start on the new candidate. Scripted to reject: the core state is unchanged, and the configured failure branch runs [ours].

### R-PRIM-6 · The guard's rule is deterministic, over harness results

- **Requirement.** A guard decides by the task's comparison rule, fixed in its manifest, over validation results that the harness computed: the new result must beat the kept one beyond the task's margin, and a tie keeps the kept one. The Result Comparison Agent still runs; its reading is recorded beside the rule's result and never decides [§3.4] [§3.6] [ours].
- **Traces.** P-ABL-5 [§3.4]; P-META-4 [§3.6]; P-ROSTER-19 [§3.4] [§3.6].
- **Why ours.** §3.4 says both "strictly outperforms" and preferred by the agent, and results span several datasets and metrics [§3.4] (tex:sections/3_new_method.tex:111-112). Departs from the paper's second reading; CLAUDE.md requires gains computed deterministically from result files [ours].
- **Decides.** A-ABL-3 [ours].
- **Depends on.** U-INT-4 and U-TOP-5, task 6: the harness and the validation split the rule reads [ours].
- **Test.** With fixture result files: a new result better beyond the margin replaces the kept one; one within the margin does not; an agent scripted to prefer the new result while the rule keeps the old one leaves the old one, and the record shows both readings [ours].

### R-PRIM-7 · Assessors and verdict vocabularies are data

- **Requirement.** Each stage's assessor kind, its rule and its verdict words are configuration: an LLM verdict mapped onto accept, refine or reject, a score against a threshold, a score with no verdict, a deterministic check, or a choice [§3.1] [§3.2] [§3.3, Eq. 4] [§3.4] [§3.5] [§3.6] [ours].
- **Traces.** P-LIM-2 [§3.1]; P-SEED-2 [§3.1]; P-SUB-2 [§3.2]; P-FULL-3 [§3.2]; P-SEL-1 [§3.3, Eq. 4]; P-ABL-3 [§3.4]; P-PEER-2 [§3.5]; P-META-1 [§3.6].
- **Test.** In mock mode: a threshold assessor at 8 maps a score of 7.9 to refine and 8.0 to accept; a score-only assessor ranks its candidates and emits no verdict; renaming a verdict in the configuration renames it in the record, with no code change [ours].

### R-PRIM-8 · Stages nest and fan out, and the result does not depend on completion order

- **Requirement.** A stage's generator or refiner can be another stage configuration, and a stage can fan out over independent items: the candidates of a round, the ablation plans, the rebuttal tasks. Items may run in parallel, and the stage's result does not depend on the order in which they finish [§3.2, Eq. 2] [§3.3, Eq. 3] [§3.4] [§3.5] [§3.6] [ours].
- **Traces.** P-CODER-1 [§3.2, Eq. 2]; P-EVO-4 [§3.3, Eq. 3]; P-ABL-1, P-ABL-2 [§3.4]; P-PEER-3, P-PEER-4 [§3.5]; P-META-5 [§3.6].
- **Depends on.** U-TOP-4, task 3: what runs in parallel [ours].
- **Test.** In mock mode, a fan-out of three items run twice, with the items finishing in two different orders: the two stage records are identical apart from timestamps [ours].

### R-PRIM-9 · Every stage leaves a record that replays its control path

- **Requirement.** Each stage records [ours]:
  - every verdict with its feedback, and every refinement [ours];
  - every guard decision, with the rule's result and the agent's reading [ours];
  - the counters, and the at-limit policy if it applied [ours];
  - every skipped step, with its reason [ours].

  The run's control path can be rebuilt from these records alone [§3] [ours].
- **Traces.** P-TOP-4 [§3].
- **Why ours.** No page of Appendices C and D prints a verdict from §3's vocabulary, so the paper's own runs cannot be replayed [pp. 34–71] [ours].
- **Depends on.** U-ART-10, task 3: the record's format and the run layout [ours].
- **Test.** Replaying the records of a mock run, with no agent called, rebuilds the same sequence of stages, verdicts and guard decisions as the run itself [ours].
