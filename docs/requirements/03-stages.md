# Requirements 3 · The stages, as configurations of the one primitive

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
Each stage below is a set of values for the parameters of [02-primitive.md](02-primitive.md), never
a loop of its own [§3] [ours]. The table states every value once; each requirement after it adds
what a value alone cannot say, and its test [ours].

## The default stage configuration

The values come from the paper where it gives them, and are our decisions where it does not; each
cell says which [Tab. 1] [App. A.2] [ours]. A value set by another task is named, never guessed: N_seed,
N_p and N_t are task 5's, and the configuration refuses to load without them (R-STG-13) [ours]. Three
checks run at points that no stage owns: the specification filter after every experiment (R-INT-4),
and the reference check and the method–code audit after every manuscript revision (R-INT-5,
R-INT-6) [§4.2] [ours].

| Stage | Generator | Judged → refined, by | Assessor and rule | Verdict map | Guard, on failure | Limit: counts, value | At the limit | Nesting, fan-out |
|---|---|---|---|---|---|---|---|---|
| LIM | Limitation Extractor, from G [§3.1] | the set → the set, expanded by the Extractor with the Verifier's list of what is missing [§3.1] [ours] | Limitation Verifier, an LLM verdict: sufficient or not [§3.1] | sufficient → accept; insufficient → refine; no reject [§3.1] | none [§3.1] | judged refinements, 16 [App. A.2] | keep the last set, flagged [ours] | none [§3.1] |
| SEED | the initial idea, then the Idea Generator, from G, the limitations and the scored pool [§3.1] [Fig. 4] (image) [ours] | each new idea joins the pool [§3.1] | Novelty Checker, with two papers from search: a score, no verdict [§3.1] [App. A.2] | none: every idea is kept, ranked by its score [§3.1] [ours] | none [§3.1] | a count stop: the pool holds N_seed ideas, set by task 5, at least N_0 + K·N_e [§3.1] [ours] | keep the whole pool, sorted by score, descending [§3.1] | one idea at a time, since each new idea sees the pool [§3.1] [ours] |
| BASE | Baseline Coding Agent, on the subset and on the full benchmark [§3.2] [ours] | nothing is refined [Tab. 1] | a deterministic check: the harness's baseline results within the manifest's tolerance of its reference numbers [ours] | within → accept; outside → stop the run, *baseline not reproduced* [ours] | none [Tab. 1] | zero refinements; a tuning refine is task 6's to add (U-SUB-2) [Tab. 1] [ours] | not applicable [Tab. 1] | once per task, before round 0 [§3.2] [ours] |
| SUB | Subset Coding Agent, from h and C_base [§3.2] | E_sub^h against E_base → h and C_sub^h, by the Subset Engineering Agent, which tunes and repairs only [§3.2] [ours] | Subset Critic, an LLM verdict under a numeric veto: no `Good` unless the harness's validation gain over E_base exceeds the task's margin [§3.2] [ours] | `Good` → accept; `Engineer` → refine; `Bad` → reject; a vetoed `Good` → `Engineer` [§3.2] [ours] | none [§3.2] | judged refinements, N_eng = 2 [App. A.2] | discard: `Bad`, pruned [§3.2] | inside A_Coder, once per idea [§3.2, Eq. 2] |
| FULL | Full-Set Coding Agent, adapting C_sub^h to the manifest's full benchmark [§3.2] [ours] | the full results against the reproduced full-set baseline → h and C, by the Full-Set Engineer, which tunes and repairs only [§3.2] [ours] | Full-Set Critic, an LLM verdict under the same numeric veto [§3.2] [ours] | as the subset row [Fig. 5] (image) [ours] | none [§3.2] | judged refinements, 2 [App. A.2] [ours] | discard: `Bad`, kept in the traces [ours] | inside A_Coder, after a subset `Good` [§3.2] |
| EVO | round 0: the top N_0 = 2 seeds; round k ≥ 1: one idea from A_Evolve over all traces, and the next unevaluated seed [§3.3] [App. A.2] [ours] | the candidates, rebuilt each round from all traces [§3.3] | A_Coder's verdict per candidate, and the count of `Good` over all rounds [§3.3] | `Good` → counted; `Bad` → kept as a trace [§3.3] | none [§3.3] | rounds after round 0, K = 4; a count stop at S = 4 `Good`, tested at the end of each round [§3.3] [App. A.2] [ours] | with at least one `Good`, go to selection; with none, stop the run [§3.3] | A_Coder per candidate, two per round; the evolved idea alone once the seeds run out [App. A.2] [ours] |
| SEL | none: every `Good` tuple from every round [§3.3, Eq. 4] | nothing is refined [Tab. 1] | the task's validation metric ranks the `Good` ideas; the Selector, an LLM, chooses among those within the task's margin of the best, and records why [§3.3] [ours] | a choice [§3.3, Eq. 4] | none [§3.3] | zero refinements [Tab. 1] | not applicable [Tab. 1] | once per run [§3.3] |
| ABL | Ablation Planner, N_p plans set by task 5; one Ablation Coding Agent per plan, on C_best [§3.4] [ours] | E_abl → h_best, by one A_FullEng call whose results the harness scores [§3.4] [ours] | Ablation Critic, an LLM verdict under a written attribution rubric [§3.4] [App. B] [ours] | `Good` → accept; `Refine` → refine; `Reject` → stop the run, *ablation reject* [§3.4] [App. B] [ours] | R-PRIM-6, E_new against E_best; on failure, go on to drafting with the unchanged h_best [§3.4] [Fig. 7] (image) [ours] | judged refinements, N_abl = 1 per downstream pass [App. A.2] [ours] | keep the current best, and go on to drafting [§3.4] [ours] | a fan-out over the N_p plans; after a promotion the stage restarts at planning [§3.4] |
| DRAFT | Initial Drafter, with PaperOrchestra, from h_best and the verified results table [§3.5] [ours] | nothing is refined [Tab. 1] | a compile-and-format check [ours] | pass → accept; a failure is repaired under the retry policy, R-OPS-7 [ours] | none [Tab. 1] | zero refinements [Tab. 1] | not applicable [Tab. 1] | once per downstream pass [§3.6] |
| PEER | the draft [§3.5] | P_new → P_new, by the Rebuttal Planner (N_t tasks, set by task 5), one Rebuttal Coding Agent per task, and the Paper Enhancer [§3.5] [ours] | ScholarPeer's score, against the threshold 8 [§3.5] [App. A.2] | 8 or more → accept; below 8 → refine; no reject [§3.5] | none: each revision replaces P_new [§3.5] | judged refinements, N_peer = 2 rebuttal cycles, so up to three reviews [App. A.2] [Tab. 5] [ours] | keep the last manuscript, never the best-scoring one [§3.5] [ours] | a fan-out over the N_t tasks of each cycle [§3.5] |
| META | the peer stage's last P_new and R_new [§3.6] | P_new and R_new → h_best, by A_FullEng; then a new downstream pass [§3.6] | Meta-Reviewer, an LLM verdict under a written venue-bar rubric, which also reads the verified results table [§3.6] [ours] | `Accept` → export; `Refine` → refine; no reject [§3.6] | R-PRIM-6, strictly superior; on failure, export the previous outputs, unapproved [§3.6] [ours] | judged refinements, N_meta = 1 [App. A.2] | export the last pass's P_new and C_best, unapproved [§3.6] [ours] | its refine nests a whole downstream pass, with fresh budgets; the Meta-Reviewer is asked again after it [§3.6] [Fig. 7] (image) [ours] |

