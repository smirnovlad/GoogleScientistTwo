# Record: `paper-analyst` closure check (2026-10-02)

- **Reviewed:** the second version (`adc3484`) against this reviewer's own wave-1 findings, and the statements the second version adds.
- **Record:** the reviewer's final message, verbatim below, unchanged.

---

# Closure check: paper-analyst, wave 1 → second version (adc3484)

Scope: my own wave-1 findings only, read against the index `docs/integrity/blocking-decisions.md` and the four files under `docs/integrity/decisions/`. I also checked the statements the second version adds, inside my lens.

## Verdict

**All 16 wave-1 findings and the R6 note are fixed. I found no new BLOCKER or MAJOR.** Three new MINOR defects remain, listed at the end.

## 1. My wave-1 findings

| Finding | Verdict | Where | Remaining |
|---|---|---|---|
| M1: A-INT-1's readings misattributed and quoted in part | fixed | a-int-1 §4 (first two WHY NOTs), §5 (readings 1–3, why INCONSISTENT stands, the delegated source) | none. Both roads not taken now argue against what §4.2 and App. B say. "both" is tied to the two failure modes, Table 15's "forbidden (audit)" is cited, §5 is quoted in full, and the reconciling reading is recorded. |
| M2: section 3.5 had no departures list | fixed | a-int-1 §5 "Where we depart"; IR-21 with IR-21.1 and IR-21.6; U-INT-1 row | none. G2's branch (discard by default), G4's detector, G3, the hooks, IR-24, IR-25 and P-INT-1 are all listed. IR-21 and section 6 now agree. |
| M3: IR-22 claimed I1 "as defined" while IR-23 widened it | fixed | IR-22.2, IR-23 (header), IR-23.6, a-int-1 §5, U-NOTE-4 row | none |
| M4: §5's native provenance check was left out | fixed | IR-22.5, a-int-1 §2 (audit of the final artifact alone), a-int-1 §5 (the fifth number) | none. It is called a precedent, not a specification. I verified §6.2 = `06f_native_cpr.tex` and line 48. |
| M5: departures missing in 1.5 and 2.6 | fixed | u-int-4 §5 (IR-7, external weights); u-top-5 §6 (IR-11 and IR-13, the tail, report re-fits, rebuttal data) | none |
| M6: p. 44's γ revived as evidence of an attack | fixed | u-top-5 §3, moved under "Steering the search on the reported data" with F-AR-2's verdict | none |
| m1: the cherry-picking writer was not ScientistOne's | fixed | u-top-5 §3 and §5 | none. I verified 06b:39 and 06b:45. |
| m2: ScientistOne's reviewers corrected verdicts | fixed | IR-25.4; a-int-3 §5; a-int-1 §5 | none |
| m3: inferences and external facts written as the paper's | fixed | IR-27.4; a-int-3 §3 and §6 (second ambiguity, A-CFG-1); u-top-5 §3; a-int-1 §2; u-int-4 §2 | none |
| m4: "No task input provides an evaluator" | fixed | u-int-4 §5 | none |
| m5: p. 47 read too narrowly | fixed | u-int-4 §2 (both bullets); a-int-1 §2 | none |
| m6: I1's cost did not follow from p. 62 | fixed | a-int-1 §7; u-int-4 §7 | none. The admission line borrows the module's 30.6 min for E_base and says that App. D's baseline is frozen; that stand-in is disclosed. |
| m7: "Table 15's 4 ICLR tasks" | fixed | u-top-5 §8 | none |
| m8: evidence quoted by halves | fixed | u-int-4 §2 (p. 41 both halves, p. 42 both gains); u-top-5 §3 (p. 47 as reach, not steering) | none |
| m9: the paper's specification shown as ours | fixed | IR-21 table (G2, G4, G5 cite §4.2); IR-28 | none |
| m10: what the paper says next to the gap | fixed | u-top-5 §6 "What the paper shows next to the gap" | none. I verified p. 49's leakage check and p. 69's "(subset test split)". |
| R6: decision 2 hid the audit's read of report | fixed | u-top-5 §6, "confirmed, with three changes" | none |

## 2. New statements checked, inside my lens

**ScientistTwo, all confirmed:**
- **TeX quotes:**
  - App. B: "a threshold in the evaluation harness" (appendix.tex:208-209) and the TeCh "general training controls (EMA and label smoothing)" (223-224).
  - Table 16: DMSQD "+0.61%±0.27"; RALI "6 zero-shot"; Pinet "training 3.0× faster".
  - Table 13: TeCh's title, "Rethinking Transformers for Medical Time Series".
  - Table 3: NeurIPS "33/38".
  - §4: "Gemini 3.6 Flash and Claude Opus 4.8".
  - §3.6 line 140; §3.5 line 130.
