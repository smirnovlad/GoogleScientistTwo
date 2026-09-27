# Development process

The running narrative: what happened, and why, newest at the bottom. Vlad's instructions are
quoted verbatim, in the same turn they arrive, because a paraphrase is already an interpretation.
A **HANDOFF** entry says where we are and the exact next step. It is kept current at every
milestone, so a context compaction or a switch of Claude account loses nothing.

## 2026-09-27: the repository is initialised

**Vlad, verbatim** (the one edit: a local folder path replaced, marked […]):

> "[…] – I wanna use these skills of multiple claude accounts sharing same sessions in that project"
>
> "I wanna implement research engine from that paper: https://arxiv.org/abs/2609.19644
>
> So your task is to initialize project for that (to use claude terminal sessions) and create todo
> list with further tasks:
>
> * Analyze paper thoroughly and understand how does it work so we can write code to replicate it.
>   Analysis should be rigorous so we implement really solid and strong system. Maybe create
>   dedicated personas in advance: system architect, research engineer and so on. We should use
>   best coding practices for that project: use abstractions, identify components of that engine
>   (so its not just monolith) and so on
>
> At first just initialize repo – I will ask agent to start this job from dedicated chat"

With it he pasted a replication note from another assistant chat. It is saved as
[docs/inputs/2026-09-27-initial-replication-note.md](docs/inputs/2026-09-27-initial-replication-note.md),
and it is unverified.

Earlier the same day, in another project's chat, about the tooling behind the first sentence:
*"I think it is very important tool which allows me to switch between different claude accounts
without lose of any context using same worktrees and claude sessions."*

**What it changed:**
- `CLAUDE.md` holds working rules only, since the architecture comes from the analysis. Its
  principles:
  - quality first;
  - the paper is the specification;
  - requirements before code;
  - components, not a monolith;
  - research integrity enforced by the setup;
  - one task per worktree per session.
- **Six personas were created in advance,** in `.claude/agents/`:
  - `paper-analyst`;
  - `system-architect`;
  - `research-engineer`;
  - `evaluation-integrity-engineer`;
  - `agent-engineer`;
  - `infrastructure-engineer`.

  Each judges by a different measure, and the routing table is in the folder's README.
- **`TODO.md` sets the order:** analysis, then requirements, then components, then reuse, scope,
  integrity and testing, and only then a build plan.
- **Two process guides** in `docs/process/`: working in parallel worktrees, and switching Claude
  accounts without losing a session.

**Found while initialising:**
- The paper is *ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI*, v1 of
  17 September 2026, per the arXiv abstract page. Its table of contents, read from the HTML version:
  - six stages in §3.1–3.6;
  - Tables 1–11;
  - Appendices A–D, where A.2 is the configuration.
- The HTML shows the stage pseudocode as a figure (Figure 4), where the pasted note says
  "Listing 1". It is a first sign that the note must be checked claim by claim (TODO task 1).
- The GitHub repository is public, so no secret, credential, email address or local path may be
  committed (`CLAUDE.md`).

## HANDOFF, 2026-09-27

- **Done:** the repository is initialised. No design and no code yet.
- **Next step:** open a Claude session in this repository and give it TODO task 1, the rigorous
  analysis of the paper, owned by `paper-analyst`.
  - For one session on `main`: `cd <this repository> && claude`.
  - For a task branch, start the session inside a worktree
    ([docs/process/worktrees-and-sessions.md](docs/process/worktrees-and-sessions.md)).
