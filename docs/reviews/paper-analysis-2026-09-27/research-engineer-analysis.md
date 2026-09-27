# Review: research-engineer, wave 2, the engine analysis (2026-09-27)

- **Reviewed:** `docs/paper/analysis.md` and `docs/paper/stages/01-seed-ideas.md` to
  `07-integrity.md`, at commit `6c10e1f`. The same reviewer's wave-1 review is
  `research-engineer.md`.
- **Lens:** can a number be trusted and reproduced.
- **Record:** the reviewer's final message, verbatim below.

---

**Review 2: the engine analysis (analysis.md, stages/01–07). Research-engineer lens, 2026-09-27, paper v1**

**What holds:**
- Every App. A.2 value in §6 matches the paper (tex:sections/appendix.tex:155).
- The §9 arithmetic is right under its stated readings: 61 + 2(2N_p + 1) + 2(2N_t + 2) + 1 = 68 + 4N_p + 4N_t.
- It reconciles with note-check's special case C once that is corrected to ten ideas (87 + 4N_t at N_p = 6). The gap of N_p − 1 comes from two readings: §9 resets the ablation budget in the meta pass (+7) and counts zero integrity sessions (−2).
- A-EVO-2 now agrees with Fig. 9 and with my wave-1 count.

No BLOCKER.

**MAJOR**

1. **analysis.md §4.2, "No gain is computed inside the loop", and §1.1 item 2 are wrong as stated.**
   - The agents' own scripts compute gains, and the critics read them: "improves average FPR95 by 1.99pp over the reproduced X-Maha and 1.58pp over the paper" [p. 42] (image).
   - A critic judged a variant "statistically inert" (tex:sections/appendix.tex:324-325), so statistics are computed inside the loop.
   - The §4.2 table also settles two open gaps without saying so: A-ABL-3 ("strictly outperforms", tex:sections/3_new_method.tex:111) and A-FULL-1.
   - Fix: say "no gain formula is specified; the numbers every critic reads (E^h) come from agent-written code (U-ART-16)", and tag both rows with their gaps. This is exactly what task 6's locked harness must replace.

2. **stages/02 A-FULL-1 and A-BASE-1, and §1.1 item 6 ("The full-set critic's reference is never produced"), miss the one artifact that shows the reference.**
   - The idea's own full-set script recomputes the baseline: "X-Maha (reproduced)" is "recomputed by this same script" [p. 41] (image). It reports both references.
   - The reproduction is weaker than the published baseline (FPR95 4.17 against 3.76), so 0.41 of the claimed 1.99 pp gain comes from the reproduction, not the idea.
   - No stage file from 02 to 04 cites an Appendix C page.
   - Fix: cite p. 41 under both gaps, and link U-ART-20.

3. **No gap records which data split each decision reads.** Searching analysis.md and stages/ finds nothing.
   - The subset and full-set critics, the Selector (a maximum over the Good ideas) and both "strictly better" gates all read the benchmark that is then reported [§3.2–§3.6].
   - The artifacts show test sets steering a redesign [pp. 46–47].
   - U-NOTE-1 and U-ART-5 hold this gap, but the document that tasks 2 and 3 build from does not.
   - Fix: add U-TOP-5, and an "Inputs: split" line to every stage template.

4. **stages/02 P-SUB-3 has an unrecorded confound: the idea gets tuned, the baseline does not.**
   - `Engineer` means "hyperparameter tuning or code adjustments" for the idea only (tex:sections/3_new_method.tex:45), for up to two rounds.
   - E_base is produced once, with no refine step [Tab. 1].
   - The paper's own TeCh case shows the consequence: the gain came from "general training controls" (tex:sections/appendix.tex:223).
   - Fix: add U-SUB-2, tuning parity. The decision it forces: give the baseline an equal tuning budget, or run a tuned-baseline control.

**MINOR**

5. **§9 calls 68 + 4N_p + 4N_t an upper bound, but it sets φ = μ = 0**, although U-INT-1 allows a filter after every experiment.
   - At N_p = 6 and N_t = 3, the open readings span 99 (note-check's readings) to 127: a per-idea baseline adds 9, π = ρ = 1 adds 8, and U-ABL-2 adds 6. Integrity sessions come on top of that.
   - Fix: label it "excluding integrity sessions", and state the floor of 16 beside it.
6. **The §6 N_0 row's corroboration proves nothing.** "Round 0's selected ideas are all seeds" is true for any value of N_0.
7. **The §6 N_p row should add two more data points:** "full tables for all six ablations" [p. 11] (image), and DynaSpec-RAG's seven ablations [pp. 64–65]. At N_p = 7 the bound becomes 96 + 4N_t.
8. **A-EVO-1 is INCONSISTENT only under A-EVO-2's disfavoured reading.** Under reading 1, which the analysis itself favours, it is AMBIGUOUS.
9. **U-BASE-1 should cite the artifacts:** "FULL, 6 of 6" [p. 40] (image) and "(subset test split)" [p. 69]. Also record that the subset's false-negative rate (Good ideas pruned on the subset) is never measured.

**What task 5 still needs**
- **An expected session count, not only a ceiling.** Fig. 10b gives Idea Refinement 45.4% of cost against Initial Implements 20.1%, a ratio of 2.26. If Initial Implements is round 0 and every idea costs the same, that is about 6.5 ideas per task for N_0 = 2, against a ceiling of 10 [inferred]. This rests on the 33 NeurIPS successes only; failed tasks run every round.
- **Tokens and GPU-hours for each session type.** The paper gives none, so the §9 bound cannot be priced. Measure them on the first task.
- **Per task, fixed before any run:**
  - a subset inside the validation split, disjoint from test;
  - the harness's baseline over 5 or more seeds, with a tolerance;
  - both full-set references (published and reproduced);
  - the baseline's tuning budget.
- **Wall-clock per session.** A 2.51-day mean against about 100 sessions implies the runs were parallel (U-TOP-4).
