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

Always from a terminal:

```bash
cd <the repository>
git fetch origin
git worktree add --no-track -b claude/<what-the-work-is> .claude/worktrees/<what-the-work-is> origin/main
cd .claude/worktrees/<what-the-work-is> && claude
```

- ⛔ **Never start a task's session as a chat in the desktop app,** from its new-session button or
  from a suggested-task chip. Two reasons:
  - the app picks the folder and the branch itself: a generated name, based on `main`;
  - `claude --resume` from a terminal is what an account switch relies on
    ([switch-claude-account.md](switch-claude-account.md)), and resuming an app chat that way is
    untested.

  An agent that wants a new session opens a terminal and runs `claude` in the task's worktree. In
  the desktop app, a tab of its Terminal panel is a terminal. Rule set by Vlad on 2026-09-28, after
  two task sessions had been started from chips. An agent that must then watch the sessions it
  starts runs them in tmux: [Running task sessions in tmux](#running-task-sessions-in-tmux).
- **Name the branch and the folder after the work:** `claude/paper-analysis`, never a generated
  name. Use `codex/<…>` for work Codex writes.
- **`--no-track` keeps the new branch from tracking its base,** so `git status` and a bare
  `git push` never point at `main`. The first push names the branch:
  `git push -u origin claude/<what-the-work-is>`.
- **A task that needs an unmerged branch starts from that branch** instead of `origin/main`, and
  its first message says so. Once that branch is merged, the task brings itself up to date with
  `main`.
- `.claude/worktrees/` is in `.gitignore`, so worktrees never show in the main checkout's status.
- **The session's first message names its task,** and points at its item in `TODO.md`.
- **When one session starts another, the first message is a brief that session wrote.** Record it
  in `DEVELOPMENT_PROCESS.md` as that brief, naming its author. Only Vlad's own words go under
  "Vlad, verbatim".

## Running task sessions in tmux

One tmux session, `gs2`, holds one window per task session, named `T<n>` after the task's number
in `TODO.md`. The session that started them reads a window with `tmux capture-pane` and types into
it with `tmux send-keys`. Vlad opens a window in any terminal tab with `gs2 <n>`. Every session
survives a closed tab or app. Set up on 2026-10-02, after a guide Vlad uses in another project.

```bash
ops/sessions.sh start T2 "$PWD/.claude/worktrees/requirements" \
  claude --permission-mode auto --effort max "'Read .claude/brief.md in this worktree and follow it.'"
tmux capture-pane -p -t gs2:T2 | tail -8    # alive, or waiting at a prompt?
ops/sessions.sh list                        # a version number: Claude runs. zsh: it does not
```

- **The brief goes in a file,** `.claude/brief.md` in the task's worktree, and the first prompt
  only names it. `.gitignore` keeps the file out of commits.
  - ⛔ WHY NOT the brief as a command-line argument: a long one has arrived cut.
- **The first start in this repository stops at Claude Code's folder-trust prompt.** Its
  highlighted choice is "No, exit", so Enter alone ends the session. Vlad answers it, or approves
  in chat that the starting session answers it. The answer is recorded for the main checkout, not
  for each worktree, so a later worktree should not ask again (untested).
- **`restart` only an idle session.** It types `/exit`, which kills anything still running under
  the session. If the session has background tasks, `/exit` opens a dialog instead, and the script
  stops for a person to look.
- **Never run two Claude processes on one session id.** Before resuming a session anywhere else,
  exit it in its window.
- **A session reads `CLAUDE.md` when it starts.** After the rules change, merge them into its
  branch and `restart` it.
- **`gs2 <n>` is a shell function in `~/.zshrc`.** Each tab gets a grouped session of its own, so
  switching windows in one tab never moves another.
  - ⛔ WHY NOT a plain `tmux attach -t gs2`: every attached client shares one current window.

  ```zsh
  gs2() {
    local w="${1:-home}" s
    if [[ "$w" == <-> ]]; then w="T$w"; fi
    if [[ "$w" != T* && "$w" != home ]]; then command gs2 "$@"; return; fi
    if ! tmux list-windows -t gs2 -F '#W' 2>/dev/null | grep -qx -- "$w"; then
      echo "gs2: no window $w (see: tmux list-windows -t gs2)" >&2; return 1
    fi
    if [[ -z "$TMUX" ]]; then
      tmux new-session -t gs2 \; set destroy-unattached on \; select-window -t "$w"
    elif [[ "$(tmux display -p '#{session_group}')" == gs2 ]]; then
      tmux select-window -t ":$w"          # this tab already shows gs2: switch window here only
    else                                   # this tab shows another session: give it its own gs2 view
      s=$(tmux new-session -d -P -F '#{session_name}' -t gs2) || return
      tmux select-window -t "$s:$w" \; switch-client -t "$s" \; set -t "$s" destroy-unattached on
    fi
  }
  ```

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
