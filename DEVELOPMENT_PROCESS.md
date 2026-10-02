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

## 2026-09-27: TODO task 1 starts, the rigorous analysis of the paper

**Vlad, verbatim:**

> "Read CLAUDE.md, TODO.md and DEVELOPMENT_PROCESS.md, then start TODO task 1."

The session runs in the main checkout, on the branch `claude/paper-analysis` (nothing reaches
`main` without review).

**The sources, pinned.** arXiv:2609.19644 has one version, v1 of 17 September 2026, under
CC BY 4.0 (the abstract page's licence link). Its TeX source, PDF and HTML are fetched by
`playground/paper/fetch_sources.sh` into the gitignored `.cache/`, with each sha256 recorded and
checked. The licence allows redistribution with attribution, so the paper's TeX text is committed
under `docs/paper/source/`. The one change is `main.tex` line 46, redacted in place because it
lists two e-mail addresses; the line count is kept, so line anchors still match the archive.

**Found before any agent ran** (each re-runnable from `playground/paper/`):
- **"Listing 1" or "Figure 4": the note was right.** The TeX puts the stage pseudocode in a minted
  `listing` float, and the arXiv PDF prints "Listing 1". The HTML (LaTeXML) turns it into
  "Figure 4", so HTML Figures 5–12 are PDF Figures 4–11. Tables and sections agree. The analysis
  cites the PDF's numbers (`float_numbering.py`).
- **Discussion is §4.3,** a subsection of the experiments, and the conclusion is §5.
- **The page references of Appendices C and D are wrong by five** in the arXiv PDF: the artifacts
  said to be on pp. 29–50 are on pp. 34–55, and the case-study draft is on pp. 56–71.

**How the work is organised.** `docs/paper/README.md` is the one brief every analyst and reviewer
follows: sources and their authority, numbering, citation format, classification, IDs, and which
file each writer owns. `playground/paper/check_citations.py` enforces the citation rule: every
statement cites the paper or is marked `[ours]`, every TeX anchor exists, and every quote of five
words or more is found in the source. Its `--selftest` shows each check failing on a planted
defect. Four `paper-analyst` agents then write in parallel, each reading the whole paper
independently: `analysis.md`, `claims.md`, `note-check.md` and `artifacts.md`. A consolidation
pass builds `unspecified.md` and `traceability.md`. Four personas review in parallel, the owner
fixes, and a blind reader tests the result.

**The analysts' work, as it landed** (each one read the whole paper, and I checked each one's
load-bearing claims against the PDF myself):
- **`artifacts.md`: the only evidence of what the agents actually return.** The appendix pages
  show a reproducibility audit that re-ran one method's scoring once, with no stated tolerance, and
  a search that tuned on the sets it reports. The HTML drops 23 of the 38 pages.
- **`note-check.md`: 125 claims of the note, none of them outright false.**
  - Its errors are overstatements, and ScientistOne's audit details presented as this paper's.
  - The paper claims that Listing 1 abstracts every stage, but only 1 of Table 1's 11 rows fits
    it exactly.
- **`claims.md` and `claims/`, with two scripts that re-run the arithmetic.**
  - ScholarPeer's reported acceptance cannot mean a score of 8 or more.
  - Under the held-out reviewer, the generated papers are accepted less often than the human
    papers they start from.
  - The 25.2% headline gain is a success-only mean read from the papers by an LLM.
- **Two analysts corrected the tooling:**
  - The brief wrongly said the paper numbers no equations; it numbers four.
  - The checker mispaired short quotes, and its default run skipped `claims/`.
- **`analysis.md`: its first run stalled** on a stream watchdog (a single very long write). It
  was resumed with its context, and told to write in chunks of at most about 120 lines.

**The review, and what it changed.** Six persona reviews ran in two waves, each through one lens,
and each is saved verbatim in `docs/reviews/paper-analysis-2026-09-27/`:
- research engineer, twice;
- evaluation-integrity engineer, twice;
- agent engineer;
- system architect.

They raised one blocker, and many overlapping majors. The blocker: `analysis.md` concluded that
Listing 1 is "a family resemblance, not a contract". Every way a stage departs from Listing 1 is
a parameter value, and the paper says it abstracts every stage with it. That conclusion would have
pushed the design towards one loop per stage, the monolith this project rules out.

