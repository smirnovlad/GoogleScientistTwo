# ScientistTwo as a specification: how the engine works

Revised 2026-09-28 after the persona review: fixes F-AN-0 (completed after the closure check), F-AN-1 to F-AN-12, F-AN-14 to F-AN-19 and F-AN-21 to F-AN-31, and the register's F-3, F-4, F-5, F-9, F-16 and F-17, of `docs/reviews/paper-analysis-2026-09-27/fix-list.md`; then the closure corrections from the four `closure-*.md` reports in that folder, and the failed-task floor in section 9 that the blind-reader quiz found missing [ours].

Paper: arXiv:2609.19644v1, *ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI* [Title]. Keys owned here: TOP, LIM, SEED, BASE, SUB, FULL, CODER, EVO, SEL, ABL, DRAFT, PEER, META, INT, CFG, ROSTER [ours].

## 1. Scope and reading guide

- **What this is.** The engine of ScientistTwo written as structure: each stage's inputs, outputs, agents, loop, limit, stopping rule and failure branch, taken from §3, Table 1, Listing 1, Figures 3–7, App. A.2 and §4.2 [§3] [Tab. 1] [Lst. 1] [App. A.2] [ours].
- **What this is not.** The quantitative claims (claims.md), the check of the initial note (note-check.md) and the agents' own outputs in Appendices C–D (artifacts.md) belong to other analysts; numbers from figures and tables appear here only as evidence about the loop structure [ours].
- **Sources.** Quotes and TeX anchors come from `docs/paper/source/` (v1). Numbering, pages and diagram content come from the arXiv PDF. The HTML was used only as a cross-check of App. A.2, Listing 1 and §3.2–§3.6, where it matches the TeX [App. A.2] [Lst. 1] [ours].
- **Numbering.** The stage pseudocode is Listing 1 on p. 5 [Lst. 1] [p. 5]; the HTML names it Listing 4 in the §3 sentence and Figure 4 in its caption, so its numbers are never cited here [ours]. The PDF numbers four equations, cited with their section: Eq. 1 on p. 6 [§3, Eq. 1], Eq. 2 and Eq. 3 on p. 7 [§3.2, Eq. 2] [§3.3, Eq. 3], Eq. 4 on p. 8 [§3.3, Eq. 4] [p. 6] [p. 7] [p. 8].
- **Marks.** SPECIFIED, UNSPECIFIED, AMBIGUOUS and INCONSISTENT as the README defines them; `[inferred]` is a step the paper implies but never states; `[ours]` is our statement; `(image)` is read from a diagram; `(paraphrase)` is our wording where the TeX is math [ours].
- **Layout.** Sections 1–4 and 6–10 are the overview. The stage-by-stage detail is in `stages/` (section 5); each stage file ends with its own gaps in full, and section 10 indexes every gap [ours].

### 1.1 Read this first

1. **Listing 1 is one setting of the stage primitive's parameters.** It returns `None` when `max_rounds` runs out, but most stages keep their candidate at the limit: finding limitations [inferred], ablation, peer review and meta-review (A-TOP-1, A-LIM-1). No stage takes Listing 1's values exactly, the subset experiment included; section 3.4 gives each stage's parameters and section 3.5 the conclusion [Lst. 1] [§3.1] [§3.4] [§3.5] [§3.6] [ours].
2. **No gain formula is specified for any decision in the loop.** Every performance comparison is an LLM judgment, since "ScientistTwo has no target metric" [Tab. 15] (tex:sections/appendix.tex:176), over numbers that agent-written code produced; those numbers may include gains [p. 42] (image) and spreads, such as the reported "+0.61%±0.27" and "+3.4%±0.2" [Tab. 16] (tex:sections/appendix.tex:288) (tex:sections/appendix.tex:311). Besides the loop limits, two fixed numeric tests exist, both applied to LLM output: ScholarPeer's score against 8, and the stop of the idea rounds at S `Good` verdicts or K rounds (section 4.2) [§3.3] (tex:sections/3_new_method.tex:84-85) [§3.5] [App. A.2]. The two update gates are worded as strict tests, and whether they are numeric or an agent's preference is AMBIGUOUS (A-ABL-3) [§3.4] [§3.6] [ours].
3. **The idea rounds are underdetermined at round 0.** §3.3 runs the top-N_0 seeds in round 0; App. A.2 says each round evaluates one seed and one evolved idea, and sets no N_0 (A-EVO-1). K = 4 refinement rounds after round 0 is corroborated by Figure 9's round labels (A-EVO-2) [§3.3] [App. A.2] [Fig. 9] (image).
4. **The ablation stage has an undeclared reject.** §3.4 gives the Ablation Critic only `Good` or `Refine`; Appendix B reports that it rejected an idea and the task yielded no contribution (A-ABL-1). Figure 7 sends a failed comparison straight to drafting (A-ABL-2) [§3.4] [App. B] [Fig. 7] (image).
5. **The baseline has two placements.** §3.2 reproduces it once, first, on the subset; Figure 5 draws the Baseline Coder inside the per-idea pipeline, and A_Coder's signature takes only (G, h) (A-BASE-1) [§3.2] [§3.2, Eq. 2] [Fig. 5] (image).
6. **No stage that §3 describes produces the full-set critic's reference.** Table 1 compares with "the original SOTA result"; the one artifact shows the idea's own script recomputing the baseline, *X-Maha (reproduced)*, beside the paper's numbers, and the reproduction is weaker (FPR95 4.17 against 3.76), so 0.41 of the 1.99 pp claimed gain comes from it (A-FULL-1) [Tab. 1] [p. 41] [p. 42] (image). The full-set engineering limit is unstated (A-FULL-2) [§3.2] [App. A.2] [ours].
7. **Model routing leaves coding agents unassigned.** App. A.2 routes four named agents to Claude Code; §4.2 says Claude Code is used whenever coding is required. The Baseline Coding Agent, both engineers and the integrity Coding Agent fall between the two (A-CFG-1) [App. A.2] [§4.2]. [ours]
8. **The meta-review restarts the downstream at most once, and can export an unapproved paper.** N_meta = 1; a refinement that fails the comparison ends the run with the manuscript the meta-reviewer had just sent back, which contradicts the §3 overview's loop until approval (A-TOP-3) [§3.6] [App. A.2] [§3]. [ours]
9. **Integrity rests on prompts and LLMs only; nothing is enforced by the setup.** §3, §4.2 and App. A.2 describe no sandbox, no read-only evaluation code, no hash and no harness: reproducibility is a prompt to the Coding Agent, while Appendix B calls a reproduction re-run a structural block (A-INT-1), and no fixed evaluator exists (U-INT-4). The specification filter can fail a whole task [§4.2] [fn. 2] [App. B] [ours].
10. **Most counts that set cost are unspecified.** N_seed, N_0, N_p, N_t and the full-set engineering limit have no value, so the coding-session bound in section 9 stays symbolic in N_p and N_t [§3.1] [§3.4] [§3.5] [App. A.2] [ours].

### 1.2 Readings corrected during this analysis

- **Disproved: §3.6 names no limit for the meta-refinement loop.** Verdict: wrong. The sentence introducing N_meta is the last line of `3_new_method.tex`, which has no trailing newline, so a line-range print stopped one line short. It is at (tex:sections/3_new_method.tex:151) and printed on p. 9, and the HTML carries it too [§3.6] [p. 9] [ours].

## 2. Problem setup [§3 "Problem Setup"] · P-TOP-1

- **P-TOP-1, SPECIFIED.** The engine maps one problem to one paper and one codebase: (P+, C+) = A(G), where A is a set of N_a agents (paraphrase of Eq. 1) [§3, Eq. 1] (tex:sections/3_new_method.tex:7-11).
- **The agents.** A comprises "specialized AI agents, each assigned to distinct phases of the research life cycle" [§3] (tex:sections/3_new_method.tex:11). N_a has no value; section 7 counts 24 stage agents and 3 integrity agents [§3] [ours].
- **What P+ must do.** P+ "should identify and resolve key methodological or empirical bottlenecks present in" G [§3] (tex:sections/3_new_method.tex:12).
- **What C+ must do.** C+ "should correctly implement the proposed idea while maintaining execution reproducibility and demonstrating measurable performance gains" [§3] (tex:sections/3_new_method.tex:12).
- **Where they come from.** On acceptance the run exports P+ ← P_new and C+ ← C_best (paraphrase) [§3.6] (tex:sections/3_new_method.tex:140).

### 2.1 What G is, concretely

| Evidence | What it says G contains | Location |
|---|---|---|
| Finding limitations | a human state-of-the-art method whose limitations can be read: "the Limitation Extractor extracts a set of limitations from" G | [§3.1] (tex:sections/3_new_method.tex:19-20) |
| Baseline | runnable experiments: a Baseline Coding Agent is employed "to reproduce the primary experiments of" G on the benchmark subset | [§3.2] (tex:sections/3_new_method.tex:37) |
| Main results | an accepted paper "whose problem specifications and codebases serve as benchmark tasks for" ScientistTwo | [§4.1] (tex:sections/4_experiment.tex:16) |
| Table 3 caption | "The top section evaluates papers accepted at each venue, which serve as inputs for" ScientistTwo | [Tab. 3] (tex:tables/conference_accepted_comparison.tex:3) |
| Benchmark | NeurIPS 2025 tasks: "these papers are drawn from benchmarks used in AutoSOTA"; ICML 2026 tasks were chosen "strictly adhering to AutoSOTA's filtering process" | [App. A.1] (tex:sections/appendix.tex:3) (tex:sections/appendix.tex:74) |
| Spec compliance | task rules: the check "ensures that solution code adheres strictly to task rules without reward hacking" | [§4.2] (tex:sections/4_experiment.tex:41) |
| Iterative expansion | the engine's own output: "When VD-STrans is subsequently provided as context in the next discovery cycle" | [§4.3] (tex:sections/5_discussion.tex:9) |
| Overview diagram | a human request, drawn as *I want to build an efficient tabular foundation model* | [Fig. 3] (image) |
| Abstract | "given a fundamental challenge by a human expert"; the engine "takes an initial problem as input" | [Abstract] (tex:sections/0_abstract.tex:2) |

- **SPECIFIED for the experiments.** G is an accepted paper's problem specification together with its codebase [§4.1] [Tab. 3].
- **AMBIGUOUS in general (A-TOP-4).** The overview diagram and the abstract present G as a natural-language challenge; §3–§4 need a paper and runnable code [Fig. 3] (image) [Abstract] [§4.1].
- **UNSPECIFIED (U-TOP-1).** The concrete contents of G: the paper's form, the codebase's state, the task rules, the reported numbers the full-set critic needs, and the benchmark subset [§3.2] [§4.2] [Tab. 1].

### 2.2 Chained runs · P-TOP-6

- **P-TOP-6, SPECIFIED.** One run's output can be the next run's input: "When VD-STrans is subsequently provided as context in the next discovery cycle", the engine produces BXT-Transducer, and from that SBR-Transducer, three iterations in all [§4.3] (tex:sections/5_discussion.tex:9) [Tab. 9].
- **What it forces [ours].** The task interface must accept a generated (P+, C+) as G, so the output format and the input format are one schema (A-TOP-4, U-TOP-1) [§4.3] [ours].

## 3. The stage primitive · P-TOP-2, P-TOP-3

### 3.1 Listing 1, verbatim [Lst. 1] (tex:tables/pseudo_code.tex:26-35)

```python
def stage(candidate, critic, refine, max_rounds):   # [Lst. 1] (tex:tables/pseudo_code.tex:26)
    for _ in range(max_rounds):                      # [Lst. 1] (tex:tables/pseudo_code.tex:27)
        verdict, feedback = critic(candidate)        # [Lst. 1] (tex:tables/pseudo_code.tex:28)
        if verdict == "accept":                      # [Lst. 1] (tex:tables/pseudo_code.tex:29)
            return candidate
        elif verdict == "refine":                    # [Lst. 1] (tex:tables/pseudo_code.tex:31)
            candidate = refine(candidate, feedback)  # [Lst. 1] (tex:tables/pseudo_code.tex:32)
        else:
            return None                              # rejected: discarded [Lst. 1] (tex:tables/pseudo_code.tex:33-34)
    return None                                      # limit reached: discarded [Lst. 1] (tex:tables/pseudo_code.tex:35)
```

- **P-TOP-2, what Listing 1 fixes.** The caption: "If accepted, the artifact is returned; if rejected, it is discarded; otherwise, it is iteratively refined based on the critic's feedback up to a maximum number of rounds" [Lst. 1] (tex:tables/pseudo_code.tex:23-24).
- **Scope claimed.** The paper abstracts every stage this way, "using the Python-style pseudocode in Listing" 1 [§3] (tex:sections/3_new_method.tex:5).
- **The candidate comes from outside.** `stage` receives a first candidate and only judges and refines it; Table 1's caption adds that a specialized agent generates it [Lst. 1] [Tab. 1] [ours].
- **The critic sees only the candidate.** In §3 the critics also read a reference: E_base (the subset critic), the original SOTA result (the full-set critic) or the review (the meta-reviewer); E_best is read by the Result Comparison Agent, which is a guard, not a critic [Lst. 1] [§3.2] [Tab. 1] [§3.4] [§3.6] [ours].
- **Three outcomes.** `"accept"` returns the candidate, `"refine"` replaces it, any other verdict returns `None` [Lst. 1].
- **Exhaustion discards.** After `max_rounds` critic calls the stage returns `None`, even if the last verdict was `"refine"` [Lst. 1] (tex:tables/pseudo_code.tex:35).
- **The last refinement is never judged.** A `"refine"` in the final round produces a candidate that the loop then drops, so `max_rounds` bounds critic calls and refinements alike (A-TOP-2) [Lst. 1] [ours].

### 3.2 Table 1, row by row, against Listing 1 · P-TOP-3

Table 1's caption: each stage generates a candidate with a specialized agent and "employs a corresponding critic agent to decide whether to accept the output or invoke a refinement agent" [Tab. 1] (tex:tables/overview.tex:3). The table below sets each row's critic against the verdicts §3 gives it and the limits App. A.2 sets [Tab. 1] [§3] [App. A.2].

