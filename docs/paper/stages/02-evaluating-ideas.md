# Stage 2 · Evaluating ideas, from subset to full set [§3.2]

Part of [analysis.md](../analysis.md). This file covers the Table 1 rows "Reproduce baseline on subset", "Idea experiment on subset" and "Idea experiment on full-set", and the unified coder A_Coder [Tab. 1] [§3.2] [ours].

- **The diagram's flow.** *Idea h* → *Baseline Coder* → *Subset Coder* → *Subset Critic*, with a two-way edge marked with a question mark to *Subset Engineer*; a ✓ edge to *Full-Set Coder* → *Full-Set Critic*, with the same kind of edge to *Full-Set Engineer*; outputs *Codebase of Idea*, *Good or Bad*, *Results & Lessons* [Fig. 5] (image).
- **Why a subset.** The engine rapidly filters ideas "on representative benchmark slices before allocating compute to full-scale experiments" [§1] (tex:sections/1_introduction.tex:16).

### Reproduce baseline on subset [Tab. 1 row "Reproduce baseline on subset"] · P-BASE-1

- **Purpose:** "To establish a reliable reference" [§3.2] (tex:sections/3_new_method.tex:37).
- **Inputs:** G, whose primary experiments are reproduced on "the benchmark subset" [§3.2] (tex:sections/3_new_method.tex:37); the subset is not defined (U-BASE-1) [ours].
- **Outputs:** E_base, the baseline results, and C_base, "a reproducible subset codebase" [§3.2] (tex:sections/3_new_method.tex:37); read by the Subset Coding Agent, which modifies C_base, and by the Subset Critic, which compares with E_base [§3.2] (tex:sections/3_new_method.tex:40-41).
- **Agents:** Baseline Coding Agent [§3.2]; *Baseline Coder* [Fig. 5] (image); absent from Figure 3 [Fig. 3] (image); model AMBIGUOUS (A-CFG-1) [App. A.2] [§4.2].
- **Steps:**
  1. P-BASE-1: G and the subset → Baseline Coding Agent → E_base, C_base [§3.2] (tex:sections/3_new_method.tex:37).
- **Loop:** none; the row's critic and refine are both empty [Tab. 1].
- **Stopping rule:** one invocation [Tab. 1] [ours].
- **On exhaustion:** not applicable [Tab. 1] [ours].
- **On failure:** UNSPECIFIED (U-BASE-2) [§3.2].
- **Placement:** once per task by §3.2, or inside every A_Coder call by Figure 5 (A-BASE-1) [§3.2] [Fig. 5] (image).
- **Gaps:** A-BASE-1, U-BASE-1, U-BASE-2, A-CFG-1 [§3.2].

### Idea experiment on subset [Tab. 1 row "Idea experiment on subset"] · P-SUB-1 … 4

- **Purpose:** screen an idea cheaply against the reproduced baseline before full scale [§3.2] [§1].
- **Inputs:** a candidate h, one of the top-N_0 seeds in round 0 or a member of H_k later [§3.2] (tex:sections/3_new_method.tex:40) [§3.3]; C_base and E_base [§3.2].
- **Outputs:** E_sub^h (the resulting logs), C_sub^h, d^h and r^h [§3.2] (tex:sections/3_new_method.tex:40-41); a `Good` idea's C_sub^h goes to the Full-Set Coding Agent [§3.2] (tex:sections/3_new_method.tex:51); every idea's result joins the traces R_k [§3.3].
- **Agents:** Subset Coding Agent [§3.2], *Subset Coder* [Fig. 5], *Coding Agent* in *Subset Experiment Agent* [Fig. 3] (image), on Claude Code with Opus 4.8 as part of the Idea Experiment Coding Agent [App. A.2] [inferred]; Subset Critic Agent [§3.2], *Subset Critic* [Fig. 5], *Critic Agent* [Fig. 3] (image), on Gemini 3.6 Flash [App. A.2]; Subset Engineering Agent [§3.2], *Subset Engineer* [Fig. 5] (image), model A-CFG-1.
- **Steps:**
  1. P-SUB-1: h and C_base → Subset Coding Agent → E_sub^h, C_sub^h: the engine "leverages a Subset Coding Agent to implement" h by modifying C_base [§3.2] (tex:sections/3_new_method.tex:40).
  2. P-SUB-2: E_sub^h against E_base → Subset Critic → d^h and r^h, a categorical decision with feedback [§3.2] (tex:sections/3_new_method.tex:41).
  3. `Bad`: "If performance is substantially inferior to the baseline", h is discarded [§3.2] (tex:sections/3_new_method.tex:43).
  4. `Good`: if h "consistently outperforms the baseline, it is approved for scale-up" [§3.2] (tex:sections/3_new_method.tex:44).
  5. `Engineer`, P-SUB-3: if h "shows potential but requires hyperparameter tuning or code adjustments", the Subset Engineering Agent refines h and C_sub^h guided by r^h and produces new results [§3.2] (tex:sections/3_new_method.tex:45).
