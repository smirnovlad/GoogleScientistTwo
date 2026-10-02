# Record: `paper-analyst` review, wave 1 (2026-10-02)

- **Reviewed:** `docs/integrity/blocking-decisions.md` at commit `a2e7eb0`, against its brief,
  `docs/integrity/README.md`.
- **Lens:** does the document say what the paper, and the source it delegates to, actually say?
  The brief named two reviewers, `research-engineer` and `system-architect`; the coordinator added
  this third lens for the document's statements about the paper.
- **Record:** the reviewer's final message, verbatim below, unchanged.

---

# Review: `docs/integrity/blocking-decisions.md` at a2e7eb0, paper-fidelity lens (paper-analyst)

## 1. Verdict

The document is fit for task 3 once the MAJOR findings are fixed; this lens finds no blocker. Every quote is verbatim and correctly located. I opened every cited image page and each fact holds (pp. 3, 40–51, 61, 62, 66–68). The defects are in framing and in departures the document never names:
- **Section 3.4** gives §4.2 and Appendix B positions that neither of them takes.
- **Section 3.5** has no list of departures.
- **IR-22** applies ScientistOne's §5 "as defined", while **IR-23** widens I1's scope.
- **Section 2.3** brings back a reading of p. 44 that task 1 withdrew.

## 2. Requirements

**R5: partly met.**
- The acceptance test passes. I re-ran the checker myself: "1 file(s) checked, 0 problem(s)".
- Each decision has a classification with quotes, and A-INT-1's resolution is marked `[ours]`.
- The content falls short in four ways:
  - section 3.5 has no "Where we depart" list (M2);
  - sections 1.5 and 2.6 leave out departures (M5);
  - A-INT-1's reading 2 is quoted incompletely (M1);
  - several inferences are written as the paper's statements (m3).
- The classifications:
  - **U-INT-4 UNSPECIFIED:** right. §3.2 does specify that the coding agents produce E, and section 1.5 correctly lists that as a departure.
  - **U-TOP-5 UNSPECIFIED:** right.
  - **A-INT-3 AMBIGUOUS:** right, but a second ambiguity should be added: App. A.2's model routing (m3).
  - **A-INT-1 INCONSISTENT:** defensible, but a reading that reconciles the two places is not recorded (M1e).

**R6: partly met.**
- All four proposals are paraphrased (not quoted). The paraphrases match `docs/paper/unspecified.md` lines 179–182, and each proposal is confirmed or replaced with a reason.
- One change goes unstated. Section 2.6 names IR-15 as decision 2's only change. But IR-14 also allows "the audit re-run (IR-23)" as a job that reads the report split after export. The proposal ("the test set is scored once, at the end") does not allow that job.

## 3. Findings

### BLOCKER

None. Each misframed item below sits in a road not taken, an evidence line or a cost. Every rule involved also rests on correct evidence.

### MAJOR

**M1. Sections 3.4 and 3.5, A-INT-1: the paper's positions are misattributed and quoted incompletely.**

(a) **"⛔ WHY NOT a post-hoc audit only, as §4.2 reads".**
- §4.2 is not post-hoc only. It adds in-run agents and leaves only I1 to a prompt: "To guarantee these properties, we introduce three dedicated refinement agents alongside careful agent prompt design" and "a validation filter that uses the Coding Agent to detect and discard rule-violating solutions immediately after experimentation" [§4.2] (tex:sections/4_experiment.tex:43).
- The bullet's own counter-example is the variant run *without* §4.2's filter.
- Section 3.5 itself says "§4.2's in-loop agents become the gates G2, G4 and G5".

(b) **"⛔ WHY NOT gates only, as Appendix B reads".**
- Appendix B never says "gates only", and it does not dispute Table 7's post-hoc audit.
- Its claim covers two named failure modes, and the document's quote never says what "both" refers to: "Optimizing a single registered number exposes two classic failure modes" … "ScientistTwo instead blocks both structurally, via a reproduction re-run (I1), a protocol-immutability audit (I2), and a method--code alignment audit (I4) rather than a prompt-level list of prohibitions, and evaluates on the paper's full benchmark grid rather than the single registered split" [App. B] (tex:sections/appendix.tex:229-239).

