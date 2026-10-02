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

Initialised on 2026-09-27. The analysis of the paper is in [docs/paper/](docs/paper/). Since
2026-10-02 a working engine exists on the branch `claude/engine`, not yet merged: it has finished
two small runs on the demo task, on a Claude subscription. Open work is in [TODO.md](TODO.md).

## The engine

`scientisttwo/` runs the pipeline end to end: every agent is a `claude -p` process on the
logged-in subscription, never the paid API, and every evaluation runs in a macOS sandbox against
a locked harness. To run it:

```sh
python3 -m scientisttwo run --task tasks/digits --profile quick --wait
```

- [docs/guide.md](docs/guide.md): how to run it, resume it, read what it produced, add a task, and
  what it does and does not guarantee.
- [docs/architecture/engine.md](docs/architecture/engine.md): the design, its contracts and the
  reasons for each decision.

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
docs/paper/                the analysis of the paper
docs/architecture/         the engine's design
docs/guide.md              how to use the engine
scientisttwo/              the engine
tasks/                     tasks the engine can run (tasks/digits is the demo)
tests/                     the whole engine on a mock backend, for $0
```
