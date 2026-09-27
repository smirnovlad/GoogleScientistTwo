# Claims of §4.3: cost, frontier expansion, human evaluation, case study (C-DISC)

Part of [claims.md](../claims.md), which holds the definitions and gaps cited here [ours]. §4.3 is a subsection despite its file name, `5_discussion.tex` [§4.3].

### C-DISC-1 · About 2.5 days per task (Fig. 10a)

- Claim: S2 "requires an average of 2–3 days to complete the entire research cycle, demonstrating significantly faster execution compared to human researchers" [§4.3 "Cost Analysis"] (tex:sections/5_discussion.tex:4); S2 "requires 2.5 days on average to improve a single paper" [Fig. 10] (tex:figures/cost.tex:4).
- Values (image) [Fig. 10a]: tasks per duration bin, below 1 day 6 (18.2%), 1–2 days 11 (33.3%), 2–3 days 5 (15.2%), 3–4 days 5 (15.2%), 4–5 days 4 (12.1%), 5 days or more 2 (6.1%); mean 2.51 days (60.2 h), median 2.00 days (48.0 h), IQR 1.1–3.1 days.
- Sample: "the 33 target problems sourced from NeurIPS 2025 papers" [§4.3] (tex:sections/5_discussion.tex:4); 33 is the NeurIPS success count [Tab. 3], so the 5 failed runs are apparently excluded [inferred] (U-COST-2); one run per task.
- Checks: 6 + 11 + 5 + 5 + 4 + 2 = 33 ✓; each share is its count over 33 ✓; 2.51 × 24 = 60.2 h ✓ (image) [Fig. 10a] [ours].
- Checks: the mean fits the histogram, 2.41 days from bin midpoints (taking 6 days for the top bin), at least 1.88 days ✓; the 17th of 33 values falls in the 1–2 day bin (6 + 11 = 17), so a median of exactly 2.00 needs that bin to include its upper edge [Fig. 10a] [ours].
- Checks: "2–3 days" in the text, 2.5 in the caption and 2.51 in the image agree ✓ [§4.3] [Fig. 10].
- Falsified by: the runs' own timings [ours].
- Assessment [ours]: no human time is measured anywhere, so "significantly faster ... compared to human researchers" has no evidence in the paper; wall-clock depends on hardware and parallelism, both unspecified (U-COST-3).

### C-DISC-2 · Where the time goes (Fig. 10b)

- Claim: "the majority of execution time is concentrated in the Idea Refinement, Dynamic Peer-Review, and Meta-Review stages" [§4.3] (tex:sections/5_discussion.tex:4).
- Caption: "Idea refinement accounts for the majority of overall time and computational cost, primarily driven by iterative idea evolution and experimental execution" [Fig. 10] (tex:figures/cost.tex:4).
- Values (image) [Fig. 10b], share of time and of cost: `Seed Idea Generation` 0.6% and 0.3%; `Initial Implements` 19% and 20.1%; `Idea Refinement` 44.9% and 45.4%; `Ablation Studies` 16.4% and 15.4%; `Initial Drafting` 3.6% and 3.1%; `Peer&Meta-Review` 15.5% and 15.8%.
- Checks: time shares sum to 100.0% and cost shares to 100.1% ✓; the text's three stages hold 44.9 + 15.5 = 60.4% of time, a majority ✓ [Fig. 10b] [ours].
- Checks: `Initial Implements` (19%) and `Ablation Studies` (16.4%) each take more time than `Peer&Meta-Review` (15.5%), so the text names the third-largest stage group after two larger ones [Fig. 10b] [ours].
- Checks: the caption's "majority" for idea refinement alone is 44.9% of time and 45.4% of cost, a plurality; it becomes a majority only with `Initial Implements` added, 63.9% and 65.5% (A-COST-1) [Fig. 10b] [ours].
- Assessment [ours]: usable for budgeting a replication (about 45% of the cost in idea refinement), once the stage boundaries are mapped to §3 (A-COST-1).

### C-DISC-3 · $3765 per task on average

- Claim: S2 "incurs an average cost of $3765, including token usage costs and virtual machine costs", and "Cost expenditure increases proportionally to execution time" [§4.3] (tex:sections/5_discussion.tex:4); the cost donut prints $3765 (image) [Fig. 10b].
- Sample: the same 33 NeurIPS runs, apparently the successes [inferred] [§4.3].
- Checks: text and figure agree ✓; §5's "approximately $3,800" is the rounded value ✓ (C-HEAD-11) [§5].
- Checks: at $3765, the stages cost about $1709 (idea refinement), $757 (initial implements), $595 (peer and meta review), $580 (ablation), $117 (initial drafting) and $11 (seed ideas) [Fig. 10b] [ours].
- Checks: the only evidence for "proportionally" is that each stage's time and cost shares differ by at most 1.1 points [Fig. 10b] [ours]; no per-task cost is shown.
- Assessment [ours]: no split between tokens and machines, no prices, no machine specification and no token counts (U-COST-1); failed runs excluded (U-COST-2); about $3.8k is the cost of a successful run, not of a success.

### C-DISC-4 · Three rounds of frontier expansion (Tab. 9)

