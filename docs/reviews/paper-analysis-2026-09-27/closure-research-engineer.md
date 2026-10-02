# Closure check: research engineer (2026-09-28)

- **Checked:** whether each finding of the research-engineer reviews RE1 and RE2 is resolved by
  its fix, and whether the reviewer accepts the two points not applied as written.
- **Scope:** the reviewer's own findings, with its arithmetic re-derived.
- **Record:** the reviewer's final message, verbatim below.

---

**Closure check of RE1 and RE2 (research engineer), 2026-09-28**

**RE1**

| Finding → fix | Status | Where | What remains |
|---|---|---|---|
| M1 → F-CL-1 | RESOLVED | claims.md:34, :363; claims/main-results.md:14 | The count leans on one knife-edge row. S2 NeurIPS counts as ruling out "≥ 8" at a population SD of 1.7502 against a printed "below 1.75". Under the sample SD, which claims.md:104 favours, the bound is 1.78; say so. |
| M2 → F-CL-2 | RESOLVED | claims.md:90; headline.md:15, :27; main-results.md:75 | — |
| M3 → F-NC-2, F-NC-3 | RESOLVED | note-check.md:198, :257–260, :333 | — |
| M4 → F-CL-3 | RESOLVED | main-results.md:75; appendix-b.md:44 | See error 2 below. |
| M5 → F-AR-1 | RESOLVED | artifacts.md:23, :101–102, :113 | — |
| m6 → F-AR-2, F-AR-3 | RESOLVED | artifacts.md:22, :238, :268 | — |
| m7 → F-AR-4 | PARTLY | artifacts.md:259 | Key finding 3 (artifacts.md:19) still states a single out-of-sample audit as general practice. Open it with "In the one audit shown (n = 1, a NeurIPS task outside Table 7's sample)". |
| m8 → F-CL-4 | RESOLVED | claims.md:41, :381; ablations.md:17 | — |
| m9 → F-CL-5 | RESOLVED | ablations.md:45 | — |
| m10 → F-CL-6 | RESOLVED | ablations.md:30 | — |
| m11 → F-CL-7 | Declined, and I accept | discussion.md:25 | Nothing: my finding was wrong. |
| m12 → F-CL-8 | RESOLVED | ablations.md:60 | — |
| m13 → F-CL-9 | RESOLVED | discussion.md:44; headline.md:73 | — |
| both → F-CL-13 | RESOLVED | claims.md:202 | — |

**RE2**

| Finding → fix | Status | Where | What remains |
|---|---|---|---|
| M1 → F-AN-1 | PARTLY | analysis.md:19, :274, :278, :288 | analysis.md:289 still says the paper computes gains "Only in evaluation", one line after the in-loop gains [p. 42]. Reword it: the paper applies a gain formula only in evaluation. |
| M2 → F-AN-15 | RESOLVED | analysis.md:23; stages/02:77, :85 | Reading 1 at stages/02:83 still says "no stage reproduces the baseline on the full set". Write "no §3 stage". |
| M3 → F-AN-3 | RESOLVED | analysis.md:517; one split line in every stage block | — |
| M4 → F-AN-16 | RESOLVED | stages/02:82 | Registering it is still pending under F-UN-1. |
| m5, m7 → F-AN-17 | PARTLY | analysis.md:477–482 | See error 1 below. |
| m6 → F-AN-18 | RESOLVED | analysis.md:327 | — |
| m8 → F-AN-19 | RESOLVED | stages/03:50; analysis.md:574 | — |
| m9 → F-AN-20 | RESOLVED | stages/02:79 | — |

**The two contested points: I accept both**
- **F-CL-7.** The crop from `fig10_seed_labels.py` shows "0.6%" and "0.3%" printed above the slice. My own crop started at 18% of the raster's height, below the label row (y 154–159 of 1174, about 13%). The six labels sum to 100.0% and 100.1%.
- **Floor of 17.** At N_0 = 1 with an end-of-round stop test, the floor is 1 + (4 × 2 + 1) + 5 = 15 sessions, or 17 with the 2 integrity sessions. With a stop test after each idea it is 16 (note-check.md:259).

**Errors a fix introduced**
1. **analysis.md:479 mixes two counting bases in "99 to 127".**
   - 99 is note-check's count, which includes 2 integrity sessions.
   - 127 is the table's 104, which counts none, plus 23.
   - On one basis the span is 97–127 without integrity sessions, or 99–129 with 2.
   - The error is mine (RE2 m5), and F-AN-17 copied it.
   - Paper location: App. A.2 (tex:sections/appendix.tex:155); §4.2 (tex:sections/4_experiment.tex:43).
2. **claims/appendix-b.md:45, "that leaves Pinet near 10%", does not follow.**
   - Suppose RALI's gain is its PLCC +0.006, which is 0.70–0.83%. Then no value of Pinet produces Tab. 4's median: sorting {0.61, RALI, 3.4, Pinet} gives a median of (RALI + 3.4)/2 = 2.05–2.12, which prints as 2.1, not 2.2.
   - A solution exists only if RALI's gain is 0.90–1.09% under a rule the paper does not print (for example SRCC +0.008 on a baseline near 0.8), with Pinet at 9.90–10.48%.
   - This strengthens the conclusion that S2's ICLR cells "cannot be rebuilt".
   - Paper location: [Tab. 4] (tex:tables/autosota_comparison.tex:13); [Tab. 16] (tex:sections/appendix.tex:320-322).

**Everything else re-derived holds:**
- the exact McNemar values 0.500, 0.625 and 0.688;
- EM +0.067, with a ratio of 15.7–20.4 within rounding;
- Table 9's chain at 26.1% and 31.5%;
- AUROC +0.26–0.40% against relative FPR95 42.3–48.0%, at least 105-fold apart;
- special case C's 27 + 6I + 4N_t, giving 81/87 and 93/99;
- 10–55 and 11–61 sessions for a task with no success;
- §9's 92 + 4N_t and 96 + 4N_t;
- about 6.5 ideas per task from Figure 10b;
- 0.29 of 2.00 pp, and 0.41 of 1.99 pp.
