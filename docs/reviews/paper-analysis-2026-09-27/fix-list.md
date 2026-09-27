# Fix list: the review of TODO task 1's analysis, deduplicated

**What this is.** Every finding of the persona reviews in this folder, merged into one list of
changes. Each fix is written once, even when several reviews raised it, and is assigned to the
owner of the document it changes. The reviews themselves are kept verbatim beside this file.

**Sources.** Each fix names the review findings it comes from:

| Short name | File |
|---|---|
| RE1 | `research-engineer.md`, wave 1 |
| RE2 | `research-engineer-analysis.md`, wave 2 |
| EI1 | `evaluation-integrity-engineer.md`, wave 1 |
| EI2 | `evaluation-integrity-engineer-analysis.md`, wave 2 |
| AE | `agent-engineer.md` |
| SA | `system-architect.md` |
| TR | the traceability step's findings (`docs/paper/traceability.md`, section 1.4) |
| UN | the consolidation step's "Fixes the source documents need" (`docs/paper/unspecified.md`) |

**Where two reviews conflict,** the orchestrating session decides, and says so under the fix.

**Evidence that comes from outside ScientistTwo's own text** is marked. ScientistOne is quoted from
its TeX as a source the paper delegates to (`docs/paper/README.md`); the ScientistOne quotes below
were checked against it on 2026-09-27. SCOOD and the X-Mahalanobis paper are external: they are
recorded as such, and they route decisions to task 5.

## analysis.md and stages/ (owner: the engine analyst)

