# Record: `research-engineer` closure check (2026-10-02)

- **Reviewed:** the second version (`adc3484`) against this reviewer's own wave-1 findings.
- **Record:** the reviewer's final message, verbatim below, unchanged. Its scratchpad script `closure_checks.py` is kept, unchanged, in `playground/integrity/reviews/research-engineer/`.

---

# Closure check: research-engineer, second version at adc3484 (2026-10-02)

The second version fixes 16 of my 19 wave-1 findings. B1 holds. Two fixes are partial, and four new defects came in with the fixes; one of them, N1, is a MAJOR.

**What I checked:**
- I read the index, the four files in `docs/integrity/decisions/`, and `fix-list.md`, including sections 4 (A1–A6) and 5.
- The script the fix cites, `playground/integrity/reviews/research-engineer/null_control.py`, is byte-identical to the one I wrote. I re-ran it, and it gives the same result: search gain +2.647, report gain +1.322.
- I checked the second version's new statistics with `closure_checks.py`, a scratchpad script with fixed seeds. It should move to `playground/integrity/reviews/research-engineer/` beside the other two if the fixes cite it.
- No file edited, no git run.

## My findings

| Finding | Verdict | Where | Remaining |
|---|---|---|---|
| B1 · training-seed luck survives the test split | fixed | u-top-5: IR-10.2, IR-14.4, IR-15.1, the null control in §4; a-int-1: IR-23.2 | Nothing in the rules. See N3 for the control's prediction. |
| B2 · weights in the code tree have no provenance | partly fixed | u-int-4: IR-3.2 to IR-3.5, and the IR-3.3 control | IR-3.3's size bound applies per file, so weights split into many small text files (base64 chunks, or Python literals across modules) pass. The control plants only one file above the bound. This leaves the B2 attack open at MAJOR level. **Fix:** also bound the total size of a tree's content that is neither pinned nor job-produced, and plant the chunked variant. |
| M1 · null-idea control | fixed | u-top-5 §4 (R = 200, seeds 0–199, ±3 SE, m recorded, second control) | See N3. |
| M2 · success at the null is a coin flip | fixed | u-top-5 §7, row A-EVAL-1/U-EVAL-1; the second null control | Nothing. α and the test are task 6 `P1`'s, by design. I verified 0.05 + 3√(0.0475/1000) = 0.0707. |
| M3 · repeated runs | fixed | u-top-5: IR-18.1 to IR-18.6; index: IR-34.2, IR-33.4; the controls in both | Nothing. |
| M4 · I1 checks values, not gains | fixed | a-int-1: IR-23.3 to IR-23.6, IR-25.3 | IR-23.4 reads as the tolerance of one value. A paired gain carries the re-fit noise of both rows (√2 × σ_r per pair), so the rule should say so. |
| M5 · sealed baseline check unbounded | fixed | u-top-5: IR-15.2 to IR-15.7; index §7 | Nothing. |
| M6 · building the roles per kind of data | fixed | u-top-5: IR-19.1 to IR-19.6 | See N1. The fix to m1 now refuses tasks that IR-19 builds correctly. |
| M7 · C_base never scored | fixed | u-int-4: IR-4.3 (A5) and its control | Nothing. Power verified at 0.990 by simulation (200,000 draws), and P(at least 95 of 100 planted cases flagged) = 0.9994. |
| M8 · seeds and variance | fixed | u-int-4: IR-9.3, IR-9.4, IR-5.5, IR-8.2, IR-3.6 | See N2 for the IR-3.6 control's arithmetic. |
| M9 · missing costs | fixed | the cost tables of all four files | Nothing. I verified the arithmetic: 23 and 20.4 A100-hours; 102 at five re-fits; 2,970 calls per configuration × 11 configurations ≈ 33,000. I accept the owner's count (fix-list §5.7). |
| m1 · near-duplicates | fixed | u-top-5: IR-10.3 and its control | See N1. |
| m2 · parameters read from the code tree | fixed | u-int-4: IR-2.3 and its control | Nothing. |
| m3 · timing | partly fixed | u-int-4: IR-8.1 | The machine configuration is in. The repeat count is wrong by a factor of 2 (N4). |
| m4 · IR-31 intervals | fixed | a-int-3: IR-31.2, IR-31.3, the IR-31.6 control | Nothing. Bounds verified: 0/59 gives 0.0495, 0/99 0.0298, 0/299 0.0100, 1/97 0.048, 2/97 0.0635. For "below 0.5", 5/20 gives 0.456, 10/30 gives 0.4994 and 18/50 gives 0.486; one more miss in each crosses 0.5. |
| m5 · numbers without their sample | fixed | u-top-5 §8 ($3765 marked [inferred]); the 30.6-minute fit time, n = 1, everywhere it is used | Nothing. |
| m6 · rows missing from R7 | fixed | U-PEER-2, U-TOP-2 (u-top-5 §7); A-TOP-4, U-COST-1 (u-int-4 §6) | Nothing. |
| m7 · admissibility screen | fixed | index §8 | Nothing. |
| m8 · guard-off builds | fixed | index: IR-38 and its control | Nothing. |

