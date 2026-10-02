# ScientistTwo's quantitative claims: evidence, samples, consistency

Every quantitative claim of arXiv:2609.19644v1, with its location, its sample, the checks we ran and our assessment [ours]. Conventions (citation, classification, IDs) are those of [README.md](README.md) [ours]. The claim entries live in five files under [claims/](claims/); this file holds the summary, how the paper measures, the App. A.1 benchmark counts and the gaps [ours].

Revised 2026-09-27 after the persona review: fixes F-CL-1, F-CL-2, F-CL-4, F-CL-5, F-CL-8, F-CL-10, F-CL-12, F-CL-13, F-12, F-15 and F-17 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md`; closure corrections on 2026-09-28, from `closure-evaluation-integrity-engineer.md` and `closure-research-engineer.md` in the same folder; and Codex review corrections on 2026-09-28, from `codex-review.md` in the same folder [ours].

## How to read this

- Abbreviations: S2 is ScientistTwo; SP is ScholarPeer, the reviewer inside the loop; SAR is the Stanford Agentic Reviewer, the "held-out evaluator" [§4 "Common Setup"].
- Each claim `C-<KEY>-n` gives the quote with its location, its sample, how the number was produced, the checks with their arithmetic, what would falsify it, and our assessment [ours].
- A value read from a figure image is marked (image); the TeX does not contain it [ours].
- The arithmetic re-runs with `python3 playground/paper/claims_arithmetic.py`, which also re-runs the reviewer's `playground/paper/reviews/research-engineer/sp_integer.py`; the Fig. 1b bar count with `python3 playground/paper/fig1b_bars.py`; the Fig. 10b seed labels with `python3 playground/paper/fig10_seed_labels.py` [ours].
- A count like 79/86 behind a printed percentage is the only k that rounds to it, computed by the arithmetic script [ours].

## Summary: the headline claims

| ID | Headline claim and location | Sample, and how the number was made | Our assessment [ours] |
|---|---|---|---|
| C-HEAD-1 | S2 improves 86 of 107 tasks, 80.4% [Fig. 1] [§1] [§4.1] [§5] | 38 NeurIPS + 5 ICLR + 64 ICML tasks [App. A.1]; no repeats or seeds reported [§4] | 86/107 = 80.37%, and Fig. 1b shows 86 bars and 21 empty slots (image); what counts as a success is ambiguous (A-EVAL-1), and the count is made on the data the search selected on |
| C-HEAD-2 | mean relative gain 25.2% over human SOTA [§1] [Fig. 1] [Tab. 4] [§5] | the 86 successes only; gains parsed by Gemini 3.6 Flash from S2's own paper tables, 10 parses averaged [§4.1] | median 7.7% [Tab. 4]; about 52 of 86 gains lie in 0–10% and 5 exceed +100% (image); the gain rule is undefined (U-EVAL-1); 20.3% if the 21 failures count as 0; measured on the data the search selected on, so inflated by an amount no variance lets us size |
| C-MAIN-1 | 91.9% acceptance, rating 7.5 vs ScientistOne's 3.8, under SP [Tab. 2] | SP is the reviewer S2 revises against [§4] [App. A.2]; baselines are 2–21 public papers each [Tab. 2] | in-distribution by the paper's own account; the acceptance rule is undefined, cannot be the in-loop threshold of 8, and is consistent only with a rating of 6 or more [inferred] (A-EVAL-3) |
| C-MAIN-2 | 72.1% acceptance under SAR, every baseline 0% [Tab. 2] | held-out reviewer [§4]; the baselines' papers are their own public releases, not runs on the 107 tasks [Tab. 2] [inferred] | the strongest evidence in the paper; SAR's acceptance rule is unknown (U-EVAL-3) and the task pools differ |
| C-HEAD-4 | "higher average review ratings than human-authored papers" [Abstract] | [Tab. 3]: S2's successes vs all 107 input papers | false under SAR for ICML (5.7 vs 6.1) and pooled over venues (5.65 vs 5.85, computed); true under SP |
| C-MAIN-5 | S2 beats accepted ICLR 2026 and NeurIPS 2025 papers under both reviewers [§4.1] [Tab. 3] | n = 4 vs 5 and 33 vs 38 papers | true as stated; the SAR margins are 0.1–0.2 points, about 0.6 standard errors; S2's SAR acceptance on NeurIPS is lower (75.8% vs 76.3%) |
| C-MAIN-8 | S2's gains beat AutoSOTA's on mean and median [§4.1] [Tab. 4] | overall pools differ (86 vs 105 tasks); AutoSOTA's deltas are its own reports [App. B] | both venue pools are shared (33 NeurIPS and 4 ICLR papers, S2's successes) and only the overall pools differ (86 vs 105); AutoSOTA leads on ICLR (7.2% vs 3.8%); S2's own ICLR cells cannot be rebuilt from Tab. 16; the deltas are self-reported on partly different metrics, and App. B calls them "not a head-to-head" (A-EVAL-7) |
| C-ABLX-4 | the review loop also raises SAR acceptance [§4.2] [Tab. 5] | 49 ICML successes, review rounds 0–2 | no held-out gain in round 2 (36 → 34 of 49; exact McNemar p ≥ 0.50), while SP rises to 46 of 49; the shipped two-round setting is the one that maximizes the in-loop reviewer |
| C-ABLX-6 | review-driven refinement is "essential" [§4.2] [Tab. 6] | one task (AI Engram) | n = 1; the refined method is worse than the human baseline on EM by +0.067 (0.071 vs 0.004, lower is better) |
| C-ABLX-7 | S2 passes all four integrity audits [§4.2] [Tab. 7] | 49 ICML successes; the auditor is unspecified (U-EVAL-5) | internally consistent (50 → 49; 19/1840 → 0/1814), but Score Verif. passed row 1's reward-hacked codebase (50/50, with 1/50 specification violations) [fn. 2], so it shows determinism, not validity; covers 49 of the 86 successes |
| C-DISC-1, C-DISC-3 | 2.5 days and $3765 per task [Fig. 10] [§4.3]; about $3,800 [§5] | 33 NeurIPS tasks, apparently the successes only [inferred] | failed runs' cost is unreported (U-COST-2); prices and machines are unspecified (U-COST-1) |
| C-DISC-5 | human reviewers rate S2 at parity overall [§4.3] [Tab. 10] | 33 papers, 9 reviewers | means only, no dispersion or agreement; protocol unspecified (U-EVAL-6) |

## The eight findings that matter most

1. **Acceptance is never defined, and SP's `Accept Rate` cannot mean a rating of 8 or more** (A-EVAL-3). §3.5 calls 8 "the acceptance threshold" [§3.5], yet S2's ICLR row accepts 4 of 4 papers at a mean of 7.0, impossible under "≥ 8" without any SD argument [Tab. 3]; the minimum-SD test rules out "≥ 8" on 9 of the other 10 rows with acceptances, for example human NeurIPS (at least 2.43 against a printed 1.9) and S2 ICML (1.37 against 1.0) [Tab. 3] [Tab. 5]; one of the nine, S2 NeurIPS, counts only by a hair under the population SD (1.7502 against below 1.75) and by 0.027 under the sample SD that P-EVAL-4 favours (1.78). With one integer rating per paper and the sample SD, only "≥ 6" fits all 11 rows (`sp_integer.py`), so the rule is consistent only with ≥ 6 [inferred]; if SP averages several reviews and accepts by majority, the argument fails [ours].
2. **The held-out reviewer does not follow the in-loop one** (C-ABLX-4). Over review rounds 0, 1, 2 SAR accepts 24, 36, 34 of 49 papers while SP accepts 23, 39, 46 [Tab. 5]: round 2 brings no held-out gain (exact McNemar p ≥ 0.50 for 36 → 34), yet it is the reported system [Tab. 3] [ours].
3. **Under SAR, S2's papers are accepted less often than the human papers they start from**: 62/86 = 72.1% against 94/107 = 87.9% [Tab. 3], and 62/107 = 57.9% per input task [ours]. The abstract's "higher average review ratings" holds only under SP (C-HEAD-4) [Abstract].
4. **The 25.2% is a skewed, success-only, LLM-extracted mean, measured on the data the search selected on** (C-HEAD-2). Its median is 7.7% [Tab. 4]; the implied ICML mean is 34.4–34.7% against 13.9% (NeurIPS) and 3.8% (ICLR) [Tab. 4]; about 52 of 86 bars fall in 0–10% and 5 exceed +100% (image) [Fig. 1]. The gain rule is undefined, and it decides the number: on p. 41's averages, AUROC gives +0.26% to +0.40% and relative FPR95 gives 42.3% to 48.0%, more than 100-fold apart (image) [p. 41]; VD-STrans is 10.9% in [Fig. 2] and a "12.3% average throughput boost" in its own paper [p. 3] (U-EVAL-1) [ours].
5. **Success has three readings** (A-EVAL-1): at least one `Good` idea [§3.3], an improvement over human SOTA [Fig. 1], or a gain the ablation critic attributes to the new mechanism [Tab. 15]; yet the ablation critic of §3.4 has no reject verdict [§3.4].
6. **Tab. 4 is framed head-to-head; App. B says such deltas are not comparable** (A-EVAL-7) [App. B]. Tab. 4's AutoSOTA ICLR figures do reproduce from Tab. 16 (mean 7.23, median 4.99 over the four papers other than TeCh), including a T-SAE gain that App. B says did not survive re-evaluation [Tab. 16] [ours].
7. **Cost and time rest on 33 NeurIPS runs that appear to be the successes only** (U-COST-2) [§4.3], and the caption's "majority" for idea refinement is 44.9% of time and 45.4% of cost (image) [Fig. 10] (A-COST-1).
8. **Every ablation is conditioned on the 49 ICML successes, from one run, without variance** [§4.2]. Fig. 9a's final gain (33.4%, image) sits 1.0–1.3 points below the ICML mean implied by Tab. 4 (34.43–34.68%); the "strictly better" gates predict that order if the two are measured at different points, so A-EVAL-6 is AMBIGUOUS, not a contradiction, and the per-round gain stays undefined (U-EVAL-8) [Fig. 9] [ours].

## Index

| File | Covers | IDs |
|---|---|---|
| [claims/headline.md](claims/headline.md) | abstract, §1 with Figs. 1–2, §5 [Abstract] [§1] [§5] | C-HEAD-1 … 11 |
| [claims/main-results.md](claims/main-results.md) | §4 setup and §4.1 with Tabs. 2–4 and Fig. 8 [§4.1] | C-MAIN-1 … 9 |
| [claims/ablations.md](claims/ablations.md) | §4.2 with Fig. 9 and Tabs. 5–8 [§4.2] | C-ABLX-1 … 8 |
| [claims/discussion.md](claims/discussion.md) | §4.3 with Fig. 10, Tabs. 9–11 and Fig. 11 [§4.3] | C-DISC-1 … 7 |
| [claims/appendix-b.md](claims/appendix-b.md) | App. B with Tabs. 15–16 [App. B] | C-APPB-1 … 10 |
| this file | App. A.1 counts, the measurement definitions, the gaps [App. A.1] | C-BENCH-1 … 4; P-EVAL, P-BENCH, P-COST; U- and A- items |

## Which tasks each number rests on

| Evidence | Tasks | n | Reviewer or judge | Models | Where |
|---|---|---|---|---|---|
| success rate, S2 rows of Tab. 3 | all venues | 107 inputs, 86 papers | SP and SAR | Gemini 3.6 Flash, and Claude Code with Opus 4.8 for four agents | [Tab. 3] [App. A.2] |
| relative gain | the successes | 86 (33 NeurIPS, 4 ICLR, 49 ICML by difference) | Gemini 3.6 Flash parsing S2's paper tables 10 times | as above | [Tab. 4] [§4.1] |
| human rows of Tab. 3 | all inputs | 107 (5, 38, 64) | SP and SAR | none | [Tab. 3] |
| baseline agents | each agent's public papers | 2–21 per agent | SP and SAR | not stated | [Tab. 2] |
| ablations: Fig. 9, Tabs. 5 and 7 | ICML 2026 Spotlight successes | 49 (50 in Tab. 7's first row) | SP, SAR, CoE audit | as above | [§4.2] |
| review-driven refinement | one ICML task, AI Engram | 1 | TOFU metrics | as above | [Tab. 6] |
| coding-agent swap | ICLR 2026 | 5 | SP and SAR | Antigravity with Gemini 3.8 Flash | [Tab. 8] |
| time and cost | NeurIPS 2025, apparently the successes [inferred] | 33 | none | as above | [§4.3] [Fig. 10] |
| frontier expansion | one ICML task, Incremental BPE | 1 | an unnamed "Rating" (A-EVAL-8) | as above | [Tab. 9] |
| human evaluation | NeurIPS-derived papers | 33 papers, 9 reviewers | humans | none | [Tab. 10] |
| DynaSpec-RAG | one NeurIPS task, TS-RAG | 1 | MSE and MAE | as above | [Tab. 11] |
| AutoSOTA detail | ICLR 2026 | 5 | self-reported deltas | as above | [App. B] |

## How the paper measures

Each definition is classified as the README prescribes; each one that is not SPECIFIED has its gap in full under "Gaps found here" [ours].

### P-EVAL-1 · Task success · AMBIGUOUS (A-EVAL-1)

- Used for: the 80.4% success rate [Fig. 1] [§4.1], the `# Papers` column [Tab. 3] [Tab. 4], and `SR` [Tab. 8].
- Reading (a), the pipeline finished: the process stops if round K "is reached with zero successful ideas" [§3.3] (tex:sections/3_new_method.tex:86), and Tab. 3 counts "the number of papers successfully generated by ScientistTwo" [Tab. 3] (tex:tables/conference_accepted_comparison.tex:3).
- Reading (b), the human SOTA was beaten: S2 "improves 86 out of 107 papers" [Fig. 1] (tex:figures/problem_setup.tex:10), and the other slots of the ring are labelled `Failed to Improve` (image) [Fig. 1b].
- Reading (c), the gain is attributed in ablation: S2 "additionally requires the gain to be attributable to the proposed mechanism in ablation" [Tab. 15] (tex:sections/appendix.tex:176-177), and TeCh's variant "was not accepted as a contribution" after the ablation critic rejected it [App. B] (tex:sections/appendix.tex:224-225).
- Why (c) conflicts with §3: the ablation critic emits only `Good` or `Refine` [§3.4] (tex:sections/3_new_method.tex:106); §3 describes no path on which an ablation verdict ends a task.