| ID | Change | From |
|---|---|---|
| F-AN-0 | **BLOCKER. Rewrite §3.3's conclusion; keep its evidence.** Listing 1 as printed fits one row exactly, but every way a stage deviates from it is a parameter value, and the paper says it abstracts every stage with Listing 1 ("we abstract all stages", tex:sections/3_new_method.tex:5). Figure 7 draws the same critic → Full-Set Engineer → Result Compare sub-graph twice, once for ablation and once for meta-review [Fig. 7] (image). Replace "a family resemblance, not a contract" with a table that has one row per stage and these columns: the generator; what the critic judges, as distinct from what gets refined; the assessor and its decision rule; the verdict map; the guard and what happens when it fails; what a limit counts (A-TOP-2) and the limit; what happens at the limit (discard, keep the last, keep the best, or stop the run); nesting and fan-out. The conclusion becomes: one primitive with parameters for each stage, where the paper's pseudocode fixes one set of parameters [ours]. Mark "A different shape, SPECIFIED as such" as our reading `[ours]`. | SA-B1 |
| F-AN-1 | **Reword §1.1 item 2 and §4.2's "Consequence".** Replace "no gain is computed inside the loop" with: the paper specifies no gain formula for any decision in the loop. Every comparison is an LLM judgement ("ScientistTwo has no target metric", [Tab. 15]) over numbers that agent-written code produced. Those numbers may include gains [p. 42] and statistics ("statistically inert", [Tab. 16]). Tag the §4.2 rows that settle A-ABL-3 and A-FULL-1 with those IDs. The two update gates are worded as strict tests, "strictly outperforms" (tex:sections/3_new_method.tex:111) and "verified as strictly superior" (tex:sections/3_new_method.tex:148). Whether they are numeric tests or an agent's preference is AMBIGUOUS, so point both places to A-ABL-3 and do not settle it. *Conflict:* AE called item 2 correct, RE2 called it wrong, and SA said it settles A-ABL-3 silently. Each is right about a different part, so all three parts are kept. | RE2-M1, AE, SA-M2 |
| F-AN-2 | **§4.2's decision table.** Add three columns: "Produced by" (whose code produced the input), "Data" (which split: the reported benchmark, with no split stated) and "Guard" (what checks it, if anything). Add rows for the content decisions that move reported numbers, each with the guard "none in the loop": the numbers put in the paper (the Drafter and the Enhancer, "updating empirical tables and figures" [§3.5]); the rebuttal's data ("50 representative TALENT datasets", [p. 51]); and the full-set scope ("entire benchmark suite" [§3.2] against "FULL CIFAR-100 benchmark" [p. 40]). | EI2-M1, EI2-M4 |
| F-AN-3 | **New U-TOP-5: which data split each decision reads.** None is stated, and every decision reads the benchmark that is reported. Link U-NOTE-1 and U-ART-5. Add an "Inputs: split" line to every stage block in `stages/`. | RE2-M3, EI2-M1 |
| F-AN-4 | **New U-TOP-6: no success criterion for any agent.** The paper tests agents only end-to-end (Tabs. 5–8; Fig. 9b, "Evolved Idea Selected: 27" of 49). Add a "Success evidence" column to the §7 roster. | AE-M1 |
| F-AN-5 | **New U-ABL-5: where the Ablation Critic draws the line between Refine and reject.** Three cases pin it: TeCh was rejected for gains "driven by general training controls" [App. B]; p. 46 found every component failing, yet the idea was refined [p. 46] [p. 40]; LC-FTT was stripped "down to the lone component that carried the gain" [Tab. 16]. | AE-M2 |
| F-AN-6 | **§7: a table of author family against judge family.** Columns: decision, author family, judge family, independence required [ours], swap-family control [ours]. Rows: the Idea Generator against the Novelty Checker; the Ablation Critic and the Result Comparison Agent, which judge refinements their own family asked for; the §4.2 audits on "the Coding Agent", the same backend as the coder; ScholarPeer, whose backbone is unknown (U-PEER-3). | AE-M5 |
| F-AN-7 | **P-CFG-9, the threshold of 8, is not "none".** It is a point on ScholarPeer's own scale, where accepted human papers average 6.2–6.9 [Tab. 3]. The reported acceptance rule fits only "≥ 6" (claims.md A-EVAL-3). Mark the threshold "reviewer-dependent; calibrate [ours]", and link C-ABLX-4. Retitle §7.2's "Reviewer independence, SPECIFIED" as "ScholarPeer is the optimisation target, not an independent judge (SPECIFIED)". Carry the same into `stages/05`. | AE-M6 |
| F-AN-8 | **The §7 roster.** Split "Model" into "Backend" and "Model". Add Figure 3's evidence to A-CFG-1: the *Ablation Study Agent* box holds the *Planning Agent*, and *New Idea* re-enters the *Full-Set Experiment Agent*. Mark the model citations of P-ROSTER-17 and P-ROSTER-23 `[inferred]`. Record that artifacts.md P-ART-3 names Claude Code for A_FullEng (see F-AR-10). | AE-m1, AE-m2 |
| F-AN-9 | **What each judge reads, and how much.** Add gaps on input bounds: the Selector receives every C^h [§3.3, Eq. 4], and the Ablation Critic read implementation detail ("forcing the practical implementation", [p. 46]). Extend U-EVO-2, or add new items. | AE-m3 |
| F-AN-10 | **P-ROSTER-26 and P-ROSTER-28 are judges.** Nothing in the paper makes them read-only, and the auditor on p. 47 saved `repro_check.json` inside the task it audited [p. 47]. | AE-m4 |
| F-AN-11 | **`stages/07`: fixed enforcement classes.** The classes are prompt, LLM filter, LLM fixer, post-hoc LLM audit, and setup. Add the post-hoc CoE audit behind Table 7 as a row. Add "setup: none [ours]": §3, §4.2 and App. A.2 describe no sandbox, no read-only evaluation code, no hash and no harness. State that the method–code fix edits the paper, not the code. Reword §1.1 item 9 as "prompts and LLMs only; nothing is enforced by the setup". | EI2-M2, EI1-M7 |
| F-AN-12 | **New U-INT-4: no fixed evaluator.** Agent code computes every metric (U-ART-16). ScientistOne's audit assumes "Each task provides a fixed evaluator, starter code, and scoring metric" (ref:2605.26340v1:sections/06a_setup.tex:8). Add the evaluator, the full-benchmark definition and the data splits to U-TOP-1. The decision behind A-INT-1 becomes: a locked harness computes the metrics, because a re-run used as a gate proves only that the code is deterministic [ours]. In `stages/07`, record the procedure the paper adopts by reference, each with its ScientistOne anchor: I1 re-runs "on the golden evaluator" (`05_coe_audit.tex:25-26`), "five times", with the tolerance max(1%, 3σ/\|s̄\|) (`06a_setup.tex:10`); I2 and I4 are LLM judges voting by majority (`05_coe_audit.tex:32, 44`), 3 of 5 (`012c_coe_audit_details.tex:302`); I3 queries four APIs (`05_coe_audit.tex:36`); I4 is lenient, counting only "a fundamentally different algorithm" (`05_coe_audit.tex:43`). | EI2-M3, EI1-M1 |
| F-AN-13 | **U-INT-3 and A-INT-3.** U-INT-3: say why the timing matters. If the repairs run before review, the Enhancer's later edits are never audited; if they run after review, the paper reviewed is not the paper exported. A-INT-3: require the post-hoc auditor to be independent of the in-loop fixer (U-EVAL-5). | EI2-m1, EI2-m3 |
| F-AN-14 | **§4 pseudocode.** In `A_Coder`, move the specification-filter comment above the `return`, where it would run. | EI2-m2 |
| F-AN-15 | **A-FULL-1 and A-BASE-1: cite p. 41.** The idea's own full-set script recomputes the baseline, "X-Maha (reproduced)", and reports both references. The reproduction is weaker than the published baseline (FPR95 4.17 against 3.76), so 0.41 of the 1.99 pp gain comes from the reproduction [p. 41] [p. 42]. Link U-ART-20. Reword §1.1 item 6: no stage that §3 describes produces the reference, while the one artifact shows the idea's script recomputing it. | RE2-M2, EI1-M3 |
| F-AN-16 | **New U-SUB-2: tuning parity.** `Engineer` tunes the idea for up to two rounds (tex:sections/3_new_method.tex:45), while E_base is produced once, with no refine step [Tab. 1]. TeCh's gain came from "general training controls" [App. B]. The decision it forces: the baseline gets an equal tuning budget, or a tuned-baseline control runs [ours]. | RE2-M4 |
| F-AN-17 | **§9's bound.** Label it "excluding integrity sessions" (φ = μ = 0). Give the floor, 16, and the span under the open readings: 99–127 at N_p = 6, N_t = 3. Add N_p data points: "full tables for all six ablations" [p. 11], and DynaSpec-RAG's seven [pp. 64–65]; at N_p = 7 the bound is 96 + 4N_t. Add, as an illustration only, the expected count from Figure 10b: about 6.5 ideas per task [inferred], with its caveats (the 33 NeurIPS successes only; a failed task runs every round). | RE2-m5, RE2-m7 |
| F-AN-18 | **§6, the N_0 row.** Drop the corroboration, since "round 0's selected ideas are all seeds" holds for any N_0. | RE2-m6 |
| F-AN-19 | **A-EVO-1's class.** It is AMBIGUOUS under reading 1 of A-EVO-2, which the analysis favours, and INCONSISTENT only under reading 2. Say so. | RE2-m8 |
| F-AN-21 | **A new gap split out of A-TOP-1: the last candidate or the best one?** A-TOP-1 says "the last or best candidate passes on", which merges two different policies. Peer review overwrites P_new, since "The updated manuscript is re-evaluated by" the reviewer (tex:sections/3_new_method.tex:131), so the exported paper can score lower than an earlier round's. Record this as its own item, and say which policy each stage follows. | SA-B1 |
| F-AN-22 | **Rewrite §8's "What persists across stages".** It is wrong as written. Give a table of what crosses stages, each object with a P- ID under a new key `STATE`, owned by analysis.md, and with its producer, its consumers, its lifetime, and whether it can change. It must include:<br>• H_0, its scores, and a record of which seeds have been used ("highest-ranked unevaluated seed ideas", line 76);<br>• C_base and E_base, which go into every A_Coder call (lines 40–41);<br>• the C^h of every Good idea, kept until selection [§3.3, Eq. 4];<br>• the "diagnostic failure logs" of Bad ideas, which A_Evolve reads (line 68);<br>• the core state;<br>• the chain of codebase versions (C_base, C_sub^h, C_full^h, C^h, C_best, C_new, C+), with "copied, never edited in place" marked `[inferred]` from the "if and only if" update (line 112) and the return to "the previous best outputs" (line 150);<br>• the evaluation protocol as read-only (Tab. 15, "forbidden (audit)"; App. B, I2).<br>Link claims.md for checkpoint granularity (Fig. 10b's shares; Fig. 10a's 2.51-day mean and 6.1% of runs at 5 days or more). | SA-M1 |
| F-AN-23 | **§4: the Verifier returns a verdict and feedback** `[inferred from Lst. 1]`. It is the Extractor that "again identifies missing limitations" (tex:sections/3_new_method.tex:22), not the Verifier. | SA-m1 |
| F-AN-24 | **"Reading choices": record both counting conventions.** The limitation loop counts critic calls, so its 16th expansion is never judged; the other loops count refinements. | SA-m2 |
| F-AN-25 | **§3.1: E_best is not among the references a critic reads.** It is the Result Comparison Agent that reads E_best (lines 111–112 and 147). | SA-m3 |
| F-AN-26 | **§4.1 "Never restarted" and "Reading choices".** Add Figure 3's evidence: the Analyzer's *New Idea* re-enters the critic of the Full-Set Experiment Agent [Fig. 3] (image). Add U-ABL-2 to "Reading choices". | SA-m4 |
| F-AN-27 | **P-CFG-11: record the other reading as disfavoured.** "with review-based refinement conducted at most once" can be read as two reviews and one rebuttal, which would leave N_meta without a value. The evidence for the main reading: Table 5 shows rebuttals in rounds 1 and 2, and the headings say "Review-Driven" (lines 134 and 142). | SA-m5 |
| F-AN-28 | **Give element IDs to the parameters App. A.2 leaves unset:** N_seed, N_0, the full-set engineering limit, N_p, N_t and N_a. They are elements of the paper even without a value (P-CFG-12 onwards). | TR |
| F-AN-29 | **Duplicated elements.** P-LIM-4 and P-CFG-1 are the same limit, and so are P-SUB-4 and P-CFG-3. Either state the relation (the loop's limit as mechanism, against its value in App. A.2) or merge them. | TR |
| F-AN-30 | **P-ROSTER-13, A_Coder as a composite.** It lists rows 6–11, which includes the Baseline Coder, which §4's own pseudocode runs outside A_Coder. It leaves out the Full-Set Engineer (row 12), which §3.2 places inside. Correct the membership, and link A-BASE-1. | TR |
| F-AN-31 | **Elements for the parts of the paper that have none:**<br>• Figure 3's group boxes;<br>• the external systems of §7.2, including the coding backend that Table 8 swaps (P-ROSTER-29 onwards);<br>• App. B's attribution rule, that the gain must be "attributable to the proposed mechanism" [Tab. 15];<br>• the chained runs of Table 9, where one run's (P+, C+) is "provided as context in the next discovery cycle" [§4.3]. | TR |
| F-AN-20 | **U-BASE-1.** Cite "FULL, 6 of 6" [p. 40] (image) and "(subset test split)" [p. 69]. Record that the subset's false-negative rate, meaning Good ideas pruned on the subset, is never measured. | RE2-m9 |

## claims.md and claims/ (owner: the claims analyst)

| ID | Change | From |
|---|---|---|
| F-CL-1 | **A-EVAL-3, finding 1 and C-MAIN-1.** Add the decisive row: S2's ICLR row is 100% accepted at a mean of 7.0, which is impossible under "≥ 8" without any SD argument [Tab. 3]. The minimum-SD test also fails "≥ 8" on 10 of the 11 rows, so give the printed examples. With one integer score per paper and the sample SD, only "≥ 6" fits all 11 rows (`playground/paper/reviews/research-engineer/sp_integer.py`). The caveat: if SP averages several reviews and accepts by majority, the argument fails. Record the result as "consistent only with ≥ 6 [inferred]", and keep the §3.5-against-the-tables item INCONSISTENT. | RE1-M1 |
| F-CL-2 | **Assessments of C-HEAD-1, C-HEAD-2, C-MAIN-8 and P-EVAL-2: winner's curse.** The gains and the success count are measured on the data the search selected on: about 8–10 candidates, then two "strictly better" gates, all on the full benchmark. The inflation cannot be sized without variance. Link U-NOTE-1, U-ART-5 and U-TOP-5. Decision for task 6: a held-out test set and a null-idea control [ours]. | RE1-M2 |
| F-CL-3 | **C-MAIN-8 and C-APPB-6.** S2's ICLR cells cannot be rebuilt from Table 16. Its unprinted gains would have to be 0.9–1.1% and 9.9–10.5%, and Pinet's printed results contain nothing near 10% (`s2_iclr.py`). | RE1-M4 |
| F-CL-4 | **A-EVAL-6 is not INCONSISTENT.** The two numbers come from two points in the pipeline, and the "strictly better" gates predict Tab. 4 ≥ Fig. 9a, which fits the observed +1.0 to +1.3. Reclassify it as AMBIGUOUS: which point each number measures. | RE1-m8 |
| F-CL-5 | **C-ABLX-4 and finding 2.** Replace "round 2 lowers SAR acceptance" with "no held-out gain in round 2 (36 → 34 of 49; exact McNemar p ≥ 0.50)". | RE1-m9 |
| F-CL-6 | **C-ABLX-2.** Drop "not of the metric": the Selector "compares performance metrics" [§3.3]. | RE1-m10 |
| F-CL-7 | **C-DISC-2.** Seed Idea Generation has no printed label; the residuals are 0.6% (time) and 0.2% (cost). Drop "sums to 100.1% ✓". | RE1-m11 |
| F-CL-8 | **C-ABLX-6.** Replace "17.75×" with the absolute difference, +0.067. If a ratio is kept, give its rounding range, 15.7–20.4. | RE1-m12 |
| F-CL-9 | **C-DISC-4 and C-HEAD-8.** State both conventions: as ratio gains the steps compound to 31.5%; as time reductions they compound to 26.1%, a 1.35× speedup. | RE1-m13 |
| F-CL-10 | **U-EVAL-1: open with the strongest example.** On p. 41's numbers, AUROC gives +0.26% to +0.40%, while relative FPR95 gives 42.3% to 48.0% [ours]. The choice of rule alone moves one task's gain more than 100-fold. Decision: pre-register the metric, direction and baseline for each task [ours]. | EI1-M6 |
| F-CL-11 | **C-ABLX-7, "internally consistent".** Add that Table 7's first row passes a reward-hacked codebase on Score Verif. (50/50, with 1/50 specification violations; fn. 2). So the check, as run, shows determinism, not validity. ScientistOne's I1 re-runs "on the golden evaluator" (ref anchor as in F-AN-12). | EI1-M2 |
| F-CL-12 | **U-EVAL-5.** Record that the audit is specified by reference, ScientistOne's CoE audit, with the protocol of F-AN-12, and link `stages/07`. | EI1-M1 |
| F-CL-13 | **A short "What task 5 must measure itself".** Link RE1's and RE2's task-5 lists rather than copying them. | RE1, RE2 |

## artifacts.md (owner: the artifacts analyst)

| ID | Change | From |
|---|---|---|
| F-AR-1 | **P-ART-3, P-ART-4 and the key findings: where the gain comes from.** The ablation's "Trace-only (X-Maha)" row scores 99.52/2.46, against 99.56/2.17 for the full method [p. 44] (image). So the headline weighting carries 0.29 of the 2.00 pp FPR95 gain over the reproduced baseline's 4.17 [p. 41]. The additive table makes the average worse with each of the first two components (4.17 → 4.28 → 4.48), yet the report says "Every component contributes", "directly rebutting" the critic [p. 41]. Record it as golden case 1 for a sycophantic critic [ours]. | RE1-M5, AE-M4, EI1-m2 |
| F-AR-2 | **The test-set finding (key finding 6, U-ART-5, P-ART-4): rest it on the critic-to-redesign loop.** The critic steers with OOD test numbers [p. 46], and the auditor calls them "test features" [p. 47]. Correct "best setting not shipped": γ stayed at 2.0 rather than the test-best 3.0, which shows the search saw the test sets, not that it selected on them. DynaSpec-RAG's grid search on validation splits is correct practice [p. 61]. Record, as external (SCOOD, Yang et al. 2021), that the benchmark defines only a training set and a testing set, so we build our own validation split [ours]. | RE1-m6, EI1-m1 |
| F-AR-3 | **U-ART-4, and a new INCONSISTENT item on the scope of "full".** Round 0 ran on CIFAR-100-LT [p. 46], but the "FULL" report covers balanced CIFAR-100 only [p. 40]. The agent decides what "full" means, and the setting that failed is absent from the final report, while App. B claims "the paper's full benchmark grid". Mark as external that the X-Mahalanobis paper's own benchmarks include ImageNet and CIFAR-100-LT. | RE1-m6, EI1-M4 |
| F-AR-4 | **A-ART-3 becomes AMBIGUOUS.** It is one audit (n = 1), of a NeurIPS task outside Table 7's sample, and a bit-exact re-run of deterministic post-hoc scoring shows where the numbers came from, not that they are robust. | RE1-m7 |
| F-AR-5 | **The audit, specified by reference (U-ART-6, U-ART-8, A-ART-3, key findings 3–4).** Give ScientistOne's I1 (the golden evaluator, five runs, the tolerance) and I4 ("a fundamentally different algorithm"), with the ref anchors of F-AN-12. p. 49's "not a different algorithm" applies the cited, lenient rule, so replace "the auditor sets its own threshold". p. 47 compares one run of the agent's `final.py` with the agent's report, with no tolerance: if p. 47 is the CoE audit (A-ART-2), it is INCONSISTENT with the referenced protocol. | EI1-M1 |
| F-AR-6 | **P-ART-6 and key finding 3.** The score verification shown compares agent code with a report the same code wrote, which proves determinism, not validity. Table 7's first row passed a hacked result (fn. 2). The audit says it skipped the baseline, yet says "the ablation table all match", and that table's first row is the baseline [p. 41]. No page compares the manuscript's numbers with a re-run. | EI1-M2 |
| F-AR-7 | **Name the weak-baseline attack (U-ART-16, U-ART-20, the run-layout row).** The baseline is a "faithful reimplementation of the paper's X-Maha" inside the agent's script [p. 41], and it trails the paper (99.16/4.17 against 99.30/3.76), which widens the FPR95 gain from 1.58 to 1.99 pp [p. 42]. p. 47 skips it; p. 50 calls it "faithful, not manipulated" from reading the code alone. Correct the run-layout row: the baseline's scores come from agent code, not from `./tasks/x_maha/code`. | EI1-M3 |
| F-AR-8 | **Smaller corrections.** The audit offers "round-number defaults" as proof of no tuning [p. 50], although the earlier defaults λ0 = μ0 = 0.1 were dropped after failing on the OOD test sets [p. 46]. Replace "No §4.2 audit covers rebuttal code" with "the paper is silent on auditing rebuttal code". Add that the rebuttal agent picked its own "50 representative TALENT datasets" [p. 51]. | EI1-m2 |
| F-AR-9 | **A-ART-4: move the RALI case out.** The "statistically inert" rejection names no critic, and a subset `Bad` fits it equally well [Tab. 16]. File it as its own item, with the critic unknown, and note that it claims significance where the runs shown use `seed=0` [p. 40]. | AE-M3 |
| F-AR-10 | **P-ART-3.** Mark "Claude Code with Opus 4.8" for A_FullEng as `[inferred]`, and link A-CFG-1. | AE-m2 |
| F-AR-11 | **P-ART-6 and P-ART-7.** Record that the auditor wrote `repro_check.json` inside the task it audited [p. 47]: nothing makes a judge read-only. | AE-m4 |

## note-check.md (owner: the note analyst)

| ID | Change | From |
|---|---|---|
| F-NC-1 | **N-40 to N-43, and summary item 4: the audit is specified by reference.** Table 7 follows ScientistOne, so N-40 to N-43 are TRUE of their source. Quote ScientistOne with `[Ref: meng2026scientistone …]` and ref anchors (F-AN-12), and keep "not in ScientistTwo's own text" explicit. Rewrite summary item 4: the note is right about ScientistOne, and the paper's one example audit differs from it. Update the counts. | EI1-M1 |
| F-NC-2 | **Special case C and N-106: redo the count under reading 1.** Figure 9 shows five rounds (Initial, then Rounds 1–4), so ten ideas, and the bound is 87 + 4N_t at N_p = 6 (99 at N_t = 3). Reconcile it with analysis.md §9: §9 resets the ablation budget in the meta pass and counts no integrity sessions. Point to §9 as the canonical bound. | RE1-M3, RE2 |
| F-NC-3 | **A-NOTE-8.** Add Figure 9's round labels as evidence for reading 1, and link A-EVO-2. | RE1-M3 |
| F-NC-4 | **N-87 and N-89: the writer can pick a better row.** PaperOrchestra "compiles unconstrained experiment logs" [§2]; the Drafter reads E_best and E_abl [§3.5]; the Draft Enhancer runs on Claude Code [App. A.2]; and a better variant than the one shipped existed (γ = 3.0 against the shipped 2.0, [p. 44]). N-89's assessment becomes: a harness-built table with labelled main, ablation and rebuttal rows, where the writer cannot choose which row is "ours" [ours]. | EI1-M5 |
| F-NC-5 | **N-15 and A-NOTE-10.** Link the enforcement classes of `stages/07` (F-AN-11). | EI1-M7 |

## From the decision register: its "Fixes the source documents need"

`docs/paper/unspecified.md` ends with 17 fixes, F-1 to F-17, each motivated by an entry D-n of its
"Where the analyses disagree". Six overlap fixes above and are applied together with them; the rest
are assigned here. Apply the register's wording; it is the more precise.

| Register fix | Owner | Overlaps | Change, in one line |
|---|---|---|---|
| F-1 | note-check.md | F-NC-3 | A-NOTE-8: Figure 9's labels, and 4 of 49 tasks picking an idea from *Round 4*, favour reading 1; "up to 10 ideas" assumes N_0 = 2, and N_0 = 1 gives 9 |
| F-2 | note-check.md | F-NC-2 | Special case C and N-106: 81 + 4N_t or 87 + 4N_t (93 or 99 at N_t = 3); 10–55 or 11–61 sessions without a success; name the two assumptions left; point to analysis.md §9 |
| F-3 | analysis.md | F-AN-24 | A-TOP-2: App. A.2 counts refinements for three loops, not two (engineering, ablation, meta-review) |
| F-4 | analysis.md, stages/03 | F-AN-19 | A-EVO-1 becomes AMBIGUOUS, in stages/03 and in §10.2 |
| F-5 | note-check.md, analysis.md | none | A-NOTE-2 and special case B: §3.4 and §3.6 *imply* keeping, with the closing clauses quoted [inferred], not "not stated"; A-TOP-1: §3.5 explicit, §3.4 and §3.6 implied |
| F-6 | note-check.md, artifacts.md | F-AR-9 | One ablation-critic rejection, TeCh's: fix A-NOTE-4's heading and its App. B bullet, special case B's ablation row, and A-ART-4 |
| F-7 | stages/04 | none | A-ABL-2: TeCh supports reading 2 only under A-ABL-1's reading 2; decide the two together |
| F-8 | note-check.md | none | Mark *wall-clock* as [inferred] in summary item 6, N-60 and special case C |
| F-9 | analysis.md, note-check.md, artifacts.md | F-AN-8, F-AR-10 | A-CFG-1: quote "Unless otherwise specified" and Figure 3's experiment boxes as evidence for reading 2; show the inference in N-9 and P-ART-3, citing A-CFG-1 |
| F-10 | stages/05 | none | "Evidence on the rounds": give the other readings of "did not undergo this process" |
| F-11 | artifacts.md | none | A-ART-5: reading 2 exceeds the trigger's wording, not §3.2's, since the engineer also refines h and Eq. 2 returns h |
| F-12 | claims.md | none | Align the decisions of U-EVAL-1 and A-EVAL-2 with the merged register row U-EVAL-1 |
| F-13 | note-check.md | none | A-NOTE-9: number the readings as A-FULL-2 does |
| F-14 | note-check.md, and any document that says it | none | "Consolidation moves them into unspecified.md" is wrong now: the entries stay, and the register indexes them |
| F-15 | claims.md | none | U-BENCH-1: the subset's gap is U-BASE-1, not a SUB item |
| F-16 | analysis.md | F-AN-17 | §9: add the lower bound, 16 at N_0 = 2 and N_p = 5, 18 at N_0 = 1 with an end-of-round stop test |
| F-17 | every gap section | none | Add to each full entry the register row it maps to, e.g. *Register: A-TOP-1* |

## unspecified.md and traceability.md (after the fixes above)

| ID | Change | From |
|---|---|---|
| F-UN-2 | **The "blocks" priority for task 3 follows the architect's ranked list** ("What task 3 needs decided first" in `system-architect.md`). The parameters of the stage primitive, and the unit of work and its failure, come first. | SA |
| F-UN-1 | Register the new IDs (U-TOP-5, U-TOP-6, U-ABL-5, U-SUB-2, U-INT-4, the last-or-best item, the new `P-STATE` elements, the new artifacts items, the input-bound items) and the reclassifications (A-EVO-1, A-ART-3, A-EVAL-6). Re-run `register_coverage.py` and `trace_coverage.py`. | all |
