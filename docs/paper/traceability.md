# Traceability: paper element → requirement → component

**For** TODO tasks 2 (requirements) and 3 (components), and for the reviewers of task 1. **Holds**
one row for every element of ScientistTwo (arXiv:2609.19644v1) that this folder defines, with the
requirement it becomes and the component that meets it; task 1 fills the paper side, and tasks 2
and 3 fill the rest [ours]. Conventions, sources and IDs follow [README.md](README.md) [ours].

- **Part 1** checks, part by part, that every part of the paper TODO task 1 requires is captured by elements, and names what no element captures [ours].
- **Part 2** is the map: 127 P- IDs over 20 keys, one row each [ours].
- **Part 3** lists the quantitative claims and artifact behaviours that could become acceptance targets for our replication, and says why each is or is not fair [ours].

## Controls

- **Coverage.** `python3 playground/paper/trace_coverage.py` collects every P- ID that a source document declares in a heading, the way the README's stage template introduces elements (`### <stage> [...] · P-<KEY>-1 … n`), expands ranges, and requires each ID exactly once in Part 2, alone in the first cell of its row [ours].
- **What else fails it:** an ID in Part 2 that nothing defines; an ID declared by two documents; a hole in a key's numbering; an undefined ID named in a source document or in Parts 1 and 3; a gap ID in Part 2 that no gap list defines [ours].
- **It can fail.** `--selftest` plants 15 defects beside a clean twin, and each must yield exactly its expected kind of problem; `--trace FILE` checks a copy of this file, which is how the planted run below was made [ours].
- **What it reads.** analysis.md, artifacts.md, claims.md, note-check.md, stages/ and claims/: 16 documents. README.md (whose IDs are examples), unspecified.md (a register of gaps) and this file define no element [ours].
- **Result, 2026-09-27.** 127 P- IDs defined over 20 keys, 127 rows in Part 2, 0 problems; the 16 source documents have no collision, no numbering hole and no dangling reference [ours].
  - Per key: ABL 6, ART 11, BASE 1, BENCH 4, CFG 11, CODER 1, COST 4, DRAFT 1, EVAL 15, EVO 6, FULL 3, INT 5, LIM 4, META 7, PEER 6, ROSTER 28, SEED 4, SEL 1, SUB 4, TOP 5 [ours].
  - The self-test passes all 16 cases. The planted copy, with the row for P-SUB-3 deleted and the row for P-EVO-2 repeated, exits 1 with exactly those two problems, although its totals still read 127 against 127: counts alone would have missed both [ours].
- **Citations.** `python3 playground/paper/check_citations.py docs/paper/traceability.md` passes [ours].

## Part 1: coverage of the paper

Each row is a part of the paper that TODO task 1 requires, the elements that capture it, where they are defined, and what no element captures. A range such as P-LIM-1 … 4 names every ID in between [ours].

### 1.1 Sections, Listing 1, Table 1 and Figures 3–7

| Part of the paper | Elements that capture it | Defined in | Left without an element |
|---|---|---|---|
| §3 overview [§3] | P-TOP-4, the end-to-end control flow; P-TOP-5, its termination branches; P-TOP-2, whose scope the overview claims for every stage | [analysis.md](analysis.md) sections 3–4 | the loop "until the manuscript is approved" is only the gap A-TOP-3 [§3] |
| Problem setup [§3 "Problem Setup"] | P-TOP-1: Eq. 1, what P+ and C+ must do, what G is | [analysis.md](analysis.md) section 2 | N_a, the number of agents [§3, Eq. 1], has a row in analysis.md section 6 and no ID; the contents of G are U-TOP-1 |
| Seed ideas [§3.1] | P-LIM-1 … 4, P-SEED-1 … 4; agents P-ROSTER-1 … 5; limits P-CFG-1, P-CFG-2 | [stages/01](stages/01-seed-ideas.md); [analysis.md](analysis.md) sections 6–7 | N_seed: a row, no ID (U-SEED-1) |
| Evaluating ideas [§3.2] | P-BASE-1, P-SUB-1 … 4, P-FULL-1 … 3, P-CODER-1; agents P-ROSTER-6 … 13; limit P-CFG-3 | [stages/02](stages/02-evaluating-ideas.md); [analysis.md](analysis.md) sections 6–7 | N_0 (A-EVO-1) and the full-set engineering limit (A-FULL-2): rows, no ID |
| Refining ideas [§3.3] | P-EVO-1 … 6, P-SEL-1; agents P-ROSTER-14, P-ROSTER-15; limits P-CFG-4 … 7 | [stages/03](stages/03-refining-ideas.md); [analysis.md](analysis.md) sections 6–7 | none |
| Ablation [§3.4] | P-ABL-1 … 6; agents P-ROSTER-12, P-ROSTER-16 … 19; limit P-CFG-8 | [stages/04](stages/04-ablation.md); [analysis.md](analysis.md) sections 6–7 | N_p: a row, no ID (U-ABL-1) |
| Drafting and review [§3.5] | P-DRAFT-1, P-PEER-1 … 6; agents P-ROSTER-20 … 24; limits P-CFG-9, P-CFG-10 | [stages/05](stages/05-drafting-peer-review.md); [analysis.md](analysis.md) sections 6–7 | N_t: a row, no ID (U-PEER-1) |
| Meta-review [§3.6] | P-META-1 … 7; agents P-ROSTER-12, P-ROSTER-19, P-ROSTER-25; limit P-CFG-11; the export, P-TOP-5 | [stages/06](stages/06-meta-review.md); [analysis.md](analysis.md) sections 4, 6, 7 | none |
| Listing 1 [Lst. 1] | P-TOP-2, the primitive verbatim | [analysis.md](analysis.md) section 3.1 | none |
| Table 1 [Tab. 1] | P-TOP-3, all eleven rows against Listing 1; each row is also the heading of its stage in stages/01–06, keys LIM to META | [analysis.md](analysis.md) section 3.2; [stages/](stages/) | none |
| Figure 3 [Fig. 3] (image) | its agent labels, in the name column of the roster rows for the agents it draws (all within P-ROSTER-1 … 25); G drawn as a human request, in P-TOP-1 | [analysis.md](analysis.md) sections 2 and 7 | the six group boxes (Idea Generator, Evaluator, Analyzer, Writer Agent, Peer-Review Agent, Meta-Review Agent), listed in analysis.md section 7.1 with no ID |
| Figure 4 [Fig. 4] (image) | P-LIM-1 … 4, P-SEED-1 … 4; the Initial Idea Generator, drawn only here, is P-ROSTER-3 | [stages/01](stages/01-seed-ideas.md); [analysis.md](analysis.md) section 7 | none |
| Figure 5 [Fig. 5] (image) | P-BASE-1 with its placement (A-BASE-1), P-SUB-1 … 4, P-FULL-1 … 3 with the engineer loop at full scale, P-CODER-1 | [stages/02](stages/02-evaluating-ideas.md) | none |
| Figure 6 [Fig. 6] (image) | P-EVO-1 … 6, P-SEL-1 | [stages/03](stages/03-refining-ideas.md) | none |
| Figure 7 [Fig. 7] (image) | P-ABL-1 … 6, P-DRAFT-1, P-PEER-1 … 6, P-META-1 … 7; its edges carry A-ABL-2 and A-META-1 | [stages/04](stages/04-ablation.md) to [stages/06](stages/06-meta-review.md) | none |
| Common Setup [§4 "Common Setup"] | P-BENCH-1, the 107 problems; P-EVAL-7, ScholarPeer in the loop and the Stanford Agentic Reviewer held out; P-EVAL-4 and P-EVAL-6, their scores | [claims.md](claims.md) | the models sentence ("Gemini 3.6 Flash and Claude Opus 4.8") is cited in analysis.md section 7 but is no element; the routing it loosens is A-CFG-1 |
| CoE Integrity Audit [§4.2 "CoE Integrity Audit"] | P-INT-1 … 5; agents P-ROSTER-26 … 28; the audit as a measurement, P-EVAL-10; its pages, P-ART-6, P-ART-7 | [stages/07](stages/07-integrity.md); [analysis.md](analysis.md) section 7; [claims.md](claims.md); [artifacts.md](artifacts.md) | none |
| Benchmark [App. A.1] | P-BENCH-1 … 3 | [claims.md](claims.md) | none |
| Configuration [App. A.2] | P-CFG-1 … 11, every limit A.2 sets; the routing sentence, in the model column of P-ROSTER-1 … 28; the ICLR 2025 format, in P-DRAFT-1 | [analysis.md](analysis.md) sections 6–7; [stages/05](stages/05-drafting-peer-review.md) | the six parameters A.2 leaves unset: N_seed, N_0, the full-set engineering limit, N_p, N_t, N_a (finding 1) |
| AutoSOTA comparison [App. B] | P-EVAL-1 (success by attribution), P-EVAL-3, P-EVAL-14, P-BENCH-4 (TeCh), P-INT-5 (the I1, I2 and I4 blocks), P-ART-5 (a critic that ends an idea), P-FULL-1 … 3 (the full benchmark grid) | [claims.md](claims.md); [stages/07](stages/07-integrity.md); [artifacts.md](artifacts.md); [stages/02](stages/02-evaluating-ideas.md) | the attribution rule under which an ablation rejection ends a task (finding 6) |
| Qualitative results [App. C] | P-ART-1 … 8, and the run layout P-ART-11 | [artifacts.md](artifacts.md) | none |
| DynaSpec-RAG [App. D] | P-ART-9 | [artifacts.md](artifacts.md) | none |