## The stages

### R-STG-1 · Finding limitations

- **Requirement.** The limitation stage runs with the LIM values: the Extractor's set is judged by the Verifier, expanded while the Verifier finds it insufficient, and passed on after at most 16 judged refinements, flagged if the limit was reached [§3.1] [App. A.2] [ours].
- **Traces.** P-LIM-1 … 4 [§3.1]; P-CFG-1 [App. A.2]; P-ROSTER-1, P-ROSTER-2 [§3.1].
- **Why ours.** The paper does not say what passes on at the limit; the next paragraph works from the limitations found, so the set passes on (A-LIM-1) [§3.1] [ours].
- **Decides.** A-TOP-1, its cell A-LIM-1 [ours].
- **Depends on.** U-LIM-1, task 3: the Verifier's criterion and the limitation record [ours].
- **Test.** In mock mode, a Verifier scripted as always insufficient: 17 Extractor calls, 17 Verifier calls, and the 17th set passes on, flagged. Scripted as sufficient at once: one call of each, no flag [ours].

### R-STG-2 · Seed ideas

- **Requirement.** The seed stage runs with the SEED values. Every idea gets a novelty score from two retrieved papers, and no idea is dropped for low novelty: the score only ranks [§3.1] [App. A.2] [ours]. The Idea Generator reads G, the limitations and the scored pool so far, under a written content rule that excludes pure compute or budget scaling [§3.1] [App. B] [ours]. The configuration refuses an N_seed below N_0 + K·N_e, so that every round finds a seed [§3.3] [ours].
- **Traces.** P-SEED-1 … 4 [§3.1]; P-CFG-2 [App. A.2]; P-CFG-12 [§3.1]; P-ROSTER-3 … 5 [§3.1] [Fig. 4] (image).
- **Why ours.** §3 says ideas are filtered for novelty while §3.1 only sorts (A-SEED-1); we keep §3.1's ranking, and a threshold stays an optional ablation. App. B says the generator does not propose compute scaling, and no inputs are named (U-SEED-3) [§3] [§3.1] [App. B] [ours].
- **Decides.** A-SEED-1; U-SEED-3; U-EVO-3, its configuration check [ours].
- **Depends on.** U-SEED-1, task 5, the value of N_seed; U-SEED-2 and A-SEED-2, task 3, the score's scale and whether the first idea has an agent of its own [ours].
- **Test.** In mock mode, with N_seed = 6 and scripted scores: the pool holds exactly 6 ideas, sorted by score, descending, each with two references, and the lowest-scoring idea is still in it; the Idea Generator's recorded input holds G, the limitations and the scored pool. A configuration with N_seed = 5, N_0 = 2, K = 4 and N_e = 1 fails to load [ours].

