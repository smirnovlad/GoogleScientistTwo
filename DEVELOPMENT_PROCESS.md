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

## 2026-09-28: task 6's `P0` part starts, the four blocking integrity decisions

**The brief, verbatim.** The session that finished task 1 wrote it. Vlad's own words behind it are
"continue", quoted in the previous section. This section first labelled the brief "Vlad, verbatim",
which was wrong; corrected on 2026-09-28.

> Start the `P0` part of TODO task 6 (the evaluation-integrity design) of the GoogleScientistTwo repository. The project replicates the research engine of ScientistTwo (arXiv:2609.19644).
>
> ## Read first, and follow
>
> - `CLAUDE.md`, `TODO.md` (task 6, its "`P0` part, before task 3"), and the last HANDOFF in `DEVELOPMENT_PROCESS.md`. They set the working rules:
>   - the paper is the specification;
>   - integrity is enforced by the setup, never by a prompt;
>   - route work to personas by the question they judge;
>   - every change passes the review gate;
>   - commits are in a plain human voice, with no AI attribution and no Co-Authored-By lines;
>   - never run a bare `git stash`.
> - **The repository is public on GitHub.** Never commit a secret, an e-mail address or a path from someone's machine.
>
> ## Base branch
>
> - Task 1's deliverables are on branch `claude/paper-analysis`, in PR #1 (https://github.com/smirnovlad/GoogleScientistTwo/pull/1). PR #1 is open and not merged into `main`.
> - Create your branch from it: `git fetch origin && git checkout -b claude/integrity-blockers origin/claude/paper-analysis`. If you are in the main checkout rather than a fresh worktree, add a worktree instead: `git worktree add -b claude/integrity-blockers .claude/worktrees/integrity-blockers origin/claude/paper-analysis`.
> - After PR #1 merges, bring your branch up to date with `main`.
>
> ## The task
>
> Task 6 owns four blocking rows of `docs/paper/unspecified.md`. Decide them before task 3 writes the harness and audit contracts.
>
> 1. **U-INT-4, with alias U-ART-16: who computes every metric the engine reads or reports.**
>    - In the paper, the agent's own script scores both methods, baseline included, and writes the report.
>    - `CLAUDE.md` already requires a locked evaluation harness.
> 2. **U-TOP-5, with aliases U-NOTE-1 and U-ART-5: which data split each decision in the loop reads.**
>    - The paper reads the benchmark it reports.
>    - `CLAUDE.md` already requires that every number an agent sees while searching is a validation number.
> 3. **A-INT-1, with aliases A-NOTE-10 and A-ART-2: integrity as gates inside the run, or only as a post-hoc audit.** §4.2 and App. B of the paper contradict each other on this.
> 4. **A-INT-3: keep the post-hoc auditor apart from the in-loop fixer.**
>
> **Where the evidence is:**
> - each row's full entry and its register row (`docs/paper/stages/07-integrity.md`, `docs/paper/artifacts.md`);
> - `docs/paper/claims.md`: P-EVAL-2, U-EVAL-1 and U-EVAL-5;
> - ScientistOne's audit, which Table 7 follows by reference (arXiv:2605.26340v1 §5). `bash playground/paper/fetch_sources.sh` caches it.
>
> **Output:** a decisions document, for example `docs/integrity/blocking-decisions.md`, with its location recorded in the HANDOFF. Give each decision:
> - the choice;
> - the attack it stops;
> - a control that proves it works;
> - the road not taken, as `⛔ WHY NOT`.
>
> Then add a pointer to your decision in each of the four register rows. Change only those rows: a parallel task-2 session may edit other rows of the same file.
>
> ## Who does it
>
> - **Owner:** the `evaluation-integrity-engineer` persona.
> - **Review:** in parallel by `research-engineer` and `system-architect`, per the review gate in `.claude/agents/README.md`. Save reviews verbatim in `docs/reviews/integrity-blockers-<date>/`.
>
> ## Boundaries with other tasks
>
> - A parallel session may be writing `docs/requirements.md` (task 2). It will reference your decisions; do not edit its file.
> - Components are task 3's. Decide the rules, not the component design.
>
> ## Process
>
> - **Commits:** commit at every milestone, push, and keep the HANDOFF current.
> - **Vlad's instructions:** quote them verbatim in `DEVELOPMENT_PROCESS.md`, in the same turn. Append a new section, and expect to merge that file by hand with the parallel session.
> - **Before the PR,** run the `/codex` review gate required by the parent `CLAUDE.md`. On this machine it needs two workarounds:
>   - the configured model `gpt-6-sol` is refused on this ChatGPT account, so pass `-c model="gpt-6-astra"`;
>   - `codex review` rejects custom instructions together with `--base`, so drop `--base` and name the range in the instructions (`git diff claude/paper-analysis...HEAD` while PR #1 is open).

**Setup.** The session runs in its own worktree, on `claude/integrity-blockers`, branched from
`origin/claude/paper-analysis` at `08a60b3`. The new branch first tracked `claude/paper-analysis`,
so a bare `git push` would have gone to PR #1's branch; the upstream was unset, and this branch
pushes to its own name. (With `push.default` unset, as here, git refuses such a push rather than
making it.)

**That session was a chat in the desktop app,** in a worktree the app named
`.claude/worktrees/nervous-rosalind-80b87b`. It was stopped at Vlad's instruction before it began
the task, and the task restarted from a terminal (next section).

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

## HANDOFF, 2026-10-02 (PR #1 awaits review; tasks 2 and 6 run in tmux)

- **Done and pushed** on `claude/paper-analysis`:
  - TODO task 1, ticked in `TODO.md` with its proof;
  - the Codex review's fixes;
  - the rule that task sessions start from a terminal;
  - `ops/sessions.sh`, and the tmux section of `docs/process/worktrees-and-sessions.md`.
- **All checks passed on 2026-09-28.** The commits since then touch none of the files they check:
  - `check_citations.py`: 18 files, 0 problems, and its self-test's 46 cases;
  - `register_coverage.py` and `trace_coverage.py`: 0 problems each, with their self-tests;
  - `claims_arithmetic.py`: exits 0;
  - `fetch_sources.sh`: the sources match their sha256, and the redaction is exact.
- **Open:** PR #1 (https://github.com/smirnovlad/GoogleScientistTwo/pull/1), `claude/paper-analysis`
  into `main`, with no review or comment as of 2026-10-02. Its description carries the Codex
  verdict. The repository has no CI yet, so no checks run on it.
- **Running, in the tmux session `gs2`.** `ops/sessions.sh list` shows the windows, and `gs2 <n>`
  opens one in a terminal tab.
  - `T2`: task 2, in `.claude/worktrees/requirements`, on `claude/requirements`. Session
    `be5dd052-f8df-4809-9900-03547c214b13`.
  - `T6`: task 6's `P0` part, in `.claude/worktrees/integrity-blockers`, on
    `claude/integrity-blockers`. Session `5c73bd1a-2ecb-42b9-bf9c-0e03b8630828`.

  To continue one that has stopped:
  `ops/sessions.sh restart T<n> claude --permission-mode auto --effort max --resume <its session>`.
- **Also running, not ours:** a Codex session, in `.claude/worktrees/codex-reuse-survey`, on
  `codex/reuse-survey`. The main checkout is on `main`, where that session left it.
- **Next steps:**
  1. Vlad reviews PR #1. Merge to `main` only with his approval. The commits made after the Codex
     passes change only process documents and `ops/sessions.sh`. They get a Codex pass of their
     own before the merge.
  2. Tasks 2 and 6's `P0` part continue in their sessions. Once PR #1 is merged, each brings its
     branch up to date with `main`.
  3. Remove the two stopped app chats' worktrees, `nervous-rosalind-80b87b` and
     `nervous-wozniak-48c870`. The app no longer lists those chats, so archiving them cannot remove
     the worktrees. `nervous-wozniak-48c870` holds an uncommitted section not worth keeping, so
     removing it takes `git worktree remove --force`: Vlad's call.
  4. Remove `.claude/worktrees/paper-analysis` once no session needs it.
- **If this session is lost:**
  - Run `bash playground/paper/fetch_sources.sh`, then read `docs/paper/README.md`.
  - The review record is in `docs/reviews/paper-analysis-2026-09-27/`. Start from `fix-list.md`,
    whose last section records the outcome of every fix, and from `codex-review.md`.

## 2026-10-02: task 6's `P0` part is relaunched in a terminal, under tmux

**The relaunch note, verbatim.** The coordinating session of 2026-10-02 wrote it, at the top of
this session's brief, and said that it wrote nothing else:

> ## Relaunch note, 2026-10-02
>
> The coordinating session of 2026-10-02 relaunched you and wrote only this note. The brief below it
> is unchanged from 2026-09-28. Record the two together, each under its author.
>
> - **The 2026-09-28 terminal start never began.** It waited at Claude Code's folder-trust prompt
>   until its tab was closed, and left no transcript and no commit. Nothing of it carries over.
> - **Vlad's words behind the relaunch, verbatim:** "Yes, relaunch both sessions in terminal, also
>   use tmux for that so you can manage these sessions easily."
> - **You run in tmux,** in window `T6` of the session `gs2`. The coordinating session can read your
>   screen and type into it. Vlad opens your window with `gs2 6`.
> - **A Codex session also works in this repository,** in `.claude/worktrees/codex-reuse-survey`, on
>   `codex/reuse-survey`. Leave its worktree alone.

**Vlad, verbatim,** as the relaunch note quotes him:

> "Yes, relaunch both sessions in terminal, also use tmux for that so you can manage these sessions easily."

**The brief, verbatim.** The session that finished task 1 wrote it on 2026-09-28, and the relaunch
note says it is unchanged since. Vlad's own words behind it are "continue", and his instruction to
restart the task sessions from a terminal, both quoted above. Its task, evidence and output match
the brief quoted in "2026-09-28: task 6's `P0` part starts"; its sections "Who wrote this brief"
and "Where you are" are new, and its section "Base branch" is gone.

> Start the `P0` part of TODO task 6 (the evaluation-integrity design) of the GoogleScientistTwo repository. The project replicates the research engine of ScientistTwo (arXiv:2609.19644).
>
> ## Who wrote this brief
>
> The session that finished task 1 wrote it. It is not Vlad's own words. His words behind it are "continue", and then his instruction to restart the task sessions from a terminal. `DEVELOPMENT_PROCESS.md` quotes both. Record this brief there verbatim, in a new section, as the brief and with its author, never under "Vlad, verbatim" (`docs/process/worktrees-and-sessions.md`).
>
> A first attempt ran as a desktop-app chat and was stopped before it began the task. Its only trace is a section of `DEVELOPMENT_PROCESS.md` that records its brief, now corrected. That brief matched this one, apart from this section and the next. `DEVELOPMENT_PROCESS.md` also records the restart ("task sessions start from a terminal").
>
> ## Read first, and follow
>
> - `CLAUDE.md`, `TODO.md` (task 6, its "`P0` part, before task 3"), and the last HANDOFF in `DEVELOPMENT_PROCESS.md`. They set the working rules:
>   - the paper is the specification;
>   - integrity is enforced by the setup, never by a prompt;
>   - route work to personas by the question they judge;
>   - every change passes the review gate;
>   - commits are in a plain human voice, with no AI attribution and no Co-Authored-By lines;
>   - never run a bare `git stash`.
> - **The repository is public on GitHub.** Never commit a secret, an e-mail address or a path from someone's machine.
>
> ## Where you are
>
> - You run in the worktree `.claude/worktrees/integrity-blockers`, on the branch `claude/integrity-blockers`, which tracks `origin/claude/integrity-blockers`. Check it with `git status -sb` before your first commit.
> - The branch contains `claude/paper-analysis`, which holds task 1's deliverables in PR #1 (https://github.com/smirnovlad/GoogleScientistTwo/pull/1). PR #1 is open and not merged into `main`. After it merges, bring your branch up to date with `main`.
> - If you need another Claude session, start it from a terminal, never as a desktop-app chat (`CLAUDE.md`). Subagents are unaffected.
>
> ## The task
>
> Task 6 owns four blocking rows of `docs/paper/unspecified.md`. Decide them before task 3 writes the harness and audit contracts.
>
> 1. **U-INT-4, with alias U-ART-16: who computes every metric the engine reads or reports.**
>    - In the paper, the agent's own script scores both methods, baseline included, and writes the report.
>    - `CLAUDE.md` already requires a locked evaluation harness.
> 2. **U-TOP-5, with aliases U-NOTE-1 and U-ART-5: which data split each decision in the loop reads.**
>    - The paper reads the benchmark it reports.
>    - `CLAUDE.md` already requires that every number an agent sees while searching is a validation number.
> 3. **A-INT-1, with aliases A-NOTE-10 and A-ART-2: integrity as gates inside the run, or only as a post-hoc audit.** §4.2 and App. B of the paper contradict each other on this.
> 4. **A-INT-3: keep the post-hoc auditor apart from the in-loop fixer.**
>
> **Where the evidence is:**
> - each row's full entry and its register row (`docs/paper/stages/07-integrity.md`, `docs/paper/artifacts.md`);
> - `docs/paper/claims.md`: P-EVAL-2, U-EVAL-1 and U-EVAL-5;
> - ScientistOne's audit, which Table 7 follows by reference (arXiv:2605.26340v1 §5). `bash playground/paper/fetch_sources.sh` caches it.
>
> **Output:** a decisions document, for example `docs/integrity/blocking-decisions.md`, with its location recorded in the HANDOFF. Give each decision:
> - the choice;
> - the attack it stops;
> - a control that proves it works;
> - the road not taken, as `⛔ WHY NOT`.
>
> Then add a pointer to your decision in each of the four register rows. Change only those rows: a parallel task-2 session may edit other rows of the same file.
>
> ## Who does it
>
> - **Owner:** the `evaluation-integrity-engineer` persona.
> - **Review:** in parallel by `research-engineer` and `system-architect`, per the review gate in `.claude/agents/README.md`. Save reviews verbatim in `docs/reviews/integrity-blockers-<date>/`.
>
> ## Boundaries with other tasks
>
> - A parallel session may be writing `docs/requirements.md` (task 2). It will reference your decisions; do not edit its file.
> - Components are task 3's. Decide the rules, not the component design.
>
> ## Process
>
> - **Commits:** commit at every milestone, push, and keep the HANDOFF current.
> - **Vlad's instructions:** quote them verbatim in `DEVELOPMENT_PROCESS.md`, in the same turn. Append a new section, and expect to merge that file by hand with the parallel session.
> - **Before the PR,** run the `/codex` review gate required by the parent `CLAUDE.md`. On this machine it needs two workarounds:
>   - the configured model `gpt-6-sol` is refused on this ChatGPT account, so pass `-c model="gpt-6-astra"`;
>   - `codex review` rejects custom instructions together with `--base`, so drop `--base` and name the range in the instructions (`git diff claude/paper-analysis...HEAD` while PR #1 is open).

**This session.**
- It started on 2026-10-02, in the worktree `.claude/worktrees/integrity-blockers`, on
  `claude/integrity-blockers` at `9ae8c0c`, up to date with its remote branch. Its first message
  was "Read .claude/brief.md in this worktree and follow it."
- The brief lives in `.claude/brief.md`, which the repository's local exclude file keeps out of
  git, so this section is its only committed record.
- PR #1 is still open (checked on 2026-10-02), so the branch stays on top of
  `claude/paper-analysis`.
- `bash playground/paper/fetch_sources.sh` filled this worktree's own `.cache/`: every sha256
  matches, ScientistOne's TeX included.

**The brief for the decisions.** Before any persona works, `docs/integrity/README.md` states what
the decisions document must meet: ten requirements, R1 to R10, each with its acceptance test, and
the questions each of the four decisions must answer. The owner and every reviewer read that one
file. The owner, the `evaluation-integrity-engineer` persona, drafts
`docs/integrity/blocking-decisions.md` from it.

**The first version.** The owner wrote `docs/integrity/blocking-decisions.md` (`a2e7eb0`), 419
lines, as 31 rules, IR-1 to IR-31:
- **U-INT-4:** a locked, hashed harness computes every number a decision reads or a report
  quotes. It runs agent code's entry points itself, on artifacts that recorded fit jobs made. The
  baseline is the task's own code at its pinned commit, never an agent's reimplementation.
- **U-TOP-5:** three disjoint data roles per task, fit, search (validation) and report (test). Every
  decision in the loop reads search, or no data. The test split is read in one test event per run,
  after a freeze, plus one sealed baseline check per task.
- **A-INT-1:** both readings of the paper, in three layers. The setup prevents, seven gates block
  inside the run, and the CoE audit runs once after export and only measures.
- **A-INT-3:** five roles in separate sessions: the author, the in-loop checker and fixer, a
  development auditor, and a held-out reporting auditor, whose model family differs from every
  family that wrote what it reads.

The owner flagged three changes for Vlad to see:
- **The sealed baseline check bends a rule of `CLAUDE.md`.** The rule says the test set is used
  "once, at the end". The check reads the test split once per task, before any candidate is
  scored, and releases only pass or fail. The published numbers it checks against are test
  numbers, and a failure found only at the end would waste a whole run.
- **The CoE audit no longer gates.** The register's proposal ran the audits as gates before export
  and again at evaluation; an audit that gates becomes the engine's optimisation target.
- **A third model family.** The reporting auditor needs one, neither Claude nor Gemini.

**Checked here before the review**, beyond the citation checker's 0 problems:
- ScientistOne's section labels: §6.1 is a real subsection, and the appendix letters D, E.1, E.2
  and F match the order of its files;
- each quoted ScientistOne line says what the document says it says, and 13 + 4 = 17 of its 22
  score-verification errors;
- every quote sits within the lines its anchor names, or on the PDF page its tag names;
- the 40 or so register rows in the "Rows it constrains" tables exist, with the owning tasks the
  document gives them.

**The review, wave 1.** Three reviews ran in parallel on `a2e7eb0`, one lens each, and each is
kept verbatim in `docs/reviews/integrity-blockers-2026-10-02/`:
- **`research-engineer`, two blockers:**
  - Training-seed luck survives the held-out split. The test event scored the very fitted models
    that search had chosen, so the noise that came from fitting reached the test numbers intact.
    At equal fit and evaluation noise, the winner of 20 null candidates keeps +1.32 of its +2.65
    search gain on the test split. Its script re-runs in `playground/integrity/`, and reproduces
    the numbers here.
  - Weights an agent places in its code tree pass the provenance rule. The fit re-run of the audit
    then reproduces them exactly.
- **`system-architect`, one blocker:** the rules count harness jobs, not released results, and
  define no resume. So a crash in the test event cannot be told from a second use of the test set.
- **`paper-analyst`, no blocker:**
  - every quote and anchor is exact, and every image-page fact holds;
  - but the two readings of A-INT-1 were misattributed, departures from the paper went unnamed,
    and I1's scope departs from the definition it claims to apply.

**The fix list.** `fix-list.md` in the same folder merges every finding into 47 entries, F-0 to
F-46, and declines none. F-0 splits the document by decision, since the fixes take it past the
600-line cap. F-46 is a question for Vlad. `CLAUDE.md` says the test set is used "once, at the
end", yet three reads of the test split go beyond that wording:
- the sealed baseline check;
- the audit's re-fits after export;
- a correction event after a defect in a locked scoring item.

None of the three can reach a decision that changes the method or the frozen rows. The document
states them as proposed exceptions awaiting Vlad's confirmation, and `CLAUDE.md` stays unchanged.

**A usage limit, then two facts from task 2.** The owner stopped midway at a usage limit, and
resumed from the files on disk once it reset. Then the task 2 session wrote to say what it adopts
from the fix list, and pointed to an instruction of Vlad's that this session had not seen. Before
acting on it, I checked the instruction on `origin/claude/engine`.

**Vlad, verbatim,** as `claude/engine`'s `DEVELOPMENT_PROCESS.md` records it (2026-10-02):

> "As a result I expect to see working engine for auto research which replicates engine from paper ScientistTwo. I am going to use it based on my claude subscription – "claude -p" backend in future, take it into account. I don't wanna pay for API.
> Don't ask me anything, deliver replicated engine."

**What it changes here:**
- **F-46 is decided in place, not put to Vlad.** The three reads of the test split are recorded as
  our reading of `CLAUDE.md`'s "used once, at the end", with their reasons. Rewording that line is
  flagged to the coordinating session.
- **The engine is already being built** on `claude/engine`. It runs every agent through
  `claude -p` on the subscription, and folds in the outputs of tasks 2 and 6 when they land.
- **The owner received five amendments, A1 to A5,** recorded at the end of `fix-list.md`:
  - A1: F-46 decided;
  - A2: the subscription, so the reporting auditor's non-Claude family must also run on a
    subscription;
  - A3: whether an exhausted identity fails or the run is suspended is left to U-TOP-2's owner;
  - A4: job arguments, such as task 2's mechanism switches, are part of a job's identity;
  - A5: C_base's code hash.
- **The reply to task 2:** nothing it adopted contradicts our decisions. It got the conditions
  under which its mechanism switches and its suspension rule keep the integrity rules.

**The coordinating session agreed.** Through task 2, the coordinating session ("Google
Autoresearch") relayed its own decision on F-46. It is the same reading as A1, with one clause made
explicit: any read of the report split that could feed a decision is a violation. Its engine
contract, `docs/architecture/engine.md` §5 on `origin/claude/engine`, gives the same reading. The
owner received the clause as A6.

That contract's task manifest gives the validation and test splits the same seeds, `[0, 1, 2]`.
That is the case of the research-engineer's blocker B1: the test numbers would inherit the seed luck
that selection exploited on validation. So the coordinating session was told directly, together with
the lineage rule and the rule of released results per identity, which its harness will also need to
meet.

**The second version.** The owner applied F-0 to F-46 and A1 to A6. The result is an index,
`docs/integrity/blocking-decisions.md`, and four decision files in `docs/integrity/decisions/`,
920 lines in all. The citation checker finds 0 problems; each file is under 600 lines; the 147
sub-IDs that are referenced are all defined; and nothing private appears. The owner contested
seven points of the fix list, with reasons, and all seven are accepted (`fix-list.md`, section 5).

**The closure checks, and the third version.** Each wave-1 reviewer checked its own findings
against the second version, and each report is kept verbatim as `closure-*.md`:
- **`system-architect`:** all 30 of its findings and tensions are fixed, and it found 5 new
  MINOR defects.
- **`paper-analyst`:** all 16 of its findings are fixed. It read the three external sources from
  their own text and found every paraphrase faithful, and it found 3 new MINOR defects.
- **`research-engineer`:** 16 of its 19 findings are fixed, and its blocker on seed luck holds. It
  found two MAJOR points:
  - weights chunked into many small text files still passed the per-file bound;
  - the near-duplicate check would refuse large tasks on false flags.

The owner applied all of them as C-1 to C-14, in a third version (`fix-list.md`, section 6).

**The register and the TODO.** The four rows of `docs/paper/unspecified.md` now point to their
decision files, and nothing else in that file changed. `register_coverage.py` and the default run of
`check_citations.py` still pass. `TODO.md` marks task 6's `P0` part done, and lists what it found
for tasks 4, 5 and 7, for the coordinating session, and for the owner of `docs/paper/`.

**The Codex gate, four passes** (`docs/reviews/integrity-blockers-2026-10-02/codex-review.md`).
Each pass ran on `gpt-6-astra`, with the range named in the instructions.
- **Pass 1, FAIL:**
  - a check after a runner change would have returned a cached record instead of running;
  - the audit's noise was calibrated on the wrong row;
  - a control ignored that every seed is checked;
  - a baseline correction had no scope it was allowed to run in.
- **Pass 2, FAIL.** Pass 1's fixes held, but:
  - calibration re-fits had no identity of their own;
  - the tolerance treated an estimated noise as known, and flagged 20% to 34% of honest rows;
  - the search cap counted seeds instead of whole evaluations.

  The owner replaced the tolerance with a pre-registered finite-sample rule per kind of fit,
  backed by `playground/integrity/audit_tolerance.py`.
- **Pass 3, PASS, with four P2:**
  - the rule's Gaussian assumption, now checked at packaging;
  - a paired gain under a shared noise estimate;
  - a fit learning its data role from its seed, now closed by a derived seed;
  - builders seeing the auditor's verdicts in the published table, which now retires the auditor.
- **Pass 4, PASS, with one P2:** the role can still be discovered through the search aggregates.
  It is now classified as detection-only, with a control.

**Two exchanges with other sessions, along the way:**
- **Task 2** asked for two rules, and both are in: how a suspended run is resumed (IR-33.3), and
  its switch-scope check in the measured corpus (IR-31.1).
- **The engine session** adopted the rule on disjoint seeds, B1, in its commit `c1850a5`. It
  reproduced the simulation: a gain of +2.647 on search keeps +1.322 on test with shared seeds,
  and −0.005 with disjoint ones. Its first run on the subscription scores the test split once, on
  10 disjoint seeds: a gain of +0.0532, against +0.0594 on validation.

  It names one gap against these rules: it refuses data files, but records no lineage of where an
  artifact came from (IR-3.1, IR-3.2).

## HANDOFF, 2026-10-02 (task 6's `P0` part: done; the PR is open)

- **Where:** the worktree `.claude/worktrees/integrity-blockers`, on `claude/integrity-blockers`,
  which sits on top of `claude/paper-analysis` (PR #1, still open).
- **Done and pushed:**
  - the decisions, in `docs/integrity/` (the index and four decision files, rules IR-1 to IR-41);
  - the pointers in the four register rows;
  - the `TODO.md` entry;
  - three persona reviews, their closure checks, the fix list and four Codex passes, in
    `docs/reviews/integrity-blockers-2026-10-02/`;
  - the scripts behind the statistics, in `playground/integrity/`.
- **The PR:** `claude/integrity-blockers` into `claude/paper-analysis`. Merge PR #1 first; after
  that, retarget this PR to `main`.
- **Next steps:**
  1. Vlad reviews the PR. "Don't ask me anything" covers decisions, not merging; nothing reaches
     `main` without review.
  2. The engine session folds in the rules it does not yet meet. The first is lineage, IR-3.1 and
     IR-3.2.
  3. Task 6's `P1` part: the audit's settings (U-NOTE-4), α and the success test (A-EVAL-1,
     U-EVAL-1), the form of the verified table, and the reporting judge.
