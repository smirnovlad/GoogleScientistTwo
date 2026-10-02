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

## Pass 2, on `157cec7` (gate: FAIL, three [P1] and one [P2])

The four findings of pass 1 hold as fixed. Verbatim, with local path prefixes cut as above:

The runner-version and task-scoped correction fixes are present, but audit calibration and search-budget counting remain inconsistent. Citation/register checks pass; no secrets, email addresses, absolute local paths, or register edits outside the four pointer additions were found.

Full review comments:

- [P1] Give calibration re-fits distinct, resumable identities — docs/integrity/decisions/a-int-1-gates-or-audit.md:42-42
  The second same-seed fit required here has exactly the same IR-32.1 identity as the first audit re-fit: kind, audit scope/key, runner version, row, arguments, seed and setting are unchanged. IR-33.1 therefore returns the first record instead of executing another fit, and IR-36.1 likewise permits only one release per check × row × seed. Calibration consequently either measures zero differences or violates the release rules. Add a fixed calibration-replicate identifier or separate job kind, with corresponding audit-unit accounting.

- [P1] Account for uncertainty in the estimated audit tolerance — docs/integrity/decisions/a-int-1-gates-or-audit.md:42-42
  The stated z thresholds assume a known Gaussian standard deviation, but σ_r is estimated from only c differences; the cost table explicitly illustrates c = 2. Even with Gaussian honest noise, this does not deliver the claimed 0.0027 row-level false-positive rate. Simulating the specified procedure with five report seeds, true difference SD 1, packaging floor 0.1 and c = 2 flags approximately 34% of honest rows. A reference-fit floor need not bound a candidate's noise. Specify a finite-sample calibrated prediction threshold that accounts for variance estimation and reuse of calibration observations.

- [P1] Count scoring batches rather than individual seed results — docs/integrity/decisions/u-top-5-which-split.md:37-38
  IR-32.1 gives every seed and setting its own identity, but this rule counts released results per identity against the stage's 1 + N_eng limit. With the documented five-seed configuration and N_eng = 2, the first candidate evaluation already needs five releases against a cap of three, before any refinement. It must therefore stop incomplete or fail IR-24(e), despite satisfying IR-9's coverage requirement. Define the capped unit as one complete evaluation batch across its required seeds/settings, while retaining per-identity attempt accounting.

- [P2] Make the clock-randomness control distinguishable from noise — docs/integrity/decisions/a-int-1-gates-or-audit.md:85-85
  Under the revised IR-23.4, each clock-seeded row calibrates its tolerance from its own repeated fits, so stationary clock randomness increases σ_r along with the discrepancies being tested. Even with perfectly known Gaussian noise, such a row is flagged at approximately 0.0027, not the required 99% detection rate; increasing its noise amplitude does not help because the tolerance scales too. Specify an independently detectable violation or revise the claimed detection guarantee, then test both arms using the actual calibration procedure, as required by [R4](docs/integrity/README.md#L63).

## Pass 3, on `1bb01eb` (gate: PASS, four [P2])

The findings of pass 2 hold as fixed. Verbatim, with local path prefixes cut as above:

The calibration identities, batch counting, and revised clock control address the previous findings, but statistical guarantees and isolation claims still need correction. Citation and cross-reference checks passed; no disclosure matches or register edits beyond the four pointer additions were found.

Full review comments:

- [P2] State the distributional assumptions of the audit tolerance — docs/integrity/decisions/a-int-1-gates-or-audit.md:42-43
  The Student-t threshold has the advertised calibration for independent, zero-mean Gaussian differences, but no rule restricts admitted fit noise to that distribution. Even with identical reference and candidate noise, independent Bernoulli(0.01) fit disturbances produce approximately 8.8% flagged rows at M=20 and n=5, rather than 0.27%. IR-23.8's allowance for noisier candidates does not address this same-distribution case. Specify and validate the threshold's applicability, or calibrate it for the admitted noise distribution before using the claimed false-positive rate.

- [P2] Simulate shared calibration estimates for paired gains — playground/integrity/audit_tolerance.py:91-97
  This simulation always draws independent calibration estimates for the two rows, whereas IR-23.4 supplies one estimate per kind of fit. When both rows have the same kind, s_o=s_b; at correlation −1, the comparison reduces to |z|>c·s_k and has the single-row flag rate, approximately 0.00269. Consequently, the control's promised upper rate of 0.00098 is false for a permitted production case. Include shared-estimate cases and correct the control's bound rather than treating this independent-estimate simulation as the worst case.

- [P2] Account for seed-based detection of the scoring role — docs/integrity/decisions/u-top-5-which-split.md:31-31
  Identical paths and environments do not establish this invariant: IR-10.2 gives search and report disjoint seed lists, and fit code receives its seed. A fit can record whether its seed belongs to the known search list in its artifact, allowing predict to distinguish report from search without inspecting either split's inputs. This permits phase-specific behavior despite the claimed setup protection. Add this attack to the controls and either prevent the information flow or classify it as detection-only, consistent with [R3](docs/integrity/README.md#L62).

- [P2] Count exposure through reported tables when retiring auditors — docs/integrity/decisions/a-int-3-checker-and-auditor.md:24-24
  A builder can read final-test integrity verdicts through the reporter's published per-task table, then change an engine prompt without ever reading the audit store directly. The store logs the reporter's identity, not that builder, so this retirement check leaves the auditor eligible despite feedback-driven optimization. This uses the intended reporting path, not administrator access. Track exposure through reporter outputs or retire the auditor conservatively after publication to preserve the [held-out-judge rule](CLAUDE.md#L48).
