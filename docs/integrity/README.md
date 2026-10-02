# Evaluation integrity (TODO task 6)

**For** the owner of this folder (the `evaluation-integrity-engineer` persona), its reviewers, and
the sessions of tasks 2 and 3 that build on its decisions. This file is the one brief they all
follow, so that each of them solves the same problem.

## The documents

| File | Holds | Written by |
|---|---|---|
| [blocking-decisions.md](blocking-decisions.md) | the index of task 6's `P0` part: the terms, every rule's ID, the rules that cross the four decisions, and what stays open | `evaluation-integrity-engineer` |
| [decisions/](decisions/) | one file per decision: U-INT-4, U-TOP-5, A-INT-1 and A-INT-3 | `evaluation-integrity-engineer` |
| README.md | this brief: the requirements of the decisions, and their acceptance tests | the coordinating session |

Task 6's `P1` part (the per-stage threat model, the verified-results table the writer sees,
deterministic gains, the reporting judge, the audit's settings) adds its own files here later.

## Why these four come first

Four rows of the decision register, [docs/paper/unspecified.md](../paper/unspecified.md), belong
to task 6 and block task 3. Task 3 cannot write the contracts of the evaluation harness or of the
integrity audit until they are decided.

| Row (aliases) | The question | Rank in task 3's order |
|---|---|---|
| U-INT-4 (U-ART-16) | who computes every metric the engine reads or reports | 3: who produces the results, and on which data |
| U-TOP-5 (U-NOTE-1, U-ART-5) | which data split each decision in the loop reads | 3 |
| A-INT-1 (A-NOTE-10, A-ART-2) | integrity as gates inside the run, or only as a post-hoc audit | 3 |
| A-INT-3 (U-ART-9) | which agent checks the code, and the post-hoc auditor kept apart from the in-loop fixer | 8: where the integrity checks hook in |

Each row already carries a proposed decision. It is a proposal to this task, never the paper's
statement, and this task confirms it or replaces it.

## The evidence

Read the sources, never a summary of them (`docs/paper/README.md`, "Sources, and which one wins").

- **The full entries** behind each row:
  - `docs/paper/stages/07-integrity.md`: A-INT-1, A-INT-3, U-INT-4, and the five enforcement
    classes;
  - `docs/paper/analysis.md`: U-TOP-5 in section 10.1, and the table of every decision in the loop;
  - `docs/paper/artifacts.md`: U-ART-5, U-ART-9, U-ART-16, A-ART-2, and pages 40 to 50;
  - `docs/paper/note-check.md`: U-NOTE-1 and A-NOTE-10.
- **The measurement side,** in `docs/paper/claims.md`: P-EVAL-2, P-EVAL-10, U-EVAL-1 and U-EVAL-5.
- **The paper:** §4.2 "CoE Integrity Audit", Table 7 and footnote 2, and Appendix B with Table 15.
  Its TeX is in `docs/paper/source/`, and the PDF text is in `.cache/` after
  `bash playground/paper/fetch_sources.sh`.
- **The audit Table 7 follows,** ScientistOne (arXiv:2605.26340v1) §5, specified by reference. The
  same script caches its TeX in `.cache/refs/2605.26340v1/src/`. Its §6 settings (five runs, the
  tolerance) are its own practice, not the definition.
- **What task 1's integrity review already found:** `docs/reviews/paper-analysis-2026-09-27/`,
  the two `evaluation-integrity-engineer*.md` reviews and their closure check.

## Requirements of `blocking-decisions.md`

Each requirement has the test that shows it is met.