Facts the reviews established, each checked here against its source:
- **Table 7's integrity audit is ScientistOne's, by reference.** Its protocol (five runs of a golden
  evaluator, an adaptive tolerance, a majority of three of five judges) is quoted from ScientistOne
  v1's TeX. That protocol assumes each task "provides a fixed evaluator"; ScientistTwo's tasks
  provide none, and the agents' own scripts compute every metric. ScientistOne is now pinned by
  the fetch script. The checker accepts a quote from it only on a line that cites it.
- **ScholarPeer's reported acceptance fits only "accept if the rating is at least 6"** on every row
  of the tables, assuming one integer rating per paper. It does not fit the threshold of 8 that
  §3.5 calls acceptance.
- **Every gain and success count is measured on the data the search selected on,** and nothing in
  the paper's loop separates validation from test.

`fix-list.md` merges all findings into 80 changes, each assigned to the owner of its document.
Where the reviews disagreed, the list records how they were reconciled.

**Consolidation.**
- **`unspecified.md` is the decision register.** It merges 133 gap items into 88 questions,
  each with the decision it forces, its owner and its priority: 27 block the design.
- **`traceability.md` maps all 127 paper elements.** It found duplicated and missing IDs.
- **Both come with coverage scripts** that fail on a missing or duplicated ID.
- **The register settled six disagreements between the analyses** from the paper itself. It also
  found that task 6 owns four blocking decisions, which must therefore come before task 3.

## 2026-09-28: the fixes, the closure checks, and the blind reader

**Vlad, verbatim.** He typed this on 2026-09-27, while two analyst agents had stalled on the stream
watchdog. It is quoted here late: the rule is to quote in the same turn.

> "contnue"

**The fixes.** Each analyst applied the fix list to its own documents, and each fixed document names
its fixes in a revision line. I checked every document against the list, fix by fix, before
committing it.
- **The blocker is fixed.** One primitive, with parameters per stage, covers every stage.
  `analysis.md` §3.4 gives each Table 1 row's values:
  - the generator;
  - what the critic judges, and what gets refined;
  - the assessor and its rule;
  - the verdict map;
  - the guard;
  - what the limit counts, and what happens at the limit;
  - nesting and fan-out.

  Listing 1 is one set of those values, and no stage takes it exactly. The earlier "only the
  subset row fits exactly" is withdrawn.
- **What crosses stages has its own table,** P-STATE-1 to 17. Each object has its producer, its
  consumers, its lifetime, and whether it may change.
- **Eight new gaps,** among them:
  - which data split each decision reads (U-TOP-5);
  - that no fixed evaluator exists (U-INT-4);
  - whether a stage at its limit keeps its last candidate or its best (U-TOP-7).
- **One fix was declined with evidence.** F-CL-7 said Figure 10b's smallest slice has no printed
  label. The raster prints 0.6% and 0.3% there, and `fig10_seed_labels.py` finds them. The
  reviewer accepted the decline.

**The closure checks.** Each reviewer then checked its own findings against the fixed documents. The
four reports are kept verbatim as `closure-*.md`.
- **Most fixes held.** The architect rated the blocker only partly fixed: the subset stage was still
  called an exact fit to Listing 1, in four places.
- **The checks found errors in the fix list:**
  - ScientistOne's five runs and its 1%/3σ tolerance are the settings of its own experiments (its
    §6). They are not part of the audit definition that ScientistTwo delegates to (its §5), and
    the fix list had merged the two.
  - One session span mixed two counting bases.
  - One citation did not bear on the claim it supported.
- **They also found two errors of mine:**
  - I had accepted "§6.1" from a TeX comment, in a file whose `\subsection` command is itself
    commented out.
  - My correction of a Table 4 argument did not follow. The corrected argument is stronger: at
    RALI's printed gain, no value for Pinet reproduces the table's median.
- **Every correction went back to the owner of its document,** and none was contested.

**The register and the map.**
- **The register:** `unspecified.md` holds 143 IDs in 93 rows.
  - Each blocking row carries its rank in the architect's list of what task 3 needs decided first.
    The primitive's parameters come first.
  - Task 6 owns four blocking rows: U-INT-4, U-TOP-5, A-INT-1 and A-INT-3. The integrity rules in
    `CLAUDE.md` already settle the first two in principle: a locked harness computes every metric,
    and every number an agent sees while searching is a validation number. `TODO.md` now puts
    these four decisions before task 3.
