# Stage 3 · Refining ideas from experimental results [§3.3]

Revised 2026-09-28 after the persona review: fixes F-AN-3, F-AN-9, F-AN-19, F-4 and F-17 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md` [ours].

Part of [analysis.md](../analysis.md). This file covers the Table 1 rows "Idea evolution" and "Select best idea" [Tab. 1] [ours].

- **The diagram's flow.** *Execution Traces* → *Idea Evolver* → *New Ideas* → *Implementer*, which also receives *Unevaluated Seed Ideas* → *Selector* → *Best Idea & Results & Code*; an edge *Update Execution Traces* runs from the Implementer back to the traces [Fig. 6] (image).
- **How the rounds are labelled elsewhere.** *Initial* and *Round 1* to *Round 4*, over 49 ICML 2026 tasks [Fig. 9] (image) [§4.2]; Figure 10b books *Initial Implements* apart from *Idea Refinement*, over 33 NeurIPS 2025 tasks [Fig. 10] (image) [§4.3].

### Idea evolution [Tab. 1 row "Idea evolution"] · P-EVO-1 … 6

- **Purpose:** improve ideas round by round with "an evolution strategy that uses these execution traces as feedback", while still trying unevaluated seeds [§3.3] (tex:sections/3_new_method.tex:64) (tex:sections/3_new_method.tex:75).
- **Inputs:** H_0 with its scores [§3.1]; G [§3.3, Eq. 3]; all earlier traces R_<k [§3.3] (tex:sections/3_new_method.tex:67).
- **Inputs, split:** results on the benchmark that is then reported, carried in the traces; no split is named (U-TOP-5) [§3.3].
- **Outputs:** the traces R_0 … R_k, with a verdict for every idea tried; the `Good` ideas go to the Selector [§3.3] (tex:sections/3_new_method.tex:90).
- **Agents:** Idea Evolver Agent A_Evolve [§3.3] [§4.2], *Idea Evolver* [Fig. 3] [Fig. 6] (image), on Gemini 3.6 Flash [App. A.2]; A_Coder, drawn as *Implementer* [§3.3] [Fig. 6] (image), whose coding agents use Claude Code [App. A.2].
- **Steps:**
  1. P-EVO-1, round 0: the top-N_0 seeds → A_Coder → R_0, "In the initial evaluation round" [§3.3] (tex:sections/3_new_method.tex:63).
  2. P-EVO-2, round k ≥ 1: R_<k → A_Evolve → I_k of N_k ideas; A_Evolve analyzes the `Good` results and the `Bad` diagnostic logs "to propose refined hypotheses" [§3.3] (tex:sections/3_new_method.tex:67-68).
  3. P-EVO-3, exploration: the next N_e "highest-ranked unevaluated seed ideas" join, so H_k = I_k ∪ H_0^(k) (paraphrase), because relying on A_Evolve alone "risks trapping the optimization process in local optima centered around early seed ideas" [§3.3] (tex:sections/3_new_method.tex:74-76).
  4. P-EVO-4: each h in H_k → A_Coder → R_k [§3.3, Eq. 3] (tex:sections/3_new_method.tex:80-83).
  5. P-EVO-5: the stop test (U-EVO-1) [§3.3] (tex:sections/3_new_method.tex:84-85).
  6. P-EVO-6: zero successes at round K → the run ends [§3.3] (tex:sections/3_new_method.tex:86).
- **App. A.2 values:** "In each idea experimentation round, we evaluate two candidates: one selected from the seed ideas and the other an evolved idea", so N_e = N_k = 1; "We run this experimentation loop for up to four rounds, terminating early once four successful ideas are obtained", so K = S = 4 [App. A.2] (tex:sections/appendix.tex:155).
- **Loop:** candidate *Evolved idea*, critic *Idea experiment*, which is A_Coder with verdict `Good` or `Bad`, refine *Evolve idea from traces* [Tab. 1] [§3.3]; limits K and S [§3.3] [App. A.2].
- **Stopping rule:** the count of `Good` verdicts over rounds 0 … k reaches S (paraphrase of the formula), or round K is reached [§3.3] (tex:sections/3_new_method.tex:84-85).
- **On exhaustion:** with at least one `Good`, selection follows, "Upon discovering at least one successful idea" [§3.3] (tex:sections/3_new_method.tex:89); with none at round K, the engine "terminates the entire process", leaving no P+ or C+ [§3.3] (tex:sections/3_new_method.tex:86) [inferred].
- **On failure:** UNSPECIFIED (U-TOP-2); running out of seeds is U-EVO-3 [§3.3].
- **Gaps:** A-EVO-1, A-EVO-2, U-EVO-1, U-EVO-2, U-EVO-3, U-EVO-4 [§3.3].

### Select best idea [Tab. 1 row "Select best idea"] · P-SEL-1

- **Purpose:** choose h_best "for downstream ablation analysis" [§3.3] (tex:sections/3_new_method.tex:89).
- **Inputs:** G and each `Good` idea's (h, E^h, C^h), from every round, all "evaluated on the full benchmark" [§3.3, Eq. 4] (tex:sections/3_new_method.tex:90-92).
- **Inputs, split:** the full-benchmark results of every `Good` idea, the same data that is reported (U-TOP-5) [§3.3].
- **Outputs:** h_best, E_best, C_best [§3.3, Eq. 4], read by ablation, drafting, the rebuttal coder and the export [§3.4] [§3.5] [§3.6].
- **Agents:** Selector Agent A_Selector [§3.3] [§4.2]; *Selector* [Fig. 6] (image); Gemini 3.6 Flash [App. A.2].
- **Steps:**
  1. P-SEL-1: the `Good` tuples → Selector → the best one: it "compares performance metrics and execution logs across all validated ideas" [§3.3] (tex:sections/3_new_method.tex:90).
- **Loop:** none; critic *What is the best idea from traces?*, no refine [Tab. 1].
- **Stopping rule:** one call [Tab. 1] [ours].
- **On exhaustion:** not applicable [Tab. 1] [ours].
- **On failure:** UNSPECIFIED (U-TOP-2) [§3.3].
- **Where selections come from:** "the majority of the top-performing ideas chosen by the Selector Agent are identified in the early stages", over 49 ICML 2026 tasks [§4.2] (tex:sections/4_experiment.tex:30) [Fig. 9b] (image).
- **Gaps:** U-SEL-1, the criterion; U-SEL-2, how much it reads [§3.3].

## Gaps found here

- **A-EVO-1 · AMBIGUOUS · What round 0 runs.** *Register: A-EVO-1.* §3.3 runs the top-N_0 seed ideas in the initial round (paraphrase) [§3.3] (tex:sections/3_new_method.tex:63); App. A.2 says "In each idea experimentation round, we evaluate two candidates: one selected from the seed ideas and the other an evolved idea" [App. A.2]. No evolved idea exists before round 1, and N_0 has no value [§3.3].
  - Class: filed first as INCONSISTENT; verdict: AMBIGUOUS. Read as the rounds k ≥ 1, which A-EVO-2's favoured reading supports, A.2 and §3.3 agree and only N_0 is left open; the two contradict each other only under A-EVO-2's reading 2 [§3.3] [App. A.2] [ours].
  - Reading 1: A.2's rounds are the rounds k ≥ 1, and round 0 runs two seeds, N_0 = 2 [App. A.2] [§3.3].
  - Reading 2: round 0 runs only the seed half, N_0 = 1 [App. A.2].
  - Evidence: round 0's selected best ideas are all seeds [Fig. 9b] (image), and Figure 10b books *Initial Implements* apart [Fig. 10] (image). Decision forced: N_0 [ours].
- **A-EVO-2 · AMBIGUOUS · Do the four rounds include round 0?** *Register: A-EVO-2.* §3.3 numbers rounds 0 … K and stops when "round K is reached" (paraphrase) [§3.3] (tex:sections/3_new_method.tex:86); App. A.2 runs the loop "for up to four rounds" [App. A.2].
  - Reading 1: K = 4 refinement rounds after round 0, five in all; Figure 9 labels *Initial* then *Round 1* to *Round 4*, and 4 of 49 tasks select their best idea in Round 4 [Fig. 9] (image).
  - Reading 2: four rounds in all, K = 3 [App. A.2].
  - Decision forced: K; the evidence favours reading 1 [ours].
- **U-EVO-1 · UNSPECIFIED · When the S test runs.** *Register: U-EVO-1.* The formula sums whole rounds, which suggests a check after each round; whether a round stops at its S-th success is not said [§3.3] (tex:sections/3_new_method.tex:85). Decision forced: the check point [ours].
- **U-EVO-2 · UNSPECIFIED · What A_Evolve reads.** *Register: U-EVO-2.* It aggregates "all historic execution traces", tuples that include whole codebases C^h; how much of each it reads, whether it sees G, the limitations or the novelty scores, and whether its ideas face the Novelty Checker are not stated [§3.3] (tex:sections/3_new_method.tex:67). Decision forced: the evolver's context, and a novelty check for evolved ideas [ours].
- **U-EVO-3 · UNSPECIFIED · Running out of seeds.** *Register: U-EVO-3.* Each round takes the next N_e "highest-ranked unevaluated seed ideas" [§3.3] (tex:sections/3_new_method.tex:76); what happens when none is left is not stated [§3.3]. Decision forced: the rule once H_0 is spent [ours].
- **U-EVO-4 · UNSPECIFIED · What a run with no success leaves.** *Register: U-EVO-4.* The engine "terminates the entire process" [§3.3] (tex:sections/3_new_method.tex:86); nothing says what is recorded, and Table 3 counts only "the number of papers successfully generated" [Tab. 3]. Decision forced: the failure record of a task [ours].
- **U-SEL-1 · UNSPECIFIED · The Selector's criterion.** *Register: U-SEL-1.* An LLM comparison of "performance metrics and execution logs", with no rule for trade-offs across datasets and metrics, no tie-break, and no word on novelty's weight [§3.3] (tex:sections/3_new_method.tex:90). Decision forced: the selection prompt, and whether numbers constrain it [ours].
- **U-SEL-2 · UNSPECIFIED · How much the Selector reads.** *Register: U-SEL-2; related row U-SEL-1.* Equation 4 hands the Selector every `Good` idea's (h, E^h, C^h), whole codebases included [§3.3, Eq. 4] (tex:sections/3_new_method.tex:90-92); it compares "performance metrics and execution logs", and no bound on what it reads is stated [§3.3] (tex:sections/3_new_method.tex:90). Decision forced: what the Selector receives, and who chose each cut [ours].