| Tab. 1 row | candidate · critic · refine (Tab. 1) | Verdicts §3 gives the critic | Limit (§3) · App. A.2 value | What §3 says at the limit | Against Listing 1 · class |
|---|---|---|---|---|---|
| Finding limitations | Set of limitations · *Can guide novel improvement?* · *Add missing limitations* [Tab. 1] | the Verifier confirms the set, or "considers the set insufficient" [§3.1] (tex:sections/3_new_method.tex:22-23) | no symbol, "maximum number of iterations" · 16 rounds [§3.1] [App. A.2] | silent; the next paragraph uses "the identified limitations" [§3.1] | accept and refine fit; no reject verdict; exhaustion unstated where Listing 1 returns `None` · A-LIM-1 [ours] |
| Seed idea generation | Seed ideas · *Is it novel?* · *Add more novel ideas* [Tab. 1] | none: the Novelty Checker returns a score s_i [§3.1] (tex:sections/3_new_method.tex:25) | N_seed, a target count · no value [§3.1] [App. A.2] | the pool is "sorted in descending order according to their novelty scores" [§3.1] (tex:sections/3_new_method.tex:27) | does not fit: a scoring critic and a count stop, no verdicts · A-SEED-1, U-SEED-1 [ours] |
| Reproduce baseline on subset | SOTA baseline result · - · - [Tab. 1] | none [§3.2] | none · none [App. A.2] | n/a | degenerate: one generation, no critic [Tab. 1] [ours] |
| Idea experiment on subset | Idea, Code, Results · *Is it better than the reproduced baseline?* · *Refine idea through engineering* [Tab. 1] | `Bad`, `Good`, `Engineer` [§3.2] (tex:sections/3_new_method.tex:43-45) | N_eng · 2: "at most two rounds" [§3.2] [App. A.2] | h "is designated as Bad and pruned" [§3.2] (tex:sections/3_new_method.tex:47) | closest fit, in our reading [ours]: `Good` = accept, `Engineer` = refine, `Bad` = reject, exhaustion = `None`; but the critic also reads E_base, the engineer rewrites h and C_sub^h behind the judged results, and App. A.2 counts engineering refinements where Listing 1 counts critic calls · A-TOP-2 [ours] |
| Idea experiment on full-set | Idea, Code, Results · *Is it better than the original SOTA result?* · *Refine idea through engineering* [Tab. 1] | only a "terminal decision" [§3.2] (tex:sections/3_new_method.tex:52); Figure 5 outputs *Good or Bad* [Fig. 5] (image) | no symbol · 2 only if A.2's engineering sentence covers it [§3.2] [App. A.2] | silent [§3.2] | the subset's shape by the diagram, which draws the same critic–engineer loop; vocabulary, limit and reference unstated · A-FULL-1, A-FULL-2, U-FULL-1 [Fig. 5] (image) |
| Idea evolution | Evolved idea · *Idea experiment* · *Evolve idea from traces* [Tab. 1] | d^h in {`Good`, `Bad`} from A_Coder [§3.3] (tex:sections/3_new_method.tex:68) | K rounds · 4; S successes · 4 [§3.3] [App. A.2] | zero successes by round K: ScientistTwo "terminates the entire process" [§3.3] (tex:sections/3_new_method.tex:86); otherwise selection | does not fit: a population loop that stops on a count of accepts (S), and whose refine makes new candidates from all traces; a different shape in our reading, not the paper's [§3.3] [ours] |
| Select best idea | Best idea · *What is the best idea from traces?* · - [Tab. 1] | none: a choice among `Good` ideas [§3.3, Eq. 4] | none · none [App. A.2] | n/a | degenerate: one selection call [Tab. 1] [ours] |
| Ablation study | Idea, Ablation results · *Is the component breakdown clean?* · *Refine the method* [Tab. 1] | `Good`, `Refine` [§3.4] (tex:sections/3_new_method.tex:106) | N_abl · 1: "we refine the idea at most once" [§3.4] [App. A.2] | the loop ends "ensuring a fully optimized hypothesis prior to manuscript generation" [§3.4] (tex:sections/3_new_method.tex:114) | deviates: no reject in §3.4, yet Appendix B reports one; the refinement replaces h_best only if the Result Comparison Agent prefers it; exhaustion passes h_best on · A-ABL-1, A-ABL-2, A-TOP-1 [§3.4] [App. B] |
| Initial drafting | Manuscript · - · - [Tab. 1] | none [§3.5] | none · none [App. A.2] | n/a | degenerate: one drafting call [Tab. 1] [ours] |
| Peer-Review | Manuscript · *Is review score good enough?* · *Run rebuttal experiments* [Tab. 1] | a number: s_review in [1, 10] against the threshold 8 [§3.5] (tex:sections/3_new_method.tex:123-124) | N_peer · 2 rounds, early stop at 8 [§3.5] [App. A.2] | "producing a polished, thoroughly validated final manuscript" [§3.5] (tex:sections/3_new_method.tex:132) | deviates: the verdict is a threshold test, there is no reject, and exhaustion keeps the manuscript · A-TOP-1, A-PEER-1 [§3.5] |
| Meta-Review | Manuscript, Review · *Does it meet the venue bar?* · *Refine idea and analyze again* [Tab. 1] | `Accept`, `Refine` [§3.6] (tex:sections/3_new_method.tex:138) | N_meta · 1: "review-based refinement conducted at most once" [§3.6] [App. A.2] | "yielding a rigorously validated final contribution" [§3.6] (tex:sections/3_new_method.tex:151); a failed comparison "terminates the process using the previous best outputs" (tex:sections/3_new_method.tex:150) | deviates: the refine restarts ablation, drafting and peer review; the update is guarded; both a failed comparison and exhaustion export · A-TOP-1, A-META-1, A-META-2 [§3.6] |

### 3.3 How far Listing 1, as printed, covers each row

- **Closest fit, in our reading [ours]:** the subset experiment keeps Listing 1's three verdicts and its discard at the limit, but its critic judges E_sub^h against E_base while the engineer refines h and C_sub^h (tex:sections/3_new_method.tex:45), and App. A.2 counts its limit in engineering refinements where Listing 1 counts critic calls (A-TOP-2) [§3.2] [Lst. 1] [App. A.2]. Our first label, *Exact fit, SPECIFIED*, is withdrawn; verdict: wrong, for these differences [ours].
- **The subset's shape, by the diagram only:** the full-set experiment, whose vocabulary and limit the text omits [§3.2] [Fig. 5] (image).
- **Partial fit:** finding limitations, which has no reject verdict and no stated exhaustion output [§3.1].
- **Degenerate (one call, no loop):** baseline reproduction, best-idea selection and initial drafting [Tab. 1].
- **A different shape, in our reading, not the paper's [ours]:** seed generation (a scoring critic and a count stop) and idea evolution (a population loop stopped by S accepts or K rounds) [§3.1] [§3.3].
- **Different exhaustion, INCONSISTENT with Listing 1 (A-TOP-1):** ablation, peer review and meta-review keep their candidate at the limit where Listing 1 discards it [§3.4] [§3.5] [§3.6] [Lst. 1].
- **Additions Listing 1 lacks, SPECIFIED:** a guarded update (the Result Comparison Agent must prefer the new result) in ablation and meta-review, and a restart of three downstream stages in meta-review [§3.4] [§3.6].
- **Counting, AMBIGUOUS (A-TOP-2):** whether each App. A.2 limit is `max_rounds` itself or the number of judged refinements [Lst. 1] [App. A.2].
- **Withdrawn conclusion [ours].** We first concluded that Listing 1 is *a family resemblance, not a contract*, so that each stage needs its own loop. Verdict: wrong. Every deviation above is a parameter value of one primitive (sections 3.4 and 3.5), and the paper abstracts all stages with Listing 1 [§3] (tex:sections/3_new_method.tex:5) [ours].

### 3.4 The primitive's parameters, per stage [ours]

Each row sets the parameters of one primitive for one Table 1 row; the values come from the paper, and the split into parameters is ours [Tab. 1] [§3] [ours].

| Stage | Generator | Critic judges → what is refined | Assessor and its rule | Verdict map | Guard, and on failure | Limit: what it counts, value | At the limit | Nesting, fan-out |
|---|---|---|---|---|---|---|---|---|
| Finding limitations | Limitation Extractor [§3.1] | the set → the same set, expanded [§3.1] | Limitation Verifier, LLM: is the set sufficient [§3.1] | confirm → accept; insufficient → refine; no reject [§3.1] | none [§3.1] | critic calls, 16 [App. A.2]; A-TOP-2 | keep the last set [inferred] [§3.1]; A-LIM-1 | none [§3.1] |
| Seed idea generation | initial idea generator, then the Idea Generator Agent [§3.1] [Fig. 4] (image) | each new idea → the pool, which grows [§3.1] | Novelty Checker, LLM with two retrieved papers: a score; stop at N_seed ideas [§3.1] [App. A.2] | none: a score, not a verdict; A-SEED-1 [§3.1] | none [§3.1] | pool size N_seed, unset (U-SEED-1) [§3.1] | keep the pool, sorted by score [§3.1] | fan-out: N_seed ideas [§3.1] |
| Reproduce baseline on subset | Baseline Coding Agent [§3.2] | nothing is judged [Tab. 1] | none [Tab. 1] | none: the result is taken as is [Tab. 1] [ours] | none; failure is U-BASE-2 [§3.2] | zero rounds [Tab. 1] [ours] | keep the one result [Tab. 1] [ours] | once per task, or per idea inside A_Coder (A-BASE-1) [§3.2] [Fig. 5] (image) |
| Idea experiment on subset | Subset Coding Agent [§3.2] | E_sub^h against E_base → h and C_sub^h, which regenerate E_sub^h [§3.2] (tex:sections/3_new_method.tex:45) | Subset Critic, LLM [§3.2] | `Good` → accept; `Engineer` → refine; `Bad` → reject [§3.2] | none in §3.2; the specification filter may act after experiments (U-INT-1) [§4.2] | engineering refinements, N_eng = 2 [App. A.2]; A-TOP-2 | discard: pruned as `Bad` [§3.2] | inside A_Coder, once per idea [§3.2, Eq. 2] |
| Idea experiment on full-set | Full-Set Coding Agent [§3.2] | full results against the original SOTA result (A-FULL-1) → h and C [§3.2] [Tab. 1] | Full-Set Critic, LLM [§3.2] | `Good`, `Engineer`, `Bad` [inferred] [Fig. 5] (image) | none [§3.2] | engineering refinements, 2 or unset (A-FULL-2) [App. A.2]; A-TOP-2 | discard as `Bad` [inferred] [§3.2]; U-FULL-1 | inside A_Coder, after a subset `Good` [§3.2] |
| Idea evolution | A_Evolve, plus the next N_e unevaluated seeds [§3.3] | each candidate, through A_Coder → the population, rebuilt from all traces [§3.3] | A_Coder's d^h per idea; stop when the `Good` count reaches S [§3.3]; when the test runs: U-EVO-1 | `Good` → counted; `Bad` → kept as a trace [§3.3] | none [§3.3] | rounds after round 0, K = 4 (A-EVO-2); S = 4 [App. A.2] [Fig. 9] (image) | keep the `Good` ideas; with none, stop the run [§3.3] | A_Coder per candidate, two per round [App. A.2] |
| Select best idea | none: the `Good` tuples of §3.3 [§3.3, Eq. 4] | the `Good` ideas → nothing is refined [Tab. 1] | Selector, LLM: a choice [§3.3] | none: a choice, not a verdict [ours] | none [§3.3] | zero rounds [Tab. 1] [ours] | keep the chosen idea [§3.3, Eq. 4] | once per run [§3.3] |
| Ablation study | Ablation Planner, then one Ablation Coding Agent per plan [§3.4] | E_abl → h_best, through A_FullEng; E_abl is then regenerated [§3.4] | Ablation Critic, LLM [§3.4] | `Good` → accept; `Refine` → refine; a reject only in App. B (A-ABL-1) [§3.4] [App. B] | the Result Comparison Agent must prefer E_new; on failure keep h_best and go to drafting [§3.4] [Fig. 7] (image) | refinements, N_abl = 1 [App. A.2]; A-TOP-2 | keep the current best, h_best [inferred] [§3.4]; A-ABL-2; a `Refine` on the re-ablation once N_abl is spent: U-ABL-4 | fan-out: N_p runs per pass; A_FullEng nested (U-ABL-2) [§3.4] |
| Initial drafting | Initial Drafter, with PaperOrchestra [§3.5] | nothing is judged [Tab. 1] | none [Tab. 1] | none [Tab. 1] [ours] | none; the integrity repairs are U-INT-3 [§4.2] | zero rounds [Tab. 1] [ours] | keep the draft [Tab. 1] [ours] | once per downstream pass [§3.6] |
| Peer-Review | the draft of the row above [§3.5] | P_new → P_new, through rebuttal experiments and enhancement [§3.5] | ScholarPeer's score, tested against 8 [§3.5] [App. A.2] | 8 or more → accept; below 8 → refine; no reject [§3.5] | none: each revision replaces P_new [§3.5] | rounds, N_peer = 2 (A-PEER-1) [App. A.2]; A-TOP-2 | keep the last manuscript, not the best-scoring one (U-TOP-7) [§3.5] | fan-out: N_t rebuttal tasks per round [§3.5] |
| Meta-Review | the peer-review stage's P_new and R_new [§3.6] | P_new and R_new → h_best, then ablation, drafting and review run again [§3.6] | Meta-Review Agent, LLM [§3.6] | `Accept` → accept; `Refine` → refine; no reject [§3.6] | the Result Comparison Agent must find E_new strictly superior; on failure export the previous outputs [§3.6] | refinements, N_meta = 1 [App. A.2]; A-TOP-2 | keep: export the last pass's P_new with C_best [inferred] [§3.6] | its refine nests the three rows above (A-META-1) [§3.6] |

### 3.5 Conclusion: one primitive, with parameters per stage [ours]

