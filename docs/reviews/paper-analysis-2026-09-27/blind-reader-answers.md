# Blind-reader answers (2026-09-28)

- **Reader:** a `technical-writer` persona with no context on this project.
- **What it could read:** only a copy of `docs/paper/` taken at commit `9e685b9`, with `source/`
  removed, so no text of the paper was reachable.
- **Questions and marking:** in [blind-reader-quiz.md](blind-reader-quiz.md).
- **Record:** the reader's final message, verbatim below, with one change. Under "Files opened" it
  named the folder of the copy by an absolute path, shortened here to `<quiz copy of docs/paper>/`,
  because this repository never holds a path from someone's machine.

---

**Blind-reader test: the ScientistTwo analysis folder, read alone**

All 28 questions could be answered from the folder, but two things would mislead a builder:
- **The documents disagree on which stage matches Listing 1** (Q25). analysis.md says no stage matches it exactly; note-check.md, unspecified.md and traceability.md say the subset stage does.
- **analysis.md's minimum session count covers only tasks that succeed.** The true minimum is in note-check.md alone (Q27).

"L" means line numbers in the named file.

**Answers**

1. **Input and output.** The engine turns one problem G into a paper and a codebase: (P+, C+) = A(G), where A is a set of N_a agents. In every experiment G is an accepted paper's problem specification plus its codebase. The abstract and Fig. 3 present G as a plain-language challenge instead (A-TOP-4, AMBIGUOUS), and what G contains is unspecified (U-TOP-1). At export P+ is the final manuscript P_new and C+ the best codebase C_best; a run with no `Good` idea produces nothing, and one run's output can be the next run's G. *analysis.md §2 (L35–62), L298.*

2. **The primitive.** `stage(candidate, critic, refine, max_rounds)`: each round the critic returns a verdict and feedback. `"accept"` returns the candidate, `"refine"` replaces it with `refine(candidate, feedback)`, and any other verdict returns `None`. When `max_rounds` runs out it returns `None` (discarded), even straight after a `"refine"`, so the last refinement is never judged. *analysis.md §3.1 (L66–87).*

3. **Table 1 rows.** No critic: "Reproduce baseline on subset" and "Initial drafting". A critic but no refine agent: "Select best idea". *analysis.md §3.2 (L97, L101, L103); note-check.md L250 agrees.*

4. **Limitation extraction.** At most 16 rounds (App. A.2); §3.1 gives the limit no symbol. What happens at the limit is unstated (A-LIM-1, AMBIGUOUS): the documents read it as passing the set found so far to idea generation [inferred], where Listing 1 would return `None`. What the 16 counts is A-TOP-2: the pseudocode allows 16 Verifier calls, so the 16th expansion is never judged, while the decision register (unspecified.md) proposes 16 judged refinements. *stages/01 (L20–22, L46–49); analysis.md L173–178, L251; unspecified.md L89.*

5. **Seed ideas.** They are sorted by novelty score, highest first. The Novelty Checker (Gemini 3.6 Flash) scores each idea against two reference papers found through Google Search; the score's scale and the search query are unspecified (U-SEED-2). The number of seeds, N_seed, has no value (U-SEED-1); the register proposes at least N_0 + K·N_e = 6. *stages/01 (L26–39, L51–55); unspecified.md L163.*

6. **Subset critic.** It returns `Bad`, `Good` or `Engineer`, each with feedback r^h.
   - `Bad` ("substantially inferior"): the idea is pruned.
   - `Good` ("consistently outperforms"): the idea goes to the Full-Set Coding Agent.
   - `Engineer` ("requires hyperparameter tuning or code adjustments"): the Subset Engineering Agent refines h and its code, then the critic judges again.

   Every idea's result joins the traces. *stages/02 (L31, L34–41).*

7. **Engineering limit.** N_eng = 2 ("at most two rounds"). Running out without a `Good` means the idea "is designated as Bad and pruned". Whether the same limit covers the full set is AMBIGUOUS (A-FULL-2): §3.2 states no full-set limit, and App. A.2's sentence names an "Idea Critic Agent" that may be the subset critic alone or both critics. The register proposes 2 for both. *stages/02 (L39–41, L87–89); unspecified.md L109.*

