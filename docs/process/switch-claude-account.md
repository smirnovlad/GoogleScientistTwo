# Switching Claude accounts without losing a session

**For** anyone working here with more than one Claude account of their own, when one account's
usage window is spent and work should carry on under another.

Each account has its own usage windows: a 5-hour one and a weekly one. Everything else a session
needs is a file on this machine: its transcript, the repository and its worktrees, the memory, and
the settings. So a switch changes who pays for the next turn. The work stays where it is.

## 1 · Before you switch

- **Let running sessions finish their step, or stop them.** A stopped session resumes from its
  transcript (§4).
- **Make sure the HANDOFF in `DEVELOPMENT_PROCESS.md` and `TODO.md` are current.**
- **Check that no environment variable overrides the login.** Claude Code uses these before the
  account you sign in with, so a switch would silently not happen:

  ```bash
  env | grep -E '^(ANTHROPIC_API_KEY|ANTHROPIC_AUTH_TOKEN|CLAUDE_CODE_OAUTH_TOKEN|ANTHROPIC_PROFILE)=' || echo "none set"
  ```

## 2 · Switch

**In the terminal.** One login serves every `claude` session run from it.

```bash
claude auth logout
claude auth login            # your Claude subscription; --console bills the API instead
```

Inside a running session, `/logout` and then `/login` do the same.

**In the desktop app,** which has its own sign-in, separate from the terminal's. Switch it from the
app's account menu.

⛔ **Switch both, or know which one you switched.** Otherwise a chat in the app and the sessions in
the terminal can run on different accounts, and the one whose usage is nearly spent keeps paying.

## 3 · Check which account is active

```bash
claude auth status --text
```

It shows the login method, the plan and the email. Inside a session, `/status` shows the same.
This is the **terminal's** login; the desktop app shows its own in its account menu.

## 4 · Resume the sessions

Resume each session from the folder it started in, under the new login:

```bash
cd '<the worktree or repository folder>' && claude --resume <session-id>
```

**To find a session's id,** run `claude --resume` with no id from that folder, and pick from the
list. The transcripts are files, named after the folder, with every character that is not a
letter, a digit or `-` replaced by `-`:

```bash
ls -t ~/.claude/projects/"$(pwd | sed 's#[^A-Za-z0-9-]#-#g')"/*.jsonl | head -5
```

If that lists nothing, use the picker instead.

⭐ **Resume from the SAME folder.** A session keeps the `CLAUDE.md`, hooks and MCP servers of the
folder it started in ([worktrees-and-sessions.md](worktrees-and-sessions.md)).

✅ **Tested on 2026-09-26, in another repository:** a session created under one account resumed
under another, and its next turn ran with its whole context.

## 5 · What changes, and what does not

| Stays the same: files on this machine | Belongs to the account |
|---|---|
| transcripts, the repository and its worktrees, memory, hooks | the usage windows (5-hour and weekly) |
| `~/.claude/settings.json`: model, effort | the prompt cache |
| project MCP servers (`.mcp.json`) | claude.ai connectors and scheduled routines |

- **The prompt cache does not carry over.** The first turn of a resumed session re-reads its whole
  context at full price on the new account. For a very long session, a fresh session started from
  the HANDOFF can cost less than `--resume`.
- **Model and effort come from your settings.** Check them with `/model` after switching.

## 6 · What the terms say

Anthropic's consumer terms, §2 *Account Creation and Access* (effective 8 October 2025, as read on
2026-09-26):

> *"You may not share your Account login information, Anthropic API key, or Account credentials
> with anyone else or make your Account available to anyone else."*

Switch only between accounts that are yours, and never sign another person into one of them.
[Consumer terms](https://www.anthropic.com/legal/consumer-terms) ·
[Claude Code authentication](https://code.claude.com/docs/en/authentication)