### P-EVAL-2 · Relative gain of one paper · UNSPECIFIED (U-EVAL-1); reference baseline AMBIGUOUS (A-EVAL-2)

- Said: a comparison "based on the performance gains reported over human state-of-the-art baselines" [§4.1] (tex:sections/4_experiment.tex:19).
- Said: "we parse the main tables for 10 times using Gemini 3.6 Flash and averaged them" [§4.1] (tex:sections/4_experiment.tex:19). The source is the generated paper's own tables, not a harness [ours].
- Not said: the formula; which table, metric or dataset; how several metrics or datasets combine; the sign for lower-is-better metrics; the spread of the 10 parses [§4.1].
- Why it matters: on p. 41's averages (Procrustes-DS 99.56/2.17 against X-Maha 99.16/4.17 reproduced and 99.30/3.76 published), AUROC gives +0.26% to +0.40% while relative FPR95 gives 42.3% to 48.0%, so the rule alone moves one task's gain more than 100-fold (image) [p. 41] [ours].
- Also: the VD-STrans result is a 10.9% gain in [Fig. 2] and a "12.3% average throughput boost" in the generated paper [p. 3]; 1 − 1/1.123 = 10.95% suggests a time-based rule [ours].
- Selection [ours]: each gain is measured on the data the search selected on. A task's winner is the best of up to 8–10 candidates [App. A.2] [inferred], chosen among ideas "evaluated on the full benchmark" [§3.3] (tex:sections/3_new_method.tex:90), and kept only through two gates, "strictly outperforms" [§3.4] (tex:sections/3_new_method.tex:111) and "verified as strictly superior" [§3.6] (tex:sections/3_new_method.tex:148).
- Consequence [ours]: the gains and the success count carry a winner's-curse inflation that cannot be sized, since no run-to-run variance is reported (U-EVAL-4); the split gaps are U-NOTE-1, U-ART-5 and U-TOP-5 (F-AN-3). Decision for task 6: a held-out test set, and a null-idea control that measures the false-success rate.

