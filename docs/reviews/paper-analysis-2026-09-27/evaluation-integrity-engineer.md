# Review: evaluation-integrity-engineer, wave 1 (2026-09-27)

- **Reviewed:** `docs/paper/artifacts.md`, `claims.md` with `claims/`, `note-check.md`, at commit
  `734797a`.
- **Lens:** can an agent move a reported number without a better method, and would we notice.
- **Record:** the reviewer's final message, verbatim below, with one change: its first line named the reviewed folder by an absolute path, shortened here to `docs/paper/`, because this
  repository never holds a path from someone's machine.
- **The external sources it consulted** were downloaded to the session scratchpad only:
  - ScientistOne v1, arXiv:2605.26340, CC BY 4.0. Its quotes were re-checked against its TeX by the
    orchestrating session: `sections/06a_setup.tex:10`, `sections/05_coe_audit.tex:25-26, 32, 36,
    43`, `sections/012c_coe_audit_details.tex:302`.
  - SCOOD (arXiv:2108.11941v1).
  - The X-Mahalanobis paper.

---

# Integrity review: artifacts.md, claims.md (+ claims/), note-check.md

Reviewed: `docs/paper/` (artifacts.md, claims.md, claims/*.md, note-check.md). No repository file was edited.

**Q1 in brief.**
- **Enforcement:** prompts, an LLM filter, LLM fixers and a post-hoc LLM audit [§4.2]. **The setup enforces nothing.**
- **Who computes the numbers:** agent scripts write every per-task number [p. 42]. Gemini parses the gain out of the paper [§4.1].
- **Validation and test:** screening, selection, ablation and refinement all read the sets that are reported [§1] [§3.3] [§3.4].
- **The writer** reads raw logs and every variant.
- **Judges:** the pipeline optimises against ScholarPeer. SAR is held out only by the authors' assertion, and the paper gives no version or date for it. Tab. 7's auditor may be the in-loop fixer.

The documents get most of this right (U-ART-16, U-EVAL-1, U-NOTE-1, P-EVAL-7, C-ABLX-4). No finding is a BLOCKER.

## Findings

**MAJOR-1 · note-check N-40–N-43 and summary item 4; artifacts U-ART-6, A-ART-3, U-ART-8 ("the auditor sets its own threshold").**
- **Problem:** Tab. 7 is an evaluation "following" Meng et al., so ScientistOne's audit is this paper's specification by reference. The documents treat it as absent.
- **Evidence:**
  - ScientistOne v1 TeX: I1 "re-runs the solution on the golden evaluator and compares to the extracted paper score within an adaptive tolerance". It adds "We run each evaluator five times", with a tolerance of max(1%, 3σ/|s̄|), and "majority vote (3/5 judges)".
  - Its I4 counts code as misaligned "only" when the paper "describes a fundamentally different algorithm". p. 49's "not a different algorithm" applies that rule.
  - p. 47 is one run of the agent's `final.py`, compared with the agent's own report, with no tolerance.
- **Fix:**
  - Mark the audit as specified by reference, and INCONSISTENT with pp. 47–50.
  - Mark N-41–N-43 as true of their source.
  - Replace "sets its own threshold" with "applies the cited, lenient rule".
  - Note that I1 checks only the headline score, so Tab. 7's "every claimed results are reproducible" overclaims.

**MAJOR-2 · artifacts key finding 3, P-ART-6; claims C-ABLX-7 ("internally consistent").**
- **Problem:** the score verification shown compares agent code with a report that the same code writes. That proves the run is deterministic, not that the number is valid.
- **Evidence:**
  - The script "scores both Procrustes-DS and the X-Maha baseline and writes this report" [p. 42].
  - Tab. 7 row 1 reads Score Verif. 50/50 and Spec. Violat. 1/50, and that codebase "contains reward hacking" [fn. 2]. A hacked result passed I1.
  - The audit says it skipped the baseline, yet says "the ablation table all match" [p. 47]. That table's first row is the baseline [p. 41].
- **Fix:** say this, cite Tab. 7 row 1, and add that no page compares the manuscript's numbers with a re-run.

**MAJOR-3 · artifacts U-ART-16, U-ART-20; run-layout row "Original code … used as the baseline reference".**
- **Problem:** the weak-baseline attack is visible and unguarded, and the documents never name it.
- **Evidence:**
  - The baseline is a "faithful reimplementation of the paper's X-Maha" inside the agent's own script [p. 41].
  - It trails the paper (99.16/4.17 against 99.30/3.76), which inflates the FPR95 gain from 1.58pp to 1.99pp [p. 42].
  - p. 47 skips it "Per the requirements". p. 50 calls it "faithful, not manipulated" from reading the code alone.
- **Fix:** name the attack, and state that the baseline's scores come from agent code, not from `./tasks/x_maha/code`.

**MAJOR-4 · artifacts U-ART-4, P-ART-3; claims C-APPB-3.**
- **Problem:** the agent decides what "full" means, and the setting where the search failed is missing from the final report.
- **Evidence:**
  - p. 40 is titled "FULL CIFAR-100 benchmark".
  - Round 0 hit "catastrophic failure (79.89% AUROC on CIFAR-100-LT)" [p. 46].
  - X-Mahalanobis itself reports CIFAR-100, ImageNet and CIFAR-100-LT (its Tabs. 1–3; external source).
  - App. B claims evaluation "on the paper's full benchmark grid".
- **Fix:** add an INCONSISTENT item, and fix each task's full set in its manifest before the run.

**MAJOR-5 · note-check N-87, N-89; artifacts P-ART-9.**
- **Problem:** the writer can pick a better row, and one of the writers can execute code.
- **Evidence:**
  - PaperOrchestra "compiles unconstrained experiment logs" [§2], and the drafter reads E_best and E_abl [§3.5].
  - The Draft Enhancer runs on Claude Code [App. A.2].
  - γ = 3.0 (99.58/2.13) beats the shipped γ = 2.0 (99.56/2.17) [p. 44].
- **Fix:** N-89 treats a single table as lost content. Instead, the harness builds one table with labelled main, ablation and rebuttal rows, and the writer cannot choose which row is "ours".

**MAJOR-6 · claims U-EVAL-1, C-HEAD-2.**
- **Problem:** the documents miss the strongest example of the undefined gain rule.
- **Evidence:** on p. 41's numbers, AUROC gives a gain of +0.26% to +0.40%, while relative FPR95 gives 42.3% to 48.0% [ours]. The choice of rule alone moves one task's gain more than 100-fold.
- **Fix:** open U-EVAL-1 with this example, and pre-register the metric, direction and baseline for each task.

**MAJOR-7 · note-check A-NOTE-10, N-15; artifacts key finding 5.**
- **Problem:** A-NOTE-10 asks whether each check is an audit or a gate. Task 6 needs to know whether it is enforced by an LLM or by the setup, and no document classifies the mechanisms that way.
- **Evidence:**
  - §4.2 relies on "careful agent prompt design" and "a validation filter that uses the Coding Agent", and the Writer must "rectify any discrepancies in the method section".
  - The only instance of App. B's "protocol-immutability audit" is p. 50: an LLM asserting that `get_measures` in the agent's tree is "identical to the original codebase". No diff or hash backs the assertion.
- **Fix:** classify every mechanism in analysis.md INT, and attribute "unmodified" to the auditor.

**MINOR-1 · artifacts key finding 6, P-ART-4.**
- "Ran on the test sets" is correct. SCOOD defines only a training set and a "testing set T", made of the CIFAR-100 test set plus the six OOD sets (Yang et al. 2021, §3.1, §4.2). The method's parameters are fit on ID-train only [p. 50].
- But "best setting not shipped" shows only that the search saw the test sets, not that it selected on them. The Selector and the Result Comparison Agent are what select [§3.3] [§3.4].
- **Fix:** record that we must construct our own validation split.

**MINOR-2 · artifacts P-ART-3, P-ART-7, P-ART-8.**
- The report claims "Every component contributes", beside two components that lower the average (99.07/4.28 and 99.02/4.48, against 99.16/4.17) [p. 41].
- The audit offers "round-number defaults" as proof of no tuning [p. 50], although the earlier defaults λ0 = μ0 = 0.1 were dropped after failing on the OOD test sets [p. 46].
- "No §4.2 audit covers rebuttal code" overstates what is only a silence in the paper. The documents also miss that the rebuttal agent picked its own "50 representative TALENT datasets" [p. 51].

## Threat model, from the paper

| Stage | Controls / writes / reads | Rewarded by | Cheapest attack | Caught by |
|---|---|---|---|---|
| §3.1 seeds | idea text | novelty against 2 searched papers | exotic naming | nothing |
| §3.2 baseline | reimplementation, eval code, data | none | weak baseline | nothing |
| §3.2 subset/full, engineer | code, scope, seeds | critics | tune on test; narrow scope | LLM filter, code only |
| §3.3 evolve, select | ideas; reads all test results | S successes; Selector | max over candidates | nothing |
| §3.4 ablate, refine | plans, datasets | critic; "strictly outperforms" | hill-climb on test | nothing |
| §3.5 draft | tables; reads raw logs | SP ≥ 8 | report the best variant | I1, if it reads the paper |
| §3.5 rebuttal | data, caps; Enhancer executes | SP ≥ 8 | write to SP; pick datasets | SAR divergence, post hoc |
| §3.6 meta-review | another refinement | Accept | another max on test | nothing |
| §4.2 fixers | method text, references | own audit | real but irrelevant citation | unknown auditor |
| §4.1 gain | parsed tables | headline | lower-is-better metric | nothing |

Sources, downloaded to the session scratchpad only: [ScientistOne v1](https://arxiv.org/abs/2605.26340) (src sha256 0655a648…) · [SCOOD](https://arxiv.org/pdf/2108.11941v1) · [X-Mahalanobis](https://palm.seu.edu.cn/weit/paper/NeurIPS2025_X-Maha.pdf)
