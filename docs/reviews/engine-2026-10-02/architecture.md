<!-- The system-architect persona's review of claude/engine at 7e3f0c3, saved verbatim on 2026-10-02 as it was handed back. Only the machine path of the worktree is replaced by <engine>, since this repository is public. -->

## Decomposition review of `claude/engine` (commit 7e3f0c3, plus uncommitted prompt edits)

This was a read-only review: nothing was modified, and no git state changed. Paths are relative to `<engine>/`.

**What is sound.** `orchestrator.py:109-118` follows analysis §4 stage by stage, and `config/paper.json` carries App. A.2's values, with §8's readings applied:
- the limitation loop counts critic calls and every other loop counts refinements;
- K counts rounds after round 0, and the S test runs at the end of each round;
- the meta-reviewer is asked again after the restart, and the loop budgets reset for each pass.

The primitive drives six stages: limitations, subset, full set, ablation, peer review and meta-review. The re-ablation and the meta restart reuse it through `after_guard`, so there is no second copy of the loop. The deviations §8 records are acceptable: the numeric Result Comparison, the A-FULL-1 reference, the ablation `Reject`, the routing, and the values for N_seed, N_0, N_p and N_t. The costs are at the edges.

### [P1] 1. A new coding backend takes four or more edits, and the paper's own split routing cannot be configured
- There is one backend per run: `runtime/agents.py:127`, built at `orchestrator.py:82`.
- A route has no backend field (`agents.py:101-105`). Yet App. A.2 puts each agent on Gemini or on Claude Code (tex:sections/appendix.tex:155), and §4.2 swaps only the coding backend, to Antigravity (tex:sections/4_experiment.tex:46).
- `cli.py:27-33,44,51` hard-codes the two backend names, and `cli.py:83` resumes every non-mock run on `claude`.
- The vendor's vocabulary sits in the data: Claude Code tool names in `agent.json`, and `opus`/`sonnet` in `routing.json`.
- The sandbox is applied inside the Claude backend (`claude_cli.py:100`). A second backend that leaves out `sbx.wrap` runs its agents unsandboxed, and nothing reports it.
- **Fix:**
  - add `backend` to each route;
  - add a registry in `runtime/backends/__init__.py` that the CLI and resume both read;
  - add a `SubprocessBackend` base class whose final `spawn()` always wraps the process;
  - name capabilities in `agent.json`, and let each backend map them to its tools.

### [P1] 2. Behaviour that analysis §3.5 and §8 (row A-TOP-1, "per stage, as data") declare as data is decided in code
- `stages.subset.exhaustion` and `stages.full.exhaustion` are passed to the primitive and then ignored: any outcome other than accept becomes `Bad` (`coder.py:129,167`).
- `stages.peer_review.exhaustion` is ignored: `writing.py:134` hard-codes `keep_last`. The real U-TOP-7 switch is an undocumented key, `keep: best_score` (`writing.py:136`).
- `discard`, Listing 1's own value, can never take effect. Limitations, ablation and meta turn a `None` back into the first candidate (`limitations.py:43`, `ablation.py:108`, `meta.py:59`).
- `keep_best` without a guard returns the first candidate (`primitive.py:73,96-99`).
- The primitive has no `on_guard_failure` parameter, although engine.md:92 shows one. `primitive.py:94-95` always returns `best`, so A-ABL-2's second reading (end the task) needs code.
- `limits.novelty_refs` (P-CFG-2) is never read. The value 2 actually lives in `agents/novelty_checker/schema.json` (`maxItems`) and `system.md:14,33`.
- **Fix:**
  - `StageOutcome` always carries `last` and `best`;
  - add `on_guard_failure` and `on_reject` parameters;
  - refuse `keep_best` when there is no guard;
  - each stage passes `stages.<name>` through unchanged;
  - wire `novelty_refs` into the novelty checker, or delete it.

### [P1] 3. A new agent needs a new code path
- Each role's agent name, its variables and its verdict handling are literals in a stage module:
  - verdict maps sit at `coder.py:29`, `limitations.py:40`, `ablation.py:96` and `meta.py:56`;
  - the verdict field name differs: `o["verdict"]` at `coder.py:110`, `o["decision"]` at `meta.py:46`.
- These maps duplicate the enums in `schema.json`. If the two disagree, `primitive.py:84` raises. The critic's unit is already stored as `ok`, so every resume replays the crash.
- The mock hard-codes the agent roster (`mock.py:91-103`), so a new critic gets `enum[0]`.
- `playground/engine/check_agents.py:19,386` uses engine.md §7 as its oracle.
- **Fix:**
  - bind each role to its agent, verdict field and verdict map in `stages.<name>`, and use one generic critic adapter;
  - check each map against the schema's enum when the agents load;
  - give each agent folder a `mock.json`.

### [P2] 4. One failed reasoning call ends a multi-day run, and resume cannot recover it
- Only four places catch `UnitFailed`: A_Coder, the ablation critic loop, the audit and the final judge.
- Everywhere else, a timeout or a second invalid output ends the run as `error` (`orchestrator.py:140-143`). The call sites:
  - `limitations.py:24,28,57-61`;
  - `evolution.py:60,81`;
  - the ablation planner, which runs outside the `try` (`ablation.py:77`);
  - `writing.py:80,86`;
  - `meta.py:43`.
