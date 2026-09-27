# Integrity mechanisms in the pipeline [§4.2 "CoE Integrity Audit"]

Part of [analysis.md](../analysis.md). These are the mechanisms §4.2 adds to the engine; none of them is a Table 1 row [§4.2] [Tab. 1] [ours].

- **The audit is evaluation, not a stage.** The CoE Integrity Audit [Bib: meng2026scientistone] "is a post-hoc evaluation framework that verifies whether claims in a generated paper are supported by its artifacts", with four checks: score verification, specification compliance, reference verification and method–code alignment [§4.2] (tex:sections/4_experiment.tex:41).
- **What the pipeline adds.** "we introduce three dedicated refinement agents alongside careful agent prompt design" [§4.2] (tex:sections/4_experiment.tex:43); Table 7's header names the three refinement agents Spec. Violat., Ref. Verif. and Method Code [Tab. 7] (tex:tables/ablation_audit.tex:7-9).

### Integrity mechanisms [§4.2 "CoE Integrity Audit"] · P-INT-1 … 5

- **Purpose:** papers and codebases "must be rigorously verifiable across all four dimensions" [§4.2] (tex:sections/4_experiment.tex:41).
- **Inputs:** experiment code and results, the manuscript, its bibliography, and task rules [§4.2] (tex:sections/4_experiment.tex:41-43).
- **Outputs:** discarded solutions, a corrected bibliography, an audit report and a corrected method section [§4.2] (tex:sections/4_experiment.tex:43).
- **Agents:** the Coding Agent in three roles, a search-augmented LLM, and the Writer Agent [§4.2]; which agents these are is A-INT-2 and A-INT-3, and their models are in section 7 of analysis.md [ours].
- **Steps:** the four rows of the table below, each a single pass [§4.2].
- **Loop:** none stated (U-INT-3) [§4.2].
- **Stopping rule:** not applicable [§4.2] [ours].
- **On exhaustion:** not applicable [§4.2] [ours].
- **On failure:** a rule-violating solution is discarded, and a whole task can be lost [§4.2] [fn. 2].
- **Gaps:** A-INT-1, A-INT-2, A-INT-3, U-INT-1, U-INT-2, U-INT-3 [§4.2].

| ID | CoE check | The mechanism, quoted | Where it sits | Reads → writes | Enforced by |
|---|---|---|---|---|---|
| P-INT-1 | Score verification | "the Coding Agent is prompted during the experimentation phase to output self-contained, reproducible scripts and execution instructions" [§4.2] (tex:sections/4_experiment.tex:43) | every coding agent that runs experiments [inferred] [§4.2] | nothing → scripts and run instructions in the codebase [§4.2] | a prompt, "ensuring full reproducibility without requiring additional post-hoc refinement" [§4.2] |
| P-INT-2 | Specification compliance | "a validation filter that uses the Coding Agent to detect and discard rule-violating solutions immediately after experimentation" [§4.2] (tex:sections/4_experiment.tex:43) | after experimentation; which experiments is U-INT-1 [§4.2] | solution code and task rules (U-INT-2) → keep or discard [§4.2] | an agent run as a filter [§4.2] |
| P-INT-3 | Reference verification | "a search-augmented LLM identifies hallucinated citations, enabling the Writer Agent to ground and correct the bibliography using live search results" [§4.2] (tex:sections/4_experiment.tex:43) | on a manuscript; when is U-INT-3 [§4.2] | bibliography and live search → a corrected bibliography [§4.2] | an LLM with search, then the Writer Agent [§4.2] |
| P-INT-4 | Method–code alignment | "the Coding Agent audits the repository against the manuscript to produce an audit report, which the Writer Agent then uses to rectify any discrepancies in the method section" [§4.2] (tex:sections/4_experiment.tex:43) | on a manuscript with its code; when is U-INT-3 [§4.2] | C_best and P_new → an audit report, then a corrected method section [§4.2] | the Coding Agent, then the Writer Agent [§4.2] |

### What they change, and what they stop · P-INT-5

