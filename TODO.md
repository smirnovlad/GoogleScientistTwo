# TODO

The ordered task list. Tick an item `- [x]` when it is done, and name the commit or file that
proves it. Add work you discover here, never only in chat. Priorities: `P0` blocks everything
after it; `P1` is needed before building; `P2` comes later.

## Phase 0: understand the paper, then decide the design (no engine code yet)

- [x] `P0` **1 · A rigorous analysis of the paper.**
  - **Done, 2026-09-28,** on the branch `claude/paper-analysis`. The proof:
    - **The deliverables are in `docs/paper/`:**
      - `analysis.md`, with `stages/`;
      - `claims.md`, with `claims/`;
      - `note-check.md` and `artifacts.md`;
      - `unspecified.md`, the decision register;
      - `traceability.md`.
    - **Every statement cites the paper, or is marked as ours.**
      `python3 playground/paper/check_citations.py` checks 18 files and finds 0 problems. It checks
      every citation and every TeX anchor, and every quote of five words or more against the source.
    - **The register and the map are complete.** `register_coverage.py` and `trace_coverage.py` both
      pass: 143 gap IDs sit in 93 register rows, and all 177 paper elements are mapped.
    - **A reader can work from `docs/paper/` alone.** A blind reader answered 27 of 28 questions from
      it, and the one conflict it found is fixed. The record is
      `docs/reviews/paper-analysis-2026-09-27/blind-reader-quiz.md`.
    - **The analysis was reviewed.** Six persona reviews, the fix list, and each reviewer's closure
      check are kept verbatim in `docs/reviews/paper-analysis-2026-09-27/`.
    - **"Listing 1" is right.** The arXiv PDF prints Listing 1. The HTML renders the same float as
      "Figure 4", and calls it "Listing 4" in §3's text.
  - **Who:** owner `paper-analyst`. `system-architect`, `research-engineer`,
    `evaluation-integrity-engineer` and `agent-engineer` review it in parallel, each through its
    own lens.
  - **Sources:** the paper's own text, never a summary: the TeX source
    (`https://arxiv.org/src/2609.19644`), the HTML (`https://arxiv.org/html/2609.19644v1`) and the
    PDF. Check the arXiv licence before committing them to this public repository; if it does not
    allow that, keep them out of git and record their sha256.
  - **Read everything:**
    - §3.1–3.6, the six stages: seed ideas from limitations, subset-to-full-set evaluation, idea
      refinement, ablation studies, manuscript drafting with simulated peer review, and
      meta-review;
    - Table 1: stages, candidates, critics and refinement agents;
    - the stage pseudocode figure;
    - Appendix A.1 (the benchmark) and A.2 (the configuration: the loop limits and their values);
    - Appendices B–D, and Tables 2–11.
  - **Deliverables in `docs/paper/`:**
    - `analysis.md`: how the engine works, stage by stage, written as structure: each step's
      inputs and outputs, the agents, the loop and its limit, the stopping rule, and the failure
      branch;
    - `traceability.md`: each paper element, the requirement it becomes, and later the component;
    - `unspecified.md`: everything the paper leaves open (prompts, subset and full-set
      definitions, model versions, …), each with the decision it forces on us;
    - `claims.md`: every quantitative claim, with its table, its sample, and our assessment.
  - **Check the initial note, `docs/inputs/2026-09-27-initial-replication-note.md`, claim by
    claim,** marking each true, false, or not in the paper. One is already known:
    - the note calls the stage pattern "Listing 1";
    - the HTML shows the stage pseudocode as a figure (Figure 4);
    - check which is right from the TeX source.
  - **Done when:** a reader can explain every stage and every loop limit from `docs/paper/` alone,
    and every statement there cites its location in the paper.

