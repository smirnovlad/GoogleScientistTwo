# Requirements 3 · The stages, as configurations of the one primitive

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
Each stage below is a set of values for the behaviours of [02-primitive.md](02-primitive.md), never
a loop of its own [§3] [ours]. The table states every value once; each requirement after it adds
what a value alone cannot say, and its test [ours].

## The default stage configuration

The values come from the paper where it gives them, and are our decisions where it does not; each
cell says which [Tab. 1] [App. A.2] [ours]. A value set by another task is named, never guessed:
N_seed, N_p and N_t are task 5's, and the configuration refuses to load without them (R-STG-13)
[ours]. The cells use R-PRIM-2's vocabulary; where a cell implies a mechanism, such as the meta
stage's downstream pass, task 3 may build the same behaviour another way (A-NOTE-1) [ours]. The
cross-cutting checks run at hook points declared by the kind of step, not by stage (R-INT-10):
after a code-producing step, the harness's scoring, then the specification filter; after a
manuscript-producing step, compile, number provenance, references, then method–code alignment
[§4.2] [ours]. The tail is not a stage of Table 1; it is the last stage of the run's sequence
(R-RUN-7) [ours].

| Stage | Generator | Judged → refined, by | Assessor and rule | Verdict map | Guard, on failure | Limit: counts, value | At the limit | Nesting, fan-out |
|---|---|---|---|---|---|---|---|---|
| LIM | Limitation Extractor, from G [§3.1] | the set → the set, expanded by the Extractor with the Verifier's list of what is missing [§3.1] [ours] | an LLM verdict, the Limitation Verifier's: sufficient or not [§3.1] | sufficient → accept; insufficient → refine; no reject [§3.1] | none [§3.1] | judged refinements, 15, so 16 rounds of extraction [App. A.2] [ours] | keep the last set, flagged [ours] | none [§3.1] |
| SEED | the initial idea, then the Idea Generator, from G, the limitations and the scored pool [§3.1] [Fig. 4] (image) [ours] | none: each new idea is appended to the pool, and the stop test decides when to stop generating [§3.1] [ours] | a score with no verdict, the Novelty Checker's, from two papers retrieved by search [§3.1] [App. A.2] | none: every idea is kept, ranked by its score [§3.1] [ours] | none [§3.1] | a count stop: the pool holds N_seed ideas, set by task 5 [§3.1] [ours] | keep the whole pool, sorted by score, descending [§3.1] | one idea at a time, since each new idea sees the pool [§3.1] [ours] |
| BASE | the harness fits and scores the task's pinned code, which is E_base; the Baseline Coding Agent prepares C_base, the pinned code with its notes [§3.2] [ours] | nothing is refined [Tab. 1] | a deterministic check: task 6's sealed check of the pinned code against the published numbers, one-sided, within the manifest's tolerance [ours] | pass → accept; fail → stop the run, *baseline not reproduced* [ours] | none [Tab. 1] | zero refinements; a tuned-baseline control is task 6's to add [Tab. 1] [ours] | not applicable [Tab. 1] | once per task, before round 0 [§3.2] [ours] |
| SUB | Subset Coding Agent, from h and C_base, declaring the idea's mechanism as switches [§3.2] [ours] | E_sub^h against E_base → h and C_sub^h, by the Subset Engineering Agent, which tunes and repairs only [§3.2] [ours] | an LLM verdict, the Subset Critic's, behind a deterministic precondition: the rule's subset entry, over the harness's records [§3.2] [ours] | `Good` → accept; `Engineer` → refine; `Bad` → reject; a `Good` the precondition blocks → `Engineer` [§3.2] [ours] | none [§3.2] | judged refinements, N_eng = 2 [App. A.2] | discard: `Bad`, pruned [§3.2] | inside A_Coder, once per idea [§3.2, Eq. 2] |
| FULL | Full-Set Coding Agent, adapting C_sub^h to every full-set setting of the manifest [§3.2] [ours] | the full-set results against E_base on every setting → h and C, by the Full-Set Engineer, which tunes and repairs only [§3.2] [ours] | an LLM verdict, the Full-Set Critic's, behind the rule's full-set entry [§3.2] [ours] | as the subset row [Fig. 5] (image) [ours] | none [§3.2] | judged refinements, 2 [App. A.2] [ours] | discard: `Bad`, kept in the traces [ours] | inside A_Coder, after a subset `Good` [§3.2] |
| EVO | round 0: the top N_0 = 2 seeds; round k ≥ 1: one idea from A_Evolve over all traces, and the next unevaluated seed while one is left [§3.3] [App. A.2] [ours] | the candidates, rebuilt each round from all traces, to which each outcome is appended [§3.3] [ours] | a nested stage, A_Coder, per candidate; its outcomes aggregated as the count of `Good` over all rounds [§3.3] [ours] | per candidate, `Good` or `Bad` into the traces; for the stage, another round until a stop test ends it [§3.3] [ours] | none [§3.3] | rounds after round 0, K = 4; a count stop at S = 4 `Good`, tested at the end of each round [§3.3] [App. A.2] [ours] | keep the accepted items, the `Good` tuples; with none, stop the run, *no Good idea* [§3.3] [ours] | a fan-out of A_Coder over the round's candidates: two, or one once the seeds run out [App. A.2] [ours] |
| SEL | none: every `Good` tuple from every round [§3.3, Eq. 4] | nothing is refined [Tab. 1] | a choice, the Selector's, behind a precondition: the rule's band entry keeps the leader and the ideas within its margin [§3.3] [ours] | the choice, with its reason [§3.3, Eq. 4] [ours] | none [§3.3] | zero refinements [Tab. 1] | not applicable [Tab. 1] | once per run [§3.3] |
| ABL | a sequence: the Ablation Planner's N_p plans, set by task 5; one Ablation Coding Agent per plan, on C_best; and the mechanism-off control, which the harness runs from C_best's switches [§3.4] [ours] | E_abl → h_best, by one A_FullEng call whose result the harness scores [§3.4] [ours] | an LLM verdict, the Ablation Critic's, under a written attribution rubric, behind a precondition: the control loses at least the rule's ablation margin [§3.4] [App. B] [ours] | `Good` → accept; `Refine` → refine; `Reject` → stop the run, *ablation reject*, or undo a promotion of this pass [§3.4] [App. B] [ours] | R-PRIM-6, E_new against E_best; on failure, go on to drafting with the unchanged h_best [§3.4] [Fig. 7] (image) [ours] | judged refinements, N_abl = 1 per downstream pass [App. A.2] [ours] | keep the current best, and go on to drafting [§3.4] [ours] | a fan-out over the N_p plans; after a promotion the stage restarts at planning [§3.4] |
| DRAFT | Initial Drafter, with PaperOrchestra, from h_best and the verified results table, its result figures rendered by engine code [§3.5] [ours] | nothing is refined [Tab. 1] | none; the manuscript hooks run after it [Tab. 1] [ours] | none [Tab. 1] | none [Tab. 1] | zero refinements [Tab. 1] | not applicable [Tab. 1] | once per downstream pass [§3.6] |
| PEER | the draft [§3.5] | P_new → P_new, by a sequence: the Rebuttal Planner's N_t tasks, set by task 5, each declaring its evaluation; one Rebuttal Coding Agent per task, scored by the harness; the Paper Enhancer [§3.5] [ours] | a score against a threshold: the in-loop reviewer's, against 8 [§3.5] [App. A.2] [ours] | 8 or more → accept; below 8 → refine; no reject [§3.5] | none: each revision replaces P_new [§3.5] | judged refinements, N_peer = 2 rebuttal cycles, so up to three reviews [App. A.2] [Tab. 5] [ours] | keep the last manuscript, never the best-scoring one [§3.5] [ours] | a fan-out over the N_t tasks of each cycle [§3.5] |
| META | the downstream pass, ablation to peer review, whose last P_new and R_new it judges [§3.6] [ours] | P_new and R_new → h_best, by A_FullEng; then a new downstream pass [§3.6] | an LLM verdict, the Meta-Reviewer's, under a written venue-bar rubric, which also reads the verified results table [§3.6] [ours] | `Accept` → accept, to the tail; `Refine` → refine; no reject [§3.6] [ours] | R-PRIM-6, strictly superior; on failure, the tail with the previous outputs, unapproved [§3.6] [ours] | judged refinements, N_meta = 1 [App. A.2] | the tail with the last pass's P_new and C_best, unapproved [§3.6] [ours] | the downstream pass nested in it, with fresh budgets on each restart; the Meta-Reviewer asked again after it [§3.6] [Fig. 7] (image) [ours] |
| TAIL | a sequence: the freeze, the one test event and the final fill, as task 6 sets them, then one revision of the text by the writer [ours] | nothing is refined; the hooks' repairs edit text only [ours] | none; the manuscript hooks run after the revision [ours] | none: nothing in the tail branches on a result [ours] | none [ours] | zero refinements [ours] | not applicable [ours] | once per run, after the meta stage [ours] |

