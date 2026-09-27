> **Moved into the repository on 2026-09-28, after the reviews; the text below is unchanged.**
> Three of its findings did not survive the review as written: 2, 34 and 36. See
> `orchestrator-coverage.md`, section "After the persona review".

# Orchestrator's independent reading of arXiv:2609.19644v1 (control list)

Written 2026-09-27 by the orchestrating session after reading every TeX file, Figures 9–10 as
images, the Appendix C/D page mapping, and the PDF/HTML numbering. Kept OUT of the repo until the
analysts and reviewers finish, so it cannot anchor them; then used to mark their coverage.
Locations use PDF numbering. Tex paths are relative to docs/paper/source/.

## Engine mechanics
1. Lst. 1: on exhaustion `return None`; the candidate produced by the last refine is never re-judged (tex:tables/pseudo_code.tex:26-35).
2. Tab. 1 rows without a critic (Reproduce baseline on subset; Initial drafting) or without a refine (Select best idea). The primitive does not cover every row as written.
3. Verdict vocabularies differ: subset critic {Bad, Good, Engineer} §3.2; ablation critic {Good, Refine} §3.4; meta {Accept, Refine} §3.6; peer review: numeric score vs threshold 8 §3.5; limitation verifier: sufficient/insufficient §3.1; novelty: a score §3.1; idea evolution's "critic" is the idea experiment itself (Tab. 1).
4. Exhaustion differs by stage: limitations continue with the current set (§3.1 "or maximum number of iterations is reached"); subset → Bad and pruned (§3.2); ablation → continue to drafting; peer review → continue with the manuscript ("producing a polished ... final manuscript"); meta → export (implied, unstated).
5. Seed generation stops at a COUNT N_seed (value unspecified), not a critic verdict; sorting by novelty score; whether low-novelty ideas are dropped is unclear ("distinct, higher-novelty ideas"). h_0 is generated first by an "initial idea" step (Fig. 4 label "Initial Idea Generator").
6. Full-set critic compares with the "original SOTA result" (Tab. 1) while the subset critic compares with the "reproduced baseline" (Tab. 1); App. B says each system "measures against its own reproduced baseline"; Tab. 16 DMSQD "+0.61% ... over reproduced DMS". Is a full-set baseline ever reproduced? Tab. 1 has only "Reproduce baseline on subset". AMBIGUOUS/INCONSISTENT.
7. Full-set engineering limit: not named in §3. A.2 "If the Idea Critic Agent flags an idea for engineering refinement, we apply engineering techniques for at most two rounds": "Idea Critic Agent" matches neither the Subset nor the Full-Set Critic by name → does N_eng = 2 cover both?
8. A.2 "In each idea experimentation round, we evaluate two candidates: one selected from the seed ideas and the other an evolved idea" → N_e = 1, N_k = 1 for k ≥ 1; N_0 AMBIGUOUS (no evolved idea exists at k = 0). Fig. 9b "Initial" selects only seeds (n = 14, 100% seed) (image).
9. A.2 "up to four rounds": Fig. 9a/9b x-axis Initial, Round 1–4 → K = 4 refinement rounds after an initial round (5 rounds in all); §3.3's sums i = 0..K agree.
10. S = 4 (A.2 "terminating early once four successful ideas are obtained").
11. At round K with 1..S−1 successes → selection proceeds (§3.3 "Upon discovering at least one successful idea"); with 0 → "terminates the entire process" (outputs nothing; a failed task).
12. Selector is an LLM comparing "performance metrics and execution logs" across Good ideas "evaluated on the full benchmark" → selection is a judgement, not an argmax.
13. Ablation: N_p unspecified (Tab. 15 "5--6 ablations per paper"); notation A_AblCritic vs A_AblCrit; critic returns {Good, Refine} but App. B/Tab. 16 TeCh: the ablation critic "rejected it ... so it was not accepted as a contribution" → a reject outcome exists in practice but not in §3.4 → INCONSISTENT. Tab. 15 caption: ScientistTwo "additionally requires the gain to be attributable to the proposed mechanism in ablation".
14. Result Comparison Agent: §3.4 "verifies whether E_new strictly outperforms E_best" and "if and only if E_new is preferred than E_best by the Result Comparison Agent" → numeric rule or LLM preference? AMBIGUOUS.
15. After an ablation-driven update, "re-executes the ablation planning phase on the updated candidate"; N_abl = 1: does the re-run ablation get another critic pass? What if it says Refine again (limit spent)?
16. Peer review threshold: "(e.g., 8)" vs "s_new ≥ 8" (symbol s_new never defined, s_review is) vs A.2 "reaches 8". N_peer = 2 "at most two rounds": Tab. 5 rows Review Round 0 (no rebuttal), 1, 2 → two rebuttal cycles after the initial review.
17. Rebuttal coder executes tasks "using codebase C_best"; the Draft Enhancer runs as Claude Code with Opus 4.8 (A.2) though it edits a manuscript.
18. N_t (rebuttal tasks) unspecified.
19. Meta: N_meta = 1 (A.2 "review-based refinement conducted at most once"). On Refine: FullEng updates h_best → Result Comparison → if superior: re-run ablation planning/execution, re-drafting, peer review; else terminate with P+ ← P_new, C+ ← C_best. Whether the meta-review runs again after the redo, and what is exported when N_meta is spent without Accept: UNSPECIFIED.
20. §3.6 "fails to outperform the baseline" where E_best is meant: wording.
21. Integrity refinement agents (§4.2) are absent from §3, Tab. 1, Lst. 1 and Figs. 4–7: spec-compliance "validation filter that uses the Coding Agent to detect and discard rule-violating solutions immediately after experimentation" (which experiment?); reference verification (search-augmented LLM → Writer Agent fixes bibliography); method–code alignment (Coding Agent audit report → Writer Agent fixes method section); score verification by PROMPTING the Coding Agent for self-contained scripts. "Writer Agent" appears only in §4.2 and Fig. 3.
22. Enforcement is by prompt and LLM filters; App. B says ScientistTwo "blocks both structurally, via a reproduction re-run (I1), a protocol-immutability audit (I2), and a method--code alignment audit (I4) rather than a prompt-level list of prohibitions" while §4.2 calls the CoE audit "a post-hoc evaluation framework"; Tab. 15 "Modifies the evaluation protocol: forbidden (audit)". "Structural" here = post-hoc audit, not construction.
23. Models (A.2): Gemini 3.6 Flash except "Idea Experiment Coding Agent", "Ablation Study Agent", "Rebuttal Agent", "Draft Enhancer" (Claude Code, Opus 4.8). Names ≠ §3's: is the Baseline Coding Agent included? the Engineers? "Ablation Study Agent" = planner+coder (Fig. 3 group) or coder only? "Rebuttal Agent" = planner+coder? AMBIGUOUS.
24. Novelty evidence: "retrieves two reference papers via Google Search" (A.2).
25. Limitation loop at most 16 rounds (A.2).
26. G: "Given a scientific problem G" (§3) vs experiments take accepted papers whose "problem specifications and codebases serve as benchmark tasks" (§4.1) vs Fig. 3 human request "I want to build an efficient tabular foundation model" (image). What G contains: UNSPECIFIED.
27. Subset: "benchmark subset" (§3.2), "representative benchmark slices" (§1) — never defined; who picks it unspecified.
28. No validation/test separation anywhere: ideas are screened, engineered, selected and reported on the same full benchmark.
29. Tab. 4 gains: "we parse the main tables for 10 times using Gemini 3.6 Flash and averaged them" — LLM-extracted from the generated papers, i.e. self-reported.
30. "Success" (86/107) is never defined. TeCh counts as a failure after the ablation critic's rejection; Tab. 7 fn.: a reward-hacked success is filtered (50 → 49).
31. ScholarPeer is both the in-loop reviewer and a reported evaluator (acknowledged as "in-distribution"); SAR held out.
32. "Accept Rate" undefined for both reviewers; Tab. 5 round 0: ScholarPeer mean 5.2±2.2 with 46.9% accepted → acceptance is not "score ≥ 8"; must be the reviewer's own decision or another threshold. UNSPECIFIED.

