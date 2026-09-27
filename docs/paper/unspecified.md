# What the paper leaves open: the decision register

**For** tasks 2 to 7. Every question that ScientistTwo (arXiv:2609.19644v1) leaves open, stated once, with the decision it forces on us and the task that owns that decision [ours]. Four analysts filed 133 gap items (`U-` and `A-` IDs) in the gap sections of [analysis.md](analysis.md) (section 10), [stages/](stages/), [claims.md](claims.md), [note-check.md](note-check.md) and [artifacts.md](artifacts.md); this register merges them into 88 decisions [ours]. The full entries, with their quotes, stay where they were filed, as [README.md](README.md) prescribes; every row points to them [ours].

**Control.** `python3 playground/paper/register_coverage.py` checks that every defined ID sits in exactly one row, as the canonical ID or as an alias, that each canonical ID follows the rule below, and that the rows are in order; `--selftest` shows that each of these checks can fail [ours].

## How to read a row

- **One row, one decision.** Items merge when one decision settles all of them; related items that need different decisions stay apart, and name each other in the question or the decision [ours].
- **Canonical ID.** The engine-side ID (analysis.md section 10.1, then stages/01 to 07) whose full entry comes first; if the row has none, the ID whose full entry comes first in claims.md, then note-check.md, then artifacts.md. Aliases follow in the same order [ours].
- **Entry codes** [ours]: the code after each ID names the file of its full entry: `an` [analysis.md](analysis.md) section 10.1; `s01` to `s07` the files in [stages/](stages/); `cl` [claims.md](claims.md); `nc` [note-check.md](note-check.md); `ar` [artifacts.md](artifacts.md).
- **Class.** As filed. Where a row's IDs were filed under different classes, the row takes one, and D-11 gives the reason [ours].
- **Task**, the owner of the decision [ours]: 2 requirements · 3 components · 4 reuse · 5 scope, tasks and budget · 6 evaluation integrity · 7 test and mock mode. Task 1 marks a finding about the sources that this folder already settles.
- **Priority** [ours]: `blocks`, task 2 or 3 cannot write its requirement or contract without it, because the answer changes the control flow or an interface; `number`, it changes a number we would report (success, gain, review score, cost, time) but not the structure; `later`, neither: wording, naming, logging detail, or a defect of the paper to note; `none`, nothing is left to decide.
- **Decision.** Every decision here is our proposal to the owning task, never the paper's statement; the owning task confirms or replaces it [ours].
- **Cross-references** [ours]: D-n is an entry of *Where the analyses disagree*, F-n an entry of *Fixes the source documents need*.

## Summary

### Counts

- **Before merging** [ours]: 133 IDs, defined in six places: analysis.md section 10.1 (14), its index in section 10.2 (60, which re-lists those 14 and the 46 of stages/), stages/ (46), claims.md (25), note-check.md (17) and artifacts.md (31). As filed, 78 are UNSPECIFIED, 31 AMBIGUOUS and 24 INCONSISTENT.
- **After merging** [ours]: 88 rows, of which 29 merge 74 IDs and 59 hold one ID each; 50 rows are UNSPECIFIED, 24 AMBIGUOUS and 14 INCONSISTENT.

| Task | Rows | IDs | blocks | number | later | none |
|---|---|---|---|---|---|---|
| 2 · requirements | 32 | 46 | 15 | 12 | 5 | 0 |
| 3 · components | 23 | 33 | 8 | 3 | 12 | 0 |
| 4 · reuse | 1 | 2 | 0 | 1 | 0 | 0 |
| 5 · scope, budget | 12 | 17 | 0 | 5 | 7 | 0 |
| 6 · integrity | 18 | 33 | 4 | 11 | 3 | 0 |
| 7 · mock mode | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 · settled here | 2 | 2 | 0 | 0 | 0 | 2 |
| **All** | **88** | **133** | **27** | **32** | **27** | **2** |

| Class | IDs as filed | Rows |
|---|---|---|
| UNSPECIFIED | 78 | 50 |
| AMBIGUOUS | 31 | 24 |
| INCONSISTENT | 24 | 14 |

- **Task 7 owns no row** [ours]: the paper describes no test or mock mode, so nothing about it is open; mock mode is our own requirement, the note's N-98, which note-check.md marks as a PROPOSAL.
- **Task 6 owns 4 blocking rows** (A-INT-1, A-INT-3, U-NOTE-1, U-ART-16), so they must be decided before task 3 writes the harness and audit contracts, although TODO.md lists task 6 after task 3 [ours]. Two of them are already settled by the project's integrity rules in CLAUDE.md: metrics come only from the locked harness, and every number an agent sees while searching is a validation number [ours].

### The ten questions that most constrain the design

1. **A-TOP-1 · What a stage returns at its limit.** Listing 1 discards the candidate; §3.5 keeps the manuscript; the stage primitive's contract and the exit of every loop depend on the answer [Lst. 1] [§3.5] [ours]. Task 2.
2. **A-NOTE-1 · One stage primitive, or several stage kinds.** Only the subset experiment fits Listing 1 exactly; task 3's component list depends on it [Lst. 1] [Tab. 1] [ours]. Task 3.
3. **U-TOP-1 · What a task hands the engine.** G is an accepted paper with its code, but its form, the task rules, the SOTA numbers and the compute are unstated: this is the task-environment contract [§4.1] [§4.2] [ours]. Task 3.
4. **U-BASE-1 · The subset and the full benchmark.** Who defines them, how large they are, and whether they are fixed before the run [§3.2] [App. A.1] [ours]. Task 2.
5. **U-ART-16 · Who computes the numbers.** In the paper's own run, the agent's script scores both methods and writes the report; our rules put every metric in a locked harness, the largest structural departure from the paper [p. 42] (image) [ours]. Task 6.
6. **U-NOTE-1 · Validation and test.** The paper selects, compares and reports on the same benchmark results; a split changes what every critic may read [§3.3] [§3.4] [§3.5] [ours]. Task 6.
7. **A-INT-1 · Integrity as gates, or as a post-hoc audit.** §4.2 prompts for reproducibility; Appendix B claims a re-run gate; a gate adds a branch to the loop [§4.2] [App. B] [ours]. Task 6.
8. **A-FULL-1 · The full-set critic's reference.** The reported SOTA, or a reproduced full-set baseline that no stage produces; one reading adds a stage [Tab. 1] [App. B] [ours]. Task 2.
9. **A-BASE-1 · The baseline once per task, or once per idea.** It changes A_Coder's signature, and adds up to 9 coding sessions per run [§3.2, Eq. 2] [Fig. 5] (image) [ours]. Task 2.
10. **A-ABL-1 · Can the ablation critic reject?** Appendix B reports a rejection that §3.4's verdicts cannot express; it adds a verdict that ends a task, and it decides what success means (A-EVAL-1) [§3.4] [App. B] [ours]. Task 2.

## The register

Rows are grouped by owning task, `blocks` first; the task number is also in each row, for search [ours].

### Task 2 · Requirements (32 rows: 15 blocks, 12 number, 5 later)

