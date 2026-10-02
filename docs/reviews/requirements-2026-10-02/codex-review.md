# Codex review of task 2's requirements, revision c2ad177

Run on 2026-10-02 with `codex review`, model `gpt-6-astra`, reasoning effort high, on `git diff claude/paper-analysis...HEAD`. Its output follows verbatim, except that the absolute path of the reviewing machine's worktree, which prefixed each file reference (10 times), is cut so that each path is relative to the repository.

Gate: FAIL (4 findings marked P1, 6 marked P2).

---

All three requested commands pass, but targeted mutations expose checker defects. Several requirements and acceptance tests also contradict the specified control flow or integrity guarantees.

Full review comments:

- [P2] Validate table-row width before indexing cells — playground/paper/requirement_coverage.py:340-340
  Removing the final `Carried by` cell from the self-test's decision row raises `IndexError` here instead of reporting the malformed row. Register and pending-table parsing have the same unchecked indexing. Check row lengths first and add truncated-row self-tests.

- [P2] Validate abbreviated range endpoints before expanding IDs — playground/paper/requirement_coverage.py:196-199
  Changing the clean fixture's `P-AAA-1 … 2` to `P-AAA-1 … 02` still returns zero problems. The regex checks only fully prefixed IDs, while `ids_in()` silently normalizes the padded endpoint. Validate both range endpoints and add this malformed-padding case to the self-test.

- [P1] Allow the rollback required after an ablation rejection — docs/requirements/05-state.md:28-30
  After `Refine → guard accepts → Reject`, R-STG-9 requires restoring the previous core state. This requirement and its test prohibit that write: restoration is neither selection nor a newly accepted refinement, and the older result would fail the improvement guard. Add an explicit audited rollback transition and test that sequence.

- [P1] Revalidate earlier manuscript gates after later repairs — docs/requirements/06-integrity.md:111-111
  An alignment repair can introduce a typed measurement or fabricated citation after provenance and reference checks have passed. Rechecking only alignment and compilation then exports a manuscript that violates R-INT-5 and R-INT-8. Require all gates to pass on the final manuscript version, retaining an overall repair bound; this also preserves the verified-results rule in [CLAUDE.md:46](../../CLAUDE.md#L46).

- [P1] Exempt the sealed baseline check from the pre-freeze test — docs/requirements/06-integrity.md:43-43
  R-STG-3 requires a report-role baseline check before round 0, and R-INT-3 explicitly permits it. This test instead forbids every pre-freeze report job and report-role record, so a compliant baseline fails it. Scan only agent-visible material, allow the sealed baseline job, and test refusal of an unauthorized candidate report job.

- [P1] Remove the unavailable test gain from the ablation-reject case — docs/requirements/07-measurement.md:20-20
  A selected idea's ablation `Reject` ends the task before the tail, so it never receives the test event whose report-role records R-MEAS-1 and R-MEAS-2 require. The expected `no, yes, no` therefore needs an impossible fixture or an unauthorized report evaluation. Define the missing-gain convention for this failure and test that instead.

- [P2] Leave the tampered file changed until the next hash check — docs/requirements/05-state.md:14-14
  If the file is edited and restored between jobs, its hash at the second job matches the registered hash; the specified start-of-job check cannot detect that history. Nor can that edit affect the twin's next evaluation after restoration. Run the second job while the file is changed, then restore it before the twin's final check.

- [P2] Exhaust first-pass budgets before testing their reset — docs/requirements/03-stages.md:187-187
  This scenario never spends the first pass's ablation budget. With an initial ablation `Good`, even an implementation that never resets N_abl permits the second-pass refinement, so the test passes for the wrong reason. Spend N_abl in pass one before asserting another refinement in pass two; similarly exhaust N_peer before checking its reset.

- [P2] Separate filesystem permission testing from verdict authority — docs/requirements/06-integrity.md:103-103
  Making the judge's workspace writable permits the planted file, but cannot make its verdict count: R-INT-9 independently requires the reporter to ignore verdicts outside engine-written records. The twin therefore cannot satisfy its expected outcome by disabling permissions alone. Assert successful writing in the permission-off twin while still ignoring that verdict, and test provenance separately.

- [P2] Explicitly bypass margin admission for the zero-margin control — docs/requirements/07-measurement.md:93-93
  With positive baseline spread and positive k, R-RUN-6 rejects a zero margin at configuration load, before this mock run reaches either veto. Specify a deliberately disabled noise-floor validation in the control twin, or test the comparison function directly; otherwise the required zero-margin experiment cannot run as written.