## The stages

### R-STG-1 · Finding limitations

- **Requirement.** The limitation stage runs with the LIM values: the Extractor's set is judged by the Verifier, expanded while the Verifier finds it insufficient, and passed on after at most 15 judged refinements, so 16 rounds of extraction, flagged if the limit was reached [§3.1] [App. A.2] [ours]. An empty set is an empty output, which fails closed (R-PRIM-10). The Verifier's criterion and the limitation record are task 3's (U-LIM-1) [ours].
- **Traces.** P-LIM-1 … 4 [§3.1]; P-CFG-1 [App. A.2]; P-ROSTER-1, P-ROSTER-2 [§3.1].
- **Why ours.** The paper does not say what passes on at the limit; the next paragraph works from the limitations found, so the set passes on (A-LIM-1) [§3.1] [ours].
- **Decides.** A-TOP-1, its cell A-LIM-1 [ours].
- **Depends on.** U-LIM-1, task 3 [ours].
- **Test.** Logic, in mock mode: a Verifier scripted as always insufficient gives 16 Extractor calls and 16 Verifier calls, and the 16th set passes on, flagged; scripted as sufficient at once, one call of each and no flag; an Extractor scripted to return an empty set is retried, then ends the run with *error after retries* [ours].

### R-STG-2 · Seed ideas

