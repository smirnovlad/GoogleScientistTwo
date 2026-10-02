# U-TOP-5 · Which split each decision reads

**For** task 3's contracts of the scoring runner and of the run state, and task 2's stages, which read only what these rules allow. The terms and the cross-cutting rules IR-32 to IR-40 are in the [index](../blocking-decisions.md) [ours].

**Status:** second version, 2026-10-02, after the wave-1 review [ours]. **This file applies:** F-1, F-4, F-6, F-10, F-12, F-14, F-21, F-28, F-30, F-31, F-38, F-43 and F-44, and the parts of F-3, F-5, F-7, F-9, F-11, F-17, F-19, F-22, F-24, F-35, F-40 and F-46 that bear on U-TOP-5; and the coordinator's amendments A1 and A6 (the reads of report decided in place), A2 (costs as usage, not bills), A4 (job arguments) and A5 (C_base's hash check) [ours].

*Row U-TOP-5, aliases U-NOTE-1 and U-ART-5, of [unspecified.md](../../paper/unspecified.md); the full entries are in analysis.md section 10.1, note-check.md and artifacts.md* [ours].

## 1. The choice

- **IR-10 · Three roles and two seed lists, built before any run.** [ours]
  - IR-10.1 For every setting, the manifest defines three disjoint data roles, each by a hashed index file: fit (the inputs and labels a method may learn from, including any validation set the task's protocol trains or selects on), search (our validation split) and report (our test split). It names the part of search that §3.2's subset row reads; every full-set setting exists in search and in report, and the full benchmark we report is report over every setting [§3.2] [ours].
  - IR-10.2 The manifest holds two disjoint seed lists: search seeds, for every fit whose artifact is scored on search, and report seeds, for E_base's report fit at admission, for the test event's report fits (IR-14.4) and for I1's re-fits (IR-23.2). A rollout's episode seeds are disjoint across roles in the same way (IR-8.3) [ours].
  - IR-10.3 Task packaging builds the roles, never an engine agent. At admission, the overlap between any two roles is zero by item ID, by content hash, and by the manifest's near-duplicate detector, or the task is refused. The detector, by default: for images, a 64-bit perceptual hash at a Hamming distance of at most 10; for text, MinHash over word 5-grams at an estimated Jaccard similarity of at least 0.8; for tabular rows, equality after rounding each feature to the manifest's precision; for time series, IR-19.2's check. Task 5 keeps a default unless, on 100 re-encoded, resized and cropped copies of the task's own items, it finds fewer than 99, or it flags more than 1% of 1,000 random pairs across roles; it then moves the threshold until both hold, and records it [ours].
  - IR-10.4 Data outside the manifest has no role and yields no result, whoever fetched it [ours].
- **IR-11 · Who reads what.** [ours]
  - IR-11.1 The table below holds for every job, in every scope [ours].

| Job | fit | search inputs | search labels | report inputs | report labels |
|---|---|---|---|---|---|
| an agent session, or any LLM agent | read | none | none | none | none [ours] |
| a search fit job, at a search seed | read | none | none | none | none [ours] |
| a search scoring, its predict step | read | read | none | none | none [ours] |
| a search scoring, its metric step | none | none | read | none | none [ours] |
| a report fit job, at a report seed | read | read under IR-19 option (2), else none | read under option (2), else none | none | none [ours] |
| a report scoring, its predict step | read | as its report fit | as its report fit | read | none [ours] |
| a report scoring, its metric step | none | none | none | none | read [ours] |

  - IR-11.2 A predict step runs agent code without network, with no write path to any place that an agent or a later session can read, on inputs under identifiers and in an order that the runner assigns per job, within what the manifest's input format allows [ours].
  - IR-11.3 A predict step sees the same paths and environment in every kind of job, so that agent code can tell a search scoring from a report scoring only by the inputs themselves [ours].
  - IR-11.4 The first row is a cut of what a model reads: no session reads search inputs. Who chose it: task 6. What it loses: per-item error analysis on search, which stays available on the validation part of fit [ours].
- **IR-12 · Every decision of the loop reads search, or no data role.** Section 2's table maps every decision of analysis.md section 4.2 to the role it reads; no decision of the loop reads report [ours].
- **IR-13 · Search scorings belong to the engine, and are bounded.** [ours]
  - IR-13.1 Engine code triggers a search scoring once, at the end of each result-producing unit of work (U-CFG-2); agent code cannot trigger one [ours].
  - IR-13.2 Inside a session, agent code may call a format check, which runs its predict step on fit items and returns pass or fail, never a score [ours].
  - IR-13.3 The run ledger counts each candidate's released search results per identity, with the attempts beside them (IR-33.5). One counter per candidate, its stage's limit, bounds its search scorings and its refinements together; a G2 retry, if task 2 allows one, uses up a refinement (IR-40.1) [ours].
  - IR-13.4 The cap derives from the stage's limit and is never a second number: for an idea on the subset, 1 + N_eng under A-TOP-2's proposal [ours].
- **IR-14 · The freeze, and the run's one test event.** [ours]
  - IR-14.1 Engine code writes the freeze when the last decision that can change code or rows has been made: the meta-review stage ends with `Accept`, with N_meta spent, or with a refinement discarded. It is computed from run state alone, written atomically and content-hashed; a crash while writing it rewrites the same hash. No freeze, no test event (hook G6) [ours].
  - IR-14.2 *ours* is the row of C_best in the run state when the freeze is written, which is the code exported as C+ [ours].
  - IR-14.3 The freeze lists exactly these rows: *ours*; E_base; C_base, unless its code hash equals E_base's (IR-4.3); every row of the last downstream pass (analysis.md section 4.1), which are its ablation rows, its A_FullEng refinement if there is one, and its rebuttal rows; and the controls and diagnostics that task 6 registers in advance (each round's best for U-EVAL-8, the null-idea controls), each marked as such. A row is a code hash with its job arguments (IR-32.1), so a mechanism-off control is a row of its own, and is listed. No row is added or left out by reading the manuscript, and a control or diagnostic row never takes the role *ours* [ours].
  - IR-14.4 The test event: for every frozen row but E_base, and every report seed, a report fit job fits the row's code hash, with its job arguments, at that seed, on fit, or on fit ∪ search where search was carved from fit (IR-19 option (2)), following IR-3's lineage, so that a post-hoc row reads E_base's report fit of the same seed (IR-3.5); report scorings then score that artifact on report, once per setting. E_base's report results are its admission records (IR-15), except for a time metric, where the test event times E_base again in the same job as the rows it is compared with (IR-8.1) [ours].
  - IR-14.5 Each test-event identity (the freeze hash, the row, the report seed, the setting, the kind) has exactly one released result (IR-33). A run has one freeze and one test event, and the runner refuses a report job whose identity the freeze does not list [ours].
  - IR-14.6 Exactly four kinds of job read report, by scope: E_base's report fit and the sealed check, at admission, once per baseline key (IR-15, task scope); the test event, once per run (run scope); a correction event, beside the originals (IR-41, run scope); and the audit's re-fits, which verify and never replace a reported value, and are counted in the audit ledger, never in the run's (IR-23, audit scope). The runner refuses every other [ours].