### 1.2 Tables 2–11 and 12–16

| Table | Elements that capture it | Defined in | Left without an element; the table's claims |
|---|---|---|---|
| Autonomous research agents [Tab. 2] | P-EVAL-4, P-EVAL-5, P-EVAL-6, P-EVAL-9, P-EVAL-14 | [claims.md](claims.md) | none; C-MAIN-1, C-MAIN-2 |
| Human-author papers [Tab. 3] | P-EVAL-1, P-EVAL-4, P-EVAL-5, P-EVAL-6, P-BENCH-4 | [claims.md](claims.md) | none; C-HEAD-1, C-HEAD-4, C-MAIN-4 to C-MAIN-7 |
| AutoSOTA gains [Tab. 4] | P-EVAL-2, P-EVAL-3, P-EVAL-14 | [claims.md](claims.md) | none; C-HEAD-2, C-MAIN-8 |
| Review rounds [Tab. 5] | P-EVAL-8; it corroborates P-CFG-10 | [claims.md](claims.md); [analysis.md](analysis.md) section 6 | none; C-ABLX-3 to C-ABLX-5 |
| Review-driven refinement [Tab. 6] | the one example under P-META-1 … 7; it corroborates P-CFG-11 | [stages/06](stages/06-meta-review.md); [analysis.md](analysis.md) section 6 | none; C-ABLX-6 |
| Integrity audit [Tab. 7] | P-INT-5, P-EVAL-10; its header's refinement agents are P-ROSTER-26 … 28 | [stages/07](stages/07-integrity.md); [claims.md](claims.md); [analysis.md](analysis.md) section 7 | none; C-ABLX-7 |
| Coding agents [Tab. 8] | P-EVAL-1, for its SR column | [claims.md](claims.md) | the coding backend itself (finding 5); C-ABLX-8 |
| Frontier expansion [Tab. 9] | P-EVAL-15; P-TOP-1, whose evidence on G includes the engine's own output | [claims.md](claims.md); [analysis.md](analysis.md) section 2.1 | chained runs (finding 7); C-DISC-4 |
| Human evaluation [Tab. 10] | P-EVAL-11 | [claims.md](claims.md) | none; C-DISC-5 |
| DynaSpec-RAG results [Tab. 11] | P-ART-9, whose own Table 1 this is | [artifacts.md](artifacts.md) | none; C-DISC-6 |
| NeurIPS 2025 papers [Tab. 12] | P-BENCH-1 | [claims.md](claims.md) | none; C-BENCH-1 |
| ICLR 2026 papers [Tab. 13] | P-BENCH-1 | [claims.md](claims.md) | none; C-BENCH-2 |
| ICML 2026 Spotlight papers [Tab. 14] | P-BENCH-1, P-BENCH-3 | [claims.md](claims.md) | none; C-BENCH-3 |
| Aggregate differences [Tab. 15] | P-EVAL-1, reading (c); P-INT-5, the protocol forbidden by audit; N_p's only count sits in a row of analysis.md section 6 with no ID | [claims.md](claims.md); [stages/07](stages/07-integrity.md); [analysis.md](analysis.md) section 6 | the attribution rule (finding 6); C-APPB-1 to C-APPB-4 |
| Paper by paper [Tab. 16] | P-EVAL-3, P-EVAL-14, P-BENCH-4 | [claims.md](claims.md) | none; C-APPB-5 to C-APPB-10 |

### 1.3 Floats outside the required list

- Figure 1 is covered by P-EVAL-1 and P-EVAL-12 [Fig. 1]; Figures 2 and 8 by P-ART-10 [Fig. 2] [Fig. 8]; Figure 9 by P-EVAL-13, and it corroborates P-CFG-6 [Fig. 9] (image); Figure 10 by P-COST-1, P-COST-3 and P-COST-4 [Fig. 10] (image); Figure 11 by P-ART-9 [Fig. 11] [ours].

### 1.4 Findings

Every required part has at least one element [ours]. Findings 1–7 are parts, or aspects of parts, that no element captures; findings 8 and 9 concern the elements themselves [ours].

1. **Six parameters have no element.** §3 introduces N_seed [§3.1], N_0 [§3.2], N_p [§3.4], N_t [§3.5] and N_a [§3, Eq. 1], and a full-set engineering loop with no limit [§3.2]; App. A.2 sets none of them [App. A.2]. analysis.md section 6 gives each a row but no P-CFG ID, so they reach task 2 only through their gaps, U-SEED-1, A-EVO-1, A-FULL-2, U-ABL-1 and U-PEER-1, and N_a through none [ours].
   - claims.md does give IDs to definitions the paper leaves open (P-EVAL-2, P-BENCH-2 … 4, P-COST-1 … 3), so the two documents apply the ID rule differently [ours].
   - An element for each would hold its symbol, where §3 introduces it, and the fact that A.2 leaves it unset [ours].