### P-EVAL-3 · Gain across papers · SPECIFIED in part

- Said: Tab. 4 reports "performance gain (%) across successful cases" [Tab. 4] (tex:tables/autosota_comparison.tex:3), with columns `Med. Gain` and `Avg. Gain`, so failures are excluded and both median and mean are given.
- Checked: the AutoSOTA ICLR cells equal the plain mean and median of Tab. 16's four deltas other than TeCh (7.23 and 4.99), which confirms per-paper averaging [ours] (C-MAIN-8).
- Not said: whether S2's Overall 25.2% is the plain mean over the 86 papers; the decomposition in C-HEAD-2 assumes it [ours].

### P-EVAL-4 · `Avg. Rating` · AMBIGUOUS (A-EVAL-4); reviewer set-up UNSPECIFIED (U-EVAL-2)

- Said: the tables give "the average review ratings, standard deviations (1–10 scale), and acceptance rates" [Tab. 3] (tex:tables/conference_accepted_comparison.tex:3).
- Said: SP produces an "overall numerical score" s_review in [1, 10] "based on the standard ICLR grading scale" [§3.5] (tex:sections/3_new_method.tex:123).
- Not said: one review or several per paper; SP's backbone model and version; population or sample SD [§4].
- Checked: with one integer rating per paper, the population SD leaves three rows with no solution (Antigravity, AI Scientist-v2, AutoResearchClaw), while the sample SD fits all 18 rows, which favours the sample SD (`sp_integer.py`, re-run by `claims_arithmetic.py`) [Tab. 2] [Tab. 8] [ours].
- Checked: among integer ratings, only 1, 2 and 3 with the sample SD reproduce Tab. 2's AI Scientist-v2 SP cell, 2.0 ± 1.0 over 3 papers; no three scores from the set 1, 3, 5, 6, 8, 10 average 2.0 [Tab. 2] [ours; the score set is our assumption about the ICLR scale].

### P-EVAL-5 · SP acceptance · INCONSISTENT (A-EVAL-3)