| ID (entry) | Class | Question [location] | Decision it forces [ours] | Task | Priority | Aliases (entry) |
|---|---|---|---|---|---|---|
| A-TOP-1 (an) | INCONSISTENT | What a stage returns when its limit runs out: Listing 1 returns `None`; §3.5 keeps the manuscript; §3.4 and §3.6 imply keeping; the limitation loop and a second ablation `Refine` are silent (D-5) [Lst. 1] [§3.1] [§3.4] [§3.5] [§3.6] | One exhaustion rule per stage, taking the text's reading: the limitation set, h_best, P_new and the meta pass's outputs pass on; only the subset experiment prunes, as §3.2 says [ours] | 2 | blocks | A-LIM-1 (s01), U-ABL-4 (s04), A-NOTE-2 (nc) |
| A-TOP-2 (an) | AMBIGUOUS | What each App. A.2 limit counts: Listing 1's `max_rounds` (N critic calls, the last refinement never judged) or judged refinements (N refinements, N + 1 critic calls); three of A.2's limits count refinements (D-4) [Lst. 1] [App. A.2] | Every limit counts judged refinements; the requirement for each of the six limits states its number of critic calls [ours] | 2 | blocks | A-NOTE-3 (nc) |
| A-BASE-1 (s02) | AMBIGUOUS | Is the baseline reproduced once per task (§3.2 runs it first, Table 1 gives it a row) or inside every A_Coder call (Figure 5), when Eq. 2 takes only G and h [§3.2] [Tab. 1] [§3.2, Eq. 2] [Fig. 5] (image) | Once per task, before round 0; A_Coder receives E_base and C_base as inputs, a recorded extension of Eq. 2 [ours] | 2 | blocks | none |
| U-BASE-1 (s02) | UNSPECIFIED | The benchmark subset and the full benchmark of each task: who defines them, how large they are, whether they stay fixed; App. A.1 lists titles only, and App. D's paper runs one ablation on a *subset test split* [§3.2] [§1] [App. A.1] [p. 69] | Both are fields of the task manifest (U-TOP-1), fixed before the run by us and never by an agent; task 5 sets them per task, with the metric (U-EVAL-1) [ours] | 2 | blocks | U-NOTE-3 (nc), U-ART-4 (ar) |
| U-BASE-2 (s02) | UNSPECIFIED | What happens when the baseline will not reproduce, or lands far from the paper's numbers; the row has no critic and no refine step [Tab. 1] [§3.2] | A check of E_base against the paper's reported numbers with a per-task tolerance; a failure ends the task with a recorded reason (U-EVO-4) [ours] | 2 | blocks | none |
| U-FULL-1 (s02) | UNSPECIFIED | The full-set critic's verdicts and their effects: §3.2 gives only a "terminal decision", while Figure 5 draws an engineer loop and outputs *Good or Bad* [§3.2] [Fig. 5] (image) | The subset's vocabulary (`Good`, `Engineer`, `Bad`); a full-set `Bad` enters the traces as a failed idea; exhaustion gives `Bad` [ours] | 2 | blocks | none |
| A-FULL-1 (s02) | AMBIGUOUS | What the full-set critic compares against: Table 1's "original SOTA result", which no stage produces, or a reproduced full-set baseline, as App. B's "own reproduced baseline" suggests [Tab. 1] [App. B] | Reproduce the baseline on the full benchmark once per task and judge against it; keep the paper's reported numbers beside it for reporting (U-EVAL-1) [ours] | 2 | blocks | A-NOTE-5 (nc), U-ART-20 (ar) |
| A-ABL-1 (s04) | INCONSISTENT | Can the ablation critic reject? §3.4 allows `Good` or `Refine` only; App. B says the ablation critic rejected DMC-TeCh, and that task produced no paper; success reading (c) of A-EVAL-1 rests on it (D-6) [§3.4] [App. B] [Tab. 15] | Add a third verdict, `Reject`, for a gain the ablation does not attribute to the idea; it ends the task with a recorded reason; weigh the alternative, a fall-back to the next `Good` idea [ours] | 2 | blocks | A-NOTE-4 (nc), A-ART-4 (ar) |
| A-ABL-2 (s04) | INCONSISTENT | What follows a failed Result Comparison: Figure 7 draws drafting with the unchanged h_best; Listing 1 would return `None`; App. B's TeCh ended without a paper, which bears on this branch only if the critic cannot reject (F-7) [Fig. 7] (image) [Lst. 1] [App. B] | Follow Figure 7 and draft with the unchanged h_best; decide together with A-ABL-1; the spent-budget half is A-TOP-1's [ours] | 2 | blocks | none |
| A-ABL-3 (s04) | AMBIGUOUS | What "better" means for the Result Comparison Agent: §3.4 says "strictly outperforms", then leaves it to the agent's preference; §3.6 says "strictly superior"; results span several datasets and metrics [§3.4] [§3.6] | A deterministic rule over the harness's validation results, with the metric, datasets and direction fixed per task; the agent's reading is logged, not decisive [ours] | 2 | blocks | none |
| U-ABL-2 (s04) | UNSPECIFIED | How A_FullEng's refinement is validated, in §3.4 and §3.6: one call that returns h_new, E_new and C_new, or a pass through the full-set coder and critic, where Figure 3 routes the *New Idea* [§3.4] [§3.6] [Fig. 3] (image) | One A_FullEng call whose results the harness scores, with no critic loop; the Figure 3 reading stays the recorded alternative, since it changes the session bound (analysis.md section 9) [ours] | 2 | blocks | none |
| A-META-1 (s06) | AMBIGUOUS | How much the meta restart re-runs: §3.6 lists ablation planning, execution, re-drafting and peer review, not the ablation critic; Figure 7's restart path runs through the critic [§3.6] [Fig. 7] (image) | Re-enter at the start of the ablation stage and run the whole pass, critic included, as Figures 7 and 3 draw it [ours] | 2 | blocks | none |
| A-META-2 (s06) | AMBIGUOUS | Is the meta-reviewer asked again after the restart, and what is exported if it says `Refine` with N_meta spent [§3.6] [Fig. 7] (image) [App. A.2] | Ask it again; a second `Refine` exports that pass's P_new and C_best under A-TOP-1's rule, marked unapproved (A-TOP-3) [ours] | 2 | blocks | none |
| U-INT-1 (s07) | UNSPECIFIED | Where the specification filter runs (after subset, full-set, ablation, rebuttal or A_FullEng experiments), and what a discard does: a `Bad` idea, or the end of the task, as footnote 2 shows once [§4.2] [fn. 2] | After every experiment that produces a reported number; a discarded result is invalid, and an idea or refinement left without a valid result counts as `Bad` [ours] | 2 | blocks | none |
| U-INT-3 (s07) | UNSPECIFIED | When the reference check and the method-code audit run: after drafting, after each enhancement, before export, or again after the meta restart [§4.2] [§3.5] [§3.6] | After every manuscript revision and before export, so that the reviewer and the meta-reviewer read a repaired draft [ours] | 2 | blocks | none |
| A-TOP-3 (an) | INCONSISTENT | Does the run loop until approval, as §3 and §1 say, or stop after one meta refinement and export a draft the meta-reviewer had returned as `Refine` [§3] [§1] [§3.6] [App. A.2] | Keep N_meta = 1 and §3.6's exit, and mark every export with its last meta verdict, so that unapproved papers are counted apart [ours] | 2 | number | none |
| A-SEED-1 (s01) | AMBIGUOUS | Is novelty a filter (§3's "filtering for those with high novelty"; Table 1's *Is it novel?*) or only a ranking (§3.1 sorts and discards nothing) [§3] [§3.1] [Tab. 1] | Rank only, as §3.1 specifies; a novelty threshold is an optional ablation [ours] | 2 | number | none |
| U-SEED-3 (s01) | UNSPECIFIED | The Idea Generator's inputs (the limitations, the pool and its scores, G) and its content rules; App. B says it deliberately does not propose compute-scaling knobs [§3.1] [App. B] | It reads G, the limitations and the scored pool; a written content rule excludes pure compute or budget scaling [ours] | 2 | number | none |
| U-SUB-1 (s02) | UNSPECIFIED | The subset critic's criteria behind "substantially inferior", "consistently outperforms" and "shows potential": no margin, seed count or test; App. B's "statistically inert" hints at a test [§3.2] [App. B] | An LLM verdict with a numeric guard over harness results: no `Good` without a pre-registered margin over E_base [ours] | 2 | number | none |
| A-FULL-2 (s02) | AMBIGUOUS | The full-set engineering limit: App. A.2's sentence on the "Idea Critic Agent" covers the subset critic only, leaving the full set unbounded, or both critics [§3.2] [App. A.2] | Two rounds at both levels, the reading that both session bounds already use (analysis.md section 9, note-check.md special case C) [ours] | 2 | number | A-NOTE-9 (nc) |
| A-EVO-1 (s03) | AMBIGUOUS | What round 0 runs: §3.3's top-N_0 seeds, against App. A.2's two candidates per round, one of them evolved; N_0 has no value; this is also the N_0 half of A-NOTE-8; reclassified from INCONSISTENT (D-3) [§3.3] [App. A.2] [Fig. 9b] (image) | A.2's rounds are the rounds k ≥ 1; round 0 runs N_0 = 2 seeds, as many candidates as each later round [ours] | 2 | number | none |
| A-EVO-2 (s03) | AMBIGUOUS | Do App. A.2's "four rounds" include round 0: K = 4 refinement rounds after it, or K = 3 (D-1) [App. A.2] [§3.3] [Fig. 9] (image) | K = 4 after round 0, as Figure 9's rounds *Initial* to *Round 4* show for the paper's own runs [ours] | 2 | number | A-NOTE-8 (nc) |
| U-EVO-4 (s03) | UNSPECIFIED | What a failed task leaves: §3.3 "terminates the entire process" and records nothing, and the paper names 1 of its 21 failed tasks [§3.3] [Tab. 3] [App. B] | Every task ends with a record: outcome, stage, a reason from a fixed list (no `Good` idea, baseline not reproduced, filter discard, ablation reject, error) and its cost [ours] | 2 | number | U-BENCH-3 (cl) |
| U-SEL-1 (s03) | UNSPECIFIED | The Selector's criterion: an LLM comparison of "performance metrics and execution logs", with no rule across datasets and metrics, no tie-break, no weight for novelty [§3.3, Eq. 4] | A numeric pre-selection on the pre-registered validation metric; the LLM chooses among near-ties and records why [ours] | 2 | number | none |
| A-PEER-1 (s05) | AMBIGUOUS | What N_peer = 2 counts: two reviews, so one rebuttal, or two rebuttal cycles, so up to three reviews, as Table 5's review rounds 0, 1 and 2 suggest [§3.5] [App. A.2] [Tab. 5] | Two rebuttal cycles, so up to three reviews [ours] | 2 | number | none |
| U-META-1 (s06) | UNSPECIFIED | Do the ablation and review budgets, N_abl and N_peer, reset for the meta restart [§3.6] [App. A.2] | Reset per pass, the reading of analysis.md section 9; D-2 shows it moves the session bound by 7 at N_p = 6 [ours] | 2 | number | none |
| U-META-2 (s06) | UNSPECIFIED | The meta-reviewer's criterion: it reads the draft and the last review only, with no rubric, score or results [§3.6] [Tab. 1] | A written rubric for Table 1's *venue bar*; it also reads the verified results table, so that a `Refine` rests on evidence [ours] | 2 | number | none |
| U-EVO-1 (s03) | UNSPECIFIED | When the S = 4 stop test runs: after each round, as the formula's sum over whole rounds suggests, or after each idea [§3.3] | After each round [ours] | 2 | later | none |
| U-EVO-3 (s03) | UNSPECIFIED | What a round does when no unevaluated seed is left [§3.3] | Run the evolved idea alone; with N_seed at least N_0 + K·N_e (U-SEED-1) it cannot happen [ours] | 2 | later | none |
| U-DRAFT-2 (s05) | UNSPECIFIED | Drafts that fail to compile or break the format, and who makes the figures: only the Enhancer updates "tables and figures", and App. D's figure is a raster diagram with layout notes [§3.5] [p. 59] (image) | A compile-and-format check after every draft and revision; figures made by code from result files, and checked against the method (A-ART-7) [ours] | 2 | later | U-ART-18 (ar) |
| U-ART-11 (ar) | UNSPECIFIED | A refined idea keeps its name after its components change (Procrustes-DS), and nothing re-checks its novelty [p. 47] [§3.4] | A refinement that replaces a component is re-scored by the Novelty Checker and may be renamed; evolved ideas likewise (U-EVO-2) [ours] | 2 | later | none |
| A-ART-5 (ar) | AMBIGUOUS | How far an engineering step may change the idea: §3.2's trigger is "hyperparameter tuning or code adjustments", yet its engineer "refines h", and the p. 40 redesign replaced four components (D-10) [§3.2] [p. 40] (image) | §3.2's engineers tune and repair code only; component changes belong to A_FullEng in §3.4 and §3.6 [ours] | 2 | later | none |

