# GoogleScientistTwo — project instructions

We are replicating the research engine of **ScientistTwo** ([arXiv:2609.19644](https://arxiv.org/abs/2609.19644)).
⏩ Read [TODO.md](TODO.md) and the last HANDOFF in [DEVELOPMENT_PROCESS.md](DEVELOPMENT_PROCESS.md) first.

> **Scope discipline.** This file holds WORKING RULES only. The architecture is decided by TODO
> tasks 1–3, written to `docs/architecture/`, and linked from here once it is agreed. Writing a
> component list here before the analysis would pre-commit a design nobody has checked.

⚠️ **This repository is public on GitHub** (checked 2026-09-27). Never commit a secret, an API
key, a credential, an email address, or a path from someone's machine.

## Principles

1. **Quality first.** Time and tokens are the cheap resource; a wrong system is the expensive one.
   Take the root fix, never the band-aid that moves a threshold.
2. **The paper is the specification.** Every statement about it cites its section, table, figure
   or appendix, taken from the paper's own text (the TeX source or the HTML). Never cite it from a
   summary. The note in `docs/inputs/` is a summary, and it is unverified.
3. **Requirements before code.** Every feature starts with its goal, its requirements and one
   acceptance test for each requirement. A requirement with no test is a wish.
4. **Components, not a monolith.** Every part of the engine has a contract (its inputs, its
   outputs, its failure modes) and lives in its own folder. What varies sits behind an interface.
5. **Independent review by several personas, built in parallel.** Build the reversible half while
   the review of the one-way half runs. A review reads a design; a run shows what the design gets
   wrong. Neither replaces the other.

## The paper is the spec

- **Sort every statement about the engine into one of three kinds:**
  - SPECIFIED, with its location in the paper;
  - UNSPECIFIED, which makes it our decision, recorded with its reason;
  - AMBIGUOUS or INCONSISTENT, which gets flagged and never silently resolved.
- **Open the source before you cite it.** A claim about the paper, a library or a number is not
  sayable until you have read the thing, in the same turn. Remembering it does not count.
- **Traceability.** Each element of the paper maps to a requirement, and each requirement maps to
  a component. The map lives in `docs/paper/` once task 1 creates it.

## Research integrity: enforced by the setup, never by a prompt

These are the working rules. Task 6 turns each into a requirement with a test.

- **Metrics come only from the locked evaluation harness.** Code an agent wrote never writes a result.
- **Evaluation code and data are read-only to every agent,** and they are checked against hashes.
- **Every number an agent sees while searching is a VALIDATION number.** The test set is used once, at the end.
- **The manuscript writer sees only verified results.**
- **Gains are computed deterministically from the result files.**
- **The judge we report is never the reviewer we optimise against.**
- **Every run is reproducible** from its recorded configuration, seed, code commit and container image.

## Engineering rules

- **One component, one folder. One file, one job,** capped at 600 lines. The cap is a proxy: split
  by responsibility, never into halves that must be read together.
- **A second implementation of anything is an interface or a base class, never a copy.** Coding
  backends, LLM providers, sandboxes, reviewers and tasks will each have more than one.
- **Behaviour is DATA, run by generic code.** Prompts, output schemas, loop limits, model routing and
  budgets are versioned files. A new agent should be mostly a prompt and a schema, not a new code path.
- **Every external dependency sits behind an interface with a mock,** including the LLM and the
  coding agent. The whole engine must run in tests for $0.
- **Long runs resume.** Every stage writes its output to disk, and a crash resumes from the last
  finished stage. A retry never spends twice for the same work.
- **Cost is bounded and recorded.** There is a budget guard per session and per task. An unknown
  cost is recorded as unknown, never as zero.
- **Describe an algorithm as structure, never as prose.** Give pseudocode, each step's inputs and
  outputs, the decision points with their thresholds, and the failure branch of every step.
- **Record each decision beside the code it constrains,** with the road not taken: a line
  `⛔ WHY NOT <the alternative>`, then the reason.
- **A green check must prove it ran.** Before you report a zero, show that the same query can
  return something other than zero. A number carries its sample: n, date and source.
- **Log each unit of work** (a stage, an agent call, a run) with its inputs, outputs, cost and
  timing. Keep run history as data you can query, not only as text.
- **A bound on model-bound content is a product decision.** A slice, a cap or a top-k on what a
  model reads says on the same line who chose it and what it loses. The default is everything.

## Personas: route by the question

The roster and its routing table are in [.claude/agents/README.md](.claude/agents/README.md).
- **Route work to the persona whose lens fits, automatically.** Never hand it to a generic agent.
- **Run reviews in parallel, one lens each.**
- **Before several agents design something, write its requirements file** and point every agent
  at that one file. Otherwise each agent invents its own problem.

## Sessions, worktrees and Claude accounts

- **One task = one git worktree = one Claude session, started inside that worktree.** A session
  loads `CLAUDE.md`, the hooks and the MCP servers from the folder it starts in. How:
  [docs/process/worktrees-and-sessions.md](docs/process/worktrees-and-sessions.md).
- **Switching to another Claude account at a usage limit keeps every session.** Transcripts live
  on this machine, so `claude --resume` continues them under the new login:
  [docs/process/switch-claude-account.md](docs/process/switch-claude-account.md).
- **Keep the HANDOFF current at every milestone,** not at the end. A compaction or an account
  switch must lose nothing that the files do not hold.

## Where things are written

| Where | What |
|---|---|
| `DEVELOPMENT_PROCESS.md` | the running narrative and the HANDOFF. Vlad's instructions are quoted VERBATIM, in the same turn they arrive |
| `TODO.md` | open work as a checkbox list: tick it with its proof, add discovered work here, never only in chat |
| `docs/paper/` | the analysis of the paper (task 1) |
| `docs/findings/YYYY-MM-DD-<slug>.md` | a conclusion that took real work to establish |
| `docs/reviews/<topic>-YYYY-MM-DD/` | a long review or research run's raw output, saved the moment it finishes, verbatim |
| `playground/` | the script that produced a claim, kept so the claim can be re-run |

## Git

- **Commits are written in a plain human voice.** No AI attribution, and no Co-Authored-By lines.
- **A branch name says what the work is:** `claude/<task>`, or `codex/<task>` for work Codex writes.
- **Never run a bare `git stash`.** Parallel worktrees share one stash stack.
- **Nothing reaches `main` without review.**