(c) **Reading 2 leaves out Table 15.** The brief asks for it, and `note-check.md` A-NOTE-10 already cites it: "Modifies the evaluation protocol | 1/5 | forbidden (audit)" [Tab. 15] (tex:sections/appendix.tex:186).

(d) **"The delegated source sides with reading 1, for the audit" drops the half of the sentence that leaves room for reading 2:** "While the CoE framework can support other evaluation forms---real-time verification during paper production or broader claim coverage---those are outside the scope of this work." [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:18).

(e) **A reconciling reading is not recorded.**
- In Appendix B, "blocks", Table 16's "make this class of edit inadmissible" and Table 15's "forbidden (audit)" can all describe the post-hoc audit's verdict. Under that reading the two places agree, and Appendix B merely overstates.
- INCONSISTENT can still stand, but the document should say why. For I1, §4.2 relies on a prompt, "ensuring full reproducibility without requiring additional post-hoc refinement". Appendix B instead credits "a reproduction re-run (I1) … rather than a prompt-level list of prohibitions".

**Fix.**
- Rewrite the first WHY NOT against what §4.2 actually does: a prompt for I1, and no re-run inside the run.
- Rewrite the second against Appendix B's actual claim: the audits block evaluator tampering and unmeasured trade-offs.
- Quote Table 15 and say what "both" refers to.
- Quote §5's sentence in full.
- Record the third reading and the reason INCONSISTENT stands.

**M2. Section 3.5 has no "Where we depart" list.** Sections 1.5, 2.6 and 4.6 each have one. As a result, decision 3's departures from §4.2 are never named:
- **G2's failure branch.**
  - Paper: "detect and discard rule-violating solutions" [§4.2] (tex:sections/4_experiment.tex:43).
  - Ours: the author gets the rule ID and retries (IR-27), and IR-21 says "when a bound is spent, the task ends without export". That ending also contradicts section 3.6's U-INT-1 row: "whether the idea becomes `Bad` or the task ends is task 2's".
- **G4's detector.**
  - Paper: "a search-augmented LLM identifies hallucinated citations, enabling the Writer Agent to ground and correct the bibliography using live search results" [§4.2].
  - Ours: API lookups, with an LLM only for near misses. This is ScientistOne's I3 used as an in-run gate, and the document should say so.
- **G3 is new and changes the writers.**
  - Paper: the Paper Enhancer works by "revising narrative claims and updating empirical tables and figures" [§3.5] (tex:sections/3_new_method.tex:130).
  - Ours: writers may no longer type a measured number.
- **No counterpart in the paper:** G1, G6, G7, IR-24's checks on the run's record of jobs and verdicts, and IR-25's way of counting integrity failures.
- **The reproducibility prompt (P-INT-1)** is never said to be kept or dropped: "the Coding Agent is prompted during the experimentation phase to output self-contained, reproducible scripts and execution instructions" [§4.2]. Either choice changes how the replicated agents behave.

**Fix:** add the list to section 3.5, one bullet per departure with its quote, and reconcile IR-21 with section 3.6.

**M3. IR-22 and IR-23: I1 is declared "as ScientistOne's §5 defines them", but its scope departs from the definition.**
- §5 checks one score: "The paper's reported score is extracted by LLMs from both \TeX{} and PDF files, then compared against scores obtained by re-running the submitted solution on the golden evaluator" (ref:2605.26340v1:sections/05_coe_audit.tex:25).
- IR-23 re-runs "the fit entry point of every reported row". That scope follows Table 7's caption ("every claimed results are reproducible", tex:tables/ablation_audit.tex:3), not the definition.
- The register records this exact scope question as open under U-NOTE-4 (A-ART-3).
- Reading "re-running the submitted solution" as a re-run of the fit step also settles a point `artifacts.md` U-ART-6 leaves open: "whether training is re-executed".
- The boundary with ScientistOne's §6 is kept: neither its five runs nor its max(1%, 3σ/|s̄|) tolerance is imported. The departure from §5 itself is what goes unmarked.
- Consequence: our "Score Verif." counts will not be comparable with Table 7's 49/49.

**Fix.**
- In IR-22, write "as §5 defines them, except I1's scope (IR-23)".
- In IR-23, mark the scope and the fit re-run as `[ours]`, resolving A-ART-3 and U-ART-6 for U-NOTE-4.
- List both in section 3.5's new departures list.
- Report a headline-only I1 count beside the every-row count.

