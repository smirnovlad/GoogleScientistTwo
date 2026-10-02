# Stage 6 · Meta-review and review-driven refinement [§3.6]

Revised 2026-09-28 after the persona review: fixes F-AN-3 and F-17 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md` [ours].

Part of [analysis.md](../analysis.md). This file covers the Table 1 row "Meta-Review" [Tab. 1] [ours].

- **The diagram's flow.** *Meta Reviewer* ✓ → *Final Paper P+ / Final Code C+*; ✗ → *Full-Set Engineer* → *Result Compare*, whose ✓ edge runs back to *Best Idea / Results / Code* ahead of the *Ablation Planner*, and whose ✗ edge goes to *Final Paper / Final Code* [Fig. 7] (image).
- **In the overview.** The *Meta-Review Agent* box holds *Critic Agent* → *Idea Refiner*; a line from the Idea Refiner runs along the bottom and up the right edge into the *Analyzer*, and the box's other exit is *Outputs* [Fig. 3] (image).

### Meta-Review [Tab. 1 row "Meta-Review"] · P-META-1 … 7

- **Purpose:** "to make a final publication assessment and generate actionable strategic feedback" [§3.6] (tex:sections/3_new_method.tex:135).
- **Inputs:** the manuscript and the review: A_Meta "takes the paper draft and reviewer feedback as inputs" [§3.6] (tex:sections/3_new_method.tex:138); no code or results are named (U-META-2) [ours].
- **Inputs, split:** the meta-review reads the manuscript and the review; its refinement's comparison reads results on the benchmark that is reported, with no split named (U-TOP-5) [§3.6] [ours].
- **Outputs:** d_meta in {`Accept`, `Refine`} and the meta-critique r_meta [§3.6] (tex:sections/3_new_method.tex:138); at export, P+ ← P_new and C+ ← C_best (paraphrase) [§3.6] (tex:sections/3_new_method.tex:140).
- **Agents:** Meta-Review Agent A_Meta [§1] [§3] [§3.6] [§4.2], the meta-reviewer [§3.6], *Meta Reviewer* [Fig. 7] (image), the *Critic Agent* in the *Meta-Review Agent* box [Fig. 3] (image), on Gemini 3.6 Flash [App. A.2]; Full-Set Engineering Agent A_FullEng [§3.6], *Full-Set Engineer* [Fig. 7], *Idea Refiner* [Fig. 3] (image), model A-CFG-1; Result Comparison Agent [§3.6], *Result Compare* [Fig. 7] (image), on Gemini [App. A.2].
- **Steps:**
  1. P-META-1: P_new and R_new → A_Meta → d_meta, r_meta [§3.6] (tex:sections/3_new_method.tex:138).
  2. P-META-2: `Accept` → P_new "is judged to meet top-tier conference standards", and the engine "finalizes the process and exports the final improved paper and its codebase" [§3.6] (tex:sections/3_new_method.tex:139-140).
  3. P-META-3: `Refine`, "indicating that the meta-reviewer identified a critical algorithmic or empirical weakness" → A_FullEng updates h_best, guided by r_meta → h_new, E_new, C_new [§3.6] (tex:sections/3_new_method.tex:143-144).
  4. P-META-4: E_new against E_best → Result Comparison Agent, "To ensure that the meta-review modification yields true scientific progression" [§3.6] (tex:sections/3_new_method.tex:147).
  5. P-META-5: if E_new "is verified as strictly superior", the core state is replaced and the engine "re-executes downstream ablation planning, ablation execution, manuscript re-drafting, and simulated peer-review cycles" [§3.6] (tex:sections/3_new_method.tex:148-149).
  6. P-META-6: otherwise the refinement is discarded and the engine "terminates the process using the previous best outputs" [§3.6] (tex:sections/3_new_method.tex:150).
  7. P-META-7: "This meta-refinement loop repeats for a maximum of" N_meta "iterations or until" d_meta is `Accept` [§3.6] (tex:sections/3_new_method.tex:151).
- **Loop:** candidate *Manuscript, Review*, critic *Does it meet the venue bar?*, refine *Refine idea and analyze again* [Tab. 1]; verdicts `Accept` and `Refine` [§3.6] (tex:sections/3_new_method.tex:138); limit N_meta [§3.6] (tex:sections/3_new_method.tex:151), set to 1: "with review-based refinement conducted at most once" [App. A.2].
- **Stopping rule:** `Accept`; a refinement that is not strictly superior; or N_meta refinements used [§3.6] (tex:sections/3_new_method.tex:139) (tex:sections/3_new_method.tex:150-151).
- **On exhaustion:** the loop ends "yielding a rigorously validated final contribution", which we read as exporting P_new and C_best [§3.6] (tex:sections/3_new_method.tex:151) [inferred]; not Listing 1's `None` (A-TOP-1) [Lst. 1].
- **On failure:** UNSPECIFIED (U-TOP-2) [§3.6].
- **An unapproved export:** after a failed comparison, P+ is the P_new the meta-reviewer had just returned as `Refine` [§3.6] (tex:sections/3_new_method.tex:150) [ours]; this is the conflict A-TOP-3 [§3].
- **The paper's one example:** "the Meta-Review Agent deemed LFR-Engram insufficient to meet expert standards", and the refinement produced FCD-Engram, on one task [§4.2] (tex:sections/4_experiment.tex:38) [Tab. 6].
- **Gaps:** A-META-1, A-META-2, U-META-1, U-META-2, A-TOP-3, A-ABL-3 [§3.6].

## Gaps found here

- **A-META-1 · AMBIGUOUS · How much the restart re-runs.** *Register: A-META-1.* §3.6 lists "downstream ablation planning, ablation execution, manuscript re-drafting, and simulated peer-review cycles", naming neither the ablation critic nor its refinement [§3.6] (tex:sections/3_new_method.tex:149). Figure 7's ✓ edge from *Result Compare* returns ahead of the *Ablation Planner*, on a path through the *Ablation Critic* and its *Full-Set Engineer* branch [Fig. 7] (image).
  - Reading 1: planning, execution, drafting and review only; the ablation critic is skipped [§3.6].
  - Reading 2: the whole downstream pass, critic and refinement included [Fig. 7] (image).
  - Decision forced: the restart's entry point [ours].
- **A-META-2 · AMBIGUOUS · Is the meta-reviewer asked again after the restart?** *Register: A-META-2.* The loop "repeats for a maximum of" N_meta iterations or until `Accept`, which implies a second verdict [§3.6] (tex:sections/3_new_method.tex:151), and Figure 7's restart path leads back through *Peer Reviewer* to *Meta Reviewer* [Fig. 7] (image). With N_meta = 1 that verdict cannot trigger another refinement, and what is exported after a second `Refine` is not said [App. A.2].
  - Reading 1: a second meta-review runs; after a `Refine`, the pass's P_new and C_best are exported [inferred] [§3.6].
  - Reading 2: no second meta-review; the restarted pass exports directly [App. A.2].
  - Decision forced: the export rule after the restart [ours].
- **U-META-1 · UNSPECIFIED · Do the loop budgets reset for the restart?** *Register: U-META-1.* Whether the re-run ablation gets a fresh N_abl, and the re-run review a fresh N_peer, is not stated [§3.6] (tex:sections/3_new_method.tex:149) [App. A.2]. Decision forced: budgets per pass or per run; the bound in section 9 of analysis.md assumes a reset [ours].
- **U-META-2 · UNSPECIFIED · The meta-reviewer's criterion.** *Register: U-META-2.* It judges against top-tier conference standards from the manuscript and the latest review alone; no score, rubric or threshold is given, and it sees neither code nor E_best [§3.6] (tex:sections/3_new_method.tex:135) (tex:sections/3_new_method.tex:139). Decision forced: the meta-review prompt, and whether it sees results [ours].