### Task 3 · Components and contracts (23 rows: 8 blocks, 3 number, 12 later)

| ID (entry) | Class | Question [location] | Decision it forces [ours] | Task | Priority | Aliases (entry) |
|---|---|---|---|---|---|---|
| A-NOTE-1 (nc) | INCONSISTENT | Does one primitive cover every stage? §3 says Listing 1 abstracts "all stages"; three Table 1 rows lack a critic or a refine step, and most critics in §3 return two verdicts, not three [§3] [Lst. 1] [Tab. 1] | A few stage kinds (single step, selection, count-driven generation, population loop, critic loop), each configured by data: a verdict map, an exhaustion rule, an optional comparison gate [ours] | 3 | blocks | none |
| U-TOP-1 (an) | UNSPECIFIED | What a task hands the engine: the paper's form, the code and its commit, the task rules the specification filter needs, the SOTA numbers the full-set critic needs, the compute [§4.1] [§4.2] [Tab. 1] | A versioned task manifest with these fields, a rules file included; task 5 fills one per task; the audit brief of U-ART-7 is U-NOTE-4's [ours] | 3 | blocks | U-INT-2 (s07), U-BENCH-1 (cl), U-ART-7 (ar) |
| U-TOP-2 (an) | UNSPECIFIED | Failure handling: an agent error, code that never runs, a timeout or a tool outage; no per-session time or cost limit is given, only averages [§3] [§4.3] [Fig. 10] (image) | A retry and timeout policy per stage, a budget guard per session and per task, and resume from the last finished stage [ours] | 3 | blocks | none |
| U-CFG-2 (an) | UNSPECIFIED | What one coding session is: one per ablation plan or rebuttal task, one per idea, or one long session per stage [§3.4] [§3.5] [App. A.2] | One session per coding call (an idea step, an ablation plan, a rebuttal task), the unit that both session bounds assume (D-2) [ours] | 3 | blocks | none |
| U-CODER-1 (s02) | UNSPECIFIED | What A_Coder returns for an idea pruned on the subset: its subset outputs, or nothing; only an unprinted TeX comment says either level [§3.2, Eq. 2] [p. 7] | The trace record keeps the subset results and code with the verdict and the feedback, so that A_Evolve can learn from failures [ours] | 3 | blocks | none |
| U-DRAFT-1 (s05) | UNSPECIFIED | What the drafter reads beyond h_best, E_best and E_abl (G's paper, C_best, rejected ideas, a literature search), and how PaperOrchestra is wrapped [§3.5] [§2] | It reads h_best, the verified results table (ablations included) and G's paper for related work, but no code and no raw logs; task 4 settles the PaperOrchestra wrapper [ours] | 3 | blocks | none |
| U-PEER-4 (s05) | UNSPECIFIED | What the Paper Enhancer, which runs on Claude Code, reads and may change: C_best, new code for figures, sections the review did not raise [§3.5] [App. A.2] | It edits the manuscript only, with code and results read-only; new numbers come from the rebuttal coder through the harness [ours] | 3 | blocks | none |
| U-ART-15 (ar) | UNSPECIFIED | The sandbox's limits: the rebuttal agent installed packages, downloaded weights, ran on 8×V100 and capped test sets, while §3.5 says only that it uses C_best [p. 51] [p. 55] (image) [§3.5] | A sandbox policy for installs, network and GPUs per stage, and a rule that no agent changes the evaluation protocol [ours] | 3 | blocks | none |
| U-TOP-4 (an) | UNSPECIFIED | Whether a round's candidates, the ablation plans or the rebuttal tasks run in parallel [§3.3] [§3.4] [§3.5] | In parallel where the inputs are independent, bounded by the GPU queue; time is recorded both as wall-clock and as busy time (U-COST-3) [ours] | 3 | number | none |
| U-ABL-3 (s04) | UNSPECIFIED | Whether ablation and rebuttal code stays in C_best, and so in C+, when every reported number must reproduce [§3.4] [§3.5] [Tab. 7] | C+ ships the method and, beside it, the scripts behind every reported number, ablation and rebuttal runs included [ours] | 3 | number | U-PEER-2 (s05) |
| A-CFG-1 (an) | AMBIGUOUS | Which agents run on Claude Code: App. A.2 names four, §4.2 says whenever coding is required, and the baseline coder, both engineers, A_FullEng, the integrity Coding Agent and both planners fall between (D-7) [App. A.2] [§4.2] | Every agent that writes or runs code uses the coding backend and the planners use the default model, all in one routing file [ours] | 3 | number | A-NOTE-6 (nc) |
| A-TOP-5 (an) | INCONSISTENT | Symbol collisions: calligraphic R for the traces and the review, s_review and s_new, A_AblCritic and A_AblCrit, and "baseline" for E_best in §3.4 and §3.6 [§3.3] [§3.4] [§3.5] [§3.6] | Distinct names in our schemas; §3.6's test compares with E_best [ours] | 3 | later | none |
| U-TOP-3 (an) | UNSPECIFIED | No agent's prompt, input format or output schema is given; Appendices C and D show outputs only [§3] [App. A.2] [App. C] | A versioned prompt and schema per agent; artifacts.md section 5 gives each schema's floor [ours] | 3 | later | U-ART-1 (ar) |
| U-CFG-1 (an) | UNSPECIFIED | Runtime configuration: sampling, context limits, Claude Code's tools, permissions and turn limits, the hardware [App. A.2] [§4.3] | All of it in versioned configuration files, recorded with every run [ours] | 3 | later | none |
| A-ROSTER-1 (an) | AMBIGUOUS | One name for two things: Peer-Review Agent (the reviewer in §1, the review-and-rebuttal box in Figure 3), Idea Generator, Idea Refiner [§1] [Fig. 3] (image) | The canonical names of analysis.md section 7 [ours] | 3 | later | none |
| U-LIM-1 (s01) | UNSPECIFIED | The Limitation Verifier's criterion, what it returns besides its verdict, and the format of a limitation; pp. 34–35 show only the final list [§3.1] [pp. 34–35] | A verifier schema (verdict, missing items) with a per-round log; the limitation record follows pp. 34–35 [ours] | 3 | later | U-ART-2 (ar) |
| U-SEED-2 (s01) | UNSPECIFIED | The novelty score: its scale, the search query, and whether G's own paper is among the comparisons; the idea pages show no score, rank or reference [App. A.2] [pp. 36–39] | A scoring prompt with a fixed scale and a query recipe; each idea record carries its score, references and rank [ours] | 3 | later | U-ART-3 (ar) |
| A-SEED-2 (s01) | AMBIGUOUS | Who generates h_0: Figure 4 draws an *Initial Idea Generator* apart from the *Idea Generator*, and §3.1 names neither [§3.1] [Fig. 4] (image) | One agent with two prompts, initial and expanding [ours] | 3 | later | none |
| U-EVO-2 (s03) | UNSPECIFIED | What A_Evolve reads from the traces, which include whole codebases; whether it sees G, the limitations or the scores; whether evolved ideas face the Novelty Checker [§3.3] | It reads ideas, verdicts, feedback and result summaries, not code; evolved ideas get a novelty score (U-ART-11) [ours] | 3 | later | none |
| A-INT-2 (s07) | AMBIGUOUS | Which Writer Agent repairs the references and the method section: the Initial Drafter or the Draft Enhancer [§4.2] [Fig. 3] (image) | The Paper Enhancer, which already revises files; the timing is U-INT-3's [ours] | 3 | later | none |
| U-ART-10 (ar) | UNSPECIFIED | No page shows a verdict (d^h, d_abl, s_review, d_meta), the Result Comparison's decision or a skipped stage, and the paper gives no run layout [pp. 34–71] [§3] | Every stage and critic writes a machine-readable record, skips and their reasons included, in a run layout of ours, with the X-Mahalanobis layout as a reference [ours] | 3 | later | U-ART-17 (ar), U-ART-19 (ar) |
| U-ART-14 (ar) | UNSPECIFIED | The review–rebuttal trail: the review item IDs (W3, Q1, S1) are undefined, and neither the task list nor the manuscript edits are shown [p. 51] (image) [§3.5] | A review schema with item IDs, a task list mapping tasks to items, and a diff of each revision [ours] | 3 | later | none |
| A-ART-1 (ar) | AMBIGUOUS | Which critic wrote p. 46, and with what verdict: the Ablation Critic with `Refine`, or an Idea Critic's engineering round; no verdict is printed [p. 46] [App. C] | Read it as the Ablation Critic's feedback, and take its per-component format as that critic's floor [ours] | 3 | later | none |

### Task 4 · Reuse (1 row: 1 number)

| ID (entry) | Class | Question [location] | Decision it forces [ours] | Task | Priority | Aliases (entry) |
|---|---|---|---|---|---|---|
| U-PEER-3 (s05) | UNSPECIFIED | ScholarPeer's configuration, as the in-loop reviewer and as an evaluator: backbone, version, settings, input form, reviews per round; no code is linked [§3.5] [§4] [Bib: goyal2026scholarpeer] | Task 4 finds whether ScholarPeer can be run or must be rebuilt; either way, pin its model and version and log raw reviews; as the optimized reviewer it is never reported as evidence [ours] | 4 | number | U-EVAL-2 (cl) |

### Task 5 · Scope, tasks and budget (12 rows: 5 number, 7 later)

| ID (entry) | Class | Question [location] | Decision it forces [ours] | Task | Priority | Aliases (entry) |
|---|---|---|---|---|---|---|
| U-SEED-1 (s01) | UNSPECIFIED | N_seed, the size of the seed pool, has no value [§3.1] [App. A.2] | At least N_0 + K·N_e, which is 6 under the proposals for A-EVO-1 and A-EVO-2; the exact value is a budget choice [ours] | 5 | number | none |
| U-ABL-1 (s04) | UNSPECIFIED | N_p, the number of ablation plans, has no value; Table 15 reports 5–6 per paper on the 4 ICLR tasks that succeeded, and App. D's paper has 7, each on its own datasets [§3.4] [Tab. 15] [pp. 69–71] | A cap on N_p, 6 by Table 15's top; each ablation runs on the full benchmark [ours] | 5 | number | U-NOTE-5 (nc), U-ART-13 (ar) |
| U-PEER-1 (s05) | UNSPECIFIED | N_t, the number of rebuttal tasks, has no value; U-NOTE-5 raises it together with N_p [§3.5] [App. A.2] | A cap on N_t per review round, set by the cost model [ours] | 5 | number | none |
| U-COST-1 (cl) | UNSPECIFIED | What the $3765 per task contains, and over which runs: tokens and virtual machines with no prices or split, averaged over 33 NeurIPS runs, the number that succeeded [§4.3] [Fig. 10b] (image) [Tab. 3] | A ledger of tokens × price and machine-hours × price per stage and task; cost reported over all runs and per success; an unknown cost recorded as unknown [ours] | 5 | number | U-COST-2 (cl), U-NOTE-7 (nc) |
| U-COST-3 (cl) | UNSPECIFIED | How the 2.5 days per task were measured: wall-clock or busy time, queueing, parallelism, hardware (D-8) [§4.3] [Fig. 10a] (image) | Wall-clock and busy time recorded per stage, with the hardware [ours] | 5 | number | none |
| A-TOP-4 (an) | AMBIGUOUS | Is G a natural-language challenge, as Figure 3 and the abstract present it, or an accepted paper with its code, as §4.1 and every experiment use it [Fig. 3] (image) [Abstract] [§4.1] | A paper with its code (U-TOP-1); a free-text challenge is out of scope [ours] | 5 | later | none |
| A-CFG-2 (an) | AMBIGUOUS | Antigravity runs on Gemini 3.8 Flash, while every other mention is Gemini 3.6 Flash: a second version, or a typo [§4.2] [Tab. 8] | It matters only if we repeat the coding-backend swap, which is out of scope unless task 5 adds it [ours] | 5 | later | none |
| U-EVAL-6 (cl) | UNSPECIFIED | The human study's protocol: how 9 reviewers were assigned to 33 papers, blinding, pairings, dispersion, agreement [§4.3] [Tab. 10] | Out of scope, unless task 5 adds a human study with a written protocol [ours] | 5 | later | none |
| U-EVAL-7 (cl) | UNSPECIFIED | What Figure 1a's radar plots: the quantity, its normalization, the *Upper Bound*, the mapping of tasks to areas [Fig. 1a] (image) | Not reproduced [ours] | 5 | later | none |
| U-EVAL-9 (cl) | UNSPECIFIED | Which papers Table 2 and the Agent4Science row of Table 3 score, and how they were chosen [Tab. 2] [Tab. 3] | Any comparison with other agents lists its papers and scores them under our locked settings; none is planned [ours] | 5 | later | none |
| U-BENCH-2 (cl) | UNSPECIFIED | How the 64 ICML tasks were chosen with AutoSOTA's filter: the pool, the criteria beyond reproducibility, who applied it [App. A.1] | A written task-selection filter, applied before any run, for task 5's own choice of tasks [ours] | 5 | later | none |
| A-COST-1 (cl) | INCONSISTENT | Figure 10's caption calls idea refinement "the majority" of time and cost; its chart shows 44.9% and 45.4%, and *Initial Implements* is not a §3 stage [Fig. 10] [Fig. 10b] (image) [§3.3] | Budget from the per-stage shares, with the chart's stages mapped onto §3's [ours] | 5 | later | A-NOTE-7 (nc) |

### Task 6 · Evaluation integrity (18 rows: 4 blocks, 11 number, 3 later)

| ID (entry) | Class | Question [location] | Decision it forces [ours] | Task | Priority | Aliases (entry) |
|---|---|---|---|---|---|---|
| A-INT-1 (s07) | INCONSISTENT | Is reproducibility a prompt (§4.2: "the Coding Agent is prompted", with no post-hoc refinement) or a structural gate (App. B: a reproduction re-run and audits); and did the pipeline or the post-hoc audit write pp. 47–50 [§4.2] [App. B] [pp. 47–50] | Gates inside the run: the harness re-executes every result before a critic reads it, and the audit runs before export; the post-hoc audit is repeated at evaluation [ours] | 6 | blocks | A-NOTE-10 (nc), A-ART-2 (ar) |
| A-INT-3 (s07) | AMBIGUOUS | Which Coding Agent runs the specification filter and the method-code audit, since §4.2 says "the Coding Agent" three times, and which model judges the audits of pp. 47–50 [§4.2] [pp. 47–50] | A session and a model separate from the agent that wrote the code; the evaluation audit (U-EVAL-5) is a third, independent judge [ours] | 6 | blocks | U-ART-9 (ar) |
| U-NOTE-1 (nc) | UNSPECIFIED | No validation/test separation: the Selector, the Result Comparison Agent and the drafter use the same benchmark results, and the X-Mahalanobis run was tuned on the test sets it reports [§3.3] [§3.4] [§3.5] [pp. 40–46] (image) | Agents see validation numbers only; the test set is scored once, at the end, by the harness [ours] | 6 | blocks | U-ART-5 (ar) |
| U-ART-16 (ar) | UNSPECIFIED | Who computes the numbers: the agent's own script runs the evaluation, recomputes the baseline and writes the report, and the audit accepts that baseline [p. 42] [p. 50] (image) [§3.2] | Every metric comes from the locked harness; agent code only produces what the harness scores [ours] | 6 | blocks | none |
| U-EVAL-1 (cl) | UNSPECIFIED | How one paper's relative gain is computed (Gemini parses the paper's own tables 10 times and averages), and against which baseline: the paper's SOTA numbers or a reproduction, the reporting half of A-NOTE-5 [§4.1] [§1] [App. B] | A pre-registered rule per task (metric, datasets, direction), computed from harness result files against both references, and both reported [ours] | 6 | number | A-EVAL-2 (cl), U-NOTE-2 (nc) |
| U-EVAL-3 (cl) | UNSPECIFIED | The Stanford Agentic Reviewer: a link and a scale, with no acceptance rule, version or query dates [§4] [fn. 1] [Tab. 3] | If it is the reporting judge: k queries per paper with the date and raw output, and our own acceptance rule; task 4 checks the service [ours] | 6 | number | none |
| U-EVAL-4 (cl) | UNSPECIFIED | Runs per task, seeds, run-to-run variance: none is reported; the ± values are spreads across papers [§4] [Tab. 2] | Repeated engine runs for every load-bearing comparison, with their variance; the number of runs set against the budget [ours] | 6 | number | none |
| U-EVAL-5 (cl) | UNSPECIFIED | Who ran the integrity audit behind Table 7, with which model, and whether it is independent of the pipeline's own fixer [Tab. 7] [§4.2] | The audit is part of the locked evaluation, run on every task by a judge that is not the pipeline's fixer [ours] | 6 | number | none |
| U-EVAL-8 (cl) | INCONSISTENT | Figure 9a's per-round gain is undefined, and its final 33.4% disagrees with the ICML mean that Table 4 implies, 34.43–34.68% [Fig. 9a] (image) [Tab. 4] | One gain definition, logged per task at named checkpoints (each round, after ablation, after the meta refinement), with no success yet made explicit [ours] | 6 | number | A-EVAL-6 (cl) |
| U-EVAL-10 (cl) | INCONSISTENT | Table 4 is bolded as a head-to-head with AutoSOTA, whose 105 papers are unsourced; App. B says the two Δ columns are "not a head-to-head" [Tab. 4] [App. B] [Tab. 16] | Compare systems only on shared tasks, metric, hardware and gain rule, or not at all [ours] | 6 | number | A-EVAL-7 (cl) |
| A-EVAL-1 (cl) | AMBIGUOUS | What success means: at least one `Good` idea (§3.3), beating the human SOTA (Figure 1), or a gain the ablation attributes to the mechanism (Table 15), which needs A-ABL-1's reject [§3.3] [Fig. 1] [Tab. 15] | Success is a full-set `Good` idea with a positive gain under U-EVAL-1's rule; all three counts are reported [ours] | 6 | number | none |
| A-EVAL-3 (cl) | INCONSISTENT | What ScholarPeer's acceptance means: §3.5 calls 8 the acceptance threshold, yet Table 3's rates and standard deviations cannot come from a rating of 8 or more [§3.5] [Tab. 3] | Acceptance defined per reviewer, explicitly; the in-loop threshold's name never reused for a reported metric [ours] | 6 | number | none |
| A-EVAL-5 (cl) | AMBIGUOUS | What a Table 5 review round is, a per-round snapshot or the final system, and how many of the 49 tasks had a second round [Tab. 5] [App. A.2] | Per task, log the round index, the stop reason and any meta change; report per-round snapshots, each with its n [ours] | 6 | number | U-NOTE-6 (nc) |
| U-NOTE-4 (nc) | UNSPECIFIED | The audit's protocol: re-runs and tolerance (p. 47 shows one exact re-run), what is re-executed, its scope (p. 47 audited the method only, Table 7 claims every result), the alignment threshold, judges, reference lookup, and the auditor's brief that U-ART-7 raises [§4.2] [p. 47] [Tab. 7] | A written protocol: every reported number re-executed k times against a per-metric tolerance, baselines included; a fixed alignment rule; one named judge [ours] | 6 | number | U-ART-6 (ar), U-ART-8 (ar), A-ART-3 (ar) |
| U-ART-12 (ar) | UNSPECIFIED | Seeds and variance of results: one seed for X-Mahalanobis, five for the rebuttal, none stated in App. D's paper; App. A.2 sets no seed policy [p. 40] [p. 51] (image) [App. A.2] | The harness reports every number as a mean over a fixed number of seeds, with its spread [ours] | 6 | number | none |
| A-EVAL-4 (cl) | AMBIGUOUS | What a rating is: one overall score per paper on the ICLR scale, or another form, such as an average of several reviews [§3.5] [Tab. 2] | Log the raw reviewer output per paper, and state the SD convention [ours] | 6 | later | none |
| A-EVAL-8 (cl) | AMBIGUOUS | Whose rating Table 9 prints: VD-STrans's 6.5 matches its Stanford Agentic Reviewer score in Figure 2, but no reviewer is named [Tab. 9] [Fig. 2] | None for the engine; recorded as unattributed [ours] | 6 | later | none |
| A-ART-7 (ar) | INCONSISTENT | App. D's generated paper contradicts itself: one method under one protocol with three sets of numbers, a do-no-harm guarantee against its own table, six ablations announced and seven shown, a figure unlike the method; the review loops let it through [pp. 56–71] [Fig. 11] | A consistency check before export: every number traced to a harness result, claims checked against tables, figures checked against the method [ours] | 6 | later | A-ART-8 (ar), A-ART-9 (ar), A-ART-10 (ar) |

