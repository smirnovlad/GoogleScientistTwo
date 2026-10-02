# Traceability: paper element → requirement → component

Revised 2026-10-02 by TODO task 2: Part 2's Requirement column is filled from `docs/requirements.md`, and the controls name the check that keeps it in step [ours].

Revised 2026-09-28 after the persona review: applies F-UN-1 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md`, with rows for the 50 new elements (P-TOP-6, P-ABL-7, P-CFG-12 … 19, P-ROSTER-29 … 51, P-STATE-1 … 17), the reclassification of A-EVO-1, A-ART-3 and A-EVAL-6 as AMBIGUOUS, and the new gaps in the rows they touch. The stage rows now map to one stage primitive with data for each stage (F-AN-0), and the state rows to their stores (F-AN-22). Section 1.4 records how F-AN-22 and F-AN-28 to F-AN-31 closed its findings. Two corrections from the blind-reader quiz follow: no stage takes Listing 1's values exactly (P-TOP-2), and both planners' backends are open (P-ROSTER-16, P-ABL-1) [ours].

**For** TODO tasks 2 (requirements) and 3 (components), and for the reviewers of task 1. **Holds**
one row for every element of ScientistTwo (arXiv:2609.19644v1) that this folder defines, with the
requirement it becomes and the component that meets it; task 1 fills the paper side, and tasks 2
and 3 fill the rest [ours]. Conventions, sources and IDs follow [README.md](README.md) [ours].

- **Part 1** checks, part by part, that every part of the paper TODO task 1 requires is captured by elements, and records the status of what the first version found uncaptured [ours].
- **Part 2** is the map: 177 P- IDs over 21 keys, one row each [ours].
- **Part 3** lists the quantitative claims and artifact behaviours that could become acceptance targets for our replication, and says why each is or is not fair [ours].

## Controls

- **Coverage.** `python3 playground/paper/trace_coverage.py` collects every P- ID that a source document declares in a heading, the way the README's stage template introduces elements (`### <stage> [...] · P-<KEY>-1 … n`), expands ranges, and requires each ID exactly once in Part 2, alone in the first cell of its row [ours].
- **What else fails it:** an ID in Part 2 that nothing defines; an ID declared by two documents; a hole in a key's numbering; an undefined ID named in a source document or in Parts 1 and 3; a gap ID in Part 2 that no gap list defines [ours].
- **It can fail.** `--selftest` plants 15 defects beside a clean twin, and each must yield exactly its expected kind of problem; `--trace FILE` checks a copy of this file, which is how the planted run below was made [ours].
- **What it reads.** analysis.md, artifacts.md, claims.md, note-check.md, stages/ and claims/: 16 documents. README.md (whose IDs are examples), unspecified.md (a register of gaps) and this file define no element [ours].
- **Result, 2026-09-28.** 177 P- IDs defined over 21 keys, 177 rows in Part 2, 0 problems; the 16 source documents have no collision, no numbering hole and no dangling reference [ours].
  - Per key: ABL 7, ART 11, BASE 1, BENCH 4, CFG 19, CODER 1, COST 4, DRAFT 1, EVAL 15, EVO 6, FULL 3, INT 5, LIM 4, META 7, PEER 6, ROSTER 51, SEED 4, SEL 1, STATE 17, SUB 4, TOP 6 [ours].
  - The self-test passes all 16 cases. The planted copy, with the row for P-STATE-9 deleted and the row for P-ROSTER-48 repeated, exits 1 with exactly those two problems, although its totals still read 177 against 177: counts alone would have missed both [ours].
- **Citations.** `python3 playground/paper/check_citations.py docs/paper/traceability.md` passes [ours].
- **Requirements (task 2).** `python3 playground/paper/requirement_coverage.py` checks that every P- ID is traced by a requirement or left out by a recorded decision, and that Part 2's Requirement column says exactly that; `--selftest` plants each defect it looks for. Result, 2026-10-02: 177 P- IDs, 172 traced by a requirement and 5 left out, 0 problems [ours].

## Part 1: coverage of the paper

Each row is a part of the paper that TODO task 1 requires, the elements that capture it, where they are defined, and what no element captures. A range such as P-LIM-1 … 4 names every ID in between [ours].

### 1.1 Sections, Listing 1, Table 1 and Figures 3–7

| Part of the paper | Elements that capture it | Defined in | Left without an element |
|---|---|---|---|
| §3 overview [§3] | P-TOP-4, the end-to-end control flow; P-TOP-5, its termination branches; P-TOP-2 and P-TOP-3, the one stage primitive the overview claims for every stage | [analysis.md](analysis.md) sections 3–4 | none; the loop "until the manuscript is approved" is the gap A-TOP-3 [§3] |
| Problem setup [§3 "Problem Setup"] | P-TOP-1: Eq. 1, what P+ and C+ must do, what G is; N_a, P-CFG-17; the task and the outputs as state, P-STATE-1 and P-STATE-17 | [analysis.md](analysis.md) sections 2, 6 and 8 | none; the contents of G are U-TOP-1 |
| Seed ideas [§3.1] | P-LIM-1 … 4, P-SEED-1 … 4; agents P-ROSTER-1 … 5; values P-CFG-1, P-CFG-2 and N_seed, P-CFG-12; state P-STATE-3, P-STATE-4 | [stages/01](stages/01-seed-ideas.md); [analysis.md](analysis.md) sections 6–8 | none |
| Evaluating ideas [§3.2] | P-BASE-1, P-SUB-1 … 4, P-FULL-1 … 3, P-CODER-1; agents P-ROSTER-6 … 13; values P-CFG-3, N_0 (P-CFG-13) and the full-set engineering limit (P-CFG-14); state P-STATE-5, P-STATE-6, P-STATE-16 | [stages/02](stages/02-evaluating-ideas.md); [analysis.md](analysis.md) sections 6–8 | none |
| Refining ideas [§3.3] | P-EVO-1 … 6, P-SEL-1; agents P-ROSTER-14, P-ROSTER-15; values P-CFG-4 … 7; state P-STATE-7 … 9 | [stages/03](stages/03-refining-ideas.md); [analysis.md](analysis.md) sections 6–8 | none |
| Ablation [§3.4] | P-ABL-1 … 7; agents P-ROSTER-12, P-ROSTER-16 … 19; values P-CFG-8 and N_p, P-CFG-15; state P-STATE-10, P-STATE-11 | [stages/04](stages/04-ablation.md); [analysis.md](analysis.md) sections 6–8 | none |
| Drafting and review [§3.5] | P-DRAFT-1, P-PEER-1 … 6; agents P-ROSTER-20 … 24; values P-CFG-9, P-CFG-10 and N_t, P-CFG-16; state P-STATE-12 … 14 | [stages/05](stages/05-drafting-peer-review.md); [analysis.md](analysis.md) sections 6–8 | none |
| Meta-review [§3.6] | P-META-1 … 7; agents P-ROSTER-12, P-ROSTER-19, P-ROSTER-25; value P-CFG-11; the export, P-TOP-5; state P-STATE-9, P-STATE-15, P-STATE-17 | [stages/06](stages/06-meta-review.md); [analysis.md](analysis.md) sections 4, 6–8 | none |
| Listing 1 [Lst. 1] | P-TOP-2, one parameter set of the stage primitive, verbatim | [analysis.md](analysis.md) sections 3.1 and 3.5 | none |
| Table 1 [Tab. 1] | P-TOP-3, all eleven rows, each a parameter set of the one primitive (analysis.md section 3.4); each row is also the heading of its stage in stages/01–06, keys LIM to META | [analysis.md](analysis.md) sections 3.2–3.5; [stages/](stages/) | none |
| Figure 3 [Fig. 3] (image) | its agent labels, in the name column of the roster rows for the agents it draws (all within P-ROSTER-1 … 25); its group boxes, P-ROSTER-29 … 40; G drawn as a human request, in P-TOP-1 | [analysis.md](analysis.md) sections 2 and 7 | none |
| Figure 4 [Fig. 4] (image) | P-LIM-1 … 4, P-SEED-1 … 4; the Initial Idea Generator, drawn only here, is P-ROSTER-3 | [stages/01](stages/01-seed-ideas.md); [analysis.md](analysis.md) section 7 | none |
| Figure 5 [Fig. 5] (image) | P-BASE-1 with its placement (A-BASE-1), P-SUB-1 … 4, P-FULL-1 … 3 with the engineer loop at full scale, P-CODER-1 | [stages/02](stages/02-evaluating-ideas.md) | none |
| Figure 6 [Fig. 6] (image) | P-EVO-1 … 6, P-SEL-1 | [stages/03](stages/03-refining-ideas.md) | none |
| Figure 7 [Fig. 7] (image) | P-ABL-1 … 6, P-DRAFT-1, P-PEER-1 … 6, P-META-1 … 7; its critic, engineer and comparison sub-graph, drawn twice, is evidence for the one primitive of P-TOP-3; its edges carry A-ABL-2 and A-META-1 | [stages/04](stages/04-ablation.md) to [stages/06](stages/06-meta-review.md); [analysis.md](analysis.md) section 3.5 | none |
| Common Setup [§4 "Common Setup"] | P-BENCH-1, the 107 problems; P-EVAL-7, ScholarPeer in the loop and the Stanford Agentic Reviewer held out; P-EVAL-4 and P-EVAL-6, their scores; the two reviewers as systems, P-ROSTER-46 and P-ROSTER-50; the model routing its models sentence loosens, P-CFG-19 (A-CFG-1) | [claims.md](claims.md); [analysis.md](analysis.md) sections 6–7 | none |
| CoE Integrity Audit [§4.2 "CoE Integrity Audit"] | P-INT-1 … 5, each under its enforcement class; agents P-ROSTER-26 … 28 and the generic Coding Agent, P-ROSTER-43; the audit as a system, P-ROSTER-51, and as a measurement, P-EVAL-10; its pages, P-ART-6, P-ART-7 | [stages/07](stages/07-integrity.md); [analysis.md](analysis.md) section 7; [claims.md](claims.md); [artifacts.md](artifacts.md) | none; the audit is specified by reference to ScientistOne, which stages/07 records [Ref: meng2026scientistone §5] |
| Benchmark [App. A.1] | P-BENCH-1 … 3 | [claims.md](claims.md) | none |
| Configuration [App. A.2] | P-CFG-1 … 19: the values A.2 sets, the six it leaves unset or ambiguous (P-CFG-12 … 17), the drafting format (P-CFG-18) and the model routing (P-CFG-19), which the roster rows apply agent by agent | [analysis.md](analysis.md) sections 6–7 | none |
| AutoSOTA comparison [App. B] | P-ABL-7, the attribution rule; P-EVAL-1, P-EVAL-3, P-EVAL-14; P-BENCH-4 (TeCh); P-INT-5 (the I1, I2 and I4 blocks); P-STATE-2, the protocol as read-only; P-ART-5; P-FULL-1 … 3 (the full benchmark grid) | [stages/04](stages/04-ablation.md); [claims.md](claims.md); [stages/07](stages/07-integrity.md); [analysis.md](analysis.md) section 8; [artifacts.md](artifacts.md); [stages/02](stages/02-evaluating-ideas.md) | none |
| Qualitative results [App. C] | P-ART-1 … 8, and the run layout P-ART-11 | [artifacts.md](artifacts.md) | none |
| DynaSpec-RAG [App. D] | P-ART-9 | [artifacts.md](artifacts.md) | none |

