<!-- The fourth /codex pass on claude/engine, on the last follow-up commit only (36de8dc...d99dc01), gpt-6-astra at high effort, 2026-10-02 18:04. Saved verbatim; only the worktree's machine path is replaced by <engine>. -->
GATE: PASS on P1 (0 P1, 7 P2)

The follow-up fixes the main retry-ordering issue but leaves actionable resume, cleanup, export, and documentation defects. Focused reproductions confirmed the findings; nine isolated tests passed, while broader tests were blocked by local socket and sandbox restrictions.

Full review comments:

- [P2] Close the crashed interval before recording cap changes — <engine>/scientisttwo/orchestrator.py:105-107
  When resuming a crashed run with `--set`, `_set_caps` appends a current-time history entry before `_close_crash` runs. `_last_alive` consequently treats the cap change as the previous engine's last activity, charging all downtime as running time. A reproduction with one minute of activity followed by a day offline recorded 24 hours, immediately exhausting the quick profile's cap. Close the crashed interval before appending the budget event, preserving the resume/accounting invariants in [CLAUDE.md:61–64](CLAUDE.md#L61-L64).

- [P2] Validate cap values before persisting resume overrides — <engine>/scientisttwo/orchestrator.py:291-295
  `Caps.from_dict` checks names only, so `resume --set budget.max_agent_calls=typo` passes this validation and permanently replaces a valid cap with a string. The next budget check raises `TypeError`, and subsequent resumes remain broken until another override repairs the record. Validate supported numeric types and ranges, while retaining supported null values, before writing `run.json`; this also preserves the bounded-cost requirement in [CLAUDE.md:63–64](CLAUDE.md#L63-L64).

- [P2] Coordinate failed-run cleanup before releasing ownership — <engine>/scientisttwo/orchestrator.py:109-113
  After this closes the lock, another engine can acquire it and begin preparing the same directory. If that engine has not created `units` yet, the failing process deletes its files and lock pathname underneath it. I reproduced deletion while a second descriptor held the run lock. Cleanup needs ownership-safe coordination rather than releasing the lock before deciding whether to remove the directory.

- [P2] Normalize the path before checking for an existing run — <engine>/scientisttwo/cli.py:83-86
  For `--run-dir '~/runs/example'`, this checks a literal `~` directory, whereas `prepare` subsequently calls `expanduser().resolve()`. An existing run in the user's home therefore bypasses the refusal and is silently resumed with its recorded task and profile, leaving G1 unfixed for a path format the engine supports. Check the same normalized path that preparation uses.

- [P2] Handle directory-shaped PDF entries during failed exports — <engine>/scientisttwo/stages/export.py:104-105
  When a committed manuscript contains a nonempty `main.pdf` directory, this `unlink` raises instead of completing the best-effort export. This is reachable when resuming manuscripts created before the new ignore rules: existing versions retain their old ignore files. With a failed PDF build, the run now aborts before exporting code and results. Remove directories safely as well as files and symlinks, as `write_regular` already does on the successful-build path.

- [P2] Return a failure exit code when automatic resume is refused — <engine>/scientisttwo/cli.py:144-146
  If the task changes or another process holds the lock when `--wait` wakes, this returns the old paused record. `main` then prints the obsolete pause reason and exits 3 rather than reporting the refusal with exit 1, unlike manual resume and the documented exit-code contract. Propagate a distinct refusal outcome to the CLI without modifying a run owned by another process.

- [P2] Update the command reference alongside the new resume example — <engine>/docs/guide.md:255-260
  Section 3 still says `--run-dir` silently resumes existing runs (line 113), and its resume flag list says profile changes are impossible from the command line (lines 120–122). Both statements became false with this patch and contradict the updated troubleshooting and cap-change sections. Update that reference to describe existing-run refusal and the budget-only `resume --set` exception.