- Said: the rebuttal starts when the score "is below the acceptance threshold (e.g., 8)" [§3.5] (tex:sections/3_new_method.tex:124); the loop stops "if the ScholarPeer review score reaches 8" [App. A.2] (tex:sections/appendix.tex:155).
- Contradicted by the tables, if a paper is accepted when the rating the table averages is 8 or more: S2's ICLR row accepts 4 of 4 at a mean of 7.0, which no SD can rescue [Tab. 3] [ours].
- The minimum-SD test rules out 9 of the other 10 rows with acceptances, among them S2 ICML (at least 1.37 against 1.0), S2 Overall (1.51 against 1.3), human NeurIPS (2.43 against 1.9), round 0 (2.59 against 2.2) and Antigravity (2.33 against 1.5); only the human ICLR row allows it [Tab. 3] [Tab. 5] [Tab. 8] [ours].
- These are population-SD bounds, the weaker convention; the count is 10 of 11 under both conventions, but one of the nine, S2 NeurIPS, counts only by a hair under the population SD (1.7502 against below 1.75) and by 0.027 under the sample SD that P-EVAL-4 favours (1.78) (`claims_arithmetic.py`) [Tab. 3] [ours].
- Consistent with: one integer rating per paper and the sample SD leave only "≥ 6" fitting all 11 rows; Antigravity's 6.3 ± 1.5 with 2 of 3 accepted forces the ratings 5, 6 and 8, hence the threshold 6 [Tab. 8] (`sp_integer.py`) [inferred].
- Caveat: if SP averages several reviews and accepts by majority, the tables constrain nothing and neither result holds [ours].
- Not said: the rule the tables do use [Tab. 3].

### P-EVAL-6 · SAR rating and acceptance · UNSPECIFIED (U-EVAL-3)

- Said: only a link, "https://paperreview.ai/" [fn. 1] (tex:sections/4_experiment.tex:5), a 1–10 scale [Tab. 3], and that SAR "serves as a held-out evaluator that was unseen during development by both the baselines and our method" [§4] (tex:sections/4_experiment.tex:5).
- Checked: SAR ratings are finer than half-points, since Zochi's 2.9 ± 0.6 over 2 papers needs a sum between 5.7 and 5.9, which no two integers or half-integers make [Tab. 2]; S2's ICLR 5.4 ± 0.2 over 4 needs a sum between 21.4 and 21.8, which no four integers make [Tab. 3] [ours].
- Not said: the acceptance rule, the service's version and query dates, repeated queries [§4].

### P-EVAL-7 · Which reviewer is in the loop · SPECIFIED

- Said: "ScholarPeer serves as an in-distribution evaluation, as it is also used to refine the draft quality generated by ScientistTwo" [§4] (tex:sections/4_experiment.tex:5); the Peer-Reviewer Agent is ScholarPeer [§3.5] (tex:sections/3_new_method.tex:123).
- Consequence [ours]: only SAR numbers measure quality beyond the optimization target, yet the headline acceptance (91.9%) is SP's; our project's rule that the reported judge is never the optimized reviewer rules out reporting SP as evidence.

### P-EVAL-8 · Review rounds of Tab. 5 · AMBIGUOUS (A-EVAL-5)

- Said: rows for `Review Round` 0, 1 and 2, with the Rebuttal Agent off only in round 0 [Tab. 5] (tex:tables/ablation_rebuttal.tex:12-14); the loop runs "for at most two rounds" and stops early at 8 [App. A.2] (tex:sections/appendix.tex:155).
- Not said: whether a paper that stopped early carries its last draft into later rounds, and whether round 2 includes the meta-review refinement; round 2 equals Tab. 3's ICML row, the final system [Tab. 3] [ours].

### P-EVAL-9 · Runs, seeds, variance · UNSPECIFIED (U-EVAL-4)

- Said: the ± values are "standard deviations" across papers [Tab. 2] (tex:tables/ai_scientist_comparison.tex:3).
- Not said: the number of runs per task, seeds, run-to-run variance; §4 mentions no repeats [§4]. Identical rows (Tab. 3 ICML = Tab. 5 round 2; Tab. 3 ICLR = Tab. 8 Claude Code) suggest one run reused across tables [inferred] [Tab. 8].

### P-EVAL-10 · CoE integrity audit · checks SPECIFIED, auditor UNSPECIFIED (U-EVAL-5)

- Said: four checks; score verification works "by comparing reported scores against those obtained from re-executing the repository" [§4.2] (tex:sections/4_experiment.tex:41); Tab. 7's columns are defined in its caption [Tab. 7] (tex:tables/ablation_audit.tex:3).
- Specified by reference: Tab. 7 is an "Evaluation of paper and code integrity following" ScientistOne [Tab. 7] (tex:tables/ablation_audit.tex:3), so ScientistOne's CoE audit specifies it; its protocol is in U-EVAL-5 [ours].
- Not said: who or what runs the audit behind Tab. 7, with which model, and whether it is the same kind of agent as the in-pipeline fixer, where "the Coding Agent audits the repository against the manuscript" [§4.2] (tex:sections/4_experiment.tex:43).

### P-EVAL-11 · Human evaluation · protocol UNSPECIFIED (U-EVAL-6)

- Said: 33 papers, "evaluated by 9 experienced human reviewers" [§4.3] (tex:sections/5_discussion.tex:12); scales "on a 1–5 Likert scale (> 3.0 indicates positive endorsement)" and "3.0 = Parity, > 3.0 favors ScientistTwo" [Tab. 10] (tex:tables/human_eval.tex:4).

### P-EVAL-12 · Fig. 1a radar · UNSPECIFIED (U-EVAL-7)

- Shown: `Human Frontier`, `Expanded Frontier` and `Upper Bound` on a radial scale from 0.2 to 1.0 over 35 sub-areas of 8 areas (image) [Fig. 1a]; no sentence defines the plotted quantity [§1].

### P-EVAL-13 · Per-round gain of Fig. 9a · UNSPECIFIED (U-EVAL-8); AMBIGUOUS against Tab. 4 (A-EVAL-6, reclassified from INCONSISTENT)

- Shown: `Relative Gain (%)` for Initial and Rounds 1–4 on the 49 ICML tasks (image) [Fig. 9a]; the text calls it "the relative gain over the human state-of-the-art baseline" [§4.2] (tex:sections/4_experiment.tex:28).

### P-EVAL-14 · Other systems' numbers · SPECIFIED in part (U-EVAL-9, U-EVAL-10, A-EVAL-7)

- Said: baselines are scored on "the number of publicly released AI-generated papers by each autonomous research agent" [Tab. 2] (tex:tables/ai_scientist_comparison.tex:3); for ICLR, AutoSOTA's delta "is self-reported by each system against its own reproduced baseline" [Tab. 16] (tex:sections/appendix.tex:263).
- Not said: which papers the baselines and Agent4Science rows are; where AutoSOTA's 105-paper and NeurIPS figures come from [Tab. 4].

### P-EVAL-15 · The `Rating` of Tab. 9 · AMBIGUOUS (A-EVAL-8)

- Shown: VD-STrans 6.5, BXT-Transducer 5.6, SBR-Transducer 7.1, reviewer unnamed [Tab. 9] (tex:tables/sequential_scientisttwo.tex:11-15).