### R-STG-3 · The baseline, reproduced once per task

- **Requirement.** The baseline runs once per task, before round 0, on the subset and on the full benchmark. A_Coder receives its results and code as inputs, a recorded extension of Eq. 2 [§3.2] [§3.2, Eq. 2] [ours]. The harness checks the baseline against the manifest's reference numbers within the manifest's tolerance; outside it, the task ends with the outcome *baseline not reproduced* and no idea runs [ours].
- **Traces.** P-BASE-1 [§3.2]; P-STATE-5 [§3.2]; P-ROSTER-6 [§3.2].
- **Why ours.** The paper runs the baseline first, on the subset, with no check (U-BASE-2); Figure 5 draws it inside each idea's pipeline (A-BASE-1); and no stage produces the full-set reference that Table 1's full-set critic compares with (A-FULL-1) [§3.2] [Fig. 5] (image) [Tab. 1]. Once per task saves up to 9 coding sessions a run, and gives every idea the same reference [ours].
- **Decides.** A-BASE-1; U-BASE-2; A-FULL-1, its first half: who produces the full-set reference [ours].
- **Depends on.** U-SUB-2, task 6, whether the baseline gets a tuning budget; U-INT-4, task 6, the harness [ours].
- **Test.** In mock mode, a run with three ideas calls the Baseline Coding Agent once. With fixture baseline results inside the tolerance, round 0 starts; outside it, the run ends with *baseline not reproduced* and no A_Coder call [ours].

