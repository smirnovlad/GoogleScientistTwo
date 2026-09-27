# TODO

The ordered task list. Tick an item `- [x]` when it is done, and name the commit or file that
proves it. Add work you discover here, never only in chat. Priorities: `P0` blocks everything
after it; `P1` is needed before building; `P2` comes later.

## Phase 0: understand the paper, then decide the design (no engine code yet)

- [ ] `P0` **1 · A rigorous analysis of the paper.**
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
    - the stage primitive, if the stages really share one pattern;
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

- [ ] `P1` **5 · Scope, tasks and budget.**
  - Choose about three cheap development tasks and a test set. The note proposes the paper's five
    ICLR 2026 tasks; verify them against the paper.
  - Measure each task's compute.
  - Build a cost model for one task, checked against the paper's reported cost per task. The note
    quotes about $3,765; verify it.
  - Decide how we are billed: API or subscription.

- [ ] `P1` **6 · The evaluation-integrity design.** Owned by `evaluation-integrity-engineer`.
  - a threat model for each stage;
  - the locked harness;
  - the validation/test separation;
  - the verified-results table the writer sees;
  - deterministic gains;
  - an independent reporting judge;
  - the audit.

  Each guard comes with the attack it stops and a control that proves it works.

- [ ] `P1` **7 · Test strategy and mock mode.** A mock LLM and a mock coding agent, so the whole
  state machine can be tested for $0. `infrastructure-engineer` owns it.

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
