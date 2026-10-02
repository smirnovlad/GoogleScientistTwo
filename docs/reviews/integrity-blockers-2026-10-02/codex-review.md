# Record: the Codex review gate (2026-10-02)

- **Required by** the parent `CLAUDE.md`: a `/codex` review of the diff before the PR.
- **Run:** `codex review` (codex-cli 0.153.4) on `git diff claude/paper-analysis...HEAD` at
  `1b6adac`, with `-c model="gpt-6-astra"` (the configured `gpt-6-sol` is refused on this ChatGPT
  account) and `model_reasoning_effort="high"`. The range is named in the instructions, since
  `codex review` refuses instructions together with `--base`.
- **Gate:** FAIL, one [P1] and three [P2].
- **Record:** Codex's output, verbatim below, with one change: its links named each file by its
  absolute path on this machine, and those 4 prefixes are cut to paths relative to the
  repository root, since this repository never holds a path from someone's machine.

---

## Pass 1

The design contains conflicting job-identity and correction-scope rules, plus audit-noise and control-calibration problems. Citation checks and simulation scripts passed; no matching private-data leaks were found, and the register changes are limited to the four pointer additions.

Full review comments:

- [P1] Version task-scoped identities when the runner changes — docs/integrity/decisions/u-int-4-who-computes.md:44-44
  When only the runner changes, IR-6.4 preserves the manifest and baseline key. Consequently, E_base's task-scoped job identity under IR-32.1 is unchanged, and IR-33.1 requires returning its existing record instead of executing this re-score. The subsequent re-admission has the same collision. Include the runner version in the relevant identities, or define a separately identified verification operation and versioned re-admission, so this check actually executes rather than comparing cached results.

- [P2] Calibrate audit noise for the rows being compared — docs/integrity/decisions/a-int-1-gates-or-audit.md:42-42
  The packaging measurement uses E_base (as the cost table specifies), but its noise need not describe subsequently generated methods. For a frozen, deterministic baseline, σ_r can be zero while an honest trained candidate has nonzero same-seed numerical noise; this rule then gives that candidate zero tolerance and classifies ordinary variation as an integrity failure. The √2 formula also assumes equal, independent noise in both rows, which shared-backbone comparisons do not guarantee. Define an applicable row-specific calibration and propagate both variances and their covariance into the paired tolerance.

- [P2] Account for all audited seeds in the control threshold — docs/integrity/decisions/a-int-1-gates-or-audit.md:85-85
  The stated 0.0026 probability assumes one comparison per honest row, whereas IR-23.2–IR-23.3 require checking every report seed. With five independent seeds and one setting, an honest row fails with probability `1 − (1 − 0.0027)^5 ≈ 0.0134`; three or more failures among 100 rows occur about 15.2% of the time, not 0.26%. Calibrate the control for its actual seeds and settings, or explicitly describe it as a single-comparison unit control and add coverage for the complete row-level audit.

- [P2] Allow task-scoped baseline correction jobs — docs/integrity/decisions/u-top-5-which-split.md:45-45
  When a scoring defect affects E_base, IR-41.2 requires its corrected identities to execute once in task scope, and IR-5.3 explicitly assigns their records there. This exhaustive allowlist permits correction events only in run scope and refuses everything else, so the required baseline correction cannot execute. Include task-scoped E_base corrections in the permitted correction kind while preserving their once-per-baseline-key identity.