- **One primitive covers every row [ours].** Its parameters are the columns above: a generator, the judged object and the refined object, an assessor with its rule, a verdict map, an optional guard with its failure branch, a limit with its counting convention, an exhaustion policy, and nesting and fan-out [Tab. 1] [ours].
- **Listing 1 fixes one set of them [ours].** A generator outside the stage, a critic that reads the candidate alone, which is also what gets refined, three verdicts, no guard, a limit that counts critic calls, and discard at the limit [Lst. 1]. No row takes exactly these values: the subset row, the closest, keeps the three verdicts and the discard at the limit, but its critic judges E_sub^h against E_base while the engineer refines h and C_sub^h (tex:sections/3_new_method.tex:45), and its limit counts engineering refinements (A-TOP-2) [§3.2] [App. A.2] [ours].
- **Why one primitive.** The paper abstracts all stages "using the Python-style pseudocode in Listing" 1 [§3] (tex:sections/3_new_method.tex:5), and Figure 7 draws the same sub-graph twice, for ablation and for meta-review: a critic's ✗ → *Full-Set Engineer* → *Result Compare*, whose ✓ returns to *Best Idea* and whose ✗ goes on [Fig. 7] (image); the text names the same agents in both places [§3.4] (tex:sections/3_new_method.tex:108) (tex:sections/3_new_method.tex:112) [§3.6] (tex:sections/3_new_method.tex:144) (tex:sections/3_new_method.tex:147).
- **Open values become per-stage data, not code [ours].** A-TOP-1, A-TOP-2, A-LIM-1, U-FULL-1, A-EVO-2, U-EVO-1, A-ABL-2, U-ABL-4 and U-TOP-7 each set one cell of the table [ours].

## 4. End-to-end control flow · P-TOP-4

The reconstruction below runs from G to (P+, C+). Every line cites the paper or says `[inferred]`; where the paper allows two readings the line names the gap and takes one reading, which is ours, not the paper's [§3] [ours]. Limits carry their App. A.2 values [App. A.2].

```python
def A_Coder(G, h):                                             # [§3.2, Eq. 2] (tex:sections/3_new_method.tex:55-58)
    # per-idea baseline here if Figure 5 is literal: A-BASE-1 [Fig. 5] (image)
    E, C = subset_coder(h, C_base)                             # [§3.2] (tex:sections/3_new_method.tex:40)
    d, r = subset_critic(E, E_base)                            # Bad, Good or Engineer [§3.2] (tex:sections/3_new_method.tex:41-45)
    eng = 0                                                    # N_eng = 2 [§3.2] (tex:sections/3_new_method.tex:47) [App. A.2]
    while d == 'Engineer' and eng < N_eng:                     # each round judged [inferred] [§3.2]; Listing 1 differs [Lst. 1]: A-TOP-2
        h, E, C = subset_engineer(h, C, r)                     # h may change too [§3.2] (tex:sections/3_new_method.tex:45)
        d, r = subset_critic(E, E_base)                        # [§3.2] (tex:sections/3_new_method.tex:41)
        eng += 1
    if d != 'Good':                                            # Bad, or Engineer at the limit [§3.2] (tex:sections/3_new_method.tex:47)
        return h, E, C, 'Bad', r                               # pruned; subset-level E and C: U-CODER-1 [§3.2]
    E, C = full_set_coder(C)                                   # whole suite [§3.2] (tex:sections/3_new_method.tex:51)
    d, r = full_set_critic(E, ORIGINAL_SOTA_RESULT)            # reference: A-FULL-1 [Tab. 1] [§3.2] (tex:sections/3_new_method.tex:52)
    eng = 0                                                    # full-set limit unstated: A-FULL-2 [§3.2] [App. A.2]
    while d == 'Engineer' and eng < N_ENG_FULL:                # loop drawn in [Fig. 5] (image); vocabulary U-FULL-1
        h, E, C = full_set_engineer(h, C, r)                   # [§3.2] (tex:sections/3_new_method.tex:52)
        d, r = full_set_critic(E, ORIGINAL_SOTA_RESULT)        # [§3.2] (tex:sections/3_new_method.tex:52)
        eng += 1
    # here, before returning, the specification filter may discard the solution [§4.2]; which experiments: U-INT-1
    return h, E, C, ('Good' if d == 'Good' else 'Bad'), r      # terminal decision [§3.2] (tex:sections/3_new_method.tex:52) [Fig. 5] (image)

def scientist_two(G):                                          # [§3, Eq. 1] (tex:sections/3_new_method.tex:7-9)
    # ---- §3.1 limitations: P-LIM-1..4, stages/01 ----
    L = limitation_extractor(G)                                # [§3.1] (tex:sections/3_new_method.tex:20)
    for _ in range(LIM_MAX):                                   # LIM_MAX = 16 [App. A.2]; no symbol in [§3.1]; count: A-TOP-2
        sufficient, feedback = limitation_verifier(G, L)       # verdict and feedback [inferred] [Lst. 1] [§3.1] (tex:sections/3_new_method.tex:21)
        if sufficient:                                         # [§3.1] (tex:sections/3_new_method.tex:23)
            break
        L = limitation_extractor(G, L, feedback)               # it finds the missing limitations [§3.1] (tex:sections/3_new_method.tex:22)
    # at the limit L passes on [inferred] [§3.1]; Listing 1 would return None [Lst. 1]: A-LIM-1

    # ---- §3.1 seed ideas: P-SEED-1..4, stages/01 ----
    h0 = initial_idea_generator(G, L)                          # [§3.1] (tex:sections/3_new_method.tex:25); name from [Fig. 4] (image)
    s = {h0: novelty_checker(h0, google_search(h0, k=2))}      # two reference papers [App. A.2]; a score [§3.1]
    H0 = [h0]                                                  # [§3.1] (tex:sections/3_new_method.tex:25)
    while len(H0) < N_seed:                                    # N_seed has no value: U-SEED-1 [§3.1] (tex:sections/3_new_method.tex:26)
        h = idea_generator(G, L, H0, s)                        # inputs [inferred] from [§3.1]; filter or rank: A-SEED-1
        s[h] = novelty_checker(h, google_search(h, k=2))       # checked after each idea [Fig. 4] (image) [App. A.2]
        H0.append(h)                                           # [§3.1] (tex:sections/3_new_method.tex:25)
    H0 = sorted(H0, key=s.get, reverse=True)                   # [§3.1] (tex:sections/3_new_method.tex:27)

    # ---- §3.2 baseline on the subset: P-BASE-1, stages/02 ----
    E_base, C_base = baseline_coder(G, SUBSET)                 # [§3.2] (tex:sections/3_new_method.tex:37); SUBSET: U-BASE-1; placement A-BASE-1

    # ---- §3.3 idea rounds: P-EVO-1..6 and P-SEL-1, stages/03 ----
    traces, k = [], 0                                          # [§3.3]
    H_k = H0[:N_0]                                             # round 0 [§3.3] (tex:sections/3_new_method.tex:63); N_0: A-EVO-1
    while True:
        R_k = [A_Coder(G, h) for h in H_k]                     # [§3.3, Eq. 3] (tex:sections/3_new_method.tex:80-83)
        traces += R_k                                          # the union R_<k [§3.3] (tex:sections/3_new_method.tex:67)
        n_good = sum(r.d == 'Good' for r in traces)            # [§3.3] (tex:sections/3_new_method.tex:85)
        if n_good >= S or k == K:                              # S = 4, K = 4 [§3.3] [App. A.2]; when checked: U-EVO-1; K: A-EVO-2
            break
        k += 1                                                 # [§3.3] (tex:sections/3_new_method.tex:67)
        I_k = idea_evolver(traces)                             # N_k = 1 [§3.3] (tex:sections/3_new_method.tex:67-68) [App. A.2]
        H_k = I_k + next_unevaluated(H0, N_e)                  # N_e = 1 [§3.3] (tex:sections/3_new_method.tex:75-76) [App. A.2]
    if n_good == 0:                                            # [§3.3] (tex:sections/3_new_method.tex:86)
        return None                                            # no P+ and no C+ [inferred] [§3.3]; U-EVO-4
    goods = [(r.h, r.E, r.C) for r in traces if r.d == 'Good'] # [§3.3, Eq. 4] (tex:sections/3_new_method.tex:90-92)
    h_best, E_best, C_best = selector(G, goods)                # an LLM choice [§3.3, Eq. 4]; criterion U-SEL-1

    meta_used = 0                                              # N_meta = 1 [§3.6] (tex:sections/3_new_method.tex:151) [App. A.2]
    while True:                                                # one downstream pass [§3.6]; budgets reset per pass: U-META-1
        # ---- §3.4 ablation: P-ABL-1..6, stages/04 ----
        abl_used = 0                                           # N_abl = 1 [§3.4] (tex:sections/3_new_method.tex:114) [App. A.2]
        while True:
            plans = ablation_planner(h_best)                   # N_p plans, no value: U-ABL-1 [§3.4] (tex:sections/3_new_method.tex:100)
            E_abl = [ablation_coder(C_best, p) for p in plans] # [§3.4] (tex:sections/3_new_method.tex:101-102)
            d_abl, r_abl = ablation_critic(h_best, E_abl)      # Good or Refine [§3.4] (tex:sections/3_new_method.tex:106); a reject: A-ABL-1
            if d_abl == 'Good' or abl_used == N_abl:           # [§3.4] (tex:sections/3_new_method.tex:107) (tex:sections/3_new_method.tex:114); U-ABL-4
                break
            abl_used += 1                                      # [§3.4]
            h_new, E_new, C_new = full_set_engineer(h_best, C_best, r_abl)   # [§3.4] (tex:sections/3_new_method.tex:108)
            if result_comparison(E_new, E_best) == 'new':      # [§3.4] (tex:sections/3_new_method.tex:111-112); criterion A-ABL-3
                h_best, E_best, C_best = h_new, E_new, C_new   # [§3.4] (tex:sections/3_new_method.tex:112)
                continue                                       # re-ablate the new h_best [§3.4] (tex:sections/3_new_method.tex:113)
            break                                              # on to drafting [Fig. 7] (image); Listing 1 and App. B differ: A-ABL-2

        # ---- §3.5 drafting and review-rebuttal: P-DRAFT-1, P-PEER-1..6, stages/05 ----
        P_new = initial_drafter(h_best, E_best, E_abl)         # PaperOrchestra [§3.5] (tex:sections/3_new_method.tex:119); ICLR 2025 format [App. A.2]
        R_new, s_review = peer_reviewer(P_new)                 # ScholarPeer, s_review in [1, 10] [§3.5] (tex:sections/3_new_method.tex:123)
        peer_used = 0                                          # N_peer = 2 [§3.5] (tex:sections/3_new_method.tex:132) [App. A.2]; A-PEER-1
        while s_review < 8 and peer_used < N_peer:             # threshold 8 [§3.5] (tex:sections/3_new_method.tex:124) [App. A.2]
            tasks = rebuttal_planner(R_new)                    # N_t tasks, no value: U-PEER-1 [§3.5] (tex:sections/3_new_method.tex:125)
            E_reb = [rebuttal_coder(C_best, t) for t in tasks] # [§3.5] (tex:sections/3_new_method.tex:126-127); code kept? U-PEER-2
            P_new = paper_enhancer(P_new, R_new, E_reb)        # [§3.5] (tex:sections/3_new_method.tex:130)
            R_new, s_review = peer_reviewer(P_new)             # [§3.5] (tex:sections/3_new_method.tex:131)
            peer_used += 1                                     # [§3.5]
        # at the limit P_new is kept [§3.5] (tex:sections/3_new_method.tex:132); Listing 1 would return None [Lst. 1]: A-TOP-1
        # integrity steps act on P_new here or later: reference check and method-code audit [§4.2]; placement U-INT-3

        # ---- §3.6 meta-review: P-META-1..7, stages/06 ----
        d_meta, r_meta = meta_reviewer(P_new, R_new)           # Accept or Refine [§3.6] (tex:sections/3_new_method.tex:138)
        if d_meta == 'Accept' or meta_used == N_meta:          # [§3.6] (tex:sections/3_new_method.tex:139) (tex:sections/3_new_method.tex:151); A-META-2
            return P_new, C_best                               # P+ and C+ [§3.6] (tex:sections/3_new_method.tex:140)
        meta_used += 1                                         # [§3.6]
        h_new, E_new, C_new = full_set_engineer(h_best, C_best, r_meta)      # [§3.6] (tex:sections/3_new_method.tex:144)
        if result_comparison(E_new, E_best) != 'new':          # needs "strictly superior" [§3.6] (tex:sections/3_new_method.tex:147-148)
            return P_new, C_best                               # refinement discarded [§3.6] (tex:sections/3_new_method.tex:150)
        h_best, E_best, C_best = h_new, E_new, C_new           # then the loop re-runs ablation, drafting, review [§3.6] (tex:sections/3_new_method.tex:148-149); A-META-1
```

- **Reading choices in this reconstruction [ours].** Two counting conventions, both readings of A-TOP-2: the limitation loop counts critic calls, as Listing 1 does, so its 16th expansion is never judged; the engineering, ablation, review and meta loops count refinements and judge each one, so they allow N + 1 critic calls [Lst. 1] [App. A.2]. Limitations pass on at the limit (A-LIM-1); a failed ablation comparison goes to drafting as Figure 7 draws it (A-ABL-2); A_FullEng is one call, although in Figure 3 the ablation-stage refiner, in the *Analyzer* box, sends its *New Idea* back through the full-set critic, while the meta-review's *Idea Refiner* leads into the ablation stage (U-ABL-2); budgets reset for the meta pass (U-META-1); the meta-reviewer is asked again after the restart, but cannot trigger a second refinement (A-META-2) [Fig. 3] [Fig. 7] (image) [§3.6] [ours].

### 4.1 Loops that restart work, and how often

| Trigger | What re-runs | Limit (App. A.2) | Source |
|---|---|---|---|
| Subset critic says `Engineer` | Subset Engineering Agent, then the critic again | N_eng = 2 rounds per idea | [§3.2] [App. A.2] |
| Full-set critic asks for engineering | Full-Set Engineer, then the critic again | unstated (A-FULL-2) | [§3.2] [Fig. 5] (image) |
| Round k ends with fewer than S successes and k < K | A_Evolve, then A_Coder on one evolved and one seed idea | K = 4 rounds after round 0 | [§3.3] [App. A.2] [Fig. 9] (image) |
| Ablation critic says `Refine` and the comparison prefers E_new | ablation planning, execution and critique of the new h_best | N_abl = 1 per downstream pass | [§3.4] [App. A.2] [Fig. 7] (image) |
| Review score below 8 | rebuttal plan, rebuttal code, enhancement, re-review | N_peer = 2 per downstream pass | [§3.5] [App. A.2] |
| Meta-review says `Refine` and E_new is strictly superior | the whole downstream pass: ablation, re-drafting, peer review | N_meta = 1 | [§3.6] [App. A.2] |