- **IR-15 · The sealed baseline check, at admission.** [ours]
  - IR-15.1 E_base's report fits, at the report seeds and on the same data as IR-14.4's, its report scorings and the check run at admission, with task scope, before any run of the task can be registered; runs refer to these records by ID and never write them [ours].
  - IR-15.2 Once per task means once per baseline key: the hashes of the scoring items, the index files and labels, E_base's commit and diff, the environment image, the pinned weights, the seed lists and the settings. Another manifest edit, such as a rule's wording or a citation, keeps the key and does not repeat the check; a changed published number is compared again with the sealed values, without a new read of report, and counts as an attempt [ours].
  - IR-15.3 Before the first attempt, the manifest fixes the seed count and the tolerance formula. The formula's inputs are E_base's spread across its search seeds (scored earlier at admission, IR-4.2), the published spread where G's paper gives one, and the sampling error of a carved report split (IR-19 option (3b)) [ours].
  - IR-15.4 The check is one-sided: it fails only when E_base's report aggregate is worse than the published number by more than the tolerance [ours].
  - IR-15.5 A task gets at most k attempts, across manifest versions, with k fixed in its first manifest. A released check result is an attempt; a crashed job that released nothing is re-run under its identity, and is no attempt (IR-33.3). Every attempt is reported. Packaging iterates on search, and reads report only for a check [ours].
  - IR-15.6 The check releases only pass or fail, and the tolerance used. Its values stay sealed from every agent, prompt and manuscript until the test event, where they become E_base's report results. The packagers see pass or fail only: a process rule, recorded by the task store's access log, which the setup cannot enforce against administrators [ours].
  - IR-15.7 A baseline that fails is never admitted: no run of the task can be registered, and the task is reported among the tasks considered, with its attempts. This replaces U-BASE-2's branch [ours].
  - ⛔ WHY NOT run the check before round 0, as the first version allowed: runs of one task started in parallel would race for a job that the runner allows once per baseline key, and the loser would halt [ours].