- **Requirement.** The seed stage runs with the SEED values. Every idea gets a novelty score from two retrieved papers, and no idea is dropped for low novelty: the score only ranks [§3.1] [App. A.2] [ours]. The Idea Generator reads G, the limitations and the scored pool so far, under a written content rule that excludes pure compute or budget scaling; the rule is a prompt, and the guard against compute scaling is R-RUN-6's guardrail [§3.1] [App. B] [ours]. N_seed is task 5's (U-SEED-1); the score's scale and query, and whether the first idea has an agent of its own, are task 3's (U-SEED-2, A-SEED-2) [ours].
- **Traces.** P-SEED-1 … 4 [§3.1]; P-CFG-2 [App. A.2]; P-CFG-12 [§3.1]; P-ROSTER-3 … 5 [§3.1] [Fig. 4] (image).
- **Why ours.** §3 says ideas are filtered for novelty while §3.1 only sorts (A-SEED-1); we keep §3.1's ranking, and a threshold stays an optional ablation. App. B says the generator does not propose compute scaling, and no inputs are named (U-SEED-3) [§3] [§3.1] [App. B] [ours].
- **Decides.** A-SEED-1; U-SEED-3 [ours].
- **Depends on.** U-SEED-1, task 5; U-SEED-2 and A-SEED-2, task 3 [ours].
- **Test.** Logic, in mock mode, with N_seed = 6 and scripted scores: the pool holds exactly 6 ideas, sorted by score, descending, each with two references, and the lowest-scoring idea is still in it; the Idea Generator's recorded input holds G, the limitations and the scored pool [ours].

### R-STG-3 · The baseline, scored once per task from its pinned code

- **Requirement.** The baseline stage runs once per task, before round 0, with the BASE values [§3.2] [ours]:
  - **E_base.** The harness fits and scores the task's code at its pinned commit, on every setting of the search role, as task 6's IR-4 sets it; no agent's code produces it (U-INT-4) [ours];
  - **C_base.** The Baseline Coding Agent prepares C_base, the copy that ideas start from: the pinned code, unchanged, with the agent's notes on how it runs beside it; a copy whose code differs from the pinned commit is refused [§3.2] [ours];
  - **The check.** Task 6's sealed check compares the pinned code with the published numbers on the report role, once per manifest version and before any candidate is scored (IR-15; U-TOP-5). It is one-sided: a baseline weaker than a published number by more than the manifest's tolerance fails, and a stronger one passes and is recorded [ours];
  - **On failure.** The task ends with *baseline not reproduced* before any idea runs. No agent repairs the baseline; a person may repackage the task as a new manifest version, and every attempt is reported (IR-15) [ours];
  - **Into A_Coder.** A_Coder receives E_base and C_base, a recorded extension of Eq. 2 [§3.2, Eq. 2] [ours].

  Whether the baseline also gets a tuning budget is task 6's (U-SUB-2) [ours].