- **Maxima per run under App. A.2, budgets reset per pass [ours].** Ablation executions ≤ (1 + N_abl)(1 + N_meta) = 4; initial drafts ≤ 1 + N_meta = 2; ScholarPeer reviews ≤ (1 + N_peer)(1 + N_meta) = 6, or 4 if N_peer counts reviews (A-PEER-1); meta-reviews ≤ 2 (A-META-2); A_FullEng calls and Result Comparison calls ≤ N_abl(1 + N_meta) + N_meta = 3 each [§3.4] [§3.5] [§3.6] [App. A.2] [ours].
- **Never restarted.** Limitations, seed ideas, the baseline, the idea rounds and the selection run once: the meta refinement edits h_best through A_FullEng and re-enters at the ablation stage, not at §3.3 [§3.6] [Fig. 7] (image). Figure 3 adds one path: the Analyzer's *New Idea* re-enters the critic of the *Full-Set Experiment Agent*, a full-set check rather than a new idea round (U-ABL-2) [Fig. 3] (image).

### 4.2 Decision points: made by an agent, or by a number

| Decision | Made by | Reads | Produced by | Data | Guard | Form | Source |
|---|---|---|---|---|---|---|---|
| Are the limitations enough? | Limitation Verifier (LLM) | the set of limitations | the Limitation Extractor (LLM) | G's paper; no benchmark | none | confirm, or insufficient | [§3.1] |
| How novel is an idea? | Novelty Checker (LLM with Google Search) | the idea and two retrieved papers | the Idea Generator (LLM); Google Search | the literature | none | a score s_i; ranking is a sort | [§3.1] [App. A.2] |
| Does the idea beat the baseline on the subset? | Subset Critic (LLM) | E_sub^h against E_base | agent-written code, the Subset and Baseline Coders' (U-ART-16) | the benchmark subset; no split stated (U-TOP-5, U-BASE-1) | none; the filter reads code only (U-INT-1) | `Bad`, `Good` or `Engineer`, with r^h | [§3.2] |
| Does it beat the SOTA on the full set? (A-FULL-1) | Full-Set Critic (LLM) | full results against the original SOTA result | agent-written code; the idea's script also recomputes the baseline [p. 41] (image) | the reported benchmark; no split stated (U-TOP-5) | none | terminal d^h | [§3.2] [Tab. 1] |
| Stop the idea rounds? | a counter | the count of `Good` verdicts, the round index | the critics' verdicts | none | none | ≥ S, or k = K | [§3.3] |
| Which idea is best? | Selector (LLM) | metrics and logs of every `Good` idea | agent-written code | the reported benchmark, "evaluated on the full benchmark" (U-TOP-5) | none | a choice | [§3.3, Eq. 4] |
| Is the component breakdown clean? | Ablation Critic (LLM) | E_abl | the Ablation Coding Agent's code | the reported benchmark, or a subset: p. 69 prints a *subset test split* (U-TOP-5) | none | `Good` or `Refine`, with r_abl | [§3.4] [p. 69] |
| Keep a refinement? (A-ABL-3) | Result Comparison Agent (LLM), in §3.4 and §3.6 | E_new against E_best | A_FullEng's code against the selected code | the reported benchmark; no split stated (U-TOP-5) | it is itself the guard | the new result preferred, or not | [§3.4] [§3.6] |
| Is the review good enough? | a threshold on ScholarPeer's score | s_review | ScholarPeer, reading the manuscript | the manuscript | none; the threshold depends on the reviewer (P-CFG-9) | 8 or more | [§3.5] [App. A.2] |
| Does it meet the venue bar? | Meta-Review Agent (LLM) | P_new and R_new | the Drafter, the Enhancer and ScholarPeer | the manuscript | none | `Accept` or `Refine`, with r_meta | [§3.6] |
| Does a solution break the rules? | the Coding Agent, as a filter | solution code, task rules | the coders | code, not results | it is itself the guard | keep or discard | [§4.2] |
| Is a citation hallucinated? | a search-augmented LLM | the bibliography, live search | the Writer Agent | the literature | it is itself the guard | flags for the Writer Agent | [§4.2] |
| Does the paper match the code? | the Coding Agent, as an auditor | repository and manuscript | the coders and the writers | code and text | it is itself the guard | an audit report | [§4.2] |
| Which numbers go into the paper? | the Initial Drafter and the Paper Enhancer | E_best, E_abl, E_reb | agent-written code | the reported benchmark | none in the loop | the paper's tables and figures, "updating empirical tables and figures" | [§3.5] |
| Which data answers a reviewer? | the Rebuttal Planner and Coder | R_new | the agent's own choice, in the one example *50 representative TALENT datasets* | datasets the agent picks | none in the loop | the supplementary results E_reb | [§3.5] [p. 51] (image) |
| What does the full set contain? | the Full-Set Coding Agent | C_sub^h | the agent adapts the code "to run across the entire benchmark suite"; one trace reports a *FULL CIFAR-100 benchmark* | the agent's reading of the benchmark | none in the loop | the scope of E_full^h | [§3.2] [p. 40] (image) |

- **Consequence [ours].** The paper specifies no gain formula for any decision in the loop: "ScientistTwo has no target metric" [Tab. 15] (tex:sections/appendix.tex:176). Whether an idea beats the baseline, which idea wins and whether a refinement helps are LLM readings of numbers that agent-written code produced (U-ART-16), which may include gains [p. 42] (image) and spreads, "+0.61%±0.27" and "+3.4%±0.2" [Tab. 16] (tex:sections/appendix.tex:288) (tex:sections/appendix.tex:311); the *statistically inert* rejection we cited first shows only a critic's judgement, not a test (A-ART-13), and is withdrawn as evidence [Tab. 16] [ours]. The gates' wording, "strictly outperforms" and "verified as strictly superior", leaves open whether they are numeric tests (A-ABL-3) [§3.4] (tex:sections/3_new_method.tex:111) [§3.6] (tex:sections/3_new_method.tex:148). The paper computes gains itself only in evaluation, by parsing: "we parse the main tables for 10 times using Gemini 3.6 Flash and averaged them" [§4.1] (tex:sections/4_experiment.tex:19); how one paper's gain is defined is claims.md's U-EVAL-1, and the gains at p. 42 are the agent's own [ours].
- **Data and guards [ours].** Every decision that reads results reads the benchmark that is then reported, with no split stated (U-TOP-5), and none has a guard in the loop beyond the code filter, which reads code, not results [§3.2] [§3.3] [§3.4] [§4.2] [ours].

### 4.3 Termination branches · P-TOP-5

| Branch | Condition | Output | Source |
|---|---|---|---|
| Accept | d_meta = `Accept` | P+ ← P_new, C+ ← C_best | [§3.6] (tex:sections/3_new_method.tex:139-140) |
| Meta limit | N_meta refinements used and the pass ends | P_new and C_best, as a "rigorously validated final contribution" | [§3.6] (tex:sections/3_new_method.tex:151) [inferred] |
| Refinement not superior | the comparison rejects E_new after `Refine` | the previous P_new, which the meta-reviewer had just sent back, and C_best | [§3.6] (tex:sections/3_new_method.tex:150) |
| No success | round K ends with zero `Good` ideas | nothing: ScientistTwo "terminates the entire process" | [§3.3] (tex:sections/3_new_method.tex:86) |
| Ablation rejection | the Ablation Critic attributes the gain to generic training controls | no contribution for that task; not described in §3 (A-ABL-1) | [App. B] (tex:sections/appendix.tex:222-224) |
| Rule violation | the specification filter finds reward hacking | the task's output is filtered out | [§4.2] [fn. 2] (tex:sections/4_experiment.tex:43) |
| Any error | a crash, a timeout, code that never runs | UNSPECIFIED (U-TOP-2) | [§3] [§4.3] |

## 5. Stage by stage

Each file follows the README's stage template for every Table 1 row it covers, and ends with its gaps in full [Tab. 1] [ours].

| File | Section | Table 1 rows | Keys |
|---|---|---|---|
| [stages/01-seed-ideas.md](stages/01-seed-ideas.md) | [§3.1] | Finding limitations; Seed idea generation | LIM, SEED |
| [stages/02-evaluating-ideas.md](stages/02-evaluating-ideas.md) | [§3.2] | Reproduce baseline on subset; Idea experiment on subset; Idea experiment on full-set; the unified coder | BASE, SUB, FULL, CODER |
| [stages/03-refining-ideas.md](stages/03-refining-ideas.md) | [§3.3] | Idea evolution; Select best idea | EVO, SEL |
| [stages/04-ablation.md](stages/04-ablation.md) | [§3.4] | Ablation study | ABL |
| [stages/05-drafting-peer-review.md](stages/05-drafting-peer-review.md) | [§3.5] | Initial drafting; Peer-Review | DRAFT, PEER |
| [stages/06-meta-review.md](stages/06-meta-review.md) | [§3.6] | Meta-Review | META |
| [stages/07-integrity.md](stages/07-integrity.md) | [§4.2] | none: the integrity mechanisms of "CoE Integrity Audit" | INT |

## 6. Loop limits · P-CFG-1 … 19

App. A.2 sets every value in one paragraph (tex:sections/appendix.tex:155) [App. A.2]. Where §3 gives no symbol, the row says so [§3].

| Symbol | Meaning | Introduced in §3 | App. A.2 value, quoted | Corroboration | Ambiguity |
|---|---|---|---|---|---|
| none (P-CFG-1) | limitation rounds | "maximum number of iterations" [§3.1] (tex:sections/3_new_method.tex:23) | 16: "We extract limitations for a maximum of 16 rounds" [App. A.2] | none | count A-TOP-2; exhaustion A-LIM-1 [ours] |
| N_seed (P-CFG-12) | size of the seed pool H_0 | [§3.1] (tex:sections/3_new_method.tex:26) | not set [App. A.2] | none | U-SEED-1 [ours] |
| none (P-CFG-2) | novelty references per idea | not in [§3.1] | 2: "To evaluate novelty, ScientistTwo retrieves two reference papers via Google Search" [App. A.2] | none | U-SEED-2 [ours] |
| N_0 (P-CFG-13) | seeds run in round 0 | [§3.2] (tex:sections/3_new_method.tex:40) [§3.3] (tex:sections/3_new_method.tex:63) | not set; each round has "two candidates" [App. A.2] | none; the earlier *round 0's selected ideas are all seeds* holds for any N_0, so it corroborates nothing [Fig. 9b] (image) [ours] | A-EVO-1 [ours] |
| N_eng (P-CFG-3) | subset engineering budget | [§3.2] (tex:sections/3_new_method.tex:47) | 2: "If the Idea Critic Agent flags an idea for engineering refinement, we apply engineering techniques for at most two rounds" [App. A.2] | none | A-TOP-2 [ours] |
| none (P-CFG-14) | full-set engineering budget | no limit stated [§3.2] (tex:sections/3_new_method.tex:52) | 2 only if the same sentence covers it [App. A.2] | the same critic–engineer loop at both levels [Fig. 5] (image) | A-FULL-2 [ours] |
| N_k (P-CFG-4) | evolved ideas per round k ≥ 1 | [§3.3] (tex:sections/3_new_method.tex:67) | 1: "the other an evolved idea" [App. A.2] | none | none [ours] |
| N_e (P-CFG-5) | unevaluated seeds per round k ≥ 1 | [§3.3] (tex:sections/3_new_method.tex:75-76) | 1: "one selected from the seed ideas" [App. A.2] | seeds are selected in rounds 1–4 [Fig. 9b] (image) | none [ours] |
| K (P-CFG-6) | refinement rounds | [§3.3] (tex:sections/3_new_method.tex:84) (tex:sections/3_new_method.tex:86) | 4: "We run this experimentation loop for up to four rounds" [App. A.2] | x-axis *Initial, Round 1 … Round 4*, 49 ICML 2026 tasks [Fig. 9] (image) [§4.2] | A-EVO-2 [ours] |
| S (P-CFG-7) | successes that stop the rounds | [§3.3] (tex:sections/3_new_method.tex:84-85) | 4: "terminating early once four successful ideas are obtained" [App. A.2] | none | U-EVO-1 [ours] |
| N_p (P-CFG-15) | ablation plans | [§3.4] (tex:sections/3_new_method.tex:100) | not set [App. A.2] | "5–6 ablations per paper" on the ICLR 2026 tasks ScientistTwo completed (4 of 5) [Tab. 15]; six with *full tables for all six ablations* [p. 11], and seven in App. D's draft [pp. 64–65] | U-ABL-1 [ours] |
| N_abl (P-CFG-8) | ablation refinements | [§3.4] (tex:sections/3_new_method.tex:114) | 1: "we refine the idea at most once" [App. A.2] | none | A-ABL-2, U-ABL-4 [ours] |
| threshold (P-CFG-9) | review score that stops the rebuttal | "(e.g., 8)" and ≥ 8 [§3.5] (tex:sections/3_new_method.tex:124) (tex:sections/3_new_method.tex:132) | 8: the loop "terminates early if the ScholarPeer review score reaches 8" [App. A.2] | none | reviewer-dependent, to calibrate [ours]: 8 is a point on ScholarPeer's own scale, where accepted human papers average 6.2–6.9 [Tab. 3]; claims.md infers that the reported acceptance fits only a rating of 6 or more, an inference that fails if ScholarPeer averages several reviews (A-EVAL-3) [Tab. 3] [inferred]; and the second review round, run to push the score toward 8, brings no held-out gain: the Stanford Agentic Reviewer's acceptance falls from 73.5% to 69.4% while ScholarPeer's rises from 79.6% to 93.9%, 49 ICML 2026 tasks (C-ABLX-4) [Tab. 5] [ours] |
| N_t (P-CFG-16) | rebuttal tasks | [§3.5] (tex:sections/3_new_method.tex:125) | not set [App. A.2] | none | U-PEER-1 [ours] |
| N_peer (P-CFG-10) | review–rebuttal budget | [§3.5] (tex:sections/3_new_method.tex:132) | 2: "the peer-review simulation runs for at most two rounds" [App. A.2] | review rounds 0, 1 and 2, 49 ICML 2026 tasks [Tab. 5] [§4.2] | A-PEER-1 [ours] |
| N_meta (P-CFG-11) | meta-review refinements | [§3.6] (tex:sections/3_new_method.tex:151) | 1: "with review-based refinement conducted at most once" [App. A.2] | one refinement, LFR-Engram to FCD-Engram, one task [Tab. 6] | A-META-2; read as two reviews and one rebuttal, the sentence would leave N_meta unset, a reading disfavoured by Table 5's rebuttals in rounds 1 and 2 and the *Review-Driven* headings (tex:sections/3_new_method.tex:134) (tex:sections/3_new_method.tex:142) [ours] |
| N_a (P-CFG-17) | number of agents | [§3, Eq. 1] (tex:sections/3_new_method.tex:9-11) | not set [App. A.2] | section 7 counts 27 | none [ours] |