2. **The state has no elements.** analysis.md section 8 lists 28 rows of state, from G and H_0 to h_best, E_best, C_best, P_new and R_new, with no IDs [§3.2] [§3.3] [§3.5]. Each becomes a schema in task 3, and each can now be traced only through the steps that produce and read it [ours].
3. **Figure 3's grouping has no elements.** Six boxes group the agents [Fig. 3] (image), and analysis.md section 7.1 lists them without IDs. Task 3 needs elements for them only if its components follow the paper's grouping [ours].
4. **External systems have no elements of their own.** analysis.md section 7.2 lists seven [§3.5] [§4.2] [App. A.2]. ScholarPeer is P-ROSTER-21; PaperOrchestra sits inside P-ROSTER-20 and Google Search inside P-CFG-2; the Stanford Agentic Reviewer and the CoE audit are measurements, P-EVAL-6 and P-EVAL-10; the coding backend, Claude Code or Antigravity, appears only in the roster's model column [ours]. Each is an external dependency that our rules put behind an interface with a mock [ours].
5. **Table 8 tests a part with no element: the coding backend.** The paper swaps Claude Code for "Antigravity powered by Gemini 3.8 Flash" on 5 ICLR 2026 tasks [§4.2] [Tab. 8]; among the IDs, only the gap A-CFG-2 and the claim C-ABLX-8 concern it. An element would hold the backend's role (the agents App. A.2 routes to Claude Code), the swap, and what the swap leaves unchanged [ours].
6. **App. B's attribution rule has no element.** Table 15 says the engine "additionally requires the gain to be attributable to the proposed mechanism in ablation" [Tab. 15], and TeCh's variant "was not accepted as a contribution" once the ablation critic rejected it [App. B]. §3.4 has no such verdict [§3.4], so the rule exists only as gaps (A-ABL-1, A-ART-4, A-EVAL-1) and as reading (c) of P-EVAL-1 [ours]. An element would hold the rule, the agent that applies it, and what a rejected task outputs [ours].
7. **Table 9's chained runs have no element.** A run's own method is "provided as context in the next discovery cycle" [§4.3] [Tab. 9]; analysis.md section 2.1 records this as evidence on G under P-TOP-1, but nothing says which parts of one run's output enter the next run's G [ours].
8. **Two IDs name one element.** P-LIM-4 and P-CFG-1 are both the 16 limitation rounds, and P-SUB-4 and P-CFG-3 are both N_eng = 2 [§3.1] [§3.2] [App. A.2]. Task 2 should map each pair to one requirement, or record why it keeps two [ours].
   - P-CODER-1 (the interface, Eq. 2) and P-ROSTER-13 (the composite agent) name one thing from two sides, as do the integrity mechanisms P-INT-2 … 4 and their agents P-ROSTER-26 … 28 [§3.2, Eq. 2] [§4.2]. That split, requirement against component, is useful, but it should be deliberate [ours].
   - P-EVO-5 and P-META-7 state stopping rules whose values P-CFG-6, P-CFG-7 and P-CFG-11 set: an overlap by design, not a duplicate [§3.3] [§3.6] [ours].
9. **analysis.md disagrees with itself on what A_Coder contains.** Its roster row for A_Coder, P-ROSTER-13, calls it the composite of rows 6–11, which takes in the Baseline Coder (row 6) and leaves out the Full-Set Engineer (row 12) [ours].
   - §3.2 abstracts "this entire idea experiment pipeline" into A_Coder, and that pipeline ends with "A Full-Set Critic Agent and Full-Set Engineer" [§3.2] (tex:sections/3_new_method.tex:52) (tex:sections/3_new_method.tex:55).
   - analysis.md's own pseudocode runs the baseline once, outside A_Coder, which is reading 1 of A-BASE-1 [§3.2] [ours].
   - The owner of analysis.md should settle the membership, since task 3's contract for A_Coder depends on it [ours].

## Part 2: element → requirement → component

- **One row per P- ID** defined anywhere in this folder, grouped by the document that defines it. The ID stands alone in its cell and appears nowhere else in this part, so a search for it finds one line here [ours].
- **Element:** a few words; the defining document holds the full entry and its quotes [ours].
- **Location:** where the paper states the element; for an artifact, its actual PDF page [ours].
- **Class:** the mark the defining document gives the element [ours].
  - `SPECIFIED (quoted)`, or `SPECIFIED (Eq. n)`: the defining document states the step by quoting the paper, or by its equation or formula, and gives it no mark of its own; a quoted statement is what the README calls SPECIFIED [ours].
  - For an agent (key ROSTER), SPECIFIED means the paper names the agent; its model follows when App. A.2 does not assign it plainly [ours].
  - After a semicolon: an aspect the defining document leaves open, with its gap [ours].
  - For the artifacts (key ART), the class is artifacts.md's basis for attributing the page to an agent, since a page is evidence, not a mechanism [ours].
- **Gaps:** the related U- and A- IDs, whose full entries sit under "Gaps found here" in the documents that define them; `none` where none is named [ours].
- **Requirement** and **Component** read `— (task 2)` and `— (task 3)` until those tasks fill them; task 2 may instead record a decision to leave the element out [ours].

### 2.1 Problem, stage primitive and control flow: [analysis.md](analysis.md) sections 2–4

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-TOP-1 | the problem setup: (P+, C+) = A(G) over N_a agents; what P+ and C+ must do; what G is | [§3, Eq. 1] | SPECIFIED for the experiments; AMBIGUOUS in general (A-TOP-4); contents UNSPECIFIED (U-TOP-1) | A-TOP-4, U-TOP-1 | — (task 2) | — (task 3) |
| P-TOP-2 | the stage primitive: candidate, critic, refine, max_rounds; accept returns, reject and exhaustion discard | [Lst. 1] | SPECIFIED (verbatim); INCONSISTENT with §3.4–§3.6 at exhaustion (A-TOP-1); count AMBIGUOUS (A-TOP-2) | A-TOP-1, A-TOP-2 | — (task 2) | — (task 3) |
| P-TOP-3 | Table 1's eleven stages, each set against Listing 1 | [Tab. 1] | SPECIFIED; an exact fit to Listing 1 only for the subset experiment | A-TOP-1, A-TOP-2, and each row's own in analysis.md section 3.2 | — (task 2) | — (task 3) |
| P-TOP-4 | the end-to-end control flow from G to (P+, C+), reconstructed as pseudocode | [§3] [§3.6] | a reconstruction: each line SPECIFIED or [inferred], one reading taken per gap; the loop until approval INCONSISTENT (A-TOP-3) | A-TOP-3, U-TOP-2, U-TOP-3, U-TOP-4 | — (task 2) | — (task 3) |
| P-TOP-5 | the run's termination branches: accept, meta limit, refinement not superior, no success, ablation rejection, rule violation, error | [§3.3] [§3.6] [§4.2] | four branches SPECIFIED, the meta limit [inferred]; ablation rejection INCONSISTENT (A-ABL-1); errors UNSPECIFIED (U-TOP-2) | A-ABL-1, U-TOP-2, U-EVO-4 | — (task 2) | — (task 3) |