### R-STG-4 · The idea experiment on the subset

- **Requirement.** The subset experiment runs with the SUB values. The Subset Critic's `Good` stands only if the harness's validation gain over E_base exceeds the task's margin; a `Good` that fails this test counts as `Engineer` while the budget lasts, and the record says why [§3.2] [ours]. The Subset Engineering Agent tunes and repairs code; it never replaces a component of the idea, which only A_FullEng does, in §3.4 and §3.6 [§3.2] [§3.4] [§3.6] [ours].
- **Traces.** P-SUB-1 … 4 [§3.2]; P-CFG-3 [App. A.2]; P-ROSTER-7 … 9 [§3.2].
- **Why ours.** The critic's words, substantially inferior or consistently better, have no margin or test (U-SUB-1). The trigger for engineering is tuning or code adjustment, yet the one redesign in the artifacts replaced four components (A-ART-5) [§3.2] [p. 40] (image) [ours].
- **Decides.** U-SUB-1; A-ART-5 [ours].
- **Depends on.** U-TOP-5 and U-INT-4, task 6: the validation split and the harness; the margin is a manifest field that task 5 fills [ours].
- **Test.** In mock mode: a critic scripted as always `Engineer` gives 2 engineer calls, 3 critic calls and `Bad`; a `Good` with the fixture gain above the margin sends the idea to the full set; a `Good` with the gain below the margin leads to engineering, and after the budget to `Bad`, with *margin not met* in the record; a first `Bad` makes no engineer call [ours].

### R-STG-5 · The idea experiment on the full benchmark

- **Requirement.** The full-set experiment runs with the FULL values: the Full-Set Critic judges against the full-set baseline reproduced by R-STG-3, under the subset's verdicts and numeric veto, with at most 2 judged engineering refinements; a full-set `Bad` enters the traces as a failed idea. The paper's published numbers sit beside the reproduced baseline in the record, for reporting only [§3.2] [Tab. 1] [ours].
- **Traces.** P-FULL-1 … 3 [§3.2]; P-CFG-14 [App. A.2]; P-ROSTER-10, P-ROSTER-11, P-ROSTER-12 [§3.2].
- **Why ours.** §3.2 gives the full-set loop no verdicts and no limit, and Figure 5 draws the subset's loop again with *Good or Bad* (U-FULL-1, A-FULL-2) [§3.2] [Fig. 5] (image). Judging against the published number would credit an idea with any gap between the paper's machine and ours: in the one trace, 0.41 of a claimed 1.99 points came from a weaker reproduction [p. 41] [p. 42] (image) [ours].
- **Decides.** U-FULL-1; A-FULL-2; A-FULL-1, its second half: the critic's reference [ours].
- **Depends on.** U-TOP-5 and U-INT-4, task 6 [ours].
- **Test.** In mock mode, a critic scripted as always `Engineer` at full scale gives 2 engineer calls, 3 critic calls, and a trace with `Bad`; the critic's recorded input holds the reproduced full-set baseline, and the record holds the published numbers beside it [ours].

### R-STG-6 · A_Coder, one call per idea

- **Requirement.** A_Coder runs the subset stage and then, after a subset `Good`, the full-set stage, as one call per idea. It takes G, h and the baseline's results and code, and returns the trace tuple (h, E^h, C^h, d^h, r^h). An idea pruned on the subset keeps in its trace its verdict, its feedback, its subset results and its code version, since A_Evolve reads the failure logs of `Bad` ideas [§3.2, Eq. 2] [§3.3] [ours].
- **Traces.** P-CODER-1 [§3.2, Eq. 2]; P-ROSTER-13 [§3.2]; P-STATE-6 [§3.2].
- **Decides.** A-BASE-1, the extended signature [ours].
- **Depends on.** U-CODER-1 and U-CFG-2, task 3: the trace record and the unit of work [ours].
- **Test.** In mock mode, an idea pruned on the subset yields a trace with `Bad`, non-empty feedback, its subset results and the ID of its code version; an idea `Good` on both levels yields full-set results and code [ours].