## New defects the fixes introduced

### MAJOR

**N1 · u-top-5, IR-10.3: the near-duplicate check refuses tasks at scale, including across boundaries the protocol itself defines.**
- **Problem.** "The overlap between any two roles is zero ... by the manifest's near-duplicate detector, or the task is refused."
  - The detector's false-positive calibration accepts a threshold that flags up to "1% of 1,000 random pairs across roles". Admission, however, tests every pair across roles. A fit/report boundary of 50,000 × 10,000 items is 5×10⁸ pairs, so even a per-pair false-positive rate of 10⁻⁶ gives about 500 false flags, and the task is refused.
  - 1,000 random pairs cannot measure a per-pair rate below about 3×10⁻³: with zero flags, the one-sided 95% bound is 0.003.
  - The check also covers fit against report, the official train/test boundary. IR-19.2 lets a boundary the protocol defines keep its borders; IR-10.3 makes no such exception. An official split that contains near-duplicates would therefore refuse the task outright.
- **Fix.**
  1. A near-duplicate across a boundary that packaging built is removed from the role packaging built (search, or the carved part of report), with counts recorded. It never refuses the task.
  2. Across a boundary the protocol defines, flagged pairs are reported, optionally with a purged report scored beside the full one, and never refuse the task.
  3. Calibrate the threshold against the expected number of false flags over all cross-role pairs, or confirm each flagged pair with a stricter second check. Do not calibrate against a per-pair rate measured on 1,000 pairs.

### MINOR

**N2 · u-int-4, the IR-3.6 control: the pass bound assumes independent flags.**
- **Problem.** All 100 honest rows are compared against one estimate of the baseline's variance, so their flags are correlated. By simulation (20,000 replications, 5 seeds, q = 0.0626), the chance that 5 or more honest rows are flagged is 0.045, not the 0.0034 that the independent binomial gives. The control would fail about 1 time in 22 with a correct guard.
- **Fix.** Either give each honest row its own baseline draw, or set the bound from the shared-denominator distribution, also by simulation. Note the same overdispersion for the flag in production.

**N3 · u-top-5 §4, the null control's guard-removed arms: the predicted value rests on a single maximum over m identical candidates.**
- **Problem.** The engine's loop gates and selects in stages, so "m, the number of candidates the loop compares" is not defined for it. "Within its prediction ± 3 SE" can then fail with no fault in any guard.
- **Evidence.** In my one gated example (a subset gate, then the maximum of the survivors, m = 10), the deviation was only 0.017 (observed 0.504, formula 0.487), about 0.4 SE at R = 200. So this is a risk, not a demonstrated failure.
- **Fix.** Pass the guard-removed arms on "above 3 SE" alone, and record the formula's prediction as a diagnostic. The guarded arm's test (0 ± 3 SE) is the proof, and it is sound.

**N4 · u-int-4, IR-8.1: the repeat count resolves one row's mean, not a difference.**
- **Problem.** n = ⌈(3σ/δ)²⌉ makes 3·SE of a single mean equal to δ. The difference of two rows has √2 times that SE. At δ = σ this gives n = 9, where the difference needs 18: 3·SE(diff) is then 1.41σ against δ = σ.
- **Fix.** Either use n = ⌈2(3σ/δ)²⌉, or define σ as the standard deviation of the per-repeat difference between interleaved pairs.