### Task 7 · Test and mock mode (0 rows)

No gap in the paper concerns testing: the paper describes no test or mock mode, which is our own requirement (see the summary) [ours].

### Task 1 · Settled in this folder (2 rows: none)

| ID (entry) | Class | Question [location] | Decision it forces [ours] | Task | Priority | Aliases (entry) |
|---|---|---|---|---|---|---|
| A-ART-6 (ar) | INCONSISTENT | Appendices C and D give page numbers five below the arXiv PDF's, and call the 16-page draft 15 pages [App. C] [App. D] | Nothing left to decide: README.md cites the actual PDF page [ours] | 1 | none | none |
| A-ART-11 (ar) | INCONSISTENT | The HTML shows 15 of the 38 artifact pages, omitting the critic feedback and nearly all of the final paper [App. C] [App. D] | Nothing left to decide: this folder reads the TeX and the PDF, never the HTML alone [ours] | 1 | none | none |

## Why these rows merge

Each merged row, and the one decision that settles all its IDs [ours]. Aliases are listed in the order of their full entries [ours].

| Row | Merged with | Why one decision settles them [ours] |
|---|---|---|
| A-TOP-1 | A-LIM-1, U-ABL-4, A-NOTE-2 | A-NOTE-2 asks the same question; A-LIM-1 and U-ABL-4 are the limitation and ablation instances of the per-stage exhaustion rule [ours] |
| A-TOP-2 | A-NOTE-3 | the same question, what App. A.2's limits count [ours] |
| U-BASE-1 | U-NOTE-3, U-ART-4 | all three ask who defines the subset and the full benchmark; U-ART-4 adds the pages that imply them [ours] |
| A-FULL-1 | A-NOTE-5, U-ART-20 | the same two readings of the full-set reference; A-NOTE-5's reporting half is also named in U-EVAL-1 [ours] |
| A-ABL-1 | A-NOTE-4, A-ART-4 | the same missing reject verdict [ours] |
| A-FULL-2 | A-NOTE-9 | the same two readings of A.2's engineering sentence, numbered in opposite order (F-13) [ours] |
| A-EVO-2 | A-NOTE-8 | A-NOTE-8's two readings are A-EVO-2's; its N_0 half is named in A-EVO-1's row [ours] |
| U-EVO-4 | U-BENCH-3 | one failure record per task, with a reason from a fixed list, settles both [ours] |
| U-DRAFT-2 | U-ART-18 | both ask who makes the figures and what checks them [ours] |
| U-TOP-1 | U-INT-2, U-BENCH-1, U-ART-7 | the task manifest says what a task hands over and where the rules come from; U-ART-7's audit brief goes to U-NOTE-4 [ours] |
| U-ABL-3 | U-PEER-2 | one rule for where auxiliary experiment code lives settles both [ours] |
| A-CFG-1 | A-NOTE-6 | one routing file settles both; A-NOTE-6 is the planners' part [ours] |
| U-TOP-3 | U-ART-1 | the same absence of prompts and output schemas [ours] |
| U-LIM-1 | U-ART-2 | the verifier's schema and its per-round log settle both [ours] |
| U-SEED-2 | U-ART-3 | the novelty score, and the idea record that must carry it [ours] |
| U-ART-10 | U-ART-17, U-ART-19 | one design of run records covers verdicts, skipped stages and the layout [ours] |
| U-PEER-3 | U-EVAL-2 | one pinned ScholarPeer configuration serves the loop and the evaluation [ours] |
| U-ABL-1 | U-NOTE-5, U-ART-13 | N_p; U-NOTE-5's N_t half is named in U-PEER-1's row [ours] |
| U-COST-1 | U-COST-2, U-NOTE-7 | one cost ledger, and the sample it is reported over [ours] |
| A-COST-1 | A-NOTE-7 | the same contradiction between Figure 10's caption and its chart [ours] |
| A-INT-1 | A-NOTE-10, A-ART-2 | a gate in the run or a post-hoc audit; A-ART-2 asks which of the two wrote pp. 47–50 [ours] |
| A-INT-3 | U-ART-9 | whether the checker is independent of the code's author [ours] |
| U-NOTE-1 | U-ART-5 | one validation/test split settles both [ours] |
| U-EVAL-1 | A-EVAL-2, U-NOTE-2 | one pre-registered gain rule includes its reference; F-12 aligns their decisions [ours] |
| U-EVAL-8 | A-EVAL-6 | one gain definition, at named checkpoints [ours] |
| U-EVAL-10 | A-EVAL-7 | one rule for comparing systems [ours] |
| A-EVAL-5 | U-NOTE-6 | per-round logging, with n per round [ours] |
| U-NOTE-4 | U-ART-6, U-ART-8, A-ART-3 | one audit protocol fixes the re-runs, the tolerance, the scope and the alignment threshold [ours] |
| A-ART-7 | A-ART-8, A-ART-9, A-ART-10 | one consistency check before export catches all four defects [ours] |