- **Also set in App. A.2, and how the IDs relate.** Model routing (P-CFG-19, section 7) and the drafting format (P-CFG-18): "We use the ICLR 2025 format for drafting, following the PaperOrchestra" [App. A.2] (tex:sections/appendix.tex:155). How the IDs relate [ours]: a P-CFG ID is a value that App. A.2 sets or leaves unset; the loop that uses it is a stage element: P-LIM-4 uses P-CFG-1, P-SUB-4 uses P-CFG-3, P-EVO-5 uses P-CFG-6 and P-CFG-7, P-ABL-6 uses P-CFG-8, P-PEER-2 uses P-CFG-9, P-PEER-6 uses P-CFG-10, and P-META-7 uses P-CFG-11 [App. A.2] [ours].

## 7. Agent roster · P-ROSTER-1 … 28

- **Routing rule.** "we employ Gemini 3.6 Flash for all agents, except for the Idea Experiment Coding Agent, the Ablation Study Agent, the Rebuttal Agent, and the Draft Enhancer, which use Claude Code with Opus 4.8" [App. A.2] (tex:sections/appendix.tex:155).
- **Two looser statements.** "All experiments are conducted using Gemini 3.6 Flash and Claude Opus 4.8, unless otherwise specified" [§4] (tex:sections/4_experiment.tex:5); "we leverage Claude Code with Opus 4.8 whenever coding capabilities are required" [§4.2] (tex:sections/4_experiment.tex:46). Agents that code but are not in A.2's list are A-CFG-1 [ours].
- **Reading the table.** Names in italics are diagram labels, read as images; *Backend* is the harness App. A.2 names, and *none named* means App. A.2 names only a model; a judge is an agent whose output chooses a branch [Fig. 3] (image) [App. A.2] [ours].

| ID | Canonical agent | Every name the paper gives it (where) | Backend | Model | Kind | Receives → returns | Success evidence |
|---|---|---|---|---|---|---|---|
| P-ROSTER-1 | Limitation Extractor | Limitation Extractor [§3.1] [Fig. 3] [Fig. 4] (image) | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | reasoning | G, later also the current set and what is missing → a set of limitations [§3.1] | none reported [ours] |
| P-ROSTER-2 | Limitation Verifier | Limitation Verifier [§3.1] [Fig. 4] (image); absent from Figure 3 | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | judge | the set → sufficient, or insufficient [§3.1] | none reported [ours] |
| P-ROSTER-3 | Initial Idea Generator | unnamed in §3.1, where ScientistTwo "first generates an initial idea"; *Initial Idea Generator* [Fig. 4] (image) | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | reasoning | the limitations → h_0 [§3.1]; A-SEED-2 | seed ideas are the chosen best for 22 of 49 tasks [Fig. 9b] (image) |
| P-ROSTER-4 | Novelty Checker | Novelty Checker [§3.1] [Fig. 3] [Fig. 4] (image) | none named, with Google Search [App. A.2] | Gemini 3.6 Flash [App. A.2] | judge, search | an idea and two retrieved papers → a novelty score s_i [§3.1] [App. A.2] | none reported [ours] |
| P-ROSTER-5 | Idea Generator | Idea Generator Agent [§3.1]; *Idea Generator* [Fig. 4] (image); "our idea generator" [App. B] | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | reasoning | the pool so far → one more distinct idea [§3.1]; A-ROSTER-1 | as row 3 [Fig. 9b] (image) |
| P-ROSTER-6 | Baseline Coder | Baseline Coding Agent [§3.2]; *Baseline Coder* [Fig. 5] (image) | Claude Code, or none named (A-CFG-1) | Opus 4.8, or Gemini 3.6 Flash (A-CFG-1) | coding | G and the subset → E_base, C_base [§3.2] | none: no reproduction rate is reported [ours] |
| P-ROSTER-7 | Subset Coder | Subset Coding Agent [§3.2]; *Subset Coder* [Fig. 5]; *Coding Agent* in *Subset Experiment Agent* [Fig. 3] (image) | Claude Code [App. A.2] [inferred] | Opus 4.8 [inferred] | coding | h, C_base → E_sub^h, C_sub^h [§3.2] | none per agent; 86 of 107 tasks end with a paper [Tab. 3] |
| P-ROSTER-8 | Subset Critic | Subset Critic Agent [§3.2]; *Subset Critic* [Fig. 5]; *Critic Agent* [Fig. 3] (image); the Idea Critic Agent of A.2 [App. A.2] [inferred] | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | judge | E_sub^h against E_base → d^h in {`Bad`, `Good`, `Engineer`}, r^h [§3.2] | none: no verdict rate is reported [ours] |
| P-ROSTER-9 | Subset Engineer | Subset Engineering Agent [§3.2]; *Subset Engineer* [Fig. 5] (image) | Claude Code, or none named (A-CFG-1) | Opus 4.8, or Gemini 3.6 Flash (A-CFG-1) | coding | h, C_sub^h, r^h → refined h, C_sub^h, E_sub^h [§3.2] | none reported [ours] |
| P-ROSTER-10 | Full-Set Coder | Full-Set Coding Agent [§3.2]; *Full-Set Coder* [Fig. 5]; *Coding Agent* in *Full-Set Experiment Agent* [Fig. 3] (image) | Claude Code [App. A.2] [inferred] | Opus 4.8 [inferred] | coding | C_sub^h → code and results on the whole suite [§3.2] | none per agent [ours] |
| P-ROSTER-11 | Full-Set Critic | Full-Set Critic Agent [§3.2]; *Full-Set Critic* [Fig. 5]; *Critic Agent* [Fig. 3] (image); perhaps the Idea Critic Agent (A-FULL-2) | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | judge | full results against the original SOTA result → terminal d^h [§3.2] [Tab. 1] | none: no verdict rate is reported [ours] |
| P-ROSTER-12 | Full-Set Engineer | Full-Set Engineer [§3.2]; Full-Set Engineering Agent A_FullEng, which §3.4 "re-engages" [§3.4] [§3.6]; *Full-Set Engineer* [Fig. 5] [Fig. 7]; *Idea Refiner* in the *Meta-Review Agent* box [Fig. 3] (image) | Claude Code, or none named (A-CFG-1); artifacts.md P-ART-3 names Claude Code | Opus 4.8, or Gemini 3.6 Flash (A-CFG-1) | coding | in §3.2 full-set engineering; in §3.4 and §3.6 h_best, C_best and r_abl or r_meta → h_new, E_new, C_new [§3.4] [§3.6] | none reported [ours] |
| P-ROSTER-13 | Idea Implementer (composite) | Idea Implementer Agent A_Coder [§3.2]; *Implementer* [Fig. 6]; roughly the *Evaluator* group [Fig. 3] (image) | its members' [App. A.2] | its members' [App. A.2] | composite of rows 7–12, and row 6 too if the baseline runs per idea (A-BASE-1) [§3.2] [Fig. 5] (image) | G, h → h, E^h, C^h, d^h, r^h [§3.2, Eq. 2] | none per agent: Table 8's success rates, 80.0 with Claude Code against 60.0 with Antigravity on 5 ICLR 2026 tasks, are the whole pipeline's, run with its coding backend swapped [§4.2] (tex:sections/4_experiment.tex:46) [Tab. 8] |
| P-ROSTER-14 | Idea Evolver | Idea Evolver Agent A_Evolve [§3.3] [§4.2]; *Idea Evolver* [Fig. 3] [Fig. 6] (image) | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | reasoning | R_<k → I_k, N_k ideas [§3.3] | evolved ideas are the chosen best for 27 of 49 tasks [Fig. 9b] (image) |
| P-ROSTER-15 | Selector | Selector Agent A_Selector [§3.3] [§4.2]; *Selector* [Fig. 6] (image) | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | judge | G and the `Good` tuples → h_best, E_best, C_best [§3.3, Eq. 4] | none: Figure 9b shows what it chose, not whether the choice was right [Fig. 9b] (image) [ours] |
| P-ROSTER-16 | Ablation Planner | Ablation Planner Agent [§3.4]; *Ablation Planner* [Fig. 7]; *Planning Agent* in *Ablation Study Agent* [Fig. 3] (image) | Claude Code if it belongs to the Ablation Study Agent [inferred]; A-CFG-1 | Opus 4.8 [inferred] | planning | h_best → N_p plans [§3.4] | none reported [ours] |
| P-ROSTER-17 | Ablation Coder | Ablation Coding Agent [§3.4]; *Ablation Coder* [Fig. 7]; *Coding Agent* in *Ablation Study Agent* [Fig. 3] (image) | Claude Code [App. A.2] [inferred] | Opus 4.8 [inferred] | coding | p_i and C_best → c_i [§3.4] | none reported [ours] |
| P-ROSTER-18 | Ablation Critic | Ablation Critic Agent A_AblCritic, also written A_AblCrit [§3.4]; *Ablation Critic* [Fig. 7] (image) [App. A.2]; *Critic Agent* in *Idea Refiner* [Fig. 3] (image); ablation critic [App. B] | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] [inferred] | judge | E_abl and h_best → d_abl in {`Good`, `Refine`}, r_abl [§3.4] | none per verdict; two outcomes are reported: TeCh's rejection [App. B] (tex:sections/appendix.tex:222-224), and LC-FTT stripped "down to the lone component that carried the gain" [Tab. 16] (tex:sections/appendix.tex:291-292) |
| P-ROSTER-19 | Result Comparison | Result Comparison Agent [§3.4] [§3.6]; *Result Compare* [Fig. 7] (image) | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | judge | E_new against E_best → keep the new result, or not [§3.4] [§3.6] | none; one keep is implied, FCD-Engram over LFR-Engram, n = 1 [Tab. 6] [inferred]: §4.2 says only that FCD-Engram "consistently outperforms LFR-Engram" and never names this agent [§4.2] (tex:sections/4_experiment.tex:38) |
| P-ROSTER-20 | Initial Drafter | Initial Drafter Agent A_Draft, "incorporating PaperOrchestra" [§3.5] [Bib: song2026paperorchestra]; *Initial Drafter* in *Writer Agent* [Fig. 3] [Fig. 7] (image) | PaperOrchestra; harness otherwise none named [App. A.2] | Gemini 3.6 Flash [inferred] | writing | h_best, E_best, E_abl → P_new [§3.5] | review round 0, without rebuttal, 49 ICML 2026 tasks [Tab. 5] |
| P-ROSTER-21 | Peer Reviewer | Peer-Reviewer Agent A_Reviewer, i.e. ScholarPeer [§3.5] [Bib: goyal2026scholarpeer]; Review Agent [§3] [§4.2] [Fig. 3] (image); *Peer Reviewer* [Fig. 7] (image); Peer-Review Agent [§1] | ScholarPeer, an external system | not stated (U-PEER-3) | judge | P_new → R_new with s_review in [1, 10] [§3.5] | none: it is itself one of the metrics [§4] |
| P-ROSTER-22 | Rebuttal Planner | Rebuttal Planner Agent A_RebPlan [§3.5]; *Rebuttal Planner* [Fig. 7] (image) | Claude Code if it belongs to the Rebuttal Agent (A-CFG-1) | Opus 4.8 [inferred] | planning | R_new → N_t tasks [§3.5] | review rounds 1 and 2 [Tab. 5] |
| P-ROSTER-23 | Rebuttal Coder | Rebuttal Coding Agent A_RebCoder [§3.5]; *Rebuttal Coder* [Fig. 7] (image); Rebuttal Agent [§1] [§3] [§4.2] [Fig. 3] (image) | Claude Code [App. A.2] [inferred] | Opus 4.8 [inferred] | coding | t_i and C_best → e_i [§3.5] | review rounds 1 and 2 [Tab. 5] |
| P-ROSTER-24 | Paper Enhancer | Paper Enhancer Agent A_Enhancer [§3.5]; Draft Enhancer [App. A.2]; *Draft Enhancer* in *Writer Agent* [Fig. 3] [Fig. 7] (image) | Claude Code [App. A.2] | Opus 4.8 [App. A.2] | writing, on files | P_new, R_new, E_reb → revised P_new [§3.5] | review rounds 1 and 2 [Tab. 5] |
| P-ROSTER-25 | Meta-Reviewer | Meta-Review Agent A_Meta [§1] [§3] [§3.6] [§4.2]; meta-reviewer [§3.6]; *Meta Reviewer* [Fig. 7]; *Critic Agent* in the *Meta-Review Agent* box [Fig. 3] (image) | none named [App. A.2] | Gemini 3.6 Flash [App. A.2] | judge | P_new and R_new → d_meta in {`Accept`, `Refine`}, r_meta [§3.6] | one reported refinement, n = 1 [Tab. 6] |
| P-ROSTER-26 | Specification filter | "a validation filter that uses the Coding Agent" [§4.2]; a refinement agent in Table 7's header [Tab. 7] | Claude Code by §4.2 [inferred]; A-INT-3 | Opus 4.8 [inferred] | judge, and can write: nothing makes it read-only | solution code and task rules → keep, or discard [§4.2] | Table 7, with and without it [Tab. 7] |
| P-ROSTER-27 | Reference checker | a search-augmented LLM, paired with the Writer Agent [§4.2] | none named [§4.2] | not stated [§4.2] | judge, search | bibliography and live search → hallucinated citations [§4.2] | Table 7 [Tab. 7] |
| P-ROSTER-28 | Method-code auditor | the Coding Agent, paired with the Writer Agent [§4.2] | Claude Code by §4.2 [inferred]; A-INT-3 | Opus 4.8 [inferred] | judge, and can write: the p. 47 auditor saved `repro_check.json` inside the task it audited [p. 47] | repository and manuscript → an audit report [§4.2] | Table 7 [Tab. 7] |

- **Success evidence (U-TOP-6), and write access [ours].** The paper tests agents only end to end, through Tables 5–8 and Figure 9b, and reports no rate of any §3 verdict [Tab. 5] [Tab. 8] [Fig. 9b] (image). Judges can write: nothing in the paper makes a judge read-only, and the auditor of p. 47 saved `repro_check.json` inside the task it audited [p. 47] [§4.2] [ours].

### 7.1 Group and generic names · P-ROSTER-29 … 44