### 2.2 Seed ideas: [stages/01](stages/01-seed-ideas.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-LIM-1 | Limitation Extractor: G → a set of limitations | [§3.1] | SPECIFIED (quoted) | U-LIM-1 | — (task 2) | — (task 3) |
| P-LIM-2 | Limitation Verifier: is the set sufficient to guide improvement? | [§3.1] | SPECIFIED (quoted); its criterion UNSPECIFIED (U-LIM-1) | U-LIM-1 | — (task 2) | — (task 3) |
| P-LIM-3 | insufficient → the Extractor adds what is missing | [§3.1] | SPECIFIED (quoted) | U-LIM-1 | — (task 2) | — (task 3) |
| P-LIM-4 | the limitation loop's limit: 16 rounds, no symbol | [§3.1] [App. A.2] | SPECIFIED value; exhaustion AMBIGUOUS (A-LIM-1); count AMBIGUOUS (A-TOP-2) | A-LIM-1, A-TOP-2 | — (task 2) | — (task 3) |
| P-SEED-1 | initial idea generation: the limitations → h_0 | [§3.1] [Fig. 4] (image) | SPECIFIED (quoted); its agent AMBIGUOUS (A-SEED-2) | A-SEED-2 | — (task 2) | — (task 3) |
| P-SEED-2 | Novelty Checker: h_0 and two retrieved papers → a novelty score | [§3.1] [App. A.2] | SPECIFIED (quoted); the score UNSPECIFIED (U-SEED-2) | U-SEED-2 | — (task 2) | — (task 3) |
| P-SEED-3 | Idea Generator Agent adds scored ideas until the pool holds N_seed | [§3.1] | SPECIFIED (quoted); N_seed UNSPECIFIED (U-SEED-1); filter or ranking AMBIGUOUS (A-SEED-1) | U-SEED-1, A-SEED-1, U-SEED-3 | — (task 2) | — (task 3) |
| P-SEED-4 | the pool H_0 sorted by novelty score, descending | [§3.1] | SPECIFIED (quoted) | A-SEED-1 | — (task 2) | — (task 3) |

### 2.3 Evaluating ideas: [stages/02](stages/02-evaluating-ideas.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-BASE-1 | Baseline Coding Agent: G on the subset → E_base, C_base | [§3.2] | SPECIFIED (quoted); placement AMBIGUOUS (A-BASE-1); the subset UNSPECIFIED (U-BASE-1) | A-BASE-1, U-BASE-1, U-BASE-2, A-CFG-1 | — (task 2) | — (task 3) |
| P-SUB-1 | Subset Coding Agent implements h by modifying C_base → E_sub^h, C_sub^h | [§3.2] | SPECIFIED (quoted) | U-BASE-1 | — (task 2) | — (task 3) |
| P-SUB-2 | Subset Critic: E_sub^h against E_base → Bad, Good or Engineer, with feedback r^h | [§3.2] | SPECIFIED (quoted); its criteria UNSPECIFIED (U-SUB-1) | U-SUB-1 | — (task 2) | — (task 3) |
| P-SUB-3 | Engineer → the Subset Engineering Agent refines h and C_sub^h | [§3.2] | SPECIFIED (quoted); its model AMBIGUOUS (A-CFG-1) | A-CFG-1 | — (task 2) | — (task 3) |
| P-SUB-4 | the subset loop's limit N_eng = 2; at the limit, Bad and pruned | [§3.2] [App. A.2] | SPECIFIED value; count AMBIGUOUS (A-TOP-2) | A-TOP-2 | — (task 2) | — (task 3) |
| P-FULL-1 | Full-Set Coding Agent adapts C_sub^h to the whole benchmark suite | [§3.2] | SPECIFIED (quoted) | U-ART-4, U-BENCH-1 | — (task 2) | — (task 3) |
| P-FULL-2 | Full-Set Critic and Engineer validate and engineer on the full benchmark | [§3.2] [Fig. 5] (image) | SPECIFIED (quoted); reference AMBIGUOUS (A-FULL-1); limit AMBIGUOUS (A-FULL-2); verdicts UNSPECIFIED (U-FULL-1) | A-FULL-1, A-FULL-2, U-FULL-1 | — (task 2) | — (task 3) |
| P-FULL-3 | the terminal decision d^h | [§3.2] [Fig. 5] (image) | SPECIFIED (quoted); its vocabulary only in Figure 5 (U-FULL-1) | U-FULL-1 | — (task 2) | — (task 3) |
| P-CODER-1 | the unified coder A_Coder(G, h) → h, E^h, C^h, d^h, r^h | [§3.2, Eq. 2] | SPECIFIED (Eq. 2); baseline inputs AMBIGUOUS (A-BASE-1); a pruned idea's return UNSPECIFIED (U-CODER-1) | A-BASE-1, U-CODER-1 | — (task 2) | — (task 3) |

### 2.4 Refining ideas: [stages/03](stages/03-refining-ideas.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-EVO-1 | round 0: the top-N_0 seeds → A_Coder → R_0 | [§3.3] | SPECIFIED (quoted); INCONSISTENT with App. A.2's rounds (A-EVO-1) | A-EVO-1 | — (task 2) | — (task 3) |
| P-EVO-2 | round k ≥ 1: A_Evolve reads all earlier traces → N_k evolved ideas | [§3.3] | SPECIFIED (quoted); what it reads UNSPECIFIED (U-EVO-2) | U-EVO-2 | — (task 2) | — (task 3) |
| P-EVO-3 | exploration: the next N_e unevaluated seeds join the evolved ideas | [§3.3] | SPECIFIED (quoted); running out of seeds UNSPECIFIED (U-EVO-3) | U-EVO-3 | — (task 2) | — (task 3) |
| P-EVO-4 | each candidate of round k → A_Coder → R_k | [§3.3, Eq. 3] | SPECIFIED (Eq. 3); parallelism UNSPECIFIED (U-TOP-4) | U-TOP-4 | — (task 2) | — (task 3) |
| P-EVO-5 | the stop test: S successes over all rounds so far, or round K | [§3.3] | SPECIFIED (the formula); when it runs UNSPECIFIED (U-EVO-1); K AMBIGUOUS (A-EVO-2) | U-EVO-1, A-EVO-2 | — (task 2) | — (task 3) |
| P-EVO-6 | zero successes at round K → the whole run ends | [§3.3] | SPECIFIED (quoted); what it leaves UNSPECIFIED (U-EVO-4) | U-EVO-4 | — (task 2) | — (task 3) |
| P-SEL-1 | Selector: every Good idea with its results and code → h_best, E_best, C_best | [§3.3, Eq. 4] | SPECIFIED (Eq. 4); its criterion UNSPECIFIED (U-SEL-1) | U-SEL-1 | — (task 2) | — (task 3) |

### 2.5 Ablation: [stages/04](stages/04-ablation.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-ABL-1 | Ablation Planner: h_best → N_p executable plans | [§3.4] | SPECIFIED (quoted); N_p UNSPECIFIED (U-ABL-1) | U-ABL-1 | — (task 2) | — (task 3) |
| P-ABL-2 | Ablation Coding Agent runs each plan on C_best → E_abl | [§3.4] | SPECIFIED (quoted); whether its code stays UNSPECIFIED (U-ABL-3) | U-ABL-3 | — (task 2) | — (task 3) |
| P-ABL-3 | Ablation Critic: E_abl → Good or Refine, with critique r_abl | [§3.4] | SPECIFIED (quoted); a reject verdict INCONSISTENT (A-ABL-1) | A-ABL-1 | — (task 2) | — (task 3) |
| P-ABL-4 | Refine → A_FullEng, guided by r_abl → h_new, E_new, C_new | [§3.4] | SPECIFIED (quoted); its validation UNSPECIFIED (U-ABL-2); its model AMBIGUOUS (A-CFG-1) | U-ABL-2, A-CFG-1 | — (task 2) | — (task 3) |
| P-ABL-5 | Result Comparison: the core state is replaced only if E_new is preferred | [§3.4] | SPECIFIED (quoted); criterion AMBIGUOUS (A-ABL-3); the failed branch INCONSISTENT (A-ABL-2) | A-ABL-3, A-ABL-2 | — (task 2) | — (task 3) |
| P-ABL-6 | after an update, ablation planning runs again on the new h_best | [§3.4] | SPECIFIED (quoted); a second Refine UNSPECIFIED (U-ABL-4) | U-ABL-4 | — (task 2) | — (task 3) |