**Kept apart, though related** [ours]: A-ABL-1 and A-ABL-2 (the verdict set, against the branch after a failed comparison); A-TOP-3 and A-META-2 (marking an unapproved export, against asking the meta-reviewer again); A-EVO-1 and A-EVO-2 (N_0, against K); A-FULL-1 and U-EVAL-1 (the in-loop reference, against the reported one); U-EVAL-4 and U-ART-12 (repeated engine runs, against seeds per number); U-EVO-2 and U-ART-11 (the evolver's context, against renaming a refined idea); U-CFG-1 and U-ART-15 (runtime values, against the sandbox policy); A-INT-3 and U-EVAL-5 (the checker in the loop, against the evaluation's auditor).

## Where the analyses disagree

Every place where two documents read the paper differently, settled from the paper where it can be, and left open with both sides where it cannot [ours]. The edits that follow are in *Fixes the source documents need* [ours].

### D-1 · Do App. A.2's four rounds include round 0? Settled for the paper's runs

- **analysis.md** (A-EVO-2, section 9): K = 4 refinement rounds after round 0, from Figure 9's labels, so 9 or 10 ideas; claims/ablations.md (C-ABLX-1) reads Figure 9 the same way [Fig. 9] (image) [ours].
- **note-check.md**: A-NOTE-8 gives both readings without Figure 9, and special case C assumes four rounds in all, so 8 ideas [App. A.2] [ours].
- **The paper**: "We run this experimentation loop for up to four rounds" (tex:sections/appendix.tex:155) [App. A.2]; §3.3 numbers the rounds from k = 0 and stops when round K is reached (paraphrase) (tex:sections/3_new_method.tex:86) [§3.3]; Figure 9's x-axis reads *Initial*, *Round 1*, *Round 2*, *Round 3*, *Round 4*, and 4 of the 49 tasks select their best idea in *Round 4* [Fig. 9b] (image).
- **Verdict: settled.** Had the four rounds included round 0, the last would be Round 3, and no task could pick an idea from Round 4; so the paper's runs used round 0 plus K = 4 [Fig. 9b] (image) [ours]. A.2's sentence alone stays ambiguous, so A-EVO-2 keeps its class with this evidence (F-1) [App. A.2] [ours].

