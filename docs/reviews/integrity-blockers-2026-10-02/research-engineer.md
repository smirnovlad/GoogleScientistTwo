# Record: `research-engineer` review, wave 1 (2026-10-02)

- **Reviewed:** `docs/integrity/blocking-decisions.md` at commit `a2e7eb0`, against its brief,
  `docs/integrity/README.md`.
- **Lens:** can a number this engine reports be trusted and reproduced?
- **Record:** the reviewer's final message, verbatim below, unchanged. It names scratchpad
  scripts by file name only; both are kept, unchanged, in
  `playground/integrity/reviews/research-engineer/`.

---

# Review: research-engineer, `docs/integrity/blocking-decisions.md` at a2e7eb0 (2026-10-02)

**Lens:** can a number this engine reports be trusted and reproduced?

**What I re-checked:**
- The mechanical tests pass: `wc -l` gives 419, `grep -c "⛔ WHY NOT"` gives 19, and `check_citations.py` reports 0 problems.
- I re-read every ScientistOne quote I rely on in its TeX, and looked at pp. 40–51 as images.
- My numbers come from two scratchpad scripts with fixed seeds, `null_control.py` and `costs_and_flags.py`. They should move to `playground/` if a fix cites them.
- No file was edited, and I did not run git.

## 1. Verdict

**The document is not yet fit for task 3 to build on, as far as this lens sees.** Two rules would be built into the harness contract wrong:
- **B1.** The test event scores the same artifacts, with the same seeds, that search selected. So whatever luck a fitted model got from its training seed carries straight through to the test split.
- **B2.** A fit job may load weights that the agent added to its code tree. That empties IR-3's provenance rule and IR-23's re-run.

Everything else can be fixed inside the document's three-layer structure.

## 2. Requirements R4, R7, R9

| R | Status | Reason |
|---|---|---|
| R4 | **partly met** | All 32 controls (10 + 8 + 9 + 5) state both outcomes and a mode or cost before any control runs, so the literal acceptance test passes. **Undecidable as written:** the stochastic controls give no threshold, seed or sample size: IR-3's flag, IR-7's sway rate, IR-8 (a) and (c), IR-12/IR-14, IR-23 ("beyond tolerance", with no tolerance set) and IR-31 ("expected below 1"). **Can pass with the attack still open:** IR-2/IR-3 and IR-23 if the weights sit in the code tree (B2); IR-10 because it plants exact copies only (m1); IR-12/IR-14 because its noise lives in evaluation only (B1, M1). |
| R7 | **met** | Each of the twelve rows the brief names gets a constraint: A-FULL-1, U-BASE-1 (1.6, 2.7); U-BASE-2 (2.7); U-SUB-2 (1.6, 2.7); U-INT-1 (3.6); U-INT-3 (2.7, 3.6); A-ABL-3, U-TOP-1 (1.6); U-ART-15 (1.6, 2.7); U-ART-12 (1.6); U-EVAL-1 (1.6, 2.7); U-NOTE-4 (1.6, 3.6, 4.7). The omissions are minor (m6). Two constraints are too weak for this lens: U-ART-12 (B1, M8) and A-EVAL-1 (M2). |
| R9 | **partly met** | Every decision has a cost section and an inadmissibility list. But the largest cost multipliers are absent or unquantified: runs per task, seeds per scoring, re-fits for every reported row, and people's time for the planted corpus. The only GPU-hour figure covers 2 of about 10 reported rows and rests on one self-reported time (n = 1). The rules are not screened against the tasks task 5 must choose from (M9, m7). |

## 3. Findings

**Where each lens question is answered:**

