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
    - [ ] R2 · The test results go into the text through a `test_reporter` writer. Run 1's judge
      found the abstract saying "no test split" beside the test table.
    - [ ] R3 · The rebuttal planner reads the results already reported. Run 1 re-ran ablation A1
      as its only rebuttal experiment.
    - [x] R4 · The critics' gain text states the margin `min_delta`, so the LLM gates and the guard
      share one threshold.
  - From the agent engineer:
    - [x] A1 · `render` raises on undeclared variables.
    - [x] A2 · The idea generator reads each seed's novelty references.
    - [x] A3 · A reference whose search failed is `unchecked` and kept, never removed.
    - [x] A4 · Read-only agents keep `Bash` for git history; engine.md §3 now says why.
  - From the integrity review:
    - [ ] G1 · `P1` Evaluated code and agents read through an allowlist under `$HOME`, plus a
      task-declared deny pattern. The reviewer read one of 9 un-denied copies of the digits data
      and scored 1.0 on the test split.
    - [ ] G2 · `P1` Agents have no network beyond the Anthropic API: a local proxy with a host
      allowlist, and the sandbox denies every other outbound connection. Per-task extra hosts.
    - [ ] G3 · `P1` U-BASE-2: the reproduced baseline must match the task's reported numbers
      within a tolerance, or the run ends `baseline_failed` (a sandbagged baseline inflates gains).
    - [ ] G4 · `P2` Prose numbers in the manuscript are checked against `results.json`; unmatched
      numbers go to the audit.
    - [ ] G5 · `P2` Reviewers read results tables regenerated from result files, never the copy
      a writer could edit; an edited copy is an audit finding.
  - From the infrastructure review:
    - [ ] I1 · `P1` A stale result can never be read for new code: `evaluate` checks the commit,
      `rt.run` checks the inputs hash, exhausted transient retries pause the run, and each resume
      records the engine commit and the CLI version.
    - [ ] I2 · `P1` One ledger line per attempt, fsync'd, before the unit is stored.
    - [ ] I3 · `P1` A truncated last ledger line is repaired, not fatal.
    - [ ] I4 · `P1` `max_hours` counts running time, not paused time.
    - [ ] I5 · `P1` A run lock; each session's process groups recorded and killed as a tree;
      orphans from a crashed engine killed on resume.
    - [ ] I6 · `P1` An evaluation cannot hang the engine: output to a file, a bounded wait, and the
      whole tree killed.
    - [ ] I7 · `P1` Agents cannot write a workspace's `.git`; git errors become unit failures.
    - [ ] I8 · `P2` A result already delivered is used even if the CLI then lingers.
    - [ ] I9 · `P2` Retries start clean: one transcript per attempt, the workspace reset, and a
      cap on usage-limit waits.
    - [ ] I10 · `P2` Errors are classified by exit code and the CLI's own usage text; environment
      faults pause; the reset time comes from the exhausted window.
    - [ ] I11 · `P2` The sandbox keeps the user's Claude setup read-only (settings, hooks,
      CLAUDE.md, memory), auto-memory and auto-update are off, the CLI path is pinned, and each
      unit gets its own TMPDIR.
  - From the architecture review:
    - [ ] S1 · `P1` A backend registry, a backend per route, and a subprocess base class that
      always applies the sandbox.
    - [ ] S2 · `P1` Stage settings are validated per stage; peer review's "keep the best" is a
      rank, not an undocumented key; `novelty_refs` is removed; §4's pseudocode matches the code.
    - [x] S3 · `P1` The critics' verdict maps are one table (`stages/roles.py`), checked against
      the schemas before a run starts.
    - [ ] S4 · `P2` A unit failure that stops the run is retried on resume, not replayed forever.
    - [ ] S5 · `P2` A run pins its prompts: the agents are snapshotted into the run, and result
      keys and commits are carried into the paper's payload.
    - [ ] S6 · `P2` §8 records each departure the review listed, and §5 says who reads test results.
      The export ships each ablation and rebuttal variant as a patch. An ablation `Reject` on a
      restarted pass keeps the previous pass.
    - [x] S7 · `P2` A_Coder's two levels are one `run_level`; ablations and rebuttals share
      `run_variants`.
    - [ ] S8 · `P2` The state types live in `state.py` and shared steps in `stages/shared.py`;
      `child_env` moves to the sandbox module; the sandbox policy follows the agent's kind.
- [ ] `P1` **E11 · A second real run** after the fixes, to check them on the subscription.
- [ ] `P1` **E9 · The user guide** (`technical-writer`), from the real runs' behaviour.
- [ ] `P2` **E10 · Fold in tasks 2 and 6:** trace `docs/requirements.md` to the engine, and align
  the harness with task 6's four blocking decisions.
