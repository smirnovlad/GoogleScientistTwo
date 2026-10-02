<!-- The third /codex pass on claude/engine, on the follow-up commit only (f470f27...36de8dc), gpt-6-astra at high effort, 2026-10-02 evening. Saved verbatim; only the worktree's machine path is replaced by <engine>. -->
GATE: PASS on P1 (0 P1, 3 P2)

The patch leaves a budget-accounting regression and bypasses binary fallback during automatic resume; the timeout regression test also misses its claimed integration. All 26 logic-only end-to-end/CLI tests passed with infrastructure mocked, but real infrastructure validation was restricted by the environment.

Full review comments:

- [P2] Cancel reservations when retry preparation fails — <engine>/scientisttwo/runtime/agents.py:255-258
  If `before_attempt` fails while recreating a retry workspace or temporary directory, admission has already journalled an attempt that never reached the backend. Its reservation remains occupied, and restarting counts it permanently as `interrupted`, potentially preventing resume at the call/session cap. Complete preparation before admission or durably cancel unstarted reservations. This preserves the budget-accounting requirement in [CLAUDE.md:63–64](CLAUDE.md#L63-L64).

- [P2] Revalidate the pinned binary after automatic waits — <engine>/scientisttwo/cli.py:98-99
  If another Claude installation session updates and removes the pinned binary while `--wait` sleeps, this callback reuses the original backend with its nonexistent executable path. The new fallback only runs in `make_backend`, so automatic resume bypasses it and fails on the next call, although a manual resume succeeds. Revalidate or refresh the Claude backend before preparing each automatic resume, consistent with [CLAUDE.md:61–62](CLAUDE.md#L61-L62).

- [P2] Exercise task timeout propagation through a coding unit — <engine>/tests/test_backends.py:504-507
  This D7 regression test supplies `timeout_s=60` directly to a reasoning agent; it never loads a task or calls `Ctx.code`. Removing the task-timeout forwarding from `Ctx.code` in memory still leaves this test passing, so the original ignored-task-timeout bug can return undetected. Exercise a coding/writer unit with a task timeout and assert the backend receives it, including the explicit routing override. See the test-confirmation requirement in [CLAUDE.md:69–70](CLAUDE.md#L69-L70).