| Question | Short answer | Findings |
|---|---|---|
| Do the controls prove their guards? | They are structured right; seven cannot be decided as written, and four can pass with the hole still open | R4, B2, M1, m1, m4 |
| The null-idea control | 1.8675 is right; the 20 has no source; one run decides nothing; it misses seed noise in the fitted model; it measures that the splits are separate, not the false-success rate | M1, B1 |
| IR-31's corpus size | 96.04 → 97 is right (Wald interval, p = 0.5), but the interval type and the precision are not enough | m4 |
| Can the three data roles be built? | i.i.d. and tabular data: yes. RL, judge-scored and throughput tasks: yes, as sets of seeds or samples, but only with B1's fix. Time series and grouped data: no, as written. OOD: yes, with a confound | M6, B1 |
| The test-once exception | Sound towards agents; unbounded towards people | M5 |
| Seeds, variance, re-runs | Seed variance is recorded but has no floor; the number of runs is not fixed in advance; variance across test items cannot be measured; re-running breaks when weights sit in the tree | B1, B2, M3, M8 |
| Can a gain or a success count move without a better method? | Yes, through five routes: seed luck, a coin-flip success rule, adding runs until the result looks good, gains too small to verify, side changes in C_base | B1, M2, M3, M4, M7 |
| Cost and admissibility | The multipliers are missing; I1 is costed for 2 of about 10 rows | M9, m7 |

### BLOCKER

**B1 · §2.1 IR-14 (with IR-3, IR-5), §2.8 Compute, and the IR-12/IR-14 control in §2.4: luck from the training seed survives the held-out split.**
- **Problem.** The freeze fixes each row's "code hash, artifact hash and seeds" (IR-14), and "the test event is one evaluation pass per seed for each frozen row" (2.8). So the report data is new, but the fitted models (artifacts) and their seeds are the ones search chose.
  - A score carries two kinds of noise:
    - noise from the evaluation sample, which differs between search and report;
    - noise from fitting (seed, initialisation, data order), which is built into the artifact and therefore shared by both splits.
  - Choosing the best row on search also chooses the luckiest fits, and that luck reaches report intact.
  - So the claims that IR-10 to IR-14 stop "Steering the search on the reported data" (2.3), and that "IR-14 keeps the reported number honest" (section 6), hold for the first kind of noise only.
  - RL (IR-8 c) is the plainest case: the role's episode seeds are new at the test event, but the trained policy is not.
- **Evidence.**
  - My simulation (`null_control.py`, seed 20261002, 20,000 replications of 20 null rows), giving the winner's mean gain on report:
    - **evaluation noise only:** −0.005;
    - **fit noise equal to evaluation noise:** +1.32, which keeps 71% of the +1.87 inflation seen on search;
    - **evaluation noise one fifth of fit noise:** +1.83.
  - Averaging 5 seeds per row shrinks both kinds of noise alike, so it keeps the same share. With fit noise 1.0 and evaluation noise 0.5, the report gain is 0.75 against 0.94 on search (80%).
  - The share retained follows σ_a²/√(σ_a²+σ_e²)·E[max], where σ_a is the fit noise and σ_e the evaluation noise.
  - The trace used a single fine-tuning seed, "seed=0", and the method and its ablations all reuse that one checkpoint [p. 40] [p. 45] (image).
  - ScientistOne found 9 of 13 value mismatches "within 5% of the paper-reported number---small enough to plausibly arise from unreported seed variance, but uniformly biased towards a better-than-rerun headline" [Ref: meng2026scientistone App. E.1] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:127-129).
  - The null control plants "unit-variance noise" per score, so it passes while this bias is untouched.
- **Fix.**
  1. Split the manifest's seeds into search seeds and report seeds, disjoint, the way the data roles are (IR-10 and U-ART-12's constraint).
  2. At the test event, re-fit every frozen row from its code hash with the report seeds, then score report once. Where search was carved from fit (IR-19 option 2), re-fit on fit ∪ search; this also restores the protocol's training size for the comparison with published numbers. IR-11 gains a row for this report fit job.
  3. IR-15 fits the baseline the same way, so its sealed value is the baseline row's report result.
  4. I1 re-fits with the report seeds.
  5. The null control plants seed-dependent noise in the fitted model as well.
  - **Cost:** one fit per report seed per frozen row. That is about 23 A100-hours per run for 9 rows × 5 seeds, at App. D's self-reported 30.6 minutes per fit (n = 1, unaudited) [p. 62].