- **Traces.** P-BASE-1 [§3.2]; P-STATE-5 [§3.2]; P-ROSTER-6 [§3.2].
- **Why ours.** The paper runs the baseline first, on the subset, with no check (U-BASE-2); Figure 5 draws it inside each idea's pipeline (A-BASE-1); and no stage produces the full-set reference that Table 1's full-set critic compares with (A-FULL-1) [§3.2] [Fig. 5] (image) [Tab. 1]. Once per task saves up to 9 coding sessions a run and gives every idea one reference [ours]. ⛔ WHY NOT let the agent change C_base: every change would pass to every idea and be credited to the idea against E_base, as general training controls were in TeCh's case [App. B] [ours]. ⛔ WHY NOT a two-sided check: a stronger baseline makes every gain in the loop harder, never easier, since the loop's gains are against E_base (EI-17) [ours].
- **Decides.** A-BASE-1; U-BASE-2, its branch; A-FULL-1, its first half: who produces the full-set reference [ours].
- **Depends on.** U-INT-4, U-TOP-5 and U-SUB-2, task 6 [ours].
- **Test.** Logic, in mock mode: a run with three ideas calls the Baseline Coding Agent once and scores the baseline once; with the sealed check scripted to pass, round 0 starts and A_Coder's recorded input holds E_base and C_base; scripted to fail, the run ends with *baseline not reproduced* and no A_Coder call [ours]. Enforcement, on the toy task: a Baseline Coding Agent scripted to weaken the code it copies is refused, and E_base and every gain are unchanged; in the twin that scores the agent's copy as E_base, every gain grows by the weakening [ours].

### R-STG-4 · The idea experiment on the subset

- **Requirement.** The subset experiment runs with the SUB values [§3.2] [ours]:
  - **Veto.** The Subset Critic's `Good` stands only if the rule's subset entry passes over the harness's search-role records of the idea against E_base (R-RUN-6; U-INT-4, U-TOP-5); a `Good` it blocks counts as `Engineer` while the budget lasts, and the record says why [§3.2] [ours];
  - **Switches.** The idea's code declares its mechanism as switches in its configuration, which turn the mechanism off and leave every other change in place; a version that declares none cannot pass the veto. R-STG-9's control reads them [ours];
  - **Engineering.** The Subset Engineering Agent tunes and repairs code. It never adds, removes or replaces a component of the idea, which only A_FullEng does, in §3.4 and §3.6; a step that changes the idea's component list is refused and counted [§3.2] [§3.4] [§3.6] [ours];
  - **Scoring.** Each coding or engineering session ends with one scoring by the harness, and agent code cannot ask for one (IR-13) [ours].
- **Traces.** P-SUB-1 … 4 [§3.2]; P-CFG-3 [App. A.2]; P-ROSTER-7 … 9 [§3.2]; P-ROSTER-32 [Fig. 3] (image).
- **Departs from.** P-SUB-2: the critic's `Good` no longer decides alone [§3.2] [ours].
- **Why ours.** The critic's words, substantially inferior or consistently better, have no margin or test (U-SUB-1). The trigger for engineering is tuning or code adjustment, yet the one redesign in the artifacts replaced four components (A-ART-5); and an ablation that cannot turn the mechanism off cannot attribute a gain to it (EI-7) [§3.2] [p. 40] (image) [ours].
- **Decides.** U-SUB-1; A-ART-5 [ours].
- **Depends on.** U-INT-4 and U-TOP-5, task 6: the harness and the role it scores [ours].
- **Test.** Logic, in mock mode: a critic scripted as always `Engineer` gives 2 engineer calls, 3 critic calls and `Bad`; a `Good` whose fixture records pass the subset entry sends the idea to the full set; a `Good` whose records fail it leads to engineering, and after the budget to `Bad`, with *margin not met* in the record; a first `Bad` makes no engineer call; an engineer scripted to remove a component is refused, and the refusal is counted; a version that declares no switch cannot pass the veto [ours].

### R-STG-5 · The idea experiment on the full benchmark