- **Loop:** candidate *Idea, Code, Results*; critic *Is it better than the reproduced baseline?*; refine *Refine idea through engineering* [Tab. 1]; `Good`, `Engineer` and `Bad` map onto accept, refine and reject [Lst. 1] [ours]; limit P-SUB-4 is N_eng [§3.2] (tex:sections/3_new_method.tex:47), set to 2: "If the Idea Critic Agent flags an idea for engineering refinement, we apply engineering techniques for at most two rounds" [App. A.2].
- **Stopping rule:** "This refinement loop repeats until" d^h is `Good` or `Bad`, or N_eng iterations are spent (paraphrase) [§3.2] (tex:sections/3_new_method.tex:47).
- **On exhaustion:** without a `Good`, h "is designated as Bad and pruned", as Listing 1's `None` would do [§3.2] (tex:sections/3_new_method.tex:47) [Lst. 1]; the stated reason is "mirroring practical research settings where unpromising avenues are abandoned after bounded optimization" [§3.2].
- **On failure:** UNSPECIFIED (U-TOP-2) [§3.2].
- **Gaps:** U-SUB-1, the criteria; A-TOP-2, the count; A-CFG-1, the engineer's model [§3.2].

### Idea experiment on full-set [Tab. 1 row "Idea experiment on full-set"] · P-FULL-1 … 3

- **Purpose:** final validation of a `Good` idea "across the entire benchmark suite", which Appendix B calls "the paper's full benchmark grid rather than the single registered split" [§3.2] (tex:sections/3_new_method.tex:51) [App. B] (tex:sections/appendix.tex:238-239).
- **Inputs:** h and C_sub^h of an idea validated as `Good` [§3.2] (tex:sections/3_new_method.tex:51); the reference, *the original SOTA result*, which no stage produces (A-FULL-1) [Tab. 1].
- **Outputs:** E_full^h, C_full^h and a terminal decision d^h [§3.2] (tex:sections/3_new_method.tex:52), returned by A_Coder as E^h, C^h, d^h and r^h [§3.2, Eq. 2]; drawn as *Codebase of Idea*, *Good or Bad*, *Results & Lessons* [Fig. 5] (image).
- **Agents:** Full-Set Coding Agent [§3.2], *Full-Set Coder* [Fig. 5], *Coding Agent* in *Full-Set Experiment Agent* [Fig. 3] (image), on Claude Code [App. A.2] [inferred]; Full-Set Critic Agent [§3.2], *Full-Set Critic* [Fig. 5], *Critic Agent* [Fig. 3] (image), on Gemini [App. A.2]; Full-Set Engineer [§3.2] [Fig. 5] (image), the agent §3.4 "re-engages" as A_FullEng [§3.4], model A-CFG-1.
- **Steps:**
  1. P-FULL-1: C_sub^h → Full-Set Coding Agent → code for the whole suite: it adapts C_sub^h "to run across the entire benchmark suite" [§3.2] (tex:sections/3_new_method.tex:51).
  2. P-FULL-2: full results → Full-Set Critic and Full-Set Engineer → E_full^h, C_full^h: "A Full-Set Critic Agent and Full-Set Engineer perform final validation and engineering against the full benchmark" [§3.2] (tex:sections/3_new_method.tex:52).
  3. P-FULL-3: → the terminal d^h [§3.2] (tex:sections/3_new_method.tex:52).
- **Loop:** critic *Is it better than the original SOTA result?*, refine *Refine idea through engineering* [Tab. 1]; §3.2 lists no verdicts; Figure 5 draws the subset's engineer edge again and outputs *Good or Bad*, so `Good`, `Engineer`, `Bad` [inferred] [Fig. 5] (image); the limit has no symbol, and App. A.2's engineering sentence may or may not cover it (A-FULL-2) [§3.2] [App. A.2].
- **Stopping rule:** not stated beyond the terminal decision (U-FULL-1) [§3.2].
- **On exhaustion:** not stated; `Bad`, by analogy with the subset [inferred] [§3.2] (U-FULL-1).
- **On failure:** UNSPECIFIED (U-TOP-2) [§3.2].
- **Gaps:** A-FULL-1, A-FULL-2, U-FULL-1, A-CFG-1 [§3.2].

### The unified coder A_Coder [§3.2 "Unified Coder Interface"] · P-CODER-1