### 2.6 Drafting and the review–rebuttal loop: [stages/05](stages/05-drafting-peer-review.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-DRAFT-1 | Initial Drafter with PaperOrchestra: h_best, E_best, E_abl → P_new, in the ICLR 2025 format | [§3.5] [App. A.2] | SPECIFIED (quoted); other inputs UNSPECIFIED (U-DRAFT-1); failures UNSPECIFIED (U-DRAFT-2) | U-DRAFT-1, U-DRAFT-2, A-INT-2 | — (task 2) | — (task 3) |
| P-PEER-1 | ScholarPeer reviews P_new → R_new with a score in [1, 10] | [§3.5] | SPECIFIED (quoted); its configuration UNSPECIFIED (U-PEER-3) | U-PEER-3 | — (task 2) | — (task 3) |
| P-PEER-2 | a score below the threshold of 8 starts the rebuttal | [§3.5] [App. A.2] | SPECIFIED (quoted) | A-EVAL-3 | — (task 2) | — (task 3) |
| P-PEER-3 | Rebuttal Planner: R_new → N_t supplementary tasks | [§3.5] | SPECIFIED (quoted); N_t UNSPECIFIED (U-PEER-1) | U-PEER-1, A-CFG-1 | — (task 2) | — (task 3) |
| P-PEER-4 | Rebuttal Coding Agent runs each task on C_best → E_reb | [§3.5] | SPECIFIED (quoted); whether its code stays UNSPECIFIED (U-PEER-2) | U-PEER-2, U-ART-15 | — (task 2) | — (task 3) |
| P-PEER-5 | Paper Enhancer: P_new, R_new, E_reb → a revised P_new | [§3.5] | SPECIFIED (quoted); its scope UNSPECIFIED (U-PEER-4) | U-PEER-4 | — (task 2) | — (task 3) |
| P-PEER-6 | the revised manuscript is reviewed again, replacing R_new and the score | [§3.5] | SPECIFIED (quoted); what N_peer counts AMBIGUOUS (A-PEER-1) | A-PEER-1, A-TOP-5 | — (task 2) | — (task 3) |

### 2.7 Meta-review: [stages/06](stages/06-meta-review.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-META-1 | Meta-Review Agent: P_new and R_new → Accept or Refine, with r_meta | [§3.6] | SPECIFIED (quoted); its criterion UNSPECIFIED (U-META-2) | U-META-2 | — (task 2) | — (task 3) |
| P-META-2 | Accept → export P+ ← P_new and C+ ← C_best | [§3.6] | SPECIFIED (quoted) | none | — (task 2) | — (task 3) |
| P-META-3 | Refine → A_FullEng, guided by r_meta → h_new, E_new, C_new | [§3.6] | SPECIFIED (quoted); its model AMBIGUOUS (A-CFG-1) | A-CFG-1, U-ABL-2 | — (task 2) | — (task 3) |
| P-META-4 | Result Comparison: E_new against E_best | [§3.6] | SPECIFIED (quoted); criterion AMBIGUOUS (A-ABL-3) | A-ABL-3, A-TOP-5 | — (task 2) | — (task 3) |
| P-META-5 | strictly superior → a new core state; ablation, drafting and review run again | [§3.6] | SPECIFIED (quoted); the restart's extent AMBIGUOUS (A-META-1); budgets UNSPECIFIED (U-META-1) | A-META-1, U-META-1 | — (task 2) | — (task 3) |
| P-META-6 | otherwise the refinement is discarded and the previous outputs are exported | [§3.6] | SPECIFIED (quoted); INCONSISTENT with the loop until approval (A-TOP-3) | A-TOP-3 | — (task 2) | — (task 3) |
| P-META-7 | the meta loop repeats up to N_meta times, or until Accept | [§3.6] [App. A.2] | SPECIFIED (quoted); a second verdict AMBIGUOUS (A-META-2) | A-META-2, A-TOP-1 | — (task 2) | — (task 3) |

### 2.8 Integrity mechanisms: [stages/07](stages/07-integrity.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-INT-1 | score verification: the Coding Agent is prompted to write reproducible scripts | [§4.2] | SPECIFIED (quoted); prompt or gate INCONSISTENT with App. B (A-INT-1) | A-INT-1 | — (task 2) | — (task 3) |
| P-INT-2 | specification filter: rule-violating solutions are discarded after experimentation | [§4.2] | SPECIFIED (quoted); hook points UNSPECIFIED (U-INT-1); task rules UNSPECIFIED (U-INT-2); which agent AMBIGUOUS (A-INT-3) | U-INT-1, U-INT-2, A-INT-3 | — (task 2) | — (task 3) |
| P-INT-3 | reference verification: a search-augmented LLM flags citations, the Writer Agent corrects them | [§4.2] | SPECIFIED (quoted); which writer AMBIGUOUS (A-INT-2); when UNSPECIFIED (U-INT-3) | A-INT-2, U-INT-3 | — (task 2) | — (task 3) |
| P-INT-4 | method–code alignment: an audit report, then the Writer Agent corrects the method section | [§4.2] | SPECIFIED (quoted); which agents AMBIGUOUS (A-INT-2, A-INT-3); when UNSPECIFIED (U-INT-3) | A-INT-2, A-INT-3, U-INT-3 | — (task 2) | — (task 3) |
| P-INT-5 | the effect: without these agents, sporadic audit failures, and one task filtered | [§4.2] [fn. 2] [Tab. 7] | SPECIFIED (quoted); App. B's account INCONSISTENT (A-INT-1) | A-INT-1, U-EVAL-5 | — (task 2) | — (task 3) |

### 2.9 Loop limits: [analysis.md](analysis.md) section 6

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-CFG-1 | limitation rounds: 16, no symbol | [§3.1] [App. A.2] | SPECIFIED value; count AMBIGUOUS (A-TOP-2); exhaustion AMBIGUOUS (A-LIM-1) | A-TOP-2, A-LIM-1 | — (task 2) | — (task 3) |
| P-CFG-2 | novelty references per idea: 2, from Google Search | [App. A.2] | SPECIFIED value; score and retrieval UNSPECIFIED (U-SEED-2) | U-SEED-2 | — (task 2) | — (task 3) |
| P-CFG-3 | N_eng, the subset engineering budget: 2 | [§3.2] [App. A.2] | SPECIFIED value; count AMBIGUOUS (A-TOP-2) | A-TOP-2 | — (task 2) | — (task 3) |
| P-CFG-4 | N_k, evolved ideas per round k ≥ 1: 1 | [§3.3] [App. A.2] | SPECIFIED value | none | — (task 2) | — (task 3) |
| P-CFG-5 | N_e, unevaluated seeds per round k ≥ 1: 1 | [§3.3] [App. A.2] | SPECIFIED value | U-EVO-3 | — (task 2) | — (task 3) |
| P-CFG-6 | K, refinement rounds: 4 | [§3.3] [App. A.2] [Fig. 9] (image) | SPECIFIED value; whether round 0 counts AMBIGUOUS (A-EVO-2) | A-EVO-2 | — (task 2) | — (task 3) |
| P-CFG-7 | S, successes that stop the rounds: 4 | [§3.3] [App. A.2] | SPECIFIED value; when it is checked UNSPECIFIED (U-EVO-1) | U-EVO-1 | — (task 2) | — (task 3) |
| P-CFG-8 | N_abl, ablation refinements: 1 | [§3.4] [App. A.2] | SPECIFIED value; count AMBIGUOUS (A-TOP-2) | A-ABL-2, U-ABL-4, A-TOP-2 | — (task 2) | — (task 3) |
| P-CFG-9 | the review-score threshold: 8 | [§3.5] [App. A.2] | SPECIFIED: App. A.2 fixes §3.5's example value | A-EVAL-3 | — (task 2) | — (task 3) |
| P-CFG-10 | N_peer, the review–rebuttal budget: 2 | [§3.5] [App. A.2] [Tab. 5] | SPECIFIED value; its unit AMBIGUOUS (A-PEER-1) | A-PEER-1, A-TOP-2 | — (task 2) | — (task 3) |
| P-CFG-11 | N_meta, meta-review refinements: 1 | [§3.6] [App. A.2] [Tab. 6] | SPECIFIED value; a second meta-review AMBIGUOUS (A-META-2) | A-META-2, U-META-1, A-TOP-2 | — (task 2) | — (task 3) |