### D-2 · How many coding sessions a task needs. Partly settled

- **note-check.md** (special case C, N-106): from 16 up to 75 + 4N_t, 87 at N_t = 3, and 9 to 49 without a success; it assumes 8 ideas, 6 ablation plans (5 for the lower bound), no ablation refinement in the meta pass, and 2 integrity sessions [ours].
- **analysis.md** (section 9): 68 + 4N_p + 4N_t, so 92 + 4N_t at N_p = 6; it assumes 10 ideas (N_0 = 2), budgets that reset for the meta pass (U-META-1), and no integrity sessions [ours].
- **Where they differ** [ours]: 10 ideas against 8 adds 12 sessions; a second ablation refinement in the meta pass adds 7 (one A_FullEng call and 6 re-ablations); the integrity sessions subtract 2; 12 + 7 − 2 = 17 = 92 − 75.
- **The paper** reports no session count [App. A.2] [§4.3]. The meta restart re-executes "downstream ablation planning, ablation execution, manuscript re-drafting, and simulated peer-review cycles" (tex:sections/3_new_method.tex:149) without saying whether their budgets reset [§3.6]; §4.2 adds "a validation filter that uses the Coding Agent" (tex:sections/4_experiment.tex:43) without saying whether it is a new session [§4.2].
- **Verdict: partly settled** [ours]. The idea count is settled by D-1: 9 or 10, never 8. With note-check.md's other assumptions, its upper bound becomes 81 + 4N_t (N_0 = 1) or 87 + 4N_t (N_0 = 2), and a task without a success spends 10 to 55 or 11 to 61 sessions (F-2). The two remaining differences, the budget reset (U-META-1) and the integrity sessions (A-INT-3, U-INT-1, U-INT-3), are open: the paper cannot settle them. The lower bound, 16 at N_0 = 2 and N_p = 5, is not disputed; it is 18 at N_0 = 1 with an end-of-round stop test (U-EVO-1).