- **Purpose:** one call runs the subset and full-set rows for one idea: "To streamline subsequent rounds of idea improvement, we abstract this entire idea experiment pipeline into a single high-level Idea Implementer Agent" [§3.2] (tex:sections/3_new_method.tex:55).
- **Signature:** h, E^h, C^h, d^h, r^h = A_Coder(G, h) (paraphrase of Eq. 2) [§3.2, Eq. 2] (tex:sections/3_new_method.tex:56-58); h can return changed, since the engineer refines h itself [§3.2] (tex:sections/3_new_method.tex:45).
- **Names:** Idea Implementer Agent A_Coder [§3.2]; *Implementer* [Fig. 6] (image); Figure 5's caption uses A_Coder "to implement the generated idea through subset testing, critic evaluation, engineering refinement loops, and full-set scaling" [Fig. 5] (tex:figures/method_3_3.tex:4).
- **Inputs outside the signature:** C_base and E_base, which the subset steps need; Equation 2 takes only G and h (A-BASE-1) [§3.2, Eq. 2] [§3.2].
- **Pruned ideas:** what E^h and C^h hold for an idea pruned on the subset is not in the printed text; an unprinted TeX comment (tex:sections/3_new_method.tex:59) says subset or full-set level (paraphrase) (U-CODER-1) [§3.2] [p. 7].
- **Pseudocode:** A_Coder is reconstructed at the top of section 4 of [analysis.md](../analysis.md) [§3.2] [ours].
- **Gaps:** U-CODER-1, A-BASE-1 [§3.2].

## Gaps found here

- **A-BASE-1 · AMBIGUOUS · Is the baseline run once per task or once per idea?** Reading 1, once: the engine "first employs a Baseline Coding Agent" before any idea, and Table 1 gives the baseline its own row [§3.2] (tex:sections/3_new_method.tex:37) [Tab. 1].
  - Reading 2, per idea: Figure 5 starts from *Idea h* and runs *Baseline Coder* before *Subset Coder*, and A_Coder takes only G and h although the subset steps need C_base and E_base [Fig. 5] (image) [§3.2, Eq. 2].
  - Decision forced: where the baseline runs; per idea it adds up to 9 coding sessions to a run (section 9 of analysis.md) [ours].
- **U-BASE-1 · UNSPECIFIED · The benchmark subset.** §3.2 says only "the benchmark subset" and §1 "representative benchmark slices"; who picks it, how, how large, and whether it stays fixed are not stated [§3.2] (tex:sections/3_new_method.tex:37) [§1] (tex:sections/1_introduction.tex:16). Decision forced: a subset definition per task [ours].
- **U-BASE-2 · UNSPECIFIED · A baseline that will not reproduce.** The row has no critic and no refine [Tab. 1], and §3.2 does not say what happens when the SOTA cannot be reproduced, or lands far from its paper's numbers [§3.2]. Decision forced: a check on E_base and a failure branch [ours].
- **U-SUB-1 · UNSPECIFIED · The subset critic's criteria.** The verdicts rest on "substantially inferior", "consistently outperforms" and "shows potential" [§3.2] (tex:sections/3_new_method.tex:43-45); no margin, seed count or test is given, and the comparison is an LLM reading of logs [§3.2]. Decision forced: the critic prompt, and whether a numeric guard backs it [ours].
- **A-FULL-1 · AMBIGUOUS · What the full-set critic compares against.** Reading 1, the reported SOTA: Table 1's critic asks *Is it better than the original SOTA result?*, against the subset row's *reproduced baseline*, and no stage reproduces the baseline on the full set [Tab. 1] [§3.2].
  - Reading 2, a reproduced full-set baseline: each system's Δ is "self-reported by each system against its own reproduced baseline", and "Because each system measures against its own reproduced baseline on different hardware" the two Δ columns are not comparable [App. B] (tex:sections/appendix.tex:263) (tex:sections/appendix.tex:202).
  - Decision forced: the full-set reference, and which stage produces it [ours].
- **A-FULL-2 · AMBIGUOUS · The full-set engineering limit.** §3.2 gives the full-set loop no symbol [§3.2] (tex:sections/3_new_method.tex:52), and App. A.2's limit sentence names an Idea Critic Agent that §3 never names: "If the Idea Critic Agent flags an idea for engineering refinement, we apply engineering techniques for at most two rounds" [App. A.2].
  - Reading 1: it means the Subset Critic, and the full-set loop has no stated limit [§3.2]. Reading 2: it means both critics, so both loops stop at 2 [App. A.2] [Fig. 5] (image).
  - Decision forced: E_f in section 9 of analysis.md [ours].
- **U-FULL-1 · UNSPECIFIED · The full-set verdicts and their effects.** §3.2 gives only a terminal decision; the verdict set, what `Bad` at full scale does, and the exhaustion rule come from the diagram alone, *Good or Bad* with an engineer loop [§3.2] (tex:sections/3_new_method.tex:52) [Fig. 5] (image). Decision forced: the full-set vocabulary; we read it as the subset's [ours].
- **U-CODER-1 · UNSPECIFIED · What A_Coder returns for a pruned idea.** Equation 2 returns E^h and C^h for every idea; for one pruned on the subset the printed text does not say whether they are the subset outputs or empty, and only an unprinted TeX comment (tex:sections/3_new_method.tex:59) says subset or full-set level (paraphrase) [§3.2, Eq. 2] [p. 7]. Decision forced: the trace record of a pruned idea, which A_Evolve reads [§3.3] [ours].