## Claims and consistency
33. Tab. 4 AutoSOTA "Overall 105 papers" is AutoSOTA's own set, not the 107; only NeurIPS (33) and ICLR (4) share inputs.
34. Tab. 4 overall 25.2 (86) with NeurIPS 13.9 (33), ICLR 3.8 (4) → implied ICML (49) mean ∈ [34.4, 34.7]; Fig. 9a final gain on the 49 ICML tasks is 33.4% (image) → ≈1.1 pp gap. Possibly different gain procedures.
35. Fig. 10 caption "Idea refinement accounts for the majority" vs 44.9% time / 45.4% cost (image): plurality. §4.3 text: majority in "Idea Refinement, Dynamic Peer-Review, and Meta-Review" (44.9 + 15.5 = 60.4%) ✓.
36. $3765: mean over the 33 NeurIPS tasks (successful ones), token + VM costs; §5 rounds to "approximately $3,800". Time: mean 2.51 d, median 2.00 d, IQR [1.1, 3.1] d (Fig. 10a, image). Per-stage cost shares (Fig. 10b, image): Initial Implements 20.1, Idea Refinement 45.4, Ablation 15.4, Initial Drafting 3.1, Peer&Meta-Review 15.8, Seed ≈0.2 (by subtraction).
37. §4.2 ablations use "the 49 target problems sourced from ICML 2026 Spotlight papers" = the 49 successes → conditioned on success.
38. Tab. 5: ScholarPeer accept 79.6 → 93.9 while SAR 73.5 → 69.4 from round 1 to 2; the shipped config (2 rounds) is the in-loop reviewer's optimum. n = 49 (46/49 = 93.9%, 36/49 = 73.5%, 34/49 = 69.4%, 23/49 = 46.9%, 24/49 = 49.0%, 39/49 = 79.6%).
39. Tab. 6: one task, one run, no variance; EM worsens 0.004 → 0.084 (variant) / 0.071 (ours).
40. Tab. 7: Score Verif. 50/50 even without refinement agents; refs 19/1840 → 0/1814 (≈37 per paper); Method-Code 39/50 → 49/49; n = 49/50.
41. Tab. 8: Antigravity uses Gemini 3.8 Flash (main: 3.6 Flash); n = 5; SR 3/5; its 16.7 gain is over 3 tasks; Claude Code row equals Tab. 3's ICLR row and Tab. 4's ICLR 3.8.
42. Tab. 9 ratings (6.5, 5.6, 7.1): reviewer unspecified; 6.5 matches SAR in Fig. 2's caption (ScholarPeer 8.0, SAR 6.5).
43. Tab. 10: 9 reviewers, 33 NeurIPS papers; no agreement statistic; pairing and blinding unspecified.
44. Tab. 2 baselines are scored on their public papers (n = 2–21, other topics) — not a controlled comparison.
45. Tab. 3: SAR accepts 96.9% of ICML spotlights vs 69.4% for ScientistTwo on ICML; "surpass the average scores of accepted papers at ICLR 2026 and NeurIPS 2025" holds for those two venues only.
46. Abstract "consistently outperform human state-of-the-art" vs 21/107 failures.
47. 25.2% mean over the 86 successes only; median 7.7 → heavy tail.
48. Tab. 3 overall row = the n-weighted venue rows (checked: ScholarPeer accept 79/86 = 91.9 ✓; SAR 62/86 = 72.1 ✓; ratings within rounding).
49. App. B numbers (Tab. 16): RALI PLCC +0.006, SRCC +0.008 (small); DMSQD +0.61%±0.27 mean QD; T-SAE +3.4%±0.2; Pinet CV 4e-4 → 2e-14, 3.0× faster.
50. "Better" across several metrics: the critic (an LLM) decides; no aggregation rule; App. B "no target metric".
51. Tab. 16 RALI "an earlier variant was rejected by our own critic as statistically inert" → which critic? Implies significance testing that §3 never describes.
52. §3.2 "consistently outperforms the baseline" — "consistently" undefined.
53. A_Coder may return a modified h (engineering "refines h and C_sub^h").
54. A_FullEng is reused by the ablation refine and the meta refine.
55. The Evolver reads "all historic execution traces" → unbounded context; truncation unspecified.
56. Iterative frontier expansion (Tab. 9) is a mode not described in §3.
57. A.2: "ICLR 2025 format for drafting, following the PaperOrchestra" while reviews use the "standard ICLR grading scale" (§3.5).

