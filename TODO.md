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
  - **Found by task 2:** rank 1 is R-PRIM-1 to R-PRIM-10, the default stage configuration
    (`docs/requirements/03-stages.md`) and R-RUN-4's sequence. The register proposals that the
    requirements presume, such as U-TOP-2's retry policy and U-ART-15's access per role, are listed
    in `docs/requirements.md`; deciding one otherwise means revising the requirement that names it.
    Rank 1 also has a table of failures after retries for every role. The engine as built departs
    from the requirements once, by keeping the run's sequence and the seed and evolution loops in
    code (R-PRIM-1, R-PRIM-2, R-RUN-4); `docs/requirements.md`, *The engine as built*.
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
  - Decide how we are billed: API or subscription. **Decided by Vlad on 2026-10-02:** the Claude
    subscription, through `claude -p`, and no API (R-OPS-12). Budgets count calls, tokens and the
    subscription's usage windows, and a cost in dollars is recorded only for metered work.
  - **Found by task 2:** price more coding sessions than `docs/paper/analysis.md` section 9
    counts: its bound leaves out the specification filter after every code-producing unit and the
    manuscript checks after every revision (R-INT-4, R-INT-10; the elicitation's CONT-8).
  - **Found by task 2:** values the requirements name and wait for, under task 6's rules: the
    baseline tolerance (IR-15.3's formula), k (IR-15.5), the seed floor (IR-9.3) and the bound on
    attempts per identity (IR-33.3); the configuration refuses to load without them (R-STG-13). The
    gates' false-pass bound α defaults to 0.05 and the duplicate rule's attempts M to 3 × N_seed,
    both ours, which task 5 may change before a task's admission.
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

  **Found by task 2:** the requirements cite the second version's rules (adc3484) by their IR- IDs,
  and eleven of task 2's decisions adopt them, marked provisional in `docs/requirements.md`. When
  its review closes, recheck those rows and every clause that cites an IR- rule. The integrity review of the
  requirements (EI-13) proposes that people also check a random sample of the audit's passes, not
  only its flags; that is U-NOTE-4's to decide.

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

- [ ] `P2` **10 · Split `DEVELOPMENT_PROCESS.md`.** Found by task 2: every task branch appends to
  it, and it is past `CLAUDE.md`'s cap of 600 lines on two of them (639 lines on
  `claude/integrity-blockers`, 608 on `claude/requirements`, counted 2026-10-02; 655 on
  `claude/requirements` after its third revision). Split it, by
  period or by task, when those branches merge, so that no branch restructures a file all of them
  write. Vlad's quotes stay verbatim, each where its section is.

## Phase 1 onwards: build

Filled in by task 8, once tasks 1–7 are done and reviewed.