- [ ] `P0` **2 · Requirements.** Write `docs/requirements.md`:
  - the goal in one line;
  - each requirement with its acceptance test, traced to the paper, or marked as our own decision
    with its reason.

  A requirements analyst (`system-analyst`, where it resolves) checks what is missing.
  **Start from** the 177 elements in `docs/paper/traceability.md`, and from the 33 register rows
  in `docs/paper/unspecified.md` that task 2 owns (17 of them block).
  **Done when:** every paper element in `traceability.md` maps to a requirement or to a recorded
  decision to leave it out.

- [ ] `P0` **3 · Components and their contracts.**
  - **Who:** owner `system-architect`, reviewed in parallel by the other personas.
  - **Why:** the engine must not be a monolith.
  - **The work:** confirm, change or reject each candidate component below against the analysis
    and the requirements. For each surviving component, write down:
    - its contract: inputs, outputs and failure modes;
    - what varies, which becomes an interface;
    - what is data, meaning prompts, schemas, limits and routing.

    The candidates are a starting list, not a decision:
    - the stage primitive. Task 1 concludes that the stages do share one pattern: one primitive,
      with parameters per stage. `docs/paper/analysis.md` §3.4 gives each stage's values;
    - run state and resume;
    - the agent runtime (prompt, schema, model route, budget);
    - the coding-backend adapter;
    - the sandbox and GPU queue;
    - the task environment;
    - the locked evaluation harness;
    - drafting;
    - reviewers;
    - the integrity audit;
    - the budget guard and cost ledger;
    - mock mode.
  - **Order:** follow the ranked blocking rows of `docs/paper/unspecified.md`, `blocks 1` to
    `blocks 8`, which is the architect's order. The primitive's parameters come first, then the
    unit of work and what happens when it fails.
  - **Blocked by** task 6's four blocking decisions (see task 6). The harness and audit contracts
    cannot be written before them.
  - **Output:** design documents in `docs/architecture/`, each decision recorded with its
    `⛔ WHY NOT`.
  - **Done when:** each of these five changes touches one component, or only data, and the design
    shows which files for each:
    - a new agent;
    - a new coding backend;
    - a new task;
    - a new loop limit;
    - a new model for one stage.

- [ ] `P1` **4 · Survey of what we can reuse.** Verify each candidate before we depend on it: that
  it exists, its licence, its maintenance, and whether it fits. The note names these candidates:
  - PaperOrchestra, for drafting;
  - AutoSOTA, for task packaging, and as the benchmark's source per Appendix A.1;
  - the ScientistOne paper's integrity audit;
  - MLE-STAR's ablation loop;
  - ScholarPeer's reviewer design;
  - the Claude Agent SDK, as a coding backend;
  - paperreview.ai, as a held-out reviewer.

  **Output:** `docs/findings/<date>-reuse-survey.md`, giving five facts for each candidate: the
  source, what it covers, how we would use it, its cost and terms, and how far to trust it.

  **Found by task 1:** ScientistOne's integrity audit is part of the paper by reference, since
  Table 7 follows it. Its TeX, arXiv:2605.26340v1, is pinned by
  `playground/paper/fetch_sources.sh`. The audit's definition is in its §5. The five evaluator runs
  and the 1%/3σ tolerance are only the settings of ScientistOne's own experiments (its §6).

- [ ] `P1` **5 · Scope, tasks and budget.**
  - Choose about three cheap development tasks and a test set. The note proposes the paper's five
    ICLR 2026 tasks; verify them against the paper.
  - Measure each task's compute.
  - Build a cost model for one task, checked against the paper's reported cost per task. The note
    quotes about $3,765; verify it.
  - Decide how we are billed: API or subscription.
  - **Found by task 1:**
    - **The $3,765 is a mean over the 33 NeurIPS successes only.** Failed runs are not costed
      (`docs/paper/claims/discussion.md`, C-DISC-3; U-COST-2).
    - **The five ICLR 2026 tasks are App. B's.** ScientistTwo succeeded on four of them, and its
      ICLR gains in Table 4 cannot be rebuilt from anything the paper prints
      (`docs/paper/claims/appendix-b.md`).
    - **Measure these ourselves:** see "What task 5 must measure itself" in `docs/paper/claims.md`.

