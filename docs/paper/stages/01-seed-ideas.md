# Stage 1 · Generating novel seed ideas [§3.1]

Revised 2026-09-28 after the persona review: fixes F-AN-3, F-AN-29 and F-17 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md` [ours].

Part of [analysis.md](../analysis.md). This file covers the Table 1 rows "Finding limitations" and "Seed idea generation" in the README's stage template [Tab. 1] [ours].

- **The diagram's flow.** *Scientific Problem* → *Limitation Extractor* → *Limitation Verifier*, with a ✗ edge back to the Extractor and a ✓ edge on to *Initial Idea Generator* → *Novelty Checker* → *Idea Generator* → *Seed Ideas H_0*, and an edge from the Idea Generator back to the Novelty Checker [Fig. 4] (image).

### Finding limitations [Tab. 1 row "Finding limitations"] · P-LIM-1 … 4

- **Purpose:** identify "the core limitations of the human state-of-the-art method" with respect to G [§3.1] (tex:sections/3_new_method.tex:19).
- **Inputs:** G, and nothing else the text names [§3.1] (tex:sections/3_new_method.tex:20).
- **Inputs, split:** none; the stage reads G's paper, not benchmark data (U-TOP-5) [§3.1] [ours].
- **Outputs:** a set of limitations with no symbol [§3.1] [Tab. 1]; read by the initial idea, "specifically designed to address the identified limitations" [§3.1] (tex:sections/3_new_method.tex:25); whether any later stage reads it is not stated (U-LIM-1) [ours].
- **Agents:** Limitation Extractor [§3.1] [Fig. 3] [Fig. 4] (image); Limitation Verifier [§3.1] [Fig. 4] (image), which Figure 3 omits; both Gemini 3.6 Flash, the default [App. A.2].
- **Steps:**
  1. P-LIM-1: G → Limitation Extractor → the set: "the Limitation Extractor extracts a set of limitations from" G [§3.1] (tex:sections/3_new_method.tex:20).
  2. P-LIM-2: the set → Limitation Verifier → a verdict: it "verifies whether this set is sufficient to guide novel improvements" to G [§3.1] (tex:sections/3_new_method.tex:21).
  3. P-LIM-3: insufficient → Extractor → a larger set: "the Limitation Extractor again identifies missing limitations or weaknesses and expands the collection" [§3.1] (tex:sections/3_new_method.tex:22).
- **Loop:** candidate the set, critic the Verifier (*Can guide novel improvement?*), refine the Extractor (*Add missing limitations*) [Tab. 1]; verdicts: confirmed, or the Verifier "considers the set insufficient" [§3.1] (tex:sections/3_new_method.tex:22); limit P-LIM-4 has no symbol, and its value, P-CFG-1 in analysis.md, is 16: "We extract limitations for a maximum of 16 rounds" [App. A.2] (tex:sections/appendix.tex:155).
- **Stopping rule:** "This verification loop repeats until the Limitation Verifier confirms that all actionable limitations have been thoroughly extracted or maximum number of iterations is reached" [§3.1] (tex:sections/3_new_method.tex:23).
- **On exhaustion:** not stated; the set so far passes on [inferred] [§3.1]; Listing 1 would return `None` (A-LIM-1) [Lst. 1].
- **On failure:** UNSPECIFIED (U-TOP-2) [§3.1].
- **Gaps:** A-LIM-1, the exhaustion output; U-LIM-1, criterion and formats; A-TOP-2, what the 16 rounds count [§3.1] [App. A.2].

### Seed idea generation [Tab. 1 row "Seed idea generation"] · P-SEED-1 … 4

- **Purpose:** a pool H_0 of N_seed ideas that address the limitations, ranked so the engine can "prioritize implementing the ideas with the highest originality" [§3.1] (tex:sections/3_new_method.tex:28).
- **Inputs:** the set of limitations [§3.1] (tex:sections/3_new_method.tex:25); G [inferred] [§3.1]; two reference papers per novelty check, from Google Search [App. A.2].
- **Inputs, split:** none; no experiment runs in this stage (U-TOP-5) [§3.1] [ours].
- **Outputs:** H_0 = {h_i}, sorted so that s_i ≥ s_j whenever i < j (paraphrase), with the scores s_i [§3.1] (tex:sections/3_new_method.tex:27); read by round 0, which takes the top N_0, and by exploration, which takes the next N_e per round [§3.2] (tex:sections/3_new_method.tex:40) [§3.3] (tex:sections/3_new_method.tex:75-76).
- **Agents:** initial idea generation, named only in the diagram as *Initial Idea Generator* [§3.1] [Fig. 4] (image); Novelty Checker [§3.1] [Fig. 3] [Fig. 4] (image); Idea Generator Agent [§3.1], *Idea Generator* in the diagram [Fig. 4] (image); Figure 3 boxes extractor and checker as *Seed Idea Generator* [Fig. 3] (image); all Gemini 3.6 Flash, the default [App. A.2].
- **Steps:**
  1. P-SEED-1: the limitations → initial idea generation → h_0 [§3.1] (tex:sections/3_new_method.tex:25).
  2. P-SEED-2: h_0 and two retrieved papers → Novelty Checker → s_0: the engine "computes its novelty score using the Novelty Checker" [§3.1] (tex:sections/3_new_method.tex:25) [App. A.2].
  3. P-SEED-3: H_0 → Idea Generator Agent → one new idea → Novelty Checker → added, expanding the pool "with distinct, higher-novelty ideas" [§3.1] (tex:sections/3_new_method.tex:25); the edge back to the checker is drawn [Fig. 4] (image).
  4. P-SEED-4: H_0 → sorted by s_i, descending [§3.1] (tex:sections/3_new_method.tex:27).
- **Loop:** candidate *Seed ideas*, critic *Is it novel?* (the Novelty Checker), refine *Add more novel ideas* (the Idea Generator) [Tab. 1]; verdicts: none, since the critic returns a score [§3.1]; limit: N_seed, a target count rather than a round budget [§3.1] (tex:sections/3_new_method.tex:26), with no value in App. A.2 (U-SEED-1) [App. A.2].
- **Stopping rule:** "This process continues until a collection of" N_seed "candidate ideas is gathered" [§3.1] (tex:sections/3_new_method.tex:26).
- **On exhaustion:** not applicable, since the loop stops on a count [§3.1] [ours].
- **On failure:** UNSPECIFIED (U-TOP-2) [§3.1].
- **Gaps:** U-SEED-1, A-SEED-1, U-SEED-2, A-SEED-2, U-SEED-3 [§3.1] [App. A.2].

## Gaps found here

- **A-LIM-1 · AMBIGUOUS · What finding limitations outputs at its limit.** *Register: A-TOP-1 (A-LIM-1 is an alias there).* §3.1 ends the loop when the Verifier confirms or the "maximum number of iterations is reached" and says no more; the next paragraph works from "the identified limitations" [§3.1] (tex:sections/3_new_method.tex:23) (tex:sections/3_new_method.tex:25).
  - Reading 1, Listing 1: after 16 rounds the stage returns `None`, and the run has no limitations to address [Lst. 1].
  - Reading 2, the text's flow: the set collected so far passes to idea generation [§3.1] [inferred].
  - Decision forced: this stage's exhaustion output [ours].
- **U-LIM-1 · UNSPECIFIED · The Verifier's criterion and both formats.** *Register: U-LIM-1.* The Verifier checks whether the set "is sufficient to guide novel improvements" to G; what it compares against, what it returns besides the verdict, and what one limitation record holds are not stated; Appendix C shows sample limitations, analysed in artifacts.md [§3.1] [App. C]. Decision forced: the verifier prompt and a limitation schema [ours].
- **U-SEED-1 · UNSPECIFIED · N_seed.** *Register: U-SEED-1.* §3.1 introduces N_seed and App. A.2 gives it no value [§3.1] (tex:sections/3_new_method.tex:26) [App. A.2]. Under App. A.2's schedule the pool needs at least N_0 + K·N_e seeds, 6 with N_0 = 2, for every round to find an unevaluated one [§3.3] [App. A.2] [ours]. Decision forced: N_seed [ours].
- **A-SEED-1 · AMBIGUOUS · Is novelty a filter or a ranking?** *Register: A-SEED-1.* Reading 1, a filter: the overview says the engine generates ideas "filtering for those with high novelty" [§3] (tex:sections/3_new_method.tex:5), and Table 1's critic asks *Is it novel?* [Tab. 1].
  - Reading 2, a ranking: §3.1 only scores and sorts, the pool is "sorted in descending order according to their novelty scores", and no discard rule or threshold appears [§3.1] (tex:sections/3_new_method.tex:27).
  - The generator adds "distinct, higher-novelty ideas", higher than what is not said [§3.1] (tex:sections/3_new_method.tex:25). Decision forced: whether a low-novelty idea is dropped, and at what threshold [ours].
- **U-SEED-2 · UNSPECIFIED · The novelty score.** *Register: U-SEED-2.* App. A.2 fixes only the retrieval: "To evaluate novelty, ScientistTwo retrieves two reference papers via Google Search" [App. A.2] (tex:sections/appendix.tex:155). The score's scale, the query, and whether G's own paper is among the comparisons are not stated [§3.1]. Decision forced: the scoring prompt and the query [ours].
- **A-SEED-2 · AMBIGUOUS · Who generates h_0.** *Register: A-SEED-2.* §3.1 says only that the engine "first generates an initial idea" [§3.1] (tex:sections/3_new_method.tex:25); Figure 4 draws an *Initial Idea Generator* apart from the *Idea Generator* [Fig. 4] (image). Reading 1: one agent with two prompts. Reading 2: two agents. Decision forced: one agent definition or two, of low impact [ours].
- **U-SEED-3 · UNSPECIFIED · The Idea Generator's inputs and limits.** *Register: U-SEED-3.* §3.1 names neither its inputs (the limitations, the pool and its scores, G) nor any content rule, yet Appendix B calls compute scaling "a pure compute-scaling knob that our idea generator deliberately does not propose" [§3.1] [App. B] (tex:sections/appendix.tex:244-245). Decision forced: the generator's inputs and prompt [ours].