## Expected note-check verdicts (key)
Listing 1 TRUE (PDF) / HTML "Figure 4" · control flow "full spec ... Easy" PARTLY (gaps above) · ~15 reasoning agents ≈TRUE · no prompts TRUE · Opus 4.8 coding TRUE with naming caveat · 107 papers, no subset/metric definitions TRUE · scripts + LLM validation filter TRUE · PaperOrchestra TRUE (open source: not in paper) · ScholarPeer TRUE · CoE audit from ScientistOne TRUE (details not in paper) · Table 6 TOFU/Llama-3.2-1B TRUE (-Instruct, forget10) · AutoSOTA CIFAR-10/ResNet-18 NOT IN PAPER · 107 from AutoSOTA benchmark or filtering TRUE (ICML 64 by filtering process) · ScientistOne audit specifics NOT IN PAPER · Agent SDK NOT IN PAPER · paperreview.ai = SAR TRUE (fn.), limits NOT IN PAPER · MLE-STAR cited; "same lead authors" check bib · $3,765 TRUE (33 NeurIPS) · $400k / 270 machine-days arithmetic ✓ but "machine-days" assumes 1 machine; paper reports wall-clock days · App. B covers the five ICLR tasks TRUE · four accepted, TeCh rejected TRUE · T-SAE models TRUE · RALI 7 datasets TRUE · Rule 1 "covers every row" FALSE · ScientistOne 16/75, 0→70%, Sakana writer NOT IN PAPER · no validation/test separation TRUE · Gemini parses tables 10× TRUE · Table 5 claim TRUE · "idea refinement most of its cost" PARTLY (plurality; the caption itself says majority) · Opus coding / Gemini Flash rest PARTLY (3.6 Flash; Draft Enhancer is Claude Code) · June 15 2026 credit NOT IN PAPER → task 5 · repo design, build plan, cheap profile PROPOSAL.