- **IR-16 · Before the freeze, manuscripts carry search numbers.** Every manuscript that the reviewer, the rebuttal planner or the meta-reviewer reads takes its result numbers from search records, labelled as validation results [§3.5] [§3.6] [ours].
- **IR-17 · After the test event, only text changes.** [ours]
  - IR-17.1 After the test event, no code, configuration, artifact, seed, row or role changes, and no decision of analysis.md section 4.2 runs, except the integrity checks G3 to G5 of the tail (IR-39), whose fixes edit text only: no critic, Selector, Result Comparison, review threshold, meta-review, rebuttal planner or coder. Hook G7 refuses every other step [ours].
  - IR-17.2 Engine code fills the manuscript's result numbers from the verified table, its search and report columns both (the final fill); the writer then changes text only, and a request for a new experiment is refused [ours].
  - IR-17.3 A correction event (IR-41) changes no text of an exported paper; its values are reported beside it [ours].
- **IR-18 · The campaign, repeated runs and the configuration key.** [ours]
  - IR-18.1 Before the first reported run, the campaign record fixes: the final-test tasks with their manifest hashes; the number of runs per task; the configuration hash, over code, prompts, schemas, routing, limits and budgets; the reporting auditor's configuration hash (IR-29.2); the aggregate, registered in advance; and the causes that allow a fresh start, with their bound per task [ours].
  - IR-18.2 Engine code registers every run in the run registry before it starts: run ID, campaign, task, manifest hash, configuration hash, engine commit, guard configuration (IR-38) and seed. A run of a final-test task registered after any test event of that task in the campaign is refused, unless it is a fresh start under IR-18.4 [ours].
  - IR-18.3 The aggregate is computed per (manifest hash, configuration hash); a run under another configuration starts a new set, and is never pooled with it [ours].
  - IR-18.4 No run is restarted, re-seeded or dropped because of any result, search or report. An infrastructure halt resumes the run (IR-34). A fresh start, for a cause on the campaign's list and within its bound, is a new registered run, and the old one stays in the aggregate as a failure, with its cause. A crash, timeout or out-of-memory error that agent code causes is a run failure, never infrastructure (IR-33.4) [ours].
  - IR-18.5 Task 5 marks each task as development or final-test. A final-test task runs only under a campaign whose configuration hash was fixed before its first run. A development task's report numbers are validation for the engine: its builders may read them, and they are never evidence in a reported table or claim [ours].
  - IR-18.6 Every registered run of a final-test task enters the aggregate; a run that ended without a test event, or in the tail's end state (IR-39.3), counts as a failure [ours].