- **Claimed effect.** "removing these refinement agents leads to sporadic audit failures" [§4.2] (tex:sections/4_experiment.tex:43); the counts are in Table 7, which claims.md assesses [Tab. 7] [ours].
- **A task-level consequence.** Without the specification filter the engine completes one more task, but "since the corresponding codebase contains reward hacking, it must be filtered", and Table 7's denominators move from 50 to 49 [fn. 2] (tex:sections/4_experiment.tex:43) [Tab. 7].
- **Appendix B's account.** The engine blocks evaluator tampering "via a reproduction re-run (I1), a protocol-immutability audit (I2), and a method-code alignment audit" (I4) "rather than a prompt-level list of prohibitions" [App. B] (tex:sections/appendix.tex:236-238); Table 15 marks changing the evaluation protocol as forbidden by audit [Tab. 15] (tex:sections/appendix.tex:186).
- **Experiments no mechanism names.** Ablation code, rebuttal code and A_FullEng's refinements are experiments too; whether the filter and the reproducibility prompt reach them is U-INT-1 [§3.4] [§3.5] [§4.2].

## Gaps found here

- **A-INT-1 · INCONSISTENT · Is reproducibility a prompt or a gate?** §4.2 meets score verification because "the Coding Agent is prompted during the experimentation phase to output self-contained, reproducible scripts and execution instructions", "ensuring full reproducibility without requiring additional post-hoc refinement", and calls the audit "a post-hoc evaluation framework" [§4.2] (tex:sections/4_experiment.tex:41) (tex:sections/4_experiment.tex:43).
  - Appendix B instead says the engine blocks such failures "via a reproduction re-run (I1), a protocol-immutability audit (I2), and a method-code alignment audit" (I4), "rather than a prompt-level list of prohibitions" [App. B] (tex:sections/appendix.tex:236-238).
  - Reading 1: inside the loop reproducibility is only prompted, and re-runs happen in post-hoc evaluation [§4.2].
  - Reading 2: the engine re-runs code and audits the protocol as gates before it accepts a result [App. B].
  - Decision forced: whether our engine re-executes results as a gate [ours].
- **A-INT-2 · AMBIGUOUS · Which Writer Agent repairs the paper.** §4.2 has the Writer Agent fix the bibliography and the method section [§4.2] (tex:sections/4_experiment.tex:43); Figure 3's *Writer Agent* box holds *Initial Drafter* and *Draft Enhancer* [Fig. 3] (image), which run on Gemini by default and on Claude Code [App. A.2].
  - Reading 1: the Initial Drafter, right after drafting [§3.5]. Reading 2: the Draft Enhancer, inside or after the review loop [§3.5] [App. A.2].
  - Decision forced: which agent owns the repairs, on which model [ours].
- **A-INT-3 · AMBIGUOUS · Which Coding Agent runs the filter and the audit.** §4.2 says the Coding Agent three times and never says which one [§4.2] (tex:sections/4_experiment.tex:43).
  - Reading 1: the agent that ran the experiment checks its own solution [§4.2].
  - Reading 2: a separate Claude Code session per check, as "whenever coding capabilities are required" suggests [§4.2] (tex:sections/4_experiment.tex:46).
  - Decision forced: whether the checker is independent of the code's author [ours].
- **U-INT-1 · UNSPECIFIED · Where the specification filter runs, and what discarding does.** The filter runs right after experimentation, but after which experiments (subset, full set, ablation, rebuttal, A_FullEng) is not said [§4.2] (tex:sections/4_experiment.tex:43). Whether a discarded solution becomes a `Bad` idea or ends the task is not said either; footnote 2 shows a whole task filtered out [fn. 2]. Decision forced: the filter's hook points and its verdict's effect [ours].
- **U-INT-2 · UNSPECIFIED · Where the task rules come from.** The check "ensures that solution code adheres strictly to task rules without reward hacking" [§4.2] (tex:sections/4_experiment.tex:41), but no stage produces task rules and G's contents are unspecified (U-TOP-1) [§3]. Decision forced: a rule file per task [ours].
- **U-INT-3 · UNSPECIFIED · When the reference and alignment repairs run.** After the initial draft, after each enhancement, once before export, or again after the meta restart: none is stated [§4.2] [§3.5] [§3.6]. Decision forced: the hook points of both repairs [ours].