### 1.2 Tables 2–11 and 12–16

| Table | Elements that capture it | Defined in | Left without an element; the table's claims |
|---|---|---|---|
| Autonomous research agents [Tab. 2] | P-EVAL-4, P-EVAL-5, P-EVAL-6, P-EVAL-9, P-EVAL-14; the two reviewers, P-ROSTER-46 and P-ROSTER-50 | [claims.md](claims.md); [analysis.md](analysis.md) section 7.2 | none; C-MAIN-1, C-MAIN-2 |
| Human-author papers [Tab. 3] | P-EVAL-1, P-EVAL-4, P-EVAL-5, P-EVAL-6, P-BENCH-4 | [claims.md](claims.md) | none; C-HEAD-1, C-HEAD-4, C-MAIN-4 to C-MAIN-7 |
| AutoSOTA gains [Tab. 4] | P-EVAL-2, P-EVAL-3, P-EVAL-14 | [claims.md](claims.md) | none; C-HEAD-2, C-MAIN-8 |
| Review rounds [Tab. 5] | P-EVAL-8; it corroborates P-CFG-10 | [claims.md](claims.md); [analysis.md](analysis.md) section 6 | none; C-ABLX-3 to C-ABLX-5 |
| Review-driven refinement [Tab. 6] | the one example under P-META-1 … 7; it corroborates P-CFG-11 | [stages/06](stages/06-meta-review.md); [analysis.md](analysis.md) section 6 | none; C-ABLX-6 |
| Integrity audit [Tab. 7] | P-INT-5, P-EVAL-10, P-ROSTER-51; its header's refinement agents are P-ROSTER-26 … 28 | [stages/07](stages/07-integrity.md); [claims.md](claims.md); [analysis.md](analysis.md) section 7 | none; C-ABLX-7 |
| Coding agents [Tab. 8] | the two backends, P-ROSTER-48 and P-ROSTER-49; P-EVAL-1, for its SR column | [analysis.md](analysis.md) section 7.2; [claims.md](claims.md) | none; C-ABLX-8 |
| Frontier expansion [Tab. 9] | P-TOP-6, chained runs; P-EVAL-15 | [analysis.md](analysis.md) section 2.2; [claims.md](claims.md) | none; C-DISC-4 |
| Human evaluation [Tab. 10] | P-EVAL-11 | [claims.md](claims.md) | none; C-DISC-5 |
| DynaSpec-RAG results [Tab. 11] | P-ART-9, whose own Table 1 this is | [artifacts.md](artifacts.md) | none; C-DISC-6 |
| NeurIPS 2025 papers [Tab. 12] | P-BENCH-1 | [claims.md](claims.md) | none; C-BENCH-1 |
| ICLR 2026 papers [Tab. 13] | P-BENCH-1 | [claims.md](claims.md) | none; C-BENCH-2 |
| ICML 2026 Spotlight papers [Tab. 14] | P-BENCH-1, P-BENCH-3 | [claims.md](claims.md) | none; C-BENCH-3 |
| Aggregate differences [Tab. 15] | P-ABL-7, the attribution rule; P-EVAL-1, reading (c); P-STATE-2 and P-INT-5, the protocol forbidden by audit; P-CFG-15, whose only count this is | [stages/04](stages/04-ablation.md); [claims.md](claims.md); [analysis.md](analysis.md) sections 6 and 8; [stages/07](stages/07-integrity.md) | none; C-APPB-1 to C-APPB-4 |
| Paper by paper [Tab. 16] | P-EVAL-3, P-EVAL-14, P-BENCH-4 | [claims.md](claims.md) | none; C-APPB-5 to C-APPB-10 |

### 1.3 Floats outside the required list

- Figure 1 is covered by P-EVAL-1 and P-EVAL-12 [Fig. 1]; Figures 2 and 8 by P-ART-10 [Fig. 2] [Fig. 8]; Figure 9 by P-EVAL-13, and it corroborates P-CFG-6 [Fig. 9] (image); Figure 10 by P-COST-1, P-COST-3 and P-COST-4 [Fig. 10] (image); Figure 11 by P-ART-9 [Fig. 11] [ours].

### 1.4 Findings, and their status after the review

Every required part has at least one element [ours]. The first version of this file found seven parts, or aspects of parts, that no element captured (findings 1–7), and two defects in the elements themselves (findings 8–9). The review turned them into fixes F-AN-22 and F-AN-28 to F-AN-31; each status below was checked against analysis.md and stages/ as they stand on 2026-09-28 [ours].

1. **Six parameters had no element (F-AN-28).** §3 introduces N_seed [§3.1], N_0 [§3.2], N_p [§3.4], N_t [§3.5] and N_a [§3, Eq. 1], and a full-set engineering loop with no limit [§3.2]; App. A.2 sets none of them [App. A.2].
   - **Status: resolved.** analysis.md section 6 gives them P-CFG-12 … 17, each with where §3 introduces it and what App. A.2 says of it: nothing for five, and for the full-set limit a 2 that holds only if A.2's engineering sentence covers it (A-FULL-2); it adds the drafting format and the model routing as P-CFG-18 and P-CFG-19 [App. A.2] [ours].