### 2.10 Agent roster: [analysis.md](analysis.md) section 7

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-ROSTER-1 | Limitation Extractor, on Gemini 3.6 Flash | [§3.1] [App. A.2] | SPECIFIED | U-LIM-1 | — (task 2) | — (task 3) |
| P-ROSTER-2 | Limitation Verifier, on Gemini; absent from Figure 3 | [§3.1] [App. A.2] | SPECIFIED | U-LIM-1, A-LIM-1 | — (task 2) | — (task 3) |
| P-ROSTER-3 | Initial Idea Generator, named only in Figure 4 | [§3.1] [Fig. 4] (image) | AMBIGUOUS: one agent with the Idea Generator, or two (A-SEED-2) | A-SEED-2 | — (task 2) | — (task 3) |
| P-ROSTER-4 | Novelty Checker, on Gemini with Google Search | [§3.1] [App. A.2] | SPECIFIED; its score UNSPECIFIED (U-SEED-2) | U-SEED-2 | — (task 2) | — (task 3) |
| P-ROSTER-5 | Idea Generator Agent, on Gemini | [§3.1] [App. A.2] | SPECIFIED; its name AMBIGUOUS (A-ROSTER-1) | A-ROSTER-1, U-SEED-3 | — (task 2) | — (task 3) |
| P-ROSTER-6 | Baseline Coder, the Baseline Coding Agent | [§3.2] [Fig. 5] (image) | SPECIFIED; its model AMBIGUOUS (A-CFG-1) | A-CFG-1, A-BASE-1 | — (task 2) | — (task 3) |
| P-ROSTER-7 | Subset Coder, on Claude Code as part of the Idea Experiment Coding Agent | [§3.2] [App. A.2] | SPECIFIED; its model [inferred] | A-CFG-1 | — (task 2) | — (task 3) |
| P-ROSTER-8 | Subset Critic, on Gemini; App. A.2's Idea Critic Agent | [§3.2] [App. A.2] | SPECIFIED; A.2's name for it [inferred] | U-SUB-1, A-FULL-2 | — (task 2) | — (task 3) |
| P-ROSTER-9 | Subset Engineer, the Subset Engineering Agent | [§3.2] [Fig. 5] (image) | SPECIFIED; its model AMBIGUOUS (A-CFG-1) | A-CFG-1 | — (task 2) | — (task 3) |
| P-ROSTER-10 | Full-Set Coder, on Claude Code | [§3.2] [App. A.2] | SPECIFIED; its model [inferred] | A-CFG-1 | — (task 2) | — (task 3) |
| P-ROSTER-11 | Full-Set Critic, on Gemini | [§3.2] [Tab. 1] | SPECIFIED; its reference AMBIGUOUS (A-FULL-1) | A-FULL-1, A-FULL-2, U-FULL-1 | — (task 2) | — (task 3) |
| P-ROSTER-12 | Full-Set Engineer, re-engaged as A_FullEng in §3.4 and §3.6 | [§3.2] [§3.4] [§3.6] | SPECIFIED; its model AMBIGUOUS (A-CFG-1) | A-CFG-1, U-ABL-2, A-ROSTER-1 | — (task 2) | — (task 3) |
| P-ROSTER-13 | Idea Implementer A_Coder, the composite of the §3.2 agents (finding 9) | [§3.2, Eq. 2] [Fig. 6] (image) | SPECIFIED | A-BASE-1, U-CODER-1 | — (task 2) | — (task 3) |
| P-ROSTER-14 | Idea Evolver A_Evolve, on Gemini | [§3.3] [App. A.2] | SPECIFIED | U-EVO-2 | — (task 2) | — (task 3) |
| P-ROSTER-15 | Selector A_Selector, on Gemini | [§3.3, Eq. 4] [App. A.2] | SPECIFIED; its criterion UNSPECIFIED (U-SEL-1) | U-SEL-1 | — (task 2) | — (task 3) |
| P-ROSTER-16 | Ablation Planner, the Planning Agent of Figure 3 | [§3.4] [Fig. 3] (image) | SPECIFIED; its model [inferred] | A-CFG-1, U-ABL-1 | — (task 2) | — (task 3) |
| P-ROSTER-17 | Ablation Coder, on Claude Code as the Ablation Study Agent | [§3.4] [App. A.2] | SPECIFIED | U-ABL-3 | — (task 2) | — (task 3) |
| P-ROSTER-18 | Ablation Critic A_AblCritic, also written A_AblCrit, on Gemini | [§3.4] [App. A.2] | SPECIFIED; its model [inferred]; a reject INCONSISTENT (A-ABL-1) | A-ABL-1, A-TOP-5 | — (task 2) | — (task 3) |
| P-ROSTER-19 | Result Comparison Agent, on Gemini | [§3.4] [§3.6] | SPECIFIED; its criterion AMBIGUOUS (A-ABL-3) | A-ABL-3 | — (task 2) | — (task 3) |
| P-ROSTER-20 | Initial Drafter A_Draft, incorporating PaperOrchestra | [§3.5] [Bib: song2026paperorchestra] | SPECIFIED; its model [inferred] | U-DRAFT-1, U-DRAFT-2 | — (task 2) | — (task 3) |
| P-ROSTER-21 | Peer Reviewer A_Reviewer, which is ScholarPeer | [§3.5] [Bib: goyal2026scholarpeer] | SPECIFIED; its backbone UNSPECIFIED (U-PEER-3) | U-PEER-3, A-ROSTER-1 | — (task 2) | — (task 3) |
| P-ROSTER-22 | Rebuttal Planner A_RebPlan | [§3.5] | SPECIFIED; its model AMBIGUOUS (A-CFG-1) | A-CFG-1, U-PEER-1 | — (task 2) | — (task 3) |
| P-ROSTER-23 | Rebuttal Coder A_RebCoder, on Claude Code as the Rebuttal Agent | [§3.5] [App. A.2] | SPECIFIED | U-PEER-2 | — (task 2) | — (task 3) |
| P-ROSTER-24 | Paper Enhancer A_Enhancer, the Draft Enhancer, on Claude Code | [§3.5] [App. A.2] | SPECIFIED | U-PEER-4 | — (task 2) | — (task 3) |
| P-ROSTER-25 | Meta-Reviewer A_Meta, on Gemini | [§3.6] [App. A.2] | SPECIFIED | U-META-2 | — (task 2) | — (task 3) |
| P-ROSTER-26 | specification filter, the Coding Agent used as a filter | [§4.2] [Tab. 7] | SPECIFIED; its model [inferred]; which session AMBIGUOUS (A-INT-3) | A-INT-3, U-INT-1 | — (task 2) | — (task 3) |
| P-ROSTER-27 | reference checker, a search-augmented LLM | [§4.2] | SPECIFIED; its model not stated | A-INT-2, U-INT-3 | — (task 2) | — (task 3) |
| P-ROSTER-28 | method–code auditor, the Coding Agent | [§4.2] | SPECIFIED; its model [inferred]; which session AMBIGUOUS (A-INT-3) | A-INT-3, U-INT-3 | — (task 2) | — (task 3) |