- **Requirement.** The full-set experiment runs with the FULL values: the Full-Set Critic judges the idea against E_base on every full-set setting of the search role, R-STG-3's reference, behind the rule's full-set entry (R-RUN-6; U-INT-4, U-TOP-5), with at most 2 judged engineering refinements; a full-set `Bad` enters the traces as a failed idea. A published number is never an operand of a verdict, and appears only in reporting (IR-1) [§3.2] [Tab. 1] [ours].
- **Traces.** P-FULL-1 … 3 [§3.2]; P-CFG-14 [App. A.2]; P-ROSTER-10, P-ROSTER-11, P-ROSTER-12 [§3.2]; P-ROSTER-33, P-ROSTER-42 [Fig. 3] (image) [App. A.2].
- **Departs from.** P-FULL-3: the critic's `Good` no longer decides alone [§3.2] [ours].
- **Why ours.** §3.2 gives the full-set loop no verdicts and no limit, and Figure 5 draws the subset's loop again with *Good or Bad* (U-FULL-1, A-FULL-2) [§3.2] [Fig. 5] (image). Judging against the published number would credit an idea with any gap between the paper's machine and ours: in the one trace, 0.41 of a claimed 1.99 points came from a weaker reproduction [p. 41] [p. 42] (image) [ours].
- **Decides.** U-FULL-1; A-FULL-2; A-FULL-1, its second half: the critic's reference [ours].
- **Depends on.** U-INT-4 and U-TOP-5, task 6 [ours].
- **Test.** Logic, in mock mode: a critic scripted as always `Engineer` at full scale gives 2 engineer calls, 3 critic calls, and a trace with `Bad`; the critic's recorded input holds E_base on every full-set setting and no published number; a `Good` whose records fail the full-set entry leads to engineering [ours].

### R-STG-6 · A_Coder, one call per idea

- **Requirement.** A_Coder runs the subset stage and then, after a subset `Good`, the full-set stage, as one call per idea. It takes G, h, E_base and C_base, and returns the trace tuple (h, E^h, C^h, d^h, r^h), each E^h a record of the harness (U-INT-4) [§3.2, Eq. 2] [ours]. An idea pruned on the subset keeps in its trace at least its verdict and its feedback, the failure log that A_Evolve reads [§3.3]. The trace's further fields, and the unit of work, are task 3's (U-CODER-1, U-CFG-2) [ours].
- **Traces.** P-CODER-1 [§3.2, Eq. 2]; P-ROSTER-13 [§3.2]; P-STATE-6 [§3.2]; P-ROSTER-31 [Fig. 3] (image).
- **Decides.** A-BASE-1, the extended signature [ours].
- **Depends on.** U-CODER-1 and U-CFG-2, task 3; U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: an idea pruned on the subset yields a trace with `Bad` and non-empty feedback, which A_Evolve's next recorded input holds; an idea `Good` on both levels yields full-set results and code [ours].

### R-STG-7 · The idea rounds

- **Requirement.** The idea rounds run with the EVO values: round 0 runs the top 2 seeds; each later round runs one evolved idea and the next unevaluated seed, or the evolved idea alone once the seeds run out; the rounds stop at the end of the round in which the count of `Good` reaches 4, or after round 4; with no `Good` by then, the task ends with *no Good idea* [§3.3] [App. A.2] [ours]. Each evolved idea gets a novelty score, which is recorded and decides nothing [§3.3] [ours]. What A_Evolve reads, and whether candidates run in parallel, are task 3's (U-EVO-2, U-TOP-4) [ours].
- **Traces.** P-EVO-1 … 6 [§3.3]; P-CFG-4 … 7 [App. A.2]; P-CFG-13 [§3.3]; P-ROSTER-14 [§3.3]; P-STATE-7, P-STATE-8 [§3.3, Eq. 3].
- **Why ours.** N_0 has no value, and App. A.2's two candidates per round fit only the rounds after round 0 (A-EVO-1); Figure 9's rounds *Initial* to *Round 4* show four rounds after round 0 (A-EVO-2); a test after each round keeps the result independent of the order in which a round's ideas finish (U-EVO-1) [§3.3] [App. A.2] [Fig. 9b] (image) [ours]. The first draft also refused at load a pool too small for every round, which left the run-alone branch unreachable; the branch is kept, and the check dropped (SA-15) [ours].
- **Decides.** U-EVO-1; A-EVO-1; A-EVO-2; U-EVO-3; U-ART-11, for evolved ideas [ours].
- **Depends on.** U-EVO-2 and U-TOP-4, task 3 [ours].
- **Test.** Logic, in mock mode: with every idea `Bad` and N_seed = 6, 10 A_Coder calls and 4 evolver calls, then *no Good idea*; with 2 `Good` in round 0 and 2 in round 1, the rounds stop after 4 A_Coder calls and selection follows; when the 4th `Good` is the first candidate of round 2, that round's second candidate still runs; with N_seed = 4 and every idea `Bad`, rounds 3 and 4 each run the evolved idea alone, 8 A_Coder calls in all [ours].

### R-STG-8 · Selecting the best idea

