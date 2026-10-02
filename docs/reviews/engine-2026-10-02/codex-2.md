<!-- The second /codex review gate on claude/engine (origin/claude/paper-analysis...f470f27), codex-cli with gpt-6-astra at high effort, 2026-10-02 17:2x. A first attempt the same hour was stopped by OpenAI's classifier ('flagged for possible cybersecurity risk') and returned nothing; this is the rerun with a plainer prompt. Saved verbatim; only the worktree's machine path is replaced by <engine>. -->
GATE: FAIL (3 P1, 7 P2)

The fixes improve the original findings, but file-boundary escapes, repeat-payment recovery gaps, budget overruns, and stale-result replay remain. Validation passed 54 targeted tests and 23 logic-only end-to-end tests with infrastructure mocked; real sandbox/end-to-end checks were blocked by this environment's restrictions.

Full review comments:

- [P1] Reject build-created PDF symlinks before exporting — <engine>/scientisttwo/stages/export.py:98-99
  A writer-controlled `.latexmkrc` can create `main.pdf` as a symlink to a protected file and exit successfully. This happens after workspace sanitization; `compile_pdf()` only checks existence, and this unsandboxed `copy2()` follows the link. A probe exported a private fixture's contents instead of a PDF. Validate the source as a regular, non-linked file and replace the destination without following links. C1 therefore remains incomplete for build outputs; see [CLAUDE.md:44](CLAUDE.md#L44).

- [P1] Reserve budget capacity atomically before admitting calls — <engine>/scientisttwo/runtime/budget.py:168-173
  With parallel execution, multiple calls pass this check while completed-call totals remain unchanged. `started()` journals attempts but reserves no capacity. A two-worker probe with both call and coding-session caps set to one completed two calls. Atomically check and reserve capacity, counting in-flight attempts without counting them again at completion. Both shipped profiles enable parallel execution, so this violates the bounded-cost requirement in [CLAUDE.md:63–64](CLAUDE.md#L63-L64).

- [P1] Recover successful attempts when the unit save fails — <engine>/scientisttwo/runtime/agents.py:278-284
  If the engine dies after the successful ledger append but before `store.put()` completes, resume finds no unit and calls the backend again. Injecting a unit-save failure produced two successful ledger entries for the same completed work; coding recovery also discards the pending workspace before retrying. C4's test only crashes after the unit was stored. Persist replayable output with the successful-attempt record and recover it before another call, as required by [CLAUDE.md:61–62](CLAUDE.md#L61-L62).

- [P2] Validate cached result identity in the rejection path — <engine>/scientisttwo/harness/harness.py:142-144
  When a missing workspace is regenerated on resume and its replacement violates a deterministic rule, `Ctx.evaluate()` calls `reject()` under the original result key. This branch returns the old result without checking its commit or status, potentially assigning a previously successful score to the newly forbidden version. Apply the same commit validation used by `evaluate()` instead of replaying an unrelated result. This preserves the recorded-code reproducibility invariant in [CLAUDE.md:49](CLAUDE.md#L49).

- [P2] Preserve usage-window metadata on failed CLI calls — <engine>/scientisttwo/runtime/agents.py:322-325
  C10 preserves dollars and tokens, but failures still discard the observed rate-limit windows: `_ledger()` uses an empty `raw` mapping when the backend raises. A failed structured-output call reporting five-hour utilization of 0.99 admitted another call under a 0.98 ceiling because `Budget.windows` remained empty. Carry rate-limit metadata through backend exceptions into the ledger so retries and resumes honor known ceilings; see [CLAUDE.md:63–64](CLAUDE.md#L63-L64).

- [P2] Include schemas and tools in the replay fingerprint — <engine>/scientisttwo/runtime/agents.py:188-190
  Changing a snapshotted agent's schema or tool list does not change this hash, so strict replay silently returns an answer produced under another contract. A probe changed the schema's required field and received the old, now-invalid output without `InputsChanged` or validation. Include the schema and relevant agent settings in the fingerprint used by both reasoning and coding replay. The current check incompletely enforces the reproducibility rule in [CLAUDE.md:49](CLAUDE.md#L49).

- [P2] Apply the task's coding-session timeout — <engine>/scientisttwo/runtime/agents.py:233-236
  A task's `timeouts.coding_session_seconds` is loaded into `Task.coding_timeout_s` but never used afterward. Calls receive only the routing timeout, so a task requesting 60-second coding sessions, as the toy fixture does, instead gets the default 2,400 seconds. Wire the task setting into call construction with explicit routing-override precedence rather than silently ignoring its session bound; see [CLAUDE.md:63–64](CLAUDE.md#L63-L64).

- [P2] Export the complete patch without the prompt-size cap — <engine>/scientisttwo/stages/export.py:101-101
  `Ctx.diff()` truncates at 200,000 characters for model prompts, but this also applies that truncation to the downloadable patch. A valid 256 KB source diff produced an exported patch that `git apply --check` rejected as corrupt. Use the uncapped workspace diff for this artifact, as the variant exports already do, so larger methods remain reproducible from their patches; see [CLAUDE.md:49](CLAUDE.md#L49).

- [P2] Check the descriptor type before wrapping it as a file — <engine>/scientisttwo/stages/manuscript.py:144-146
  If a writer leaves a directory named `main.tex`, `references.bib`, or `results.tex`, `os.open()` succeeds but `os.fdopen()` raises `IsADirectoryError` before the regular-file check runs. Consequently manuscript reading or auditing crashes instead of treating the entry as missing or edited, and replay preserves the offending version. Perform `fstat()` before `fdopen()` and close non-regular descriptors.

- [P2] Prove the detached cleanup-test child actually ran — <engine>/tests/test_backends.py:189-191
  Both observations treat a missing heartbeat file as zero, so the test passes when the detached child never starts successfully. Making the stand-in child exit before its first heartbeat still passed this test. Have the fixture acknowledge a live, heartbeating child before emitting the CLI result, then assert cleanup stops it. Otherwise the test does not establish process-tree termination, contrary to [CLAUDE.md:69–70](CLAUDE.md#L69-L70).
