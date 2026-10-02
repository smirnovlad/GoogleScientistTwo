# Codex review of the fourth revision (fd9bcf9..4ac9a04)

Run 2026-10-02 with `codex review`, model gpt-6-astra, reasoning effort high, the range named in the instructions. The verdict and findings below are verbatim, except that absolute paths of the reviewing machine are cut to repository paths.

Coverage, all 54 self-tests, and citation checking pass; temporary-copy mutations confirmed the intended checker fixes. The requirements still contain an incorrect admission-reuse rule, an incompatible acceptance outcome, and incomplete synchronization of the revised contracts.

Full review comments:

- [P1] Recheck changed published numbers without rescoring report — docs/requirements/03-stages.md:91-91
  When only a published reference number changes, the baseline key stays unchanged, so this rule and its acceptance test skip the comparison entirely. IR-15.2 at adc3484 explicitly requires comparing the new reference against the cached sealed values and counting another admission attempt, without reading report again. Otherwise admission retains a stale pass or failure. Restrict reuse to the scored values and add a changed-reference fixture.

- [P1] Align the baseline retry test with the admission outcome — docs/requirements/08-operation.md:69-69
  The permanently failing baseline fixture still requires `error after retries`, but revised R-RUN-5 explicitly assigns preparation failures to `not admitted`, and the Baseline Coding Agent's failure-table row now agrees. No run exists at that point. An implementation following the new outcome contract therefore fails this acceptance test; update the fixture to require admission refusal with no run started.

- [P2] Include a per-unit discriminator in audit-scoped keys — docs/requirements/05-state.md:63-63
  For audit-scoped agent calls, the listed key contains only the audit identity, which IR-36.1 at adc3484 defines as `(bundle hash, configuration hash)`. Different checks within that audit consequently have no distinct unit keys; the harness-job exception does not cover these agent calls. Add the check and applicable row/input identifiers so completion and replay cannot confuse separate checks. This is also necessary for the resume invariant in [CLAUDE.md:61–62](../../CLAUDE.md#L61-L62).

- [P2] Update the shared rule's ablation reference too — docs/requirements/03-stages.md:161-161
  This precondition now deliberately reads C_best's selected, released search records, but R-RUN-6 in `01-run.md:88` still defines its reference as a fresh fit of C_best. The two normative requirements therefore specify different operands, leaving the previous review's fresh-fit problem partly unresolved. Update the shared comparison rule to name the released records and reserve independent attribution fits for the test event.
