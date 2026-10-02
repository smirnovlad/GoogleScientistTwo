# Codex review of the third revision (c2ad177..fd9bcf9)

Run 2026-10-02 with `codex review`, model gpt-6-astra, reasoning effort high, the range named in the instructions. The verdict and findings below are verbatim, except that absolute paths of the reviewing machine are cut to repository paths.

The previous review's concrete scenarios are largely repaired, and coverage, all 52 self-tests, and citation checking pass. However, the revision introduces contradictory requirements and an impossible enforcement outcome; temporary-copy mutations also expose incomplete checker validation.

Full review comments:

- [P1] Allocate independent draws for the ablation confirmation fits — docs/requirements/03-stages.md:156-158
  For a method deterministic given its seed, fitting C_best again on the manifest's search seeds reproduces the selected E_best values, preserving the selection bias this change claims to remove. Moreover, IR-32.1 and IR-33.1 at adc3484 give these jobs the already-released identities, so a compliant runner returns their cached records. A null mechanism whose off-path reproduces E_base can therefore pass attribution whenever its selected gain exceeds the margin; the enforcement test cannot distinguish the guarded and E_best twins. Define independent, pre-registered confirmation draws and compatible identities with task 6, rather than treating a same-seed refit as fresh evidence.

- [P1] Key sealed baseline checks by the baseline key — docs/requirements/03-stages.md:88-88
  A manifest version that changes only a citation or rule's wording must not trigger another report evaluation. IR-15.2 at adc3484 explicitly keys the check by the baseline key, not the manifest version; even a changed published number is compared against cached sealed values. Requiring the check once per manifest version permits unnecessary report reads and can consume the task's bounded admission attempts. Use the baseline-key reuse rule here and add its unchanged-key case to the acceptance test.

- [P1] Preserve the test-event exception for timing metrics — docs/requirements/01-run.md:104-104
  For a time or throughput metric, the cited IR-14.4 explicitly requires E_base to be timed again alongside the frozen rows, following IR-8.1's interleaved comparison. The unconditional instruction to use admission results omits that exception, allowing current method timings to be compared with an older baseline measurement under different machine conditions. Preserve admission-result reuse for other metrics, but require the same-job baseline timing and a corresponding test.

- [P1] Exclude post-test terminal failures from success counts — docs/requirements/07-measurement.md:17-17
  A run whose gain passes the success test but whose tail exhausts its manuscript repairs has a test event and no exported artifact to audit. Neither override here applies, so the second reading still counts it as successful. That contradicts adc3484's IR-39.3 and IR-18.6, which require this terminal outcome to count as failure, and R-RUN-5's acceptance test. Add an explicit terminal-failure override and a positive-gain fixture ending with `test event done, not exported`.

- [P1] Separate the writable-mount twin from the hash-check outcome — docs/requirements/06-integrity.md:38-38
  Making the evaluation mount writable permits the edit but does not let the next scoring use it: the independently required start-of-job hash check detects the change and refuses that job. Thus a compliant engine cannot produce this twin's expected outcome. Assert that the write succeeds while the hash guard still refuses scoring, or explicitly disable both guards for a separate combined attack. This preserves the two independent protections required by [CLAUDE.md:44](../../CLAUDE.md#L44).

- [P2] Define exhausted-retry outcomes for both experiment critics — docs/requirements/03-stages.md:50-50
  The Subset Critic and Full-Set Critic are absent from this supposedly complete failure map: this row covers only coders and engineers, and neither performance critic is an integrity check. R-PRIM-10 now delegates its defaults entirely to this table, so its malformed-critic acceptance case has no configured terminal branch after retries. Add explicit outcomes for both critics, consistent with the structured failure-branch requirement in [CLAUDE.md:65–66](../../CLAUDE.md#L65-L66).

- [P2] Validate row width against the full table header — playground/paper/requirement_coverage.py:363-365
  This prevents indexing crashes but does not fully enforce the new no-truncated-rows guarantee. In a temporary copy of the real files, moving `Carried by` earlier in the decisions table remained valid; deleting the final `Reason` cell from A-TOP-1 then still returned `0 problem(s)`. Since columns are resolved by name, a required column need not be last. Compare the row's width with the complete header and add a reordered-header mutation to the self-test.

- [P2] Parse multi-digit task numbers in attribution checks — playground/paper/requirement_coverage.py:438-439
  The single-digit pattern silently skips attribution checking for multi-digit task numbers. Changing the real R-PRIM-1 dependency from `A-NOTE-1, task 3` to `A-NOTE-1, task 10` in a temporary copy still returned `0 problem(s)`, although the register assigns it to task 3. Parse the complete task number, for example with `\d+`, so incorrect multi-digit owners are compared rather than ignored.