### R-STG-7 · The idea rounds

- **Requirement.** The idea rounds run with the EVO values: round 0 runs the top 2 seeds; each later round runs one evolved idea and the next unevaluated seed; the rounds stop at the end of the round in which the count of `Good` reaches 4, or after round 4; with no `Good` by then, the task ends with *no Good idea* [§3.3] [App. A.2] [ours]. Once the seeds run out, the evolved idea runs alone. Each evolved idea gets a novelty score, which is recorded and decides nothing [§3.3] [ours].
- **Traces.** P-EVO-1 … 6 [§3.3]; P-CFG-4 … 7 [App. A.2]; P-CFG-13 [§3.3]; P-ROSTER-14 [§3.3]; P-STATE-7, P-STATE-8 [§3.3, Eq. 3].
- **Why ours.** N_0 has no value, and App. A.2's two candidates per round fit only the rounds after round 0 (A-EVO-1); Figure 9's rounds *Initial* to *Round 4* show four rounds after round 0 (A-EVO-2); a test after each round keeps the result independent of the order in which a round's ideas finish (U-EVO-1) [§3.3] [App. A.2] [Fig. 9b] (image) [ours].
- **Decides.** U-EVO-1; A-EVO-1; A-EVO-2; U-EVO-3; U-ART-11, for evolved ideas [ours].
- **Depends on.** U-EVO-2, task 3, what A_Evolve reads; U-TOP-4, task 3, parallel candidates [ours].
- **Test.** In mock mode: with every idea `Bad`, 10 A_Coder calls and 4 evolver calls, then *no Good idea*; with 2 `Good` in round 0 and 2 in round 1, the rounds stop after 4 A_Coder calls and selection follows; when the 4th `Good` is the first candidate of round 2, that round's second candidate still runs [ours].

### R-STG-8 · Selecting the best idea

- **Requirement.** The task's validation metric ranks the `Good` ideas. If one leads by more than the task's margin, it is h_best; otherwise the Selector chooses among those within the margin of the best, and its reason is recorded [§3.3, Eq. 4] [ours].
- **Traces.** P-SEL-1 [§3.3, Eq. 4]; P-ROSTER-15 [§3.3]; P-STATE-9 [§3.3, Eq. 4].
- **Why ours.** The Selector compares metrics and logs with no rule across datasets and metrics, no tie-break, and no weight for novelty (U-SEL-1) [§3.3] [ours].
- **Decides.** U-SEL-1 [ours].
- **Depends on.** U-SEL-2, task 3, how much the Selector reads; U-TOP-5, task 6 [ours].
- **Test.** With fixture results, a clear leader is chosen whatever the mock Selector prefers; with two ideas within the margin, the mock Selector's choice stands and its reason is in the record [ours].

### R-STG-9 · Ablation, and its one refinement

- **Requirement.** The ablation stage runs with the ABL values [§3.4] [ours]:
  - **Verdicts.** The Ablation Critic returns `Good`, `Refine` or `Reject`; `Reject` means that the gain is not attributable to the idea's mechanism, and it ends the task with *ablation reject* [§3.4] [App. B] [ours].
  - **Rubric.** A written rubric draws the line between `Refine` and `Reject`, and three cases from the paper are its first test cases: TeCh, p. 46 and LC-FTT [App. B] [p. 46] [Tab. 16] [ours].
  - **Refinement.** `Refine` calls A_FullEng once; the harness scores its result, and the guard of R-PRIM-6 decides [§3.4] [ours].
  - **After the guard.** If the guard accepts, the core state is replaced and the stage restarts at planning. If it rejects, or if a second `Refine` comes once N_abl is spent, drafting follows with the current h_best [§3.4] [Fig. 7] (image) [ours].
  - **Novelty.** A refinement that replaces a component gets a new novelty score, and the idea's record keeps its lineage, whatever its name [p. 47] [ours].