- [ ] `P1` **6 · The evaluation-integrity design.** Owned by `evaluation-integrity-engineer`.
  - a threat model for each stage;
  - the locked harness;
  - the validation/test separation;
  - the verified-results table the writer sees;
  - deterministic gains;
  - an independent reporting judge;
  - the audit.

  Each guard comes with the attack it stops and a control that proves it works.

  **`P0` part, before task 3: decide the four blocking rows** of `docs/paper/unspecified.md`.
  - **U-INT-4:** a locked harness computes every metric.
  - **U-TOP-5:** a validation split for every decision in the loop.
  - **A-INT-1:** integrity as gates in the run, or only as a post-hoc audit.
  - **A-INT-3:** the integrity auditor kept apart from the in-loop fixer.

  The integrity rules in `CLAUDE.md` already settle the first two in principle.

- [ ] `P1` **7 · Test strategy and mock mode.** A mock LLM and a mock coding agent, so the whole
  state machine can be tested for $0. `infrastructure-engineer` owns it. **Found by task 1:** the
  paper gives no success criterion for any agent, and tests them only end to end (U-TOP-6). A test
  per agent is therefore our own requirement.

- [ ] `P2` **8 · The build plan.** Phases, each with a "done when".
  - **Order:** by risk. Environments and the evaluation harness come first, and agents come last.
  - **Sizing:** in wall-clock time with AI assistance, split into three kinds of work, which
    compress differently:
    - writing code we understand;
    - porting;
    - discovering how something fails.

- [ ] `P2` **9 · Shared personas.** Once the shared persona plugin exists (a separate
  "agent-workbench" repository), decide whether this repo's generic personas move there. The
  research-specific ones stay here.

## Phase 1 onwards: build

Filled in by task 8, once tasks 1–7 are done and reviewed.

## Goal of 2026-10-02: a working engine, on the subscription

Set by Vlad on 2026-10-02 (`DEVELOPMENT_PROCESS.md`, verbatim there): deliver a working engine
that replicates ScientistTwo, run through `claude -p` on his subscription, never the API, with no
questions to him. It runs ahead of tasks 2–8, on `claude/engine`; tasks 2 and 6 continue in
`gs2:T2` and `gs2:T6`, and are folded in when they land.

- [x] `P0` **E1 · The design contract:** `docs/architecture/engine.md`. Components and contracts,
  the `claude -p` backend, integrity by mechanism, the task contract, the 27 agents, and a
  decision with its `⛔ WHY NOT` for every gap the engine must close.
- [x] `P0` **E2 · Probes of the subscription CLI.** Isolation from Vlad's own setup without
  `--bare` (which bills the API), `--json-schema`, the stream format, `apiKeySource`, usage
  windows; and `sandbox-exec` around a real coding agent. Recorded in `DEVELOPMENT_PROCESS.md`.
- [x] `P0` **E3 · The engine core** in `scientisttwo/`: the backends (`claude -p`, mock), the run
  store and resume, the budget guard and ledger, the sandbox, the locked harness, workspaces, the
  stage primitive, every stage of §3.1–§3.6 and §4.2, the export, the CLI.
- [x] `P0` **E4 · The 27 agents as data** (`scientisttwo/agents/`), checked by
  `playground/engine/check_agents.py`. Owner `agent-engineer`. Proof (2026-10-02): the checker
  reports 27 agents and 0 problems, 291 schema mutants are rejected, and the self-test catches
  21 of 21 corruptions. A live haiku call on a known-answer case returned the expected verdict.
- [x] `P0` **E5 · The demo task** `tasks/digits/`, with measured baseline numbers and headroom.
  Owner `research-engineer`. Baseline: subset 0.8960 ± 0.0217, full 0.9118 ± 0.0170, test
  0.9090 ± 0.0196 (3 seeds). The lookup attack failed under the real policy.
- [x] `P0` **E6 · Tests for $0:** the primitive, harness, sandbox, backends and runtime, plus
  every terminal branch end to end on the mock backend (`tests/`, 56 passed on 2026-10-02).
  The gaps the reviews found are F-items below.