### P-BENCH-1 · The 107 tasks · SPECIFIED, with claims C-BENCH-1 … 4

- C-BENCH-1: "We utilize 38 papers accepted at NeurIPS 2025", drawn from AutoSOTA's benchmarks [App. A.1] (tex:sections/appendix.tex:3); Tab. 12 lists 38 rows (tex:sections/appendix.tex:13-50) [Tab. 12].
- C-BENCH-2: "We utilize 5 papers accepted at ICLR 2026", also from AutoSOTA [App. A.1] (tex:sections/appendix.tex:55); Tab. 13 lists 5 rows (tex:sections/appendix.tex:65-69) [Tab. 13].
- C-BENCH-3: "We utilize 64 papers accepted as spotlight presentations at ICML 2026" [App. A.1] (tex:sections/appendix.tex:74); Tab. 14 lists 64 rows (tex:sections/appendix.tex:85-148) [Tab. 14].
- C-BENCH-4: "107 scientific problems drawn from top machine learning venues" [§4] (tex:sections/4_experiment.tex:5), repeated in [§1] and [§5].
- Checks: 38 + 5 + 64 = 107; the 107 bib keys are distinct; the booktitle of all 107 entries in main.bib matches its list, the Thirty-ninth NeurIPS for all 38 of Tab. 12, the Fourteenth ICLR for all 5 of Tab. 13, the Forty-third ICML for all 64 of Tab. 14; one entry per list, for example: [Bib: wei2025xmahalanobis] [Bib: bhalla2026temporal] [Bib: jiang2026incremental] [ours].
- Not checkable: spotlight status, which the bib does not record [Tab. 14] [ours].
- Assessment [ours]: the task list is fully specified and verified; what each task hands the engine is not (U-BENCH-1).

### P-BENCH-2 · What a task gives the engine · UNSPECIFIED (U-BENCH-1)

- Said: accepted papers "whose problem specifications and codebases serve as benchmark tasks" [§4.1] (tex:sections/4_experiment.tex:16); the engine is defined on "a scientific problem" G alone [§3 "Problem Setup"] (tex:sections/3_new_method.tex:7).

### P-BENCH-3 · How the ICML 64 were chosen · UNSPECIFIED (U-BENCH-2)

- Said: they "were selected from among all spotlight papers by strictly adhering to AutoSOTA's filtering process (e.g., verifying reproducibility)" [App. A.1] (tex:sections/appendix.tex:74).

### P-BENCH-4 · The 21 failures · UNSPECIFIED (U-BENCH-3)

- Said: per venue, 1 of 5 (ICLR), 5 of 38 (NeurIPS), 15 of 64 (ICML) failed [Tab. 3]; only the ICLR one is named, TeCh [Tab. 16] (tex:sections/appendix.tex:298-300).

### P-COST-1 · Dollar cost · components UNSPECIFIED (U-COST-1)

- Said: "an average cost of $3765, including token usage costs and virtual machine costs" [§4.3] (tex:sections/5_discussion.tex:4); the same $3765 sits in the cost donut (image) [Fig. 10b].

### P-COST-2 · Which runs are costed · UNSPECIFIED (U-COST-2)

- Said: "we analyze on the 33 target problems sourced from NeurIPS 2025 papers" [§4.3] (tex:sections/5_discussion.tex:4); 33 is exactly the number of NeurIPS successes [Tab. 3], so the 5 failed runs are apparently excluded [inferred].

### P-COST-3 · Time · UNSPECIFIED (U-COST-3)

- Shown: days per task, as a histogram with mean 2.51, median 2.00 and IQR 1.1–3.1 days (image) [Fig. 10a]; how time was measured is not stated [§4.3].

### P-COST-4 · Stage breakdown · AMBIGUOUS (A-COST-1)

- Shown: six stages, `Seed Idea Generation`, `Initial Implements`, `Idea Refinement`, `Ablation Studies`, `Initial Drafting` and `Peer&Meta-Review` (image) [Fig. 10b]; §3 has no stage called Initial Implements [§3].

## What task 5 must measure itself

The paper gives no reproducible per-task targets, no run-to-run variance, no token or machine split of its cost, and no definition of a task's subset, full set, metric, gain rule or seeds (U-EVAL-1, U-EVAL-4, U-COST-1, U-TOP-1) [§4] [App. A.1] [ours]. Task 5's list of what to measure on our own first tasks is kept in the reviews rather than copied here [ours]:

- the research engineer's wave 1, section *What task 5 still needs from the paper*: targets, statistical power, cost per success, billing and task definitions, in [research-engineer.md](../reviews/paper-analysis-2026-09-27/research-engineer.md) [ours];
- the research engineer's wave 2, section *What task 5 still needs*: an expected session count, tokens and GPU-hours per session type, the per-task fields fixed before any run, and wall-clock per session, in [research-engineer-analysis.md](../reviews/paper-analysis-2026-09-27/research-engineer-analysis.md) [ours].

## Gaps found here

### U-EVAL-1 · How one paper's relative gain is computed

- *Register: U-EVAL-1*
- Strongest example [ours]: on p. 41's averages, AUROC gives a gain of +0.26% to +0.40% while relative FPR95 gives 42.3% to 48.0%; the choice of rule alone moves one task's gain more than 100-fold (image) [p. 41].
- Statement: every gain in the paper (25.2%, 13.9%, 3.8%, Fig. 9a, Tabs. 8 and 9) rests on a per-paper formula the paper never gives [Tab. 4] [ours].
- The paper says: "we parse the main tables for 10 times using Gemini 3.6 Flash and averaged them" [§4.1] (tex:sections/4_experiment.tex:19).
- Silent on: the metric and datasets used when a table has several, how they combine, the sign for lower-is-better metrics, what counts as a main table, and the spread of the 10 parses [§4.1].
- Silent on: whether a parsed gain matches re-executed code; score verification is reported only for the 49 ICML papers [Tab. 7].
- A second example: the VD-STrans result is 10.9% in [Fig. 2] but a "12.3% average throughput boost" in its own paper [p. 3] [ours].
- Decision it forces [ours], the register's U-EVAL-1 (F-12): a pre-registered rule per task (metric, datasets, direction), computed from harness result files against both references, the published number and our reproduction, with both reported; never from the generated paper; reported as mean, median and a failure-inclusive mean.

### U-EVAL-2 · ScholarPeer's set-up