- **Traces.** P-ABL-1 … 7 [§3.4] [Tab. 15]; P-CFG-8 [App. A.2]; P-CFG-15 [§3.4]; P-ROSTER-12 [§3.4]; P-ROSTER-16 … 19 [§3.4]; P-STATE-10, P-STATE-11 [§3.4].
- **Why ours.** §3.4 gives no reject, yet App. B reports one that ended a task (A-ABL-1); Figure 7 sends a failed comparison to drafting (A-ABL-2); Figure 3 sends a refined idea back through the full-set loop, which would add sessions under no stated limit (U-ABL-2) [§3.4] [App. B] [Fig. 7] [Fig. 3] (image). ⛔ WHY NOT fall back to the next `Good` idea after a `Reject`: the paper's one case ended the task, and a fall-back adds a loop the paper never describes, on an idea the Selector ranked lower [App. B] [ours].
- **Decides.** A-ABL-1; A-ABL-2; U-ABL-2; U-ABL-5; A-TOP-1, its cell U-ABL-4; U-ART-11, for refined ideas [ours].
- **Depends on.** U-ABL-1, task 5, the value of N_p; U-ABL-3 and U-ABL-6, task 3, where ablation code lives and what the critic reads [ours].
- **Test.** In mock mode, with N_p = 3 and scripted verdicts and guard [ours]:
  - `Good`: one planner call, 3 coder calls, drafting next [ours];
  - `Refine`, guard accepts, then `Good`: two planner calls, one A_FullEng call, drafting with the new h_best [ours];
  - `Refine`, guard rejects: drafting with the old h_best [ours];
  - `Refine`, accepted, then `Refine` again: drafting with the promoted h_best, and no second A_FullEng call [ours];
  - `Reject`: the task ends with *ablation reject* [ours].

### R-STG-10 · Drafting

- **Requirement.** The Initial Drafter, wrapping PaperOrchestra, writes the manuscript in the ICLR 2025 format from h_best and the verified results table, which holds the main and ablation results [§3.5] [App. A.2] [ours]. A compile-and-format check runs after the draft and after every revision, and every figure is made by a script from result files [ours].
- **Traces.** P-DRAFT-1 [§3.5]; P-CFG-18 [App. A.2]; P-ROSTER-20 [§3.5]; P-ART-9 [pp. 56–71]; P-STATE-12 [§3.5].
- **Why ours.** The paper does not cover a draft that fails to compile, or say who makes the first figures, and App. D's figure is a raster diagram unlike the method it shows (U-DRAFT-2) [§3.5] [p. 59] (image) [ours].
- **Decides.** U-DRAFT-2 [ours].
- **Depends on.** U-DRAFT-1, task 3, the drafter's inputs; A-ART-7, task 6, the consistency check before export [ours].
- **Test.** In mock mode, a draft built from fixture results compiles in the ICLR 2025 template; a draft scripted to fail compilation is repaired under the retry policy, and the failure is recorded; every figure in the draft has a recorded script and the result files it read [ours].

### R-STG-11 · Peer review and rebuttal