**B2 · §1.1 IR-3 (with IR-2, IR-23, and "agent code" in Terms): weights loaded from the code tree have no provenance, and a shared checkpoint has no rule.**
- **Problem.**
  - IR-3 admits weights that "are in the hashed environment or code tree", and "agent code" includes "any weights or data files it adds" (Terms).
  - A fit entry point that only loads weights the agent placed in its tree passes IR-3 ("a fit job that engine code ran and recorded produced it, from the same code hash"). I1's re-run of the fit then reproduces it exactly, which is the case IR-23 exists to rule out: "that the artifact comes from the code".
  - Such weights can come from tuning in the sandbox that nothing recorded (for example, the best of many seeds on fit's own validation data). They can also come from public test labels fetched over the network, a route section 6 lists as "Detection only".
  - The guard is detection by G2 ("listed in the ledger with their sizes for G2"), although a setup rule is available (R3).
  - **The legitimate case has no rule either.** The trace's method is post-hoc on the baseline's checkpoint: "Procrustes-DS is post-hoc and reuses this checkpoint" [p. 40] (image). Its ablation "Reuses the AdaptFormer-PEFT checkpoint and the cached 12-layer features written by final.py" [p. 45] (image). IR-3's "same code hash" forbids reusing the baseline fit job's artifact. Every candidate and seed would then re-train the backbone, which costs compute and loses the pairing with the baseline.
- **Evidence.** IR-3 and Terms, as quoted above. IR-23's control expects "the fit re-run differs beyond tolerance" for "weights from a hidden extra step" (3.3); that holds only if the weights live outside the tree.
- **Fix: a lineage rule, enforced by the setup.**
  - A fit job's inputs are the fit role (plus search for B1's report fit), weights pinned with their hashes in the manifest at packaging, and artifacts of other recorded fit jobs, named by hash, whose own lineage is recorded.
  - When a code tree is hashed, refuse any array or binary file, and any file above a size bound, that no recorded job produced.
  - Where a method reuses a checkpoint, the candidate and the baseline share the recorded upstream checkpoint of the same seed, so the comparison is paired.
  - What remains, constants written into source code, is detection by G2 and I2.
  - Re-plant the IR-2/IR-3 and IR-23 controls with the weights inside the tree.

### MAJOR

**M1 · §2.4, the IR-12/IR-14 control: the null-idea control cannot be decided, and 20 is not this engine's number.**
- **The 20 has no source.** The reported row survives up to 10 ideas (D-1), each with up to 1 + N_eng subset scorings, then the Selector's maximum over the `Good` ideas, then up to 3 strict comparisons (analysis.md section 4.1). The expected maximum ranges from 1.03 (m = 4) through 1.49 (m = 9), 1.54 (m = 10) and 1.87 (m = 20) to 2.04 (m = 30), by numerical integration.
- **One run decides nothing.** The standard deviation of the maximum of 20 normals is 0.525. With a pass threshold at 1.0σ:
  - the guarded arm wrongly fails 15.9% of the time;
  - the unguarded arm wrongly passes 3.2% of the time.
  - No seed, replication count or threshold is stated.
- **It measures the wrong thing.** It shows that report is independent of the choice. It does not measure the false-success rate that claims.md P-EVAL-2 asked task 6 for.
- **Fix.**
  - Run the control through the engine's own loop in mock mode, with scripted null candidates and noise planted in the fitted model (B1), so that m is whatever the loop does.
  - Use a fixed seed list and at least R = 100 replications. This costs $0 and gives a standard error of 0.10 on the guarded mean and 0.053 on the unguarded one.
  - Pass when the guarded mean report gain is within ±3 SE of 0, and the unguarded mean is within ±3 SE of the simulated search optimism. Record that optimism as the bias that section 6 promises to measure.
  - Add a second null control: the share of null tasks that the pre-registered success rule counts as a success must be at most its α (M2).

**M2 · §2.7 rows A-EVAL-1 and U-EVAL-1, and §1.6 U-EVAL-1: a success count and a gain can still move without a better method.**
- **Problem.**
  - The only constraint is "success and gains are computed from report records".
  - The register proposes "Success is a full-set `Good` idea with a positive gain" (A-EVAL-1). On report, a method no better than the baseline shows a positive gain with probability 0.5, so half of the null tasks would count as successes.
  - The baseline's report value is computed once per task (IR-15) and reused by every run (IR-14, IR-18). Its noise is therefore shared by all of a task's gains and never averages out.