### D-3 · The class of the round-0 question. Settled: AMBIGUOUS

- **analysis.md** files A-EVO-1 as INCONSISTENT; **note-check.md** files the same N_0 question, inside A-NOTE-8, as AMBIGUOUS [ours].
- **The paper**: §3.3's initial round executes the top-N_0 seed ideas (paraphrase) (tex:sections/3_new_method.tex:63) [§3.3]; App. A.2: "In each idea experimentation round, we evaluate two candidates: one selected from the seed ideas and the other an evolved idea" (tex:sections/appendix.tex:155) [App. A.2].
- **Reasoning** [ours]: the two texts contradict each other only if round 0 is one of A.2's rounds. Read as the rounds k ≥ 1, which D-1's evidence supports, both hold, and only N_0 is left open; Figure 9b's *Initial* bar is 100% seed ideas, as that reading predicts [Fig. 9b] (image).
- **Verdict: AMBIGUOUS**, on which rounds A.2 means, with N_0 UNSPECIFIED under either reading (F-4) [ours].

### D-4 · How many of App. A.2's limits count refinements. Settled: three

- **analysis.md** (A-TOP-2): A.2 counts refinements for two loops, engineering and ablation, and rounds for the others [ours].
- **note-check.md** (A-NOTE-3): three, adding the meta-review's, while the peer-review loop counts rounds [ours].
- **The paper**: "we apply engineering techniques for at most two rounds", "we refine the idea at most once", and "with review-based refinement conducted at most once" (tex:sections/appendix.tex:155) [App. A.2].
- **Verdict: settled.** Three limits count refinements (engineering, ablation, meta-review); the limitation loop and the peer-review loop count rounds [App. A.2] [ours]. The ambiguity of A-TOP-2 itself stands (F-3) [ours].

### D-5 · Do §3.4 and §3.6 say what happens at the limit? Partly settled

- **analysis.md** (A-TOP-1): the text keeps the candidate, in §3.4, §3.5 and §3.6 [ours].
- **note-check.md** (A-NOTE-2, special case B): §3.4 and §3.6 say nothing; the ablation and meta-review rows read *not stated* [ours].
- **The paper**: §3.4's loop sentence ends "ensuring a fully optimized hypothesis prior to manuscript generation" (tex:sections/3_new_method.tex:114) [§3.4]; §3.6's ends "yielding a rigorously validated final contribution" (tex:sections/3_new_method.tex:151) [§3.6]; §3.5 ties its outcome to the limit: "review iterations is reached, producing a polished, thoroughly validated final manuscript" (tex:sections/3_new_method.tex:132) [§3.5].
- **Verdict** [ours]: settled for §3.5, which keeps the manuscript explicitly. In §3.4 and §3.6 the closing clause follows both endings of the loop, the limit and the good verdict, so keeping is implied, not stated [inferred]. No sentence of §3 supports discarding at the limit. A-TOP-1's class, INCONSISTENT, rests on §3.5 alone; both documents need an edit (F-5).

### D-6 · How many rejections Appendix B gives the ablation critic. Settled: one

- **analysis.md** (A-ABL-1) cites TeCh alone, and **claims/appendix-b.md** (C-APPB-9) sends RALI's rejection to the subset and full-set critics [ours].
- **note-check.md** (A-NOTE-4) is headed *App. B reports rejections* and counts RALI; **artifacts.md** (A-ART-4) cites RALI under the same question [ours].
- **The paper**: on TeCh, "the ablation critic rejected it because" (tex:sections/appendix.tex:222-223) [App. B]; on RALI, "an earlier variant was rejected by our own critic as statistically inert" (tex:sections/appendix.tex:324-325) [Tab. 16], which names no critic; and §3.2's subset critic can discard an idea: "If performance is substantially inferior to the baseline" (tex:sections/3_new_method.tex:43) [§3.2].
- **Verdict: settled.** One rejection, TeCh's, is the ablation critic's. RALI's can be any critic's, the subset critic's `Bad` included, so it is no evidence for A-ABL-1 (F-6) [ours].

### D-7 · Which agents run on Claude Code. Open, with a lean

- **analysis.md** (A-CFG-1): AMBIGUOUS for the baseline coder, both engineers, A_FullEng, the integrity Coding Agent and both planners [ours].
- **note-check.md** rates the note's N-9 TRUE, putting the baseline coder and the engineers on Claude Code by §4.2's rule, marked [inferred]; **artifacts.md** (P-ART-3) puts A_FullEng on Claude Code as the *Idea Experiment Coding Agent*, without a mark [ours].
- **The paper**: "Unless otherwise specified, we employ Gemini 3.6 Flash for all agents", then four named exceptions (tex:sections/appendix.tex:155) [App. A.2]; "we leverage Claude Code with Opus 4.8 whenever coding capabilities are required" (tex:sections/4_experiment.tex:46) [§4.2]; Figure 3's experiment boxes hold only a *Coding Agent* and a *Critic Agent* in a cycle, with no separate engineer [Fig. 3] (image).
- **Verdict: open** [ours]. A.2's own "Unless otherwise specified" lets §4.2's rule send every agent that writes or runs code to Claude Code, and Figure 3 folds engineering into the Coding Agent, so the text leans that way. A.2's explicit list of four keeps the other reading alive, and the two planners are open under either. The row stays AMBIGUOUS; N-9 and P-ART-3 should show their inference (F-9).

### D-8 · What the time per task measures. Settled: the paper does not say

- **note-check.md** (summary item 6, N-60, special case C) calls it wall-clock days per task; **claims.md** (U-COST-3) lists wall-clock against busy time as unstated [ours].
- **The paper**: Figure 10a's axis, *Required Time per Task (Days)* [Fig. 10a] (image); §4.3, the engine needs 2–3 days "to complete the entire research cycle" (tex:sections/5_discussion.tex:4) [§4.3].
- **Verdict: settled.** The paper never says how time was measured. Wall-clock is the natural reading of "complete the entire research cycle", but it is [inferred], and note-check.md should mark it so (F-8); its conclusion stands, since machine-days cannot be derived either way [ours].

### D-9 · Why the Procrustes-DS run had no rebuttal. Open

- **analysis.md** (stages/05, evidence on the rounds) reads it as consistent with a rebuttal that runs only below the score threshold, marked [inferred]; **artifacts.md** (U-ART-19) says Appendix C gives no reason [ours].
- **The paper**: "since Procrustes-DS did not undergo this process" (tex:sections/appendix.tex:344) [App. C], and nothing more; the alignment audit quotes the method sections of a manuscript, so a draft existed [p. 48] (image).
- **Verdict: open.** A first review at 8 or above is one reading; a review loop that never ran for this task is another; the paper gives no reason (F-10) [ours].

### D-10 · How far an engineering step may change the idea. Open

- **artifacts.md** (A-ART-5) reads §3.2's trigger as a bound, so the p. 40 redesign, had it followed an `Engineer` verdict, would exceed §3.2's wording [ours].
- **analysis.md** (stages/02, section 4) reads §3.2's engineer as refining h itself, which A_Coder returns [ours].
- **The paper**: the `Engineer` case is an idea that "shows potential but requires hyperparameter tuning or code adjustments", whereupon the Subset Engineering Agent refines h and its code (paraphrase) (tex:sections/3_new_method.tex:45) [§3.2]; Eq. 2 returns h [§3.2, Eq. 2].
- **Verdict: open.** The paper says when the engineer acts, and that h may change; it bounds neither how far nor in what way (F-11). A-ART-5's row proposes a decision of ours [ours].

### D-11 · Different classes for one question. Settled by choosing one class per row

