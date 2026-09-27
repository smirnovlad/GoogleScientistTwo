# Claims of §4.2: ablations, Figure 9 and Tables 5–8 (C-ABLX)

Part of [claims.md](../claims.md), which holds the definitions and gaps cited here [ours].

Revised 2026-09-27 after the persona review: fixes F-CL-4, F-CL-5, F-CL-6, F-CL-8 and F-CL-11 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md` [ours].

**Scope of every §4.2 number.** §4.2 evaluates "on the 49 target problems sourced from ICML 2026 Spotlight papers" [§4.2] (tex:sections/4_experiment.tex:25), which are exactly S2's ICML successes, 49 of 64 [Tab. 3]. Every ablation is therefore conditioned on the full system succeeding, and none reports a seed or a spread across runs (U-EVAL-4) [ours]. The exceptions are Tab. 6, one task, and Tab. 8, five ICLR tasks [Tab. 6] [Tab. 8].

### C-ABLX-1 · Idea evolution raises the gain, most in the first round (Fig. 9a)

- Claim: "the relative gain over the human state-of-the-art baseline steadily increases as ScientistTwo proceeds through iterative idea refinement", and "the magnitude of improvement is most pronounced during the early refinement stages" [§4.2 "Effectiveness of Idea Evolution"] (tex:sections/4_experiment.tex:28).
- Caption: "Relative performance gains are largest during the initial improvement rounds and steadily diminish in later stages" [Fig. 9] (tex:figures/abl_idea_improvement.tex:4).
- Values (image) [Fig. 9a]: Initial 20.6%, Round 1 30.8% (+10.2), Round 2 32.4% (+1.6), Round 3 32.8% (+0.4), Round 4 33.4% (+0.6); a summary box gives initial 20.6%, final 33.4%, total boost +12.8%.
- Sample: the 49 ICML successes; the per-round gain is undefined (U-EVAL-8); one run [§4.2].
- Checks: 10.2 + 1.6 + 0.4 + 0.6 = 12.8 = 33.4 − 20.6 ✓ (image) [Fig. 9a]; the curve never falls, as a best-so-far value would behave [ours].
- Checks: "steadily diminish" is not strictly true, since Round 4's step (+0.6) is larger than Round 3's (+0.4) [Fig. 9a] [ours].
- Checks: the final 33.4% sits 1.0–1.3 points below the ICML mean implied by Tab. 4, 34.43–34.68%, the order the "strictly better" gates predict if the two are measured at different points (A-EVAL-6, reclassified AMBIGUOUS) [Tab. 4] [ours].
- Falsified by: the per-task values showing a smaller first step or a falling mean [ours].
- Assessment [ours]: descriptive, with no control arm (for example, fresh seed ideas at the same budget), so it cannot separate evolution from evaluating more candidates.
- For analysis.md [ours]: the five points (Initial and Rounds 1–4) suggest that App. A.2's "up to four rounds" counts refinement rounds after an initial round (key CFG) [App. A.2].

### C-ABLX-2 · Best ideas come early, and later ones are mostly evolved (Fig. 9b)

- Claim: "the majority of the top-performing ideas chosen by the Selector Agent are identified in the early stages", and later "newly selected best ideas are substantially more likely to be drawn from evolved candidates rather than original seed ideas" [§4.2 "Balancing Exploration and Exploitation"] (tex:sections/4_experiment.tex:30).
- Caption: "Across iterations, evolved ideas are selected for the majority of tasks" [Fig. 9] (tex:figures/abl_idea_improvement.tex:5).
- Values (image) [Fig. 9b]: tasks whose selected idea came from each round, Initial 14 (100% seed), Round 1 16 (87.5% evolved), Round 2 12 (75.0% evolved), Round 3 3 (66.7% evolved), Round 4 4 (50.0% evolved); a summary box gives 49 tasks, 27 evolved (55.1%), 22 seed (44.9%).
- Checks: 14 + 16 + 12 + 3 + 4 = 49 ✓; evolved 0 + 14 + 9 + 2 + 2 = 27 = 55.1% ✓; seed 22 = 44.9% ✓ (image) [Fig. 9b] [ours].
- Checks: Initial and Round 1 hold 30 of 49 (61.2%), a majority ✓; after Initial, 27 of 35 picks (77.1%) are evolved ideas ✓ [Fig. 9b] [ours].
- Sample: the 49 ICML successes; the loop stops at four successes [App. A.2], so later rounds hold fewer tasks, and per-round counts mix idea quality with the number of tasks still running [ours].
- Assessment [ours]: consistent; with one seed and one evolved candidate per round [App. A.2], 77% evolved picks after the first round is a real preference of the Selector, an LLM agent that "compares performance metrics and execution logs" [§3.3] (tex:sections/3_new_method.tex:90) (engine side: analysis.md, SEL).

### C-ABLX-3 · The rebuttal loop raises SP scores (Tab. 5)

- Claim: "this rebuttal procedure effectively addresses the weaknesses flagged by ScholarPeer" [§4.2 "Effectiveness of the Rebuttal Agent"] (tex:sections/4_experiment.tex:33).
- Values: SP rating 5.2 ± 2.2, 6.9 ± 1.6, 7.6 ± 1.0 and acceptance 46.9%, 79.6%, 93.9% for review rounds 0, 1, 2 [Tab. 5] (tex:tables/ablation_rebuttal.tex:12-14).
- Checks: 23, 39 and 46 of 49 papers ✓; the round-2 row equals Tab. 3's ICML row (7.6 ± 1.0, 93.9, 5.7 ± 0.6, 69.4), so the ablation reuses the main run [inferred] [Tab. 3].
- Assessment [ours]: the loop stops when SP reaches 8 [App. A.2], so rising SP scores are the optimization target, not independent evidence; the paper grants it ("it is not surprising") [§4.2] (tex:sections/4_experiment.tex:34).

### C-ABLX-4 · ... and SAR acceptance, "particularly pronounced in the first review round" (Tab. 5)

- Claim: "incorporating ScholarPeer reviews also improves acceptance rate from Stanford Agentic Reviewer, with this effect being particularly pronounced in the first review round" [§4.2] (tex:sections/4_experiment.tex:34).
- Values: SAR 5.6 ± 0.5 with 49.0%, 5.8 ± 0.6 with 73.5%, 5.7 ± 0.6 with 69.4% for rounds 0, 1, 2 [Tab. 5] (tex:tables/ablation_rebuttal.tex:12-14).
- Checks: 24, 36 and 34 of 49 papers; round 0 → 1 gains 12 papers, round 1 → 2 loses 2 papers and 0.1 rating points, and even if only those two papers changed, the exact McNemar p is 0.50, rising with more discordant pairs (0.625 at 3 against 1) [Tab. 5] [ours]; the table bolds round 1 as the best SAR result (tex:tables/ablation_rebuttal.tex:13).
- Falsified by: repeated SAR queries showing the round-1 to round-2 difference is query noise, or a larger sample reversing it [ours].
- Assessment [ours]: round 1 transfers to the held-out reviewer; round 2 shows no held-out gain (36 → 34 of 49; exact McNemar p ≥ 0.50) while lifting SP to 93.9%; the shipped two-round setting is the one that maximizes the in-loop reviewer, and the round semantics are ambiguous (A-EVAL-5).

### C-ABLX-5 · Initial drafts already beat ScientistOne (Tab. 5)

- Claim: "even without the Rebuttal Agent, ScientistTwo produces initial drafts of significantly higher quality than the prior state-of-the-art baseline, ScientistOne", "achieving a nearly 50% acceptance rate when evaluated by both ScholarPeer and Stanford Agentic Reviewer" [§4.2] (tex:sections/4_experiment.tex:35).
- Values: round 0 SP 5.2 ± 2.2 with 46.9% (23/49) and SAR 5.6 ± 0.5 with 49.0% (24/49), against ScientistOne's 3.8 ± 1.2 with 14.3% (3/21) and 4.1 ± 0.7 with 0.0% [Tab. 5] (tex:tables/ablation_rebuttal.tex:11-12).
- Checks: "nearly 50%" ✓; Welch statistics from the printed values, 1.4 / 0.41 = 3.4 (SP) and 1.5 / 0.17 = 8.9 (SAR) [Tab. 5] [ours]; no test is reported, so "significantly" is untested [ours].
- Assessment [ours]: the ScientistOne row is Tab. 2's, 21 papers on ScientistOne's own tasks, while S2's drafts are for its 49 successful tasks; the comparison crosses task pools.

### C-ABLX-6 · Review-driven refinement: FCD-Engram beats LFR-Engram (Tab. 6)

- Claim: S2 "synthesized FCD-Engram, which consistently outperforms LFR-Engram", and "This case study demonstrates that review-driven refinement is essential for producing more novel, high-impact research ideas" [§4.2 "Effectiveness of Review-Driven Idea Refinement"] (tex:sections/4_experiment.tex:38).
- Claim: before refinement S2 had "LFR-Engram, outperforming the human baseline Engram" [§4.2] (tex:sections/4_experiment.tex:38).
- Values: Overall 0.705 / 0.897 / 0.916, Mem. 0.922 / 0.963 / 0.969, Util. 0.871 / 0.917 / 0.926, Priv. 0.495 / 0.824 / 0.860, EM (lower is better) 0.004 / 0.084 / 0.071, FQ −0.551 / −0.014 / −0.001 for Engram, LFR and FCD [Tab. 6] (tex:tables/ablation_review_refine.tex:9-11).
- Sample: one task, AI Engram, an ICML 2026 Spotlight [Tab. 14] [Bib: kwon2026ai]; TOFU forget10 with Llama-3.2-1B-Instruct [Tab. 6]; one run, no variance.
- Checks: FCD beats LFR on all six columns ✓ [Tab. 6]; both are worse than Engram on EM (0.084 and 0.071 against 0.004, lower is better: FCD is worse by +0.067, a ratio of 15.7–20.4 within rounding), so "outperforming" holds on 5 of 6 columns [ours]; on Overall, LFR gains 27.2% and FCD 29.9% [ours].
- Falsified by: the across-task rate at which meta-review refinement improves results [ours].
- Assessment [ours]: n = 1 cannot show "essential"; the paper never reports how often the meta-reviewer returned `Refine`, or how often the refined idea was kept, across the 49 tasks.

### C-ABLX-7 · All four integrity audits passed (Tab. 7)

- Claim: S2 "faithfully passes all four audits; removing these refinement agents leads to sporadic audit failures" [§4.2 "CoE Integrity Audit"] (tex:sections/4_experiment.tex:43); a footnote adds that S2 "successfully completes an additional task without a refinement agent for specification compliance", whose codebase "contains reward hacking" [fn. 2] (tex:sections/4_experiment.tex:43).
- Values, rows without agents / with the specification agent / with specification and reference agents / with all three: Score Verif. 50/50, 49/49, 49/49, 49/49; Spec. Violat. 1/50, 0/49, 0/49, 0/49; Ref. Verif. 19/1840, 19/1817, 0/1814, 0/1814; Method-Code 39/50, 38/49, 38/49, 49/49 [Tab. 7] (tex:tables/ablation_audit.tex:11-14).
- Sample: the ICML successes, 49, or 50 without the specification filter [Tab. 7]; auditor unspecified (U-EVAL-5); one run.
- Checks: the footnote's extra task explains 50 → 49 and the single violation ✓; 1840 − 1817 = 23 references belonged to the removed paper, none hallucinated (19 stays 19) ✓; reference correction leaves 3 fewer references (1817 → 1814) [Tab. 7] [ours].
- Checks: method–code alignment goes 39/50 → 38/49 (the removed paper was aligned) → 49/49, so the last agent fixed 11 papers; about 37 references per paper [Tab. 7] [ours].
- Falsified by: an independent re-audit of the 49 repositories finding a violation [ours].
- What Score Verif. shows (F-CL-11) [ours]: Tab. 7's first row passes a reward-hacked codebase, 50/50 on Score Verif. with 1/50 specification violations, the codebase that "contains reward hacking" [fn. 2] (tex:sections/4_experiment.tex:43); so the check, as run, shows the code is deterministic, not that its number is valid [Tab. 7].
- The delegated protocol re-runs on a fixed evaluator: ScientistOne's I1 compares with "scores obtained by re-running the submitted solution on the golden evaluator" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:25-26); ScientistTwo's tasks name no such evaluator (U-EVAL-5).
- Assessment [ours]: internally consistent, but a check of determinism rather than validity (above); whether the variants are separate runs or stages switched off in one run is not said; it covers 49 of 86 successes; and the pipeline's own fix uses "the Coding Agent audits the repository against the manuscript" [§4.2] (tex:sections/4_experiment.tex:43), so if Tab. 7's auditor is the same kind of agent, 49/49 is in-distribution.

### C-ABLX-8 · Another coding agent still works (Tab. 8)

- Claim: S2 "remains capable of generating state-of-the-art methods across different coding agents", and "the codebases generated by Antigravity remain fully reproducible, exhibit no specification violations, and faithfully align with the designs proposed by ScientistTwo" [§4.2 "Generalizability Across Coding Agents"] (tex:sections/4_experiment.tex:46).
- Values: Claude Code SR 80.0, gain 3.8, SP 7.0 ± 1.2 with 100.0, SAR 5.4 ± 0.2 with 75.0; Antigravity SR 60.0, gain 16.7, SP 6.3 ± 1.5 with 66.7, SAR 4.8 ± 1.0 with 66.7 [Tab. 8] (tex:tables/antigravity.tex:11-12).
- Sample: 5 ICLR 2026 tasks, with 4 and 3 successes; Antigravity is powered by Gemini 3.8 Flash [Tab. 8] (tex:tables/antigravity.tex:3), while the rest of the engine runs Gemini 3.6 Flash [App. A.2].
- Checks: 4/5, 3/5, 2/3 and 2/3 ✓; the Claude Code row equals Tab. 3's ICLR row and Tab. 4's ICLR gain (3.8), so it is the main run [inferred] [Tab. 3] [Tab. 4]; no table backs the audit claims for Antigravity [ours].
- Assessment [ours]: n = 3–5; Antigravity is lower on 5 of 6 columns and higher only on gain (16.7 against 3.8), which with 3 successes may be one task; the Gemini version also differs, so this is not a pure swap of the coding agent.