| ID | Name | Where | What it denotes | Resolution |
|---|---|---|---|---|
| P-ROSTER-29 | *Idea Generator*, as a group | [Fig. 3] (image) | the box around *Seed Idea Generator* and *Idea Evolver* | collides with the §3.1 Idea Generator Agent: A-ROSTER-1 [§3.1] |
| P-ROSTER-30 | *Seed Idea Generator* | [Fig. 3] (image) | Limitation Extractor and Novelty Checker | §3.1 as a whole [§3.1] |
| P-ROSTER-31 | *Evaluator* | [Fig. 3] (image) | the subset and full-set experiment boxes | about A_Coder [§3.2] [inferred] |
| P-ROSTER-32 | *Subset Experiment Agent* | [Fig. 3] (image) | a Coding Agent and a Critic Agent joined by a cycle arrow | the subset level of §3.2 [§3.2] |
| P-ROSTER-33 | *Full-Set Experiment Agent* | [Fig. 3] (image) | a Coding Agent and a Critic Agent joined by a cycle arrow, with no separate engineer | the full-set level of §3.2 [§3.2] |
| P-ROSTER-34 | *Analyzer* | [Fig. 3] (image) | *Ablation Study Agent* and *Idea Refiner* | §3.4 [§3.4] |
| P-ROSTER-35 | Ablation Study Agent | [Fig. 3] (image) [App. A.2] | *Planning Agent* and *Coding Agent* | A.2's Claude Code group [inferred] [App. A.2] |
| P-ROSTER-36 | *Idea Refiner*, twice | [Fig. 3] (image) | in *Analyzer*, a Critic Agent emitting a *New Idea*; in *Meta-Review Agent*, the step after the critic | Ablation Critic with A_FullEng; A_FullEng alone [§3.4] [§3.6] [inferred]; A-ROSTER-1 |
| P-ROSTER-37 | Writer Agent | [Fig. 3] (image) [§4.2] | *Initial Drafter* and *Draft Enhancer* | which one repairs references and the method section: A-INT-2 [§4.2] |
| P-ROSTER-38 | Peer-Review Agent | [Fig. 3] (image) [§1] | in Figure 3 the box of Review Agent and Rebuttal Agent; in §1 the reviewer itself | A-ROSTER-1 [§1] |
| P-ROSTER-39 | Rebuttal Agent | [§1] [§3] [§4.2] [App. A.2] [Fig. 3] (image) | the §3.5 planner and coder [inferred] | the planner's model: A-CFG-1 [§3.5] |
| P-ROSTER-40 | *Meta-Review Agent*, as a box | [Fig. 3] (image) | *Critic Agent* and *Idea Refiner* | A_Meta and A_FullEng [§3.6] [inferred] |
| P-ROSTER-41 | Idea Experiment Coding Agent | [App. A.2] | the coding agents of A_Coder [inferred] | which ones: A-CFG-1 [§3.2] |
| P-ROSTER-42 | Idea Critic Agent | [App. A.2] | the Subset Critic, and perhaps the Full-Set Critic | A-FULL-2 [§3.2] |
| P-ROSTER-43 | Coding Agent | [§4.2] [Fig. 3] (image) | generic | which session runs the integrity checks: A-INT-3 [§4.2] |
| P-ROSTER-44 | Critic Agent | [Fig. 3] (image) [§4.3] [App. C] | generic; App. C carries a page of Critic Agent feedback | which critic wrote it belongs to artifacts.md [ours] |

### 7.2 External systems · P-ROSTER-45 … 51

| ID | System | Role in the engine | Where |
|---|---|---|---|
| P-ROSTER-45 | PaperOrchestra [Bib: song2026paperorchestra] | inside the Initial Drafter; the ICLR 2025 format follows it | [§2] [§3.5] [App. A.2] |
| P-ROSTER-46 | ScholarPeer [Bib: goyal2026scholarpeer] | the in-loop reviewer, and also an evaluation reviewer | [§3.5] [§4] [App. A.2] |
| P-ROSTER-47 | Google Search | two reference papers per novelty check | [App. A.2] |
| P-ROSTER-48 | Claude Code with Opus 4.8 [Bib: liu2026dive] | the coding backend | [§4.2] [App. A.2] |
| P-ROSTER-49 | Antigravity with Gemini 3.8 Flash | the replacement coding backend in one experiment, 5 ICLR 2026 tasks | [§4.2] [Tab. 8] |
| P-ROSTER-50 | Stanford Agentic Reviewer | a held-out evaluator, never in the loop | [§4] [fn. 1] |
| P-ROSTER-51 | CoE Integrity Audit [Bib: meng2026scientistone] | post-hoc evaluation of integrity, not a stage | [§4.2] |

- **ScholarPeer is the optimisation target, not an independent judge (SPECIFIED).** "ScholarPeer serves as an in-distribution evaluation, as it is also used to refine the draft quality", while the Stanford Agentic Reviewer "serves as a held-out evaluator that was unseen during development" [§4] (tex:sections/4_experiment.tex:5). The in-loop threshold of 8 therefore depends on this reviewer (P-CFG-9, C-ABLX-4) [ours].

### 7.3 Author family against judge family [ours]

App. A.2 puts every agent it does not name on Gemini 3.6 Flash, so at several gates the author and the judge share a family [App. A.2] [ours].

| Decision | Author, and its family | Judge, and its family | Independence required [ours] | Swap-family control [ours] |
|---|---|---|---|---|
| Is the idea novel? | the Idea Generator, Gemini [§3.1] [App. A.2] | the Novelty Checker, Gemini [§3.1] [App. A.2] | yes: one family writes and scores the idea [ours] | re-score a sample with another family and check that the ranking holds [ours] |
| Does the idea beat the baseline? | the coders, Claude Code with Opus 4.8 [App. A.2] [inferred]; after `Engineer`, the engineers, which App. A.2 never names (A-CFG-1) [§3.2] (tex:sections/3_new_method.tex:45) | the subset and full-set critics, Gemini [§3.2] [App. A.2] | met only under A-CFG-1's reading 2, which puts the engineers on Claude Code; under reading 1 an engineer may share the critic's family [ours] | under reading 2, log the critic's inputs; under reading 1, as in the first row [ours] |
| Keep an ablation refinement? | the Ablation Critic, Gemini, asks for it; A_FullEng writes it (A-CFG-1) [§3.4] | the Result Comparison Agent, Gemini [§3.4] [App. A.2] | yes: the judge's family asked for the change it judges [ours] | judge a sample with another family, or with a numeric rule (A-ABL-3) [ours] |
| Keep a meta refinement? | the Meta-Review Agent, Gemini, asks for it; A_FullEng writes it [§3.6] | the Result Comparison Agent, Gemini [§3.6] [App. A.2] | yes, for the same reason [ours] | as in the row above [ours] |
| Does the code break rules, or differ from the paper? | the coders, Claude Code [App. A.2] [inferred] | the Coding Agent, the same backend by §4.2 [inferred] (A-INT-3) [§4.2] | yes: the auditor shares the author's backend [ours] | audit with another family; keep the post-hoc auditor apart from the in-loop fixer (U-EVAL-5) [ours] |
| Is the review good enough? | the Drafter, Gemini, and the Enhancer, Claude Code [§3.5] [App. A.2] | ScholarPeer, whose backbone is not stated (U-PEER-3) [§3.5] | cannot be checked [ours] | score a sample with a held-out reviewer, as §4 does with the Stanford Agentic Reviewer [§4] |

## 8. State and data objects · P-STATE-1 … 17

One row per object the engine keeps, with every symbol it covers; lifetime and mutability are our reading of the flow, cited where the paper fixes them [§3] [ours].

| ID | Object, and its symbols | Defined | Producer | Consumers | Lifetime | Can it change? |
|---|---|---|---|---|---|---|
| P-STATE-1 | the task G: the paper, its code, and whatever else a task holds (U-TOP-1) | [§3, Eq. 1] | the task | Extractor, Verifier, Baseline Coder, A_Coder [§3.2, Eq. 2], Selector [§3.3, Eq. 4] | the run | no [ours] |
| P-STATE-2 | the evaluation protocol, part of G | [App. B] | the task | every experiment | the run | no: changing it is "forbidden (audit)" [Tab. 15] (tex:sections/appendix.tex:186), under a "protocol-immutability audit (I2)" (tex:sections/appendix.tex:237); an audit, not the setup, enforces it [ours] |
| P-STATE-3 | the set of limitations, with no symbol | [§3.1] | Limitation Extractor | Verifier; initial idea generation; later stages not stated [§3.1] | §3.1, then unknown | grows until the Verifier confirms [§3.1] |
| P-STATE-4 | the seed pool H_0 with h_0, the scores s_i, and a record of the seeds already run | [§3.1] [§3.3] | Idea Generator Agent and Novelty Checker; the record, each round | round 0 takes the top N_0; each later round the next N_e "highest-ranked unevaluated seed ideas" (tex:sections/3_new_method.tex:76) [§3.3] | §3.1 to selection | the pool is fixed once sorted; the record grows [§3.3] [ours] |
| P-STATE-5 | the baseline, E_base and C_base | [§3.2] | Baseline Coding Agent | every A_Coder call: the Subset Coder modifies C_base and the Subset Critic reads E_base (tex:sections/3_new_method.tex:40-41) | §3.2 to selection | no: each idea starts from the same C_base, so it is copied [inferred] [§3.2] |
| P-STATE-6 | one idea's working state: h, E_sub^h, C_sub^h, E_full^h, C_full^h, d^h, r^h | [§3.2] | the coders, critics and engineers inside A_Coder | the next step of the same call | one A_Coder call | yes: engineering rewrites h and its code [§3.2] (tex:sections/3_new_method.tex:45) |
| P-STATE-7 | the traces R_k and their union R_<k, tuples (h, E^h, C^h, d^h, r^h) | [§3.3, Eq. 3] | A_Coder | the `Good` count; A_Evolve reads all of them, the "diagnostic failure logs" of `Bad` ideas included (tex:sections/3_new_method.tex:68); the Selector receives every `Good` idea's C^h [§3.3, Eq. 4] | §3.3 to selection | append-only [inferred] [§3.3] |
| P-STATE-8 | a round's candidates: I_k of N_k ideas, H_0^(k) of N_e seeds, H_k, and the round index k | [§3.3] | A_Evolve and the seed record | A_Coder | one round | no [ours] |
| P-STATE-9 | the core state, h_best, E_best, C_best | [§3.3, Eq. 4] [§3.6] | the Selector; replaced in §3.4 and §3.6 | ablation, drafting, the rebuttal coder, both comparisons, the export [§3.4] [§3.5] [§3.6] | selection to export | only through the guard, "if and only if" the Result Comparison Agent prefers the new result (tex:sections/3_new_method.tex:112) [§3.4] |
| P-STATE-10 | an ablation pass: plans p_i (N_p of them), outcomes c_i, E_abl, and d_abl with r_abl | [§3.4] | Ablation Planner, Ablation Coding Agent, Ablation Critic | the Critic; A_FullEng reads r_abl; the last E_abl goes to drafting [§3.4] [§3.5] | one pass; the last E_abl lasts to drafting | regenerated after an update [§3.4] (tex:sections/3_new_method.tex:113) |
| P-STATE-11 | a refinement candidate, h_new, E_new, C_new | [§3.4] [§3.6] | A_FullEng | the Result Comparison Agent | until its verdict | promoted to the core state, or discarded [§3.4] [§3.6] |
| P-STATE-12 | the manuscript P_new | [§3.5] | Initial Drafter, then Paper Enhancer | Reviewer, Enhancer, Meta-Reviewer, the export [§3.5] [§3.6] | one downstream pass; re-drafted after a meta restart [§3.6] | yes: each enhancement replaces it, and the last is kept (U-TOP-7) [§3.5] |
| P-STATE-13 | the review R_new with its score s_review, also written s_new | [§3.5] | Peer Reviewer | Rebuttal Planner, Enhancer, Meta-Reviewer [§3.5] [§3.6] | until the next review | yes: overwritten each round, not accumulated, so the Meta-Review Agent sees the last review only [inferred] [§3.5] (tex:sections/3_new_method.tex:131) [§3.6] |
| P-STATE-14 | a rebuttal round: tasks t_i (N_t of them), results e_i, E_reb | [§3.5] | Rebuttal Planner and Rebuttal Coding Agent | Paper Enhancer [§3.5] | one rebuttal round | no [ours] |
| P-STATE-15 | the meta decision d_meta with r_meta | [§3.6] | Meta-Review Agent | the control flow; A_FullEng reads r_meta [§3.6] | one meta-review | no [ours] |
| P-STATE-16 | the chain of codebase versions: C_base, C_sub^h, C_full^h, C^h, C_best, C_new, C+ | [§3.2] [§3.3] [§3.4] [§3.6] | the coders, the engineers and A_FullEng | each the next | the run | copied, never edited in place [inferred]: the update happens "if and only if" the new result is preferred (tex:sections/3_new_method.tex:112), and a failed refinement ends with "the previous best outputs" (tex:sections/3_new_method.tex:150) |
| P-STATE-17 | the outputs P+ and C+ | [§3, Eq. 1] [§3.6] | the export, from P_new and C_best | the reader, and the next run's G (P-TOP-6) [§4.3] | after the run | no [ours] |

- **What crosses stages [ours].** Beside the core state (P-STATE-9), the seed pool with its record (P-STATE-4), the baseline (P-STATE-5), the traces with every `Good` codebase and every `Bad` failure log (P-STATE-7), and the last E_abl, P_new and R_new (P-STATE-10, P-STATE-12, P-STATE-13) outlive the stage that made them [§3.3] [§3.4] [§3.5] [ours]. Our first version said only the core state and those last three cross; verdict: wrong, corrected by the table [ours].
- **Checkpoints [ours].** *Initial Implements* and *Idea Refinement* together take 63.9% of the time and 65.5% of the cost, and a run lasts 2.51 days on average, 6.1% of runs 5 days or more (claims.md C-DISC-1, C-DISC-2) [Fig. 10] (image); so the unit that is checkpointed and resumed must sit inside A_Coder [ours].
- **Symbol collisions (A-TOP-5).** Calligraphic R names both the traces R_k and the review R_new; the score is s_review and s_new; the critic is A_AblCritic and A_AblCrit; "baseline" means E_best in §3.4 and §3.6 [§3.3] [§3.4] [§3.5] [§3.6].

