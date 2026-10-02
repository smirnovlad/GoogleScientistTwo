# Review: system-architect, wave 2, the engine analysis (2026-09-27)

- **Reviewed:** `docs/paper/analysis.md` and `docs/paper/stages/01-seed-ideas.md` to
  `07-integrity.md`, at commit `13477a0`.
- **Lens:** what the next change costs, and whether a crashed multi-day run resumes. The analysis is
  the input to TODO task 3.
- **Record:** the reviewer's final message, verbatim below, with one change: it named the reviewed
  file by an absolute path, shortened here to `docs/paper/analysis.md`, because this repository never
  holds a path from someone's machine.

---

**Verdict.** The control flow in analysis.md §4 is correct, so task 3 can use it as written. Two parts are not ready yet: the conclusion about the stage primitive (§3.3) and the state summary (§8). Unless stated otherwise, line numbers refer to `sections/3_new_method.tex`.

**What I read.** `docs/paper/analysis.md` and `stages/01` to `07`. I checked them against the TeX: §3, Listing 1, Table 1, appendix.tex:155 and lines 170–300, §4.2 and §4.3. I also rendered Figures 3–7, 9 and 10 and read them as images.

**What is right**
- The control flow in §4 matches §3, Listing 1, Table 1, App. A.2 and Figures 3–7. No step is misplaced and no loop is wrong.
- Both restarts go back to ablation planning. Figure 7 draws this with its ✓ edge, and Figure 3 with the line along its bottom.
- The loop limits in §6 are correct, and the arithmetic in §9 checks out.

## BLOCKER

**B1 · analysis.md §3.3: "Does one primitive cover every row? No", and "a family resemblance, not a contract".**
- **Problem.**
  - The evidence given for each row is right, but the conclusion does not follow from it. Every way a stage differs from Listing 1 is a parameter value.
  - As written, the conclusion pushes task 3's first design decision toward one loop per stage. A new limit or a new stage would then mean changing code.
  - The line "A different shape, SPECIFIED as such" is our reading, not the paper's. The paper says the opposite.
- **Evidence.**
  - The paper says "we abstract all stages" "using the Python-style pseudocode in Listing" 1 (tex:sections/3_new_method.tex:5).
  - Figure 7 (image) draws the same sub-graph twice, once for ablation and once for meta-review: critic ✗ → Full-Set Engineer → Result Compare, then ✓ back to *Best Idea* and ✗ onward.
  - The text names the same agents in both places (lines 108/112 and 144/147).
- **Fix.** Replace the conclusion with a table that has one row per stage and these columns:
  - the generator;
  - what the critic judges, as distinct from what gets refined. Ablation and meta-review refine h_best, then regenerate the thing the critic judges;
  - the assessor and its decision rule: score ≥ 8 for peer review, N_seed reached for seeds, number of Good ideas ≥ S for evolution;
  - the verdict map;
  - the guard, and what happens when it fails (exit and keep the current best);
  - what a limit counts (A-TOP-2), and the limit itself;
  - what happens when the limit is reached:
    - subset: discard;
    - peer review: keep the last candidate;
    - limitations: keep the last candidate [inferred];
    - ablation and meta-review: keep the current best;
    - evolution: keep if there is at least one Good idea, otherwise stop the run;
  - nesting and fan-out.
- **A gap nobody has recorded.** A-TOP-1 says "the last or best candidate passes on", which merges two different policies. Peer review overwrites P_new ("The updated manuscript is re-evaluated by", line 131). The exported paper can therefore score lower than one from an earlier round.

## MAJOR

**M1 · analysis.md §8: "What persists across stages [ours]" is wrong, and it leaves out facts about state.**
- **Things that cross stages and are missing from the list.** The list says only the core state crosses. Four more things do:
  - H_0, its scores, and a record of which seeds have been used go into every round ("highest-ranked unevaluated seed ideas", line 76).
  - C_base and E_base go into every call to A_Coder (lines 40–41).
  - The codebase C^h of every Good idea must be kept until selection [§3.3, Eq. 4].
  - The "diagnostic failure logs" of Bad ideas feed A_Evolve (line 68).
- **Implied: codebases are copied, never edited in place.**
  - The state is updated "if and only if" the new result is preferred (line 112). Otherwise the engine "terminates the process using the previous best outputs" (line 150).
  - So neither A_FullEng nor the ablation coder can edit C_best directly.
  - The codebases form a chain of versions. The paper names seven: C_base, C_sub^h, C_full^h, C^h, C_best, C_new and C+.
