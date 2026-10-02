<!-- The infrastructure-engineer persona's review of claude/engine at 7e3f0c3 plus uncommitted edits, saved verbatim on 2026-10-02 as it was handed back. Only machine paths are replaced (<engine>, <scratchpad>, ~), since this repository is public. Its experiment scripts are copied to playground/engine/infra-review/. -->

The engine's happy path is consistent, but the failure paths can't yet be trusted across a crash, a resume or a retry: I found 7 P1 and 4 P2 issues. I reproduced every one (live-run inspection, mock-mode scripts or the fake CLI) except the parts marked as following from the code.

I reviewed `claude/engine` at 7e3f0c3 plus the uncommitted edits. `agents.py`, `common.py`, `coder.py` and `writing.py` changed while I was reviewing; the line numbers below are for the current files, and I re-ran E1 and E5 on the current tree with the same outcome. I modified nothing in the worktree or in `runs/digits-quick-1`. The experiments (E1–E5) are mock-mode or fake-CLI scripts in `<scratchpad>/exp/` (`e1_stale_memo.py`, `e2_budget.py`, `e3_procs.py`, `e4_harness.py`, `e5_git.py`). Every process they spawned was killed and checked gone.

## P1

**1. After a resume, the critic can read an old result for new code, and the unit is paid twice.**
- When a unit runs out of transient retries, it raises `UnitFailed` directly (agents.py:189-192), not through `_fail`. Nothing is stored and nothing goes to the ledger.
- `Ctx.code` still finalizes the version (common.py:129-131).
- On resume the unit runs again and is paid again. `finalize` deletes and replaces the version (workspace.py:66).
- `Harness.evaluate` returns its saved result by key alone (harness.py:149).
- E1: the first run saved eval0 = 0.7600 at commit 716aa1d88c. After resume the version is eb23af8b12, which really scores 1.0000, and the critic reads 0.7600 for 716aa1d88c.
- Same root cause: the stored `inputs_sha256` is never compared on lookup (agents.py:152 vs 161), and manuscript versions are reused by name (writing.py:46, export.py:35). A prompt edit between two runs of the process is replayed silently.
- This nearly happened live: the coder prompts were edited at 13:55:18, five seconds after run.json was written (13:55:13), and run.json records `engine_commit` without `+dirty`. A resume would have used the new prompts with no record of it.
- Fix:
  - When transient retries run out, pause the run (it is not the idea's fault) instead of leaving a half-recorded unit.
  - `evaluate` raises when `result["commit"] != commit`.
  - `rt.run` raises when `inputs_sha256` differs from the stored one.
  - Record the engine commit and the CLI version each time the run is resumed.

**2. Some spending never reaches the ledger.**
- Only a final success (agents.py:211) or `_fail` (233) writes a ledger line. Transient, invalid-output and usage-limited attempts write nothing.
- The caps count only recorded calls (budget.py:92-96).
- E2: with `max_agent_calls=1`, three backend calls ran and one was recorded. When transient retries run out, nothing is recorded at all.
- The ledger line is written after the unit (agents.py:206 then 211) and without fsync (budget.py:119), while the unit is fsync'd. A crash between the two loses the line.
- Fix: write one ledger line per attempt, fsync'd, before `store.put`. Take `equiv_usd` from the result when there is one (an invalid output comes from a result that has a cost), otherwise null.

**3. A partial last ledger line blocks every resume.** budget.py:64-66 runs `json.loads` on every line. E2: a truncated last line makes `prepare` fail with `JSONDecodeError`. Power loss or a full disk during the append causes this. Disk does fill: every version copies the full `.git` (workspace.py:57). Fix: truncate to the last newline and log the repair.

**4. A usage-window pause becomes permanent.**
- `max_hours` is measured as calendar time since `created_at` (orchestrator.py:80, budget.py:97), so paused time counts.
- E2, with the paper profile's caps (7-day ceiling 0.95, `max_hours` 96): the run pauses for 5.0 days. After the window resets, resume pauses again with "wall-clock cap reached (120.0 h / 96 h)", on every attempt.
- Fix: sum the running intervals recorded in run.json's history.

**5. Killing a session misses the processes it started, and nothing stops two engines on one run.**
- In the live run, claude pid 77331 (process group 77331) started its Bash-tool shell as pid 77505 in its own group (77505, stat `Ss`). So `killpg(proc.pid)` at claude_cli.py:116 misses it.
- E3: after `AgentTimeout`, a detached child of the CLI was still alive and still writing.
- Each claude child is started with `start_new_session=True` (claude_cli.py:110). The engine has no signal handler, no pidfile and no lock; grep finds only the two `killpg` calls.
- E3: when I SIGKILLed the engine, its claude child kept running, and it would keep spending.
- From the code (not run): resume then runs the same unit again in the same `<name>.tmp`, which `fresh` deletes and re-copies (workspace.py:56) while the orphan may still be writing there. Two `resume`s on one run would both pay for the same units.
- The live engine (pid 65134) is a plain child of a Claude Code shell (group 65132), so closing that shell would kill it and leave its sessions running.
- Fix:
  - Hold `fcntl.flock(run_dir/run.lock)` for the life of the process.
  - Write each child's process group to disk before the call, and on startup kill any recorded group that is still alive.
  - On timeout, first list the session's whole process tree (`ps` pid/ppid/pgid), then send SIGTERM, wait a grace period, and SIGKILL every group in that tree.

**6. An evaluation can hang the engine.**
- After the timeout kill, `proc.communicate()` has no time limit (harness.py:207).
- E4: with a 2 s timeout, `evaluate()` returned after 15.0 s, which was the full lifetime of a child started in its own session that held stdout open. A child that never exits would block its `Ctx.map` worker forever.
- Fix: send stdout to a file in `eval_dir`, use `wait(timeout)`, and kill all descendant groups.

**7. An agent writing to its own `.git` can stop the run or make it unresumable.**
- The coding sandbox makes the whole working directory writable, `.git` included (common.py:84).
- Git failures in `finalize` or in the diff raise `RuntimeError`, which nothing treats as a unit failure (workspace.py:31-35). `on_done` runs before `store.put` (agents.py:204-206).
- E5, leftover `.git/index.lock`: the run ends in error, and the finished coder unit is paid again on resume.
- E5, `rm -rf .git && git init`: `git diff <task_commit> HEAD` (common.py:148) fails on every resume, so the run can never get past that point.
- Fix: deny writes to `<tmp>/.git` in the coding profile, and turn finalize or diff errors into a unit failure or a failed result.

## P2

**8. A delivered result can be thrown away as a timeout.** claude_cli.py:170 checks the kill reason before it looks at the result. E3: the result arrived at t=0, the CLI lingered, and `AgentTimeout` was raised at 3.0 s and stored as a failure. Fix: once a `result` event is read, use it and then clean up the process.

**9. Retries do not start clean.**
- A coding retry reuses the `.tmp` workspace with the failed attempt's edits still in it.
- Each attempt reopens the same transcript file with `"w"` (claude_cli.py:106, one path per key at agents.py:163), so failed attempts' transcripts are lost.
- Usage-limit waits have no attempt limit (agents.py:181-187).
- Fix: one transcript per attempt, reset the workspace from its parent before a retry, and cap the number of waits.

**10. Environment problems are classified as permanent failures or as multi-day pauses.**
- `_USAGE_ERROR` (claude_cli.py:42) matches `Error: EPERM…` and `Error: ENOSPC…`. These become `AgentFailed`, which is stored and replayed on every resume.
- A stored failure in a stage that does not catch it errors every resume, and there is no `--retry-failed`. Those stages are limitations, seeds, evolver, selector, peer review, rebuttal plan and meta review.
- `_LIMIT_TEXT` (line 36) matches "context limit reached", a string present in the 2.1.287 binary, so that error would pause the run as a usage limit.
- On the live `allowed_warning` event, `_reset_at` returns the 7-day reset (5.6 days away), although the five-hour window resets in 1.8 h.
- `_check_windows` raises forever if the last recorded window has no numeric `resetsAt`, because no call can run to refresh it.
- Fix:
  - Only treat a failure as an argument error when the exit code or the CLI's own usage text says so.
  - Make environment faults pause the run rather than fail a unit.
  - Take the reset time from the window that is actually exhausted.

**11. The sandbox is too open for a multi-day run.**
- Integrity holes:
  - `claude_state` opens all of `~/.claude`, `~/.claude.json` and `~/Library/Caches` for writing (sandbox.py:89-92). That gives agents running with bypassed permissions and network access write access to the user's settings and hooks, the global CLAUDE.md and other projects' memory. Hooks then run unsandboxed in the user's own sessions.
  - Auto-memory is on: the init event reports `memory_paths.auto`, and for reasoning agents it resolves to the user's own GoogleScientistTwo memory folder.
  - The temp folders are writable by every agent and readable by the evaluation, so a result can depend on files outside its commit.
- CLI drift and clutter:
  - The binary recognizes `CLAUDE_CODE_DISABLE_AUTO_MEMORY` and `DISABLE_AUTOUPDATER`; `child_env` (line 51) sets neither. So the CLI can update itself mid-run while run.json records its version only once.
  - Every session leaves a `~/.claude/projects/<slug>` folder (12 from this run).
- Fix:
  - Narrow the writable state to a minimum found by a probe.
  - Set both environment switches.
  - Pin the resolved CLI binary path.
  - Give each unit its own TMPDIR.
  - Hide the temp folders from the evaluation.

## Checked and found sound

- Unit and result files are written atomically (temp file, fsync, rename). Versions appear by rename, and leftover `.tmp` folders are rebuilt. An evaluation can be repeated safely because its result file is written last.
- Unit keys are positional and stable on resume: `Ctx.map` keeps input order, evolution ids come from saved outputs, and parallel units have separate keys and version names.
- A unit failed through `_fail` replays on resume. Pause then resume pays for no finished unit (test at test_e2e_mock.py:113).
- Separate stdin and stderr threads prevent pipe deadlock. Budget accounting is thread-safe; it can overshoot a cap by at most `parallel` in-flight calls.
- The live run finished `done`: 36 units and 36 ledger lines, 12 of 12 result commits equal to their version's HEAD, and `apiKeySource` `none` on every call. It had no retry, timeout or resume, so none of the paths above were exercised in it.
- The test suite passes (56 passed, run from a scratch copy). Its only resume test is a single pause, and no test kills the run at each stage.
