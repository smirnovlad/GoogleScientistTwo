# The paper, as a specification

**For** anyone who needs to know what ScientistTwo (arXiv:2609.19644v1) actually says: the analysts
who write this folder, the reviewers who check it, and the tasks after it (requirements,
components). TODO task 1 fills it.

This file is the conventions every document here follows. It is the one brief given to every
agent that writes or reviews this folder, so that each one solves the same problem.

## The documents

| File | Holds | Written by |
|---|---|---|
| [analysis.md](analysis.md) | how the engine works, stage by stage, as structure: steps, inputs, outputs, agents, loops and limits, stopping rules, failure branches | `paper-analyst` |
| [claims.md](claims.md) | every quantitative claim: its location, its sample, its internal consistency, our assessment | `paper-analyst` |
| [note-check.md](note-check.md) | the initial note (`docs/inputs/`), claim by claim: true, false, partly true, or not in the paper | `paper-analyst` |
| [artifacts.md](artifacts.md) | what Appendices C and D (the agents' own outputs) show about each agent's inputs, outputs and format | `paper-analyst` |
| [unspecified.md](unspecified.md) | everything the paper leaves open, ambiguous or inconsistent, each with the decision it forces on us | `paper-analyst`, consolidated from the four above |
| [traceability.md](traceability.md) | each paper element → the requirement it becomes (task 2) → the component (task 3) | `paper-analyst`, consolidated |
| [source/](source/) | the paper's TeX, committed (licence below) | fetched, never edited |

## Sources, and which one wins

| Source | Where | Use it for |
|---|---|---|
| **TeX source**, v1 | `docs/paper/source/` (committed) and `.cache/paper/2609.19644v1/src/` (with figures) | what the authors wrote: every quote, every TeX anchor |
| **PDF**, arXiv-compiled from that TeX | `.cache/paper/2609.19644v1/paper.pdf`; text in `paper.pdf.txt` | **numbering** (sections, tables, figures, the listing), **page numbers**, and the content of images |
| **HTML** (LaTeXML) | `.cache/paper/2609.19644v1/paper.html` | a cross-check only. ⛔ Never cite its figure numbers |
| **Figure files** | `.cache/paper/2609.19644v1/src/figures/*.pdf`, `src/sections/*/` | diagrams and plots, whose content is an image, not text. Open them with the Read tool |

- **Get the cache** with `bash playground/paper/fetch_sources.sh`. It pins v1, verifies the sha256
  of each download, and checks that the committed TeX is the archive's text.
- ⛔ **Never use a summary as a source**, including a web tool that summarises a page, this
  repository's `docs/inputs/`, or another agent's report. Read the TeX and the PDF, which are local.
- **When two renderings disagree, say so,** and cite both.

**Licence.** The paper is © its authors, under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (as the arXiv abstract page states). The
committed TeX is the arXiv archive's text with one change: `main.tex` line 46 lists two e-mail
addresses, and this repository never commits an e-mail address (`CLAUDE.md`), so that line is
redacted in place. The line count is unchanged, so every line anchor matches the original. Figures,
the class file and the bibliography's compiled form are not committed; the fetch script restores them.

| Download (2026-09-27) | sha256 |
|---|---|
| `https://arxiv.org/src/2609.19644v1` (tar.gz) | `60e05f1188a289bc1ec1fd44f1432b7b2dc4d910effb502dc272953924822980` |
| `https://arxiv.org/pdf/2609.19644v1` (71 pages) | `98fb7802ec28beea159895a3de219307e019867b16296dfe4a79e68daaef9a17` |
| `https://arxiv.org/html/2609.19644v1` | `23f93180ac10e5b4e1cbdf9f1e532aa80c33351b7968345752ec7c6d12925aa3` |

## Numbering: cite the PDF's

The PDF is the authors' own rendering of the TeX, so its numbers are the paper's numbers.
Evidence: `python3 playground/paper/float_numbering.py`.

- **The stage pseudocode is Listing 1.** The TeX puts it in a minted `listing` float
  (`tex:tables/pseudo_code.tex:22-38`); the PDF prints "Listing 1".
- **The HTML calls it "Figure 4"**, so HTML Figures 5–12 are PDF Figures 4–11. Tables 1–16 and all
  section numbers agree between the two. The HTML even disagrees with itself: its caption says
  "Figure 4", while its §3 sentence points to "Listing 4".
- **Sections:** 1 Introduction · 2 Related Work · 3 ScientistTwo (3.1–3.6, the six stages) ·
  4 Experiments (4.1 Main Results, 4.2 Ablation Studies, **4.3 Discussion**) · 5 Conclusion ·
  Appendix A (A.1 Benchmark, A.2 Configuration) · B Detailed Comparison with AutoSOTA ·
  C Qualitative Results · D Case Study: DynaSpec-RAG.
- **Floats in the PDF:** Figures 1–3 (§1), Listing 1 and Table 1 (§3), Figures 4–7 (§3.1–3.6),
  Tables 2–8 and Figures 8–9 (§4.1–4.2), Figure 10 and Tables 9–11 and Figure 11 (§4.3),
  Tables 12–16 (Appendices A–B). The pages of Appendices C and D are unnumbered figures.

⚠️ **Appendices C and D give page numbers that are wrong by five in the arXiv PDF.** The text
says pp. 29–50 and pp. 51–65; the pages are:

| Appendix text says | Content | Figure file (`src/sections/…`) | Actual PDF page |
|---|---|---|---|
| pp. 29–30 | Limitations of X-Mahalanobis | `x_maha_qual/limitation_1–2.pdf` | 34–35 |
| pp. 31–34 | Ideation and method proposal | `x_maha_qual/idea_1–4.pdf` | 36–39 |
| pp. 35–37 | Experimental evaluation report | `x_maha_qual/result_1–3.pdf` | 40–42 |
| pp. 38–40 | Ablation study report | `x_maha_qual/ablation_1–3.pdf` | 43–45 |
| p. 41 | Critic agent feedback | `x_maha_qual/critic.pdf` | 46 |
| p. 42 | Reproducibility audit report | `x_maha_qual/audit1.pdf` | 47 |
| pp. 43–45 | Specification and method–code alignment audit | `x_maha_qual/audit_1–3.pdf` | 48–50 |
| pp. 46–50 | Rebuttal report (TABHARMONY) | `x_maha_qual/rebuttal_1–5.pdf` | 51–55 |
| pp. 51–65 | DynaSpec-RAG final draft (16 pages, not 15) | `dynaspec_qual/ts_rag1–16.pdf` | 56–71 |

Cite these pages by the **actual** PDF page: `[p. 46]`.

## How to cite

Every statement in these documents carries its location. The checker enforces it:
`python3 playground/paper/check_citations.py` (and `--selftest` shows it can fail).

- **A location tag,** in square brackets: `[§3.2]`, `[Tab. 1]`, `[Lst. 1]`, `[Fig. 9b]`, `[Eq. 2]`,
  `[App. A.2]`, `[p. 46]`, `[fn. 1]`, `[Abstract]`, `[Bib: meng2026scientistone]`. Name the part
  when it helps: `[§3.2 "Scaling Up to the Full-Set"]`, `[Tab. 1 row "Peer-Review"]`.
  - The PDF numbers four equations, all in §3: Eq. 1, the engine (P+, C+) = A(G) [§3];
    Eq. 2, the unified coder A_Coder [§3.2]; Eq. 3, the round's traces R_k [§3.3]; Eq. 4, the
    Selector [§3.3]. Cite one with its section: `[§3.3, Eq. 3]`. (An earlier version of this
    brief said the paper numbers no equations. That was wrong, and the note-check analyst caught
    it.)
- **A TeX anchor** where the text is in the TeX: `(tex:sections/3_new_method.tex:47)` or a range
  `(tex:sections/appendix.tex:154-155)`. Paths are relative to `docs/paper/source/`. The checker
  verifies every anchor.
- **Quote exactly,** in double quotes, and keep quotes short: a clause, never a paragraph.
  - The checker looks for every quote of five or more words in the TeX, the PDF text and the note.
  - Where math makes the TeX unquotable, quote the PDF's wording, or paraphrase and say so:
    `(paraphrase)`.
- **Content that is only in an image** (a diagram's arrows, a plot's values) is marked `(image)`,
  with its figure: `[Fig. 10b] (image)`.
- **Our own statement** (an assessment, a decision, a reconstruction's rationale) carries
  `[ours]`. Never let our reading pass as the paper's.

## How to classify

Every mechanism the engine needs is one of these:

| Mark | Meaning | What it must show |
|---|---|---|
| **SPECIFIED** | the paper says it | the quote and its location |
| **UNSPECIFIED** | the paper is silent | what the paper does say nearby, and the decision the silence forces on us |
| **AMBIGUOUS** | two readings both fit the text | both readings, each with its quote |
| **INCONSISTENT** | two places in the paper contradict each other | both places, each quoted |

- **`[inferred]`** marks a step the paper implies but never states, such as the order of two
  operations that must happen in sequence. It always cites what it is inferred from.
- ⛔ **Never resolve an ambiguity silently,** and never fill a gap with a plausible guess presented
  as the paper's. The gap is the finding.
- ⛔ **Never delete a reading that turned out wrong.** Mark its verdict beside it.

## IDs

IDs make the chain from paper to requirement to component traceable. Each document owns the keys
listed for it, so that parallel writers never collide.

| Prefix | Is | Example |
|---|---|---|
| `P-<KEY>-n` | a paper element: a step, an agent, a loop, a limit, a data object | `P-SUB-3` |
| `U-<KEY>-n` | an UNSPECIFIED item | `U-SUB-1` |
| `A-<KEY>-n` | an AMBIGUOUS or INCONSISTENT item | `A-PEER-2` |
| `C-<KEY>-n` | a quantitative claim | `C-MAIN-4` |
| `N-n` | a claim of the initial note | `N-12` |

| Keys | Area | Owned by |
|---|---|---|
| `TOP` | problem setup, the stage primitive (Listing 1, Table 1), the end-to-end loop | analysis.md |
| `LIM`, `SEED` | §3.1 finding limitations; seed idea generation and novelty | analysis.md |
| `BASE`, `SUB`, `FULL`, `CODER` | §3.2 baseline on the subset; subset experiment; full-set experiment; the unified coder | analysis.md |
| `EVO`, `SEL` | §3.3 idea evolution; selecting the best idea | analysis.md |
| `ABL` | §3.4 ablation planning, execution, critic, refinement, result comparison | analysis.md |
| `DRAFT`, `PEER`, `META` | §3.5 initial drafting; review–rebuttal loop; §3.6 meta-review | analysis.md |
| `INT` | integrity mechanisms in the pipeline (§4.2 "CoE Integrity Audit") | analysis.md |
| `CFG`, `ROSTER` | App. A.2 configuration and loop limits; the agent roster and model routing | analysis.md |
| `MAIN`, `ABLX`, `DISC`, `APPB`, `HEAD` | claims of §4.1, §4.2, §4.3, Appendix B, and the abstract, introduction, teaser and conclusion | claims.md |
| `EVAL`, `BENCH`, `COST` | how the paper measures (reviewers, gains, success); the benchmark (App. A.1); cost | claims.md |
| `ART` | what Appendices C–D show | artifacts.md |
| `NOTE` | gaps that checking the initial note brings to light | note-check.md |

Each writer ends its document with a section **"Gaps found here"** that lists its `U-` and `A-`
items in full: the statement, the location, the quotes. The consolidation step moves them into
`unspecified.md` and leaves links behind.

**A writer edits only the files it owns,** and never runs git; the orchestrating session commits.

## How to write

- **Structure, not prose.** A stage is written as:

  ```
  ### <stage> [Tab. 1 row "<row>"]  ·  P-<KEY>-1 … n
  - Purpose:        one line
  - Inputs:         each input, its symbol, and the step that produces it
  - Outputs:        each output, its symbol, and who consumes it
  - Agents:         each agent under every name the paper gives it (§3 text, Tab. 1, figures,
                    App. A.2, §4.2), and its model per App. A.2
  - Steps:          numbered: input → agent → output, each cited
  - Loop:           Listing 1's roles (candidate, critic, refine), the verdict vocabulary,
                    the limit's symbol and value, each cited
  - Stopping rule:  the exact condition
  - On exhaustion:  what the text says happens when the limit is reached
  - On failure:     what happens when a step fails; UNSPECIFIED if the paper is silent
  - Gaps:           U-/A- IDs, one line each
  ```

- **Every loop limit** appears with its symbol, its value, and both locations: where §3 introduces
  it, and where App. A.2 sets it (or UNSPECIFIED).
- **Every number** carries its sample: n, which tasks, which reviewer, which model.
- **Keep a file under about 600 lines.** If analysis.md needs more, move the stage detail into
  `stages/NN-<stage>.md` and keep analysis.md as the overview that links them.
- **Plain Markdown,** readable on GitHub. No HTML.

## Done when

TODO task 1's own test: a reader can explain every stage and every loop limit from this folder
alone, and every statement here cites its location in the paper. Two controls prove it:

1. **The checker passes** on every deliverable: `python3 playground/paper/check_citations.py`.
2. **A blind reader** (a fresh agent that has read this folder, never the paper) answers a fixed set
   of questions about stages and limits, and the answers are marked against the paper.

## Where things are in the TeX

| File under `source/` | Holds |
|---|---|
| `sections/0_abstract.tex`, `1_introduction.tex` | abstract; §1 (with Figures 1–3 via `figures/problem_setup.tex`, `qualitative_result.tex`, `overview.tex`) |
| `sections/2_related_works.tex` | §2 |
| `sections/3_new_method.tex` | §3 and §3.1–3.6; inputs Listing 1 (`tables/pseudo_code.tex`), Table 1 (`tables/overview.tex`), Figures 4–7 (`figures/method_3_*.tex`) |
| `sections/4_experiment.tex` | §4, §4.1–4.2; Tables 2–8 (`tables/*.tex`), Figures 8–9 |
| `sections/5_discussion.tex` | §4.3 (a subsection, despite the file name); Figure 10, Tables 9–11, Figure 11 |
| `sections/6_conclusion.tex` | §5, including the limitations paragraph |
| `sections/appendix.tex` | Appendices A–D: A.1 benchmark lists (Tables 12–14), **A.2 configuration (line 155)**, B (Tables 15–16), C and D (figure pages) |
| `main.bib` | the bibliography; cite an entry as `[Bib: <key>]` |
