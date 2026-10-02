# Review: evaluation-integrity-engineer, wave 2, the engine analysis (2026-09-27)

- **Reviewed:** `docs/paper/analysis.md` and `docs/paper/stages/01-seed-ideas.md` to
  `07-integrity.md`, at commit `6c10e1f`. The same reviewer's wave-1 review is
  `evaluation-integrity-engineer.md`.
- **Lens:** can an agent move a reported number without a better method, and would we notice.
- **Record:** the reviewer's final message, verbatim below, with one change: its first line named
  the reviewed file by an absolute path, shortened here to `docs/paper/analysis.md`, because this
  repository never holds a path from someone's machine.

---

# Integrity review, wave 2: analysis.md and stages/01–07

Reviewed: `docs/paper/analysis.md` and `docs/paper/stages/01-seed-ideas.md` to `07-integrity.md`. No file was edited.

**Verdict.** No finding is a BLOCKER.
- **Right as written:** the new "Enforced by" column in stages/07, and the gaps A-INT-2, A-INT-3, U-INT-1, U-INT-2, U-SUB-1, U-BASE-2, U-PEER-4, U-META-2, A-ABL-3 and A-TOP-3.
- **Missing:**
  - The engine analysis never says whether any decision reads validation data or test data.
  - The decision table does not say who produced each decision's input, or what guards it.
  - No gap records that there is no fixed evaluator.

## Findings

**MAJOR-1 · analysis.md §4.2 table and its "Consequence" bullet; stages/02 P-SUB-3, P-FULL-2; stages/03 P-SEL-1; stages/04 P-ABL-5.**
- **Problem:** nothing says that every decider reads the same benchmark that gets reported. "Validation" appears only in a filter's name and in "final validation". U-NOTE-1 and U-ART-5 exist, but outside the engine analysis.
- **Evidence:**
  - Full-set agents do "final validation and engineering against the full benchmark", after "hyperparameter tuning or code adjustments" on the subset [§3.2].
  - The Selector compares ideas "evaluated on the full benchmark", and the paper calls this "the optimization process" [§3.3].
  - The Result Comparison Agent judges E_new against E_best, and E_best is what gets drafted [§3.4] [§3.5].
  - The only guard inside the loop, the filter, reads "solution code" [§4.2]. It never sees the history of which ideas were selected.
- **Fix:**
  - Add a "Produced by" column: the agent's own code.
  - Add a "Data" column: the reported benchmark, with no split stated.
  - Add a "Guard" column: none except the code filter.
  - Add a TOP gap that links U-NOTE-1.

**MAJOR-2 · stages/07 P-INT-1..4; analysis.md §1.1 item 9 ("Integrity is partly a prompt").**
- **Problem:** the classification that my wave-1 MAJOR-7 asked for is only half done. There is no row for the post-hoc audit behind Tab. 7 and no verdict on the setup. The classes also drift ("an agent run as a filter", "the Coding Agent, then the Writer Agent").
- **Evidence:**
  - §4.2 adds only "three dedicated refinement agents alongside careful agent prompt design". §3, §4.2 and App. A.2 describe no sandbox, no read-only evaluation code, no hash and no harness.
  - P-INT-4 repairs the paper, not the code: the Writer uses the report "to rectify any discrepancies in the method section" [§4.2].
- **Fix:**
  - Use fixed classes: prompt, LLM filter, LLM fixer, post-hoc LLM audit, setup.
  - Add the post-hoc audit as a row.
  - Add "setup: none" [ours], and state that the alignment fix edits the paper, not the code.
  - Reword item 9 to "prompts and LLMs only; nothing is enforced by the setup".

**MAJOR-3 · U-TOP-1; stages/07 U-INT-*; A-INT-1's decision ("whether our engine re-executes results as a gate").**
- **Problem:** the analysis never records that there is no evaluator. No task input provides one, and the coders produce E themselves (`E, C = subset_coder(h, C_base)`, §4). The audit the paper cites assumes one exists.
- **Evidence:**
  - In ScientistOne v1, I1 "re-runs the solution on the golden evaluator", and "Each task provides a fixed evaluator". This is my wave-1 MAJOR-1, which you confirmed.
  - Tab. 7 row 1 scores 50/50 on Score Verif. and 1/50 on Spec. Violat., and fn. 2 says that codebase "contains reward hacking". So a re-run passed a hacked result.
- **Fix:**
  - Add U-INT-4: agent code computes every metric.
  - Add the evaluator, the definition of the full benchmark, and the data splits to U-TOP-1.
  - Make A-INT-1's decision "a locked harness computes the metrics". A re-run used as a gate proves only that the code is deterministic.
  - In stages/07, record the procedure the paper adopts by reference: five runs, a tolerance of max(1%, 3σ/|s̄|), a 3-of-5 vote, and the lenient I4 criterion.

**MAJOR-4 · analysis.md §4.2 table: missing rows.**
- **Problem:** the table lists verdicts only. The content decisions that move reported numbers are absent.
- **Evidence:**
  - The drafter and the Enhancer choose what the paper's tables hold, "updating empirical tables and figures" [§3.5].
  - The rebuttal picked its own "50 representative TALENT datasets" [p. 51].
  - The Full-Set Coding Agent adapts code "to run across the entire benchmark suite" [§3.2], so it decides what "entire" means. One trace reports only a "FULL CIFAR-100 benchmark" [p. 40].
- **Fix:** add rows for the numbers in the paper, the rebuttal's data and the full-set scope. Mark each "guard: none in the loop".

**MINOR-1 · U-INT-3.** Say why the timing matters:
- If the repairs run before review, the Enhancer's later edits are never audited.
- If they run after review, the paper that was reviewed is not the paper that is exported.

**MINOR-2 · analysis.md §4 pseudocode.** The filter comment sits after `return`, so as code it could never run. Move it above the return.

**MINOR-3 · A-INT-3.** Also require the post-hoc auditor to be independent of the in-loop fixer (U-EVAL-5).