- *Register: U-PEER-3*
- Statement: SP is both the in-loop reviewer and a reported evaluator, and its configuration is not given [§3.5] [§4] [Bib: goyal2026scholarpeer].
- The paper says: "ScholarPeer serves as an in-distribution evaluation, as it is also used to refine the draft quality generated by ScientistTwo" [§4] (tex:sections/4_experiment.tex:5); it scores on "the standard ICLR grading scale" [§3.5] (tex:sections/3_new_method.tex:123).
- Silent on: backbone model and version, reviews per paper, temperature, and whether the evaluation uses the in-loop configuration and prompt [§4].
- Decision it forces [ours]: pin SP's implementation, model and version, and log raw reviews; as the optimized reviewer, SP is never reported as evidence.

### U-EVAL-3 · The Stanford Agentic Reviewer

- *Register: U-EVAL-3*
- Statement: SAR is the paper's only held-out judge, and the paper gives a link and a scale, nothing more [fn. 1] [Tab. 3].
- The paper says: SAR "serves as a held-out evaluator that was unseen during development by both the baselines and our method" [§4] (tex:sections/4_experiment.tex:5).
- Silent on: the acceptance rule, what the score aggregates, the service version and query dates, repeated queries, and whether the published human papers may be known to its model [§4].
- Decision it forces [ours]: whether an external service versioned by its host can serve as a locked evaluator; if used, k queries per paper with date and raw output, and our own acceptance rule.

### U-EVAL-4 · Runs, seeds and variance

- *Register: U-EVAL-4*
- Statement: no number in the paper carries a run-to-run spread; the ± values are "standard deviations" across papers [Tab. 2] [§4].
- Silent on: runs per task, seeds, and whether ablation variants are separate runs or stages switched off in the main run [§4.2].
- Decision it forces [ours]: runs per task, seeds, and a variance report for every headline number.

### U-EVAL-5 · Who runs the integrity audit

- *Register: U-EVAL-5*
- Statement: Tab. 7 comes from an unnamed auditor [Tab. 7].
- The paper says: the audit "is a post-hoc evaluation framework that verifies whether claims in a generated paper are supported by its artifacts" [§4.2] (tex:sections/4_experiment.tex:41).
- Silent on: the auditing model, its independence from the pipeline's own fixer, where "the Coding Agent audits the repository against the manuscript" [§4.2] (tex:sections/4_experiment.tex:43), and audits of the NeurIPS, ICLR and Antigravity papers [§4.2].
- Note: the Antigravity codebases are said to "remain fully reproducible, exhibit no specification violations" with no table behind it [§4.2] (tex:sections/4_experiment.tex:46).
- Specified by reference (F-CL-12) [ours]: Tab. 7 follows ScientistOne [Tab. 7], so its audit is ScientistOne's CoE audit; the delegated definition is ScientistOne's §5, below, and the engine side records it in [stages/07-integrity.md](stages/07-integrity.md) (F-AN-12); ScientistOne's §6 and App. E add the settings of its own runs, which are not part of that definition.
- I1 compares the paper's score with "scores obtained by re-running the submitted solution on the golden evaluator", passing "within an adaptive tolerance that accounts for evaluator noise" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:25-26).
- In ScientistOne's own runs, not in its audit's definition: "We run each evaluator five times", against the tolerance max(1%, 3σ/|s̄|) (paraphrase of the formula), on tasks where "Each task provides a fixed evaluator, starter code, and scoring metric" [Ref: meng2026scientistone §6] (ref:2605.26340v1:sections/06a_setup.tex:8-10); these are the settings of its own benchmark, and the definition (§5, above) names only an adaptive tolerance, with no run count or formula [ours].
- I2 is LLM judgment "with majority vote across multiple runs" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:32); in ScientistOne's own runs the vote is "majority vote (3/5 judges)" [Ref: meng2026scientistone App. E] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:302).
- I3 queries four academic APIs, Semantic Scholar, arXiv, OpenAlex and CrossRef [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:36).
- I4 is lenient: "only cases where the paper describes a fundamentally different algorithm count as misaligned" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:43).
- Still open [ours]: the reference fixes the procedure, not who ran it for Tab. 7, with which model or on which tasks; and ScientistTwo's tasks come with no golden evaluator for I1 to use (U-INT-4, which F-AN-12 adds) [§4.2].
- Decision it forces [ours]: the audit belongs to the locked evaluation, run on every task by a judge that is not the pipeline's fixer.

### U-EVAL-6 · The human evaluation's protocol

- *Register: U-EVAL-6*
- Statement: Tab. 10 gives six means per scale and nothing else [Tab. 10].
- The paper says: 33 papers were "evaluated by 9 experienced human reviewers", first standalone and then "in pairwise comparative assessments against accepted human-authored papers" [§4.3] (tex:sections/5_discussion.tex:12).
- Silent on: assignment of the 9 reviewers to the 33 papers, reviews per paper, blinding, the human paper each S2 paper was compared with, recruitment, dispersion and agreement [§4.3].
- Decision it forces [ours]: whether a human study is in scope; if so, a written protocol with blinding and agreement statistics.

### U-EVAL-7 · What Fig. 1a plots

- *Register: U-EVAL-7*
- Statement: the radar's quantity is never defined; it shows `Human Frontier`, `Expanded Frontier` and `Upper Bound` on a 0.2–1.0 scale over 35 sub-areas (image) [Fig. 1a].
- Silent on: the quantity, its normalization, the meaning of `Upper Bound`, and how tasks map to sub-areas [§1].
- Decision it forces [ours]: none for the engine; we do not reproduce Fig. 1a.

### U-EVAL-8 · What Fig. 9a's per-round gain is

- *Register: U-EVAL-8*
- Statement: Fig. 9a plots a per-round `Relative Gain (%)` without a definition (image) [Fig. 9a].
- Silent on: how a task with no `Good` idea yet is counted, whether the value is best-so-far (the curve never falls, image), whether it is measured in the loop or parsed from the final paper, and which tasks remain in later rounds given the early stop at four successes [App. A.2].
- Decision it forces [ours]: log, per task and round, the best full-set gain so far under the U-EVAL-1 rule, with "no success yet" explicit.

### U-EVAL-9 · Which comparison papers