**M4. Section 3.2 ("An audit that sees only the final artifact") and IR-24(c): the quote from the delegated definition stops one sentence before that definition's own provenance check.**
- IR-24(c) re-invents that check as ours. The next sentence of §5 reads: "For systems that emit structured provenance at write-time---linking each claim to a specific source record---an additional \emph{native} check becomes possible: the \textbf{numerical Claim Provenance Rate (CPR)}, which measures the fraction of quantitative claims in the paper that trace to a matching entry in the experimental log." (ref:2605.26340v1:sections/05_coe_audit.tex:48).
- ScientistOne reports CPR separately from the four checks (`sections/06f_native_cpr.tex` in its source).
- ScientistTwo's TeX never mentions provenance; a grep finds no match. It requires its papers to be verifiable "across all four dimensions" [§4.2] (tex:sections/4_experiment.tex:41).

**Fix.**
- Cite §5's native check as specified by reference, and as the precedent for IR-24(c) and G3.
- Report it as a fifth, native number beside the four checks, so that the four stay comparable with Table 7.
- Keep the quote about the four checks for what the native check also misses: the intermediate steering, covered by IR-24 (a), (b), (d), (e) and (f).

**M5. Sections 1.5 and 2.6: three rules change behaviour the paper specifies, and neither "Where we depart" list names them.**
- **IR-7** puts a numeric precondition under every performance gate, and lets the LLM only be stricter. The paper gives these decisions to LLM agents alone:
  - "If h consistently outperforms the baseline, it is approved for scale-up" [§3.2] (tex:sections/3_new_method.tex:44);
  - the update happens "if and only if" E_new "is preferred than" E_best "by the Result Comparison Agent" [§3.4] (tex:sections/3_new_method.tex:112);
  - the Ablation Critic judges whether the breakdown is clean [§3.4].
- **IR-11 and IR-13** give an agent session no data from the search or report splits, and no score.
  - In the paper, the coders run the benchmark and produce E themselves: "producing the resulting logs" [§3.2] (tex:sections/3_new_method.tex:40).
  - In the trace, the ablation agent swept eight layer-weighting variants (γ in {0.5, 1.0, 2.0, 3.0}) on the six OOD sets inside one plan [pp. 43–45] (image).
  - This changes every coding agent's working loop.
- **IR-17** adds a stage after the paper's last one. The paper exports at `Accept`: ScientistTwo "finalizes the process and exports the final improved paper and its codebase" [§3.6] (tex:sections/3_new_method.tex:140). We add the test event, the final fill, a text-only revision, and G3 to G5.
- **Also missing:** rebuttal data is limited to the task's manifest (section 2.2), whereas the paper's one rebuttal chose "50 representative TALENT datasets" and capped its test sets at 2000 [p. 51] (image). §3.5 is silent on data, so this departs from what the paper shows, not from its text. Say which.

**Fix:** add each departure, with its quote, to its section's list.

**M6. Section 2.3 ("Picking the best row after the fact") brings back a reading that task 1 withdrew.**
- The fact is right: γ = 3.0 scores 99.58 / 2.13, against the shipped γ = 2.0 at 99.56 / 2.17 [p. 44] (image).
- But the trace kept γ = 2.0, "the final.py default", calling it "among the strongest" [p. 45] (image).
- `artifacts.md` records task 1's verdict (its fix F-AR-2): "keeping γ at 2.0 shows the reverse for this parameter: the search saw the test sets, and did not pick γ on them".
- Placed under this attack, the line reads as evidence that ScientistTwo picked the best row. No rule rests on it alone, since the Sakana case carries the attack.

**Fix:** either drop the line, or keep it with its verdict ("the opportunity existed and was not taken; F-AR-2") under section 2.3's first attack, where it shows that the search saw the test sets.

### MINOR

**m1. Section 2.5: "as ScientistOne's cherry-picking writer did" names the wrong system.**
- The cherry-picking writer was Sakana AI-Scientist v2's, found by ScientistOne's audit: "Sakana ASv2 matches in 5/12 (42%)" … "First, cross-stage score cherry-picking (4 of 7 failures): the writeup LLM receives summaries from all four BFTS stages" (ref:2605.26340v1:sections/06b_integrity.tex:43-45).
- ScientistOne's own system "achieves perfect score verification (12/12)" (line 39).
- Section 2.3 has this right ("In ScientistOne's audit"); section 2.5 should use the same wording.