- **The map:** `traceability.md` maps all 177 paper elements. Its component column holds only
  candidates for task 3 to confirm, one stage primitive with per-stage configuration among them.
- **The pointers:** every gap entry points at its register row, and `register_coverage.py` fails
  when a pointer goes stale.

**The blind reader.**
- **Setup:** a `technical-writer` persona with no project context answered 28 questions. It read
  only a copy of `docs/paper/`, with the paper's source removed.
- **Result:** it answered 27 correctly from the documents alone, none wrong and none unanswered.
- **The one partial answer was a conflict between documents.** The "exact fit" correction had
  reached `analysis.md` but not three other documents.
- **It found a gap in my answer key as well:** the cheapest task is one that fails, at 10 or 11
  coding sessions, and only note-check.md said so.
- **All three defects it found are fixed.** The quiz, the marking and the answers are in
  `docs/reviews/paper-analysis-2026-09-27/blind-reader-quiz.md` and `blind-reader-answers.md`.

**The Codex review of the branch.** The parent `CLAUDE.md` requires a `/codex` review before a PR.
- **Setup.** The configured Codex model was refused for this account (`gpt-6-sol`), so the review
  ran on `gpt-6-astra`, the model of the earlier config, passed with `-c` for these runs only.
- **Three passes gated PASS,** with no [P1], and raised 16 findings at [P2] (7, 5 and 4). Each
  pass, its verdict and its fixes are recorded verbatim in
  `docs/reviews/paper-analysis-2026-09-27/codex-review.md`.
- **The first pass found three false passes in the citation checker:**
  - a location that does not exist, such as `[§999.999]`;
  - a fabricated quote wrapped across two lines;
  - the initial note's wording, which passed as the paper's.
- **It also found three more:**
  - a redaction check that would not have noticed the e-mail addresses coming back;
  - a reviewer's script that called an infeasible row "ok";
  - two claims that contradicted the rest of the analysis.
- **The second pass found that two of those fixes stopped short,** and three more gaps: any
  `[Ref:` text unlocked every cached source; an empty quote crashed the checker; an anchor could
  climb out of its folder.
- **The third pass found smaller edge cases:** a bare number after a location, a figure panel
  that does not exist, a fabricated fragment inside a quote cut with an ellipsis, and a false
  failure on page tags.
- **All were fixed.** The checker now verifies every location and figure panel a tag names, and
  binds `[Ref: key]` to that key's own cached source. Its self-test grew from 11 cases to 46.
  The documents passed the stricter checker unchanged.
- **The stopping rule was set before the third pass:** fix any [P1] before the PR, and fix
  further [P2] edge cases when cheap. No pass can settle whether a cited location supports its
  statement. That remains the job of the persona reviews and the blind reader.

## 2026-09-28: after task 1, the next tasks start in their own sessions

**Vlad, verbatim**, after the summary that PR #1 was open:

> "continue"

**PR #1 stays open.** It has no comment or review yet, and "continue" is not an approval to merge.
The next work is task 2 (requirements) and task 6's `P0` part (the four blocking decisions).

**This session does not take them on.** The rule is one task, one worktree, one session
(`docs/process/worktrees-and-sessions.md`), and this session is task 1's. Each is proposed as a
session of its own. Each starts from a branch of `claude/paper-analysis`, since task 1's
deliverables are not on `main` yet:
- **Task 2:** `claude/requirements`, writing `docs/requirements.md`.
- **Task 6's `P0` part:** `claude/integrity-blockers`, deciding U-INT-4, U-TOP-5, A-INT-1 and
  A-INT-3.

**The two can run in parallel.** Task 2 references task 6's decisions rather than making them.
Both append to this file, so it will need merging by hand.

## 2026-09-28: task sessions start from a terminal

**Vlad, verbatim**, on how the sessions for task 2 and task 6's `P0` part had been started:

> "btw, why do you start separate chats in claude code and not terminal session?"

The answer: they had been started from the desktop app's suggested-task chips.
`docs/process/worktrees-and-sessions.md` prescribes a terminal. Then:

> "Stop them and restart as terminal sessions – it should be a rule. Bcs I am not sure if such chats in claude code are saved in same way as terminal sessions"

