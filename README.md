# GoogleScientistTwo

A replication of **ScientistTwo**, the autonomous research engine described in *ScientistTwo:
Pioneering the Human Knowledge Frontier with Autonomous AI* (Nam, Yoon, Pan, Wang, Meng et al.,
[arXiv:2609.19644](https://arxiv.org/abs/2609.19644), v1, 17 September 2026; project site
[scientist-two.github.io](https://scientist-two.github.io/)).

The goal is the **system**: an engine that takes a research problem, establishes baselines,
proposes and tests ideas, runs ablations, drafts a paper and answers simulated peer review. It is
built as components with explicit contracts, not as a monolith. Re-running the paper's full
benchmark is not the goal.

## Status

Initialised on 2026-09-27. The paper analysis is complete on the
`claude/paper-analysis` lineage. This branch adds a first executable engine
component, the [run journal](scientist_two/run_journal/README.md), with a
credential-free example and tests. The six-stage controller, task environments,
locked evaluator, drafting and reviewer backends are still open work in
[TODO.md](TODO.md).

## Start here

1. [CLAUDE.md](CLAUDE.md): how we work. It loads into every Claude session and every agent.
2. [TODO.md](TODO.md): the ordered task list.
3. [DEVELOPMENT_PROCESS.md](DEVELOPMENT_PROCESS.md): what happened and why. Its last HANDOFF entry
   says where we are and the exact next step.
4. [.claude/agents/README.md](.claude/agents/README.md): the personas, and when to use each one.
5. [docs/process/](docs/process/): working in parallel sessions, and switching Claude accounts
   without losing a session.

## Layout

```
CLAUDE.md                  working rules (no architecture until task 3 decides it)
TODO.md                    the task list
DEVELOPMENT_PROCESS.md     the running narrative and the handoff
.claude/agents/            the project's personas
docs/inputs/               material we were given, kept verbatim and marked unverified
docs/process/              how we work across sessions, worktrees and accounts
```

Folders for the analysis (`docs/paper/`), the requirements, the architecture and the code are
created by the tasks that fill them.

The run-journal slice lives in `scientist_two/run_journal/`; its scoped
requirements are in `docs/requirements/run-journal.md`. Run
`python3 -m unittest discover -s tests -v` and `python3 examples/mock_run.py`
from the repository root to verify it without credentials.
