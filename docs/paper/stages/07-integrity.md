# Integrity mechanisms in the pipeline [§4.2 "CoE Integrity Audit"]

Revised 2026-09-28 after the persona review: fixes F-AN-3, F-AN-11, F-AN-12, F-AN-13 and F-17 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md`; then the closure corrections from the `closure-*.md` reports in that folder [ours].

Part of [analysis.md](../analysis.md). These are the mechanisms §4.2 adds to the engine; none of them is a Table 1 row [§4.2] [Tab. 1] [ours].

- **The audit is evaluation, not a stage.** The CoE Integrity Audit [Bib: meng2026scientistone] "is a post-hoc evaluation framework that verifies whether claims in a generated paper are supported by its artifacts", with four checks: score verification, specification compliance, reference verification and method–code alignment [§4.2] (tex:sections/4_experiment.tex:41).
- **What the pipeline adds.** "we introduce three dedicated refinement agents alongside careful agent prompt design" [§4.2] (tex:sections/4_experiment.tex:43); Table 7's header names the three refinement agents Spec. Violat., Ref. Verif. and Method Code [Tab. 7] (tex:tables/ablation_audit.tex:7-9).

### Integrity mechanisms [§4.2 "CoE Integrity Audit"] · P-INT-1 … 5

- **Purpose:** papers and codebases "must be rigorously verifiable across all four dimensions" [§4.2] (tex:sections/4_experiment.tex:41).
- **Inputs:** experiment code and results, the manuscript, its bibliography, and task rules [§4.2] (tex:sections/4_experiment.tex:41-43).
- **Inputs, split:** none named; the one audit extracted *test features* to check a cache [p. 47] (U-TOP-5) [§4.2].
- **Outputs:** discarded solutions, a corrected bibliography, an audit report and a corrected method section [§4.2] (tex:sections/4_experiment.tex:43).
- **Agents:** the Coding Agent in three roles, a search-augmented LLM, and the Writer Agent [§4.2]; which agents these are is A-INT-2 and A-INT-3, and their models are in section 7 of analysis.md [ours].
- **Steps:** the four rows of the table below, each a single pass [§4.2].
- **Loop:** none stated (U-INT-3) [§4.2].
- **Stopping rule:** not applicable [§4.2] [ours].
- **On exhaustion:** not applicable [§4.2] [ours].
- **On failure:** a rule-violating solution is discarded, and a whole task can be lost [§4.2] [fn. 2].
- **Gaps:** A-INT-1, A-INT-2, A-INT-3, U-INT-1, U-INT-2, U-INT-3, U-INT-4 [§4.2].

Each mechanism is filed under one of five fixed enforcement classes: prompt, LLM filter, LLM fixer, post-hoc LLM audit, and setup [ours].

| ID | CoE check | The mechanism, quoted | Where it sits | Reads → writes | Enforced by |
|---|---|---|---|---|---|
| P-INT-1 | Score verification | "the Coding Agent is prompted during the experimentation phase to output self-contained, reproducible scripts and execution instructions" [§4.2] (tex:sections/4_experiment.tex:43) | every coding agent that runs experiments [inferred] [§4.2] | nothing → scripts and run instructions in the codebase [§4.2] | prompt, "ensuring full reproducibility without requiring additional post-hoc refinement" [§4.2] |
| P-INT-2 | Specification compliance | "a validation filter that uses the Coding Agent to detect and discard rule-violating solutions immediately after experimentation" [§4.2] (tex:sections/4_experiment.tex:43) | after experimentation; which experiments is U-INT-1 [§4.2] | solution code and task rules (U-INT-2) → keep or discard [§4.2] | LLM filter [§4.2] [ours] |
| P-INT-3 | Reference verification | "a search-augmented LLM identifies hallucinated citations, enabling the Writer Agent to ground and correct the bibliography using live search results" [§4.2] (tex:sections/4_experiment.tex:43) | on a manuscript; when is U-INT-3 [§4.2] | bibliography and live search → a corrected bibliography [§4.2] | LLM fixer: an LLM with search flags, the Writer Agent corrects [§4.2] [ours] |
| P-INT-4 | Method–code alignment | "the Coding Agent audits the repository against the manuscript to produce an audit report, which the Writer Agent then uses to rectify any discrepancies in the method section" [§4.2] (tex:sections/4_experiment.tex:43) | on a manuscript with its code; when is U-INT-3 [§4.2] | C_best and P_new → an audit report, then a corrected method section [§4.2] | LLM fixer: the fix edits the paper, not the code [§4.2] [ours] |
| P-INT-5 | all four | the audit behind Table 7, "a post-hoc evaluation framework", following ScientistOne [§4.2] (tex:sections/4_experiment.tex:41) [Tab. 7] | after the run, outside the loop [§4.2] | the paper, its code, outputs and bibliography → a result per check [Tab. 7] | post-hoc LLM audit, specified by reference (below) [§4.2] [ours] |
| none | none | nothing: §3, §4.2 and App. A.2 describe no sandbox, no read-only evaluation code, no hash and no harness [§3] [§4.2] [App. A.2] | none | none | setup: none [ours] |

### The audit Table 7 follows, specified by reference [Ref: meng2026scientistone §5]

Table 7 evaluates integrity "following" ScientistOne, and §4.2 gives each check one clause, so ScientistOne's definition of the audit is part of the specification by reference; whether ScientistTwo's runs used ScientistOne's settings is not stated [Tab. 7] (tex:tables/ablation_audit.tex:3) [§4.2] [ours].

- **I1, score verification.** The reported score is compared with "scores obtained by re-running the submitted solution on the golden evaluator", passing "within an adaptive tolerance that accounts for evaluator noise" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:25-26).
- **I1, its settings in ScientistOne's own runs.** "We run each evaluator five times and compare against the adaptive tolerance" max(1%, 3σ/|s̄|) (paraphrase of the math), and there "Each task provides a fixed evaluator, starter code, and scoring metric" [Ref: meng2026scientistone §6] (ref:2605.26340v1:sections/06a_setup.tex:8) (ref:2605.26340v1:sections/06a_setup.tex:10).
- **I2, specification violation.** "LLMs inspect the solution code against the golden evaluator and task specification to detect such violations, with majority vote across multiple runs", counted by majority vote of 3 out of 5 judges [Ref: meng2026scientistone §5, appendix table on I2] (ref:2605.26340v1:sections/05_coe_audit.tex:32) (ref:2605.26340v1:sections/012c_coe_audit_details.tex:302).
- **I3, reference verification.** "Each bibliography entry is resolved by querying multiple academic APIs (Semantic Scholar, arXiv, OpenAlex, CrossRef) using arXiv ID, DOI, and title" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:36).
- **I4, method–code alignment, a lenient rule.** "only cases where the paper describes a fundamentally different algorithm count as misaligned", judged over "multiple independent runs with majority vote" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:43-44).
- **What this leaves open [ours].** I1 presumes a golden evaluator, and ScientistTwo's tasks name none, since agent code computes every metric (U-INT-4); Table 7's first row passes a reward-hacked codebase on score verification, 50/50 with 1/50 specification violations, so a re-run shows determinism, not validity [Tab. 7] [fn. 2] [ours].

### What they change, and what they stop · P-INT-5

- **Claimed effect.** "removing these refinement agents leads to sporadic audit failures" [§4.2] (tex:sections/4_experiment.tex:43); the counts are in Table 7, which claims.md assesses [Tab. 7] [ours].
- **A task-level consequence.** Without the specification filter the engine completes one more task, but "since the corresponding codebase contains reward hacking, it must be filtered", and Table 7's denominators move from 50 to 49 [fn. 2] (tex:sections/4_experiment.tex:43) [Tab. 7].
- **Appendix B's account.** The engine blocks evaluator tampering "via a reproduction re-run (I1), a protocol-immutability audit (I2), and a method-code alignment audit" (I4) "rather than a prompt-level list of prohibitions" [App. B] (tex:sections/appendix.tex:236-238); Table 15 marks changing the evaluation protocol as forbidden by audit [Tab. 15] (tex:sections/appendix.tex:186).
- **Experiments no mechanism names.** Ablation code, rebuttal code and A_FullEng's refinements are experiments too; whether the filter and the reproducibility prompt reach them is U-INT-1 [§3.4] [§3.5] [§4.2].

## Gaps found here

- **A-INT-1 · INCONSISTENT · Is reproducibility a prompt or a gate?** *Register: A-INT-1.* §4.2 meets score verification because "the Coding Agent is prompted during the experimentation phase to output self-contained, reproducible scripts and execution instructions", "ensuring full reproducibility without requiring additional post-hoc refinement", and calls the audit "a post-hoc evaluation framework" [§4.2] (tex:sections/4_experiment.tex:41) (tex:sections/4_experiment.tex:43).
  - Appendix B instead says the engine blocks such failures "via a reproduction re-run (I1), a protocol-immutability audit (I2), and a method-code alignment audit" (I4), "rather than a prompt-level list of prohibitions" [App. B] (tex:sections/appendix.tex:236-238).
  - Reading 1: inside the loop reproducibility is only prompted, and re-runs happen in post-hoc evaluation [§4.2].
  - Reading 2: the engine re-runs code and audits the protocol as gates before it accepts a result [App. B].
  - Decision forced: a locked harness computes the metrics (U-INT-4), because a re-run used as a gate proves only that the code is deterministic: Table 7's first row passes a reward-hacked codebase on score verification [Tab. 7] [fn. 2] [ours]. This replaces our first wording, whether our engine re-executes results as a gate [ours].
- **A-INT-2 · AMBIGUOUS · Which Writer Agent repairs the paper.** *Register: A-INT-2.* §4.2 has the Writer Agent fix the bibliography and the method section [§4.2] (tex:sections/4_experiment.tex:43); Figure 3's *Writer Agent* box holds *Initial Drafter* and *Draft Enhancer* [Fig. 3] (image), which run on Gemini by default and on Claude Code [App. A.2].
  - Reading 1: the Initial Drafter, right after drafting [§3.5]. Reading 2: the Draft Enhancer, inside or after the review loop [§3.5] [App. A.2].
  - Decision forced: which agent owns the repairs, on which model [ours].
- **A-INT-3 · AMBIGUOUS · Which Coding Agent runs the filter and the audit.** *Register: A-INT-3.* §4.2 says the Coding Agent three times and never says which one [§4.2] (tex:sections/4_experiment.tex:43).
  - Reading 1: the agent that ran the experiment checks its own solution [§4.2].
  - Reading 2: a separate Claude Code session per check, as "whenever coding capabilities are required" suggests [§4.2] (tex:sections/4_experiment.tex:46).
  - Decision forced: whether the checker is independent of the code's author; the post-hoc auditor must also be independent of the in-loop fixer (claims.md U-EVAL-5) [ours].
- **U-INT-1 · UNSPECIFIED · Where the specification filter runs, and what discarding does.** *Register: U-INT-1.* The filter runs right after experimentation, but after which experiments (subset, full set, ablation, rebuttal, A_FullEng) is not said [§4.2] (tex:sections/4_experiment.tex:43). Whether a discarded solution becomes a `Bad` idea or ends the task is not said either; footnote 2 shows a whole task filtered out [fn. 2]. Decision forced: the filter's hook points and its verdict's effect [ours].
- **U-INT-2 · UNSPECIFIED · Where the task rules come from.** *Register: U-TOP-1 (U-INT-2 is an alias there).* The check "ensures that solution code adheres strictly to task rules without reward hacking" [§4.2] (tex:sections/4_experiment.tex:41), but no stage produces task rules and G's contents are unspecified (U-TOP-1) [§3]. Decision forced: a rule file per task [ours].
- **U-INT-3 · UNSPECIFIED · When the reference and alignment repairs run.** *Register: U-INT-3.* After the initial draft, after each enhancement, once before export, or again after the meta restart: none is stated [§4.2] [§3.5] [§3.6]. Why it matters: if the repairs run before review, the Enhancer's later edits are never audited, and if they run after review, the paper that was reviewed is not the paper that is exported [ours]. Decision forced: the hook points of both repairs [ours].
- **U-INT-4 · UNSPECIFIED · No fixed evaluator.** *Register: U-INT-4 (U-ART-16 is an alias there).* No task input provides an evaluator: the coders produce E themselves, the Subset Coding Agent's "resulting logs" [§3.2] (tex:sections/3_new_method.tex:40), and the one trace scores the idea and recomputes the baseline in the agent's own script [p. 41] (image). The audit Table 7 follows presumes one, since I1 re-runs "on the golden evaluator" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:25). Elsewhere in this folder: U-ART-16. Decision forced: a locked evaluation harness per task computes every metric the engine reads or reports [ours].