### 2.11 Artifacts of Appendices C and D: [artifacts.md](artifacts.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-ART-1 | limitations of X-Mahalanobis: five, each a flaw, why it limits, an opportunity | [pp. 34–35] | producer [inferred] from content | U-ART-2 | — (task 2) | — (task 3) |
| P-ART-2 | the idea Procrustes-DS: components tagged by limitation, with PyTorch code | [pp. 36–39] | producer [inferred] from content | U-ART-3 | — (task 2) | — (task 3) |
| P-ART-3 | the experimental evaluation report of the refined idea | [pp. 40–42] | producer [inferred]; which critic led to it AMBIGUOUS (A-ART-1) | A-ART-1, A-ART-5, U-ART-4, U-ART-11, U-ART-16, U-ART-20 | — (task 2) | — (task 3) |
| P-ART-4 | the ablation study report: one plan, eight variants | [pp. 43–45] | producer [inferred] | U-ART-5, U-ART-13 | — (task 2) | — (task 3) |
| P-ART-5 | the critic's feedback: five component flaws, no verdict printed | [p. 46] | producer [inferred]; which critic AMBIGUOUS (A-ART-1) | A-ART-1, A-ART-4 | — (task 2) | — (task 3) |
| P-ART-6 | the reproducibility audit: one re-run, one boolean | [p. 47] | producer AMBIGUOUS (A-ART-2); its scope INCONSISTENT with Table 7 (A-ART-3) | A-ART-2, A-ART-3, U-ART-6, U-ART-7 | — (task 2) | — (task 3) |
| P-ART-7 | the specification and alignment audit: two booleans with evidence | [pp. 48–50] | producer AMBIGUOUS (A-ART-2) | A-ART-2, U-ART-7, U-ART-8, U-ART-9 | — (task 2) | — (task 3) |
| P-ART-8 | the rebuttal report for TABHARMONY | [pp. 51–55] | producer [inferred] | U-ART-14, U-ART-15 | — (task 2) | — (task 3) |
| P-ART-9 | the final paper, DynaSpec-RAG: 16 pages in the ICLR 2025 template | [pp. 56–71] [App. D] | the paper's own statement; who wrote which part UNSPECIFIED (U-ART-19) | A-ART-7, A-ART-8, A-ART-9, A-ART-10, U-ART-12, U-ART-18, U-ART-19 | — (task 2) | — (task 3) |
| P-ART-10 | the generated-paper pages inside Figures 2 and 8 | [Fig. 2] [Fig. 8] [p. 3] [p. 11] | producer [inferred] | U-ART-12 | — (task 2) | — (task 3) |
| P-ART-11 | one task's run layout, commands and environments | [pp. 40–55] | [ours], derived from the pages | U-ART-17, U-ART-15 | — (task 2) | — (task 3) |

### 2.12 Measurement, benchmark and cost: [claims.md](claims.md)

| ID | Element | Location | Class | Gaps | Requirement | Component |
|---|---|---|---|---|---|---|
| P-EVAL-1 | task success | [Fig. 1] [Tab. 3] [Tab. 15] | AMBIGUOUS (A-EVAL-1) | A-EVAL-1, A-ABL-1 | — (task 2) | — (task 3) |
| P-EVAL-2 | the relative gain of one paper | [§4.1] | UNSPECIFIED (U-EVAL-1); its baseline AMBIGUOUS (A-EVAL-2) | U-EVAL-1, A-EVAL-2 | — (task 2) | — (task 3) |
| P-EVAL-3 | the gain across papers: mean and median over the successes | [Tab. 4] | SPECIFIED in part | U-EVAL-1 | — (task 2) | — (task 3) |
| P-EVAL-4 | the average rating | [Tab. 3] [§3.5] | AMBIGUOUS (A-EVAL-4); reviewer set-up UNSPECIFIED (U-EVAL-2) | A-EVAL-4, U-EVAL-2 | — (task 2) | — (task 3) |
| P-EVAL-5 | ScholarPeer acceptance | [Tab. 3] [§3.5] | INCONSISTENT (A-EVAL-3) | A-EVAL-3 | — (task 2) | — (task 3) |
| P-EVAL-6 | the Stanford Agentic Reviewer's rating and acceptance | [§4] [fn. 1] | UNSPECIFIED (U-EVAL-3) | U-EVAL-3 | — (task 2) | — (task 3) |
| P-EVAL-7 | which reviewer is in the loop: ScholarPeer, with the other held out | [§4] | SPECIFIED | U-EVAL-2 | — (task 2) | — (task 3) |
| P-EVAL-8 | the review rounds of Table 5 | [Tab. 5] | AMBIGUOUS (A-EVAL-5) | A-EVAL-5, A-PEER-1 | — (task 2) | — (task 3) |
| P-EVAL-9 | runs, seeds and variance | [Tab. 2] [§4] | UNSPECIFIED (U-EVAL-4) | U-EVAL-4, U-ART-12 | — (task 2) | — (task 3) |
| P-EVAL-10 | the CoE integrity audit as a measurement | [§4.2] [Tab. 7] | checks SPECIFIED; auditor UNSPECIFIED (U-EVAL-5) | U-EVAL-5, A-ART-2 | — (task 2) | — (task 3) |
| P-EVAL-11 | the human evaluation | [§4.3] [Tab. 10] | protocol UNSPECIFIED (U-EVAL-6) | U-EVAL-6 | — (task 2) | — (task 3) |
| P-EVAL-12 | the radar of Figure 1a | [Fig. 1a] (image) | UNSPECIFIED (U-EVAL-7) | U-EVAL-7 | — (task 2) | — (task 3) |
| P-EVAL-13 | the per-round gain of Figure 9a | [Fig. 9a] (image) | UNSPECIFIED (U-EVAL-8); INCONSISTENT with Table 4 (A-EVAL-6) | U-EVAL-8, A-EVAL-6 | — (task 2) | — (task 3) |
| P-EVAL-14 | other systems' numbers | [Tab. 2] [Tab. 4] [Tab. 16] | SPECIFIED in part | U-EVAL-9, U-EVAL-10, A-EVAL-7 | — (task 2) | — (task 3) |
| P-EVAL-15 | the rating of Table 9 | [Tab. 9] | AMBIGUOUS (A-EVAL-8) | A-EVAL-8 | — (task 2) | — (task 3) |
| P-BENCH-1 | the 107 tasks: 38 NeurIPS 2025, 5 ICLR 2026, 64 ICML 2026 Spotlight | [App. A.1] [Tab. 12] [Tab. 13] [Tab. 14] | SPECIFIED | U-BENCH-1 | — (task 2) | — (task 3) |
| P-BENCH-2 | what a task gives the engine | [§4.1] | UNSPECIFIED (U-BENCH-1) | U-BENCH-1, U-TOP-1 | — (task 2) | — (task 3) |
| P-BENCH-3 | how the 64 ICML tasks were chosen | [App. A.1] | UNSPECIFIED (U-BENCH-2) | U-BENCH-2 | — (task 2) | — (task 3) |
| P-BENCH-4 | the 21 failed tasks | [Tab. 3] [Tab. 16] | UNSPECIFIED (U-BENCH-3) | U-BENCH-3 | — (task 2) | — (task 3) |
| P-COST-1 | the dollar cost, $3765 per task | [§4.3] [Fig. 10b] (image) | components UNSPECIFIED (U-COST-1) | U-COST-1 | — (task 2) | — (task 3) |
| P-COST-2 | which runs are costed: 33 NeurIPS tasks | [§4.3] | UNSPECIFIED (U-COST-2) | U-COST-2 | — (task 2) | — (task 3) |
| P-COST-3 | the time per task | [Fig. 10a] (image) | UNSPECIFIED (U-COST-3) | U-COST-3 | — (task 2) | — (task 3) |
| P-COST-4 | the stage breakdown of time and cost | [Fig. 10b] (image) | AMBIGUOUS (A-COST-1) | A-COST-1 | — (task 2) | — (task 3) |