**What the two app chats were.** For each one, the app made a worktree with a generated name
(`.claude/worktrees/nervous-…`), on a generated branch based on `main`. Each chat then switched to
its task branch, as its brief said.

**Both were stopped** after about ten minutes, before either began its task:
- task 2's had written one section of this file, not committed;
- task 6's had pushed one commit, `ed19388`, holding the same kind of section.

**Both sections were wrong in the same way.** They quoted the brief under "Vlad, verbatim", but
this session wrote the brief. The process guide now says how to record a brief.

**What the app stores,** checked for Vlad's question:
- the app writes the same JSONL transcripts as the terminal, in the same folders under
  `~/.claude/projects/`, and marks their lines `"entrypoint":"claude-desktop"`;
- `claude --resume`, run in one of those folders, opens its picker;
- resuming an app chat from a terminal was not tried.

**The rule** is now in `CLAUDE.md` and in `docs/process/worktrees-and-sessions.md`: a task's
session starts from a terminal, as `claude` run inside the worktree made for it, and never as a
chat in the desktop app. The guide also gains three points:
- `--no-track`, so a new branch never tracks its base;
- how to start from an unmerged branch;
- how to record a brief that one session writes for another.

**The restart.** Both task branches contain the commit that records this, so their sessions load
the new rule:
- `claude/requirements`, in `.claude/worktrees/requirements`. It had no commit of its own, and now
  starts from this one.
- `claude/integrity-blockers`, in `.claude/worktrees/integrity-blockers`. It keeps the app chat's
  commit, `ed19388`. Resetting the branch to drop it was refused as a destructive git action. So
  the branch merges `claude/paper-analysis` instead, and a commit on it corrects the brief's
  attribution.

**How each session runs:**
- in a tab of the desktop app's Terminal panel;
- started with `claude --permission-mode auto --effort max`, the mode and effort this session
  runs with;
- with a brief that names its author.

The two app chats stay stopped, not archived. Their worktrees are detached from the task branches
and hold nothing to keep.

## 2026-10-02: the task sessions relaunch in tmux

**Vlad, verbatim:**

> "Status of previous session in that worktree?"

**The 2026-09-28 terminal start never began.** Both sessions stopped at Claude Code's
folder-trust prompt, whose highlighted choice is "No, exit", and their tabs were later closed.
Checked on 2026-10-02:
- neither worktree had a transcript folder under `~/.claude/projects/`;
- the main checkout's entry in `~/.claude.json` still recorded no accepted trust. A worktree has no
  entry of its own: accepting the prompt in one flips the main checkout's entry;
- the Terminal panel held only Vlad's own tab;
- neither task branch had a commit past the restart.

So the last HANDOFF's "Running" was wrong: neither session ever ran.

**Vlad, verbatim** (the one edit: the path of an attached file replaced, marked […]. The file is a
guide to running Claude sessions in tmux, from another of his projects):

> "[…] Yes, relaunch both sessions in terminal, also use tmux for that so you can manage these sessions easily."

**What was set up, after that guide:**
- **`ops/sessions.sh`** keeps one tmux session, `gs2`, with one window per task session, `T<n>`.
  It can `start`, `restart` and `list` them. Each window's shell starts from an empty environment
  plus a short allowlist. So a task session never inherits the launching session's variables (its
  session id, its account, its messaging socket), whoever started the tmux server.
- **`gs2 <n>`**, a shell function added to Vlad's `~/.zshrc` after a backup, opens window `T<n>` in
  a terminal tab.
- **The brief is a file,** `.claude/brief.md` in the task's worktree, and the first prompt only
  names it. The guide records a long brief, passed on the command line, arriving cut. `.gitignore`
  now keeps the file out of commits. Until the task branches have that line, a local
  `.git/info/exclude` does.
- **Each brief is the 2026-09-28 one, unchanged,** under a relaunch note that this session wrote.
  The note names its author, quotes Vlad's words above, and says where the session runs.
- `docs/process/worktrees-and-sessions.md` gains a section on running task sessions in tmux.

**The relaunch:**
- window `T2`: task 2, in `.claude/worktrees/requirements`;
- window `T6`: task 6's `P0` part, in `.claude/worktrees/integrity-blockers`;
- each runs `claude --permission-mode auto --effort max`.

Both stopped at the trust prompt again. Vlad approved answering it for him. This session selected
"Yes, I trust this folder" in each window, and each session then read its brief and began.