**m2. Section 4.5: "as ScientistOne's reviewers checked every flagged I1 to I3 case" implies the practice IR-25 adopts. ScientistOne did the opposite.**
- Its reviewers replaced the automated verdicts: "all flagged positives for I1 (Score Verification), I2 (Specification Violation), and I3 (Reference Verification) were manually reviewed and corrected by human reviewers before reporting" (ref:2605.26340v1:sections/012c_coe_audit_details.tex:54).
- IR-25 keeps a person's review "never in its place".
- Fix: write "unlike ScientistOne", and name it as a departure from its practice.

**m3. Inferences and external facts are written as the paper's.**
- **Which model backs the in-loop checker.**
  - The document says IR-27 "as §4.2 reads", section 4.3 "on the backend that writes the code", and section 4.5 "§4.2's routing to the coding backend is kept".
  - §4.2 only says Claude Code is used "whenever coding capabilities are required" (tex:sections/4_experiment.tex:46).
  - App. A.2 assigns "Gemini 3.6 Flash for all agents, except for" four named agents, and none of the four is an integrity agent (tex:sections/appendix.tex:155).
  - Task 1 marked this as inferred: `analysis.md` records P-ROSTER-26 and P-ROSTER-28 as "Claude Code by §4.2 [inferred]", and the register keeps A-CFG-1 AMBIGUOUS.
  - Under A-INT-3's reading 2, App. A.2's default would put the checker on a different model family.
  - Fix: mark it `[inferred]`, cite A-CFG-1, and add this ambiguity to section 4.6.
- **Section 2.3, "the critic steered the X-Mahalanobis redesign with an OOD set":** `artifacts.md` marks this `[inferred]`; so should this document.
- **Section 3.2, "the dropped CIFAR-100-LT setting":** that CIFAR-100-LT belongs to this task's benchmark comes from the X-Mahalanobis paper, an external source (`artifacts.md`, A-ART-12). Mark it as external.

**m4. Section 1.5: "No task input provides an evaluator" overstates.**
- The original codebases are part of the tasks: "whose problem specifications and codebases serve as benchmark tasks" [§4.1] (tex:sections/4_experiment.tex:16).
- The trace's metrics "come from the unmodified get_measures (train.py:160-171)" [p. 50] (image).
- The register's wording, "No fixed evaluator", is the accurate one.
- Fix: write "no stage names a fixed evaluator: the agent's script calls the codebase's metric code, picks the data and the baseline, and writes the report".

**m5. p. 47 is read too narrowly in two places.**
- **Section 1.2, "the reproducibility audit skipped it [the baseline]".**
  - The same page also says "CIFAR-100 ID top-1 = 92.95%, non-uniform Fisher weights, and the ablation table all match".
  - That table's first row is the baseline, 99.16 / 4.17 [p. 41] (image).
  - `artifacts.md` already records this contradiction within the page.
- **Section 3.2, "re-ran a scoring script over a saved checkpoint".**
  - This understates what was re-run:
    - final.py extracts the features and scores both methods [p. 42] (image);
    - the method's statistics "are fit on ID-train only" [p. 49] (image);
    - Procrustes-DS "is post-hoc and reuses this checkpoint" [p. 40] (image).
  - So the re-run did re-fit the method. What it reused was the fine-tuned backbone the two methods share, and its cached features.
- IR-23's argument survives both corrections.

**m6. Section 3.7: the cost of I1 does not follow from p. 62.**
- "30.6 minutes on a single NVIDIA A100" is the DynaSpec-RAG module's training only ("The module is trained for 40 epochs on pooled training splits").
- The baseline is "the frozen TS-RAG (Chronos-Bolt + ARM)" [p. 62], so it has no comparable training run.
- IR-23's "every reported row" also includes the draft's seven ablations (its Tables 4–9 and 11) [pp. 69–71].
- ScientistOne's "We run each evaluator five times" absorbs evaluator noise on its ADRS benchmark of solver tasks, which involve no training (ref:2605.26340v1:sections/06a_setup.tex:7-10). "Five fits" is our assumption, not its count.
- Fix: recompute the cost from the page, and label the assumption as ours.