## 9. Coding-session bound

- **Session, our definition.** One invocation of an agent that App. A.2 routes to Claude Code, or that §4.2 says uses the Coding Agent; one per ablation plan and one per rebuttal task, since §3.4 runs the coder "for each ablation plan" and §3.5 runs it on each planned task [App. A.2] [§4.2] [§3.4] [§3.5] [ours]. The paper never defines a session (U-CFG-2) [ours].
- **Switches for the ambiguous terms, and the readings taken [ours].** β_T = 1 and β_I = 0 if the baseline runs once per task, the reverse if it runs per idea (A-BASE-1); E_f is the full-set engineering limit (A-FULL-2); π and ρ are 1 if the Ablation Planner and the Rebuttal Planner are Claude Code sessions (A-CFG-1); φ and μ count specification-filter and method-code-audit sessions, set to 0 below (U-INT-1, U-INT-3) [§3.2] [§4.2] [App. A.2]. Budgets reset for the meta pass (U-META-1), N_peer counts rebuttal cycles (A-PEER-1), and A_FullEng is one call, not a new critic loop (U-ABL-2) [§3.4] [§3.5] [§3.6] [ours].

| Scope | Upper bound on coding sessions | Under App. A.2 | Terms the paper leaves open |
|---|---|---|---|
| One idea through A_Coder | β_I + 1 + N_eng + 1 + E_f | 6, with β_I = 0 and E_f = 2 [§3.2] [App. A.2] | E_f, β_I, φ [ours] |
| One idea pruned on the subset | β_I + 1 + N_eng | 3 [§3.2] [App. A.2] | β_I [ours] |
| Ideas evaluated, n_I | N_0 + K(N_k + N_e), capped by the seeds left in H_0 | 10 if N_0 = 2, 9 if N_0 = 1; 8 if the four rounds include round 0 [§3.3] [App. A.2] | N_0 (A-EVO-1), N_seed (U-SEED-1), K's count (A-EVO-2) [ours] |
| §3.2–§3.3 | β_T + n_I (β_I + 2 + N_eng + E_f) | 61 with the baseline once; 70 with a baseline per idea [§3.2] [§3.3] | as above [ours] |
| §3.4, one pass | (1 + N_abl)(π + N_p) + N_abl | 2N_p + 1 if π = 0; 2N_p + 3 if π = 1 [§3.4] [App. A.2] | N_p (U-ABL-1), π [ours] |
| §3.5, one pass | N_peer (ρ + N_t + 1) + μ, the 1 being the Enhancer | 2N_t + 2 if ρ = 0; 2N_t + 4 if ρ = 1 [§3.5] [App. A.2] | N_t (U-PEER-1), ρ, μ; N_t + 1 if N_peer counts reviews [ours] |
| §3.6 | N_meta, the A_FullEng call | 1 [§3.6] [App. A.2] | none [ours] |
| Whole run, excluding integrity sessions (φ = μ = 0) | T_idea + (1 + N_meta)(T_abl + T_peer) + N_meta | 68 + 4N_p + 4N_t if π = ρ = 0; 76 + 4N_p + 4N_t if π = ρ = 1 [App. A.2] | N_p, N_t [ours] |

- **Illustration, not the paper's configuration [ours].** With N_p = 6, the top of the "5–6 ablations per paper" that Table 15 reports for the 4 ICLR 2026 tasks ScientistTwo completed, and the count of p. 11's example, *full tables for all six ablations*, the bound is 92 + 4N_t; with N_p = 7, as in App. D's draft, it is 96 + 4N_t [Tab. 15] [p. 11] [pp. 64–65] [ours]. At N_p = 6, N_t = 3 and N_0 = 2, the readings left open span 97 to 127 sessions without integrity sessions, or 99 to 129 with note-check.md's 2: the low end is note-check.md's reading of no ablation refinement in the meta pass, 7 fewer than this table's 104, and the high end adds a per-idea baseline (+9), both planners as sessions (+8) and A_FullEng's own full-set loop (+6) to the 104. Our first span, 99 to 127, mixed the two bases; verdict: wrong [ours].
- **Why the bound is loose [ours].** Pruning at the subset (3 sessions instead of 6) and the early stop at S = 4 successes cut the idea stage; the figure is a ceiling for budgeting, not an expected count [§3.2] [§3.3] [ours].
- **The floors [ours].** The cheapest task fails: every idea is judged `Bad` at once on the subset, so all rounds run and the process stops without a paper (tex:sections/3_new_method.tex:86), after 1 baseline + 1 session per idea: 10 sessions at N_0 = 1 (9 ideas) and 11 at N_0 = 2 (10 ideas), counting no integrity sessions, since nothing is drafted, with the baseline once per task (A-BASE-1) and K counted after round 0 (A-EVO-2); a specification filter after every experiment would add up to one session per idea (U-INT-1), and note-check.md's special case C spans a failed task from 10 to 55 sessions at N_0 = 1 and 11 to 61 at N_0 = 2 [§3.2] [§3.3] [App. A.2] [ours]. The cheapest task that succeeds has no refinement anywhere, N_p = 5 (the low end of Table 15) and a first review of 8 or more: at N_0 = 2, 1 baseline + 4 `Good` ideas × 2 (an early stop after round 1) + 5 ablations = 14 sessions, or 16 with note-check.md's 2 integrity sessions [Tab. 15] [§3.3] [App. A.2] [ours]. At N_0 = 1 with an end-of-round stop test (U-EVO-1), round 2 must finish, and its second idea can fail at once on the subset for 1 session: 1 + 9 + 5 = 15, or 17 with the 2 integrity sessions. The register's D-2 first gave 18, counting that fifth idea as `Good`, and now gives 17 [§3.2] [§3.3] [ours].
- **An expected count, as an illustration only [inferred].** Figure 10b gives *Idea Refinement* 45.4% of the cost and *Initial Implements* 20.1%, a ratio of 2.26; if *Initial Implements* is round 0 with N_0 = 2 and every idea costs the same, a task runs about 2 + 2 × 2.26 ≈ 6.5 ideas, against a ceiling of 10 [Fig. 10] (image) [inferred]. The caveats: the 33 NeurIPS 2025 tasks behind the figure are successes only, a failed task runs every round, *Initial Implements* may include the baseline, and an idea pruned on the subset costs less [§4.3] [ours].
- **What it leaves out [ours].** Critic, Selector, Result Comparison and Meta-Review calls are LLM calls, not coding sessions; if A_FullEng runs its own full-set critic loop (U-ABL-2), each of its N_abl(1 + N_meta) + N_meta = 3 calls can grow to 1 + E_f sessions [§3.4] [§3.6] [ours].

## 10. Gaps found here

Cross-cutting items (TOP, CFG, ROSTER) are in full below; each stage's items are in full at the end of its stage file, and 10.2 indexes all 68. Each full entry names its row in the decision register, unspecified.md, or says it is new [ours].

### 10.1 Cross-cutting items, in full

- **A-TOP-1 · INCONSISTENT · What a stage returns when its limit runs out.** *Register: A-TOP-1.* Listing 1 ends with `return None` after `max_rounds` [Lst. 1] (tex:tables/pseudo_code.tex:35). §3.5 keeps the candidate explicitly; §3.4 and §3.6 imply keeping through closing clauses that follow both endings of their loops, the limit and the good verdict [inferred] [§3.4] [§3.5] [§3.6].
  - §3.4, implied [inferred]: the loop ends "ensuring a fully optimized hypothesis prior to manuscript generation" [§3.4] (tex:sections/3_new_method.tex:114).
  - §3.5, explicit: "review iterations is reached, producing a polished, thoroughly validated final manuscript" [§3.5] (tex:sections/3_new_method.tex:132).
  - §3.6, implied [inferred]: "yielding a rigorously validated final contribution" [§3.6] (tex:sections/3_new_method.tex:151).
  - Reading 1, Listing 1: the stage discards its candidate and the task produces nothing [Lst. 1]. Reading 2, the text: a candidate passes on; whether it is the last or the best differs by stage (U-TOP-7) [§3.5] [§3.6].
  - Evidence for reading 2: the 86 generated papers average 7.5 under ScholarPeer, below the loop's threshold of 8, so papers that never reached 8 were still produced [Tab. 3] [App. A.2] [inferred].
  - Decision forced: an exhaustion rule for each stage [ours].
- **A-TOP-2 · AMBIGUOUS · What a limit counts.** *Register: A-TOP-2.* Listing 1 calls the critic at most `max_rounds` times, and a refinement made in the last round is never judged [Lst. 1] (tex:tables/pseudo_code.tex:27-32). App. A.2 counts refinements for three loops, "we apply engineering techniques for at most two rounds", "we refine the idea at most once" and "with review-based refinement conducted at most once", and rounds for the limitation and peer-review loops [App. A.2] (tex:sections/appendix.tex:155).
  - Reading 1: the A.2 number is `max_rounds`: N critic calls, the N-th refinement wasted [Lst. 1]. Reading 2: the A.2 number caps judged refinements: N refinements and N + 1 critic calls [App. A.2] [ours].
  - Applies to the 16 limitation rounds, N_eng, the full-set budget, N_abl, N_peer and N_meta [App. A.2]. Decision forced: critic calls per loop [ours].
- **A-TOP-3 · INCONSISTENT · Does the run loop until approval?** *Register: A-TOP-3.* The overview says the engine "iterates through the pipeline until the manuscript is approved for submission" [§3] (tex:sections/3_new_method.tex:5), and §1 promises "triggering recursive refinement loops until rigorous acceptance criteria are satisfied" [§1] (tex:sections/1_introduction.tex:18).
  - Against it: a refinement that is not better "terminates the process using the previous best outputs" [§3.6] (tex:sections/3_new_method.tex:150), and App. A.2 allows "review-based refinement conducted at most once" [App. A.2].
  - Decision forced: a run can export a manuscript the Meta-Review Agent returned as `Refine`; whether to mark such outputs [ours].
- **A-TOP-4 · AMBIGUOUS · What G is.** *Register: A-TOP-4.* Reading 1, a natural-language challenge: Figure 3's human request *I want to build an efficient tabular foundation model*, and the abstract's "given a fundamental challenge by a human expert" [Fig. 3] (image) [Abstract].
  - Reading 2, an accepted paper with its code: tasks are papers "whose problem specifications and codebases serve as benchmark tasks for" ScientistTwo [§4.1] (tex:sections/4_experiment.tex:16).
  - Decision forced: the task interface; every experiment uses reading 2 [§4.1] [ours].
- **A-TOP-5 · INCONSISTENT, notation · Symbol collisions.** *Register: A-TOP-5.* Calligraphic R names the traces R_k [§3.3, Eq. 3] and the review R_new [§3.5] (tex:sections/3_new_method.tex:123).
  - The score is s_review (tex:sections/3_new_method.tex:123) and s_new (tex:sections/3_new_method.tex:132) [§3.5]; the critic is A_AblCritic (tex:sections/3_new_method.tex:106) and A_AblCrit (tex:sections/3_new_method.tex:114) [§3.4].
  - "The baseline variables are updated" means (h_best, E_best, C_best) [§3.4] (tex:sections/3_new_method.tex:112); "fails to outperform the baseline, the refinement is discarded" compares with E_best [§3.6] (tex:sections/3_new_method.tex:150); elsewhere the baseline is the human SOTA, E_base [§3.2].
  - Decision forced: distinct names in our schemas; the §3.6 test compares with E_best [inferred] [§3.6].
- **U-TOP-1 · UNSPECIFIED · The contents of G.** *Register: U-TOP-1.* The paper's form, the codebase's state, the task rules the specification filter needs, the reported numbers the full-set critic needs, the benchmark subset and the compute environment; also the fixed evaluator, which no task input provides (U-INT-4), the definition of the full benchmark, and the data splits (U-TOP-5) [§3.2] [§4.1] [§4.2] [Tab. 1]. Decision forced: a task schema [ours].
- **U-TOP-2 · UNSPECIFIED · Failure handling.** *Register: U-TOP-2.* No stage says what happens when an agent errs, code never runs, a run times out or a tool is down; there is no per-session time or cost limit, only averages over 33 NeurIPS 2025 tasks [§3] [§4.3] [Fig. 10] (image). Decision forced: retry, timeout and budget policy [ours].
- **U-TOP-3 · UNSPECIFIED · Prompts and schemas.** *Register: U-TOP-3.* No agent's prompt, input format or output schema appears in §3 or App. A.2; Appendices C–D show outputs only, analysed in artifacts.md [§3] [App. A.2] [App. C]. Decision forced: every prompt and schema [ours].
- **U-TOP-4 · UNSPECIFIED · Parallelism.** *Register: U-TOP-4.* Whether a round's candidates, the ablation plans or the rebuttal tasks run in parallel [§3.3] [§3.4] [§3.5]. Decision forced: the scheduler [ours].
- **U-TOP-5 · UNSPECIFIED · Which data split each decision reads.** *Register: U-TOP-5 (U-NOTE-1 and U-ART-5 are aliases there).* No stage names a split: the subset and full-set critics, the Selector, which picks among ideas "evaluated on the full benchmark", and both strict-improvement gates read the benchmark that is then reported [§3.2] [§3.3] [§3.4] [§3.6].
  - The one trace shows OOD test results steering a redesign [p. 46] and an auditor extracting *test features* [p. 47]; App. D's draft runs an ablation on a *subset test split* [p. 69]. Elsewhere in this folder: U-NOTE-1 and U-ART-5 [ours].
  - Decision forced: a validation split inside each task, disjoint from the test split, for every decision in the loop [ours].
- **U-TOP-6 · UNSPECIFIED · No success criterion for any agent.** *Register: U-TOP-6.* The paper tests agents only end to end: the rebuttal through Table 5, the meta-review through Table 6 (n = 1), the integrity agents through Table 7, the coding backend through Table 8, and the Selector and the Evolver through Figure 9b's *Evolved Idea Selected: 27* of 49; no rate of any §3 verdict is reported [Tab. 5] [Tab. 6] [Tab. 7] [Tab. 8] [Fig. 9b] (image). Decision forced: a success test for each agent on a golden set, beside the end-to-end numbers [ours].
- **U-TOP-7 · UNSPECIFIED · At the limit, the last candidate or the best one?** *Register: A-TOP-1 (U-TOP-7 is an alias there: last or best is one more value of the exhaustion parameter).* A-TOP-1's reading 2 merged two policies [ours]. Peer review overwrites the manuscript, since "The updated manuscript is re-evaluated by" the reviewer, so the exported paper can score below an earlier round's [§3.5] (tex:sections/3_new_method.tex:131).
  - Ablation and meta-review keep the best, through their guard [§3.4] (tex:sections/3_new_method.tex:112) [§3.6] (tex:sections/3_new_method.tex:148); the limitation loop keeps its last set [inferred] [§3.1]; no sentence says whether a better earlier manuscript may be exported [§3.5]. Decision forced: last or best, per stage; for peer review, whether to keep the best-scoring round [ours].