| ID | Requirement | Acceptance test |
|---|---|---|
| R1 | Each of the four rows gets one decision, with four parts: the choice, the attack it stops, a control that proves it works, and the road not taken as `⛔ WHY NOT`. | Every decision shows all four parts, and each decision file holds at least one `⛔ WHY NOT` line. |
| R2 | A choice is a set of rules, each stated as an invariant that can be checked: who may read, write or compute what, and when. Each rule has a stable ID that task 2 can cite. | A reviewer can turn each rule into a test, with no rule that says only "should" or "ensure". |
| R3 | Each guard is enforced by the setup, never by a prompt. Each guard names its class, one of the five in `stages/07-integrity.md`: prompt, LLM filter, LLM fixer, post-hoc LLM audit, or setup. An LLM check counts as detection, with a rate to measure, never as enforcement. | No rule rests on a guard of class "prompt". Every LLM guard says how its miss rate is measured. |
| R4 | Each control proves that it ran. It names the attack it plants and the outcome with the guard removed, where the attack succeeds, and with the guard in place, where it fails. It says whether it runs in mock mode for $0; if not, what it costs. | Every control has both outcomes, stated before it is run. |
| R5 | Each decision states how it relates to the paper: what the paper does, classified as SPECIFIED, UNSPECIFIED, AMBIGUOUS or INCONSISTENT with its quote, and where our rule departs from it. For A-INT-1, both readings are quoted, and the resolution is marked as ours. | `python3 playground/paper/check_citations.py docs/integrity/blocking-decisions.md docs/integrity/decisions/*.md` reports 0 problems: every unit cites its location or carries `[ours]`, and every quote is verbatim. |
| R6 | Each decision is compared with its row's proposal. Where it changes that proposal, it says so and why. | A reviewer finds each of the four proposals confirmed or replaced, with the reason. |
| R7 | Each decision names the rows it constrains elsewhere in the register, without deciding them, such as A-FULL-1, U-BASE-1, U-BASE-2, U-SUB-2, U-INT-1, U-INT-3, A-ABL-3, U-TOP-1, U-ART-15, U-ART-12, U-EVAL-1 and U-NOTE-4. | Each decision lists those rows, and the constraint each one receives. |
| R8 | The rules are rules, not a component design. They state what the harness and the audit must guarantee, and leave the interfaces, the components and their boundaries to task 3. | The `system-architect` review confirms that task 3 can write both contracts without deciding any of the four questions again, and that no rule fixes a component boundary it does not need. |
| R9 | Each decision states its cost: compute, money and wall-clock, at least in order of magnitude. It also states every task it makes inadmissible, such as a task with no validation split, or a task whose metric the harness cannot compute. | The `research-engineer` review finds each cost and each admissibility rule, with no number left without its sample. |
| R10 | The document is structure, not prose: rules, tables and the decision points with their thresholds, and pseudocode with a failure branch for every step of any new stage. Each file stays under 600 lines, split by decision, never into halves that must be read together. | `wc -l` of each file is under 600. |

## Questions each decision must answer

A decision that leaves one of these open says so, and says why.

**U-INT-4, who computes every metric.**
- What agent code hands the harness, and what it may never do: compute a number that a decision
  reads or a report quotes.
- Who produces the baseline's numbers, and from which code: the task's own code at its pinned
  commit, or an agent's adaptation of it.
- How metrics that are not a function of predictions are measured: wall-clock and throughput,
  numbers from an LLM judge, and returns from rollouts.
- What a critic may read that an agent wrote, such as its logs and its own report, without that
  text carrying a number into a decision.
- What is locked and hashed, when the hashes are checked, and what happens on a mismatch.
- Who may write a result, and what a result record holds.
- Ablation variants and rebuttal experiments, and not only the main result.

**U-TOP-5, which split each decision reads.**
- The data roles a task defines, and who may read each one.
- How the paper's subset and full set map onto those roles.
- Every decision in the table of `analysis.md`, each with the split it reads.
- A benchmark that has no validation split, and who builds one, before which step.
- What "the test set is used once" counts: per task run, which candidates, and which events. In
  particular, whether the check that the baseline reproduces (U-BASE-2) may read the test split.
- What the writer sees, before and after the test set is scored, and what may still change once
  test numbers exist.
- Repeated engine runs on one task (U-EVAL-4): no run is chosen by its test number.

**A-INT-1, gates in the run, or a post-hoc audit.**
- Which checks block inside the run, which only measure after it, and why each sits where it
  does.
- What a re-run proves once the harness computes every metric, and what it still has to prove.
- What a failed gate does, and what a failed post-hoc audit does to the numbers we report.
- What a post-hoc audit of the final artifact alone misses: the intermediate results that steered
  the search.

**A-INT-3, the auditor kept apart from the fixer.**
- The roles that must be separate (the author, the in-loop checker and its fixer, the post-hoc
  auditor), and what separate means: session, context, model, prompt, permissions, and which way
  information flows.
- Whether the engine may ever see the post-hoc auditor's prompt or its verdicts.
- Where each verdict is written, and who may write there.
- How the auditor's own error rate is measured.

## Conventions

- **Cite as `docs/paper/README.md` prescribes:** location tags, TeX anchors, exact short quotes,
  `[Ref: meng2026scientistone §5]` for the delegated source, and `[ours]` on every statement of
  our own. Never let our reading pass as the paper's.
- **Refer to the register by row ID,** and link the full entries rather than copy them.
- **Scope.** Change only the four rows of `docs/paper/unspecified.md` named above, and only to add
  a pointer to the decision. Never edit `docs/requirements.md`, which belongs to task 2. A
  component design belongs to task 3.
- **Writers do not run git.** The coordinating session commits.
