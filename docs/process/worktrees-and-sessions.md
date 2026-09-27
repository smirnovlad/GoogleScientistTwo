# Worktrees and sessions: one task, one worktree, one session

**For** anyone starting work here: a person, or an agent launching a session for a task.

## The rule

**One task = one git worktree = one Claude session, started inside that worktree.** A second task
gets its own worktree and its own session.

**Why it matters.** A session loads `CLAUDE.md`, the hooks (`.claude/settings.json`) and the MCP
servers (`.mcp.json`) from the folder it **starts** in. Every agent it spawns receives that same
copy of `CLAUDE.md`. A session started in one folder and then moved into a worktree keeps the first
folder's rules, and so do its agents.

- ⛔ **Never move a running session into another worktree** instead of starting a new session there.
- ⛔ **Never move a session while its agents are running.** They lose their folder mid-run.

## Starting a task

```bash
cd <the repository>
git fetch origin
git worktree add -b claude/<what-the-work-is> .claude/worktrees/<what-the-work-is> origin/main
cd .claude/worktrees/<what-the-work-is> && claude
```

- **Name the branch and the folder after the work:** `claude/paper-analysis`, never a generated
  name. Use `codex/<…>` for work Codex writes.
- `.claude/worktrees/` is in `.gitignore`, so worktrees never show in the main checkout's status.
- **The session's first message names its task,** and points at its item in `TODO.md`.

## While working

- **Commit at every milestone, and push the branch,** so nothing lives on only one machine.
- **Parallel sessions share a few things:**
  - the git stash: never run a bare `git stash`;
  - GPUs, ports and containers;
  - any shared data.

  Before taking a shared resource, say so to the other sessions, and note it in
  `DEVELOPMENT_PROCESS.md`.
- **Record Vlad's instructions verbatim** in `DEVELOPMENT_PROCESS.md`, in the same turn.

## Finishing

1. Review the change: the persona gate in `.claude/agents/README.md`.
2. Merge it into `main`.
3. Remove the worktree, only after its branch is merged:
   `git worktree remove .claude/worktrees/<name>`. Never delete an unmerged branch.

## Resuming, and switching accounts

A stopped session continues from its own folder:

```bash
cd .claude/worktrees/<name> && claude --resume <session-id>
```

It runs under whichever account the terminal is signed in to. To move to another account first,
follow [switch-claude-account.md](switch-claude-account.md).
