# Review: research-engineer, wave 1 (2026-09-27)

- **Reviewed:** `docs/paper/claims.md` with `claims/`, `note-check.md`, `artifacts.md`, at commit
  `734797a`.
- **Lens:** can a number be trusted and reproduced.
- **Record:** the reviewer's final message, verbatim below, with one change: its last line named the scripts by an absolute scratchpad path, shortened here to file names, because this
  repository never holds a path from someone's machine. Its three scripts are kept under
  `playground/paper/reviews/research-engineer/`.

---

**Review: claims.md + claims/*.md, note-check.md, artifacts.md. Research-engineer lens, 2026-09-27, paper v1**

I found no BLOCKER. I re-ran every load-bearing check with my own scripts, and these all hold:
- the SD bounds (1.37 and 1.51);
- the implied ICML mean of 34.56% (34.43–34.68);
- the Tab. 3 pooled ratings, 7.457 and 5.648 against 6.647 and 5.845. The SAR reversal survives rounding: at most 5.698 against at least 5.795;
- the Tab. 5 counts, 23/39/46 and 24/36/34, each the only count that rounds to its printed rate;
- the cost arithmetic: $402,855, 268.6 days and the stage dollars;
- the Fig. 9 and Fig. 10 labels, which match the images.

The citation checker passes, and note-check's summary counts match its 125 rows.

**MAJOR**

1. **claims.md, A-EVAL-3, finding 1, C-MAIN-1: only 2 of 11 ScholarPeer rows are used, and the decisive row is missed.**
   - S2 ICLR is 100.0% accepted at a mean of 7.0 [Tab. 3]. Under "rating ≥ 8" that is impossible, with no SD argument needed.
   - Under ≥ 8, the minimum SD beats the printed SD on 10 of 11 rows. Examples: human NeurIPS 2.43 against < 1.95; round 0 2.59 against < 2.25; Antigravity 2.33 against < 1.55.
   - P-EVAL-4's own check implies one integer score per paper with the sample SD. (With the population SD, three rows have no integer solution.) Under that model exactly one threshold fits every row: **≥ 6**. Antigravity's 6.3 ± 1.5 with 2 of 3 accepted forces the ratings {5, 6, 8} [Tab. 8], and S2 ICLR forces {6, 6, 8, 8}.
   - Caveat: if SP averages several reviews and accepts by majority, none of this holds. So "cannot mean ≥ 8" needs that condition stated.
   - Fix: add these rows, record "consistent only with ≥ 6 [inferred]", and keep the §3.5-vs-tables item INCONSISTENT.

2. **claims.md C-HEAD-1, C-HEAD-2, C-MAIN-8, P-EVAL-2: none of them says the gains and the success count are measured on the data the search selected on.**
   - A search for "validation" finds nothing in any claims file.
   - Each task picks among about 8–10 candidates, then passes two "strictly better" gates [§3.4] [§3.6], all on the full benchmark (U-NOTE-1, U-ART-5).
   - So 25.2% and 80.4% carry winner's-curse inflation that cannot be sized, because no run-to-run variance is reported.
   - Fix: say so in each assessment and link the two gaps. Decision for task 6: a held-out test set, plus a null-idea control to measure the false-success rate.

3. **note-check special case C contradicts claims C-ABLX-1.**
   - Fig. 9b plots five rounds (Initial, then Rounds 1–4, with 4 ideas selected in Round 4). C-ABLX-1 reads this as A-NOTE-8's reading 1.
   - Special case C assumes reading 2 (8 ideas), so its "upper bound" of 87 is not an upper bound. With two seeds in round 0 it is 87 + 4·N_t, which is 99 for N_t = 3.
   - Fix: redo the count. It feeds task 5's billing decision.

4. **Missing check (C-MAIN-8, C-APPB-6): AutoSOTA's ICLR cells were rebuilt from Tab. 16, but S2's were not.**
   - Tab. 16 gives S2's DMSQD at +0.61% and T-SAE at +3.4%. For Tab. 4's S2 median of 2.2 and mean of 3.8, the two unprinted gains must be 0.9–1.1% and 9.9–10.5%.
   - Pinet's printed results (RS −69%, 3.0× faster training, the CV drop) contain nothing near 10%.
   - So S2's ICLR gains cannot be rebuilt from the paper.

5. **artifacts P-ART-3 and P-ART-4 do not say where the gain comes from.**
   - With every other new component held fixed, the ablation's "Trace-only (X-Maha)" row scores 99.52/2.46, against 99.56/2.17 for the full method [p. 44] (image).
   - The refined idea's headline weighting therefore carries 0.29 of the 2.00 pp FPR95 gain over the reproduced baseline's 4.17 [p. 41].
   - The additive table worsens the average with each of the first two components (4.17 → 4.28 → 4.48), yet the text says "Every component contributes" [p. 41] (image). No critic verdict follows.
   - This is the paper's only ablation with numbers. Use it in the ablation critic's contract.

**MINOR**

6. **Question 4a, artifacts key findings and U-ART-5: the test-set reading is right in substance.** The critic steers the redesign with OOD test numbers (CIFAR-10 96.83 → 88.02) [p. 46], and the auditor calls them "test features" [p. 47]. Two corrections:
   - "The ablation's best setting is not the shipped one" argues the other way: γ stayed at 2.0 rather than the test-best 3.0.
   - DynaSpec-RAG's "grid search ... on validation splits" [p. 61] is correct practice.

   Rest the finding on the critic-to-redesign loop. Also add to U-ART-4: round 0 ran on CIFAR-100-LT [p. 46], but the "FULL" report covers balanced CIFAR-100 only [p. 40].
7. **Questions 4b and 4c.**
   - 4b: score verification is read correctly [p. 47]. But it is one audit (n = 1), of a NeurIPS task outside Tab. 7's sample. A bit-exact re-run of deterministic post-hoc scoring shows where the numbers came from, not that they are robust. A-ART-3 should be AMBIGUOUS, not INCONSISTENT.
   - 4c: "no variance" is confirmed. The text layer of pp. 56–71 includes the tables and has no ± value, seed or run count.
8. **A-EVAL-6 is not INCONSISTENT.** The two numbers are measured at different points in the pipeline. §3.4 and §3.6 replace the best idea only when the new one is "strictly" better, which predicts Tab. 4 ≥ Fig. 9a. That is the gap observed: +1.0 to +1.3 points.
9. **C-ABLX-4 and finding 2: "round 2 lowers SAR acceptance" rests on a net change of −2 of 49.** Even if only those two papers changed, the exact McNemar p is 0.50. Say "no held-out gain" instead.
10. **C-ABLX-2: "not of the metric" is unsupported.** The Selector "compares performance metrics" [§3.3].
11. **C-DISC-2: Seed Idea Generation has no printed label.** The printed labels sum to 99.4% (time) and 99.8% (cost), so the residuals are 0.6% and 0.2%, not 0.3%. "Sums to 100.1% ✓" checks a value the figure never prints.
12. **C-ABLX-6: "17.75×" is false precision.** Rounding of the printed values allows 15.7–20.4. Report the absolute difference, +0.067.
13. **C-DISC-4 and C-HEAD-8 use different gain conventions.** C-DISC-4 compounds the gains as ratios (31.5%). C-HEAD-8 reads them as time reductions, which compound to 26.1% (a 1.35× speedup). State both.

**What task 5 still needs from the paper**
- **Targets for the ICLR test set:** the paper gives none that can be reproduced (item 4). Baselines exist only as AutoSOTA's own reproductions: TeCh 0.8431, RALI 0.7803 on one split, T-SAE 0.7586. Task specs need our own baselines, 5 or more seeds, and a tolerance. The one reproduction shown fell 0.41 pp FPR95 short, which is 21% of the gain claimed against it [p. 42].
- **Statistical power:** 4 successes of 5 has a 95% interval of 28–99%. Five tasks can compare per-task gains over seeds, not success rates.
- **Cost:** the $3765 covers the 33 NeurIPS successes, with no token/VM split, prices or hardware.
  - Per success it is at least $3,765, or about $4.3–4.7k if a failed run costs as much as a successful one [ours].
  - There is no figure for the ICLR tasks, so cost must be measured on our first task.
  - The paper supports only the stage shares, the 2.51-day mean wall-clock, and 16–99 coding sessions per task.
- **Billing:** the paper gives no token counts.
- **Task definitions:** the paper defines no subset, full set, per-task metric and direction, gain rule or seed policy. The one run shown used seed 0 on a single checkpoint, so we must measure the noise floor ourselves.

**Scripts behind my numbers** (in the session scratchpad, not in the repo; they should move to `playground/paper/`): `sp_threshold.py`, `sp_integer.py` and `s2_iclr.py`.