- **Page facts:**
  - p. 3's text layer: "pinned to a single NUMA node, with Hyper-Threading (SMT), Turbo Boost, and Address Space Layout Randomization (ASLR) dis[abled]".
  - p. 40: seed=0, and the checkpoint is reused.
  - p. 51: TabPFN v2 is a vendor package.
  - pp. 61–62: T = 512 and L = 64.
  - pp. 69–71: seven ablation tables.
- **Arithmetic:** 40 fits × 30.6 min = 20.4 h, and 200 fits = 102 h.

**ScientistOne, all confirmed:**
- §4.3 line 7 (Ground "validates each tag deterministically").
- §6 lines 29 and 31 ("up to 3 attempts per run"; 16 runs retried).
- §6.2 `06f_native_cpr.tex`: line 12 ("within a 5% relative tolerance") and line 16 ("predominantly false positives of the extraction heuristic").
- App. E.1: lines 118 ("cannot be re-evaluated within the budget") and 127–129 (9 of 13 mismatches "within 5%").

**External sources.** I fetched each with curl from its own text and read the text directly:
- **TALENT** (arXiv source of 2407.00956v4, `JMLR/appendix.tex`, "Datasets Selection Details"): "often early-stopped using a separate validation set of real-world datasets" and "identified **27 datasets** that overlap with those in our 300-dataset benchmark". The paraphrase is faithful.
- **OpenOOD v1.5** (arXiv source of 2306.09301v5):
  - §3 (`3_evaluation_protocol.tex:23-24`): validation data is introduced instead of "determin[ing] hyperparameter values using test samples".
  - §4 (`4_benchmark_and_methods.tex:63,66,73,75`): CIFAR-10 holds out "1,000 samples from the test set to form" the ID validation set, and "Another 1,000 TIN images covering 20 categories are held out" as OOD validation, "disjoint with" the OOD test sets; CIFAR-100 does the same.
  - The paraphrase is faithful. See N1 for how IR-19.4 classes it.
- **Time-Series-Library** `data_provider/data_loader.py` (raw, current main):
  - ETT borders are 12 / 4 / 4 months of 30 days.
  - Each later block starts at `border − seq_len`.
  - `scaler.fit` runs on the training block only.
  - Prediction targets start at the border.
  - The paraphrase is faithful.

**Index section 8 (App. B's five tasks).** Every fact checks against Tables 13 and 16. TeCh's grouped and temporal roles are correctly left to task 5 as inference.

## 3. New defects

### BLOCKER
None.

### MAJOR
None.

### MINOR

**N1. IR-19.4 (u-top-5) calls OpenOOD "the model" under option (3a), but only its OOD validation is a disjoint source.**
- Evidence: its ID validation is a carve-out of the ID test set. "hold out 1,000 samples from the test set to form" the ID validation set, "while the remaining 9,000 test samples are taken as" the ID test set; for CIFAR-100, "We take 1,000 samples out of the ID test set" (`4_benchmark_and_methods.tex:63,73`). That is option (3b) for the ID part.
- Fix:
  - Say that OpenOOD pairs (3a) for OOD with (3b) for ID.
  - Apply IR-19.6's disclosure to the ID part: report holds 9,000 ID images against the published comparison on the full test set.

**N2. u-top-5 §3, "Training-seed luck carried to the test set", cites ScientistOne's value mismatches as training-seed evidence.**
- Evidence: ScientistOne's own words are "plausibly arise from unreported seed variance" (`012c_coe_audit_details.tex:127-129`). Those are ADRS solver tasks, which a-int-1 §7 itself describes as involving "no training".
- Fix: cite them as evidence that seed variance biases headlines in general, and let the training-seed claim rest on the null-control simulation.

**N3. u-top-5 §8 says "$3765 … tokens and machines with no breakdown".**
- Evidence: Figure 10(b) splits the cost per stage (image): Idea Refinement 45.4%, Initial Implements 20.1%, Peer & Meta-Review 15.8%, Ablation Studies 15.4%, Initial Drafting 3.1% [Fig. 10b]. What the paper lacks is the split between tokens and machines.
- Fix: say exactly that. Optionally, use Fig. 10(b)'s Peer & Meta-Review share to size IR-39's tail.