- **Fix.**
  - Success requires the paired report gain (per report seed, against the baseline on the same seeds) to have a one-sided lower confidence bound above 0, at a pre-registered α. Then P(success | null) = α.
  - The bound includes the baseline's variance once per task.
  - A task whose gain is inside the noise is reported as "no detectable gain", separately from failures.

**M3 · §2.1 IR-18: repeated runs allow adding runs until the result looks good, and selective restarts.**
- **Problems.**
  - **(a) The number of runs is not fixed in advance.** Each run is "registered before it starts", but nothing fixes how many runs a task gets before any result is seen. A fourth run can be registered after three test events.
  - **(b) Only report numbers are named.** "No run is restarted, re-seeded or dropped because of its report numbers" leaves restarts or drops because of search numbers, which track report numbers by design.
  - **(c) Retries have no bound and no definition of an infrastructure failure.**
    - ScientistOne allowed "up to 3~attempts per run" (ref:2605.26340v1:sections/06a_setup.tex:29).
    - It counted "LaTeX compilation errors" as infrastructure (same line).
    - 16 of its 75 runs needed a retry (ref:2605.26340v1:sections/06a_setup.tex:31) [Ref: meng2026scientistone §6].
  - **(d) Development tasks' report numbers have no stated status.** The people who change the engine see them.
  - The best-of-three control tests none of these.
- **Fix.**
  - Before the first final-test run, pre-register the final-test task list and the number of runs per task.
  - No run is restarted, re-seeded or dropped because of any result, search or report.
  - Retries are allowed only for causes on a list written in advance, are bounded, and are all reported. Crashes, timeouts and out-of-memory errors caused by agent code are run failures, not infrastructure.
  - Development-task report numbers count as validation for the engine and are never quoted as evidence.
  - Add a control: a run registered after the others' test events is refused.

**M4 · §3.1 IR-23 and IR-25: I1 checks values, not gains, and "not verified" has no consequence.**
- **The tolerance can swallow a gain.**
  - The tolerance's starting value is ScientistOne's max(1%, 3σ/|s̄|) [Ref: meng2026scientistone §6] (ref:2605.26340v1:sections/06a_setup.tex:10).
  - S2's own DMSQD gain is "+0.61%±0.27 mean QD over reproduced DMS" [Tab. 16] (tex:sections/appendix.tex:288), which is below the 1% floor.
  - A re-fit in which that gain vanishes would still pass.
- **"Not verified" is not counted.**
  - ScientistOne counts "Submitted artifact cannot be re-evaluated within the budget" as a confirmed I1 error [Ref: meng2026scientistone App. E.1] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:118).
  - IR-25 counts only failed I1, I2 or ledger checks. An expensive fit therefore escapes I1 and can still count as a success.
- **Fix.**
  - I1 also re-derives the paired gain from the re-fits. Its tolerance comes from re-fit noise measured on the manifest's hardware class and must lie below the reported gain; otherwise the gain is reported as "not verifiable".
  - Fix each row's audit budget before the audit, from its recorded fit time.
  - If the *ours* or baseline row is not verified, the task is not a success in the primary count, and it gets its own column.

**M5 · §2.1 IR-15: the sealed baseline check is unbounded.**
- **What it leaks.**
  - **To agents, nothing usable.** No agent code runs and no candidate is scored. The only bit it releases, "pass", is the same for every run that starts.
  - **To people, the values themselves, as often as they ask.** Section 6 admits that whoever packages tasks sees them.
- **Problems.**
  - "The tolerance used" is not fixed before the check.
  - "Every attempt is a ledger entry" sets no limit on attempts.
  - "Once per task (that is, per manifest hash)" restarts the count with every manifest edit, so a person can iterate the packaging diff against report until it passes.
  - The direction of the check is not stated. A two-sided check can fail a baseline for being stronger than published, which invites weakening it.
  - No seed count is given, although the baseline's variance is the first thing to measure.