**A Codex session works in parallel.** At 12:45 the main checkout moved from
`claude/paper-analysis` to `main`, and a worktree `.claude/worktrees/codex-reuse-survey` appeared,
on `codex/reuse-survey`. Vlad, verbatim:

> "its codex, I've also launched gpt astra"

This session leaves both alone. It commits to `claude/paper-analysis` through a worktree of its
own, `.claude/worktrees/paper-analysis`.

**Review.** The `/codex` gate, run with `gpt-6-astra`, failed the first version on one [P1] and one
[P2]. Both were fixed, then tested:
- **[P1] `env -i` on the tmux client does not clean a window.** A window inherits the tmux server's
  environment, and the server is shared. Now each window's shell starts under `env -i` itself. In
  the test, a fake `CLAUDE_CODE_SESSION_ID` was planted in the session's environment:
  - a window started the old way inherited it;
  - a window started by the script did not, and otherwise had the same 24 variables.

  The two running sessions were checked as well. Neither has a `CLAUDE_*` or `ANTHROPIC_*`
  variable, because this server had been started clean.
- **[P2] From inside another tmux session, `gs2 <n>` moved the tab into the shared session,** so two
  such tabs would switch windows together. Now it gives the tab a grouped session of its own. Each
  branch of the function was tested with a real tmux client on a pseudo-terminal.

A second pass passed: both fixes "appear correct", with no new finding and no sensitive
disclosure. `codex review` refuses custom instructions with `--uncommitted` as it does with
`--base`, so both passes named the diff in their instructions instead.

## 2026-10-02: the goal becomes a working engine, on the subscription

**Vlad, verbatim**, set as this session's goal:

> "As a result I expect to see working engine for auto research which replicates engine from paper ScientistTwo. I am going to use it based on my claude subscription – "claude -p" backend in future, take it into account. I don't wanna pay for API.
> Don't ask me anything, deliver replicated engine."

**What it changes:**
- **The engine is built now,** on `claude/engine` in `.claude/worktrees/engine`, from `docs/paper/`
  directly. TODO tasks 2–8 had put requirements, components and a build plan before any code.
  Tasks 2 and 6 keep running in `gs2:T2` and `gs2:T6`, and their outputs are folded in when they
  land.
- **Every agent runs through `claude -p`, on Vlad's subscription.** Nothing may bill the API.
- **No questions to Vlad.** Every open decision is taken here, and recorded with its reason and its
  `⛔ WHY NOT`.

**First finding: `--bare` would bill the API.** `claude --help` (2.1.287) says that under `--bare`
"Anthropic auth is strictly ANTHROPIC_API_KEY or apiKeyHelper via --settings (OAuth and keychain
are never read)". So the engine never passes `--bare`, and isolates its agents from Vlad's own
Claude setup by other means.

**Second finding: those other means work, on the subscription.** A probe put a canary `CLAUDE.md`
("The canary word is BLUEBERRY") in a scratch project, and asked `claude -p` (haiku, an
environment with no `ANTHROPIC_*` variable) for the canary and whether any instruction mentions
gstack or `DEVELOPMENT_PROCESS.md`, which only Vlad's global `~/.claude/CLAUDE.md` does:

| Flags | Canary | Global instructions | Auth |
|---|---|---|---|
| none (control) | BLUEBERRY | both seen | OAuth, no error |
| `--setting-sources ""` `--strict-mcp-config` `--mcp-config '{"mcpServers":{}}'` `--disable-slash-commands` | UNKNOWN | neither | OAuth, no error |
| the same, plus `--json-schema` | UNKNOWN | neither | OAuth, no error; a validated `structured_output` field |

So an engine agent sees only the prompt the engine gives it, and `--json-schema` gives each agent a
validated output. The JSON envelope also reports `total_cost_usd`: an API-equivalent figure, which
the ledger records as such, since the subscription bills nothing per call.

**Third finding: the stream reports the auth source and the usage windows.** With
`--output-format stream-json --verbose`, the `init` event carries `apiKeySource` ("none" on the
subscription) and a `rate_limit_event` carries the five-hour and seven-day windows (40% and 55%
used at the time). So the backend refuses any call whose `apiKeySource` is not "none", killing it
at the `init` event, and the budget guard pauses a run, resumably, before a window runs out.