**m7. Section 2.8: "Table 15's 4 ICLR tasks" misstates the table's sample.** Table 15 covers "the five papers". ScientistTwo's column gives a reported gain on "4/5" papers, and "5--6 ablations per paper" (tex:sections/appendix.tex:174-188). Fix: n = 4 of 5.

**m8. Some evidence is quoted by halves.**
- **"Every component contributes" (p. 41).** The page justifies this by the near-OOD gain: "drive the near-OOD (CIFAR-10) gain". CIFAR-10 AUROC does rise (95.91 → 97.18 → 97.58), while the six-set average falls. Quote both.
- **p. 42 states both gains:** "1.99pp over the reproduced X-Maha and 1.58pp over the paper".
- **Section 2.3's "I extracted test features fresh from the checkpoint" [p. 47]** is the audit, after the search. It shows test data was within an agent's reach, not that the search was steered by it.

**m9. The reverse case: what the paper specifies is marked as ours.**
- IR-21's rows for G2, G4 and G5, and IR-28, carry only `[ours]`, but §4.2 specifies:
  - G2's hook: "immediately after experimentation";
  - G4's fix: "enabling the Writer Agent to ground and correct the bibliography";
  - the text-only fix of G5 and IR-28: "which the Writer Agent then uses to rectify any discrepancies in the method section" (tex:sections/4_experiment.tex:43).
- Fix: cite §4.2 in each row, so that what is kept stands apart from M2's departures.

**m10. Section 2.6: what the paper says next to the gap is missing.** Add two items:
- the audit's check "Test / OOD data leakage into calibration" [p. 49] (image), a separation inside the method that U-NOTE-1 cites;
- App. D's "(subset test split)" for its Ablation 1 [p. 69], which shows test data feeding the ablation critic's decision (`analysis.md` section 4.2).

**Outside this lens, noted for the coordinator:**
- IR-15 and IR-23 reinterpret CLAUDE.md's "The test set is used once, at the end." The person should confirm.
- IR-4's "once per task, before any candidate is scored" settles the E_base half of A-BASE-1, but section 1.6 does not list A-BASE-1.

## 4. What is right and must not be lost

- **Quotes and anchors are exact.** Every verbatim quote and anchor is correctly located:
  - ScientistTwo: §4.2 lines 41 and 43, App. B lines 236–238, Table 16 lines 306–313, and fn. 2.
  - ScientistOne:
    - §5, lines 16, 18, 25 and 47;
    - §6, lines 8, 10, 27 and 29;
    - §6.1, lines 13, 40, 45, 48, 54 and 56;
    - App. D, lines 46–48 and 54;
    - App. E.1, lines 115–116;
    - App. E.2, line 302;
    - App. F, line 567;
    - §4.3, line 20.
- **Every image-page fact I checked is confirmed:**
  - FPR95 4.17 against 3.76, and the gain going from 1.58 to 1.99 pp as the report states [pp. 41–42];
  - the script "scores both … and writes this report" [p. 42];
  - the report titled FULL covers the six OOD sets of balanced CIFAR-100 [p. 40];
  - "CIFAR-10 AUROC drops from 96.83% to 88.02%" [p. 46];
  - "Per the requirements", with the verdict saved under the task's own folder, `./tasks/x_maha/` [p. 47];
  - "faithful, not manipulated" [p. 50];
  - 50 TALENT datasets, test sets capped at 2000, and inner cross-validation [p. 51];
  - the scale tuned on validation splits [p. 61];
  - 30.6 minutes [p. 62];
  - 42 references [pp. 66–68];
  - VD-STrans's throughput speed-up [p. 3].
- **The delegation boundary is kept everywhere the brief asked about.** ScientistOne's §6 run settings are never presented as the definition, and the tolerance is left to U-NOTE-4. Every citation of §6 or an appendix is labelled as ScientistOne's practice or audit finding. Sections 1.2 and 2.3 correctly write "In ScientistOne's audit" for Sakana's failures.
- **The classifications of U-INT-4, U-TOP-5 and A-INT-3 are right,** and A-ART-2 is rightly kept open.
- **The register comparisons are faithful:** all four proposal paraphrases, and the record that `note-check.md`'s account of A-INT-1 is superseded.
- **The departures that are listed are real:**
  - the golden evaluator;
  - E_base from task packaging;
  - a split the paper does not have;
  - the exported paper is no longer the reviewed one;
  - the published-SOTA comparison moves to reporting;
  - the held-out reporting auditor.