- *Register: U-EVAL-9*
- Statement: Tab. 2 and the Agent4Science row of Tab. 3 score papers the paper never lists [Tab. 2] [Tab. 3].
- The paper says: they are "publicly released AI-generated papers" [Tab. 2] (tex:tables/ai_scientist_comparison.tex:3) and "AI-generated papers accepted at Agent4Science 2025" [§4.1] (tex:sections/4_experiment.tex:16).
- Silent on: which papers, how they were chosen, and whether they were reviewed under the same settings [Tab. 2].
- Decision it forces [ours]: any comparison with other agents lists its papers and scores them under the same locked settings.

### U-EVAL-10 · Where AutoSOTA's numbers come from

- *Register: U-EVAL-10*
- Statement: Tab. 4's AutoSOTA row has 105 papers and NeurIPS figures of unstated source [Tab. 4].
- The paper says: S2 ran "on the same five ICLR 2026 submissions (Table 13) that AutoSOTA reports" [App. B] (tex:sections/appendix.tex:194-195), with deltas "self-reported by each system" [Tab. 16] (tex:sections/appendix.tex:263).
- Silent on: the 105 papers, how AutoSOTA's NeurIPS figures were restricted to S2's 33 successes, and AutoSOTA's version [Tab. 4].
- Decision it forces [ours]: compare with AutoSOTA only on shared tasks under one gain rule, or not at all.

### U-BENCH-1 · What a task hands the engine

- *Register: U-TOP-1*
- Statement: each task is an accepted paper "whose problem specifications and codebases serve as benchmark tasks" [§4.1] (tex:sections/4_experiment.tex:16), and nothing more precise is said.
- Silent on: paper text or PDF, the repository and its commit, compute, which reported numbers define the human SOTA, what the full benchmark is, and the screening subset, whose own gap is U-BASE-1 in stages/02 (F-15) [§3.2].
- Decision it forces [ours]: a per-task manifest (paper source, repository at a commit, SOTA table and metric, full-benchmark definition, screening subset, hardware).

### U-BENCH-2 · How the ICML 64 were chosen

- *Register: U-BENCH-2*
- Statement: they "were selected from among all spotlight papers by strictly adhering to AutoSOTA's filtering process" [App. A.1] (tex:sections/appendix.tex:74).
- Silent on: the pool size, the criteria beyond "verifying reproducibility", and who applied them and when [App. A.1].
- Decision it forces [ours]: a written task-selection filter, applied and recorded before any run.

### U-BENCH-3 · Why 21 tasks failed

- *Register: U-EVO-4*
- Statement: failures are counted per venue (1 of 5, 5 of 38, 15 of 64) but not listed or explained [Tab. 3], except TeCh [App. B] (tex:sections/appendix.tex:298-300).
- Silent on: the failed tasks and their causes, such as no `Good` idea after K rounds, a baseline not reproduced, or the specification filter [§3.3] [§4.2].
- Decision it forces [ours]: a failure reason per task from a fixed taxonomy, logged by the engine.

### U-COST-1 · What the $3765 contains

- *Register: U-COST-1*
- Statement: the cost is "including token usage costs and virtual machine costs" [§4.3] (tex:sections/5_discussion.tex:4), with no breakdown.
- Silent on: tokens per model, prices and their date, machine type, GPU count, hours and hourly price, and whether reviewer calls are included [§4.3].
- Decision it forces [ours]: record tokens per model with price and machine-hours with price, per stage and per task; an unknown cost is recorded as unknown.

### U-COST-2 · Which runs are costed

- *Register: U-COST-1*
- Statement: time and cost average "the 33 target problems sourced from NeurIPS 2025 papers" [§4.3] (tex:sections/5_discussion.tex:4); 33 is the NeurIPS success count [Tab. 3], so the 5 failed runs look excluded [inferred].
- Silent on: the cost of failed runs, and the cost per successful paper [§4.3].
- Decision it forces [ours]: report cost over all runs and per success.

### U-COST-3 · How time was measured

- *Register: U-COST-3*
- Statement: Fig. 10a gives days per task (image) [Fig. 10a].
- Silent on: wall-clock or busy time, queueing, parallelism (for example the two candidates per round [App. A.2]), and hardware [§4.3].
- Decision it forces [ours]: record wall-clock and busy time per stage, with the hardware.

### A-EVAL-1 · What "success" means · AMBIGUOUS, and reading (c) INCONSISTENT with §3.4

- *Register: A-EVAL-1*
- Reading (a), the pipeline finished with at least one `Good` idea: the run ends if round K "is reached with zero successful ideas" [§3.3] (tex:sections/3_new_method.tex:86); Tab. 3 counts "the number of papers successfully generated by ScientistTwo" [Tab. 3] (tex:tables/conference_accepted_comparison.tex:3).
- Reading (b), the human SOTA was beaten: S2 "improves 86 out of 107 papers (an 80.4% success rate)" [Fig. 1] (tex:figures/problem_setup.tex:10).
- Reading (c), the gain survives attribution: S2 "additionally requires the gain to be attributable to the proposed mechanism in ablation" [Tab. 15] (tex:sections/appendix.tex:176-177); DMC-TeCh "was not accepted as a contribution" [Tab. 16] (tex:sections/appendix.tex:299-300).
- Conflict: the ablation critic of §3.4 returns only `Good` or `Refine` [§3.4] (tex:sections/3_new_method.tex:106), so reading (c) needs a veto §3 does not describe (engine side: analysis.md, ABL).
- Decision it forces [ours]: success is a full-set `Good` idea with a positive gain under the U-EVAL-1 rule; whether an attribution check would veto it is recorded separately; all three counts are reported.

### A-EVAL-2 · Gain against which baseline · AMBIGUOUS

- *Register: U-EVAL-1*
- Reading (a), the paper's own numbers: the full-set critic asks "Is it better than the original SOTA result?" [Tab. 1] (tex:tables/overview.tex:16), and gains are "over the original human state-of-the-art baselines" [§1] (tex:sections/1_introduction.tex:21).
- Reading (b), a reproduction: each system "measures against its own reproduced baseline on different hardware" [App. B] (tex:sections/appendix.tex:202); S2 reproduces the baseline on the subset as E_base [§3.2] (tex:sections/3_new_method.tex:37).
- Decision it forces [ours], the register's U-EVAL-1, which this item joins (F-12): U-EVAL-1's pre-registered rule is computed against both references, the published number and our reproduction on our hardware, and both are reported.

### A-EVAL-3 · What ScholarPeer acceptance means · INCONSISTENT

