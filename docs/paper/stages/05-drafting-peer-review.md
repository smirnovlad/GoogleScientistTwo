# Stage 5 · Drafting and the simulated review–rebuttal loop [§3.5]

Part of [analysis.md](../analysis.md). This file covers the Table 1 rows "Initial drafting" and "Peer-Review" [Tab. 1] [ours].

- **The diagram's flow.** *Initial Drafter* → *Peer Reviewer*; ✗ → *Rebuttal Planner* → *Rebuttal Coder* → *Draft Enhancer* → back to *Peer Reviewer*; ✓ → *Meta Reviewer* [Fig. 7] (image).
- **In the overview.** *Writer Agent* (*Initial Drafter* → *Draft Enhancer*) and *Peer-Review Agent* (*Review Agent* → *Rebuttal Agent*), joined by a cycle arrow [Fig. 3] (image).

### Initial drafting [Tab. 1 row "Initial drafting"] · P-DRAFT-1

- **Purpose:** turn the finalized idea and its results into "a full, conference-formatted manuscript" [§3.5] (tex:sections/3_new_method.tex:119).
- **Inputs:** h_best, E_best and E_abl, and nothing else the text names [§3.5] (tex:sections/3_new_method.tex:119); G, C_best and the traces are not listed (U-DRAFT-1) [ours].
- **Outputs:** P_new, in "the ICLR 2025 format" [App. A.2] (tex:sections/appendix.tex:155); read by the Peer Reviewer [§3.5] (tex:sections/3_new_method.tex:123).
- **Agents:** Initial Drafter Agent A_Draft, "incorporating PaperOrchestra" [§3.5] [Bib: song2026paperorchestra]; *Initial Drafter* inside *Writer Agent* [Fig. 3] [Fig. 7] (image); on Gemini 3.6 Flash by default [App. A.2] [inferred]; PaperOrchestra "compiles unconstrained experiment logs and ideas into LaTeX manuscripts" [§2] (tex:sections/2_related_works.tex:5).
- **Steps:**
  1. P-DRAFT-1: h_best, E_best, E_abl → A_Draft → P_new; the drafter "synthesizes the selected idea", the main benchmark results and the ablations into the manuscript [§3.5] (tex:sections/3_new_method.tex:119).
- **Loop:** none; the row's critic and refine are empty [Tab. 1].
- **Stopping rule:** one call [Tab. 1] [ours].
- **On exhaustion:** not applicable [Tab. 1] [ours].
- **On failure:** UNSPECIFIED (U-DRAFT-2) [§3.5].
- **Integrity:** the reference check and the method–code audit act on the manuscript; where they sit is U-INT-3 [§4.2].
- **Gaps:** U-DRAFT-1, U-DRAFT-2, A-INT-2 [§3.5].

### Peer-Review [Tab. 1 row "Peer-Review"] · P-PEER-1 … 6

- **Purpose:** the engine "simulates an interactive peer-review and rebuttal process" to raise the manuscript [§3.5] (tex:sections/3_new_method.tex:122).
- **Inputs:** P_new [§3.5] (tex:sections/3_new_method.tex:123); C_best, for the rebuttal experiments [§3.5] (tex:sections/3_new_method.tex:126).
- **Outputs:** the last P_new, and the last R_new with its score, read by the Meta-Review Agent [§3.5] (tex:sections/3_new_method.tex:132) [§3.6] (tex:sections/3_new_method.tex:135).
- **Agents:** Peer-Reviewer Agent A_Reviewer, which is ScholarPeer [§3.5] [Bib: goyal2026scholarpeer], also *Peer Reviewer* [Fig. 7] (image), Review Agent [§3] [Fig. 3] (image) and Peer-Review Agent [§1]; Rebuttal Planner Agent A_RebPlan [§3.5], *Rebuttal Planner* [Fig. 7] (image); Rebuttal Coding Agent A_RebCoder [§3.5], *Rebuttal Coder* [Fig. 7] (image); Paper Enhancer Agent A_Enhancer [§3.5], Draft Enhancer [App. A.2] [Fig. 3] [Fig. 7] (image).
- **Models:** the Rebuttal Agent and the Draft Enhancer use Claude Code with Opus 4.8 [App. A.2]; whether the planner belongs to the Rebuttal Agent is A-CFG-1; ScholarPeer's backbone is not stated (U-PEER-3) [App. A.2].
- **Steps:**
  1. P-PEER-1: P_new → A_Reviewer → R_new, "containing identified strengths, weaknesses, targeted questions, and an overall numerical score" s_review in [1, 10], "based on the standard ICLR grading scale" [§3.5] (tex:sections/3_new_method.tex:123).
  2. P-PEER-2: if s_review "is below the acceptance threshold (e.g., 8)", the engine "initiates an automated rebuttal stage to address reviewer concerns" [§3.5] (tex:sections/3_new_method.tex:124).
  3. P-PEER-3: R_new → A_RebPlan → N_t supplementary tasks "designed to resolve reviewer queries" [§3.5] (tex:sections/3_new_method.tex:125).
  4. P-PEER-4: each t_i with C_best → A_RebCoder → e_i, and E_reb = {e_1, …, e_Nt}; the coder "implements and executes each planned task" [§3.5] (tex:sections/3_new_method.tex:126-127).
  5. P-PEER-5: P_new, R_new, E_reb → A_Enhancer → a revised P_new, "revising narrative claims and updating empirical tables and figures" [§3.5] (tex:sections/3_new_method.tex:130).
  6. P-PEER-6: "The updated manuscript is re-evaluated by" A_Reviewer, which replaces R_new and s_review [§3.5] (tex:sections/3_new_method.tex:131).
