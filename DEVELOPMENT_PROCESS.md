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

## HANDOFF, 2026-09-27 (task 1: the fix phase)

- **Done and pushed** on `claude/paper-analysis`:
  - all six deliverables in `docs/paper/`;
  - six review records and `fix-list.md`;
  - the checkers in `playground/paper/`, all passing on the committed state.
- **Running:** the four original analysts applying their fixes from `fix-list.md`, each only to
  their own documents.
- **Next steps:**
  1. Check the fixed documents against the fix list, fix by fix.
  2. The register and traceability owners register the new IDs, and both coverage scripts pass.
  3. The blind-reader quiz. Its questions and answer key stay out of the repository until it runs.
  4. The orchestrator's independent reading and coverage marking go into
     `docs/reviews/paper-analysis-2026-09-27/`.
  5. Tick TODO task 1. Add the discovered work to `TODO.md`:
     - task 6's four blocking decisions (A-INT-1, A-INT-3, U-NOTE-1, U-ART-16; see
       `docs/paper/unspecified.md`) come before task 3;
     - two of them are already settled by the integrity rules in `CLAUDE.md`.
  6. A `/codex` review of the branch, then a PR for Vlad.
- **If this session is lost:**
  - Run `bash playground/paper/fetch_sources.sh`, then read `docs/paper/README.md` and
    `fix-list.md`.
  - Each fixed document carries a "Revised … after the persona review" line naming the fixes it
    applied. A document without that line has not been fixed yet.