**Fourth finding: `sandbox-exec` confines a real coding agent.** A `claude -p` coding session
(haiku, `bypassPermissions`) ran inside a profile that allows writes only to its workspace and
Claude's own state, and denies a "secret" directory. It wrote its file; reading the secret and
writing to the home directory each failed with "Operation not permitted"; it still ran on the
subscription. So the harness's labels are locked by the setup, not by a prompt.

**The build.** `docs/architecture/engine.md` is the contract. Two personas built data against it
in parallel: `agent-engineer` the 27 agents (`scientisttwo/agents/`), `research-engineer` the demo
task (`tasks/digits/`). This session built the engine in `scientisttwo/`: the backends, the run
store, the budget guard, the sandbox and the harness, workspaces, the stage primitive, the stages
of §3.1–§3.6 and §4.2, the export and the CLI.

**What the tests found.** A test that tried to write outside the workspace showed that the
profile left every temporary directory writable, so a run directory placed there could have its
result files forged by agent code. Now every profile protects the whole run directory, and
re-opens only the one directory a process needs; the test tries to forge a result, overwrite
another version and write to the home directory, and each fails. A cross-check of the 27 agents
against the stage code (variables passed, output fields read, verdict enums, schemas) found no
mismatch.

## 2026-10-02: the first real run, three reviews, and the fixes

**Run 1 finished end to end on the subscription** (`runs/digits-quick-1`, profile `quick`, not
committed: `runs/` is ignored). In 0.16 h it made 36 agent calls, 15 of them sessions with tools,
for $2.91 API-equivalent, with nothing billed; every call's `apiKeySource` was "none".

| | baseline | proposed (PCS-Init MLP) | gain |
|---|---|---|---|
| validation, `full` | 0.9118 ± 0.0170 | 0.9879 ± 0.0032 | +0.0761 |
| test, once at export | 0.9090 ± 0.0196 | 0.9638 | +0.0548 |

The peer reviewer scored it 3/10, the meta-reviewer asked for a refinement the guard then
refused (the refined code was unchanged), and the final judge, on opus, scored it 3/10, reject.
The chain worked as designed and found the flaw itself. Ablation A1 (standardisation with Glorot
initialisation) already scored 0.9759, so input standardisation carried 84% of the gain. The
ablation critic had accepted the idea, because it was never shown the baseline. Run 1 found four
engine defects, R1–R4 in `TODO.md`:
- the ablation critic lacked the baseline;
- the abstract said "no test split" beside the engine's test table;
- the rebuttal planner re-ran ablation A1;
- the critics' gain text did not state the margin.

**Three persona reviews ran in parallel,** and each is saved verbatim (machine paths redacted) in
`docs/reviews/engine-2026-10-02/`. The `agent-engineer`'s report came back as a hand-back. Every
finding is a checkbox in `TODO.md`:
- **Architecture:** a second backend needed four edits and could run unsandboxed; profile
  settings were ignored; one failed call stopped a run that resume could never recover; prompts
  were not pinned to their run.
- **Infrastructure:** seven P1s, each reproduced:
  - a stale result read for new code after a resume;
  - unrecorded spending;
  - a torn ledger line that blocked every resume;
  - pauses that turned permanent;
  - orphaned processes and no run lock;
  - an evaluation that could hang the engine;
  - agents able to break their own `.git`.

  Among its four P2s: agents could write the user's Claude settings, hooks and memory.
- **Integrity:** three P1s and two P2s.
  - It read one of 9 un-denied copies of the digits labels from inside the evaluation sandbox,
    and scored 1.0 on the test split.
  - Coding agents had the open internet.
  - The baseline had no numeric check, so a weaker baseline would inflate every gain.
  - Prose numbers were unchecked.
  - Reviewers read a results table a writer could edit.

**Probes behind the new sandbox** (`playground/engine/sandbox-probe/probe_agent.py`, one haiku
call each, 2026-10-02):