- **Requirement.** The rule's band entry (R-RUN-6) ranks the `Good` ideas on the harness's search-role records (U-INT-4, U-TOP-5). If one leads by more than the band's margin, it is h_best; otherwise the Selector chooses among those within the margin of the leader, and its reason is recorded. A choice outside the band is replaced by the leader, and the override is recorded [§3.3, Eq. 4] [ours]. How much the Selector reads is task 3's (U-SEL-2) [ours].
- **Traces.** P-SEL-1 [§3.3, Eq. 4]; P-ROSTER-15 [§3.3]; P-STATE-9 [§3.3, Eq. 4].
- **Departs from.** P-SEL-1 and P-ROSTER-15: the Selector chooses only within the band [§3.3] [ours].
- **Why ours.** The Selector compares metrics and logs with no rule across datasets and metrics, no tie-break, and no weight for novelty (U-SEL-1) [§3.3] [ours].
- **Decides.** U-SEL-1 [ours].
- **Depends on.** U-SEL-2, task 3; U-INT-4 and U-TOP-5, task 6 [ours].
- **Test.** Logic, with fixture records: a clear leader is chosen whatever the mock Selector prefers; with two ideas within the margin, the mock Selector's choice stands and its reason is in the record; with a third idea outside the margin, a Selector scripted to choose it is overridden by the leader, and the override is recorded; shuffling the order of the inputs changes nothing [ours].

### R-STG-9 · Ablation, its control, and its one refinement

- **Requirement.** The ablation stage runs with the ABL values [§3.4] [ours]:
  - **Plans.** The Ablation Planner writes N_p plans, a value of task 5's (U-ABL-1), and one Ablation Coding Agent runs each on C_best; where their code lives is task 3's (U-ABL-3) [§3.4] [ours];
  - **Control.** Every pass also has a mechanism-off control, which the harness fits and scores from C_best with the idea's declared switches off and every other change kept; no agent writes or omits it (U-INT-4) [ours];
  - **Verdicts.** The Ablation Critic returns `Good`, `Refine` or `Reject`, reading what task 3 gives it (U-ABL-6), the dropped plans and their reasons included; `Reject` means that the gain is not attributable to the idea's mechanism [§3.4] [App. B] [ours];
  - **Precondition.** `Good` stands only if the control was scored and loses to C_best by at least the rule's ablation margin, on the search role (R-RUN-6; U-TOP-5); a `Good` it blocks counts as `Refine` [ours];
  - **Rubric.** A written rubric draws the line between `Refine` and `Reject`, and three cases from the paper are its first test cases: TeCh, p. 46 and LC-FTT [App. B] [p. 46] [Tab. 16] [ours];
  - **Refinement.** `Refine` calls A_FullEng once, and its code declares the switches of the mechanism it ships; the harness scores its result, and the guard of R-PRIM-6 decides [§3.4] [ours];
  - **After the guard.** If the guard accepts, the core state is replaced and the stage restarts at planning. If it rejects, or if a second `Refine` comes once N_abl is spent, drafting follows with the current h_best [§3.4] [Fig. 7] (image) [ours];
  - **A `Reject`.** Of the selected idea, it ends the task with *ablation reject*; of a candidate promoted in this downstream pass, it undoes the promotion, and the flow goes on as when the guard rejects [App. B] [ours];
  - **Novelty.** A refinement that replaces a component gets a new novelty score, and the idea's record keeps its lineage, whatever its name [p. 47] [ours].

  Whether a tuned-baseline control runs as well is task 6's (U-SUB-2) [ours].
- **Traces.** P-ABL-1 … 7 [§3.4] [Tab. 15]; P-CFG-8 [App. A.2]; P-CFG-15 [§3.4]; P-ROSTER-12 [§3.4]; P-ROSTER-16 … 19 [§3.4]; P-STATE-10, P-STATE-11 [§3.4]; P-ROSTER-34 [Fig. 3] (image).
- **Departs from.** P-ABL-3: the critic's `Good` no longer decides alone [§3.4] [ours].
- **Why ours.** §3.4 gives no reject, yet App. B reports one that ended a task (A-ABL-1); Figure 7 sends a failed comparison to drafting (A-ABL-2); Figure 3 sends a refined idea back through the full-set loop, which would add sessions under no stated limit (U-ABL-2) [§3.4] [App. B] [Fig. 7] [Fig. 3] (image). In TeCh's case the critic found the gains driven by general training controls, and on p. 41 the agent's report calls every component useful beside a table in which two of them make the result worse; a control that turns only the mechanism off measures what the critic is asked (EI-7) [App. B] [p. 41] (image) [ours]. ⛔ WHY NOT fall back to the next `Good` idea after a `Reject`: the paper's one case ended the task, and a fall-back adds a loop the paper never describes, on an idea the Selector ranked lower [App. B] [ours].
- **Decides.** A-ABL-1; A-ABL-2; U-ABL-2; U-ABL-5; A-TOP-1, its cell U-ABL-4; U-ART-11, for refined ideas [ours].
- **Depends on.** U-ABL-1, task 5; U-ABL-3 and U-ABL-6, task 3; U-INT-4, U-TOP-5 and U-SUB-2, task 6 [ours].
- **Test.** Logic, in mock mode, with N_p = 3 and scripted verdicts, guard and control records [ours]:
  - `Good`, with the control losing beyond the margin: one planner call, 3 coder calls, one control scoring, drafting next [ours];
  - `Good`, with the control within the margin: counted as `Refine` [ours];
  - `Refine`, guard accepts, then `Good`: two planner calls, one A_FullEng call, drafting with the new h_best [ours];
  - `Refine`, guard rejects: drafting with the old h_best [ours];
  - `Refine`, accepted, then `Refine` again: drafting with the promoted h_best, and no second A_FullEng call [ours];
  - `Reject` of the selected idea ends the task with *ablation reject*; `Reject` after a promotion leads to drafting with the idea as it was before it [ours].

  Enforcement, on the toy task: an Ablation Coding Agent scripted to write a weakened control of its own changes no control result, while in the twin whose control is the agent's the blocked `Good` passes [ours].

