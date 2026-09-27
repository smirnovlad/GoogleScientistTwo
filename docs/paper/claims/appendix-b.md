# Claims of Appendix B: the detailed AutoSOTA comparison, Tables 15–16 (C-APPB)

Part of [claims.md](../claims.md), which holds the definitions and gaps cited here [ours]. App. B runs S2 "on the same five ICLR 2026 submissions (Table 13) that AutoSOTA reports" [App. B] (tex:sections/appendix.tex:194-195); every number here concerns those five tasks, Pinet, DMSQD, TeCh, T-SAE and RALI [Tab. 16].

Revised 2026-09-27 after the persona review: fix F-CL-3 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md`; Codex review corrections on 2026-09-28, from `codex-review.md` in the same folder [ours].

**How the numbers were made.** Each side's delta "is self-reported by each system against its own reproduced baseline" [Tab. 16] (tex:sections/appendix.tex:263), "on different hardware" [App. B] (tex:sections/appendix.tex:202); none of the deltas carries a run count, and the two ± values do not say what they range over [ours].

### C-APPB-1 · Papers with a reported gain: 5/5 against 4/5 (Tab. 15)

- Claim: `Papers with a reported gain`, AutoSOTA 5/5 and S2 4/5 [Tab. 15] (tex:sections/appendix.tex:183).
- Checks: S2's 4/5 matches Tab. 3's ICLR `4/5` and Tab. 8's SR of 80.0 ✓ [Tab. 3] [Tab. 8]; the failure is TeCh, whose DMC-TeCh "was not accepted as a contribution" [Tab. 16] (tex:sections/appendix.tex:298-300).
- Assessment [ours]: consistent; it names 1 of the 21 failures (U-BENCH-3).

### C-APPB-2 · Configuration changes against new modules (Tab. 15)

- Claim: `Typical change` config against new modules, and `New algorithmic component` 0/5 against 4/4 [Tab. 15] (tex:sections/appendix.tex:184-185); "No new algorithmic component appears in any of the five, and the median change is under ten lines" [App. B "What gets optimized"] (tex:sections/appendix.tex:210-211).
- Checks: Tab. 16 counts 3 lines for Pinet, 1 for DMSQD and 1 for T-SAE, and none for TeCh or RALI, so the median of the known counts is at most 3 [Tab. 16] [ours]; the 4/4 counts only S2's four successes [Tab. 15].
- Assessment [ours]: whether a change is "algorithmic" is the authors' judgment; the denominators differ (5 against 4).

### C-APPB-3 · Evaluation protocol and full benchmark (Tab. 15)

- Claim: `Modifies the evaluation protocol` 1/5 against forbidden (audit); `Evaluated on the full benchmark` 0/5 against 4/4 [Tab. 15] (tex:sections/appendix.tex:186-187); S2 "evaluates on the paper's full benchmark grid rather than the single registered split" [App. B "Robustness and scope"] (tex:sections/appendix.tex:238-239).
- Checks: the 1/5 is T-SAE's harness edit [Tab. 16]; "on one split" is stated for RALI only (tex:sections/appendix.tex:318), and the evaluation scope of the other three AutoSOTA results is not given [Tab. 16] [ours].
- Assessment [ours]: "forbidden (audit)" points to the I2 audit described in App. B; no audit result is reported for these five tasks (U-EVAL-5).

### C-APPB-4 · Five or six ablations per paper (Tab. 15)

- Claim: `Component-level attribution`, AutoSOTA none against S2's 5–6 ablations per paper [Tab. 15] (tex:sections/appendix.tex:188).
- Assessment [ours]: not checkable; it is the only count the paper gives for the ablation plans N_p, which App. A.2 does not set (engine side: analysis.md, ABL) [App. A.2].

### C-APPB-5 · TeCh: +4.45% for AutoSOTA, a rejected variant for S2

- Claim: "AutoSOTA reports +4.45% accuracy from widening the backbone and adding label smoothing" [App. B "What counts as success"] (tex:sections/appendix.tex:220-221); S2's "DMC-TeCh variant beat the baseline on 5 of 6 metrics", but the ablation critic rejected it because "the gains were primarily driven by general training controls (EMA and label smoothing) rather than the multi-core architectural innovation itself" [App. B] (tex:sections/appendix.tex:221-224).
- Values: AutoSOTA's accuracy goes from 0.8431 to 0.8806 [Tab. 16] (tex:sections/appendix.tex:296-297).
- Checks: 0.8806 / 0.8431 = 1.0445, +4.45% ✓ [Tab. 16] [ours].
- Assessment [ours]: evidence that S2's ablation critic can veto a result that improves the metric, the attribution reading of success (A-EVAL-1); no table shows DMC-TeCh's numbers.

### C-APPB-6 · Pinet

- Claim: AutoSOTA's 3-line configuration change gives "Latency −16.7%; feasibility unreported" [Tab. 16] (tex:sections/appendix.tex:272-273).
- Claim: S2's ANSE, over the 4 DC3 sets, has "RS lower on 3/4 (up to −69%)", constraint violation from 4e−4 to 2e−14 on all four, and training 3.0 times faster [Tab. 16] (tex:sections/appendix.tex:274-277).
- Checks: none possible, since no baseline values are given [Tab. 16] [ours].
- Check (F-CL-3) [ours]: with Tab. 4's S2 ICLR median of 2.2 and mean of 3.8, and Tab. 16's two relative S2 gains, DMSQD +0.61% and T-SAE +3.4%, the two unprinted gains must be 0.90–1.09% and 9.90–10.48% (`claims_arithmetic.py` prints the two ranges; the reviewer's `s2_iclr.py` finds the same solutions, printed as one range per unknown) [Tab. 4] [Tab. 16].
- Which is which [inferred]: RALI's absolute PLCC +0.006 is 0.70–0.83% within rounding of 0.7803, the only RALI baseline printed (AutoSOTA's, on one split). At that value no Pinet gain fits Tab. 4: the median would be (RALI + 3.4)/2 = 2.05–2.12, not 2.2. A solution needs RALI at 0.90–1.09% under a rule the paper does not print (SRCC's +0.008 on a baseline near 0.8, for one) and Pinet at 9.90–10.48%, yet none of Pinet's printed results (RS up to −69%, CV 4e−4 → 2e−14, training 3.0× faster) is near 10% [Tab. 4] [Tab. 16].
- Assessment [ours]: S2's result is multi-metric with no single relative gain, the paper never says how Tab. 4's ICLR mean (3.8%) turned it into one number, and Tab. 4's S2 ICLR cells cannot be rebuilt from anything the paper prints (U-EVAL-1).

### C-APPB-7 · T-SAE

- Claim: AutoSOTA's "Score +2.25%, but the reported re-evaluation is 0.7557 < baseline 0.7586" [Tab. 16] (tex:sections/appendix.tex:307-308); its gain "does not survive its own re-run" (tex:sections/appendix.tex:312).
- Claim: S2's Sheaf-SAE "wins Semantics and Context probes on 3/3 suites for both models at matched FVE", at +3.4% ± 0.2 [Tab. 16] (tex:sections/appendix.tex:310-311).
- Checks: 0.7557 / 0.7586 − 1 = −0.38% [ours]; Tab. 4's AutoSOTA ICLR mean of 7.2 still counts T-SAE at +2.25% (C-MAIN-8) [Tab. 4].
- Assessment [ours]: what the ± 0.2 ranges over (seeds, suites or models) is not stated.

### C-APPB-8 · DMSQD

- Claim: AutoSOTA's change is "Config tuning, 1 line change, 1 iteration: emitters 15 → 20. QD score +7.3%, at +33% evaluations per iteration (unreported)" [Tab. 16] (tex:sections/appendix.tex:283-284).
- Claim: S2's LC-FTT, "Over the full 11-domain grid", reaches "up to +536 QD / +2.08pp coverage on 10D Sphere", "+422 QD / +1.16pp averaged", and "+0.61%±0.27 mean QD over reproduced DMS, reproduced bit-exact" [Tab. 16] (tex:sections/appendix.tex:286-289).
- Checks: 20 / 15 = 1.333, +33% evaluations ✓ [ours]; the text repeats "+422 QD / +1.16pp coverage averaged, reproduced bit-exact" [App. B "Complementarity"] (tex:sections/appendix.tex:247-248), matching the table ✓.
- Assessment [ours]: S2's mean QD gain (+0.61%) is small next to AutoSOTA's +7.3%, which costs 33% more evaluations; App. B presents the two as complementary.

### C-APPB-9 · RALI

- Claim: AutoSOTA's fusion-weight tuning gives "PLCC 0.7803 → 0.8012 (+2.68%) on one split" [Tab. 16] (tex:sections/appendix.tex:317-318).
- Claim: S2's DisCoRe-IQA, trained on KonIQ only and tested on "full splits of all 7 datasets (6 zero-shot): PLCC +0.006, SRCC +0.008", with "content probe 0.935 → 0.130; worst-region hit rate 0.899" [Tab. 16] (tex:sections/appendix.tex:320-322).
- Claim: "an earlier variant was rejected by our own critic as statistically inert" [Tab. 16] (tex:sections/appendix.tex:324-325).
- Checks: 0.8012 / 0.7803 = 1.0268, +2.68% ✓ [ours]; S2's PLCC +0.006 is absolute, about +0.8% relative if the baseline is near AutoSOTA's 0.78 [Tab. 16] [ours; the baseline level is our assumption].
- Assessment [ours]: "statistically inert" is a critic's verdict worded as a statistical one. No page shows a test, and the one run the appendices show in full uses seed=0, with Procrustes-DS reusing that single checkpoint (image) [p. 40]; so whether any critic runs a test is unknown, and so is which critic rejected the variant (artifacts.md A-ART-13; engine side: analysis.md, SUB and FULL) [Tab. 16] [§3.2].
- Withdrawn reading [ours]: this entry first said the phrase *implies a significance test inside the critic*; that went beyond the evidence, since the phrase shows only a critic's judgement, and analysis.md withdraws the same inference (Codex review) [Tab. 16].

### C-APPB-10 · "Not a head-to-head"

- Claim: "Because each system measures against its own reproduced baseline on different hardware, the two Δ columns are not a head-to-head on a common metric" [App. B] (tex:sections/appendix.tex:202); "the two columns optimize different metrics in three of five cases and are not a head-to-head" [Tab. 16] (tex:sections/appendix.tex:263-264).
- Checks: the metrics differ for Pinet (latency against RS, violation and training time), T-SAE (judge score against probes) and TeCh (accuracy against no accepted result), three of five ✓ [Tab. 16] [ours].
- Assessment [ours]: this contradicts the head-to-head framing of Tab. 4 and its "superior performance" (A-EVAL-7).