8. **What the critics compare against.** The subset critic compares E_sub^h (the idea's subset results) with E_base (the baseline reproduced on the subset). The full-set critic compares with "the original SOTA result" (Table 1), which no stage produces. Whether that means the published numbers or a reproduced full-set baseline is AMBIGUOUS (A-FULL-1); the one artifact recomputes a weaker baseline inside the idea's own script (FPR95 4.17 against the published 3.76). *stages/02 (L35, L48, L83–86); analysis.md L161; unspecified.md L96.*

9. **Ideas per round.** Each refinement round (k ≥ 1) evaluates two ideas: one evolved by A_Evolve from all earlier traces (`Good` results and `Bad` failure logs alike), and the next highest-ranked unevaluated seed. Round 0 runs the top N_0 seeds, and N_0 has no value (A-EVO-1, AMBIGUOUS): 2 if App. A.2's "two candidates" describes only the rounds after round 0, 1 if round 0 runs only the seed half. The register proposes 2. *stages/03 (L18–24, L49–53); unspecified.md L110.*

10. **K and S.** K is the number of refinement rounds and S the number of `Good` ideas that stops them early; both are 4. Whether the four rounds include round 0 is AMBIGUOUS (A-EVO-2). The documents take round 0 plus 4, so at most 5 rounds, because Fig. 9 labels "Initial" and "Round 1" to "Round 4", and 4 of 49 tasks picked their best idea in Round 4 (D-1). When the S test runs is unspecified (U-EVO-1). *stages/03 (L24–26, L54–58); unspecified.md L256–262.*

11. **End of the last round.** With no success, the engine "terminates the entire process" and exports nothing [inferred]; what it records is unspecified (U-EVO-4). With two successes S is not reached, so the rounds run to K and the Selector then chooses between the two. *stages/03 (L27, L61); analysis.md L200–208.*

12. **Choosing the best idea.** The Selector Agent, an LLM on Gemini 3.6 Flash, chooses. It receives G and each `Good` idea's idea, results and code, all "evaluated on the full benchmark", and it "compares performance metrics and execution logs". Its criterion is unspecified (U-SEL-1): no rule for trading off datasets or metrics, no tie-break, no weight for novelty. *stages/03 (L31–39, L62).*

13. **Ablation critic.** It returns `Good` or `Refine`, with a critique (App. B adds a rejection; see Q14). One ablation-driven refinement is allowed (N_abl = 1). On `Refine`, the full-set engineer A_FullEng produces a new idea, results and code. The new state replaces the best "if and only if" the Result Comparison Agent prefers the new results over the best ones, and the ablation then re-runs on the new best idea. Whether "strictly outperforms" is a numeric test is AMBIGUOUS (A-ABL-3); whether the new results must also pass a full-set critic is unspecified (U-ABL-2). *stages/04 (L19–28, L46–51).*

14. **Outright rejection.** Yes, once. In App. B, DMC-TeCh beat the baseline on 5 of 6 metrics, "but the ablation critic rejected it" (the gain came from EMA and label smoothing), and that task produced no paper. RALI's rejection names no critic, so it is not counted (D-6). §3.4's two verdicts therefore contradict App. B (A-ABL-1, INCONSISTENT): either a third `Reject` verdict ends the task, or a `Refine` with the budget spent does. *stages/04 (L31, L36–40); unspecified.md L97, L298–304.*

15. **Review–rebuttal loop.** It stops when ScholarPeer's score reaches 8, or after N_peer = 2 rounds. Whether N_peer counts reviews or rebuttal cycles is AMBIGUOUS (A-PEER-1); Table 5 favours cycles. One cycle runs:
    1. Rebuttal Planner: turns the review into tasks.
    2. Rebuttal Coding Agent: runs each task on the best codebase.
    3. Paper Enhancer: revises the manuscript.
    4. Peer Reviewer: reviews it again.

    *stages/05 (L34–43, L53–56).*

16. **Reviewers.** ScholarPeer is used inside the loop, "as it is also used to refine the draft quality". The Stanford Agentic Reviewer is held out, "unseen during development". *analysis.md L415; claims.md L123–126.*

17. **Meta-reviewer.** It returns `Accept` or `Refine`, with a critique, and cannot reject. One meta-driven refinement is allowed (N_meta = 1). If the Result Comparison Agent does not find the refined results "strictly superior", the refinement is discarded and the engine exports "the previous best outputs". That exported paper is one the meta-reviewer had just sent back with `Refine`, which contradicts §3's "until the manuscript is approved" (A-TOP-3, INCONSISTENT). *stages/06 (L15–29); analysis.md L496–498.*

18. **What re-runs after a meta refinement.** §3.6 lists "ablation planning, ablation execution, manuscript re-drafting, and simulated peer-review cycles". Whether the ablation critic re-runs too is AMBIGUOUS (A-META-1); the documents re-run the whole pass, ask the meta-reviewer again (A-META-2) and reset the loop budgets (U-META-1). Limitations, seed ideas, the baseline, the idea rounds and selection never re-run. *stages/06 (L22, L35–43); analysis.md L265.*

19. **Models.** App. A.2 runs four named agents on Claude Code with Opus 4.8 and everything else on Gemini 3.6 Flash.
    - Claude Code: the subset and full-set coders, the ablation coder and the rebuttal coder [inferred], and the Paper Enhancer.
    - Gemini: the limitation, idea, novelty, critic, evolver, selector, comparison, drafter [inferred] and meta-review agents.
    - AMBIGUOUS (A-CFG-1, open per D-7), because §4.2 uses Claude Code "whenever coding capabilities are required": the baseline coder, both engineers including A_FullEng, both planners, and the integrity Coding Agent.

    ScholarPeer's model is not stated. *analysis.md L345–378, L516–520; unspecified.md L306–312.*

20. **Integrity mechanisms.** None is enforced by the setup: no sandbox, hash or locked harness.
    1. Score verification: a prompt, during experiments, asking for reproducible scripts.
    2. Specification compliance: an LLM filter that discards rule-breaking solutions "immediately after experimentation"; which experiments is unspecified (U-INT-1).
    3. Reference verification: a search-augmented LLM flags bad citations, and the Writer Agent fixes the bibliography.
    4. Method–code alignment: the Coding Agent audits code against the paper, and the Writer Agent fixes the paper, not the code.

    When checks 3 and 4 run is unspecified (U-INT-3). The integrity audit behind Table 7 is post-hoc, and App. B's claim of built-in re-run gates contradicts §4.2 (A-INT-1). *stages/07 (L7–8, L26–33, L55–59).*

21. **The subset.** Almost nothing is said. §3.2 names "the benchmark subset", and §1 calls it "representative benchmark slices" used to screen ideas. Who picks it, how large it is and whether it is fixed are unspecified (U-BASE-1). *stages/02 (L8, L13–14, L79); note-check.md L87.*

22. **How gains were computed.** Gemini 3.6 Flash parsed each generated paper's main tables 10 times, and the results were averaged. So the gains were read out of the system's own papers, not computed by a harness. The per-paper formula is unspecified (U-EVAL-1) and the baseline ambiguous (A-EVAL-2); on one task the choice of rule alone moves the gain more than 100-fold. Table 4's figures cover successful tasks only. *claims.md L83–97, L212–221.*

23. **Selection data versus reported data.** They are never separated. No stage names a data split, so the critics, the Selector and both improvement checks read the benchmark that is later reported (U-TOP-5). *analysis.md L289, L510–512; note-check.md L171.*

24. **Loop limits.**

    | Symbol | Value |
    |---|---|
    | none (limitation rounds) | 16 |
    | N_eng | 2 |
    | N_k | 1 |
    | N_e | 1 |
    | K | 4 |
    | S | 4 |
    | N_abl | 1 |
    | none (review score threshold) | 8 |
    | N_peer | 2 |
    | N_meta | 1 |
    | N_seed | unspecified |
    | N_0 | unspecified |
    | N_p | unspecified (Table 15 reports 5–6) |
    | N_t | unspecified |
    | none (full-set engineering) | 2, or unset (A-FULL-2) |

    What each limit counts is AMBIGUOUS (A-TOP-2). D-4 settles that the engineering, ablation and meta limits count refinements, and the limitation and review limits count rounds. *analysis.md §6 (L317–341); unspecified.md L282–288.*

25. **One primitive?** Yes, in the documents' reading: §3 abstracts "all stages" with Listing 1. analysis.md sets these per stage: the generator, what is judged and what is refined, the assessor and its rule, the verdict map, an optional guard with its failure branch, the limit and what it counts, the exhaustion policy, and nesting and fan-out.

    **CONFLICT** on which stage matches Listing 1 as printed. analysis.md says none: the subset stage is closest, but its critic also reads E_base and its limit counts refinements, and its earlier "exact fit" label is withdrawn. note-check.md calls the subset row "the one exact fit", and unspecified.md and traceability.md's P-TOP-2 row repeat it. *analysis.md L18, L109, L139–140; note-check.md L26, L241, L250; unspecified.md L69, L126; traceability.md L127.*

26. **State that outlives its stage.**
    - Outlives its stage: the best idea, results and code (h_best, E_best, C_best); the seed pool and its record of seeds tried; the baseline; the append-only traces; the last ablation results, manuscript and review.
    - Lasts the whole run: G, the evaluation protocol, and the chain of code versions.

    The paper itself fixes only the evaluation protocol as unchangeable ("forbidden (audit)", enforced by audit, not by the setup). The documents add, as their own reading: G, the baseline, the traces, the sorted pool, past code versions, and the exported paper and code. The best state changes only through the comparison check. *analysis.md §8 (L436–454).*

27. **Coding sessions per task.**
    - At most 68 + 4N_p + 4N_t, or 76 + 4N_p + 4N_t if the two planners count as sessions. This assumes N_0 = 2, one baseline run, a full-set limit of 2, and budgets reset for the meta pass; the open readings span 97–127 at N_p = 6 and N_t = 3.
    - At least 10 (N_0 = 1) or 11 (N_0 = 2), for a task whose every idea fails its first subset run (note-check.md L260).
    - A task that succeeds needs at least 14, or 15 at N_0 = 1 with an end-of-round stop test, plus 2 if the integrity checks count as sessions (analysis.md L476).

    The count leaves out integrity sessions, every non-coding LLM call, and any full-set loop inside A_FullEng. The paper never defines a session (U-CFG-2). *analysis.md §9 (L458–478); unspecified.md L264–272.*

28. **Last, best or neither at the limit.** It depends on the stage, and the paper is INCONSISTENT here (A-TOP-1, which includes U-TOP-7, last or best).
    - Neither: Listing 1 and the subset stage discard the candidate as `Bad`, and the documents infer the same for the full set.
    - The last: the limitation loop passes on its last set [inferred], and peer review keeps the last manuscript, not the best-scoring one.
    - The best: ablation and meta-review keep the best state through their comparison check [inferred].
    - Idea evolution keeps its `Good` ideas, or ends the run if there are none.

    *analysis.md L125–135, L486–492, L514–515; unspecified.md L88.*

**Files opened**

All 19 files, each read in full; no other path. They are all under `<quiz copy of docs/paper>/`:
- README.md, analysis.md, claims.md, note-check.md, artifacts.md, unspecified.md, traceability.md
- stages/01-seed-ideas.md, 02-evaluating-ideas.md, 03-refining-ideas.md, 04-ablation.md, 05-drafting-peer-review.md, 06-meta-review.md, 07-integrity.md
- claims/headline.md, main-results.md, ablations.md, discussion.md, appendix-b.md

**Ratings for a builder**

- **README.md:** its map of which file owns which ID key made finding answers fast, but it holds no content about the engine.
- **analysis.md:** the backbone. Its per-stage table, pseudocode, limits table and state table answered about 15 questions. It is hard going, because every line mixes the paper's words with [inferred] and [ours]. Its minimum session count covers only successful tasks, and it contradicts three files on the "exact fit".
- **stages/01:** a clean template; Q4 and Q5 were quick.
- **stages/02:** the most valuable file (Q6–Q8, Q21), with both full-set ambiguities written out in full.
- **stages/03:** answers Q9–Q12 directly, but keeping N_0 (A-EVO-1) apart from K (A-EVO-2) takes care.
- **stages/04:** answers Q13 and Q14 directly; the TeCh contradiction is clear.
- **stages/05:** answers Q15 directly, including the order of the rebuttal cycle.
- **stages/06:** answers Q17 and Q18; its three restart ambiguities are cleanly separated.
- **stages/07:** its enforcement table answered Q20 in one read.
- **claims.md:** its sections on how the paper measures gains answered Q22 cleanly; the rest covers evaluation, not construction.
- **claims/headline.md:** corroborated Q22 only.
- **claims/main-results.md:** not needed.
- **claims/ablations.md:** only C-ABLX-1 (the round labels behind K) matters.
- **claims/discussion.md:** not needed.
- **claims/appendix-b.md:** corroborated TeCh only.
- **unspecified.md:** needed to see which reading the documents adopt, and to reconcile the two session bounds (D-2). It is long, and it repeats the "subset only" fit that analysis.md withdrew.
- **traceability.md:** adds nothing a builder needs. Its P-TOP-2 row carries the withdrawn "exact fit", and its P-ROSTER-16 row puts the Ablation Planner on Claude Code [inferred], where D-7 leaves both planners open.
- **note-check.md:** special cases B (Listing 1 against each row) and C (the session arithmetic, and the only minimum for a failing task) were the best cross-checks, but it still says "the one exact fit".
- **artifacts.md:** evidence only (Q8's weaker baseline, Q23's use of test data during the search); long, mostly read from images, and not needed for how the loops work.