2. **The state had no elements (fixed by F-AN-22, which the architect's review also asked for).** analysis.md section 8 listed the objects without IDs [§3.3] [ours].
   - **Status: resolved.** Section 8 now gives P-STATE-1 … 17, each with its producer, consumers, lifetime and whether it can change; Part 2.12 maps each to a store [ours].
3. **Figure 3's grouping had no elements (F-AN-31).** Six boxes group the agents [Fig. 3] (image).
   - **Status: resolved.** P-ROSTER-29 … 40 name the boxes and their inner groups, each with its resolution [ours].
4. **External systems had no elements of their own (F-AN-31).** analysis.md section 7.2 listed seven without IDs [§3.5] [§4.2] [App. A.2].
   - **Status: resolved.** They are P-ROSTER-45 … 51: PaperOrchestra, ScholarPeer, Google Search, Claude Code with Opus 4.8, Antigravity, the Stanford Agentic Reviewer and the CoE audit [ours].
5. **Table 8 tested a part with no element, the coding backend (F-AN-31).** The paper swaps Claude Code for "Antigravity powered by Gemini 3.8 Flash" on 5 ICLR 2026 tasks [§4.2] [Tab. 8].
   - **Status: resolved.** P-ROSTER-48 is the backend and P-ROSTER-49 its replacement [ours].
6. **App. B's attribution rule had no element (F-AN-31).** Table 15 says the engine "additionally requires the gain to be attributable to the proposed mechanism in ablation" [Tab. 15], and §3.4 has no such verdict [§3.4].
   - **Status: resolved.** P-ABL-7, in stages/04, is the rule, marked as absent from §3.4; where the critic draws the line between `Refine` and a reject is the new gap U-ABL-5, with TeCh, p. 46 and LC-FTT as its first cases [App. B] [ours].
7. **Table 9's chained runs had no element (F-AN-31).** A run's own method is "provided as context in the next discovery cycle" [§4.3] [Tab. 9].
   - **Status: resolved as an element.** P-TOP-6 records the chain and what it forces, one schema for G and for (P+, C+); which parts of one run's output enter the next run's G stays open, under A-TOP-4 and U-TOP-1 [ours].
8. **Two IDs named one element (F-AN-29).** P-LIM-4 and P-CFG-1 are both the 16 limitation rounds, and P-SUB-4 and P-CFG-3 both N_eng = 2 [§3.1] [§3.2] [App. A.2].
   - **Status: resolved, by stating the relation rather than merging.** stages/01 says P-LIM-4's value is P-CFG-1, stages/02 says P-SUB-4's is P-CFG-3, and analysis.md section 6 gives the rule for every pair: a P-CFG ID is a value, and the stage element that uses it is the mechanism, as P-EVO-5 uses P-CFG-6 and P-CFG-7, and P-META-7 uses P-CFG-11 [App. A.2] [ours].
   - In Part 2 both rows of a pair map to the same field of the same stage config: the mechanism to what the limit counts, the value to its number, so task 2 can give the pair one requirement [ours].
   - Unchanged, and deliberate: P-CODER-1 (the interface) against P-ROSTER-13 (the composite agent), and P-INT-2 … 4 (mechanisms) against P-ROSTER-26 … 28 (agents) [§3.2, Eq. 2] [§4.2] [ours].
9. **analysis.md disagreed with itself on what A_Coder contains (F-AN-30).** Its roster made A_Coder the composite of rows 6–11, which took in the Baseline Coder and left out the Full-Set Engineer, although §3.2 abstracts "this entire idea experiment pipeline" into A_Coder and that pipeline ends with "A Full-Set Critic Agent and Full-Set Engineer" [§3.2] (tex:sections/3_new_method.tex:52) (tex:sections/3_new_method.tex:55).
   - **Status: resolved.** P-ROSTER-13 is now the composite of rows 7–12, the Full-Set Engineer included, with row 6 only if the baseline runs per idea, linked to A-BASE-1 [§3.2] [Fig. 5] (image); the Part 2 row follows it [ours].

## Part 2: element → requirement → component

- **One row per P- ID** defined anywhere in this folder, grouped by the document that defines it. The ID stands alone in its cell and appears nowhere else in this part, so a search for it finds one line here [ours].
- **Element, Location, Gaps:** a few words; where the paper states it (for an artifact, its actual PDF page); the related U- and A- IDs, whose full entries sit under "Gaps found here" in the documents that define them, or `none` [ours].
- **Class:** the mark the defining document gives the element [ours].
  - `SPECIFIED (quoted)`, or `SPECIFIED (Eq. n)`: the defining document states the step by quoting the paper, or by its equation or formula, and gives it no mark of its own; a quoted statement is what the README calls SPECIFIED [ours].
  - For an agent or a name (key ROSTER), SPECIFIED means the paper names it; its backend or model follows when App. A.2 does not assign it plainly [ours].
  - For the state (key STATE), the object is the paper's, and whether it can change is analysis.md's reading unless the cell cites the paper [ours].
  - For the artifacts (key ART), the class is artifacts.md's basis for attributing the page to an agent, since a page is evidence, not a mechanism [ours].
  - After a semicolon: an aspect the defining document leaves open, with its gap [ours].
- **Requirement:** the requirements (`R-`) of `docs/requirements.md` and `docs/requirements/` that trace the element, or the decision (`X-`) in `docs/requirements.md` that leaves it out. Task 2 filled the column on 2026-10-02, and `requirement_coverage.py --write` regenerates it from the requirements' own *Traces* and *Leaves out* fields, so it is never edited by hand [ours].
- **Component:** a candidate that task 3 confirms, changes or rejects, named from TODO task 3's starting list [ours].
  - `stage primitive`: the one loop of analysis.md section 3.5, named on the rows that are loop mechanics: a refine step, a re-judgement, a stop test [ours].
  - `stage config <KEY>`: the data that sets the primitive for one Table 1 row, keyed LIM, SEED, BASE, SUB, FULL, EVO, SEL, ABL, DRAFT, PEER or META, with the fields of analysis.md section 3.4: generator; judged → refined, with the agent that refines; assessor and rule; verdict map; guard, with its failure branch; limit, with what it counts; at-limit policy; nesting and fan-out [ours].
  - `run state`, `task environment`, `evaluation harness`, `sandbox`: the stores for the state rows, each with whether its object can change [ours].
  - `— (task 3)`: rows that no conclusion of the analysis maps yet, namely the problem setup, chained runs, the integrity mechanisms, the agents and names, the three App. A.2 values that are no stage's data (N_a, the drafting format, the model routing), the artifacts, the measurements, the benchmark and the cost [ours].

### 2.1 Problem, stage primitive and control flow: [analysis.md](analysis.md) sections 2–4

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-TOP-1 | the problem setup: (P+, C+) = A(G) over N_a agents; what P+ and C+ must do; what G is | [§3, Eq. 1] | SPECIFIED for the experiments; AMBIGUOUS in general (A-TOP-4); contents UNSPECIFIED (U-TOP-1) | A-TOP-4, U-TOP-1 | R-RUN-1 | — (task 3) |
| P-TOP-2 | Listing 1: one parameter set of the stage primitive, in which accept returns the candidate, and a reject or the limit discards it | [Lst. 1] | SPECIFIED (verbatim); the other stages set other values, INCONSISTENT at the limit (A-TOP-1), and what the limit counts is AMBIGUOUS (A-TOP-2) | A-TOP-1, A-TOP-2, U-TOP-7 | R-PRIM-2, R-PRIM-3, R-PRIM-4 | stage primitive; no stage config takes its values exactly: SUB comes closest, keeping the three verdicts and the discard at the limit, but its critic judges E_sub^h against E_base while the engineer refines h and C_sub^h, and its limit counts engineering refinements, not critic calls (A-TOP-2) |
| P-TOP-3 | Table 1's eleven stages, each a parameter set of one primitive | [Tab. 1] [Fig. 7] (image) | SPECIFIED (Table 1); one primitive with a parameter set per stage is analysis.md's conclusion [ours] | A-TOP-1, A-TOP-2, and each row's own in analysis.md section 3.4 | R-PRIM-1, R-PRIM-2 | stage primitive; one stage config per row |
| P-TOP-4 | the end-to-end control flow from G to (P+, C+), reconstructed as pseudocode | [§3] [§3.6] | a reconstruction: each line SPECIFIED or [inferred], one reading taken per gap; the loop until approval INCONSISTENT (A-TOP-3) | A-TOP-3, U-TOP-2, U-TOP-3, U-TOP-4 | R-RUN-4, R-PRIM-9 | stage primitive, composed through the nesting fields of the stage configs |
| P-TOP-5 | the run's termination branches: accept, meta limit, refinement not superior, no success, ablation rejection, rule violation, error | [§3.3] [§3.6] [§4.2] | four branches SPECIFIED, the meta limit [inferred]; ablation rejection INCONSISTENT (A-ABL-1); errors UNSPECIFIED (U-TOP-2) | A-ABL-1, U-TOP-2, U-EVO-4 | R-RUN-5 | stage config EVO, ABL and META: at-limit policy and the guard's failure branch; run state: a failure record per task |
| P-TOP-6 | chained runs: one run's (P+, C+) given as context to the next run | [§4.3] [Tab. 9] | SPECIFIED; which parts enter the next run's G UNSPECIFIED (U-TOP-1) | A-TOP-4, U-TOP-1 | R-RUN-3 | — (task 3) |

### 2.2 Seed ideas: [stages/01](stages/01-seed-ideas.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-LIM-1 | Limitation Extractor: G → a set of limitations | [§3.1] | SPECIFIED (quoted) | U-LIM-1 | R-STG-1 | stage config LIM: generator |
| P-LIM-2 | Limitation Verifier: is the set sufficient to guide improvement? | [§3.1] | SPECIFIED (quoted); its criterion UNSPECIFIED (U-LIM-1) | U-LIM-1 | R-PRIM-7, R-STG-1 | stage config LIM: assessor and rule, verdict map |
| P-LIM-3 | insufficient → the Extractor adds what is missing | [§3.1] | SPECIFIED (quoted) | U-LIM-1 | R-STG-1 | stage primitive: the refine step; stage config LIM: judged → refined |
| P-LIM-4 | the limitation stage's limit, with no symbol, whose value is 16 rounds | [§3.1] [App. A.2] | SPECIFIED; what it counts AMBIGUOUS (A-TOP-2); what passes on at the limit AMBIGUOUS (A-LIM-1) | A-LIM-1, A-TOP-2, U-TOP-7 | R-PRIM-3, R-STG-1 | stage config LIM: limit (what it counts), at-limit policy |
| P-SEED-1 | initial idea generation: the limitations → h_0 | [§3.1] [Fig. 4] (image) | SPECIFIED (quoted); its agent AMBIGUOUS (A-SEED-2) | A-SEED-2 | R-STG-2 | stage config SEED: generator |
| P-SEED-2 | Novelty Checker: h_0 and two retrieved papers → a novelty score | [§3.1] [App. A.2] | SPECIFIED (quoted); the score UNSPECIFIED (U-SEED-2) | U-SEED-2 | R-PRIM-7, R-STG-2 | stage config SEED: assessor and rule, a score and no verdict |
| P-SEED-3 | Idea Generator Agent adds scored ideas until the pool holds N_seed | [§3.1] | SPECIFIED (quoted); N_seed UNSPECIFIED (U-SEED-1); filter or ranking AMBIGUOUS (A-SEED-1) | U-SEED-1, A-SEED-1, U-SEED-3 | R-STG-2 | stage primitive: a count stop; stage config SEED: judged → refined, limit, fan-out |
| P-SEED-4 | the pool H_0 sorted by novelty score, descending | [§3.1] | SPECIFIED (quoted) | A-SEED-1 | R-STG-2 | stage config SEED: at-limit policy, keep all, sorted |

### 2.3 Evaluating ideas: [stages/02](stages/02-evaluating-ideas.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-BASE-1 | Baseline Coding Agent: G on the subset → E_base, C_base | [§3.2] | SPECIFIED (quoted); placement AMBIGUOUS (A-BASE-1); the subset UNSPECIFIED (U-BASE-1) | A-BASE-1, U-BASE-1, U-BASE-2, U-SUB-2, A-CFG-1 | R-STG-3 | stage config BASE: generator, zero rounds; nesting once per task, or inside each A_Coder call (A-BASE-1) |
| P-SUB-1 | Subset Coding Agent implements h by modifying C_base → E_sub^h, C_sub^h | [§3.2] | SPECIFIED (quoted) | U-BASE-1, U-TOP-5 | R-STG-4 | stage config SUB: generator |
| P-SUB-2 | Subset Critic: E_sub^h against E_base → Bad, Good or Engineer, with feedback r^h | [§3.2] | SPECIFIED (quoted); its criteria UNSPECIFIED (U-SUB-1) | U-SUB-1, U-TOP-5 | R-PRIM-7, R-STG-4, R-INT-3 | stage config SUB: assessor and rule, verdict map |
| P-SUB-3 | Engineer → the Subset Engineering Agent refines h and C_sub^h | [§3.2] | SPECIFIED (quoted); its model AMBIGUOUS (A-CFG-1) | A-CFG-1, U-SUB-2 | R-STG-4 | stage primitive: the refine step; stage config SUB: judged → refined |
| P-SUB-4 | the subset stage's limit N_eng; at the limit, Bad and pruned | [§3.2] [App. A.2] | SPECIFIED; what it counts AMBIGUOUS (A-TOP-2) | A-TOP-2 | R-PRIM-3, R-PRIM-4, R-STG-4 | stage config SUB: limit (what it counts), at-limit policy, discard |
| P-FULL-1 | Full-Set Coding Agent adapts C_sub^h to the whole benchmark suite | [§3.2] | SPECIFIED (quoted) | A-ART-12, U-ART-4, U-BENCH-1 | R-STG-5 | stage config FULL: generator |
| P-FULL-2 | Full-Set Critic and Engineer validate and engineer on the full benchmark | [§3.2] [Fig. 5] (image) | SPECIFIED (quoted); reference AMBIGUOUS (A-FULL-1); limit AMBIGUOUS (A-FULL-2); verdicts UNSPECIFIED (U-FULL-1) | A-FULL-1, A-FULL-2, U-FULL-1, U-TOP-5 | R-STG-5, R-INT-3 | stage primitive; stage config FULL: assessor and rule, judged → refined, limit |
| P-FULL-3 | the terminal decision d^h | [§3.2] [Fig. 5] (image) | SPECIFIED (quoted); its vocabulary only in Figure 5 (U-FULL-1) | U-FULL-1 | R-PRIM-7, R-STG-5 | stage config FULL: verdict map, at-limit policy |
| P-CODER-1 | the unified coder A_Coder(G, h) → h, E^h, C^h, d^h, r^h | [§3.2, Eq. 2] | SPECIFIED (Eq. 2); baseline inputs AMBIGUOUS (A-BASE-1); a pruned idea's return UNSPECIFIED (U-CODER-1) | A-BASE-1, U-CODER-1 | R-PRIM-8, R-STG-6 | stage config SUB and FULL: nesting, both in one call per idea |

### 2.4 Refining ideas: [stages/03](stages/03-refining-ideas.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-EVO-1 | round 0: the top-N_0 seeds → A_Coder → R_0 | [§3.3] | SPECIFIED (quoted); AMBIGUOUS against App. A.2's rounds (A-EVO-1), INCONSISTENT only under A-EVO-2's reading 2 | A-EVO-1, A-EVO-2 | R-STG-7 | stage config EVO: generator in round 0, fan-out N_0 |
| P-EVO-2 | round k ≥ 1: A_Evolve reads all earlier traces → N_k evolved ideas | [§3.3] | SPECIFIED (quoted); what it reads UNSPECIFIED (U-EVO-2) | U-EVO-2 | R-STG-7 | stage config EVO: judged → refined, the population rebuilt from all traces by A_Evolve |
| P-EVO-3 | exploration: the next N_e unevaluated seeds join the evolved ideas | [§3.3] | SPECIFIED (quoted); running out of seeds UNSPECIFIED (U-EVO-3) | U-EVO-3 | R-STG-7 | stage config EVO: generator in later rounds, fan-out N_e |
| P-EVO-4 | each candidate of round k → A_Coder → R_k | [§3.3, Eq. 3] | SPECIFIED (Eq. 3); parallelism UNSPECIFIED (U-TOP-4) | U-TOP-4 | R-PRIM-8, R-STG-7 | stage config EVO: assessor, the nested A_Coder; fan-out, one call per candidate |
| P-EVO-5 | the stop test: S successes over all rounds so far, or round K | [§3.3] | SPECIFIED (the formula); when it runs UNSPECIFIED (U-EVO-1); K AMBIGUOUS (A-EVO-2) | U-EVO-1, A-EVO-2 | R-STG-7 | stage primitive: the stop test; stage config EVO: limit, K rounds and S successes |
| P-EVO-6 | zero successes at round K → the whole run ends | [§3.3] | SPECIFIED (quoted); what it leaves UNSPECIFIED (U-EVO-4) | U-EVO-4 | R-STG-7 | stage config EVO: at-limit policy, stop the run |
| P-SEL-1 | Selector: every Good idea with its results and code → h_best, E_best, C_best | [§3.3, Eq. 4] | SPECIFIED (Eq. 4); its criterion UNSPECIFIED (U-SEL-1) | U-SEL-1, U-SEL-2, U-TOP-5 | R-PRIM-7, R-STG-8, R-INT-3 | stage config SEL: assessor and rule, zero rounds |

### 2.5 Ablation: [stages/04](stages/04-ablation.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-ABL-1 | Ablation Planner: h_best → N_p executable plans | [§3.4] | SPECIFIED (quoted); N_p UNSPECIFIED (U-ABL-1) | U-ABL-1, A-CFG-1 | R-PRIM-8, R-STG-9 | stage config ABL: generator, fan-out N_p |
| P-ABL-2 | Ablation Coding Agent runs each plan on C_best → E_abl | [§3.4] | SPECIFIED (quoted); whether its code stays UNSPECIFIED (U-ABL-3) | U-ABL-3 | R-PRIM-8, R-STG-9 | stage config ABL: generator, one coder per plan |
| P-ABL-3 | Ablation Critic: E_abl → Good or Refine, with critique r_abl | [§3.4] | SPECIFIED (quoted); a reject verdict INCONSISTENT (A-ABL-1); what it reads UNSPECIFIED (U-ABL-6) | A-ABL-1, U-ABL-5, U-ABL-6, U-TOP-5 | R-PRIM-7, R-STG-9 | stage config ABL: assessor and rule, verdict map |
| P-ABL-4 | Refine → A_FullEng, guided by r_abl → h_new, E_new, C_new | [§3.4] | SPECIFIED (quoted); its validation UNSPECIFIED (U-ABL-2); its model AMBIGUOUS (A-CFG-1) | U-ABL-2, A-CFG-1 | R-STG-9 | stage primitive: the refine step; stage config ABL: judged → refined, E_abl judged and h_best refined by A_FullEng |
| P-ABL-5 | Result Comparison: the core state is replaced only if E_new is preferred | [§3.4] | SPECIFIED (quoted); criterion AMBIGUOUS (A-ABL-3); the failed branch INCONSISTENT (A-ABL-2) | A-ABL-3, A-ABL-2, U-TOP-5 | R-PRIM-5, R-PRIM-6, R-STG-9, R-INT-3 | stage config ABL: guard, with its failure branch |
| P-ABL-6 | after an update, ablation planning runs again on the new h_best | [§3.4] | SPECIFIED (quoted); a second Refine UNSPECIFIED (U-ABL-4) | U-ABL-4 | R-PRIM-3, R-STG-9 | stage primitive: the re-judgement after a refine; stage config ABL: limit |
| P-ABL-7 | the attribution rule: the gain must be attributable to the proposed mechanism | [Tab. 15] [App. B] | SPECIFIED in App. B only (quoted), absent from §3.4, whose critic has no reject (A-ABL-1); its boundary UNSPECIFIED (U-ABL-5) | A-ABL-1, U-ABL-5, A-ART-4, A-ART-13, A-EVAL-1 | R-STG-9 | stage config ABL: the assessor's rule, and a reject in the verdict map if A-ABL-1 is read so |

### 2.6 Drafting and the review–rebuttal loop: [stages/05](stages/05-drafting-peer-review.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-DRAFT-1 | Initial Drafter with PaperOrchestra: h_best, E_best, E_abl → P_new, in the ICLR 2025 format | [§3.5] [App. A.2] | SPECIFIED (quoted); other inputs UNSPECIFIED (U-DRAFT-1); failures UNSPECIFIED (U-DRAFT-2) | U-DRAFT-1, U-DRAFT-2, A-INT-2 | R-STG-10, R-INT-8 | stage config DRAFT: generator, zero rounds |
| P-PEER-1 | ScholarPeer reviews P_new → R_new with a score in [1, 10] | [§3.5] | SPECIFIED (quoted); its configuration UNSPECIFIED (U-PEER-3) | U-PEER-3 | R-STG-11 | stage config PEER: assessor |
| P-PEER-2 | a score below the threshold of 8 starts the rebuttal | [§3.5] [App. A.2] | SPECIFIED (quoted); the threshold reviewer-dependent, to calibrate [ours] | A-EVAL-3 | R-PRIM-7, R-STG-11 | stage config PEER: assessor's rule and verdict map, 8 or more → accept |
| P-PEER-3 | Rebuttal Planner: R_new → N_t supplementary tasks | [§3.5] | SPECIFIED (quoted); N_t UNSPECIFIED (U-PEER-1) | U-PEER-1, A-CFG-1 | R-PRIM-8, R-STG-11 | stage config PEER: judged → refined, first of three refining agents; fan-out N_t |
| P-PEER-4 | Rebuttal Coding Agent runs each task on C_best → E_reb | [§3.5] | SPECIFIED (quoted); whether its code stays UNSPECIFIED (U-PEER-2) | U-PEER-2, U-ART-15, U-TOP-5 | R-PRIM-8, R-STG-11 | stage config PEER: judged → refined, second refining agent |
| P-PEER-5 | Paper Enhancer: P_new, R_new, E_reb → a revised P_new | [§3.5] | SPECIFIED (quoted); its scope UNSPECIFIED (U-PEER-4) | U-PEER-4 | R-STG-11, R-INT-8 | stage config PEER: judged → refined, third refining agent |
| P-PEER-6 | the revised manuscript is reviewed again, replacing R_new and the score | [§3.5] | SPECIFIED (quoted); what N_peer counts AMBIGUOUS (A-PEER-1); last or best UNSPECIFIED (U-TOP-7) | A-PEER-1, U-TOP-7, A-TOP-5 | R-PRIM-3, R-PRIM-4, R-STG-11 | stage primitive: the re-judgement after a refine; stage config PEER: limit, at-limit policy, keep the last |

### 2.7 Meta-review: [stages/06](stages/06-meta-review.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-META-1 | Meta-Review Agent: P_new and R_new → Accept or Refine, with r_meta | [§3.6] | SPECIFIED (quoted); its criterion UNSPECIFIED (U-META-2) | U-META-2 | R-PRIM-7, R-STG-12 | stage config META: assessor and rule, verdict map |
| P-META-2 | Accept → export P+ ← P_new and C+ ← C_best | [§3.6] | SPECIFIED (quoted) | none | R-STG-12 | stage config META: verdict map, accept → export |
| P-META-3 | Refine → A_FullEng, guided by r_meta → h_new, E_new, C_new | [§3.6] | SPECIFIED (quoted); its model AMBIGUOUS (A-CFG-1) | A-CFG-1, U-ABL-2 | R-STG-12 | stage primitive: the refine step; stage config META: judged → refined, P_new and R_new judged and h_best refined by A_FullEng |
| P-META-4 | Result Comparison: E_new against E_best | [§3.6] | SPECIFIED (quoted); criterion AMBIGUOUS (A-ABL-3) | A-ABL-3, A-TOP-5, U-TOP-5 | R-PRIM-5, R-PRIM-6, R-STG-12, R-INT-3 | stage config META: guard |
| P-META-5 | strictly superior → a new core state; ablation, drafting and review run again | [§3.6] | SPECIFIED (quoted); the restart's extent AMBIGUOUS (A-META-1); budgets UNSPECIFIED (U-META-1) | A-META-1, U-META-1 | R-PRIM-5, R-PRIM-8, R-STG-12 | stage config META: nesting, the ABL, DRAFT and PEER configs inside its refine |
| P-META-6 | otherwise the refinement is discarded and the previous outputs are exported | [§3.6] | SPECIFIED (quoted); INCONSISTENT with the loop until approval (A-TOP-3) | A-TOP-3 | R-PRIM-5, R-STG-12 | stage config META: the guard's failure branch, export |
| P-META-7 | the meta stage's limit N_meta, or until Accept | [§3.6] [App. A.2] | SPECIFIED (quoted); a second verdict AMBIGUOUS (A-META-2) | A-META-2, A-TOP-1 | R-PRIM-3, R-PRIM-4, R-STG-12 | stage primitive: the stop test; stage config META: limit, at-limit policy |

### 2.8 Integrity mechanisms: [stages/07](stages/07-integrity.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-INT-1 | score verification, by a prompt: the Coding Agent is asked for reproducible scripts | [§4.2] | SPECIFIED (quoted); prompt or gate INCONSISTENT with App. B (A-INT-1) | A-INT-1, U-INT-4 | R-INT-1 | — (task 3) |
| P-INT-2 | specification compliance, by an LLM filter: rule-violating solutions discarded after experimentation | [§4.2] | SPECIFIED (quoted); hook points UNSPECIFIED (U-INT-1); task rules UNSPECIFIED (U-INT-2); which agent AMBIGUOUS (A-INT-3) | U-INT-1, U-INT-2, A-INT-3 | R-INT-4 | — (task 3) |
| P-INT-3 | reference verification, by an LLM fixer: a search-augmented LLM flags citations, the Writer Agent corrects them | [§4.2] | SPECIFIED (quoted); which writer AMBIGUOUS (A-INT-2); when UNSPECIFIED (U-INT-3) | A-INT-2, U-INT-3 | R-INT-5 | — (task 3) |
| P-INT-4 | method–code alignment, by an LLM fixer: an audit report, then the Writer Agent corrects the paper, not the code | [§4.2] | SPECIFIED (quoted); which agents AMBIGUOUS (A-INT-2, A-INT-3); when UNSPECIFIED (U-INT-3) | A-INT-2, A-INT-3, U-INT-3 | R-INT-6 | — (task 3) |
| P-INT-5 | the post-hoc audit behind Table 7, following ScientistOne, and what removing the refinement agents does | [§4.2] [Tab. 7] [fn. 2] [Ref: meng2026scientistone §5] | SPECIFIED by reference; App. B's account INCONSISTENT (A-INT-1); the auditor UNSPECIFIED (U-EVAL-5) | A-INT-1, U-EVAL-5, U-INT-4 | R-INT-7 | — (task 3) |

### 2.9 App. A.2 values: [analysis.md](analysis.md) section 6

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-CFG-1 | limitation rounds: 16, no symbol | [§3.1] [App. A.2] | SPECIFIED value; what it counts AMBIGUOUS (A-TOP-2); at the limit AMBIGUOUS (A-LIM-1) | A-TOP-2, A-LIM-1 | R-STG-1, R-STG-13 | stage config LIM: limit (its value) |
| P-CFG-2 | novelty references per idea: 2, from Google Search | [App. A.2] | SPECIFIED value; score and retrieval UNSPECIFIED (U-SEED-2) | U-SEED-2 | R-STG-2, R-STG-13, R-AGT-6 | stage config SEED: the assessor's input, two retrieved papers |
| P-CFG-3 | N_eng, the subset engineering budget: 2 | [§3.2] [App. A.2] | SPECIFIED value; what it counts AMBIGUOUS (A-TOP-2) | A-TOP-2 | R-STG-4, R-STG-13 | stage config SUB: limit (its value) |
| P-CFG-4 | N_k, evolved ideas per round k ≥ 1: 1 | [§3.3] [App. A.2] | SPECIFIED value | none | R-STG-7, R-STG-13 | stage config EVO: fan-out, evolved ideas |
| P-CFG-5 | N_e, unevaluated seeds per round k ≥ 1: 1 | [§3.3] [App. A.2] | SPECIFIED value | U-EVO-3 | R-STG-7, R-STG-13 | stage config EVO: fan-out, seeds |
| P-CFG-6 | K, refinement rounds: 4 | [§3.3] [App. A.2] [Fig. 9] (image) | SPECIFIED value; whether round 0 counts AMBIGUOUS (A-EVO-2) | A-EVO-2 | R-STG-7, R-STG-13 | stage config EVO: limit, K |
| P-CFG-7 | S, successes that stop the rounds: 4 | [§3.3] [App. A.2] | SPECIFIED value; when it is checked UNSPECIFIED (U-EVO-1) | U-EVO-1 | R-STG-7, R-STG-13 | stage config EVO: limit, the stop count S |
| P-CFG-8 | N_abl, ablation refinements: 1 | [§3.4] [App. A.2] | SPECIFIED value; what it counts AMBIGUOUS (A-TOP-2) | A-ABL-2, U-ABL-4, A-TOP-2 | R-STG-9, R-STG-13 | stage config ABL: limit (its value) |
| P-CFG-9 | the review-score threshold: 8 | [§3.5] [App. A.2] | SPECIFIED: App. A.2 fixes §3.5's example value; reviewer-dependent, to calibrate [ours] | A-EVAL-3 | R-STG-11, R-STG-13 | stage config PEER: the assessor's rule, the threshold |
| P-CFG-10 | N_peer, the review–rebuttal budget: 2 | [§3.5] [App. A.2] [Tab. 5] | SPECIFIED value; its unit AMBIGUOUS (A-PEER-1) | A-PEER-1, A-TOP-2 | R-STG-11, R-STG-13 | stage config PEER: limit (its value) |
| P-CFG-11 | N_meta, meta-review refinements: 1 | [§3.6] [App. A.2] [Tab. 6] | SPECIFIED value; a second meta-review AMBIGUOUS (A-META-2) | A-META-2, U-META-1, A-TOP-2 | R-STG-12, R-STG-13 | stage config META: limit (its value) |
| P-CFG-12 | N_seed, the size of the seed pool | [§3.1] [App. A.2] | UNSPECIFIED: App. A.2 sets no value (U-SEED-1) | U-SEED-1 | R-STG-2, R-STG-13 | stage config SEED: limit, the pool size |
| P-CFG-13 | N_0, the seeds run in round 0 | [§3.2] [§3.3] [App. A.2] | UNSPECIFIED value; round 0 AMBIGUOUS (A-EVO-1) | A-EVO-1 | R-STG-7, R-STG-13 | stage config EVO: fan-out in round 0 |
| P-CFG-14 | the full-set engineering limit, with no symbol | [§3.2] [App. A.2] | AMBIGUOUS: 2, or unset (A-FULL-2) | A-FULL-2 | R-STG-5, R-STG-13 | stage config FULL: limit (its value) |
| P-CFG-15 | N_p, the number of ablation plans | [§3.4] [App. A.2] [Tab. 15] | UNSPECIFIED (U-ABL-1); Table 15 reports 5–6 per paper | U-ABL-1 | R-STG-9, R-STG-13 | stage config ABL: fan-out N_p |
| P-CFG-16 | N_t, the number of rebuttal tasks | [§3.5] [App. A.2] | UNSPECIFIED (U-PEER-1) | U-PEER-1 | R-STG-11, R-STG-13 | stage config PEER: fan-out N_t |
| P-CFG-17 | N_a, the number of agents | [§3, Eq. 1] [App. A.2] | UNSPECIFIED: A.2 sets no value; the roster counts 27 [ours] | none | R-AGT-1 | — (task 3) |
| P-CFG-18 | the drafting format: ICLR 2025, following PaperOrchestra | [App. A.2] | SPECIFIED | U-DRAFT-2 | R-STG-10, R-STG-13 | — (task 3) |
| P-CFG-19 | model routing: Gemini 3.6 Flash for every agent but four, which run on Claude Code with Opus 4.8 | [App. A.2] [§4] [§4.2] | SPECIFIED; which agents run on Claude Code AMBIGUOUS (A-CFG-1) | A-CFG-1, A-CFG-2, U-CFG-1 | R-AGT-2 | — (task 3) |

### 2.10 Agent roster: [analysis.md](analysis.md) section 7

The paper tests every agent below only end to end, through Tables 5–8 and Figure 9b, so U-TOP-6 applies to each row; a judge is an agent whose output chooses a branch [Tab. 5] [Tab. 8] [Fig. 9b] (image) [ours].

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-ROSTER-1 | Limitation Extractor, on Gemini 3.6 Flash | [§3.1] [App. A.2] | SPECIFIED | U-LIM-1 | R-STG-1, R-AGT-1 | — (task 3) |
| P-ROSTER-2 | Limitation Verifier, a judge, on Gemini; absent from Figure 3 | [§3.1] [App. A.2] | SPECIFIED | U-LIM-1, A-LIM-1 | R-STG-1, R-AGT-1 | — (task 3) |
| P-ROSTER-3 | Initial Idea Generator, named only in Figure 4 | [§3.1] [Fig. 4] (image) | AMBIGUOUS: one agent with the Idea Generator, or two (A-SEED-2) | A-SEED-2 | R-STG-2, R-AGT-1 | — (task 3) |
| P-ROSTER-4 | Novelty Checker, a judge, on Gemini with Google Search | [§3.1] [App. A.2] | SPECIFIED; its score UNSPECIFIED (U-SEED-2) | U-SEED-2 | R-STG-2, R-AGT-1 | — (task 3) |
| P-ROSTER-5 | Idea Generator Agent, on Gemini | [§3.1] [App. A.2] | SPECIFIED; its name AMBIGUOUS (A-ROSTER-1) | A-ROSTER-1, U-SEED-3 | R-STG-2, R-AGT-1 | — (task 3) |
| P-ROSTER-6 | Baseline Coder, the Baseline Coding Agent | [§3.2] [Fig. 5] (image) | SPECIFIED; its backend and model AMBIGUOUS (A-CFG-1) | A-CFG-1, A-BASE-1 | R-STG-3, R-AGT-1 | — (task 3) |
| P-ROSTER-7 | Subset Coder, part of the Idea Experiment Coding Agent | [§3.2] [App. A.2] | SPECIFIED; Claude Code with Opus 4.8 [inferred] | A-CFG-1 | R-STG-4, R-AGT-1 | — (task 3) |
| P-ROSTER-8 | Subset Critic, a judge, on Gemini; App. A.2's Idea Critic Agent | [§3.2] [App. A.2] | SPECIFIED; A.2's name for it [inferred] | U-SUB-1, A-FULL-2 | R-STG-4, R-AGT-1 | — (task 3) |
| P-ROSTER-9 | Subset Engineer, the Subset Engineering Agent | [§3.2] [Fig. 5] (image) | SPECIFIED; its backend and model AMBIGUOUS (A-CFG-1) | A-CFG-1 | R-STG-4, R-AGT-1 | — (task 3) |
| P-ROSTER-10 | Full-Set Coder, part of the Idea Experiment Coding Agent | [§3.2] [App. A.2] | SPECIFIED; Claude Code with Opus 4.8 [inferred] | A-CFG-1, A-ART-12 | R-STG-5, R-AGT-1 | — (task 3) |
| P-ROSTER-11 | Full-Set Critic, a judge, on Gemini | [§3.2] [Tab. 1] | SPECIFIED; its reference AMBIGUOUS (A-FULL-1) | A-FULL-1, A-FULL-2, U-FULL-1 | R-STG-5, R-AGT-1 | — (task 3) |
| P-ROSTER-12 | Full-Set Engineer, re-engaged as A_FullEng in §3.4 and §3.6 | [§3.2] [§3.4] [§3.6] | SPECIFIED; its backend and model AMBIGUOUS (A-CFG-1) | A-CFG-1, U-ABL-2, A-ROSTER-1 | R-STG-5, R-STG-9, R-AGT-1 | — (task 3) |
| P-ROSTER-13 | Idea Implementer A_Coder, the composite of the §3.2 coders, critics and engineers, and of the baseline coder only if it runs per idea | [§3.2, Eq. 2] [Fig. 6] (image) | SPECIFIED; its membership follows A-BASE-1 | A-BASE-1, U-CODER-1 | R-STG-6, R-AGT-1 | — (task 3) |
| P-ROSTER-14 | Idea Evolver A_Evolve, on Gemini | [§3.3] [App. A.2] | SPECIFIED | U-EVO-2 | R-STG-7, R-AGT-1 | — (task 3) |
| P-ROSTER-15 | Selector A_Selector, a judge, on Gemini | [§3.3, Eq. 4] [App. A.2] | SPECIFIED; its criterion UNSPECIFIED (U-SEL-1) | U-SEL-1, U-SEL-2 | R-STG-8, R-AGT-1 | — (task 3) |
| P-ROSTER-16 | Ablation Planner, the Planning Agent of Figure 3 | [§3.4] [Fig. 3] (image) | SPECIFIED; its backend AMBIGUOUS (A-CFG-1): Claude Code only if it belongs to the Ablation Study Agent [inferred] | A-CFG-1, U-ABL-1 | R-STG-9, R-AGT-1 | — (task 3) |
| P-ROSTER-17 | Ablation Coder, part of the Ablation Study Agent | [§3.4] [App. A.2] | SPECIFIED; Claude Code with Opus 4.8 [inferred] | U-ABL-3 | R-STG-9, R-AGT-1 | — (task 3) |
| P-ROSTER-18 | Ablation Critic A_AblCritic, also written A_AblCrit, a judge, on Gemini | [§3.4] [App. A.2] | SPECIFIED; its model [inferred]; a reject INCONSISTENT (A-ABL-1) | A-ABL-1, U-ABL-5, U-ABL-6, A-TOP-5 | R-STG-9, R-AGT-1, R-AGT-9 | — (task 3) |
| P-ROSTER-19 | Result Comparison Agent, a judge, on Gemini | [§3.4] [§3.6] | SPECIFIED; its criterion AMBIGUOUS (A-ABL-3) | A-ABL-3 | R-PRIM-6, R-STG-9, R-AGT-1 | — (task 3) |
| P-ROSTER-20 | Initial Drafter A_Draft, incorporating PaperOrchestra | [§3.5] [Bib: song2026paperorchestra] | SPECIFIED; its model [inferred] | U-DRAFT-1, U-DRAFT-2 | R-STG-10, R-AGT-1 | — (task 3) |
| P-ROSTER-21 | Peer Reviewer A_Reviewer, a judge, which is ScholarPeer | [§3.5] [Bib: goyal2026scholarpeer] | SPECIFIED; its backbone UNSPECIFIED (U-PEER-3) | U-PEER-3, A-ROSTER-1 | R-STG-11, R-AGT-1 | — (task 3) |
| P-ROSTER-22 | Rebuttal Planner A_RebPlan | [§3.5] | SPECIFIED; its backend AMBIGUOUS (A-CFG-1) | A-CFG-1, U-PEER-1 | R-STG-11, R-AGT-1 | — (task 3) |
| P-ROSTER-23 | Rebuttal Coder A_RebCoder, the Rebuttal Agent | [§3.5] [App. A.2] | SPECIFIED; Claude Code with Opus 4.8 [inferred] | U-PEER-2 | R-STG-11, R-AGT-1 | — (task 3) |
| P-ROSTER-24 | Paper Enhancer A_Enhancer, the Draft Enhancer, on Claude Code with Opus 4.8 | [§3.5] [App. A.2] | SPECIFIED | U-PEER-4 | R-STG-11, R-AGT-1 | — (task 3) |
| P-ROSTER-25 | Meta-Reviewer A_Meta, a judge, on Gemini | [§3.6] [App. A.2] | SPECIFIED | U-META-2 | R-STG-12, R-AGT-1 | — (task 3) |
| P-ROSTER-26 | specification filter: the Coding Agent as a judge, which nothing makes read-only | [§4.2] [Tab. 7] | SPECIFIED; its model [inferred]; which session AMBIGUOUS (A-INT-3) | A-INT-3, U-INT-1 | R-AGT-1, R-INT-4, R-INT-9 | — (task 3) |
| P-ROSTER-27 | reference checker, a search-augmented LLM | [§4.2] | SPECIFIED; its model not stated | A-INT-2, U-INT-3 | R-AGT-1, R-INT-5 | — (task 3) |
| P-ROSTER-28 | method–code auditor: the Coding Agent as a judge, which saved its verdict inside the task it audited | [§4.2] [p. 47] | SPECIFIED; its model [inferred]; which session AMBIGUOUS (A-INT-3) | A-INT-3, U-INT-3 | R-AGT-1, R-INT-6, R-INT-9 | — (task 3) |

### 2.11 Group names and external systems: [analysis.md](analysis.md) sections 7.1–7.2

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-ROSTER-29 | Idea Generator, Figure 3's box around seed generation and the evolver | [Fig. 3] (image) | SPECIFIED (image); its name collides (A-ROSTER-1) | A-ROSTER-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-30 | Seed Idea Generator: the Limitation Extractor and the Novelty Checker | [Fig. 3] (image) | SPECIFIED (image) | none | R-AGT-3 | — (task 3) |
| P-ROSTER-31 | Evaluator: the two experiment agents | [Fig. 3] (image) | SPECIFIED (image); that it is A_Coder [inferred] | A-BASE-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-32 | Subset Experiment Agent: a Coding Agent and a Critic Agent in a cycle | [Fig. 3] (image) | SPECIFIED (image) | U-BASE-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-33 | Full-Set Experiment Agent: the same pair, with no separate engineer | [Fig. 3] (image) | SPECIFIED (image) | A-CFG-1, U-ABL-2 | R-AGT-3 | — (task 3) |
| P-ROSTER-34 | Analyzer: the Ablation Study Agent and an Idea Refiner | [Fig. 3] (image) | SPECIFIED (image) | U-ABL-2 | R-AGT-3 | — (task 3) |
| P-ROSTER-35 | Ablation Study Agent: a Planning Agent and a Coding Agent | [Fig. 3] (image) [App. A.2] | SPECIFIED; App. A.2's Claude Code group [inferred] | A-CFG-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-36 | Idea Refiner, drawn twice, in the Analyzer and in the Meta-Review Agent box | [Fig. 3] (image) | AMBIGUOUS: one name for two roles (A-ROSTER-1) | A-ROSTER-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-37 | Writer Agent: the Initial Drafter and the Draft Enhancer | [Fig. 3] (image) [§4.2] | SPECIFIED; which one repairs the paper AMBIGUOUS (A-INT-2) | A-INT-2 | R-AGT-3, R-INT-5 | — (task 3) |
| P-ROSTER-38 | Peer-Review Agent: in Figure 3 a box of two agents, in §1 the reviewer | [Fig. 3] (image) [§1] | AMBIGUOUS (A-ROSTER-1) | A-ROSTER-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-39 | Rebuttal Agent, the §3.5 planner and coder | [§3] [§4.2] [App. A.2] | SPECIFIED; its members [inferred]; the planner's backend AMBIGUOUS (A-CFG-1) | A-CFG-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-40 | Meta-Review Agent as a box: a Critic Agent and an Idea Refiner | [Fig. 3] (image) | SPECIFIED (image); its members [inferred] | A-ROSTER-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-41 | Idea Experiment Coding Agent, App. A.2's group for the coders of A_Coder | [App. A.2] | SPECIFIED; which coders it holds AMBIGUOUS (A-CFG-1) | A-CFG-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-42 | Idea Critic Agent, App. A.2's name for the subset critic, and perhaps the full-set one | [App. A.2] | SPECIFIED; its scope AMBIGUOUS (A-FULL-2) | A-FULL-2 | R-AGT-3 | — (task 3) |
| P-ROSTER-43 | Coding Agent, a generic name | [§4.2] [Fig. 3] (image) | SPECIFIED; which session runs the checks AMBIGUOUS (A-INT-3) | A-INT-3 | R-AGT-3 | — (task 3) |
| P-ROSTER-44 | Critic Agent, a generic name; App. C prints a page of its feedback | [Fig. 3] (image) [App. C] | SPECIFIED; which critic wrote that page AMBIGUOUS (A-ART-1) | A-ART-1 | R-AGT-3 | — (task 3) |
| P-ROSTER-45 | PaperOrchestra, inside the Initial Drafter | [§2] [§3.5] [Bib: song2026paperorchestra] | SPECIFIED; how it divides the work UNSPECIFIED (U-DRAFT-1) | U-DRAFT-1 | R-AGT-7 | — (task 3) |
| P-ROSTER-46 | ScholarPeer, the in-loop reviewer and an evaluation reviewer | [§3.5] [§4] [Bib: goyal2026scholarpeer] | SPECIFIED; its configuration UNSPECIFIED (U-PEER-3) | U-PEER-3, U-EVAL-2 | R-AGT-5 | — (task 3) |
| P-ROSTER-47 | Google Search, two reference papers per novelty check | [App. A.2] | SPECIFIED; the query UNSPECIFIED (U-SEED-2) | U-SEED-2 | R-AGT-6 | — (task 3) |
| P-ROSTER-48 | Claude Code with Opus 4.8, the coding backend | [§4.2] [App. A.2] | SPECIFIED; which agents use it AMBIGUOUS (A-CFG-1) | A-CFG-1, U-CFG-1 | R-AGT-4 | — (task 3) |
| P-ROSTER-49 | Antigravity with Gemini 3.8 Flash, Table 8's replacement backend | [§4.2] [Tab. 8] | SPECIFIED; its Gemini version AMBIGUOUS (A-CFG-2) | A-CFG-2 | R-AGT-4 | — (task 3) |
| P-ROSTER-50 | Stanford Agentic Reviewer, the held-out evaluator | [§4] [fn. 1] | SPECIFIED; its acceptance rule UNSPECIFIED (U-EVAL-3) | U-EVAL-3 | R-MEAS-5 | — (task 3) |
| P-ROSTER-51 | CoE Integrity Audit, a post-hoc evaluation and not a stage | [§4.2] [Bib: meng2026scientistone] | SPECIFIED by reference; its auditor UNSPECIFIED (U-EVAL-5) | U-EVAL-5, A-INT-1 | R-INT-7 | — (task 3) |

### 2.12 State and data objects: [analysis.md](analysis.md) section 8

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-STATE-1 | the task G: the paper, its code, and whatever else a task holds | [§3, Eq. 1] | SPECIFIED; its contents UNSPECIFIED (U-TOP-1); read-only [ours] | U-TOP-1, A-TOP-4 | R-RUN-2, R-STATE-1 | task environment; read-only |
| P-STATE-2 | the evaluation protocol, part of G | [App. B] [Tab. 15] | SPECIFIED: changing it is forbidden, by audit | U-INT-4, A-INT-1 | R-RUN-2, R-STATE-1, R-INT-2 | evaluation harness; read-only and hash-checked by the setup, where the paper relies on an audit [ours] |
| P-STATE-3 | the set of limitations | [§3.1] | SPECIFIED; it grows until the Verifier confirms | U-LIM-1 | R-STATE-2 | run state; grows within its stage, then fixed |
| P-STATE-4 | the seed pool H_0 with its scores, and the record of seeds already run | [§3.1] [§3.3] | SPECIFIED; the record is implied by the next unevaluated seeds; mutability [ours] | U-SEED-1, U-EVO-3 | R-STATE-2 | run state; the pool fixed once sorted, the record append-only |
| P-STATE-5 | the baseline, E_base and C_base | [§3.2] | SPECIFIED; copied into each idea [inferred] | A-BASE-1, U-BASE-2 | R-STG-3, R-STATE-4 | run state; read-only, copied into each idea's sandbox |
| P-STATE-6 | one idea's working state: h, E_sub^h, C_sub^h, E_full^h, C_full^h, d^h, r^h | [§3.2] | SPECIFIED; engineering rewrites h and its code | U-CODER-1 | R-STG-6, R-STATE-4 | sandbox, one per A_Coder call; changes within the call |
| P-STATE-7 | the traces R_k and their union, tuples (h, E^h, C^h, d^h, r^h) | [§3.3, Eq. 3] | SPECIFIED (Eq. 3); append-only [inferred] | U-EVO-2, U-SEL-2 | R-STG-7, R-STATE-2 | run state; append-only |
| P-STATE-8 | a round's candidates: I_k, H_0^(k), H_k and the round index k | [§3.3] | SPECIFIED; fixed per round [ours] | U-EVO-1, A-EVO-1 | R-STG-7, R-STATE-5 | run state; fixed once the round starts |
| P-STATE-9 | the core state, h_best, E_best, C_best | [§3.3, Eq. 4] [§3.4] [§3.6] | SPECIFIED (Eq. 4); replaced only through the guard, if and only if the new result is preferred | A-ABL-3 | R-PRIM-5, R-STG-8, R-STATE-3 | run state; replaced only through the guard |
| P-STATE-10 | an ablation pass: plans, outcomes, E_abl, d_abl and r_abl | [§3.4] | SPECIFIED; regenerated after an update | U-ABL-1, U-ABL-3 | R-STG-9, R-STATE-5 | run state; one record per pass, regenerated after an update |
| P-STATE-11 | a refinement candidate, h_new, E_new, C_new | [§3.4] [§3.6] | SPECIFIED; promoted or discarded | U-ABL-2 | R-STG-9, R-STATE-3 | run state; promoted to the core state, or discarded |
| P-STATE-12 | the manuscript P_new | [§3.5] | SPECIFIED; each enhancement replaces it, and the last is kept | U-TOP-7, U-PEER-4 | R-STG-10, R-STG-11, R-STATE-5 | run state; one version per enhancement, the kept one last or best (U-TOP-7) |
| P-STATE-13 | the review R_new, with its score s_review, also written s_new | [§3.5] | SPECIFIED; overwritten each round | A-TOP-5, U-PEER-3 | R-STG-11, R-STATE-2 | run state; overwritten each round |
| P-STATE-14 | a rebuttal round: tasks, results, E_reb | [§3.5] | SPECIFIED; fixed once run [ours] | U-PEER-1, U-PEER-2 | R-STG-11, R-STATE-5 | run state; fixed once run |
| P-STATE-15 | the meta decision d_meta, with r_meta | [§3.6] | SPECIFIED; fixed once made [ours] | U-META-2 | R-STG-12, R-STATE-5 | run state; fixed once made |
| P-STATE-16 | the chain of codebase versions, from C_base through C_best and C_new to C+ | [§3.2] [§3.4] [§3.6] | SPECIFIED; copied, never edited in place [inferred] | U-ABL-3, U-PEER-2 | R-STATE-4 | run state: code snapshots, copied and never edited in place |
| P-STATE-17 | the outputs P+ and C+ | [§3, Eq. 1] [§3.6] | SPECIFIED; fixed at export [ours] | A-TOP-3, U-TOP-1 | R-RUN-1, R-STATE-6 | run state: the export, fixed; the next run's task environment when runs are chained |

### 2.13 Artifacts of Appendices C and D: [artifacts.md](artifacts.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-ART-1 | limitations of X-Mahalanobis: five, each a flaw, why it limits, an opportunity | [pp. 34–35] | producer [inferred] from content | U-ART-2 | R-AGT-8 | — (task 3) |
| P-ART-2 | the idea Procrustes-DS: components tagged by limitation, with PyTorch code | [pp. 36–39] | producer [inferred] from content | U-ART-3 | R-AGT-8 | — (task 3) |
| P-ART-3 | the experimental evaluation report of the refined idea | [pp. 40–42] | producer [inferred]; which critic led to it AMBIGUOUS (A-ART-1) | A-ART-1, A-ART-5, A-ART-12, U-ART-4, U-ART-11, U-ART-16, U-ART-20 | R-AGT-8, R-AGT-9 | — (task 3) |
| P-ART-4 | the ablation study report: one plan, eight variants | [pp. 43–45] | producer [inferred] | U-ART-5, U-ART-13 | R-AGT-8 | — (task 3) |
| P-ART-5 | the critic's feedback: five component flaws, no verdict printed | [p. 46] | producer [inferred]; which critic AMBIGUOUS (A-ART-1) | A-ART-1, A-ART-4, U-ART-10 | R-AGT-8, R-AGT-9 | — (task 3) |
| P-ART-6 | the reproducibility audit: one re-run, one boolean | [p. 47] | producer AMBIGUOUS (A-ART-2); its scope AMBIGUOUS against Table 7 (A-ART-3) | A-ART-2, A-ART-3, U-ART-6, U-ART-7 | R-AGT-8, R-AGT-9, R-INT-7 | — (task 3) |
| P-ART-7 | the specification and alignment audit: two booleans with evidence | [pp. 48–50] | producer AMBIGUOUS (A-ART-2) | A-ART-2, U-ART-7, U-ART-8, U-ART-9 | R-AGT-8, R-INT-7 | — (task 3) |
| P-ART-8 | the rebuttal report for TABHARMONY | [pp. 51–55] | producer [inferred] | U-ART-14, U-ART-15 | R-AGT-8, R-OPS-8 | — (task 3) |
| P-ART-9 | the final paper, DynaSpec-RAG: 16 pages in the ICLR 2025 template | [pp. 56–71] [App. D] | the paper's own statement; who wrote which part UNSPECIFIED (U-ART-19) | A-ART-7, A-ART-8, A-ART-9, A-ART-10, U-ART-12, U-ART-18, U-ART-19 | R-STG-10 | — (task 3) |
| P-ART-10 | the generated-paper pages inside Figures 2 and 8 | [Fig. 2] [Fig. 8] [p. 3] [p. 11] | producer [inferred] | U-ART-12 | X-5 | — (task 3) |
| P-ART-11 | one task's run layout, commands and environments | [pp. 40–55] | [ours], derived from the pages | U-ART-17, U-ART-15 | R-STATE-8 | — (task 3) |

### 2.14 Measurement, benchmark and cost: [claims.md](claims.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-EVAL-1 | task success | [Fig. 1] [Tab. 3] [Tab. 15] | AMBIGUOUS (A-EVAL-1) | A-EVAL-1, A-ABL-1 | R-MEAS-1 | — (task 3) |
| P-EVAL-2 | the relative gain of one paper | [§4.1] | UNSPECIFIED (U-EVAL-1); its baseline AMBIGUOUS (A-EVAL-2) | U-EVAL-1, A-EVAL-2, U-TOP-5 | R-MEAS-2 | — (task 3) |
| P-EVAL-3 | the gain across papers: mean and median over the successes | [Tab. 4] | SPECIFIED in part | U-EVAL-1 | R-MEAS-3 | — (task 3) |
| P-EVAL-4 | the average rating | [Tab. 3] [§3.5] | AMBIGUOUS (A-EVAL-4); reviewer set-up UNSPECIFIED (U-EVAL-2) | A-EVAL-4, U-EVAL-2 | R-MEAS-4 | — (task 3) |
| P-EVAL-5 | ScholarPeer acceptance | [Tab. 3] [§3.5] | INCONSISTENT (A-EVAL-3) | A-EVAL-3 | R-MEAS-4 | — (task 3) |
| P-EVAL-6 | the Stanford Agentic Reviewer's rating and acceptance | [§4] [fn. 1] | UNSPECIFIED (U-EVAL-3) | U-EVAL-3 | R-MEAS-5 | — (task 3) |
| P-EVAL-7 | which reviewer is in the loop: ScholarPeer, with the other held out | [§4] | SPECIFIED | U-EVAL-2 | R-AGT-5, R-MEAS-5 | — (task 3) |
| P-EVAL-8 | the review rounds of Table 5 | [Tab. 5] | AMBIGUOUS (A-EVAL-5) | A-EVAL-5, A-PEER-1 | R-MEAS-6 | — (task 3) |
| P-EVAL-9 | runs, seeds and variance | [Tab. 2] [§4] | UNSPECIFIED (U-EVAL-4) | U-EVAL-4, U-ART-12 | R-MEAS-7 | — (task 3) |
| P-EVAL-10 | the CoE integrity audit as a measurement | [§4.2] [Tab. 7] | checks SPECIFIED; auditor UNSPECIFIED (U-EVAL-5) | U-EVAL-5, A-ART-2 | R-INT-7 | — (task 3) |
| P-EVAL-11 | the human evaluation | [§4.3] [Tab. 10] | protocol UNSPECIFIED (U-EVAL-6) | U-EVAL-6 | X-1 | — (task 3) |
| P-EVAL-12 | the radar of Figure 1a | [Fig. 1a] (image) | UNSPECIFIED (U-EVAL-7) | U-EVAL-7 | X-2 | — (task 3) |
| P-EVAL-13 | the per-round gain of Figure 9a | [Fig. 9a] (image) | UNSPECIFIED (U-EVAL-8); AMBIGUOUS against Table 4 (A-EVAL-6) | U-EVAL-8, A-EVAL-6 | R-MEAS-6 | — (task 3) |
| P-EVAL-14 | other systems' numbers | [Tab. 2] [Tab. 4] [Tab. 16] | SPECIFIED in part | U-EVAL-9, U-EVAL-10, A-EVAL-7 | X-3 | — (task 3) |
| P-EVAL-15 | the rating of Table 9 | [Tab. 9] | AMBIGUOUS (A-EVAL-8) | A-EVAL-8 | X-4 | — (task 3) |
| P-BENCH-1 | the 107 tasks: 38 NeurIPS 2025, 5 ICLR 2026, 64 ICML 2026 Spotlight | [App. A.1] [Tab. 12] [Tab. 13] [Tab. 14] | SPECIFIED | U-BENCH-1 | R-MEAS-9 | — (task 3) |
| P-BENCH-2 | what a task gives the engine | [§4.1] | UNSPECIFIED (U-BENCH-1) | U-BENCH-1, U-TOP-1 | R-RUN-2 | — (task 3) |
| P-BENCH-3 | how the 64 ICML tasks were chosen | [App. A.1] | UNSPECIFIED (U-BENCH-2) | U-BENCH-2 | R-MEAS-9 | — (task 3) |
| P-BENCH-4 | the 21 failed tasks | [Tab. 3] [Tab. 16] | UNSPECIFIED (U-BENCH-3) | U-BENCH-3 | R-RUN-5 | — (task 3) |
| P-COST-1 | the dollar cost, $3765 per task | [§4.3] [Fig. 10b] (image) | components UNSPECIFIED (U-COST-1) | U-COST-1 | R-MEAS-8 | — (task 3) |
| P-COST-2 | which runs are costed: 33 NeurIPS tasks | [§4.3] | UNSPECIFIED (U-COST-2) | U-COST-2 | R-MEAS-8 | — (task 3) |
| P-COST-3 | the time per task | [Fig. 10a] (image) | UNSPECIFIED (U-COST-3) | U-COST-3 | R-MEAS-8 | — (task 3) |
| P-COST-4 | the stage breakdown of time and cost | [Fig. 10b] (image) | AMBIGUOUS (A-COST-1) | A-COST-1 | R-MEAS-8 | — (task 3) |

## Part 3: acceptance targets, a shortlist

Candidates for the acceptance tests of our replication. A target is fair when the paper defines it, we can measure it at our scale in our locked harness, and it does not reward the reviewer the loop optimizes. Every judgment in this part is ours [ours].

| Candidate target | Source | Fair? | Why [ours] |
|---|---|---|---|
| Every stage's limit and early stop holds as App. A.2 sets it, read by the one primitive from each stage's config: 16 limitation rounds, N_eng = 2, one seed and one evolved idea per round, K = 4, S = 4, N_abl = 1, a stop at score 8 within N_peer = 2, N_meta = 1 | P-CFG-1 … 11 [App. A.2] | Yes | deterministic, and testable at no cost with a mocked LLM that counts calls; what four limits count must be decided first (A-TOP-2, A-EVO-2, A-PEER-1, A-META-2), and each stage's at-limit policy too (A-TOP-1, U-TOP-7) [ours] |
| A refinement replaces the core state only when the comparison prefers it; a failed meta refinement exports the previous outputs | P-ABL-5, P-META-5, P-META-6, P-STATE-9 [§3.4] [§3.6] | Yes | a control-flow rule, testable with fixture results; the comparison's own criterion stays open (A-ABL-3) [ours] |
| The ablation critic rejects a variant whose gain comes from generic training controls, as it did for DMC-TeCh | C-APPB-5, P-ABL-7, P-ART-5 [App. B] [Tab. 16] | As a planted fixture, yes; as a task outcome, no | a fixture ablation in which EMA and label smoothing carry the gain tests the attribution rule; TeCh is one task, the paper prints no DMC-TeCh numbers, §3.4 gives the critic no reject (A-ABL-1), and the line between `Refine` and a reject is open, with TeCh, p. 46 and LC-FTT as its first cases (U-ABL-5) [ours] |
| The specification filter discards a reward-hacking solution, and an edit to the evaluator is blocked | P-INT-2, P-STATE-2 [§4.2] [fn. 2]; C-APPB-7 [Tab. 16] | Yes, as planted defects | footnote 2 records one real catch, and App. B's T-SAE change to how tokens are shown to the judge is a ready-made defect; a violation needs our own task rules first (U-INT-2) [ours] |
| Every exported run passes the four integrity checks; Table 7 reports 49/49 reproducible, 0/49 violations, 0 of 1814 references hallucinated, 49/49 aligned | C-ABLX-7 [Tab. 7] | As a gate on our exports, yes; as counts to match, no | Table 7's first row passes a reward-hacked codebase on score verification, 50/50 with 1/50 violations, so the check as run shows determinism, not validity; the auditor is unnamed (U-EVAL-5); ours runs in the locked harness, under a judge that is not the fixer [ours] |
| Without the refinement agents the checks fail on some papers: 1/50 violations, 19/1840 hallucinated references, 39/50 aligned | C-ABLX-7 [Tab. 7] | Yes, as a sensitivity check | it shows that the checks can fail; the direction is the target, not the counts [ours] |
| Re-executing the solution reproduces the reported scores | P-ART-6 [p. 47]; I1 [Ref: meng2026scientistone §5] | Yes, as ScientistOne defines it | I1 re-runs the solution on a fixed evaluator within a tolerance, set in ScientistOne's own runs to five runs and the larger of 1% and three standard deviations over the mean (paraphrase) (ref:2605.26340v1:sections/06a_setup.tex:10); p. 47 re-ran the agent's own script once, for the method only, with no tolerance (A-ART-3, U-ART-6); ours runs I1 on the locked harness (U-INT-4) [ours] |
| The review loop raises the in-loop score: ScholarPeer 5.2 to 7.6, acceptance 46.9% to 93.9% | C-ABLX-3 [Tab. 5] | No | ScholarPeer is the reviewer the loop optimizes, as the paper itself says [§4 "Common Setup"]; the judge we report is never the reviewer we optimize against [ours] |
| Held-out acceptance: the Stanford Agentic Reviewer accepts 72.1% of the papers, and 0% for every baseline | C-MAIN-2 [Tab. 2] | As a direction only | the paper's only held-out evidence, but its acceptance rule is unknown (U-EVAL-3), the service is versioned by its host, and the second review round adds no held-out gain (C-ABLX-4) [ours] |
| Success on 86 of 107 tasks, 80.4% | C-HEAD-1 [Tab. 3] [Fig. 1] | No | success has three readings (A-EVAL-1) and is declared on the data the search selected on (U-TOP-5); 107 tasks at about $3765 each is beyond a pilot; one run per task, so no interval [ours] |
| Mean relative gain 25.2%, median 7.7% | C-HEAD-2 [Tab. 4] | No | parsed by Gemini from the generated papers under no stated rule (U-EVAL-1), a success-only mean pulled up by a few outliers, and inflated by selection on the reported data by an amount that cannot be sized without variance (P-EVAL-2); ours is a gain the harness computes under a rule fixed in advance, reported as median and failure-inclusive mean [ours] |
| Idea evolution raises the best gain after round 0, most in round 1: 20.6%, 30.8%, then 33.4% at round 4 | C-ABLX-1 [Fig. 9a] (image) | Its shape only | the per-round gain is undefined (U-EVAL-8), and no control arm separates evolution from trying more ideas; a fair test sets evolved ideas against fresh seeds at the same budget [ours] |
| About $3765 and 2.5 days per task, with 45.4% of the cost in idea refinement | C-DISC-1, C-DISC-2, C-DISC-3 [§4.3] [Fig. 10] (image) | As a budget reference only | prices, machines and failed runs are not reported (U-COST-1, U-COST-2); our ledger records cost by stage, and the paper's split is a sanity check [ours] |
| A second coding backend still completes tasks: 3 of 5 with Antigravity | C-ABLX-8, P-ROSTER-48, P-ROSTER-49 [Tab. 8] | As a structural test, yes | the target is that the engine runs end to end through a second adapter; 3 of 5, with another Gemini version, is no number to match [ours] |
| Five or six ablations per paper | C-APPB-4, P-CFG-15 [Tab. 15] | As a default for N_p, not a target | it is the only count the paper gives for N_p, which App. A.2 leaves unset (U-ABL-1) [ours] |
| Results on one task, or under an unstated protocol: FCD-Engram over LFR-Engram, three chained gains, parity with human papers | C-ABLX-6 [Tab. 6]; C-DISC-4 [Tab. 9]; C-DISC-5 [Tab. 10] | No | one task each, or a protocol the paper does not give (U-EVAL-6); the fair measure behind the first is how often a meta-review Refine is kept across tasks, which the paper never reports [ours] |

- **In short.** The fair targets are the mechanics (rows 1–2), the planted behaviours (rows 3, 4, 6 and 7), the integrity gate (row 5) and the backend swap (row 14) [ours].
- **Not fair as numbers:** every headline outcome (rows 8–11 and 16), since each rests on an undefined measure, on the reviewer the loop optimizes, or on one task; rows 12, 13 and 15 serve as a shape, a budget and a default [ours].
