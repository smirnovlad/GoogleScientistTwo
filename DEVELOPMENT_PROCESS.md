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

## HANDOFF, 2026-09-28 (task 1 done; PR #1 awaits review; tasks 2 and 6 run in the terminal)

- **Done and pushed** on `claude/paper-analysis`:
  - TODO task 1, ticked in `TODO.md` with its proof;
  - the Codex review's fixes;
  - the rule that task sessions start from a terminal.
- **All checks pass:**
  - `check_citations.py`: 18 files, 0 problems, and its self-test's 46 cases;
  - `register_coverage.py` and `trace_coverage.py`: 0 problems each, with their self-tests;
  - `claims_arithmetic.py`: exits 0;
  - `fetch_sources.sh`: the sources match their sha256, and the redaction is exact.
- **Open:** PR #1 (https://github.com/smirnovlad/GoogleScientistTwo/pull/1), `claude/paper-analysis`
  into `main`. Its description carries the Codex verdict. The repository has no CI yet, so no
  checks run on it.
- **Running, each in its own terminal session:**
  - task 2, in `.claude/worktrees/requirements`, on `claude/requirements`;
  - task 6's `P0` part, in `.claude/worktrees/integrity-blockers`, on `claude/integrity-blockers`.

  To continue one, run `claude --resume` in its folder and pick it from the list.
- **Next steps:**
  1. Vlad reviews PR #1. Merge to `main` only with his approval. The commits made after the Codex
     passes change only process documents. They get a Codex pass of their own before the merge.
  2. Tasks 2 and 6's `P0` part continue in their sessions. Once PR #1 is merged, each brings its
     branch up to date with `main`.
  3. Archive the two stopped app chats, "Start TODO task 2: requirements" and "Decide task 6's
     four integrity blockers". Archiving removes their `nervous-…` worktrees.
- **If this session is lost:**
  - Run `bash playground/paper/fetch_sources.sh`, then read `docs/paper/README.md`.
  - The review record is in `docs/reviews/paper-analysis-2026-09-27/`. Start from `fix-list.md`,
    whose last section records the outcome of every fix, and from `codex-review.md`.

## 2026-10-02: task 2 is relaunched in a terminal, under tmux

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
> - **You run in tmux,** in window `T2` of the session `gs2`. The coordinating session can read your
>   screen and type into it. Vlad opens your window with `gs2 2`.
> - **A Codex session also works in this repository,** in `.claude/worktrees/codex-reuse-survey`, on
>   `codex/reuse-survey`. Leave its worktree alone.

**Vlad, verbatim,** as the relaunch note quotes him (this session did not see the message itself):

> "Yes, relaunch both sessions in terminal, also use tmux for that so you can manage these sessions easily."

**The brief, verbatim.** The session that finished task 1 wrote it on 2026-09-28, and the relaunch
note says it is unchanged since. Vlad's own words behind it are "continue", and his instruction to
restart the task sessions from a terminal, both quoted above. It is not Vlad's own words.

