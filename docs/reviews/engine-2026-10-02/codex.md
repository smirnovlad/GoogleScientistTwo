<!-- The /codex review gate on claude/engine (origin/claude/paper-analysis...cba39df), codex-cli 0.153.4 with gpt-6-astra at high reasoning effort, run 2026-10-02 15:32-16:05. Saved verbatim; only the machine path of the worktree is replaced by <engine>, since this repository is public. -->
GATE: FAIL (7 P1, 9 P2)

Focused probes reproduced protected-file overwrites, repeated completed work, mixed evaluation protocols after resume, and forged tables reaching meta-review. Process cleanup and accounting also remain incomplete. Full-suite validation was constrained by this environment denying sandbox-exec, process inspection, and loopback binds.

Full review comments:

- [P1] Reject symlinks before regenerating manuscript results — <engine>/scientisttwo/stages/manuscript.py:132-134
  A writer can replace `results.json` or `results.tex` with a symlink to a protected file. `Workspaces.fresh()` preserves that symlink, and these unsandboxed writes follow it during refresh or export. I reproduced overwriting a file outside the manuscript workspace. Reject escaping symlinks and replace result files without following them; otherwise the engine bypasses its own write sandbox. This violates [CLAUDE.md:44](CLAUDE.md#L44).

- [P1] Export the commit that the harness evaluated — <engine>/scientisttwo/workspace.py:122-124
  The harness evaluates an archive of the recorded commit, but export copies the working tree, including ignored and untracked files, and follows symlinks. Consequently, post-commit changes can make C+ differ from the scored method; an ignored symlink can also copy otherwise forbidden host data into the export. Both behaviors reproduced in a focused probe. Export the recorded commit using the existing safe archive path, as required by [CLAUDE.md:49](CLAUDE.md#L49).

- [P1] Kill descendants before waiting for the output pipe to close — <engine>/scientisttwo/runtime/backends/claude_cli.py:131-138
  If a CLI descendant starts another session and inherits stdout, this timeout kills only the CLI's group. The reader remains blocked in `for line in proc.stdout`, so it never reaches `spawned.finish()`, which would kill the descendant. A one-second timeout with a four-second pipe-holding child exceeded seven seconds in a probe; a persistent child can hang the run indefinitely. Apply whole-tree termination at timeout and bound the stream reader independently.

- [P1] Persist completed responses before workspace finalization — <engine>/scientisttwo/runtime/agents.py:260-265
  After a successful paid call, `on_done` commits and renames the workspace before its unit record is durable. A crash or filesystem error during this interval leaves completed work without a replayable result; resume calls the backend again and replaces the finished version. Injecting a store failure after finalization reproduced two calls for the same completed coding unit. Persist a recoverable response/finalization state first, honoring [CLAUDE.md:61–62](CLAUDE.md#L61-L62).

- [P1] Pin the task manifest across resumes — <engine>/scientisttwo/orchestrator.py:137-137
  Resume reloads the current task manifest rather than a recorded copy, while existing evaluations are replayed by key and commit. Changing `full.seeds` during a pause therefore silently mixes evaluation protocols: a probe resumed successfully with baseline seeds `[0, 1]` and ablation seeds `[7, 8]`. The harness hashes do not cover these manifest settings. Snapshot or verify the task configuration before replay, consistent with [CLAUDE.md:49](CLAUDE.md#L49).

- [P1] Regenerate verified tables for the meta-reviewer — <engine>/scientisttwo/stages/meta.py:56-58
  Unlike peer review and the final judge, this call omits the regenerated tables argument and reads the writer-controlled `results.tex`. An audit repair is itself another writer session, so it can leave edited tables even when marked repaired. I reproduced a forged `0.9999` reaching the meta-review prompt while the peer-review prompt contained verified numbers. Use the verified-payload reader here too, preserving the setup-enforced integrity required by [CLAUDE.md:43–46](CLAUDE.md#L43-L46).

- [P1] Reap surviving process groups after their leader exits — <engine>/scientisttwo/runtime/procs.py:205-207
  A process group can remain alive after its leader exits, for example when a Bash shell leaves a training child running. On resume, `started(pgid)` then returns nothing, so this condition skips the live group and subsequently deletes its recovery record. The orphan survives while the replacement unit starts. Preserve a verifiable surviving-member identity or persist and recover the unit marker instead of requiring the original group leader to remain alive.

- [P2] Validate inputs before replaying completed coding units — <engine>/scientisttwo/stages/common.py:119-121
  This early return bypasses `AgentRuntime.run()` and its input-hash validation for every cached coder and writer. Changed prompts, variables, or routing therefore silently replay an old version even with strict replay enabled. A probe changed a coding unit's input and received its cached output without `InputsChanged`. Route this branch through the same replay validation used for reasoning units; otherwise the reproducibility guarantee in [CLAUDE.md:49](CLAUDE.md#L49) does not cover code generation.

- [P2] Give the ablation planner read access to the selected version — <engine>/scientisttwo/harness/policies.py:77-79
  `ablation_planner` is declared as `reasoning`, although `ablation_pass()` supplies a workspace for its Read/Glob/Grep tools. This branch discards that workspace, and `Ctx.think()` also changes its cwd to scratch. For normal runs under HOME, the planner cannot inspect the selected implementation and must plan from the supplied diff alone. Preserve read-only workspace access for this role, or classify it as read-only; the mock backend never exercises these reads.

- [P2] Preserve reported costs when rejecting CLI results — <engine>/scientisttwo/runtime/backends/claude_cli.py:222-225
  A CLI result can include `total_cost_usd` and usage even when its structured output is missing or it reports an error. These exceptions discard that metadata before returning an `AgentResult`, so the runtime records an unknown cost and the equivalent-dollar cap ignores known spending. A result reporting $12.30 was counted as $0 known spending and permitted another call under a $1 cap. Carry usage metadata through failures, as required by [CLAUDE.md:63–64](CLAUDE.md#L63-L64).

- [P2] Journal in-flight attempts before calling the backend — <engine>/scientisttwo/runtime/agents.py:218-225
  An attempt is added to the ledger only after the backend returns or raises. If the engine is killed while the CLI is spending, resume reaps its processes but never accounts for that interrupted attempt: agent-call and coding-session caps regain already-consumed capacity. Write a durable attempt-start record before invocation and reconcile unfinished attempts as interrupted with unknown cost. This is needed for the bounded, recorded spending required by [CLAUDE.md:63–64](CLAUDE.md#L63-L64).

- [P2] Keep transcript attempt identifiers unique across resumes — <engine>/scientisttwo/runtime/agents.py:283-286
  The attempt counter restarts at one whenever an unfinished unit resumes, so these names collide with previous attempts. `ClaudeCLIBackend.call()` opens the transcript with `"w"`, overwriting the evidence from the paused or crashed invocation while its ledger entries remain. Allocate persistent attempt numbers or immutable invocation IDs across resumes, so the run retains the history required by [CLAUDE.md:71–72](CLAUDE.md#L71-L72).

- [P2] Exclude crash downtime from the running-time budget — <engine>/scientisttwo/runtime/budget.py:83-87
  A hard crash leaves the last status as `running`, so the entire interval until resume is charged as active time. The resume history event closes that interval only at restart. A quick run that crashes and remains stopped overnight can therefore exceed its 12-hour cap permanently without doing more work. Recover running intervals from a durable heartbeat or equivalent crash boundary, rather than treating all downtime as execution; otherwise [CLAUDE.md:61–62](CLAUDE.md#L61-L62) is not met.

- [P2] Snapshot the reported budget after export-time calls — <engine>/scientisttwo/orchestrator.py:207-207
  This summary is captured before export runs the test reporter and final judge. `export/results.json` and `report.md` therefore omit those calls, their retries, costs, and duration, although `run.json` records them. A completed probe reported 19 calls in the export versus 21 in the final run record. Obtain the summary after export's agent work, preserving the accounting required by [CLAUDE.md:63–64](CLAUDE.md#L63-L64).

- [P2] Prove sandbox probes reach the forbidden operation — <engine>/scientisttwo/tests/test_harness.py:78-80
  These assertions also pass when `sandbox-exec` itself fails with `sandbox_apply: Operation not permitted`, before the probe executes. That happened in this review environment: the label-denial test passed without attempting a label read. Emit and assert an execution marker, verify an allowed read, and catch the specific forbidden operation inside the child. Otherwise this test cannot establish the boundary it claims to protect, contrary to [CLAUDE.md:69–70](CLAUDE.md#L69-L70).

- [P2] Clean up the entire LaTeX process tree on timeout — <engine>/scientisttwo/stages/manuscript.py:232-235
  `latexmk` launches TeX and bibliography subprocesses, but `subprocess.run(timeout=240)` kills only its immediate child. A hung TeX process can survive the timeout, retain the captured pipes, and continue writing into a build directory that resume reuses. This path also bypasses the process registry, so crash recovery cannot reap it. Use the existing registered process-tree runner with file-backed output for manuscript builds too.