- *Register: A-EVAL-3*
- Place 1: the rebuttal starts when the score "is below the acceptance threshold (e.g., 8)" [§3.5] (tex:sections/3_new_method.tex:124); the loop "terminates early if the ScholarPeer review score reaches 8" [App. A.2] (tex:sections/appendix.tex:155).
- Place 2: `Accept Rate` 100.0% at a mean of 7.0 (S2 ICLR, n = 4), 93.9% with 7.6 ± 1.0 (ICML, n = 49) and 91.9% with 7.5 ± 1.3 (Overall, n = 86) [Tab. 3] (tex:tables/conference_accepted_comparison.tex:19-22).
- Why they conflict [ours]: if a paper is accepted when the rating the table averages is 8 or more, S2's ICLR row is impossible outright, and the minimum-SD test rules out 9 of the other 10 rows with acceptances (ICML needs an SD of at least 1.37 against 1.0, Overall 1.51 against 1.3; one of the nine, S2 NeurIPS, counts only by a hair under the population SD (1.7502 against below 1.75) and by 0.027 under the sample SD that P-EVAL-4 favours (1.78)); only human ICLR allows it (`claims_arithmetic.py`; the reviewer's `sp_threshold.py` agrees on every row, printing 1.52 for Overall on its coarser grid) [Tab. 3] [Tab. 5] [Tab. 8].
- What the tables do fit [inferred]: with one integer rating per paper and the sample SD, only a threshold of 6 fits all 11 rows (`sp_integer.py`) [Tab. 3] [Tab. 8].
- Caveat [ours]: if SP averages several reviews and accepts by majority, the tables do not constrain the rule and this argument fails; the item stays INCONSISTENT as filed, on the single-rating reading.
- Decision it forces [ours]: define acceptance per reviewer explicitly, and never reuse the in-loop threshold's name for a reported metric.

### A-EVAL-4 · What a rating is · AMBIGUOUS

- *Register: A-EVAL-4*
- Reading (a): one "overall numerical score" per paper, "based on the standard ICLR grading scale" [§3.5] (tex:sections/3_new_method.tex:123).
- Reading (b): another form, such as integers outside the ICLR score set or an average of several reviews; among integer ratings, Tab. 2's AI Scientist-v2 cell (2.0 ± 1.0, n = 3) fits only 1, 2 and 3 with the sample SD [Tab. 2] [ours].
- Decision it forces [ours]: log the raw reviewer output per paper, and state the SD convention.

### A-EVAL-5 · What a review round in Tab. 5 is · AMBIGUOUS

- *Register: A-EVAL-5*
- Reading (a): the state after r review–rebuttal cycles, each paper frozen once it reaches 8 [App. A.2] (tex:sections/appendix.tex:155).
- Reading (b): round 2 is the final system including the meta-review refinement, since its row equals Tab. 3's ICML row [Tab. 5] [Tab. 3].
- Decision it forces [ours]: log per paper the round index, the stop reason and whether the meta-review changed the idea; report per-round snapshots and the final output separately.

### A-EVAL-6 · Two gains on the same 49 tasks differ · AMBIGUOUS (filed INCONSISTENT, reclassified after the review)

- *Register: U-EVAL-8*
- Place 1: the final round of Fig. 9a is 33.4% (image) [Fig. 9a].
- Place 2: Tab. 4 implies an ICML mean of 34.43–34.68%, from (86 × 25.2 − 33 × 13.9 − 4 × 3.8) / 49 with rounding [Tab. 4] [ours].
- Reading (a), two points in the pipeline: Fig. 9a is read at the end of idea refinement and Tab. 4 on the final paper; ablation and meta-review refinement replace h_best only when the new result "strictly outperforms" or is "verified as strictly superior" [§3.4] [§3.6], which predicts Tab. 4 ≥ Fig. 9a, as observed (+1.0 to +1.3 points) [ours].
- Reading (b), two measurements: a gain measured in the loop against one parsed by Gemini from the final paper's tables [§4.1] [ours].
- Verdict on the first filing [ours]: filed INCONSISTENT; the review (F-CL-4) showed that reading (a) predicts the observed order, so the two numbers need not contradict each other; what is AMBIGUOUS is which point each number measures.
- Decision it forces [ours]: one gain definition, computed at named checkpoints.

### A-EVAL-7 · Is Tab. 4 a head-to-head? · INCONSISTENT

- *Register: U-EVAL-10*
- Place 1: Tab. 4 bolds "the best score" [Tab. 4] (tex:tables/autosota_comparison.tex:3), and the text says S2 "shows superior performance to AutoSOTA" [§4.1] (tex:sections/4_experiment.tex:19).
- Place 2: "the two Δ columns are not a head-to-head on a common metric" [App. B] (tex:sections/appendix.tex:202); "the two columns optimize different metrics in three of five cases and are not a head-to-head" [Tab. 16] (tex:sections/appendix.tex:263-264).
- Decision it forces [ours]: compare systems only on common tasks, metric, hardware and gain rule.

### A-EVAL-8 · Whose rating Tab. 9 prints · AMBIGUOUS

- *Register: A-EVAL-8*
- Reading (a), SAR: VD-STrans's 6.5 equals its SAR score, "6.5 from the Stanford Agentic Reviewer" [Fig. 2] (tex:figures/qualitative_result.tex:21).
- Reading (b), unattributed: Tab. 9 names no reviewer, and SP gave the same paper 8.0 [Tab. 9] (tex:tables/sequential_scientisttwo.tex:11).
- Decision it forces [ours]: none for the engine; Tab. 9's ratings are recorded as unattributed.

### A-COST-1 · Fig. 10b's stages, and whether idea refinement is a majority · INCONSISTENT (caption vs image), stage mapping AMBIGUOUS

- *Register: A-COST-1*
- Place 1: "Idea refinement accounts for the majority of overall time and computational cost" [Fig. 10] (tex:figures/cost.tex:4).
- Place 2: `Idea Refinement` is 44.9% of time and 45.4% of cost (image) [Fig. 10b], a plurality; only with `Initial Implements` added is it a majority, 63.9% and 65.5% [ours].
- Place 3: the text names "the Idea Refinement, Dynamic Peer-Review, and Meta-Review stages" [§4.3] (tex:sections/5_discussion.tex:4), yet `Initial Implements` (19%) and `Ablation Studies` (16.4%) each take more time than `Peer&Meta-Review` (15.5%) (image) [Fig. 10b].
- Stage names: §3 has no stage named Initial Implements; the k = 0 round is described inside §3.3 [§3.3] (tex:sections/3_new_method.tex:63).
- Decision it forces [ours]: stage boundaries in our logs follow §3's stages, and shares are reported by those.