- **Fix.**
  - Before the first attempt, the manifest fixes the seed count and the tolerance formula. The formula's inputs are the baseline's spread across its seeds on search (scored earlier, IR-4), the published spread where the paper gives one, and the sampling error of a carved report split (IR-19 option 3).
  - Fail only when the reproduction is worse than published by more than the tolerance.
  - Allow at most k attempts per task across manifest versions, and report them all.
  - Iterate the packaging on search; read report once.
  - Ask the coordinator to amend `CLAUDE.md`'s "The test set is used once, at the end" so that the two rules agree.

**M6 · §2.1 IR-19 and IR-10: building the roles is wrong for temporal, grouped and OOD data, and the cost of a carve-out in power is not stated.**
IR-19's order of preference is right for i.i.d. data. Four cases need more:
- **Time series.**
  - "A seeded, stratified carve-out of fit" puts random windows into search. With App. D's lookback T = 512 and horizon L = 64 [p. 61], two windows one step apart share 511 context steps and 63 target steps. Search targets then sit inside fit windows.
  - The standard loader uses contiguous blocks instead, and starts each split's context `seq_len` steps before the boundary: `border1s = [0, 12 * 30 * 24 - self.seq_len, ...]` (Time-Series-Library, `data_provider/data_loader.py`, fetched 2026-10-02). So inputs cross a boundary backwards in time by design, while targets never do.
  - IR-10's item-level hash check passes such leaks trivially, and it cannot express the legitimate overlap.
- **Grouped data** (subjects, patients, series) needs carve-outs and the overlap check by group. TeCh, one of the five ICLR tasks, is a medical time-series task (App. A.1); its protocol is unchecked.
- **OOD.**
  - Under option (3), search is drawn from the test OOD distributions. The candidates are then selected with access to those distributions, while the published baseline was not.
  - OpenOOD v1.5 instead builds OOD validation data whose classes are disjoint from the test OOD sets, to "avoid reporting overoptimistic results" (arXiv:2306.09301, fetched 2026-10-02).
  - The trace's critic steered the redesign on a test set, CIFAR-10 [p. 46].
- **A carve-out of fit (option 2).** Both arms then train on less data than the protocol uses. TALENT, for example, splits each dataset "64%/16%/20%", selects hyperparameters and early-stops on its validation split, and averages 15 seeds (arXiv:2407.00956v4, fetched 2026-10-02). Less training data shifts the reproduction away from the published numbers that IR-15 compares against. B1's re-fit on fit ∪ search removes the shift.
- **Power.** Carving a fraction f off the official test set multiplies report's standard error, and its minimal detectable effect, by 1/√(1−f):

  | f | Multiplier |
  |---|---|
  | 0.1 | ×1.054 |
  | 0.2 | ×1.118 |
  | 0.3 | ×1.195 |
  | 0.5 | ×1.414 |

  The admissibility rule in 2.8 refers to "the power that task 5 requires" without stating this cost.
- **Fix.** Write the role construction per kind of data:
  - temporal roles as contiguous blocks in time order, with a gap of at least T + L steps, and the overlap checked on target timestamps;
  - grouped roles by group;
  - for OOD, (3a) the protocol's, or its successor's, validation sources that are disjoint from the test OOD sets, before (3b) a carve-out, which every gain then discloses;
  - under option (2), B1's re-fit.
  - State the power formula beside the rule.

**M7 · §1.1 IR-4: the agent's adaptation C_base is never scored, so a side change in it passes as the idea's gain.**
- **Problem.**
  - Ideas start from C_base, which the Baseline Coding Agent prepares; gains are measured against E_base, the pinned code.
  - Any training change made while adapting the code (for example a regulariser or longer training) is carried into every candidate and every ablation row. The ablation critic cannot attribute it, and it counts towards the gain over E_base.
  - This is the same class of change App. B blames for TeCh's gain: "general training controls (EMA and label smoothing)" (tex:sections/appendix.tex:223-224).
- **Fix.**
  - Score unmodified C_base as a row like any other, and freeze it as a control.
  - Show ours − C_base beside ours − E_base in the verified table.
  - Flag a C_base − E_base difference outside the baseline's seed noise before any idea is scored.

