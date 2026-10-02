# Claims of the abstract, §1, Figures 1–2 and §5 (C-HEAD)

Part of [claims.md](../claims.md), which holds the summary, the measurement definitions (P-EVAL, P-BENCH, P-COST) and the gaps cited here [ours]. S2 is ScientistTwo, SP is ScholarPeer (in the loop), SAR is the Stanford Agentic Reviewer (held out) [§4].

Revised 2026-09-27 after the persona review: fixes F-CL-2 and F-CL-9 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md` [ours].

### C-HEAD-1 · 86 of 107 tasks succeed (80.4%)

- Claim: S2 "improves 86 out of 107 papers (an 80.4% success rate)" [Fig. 1] (tex:figures/problem_setup.tex:10); also "successfully advances 80.4% of the target problems" [§1] (tex:sections/1_introduction.tex:21) and "successfully advanced 80.4% of target problems" [§5] (tex:sections/6_conclusion.tex:3).
- Same claim in §4.1 and Tab. 3: "successfully executes research on 86 out of 107 problems" [§4.1] (tex:sections/4_experiment.tex:16), and the Overall row reads `86/107` [Tab. 3] (tex:tables/conference_accepted_comparison.tex:22).
- Sample: 107 tasks, 38 NeurIPS 2025, 5 ICLR 2026 and 64 ICML 2026 Spotlight [App. A.1]; successes 4/5, 33/38, 49/64, that is 80.0%, 86.8% and 76.6% [Tab. 3]; agents on Gemini 3.6 Flash, four of them on Claude Code with Opus 4.8 [App. A.2]; no repeats or seeds are reported [§4].
- Produced by: a count of the papers S2 generated [Tab. 3]; what counts as a success has three readings (A-EVAL-1) [ours].
- Checks: 86/107 = 80.37% ✓; 4 + 33 + 49 = 86 and 5 + 38 + 64 = 107 ✓ [Tab. 3]; Fig. 1b's ring holds 107 slots, 86 bars and 21 empty `Failed to Improve` slots (image) [Fig. 1b], counted by `playground/paper/fig1b_bars.py` [ours]; the TeX, the PDF and the HTML print 80.4 in the same four places [ours].
- Falsified by: a per-task list in which one of the 86 has no gain over the human SOTA, or a re-run with a materially different count [ours].
- Assessment [ours]: consistent wherever it appears; its meaning hangs on the success criterion; the 21 failures are never analyzed (U-BENCH-3); one run per task, so no interval. A success is declared on the data the search selected on, the best of up to 8–10 candidates passed through two "strictly better" gates, all on the full benchmark, so the count carries a winner's-curse inflation no reported variance can size; see P-EVAL-2 in claims.md, U-NOTE-1, U-ART-5 and U-TOP-5, and task 6's decision there, a held-out test set and a null-idea control.

### C-HEAD-2 · Mean relative gain 25.2%

- Claim: "delivering an average relative performance gain of 25.2% over the original human state-of-the-art baselines" [§1] (tex:sections/1_introduction.tex:21); "with an average relative improvement of 25.2%" [Fig. 1] (tex:figures/problem_setup.tex:10); "achieving an average relative improvement of 25.2%" [§5] (tex:sections/6_conclusion.tex:3); `Avg. Gain` 25.2 [Tab. 4] (tex:tables/autosota_comparison.tex:13).
- Sample: the 86 successes only, "across successful cases" [Tab. 4] (tex:tables/autosota_comparison.tex:3); by venue 13.9% (NeurIPS, 33) and 3.8% (ICLR, 4); no ICML value is printed [Tab. 4].
- Produced by: Gemini 3.6 Flash parsing each generated paper's main tables 10 times and averaging [§4.1] (tex:sections/4_experiment.tex:19); the per-paper formula is undefined (U-EVAL-1) and so is the reference baseline (A-EVAL-2) [ours].
- Check, by venue: the implied ICML mean is (86 × 25.2 − 33 × 13.9 − 4 × 3.8) / 49 = 34.56%, or 34.43–34.68% with rounding [Tab. 4] [ours].
- Check, the shape: the median is 7.7% [Tab. 4], far below the mean; 25.2 × 86 / 107 = 20.3% if a failure counts as 0 [ours].
- Check, Fig. 1b by bar colour: about 52 bars in 0–10%, 15 in 10–25%, 10 in 25–50%, 3 in 50–75%, 1 in 75–100% and 5 above 100% (image) [Fig. 1b]; the colour scale is continuous, so a bar near a bin edge may sit one bin off [ours].
- Check, the tail: at the bins' lower edges the mean is at least 13.1%; with the 81 bars below 100% at their bin midpoints, the five largest must average about 199% for a mean of 25.2% [Fig. 1b] [ours].
- Falsified by: recomputing the 86 gains from the papers' tables under any fixed rule and finding a mean far from 25.2%, or a median far from 7.7% [ours].
- Assessment [ours]: a success-only mean pulled up by about five outliers and by the ICML subset; the typical task gains under 10%; it is the system's own reported result as read by an LLM, not a harness measurement; a replication should report the median and a failure-inclusive mean from harness numbers. It is also measured on the data the search selected on, so it carries a winner's-curse inflation that cannot be sized without variance (P-EVAL-2), and the undefined gain rule alone can move one task's gain more than 100-fold (U-EVAL-1).

### C-HEAD-3 · "Consistently outperform human state-of-the-art"

- Claim: "Its solutions consistently outperform human state-of-the-art models" [Abstract] (tex:sections/0_abstract.tex:3); "with the resulting methodologies consistently outperforming human state-of-the-art baselines" [Fig. 1] (tex:figures/problem_setup.tex:10).
- Sample: the 86 successes [Tab. 4].
- Checks: 21 of 107 tasks (19.6%) failed to improve, and all 86 bars are gains (image) [Fig. 1b] [ours].
- Falsified by: a success with a negative gain [ours].
- Assessment [ours]: true only after conditioning on success; one task in five was not improved.

### C-HEAD-4 · Higher ratings than human-authored papers

- Claim: S2's papers "achieve higher average review ratings than human-authored papers under automated AI review agents" [Abstract] (tex:sections/0_abstract.tex:3).
- Sample: S2's successes (4, 33, 49) against all input papers (5, 38, 64), per venue, under SP and SAR [Tab. 3].
- Checks under SP: 7.0 vs 6.8 (ICLR), 7.3 vs 6.2 (NeurIPS), 7.6 vs 6.9 (ICML), all higher ✓ [Tab. 3].
- Checks under SAR: 5.4 vs 5.2 ✓, 5.6 vs 5.5 ✓, and 5.7 vs 6.1 ✗ for ICML [Tab. 3].
- Checks, pooled over venues (weights 4, 33, 49 against 5, 38, 64): SP 7.46 vs 6.65 ✓; SAR 5.65 vs 5.85 ✗ [Tab. 3] [ours].
- Falsified by: Tab. 3 itself, for the held-out reviewer on the largest subset, 49 of 86 papers [Tab. 3].
- Assessment [ours]: true for the in-loop reviewer, false for the held-out one on ICML and pooled; §4.1 and the Fig. 1 caption state the narrower claim (C-HEAD-5); the abstract drops the qualifier.

### C-HEAD-5 · Above accepted ICLR 2026 and NeurIPS 2025 papers

- Claim: papers "surpass the average scores of accepted papers at ICLR 2026 and NeurIPS 2025 under the Stanford Agentic Reviewer" [Fig. 1] (tex:figures/problem_setup.tex:10); "surpassing average scores from ICLR 2026 and NeurIPS 2025" [§5] (tex:sections/6_conclusion.tex:5).
- Sample and checks: as C-MAIN-5, which carries the §4.1 version of this claim [Tab. 3].
- Assessment [ours]: true as worded; the SAR margins (0.2 and 0.1 points) are about 0.6 standard errors each, and S2's SAR acceptance on NeurIPS is lower, 25/33 = 75.8% against 29/38 = 76.3%.

### C-HEAD-6 · High acceptance under "independent" reviewers

- Claim: manuscripts and codebases "consistently achieve high acceptance rates across independent automated peer-review evaluations with high scores" [§1] (tex:sections/1_introduction.tex:21).
- Sample: 86 papers; 91.9% under SP, 72.1% under SAR [Tab. 3].
- Checks: SAR does not accept 24 of the 86 (27.9%); per input task, SAR accepts 62 of 107 (57.9%) [Tab. 3] [ours].
- Assessment [ours]: SP is not independent, since it "is also used to refine the draft quality" [§4] (tex:sections/4_experiment.tex:5); acceptance is undefined for both reviewers (A-EVAL-3, U-EVAL-3).

### C-HEAD-7 · What Figure 1 shows

- Panel (a): `Human Frontier`, `Expanded Frontier` and `Upper Bound` over 35 sub-areas of 8 areas (Theory, Applications, Deep Learning, General ML, Optimization, Probabilistic, RL, Social Aspects), radial scale 0.2–1.0; the red polygon lies on or outside the blue one on every spoke (image) [Fig. 1a].
- Panel (b): one slot per task around a ring of the same 8 areas; a bar's colour bins the gain from 0–10% to above 100%, and `Failed to Improve` slots have no bar (image) [Fig. 1b].
- Checks: 86 bars + 21 empty slots = 107 slots of 3.37° each, binned as in C-HEAD-2 [Fig. 1b] [ours]; every area the caption names, "(e.g., LLMs, robotics, neuroscience, speech, robustness, reinforcement learning, game theory, privacy, optimization, and time series)", appears as a label (image) [Fig. 1].
- Assessment [ours]: panel (b) agrees with 86/107 and is the only per-task view of the gains; panel (a) cannot be checked or reproduced, because its quantity is never defined (U-EVAL-7).

### C-HEAD-8 · Figure 2's case: 10.9%, and scores of 8.0 and 6.5

- Claim: S2 "achieves a 10.9% relative improvement over the human-designed state-of-the-art baseline" and the paper is accepted, "receiving impressive scores of 8.0 from ScholarPeer and 6.5 from the Stanford Agentic Reviewer" [Fig. 2] (tex:figures/qualitative_result.tex:21).
- Sample: one task, Incremental BPE Tokenization, an ICML 2026 Spotlight [Tab. 14] [Bib: jiang2026incremental]; the pages shown are the VD-STrans paper (image) [p. 3].
- Check: the embedded abstract says VD-STrans "achieves a geometric mean throughput speedup of 1.123" over the incremental SOTA (image) [p. 3], and its introduction reports a "12.3% average throughput boost" [p. 3].
- Check: 1 − 1/1.123 = 10.95% (10.91–10.99% for a speedup between 1.1225 and 1.1235), so 10.9% matches the time reduction, not the paper's own 12.3% [ours]; 10.9% and 6.5 recur in [Tab. 9] and [§4.3] ✓.
- Two conventions for Tab. 9's chain [ours]: if its three gains are time reductions, as this one appears to be, they compound to 1 − 0.891 × 0.904 × 0.918 = 26.1%, a 1.35× speedup; read as ratio gains they compound to 31.5% (C-DISC-4) [Tab. 9].
- Falsified by: the task's main table giving a different gain under the paper's rule [ours].
- Assessment [ours]: the undefined gain rule moves this one result by 1.4 points (U-EVAL-1); SP's 8.0 is exactly the in-loop stopping threshold [App. A.2]; "accepted" is defined for neither reviewer (A-EVAL-3, U-EVAL-3).

### C-HEAD-9 · "Fully verified, executable codebases"

- Claim: S2 "autonomously generates expert-level, publishable papers and fully verified, executable codebases" [Abstract] (tex:sections/0_abstract.tex:2), "faithfully passing rigorous multi-dimensional integrity audits" [§5] (tex:sections/6_conclusion.tex:3).
- Sample: audits are reported for the 49 ICML successes only [Tab. 7] [§4.2]; the Antigravity runs are said to pass without numbers [§4.2].
- Checks: 49 of 86 successes (57%) have audit numbers [Tab. 7] [ours].
- Assessment [ours]: extrapolated from one subset; the auditor is unspecified (U-EVAL-5); "expert-level, publishable" rests on the reviewer numbers of C-MAIN-1 and C-MAIN-2.

### C-HEAD-10 · Acceptance thresholds met

- Claim: the manuscripts "consistently met top-tier conference acceptance thresholds" [§5] (tex:sections/6_conclusion.tex:3); S2 "consistently exceeds the acceptance threshold for standard conference publications" [§5 "Limitations"] (tex:sections/6_conclusion.tex:5).
- Checks: SAR accepts 62 of 86 S2 papers (72.1%) and 94 of the 107 human input papers (87.9%) [Tab. 3] [ours].
- Assessment [ours]: true of the ICLR and NeurIPS venue averages, not of individual papers; no "acceptance threshold" is defined for either reviewer (A-EVAL-3, U-EVAL-3).

### C-HEAD-11 · About $3,800 per task

- Claim: S2 "costs approximately $3,800 to execute a single task" [§5] (tex:sections/6_conclusion.tex:7).
- Checks: $3765 in [§4.3] and in the cost donut (image) [Fig. 10b] rounds to $3,800 ✓.
- Sample: 33 NeurIPS runs, apparently the successes only (U-COST-2); details in C-DISC-3 [§4.3].
- Assessment [ours]: an average over successful runs; the cost per successful paper, failed runs included, is unknown.