- **IR-19 · Building search, per kind of data.** [ours]
  - IR-19.1 Data whose items are independent: packaging builds search in this order of preference. (1) The protocol's own validation set, if the protocol neither trains nor selects on it. (2) A seeded, stratified carve-out of fit; report fits then train on fit ∪ search (IR-14.4), which restores the protocol's training size for the comparison with published numbers. (3) Only where the evaluation needs data that fit cannot supply, such as OOD sets or unseen domains: (3a) validation sources disjoint from the test sets, as the protocol or its successor defines them, before (3b) a seeded, stratified carve-out of each official test set, the rest being report [ours].
  - IR-19.2 Temporal data: each role is one contiguous block, in time order, fit before search before report, and the check runs on target timestamps: no target timestamp lies in two roles, and every target of a role precedes every target of the next. At each boundary that packaging builds, a gap of at least T + L steps (the lookback plus the horizon) separates the last target of one role from the first target of the next, so that no window of either role reaches the other's targets; the gap is taken from the role packaging builds, never from report. A boundary the protocol defines keeps the protocol's borders. Time-Series-Library's loader for the ETT data, for one, cuts contiguous blocks of 12, 4 and 4 months, starts each later block's inputs one lookback before its border, so that inputs cross a border backwards in time while targets never do, and fits its scaler on the training block alone ([data_provider/data_loader.py](https://raw.githubusercontent.com/thuml/Time-Series-Library/main/data_provider/data_loader.py), fetched with curl on 2026-10-02) [ours].
  - IR-19.3 Grouped data (subjects, patients, series): roles are built by group, and the overlap check runs on group IDs as well as on items; a group in two roles refuses the task [ours].
  - IR-19.4 OOD data: under (3a), OpenOOD v1.5 is the model. For its CIFAR benchmarks it holds 1,000 images of the ID test set out as ID validation, and 1,000 Tiny ImageNet images from 20 categories, held out from and disjoint with its OOD test sets, as OOD validation, so that hyperparameters are never set on test samples ([OpenOOD v1.5, arXiv:2306.09301v5](https://arxiv.org/abs/2306.09301v5), its sections 3 and 4, fetched with curl on 2026-10-02). Under (3b) the candidates are selected with access to the test OOD distributions, unlike the published baseline, and every gain says so (U-EVAL-1) [ours].
  - IR-19.5 Power: carving a fraction f off an official test set multiplies report's standard error, and its minimal detectable effect, by 1/√(1−f): ×1.054 at f = 0.1, ×1.118 at 0.2, ×1.195 at 0.3, ×1.414 at 0.5. Task 5 admits the task only if report keeps the power it requires [ours].
  - IR-19.6 The manifest records, per setting, the option used and why, its seed, the sizes and the power multiplier; under (3b), the published numbers come from a different sample than report, and every gain against them says so [ours].
- **IR-41 · The correction event.** [ours]
  - IR-41.1 A defect found in a locked scoring item after a test event is filed by a person, with a control that shows it: an input on which the old item gives a wrong value and the corrected item the right one [ours].
  - IR-41.2 The correction event re-runs, with the corrected item (a new manifest version), the frozen identities that the defect touched: the report scorings, and the report fits as well if the defect touched what a fit reads, at the same report seeds and from the same code hashes; E_base's identities are corrected in the same event. It reads report besides the one test event, and, by task 6's decision in the index's section 7, is not a use of report in the sense of `CLAUDE.md`'s rule, since nothing it produces feeds a decision [ours].
  - IR-41.3 Its values are reported beside the original values, never in their place, with the cause and the control. No decision reads them, and *ours*, the rows, the code and the exported text stay as they were [ours].
  - IR-41.4 Its records go to the run's correction ledger (IR-5.6), under identities of their own; one correction event per defect and run [ours].

## 2. Every decision in the loop, and the role it reads

| Decision, from analysis.md section 4.2 | What it reads |
|---|---|
| Are the limitations enough? How novel is an idea? | no data role: G's paper and the literature [§3.1] [ours] |
| Does the idea beat the baseline on the subset? | search, the manifest's subset: the idea's records and E_base's [§3.2] [ours] |
| Does it beat the SOTA on the full set? | search, every setting; the reference that A-FULL-1 picks, also on search [§3.2] [ours] |
| Stop the idea rounds? | no data role: the verdict counts [§3.3] [ours] |
| Which idea is best? | the search records of every `Good` idea [§3.3, Eq. 4] [ours] |
| Is the component breakdown clean? | the search records of the ablation rows [§3.4] [ours] |
| Keep a refinement, in §3.4 and in §3.6? | the search records of E_new and E_best [§3.4] [§3.6] [ours] |
| Is the review good enough? Does it meet the venue bar? | a manuscript whose result numbers are search numbers (IR-16) [§3.5] [§3.6] [ours] |
| Does a solution break the rules? Does the paper match the code? | the code, the task rules and the manuscript; no data role [§4.2] [ours] |
| Is a citation hallucinated? | the bibliography and the lookup records; no data role [§4.2] [ours] |
| Which numbers go into the paper? | before the freeze, search cells; after the test event, search and report cells, filled by engine code (IR-17.2) [§3.5] [ours] |
| Which data answers a reviewer? | the manifest's data only, scored on search; every rebuttal row of the last pass enters the freeze (IR-14.3) [§3.5] [ours] |
| What does the full set contain? | the manifest's settings (U-BASE-1), never an agent's choice [§3.2] [ours] |
| Does C_base differ from E_base? (IR-4.3) | their code hashes, at the start of the run; if they differ, search, before any idea is scored [ours] |
| Does the baseline reproduce? (U-BASE-2) | report, sealed, at admission (IR-15) [ours] |
| The post-hoc audit's I1 | report, after export, through re-fits under the audit's identity (IR-23) [ours] |
| A correction (IR-41) | report, after a test event, beside the originals [ours] |

## 3. The attacks these rules stop, with the evidence

- **Steering the search on the reported data.** The Selector compares ideas "evaluated on the full benchmark" [§3.3] (tex:sections/3_new_method.tex:90). The critic's account of the X-Mahalanobis redesign cites an OOD set that the final report publishes, "CIFAR-10 AUROC drops from 96.83% to 88.02%" [p. 46] [p. 40] (image), and that this steered the redesign is our inference [inferred]. The ablation agent swept eight layer-weighting variants, γ among them, on the six OOD sets, and kept γ = 2.0, the default, although γ = 3.0 scored best on both averages, 99.58 / 2.13 against 99.56 / 2.17 [pp. 43–45] (image): the search saw the test sets, and did not pick γ on them, as task 1's fix F-AR-2 concluded (artifacts.md). Each reported gain is then the best of up to 9 or 10 candidates, measured on the data that chose them (D-1; claims.md, P-EVAL-2) [App. A.2]. Stopped by IR-10 to IR-14 [ours].
- **Test data within an agent's reach.** The audit, after the search, says "I extracted test features fresh from the checkpoint" [p. 47]. This shows that test data was within an agent's reach, not that the search was steered by it. Stopped by IR-11 [ours].
- **Training-seed luck carried to the test set.** The trace fine-tuned one checkpoint, at seed=0, which the method and its ablations reuse [p. 40] [p. 45] (image). In ScientistOne's audit, 9 of 13 value mismatches were "within 5% of the paper-reported number—small enough to plausibly arise from unreported seed variance, but uniformly biased towards a better-than-rerun headline" [Ref: meng2026scientistone App. E.1] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:127-129). When the test split scores the artifact that search selected, the fit's luck goes with it: with fit noise equal to evaluation noise and 20 null candidates, the winner's +2.65 on search keeps +1.32 on report (`playground/integrity/reviews/research-engineer/null_control.py`, 20,000 replications, seed 20261002, run again 2026-10-02). Stopped by IR-14.4's re-fit at the report seeds [ours].
- **Picking the best row after the fact.** In ScientistOne's audit, the writing stage of Sakana's AI Scientist v2, not ScientistOne's own, "selects the most favorable score from ablation-stage nodes rather than the score of the node whose code is used as the final solution", while ScientistOne itself "achieves perfect score verification (12/12)" [Ref: meng2026scientistone §6.1] (ref:2605.26340v1:sections/06b_integrity.tex:39) (ref:2605.26340v1:sections/06b_integrity.tex:45). Stopped by IR-14.2's binding of *ours* to C_best, IR-14.3's freeze from run state, and G3 [ours].
- **Querying the test set while searching.** ScientistOne let its agent "query the grading server up to 16 times to obtain evaluation scores on the test data", a departure from MLE-Bench's official protocol, which "restricts evaluation to a single submission of the final generated solution" [Ref: meng2026scientistone App. F] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:567). Stopped by IR-11 and IR-14 [ours].
- **The best of several runs, and runs added later.** ScientistOne's practice was that "No run was re-attempted to improve solver scores", while runs that crashed for infrastructure were re-attempted with fresh state, "up to 3 attempts per run", and 16 of its 75 runs needed a retry [Ref: meng2026scientistone §6] (ref:2605.26340v1:sections/06a_setup.tex:29) (ref:2605.26340v1:sections/06a_setup.tex:31). ScientistTwo states no number of runs per task [§4]. Stopped by IR-18 [ours].
- **Learning the split from inside a scoring job.** A predict step that saves the search inputs for a later session, reads a native file name, or branches on a path, learns what it is scored on. Stopped by IR-11 [ours].
- **Iterating the packaging against the test split.** A sealed check counted per manifest hash restarts with every manifest edit, so that a person could adjust the packaging diff until the check passes; a two-sided check would fail a baseline stronger than published, which invites weakening it. Stopped by IR-15.2 to IR-15.5 [ours].

## 4. Guards and their controls

Every outcome below was stated before any control ran. Unless the last cell says otherwise, a control runs with scripted agents on the production setup (IR-37), on a CPU, with no LLM call [ours].

| Guard | Class | Planted attack | Expected with the guard removed | Expected with the guard in place | Mode, cost |
|---|---|---|---|---|---|
| IR-10.3 | setup | 10% of report's items copied into search under new IDs: half exact, half near-duplicates (re-encoded at JPEG quality 75, resized by 0.9, cropped by 5%) | the search rewards the copied items | admission refuses the task: the exact copies by hash, the near ones by the detector [ours] | as above |
| IR-10.2 | setup | a search fit job is passed a report seed | report's seed draws reach the search | refused: the seed is not on the search list [ours] | as above |
| IR-11 | setup | agent code opens the label paths; a predict step writes the search inputs to the workspace; a predict step branches on the job's path; a report fit under option (1) opens search | a perfect score; the next session finds the inputs; search and report behave differently; the report fit trains on search | the files are absent, nothing is written, the branch never fires, and search is not mounted [ours] | as above |
| IR-12, IR-14.4 | setup | the null-idea control, below | see below | see below [ours] | as above, 200 replications |
| IR-13 | setup | agent code calls the search scoring in a loop to tune; a search scoring is killed and run again | many scorings, and search overfitted; the re-run counted twice | the calls are refused; the killed scoring's re-run releases one result under its identity, and the count stays 1 [ours] | as above |
| IR-14.2, IR-14.3 | setup | the writer presents the best ablation row as the method and leaves *ours*' row out of its tables | the best ablation row is test-scored as *ours* | the freeze, computed from run state, binds C_best's row and lists every row of the last pass [ours] | as above |
| IR-14.5, IR-14.6 | setup | after the test event, a second test event, or *ours* rebound to the best ablation row | the best variant is reported | both refused, and G3 rejects the manuscript [ours] | as above |
| IR-15 | setup | a packager edits the diff and runs the check 4 times at k = 3; a rule's wording is edited; a baseline better than published; two runs of the task registered at once | report read 4 times; the check repeated; the strong baseline failed; the second run halted | the fourth attempt refused; the check not repeated; the strong baseline passes; both runs refer to the admission records [ours] | as above |
| IR-15.6, IR-16 | setup | the sealed value is put into a critic's prompt or a draft | report numbers reach the loop | no record a session can read holds it, and drafts hold search cells only [ours] | as above |
| IR-17 | setup | after the test event, the writer asks for a new rebuttal experiment; G5 finds a component the code lacks | a row is added after the test; under the first version's wording, G5 could not block | the request is refused; G5 blocks export until the text is fixed [ours] | as above |
| IR-18 | setup | a fourth run registered after three test events; a run dropped after a bad search trajectory; a run under a changed loop limit; a crashed run restarted with fresh state | the fourth run counted; the drop raises the rate; the runs pooled across engines; the restart re-rolls | refused; counted as a failure; a new set; refused, and resumed instead [ours] | as above |
| IR-19.2, IR-19.3 | setup | a carve-out of random windows from a time series; one subject in two roles | search targets inside fit windows; a subject seen in fit is scored | refused at admission by the target-timestamp check and the group check [ours] | as above, temporal and grouped fixtures |
| IR-41 | setup | a defect planted in a scoring item (NaN averaged as 0), found after the test event | the corrected values replace the originals, or whole runs are re-run | the corrected values appear beside the originals, with the cause and the control [ours] | as above |

- **The null-idea control (IR-12, IR-14.4), through the engine's own loop.** Scripted null candidates, whose true gain is 0. A fitted artifact's quality is fit noise, drawn per row and seed with standard deviation σ_a = 1 and baked into the artifact; a scoring adds evaluation noise, drawn per artifact and split with σ_e = 1. Five seeds per role; m, the number of candidates the loop compares, is whatever the loop does, and is recorded per replication; R = 200 replications, seeds 0–199 [ours].

| Arm | What is removed | Expected mean report gain | Pass |
|---|---|---|---|
| guarded | nothing: selection on search, re-fit at the report seeds | 0 | within 0 ± 3 SE [ours] |
| no re-fit | IR-14.4's re-fit: the selected artifacts are scored on report | E[max_m] · σ_a² / (√s · √(σ_a² + σ_e²)), 0.59 at m = 20 and s = 5 | within its prediction ± 3 SE, and above 3 SE [ours] |
| selection on report | IR-12: the loop selects on report | E[max_m] · √((σ_a² + σ_e²) / s), 1.18 at m = 20 and s = 5 | within its prediction ± 3 SE [ours] |

- E[max_m], the expected maximum of m standard normals, is 1.03 at m = 4, 1.49 at 9, 1.54 at 10, 1.87 at 20 and 2.04 at 30; each prediction uses the m the loop recorded, and SE is each arm's standard deviation over √R. The guarded arm's mean gain on search is recorded as the optimism of selection on search, the residual the index lists among the attacks not stopped [ours].
- **The second null control (the A-EVAL-1 constraint of section 7).** R = 1000 null tasks through the loop, seeds 0–999, judged by the pre-registered success rule at its α. With the guard removed, success meaning a positive point estimate, about half the null tasks succeed. With it in place, the success share is at most α + 3√(α(1−α)/R): 0.0707 at α = 0.05 [ours].

## 5. Roads not taken

- ⛔ WHY NOT the paper's way, every decision on the reported benchmark: every reported gain is then the maximum of noisy candidates on the data that chose them, an inflation that no reported variance lets anyone size (claims.md, P-EVAL-2) [§3.3] [ours].
- ⛔ WHY NOT score, at the test event, the artifacts that search selected, as the first version did: the fit's seed luck travels with the artifact, and survives the held-out split (section 3) [ours].
- ⛔ WHY NOT re-fit at the test event with the search seeds: the same seeds give back the same luck, up to nondeterminism [ours].
- ⛔ WHY NOT score the test split right after selection, before ablation and drafting: the ablation critic, the Result Comparison Agent, the reviewer and the meta-reviewer would read test numbers, and a meta refinement could change the method after its test number was known [§3.4] [§3.6] [ours].
- ⛔ WHY NOT let the search see test numbers with noise added: noise lowers what one query leaks but bounds nothing without a formal budget, and every such query breaks the one-use count [ours].
- ⛔ WHY NOT check the baseline on search only: the published numbers are test numbers, so the check would need a tolerance wide enough to let a weakened reproduction through (IR-4) [ours].
- ⛔ WHY NOT a two-sided baseline check: it fails a baseline stronger than published, which invites weakening it [ours].
- ⛔ WHY NOT keep even the check's pass or fail until the end: a baseline that does not reproduce would first cost a whole run, which the paper puts at $3765 on average over the 33 NeurIPS 2025 problems of §4.3, an API-equivalent figure for us [§4.3] [ours].
- ⛔ WHY NOT let the writer revise freely after the test event: a writer that can add rows or rebind *ours* picks the best variant, as the writing stage of Sakana's AI Scientist v2 did in ScientistOne's audit (section 3) [ours].
- ⛔ WHY NOT pool runs across configurations: a new loop limit or a new model would silently change what the reported number averages [ours].
- ⛔ WHY NOT carve random windows out of a time series: windows one step apart share T − 1 inputs and L − 1 targets, so search targets sit inside fit windows; App. D's draft uses a lookback of 512 and a horizon of 64 [p. 61] [p. 62] [ours].
- ⛔ WHY NOT replace a defective item's values in place: the originals are what the run's decisions and its text were made with [ours].

## 6. Relation to the paper and to the register

- **The paper: UNSPECIFIED.** No stage names a split. The full-set agents "perform final validation and engineering against the full benchmark" [§3.2] (tex:sections/3_new_method.tex:52); the Selector reads ideas "evaluated on the full benchmark" [§3.3] (tex:sections/3_new_method.tex:90); both update gates compare E_new with E_best [§3.4] [§3.6]; and the drafter writes up the main benchmark results [§3.5]. Validation appears only inside the agents' own outputs: App. D's generated paper tunes a scale by a grid search on validation splits [p. 61], and the rebuttal's method picks its configuration by an inner cross-validation [p. 51] (image) [ours].
- **What the paper shows next to the gap.** The specification audit checks, as its first item, that no test or OOD data leaks into the method's calibration, and finds none [p. 49] (image) (paraphrase): a separation inside the method, which U-NOTE-1 cites, not a split of the search. App. D's draft runs its first ablation on a subset of the test split, "Frequency decomposition isolation (subset test split)" [p. 69], so test data fed the ablation critic's decision (analysis.md section 4.2) [ours].
- **Where we depart.** One bullet per departure [ours]:
  - **A split for every decision.** Every decision of the loop reads a split the paper does not have, and the comparison with the published SOTA moves from the loop to reporting [§3.2] [ours].
  - **IR-11 and IR-13.** Agent sessions get no data from search or report, and no score. In the paper the coders run the benchmark and produce E themselves, "producing the resulting logs" [§3.2] (tex:sections/3_new_method.tex:40), and in the trace the ablation agent swept eight variants on the six OOD sets inside one plan [pp. 43–45] (image); this changes every coding agent's working loop [ours].
  - **The tail (IR-17, IR-39).** The paper exports at `Accept`: ScientistTwo "finalizes the process and exports the final improved paper and its codebase" [§3.6] (tex:sections/3_new_method.tex:140). We add the test event, the final fill, a text-only revision and G3 to G5, so the exported paper is not the one the reviewers read [ours].
  - **Re-fits at the report seeds (IR-14.4).** The trace reports one fit at one seed, which every row reuses [p. 40] [p. 45] (image) [ours].
  - **The rebuttal's data.** Only the manifest's data, where the paper's one rebuttal chose 50 representative TALENT datasets and capped their test sets at 2000 [p. 51] (image). §3.5 says nothing of data, so this departs from what the paper shows, not from its text [§3.5] [ours].
- **The register's proposal: confirmed, with three changes.** It proposed a validation split inside each task, disjoint from the test split, validation numbers only for every decision in the loop, and one scoring of the test set, at the end, by the harness. Confirmed, and made precise by three roles and two seed lists (IR-10), the freeze and the test event's re-fits (IR-14), and what may change after it (IR-17). Changed: three more reads of report are allowed besides the one scoring at the end; by task 6's decision in the index's section 7, none is a use in `CLAUDE.md`'s sense, since nothing they produce feeds a decision, and any read that could feed one is a violation: (1) the sealed baseline check, at admission (IR-15), because the published numbers it is checked against are test numbers, and a failure found only at the end costs a whole run; (2) the audit's re-fits, after export (IR-23), which the first version also allowed without listing them as a change; (3) the correction event (IR-41) [ours].

## 7. Rows it constrains

| Row (owning task) | The constraint it receives |
|---|---|
| U-BASE-1 (2) | the subset is a manifest part of search, and every full-set setting exists in search and in report [ours] |
| U-BASE-2 (2) | its check reads report at admission, sealed, once per baseline key, one-sided, at most k attempts (IR-15); a baseline that fails is never admitted, so no run starts: this decides its fail branch, in place of the register's proposal that the task ends [ours] |
| A-FULL-1 (2) | the full-set critic's reference is E_base's record on search [ours] |
| A-TOP-1 (2) | the kept manuscript carries search numbers until the test event [ours] |
| A-TOP-2 (2) | its counting value sets IR-13's cap, through one counter per candidate (IR-13.3) [ours] |
| U-TOP-2 (3) | resume from the last finished stage, before or after the freeze; attempts per identity; halts by class (IR-33 to IR-35) [ours] |
| U-INT-3 (2) | the reference and alignment repairs also run in the tail, on text only [ours] |
| U-PEER-1 (5), U-ART-15 (3) | rebuttal experiments use the manifest's data only, and every rebuttal row of the last pass enters the freeze [ours] |
| U-PEER-2 (2) | rebuttal code is kept by its code hash, because its rows are re-fitted at the test event and by I1; whether it stays in C_best and C+ stays task 2's [ours] |
| U-SUB-2 (6) | a tuned baseline is tuned on search within the idea's budget, and enters the freeze as a control [ours] |
| U-EVAL-4 (6) | runs per task follow IR-18: fixed in the campaign record, aggregated per configuration, none dropped [ours] |
| U-EVAL-8 (6) | per-round gains are search numbers during the run, and report numbers only as diagnostic rows of the freeze [ours] |
| A-EVAL-1, U-EVAL-1 (6) | success is never the sign of a point estimate: it is a pre-registered one-sided test on the paired report gain, per report seed against E_base on the same seeds, counting E_base's variance once per task, so that the false-success rate at the null is at most α; no detectable gain is reported apart from failures. Choosing α and the test is task 6's `P1` part [ours] |
| U-ART-12 (6) | two disjoint seed lists per task, search and report, and the seed floor of IR-9.3 [ours] |
| U-TOP-1 (3) | the manifest holds the roles, their index files and construction, the seed lists and the settings [ours] |
| U-TOP-6 (7) | an agent's golden-set test reads search numbers only [ours] |

## 8. Cost, and the tasks it makes inadmissible

LLM work is counted in calls and tokens against the subscription's usage windows (amendment A2); a dollar figure is an API equivalent, labelled as such, never a bill [ours].

| Item | Order of magnitude | Its sample |
|---|---|---|
| Report fits at the test event (IR-14.4) | one fit per frozen row and report seed: 9 rows × 5 seeds, about 23 A100-hours per run | 30.6 minutes per fit, App. D's module training, n = 1, self-reported and unaudited [p. 62]; 9 rows for illustration [ours] |
| Report scorings at the test event | one evaluation pass per frozen row, report seed and setting; the rows are *ours*, C_base when its code hash differs from E_base's, the last pass's ablations (5–6 per paper, for the 4 of Table 15's 5 papers that report a gain), its rebuttal rows, the controls and the diagnostics, with E_base only for a time metric | [Tab. 15]; the time of a pass is unknown until task 5 measures it [ours] |
| Repeated runs (IR-18) | 3 runs per task: about $11,295 at the paper's mean, an API-equivalent figure, never a bill; under the subscription (amendment A2) the runs cost usage windows | $3765 per run is the mean over the 33 NeurIPS 2025 problems of the cost analysis, tokens and machines with no breakdown [§4.3]; that these are Table 3's 33 successes out of 38 is our inference [Tab. 3] [inferred] |
| E_base at admission (IR-15) | its report fits, one per report seed, once per baseline key; counted in the U-INT-4 file's admission line | as there [ours] |
| Search data (IR-19) | under (2), fit loses what search takes until the report fit; under (3b), report shrinks, and its standard error grows by 1/√(1−f), ×1.054 to ×1.414 for f from 0.1 to 0.5 | the formula [ours] |
| Temporal gaps (IR-19.2) | T + L steps per built boundary, 576 steps at App. D's T = 512 and L = 64 | [p. 61] [ours] |
| The tail (IR-39) | one writer session, and G3 to G5 once more, per run | none [ours] |
| The null-idea controls | CPU only: 200 replications of the loop in mock mode, and 1000 null tasks | the controls' own sizes [ours] |
| Corrections (IR-41) | one report pass per frozen identity the defect touched, plus the fits it touched; none expected | none [ours] |
| Fidelity | the in-loop reviews judge drafts with validation numbers, which differ from the exported paper, so measurements like the paper's review rounds are made on other drafts | [Tab. 5] [ours] |

- **Inadmissible:** a task where IR-19 cannot build search while leaving report the power task 5 requires; a benchmark whose test labels we do not hold, such as a hidden leaderboard; a protocol that requires test feedback during development; a temporal task too short for its T + L gaps; a grouped task whose group IDs are unknown [ours].