- The stored failure replays on every resume (`agents.py:149-150`, tested at `tests/test_backends.py:123`). This contradicts §8's own U-TOP-2 row: "a multi-day run must survive one bad call".
- **Fix:** give each stage spec a failure branch, and store timeouts and exhausted transient retries as retryable.

### [P2] 5. A run's prompts are not pinned to it
- `inputs_sha256` is recorded but never compared (`agents.py:147-157`).
- The harness caches results by key alone (`harness.py:148-150`).
- Agent specs are reloaded from the package on resume (`orchestrator.py:82`).
- Evidence from the live run:
  - `runs/digits-quick-1/run.json` records a clean `7e3f0c3`, created at 13:55:13;
  - 15 prompt files then changed between 13:55:18 and 13:56:46;
  - one resume would therefore mix two prompt versions under a clean commit.
- `summarize` drops each result's `key` and `commit` (`harness.py:227`), so a number in the paper cannot be traced back to its result file.
- **Fix:** snapshot or hash `agents/` into the run, stop on a hash mismatch, and carry `key` and `commit` into `payload`.

### [P2] 6. Fidelity: departures from the paper or the analysis that §8 does not record

| Code | Paper / analysis | In §8? |
|---|---|---|
| The audit and its LLM repair run after the review loop and before meta; the repaired paper is never reviewed again (`meta.py:27-29`, `writing.py:165-175`) | U-INT-3 names exactly this risk | no |
| The spec filter runs only after a full-set `Good` and inside the refinement guard; a violation makes the idea `Bad`; ablation and rebuttal code is never filtered (`coder.py:173-178`, `ablation.py:36-46`) | analysis §4.3: "the task's output is filtered out"; U-INT-1 | no |
| A baseline that fails to run ends the run as `baseline_failed` (`coder.py:77-79`) | U-BASE-2 | no |
| The ablation and rebuttal variants are not in C+, so the exported code cannot reproduce the paper's tables (`export.py:59`) | U-ABL-3 / U-PEER-2; §3 requires C+ to reproduce | no |
| One `Good` idea skips the Selector, and an invented id falls back to the largest gain (`evolution.py:74-89`) | §3.3, Eq. 4 | inline only |
| An ablation `Reject` during the meta pass ends the run and drops pass 0's reviewed paper (`ablation.py:103-106`) | A-ABL-1 was decided for one pass only | no |
| The final judge reads the test table (`export.py:33-45`) | engine.md §5: "no agent sees it" | contradicts §5 |

### [P2] 7. The wiring around the primitive is copied (question 4)
- A_Coder's subset and full-set levels are two copies of the same code (`coder.py:97-134` and `136-171`). Each smuggles its last state out through a closure, because `StageOutcome` drops the candidate on reject.
- The ablation pass and the rebuttal round are two copies of plan, then fan out, then evaluate (`ablation.py:49-70`, `writing.py:83-101`).
- Seeds and evolution are hand-written loops (`limitations.py:48-65`, `evolution.py:38-66`). That is a legitimately different shape, but:
  - engine.md:13-14 says "Every stage is one parameterised stage primitive";
  - U-EVO-1's check point is hard-coded at `evolution.py:55`.
- **Fix:**
  - one `run_level` function over a configured list of levels;
  - one `fan_out` helper;
  - a §8 row for the population shape, with its WHY NOT.

### [P2] 8. Hidden couplings between components
- The locked harness imports `child_env` from the Claude backend (`harness.py:192`).
- Shared code lives inside stage modules, so meta imports ablation, which imports coder and evolution:
  - the state types: `Baseline` and `Trace` in `coder.py`, `Core` in `evolution.py`;
  - A_FullEng, `admits` and `spec_check`, in `ablation.py` and `coder.py`.
- `Ctx` mixes four jobs: integrity rules (`common.py:140-155`, which belong in the harness), the sandbox choice, prose the agents read (`common.py:168-181`), and threading.
- "Auditors cannot write" (A-INT-3) holds only because the call site passes `readonly=` (`coder.py:189`, `writing.py:159`), not because of the agent's `kind`.
- **Fix:**
  - move the state types to `scientisttwo/state.py`, and A_FullEng, the guard and the filter to `stages/shared.py`;
  - move `child_env` into `harness/sandbox.py`;
  - let the runtime derive the sandbox policy from `spec.kind`.

### The five changes against the bar

| Change | Files touched today | Meets the bar? |
|---|---|---|
| A new agent, for a new role | `agents/<a>/` (four data files), a stage module (call site, variables, verdict map), `mock.py`, engine.md §7 | **No.** Re-prompting an existing role is data only. |
| A new coding backend | `backends/<b>.py`; `cli.py` (factory, choices, resume); `agents.py`, `orchestrator.py` and `routing.json` to route only coding agents to it; translated tool and model names | **No** |
| A new task | Only `tasks/<id>/`, if its evaluation is one inputs file, one prediction file and one scalar `primary` (`harness.py:157-164,211-222`). Otherwise also `harness.py`, `task.py`, `common.py` and `manuscript.py`. | Yes for tasks like digits; **no** for multi-dataset, multi-metric tasks |
| A different loop limit | The profile, or `--set limits.X=` | Yes, except `novelty_refs` (never read) and the timing of the S test (in code) |
| A new model for one stage | `routing.json`, under `agents.<name>` | Yes per agent. **No** for agents shared across stages (`full_set_engineer` in §3.2, §3.4 and §3.6; `paper_enhancer`; `spec_filter`), because routes are keyed by agent name only (`agents.py:114-119`) |
