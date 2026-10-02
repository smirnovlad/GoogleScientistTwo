# Blind-reader quiz for TODO task 1: questions, key, marking and fixes

The reader sees only a copy of docs/paper/*.md, stages/ and claims/, without source/. It never sees
the cache, the web, docs/reviews/ or docs/inputs/. It answers Q1–Q28, citing for each answer the
file and section it used.

Each answer is marked against this key as CORRECT, PARTIAL, WRONG or DOC SILENT. Every PARTIAL,
WRONG or DOC SILENT is a defect in docs/paper/, and is fixed before the task is ticked. A reader who
answers from the paper's text and not from the docs is marked on the docs: an answer the docs do
not give is DOC SILENT, however right it is.

Revised 2026-09-28, after the persona review, so that the key matches the revised documents.
Q25–Q28 were added to test the review's changes: one primitive, state, the session bound, and last
or best at a limit.

## Questions (given to the reader)

1. What does the engine take as input, and what does it produce?
2. State the per-stage primitive of Listing 1, and what it returns when its round limit runs out.
3. Which rows of Table 1 have no critic? Which has a critic but no refine agent?
4. At most how many rounds does limitation extraction run, and what happens when that limit is reached?
5. How are seed ideas ordered? What evidence does the novelty check use? How many seed ideas are generated?
6. What decisions can the subset critic return, and what happens after each one?
7. What is the engineering limit, what happens when it runs out without a Good verdict, and does the same limit apply to full-set engineering?
8. What does the subset critic compare an idea's results against? What does the full-set critic compare against?
9. How many ideas are evaluated in each refinement round, where do they come from, and how many in the initial round?
10. What are K and S, and at most how many experimentation rounds happen in total?
11. What happens if no idea has succeeded when the last round ends? And if two have?
12. Who chooses the best idea, and on what basis?
13. What can the ablation critic return, how many ablation-driven refinements are allowed, and what must happen before a refined idea replaces the best one?
14. Does the paper report the ablation critic rejecting an idea outright? What does that imply for the verdicts §3.4 allows it?
15. What stops the review–rebuttal loop (threshold and limit)? Which agents run in one rebuttal cycle, in order?
16. Which reviewer is used inside the loop, and which one is held out for evaluation?
17. What can the meta-reviewer return, how many meta-driven refinements are allowed, and what happens if the refined idea fails to beat the current best?
18. After a successful meta-driven refinement, which stages run again?
19. Which agents run as Claude Code with Opus 4.8, and which use Gemini 3.6 Flash?
20. Where do the integrity mechanisms of §4.2 act in the pipeline, and how is each one enforced?
21. What does the paper say the "subset" is?
22. How were the reported performance gains computed?
23. Where does the engine separate the data used to select ideas from the data used to report results?
24. List every loop limit with its symbol and value, or say that it is unspecified.
25. Does one primitive describe every stage? If so, what varies from stage to stage, and which stage matches Listing 1 as printed?
26. What state outlives the stage that made it, and which of it must never change?
27. How many coding sessions can one task take, at least and at most, and what does that count leave out?
28. When a stage reaches its limit, does the engine keep the last candidate, the best one, or neither?

## Answer key (never shown to the reader)

1. A scientific problem G; the engine outputs a paper P+ and a reproducible codebase C+ [§3, Eq. 1]. In the experiments G is an accepted paper whose problem specifications and codebases serve as benchmark tasks [§4.1]. What G contains exactly is UNSPECIFIED (U-TOP-1). Full credit also notes that the overview and the abstract present G as a natural-language challenge (A-TOP-4), or that one run's output can be the next run's G (P-TOP-6).
2. stage(candidate, critic, refine, max_rounds): it loops max_rounds times. The critic returns (verdict, feedback); accept returns the candidate, refine replaces it, any other verdict returns None, and after the loop it returns None [Lst. 1]. Full credit also notes that the last refined candidate is never judged.
3. No critic: "Reproduce baseline on subset" and "Initial drafting". A critic but no refine: "Select best idea" [Tab. 1].
4. 16 rounds [App. A.2]. The loop repeats until the Verifier confirms, "or maximum number of iterations is reached" [§3.1]. What passes on at the limit is not stated. The docs infer that the last set passes on (A-LIM-1), where Listing 1 would return None. Full credit also notes the counting question (A-TOP-2): counted as critic calls, the 16th expansion is never judged.
5. By novelty score, in descending order [§3.1]. The novelty check uses two reference papers retrieved via Google Search [App. A.2]. N_seed has no value: UNSPECIFIED (U-SEED-1).
6. Bad → pruned. Good → scaled to the full set. Engineer → the Subset Engineering Agent refines h and C_sub^h, guided by r^h, and re-runs [§3.2].
7. At most two rounds [App. A.2]; on exhaustion without Good, h is designated Bad and pruned [§3.2]. Whether the limit also bounds full-set engineering is AMBIGUOUS (A-FULL-2): §3.2 names no full-set limit, and App. A.2's "Idea Critic Agent" matches neither critic's name exactly.
8. Subset: E_base, the baseline reproduced on the subset [§3.2] [Tab. 1]. Full set: "the original SOTA result" [Tab. 1], which no stage that §3 describes produces (A-FULL-1). Full credit also notes that the one artifact shows the idea's own script recomputing the baseline, and that the weaker reproduction inflates the gain [p. 41] [p. 42].
9. Two per round: the next highest-ranked unevaluated seed idea and one evolved idea [§3.3] [App. A.2]. Round 0 runs the top N_0 seeds, and N_0 has no value: AMBIGUOUS, 1 or 2 (A-EVO-1).
10. K = 4 refinement rounds after round 0, and S = 4 successes [App. A.2], so at most 5 rounds in all. Figure 9's axis reads Initial, Round 1–4 (A-EVO-2). When the S test is checked, after each idea or at the end of a round, is U-EVO-1.
11. Zero successes after round K: the whole process terminates, with no paper [§3.3]. One or more: the Selector picks among the Good ideas [§3.3].
12. The Selector Agent, an LLM. It compares performance metrics and execution logs across the Good ideas, evaluated on the full benchmark [§3.3, Eq. 4]. Its criterion is UNSPECIFIED (U-SEL-1).
13. Good or Refine [§3.4]; at most one refinement [App. A.2]. The Result Comparison Agent must prefer E_new over E_best, and then ablation re-runs on the new candidate [§3.4]. Whether "strictly outperforms" is a numeric test or an agent's preference is AMBIGUOUS (A-ABL-3).
14. Yes: TeCh, rejected because its gain came from general training controls [App. B] [Tab. 16]. §3.4 allows only Good or Refine, so the two are INCONSISTENT (A-ABL-1). Full credit also notes that where the critic draws the line between Refine and reject is unspecified (U-ABL-5).
15. A review score of 8 or more, or N_peer = 2 rounds [§3.5] [App. A.2]. One cycle: the Rebuttal Planner forms N_t tasks; the Rebuttal Coding Agent runs them on C_best; the Paper Enhancer revises the draft; the reviewer re-scores [§3.5]. Full credit also notes that at the limit the last manuscript is kept, not the best-scoring one (U-TOP-7).
16. ScholarPeer inside the loop; the Stanford Agentic Reviewer held out [§4] [fn. 1].
17. Accept or Refine [§3.6]; at most one refinement [App. A.2]. If the refined result is not strictly superior, the refinement is discarded and the run exports the previous P_new, the one the meta-reviewer had just sent back, with C_best [§3.6] (A-TOP-3).
18. Ablation planning, ablation execution, re-drafting, and the peer-review cycles [§3.6].
19. Claude Code with Opus 4.8: the Idea Experiment Coding Agent, the Ablation Study Agent, the Rebuttal Agent and the Draft Enhancer. Gemini 3.6 Flash: every other agent [App. A.2]. How these names map onto §3's agents is AMBIGUOUS (A-CFG-1), and §4.2 adds that Claude Code is used whenever coding is required.
20. Score verification is a prompt: the Coding Agent is asked to write self-contained, reproducible scripts. Specification compliance is an LLM filter that discards rule-breaking solutions after experiments. References: a search-augmented LLM flags hallucinated citations, and the Writer Agent fixes them. Method–code: the Coding Agent audits and the Writer Agent fixes the paper, not the code. The post-hoc CoE audit behind Table 7 follows ScientistOne, by reference. Nothing is enforced by the setup, and none of these steps appears in §3 or Table 1; where each sits is U-INT-1 and U-INT-3 [§4.2].
21. Nothing precise: a "benchmark subset" [§3.2]. UNSPECIFIED (U-BASE-1). Full credit also notes that the subset's false-negative rate is never measured. *Key corrected after the run:* it also credited the p. 69 *subset test split* as evidence about the subset, but that label belongs to an ablation inside a generated paper (closure-evaluation-integrity-engineer.md, error 3).
22. By parsing the generated papers' main tables 10 times with Gemini 3.6 Flash and averaging [§4.1]. The formula is UNSPECIFIED (U-EVAL-1), and the mean covers successes only. Full credit also notes that the choice of rule alone moves one task's gain more than 100-fold [p. 41].
23. Nowhere (U-TOP-5; also U-NOTE-1 and U-ART-5). Every decision reads the benchmark that is reported, so the gains are measured on the data the search selected on (P-EVAL-2).
24. Limitation rounds, no symbol: 16 (count A-TOP-2). N_seed: unset. Novelty references: 2. N_0: unset, 1 or 2 (A-EVO-1). N_eng = 2, with its full-set scope ambiguous (A-FULL-2). N_k = 1. N_e = 1. K = 4, after round 0. S = 4. N_p: unset (Table 15 gives 5–6 per paper). N_abl = 1. Threshold 8. N_t: unset. N_peer = 2 (A-PEER-1). N_meta = 1. N_a: unset.
25. Yes: one primitive with parameters per stage [analysis §3.4–3.5]; the paper says it abstracts all stages with Listing 1 [§3]. The parameters: the generator; the judged object and the refined object; the assessor and its rule; the verdict map; the guard and its failure branch; the limit and what it counts; the policy at the limit; nesting and fan-out. Listing 1's printed values are the subset experiment's, except perhaps the counting (A-TOP-2). WRONG if the reader says each stage needs its own loop.
26. The core state (h_best, E_best, C_best); the seed pool with a record of the seeds used; the baseline, E_base and C_base; the traces, with every Good idea's codebase and every Bad idea's failure logs; and the last E_abl, P_new and R_new [analysis §8]. Never changed: G, and the evaluation protocol, which is "forbidden (audit)" [Tab. 15]. Codebases are copied, never edited in place [inferred].
27. The ceiling excludes integrity sessions: 68 + 4N_p + 4N_t, or 76 + 4N_p + 4N_t if both planners are sessions. N_p and N_t have no values, so it stays symbolic; at N_p = 6 and N_t = 3 the open readings span 99–127. The floor is 16 at N_0 = 2 and 17 at N_0 = 1, each with 2 integrity sessions [analysis §9]. *Key corrected after the run:* that is the floor for a task that succeeds. A task whose every idea fails at once on the subset takes 10 sessions (N_0 = 1) or 11 (N_0 = 2), which the reader found in note-check.md's special case C and the key had missed. LLM calls (critics, the Selector, the comparison, the meta-review) are not coding sessions.
28. It depends on the stage. The subset experiment discards. Limitations keep the last set [inferred]. Peer review keeps the last manuscript, not the best-scoring one (U-TOP-7). Ablation and meta-review keep the current best, through the guarded update. Evolution keeps its Good ideas, or stops the run if there are none [analysis §3.4].

## The run (2026-09-28)

- **Reader:** a `technical-writer` persona with no context on this project. Its answers are verbatim in
  [blind-reader-answers.md](blind-reader-answers.md).
- **What it saw:** a copy of `docs/paper/` at commit `9e685b9`, with `source/` removed, so the paper's text could not be
  reached from its folder. It reports opening the 19 documents and no other path.
- **Result: 27 of 28 CORRECT, 1 PARTIAL, 0 WRONG, 0 DOC SILENT.** The one PARTIAL is a conflict between the documents,
  not a gap in them.

| Q | Mark | Note |
|---|---|---|
| 1–3 | CORRECT | Q1 and Q2 with full credit |
| 4 | CORRECT | full credit; it also noticed that the register's A-TOP-2 decision counts judged refinements for every limit, where analysis.md reads the limitation loop as counting critic calls. The register's row says so itself, so no fix is needed |
| 5–13 | CORRECT | Q8 and Q13 with full credit |
| 14 | CORRECT | it leaves out U-ABL-5, which stages/04 gives |
| 15–24 | CORRECT | Q17 and Q22 with full credit |
| 25 | PARTIAL | **CONFLICT, defect D1:** analysis.md says no stage takes Listing 1's values exactly, while note-check.md, unspecified.md and traceability.md still called the subset row "the one exact fit" |
| 26 | CORRECT | |
| 27 | CORRECT | more complete than the key. **Defect D2:** analysis.md §9 gave only the floor for a task that succeeds |
| 28 | CORRECT | full credit |

## Defects found, and their fixes

- **D1: "the one exact fit" survived in three documents.** The closure correction of analysis.md (commit `7b0f57d`)
  was not carried to note-check.md (summary item 1, N-3, N-79, special case B and its tally), unspecified.md (A-NOTE-1,
  twice) or traceability.md (P-TOP-2). Each owner corrected its own document.
- **D2: §9 gave only the floor for a task that succeeds.** The analysis owner added the floor for a task that fails,
  10 or 11 sessions.
- **D3: traceability.md's P-ROSTER-16 put the Ablation Planner on Claude Code.** analysis.md makes that conditional,
  and the register's D-7 leaves both planners open. The traceability owner corrected it.

The reader rated `analysis.md` "the backbone", but "hard going, because every line mixes the paper's words with
[inferred] and [ours]". That is the cost of the citation rule, and it is kept on purpose: task 2 reads the analysis
to write requirements, and it must see which statements are the paper's and which are ours.