**M8 · §1.1 IR-3, IR-5, IR-9: seeds and variance have no floor, no pairing and no item-level record.**
- **No minimum seed count.** A manifest with one seed satisfies every rule, and IR-5's "spread" is then undefined. The trace used one seed [p. 40].
- **No pairing rule.** Using the same seed list for every row and computing gains per seed pair is possible from IR-5's records, but no rule requires it.
- **Failed seeds.** IR-9 forbids dropping a failed setting, but nothing forbids dropping a failed or timed-out seed from a row's aggregate.
- **Item-level outputs.**
  - IR-5 only keeps per-item outputs away from agents; it never requires storing them.
  - Without them, the variance from the evaluation sample (a paired bootstrap over items) cannot be measured. For post-hoc methods on a single checkpoint, that is the only variance there is.
  - IR-8 (b) records a spread for judge-scored metrics, but not the judge's raw outputs.
- **IR-3's flag rarely fires.** "Identical results across seeds" is rare under GPU nondeterminism, and the flag never fires on a partial seed game.
- **Fix.**
  - Set a seed floor for every reported row. Task 5 sets the value from measured noise, and it is never 1.
  - Use one seed list per role, shared by all rows, and compute gains per seed pair.
  - A row's aggregate covers every seed, and a failed seed invalidates the row.
  - Store per-item predictions and raw judge outputs, hashed in the record and readable only by engine code and the audit.
  - Make IR-3's flag statistical: with 5 seeds, it fires when a row's seed variance is below the 1% quantile of F(4,4), 0.0626, times the baseline's. That is a standard-deviation ratio below 0.25.

**M9 · §1.7, §2.8, §3.7, §4.7: the largest costs are missing or carry no sample.**

| Cost | What the document gives | Order of magnitude, with its sample |
|---|---|---|
| Repeated runs (IR-18) | nothing | $11,295 per task at 3 runs, from the paper's mean of $3,765 per run (n = 33 NeurIPS 2025 tasks, which are the 33 successes of 38 [Tab. 3] [§4.3]; tokens and machines, no breakdown) |
| Seeds per scoring | "the seed count being U-ART-12's" | The paper's run used one seed. Fits alone reach 53 A100-hours per run at 1 seed and 265 at 5, at 30.6 min per fit (n = 1, self-reported by an agent-written paper, unaudited [p. 62]) and analysis.md's ceiling of 104 units (N_p = 6, N_t = 3). This is a ceiling, for illustration. |
| I1 re-fits (IR-23) | 5.1 A100-hours, for 2 rows and no seeds | IR-23 re-fits every reported row: ours, the baseline, 5–7 ablations [Tab. 15] [pp. 64–65], the tuned-baseline control and the rebuttal rows. For 10 rows × 5 seeds: 25.5 A100-hours at one re-fit, 127.5 at ScientistOne's five. The p. 51 rebuttal alone is 50 datasets × 5 seeds, 250 jobs per re-fit. |
| B1's re-fit at the test event | n/a | about 23 A100-hours per run |
| IR-31's corpus | 970 judge calls per check and configuration | About 20,000 calls (970 × 7 LLM checks × at least 3 configurations). The people who write about 97 hacks per check are not costed at all. |
| A judge-scored metric (IR-8 b) | "k calls per item and scoring" | neither estimated nor recorded as unknown |

- **Fix:** one cost table per decision, with these lines, each carrying its sample, and "unknown" where it is unknown.

### MINOR

- **m1 · IR-10 and its control in 2.4.**
  - **Problem:** exact content hashes miss near-duplicates (re-encoded, resized or cropped copies). Under a carve-out (option 3), near-duplicates let a choice made on search pick up report noise.
  - **Fix:** plant a near-duplicate in the control, and state the detector and its threshold.
- **m2 · IR-8 (b).**
  - **Problem:** T-SAE's edit was a parameter, `act_threshold_frac` (tex:sections/appendix.tex:306), "a threshold in the evaluation harness" (tex:sections/appendix.tex:208-209), not code.
  - **Fix:** state that the harness reads no parameter from the code tree, and plant the control as a configuration value.
- **m3 · IR-8 (a).**
  - **Problem:** a hardware class does not fix timing noise. VD-STrans's own paper names Hyper-Threading, Turbo Boost and ASLR in its measurement setup [p. 3]. Pinet's "training 3.0× faster" [Tab. 16] is also a time metric.
  - **Fix:** the manifest records the machine's configuration, and the repeat count comes from a measured noise floor.