- **A-CFG-1 · AMBIGUOUS · Which agents run on Claude Code.** *Register: A-CFG-1.* App. A.2 names four: "the Idea Experiment Coding Agent, the Ablation Study Agent, the Rebuttal Agent, and the Draft Enhancer" [App. A.2] (tex:sections/appendix.tex:155); §4.2 says Claude Code is used "whenever coding capabilities are required" [§4.2] (tex:sections/4_experiment.tex:46).
  - Undetermined: the Baseline Coding Agent, both engineers, A_FullEng in §3.4 and §3.6, the integrity Coding Agent, the Ablation Planner and the Rebuttal Planner [§3.2] [§3.4] [§3.5] [§4.2].
  - Reading 1, A.2 literally: only the named groups use Claude Code [App. A.2]. Reading 2: every coding agent does. A.2 opens "Unless otherwise specified", which leaves room for §4.2's rule; Figure 3's experiment boxes hold only a *Coding Agent* and a *Critic Agent*, with no separate engineer; the *Ablation Study Agent* box holds the *Planning Agent*, and the ablation stage's *New Idea* re-enters the *Full-Set Experiment Agent* [App. A.2] [§4.2] [Fig. 3] (image).
  - Elsewhere in this folder: artifacts.md's P-ART-3 names Claude Code for A_FullEng, which is reading 2 (F-AR-10) [ours].
  - Decision forced: the model-routing file [ours].
- **A-CFG-2 · AMBIGUOUS, minor · A second Gemini version.** *Register: A-CFG-2.* Antigravity is "powered by Gemini 3.8 Flash" [§4.2] (tex:sections/4_experiment.tex:46) [Tab. 8], while every other mention is Gemini 3.6 Flash [§4] [App. A.2]: a second version or a typo; it touches only the coding-backend experiment, 5 ICLR 2026 tasks [ours].
- **U-CFG-1 · UNSPECIFIED · Runtime configuration.** *Register: U-CFG-1.* Sampling parameters, context limits, Claude Code's tools, permissions and turn limits, and the experiment hardware; §4.3 mentions only virtual machine costs [App. A.2] [§4.3]. Decision forced: all runtime configuration [ours].
- **U-CFG-2 · UNSPECIFIED · What one coding session is.** *Register: U-CFG-2.* Per plan, per task, per idea, or one long session per stage [§3.4] [§3.5] [App. A.2]. Decision forced: session granularity, which sets the bound in section 9 [ours].
- **A-ROSTER-1 · AMBIGUOUS · Name collisions.** *Register: A-ROSTER-1.* "Peer-Review Agent" is the reviewer in §1, where "generated drafts are critiqued by a simulated Peer-Review Agent", but the box of Review Agent and Rebuttal Agent in Figure 3 [§1] (tex:sections/1_introduction.tex:18) [Fig. 3] (image).
  - "Idea Generator" is both the §3.1 agent and Figure 3's top-level box; *Idea Refiner* appears twice in Figure 3, in the ablation box and in the meta-review box [§3.1] [Fig. 3] (image).
  - Decision forced: the canonical names of section 7 [ours].

### 10.2 Index of every gap

| ID | Class | In one line | In full at |
|---|---|---|---|
| A-TOP-1 | INCONSISTENT | Listing 1 discards at the limit; §3.4–§3.6 keep the candidate [Lst. 1] [§3.5] | 10.1 |
| A-TOP-2 | AMBIGUOUS | a limit counts critic calls or judged refinements [Lst. 1] [App. A.2] | 10.1 |
| A-TOP-3 | INCONSISTENT | loop until approval, against one meta refinement and termination [§3] [§3.6] | 10.1 |
| A-TOP-4 | AMBIGUOUS | G as a natural-language challenge or as a paper with code [§4.1] [Fig. 3] (image) | 10.1 |
| A-TOP-5 | INCONSISTENT | symbol collisions: R, s_new, A_AblCrit, baseline [§3.4] [§3.5] | 10.1 |
| U-TOP-1 | UNSPECIFIED | the contents and format of G [§4.1] | 10.1 |
| U-TOP-2 | UNSPECIFIED | failure handling, timeouts and budgets [§3] | 10.1 |
| U-TOP-3 | UNSPECIFIED | prompts and output schemas of every agent [§3] | 10.1 |
| U-TOP-4 | UNSPECIFIED | parallelism within a round or a stage [§3.3] | 10.1 |
| U-TOP-5 | UNSPECIFIED | which data split each decision reads; none is named [§3.2] [§3.3] | 10.1 |
| U-TOP-6 | UNSPECIFIED | no success criterion for any agent; the tests are end to end only [Tab. 5] [Fig. 9b] (image) | 10.1 |
| U-TOP-7 | UNSPECIFIED | at the limit, the last candidate or the best one [§3.4] [§3.5] | 10.1 |
| A-CFG-1 | AMBIGUOUS | which agents run on Claude Code [App. A.2] [§4.2] | 10.1 |
| A-CFG-2 | AMBIGUOUS | Gemini 3.8 Flash beside Gemini 3.6 Flash [§4.2] | 10.1 |
| U-CFG-1 | UNSPECIFIED | runtime configuration of models and Claude Code [App. A.2] | 10.1 |
| U-CFG-2 | UNSPECIFIED | what one coding session is [App. A.2] | 10.1 |
| A-ROSTER-1 | AMBIGUOUS | one name for two things: Peer-Review Agent, Idea Generator, Idea Refiner [Fig. 3] (image) | 10.1 |
| A-LIM-1 | AMBIGUOUS | what finding limitations outputs after 16 rounds [§3.1] | [stages/01](stages/01-seed-ideas.md) |
| U-LIM-1 | UNSPECIFIED | the Verifier's criterion and both agents' formats [§3.1] | [stages/01](stages/01-seed-ideas.md) |
| U-SEED-1 | UNSPECIFIED | N_seed has no value [§3.1] [App. A.2] | [stages/01](stages/01-seed-ideas.md) |
| A-SEED-1 | AMBIGUOUS | novelty as a filter, or only a ranking [§3] [§3.1] | [stages/01](stages/01-seed-ideas.md) |
| U-SEED-2 | UNSPECIFIED | the novelty score and the retrieval behind it [App. A.2] | [stages/01](stages/01-seed-ideas.md) |
| A-SEED-2 | AMBIGUOUS | which agent generates h_0 [Fig. 4] (image) | [stages/01](stages/01-seed-ideas.md) |
| U-SEED-3 | UNSPECIFIED | the Idea Generator's inputs and content constraints [§3.1] [App. B] | [stages/01](stages/01-seed-ideas.md) |
| A-BASE-1 | AMBIGUOUS | baseline once per task, or once per idea [§3.2] [Fig. 5] (image) | [stages/02](stages/02-evaluating-ideas.md) |
| U-BASE-1 | UNSPECIFIED | the benchmark subset [§3.2] | [stages/02](stages/02-evaluating-ideas.md) |
| U-BASE-2 | UNSPECIFIED | what happens if the baseline cannot be reproduced [Tab. 1] | [stages/02](stages/02-evaluating-ideas.md) |
| U-SUB-1 | UNSPECIFIED | the subset critic's criteria [§3.2] | [stages/02](stages/02-evaluating-ideas.md) |
| U-SUB-2 | UNSPECIFIED | tuning parity: the idea is engineered, the baseline never is [§3.2] [Tab. 1] | [stages/02](stages/02-evaluating-ideas.md) |
| A-FULL-1 | AMBIGUOUS | the full-set reference: the reported SOTA, or a reproduced baseline [Tab. 1] [App. B] | [stages/02](stages/02-evaluating-ideas.md) |
| A-FULL-2 | AMBIGUOUS | the full-set engineering limit [§3.2] [App. A.2] | [stages/02](stages/02-evaluating-ideas.md) |
| U-FULL-1 | UNSPECIFIED | the full-set verdicts and their effects [§3.2] | [stages/02](stages/02-evaluating-ideas.md) |
| U-CODER-1 | UNSPECIFIED | what A_Coder returns for an idea pruned on the subset [§3.2, Eq. 2] | [stages/02](stages/02-evaluating-ideas.md) |
| A-EVO-1 | AMBIGUOUS | round 0: top-N_0 seeds, against one seed and one evolved idea; INCONSISTENT only if round 0 counts among A.2's rounds [§3.3] [App. A.2] | [stages/03](stages/03-refining-ideas.md) |
| A-EVO-2 | AMBIGUOUS | whether the four rounds include round 0 [App. A.2] [Fig. 9] (image) | [stages/03](stages/03-refining-ideas.md) |
| U-EVO-1 | UNSPECIFIED | when the S test runs [§3.3] | [stages/03](stages/03-refining-ideas.md) |
| U-EVO-2 | UNSPECIFIED | what A_Evolve reads; whether evolved ideas get a novelty check [§3.3] | [stages/03](stages/03-refining-ideas.md) |
| U-EVO-3 | UNSPECIFIED | running out of unevaluated seeds [§3.3] | [stages/03](stages/03-refining-ideas.md) |
| U-EVO-4 | UNSPECIFIED | what a run with no success leaves behind [§3.3] | [stages/03](stages/03-refining-ideas.md) |
| U-SEL-1 | UNSPECIFIED | the Selector's criterion [§3.3] | [stages/03](stages/03-refining-ideas.md) |
| U-SEL-2 | UNSPECIFIED | how much the Selector reads: every `Good` idea arrives with its codebase [§3.3, Eq. 4] | [stages/03](stages/03-refining-ideas.md) |
| A-ABL-1 | INCONSISTENT | no reject verdict in §3.4, a rejection in App. B [§3.4] [App. B] | [stages/04](stages/04-ablation.md) |
| A-ABL-2 | INCONSISTENT | after a failed comparison or at the limit: drafting, or the end of the task [Fig. 7] (image) [Lst. 1] | [stages/04](stages/04-ablation.md) |
| A-ABL-3 | AMBIGUOUS | strict outperformance, or the agent's preference [§3.4] | [stages/04](stages/04-ablation.md) |
| U-ABL-1 | UNSPECIFIED | N_p has no value [§3.4] | [stages/04](stages/04-ablation.md) |
| U-ABL-2 | UNSPECIFIED | whether A_FullEng runs a full-set critic loop [§3.4] [Fig. 3] (image) | [stages/04](stages/04-ablation.md) |
| U-ABL-3 | UNSPECIFIED | whether ablation code stays in C_best and C+ [§3.4] | [stages/04](stages/04-ablation.md) |
| U-ABL-4 | UNSPECIFIED | the critic's verdict on a re-ablation once N_abl is spent [§3.4] [Fig. 7] (image) | [stages/04](stages/04-ablation.md) |
| U-ABL-5 | UNSPECIFIED | where the Ablation Critic draws the line between `Refine` and a reject [§3.4] [App. B] | [stages/04](stages/04-ablation.md) |
| U-ABL-6 | UNSPECIFIED | how much the Ablation Critic reads: results only, or the implementation too [§3.4] [p. 46] | [stages/04](stages/04-ablation.md) |
| U-DRAFT-1 | UNSPECIFIED | the drafter's inputs beyond h_best, E_best and E_abl [§3.5] | [stages/05](stages/05-drafting-peer-review.md) |
| U-DRAFT-2 | UNSPECIFIED | drafting failures and who makes the figures [§3.5] | [stages/05](stages/05-drafting-peer-review.md) |
| A-PEER-1 | AMBIGUOUS | N_peer counts reviews, or rebuttal cycles [§3.5] [Tab. 5] | [stages/05](stages/05-drafting-peer-review.md) |
| U-PEER-1 | UNSPECIFIED | N_t has no value [§3.5] | [stages/05](stages/05-drafting-peer-review.md) |
| U-PEER-2 | UNSPECIFIED | whether rebuttal code stays in C_best and C+ [§3.5] | [stages/05](stages/05-drafting-peer-review.md) |
| U-PEER-3 | UNSPECIFIED | ScholarPeer's configuration and backbone [§3.5] | [stages/05](stages/05-drafting-peer-review.md) |
| U-PEER-4 | UNSPECIFIED | what the Enhancer reads and may change [§3.5] | [stages/05](stages/05-drafting-peer-review.md) |
| A-META-1 | AMBIGUOUS | the restart's extent: the text's list, or Figure 7's path [§3.6] [Fig. 7] (image) | [stages/06](stages/06-meta-review.md) |
| A-META-2 | AMBIGUOUS | whether the meta-reviewer is asked again after the restart [§3.6] | [stages/06](stages/06-meta-review.md) |
| U-META-1 | UNSPECIFIED | whether loop budgets reset for the restart [§3.6] | [stages/06](stages/06-meta-review.md) |
| U-META-2 | UNSPECIFIED | the meta-reviewer's criterion [§3.6] | [stages/06](stages/06-meta-review.md) |
| A-INT-1 | INCONSISTENT | reproducibility by a prompt (§4.2), or a re-run gate (App. B) [§4.2] [App. B] | [stages/07](stages/07-integrity.md) |
| A-INT-2 | AMBIGUOUS | which Writer Agent repairs references and the method section [§4.2] [Fig. 3] (image) | [stages/07](stages/07-integrity.md) |
| A-INT-3 | AMBIGUOUS | which Coding Agent runs the filter and the audit [§4.2] | [stages/07](stages/07-integrity.md) |
| U-INT-1 | UNSPECIFIED | where the specification filter runs, and what discarding does [§4.2] [fn. 2] | [stages/07](stages/07-integrity.md) |
| U-INT-2 | UNSPECIFIED | where the task rules come from [§4.2] | [stages/07](stages/07-integrity.md) |
| U-INT-3 | UNSPECIFIED | where and how often the reference and alignment steps run [§4.2] | [stages/07](stages/07-integrity.md) |
| U-INT-4 | UNSPECIFIED | no fixed evaluator: agent code computes every metric [§3.2] [§4.2] | [stages/07](stages/07-integrity.md) |