### R-STG-10 · Drafting

- **Requirement.** The Initial Drafter, wrapping PaperOrchestra, writes the manuscript in the ICLR 2025 format from h_best and the verified results table, which holds the main, ablation and control results (R-STATE-10; U-INT-4) [§3.5] [App. A.2] [ours]. Every figure that shows a result is rendered by engine code from the table's entries; a figure the writer draws is a diagram and carries no measurement [ours]. The manuscript hooks run after the draft and after every revision: compile, number provenance, references, then method–code alignment (R-INT-10; A-INT-1) [§4.2] [ours]. What the drafter reads is task 3's (U-DRAFT-1), and the check of consistency before export is task 6's (A-ART-7) [ours].
- **Traces.** P-DRAFT-1 [§3.5]; P-CFG-18 [App. A.2]; P-ROSTER-20 [§3.5]; P-ART-9 [pp. 56–71]; P-STATE-12 [§3.5].
- **Why ours.** The paper does not cover a draft that fails to compile, or say who makes the first figures, and App. D's figure is a raster diagram unlike the method it shows (U-DRAFT-2); a figure drawn from a raw result file can show a number the table does not hold (EI-5) [§3.5] [p. 59] (image) [ours].
- **Decides.** U-DRAFT-2 [ours].
- **Depends on.** U-DRAFT-1, task 3; A-ART-7, A-INT-1 and U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: a draft built from fixture entries compiles in the ICLR 2025 template; a draft scripted to fail compilation is repaired by the writer within the hook's bound, and the failure is recorded; every figure that shows a result names the entries it was rendered from, and a figure scripted to plot a number read from a raw result file fails the number-provenance hook [ours].

### R-STG-11 · Peer review and rebuttal

- **Requirement.** The review stage runs with the PEER values: below a score of 8, a rebuttal cycle plans N_t tasks, a value of task 5's (U-PEER-1), runs each on C_best, and revises the manuscript, which is then reviewed again; at most two cycles run, so at most three reviews. The last manuscript passes on, never the best-scoring one [§3.5] [App. A.2] [Tab. 5] [ours]. Besides [ours]:
  - **Rebuttal data.** Each rebuttal task declares its evaluation before it runs, from settings the manifest registers, and the harness scores it on the search role (U-INT-4, U-TOP-5); a task that names any other data is refused [§3.5] [ours];
  - **Every row kept.** Every rebuttal result enters the verified results table whatever its sign, and the export record lists the rows the manuscript does not cite [ours];
  - **Reviews.** Every review is kept raw. The reviewer is R-AGT-5's, which task 4 chooses (U-PEER-3), and the threshold's calibration is task 6's (A-EVAL-3) [§3.5] [ours];
  - **Scope.** What the Enhancer may change is task 3's (U-PEER-4) [ours].