## Part 3: acceptance targets, a shortlist

Candidates for the acceptance tests of our replication. A target is fair when the paper defines it, we can measure it at our scale in our locked harness, and it does not reward the reviewer the loop optimizes. Every judgment in this part is ours [ours].

| Candidate target | Source | Fair? | Why [ours] |
|---|---|---|---|
| Every loop limit and early stop holds as App. A.2 sets it: 16 limitation rounds, N_eng = 2, one seed and one evolved idea per round, K = 4, S = 4, N_abl = 1, a stop at score 8 within N_peer = 2, N_meta = 1 | P-CFG-1 … 11 [App. A.2] | Yes | deterministic, and testable at no cost with a mocked LLM that counts calls; the unit of four counts must be decided first (A-TOP-2, A-EVO-2, A-PEER-1, A-META-2) [ours] |
| A refinement replaces the core state only when the comparison prefers it; a failed meta refinement exports the previous outputs | P-ABL-5, P-META-5, P-META-6 [§3.4] [§3.6] | Yes | a control-flow rule, testable with fixture results; the comparison's own criterion stays open (A-ABL-3) [ours] |
| The ablation critic rejects a variant whose gain comes from generic training controls, as it did for DMC-TeCh | C-APPB-5, P-ART-5 [App. B] [Tab. 16] | As a planted fixture, yes; as a task outcome, no | a fixture ablation in which EMA and label smoothing carry the gain tests the critic's attribution reading; TeCh is one task, the paper prints no DMC-TeCh numbers, and §3.4 gives the critic no reject verdict (A-ABL-1) [ours] |
| The specification filter discards a reward-hacking solution, and an edit to the evaluator is blocked | P-INT-2 [§4.2] [fn. 2]; C-APPB-7 [Tab. 16] | Yes, as planted defects | footnote 2 records one real catch, and App. B's T-SAE change to how tokens are shown to the judge is a ready-made defect; a violation needs our own task rules first (U-INT-2) [ours] |
| Every exported run passes the four integrity checks; Table 7 reports 49/49 reproducible, 0/49 violations, 0 of 1814 references hallucinated, 49/49 aligned | C-ABLX-7 [Tab. 7] | As a gate on our exports, yes; as counts to match, no | the auditor is unnamed (U-EVAL-5) and may be the kind of agent that fixed the paper, so 49/49 can be in-distribution; our audit runs in the locked harness under a judge that is not the fixer, and may score lower [ours] |
| Without the refinement agents the checks fail on some papers: 1/50 violations, 19/1840 hallucinated references, 39/50 aligned | C-ABLX-7 [Tab. 7] | Yes, as a sensitivity check | it shows that the checks can fail; the direction is the target, not the counts [ours] |
| Re-executing the code reproduces the reported scores | P-ART-6 [p. 47] | Yes, made stricter | the page re-ran one scoring script, for the proposed method only, with no tolerance (A-ART-3, U-ART-6); ours re-runs method and baseline under a declared tolerance [ours] |
| The review loop raises the in-loop score: ScholarPeer 5.2 to 7.6, acceptance 46.9% to 93.9% | C-ABLX-3 [Tab. 5] | No | ScholarPeer is the reviewer the loop optimizes, as the paper itself says [§4 "Common Setup"]; the judge we report is never the reviewer we optimize against [ours] |
| Held-out acceptance: the Stanford Agentic Reviewer accepts 72.1% of the papers, and 0% for every baseline | C-MAIN-2 [Tab. 2] | As a direction only | the paper's only held-out evidence, but its acceptance rule is unknown (U-EVAL-3), the service is versioned by its host, and the second review round already lowers it (C-ABLX-4) [ours] |
| Success on 86 of 107 tasks, 80.4% | C-HEAD-1 [Tab. 3] [Fig. 1] | No | success has three readings (A-EVAL-1); 107 tasks at about $3765 each is beyond a pilot; one run per task, so no interval [ours] |
| Mean relative gain 25.2%, median 7.7% | C-HEAD-2 [Tab. 4] | No | parsed by Gemini from the generated papers under no stated rule (U-EVAL-1), and a success-only mean pulled up by a few outliers; ours is a gain the harness computes under a rule fixed in advance, reported as median and failure-inclusive mean [ours] |
| Idea evolution raises the best gain after round 0, most in round 1: 20.6%, 30.8%, then 33.4% at round 4 | C-ABLX-1 [Fig. 9a] (image) | Its shape only | the per-round gain is undefined (U-EVAL-8), and no control arm separates evolution from trying more ideas; a fair test sets evolved ideas against fresh seeds at the same budget [ours] |
| About $3765 and 2.5 days per task, with 45.4% of the cost in idea refinement | C-DISC-1, C-DISC-2, C-DISC-3 [§4.3] [Fig. 10] (image) | As a budget reference only | prices, machines and failed runs are not reported (U-COST-1, U-COST-2); our ledger records cost by stage, and the paper's split is a sanity check [ours] |
| A second coding backend still completes tasks: 3 of 5 with Antigravity | C-ABLX-8 [Tab. 8] | As a structural test, yes | the target is that the engine runs end to end through a second adapter; 3 of 5, with another Gemini version, is no number to match [ours] |
| Five or six ablations per paper | C-APPB-4 [Tab. 15] | As a default for N_p, not a target | it is the only count the paper gives for N_p, which App. A.2 leaves unset (U-ABL-1) [ours] |
| Results on one task, or under an unstated protocol: FCD-Engram over LFR-Engram, three chained gains, parity with human papers | C-ABLX-6 [Tab. 6]; C-DISC-4 [Tab. 9]; C-DISC-5 [Tab. 10] | No | one task each, or a protocol the paper does not give (U-EVAL-6); the fair measure behind the first is how often a meta-review Refine is kept across tasks, which the paper never reports [ours] |

- **In short.** The fair targets are the mechanics (rows 1–2), the planted behaviours (rows 3, 4, 6 and 7), the integrity gate (row 5) and the backend swap (row 14) [ours].
- **Not fair as numbers:** every headline outcome (rows 8–11 and 16), since each rests on an undefined measure, on the reviewer the loop optimizes, or on one task; rows 12, 13 and 15 serve as a shape, a budget and a default [ours].