- **The evaluation protocol is read-only.** Table 15 marks changing it "forbidden (audit)" (tex:sections/appendix.tex:186). App. B lists a "protocol-immutability audit (I2)". §8 folds the protocol into G.
- **How finely to checkpoint.**
  - Initial Implements and Idea Refinement both run inside A_Coder. Together they take 63.9% of the time and 65.5% of the cost [Fig. 10b] (image).
  - A run takes 2.51 days on average, and 6.1% of runs take 5 days or more [Fig. 10a].
  - These figures are in claims.md, but analysis.md does not link to them.
- **No IDs.** None of the objects in §8 has a P- ID, although the README reserves P- IDs for "a data object". Without IDs, the artifact schemas cannot be traced back to the paper.
- **Fix.**
  - Add a table of what crosses stages, giving each object's P- ID, producer, consumers, lifetime, and whether it can change.
  - Record the copy-not-edit point as [inferred].

**M2 · §1.1 item 2 and the §4.2 "Consequence" settle A-ABL-3 without saying so.**
- **Problem.**
  - They state "Every performance comparison is an LLM judgment" and "No gain is computed inside the loop".
  - The paper speaks of "strictly outperforms" (line 111) and "verified as strictly superior" (line 148), which suggests a numeric test.
  - §10.2 still lists A-ABL-3 as open.
- **Why it matters.** This comparison decides which numbers get exported. Our own rule, "Gains are computed deterministically from the result files", favours the numeric reading.
- **Fix.** Mark both places AMBIGUOUS and point them to A-ABL-3.

## MINOR

- **m1 · §4, `sufficient, missing = limitation_verifier(G, L)`.**
  - In the paper it is the Extractor that "again identifies missing limitations" (line 22), not the Verifier.
  - **Fix:** have the Verifier return a verdict and feedback [inferred from Lst. 1].
- **m2 · §4 counts its limits two different ways.**
  - The limitation loop counts critic calls, so its 16th expansion is never judged.
  - The other loops count refinements, which allows N+1 critic calls.
  - "Reading choices" records only the second way.
- **m3 · §3.1 includes E_best in the references that critics read.** No critic reads E_best; the Result Comparison Agent does (lines 111–112 and 147).
- **m4 · §4.1, "Never restarted".**
  - It cites only Figure 7.
  - Figure 3 (image) sends the Analyzer's *New Idea* into the critic of the Full-Set Experiment Agent (U-ABL-2).
  - "Reading choices" leaves out U-ABL-2.
- **m5 · P-CFG-11.**
  - "with review-based refinement conducted at most once" comes right after the peer-review sentence.
  - It can also be read as two reviews and one rebuttal, which would leave N_meta without a value. That reading is not recorded.
  - The analysis's reading is still the better one. Table 5 shows rebuttals in rounds 1 and 2, and the "Review-Driven" headings (lines 134 and 142) point the same way.

## What task 3 needs decided first (this also answers question 4)

1. **The parameters of the stage primitive.** A-TOP-1, A-TOP-2, A-LIM-1, U-FULL-1, A-ABL-2, U-ABL-4 and U-EVO-1 become per-stage data values, not code.
2. **The unit of work and what happens when it fails** (U-TOP-2, U-CFG-2). This unit is what gets checkpointed, retried and costed, and Figure 10b says it must sit inside A_Coder.
3. **Who produces the results E** (A-INT-1). In §3.2 the coding agent produces "the resulting logs", which our harness rule forbids. The answer decides the interface to the coding backend.
4. **Codebase versions, and who may write them:** U-ABL-3, U-PEER-2, U-PEER-4.
5. **The shape of the stage graph:** A-BASE-1, A-FULL-1, U-ABL-2, A-ABL-1.
6. **Restarts, and whether loop counters reset:** A-META-1, A-META-2, U-META-1.
7. **What a task contains:** U-TOP-1, A-TOP-4, U-INT-2, U-BASE-1.
   - It must include the read-only evaluation protocol.
   - The output (P+, C+) must be usable as the next run's input G (tex:sections/5_discussion.tex:9).
8. **Where the integrity checks hook in:** U-INT-1, U-INT-3, A-INT-3.
9. **Pure configuration, decided last.**
   - This covers A-CFG-1, U-CFG-1, U-TOP-4, every count, and the gaps about criteria and prompts.
   - One point from this group must be settled now. App. A.2 runs a writing agent, the Draft Enhancer, on Claude Code. So which backend runs each agent has to be a setting in the routing configuration, not code.
