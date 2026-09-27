# Control: the analysts' coverage against the orchestrator's independent reading

**What this is.** Before any analyst ran, the orchestrating session read every TeX file of
arXiv:2609.19644v1, Figures 9–10 as images, and the PDF/HTML numbering, and wrote 57 findings plus an
answer key for the initial note (`orchestrator-reading.md`, beside this file). It was kept out of the
repository until the analysts and reviewers had finished, so that it could not anchor them. This
file marks where the deliverables cover each finding.

**Result, 2026-09-27: 57 of 57 covered.** Every expected note verdict matched, with one difference
of labelling: the note's "Listing 1 covers every row of Table 1" was expected FALSE and is marked
PARTLY TRUE in note-check.md (N-79), because the paper itself asserts it (§3) while its stage
descriptions contradict it. The reasoning in N-79 is the same as expected.

## Coverage

| # | Finding (short) | Covered by |
|---|---|---|
| 1 | Listing 1's last refinement is never judged | A-TOP-2, A-NOTE-3 |
| 2 | Table 1 rows without a critic or a refine step | analysis.md §3.2; note-check.md special case B |
| 3 | verdict vocabularies differ by stage | analysis.md §3.2 table |
| 4 | exhaustion semantics differ from Listing 1 | A-TOP-1, A-NOTE-2 |
| 5 | seed loop stops on a count; novelty filter unclear; initial idea generator | U-SEED-1, A-SEED-1, A-SEED-2 |
| 6 | the full-set critic's reference | A-FULL-1, A-NOTE-5, U-ART-20, A-EVAL-2 |
| 7 | the full-set engineering limit | A-FULL-2, A-NOTE-9 |
| 8 | N_0 at round 0 | A-EVO-1, A-NOTE-8 |
| 9 | K = 4 refinement rounds after round 0 (Fig. 9 axis) | A-EVO-2 |
| 10 | S = 4 | analysis.md §6 (P-CFG-7) |
| 11 | 1..S−1 successes go to selection; 0 ends the run | analysis.md §4.3; U-EVO-4 |
| 12 | the Selector is an LLM judgement | U-SEL-1; analysis.md §4.2 |
| 13 | N_p unspecified; A_AblCrit notation; the missing reject verdict | U-ABL-1, A-TOP-5, A-ABL-1 |
| 14 | Result Comparison: strict rule or preference | A-ABL-3 |
| 15 | re-ablation after an update, once N_abl is spent | U-ABL-4 |
| 16 | threshold "e.g., 8"; s_new; what N_peer counts | A-TOP-5, A-PEER-1 |
| 17 | rebuttal code on C_best; the Enhancer on Claude Code | P-ROSTER-24; U-PEER-2; U-ART-15 |
| 18 | N_t unspecified | U-PEER-1 |
| 19 | meta-review: second pass, export at the limit | A-META-2, U-META-1, A-TOP-3 |
| 20 | "fails to outperform the baseline" means E_best | A-TOP-5 |
| 21 | integrity agents absent from §3 and Table 1 | stages/07-integrity.md; U-INT-1…3; A-INT-2, A-INT-3 |
| 22 | "structural" blocking versus a post-hoc audit | A-INT-1, A-NOTE-10, A-ART-2 |
| 23 | A.2's agent names do not match §3's | A-CFG-1, A-NOTE-6 |
| 24 | novelty from two Google Search results | U-SEED-2 |
| 25 | 16 limitation rounds | P-CFG-1 |
| 26 | what G is | A-TOP-4, U-TOP-1, U-BENCH-1 |
| 27 | the subset is never defined | U-BASE-1, U-NOTE-3, U-ART-4 |
| 28 | no validation/test separation | U-NOTE-1, U-ART-5 |
| 29 | gains parsed by an LLM | U-EVAL-1, U-NOTE-2 |
| 30 | "success" undefined | A-EVAL-1 |
| 31 | ScholarPeer both in the loop and reported | P-EVAL-7 |
| 32 | "Accept Rate" undefined, and not score ≥ 8 | A-EVAL-3 (with an SD bound, stronger than the orchestrator's argument) |
| 33 | AutoSOTA's overall pool differs | C-MAIN-8, U-EVAL-10, A-EVAL-7 |
| 34 | Fig. 9a 33.4% against the implied ICML mean | A-EVAL-6 |
| 35 | "majority" is a plurality | A-COST-1, A-NOTE-7 |
| 36 | cost sample, contents and prices | C-DISC-1…3; U-COST-1…3 |
| 37 | ablations conditioned on the 49 ICML successes | claims.md finding 8 |
| 38 | Table 5: in-loop up, held-out down in round 2 | C-ABLX-4; N-96 |
| 39 | Table 6: n = 1, EM worsens | C-ABLX-6 |
| 40 | Table 7 counts | C-ABLX-7 |
| 41 | Table 8: Gemini 3.8 Flash, n = 5 | A-CFG-2; C-ABLX-8 |
| 42 | Table 9's reviewer | A-EVAL-8 |
| 43 | Table 10's protocol | U-EVAL-6 |
| 44 | Table 2's baselines are their own public papers | U-EVAL-9 |
| 45 | Table 3: SAR accepts 96.9% of ICML spotlights | C-MAIN-6 |
| 46 | "consistently outperform" against 21 failures | C-HEAD-3 |
| 47 | 25.2% is a success-only mean; median 7.7% | C-HEAD-2 |
| 48 | Table 3's overall row is the weighted venue rows | claims_arithmetic.py |
| 49 | Appendix B's per-paper numbers | claims/appendix-b.md |
| 50 | "better" across several metrics is an LLM call | claims.md; stages/04-ablation.md; analysis.md §4.2 |
| 51 | RALI's "statistically inert" rejection | A-ART-4; claims/appendix-b.md; note-check.md |
| 52 | "consistently outperforms" undefined | stages/02-evaluating-ideas.md; claims/ablations.md |
| 53 | A_Coder may return a changed h | analysis.md §4 |
| 54 | A_FullEng reused in §3.4 and §3.6 | P-ROSTER-12 |
| 55 | the Evolver reads all traces | U-EVO-2 |
| 56 | iterative frontier expansion is outside §3 | analysis.md §2.1; C-DISC-4 |
| 57 | ICLR 2025 drafting format; ICLR grading scale | stages/05-drafting-peer-review.md; analysis.md |

## Found by the analysts, not by the orchestrator

- Figure 5 draws the baseline inside each idea's pipeline (A-BASE-1); Figure 7 sends a failed
  ablation comparison to drafting (A-ABL-2). Both checked against the images.
- A run can export a paper the meta-reviewer had just sent back (A-TOP-3).
- ScholarPeer's "Accept Rate" cannot be score ≥ 8, proved with an SD bound (A-EVAL-3).
- Under the held-out reviewer, human input papers are accepted more often than the generated ones
  (94/107 against 62/86).
- One gain is 10.9% in Figure 2 but 12.3% in its own paper; 1 − 1/1.123 = 10.95% (U-EVAL-1).
- Figure 1b holds exactly 86 bars and 21 empty slots (fig1b_bars.py).
- Every appendix artifact detail: the one-re-run reproducibility audit, the auditor's own
  alignment threshold, the rebuttal installing TabPFN, the generated paper's internal
  contradictions, the HTML dropping 23 of 38 pages (artifacts.md).
- The HTML's §3 sentence reads "Listing 4" while its caption reads "Figure 4".
- The only complete generated draft is 16 pages (N-51); how many tasks reached review round 2 is
  never stated (U-NOTE-6).
- The brief's claim that the paper numbers no equations was wrong; the checker mispaired short
  quotes and skipped `claims/`.

## After the persona review (2026-09-28): where the orchestrator's own reading was wrong

The control reading is kept as written. Two of its findings did not survive the review, and it
missed the review's blocker too:

- **Finding 2 stopped one step short.** It says the primitive "does not cover every row as
  written". That is true of Listing 1 as printed, and analysis.md's first version concluded the
  same, calling it "a family resemblance, not a contract". The architect's review (B1, fixed by
  F-AN-0) showed the conclusion that matters for the design: every way a stage departs from
  Listing 1 is a parameter value. So one primitive with per-stage parameters covers every row,
  and Listing 1 is one set of those parameters (analysis.md §3.4–3.5). Neither this reading nor
  the analysts reached it before the review.
- **Finding 36's "Seed ≈0.2 (by subtraction)" is wrong for cost.** The raster prints 0.6% (time)
  and 0.3% (cost) above that slice. The research-engineer review made the same subtraction and
  asked for the label to be dropped (F-CL-7). The claims analyst declined, with
  `playground/paper/fig10_seed_labels.py` as evidence.
- **Finding 34 is AMBIGUOUS, not a contradiction.** The 1.0–1.3 point gap between Figure 9a and
  Table 4 is the order the "strictly better" gates predict if the two numbers are measured at
  different points (F-CL-4).