| Mode | Result |
|---|---|
| outbound network only to a local CONNECT proxy | works; the CLI reached only `api.anthropic.com` (and a telemetry host, now off) |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` | the `init` event's `memory_paths` is gone (it named Vlad's own memory folder) |
| a fresh `CLAUDE_CONFIG_DIR` | "Not logged in": the login is bound to the default config |
| no writes to `~/.claude`, `~/.claude.json`, `~/Library/Caches` | works |
| reads under `$HOME` limited to the CLI's binary and config, git's config, Python, the workdir | "Not logged in"; adding `~/Library/Keychains` makes it work, and `~/.claude` is not needed |

One more probe found a trap in the profile language. A deny written for `file-read*` does not
override an earlier allow of `file-read-data`. A deny pattern inside the allowed Python prefix
therefore still read the file, until the deny named `file-read-data` itself. A test caught it,
and with the fix the engine's own copy of the digits data is unreadable, while sklearn imports and
trains.

**The fixes,** in `cba39df`. The design contract (`docs/architecture/engine.md`, sections 1–5,
8 and 9) now describes them:
- reads under `$HOME` are an allowlist, plus task deny patterns;
- agents reach only the Anthropic API, through a logged egress proxy;
- evaluation runs an export of the version's commit, one directory per seed;
- the baseline must match the task's reported number;
- tables are regenerated for every reader, and prose numbers are checked;
- a `test_reporter` writes the test results into the text, and the final variants are scored on
  test once;
- the ablation critic reads the baseline and a `reject_share`;
- a run lock; process trees are watched, killed and reaped after a crash;
- one ledger line per attempt; replay checks the inputs hash; each run keeps a copy of its agents;
- the structural changes the architecture review asked for.

**Proof that the new checks catch what they claim:**
- Three tests failed on their first run, each because its check was not yet doing its job:
  - the tree-kill test, before the environment marker found a detached child;
  - the deny-pattern test, before the deny named `file-read-data`;
  - a stale orphan from the first attempt, still writing.
- 95 tests now pass on the mock backend, and the agent checker reports 0 problems on 28 agents.
- The `agent-engineer` ran a golden case live on run 1's real ablation inputs. The new critic
  returned `Reject`, which is what App. B's rule expects. A synthetic control shaped like LC-FTT
  returned `Refine`.

## 2026-10-02: the Codex gate fails, and the first fixes

- **The `/codex` gate** (gpt-6-astra, high effort, 15:32–16:05) returned **FAIL: 7 P1, 9 P2**,
  saved verbatim in `docs/reviews/engine-2026-10-02/codex.md`. TODO E8 lists them as C1–C16.
- **The worst one is real, and a sandbox probe confirmed it.** A sandboxed writer can make a
  symlink to a file it cannot read, though not a hard link. The engine reads, commits and copies
  versions outside the sandbox. So a linked `main.tex` would have sent a private file to a
  reviewer, and a linked `results.tex` let the engine overwrite a file outside the run. The fix
  sits at the one choke point every version passes, `finalize`, which removes such entries before
  git reads them; the manuscript code reads only regular files as a second line.
- **Fixed with tests** (each test fails on `cba39df`):
  - C1, links;
  - C2, export by commit;
  - C4, a unit is stored before its version is made, and a resume finishes the version;
  - C5, the task manifest pinned in `run.json`;
  - C6, the meta-reviewer's tables;
  - C8, a coding unit's replay check.
- **Task 6's blocker B1 is adopted:** a test seed is never a search seed. Their null control,
  rerun here, gives +1.32 of +2.65 kept on test with shared seeds. The digits test seeds are now
  100–109. Run 2 had read no test split yet, so its resume adopts them; `run.json` records the
  pin.
- **Decisions sent to the other sessions:**
  - To task 2 (requirements), on engine versus primitive-as-data: (b). Task 3 starts from
    `engine.md`, and the requirements record each departure.
  - To task 2 and task 6, on F-46: no question to Vlad. The extra reads of the test split are
    allowed, because none feeds a decision. Task 6 adopted this and records any read that could
    feed one as a violation.

## 2026-10-02: run 2 finishes, and the rest of the Codex findings

- **Run 2** (`runs/digits-quick-2`) resumed on `c1850a5` at 16:33, after the 16:00 reset. It
  finished `done` at 16:41:
  - 42 agent calls, all ok; $3.42 API-equivalent, nothing billed; 0.31 h of running time;
  - validation +0.0594 (3 seeds), test +0.0532 (10 seeds disjoint from search, read once);
  - in-loop review 3/10; the held-out judge gave 4/10, reject.
- **What its ablations show.** The idea combined a data-dependent orthogonal init (DOI) with
  class-balanced batches (CSB). On test, removing the idea's own mechanism gives 0.9139, near the
  baseline's 0.9103, so the gain is the idea's and not generic training controls. DOI alone (S1,
  0.9641) carries all of it, and CSB adds nothing measurable. A paper true to these numbers would
  claim the init alone.
- **What it found wrong in the engine:**
  - every PDF failed (R5);
  - a finished run kept its earlier pause reason (R6);
  - the export's budget said 40 calls beside 42 outcomes (folded into C14).

  R5 took a bisection of the build profile, rule by rule. bibtex writes beside its sources, and
  the build sandbox allowed writes only to a separate directory. A build now compiles an export of
  the commit, in a directory of its own.
- **The rest of the Codex findings are fixed**, each with a test that fails on `c1850a5`:
  - C3: a timeout kills the whole tree, and the reader is bounded;
  - C7: an orphan is reaped by pid, start time and marker;
  - C9: the ablation planner is read-only, by the `agent-engineer`;
  - C10: a failed call keeps its reported cost;
  - C11 and C12: attempts are journalled before the call and numbered across resumes;
  - C13: a heartbeat closes a dead engine's running time;
  - C14: the export's budget is taken last, and a summary is a copy;
  - C15: every sandbox test proves its child ran;
  - C16: the PDF build runs in the process-tree runner.

## HANDOFF, 2026-10-02 (run 2 done; every Codex finding fixed; the gate reruns next)

- **The goal** (Vlad, verbatim above): a working ScientistTwo engine on `claude -p`, on the
  subscription, delivered without questions.
- **Where it is:** branch `claude/engine` in `.claude/worktrees/engine`, stacked on
  `claude/paper-analysis` (PR #1, still open). `c1850a5` holds the first Codex fixes and task 6's
  B1; the next commit holds the rest (C3, C7, C9–C16) and run 2's R5 and R6.
- **State:**
  - **Run 1** (`runs/digits-quick-1`) finished `done` before the hardening (see above).
  - **Run 2** (`runs/digits-quick-2`) finished `done` on the subscription: test +0.0532 on 10
    disjoint seeds, judge 4/10. E11 is ticked; the section above has its numbers and findings.
  - **All 16 Codex findings are fixed with tests.** 113 tests pass on the mock backend, and
    `playground/engine/check_agents.py` reports 0 problems on 28 agents.
  - The `technical-writer` stopped at the session limit before it wrote the guide (E9).
- **Next steps:**
  1. Rerun the `/codex` gate on the whole branch, and fix or record what it finds.
  2. The guide (E9): relaunch, then review it against the code.
  3. Push. Open the engine's PR against `claude/paper-analysis`, with the Codex verdict in its body.
  4. A run 3 on the final engine, from scratch, for a clean end-to-end record.
- **To run the engine:** `python3 -m scientisttwo run --task tasks/digits --profile quick`, then
  `python3 -m scientisttwo status <run-dir>`, and `resume <run-dir>` after a pause. Outputs are in
  `<run-dir>/export/`. The guide (`docs/guide.md`) covers the rest.
- **Still true from the previous handoff:**
  - PR #1 awaits Vlad's review.
  - Tasks 2 and 6 run in tmux session `gs2` (`ops/sessions.sh list`; `gs2 <n>` opens one).
  - The `nervous-*` worktrees and `.claude/worktrees/paper-analysis` wait to be removed (Vlad's
    call for the one needing `--force`).
  - **Vlad's Codex session forked this engine.** At 14:08 it copied the `scientisttwo/` package,
    the agents, `engine.md` and the agent checker into `codex/engine-integration` (`462c4d0`).
    That was before this branch's hardening (`cba39df`, 14:55). It then built on the copy:
    - `codex/run-journal`, `codex/budget-admission`, `codex/verified-tables`, its own
      `scientist_two/` package;
    - a capped subscription run, a research-direction option for idea search;
    - `codex/rsi-uncertainty`.

    None of those branches holds `cba39df`: the allowlisted sandbox, the egress proxy, commit
    evaluation, the run lock and process reaping, and the per-attempt ledger exist only on
    `claude/engine`. Bringing the two lines together is a merge to plan with Vlad. This session
    leaves Codex's worktrees and branches alone.
- **If this session is lost:** read `TODO.md` ("Goal of 2026-10-02"), then this file's last two
  sections, then `docs/architecture/engine.md`.