- **Loop:** candidate *Manuscript*, critic *Is review score good enough?*, refine *Run rebuttal experiments* [Tab. 1]; the verdict is a threshold test on a number [§3.5]; limit N_peer [§3.5] (tex:sections/3_new_method.tex:132), set to 2 with threshold 8: "the peer-review simulation runs for at most two rounds and terminates early if the ScholarPeer review score reaches 8" [App. A.2].
- **Stopping rule:** "This review-rebuttal cycle repeats until" s_new ≥ 8 or N_peer review iterations are reached (paraphrase) [§3.5] (tex:sections/3_new_method.tex:132); s_new and s_review are one score (A-TOP-5).
- **On exhaustion:** the manuscript is kept, "producing a polished, thoroughly validated final manuscript" [§3.5] (tex:sections/3_new_method.tex:132), not discarded as Listing 1 would (A-TOP-1) [Lst. 1].
- **On failure:** UNSPECIFIED (U-TOP-2) [§3.5].
- **Evidence on the rounds:** Table 5 reports review rounds 0, without the Rebuttal Agent, then 1 and 2, over 49 ICML 2026 tasks [Tab. 5] [§4.2]; Appendix C's Procrustes-DS example "did not undergo this process", consistent with a rebuttal that runs only below the threshold [App. C] (tex:sections/appendix.tex:344) [inferred].
- **Reviewer and evaluator:** ScholarPeer "serves as an in-distribution evaluation, as it is also used to refine the draft quality", while the Stanford Agentic Reviewer is held out [§4] (tex:sections/4_experiment.tex:5) [fn. 1].
- **Gaps:** A-PEER-1, U-PEER-1, U-PEER-2, U-PEER-3, U-PEER-4, A-TOP-1, A-TOP-5 [§3.5].

## Gaps found here

- **U-DRAFT-1 · UNSPECIFIED · What the drafter reads.** §3.5 lists only h_best, E_best and E_abl [§3.5] (tex:sections/3_new_method.tex:119); whether it also receives G (the human paper, for related work and baselines), C_best, the traces of rejected ideas or a literature search, and how the incorporated PaperOrchestra divides the work, are not stated [§3.5] [§2]. Decision forced: the drafter's inputs and its wrapper [ours].
- **U-DRAFT-2 · UNSPECIFIED · Drafting failures and figures.** Nothing covers a draft that fails to compile or breaks the format, or says which agent makes the first figures; only the Enhancer is said to update "empirical tables and figures" [§3.5] (tex:sections/3_new_method.tex:130) [App. A.2]. Decision forced: a compile check and a figure step [ours].
- **A-PEER-1 · AMBIGUOUS · What N_peer counts.** §3.5 caps the review iterations at N_peer [§3.5] (tex:sections/3_new_method.tex:132); App. A.2 says "the peer-review simulation runs for at most two rounds" [App. A.2].
  - Reading 1: two reviews, so at most one rebuttal [§3.5].
  - Reading 2: two rebuttal cycles, so up to three reviews; Table 5 shows review rounds 0, 1 and 2, the last two with the Rebuttal Agent, over 49 ICML 2026 tasks [Tab. 5] [§4.2].
  - Decision forced: N_peer's unit; the evidence favours reading 2 [ours].
- **U-PEER-1 · UNSPECIFIED · N_t.** §3.5 introduces N_t and App. A.2 gives no value [§3.5] (tex:sections/3_new_method.tex:125) [App. A.2]. Decision forced: N_t, or a rule for it [ours].
- **U-PEER-2 · UNSPECIFIED · Whether rebuttal code survives.** The coder runs each task on C_best [§3.5] (tex:sections/3_new_method.tex:126); whether its code enters C_best, and so C+, is not stated, although the paper's new numbers must reproduce [§3.5] [Tab. 7]. Decision forced: where rebuttal code lives [ours].
- **U-PEER-3 · UNSPECIFIED · ScholarPeer's configuration.** Its backbone (App. A.2's default would make it Gemini 3.6 Flash), version, settings and input (PDF or LaTeX), and whether a round is one review or several, are not stated [§3.5] [App. A.2] [Bib: goyal2026scholarpeer]. Decision forced: the reviewer's configuration [ours].
- **U-PEER-4 · UNSPECIFIED · What the Enhancer reads and may change.** It integrates R_new and E_reb into P_new [§3.5] (tex:sections/3_new_method.tex:130); whether it may change C_best, run code for figures, or edit sections the review did not raise is not stated; its routing to Claude Code suggests it works on files [App. A.2] [inferred]. Decision forced: the Enhancer's tools and write scope [ours].