- [x] `P0` **E7 · A real run on the subscription:** `runs/digits-quick-1`, profile `quick`.
  Status `done` in 0.16 h: 36 agent calls, 15 sessions, $2.91 API-equivalent, nothing billed.
  Validation gain +0.0761, test gain +0.0548, peer review 3/10, final judge 3/10 (reject).
  Its findings are R1–R4.
- [ ] `P1` **E8 · Review:** personas in parallel, saved verbatim in
  `docs/reviews/engine-2026-10-02/` (architecture, infrastructure, integrity; agent-engineer's
  report in the hand-back), then the `/codex` gate. The findings, each fixed with a test:
  - From run 1:
    - [x] R1 · The ablation critic gets the baseline and the gain over it (P-ABL-7). Run 1's critic said
      "The baseline score was not supplied", while standardisation alone carried 84% of the gain.
    - [x] R2 · The test results go into the text through a `test_reporter` writer. Run 1's judge
      found the abstract saying "no test split" beside the test table.
      Proof: `test_a_full_run_exports_a_paper_and_code` asserts the reporter runs; the agent
      engineer's live test on run 1's paper removed all 4 "no test split" claims.
    - [x] R3 · The rebuttal planner reads the results already reported. Run 1 re-ran ablation A1
      as its only rebuttal experiment.
      Proof: `test_a_rebuttal_plan_reads_the_results_already_reported`; live on run 1's review it
      cited A1 instead of re-running it.
    - [x] R4 · The critics' gain text states the margin `min_delta`, so the LLM gates and the guard
      share one threshold.
  - From the agent engineer:
    - [x] A1 · `render` raises on undeclared variables.
    - [x] A2 · The idea generator reads each seed's novelty references.
    - [x] A3 · A reference whose search failed is `unchecked` and kept, never removed.
    - [x] A4 · Read-only agents keep `Bash` for git history; engine.md §3 now says why.
  - From the integrity review:
    - [x] G1 · `P1` Evaluated code and agents read through an allowlist under `$HOME`, plus a
      task-declared deny pattern. The reviewer read one of 9 un-denied copies of the digits data
      and scored 1.0 on the test split.
      Proof: `test_a_dataset_copy_under_home_is_unreadable_unless_allowlisted`,
      `test_a_deny_pattern_hides_every_copy_anywhere`; the engine's own digits copy is unreadable
      while sklearn trains (probe, 2026-10-02).
    - [x] G2 · `P1` Agents have no network beyond the Anthropic API: a local proxy with a host
      allowlist, and the sandbox denies every other outbound connection. Per-task extra hosts.
      Proof: `test_an_agent_reaches_the_proxy_and_nothing_else`; run 2's `egress.jsonl` holds only
      `api.anthropic.com`.
    - [x] G3 · `P1` U-BASE-2: the reproduced baseline must match the task's reported numbers
      within a tolerance, or the run ends `baseline_failed` (a sandbagged baseline inflates gains).
      Proof: `test_a_baseline_that_misses_the_reported_number_ends_the_run`; run 2's check passed at
      0.9118.
    - [x] G4 · `P2` Prose numbers in the manuscript are checked against `results.json`; unmatched
      numbers go to the audit.
      Proof: `test_a_number_in_the_prose_that_no_result_holds_is_flagged`.
    - [x] G5 · `P2` Reviewers read results tables regenerated from result files, never the copy
      a writer could edit; an edited copy is an audit finding.
      Proof: `test_a_writer_cannot_change_the_numbers_a_reviewer_reads`.
  - From the infrastructure review:
    - [x] I1 · `P1` A stale result can never be read for new code: `evaluate` checks the commit,
      `rt.run` checks the inputs hash, exhausted transient retries pause the run, and each resume
      records the engine commit and the CLI version.
      Proof: `test_a_replay_with_other_inputs_is_refused`,
      `test_a_run_keeps_its_own_prompts_and_refuses_a_changed_one`,
      `test_transient_errors_that_persist_pause_the_run_and_store_nothing`.
    - [x] I2 · `P1` One ledger line per attempt, fsync'd, before the unit is stored.
      Proof: `test_transient_errors_are_retried_and_each_attempt_is_in_the_ledger`,
      `test_retries_count_against_the_caps`.
    - [x] I3 · `P1` A truncated last ledger line is repaired, not fatal.
      Proof: `test_a_partial_ledger_line_is_repaired`.
    - [x] I4 · `P1` `max_hours` counts running time, not paused time.
      Proof: `test_paused_time_does_not_count_as_running`.
    - [x] I5 · `P1` A run lock; each session's process groups recorded and killed as a tree;
      orphans from a crashed engine killed on resume.
      Proof: `test_one_engine_per_run`, `test_the_whole_process_tree_dies_with_the_call` (failed
      before the environment marker),
      `test_orphans_of_a_crashed_engine_are_killed_on_resume_and_only_they`.
    - [x] I6 · `P1` An evaluation cannot hang the engine: output to a file, a bounded wait, and the
      whole tree killed.
      Proof: `test_a_hung_child_holding_the_output_cannot_hang_the_harness`.
    - [x] I7 · `P1` Agents cannot write a workspace's `.git`; git errors become unit failures.
      Proof: `test_a_coding_agent_cannot_write_its_versions_git`; evaluation runs the commit
      (`test_evaluation_runs_the_commit_not_the_working_tree`).
    - [x] I8 · `P2` A result already delivered is used even if the CLI then lingers.
      Proof: `test_a_delivered_result_survives_a_lingering_cli`.
    - [x] I9 · `P2` Retries start clean: one transcript per attempt, the workspace reset, and a
      cap on usage-limit waits.
      Proof: `test_a_timeout_is_retried_once_then_fails`, `test_usage_limit_waits_are_capped`;
      per-attempt transcripts in `AgentRuntime._transcript`.
    - [x] I10 · `P2` Errors are classified by exit code and the CLI's own usage text; environment
      faults pause; the reset time comes from the exhausted window.
      Proof: `test_failures_are_classified` (context limit, EPERM, usage),
      `test_the_reset_comes_from_the_spent_window`,
      `test_a_window_with_no_reset_time_does_not_block_forever`.
    - [x] I11 · `P2` The sandbox keeps the user's Claude setup read-only (settings, hooks,
      CLAUDE.md, memory), auto-memory and auto-update are off, the CLI path is pinned, and each
      unit gets its own TMPDIR.
      Proof: `test_no_agent_can_write_the_users_claude_setup_or_read_its_history`; probes of
      2026-10-02 (DEVELOPMENT_PROCESS.md).
  - From the architecture review:
    - [x] S1 · `P1` A backend registry, a backend per route, and a subprocess base class that
      always applies the sandbox.
      Proof: `test_the_registry_resumes_a_run_on_the_backend_it_recorded`,
      `test_no_policy_no_process`. Capability names in agent.json wait for a second real backend.
    - [x] S2 · `P1` Stage settings are validated per stage; peer review's "keep the best" is a
      rank, not an undocumented key; `novelty_refs` is removed; §4's pseudocode matches the code.
      Proof: `config.validate_profile` on both profiles; `test_keep_best_needs_a_guard_or_a_rank`;
      engine.md §4 rewritten from the code.
    - [x] S3 · `P1` The critics' verdict maps are one table (`stages/roles.py`), checked against
      the schemas before a run starts.
    - [x] S4 · `P2` A unit failure that stops the run is retried on resume, not replayed forever.
      Proof: `test_a_failure_that_stops_the_run_is_retried_on_resume`.
    - [x] S5 · `P2` A run pins its prompts: the agents are snapshotted into the run, and result
      keys and commits are carried into the paper's payload.
      Proof: `test_a_run_keeps_its_own_prompts_and_refuses_a_changed_one` (a coding unit included);
      payload rows carry `result_key` and `commit`.
    - [x] S6 · `P2` §8 records each departure the review listed, and §5 says who reads test results.
      The export ships each ablation and rebuttal variant as a patch. An ablation `Reject` on a
      restarted pass keeps the previous pass.
      Proof: engine.md §5 and §8;
      `test_a_restart_the_ablation_critic_rejects_keeps_the_previous_pass`; `export/variants/` in
      the full-run test.
    - [x] S7 · `P2` A_Coder's two levels are one `run_level`; ablations and rebuttals share
      `run_variants`.
    - [x] S8 · `P2` The state types live in `state.py` and shared steps in `stages/shared.py`;
      `child_env` moves to the sandbox module; the sandbox policy follows the agent's kind.
      Proof: `harness/policies.py` builds every sandbox from the agent's kind; `Ctx.think` refuses a
      coding agent and a read-only agent without its version.
  - From the `/codex` gate (gpt-6-astra, `origin/claude/paper-analysis...cba39df`): **GATE: FAIL,
    7 P1 and 9 P2**, saved verbatim in `docs/reviews/engine-2026-10-02/codex.md`. Each new test
    below fails on `cba39df` and passes after the fix (checked 2026-10-02 in a detached worktree).
    - [x] C1 · `P1` The engine never follows a writer's link. `finalize` removes, before git reads
      a byte, every symlink that leaves the version, every hard-linked file and every special file.
      Manuscript files are read only as regular files, and the engine's own files replace whatever
      is there. On `cba39df` a probe wrote through a linked `results.tex`, read a secret through a
      linked `main.tex`, and exported both.
      Proof: `tests/test_workspace.py` (3 tests). A sandbox probe showed a writer CAN link to a file
      it cannot read, and CANNOT hard-link one.
    - [x] C2 · `P1` The export is the version's commit (`git archive`), never its working tree.
      Proof: `test_the_export_is_the_commit_not_the_working_tree`.
    - [x] C3 · `P1` The CLI's timeout kills the whole tree, and the stream reader is bounded.
      Proof: `test_a_timeout_kills_a_descendant_that_holds_the_output`,
      `test_the_reader_is_bounded_even_when_a_holder_escapes_every_kill`. On `c1850a5` each call
      took about 33 s, the holder's life; now under 8 s.
    - [x] C4 · `P1` A finished unit is stored before its version is made, and a resume makes a
      missing version from the working copy the agent left, without a second call.
      Proof: `test_a_crash_between_storing_a_unit_and_making_its_version_does_not_pay_twice`.
    - [x] C5 · `P1` A run pins its `task.json`; a changed one stops the resume unless
      `--allow-changed`, which records the changed keys.
      Proof: `test_a_resume_keeps_the_task_settings_the_run_started_with`.
    - [x] C6 · `P1` The meta-reviewer reads the tables regenerated from the result files.
      `manuscript_text` has no default to the version's copy any more.
      Proof: `test_the_meta_reviewer_reads_the_verified_tables` (a forged 0.9999 in the repaired
      version no longer reaches the prompt).
    - [x] C7 · `P1` Process groups that outlive their leader are reaped on resume: a record names
      every process by pid and start time, and the unit's marker.
      Proof: `test_a_group_that_outlived_its_leader_is_reaped_on_resume`; on `c1850a5` the child
      survived (`reaped []`).
    - [x] C8 · `P2` A coding unit's replay is checked against its inputs.
      Proof: `test_a_run_keeps_its_own_prompts_and_refuses_a_changed_one` (the `subset/code` step).
    - [x] C9 · `P2` The ablation planner reads the selected version (kind `readonly`).
      Proof: `test_the_ablation_planner_reads_the_selected_version_and_cannot_write_it`;
      `check_agents.py` 0 problems.
    - [x] C10 · `P2` A failed CLI result keeps its reported cost and usage.
      Proof: `test_a_failed_result_keeps_the_cost_it_reported` (a $1 cap now stops the next call).
    - [x] C11 · `P2` An attempt is journalled before the call; one cut off by a crash is counted.
    - [x] C12 · `P2` Transcript and attempt numbers stay unique across resumes.
      Proof (both): `test_an_attempt_cut_off_by_the_engines_end_is_counted_and_numbered_on`.
    - [x] C13 · `P2` Downtime after a crash is not counted as running time: a heartbeat every 30 s,
      and a resume closes a dead engine's interval at it (status `crashed`).
      Proof: `test_downtime_after_a_crash_is_not_running_time` (10 h of downtime counted before,
      60 s now).
    - [x] C14 · `P2` The exported budget is taken after the export's own calls, and a summary is a
      copy. Run 2's export said 40 calls next to 42 outcomes.
      Proof: `test_the_exported_budget_counts_the_exports_own_calls`.
    - [x] C15 · `P2` The sandbox tests prove the child ran (a marker) and reached the forbidden step.
      Proof: every denial test asserts `PROBE-REACHED` and `PROBE-DENIED`;
      `test_a_child_that_never_ran_is_not_a_denial` shows the check can fail.
    - [x] C16 · `P2` The LaTeX build runs in the registered process-tree runner.
      Proof: `test_a_hung_build_dies_with_its_whole_tree`.
  - From the second `/codex` gate (`origin/claude/paper-analysis...f470f27`): **GATE: FAIL, 3 P1
    and 7 P2**, saved verbatim in `docs/reviews/engine-2026-10-02/codex-2.md`. A first attempt
    was stopped by OpenAI's classifier ("possible cybersecurity risk") and returned nothing.
    - [x] D1 · `P1` A writer's `.latexmkrc` could turn the built PDF into a link that the export
      followed. The build now runs with `-norc`, and the PDF is read and written only as a
      regular file.
      Proof: `test_a_pdf_the_build_left_as_a_link_is_not_a_pdf`; the bibliography test now plants
      an rc file too.
    - [x] D2 · `P1` Parallel workers each passed a cap of one. `Budget.admit` now checks the caps
      and reserves the call in one step.
      Proof: `test_parallel_calls_cannot_pass_a_cap_together`.
    - [x] D3 · `P1` A crash after the success line and before the unit write paid twice. The success
      line now holds the unit, and the next start rebuilds the unit from it. `forget` journals a
      deletion, so a forgotten unit stays forgotten.
      Proof: `test_a_unit_finished_but_not_stored_is_rebuilt_without_a_second_call`.
    - [x] D4 · `P2` A rejection replayed another commit's result.
      Proof: `test_a_rejection_never_replays_another_commits_result`.
    - [x] D5 · `P2` A failed call now keeps the usage windows it saw.
      Proof: `test_a_failed_call_keeps_its_usage_windows`.
    - [x] D6 · `P2` The replay fingerprint now covers the schema, the kind and the tools. Units
      hashed before this change need `--allow-changed` to replay.
      Proof: `test_a_changed_schema_does_not_replay`.
    - [x] D7 · `P2` The task's `coding_session_seconds` bounds every coding and writer session.
      An agent's own routing entry still wins over it.
      Proof: `test_a_coding_session_gets_the_tasks_timeout_unless_its_route_sets_one`.
    - [x] D8 · `P2` The exported patch is the whole diff, not the copy capped for prompts.
      Proof: `test_the_exported_patch_is_the_whole_change` (`git apply --check` on 280 kB).
    - [x] D9 · `P2` A directory named like a manuscript file now reads as missing instead of
      crashing. Proof: `test_the_engine_neither_writes_nor_reads_through_a_writers_link`.
    - [x] D10 · `P2` The orphan test now waits for the child's first heartbeat.
      Proof: `test_the_whole_process_tree_dies_with_the_call`.
  - From task 6 (`integrity-blockers`), blocker B1:
    - [x] T1 · A test seed is never a search seed; the digits test seeds are 100–109. With shared
      seeds the winner of 20 null candidates keeps +1.32 of its +2.65 validation gain on test
      (task 6's `null_control.py`, rerun 2026-10-02).
      Proof: `test_a_test_seed_is_never_a_search_seed`.
  - From run 2:
    - [x] R5 · `P1` Every PDF failed in the build sandbox. bibtex writes beside its sources, the
      build could write only elsewhere, and bibtex reported "Not writing to /Use.bbl". The cause
      was bisected rule by rule. A build now compiles an export of the commit with the engine's
      tables, in its own directory, and the error goes into the event.
      Proof: `test_a_paper_with_a_bibliography_builds_in_the_sandbox`; run 2's two papers rebuild
      in about 1 s each.
    - [x] R6 · `P2` A finished run kept the reason and `resume_after` of its earlier pause.
      Proof: `test_downtime_after_a_crash_is_not_running_time` (its last assertion).
  - For use on the subscription, found while writing the guide:
    - [x] U1 · `P1` A long run pauses at every 5-hour window and waited for a person. `run` and
      `resume` now take `--wait`: sleep until the window resets, then resume, until the run ends.
      A pause with no known reset, or one further than `--max-wait-hours` (24), still stops.
      Proof: `tests/test_cli.py` (a run paused by a usage window finishes `done` after one sleep;
      a cap pause is not waited on).
    - [x] U2 · `P2` A resume after the CLI updated itself would fail on the deleted pinned binary.
      The current `claude` now takes over, with a warning, and the history entry of that start
      records its path and version.
      Proof: `test_the_registry_resumes_a_run_on_the_backend_it_recorded`.
- [x] `P1` **E11 · A second real run** after the fixes, to check them on the subscription.
  `runs/digits-quick-2`, profile `quick`, engine `cba39df`, resumed on `c1850a5` after the
  usage-window pause. Status `done`: 42 agent calls, all ok; 17 coding sessions; $3.42
  API-equivalent, nothing billed; 0.31 h running.
  - Validation: +0.0594 (0.9118 to 0.9712, 3 seeds).
  - Test, once, 10 seeds disjoint from search: +0.0532 (0.9103 ± 0.0101 to 0.9635 ± 0.0055).
  - Reviews: in-loop 3/10, held-out judge 4/10, reject.
  - Integrity: references 6/6 verified; two invented numbers flagged in the draft and repaired;
    no writer edit of the tables; egress only to the Anthropic API plus 6 logged fetches by
    agents with WebFetch.
  - It found R5 and R6, and the inconsistent export budget behind C14.
- [x] `P1` **E12 · Run 3, from scratch on the final engine** (`f470f27`), to check every fix
  live. `runs/digits-quick-3`, profile `quick`: status `done` in 0.31 h, with 36 agent calls, all
  ok, and 36 outcomes. $2.85 API-equivalent, nothing billed.
  - Idea CCI-CM, a class-contrast prototype init with a cosine-margin head.
  - Validation +0.0557. Test, once, on 10 disjoint seeds: +0.0465 (0.9103 to 0.9568).
  - Every PDF built in the sandbox. One invented number was flagged and repaired.
  - Egress went only to the API, plus 6 logged fetches by agents with WebFetch.
  - Judge 4/10.
  - Its ablations: removing the init costs 0.011 on test, while removing the cosine head gains
    0.006. So the head hurts, and a true paper would drop it.
  - It found R7: a writer that compiled its draft committed LaTeX's outputs into the paper, and
    the export carried them. These outputs are now ignored in every version.
    Proof: `test_the_export_is_the_commit_not_the_working_tree`.
- [ ] `P1` **E9 · The user guide** (`technical-writer`), from the real runs' behaviour.
- [ ] `P2` **E10 · Fold in tasks 2 and 6:** trace `docs/requirements.md` to the engine, and align
  the harness with task 6's four blocking decisions. Task 6's PR #3 adds positive lineage
  (IR-3.1–3.4 in its `docs/integrity/decisions/u-int-4-who-computes.md`): score only artifacts
  that a recorded fit job produced. The engine enforces lineage only by exclusion (checks.py);
  that is new work, here.