| Row | Classes as filed | Chosen | Why [ours] |
|---|---|---|---|
| A-TOP-1 | INCONSISTENT (A-TOP-1, A-NOTE-2), AMBIGUOUS (A-LIM-1), UNSPECIFIED (U-ABL-4) | INCONSISTENT | Listing 1's `None` contradicts §3.5's explicit clause (D-5); the other two are silent instances of the same rule [ours] |
| A-EVO-1 | INCONSISTENT (A-EVO-1), AMBIGUOUS (A-NOTE-8, its N_0 half) | AMBIGUOUS | one reading of App. A.2 removes the contradiction (D-3) [ours] |
| A-FULL-1 | AMBIGUOUS (A-FULL-1, A-NOTE-5), UNSPECIFIED (U-ART-20) | AMBIGUOUS | two readings, each with its quote [ours] |
| A-INT-1 | INCONSISTENT (A-INT-1, A-NOTE-10), AMBIGUOUS (A-ART-2) | INCONSISTENT | §4.2 and App. B contradict each other; A-ART-2 only asks which side wrote pp. 47–50 [ours] |
| A-INT-3 | AMBIGUOUS (A-INT-3), UNSPECIFIED (U-ART-9) | AMBIGUOUS | "the Coding Agent" has two readings [ours] |
| U-EVAL-1 | UNSPECIFIED (U-EVAL-1, U-NOTE-2), AMBIGUOUS (A-EVAL-2) | UNSPECIFIED | the formula is absent; its reference is the ambiguous half [ours] |
| U-EVAL-8 | UNSPECIFIED (U-EVAL-8), INCONSISTENT (A-EVAL-6) | INCONSISTENT | two numbers in the paper disagree; the missing definition is the likely cause [ours] |
| U-EVAL-10 | UNSPECIFIED (U-EVAL-10), INCONSISTENT (A-EVAL-7) | INCONSISTENT | Table 4 is framed as a head-to-head, and App. B denies that it is one [ours] |
| A-EVAL-5 | AMBIGUOUS (A-EVAL-5), UNSPECIFIED (U-NOTE-6) | AMBIGUOUS | a round has two readings, and its count is unstated under both [ours] |
| U-NOTE-4 | UNSPECIFIED (U-NOTE-4, U-ART-6, U-ART-8), INCONSISTENT (A-ART-3) | UNSPECIFIED | the protocol is absent; A-ART-3's contradiction on scope is one parameter of it [ours] |

### Reconciled on a close reading

- **Agent counts** [ours]: note-check.md (N-4) counts 15 non-coding agents named in §3.1 to §3.6, and analysis.md (section 7) 24 stage agents and 3 integrity agents; the sets differ, and the two lists agree [§3.1] [§3.6] [§4.2].
- **ScholarPeer's backbone** [ours]: note-check.md (N-115) puts it under App. A.2's Gemini default [inferred], while analysis.md (P-ROSTER-21) and claims.md (U-EVAL-2) call it unstated, and stages/05 (U-PEER-3) adds that A.2's default would make it Gemini 3.6 Flash; all agree that the paper names no backbone [App. A.2] [§3.5].
- **What N_peer counts** [ours]: A-PEER-1 favours two rebuttal cycles, and note-check.md's special case C counts two [Tab. 5] [App. A.2].
- **Figure 10b's shares** [ours]: claims.md and note-check.md read the same values, 44.9% of the time and 45.4% of the cost for idea refinement [Fig. 10b] (image).
- **The full-set engineering limit** [ours]: A-FULL-2 and A-NOTE-9 give the same two readings in opposite order, and both session bounds take the same one [App. A.2].

### Still open after this pass

- **D-2, in part** [ours]: whether budgets reset for the meta pass (U-META-1), and whether the integrity checks are sessions of their own (A-INT-3).
- **D-7** [ours]: the model of the code-writing agents that App. A.2 does not name, and of the two planners (A-CFG-1).
- **D-9** [ours]: why Procrustes-DS had no rebuttal; this bears on no row, only on how far Appendix C shows the review loop [App. C].
- **D-10** [ours]: how far a §3.2 engineering step may change an idea (A-ART-5) [§3.2].

## Fixes the source documents need

For each document's owner to apply; this register edits nothing else [ours]. Each fix names its place, the edit, and the entry above that motivates it [ours].

- **F-1 · note-check.md, A-NOTE-8.** Add Figure 9's evidence: the rounds are labelled *Initial*, then *Round 1* to *Round 4*, and 4 of 49 tasks pick an idea from *Round 4*, which favours reading 1; say that "up to 10 ideas" assumes N_0 = 2, and that N_0 = 1 gives 9 (D-1) [Fig. 9b] (image) [ours].
- **F-2 · note-check.md, special case C and N-106.** Redo the bound with 9 or 10 ideas: 81 + 4N_t or 87 + 4N_t (93 or 99 at N_t = 3), and 10 to 55 or 11 to 61 sessions without a success; name the two assumptions left, no ablation refinement in the meta pass (U-META-1) and 2 integrity sessions, and point to analysis.md section 9 (D-2) [App. A.2] [ours].
- **F-3 · analysis.md, A-TOP-2 in section 10.1.** App. A.2 counts refinements for three loops, not two: add the meta-review's "with review-based refinement conducted at most once" (D-4) [App. A.2] [ours].
- **F-4 · stages/03, A-EVO-1, and analysis.md, its row in section 10.2.** Change the class to AMBIGUOUS, since reading A.2's rounds as k ≥ 1 removes the contradiction; N_0 stays unset (D-3) [§3.3] [App. A.2] [ours].
- **F-5 · note-check.md, A-NOTE-2 and special case B (the ablation and meta-review rows, and the tally); analysis.md, A-TOP-1.** §3.4 and §3.6 imply keeping through their closing clauses: note-check.md should say *implied* [inferred] instead of *not stated*, quoting the clauses, and analysis.md should mark §3.4 and §3.6 as implied and §3.5 as explicit (D-5) [§3.4] [§3.5] [§3.6] [ours].
- **F-6 · note-check.md, A-NOTE-4 (its heading and its App. B bullet) and special case B's ablation row; artifacts.md, A-ART-4.** RALI's "our own critic" names no critic; count one ablation-critic rejection, TeCh's (D-6) [App. B] [Tab. 16] [ours].
- **F-7 · stages/04, A-ABL-2.** Appendix B describes TeCh's end as a rejection by the critic, not as a failed comparison, so it supports reading 2 only under A-ABL-1's reading 2; say so, and decide the two together [App. B] [§3.4] [ours].
- **F-8 · note-check.md, summary item 6, N-60, and special case C (time).** Mark *wall-clock* as [inferred], as claims.md's U-COST-3 does (D-8) [Fig. 10a] (image) [ours].
- **F-9 · analysis.md, A-CFG-1; note-check.md, A-NOTE-6, N-9; artifacts.md, P-ART-3 and its row in section 5.** Quote A.2's opening "Unless otherwise specified" and Figure 3's experiment boxes, which draw no separate engineer, as evidence for reading 2; and in N-9 and P-ART-3, show the inference that puts the baseline coder, the engineers and A_FullEng on Claude Code, citing A-CFG-1 (D-7) [App. A.2] [Fig. 3] (image) [ours].
- **F-10 · stages/05, "Evidence on the rounds".** Beside the threshold reading, give the other readings of "did not undergo this process", as artifacts.md's U-ART-19 does (D-9) [App. C] [ours].
- **F-11 · artifacts.md, A-ART-5.** Its reading 2 exceeds the trigger's wording, not §3.2's: §3.2 also has the engineer refine h, and Eq. 2 returns h (D-10) [§3.2] [§3.2, Eq. 2] [ours].
- **F-12 · claims.md, U-EVAL-1 and A-EVAL-2.** Their decisions differ, one pre-registered reference value against both references reported; align them with the merged row U-EVAL-1 [§4.1] [ours].
- **F-13 · note-check.md, A-NOTE-9.** Number the readings as A-FULL-2 does, reading 1 being the subset critic alone [App. A.2] [ours].
- **F-14 · note-check.md, the paragraph under "Gaps found here".** It says consolidation moves the entries into unspecified.md; the README keeps each entry where it was filed, so it should say the entries are indexed here [ours].
- **F-15 · claims.md, U-BENCH-1.** The screening subset's gap is U-BASE-1, under the key BASE, not the key SUB; point to U-BASE-1 [§3.2] [ours].
- **F-16 · analysis.md, section 9.** Add the lower bound that D-2 carries over from note-check.md: 16 sessions at N_0 = 2 and N_p = 5, 18 at N_0 = 1 with an end-of-round stop test [§3.3] [ours].
- **F-17 · every gap section.** Add to each full entry the register row it maps to, for example *Register: A-TOP-1*, so that a reader of an entry finds its decision [ours].
