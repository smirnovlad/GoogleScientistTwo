# Stage 4 · Ablation studies: sources of gain, and one more refinement [§3.4]

Revised 2026-09-28 after the persona review: fixes F-AN-3, F-AN-5, F-AN-9, F-AN-31, F-7 and F-17 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md`; then the closure corrections from the `closure-*.md` reports in that folder [ours].

Part of [analysis.md](../analysis.md). This file covers the Table 1 row "Ablation study" [Tab. 1] [ours].

- **The diagram's flow.** *Best Idea / Results / Code* → *Ablation Planner* → *Ablation Coder* → *Ablation Critic*; ✓ to *Initial Drafter*; ✗ to *Full-Set Engineer* → *Result Compare*, whose ✓ edge returns to *Best Idea / Results / Code* and whose ✗ edge runs over the top to *Initial Drafter* [Fig. 7] (image).
- **In the overview.** The *Analyzer* box holds *Ablation Study Agent* (*Planning Agent*, *Coding Agent*) and *Idea Refiner* (*Critic Agent* → *New Idea*); the new idea's arrow re-enters the *Full-Set Experiment Agent* [Fig. 3] (image).

### Ablation study [Tab. 1 row "Ablation study"] · P-ABL-1 … 7

- **Purpose:** isolate "the explicit sources of empirical gain for scientific interpretation" and use the breakdown for "an additional round of idea refinement" [§3.4] (tex:sections/3_new_method.tex:97).
- **Inputs:** h_best, E_best and C_best from the Selector [§3.4] [§3.3, Eq. 4].
- **Inputs, split:** results on the benchmark that is then reported, or on a subset: App. D's draft labels an ablation a *subset test split* [p. 69] (U-TOP-5) [§3.4].
- **Outputs:** the final h_best, E_best and C_best, possibly replaced by h_new, E_new and C_new, and E_abl, all passed to drafting [§3.4] (tex:sections/3_new_method.tex:107) [§3.5] (tex:sections/3_new_method.tex:119).
- **Agents:** Ablation Planner Agent [§3.4], *Ablation Planner* [Fig. 7], *Planning Agent* [Fig. 3] (image), and Ablation Coding Agent [§3.4], *Ablation Coder* [Fig. 7], *Coding Agent* [Fig. 3] (image), together Figure 3's *Ablation Study Agent*, which App. A.2 routes to Claude Code with Opus 4.8 [App. A.2] [inferred].
- **Agents, continued:** Ablation Critic Agent A_AblCritic, also written A_AblCrit [§3.4], *Ablation Critic* [Fig. 7] (image) [App. A.2], on Gemini by default [App. A.2] [inferred]; Full-Set Engineering Agent A_FullEng [§3.4], *Full-Set Engineer* [Fig. 7] (image), model A-CFG-1; Result Comparison Agent [§3.4], *Result Compare* [Fig. 7] (image), on Gemini [App. A.2].
- **Steps:**
  1. P-ABL-1: h_best → Ablation Planner → N_p plans; the planner "automatically formulates a set of" N_p "executable ablation plans" [§3.4] (tex:sections/3_new_method.tex:100).
  2. P-ABL-2: each p_i with C_best → Ablation Coding Agent → c_i, and E_abl = {c_1, …, c_Np} [§3.4] (tex:sections/3_new_method.tex:101-102).
  3. P-ABL-3: E_abl → Ablation Critic → d_abl, r_abl; it "inspects the component breakdown to determine whether" h_best "is optimal or requires additional modification" [§3.4] (tex:sections/3_new_method.tex:106); on `Good`, h_best "is finalized and passed to the paper drafting stage" (tex:sections/3_new_method.tex:107).
  4. P-ABL-4: `Refine` → A_FullEng, guided by r_abl → h_new, E_new, C_new [§3.4] (tex:sections/3_new_method.tex:108).
  5. P-ABL-5: E_new against E_best → Result Comparison Agent; the core state is replaced if and only if the agent prefers E_new (paraphrase) [§3.4] (tex:sections/3_new_method.tex:111-112).
  6. P-ABL-6: after an update the engine "re-executes the ablation planning phase on the updated candidate" [§3.4] (tex:sections/3_new_method.tex:113).
- **Why refine at all:** in expert practice, "where removing redundant or counterproductive components often yields a better method" [§3.4] (tex:sections/3_new_method.tex:105); §1 promises "dynamically pruning ineffective components and refining its core hypothesis" [§1] (tex:sections/1_introduction.tex:17).
- **P-ABL-7, the attribution rule:** App. B adds a criterion that §3.4 does not state, that the engine "additionally requires the gain to be attributable to the proposed mechanism in ablation" [Tab. 15] (tex:sections/appendix.tex:177); Table 1's *Is the component breakdown clean?* is the nearest wording in §3 [Tab. 1].
- **Loop:** candidate *Idea, Ablation results*, critic *Is the component breakdown clean?*, refine *Refine the method* [Tab. 1]; verdicts `Good` and `Refine` only [§3.4] (tex:sections/3_new_method.tex:106); limit N_abl [§3.4] (tex:sections/3_new_method.tex:114), set to 1: "when the Ablation Critic Agent recommends refinement based on ablation results, we refine the idea at most once" [App. A.2].
- **Stopping rule:** "This refinement loop repeats for a maximum of" N_abl "iterations or until" the critic emits `Good` (paraphrase) [§3.4] (tex:sections/3_new_method.tex:114).
- **On exhaustion:** the text moves to drafting, "ensuring a fully optimized hypothesis prior to manuscript generation" [§3.4] (tex:sections/3_new_method.tex:114); Figure 7 sends a failed comparison to *Initial Drafter* [Fig. 7] (image); Listing 1 and Appendix B point the other way (A-ABL-1, A-ABL-2) [Lst. 1] [App. B].
- **On failure:** UNSPECIFIED (U-TOP-2) [§3.4].
- **What the critic did in the paper's own runs:** for DMC-TeCh "the ablation critic rejected it because" the gain came from EMA and label smoothing [App. B] (tex:sections/appendix.tex:222-224); for LC-FTT "The ablation critic stripped" the extra machinery "down to the lone component that carried the gain" [Tab. 16] (tex:sections/appendix.tex:291-292).
- **Gaps:** A-ABL-1, A-ABL-2, A-ABL-3, U-ABL-1, U-ABL-2, U-ABL-3, U-ABL-4, U-ABL-5, U-ABL-6, A-CFG-1 [§3.4].

## Gaps found here

- **A-ABL-1 · INCONSISTENT · Can the ablation critic reject?** *Register: A-ABL-1.* §3.4 gives d_abl only `Good` or `Refine` [§3.4] (tex:sections/3_new_method.tex:106). In Appendix B, DMC-TeCh beat the baseline on 5 of 6 metrics, "but the ablation critic rejected it because" the gain came from generic training controls, "so it was not accepted as a contribution" [App. B] (tex:sections/appendix.tex:222-224).
  - Table 15 counts ScientistTwo's "Papers with a reported gain" as 4 of 5, and its caption says the engine "additionally requires the gain to be attributable to the proposed mechanism in ablation" [Tab. 15] (tex:sections/appendix.tex:177) (tex:sections/appendix.tex:183).
  - Reading 1: a third verdict, reject, ends the task without a paper [App. B].
  - Reading 2: `Refine` with N_abl spent ends the task, as Listing 1's `None` would [Lst. 1] [§3.4].
  - Decision forced: the verdict set, and a rejection's effect on the task [ours].
- **A-ABL-2 · INCONSISTENT · What follows a failed comparison or a spent budget.** *Register: A-ABL-2.* Figure 7 draws a ✗ edge from *Result Compare* to *Initial Drafter*, and §3.4 ends its loop "ensuring a fully optimized hypothesis prior to manuscript generation" [Fig. 7] (image) [§3.4] (tex:sections/3_new_method.tex:114). Listing 1 returns `None` at the limit [Lst. 1], and Appendix B's TeCh task yielded no contribution [App. B].
  - Reading 1: drafting follows with the unchanged h_best [Fig. 7] (image).
  - Reading 2: the task ends [Lst. 1] [App. B].
  - Appendix B describes TeCh's end as the critic's rejection, not as a failed comparison, so it supports reading 2 only under A-ABL-1's reading 2; the two items are decided together [App. B] [§3.4] [ours].
  - Decision forced: the branch after a failed refinement [ours].
- **A-ABL-3 · AMBIGUOUS · What better means.** *Register: A-ABL-3.* §3.4 first says the engine checks whether E_new "strictly outperforms" E_best, then updates the state if E_new is preferred "by the Result Comparison Agent" [§3.4] (tex:sections/3_new_method.tex:111-112).
  - Reading 1: a numeric test of strict improvement, on every metric or on an aggregate, which is not said [§3.4].
  - Reading 2: the agent's judgment [§3.4].
  - The same agent decides in §3.6, where E_new must be "strictly superior" [§3.6] (tex:sections/3_new_method.tex:148). Decision forced: the comparison rule for multi-dataset, multi-metric results [ours].
- **U-ABL-1 · UNSPECIFIED · N_p.** *Register: U-ABL-1.* §3.4 introduces N_p and App. A.2 gives no value [§3.4] (tex:sections/3_new_method.tex:100) [App. A.2]; Table 15 reports "5–6 ablations per paper" on the 4 ICLR 2026 tasks ScientistTwo completed [Tab. 15] (tex:sections/appendix.tex:188). Decision forced: N_p, or a rule for it [ours].
- **U-ABL-2 · UNSPECIFIED · How A_FullEng's refinement is validated.** *Register: U-ABL-2.* §3.4 names one agent producing h_new, E_new and C_new [§3.4] (tex:sections/3_new_method.tex:108); Figure 3 routes the *New Idea* back into the *Full-Set Experiment Agent*, a coder–critic loop [Fig. 3] (image). Whether E_new passes the full-set critic, and under what budget, is not stated [§3.4]. Decision forced: one call, or a full-set loop [ours].
- **U-ABL-3 · UNSPECIFIED · Whether ablation code survives.** *Register: U-ABL-3.* The Ablation Coding Agent modifies C_best to run each plan [§3.4] (tex:sections/3_new_method.tex:101); whether the variants stay in C_best, and so in C+, is not stated, although Table 7's score check means "every claimed results are reproducible" [§3.4] [Tab. 7] (tex:tables/ablation_audit.tex:3). Decision forced: where ablation code lives [ours].
- **U-ABL-4 · UNSPECIFIED · The critic's verdict on a re-ablation.** *Register: A-TOP-1 (U-ABL-4 is an alias there).* After an update the engine re-runs planning and execution [§3.4] (tex:sections/3_new_method.tex:113), and Figure 7's ✓ edge from *Result Compare* returns ahead of the *Ablation Planner*, so the critic judges again [Fig. 7] (image). With N_abl = 1 spent, what a second `Refine` does is not stated [§3.4] [App. A.2]. Decision forced: the rule for that verdict [ours].
- **U-ABL-5 · UNSPECIFIED · Where the Ablation Critic draws the line between `Refine` and a reject.** *Register: not yet indexed (new); related row A-ABL-1.* The rule is a gain "attributable to the proposed mechanism" [Tab. 15] (tex:sections/appendix.tex:177), and three cases pin the boundary [App. B] [ours].
  - TeCh was rejected because "the gains were primarily driven by general training controls" [App. B] (tex:sections/appendix.tex:222-224).
  - On p. 46 every component falls short of its design, "The performance actually relies heavily on X-Maha's trace-variance factor rather than HSKP itself", yet the idea was refined, every component changed and one removed [p. 46] [p. 40] (image); that p. 46 is the Ablation Critic's is artifacts.md's A-ART-1 [ours].
  - LC-FTT was stripped "down to the lone component that carried the gain" [Tab. 16] (tex:sections/appendix.tex:291-292).
  - Decision forced: a written boundary between `Refine` and a reject, with these three cases as its first test set [ours].
- **U-ABL-6 · UNSPECIFIED · How much the Ablation Critic reads.** *Register: not yet indexed (new); related row U-EVO-2.* §3.4 says only that it inspects the component breakdown [§3.4] (tex:sections/3_new_method.tex:106), yet the p. 46 feedback argues from the implementation, the gating "forcing the practical implementation to move residuals to score-level addition" [p. 46]; whether it reads results only, or code and logs too, and within what bound, is not stated [§3.4] [ours]. Decision forced: the critic's inputs and their bound [ours].