- **Requirement.** The review stage runs with the PEER values: below a score of 8, a rebuttal cycle plans N_t tasks, runs each on C_best, and revises the manuscript, which is then reviewed again; at most two cycles run, so at most three reviews. The last manuscript passes on, never the best-scoring one [§3.5] [App. A.2] [Tab. 5] [ours]. Every review is kept raw in the record [ours].
- **Traces.** P-PEER-1 … 6 [§3.5]; P-CFG-9, P-CFG-10 [App. A.2]; P-CFG-16 [§3.5]; P-ROSTER-21 … 24 [§3.5]; P-STATE-12, P-STATE-13, P-STATE-14 [§3.5].
- **Why ours.** Table 5's review rounds 0, 1 and 2 fit two rebuttal cycles (A-PEER-1); keeping the best-scoring round would add a selection on the reviewer the loop optimises against (U-TOP-7) [Tab. 5] [§4] [ours].
- **Decides.** A-PEER-1; A-TOP-1, its cell U-TOP-7 [ours].
- **Depends on.** U-PEER-1, task 5, the value of N_t; U-PEER-3, task 4, ScholarPeer; U-PEER-4, task 3, what the Enhancer may change; A-EVAL-3, task 6, the threshold's calibration [ours].
- **Test.** In mock mode, reviews scripted at 6, 7 and 7: 2 rebuttal cycles, 3 reviews, and the third manuscript passes on. Scripted at 6, then 9: one cycle, and the manuscript reviewed at 9 passes on. Scripted at 8: no rebuttal [ours].

### R-STG-12 · Meta-review, and the downstream restart

- **Requirement.** The meta stage runs with the META values [§3.6] [ours]:
  - **Rubric.** The Meta-Reviewer judges against a written rubric for the venue bar, and reads the verified results table besides the manuscript and the last review [§3.6] [Tab. 1] [ours].
  - **Restart.** `Refine` calls A_FullEng, and the guard of R-PRIM-6 decides. If it accepts, a new downstream pass starts at ablation planning, with the ablation critic included and fresh N_abl and N_peer counters, and the Meta-Reviewer is asked again at its end [§3.6] [Fig. 7] (image) [ours].
  - **Export.** Every export carries the last meta verdict. After a second `Refine`, or after a refinement the guard rejects, the last P_new and C_best are exported and marked unapproved [§3.6] [ours].
- **Traces.** P-META-1 … 7 [§3.6]; P-CFG-11 [App. A.2]; P-ROSTER-25 [§3.6]; P-STATE-15 [§3.6].
- **Why ours.** §3.6's restart names no ablation critic, while Figure 7's path runs through it (A-META-1); the paper does not say whether the Meta-Reviewer is asked again (A-META-2), whether budgets reset (U-META-1), or what the Meta-Reviewer judges by (U-META-2); and a run can export a paper the Meta-Reviewer had just returned as `Refine`, against the loop until approval of §3 (A-TOP-3) [§3] [§3.6] [Fig. 7] (image) [ours].
- **Decides.** A-META-1; A-META-2; U-META-1; U-META-2; A-TOP-3; A-TOP-1, its meta-review cell [ours].
- **Test.** In mock mode, with scripted verdicts and guard [ours]:
  - `Accept`: an accepted export after one meta call [ours];
  - `Refine`, guard accepts, `Accept`: a second pass from ablation planning, with fresh counters, then an accepted export [ours];
  - `Refine`, guard accepts, `Refine`: an export marked unapproved, and no second A_FullEng call [ours];
  - `Refine`, guard rejects: the first pass's outputs exported, marked unapproved [ours].

### R-STG-13 · App. A.2's values are the defaults, and nothing is guessed

- **Requirement.** The default configuration holds App. A.2's values: 16 limitation rounds, 2 reference papers, N_eng = 2, N_k = N_e = 1, K = 4, S = 4, N_abl = 1, the threshold 8, N_peer = 2, N_meta = 1 and the ICLR 2025 format. It adds our values for the full-set limit, 2, and N_0 = 2. N_seed, N_p and N_t have no default, and the configuration refuses to load until task 5 sets them [App. A.2] [ours].
- **Traces.** P-CFG-1 … 16, P-CFG-18 [App. A.2].
- **Why ours.** An unset value filled silently would pass as the paper's; CLAUDE.md records an unknown as unknown [ours].
- **Depends on.** U-SEED-1, U-ABL-1 and U-PEER-1, task 5 [ours].
- **Test.** Loading the default configuration yields exactly the values above; with N_p removed, loading fails, and the message names U-ABL-1 [ours].