> Start TODO task 2 (Requirements) of the GoogleScientistTwo repository. The project replicates the research engine of ScientistTwo (arXiv:2609.19644).
>
> ## Who wrote this brief
>
> The session that finished task 1 wrote it. It is not Vlad's own words. His words behind it are "continue", and then his instruction to restart the task sessions from a terminal. `DEVELOPMENT_PROCESS.md` quotes both. Record this brief there verbatim, in a new section, as the brief and with its author, never under "Vlad, verbatim" (`docs/process/worktrees-and-sessions.md`).
>
> A first attempt ran as a desktop-app chat and was stopped before it began the task. Nothing of it carries over. `DEVELOPMENT_PROCESS.md` records the restart ("task sessions start from a terminal").
>
> ## Read first, and follow
>
> - `CLAUDE.md`, `TODO.md` (task 2), and the last HANDOFF in `DEVELOPMENT_PROCESS.md`. They set the working rules:
>   - the paper is the specification;
>   - requirements come before code;
>   - route work to personas by the question they judge;
>   - every change passes the review gate;
>   - commits are in a plain human voice, with no AI attribution and no Co-Authored-By lines;
>   - never run a bare `git stash`.
> - **The repository is public on GitHub.** Never commit a secret, an e-mail address or a path from someone's machine.
>
> ## Where you are
>
> - You run in the worktree `.claude/worktrees/requirements`, on the branch `claude/requirements`, which tracks `origin/claude/requirements`. Check it with `git status -sb` before your first commit.
> - The branch contains `claude/paper-analysis`, which holds task 1's deliverables in PR #1 (https://github.com/smirnovlad/GoogleScientistTwo/pull/1). PR #1 is open and not merged into `main`. After it merges, bring your branch up to date with `main`.
> - If you need another Claude session, start it from a terminal, never as a desktop-app chat (`CLAUDE.md`). Subagents are unaffected.
>
> ## The task
>
> Write `docs/requirements.md` (TODO.md, task 2):
> - the goal, in one line;
> - each requirement with its acceptance test, and either traced to the paper (P- ID and location) or marked as our own decision, with its reason.
>
> **Done when** every one of the 177 paper elements (P- IDs) in `docs/paper/traceability.md` maps to a requirement, or to a recorded decision to leave it out. A script must prove it. Extend `playground/paper/trace_coverage.py`, or add a checker beside it, with a `--selftest` that shows the check can fail.
>
> ## Inputs
>
> - **`docs/paper/traceability.md`:** 177 elements, whose requirement column reads `— (task 2)`. Fill it, or map it from your file.
> - **`docs/paper/unspecified.md`:** the decision register. Task 2 owns 33 of its rows, 17 of them blocking. Blocking rows are ranked `blocks 1` to `blocks 8`, in the order task 3 needs them.
> - **`docs/paper/analysis.md` §3.4–3.5:** one stage primitive, with parameters per stage. The stage requirements should state parameters as data, not one loop per stage.
> - **`docs/paper/README.md`:** citation conventions. `python3 playground/paper/check_citations.py` enforces them on `docs/paper/`; decide whether it should also check your file.
>
> ## Boundaries with other tasks
>
> - **Integrity:** a parallel session may be deciding task 6's four blocking rows, U-INT-4, U-TOP-5, A-INT-1 and A-INT-3, in `docs/integrity/`. Reference those decisions; do not decide them yourself. The integrity rules in `CLAUDE.md` already settle U-INT-4 and U-TOP-5 in principle.
> - **Components** are task 3's. Do not design them.
>
> ## Process
>
> - **Persona routing:** see `.claude/agents/README.md`. The completeness check belongs to `system-analyst`, which judges by what is missing, where it resolves.
> - **Review gate:** two or three personas in parallel, one lens each, then fix. Save reviews verbatim in `docs/reviews/requirements-<date>/`.
> - **Commits:** commit at every milestone, push, and keep the HANDOFF current.
> - **Vlad's instructions:** quote them verbatim in `DEVELOPMENT_PROCESS.md`, in the same turn. Append a new section. A parallel session appends too, so expect to merge that file by hand.
> - **Before the PR,** run the `/codex` review gate required by the parent `CLAUDE.md`. On this machine it needs two workarounds:
>   - the configured model `gpt-6-sol` is refused on this ChatGPT account, so pass `-c model="gpt-6-astra"`;
>   - `codex review` rejects custom instructions together with `--base`, so drop `--base` and name the range in the instructions (`git diff main...HEAD`, or against `claude/paper-analysis` while PR #1 is open).

**This session.**
- It started on 2026-10-02, in the worktree `.claude/worktrees/requirements`, on
  `claude/requirements` at `fb4c8b1`, up to date with its remote branch. Its first message was
  "Read .claude/brief.md in this worktree and follow it."
- The brief lives in `.claude/brief.md`, which the repository's local exclude file keeps out of
  git, so this section is its only committed record.
- PR #1 is still open, with no review or comment (checked on 2026-10-02), so the branch stays on
  top of `claude/paper-analysis`.
- `bash playground/paper/fetch_sources.sh` filled this worktree's own `.cache/`: every sha256
  matches, ScientistOne's TeX included. Every check of task 1 passes here unchanged:
  `trace_coverage.py` (177 of 177), `register_coverage.py` and `check_citations.py` (18 files,
  0 problems), each with its self-test.
- **Task 6 has decided nothing yet.** Its branch, `claude/integrity-blockers`, holds no
  `docs/integrity/` (checked on 2026-10-02). The requirements reference its four rows, U-INT-4,
  U-TOP-5, A-INT-1 and A-INT-3, as pending, and depend only on what `CLAUDE.md` already settles.

## 2026-10-02: task 2's first draft, and the check that proves its coverage

**What exists now** (on `claude/requirements`):
- **`docs/requirements.md`**, the entry point. It holds the goal in one line, how to read the
  requirements, the decisions on task 2's 33 register rows, the five elements left out, and the
  rows the requirements leave to tasks 3 to 7.
- **`docs/requirements/01-run.md` to `08-operation.md`:** 71 requirements in eight areas, each with
  its trace to the paper or its reason, and one acceptance test, mostly in mock mode.
  - **The stages are data.** They are one table, the default stage configuration, setting the
    parameters of one primitive (`02-primitive.md`). Each stage then has one requirement for what a
    value alone cannot say, and its test.
- **The decisions.** Of the 33 rows, 25 are confirmed as the register proposed them, 8 are refined,
  and none is replaced. Each register row now ends with a pointer to its decision.
- **`playground/paper/requirement_coverage.py`.** It checks that every one of the 177 paper elements
  is traced by a requirement (172) or left out by a recorded decision (5). It also checks the
  requirement fields, the decisions table, the register pointers and the boundary: a requirement
  may decide only task 2's rows, and lists every other task's rows under *Depends on*.
  - `--write` filled `traceability.md`'s requirement column. The diff was checked to change that
    cell only, in all 177 rows.
  - `--selftest` plants 26 defects beside a clean twin, and checks the column fill.
  - Before the column was filled, the real run failed with 210 problems: 177 placeholders and 33
    missing pointers.
- **`check_citations.py` now checks the requirements too,** 27 files in all. The requirements mix the
  paper's statements with our decisions, which is where a reading of ours could pass as the paper's.

**Persona routing.** A `system-analyst` elicitation pass started first, in the background, reading
the same inputs independently. Its report goes into the review folder when it arrives.

## HANDOFF, 2026-10-02 (task 2: first draft committed; the review gate is next)

- **Done:** the draft above. All checks pass: `check_citations.py` (27 files),
  `trace_coverage.py`, `register_coverage.py` and `requirement_coverage.py`, each with its
  self-test.
- **Next:**
  1. Save the `system-analyst` elicitation verbatim in `docs/reviews/requirements-2026-10-02/`.
  2. Run the review gate: `system-analyst`, `system-architect` and `evaluation-integrity-engineer` in
     parallel, one lens each, saved verbatim in the same folder. Fix, then a closure check.
  3. Run the `/codex` gate on `git diff claude/paper-analysis...HEAD`, with
     `-c model="gpt-6-astra"` and no `--base`.
  4. Tick task 2 in `TODO.md` with its proof, and open the PR against `claude/paper-analysis` while
     PR #1 is open.
- **Task 6 had decided nothing** when the draft was written. If its decisions land, check every
  requirement that lists U-INT-4, U-TOP-5, A-INT-1 or A-INT-3 under *Depends on*.