- **m4 · IR-31.**
  - **Problem:** the arithmetic, 1.96² × 0.25 / 0.1² = 96.04, is right but too coarse:
    - Wald gives [0, 0] for 0/97, where Wilson gives [0, 0.038];
    - ±0.1 cannot resolve rates of Table 7's size, 1/50 and 0/49 [Tab. 7];
    - 97 positives over three attack kinds is about 32 per kind, which gives ±0.17;
    - a false-positive rate near 1% needs about 1,521 clean items for ±0.5%;
    - the control's "expected below 1" passes on a single catch.
  - **Fix:** use Wilson or Clopper–Pearson intervals, size the corpus from the precision each reported count needs, and give the control an upper bound with the number of missed cases that bound needs.
- **m5 · Numbers without their sample.**
  - "$3765 ... over the paper's 33 NeurIPS tasks": these are the 33 successes of 38 [Tab. 3] (U-COST-2 [inferred]).
  - 30.6 minutes: n = 1, self-reported.
  - The 20 null candidates: no source.
  - 5.1 A100-hours: 2 rows, no seeds.
  - **Fix:** state each sample beside its number.
- **m6 · R7 omissions.**
  - U-PEER-2: rebuttal code must be kept, because rebuttal rows enter the freeze and IR-23 re-fits them.
  - A-TOP-4 / P-TOP-6: a chained run's baseline is the previous run's C+, which IR-4 has a person package, and whose report number came from the previous run's test event.
  - U-TOP-2: IR-18's retry rule constrains it.
  - U-COST-1: M9's new cost lines belong there.
  - **Fix:** add each with its constraint.
- **m7 · Admissibility, against the tasks task 5 will choose from** (App. A.1, Table 13):
  - T-SAE needs a judge whose version can be pinned (1.7);
  - TeCh needs grouped or temporal roles (M6);
  - RALI's six zero-shot sets need carve-outs, which cost power (M6);
  - Pinet reports a time metric (m3);
  - DMSQD's gain sits below a 1% I1 floor (M4).
  - **Fix:** a short screen of these tasks against the rules, so task 5 sees which are admissible and cheap.
- **m8 · Guard-off builds.**
  - **Problem:** the controls need builds with guards removed, and nothing stops such a build from producing a reportable number.
  - **Fix:** state that a record from a guard-off build is never reportable. The run registry should carry the engine commit and the guard configuration, reachable from the run ID in IR-5.

## 4. What is right as written and must not be lost

- **Who computes:** the harness computes every number, and agent code hands over a code tree only (IR-1, IR-2, IR-5). An LLM can only be stricter than the numeric precondition (IR-7).
- **The baseline:** E_base comes from the pinned code (IR-4), and the weak-baseline evidence is quantified: 0.41 of 1.99 pp [pp. 41–42].
- **Search access:** IR-11's read table, including a predict step that cannot tell search from report, and IR-13's search scorings, triggered by the engine and counted.
- **The test event:** IR-14's freeze binds *ours* before it, there are three kinds of report job, and after it only text changes, with both columns in the final fill (IR-17).
- **The audit:** IR-23 re-fits rather than re-scores, and reads the paper's numbers from the paper; IR-24 adds the ledger checks.
- **Denominators:** integrity failures stay in every denominator (IR-20, IR-25).
- **The auditors:** a held-out reporting auditor, one-way flow, separate stores, measured error rates, and a separate development auditor (IR-29 to IR-31).
- **The controls and section 6:** every control states both outcomes before it runs, nearly all in mock mode at $0, and section 6 is an honest list of what is not stopped.

**External sources.** They were fetched 2026-10-02 through a summarising fetch, so re-check each quote against the source text before it enters the repository:
- [TALENT, arXiv:2407.00956v4](https://arxiv.org/html/2407.00956v4)
- [OpenOOD v1.5, arXiv:2306.09301](https://arxiv.org/html/2306.09301)
- [Time-Series-Library, `data_provider/data_loader.py`](https://raw.githubusercontent.com/thuml/Time-Series-Library/main/data_provider/data_loader.py)