- **Traces.** P-PEER-1 … 6 [§3.5]; P-CFG-9, P-CFG-10 [App. A.2]; P-CFG-16 [§3.5]; P-ROSTER-21 … 24 [§3.5]; P-STATE-12, P-STATE-13, P-STATE-14 [§3.5].
- **Why ours.** Table 5's review rounds 0, 1 and 2 fit two rebuttal cycles (A-PEER-1); keeping the best-scoring round would add a selection on the reviewer the loop optimises against (U-TOP-7) [Tab. 5] [§4] [ours]. The one rebuttal shown chose its own datasets and test caps, which no stage defines, and a rebuttal that reports only its favourable rows leaves no trace of the others (EI-6) [p. 51] (image) [ours].
- **Decides.** A-PEER-1; A-TOP-1, its cell U-TOP-7 [ours].
- **Depends on.** U-PEER-1, task 5; U-PEER-3, task 4; U-PEER-4, task 3; A-EVAL-3, U-INT-4 and U-TOP-5, task 6 [ours].
- **Test.** Logic, in mock mode: reviews scripted at 6, 7 and 7 give 2 rebuttal cycles, 3 reviews, and the third manuscript passes on; at 6, then 9, one cycle, and the manuscript reviewed at 9 passes on; at 8, no rebuttal; a rebuttal task that names an unregistered dataset is refused before it runs; a rebuttal row with a negative result is in the verified table, and the export record lists it when the manuscript leaves it out [ours].

### R-STG-12 · Meta-review, and the downstream restart

- **Requirement.** The meta stage runs with the META values [§3.6] [ours]:
  - **Rubric.** The Meta-Reviewer judges against a written rubric for the venue bar, and reads the verified results table besides the manuscript and the last review; until the test event, the manuscript's numbers are search-role numbers (IR-16; U-TOP-5, U-INT-4) [§3.6] [Tab. 1] [ours];
  - **Restart.** `Refine` calls A_FullEng, and the guard of R-PRIM-6 decides. If it accepts, a new downstream pass starts at ablation planning, with the ablation critic included and fresh N_abl and N_peer counters, and the Meta-Reviewer is asked again at its end [§3.6] [Fig. 7] (image) [ours];
  - **End.** `Accept` leads to the tail (R-RUN-7). After a second `Refine`, or after a refinement the guard rejects, the tail runs with the last P_new and C_best, and the export is marked unapproved; every export carries its last meta verdict [§3.6] [ours].
- **Traces.** P-META-1 … 7 [§3.6]; P-CFG-11 [App. A.2]; P-ROSTER-25 [§3.6]; P-STATE-15 [§3.6].
- **Why ours.** §3.6's restart names no ablation critic, while Figure 7's path runs through it (A-META-1); the paper does not say whether the Meta-Reviewer is asked again (A-META-2), whether budgets reset (U-META-1), or what the Meta-Reviewer judges by (U-META-2); and a run can export a paper the Meta-Reviewer had just returned as `Refine`, against the loop until approval of §3 (A-TOP-3) [§3] [§3.6] [Fig. 7] (image) [ours].
- **Decides.** A-META-1; A-META-2; U-META-1; U-META-2; A-TOP-3; A-TOP-1, its meta-review cell [ours].
- **Depends on.** U-INT-4 and U-TOP-5, task 6 [ours].
- **Test.** Logic, in mock mode, with scripted verdicts and guard [ours]:
  - `Accept`: the tail, then an accepted export, after one meta call [ours];
  - `Refine`, guard accepts, `Accept`: a second pass from ablation planning, then an accepted export [ours];
  - `Refine`, guard accepts, and the Ablation Critic scripted to `Refine` in the second pass: one more A_FullEng call follows, which shows the counters are fresh [ours];
  - `Refine`, guard accepts, `Refine`: an export marked unapproved, and no further A_FullEng call [ours];
  - `Refine`, guard rejects: the first pass's outputs exported, marked unapproved [ours].

### R-STG-13 · App. A.2's values are the defaults, and nothing is guessed

- **Requirement.** The default configuration holds App. A.2's values: 16 rounds of limitation extraction, 2 reference papers, N_eng = 2, N_k = N_e = 1, K = 4, S = 4, N_abl = 1, the threshold 8, N_peer = 2, N_meta = 1 and the ICLR 2025 format. It adds our values: the full-set limit, 2; N_0 = 2; and 2 repairs per manuscript hook. N_seed, N_p and N_t have no default, and the configuration refuses to load until task 5 sets them (U-SEED-1, U-ABL-1, U-PEER-1) [App. A.2] [ours].
- **Traces.** P-CFG-1 … 16, P-CFG-18 [App. A.2].
- **Why ours.** An unset value filled silently would pass as the paper's; CLAUDE.md records an unknown as unknown [ours].
- **Depends on.** U-SEED-1, U-ABL-1 and U-PEER-1, task 5 [ours].
- **Test.** Logic: loading the default configuration yields exactly the values above; with N_p removed, loading fails, and the message names U-ABL-1 [ours].