- Claim: S2 discovers VD-STrans, "achieving a 10.9% improvement over the existing state of the art", then BXT-Transducer, "yielding an additional 9.6% relative improvement over VD-STrans", then SBR-Transducer, "again yielding an additional 8.2% improvement over BXT-Transducer" [§4.3 "Iterative Frontier Expansion"] (tex:sections/5_discussion.tex:9).
- Values: gains 10.9%, 9.6% and 8.2%; ratings 6.5, 5.6 and 7.1 [Tab. 9] (tex:tables/sequential_scientisttwo.tex:10-15).
- Sample: one task, Incremental BPE, an ICML 2026 Spotlight [Tab. 14]; three sequential runs; the reviewer behind `Rating` is not named (A-EVAL-8) [Tab. 9].
- Checks: compounded, 1.109 × 1.096 × 1.082 = 1.315, a 31.5% gain over the human baseline if the three gains are multiplicative on one metric [ours]; 10.9% and 6.5 match Fig. 2 (C-HEAD-8) [Fig. 2]; the second paper is rated lower (5.6) than the first (6.5) despite its gain [Tab. 9].
- Falsified by: a re-run of the chain, or other tasks [ours].
- Assessment [ours]: an anecdote with n = 1; the metric (throughput or time) and the reviewer are unnamed; from the second step on, S2's own previous method is the baseline.

### C-DISC-5 · Human evaluation (Tab. 10)

- Claim: "a human expert evaluation across 33 papers generated from NeurIPS-derived problems, evaluated by 9 experienced human reviewers" [§4.3 "Human Evaluation"] (tex:sections/5_discussion.tex:12).
- Claim: S2 "consistently received positive endorsements across all evaluated criteria, achieving notable strengths in ablation design", "achieved overall parity and was favored in experimental execution", while "human researchers retained a slight advantage in methodological rigor" [§4.3] (tex:sections/5_discussion.tex:12).
- Values: standalone 4.2, 4.1, 4.0, 4.3, 4.0 and 3.7, relative 3.1, 2.9, 3.5, 3.3, 3.3 and 3.0, for Introduction, Method, Baseline & Benchmark, Ablations, Insight & Limitation and Overall [Tab. 10] (tex:tables/human_eval.tex:10-15).
- Scales: standalone "on a 1–5 Likert scale (> 3.0 indicates positive endorsement)"; relative "3.0 = Parity, > 3.0 favors ScientistTwo" [Tab. 10] (tex:tables/human_eval.tex:4).
- Checks: every standalone score exceeds 3.0 ✓; Ablations is the highest standalone score (4.3) ✓; relative Overall is 3.0 ✓; Baseline & Benchmark is the highest relative score (3.5) ✓; Method is below parity (2.9) ✓ [Tab. 10] [ours].
- Checks: the standalone Overall score (3.7) is the lowest of the six [Tab. 10] [ours].
- Sample: 33 papers, which are the NeurIPS successes [Tab. 3], and 9 reviewers; assignment, reviews per paper, blinding, the paired human paper, dispersion and agreement are unspecified (U-EVAL-6) [§4.3].
- Assessment [ours]: descriptive means without dispersion; the reviewers' relation to the authors is not stated; parity on Overall (3.0) is the strongest statement it supports.

### C-DISC-6 · DynaSpec-RAG "consistently surpasses strong baselines" (Tab. 11)

- Claim: "it consistently surpasses strong baselines across standard benchmarks (see Table 11)" [§4.3 "Case Study"] (tex:sections/5_discussion.tex:18).
- Values: MSE and MAE on 7 datasets for 8 models at T = 512, L = 64 [Tab. 11] (tex:tables/case_study_ts_rag.tex:10-18).
- Sample: one task, TS-RAG, from NeurIPS 2025 [Tab. 12] [Bib: ning2025tsrag]; one run; whether the baseline numbers were re-run or copied is not stated [Tab. 11].
- Checks: every `Average` entry recomputes from its rows ✓, TimesFM's over 5 datasets because of its two dashes [Tab. 11] [ours].
- Checks: DynaSpec-RAG is not best on 3 of 14 cells, ETTh1 MAE (0.3627 against TS-RAG's 0.3624), Electricity MSE (0.1135 against 0.1120) and Electricity MAE (0.2059 against 0.2002); on Electricity it is third, behind TS-RAG and Chronos-Bolt B, as the bolding shows [Tab. 11] [ours].
- Checks: its average gain over TS-RAG is 2.47% in MSE and 0.16% in MAE [Tab. 11] [ours].
- Assessment [ours]: "consistently" overstates a result that wins 11 of 14 cells; the average margin is small, and in MAE it is 0.16%.

### C-DISC-7 · DynaSpec-RAG's size, transfer and acceptance

- Claim: DynaSpec-RAG "introduces only 0.27M trainable parameters", "transfers zero-shot to completely unseen multi-domain datasets without retraining", and reflects "parameter-efficient solutions that earn acceptance from competitive peer review" [§4.3] (tex:sections/5_discussion.tex:18).
- Claim: "it operates strictly on the output space of frozen time-series foundation models" [§4.3] (tex:sections/5_discussion.tex:18).
- Evidence: none in the main text; the generated paper is Appendix D, from [p. 56] on, which artifacts.md checks [App. D].
- Figure check: the architecture feeds the frozen backbone's `Query Latent Vector` into the cross-attention blocks (image) [Fig. 11], which is more than the output space [ours].
- Assessment [ours]: unverified here; the main text names neither the reviewer that accepted DynaSpec-RAG nor its score.
