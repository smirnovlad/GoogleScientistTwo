# The initial note, checked claim by claim

Revised 2026-09-27 after the persona review: fixes F-NC-1 to F-NC-5, F-1, F-2, F-5, F-6, F-8, F-9, F-13, F-14 and F-17 of `docs/reviews/paper-analysis-2026-09-27/fix-list.md`, with the edits they imply in N-20, N-83, N-86, N-88, N-110 and U-NOTE-4; then closure corrections on 2026-09-28 from `closure-evaluation-integrity-engineer.md` (its error 2 and the rest of EI1-M7), in summary item 4, N-40 to N-42, A-NOTE-10 and U-NOTE-4 [ours].

**What this is.** Every claim in `docs/inputs/2026-09-27-initial-replication-note.md`, split into atomic items `N-1` to `N-125` in the note's order, each checked against arXiv:2609.19644v1 [ours]. Conventions, sources and citation format follow `docs/paper/README.md` [ours]. The note is a secondary source written by an AI assistant in another chat; nothing in it counts until it is checked here, and the note itself is left untouched [ours].

**Sources.** Quotes and anchors come from the TeX; numbering, page numbers and image content come from the PDF [ours]. The HTML is used only to explain its numbering in special case A [Lst. 1]. The authors' project site (https://scientist-two.github.io/, fetched 2026-09-27 with WebFetch, which returns a model's rendering of the page, not the raw page) is used only for N-27, N-65 and N-124, and is paraphrased, because the citation checker can verify quotes only from the paper, the note and the sources the paper delegates to [ours]. ScientistOne (arXiv:2605.26340v1) is such a source for the CoE audit, since Table 7 is an evaluation "following Meng et al. (2026)"; it is quoted from its TeX, for that part only, under `[Ref: meng2026scientistone §n]` with `ref:` anchors [Tab. 7] [ours].

**How to read a row.** The quote is the note's exact wording (for a very short phrase, italics). The verdict is one of TRUE, PARTLY TRUE, FALSE, NOT IN THE PAPER, or PROPOSAL (the note's own recommendation, not a claim about the paper) [ours]. TRUE (by reference) means the paper delegates the point to a cited source and that source says it, while ScientistTwo's own text does not; it counts as TRUE [ours]. An arrow such as → TODO task 4 says where an external claim gets verified: task 4 is the reuse survey, task 5 scope, tasks and budget, task 6 the evaluation-integrity design, task 7 mock mode, task 8 the build plan [ours].

## Summary

| Verdict | Count | Meaning |
|---|---|---|
| TRUE | 32 | the paper says it; location and quote given; 4 of them (N-40 to N-43) TRUE (by reference), through the audit Table 7 follows [ours] |
| PARTLY TRUE | 12 | part holds, part does not; both shown [ours] |
| FALSE | 0 | the paper contradicts it [ours] |
| NOT IN THE PAPER | 38 | the paper neither says nor contradicts it; external claims are routed to a task [ours] |
| PROPOSAL | 43 | the note's own recommendation; any paper claim it rests on is its own item [ours] |
| **Total** | 125 | the first version counted 27, 13, 0, 42 and 43; N-40 to N-43 and N-110 changed (F-NC-1, F-1) [ours] |

No claim is outright FALSE: the note's errors are overstatements of what the paper says, and external facts given without a source that can be checked here [ours].

**The claims that matter most for the design** (wrong, overconfident, or resting on something outside the paper) [ours]:

1. **One stage primitive (N-78 to N-80).** The note says Listing 1 covers every row of Table 1. The paper says so too [§3], but its own stage descriptions contradict it: only one of Table 1's eleven rows fits Listing 1 exactly [Tab. 1] [Lst. 1]. Details in special case B; gaps A-NOTE-1 to A-NOTE-3.
2. **A full control-flow spec (N-1, N-3).** A.2 leaves several quantities unset (`N_seed`, `N_0`, `N_p`, `N_t`, a full-set engineering limit), and exhaustion rules differ by stage or are not stated [App. A.2] [§3.4] [§3.6]. Control flow is not the easy part the note rates it.
3. **The TeCh test (N-66, N-68).** App. B does say the ablation critic rejected DMC-TeCh [App. B], but §3.4 gives that critic only two verdicts, neither of them a reject [§3.4] (A-NOTE-4). As a test of our system, it also rests on one run of a stochastic system, and on our system proposing the same idea.
4. **The audit protocol, and three other ScientistOne claims (N-40 to N-43, N-83, N-86, N-88).** On the audit the note is right about ScientistOne, and since Table 7 is an evaluation "following Meng et al. (2026)", ScientistOne's audit is this paper's specification by reference: a re-run on a golden evaluator within an adaptive tolerance, majority votes of LLM judges, four reference APIs, and a lenient method–code check [Tab. 7] [Ref: meng2026scientistone §5]; the five runs and max(1%, 3σ/\|s̄\|) the note cites are the settings in ScientistOne's own runs [Ref: meng2026scientistone §6]. None of it is in ScientistTwo's own text [§4.2], and the paper's one example audit differs from both: it states no tolerance, where the definition calls for an adaptive one, and re-runs once, where ScientistOne's own runs used five [p. 47] (image). The referenced I1 also presumes a fixed evaluator per task, which ScientistTwo's tasks are never said to have (U-NOTE-4). The other three claims concern ScientistOne's own experiments, which this paper does not delegate, and stay NOT IN THE PAPER.
5. **AutoSOTA's task packaging (N-24, N-36 to N-38).** All external. The paper says the 64 ICML tasks were selected following AutoSOTA's filtering process, by ScientistTwo's authors [inferred], not taken from AutoSOTA's benchmark [App. A.1], so an AutoSOTA ICML folder, if one exists, is not the paper's task definition.
6. **Cost and time extrapolations (N-59, N-60, N-107).** The arithmetic is right, but the per-task figures come from 33 NeurIPS tasks only [§4.3]; the time is days per task, wall-clock by the natural reading but never stated [inferred], and not machine-days [Fig. 10a] (image); and idea refinement is 45.4% of cost, not a majority, whatever the caption says [Fig. 10b] (image).
7. **Models (N-9, N-115).** Gemini 3.6 Flash by default; four named agents run on Claude Code with Opus 4.8 [App. A.2]. The unnamed code-writing agents most likely do too [inferred] [§4.2] [Fig. 3] (image); the planners inside the named agents are open (A-NOTE-6).
8. **Proposals that depart from the paper (N-84, N-87, N-89).** A locked harness, and a writer that sees one harness-built table with labelled rows, are sound choices, but they must be recorded as deviations: in the paper the coding agents produce the results [§3.2], and the writers read raw logs and every variant, one of them on Claude Code, so they could have picked a better row than the one shipped [§2] [§3.5] [App. A.2] [p. 44] (image).

Where the note is right and it matters: the paper has no validation/test separation (N-91, U-NOTE-1), defines no subsets (N-27, U-NOTE-3), reports LLM-parsed gains (N-94, U-NOTE-2), its Table 5 shows the in-loop and held-out reviewers diverging in round 2 (N-96), and its audit details are those of the source Table 7 follows (N-40 to N-43) [§3.3] [§4.1] [Tab. 5] [Tab. 7].

**Where the required checks are** [ours]:

| Check | Items |
|---|---|
| The stage pattern's name, Listing 1 or Figure 4 | N-2; special case A [Lst. 1] |
| Listing 1 covering every row of Table 1 | N-79; special case B [Tab. 1] |
| The five ICLR 2026 tasks | N-62 to N-72 [App. B] [Tab. 13] |
| TeCh | N-66, N-68; A-NOTE-4 [App. B] |
| Table 5 | N-96; U-NOTE-6 [Tab. 5] |
| Table 6 | N-25, N-26 [Tab. 6] |
| The average cost | N-58 to N-60, N-107; special case C [§4.3] |
| The models | N-9, N-115, N-116; A-NOTE-6 [App. A.2] |
| The audit protocol, specified by reference | N-40 to N-43; U-NOTE-4 [Tab. 7] |
| Where the benchmark papers come from | N-35, N-24, N-37 [App. A.1] |

## 1. "Where the difficulty actually is" (the note's opening table)

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-1 | "A full spec: Section 3, Table 1, the Listing 1 stage pattern, and the loop limits in Appendix A.2" | **PARTLY TRUE** | The four parts exist [§3] [Tab. 1] [Lst. 1] [App. A.2]. Full does not hold: A.2 sets no value for `N_seed`, `N_0`, `N_p`, `N_t` or a full-set engineering limit, and the limitation loop has no symbol in §3.1, only "We extract limitations for a maximum of 16 rounds" in A.2 (tex:sections/appendix.tex:155) [§3.1] [§3.4] [§3.5]. Verdict sets and exhaustion rules differ by stage, and some are unstated (special case B; A-NOTE-2, A-NOTE-4, A-NOTE-8, A-NOTE-9, U-NOTE-5). |
| N-2 | "the Listing 1 stage pattern" | **TRUE** | The TeX float is a `listing` and the PDF prints it as Listing 1 [Lst. 1] [p. 5] (tex:tables/pseudo_code.tex:22-38). The HTML's label, figure 4, is a rendering artefact; see special case A. |
| N-3 | Control flow rated *Easy* | **NOT IN THE PAPER** | An assessment [ours]. It rests on N-1 and N-79, neither of which holds as stated: only one of Table 1's eleven rows fits Listing 1 exactly [Tab. 1] [Lst. 1]. |
| N-4 | "~15 reasoning agents" | **NOT IN THE PAPER** | The paper gives the agent count only as the symbol `N_a` in its problem setup, with no value [§3, Problem Setup] (tex:sections/3_new_method.tex:11). Our count of the non-coding agents named in §3.1 to §3.6 is 15: Limitation Extractor, Limitation Verifier, Novelty Checker, Idea Generator, Subset Critic, Full-Set Critic, Idea Evolver, Selector, Ablation Planner, Ablation Critic, Result Comparison, Initial Drafter, Peer-Reviewer, Rebuttal Planner, Meta-Review [ours] [§3.1] [§3.2] [§3.3] [§3.4] [§3.5] [§3.6]. Fig. 4 also draws an Initial Idea Generator [Fig. 4] (image), and two of the 15 are multi-agent systems in their own right, PaperOrchestra and ScholarPeer [§2]. |
| N-5 | "(extractor, critics, evolver, selector, planners, meta-reviewer)" | **TRUE** | Each role is named: Limitation Extractor [§3.1]; Subset and Full-Set Critic Agents [§3.2]; Idea Evolver Agent and Selector Agent [§3.3]; Ablation Planner Agent [§3.4]; Rebuttal Planner Agent [§3.5]; Meta-Review Agent [§3.6]. Whether the planners run on Gemini or inside Claude Code is ambiguous (A-NOTE-6). |
| N-6 | "Their roles, inputs and outputs" | **PARTLY TRUE** | Roles are given for every agent [§3.1] to [§3.6]. Inputs and outputs are formal for some: the unified coder's tuple [§3.2, Eq. 2], the Selector [§3.3, Eq. 4], and the critics' decision and feedback pairs [§3.2] [§3.4] [§3.6]. They are not given for the Limitation Verifier's output, the Novelty Checker's score scale, the Result Comparison Agent's output, or the evolver's `N_k` [§3.1] [§3.3] [§3.4] [ours]. |
| N-7 | "but no prompts" | **TRUE** | No prompt text appears in the TeX; §4.2 mentions only "careful agent prompt design" [§4.2] (tex:sections/4_experiment.tex:43). Appendix C holds "representative excerpts generated by ScientistTwo across its research pipeline" [App. C] (tex:sections/appendix.tex:334), i.e. outputs: the pages we opened are an idea proposal, an ablation table, critic feedback, two audit reports and a rebuttal report [p. 36] [p. 44] [p. 46] [p. 47] [p. 48] [p. 51] (image), and a text search of pp. 33 to 71 finds no prompt wording [ours]. |
| N-8 | "Easy to write, hard to make good" | **NOT IN THE PAPER** | An assessment [ours]. |
| N-9 | "Coding stages (baseline, subset and full coders, engineer, ablation, rebuttal, enhancer)" use "Claude Code with Opus 4.8" | **TRUE** | "we leverage Claude Code with Opus 4.8 whenever coding capabilities are required" [§4.2] (tex:sections/4_experiment.tex:46). A.2 names four agents on it: "the Idea Experiment Coding Agent, the Ablation Study Agent, the Rebuttal Agent, and the Draft Enhancer" [App. A.2]. The baseline coder, the engineers and A_FullEng are not among them; they reach Claude Code by an inference: A.2 opens *Unless otherwise specified*, which leaves room for §4.2's rule, and Figure 3's experiment boxes draw only a Coding Agent and a Critic Agent in a cycle, with no separate engineer [App. A.2] [Fig. 3] (image) [inferred]. A.2's explicit list of four keeps the other reading open, and the planners are open under both; register row A-CFG-1 (D-7; A-NOTE-6) [ours]. |
| N-10 | "Medium. Wiring them up is simple; keeping dozens of long sessions reliable isn't" | **NOT IN THE PAPER** | An assessment [ours]. The paper reports no session counts or failure rates; the session count is recomputed in special case C [App. A.2] [ours]. |
| N-11 | "The list of 107 papers" | **TRUE** | 38 NeurIPS 2025, 5 ICLR 2026 and 64 ICML 2026 Spotlight papers [App. A.1] [Tab. 12] [Tab. 13] [Tab. 14]. |
| N-12 | "with no subset or metric definitions" | **PARTLY TRUE** | No subset is defined for any task: App. A.1 lists titles only [App. A.1], and §3.2 names the benchmark subset without defining it [§3.2]. Metrics are not defined per task either, but some appear: TOFU forget10 metrics for AI Engram [Tab. 6], MSE and MAE on seven forecasting benchmarks for TS-RAG [Tab. 11], and per-task metrics for the five ICLR papers [Tab. 16]. U-NOTE-3. |
| N-13 | "Hard, and manual for every task" | **NOT IN THE PAPER** | An assessment [ours]; consistent with U-NOTE-3. |
| N-14 | "Self-contained scripts plus an LLM validation filter" | **PARTLY TRUE** | Both exist: the Coding Agent "is prompted during the experimentation phase to output self-contained, reproducible scripts and execution instructions", and there is "a validation filter that uses the Coding Agent to detect and discard rule-violating solutions immediately after experimentation" [§4.2] (tex:sections/4_experiment.tex:43). The note omits the other two mechanisms: "a search-augmented LLM identifies hallucinated citations", and a Coding Agent audit of code against manuscript that the Writer Agent uses to fix the method section [§4.2]. |
| N-15 | "Hard, because it has to be enforced by the setup, not by prompts" | **PROPOSAL** | Our design rule, not the paper's [ours]. The paper's own score-verification mechanism is a prompt: "the Coding Agent is prompted during the experimentation phase" [§4.2]. App. B instead claims structural blocking by the I1, I2 and I4 audits [App. B] (A-NOTE-10). In the enforcement classes of [stages/07-integrity.md](stages/07-integrity.md), as fix F-AN-11 fixes them (prompt, LLM filter, LLM fixer, post-hoc LLM audit, setup), every mechanism §4.2 describes is one of the first four, and none is enforced by the setup [§4.2] [ours]. |
| N-16 | Drafting: *PaperOrchestra* | **TRUE** | The Initial Drafter Agent is described as *incorporating PaperOrchestra* [§3.5] (tex:sections/3_new_method.tex:119), and "We use the ICLR 2025 format for drafting, following the PaperOrchestra" [App. A.2]. |
| N-17 | "Easy, since it's open source" | **NOT IN THE PAPER** | The paper cites PaperOrchestra as arXiv:2604.05018 and says nothing of code or licence [Bib: song2026paperorchestra] (tex:main.bib:148-153). → TODO task 4. |
| N-18 | In-loop reviewer: *ScholarPeer* | **TRUE** | The Peer-Reviewer Agent is ScholarPeer [§3.5] (tex:sections/3_new_method.tex:123), and "ScholarPeer serves as an in-distribution evaluation, as it is also used to refine the draft quality" [§4] (tex:sections/4_experiment.tex:5). |
| N-19 | "Medium: you'd rebuild it from its paper" | **NOT IN THE PAPER** | The paper links no ScholarPeer code; it cites arXiv:2601.22638 [Bib: goyal2026scholarpeer] (tex:main.bib:155-160) and describes only its output, "containing identified strengths, weaknesses, targeted questions, and an overall numerical score" [§3.5]. → TODO task 4. |
| N-20 | "The CoE audit, specified in the ScientistOne paper" | **TRUE** | The CoE Integrity Audit is cited to ScientistOne [§4.2] (tex:sections/4_experiment.tex:41) [Bib: meng2026scientistone], and Table 7 is an evaluation "following Meng et al. (2026)" [Tab. 7], which makes ScientistOne's audit this paper's specification by reference; its content is checked at N-40 to N-43, and adopting it is TODO task 6 [ours]. |
| N-21 | Integrity audit rated *Medium* | **NOT IN THE PAPER** | An assessment [ours]. |

## 2. The benchmark-gap paragraph

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-22 | "The benchmark gap is real." | **NOT IN THE PAPER** | The note's conclusion from N-24, which is external [ours]. |
| N-23 | "Take the AI Engram paper." | **TRUE** | AI Engram is one of the 64 ICML 2026 Spotlight tasks [Tab. 14] [Bib: kwon2026ai]. |
| N-24 | "AutoSOTA's packaged version of that task optimizes an approximate ToW score on CIFAR-10 with ResNet-18." | **NOT IN THE PAPER** | The paper describes no AutoSOTA packaging of any task [ours]. It says the ICML tasks were selected "by strictly adhering to AutoSOTA's filtering process" [App. A.1] (tex:sections/appendix.tex:74), i.e. by ScientistTwo's authors [inferred: the sentence is passive], not taken from AutoSOTA's benchmark. → TODO task 4. |
| N-25 | "ScientistTwo's Table 6 evaluates the same paper on TOFU with Llama-3.2-1B." | **TRUE** | Tab. 6 reports "the unlearning performance on TOFU" on the forget10 split with Llama-3.2-1B-Instruct, as "main benchmark results generated by ScientistTwo" with AI Engram as input [Tab. 6] (tex:tables/ablation_review_refine.tex:3). The model is the Instruct variant [Tab. 6]. |
| N-26 | "Same paper, different benchmark." | **PARTLY TRUE** | The ScientistTwo side holds (N-25) [Tab. 6]; the AutoSOTA side is external and unchecked (N-24) [ours]. |
| N-27 | "ScientistTwo never published its subset and full-set definitions" | **TRUE** | Not in the paper: App. A.1 lists titles only, and §3.2 defines neither set [App. A.1] [§3.2]. App. B says only that ScientistTwo "evaluates on the paper's full benchmark grid rather than the single registered split" [App. B] (tex:sections/appendix.tex:238-239). Project site, fetched 2026-09-27: it links the arXiv page, in-page anchors, a demo video and a template credit, and no code, data or task definitions (paraphrase) [ours]. |
| N-28 | "so you'll have to define your own" | **PROPOSAL** | Follows from N-27 [ours] [App. A.1]; U-NOTE-3. |

## 3. "Reuse before you build"

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-29 | *Reuse before you build* (the section's advice) | **PROPOSAL** | [ours]; each candidate is checked below and verified in TODO task 4. |
| N-30 | "Google Research open-sourced PaperOrchestra" | **NOT IN THE PAPER** | The paper gives neither an affiliation nor a code release for PaperOrchestra; its authors include two ScientistTwo authors, Pfister and Yoon [Bib: song2026paperorchestra] (tex:main.bib:148-153) (tex:main.tex:57-63). → TODO task 4. |
| N-31 | "which turns idea summaries and experiment logs into LaTeX manuscripts" | **TRUE** | PaperOrchestra "compiles unconstrained experiment logs and ideas into LaTeX manuscripts" [§2] (tex:sections/2_related_works.tex:5). |
| N-32 | "using outline, literature-review, section-writing, refinement and plotting agents" | **NOT IN THE PAPER** | The paper does not describe PaperOrchestra's internals [§2] [§3.5]. → TODO task 4. |
| N-33 | "That's exactly what ScientistTwo's drafter wraps." | **PARTLY TRUE** | The drafter is described as *incorporating PaperOrchestra* [§3.5], and drafting follows PaperOrchestra's ICLR 2025 format [App. A.2]. How it is incorporated is not said, and writing also happens outside it: the Paper Enhancer revises the draft on Claude Code, and the Writer Agent corrects references and the method section [§3.5] [§4.2] [App. A.2]. |
| N-34 | "A community port notes that the paper's appendix includes the prompts for every agent." | **NOT IN THE PAPER** | Read as PaperOrchestra's appendix (the bullet's subject), it is external → TODO task 4. Read as ScientistTwo's appendix it would be false: Appendices A to D hold benchmark lists, the configuration, the AutoSOTA comparison, agent outputs and one generated paper, and no prompts [App. A.1] [App. A.2] [App. B] [App. C] [App. D]. |
| N-35 | "All 107 of ScientistTwo's target papers came from AutoSOTA's benchmark or its filtering process (Appendix A.1)." | **TRUE** | NeurIPS (38): "these papers are drawn from benchmarks used in AutoSOTA" (tex:sections/appendix.tex:3); ICLR (5): the same sentence, with the typo *benchmakrs* (tex:sections/appendix.tex:55); ICML (64): "selected from among all spotlight papers by strictly adhering to AutoSOTA's filtering process" (tex:sections/appendix.tex:74) [App. A.1]. So 43 tasks come from AutoSOTA's benchmarks, and 64 were selected by the authors with AutoSOTA's filter [ours]. |
| N-36 | "AutoSOTA maintains a leaderboard of automatically optimized research codebases and ships a CLI." | **NOT IN THE PAPER** | The paper describes AutoSOTA's method only: it "locates the repository, reconstructs a runnable baseline, and distills the paper's headline result into a single numerical target" [App. B] (tex:sections/appendix.tex:196-198) [Bib: li2026autosota]. → TODO task 4. |
| N-37 | "Its ICML-2026 folder has slimmed code for hundreds of papers, with datasets and weights stripped, plus a final report for each." | **NOT IN THE PAPER** | External → TODO task 4. The paper does not say AutoSOTA covers ICML 2026; its ICML tasks were selected with AutoSOTA's filter, apparently by ScientistTwo's authors (N-35) [App. A.1] [inferred]. |
| N-38 | "The AI Engram folder also records the eval command, the baseline scores and the files that must not be modified." | **NOT IN THE PAPER** | External → TODO task 4 [ours] [Tab. 14]. |
| N-39 | "Use these folders as your template for packaging a task." | **PROPOSAL** | Rests on N-36 to N-38, all external [ours]. → TODO tasks 4 and 5. |
| N-40 | "The ScientistOne paper specifies it precisely" | **TRUE (by reference)** | Not in ScientistTwo's own text, which gives each of the four checks one clause [§4.2] (tex:sections/4_experiment.tex:41). But Table 7 is an evaluation "following Meng et al. (2026)" [Tab. 7], so ScientistOne's audit is this paper's specification by reference, and ScientistOne does specify it: the definition of the four checks [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:23-44), the run count and tolerance of its own runs [Ref: meng2026scientistone §6] (ref:2605.26340v1:sections/06a_setup.tex:10), and the judge models, the votes and the human review of flagged cases in its own evaluation [Ref: meng2026scientistone App. D] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:27-57). Its I1 re-runs the solution on the golden evaluator (paraphrase) (ref:2605.26340v1:sections/05_coe_audit.tex:25), which ScientistOne's own benchmark supplies: "Each task provides a fixed evaluator, starter code, and scoring metric" (ref:2605.26340v1:sections/06a_setup.tex:8); ScientistTwo's tasks are never said to have one (U-NOTE-4). Revised from NOT IN THE PAPER, which missed the delegation (F-NC-1) [ours]. → TODO task 6. |
| N-41 | "Re-run the solution on the reference evaluator five times; it passes if the reported score is within" max(1%, 3σ/\|mean\|) | **TRUE (by reference)** | ScientistOne's I1 extracts the paper's score, which is "then compared against scores obtained by re-running the submitted solution on the golden evaluator" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:25), and its setup says "We run each evaluator five times and compare against the adaptive tolerance" max(1%, 3σ/\|s̄\|) [Ref: meng2026scientistone §6] (ref:2605.26340v1:sections/06a_setup.tex:10). Both numbers sit in the setup for ScientistOne's own benchmark; its audit definition says only "an adaptive tolerance that accounts for evaluator noise" (ref:2605.26340v1:sections/05_coe_audit.tex:26) [ours]. Not in ScientistTwo's own text, which says only "comparing reported scores against those obtained from re-executing the repository" [§4.2] (tex:sections/4_experiment.tex:41). Its one example audit is a single re-run of the agent's final.py, whose numbers matched the experiment report exactly (paraphrase) [p. 47] (image): it states no tolerance, where the definition calls for an adaptive one, and re-runs once, where ScientistOne's own runs used five [ours]. Revised from NOT IN THE PAPER, which missed the delegation (F-NC-1) [ours]. → TODO task 6; U-NOTE-4. |
| N-42 | "Judge spec violations and method–code alignment by majority vote of several LLM judges." | **TRUE (by reference)** | In ScientistOne's definition, I2 detects violations "with majority vote across multiple runs" (ref:2605.26340v1:sections/05_coe_audit.tex:32) and I4 uses "multiple independent runs with majority vote" (ref:2605.26340v1:sections/05_coe_audit.tex:44) [Ref: meng2026scientistone §5]; in its own runs, the I2 counts "use majority vote (3/5 judges)" [Ref: meng2026scientistone App. E] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:302). The note leaves out how lenient I4 is: "only cases where the paper describes a fundamentally different algorithm count as misaligned" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:43). Not in ScientistTwo's own text, which describes no vote [§4.2]; its example is one report with one verdict per dimension [p. 48] (image). Revised from NOT IN THE PAPER, which missed the delegation (F-NC-1) [ours]. → TODO task 6. |
| N-43 | "Resolve every reference against Semantic Scholar, arXiv, OpenAlex and Crossref." | **TRUE (by reference)** | ScientistOne's I3: "Each bibliography entry is resolved by querying multiple academic APIs (Semantic Scholar, arXiv, OpenAlex, CrossRef)", and an LLM "cross-checks the full bib entry against returned records" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:36-37). Not in ScientistTwo's own text: its in-pipeline fix is "a search-augmented LLM identifies hallucinated citations", which the Writer Agent corrects from live search results [§4.2], and Tab. 7 counts hallucinated references, 0 of 1814 for the full system [Tab. 7]. Revised from NOT IN THE PAPER, which missed the delegation (F-NC-1) [ours]. → TODO task 6. |
| N-44 | "The Claude Agent SDK gives you the same tools, agent loop and context management as Claude Code, from Python or TypeScript." | **NOT IN THE PAPER** | The paper never mentions an Agent SDK; it uses "Claude Code with Opus 4.8" [App. A.2] and cites Claude Code in related work [§2] [Bib: liu2026dive]. → TODO task 4. |
| N-45 | "The SDK packages support structured outputs and tool-approval callbacks, and they respect CLAUDE.md files, skills and hooks." | **NOT IN THE PAPER** | External → TODO task 4 [ours]. |
| N-46 | "So you can block any edit to the evaluation files at the tool level." | **PROPOSAL** | Rests on N-45 [ours]. The paper blocks rule violations after the fact, with a validation filter and audits, not at the tool level [§4.2] [App. B]. → TODO task 6. |
| N-47 | "I couldn't find released code for ScholarPeer" | **NOT IN THE PAPER** | The paper gives no ScholarPeer code link either [§3.5] [Bib: goyal2026scholarpeer]. → TODO task 4. |
| N-48 | "a historian agent builds the field's context, a baseline scout looks for missing comparisons, and a Q&A engine checks claims against current literature" | **NOT IN THE PAPER** | The paper says only that ScholarPeer "deploys a multi-agent system that acts as peer-reviewers" [§2] (tex:sections/2_related_works.tex:5); its reference title is "context-aware multi-agent framework for automated peer review" [Bib: goyal2026scholarpeer]. → TODO task 4. |
| N-49 | "For an independent (held-out) reviewer, paperreview.ai" | **TRUE** | The paper's held-out reviewer is the Stanford Agentic Reviewer, footnoted as https://paperreview.ai/, which "serves as a held-out evaluator that was unseen during development" [§4] [fn. 1] (tex:sections/4_experiment.tex:5). |
| N-50 | *paperreview.ai is free* | **NOT IN THE PAPER** | No price is given [fn. 1]. → TODO tasks 4 and 5. |
| N-51 | "but it only accepts PDFs and reads at most 15 pages" | **NOT IN THE PAPER** | Not stated [§4] [fn. 1]. If true, it matters: the one complete generated draft in the paper spans 16 included pages [App. D] (tex:sections/appendix.tex:483) (tex:sections/appendix.tex:558), and the paper does not say how drafts were submitted to this reviewer [ours]. → TODO task 4. |
| N-52 | "Its tech overview describes its workflow, which grounds reviews in searched arXiv papers, if you'd rather build your own version." | **NOT IN THE PAPER** | External → TODO task 4 [ours] [fn. 1]. |
| N-53 | "MLE-STAR, by the same lead authors" | **TRUE** | MLE-STAR's first two authors are Jaehyun Nam and Jinsung Yoon [Bib: nam2026mle] (tex:main.bib:120-125), ScientistTwo's first two authors [Title] (tex:main.tex:57-58). |
| N-54 | *is open source* (MLE-STAR) | **NOT IN THE PAPER** | The paper cites MLE-STAR as a NeurIPS paper, with no code link [Bib: nam2026mle]. → TODO task 4. |
| N-55 | "its refinement loop already uses ablations over individual code blocks" | **NOT IN THE PAPER** | The paper says only that MLE-STAR and similar frameworks "automate end-to-end ML workflows by executing and improving modeling pipelines" [§2] (tex:sections/2_related_works.tex:3). → TODO task 4. |
| N-56 | "Its prompts are worth borrowing." | **PROPOSAL** | → TODO task 4 [ours]. |

## 4. "Scope: replicate the system, not the 107-task numbers"

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-57 | "Scope: replicate the system, not the 107-task numbers" | **PROPOSAL** | → TODO task 5 [ours]. |
| N-58 | "At the paper's average of \$3,765 per task" | **TRUE** | ScientistTwo "incurs an average cost of \$3765, including token usage costs and virtual machine costs" [§4.3] (tex:sections/5_discussion.tex:4), the figure printed in Fig. 10b [Fig. 10b] (image). Sample: "the 33 target problems sourced from NeurIPS 2025 papers" [§4.3], the same count as the successful NeurIPS runs, 33 of 38 [Tab. 3]; whether failed runs are included is not said (U-NOTE-7). The conclusion rounds it to about \$3,800 [§5] (tex:sections/6_conclusion.tex:7). |
| N-59 | "running the full benchmark would cost about \$400k" | **NOT IN THE PAPER** | The note's extrapolation [ours]. Arithmetic: 107 × \$3,765 = \$402,855, so about \$400k holds [ours]. But the average comes from 33 NeurIPS tasks only [§4.3]; the paper reports no cost for the ICML or ICLR tasks, nor for failed runs [ours]. → TODO task 5. |
| N-60 | "and take roughly 270 machine-days" | **NOT IN THE PAPER** | Arithmetic: 107 × 2.51 days = 268.6 days, so the number holds [ours] [Fig. 10a] (image). The unit does not: the paper measures "Required Time per Task (Days)", which reads as wall-clock time per task [inferred], though the paper never says how time was measured, nor how many machines or GPUs a task uses; machine-days follow on neither reading [Fig. 10a] [ours]. The first version stated wall-clock without the mark (F-8) [ours]. → TODO task 5. |
| N-61 | "Your numbers would differ anyway, because your models, prompts and benchmark definitions will differ." | **NOT IN THE PAPER** | The note's reasoning [ours]; consistent with the unreleased prompts (N-7) and undefined subsets (N-27) [§4.2] [App. A.1]. |
| N-62 | "A better target: build on three cheap development tasks, then use the five ICLR 2026 tasks as your test set." | **PROPOSAL** | → TODO task 5 [ours]. Its premise holds: the paper itself uses these five as a small probe set, running the coding-agent swap "on 5 tasks sourced from ICLR 2026 accepted papers" [Tab. 8] (tex:tables/antigravity.tex:3), the same five because the benchmark has only five ICLR papers and the Claude Code row repeats the ICLR numbers of Tab. 3 [inferred] [Tab. 13] [Tab. 3], and it details each in App. B [App. B]. |
| N-63 | "Appendix B documents what ScientistTwo did on each of them" | **TRUE** | "We run ScientistTwo on the same five ICLR 2026 submissions" [App. B] (tex:sections/appendix.tex:194), one row per paper in Tab. 16 [Tab. 16]. |
| N-64 | "It produced accepted methods for Pinet, DMSQD, T-SAE and RALI" | **TRUE** | "ScientistTwo's accepted solutions instead introduce transferable mechanisms" for Pinet, T-SAE, RALI and DMSQD [App. B] (tex:sections/appendix.tex:211-216), and Tab. 15 counts "Papers with a reported gain" as 4 of 5 [Tab. 15]. Accepted means accepted by its own pipeline: the held-out reviewer accepted 75.0% of the four ICLR papers, i.e. 3 of 4 [Tab. 3] [ours]. |
| N-65 | "those four generated papers are on the project site" | **NOT IN THE PAPER** | A claim about the site. Project site, fetched 2026-09-27: it announces 86 generated papers in a gallery (paraphrase), which by count would include the four, since 86 = 4 + 33 + 49 [Tab. 3]; but the gallery loads by script, and the fetched text names none of ANSE, LC-FTT, Sheaf-SAE or DisCoRe-IQA [ours]. Unverified → TODO task 5. |
| N-66 | "It rejected its own idea for TeCh, because its ablation critic traced the gain to EMA and label smoothing rather than the new mechanism." | **TRUE** | DMC-TeCh "beat the baseline on 5 of 6 metrics, but the ablation critic rejected it because" "the gains were primarily driven by general training controls (EMA and label smoothing)", "so it was not accepted as a contribution" [App. B] (tex:sections/appendix.tex:221-225) [Tab. 16]. But §3.4 gives the Ablation Critic no reject verdict (A-NOTE-4) [§3.4]. |
| N-67 | "It also shows what AutoSOTA did on the same five papers." | **TRUE** | Tab. 16's AutoSOTA column, one row per paper [Tab. 16] (tex:sections/appendix.tex:262-265). |
| N-68 | "TeCh doubles as a test of your own system: your ablation critic should reject that idea too." | **PROPOSAL** | Rests on N-66 [ours]. Three caveats: §3.4 has no reject verdict to reproduce (A-NOTE-4) [§3.4]; the test assumes our system proposes the same DMC-TeCh idea, which it may never do [App. B]; and the paper's evidence is one run [Tab. 16] [ours]. |
| N-69 | "Check compute before you commit." | **PROPOSAL** | → TODO task 5 [ours]. |
| N-70 | "T-SAE trains sparse autoencoders on Pythia-160m and Gemma-2-2b" | **PARTLY TRUE** | It is ScientistTwo's solution, Sheaf-SAE, that was "Trained from scratch on Pythia-160m and Gemma-2-2b" [Tab. 16] (tex:sections/appendix.tex:310-311); the paper does not describe the T-SAE paper's own setup [ours]. The compute warning still holds for a replication [ours]. |
| N-71 | "RALI spans seven image-quality datasets" | **TRUE** | "KonIQ-only training, full splits of all 7 datasets (6 zero-shot)" [Tab. 16] (tex:sections/appendix.tex:320-321); RALI is an image-quality-assessment paper [Tab. 13]. |
| N-72 | "The other three look lighter." | **NOT IN THE PAPER** | The paper gives no per-task compute [ours]. Its only scale indicators are breadth, not cost: the DMSQD run covers "Over the full 11-domain grid" and the Pinet run all four DC3 sets [Tab. 16] (tex:sections/appendix.tex:287). → TODO task 5. |

## 5. "Repo design"

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-73 | The repository tree (`scientist2-repro/` and its folders) | **PROPOSAL** | [ours]; TODO task 3 decides the components. |
| N-74 | "loop limits (App. A.2), model routing, budgets" | **PARTLY TRUE** | As a premise: A.2 holds loop limits and model routing [App. A.2], but not every limit (N-1), and no budgets [ours]. |
| N-75 | *in-loop + held-out reviewers* | **TRUE** | As a premise: ScholarPeer is the in-distribution reviewer because it refines drafts, and the Stanford Agentic Reviewer is held out [§4] (tex:sections/4_experiment.tex:5). |
| N-76 | *I1–I4 checks* | **PARTLY TRUE** | The labels I1, I2 and I4 appear only in App. B: "a reproduction re-run (I1), a protocol-immutability audit (I2)" and "a method–code alignment audit (I4)" [App. B] (tex:sections/appendix.tex:236-238). I3 is never named; §4.2 numbers the four checks (1) to (4), reference verification third [§4.2]. |
| N-77 | "Agent SDK adapter (OpenHands/Codex as fallback)" | **PROPOSAL** | [ours]. The paper's own alternative backend was Antigravity with Gemini 3.8 Flash [§4.2] [Tab. 8]; OpenHands appears only as related work [§2]. |

## 6. The seven rules

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-78 | *Build one stage primitive.* | **PROPOSAL** | Rests on N-79 [ours] [Lst. 1]. |
| N-79 | "Listing 1's pattern covers every row of Table 1: generate, let a critic accept, refine or reject, and stop after N rounds." | **PARTLY TRUE** | The paper asserts it: "we abstract all stages (see overview in Table 1) using the Python-style pseudocode in Listing 1" [§3] (tex:sections/3_new_method.tex:5). Its own stage descriptions contradict it: only the subset-experiment row fits exactly; two rows have no critic, three have no refine step, four critics have no reject verdict, two loops stop on a count, and five rows keep, or leave unstated, what Listing 1 discards on exhaustion [Tab. 1] [§3.1] [§3.2] [§3.3] [§3.4] [§3.5] [§3.6] (special case B). The paraphrase also drifts: Listing 1 does not generate, since the candidate is its argument, and it returns None when the rounds run out [Lst. 1]. A-NOTE-1 to A-NOTE-3. |
| N-80 | "Implement it once and configure each stage." | **PROPOSAL** | Rests on N-79 [ours]. One primitive would need, per stage, a verdict map, an exhaustion policy, an optional comparison gate, a count-based stop and a no-critic mode [Tab. 1] [§3.4] [§3.6] [ours]. |
| N-81 | "Make runs resumable. Every stage writes its output to files, every idea lives on its own git branch, and a crash resumes from the last finished stage." | **PROPOSAL** | The paper describes no resumption or branching [ours] [§3]. |
| N-82 | *Runs take days.* | **TRUE** | ScientistTwo "requires an average of 2–3 days to complete the entire research cycle" [§4.3] (tex:sections/5_discussion.tex:4); mean 2.51 days, median 2.00, interquartile range 1.1 to 3.1 days, over 33 NeurIPS tasks [Fig. 10a] (image). |
| N-83 | "In ScientistOne's evaluation, 16 of 75 runs needed an infrastructure retry." | **NOT IN THE PAPER** | Not in this paper, and outside what it delegates to ScientistOne, which is the audit (N-40 to N-43): a claim about ScientistOne's own runs, not checked here [ours] [Bib: meng2026scientistone]. → TODO task 4. |
| N-84 | "Metrics come only from the locked evaluation harness. Agent code never writes results." | **PROPOSAL** | A departure from the paper, to be recorded as our decision [ours]: in ScientistTwo the coding agents run the experiments and produce the results, e.g. the Subset Coding Agent produces *the resulting logs* [§3.2] (tex:sections/3_new_method.tex:40), and integrity rests on prompts, a filter and a post-hoc audit [§4.2]. → TODO task 6. |
| N-85 | "The harness runs in its own container, with the evaluation code and data splits mounted read-only and checked against hashes. This has to be enforced by the setup, not by prompts." | **PROPOSAL** | No container, mount or hash check appears in the paper [ours] [§4.2]. → TODO task 6. |
| N-86 | "In ScientistOne's scaling experiments, the share of attempts flagged for gaming the metric rose from about 0% to about 70% as the per-attempt budget grew." | **NOT IN THE PAPER** | Not in this paper, and outside what it delegates to ScientistOne (the audit): a claim about ScientistOne's own scaling runs, not checked here [ours] [Bib: meng2026scientistone]. This paper's only reward-hacking figure is one filtered codebase: "since the corresponding codebase contains reward hacking, it must be filtered" [fn. 2] [Tab. 7]. → TODO task 6. |
| N-87 | "The paper writer sees only verified numbers." | **PROPOSAL** | [ours]. In the paper the writers see raw material and can pick among it: PaperOrchestra "compiles unconstrained experiment logs and ideas into LaTeX manuscripts" [§2]; the drafter receives the best idea, its main results and the ablation results [§3.5] (tex:sections/3_new_method.tex:119); the Paper Enhancer receives the review and the rebuttal results and updates the empirical tables and figures [§3.5]; and the Draft Enhancer runs on Claude Code, so it can execute code [App. A.2]. A better row than the shipped one was there to pick: in the ablation table, γ = 3.0 scores 99.58/2.13 against 99.56/2.17 for the shipped γ = 2.0 [p. 44] (image). |
| N-88 | "ScientistOne caught Sakana's AI Scientist writer picking better scores from ablation runs." | **NOT IN THE PAPER** | The paper says only that AI Scientist "suffered from execution instability and issues with hallucinated writing" [§2] [Bib: lu2024ai]. Sakana appears only in an uncited bibliography entry, beel2025evaluating (tex:main.bib:43-48), which the compiled paper does not print [ours]. The anecdote concerns ScientistOne's own evaluation, not the audit this paper delegates, so it is not checked here [ours]. → TODO task 6. |
| N-89 | "Pass PaperOrchestra a single verified results table and nothing else." | **PROPOSAL** | The risk to address is the writer choosing its own row, not lost content (N-87) [ours]. Our assessment: the harness builds one table with labelled main, ablation and rebuttal rows, and the writer cannot choose which row counts as the method's result; that keeps the ablation and rebuttal material the paper's drafter reads [§3.5] (tex:sections/3_new_method.tex:119) [ours]. The first version read a single table as lost content (F-NC-4) [ours]. → TODO task 6. |
| N-90 | "Search on validation data, test once." | **PROPOSAL** | → TODO task 6 [ours]. |
| N-91 | "I couldn't find where the paper separates the data used to pick ideas from the final test data." | **TRUE** | We find none either [ours]: the Selector compares ideas "evaluated on the full benchmark" [§3.3] (tex:sections/3_new_method.tex:90), the Result Comparison Agent compares new results against the best ones [§3.4] [§3.6], and the drafter writes up those same best results [§3.5]. U-NOTE-1. |
| N-92 | "Make every number an agent can see a validation number, and report test results only at the end." | **PROPOSAL** | → TODO task 6 [ours]. |
| N-93 | "Compute gains deterministically and use a separate judge. Calculate gains directly from the results files" | **PROPOSAL** | → TODO task 6 [ours]; U-NOTE-2 [§4.1]. |
| N-94 | "the paper instead had Gemini parse its tables 10 times and averaged" | **TRUE** | "we parse the main tables for 10 times using Gemini 3.6 Flash and averaged them" [§4.1] (tex:sections/4_experiment.tex:19). The headline 25.2% average gain is Tab. 4's ScientistTwo value, so it comes from this parsing [inferred] [Tab. 4] [§1]. |
| N-95 | "Never evaluate with the reviewer you optimize against" | **PROPOSAL** | The paper already reports a held-out reviewer beside the in-loop one [§4] (tex:sections/4_experiment.tex:5) [ours]. |
| N-96 | "in Table 5, a second review round raised the in-loop reviewer's acceptance rate while the held-out reviewer's rate dropped" | **TRUE** | From round 1 to round 2, ScholarPeer's acceptance rate rises from 79.6% to 93.9% and the Stanford Agentic Reviewer's falls from 73.5% to 69.4% [Tab. 5]. Sample: the 49 ICML 2026 Spotlight tasks [§4.2]; in papers, 39 to 46 and 36 to 34 of 49 [ours]. The text mentions only the first-round gain, "particularly pronounced in the first review round" [§4.2]; how many tasks had a second round is not reported (U-NOTE-6). |
| N-97 | "Add a budget guard and a mock mode. Put hard cost caps on each session and each task." | **PROPOSAL** | The paper bounds loops, not money [App. A.2] [ours]. → TODO tasks 5 and 7. |
| N-98 | "Add a fake LLM and fake coding agent so you can test the whole state machine for free." | **PROPOSAL** | → TODO task 7 [ours]. |

## 7. "Build plan"

Each item is a whole phase row of the note's table (its time, build and done-when cells); the quote identifies the row [ours].

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-99 | Phase 0: "Environments for 3 dev tasks; locked evaluation harness" | **PROPOSAL** | → TODO task 8 [ours]. |
| N-100 | Phase 1: "A hand-written idea runs end to end: subset run, critic, full run" | **PROPOSAL** | Mirrors §3.2's subset-then-full-set flow [§3.2] [ours]. |
| N-101 | Phase 2: "Limitation loop, seed ideas with novelty check, engineering loop, idea evolution and selection, ablation loop" | **PROPOSAL** | Mirrors §3.1 to §3.4 [§3.1] [§3.4] [ours]. |
| N-102 | Phase 3: "PaperOrchestra drafting, review-and-rebuttal loop, meta-review" | **PROPOSAL** | Mirrors §3.5 and §3.6 [§3.5] [§3.6] [ours]. |
| N-103 | Phase 4: "I1–I4 audit, gain calculator, held-out reviewing" | **PROPOSAL** | Rests on N-76 (the labels) and on §4.2's four checks [§4.2] [ours]. |
| N-104 | Phase 5: "Prompt tuning from traces, the five ICLR tasks, ablations of your own loops" | **PROPOSAL** | Rests on N-62 to N-67 [App. B] [ours]. |
| N-105 | "These durations are rough estimates for one person working with heavy AI assistance." | **NOT IN THE PAPER** | The note's estimate [ours]. → TODO task 8. |

## 8. "Budget and models"

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-106 | "By my count from the paper's loop limits, each task runs several dozen long coding-agent sessions." | **NOT IN THE PAPER** | The paper reports no session counts [ours]. Our recount from A.2's limits gives at least 16 coding sessions per task and at most 81 + 4 × `N_t` or 87 + 4 × `N_t` (93 or 99 if `N_t` = 3), under two assumptions that analysis.md section 9, the canonical bound, reads differently (special case C; D-2) [App. A.2] [ours]. The first version's 87 assumed 8 ideas (F-2) [ours]. |
| N-107 | "The paper says idea refinement accounts for most of its cost." | **PARTLY TRUE** | The caption says so: "Idea refinement accounts for the majority of overall time and computational cost" [Fig. 10] (tex:figures/cost.tex:4). The chart shows 45.4% of cost and 44.9% of time: the largest share, but under half [Fig. 10b] (image). A-NOTE-7. |
| N-108 | "For development, use a cheap profile and measure cost on your first task before scaling" | **PROPOSAL** | → TODO task 5 [ours]. |
| N-109 | "two evolution rounds instead of four" | **PROPOSAL** | → TODO task 5 [ours]. |
| N-110 | The premise of N-109, *instead of four* | **TRUE** | A.2 runs the experimentation loop "for up to four rounds, terminating early once four successful ideas are obtained" [App. A.2]. The paper's runs had four rounds after the initial one: Figure 9 labels them *Initial* and *Round 1* to *Round 4*, and 4 of 49 tasks picked their best idea in *Round 4* [Fig. 9b] (image), so the four are evolution rounds, each with one seed and one evolved idea [inferred] [§3.3]. A.2's sentence alone stays ambiguous (A-NOTE-8; D-1). Revised from PARTLY TRUE, which rested on the ambiguity that Figure 9 settles for the paper's runs (F-1) [ours]. |
| N-111 | *one review round* | **PROPOSAL** | The paper allows at most two [App. A.2] [ours]. |
| N-112 | *no meta-review refinement* | **PROPOSAL** | The paper allows it at most once [App. A.2] [ours]. |
| N-113 | "a cheaper coding model for subset screening" | **PROPOSAL** | [ours]; the paper's primary runs use one coding model for every coding stage [App. A.2] [§4.2]. |
| N-114 | *hard caps on turns per session* | **PROPOSAL** | The paper gives no per-session caps [App. A.2] [ours]. |
| N-115 | "The paper used Opus 4.8 for coding and Gemini Flash for everything else." | **PARTLY TRUE** | "we employ Gemini 3.6 Flash for all agents, except for" four named agents, "which use Claude Code with Opus 4.8" [App. A.2]. So: Gemini 3.6 Flash specifically; Opus 4.8 through the Claude Code harness; one writing agent, the Draft Enhancer, is on Claude Code [App. A.2]; gain parsing used Gemini 3.6 Flash [§4.1]; the backend swap used Antigravity with Gemini 3.8 Flash [Tab. 8]; the in-loop ScholarPeer falls under A.2's Gemini default [inferred], and the held-out reviewer's model is not given [§4] [ours]. A-NOTE-6. |
| N-116 | "Through the Agent SDK you can point the coding stages at Opus 5.5 or Sonnet 5, and use Haiku 4.5 or a Flash-class model for the reasoning agents." | **NOT IN THE PAPER** | External; the paper names only Gemini 3.6 Flash, Opus 4.8 and Gemini 3.8 Flash [App. A.2] [Tab. 8]. → TODO tasks 4 and 5. |
| N-117 | "If you run on a Claude subscription, note that since June 15, 2026, Agent SDK and headless usage draws from a separate monthly Agent SDK credit." | **NOT IN THE PAPER** | External → TODO task 5 [ours]. |
| N-118 | "At this volume, plan for API billing." | **PROPOSAL** | → TODO task 5 [ours]. |

## 9. "How to vibe-code it"

| ID | The note says | Verdict | Evidence |
|---|---|---|---|
| N-119 | "Let Claude Code write the plumbing: orchestration, adapters, sandbox and audit." | **PROPOSAL** | [ours]. |
| N-120 | "Give it a SPEC.md that maps each paper section to a module and a JSON schema" | **PROPOSAL** | [ours]; the same sentence proposes a CLAUDE.md rule against editing evaluation files. |
| N-121 | "Build in order of risk: environments and sandbox first, agents last." | **PROPOSAL** | → TODO task 8 [ours]. |
| N-122 | "Have it write the mock-mode tests before any real model runs." | **PROPOSAL** | → TODO task 7 [ours]. |
| N-123 | *Write the prompts yourself.* | **PROPOSAL** | [ours]. |
| N-124 | "They're what the paper didn't release" | **TRUE** | The paper contains no prompts (N-7) [§4.2] [App. C]. Project site, fetched 2026-09-27: no code or prompts are linked (paraphrase) [ours]. |
| N-125 | "they'll decide whether the system finds real gains or just produces well-formatted noise" | **NOT IN THE PAPER** | An opinion [ours]. The paper credits prompting with one integrity property only, reproducible scripts: "the Coding Agent is prompted during the experimentation phase" [§4.2]. |

## Special case A. "Listing 1" or "Figure 4"? Listing 1.

- **TeX.** The pseudocode sits in a `listing` float with its own caption and the label `lst:stage_pseudocode`; the code inside is an `lstlisting` block in the `pseudopython` style [Lst. 1] (tex:tables/pseudo_code.tex:22-38) (tex:main.tex:13-28). §3 cites it as `Listing~\ref{lst:stage_pseudocode}` [§3] (tex:sections/3_new_method.tex:5). A commented-out earlier version put a minted block in the same kind of float [Lst. 1] (tex:tables/pseudo_code.tex:2-21).
- **Where the name comes from.** The `listing` float is defined by the minted package, loaded at (tex:main.tex:9) [Lst. 1]. In the local TeX Live 2025 copy of `minted.sty`, it is declared with `\newfloat{listing}` and named by `\floatname{listing}{\listingscaption}`, with `\listingscaption` defined as Listing (lines 1938 to 1942) [ours]. arXiv's build may use another minted version; the PDF is what counts.
- **PDF, the authors' compiled rendering.** Page 5 prints the caption as "Listing 1 | Python-style pseudocode for each pipeline stage." and §3 reads "using the Python-style pseudocode in Listing 1" [p. 5] [Lst. 1] [§3].
- **HTML (LaTeXML).** The float is rendered as a generic figure (element `figure`, class `ltx_figure`, id `S2.F4`) whose caption tag reads Figure 4, while the same page's §3 sentence reads Listing 4 [ours]. LaTeXML numbered the float in the figure counter, after Figures 1 to 3; the `S2` in its id places it in §2, because `\input{tables/pseudo_code}` precedes `\section` in the TeX (tex:sections/3_new_method.tex:1-3) [ours]. So the HTML disagrees with itself, and every later HTML figure number is one higher than the PDF's [ours].
- **Verdict.** The note's Listing 1 is right (N-2). The repository's preface to the note, which says the HTML shows the pseudocode as Figure 4, is right about the HTML only; cite it as [Lst. 1].

## Special case B. Does Listing 1's pattern cover every row of Table 1? (N-79)

Listing 1's contract: a candidate goes in; each round, the critic returns a verdict and feedback; `accept` returns the candidate, `refine` replaces it with the refined one, anything else returns None; and when `max_rounds` rounds pass without acceptance, it returns None [Lst. 1] (tex:tables/pseudo_code.tex:26-35). Table 1's caption describes the same shape: a candidate from a specialized agent, and a critic that decides "whether to accept the output or invoke a refinement agent" [Tab. 1] (tex:tables/overview.tex:3).

| Tab. 1 row | critic → refine (Tab. 1) | Verdicts in §3 | Limit: symbol, A.2 value | On exhaustion | Fits Lst. 1? |
|---|---|---|---|---|---|
| Finding limitations | *Can guide novel improvement?* → *Add missing limitations* [Tab. 1] | sufficient or insufficient; no reject [§3.1] | no symbol; 16 rounds [App. A.2] | the loop ends when the "maximum number of iterations is reached"; what is kept is not said [§3.1] | Partly: no reject, and Lst. 1 would discard the set [ours] |
| Seed idea generation | *Is it novel?* → *Add more novel ideas* [Tab. 1] | a novelty score, not a verdict; ideas are then sorted by it [§3.1] | stops at `N_seed` ideas, a count with no A.2 value; novelty uses two papers retrieved via Google Search [App. A.2] | not applicable [§3.1] | No: count-driven generation [ours] |
| Reproduce baseline on subset | `-` → `-` [Tab. 1] | none [§3.2] | none | failure not described [§3.2] | No: a single step [ours] |
| Idea experiment on subset | *Is it better than the reproduced baseline?* → *Refine idea through engineering* [Tab. 1] | Good, Engineer, Bad: accept, refine, reject [§3.2] | `N_eng`; at most two engineering rounds [App. A.2] | "is designated as Bad and pruned" [§3.2] | **Yes**, the one exact fit [ours] |
| Idea experiment on full-set | *Is it better than the original SOTA result?* → *Refine idea through engineering* [Tab. 1] | a *terminal decision*, whose values are not listed [§3.2] | no symbol; A.2's limit names an Idea Critic Agent (A-NOTE-9) [App. A.2] | not stated [§3.2] | Partly [ours] |
| Idea evolution | *Idea experiment* → *Evolve idea from traces* [Tab. 1] | Good or Bad per idea, from the unified coder [§3.3] | `K` rounds and `S` successes; four and four, with `K` counted after round 0 in the paper's runs [App. A.2] [Fig. 9b] (image) | no success at all ends the whole run; one or more go on to selection [§3.3] | No: a population loop that stops on a count [ours] |
| Select best idea | *What is the best idea from traces?* → `-` [Tab. 1] | a choice, not a verdict [§3.3] | none | not applicable [§3.3] | No [ours] |
| Ablation study | *Is the component breakdown clean?* → *Refine the method* [Tab. 1] | Good or Refine; no reject [§3.4], though App. B reports one rejection, TeCh's (A-NOTE-4; the first version also counted RALI's, F-6) | `N_abl`; at most once [App. A.2] | keeping is implied: the loop sentence ends "ensuring a fully optimized hypothesis prior to manuscript generation", after either ending [inferred]; a Result Comparison Agent decides whether a refinement is kept [§3.4] | Partly: no reject, an extra gate, and it keeps at the limit [ours] |
| Initial drafting | `-` → `-` [Tab. 1] | none [§3.5] | none | not described [§3.5] | No: a single step [ours] |
| Peer-Review | *Is review score good enough?* → *Run rebuttal experiments* [Tab. 1] | a score against a threshold (e.g., 8); no reject [§3.5] | `N_peer`; at most two rounds, stopping early at 8 [App. A.2] | keeps the manuscript, "producing a polished, thoroughly validated final manuscript" [§3.5] | Partly: Lst. 1 would discard it [ours] |
| Meta-Review | *Does it meet the venue bar?* → *Refine idea and analyze again* [Tab. 1] | Accept or Refine; no reject [§3.6] | `N_meta`; at most once [App. A.2] | keeping is implied: the loop sentence ends "yielding a rigorously validated final contribution", after either ending [inferred]; if the refined result does not win, the run ends with the previous outputs [§3.6] | Partly: an extra gate, downstream re-runs, and it keeps at the limit [ours] |

**Tally** [ours]: an exact fit for 1 row of 11. No critic: 2 rows (baseline, drafting). No refine step: 3 (baseline, selection, drafting). Two-verdict critics with no reject: 4 (limitations, ablation, peer review, meta-review); a score instead of a verdict: 1 (seed ideas). Loops that stop on a count: 2 (seed ideas, evolution). Exhaustion that keeps the candidate, explicitly (peer review) or by implication (ablation, meta-review), or is not stated (limitations, full set): 5. The first version marked the ablation and meta-review rows not stated (F-5). Listing 1 also has no place for the Result Comparison gate or for re-running downstream stages after an update [§3.4] [§3.6]. What its limit counts is itself ambiguous (A-NOTE-3) [Lst. 1].

## Special case C. The note's arithmetic, redone

- **Cost (N-59).** 107 × \$3,765 = \$402,855 [ours]. The input averages "the 33 target problems sourced from NeurIPS 2025 papers", with token and virtual-machine costs [§4.3]; no cost is reported for the 64 ICML or 5 ICLR tasks, or for failed runs [ours] [Tab. 3].
- **Time (N-60).** 107 × 2.51 days = 268.6 days [ours]. Fig. 10a gives a mean of 2.51 days (60.2 h), a median of 2.00 days and an interquartile range of 1.1 to 3.1 days, from bars of 6, 11, 5, 5, 4 and 2 tasks, 33 in all [Fig. 10a] (image). These are days per task, wall-clock by the natural reading of "to complete the entire research cycle" [inferred] [§4.3]; the paper never says how it measured time or how many machines a task uses, so machine-days cannot be derived on either reading [ours].
- **Coding sessions (N-106).** Inputs: up to four rounds of two candidates, one seed and one evolved, after an initial round of `N_0` seeds, stopping at four successes, as Figure 9's rounds *Initial* to *Round 4* show (D-1) [Fig. 9b] (image); at most two engineering rounds per flagged idea; at most one ablation refinement; at most two review rounds, stopping at a score of 8; at most one meta-review refinement [App. A.2]; 5 to 6 ablations per paper on the four ICLR papers [Tab. 15]; one Ablation Coding Agent run per plan [§3.4], and one Rebuttal Coding Agent run per planned task [§3.5]. So a task tries I = 8 + `N_0` ideas: 9 if `N_0` = 1, 10 if `N_0` = 2 [ours]. Our other assumptions: one session per coding call; the two-round engineering limit applies on the full set too (A-NOTE-9, reading 2); the Initial Drafter is not a Claude Code agent, since A.2 does not list it [ours].
  - Upper bound: 1 baseline + I ideas × 6 (subset code, two engineering rounds, full-set code, two engineering rounds) + 6 ablations + 7 (one refinement, then the ablations again) + 2 × (`N_t` + 1) (rebuttal tasks and the enhancer, two rounds) + 1 + 6 + 2 × (`N_t` + 1) (meta-review refinement, ablations and review again) + 2 (integrity) = 27 + 6 × I + 4 × `N_t`: 81 + 4 × `N_t` at `N_0` = 1, and 87 + 4 × `N_t` at `N_0` = 2, i.e. 93 or 99 if `N_t` = 3 [ours]. The first version took four rounds in all, 8 ideas, and gave 75 + 4 × `N_t`; Figure 9 rules that out for the paper's runs (F-2) [ours].
  - Two assumptions stay open: the meta pass re-runs the ablations without a second ablation refinement (U-META-1), and the integrity checks add two sessions (A-INT-3) [ours]. analysis.md section 9 is the canonical bound: it resets the budgets for the meta pass (+7) and counts no integrity sessions (−2), so at `N_0` = 2 and `N_p` = 6 it gives 92 + 4 × `N_t` (D-2) [§3.6] [ours].
  - Lower bound, for a task that succeeds with no refinement anywhere: at `N_0` = 2, 1 + 4 ideas × 2 (early stop after two rounds) + 5 ablations + 0 (a score of 8 at the first review) + 2 = 16 [ours]. At `N_0` = 1 it depends on when the stop is tested (U-EVO-1): 16 if after each idea, 17 if after each round and the round's fifth idea fails at once on the subset; the register's 18 (D-2) counts that fifth idea as a success [ours].
  - A task that finds no successful idea spends 1 + I to 1 + 6 × I sessions and then stops: 10 to 55 at `N_0` = 1, 11 to 61 at `N_0` = 2 [§3.3] [ours].
  - So several dozen lies inside the range, but it is not a count: it depends on `N_0`, `N_t`, `N_p`, the full-set engineering limit, the two open assumptions, and whether one agent call is one session [ours] (U-NOTE-5).

## Gaps found here

Each item states the gap, where it sits, the quotes on each side, and the decision it forces on us [ours]. The entries stay here; the decision register, [unspecified.md](unspecified.md), indexes each one under the row named in its Register line, and records the decision there [ours]. The first version said consolidation would move them (F-14) [ours].

### A-NOTE-1 · INCONSISTENT · Listing 1 is said to abstract every stage, but three stages have no critic or no refine step

- **Where:** [§3] (tex:sections/3_new_method.tex:5); [Lst. 1] (tex:tables/pseudo_code.tex:23); [Tab. 1] (tex:tables/overview.tex:14) (tex:tables/overview.tex:20) (tex:tables/overview.tex:26).
- **One side:** "we abstract all stages (see overview in Table 1) using the Python-style pseudocode in Listing 1" [§3], and the caption calls it "Python-style pseudocode for each pipeline stage" [Lst. 1].
- **The other side:** Table 1 gives *Reproduce baseline on subset* and *Initial drafting* neither a critic nor a refine step, and *Select best idea* no refine step [Tab. 1]; most of §3's critics return two verdicts, not three [§3.1] [§3.4] [§3.5] [§3.6].
- **Decision it forces:** one primitive with a verdict map and an exhaustion policy per stage, or a few stage kinds (single step, selection, count-driven generation, population loop, critic loop) [ours]. Raised by N-79 and N-80.
- *Register: A-NOTE-1*

### A-NOTE-2 · INCONSISTENT · What a loop returns when its limit is reached

- **Where:** [Lst. 1] (tex:tables/pseudo_code.tex:24) (tex:tables/pseudo_code.tex:35); [§3.1] (tex:sections/3_new_method.tex:23); [§3.2] (tex:sections/3_new_method.tex:47); [§3.5] (tex:sections/3_new_method.tex:132); [§3.4] (tex:sections/3_new_method.tex:114); [§3.6] (tex:sections/3_new_method.tex:151).
- **Listing 1:** the candidate is "iteratively refined based on the critic's feedback up to a maximum number of rounds", and the function then ends with `return None`, discarding it [Lst. 1].
- **The stages:** the subset loop matches, since the idea "is designated as Bad and pruned" [§3.2]; the peer-review loop keeps its output instead, "producing a polished, thoroughly validated final manuscript" [§3.5]; the limitation loop ends when the "maximum number of iterations is reached", and the next step uses the limitations found [§3.1]; §3.4 and §3.6 imply keeping, since their loop sentences end "ensuring a fully optimized hypothesis prior to manuscript generation" and "yielding a rigorously validated final contribution", clauses that follow either ending of the loop [inferred] [§3.4] [§3.6]. The first version said §3.4 and §3.6 do not say (F-5; D-5) [ours].
- **Decision it forces:** an exhaustion policy per stage: discard, keep the last candidate, keep the best so far, or end the task [ours]. Raised by N-79.
- *Register: A-TOP-1*

### A-NOTE-3 · AMBIGUOUS · What `max_rounds` counts

- **Where:** [Lst. 1] (tex:tables/pseudo_code.tex:27-32); [App. A.2] (tex:sections/appendix.tex:155).
- **Listing 1:** the critic runs at the start of every round, so with `max_rounds` = n the critic runs n times, up to n refinements happen, and the n-th refinement is never judged before `return None` [Lst. 1] [ours].
- **A.2** counts refinements, "we apply engineering techniques for at most two rounds", "we refine the idea at most once" and "with review-based refinement conducted at most once", and counts reviews: the peer-review simulation "runs for at most two rounds" [App. A.2].
- **Reading 1:** `max_rounds` equals the A.2 value, and the last refinement goes unjudged. **Reading 2:** `max_rounds` is the A.2 value plus one, so every refinement is judged [ours].
- **Decision it forces:** the counting convention for each limit [ours]. Raised by N-79 and N-80.
- *Register: A-TOP-2*

### A-NOTE-4 · INCONSISTENT · The ablation critic cannot reject in §3.4, yet App. B reports it rejecting TeCh

- **Where:** [§3.4] (tex:sections/3_new_method.tex:106) (tex:sections/3_new_method.tex:114); [App. B] (tex:sections/appendix.tex:221-225); [Tab. 15] (tex:sections/appendix.tex:177); [Tab. 16] (tex:sections/appendix.tex:298-300) (tex:sections/appendix.tex:324-325); [Tab. 3].
- **§3.4:** the Ablation Critic Agent's decision takes one of two values, Good or Refine (paraphrase of the set notation), and the loop "repeats for a maximum of" `N_abl` iterations or until Good; nothing is said about running out without Good [§3.4].
- **App. B:** "the ablation critic rejected it because" the gains came from generic training controls, "so it was not accepted as a contribution" [App. B]; and ScientistTwo "additionally requires the gain to be attributable to the proposed mechanism in ablation" [Tab. 15]. The TeCh task yielded no paper: ICLR 2026 is 4 of 5 [Tab. 3]. That is the only rejection App. B gives the ablation critic: for RALI, "an earlier variant was rejected by our own critic as statistically inert" names no critic, and a subset critic's Bad fits it as well [Tab. 16] [§3.2]. The first version counted RALI's rejection here (F-6; D-6) [ours].
- **Decision it forces:** whether the ablation critic can reject, and what a rejection does: end the task, or fall back to the next successful idea in the pool of up to `S` [ours]. Raised by N-66 and N-68.
- *Register: A-ABL-1*

### A-NOTE-5 · AMBIGUOUS · Which baseline the full-set critic, and every reported gain, is measured against

- **Where:** [Tab. 1] (tex:tables/overview.tex:15-16); [§3.2] (tex:sections/3_new_method.tex:37); [App. B] (tex:sections/appendix.tex:202); [Tab. 16] (tex:sections/appendix.tex:263).
- **Table 1:** the subset critic asks "Is it better than the reproduced baseline?", the full-set critic "Is it better than the original SOTA result?" [Tab. 1]. §3.2 describes a baseline run on the subset only: the Baseline Coding Agent is to "reproduce the primary experiments of" the problem on the benchmark subset [§3.2].
- **App. B:** each system measures "against its own reproduced baseline on different hardware", and Tab. 16's gains are "self-reported by each system against its own reproduced baseline" [App. B] [Tab. 16].
- **Reading 1:** the full-set critic compares with the numbers published in the source paper. **Reading 2:** with a full-set re-run of the baseline, which §3.2 never describes [ours].
- **Decision it forces:** whether the engine reproduces the baseline on the full set, and what every gain is relative to [ours]. Raised by N-93 and N-94.
- *Register: A-FULL-1*; its reporting half is named in the row of U-EVAL-1 [ours].

### A-NOTE-6 · AMBIGUOUS · Which model the planners inside the Claude Code agents use

- **Where:** [App. A.2] (tex:sections/appendix.tex:155); [Fig. 3] (image); [§3.4] (tex:sections/3_new_method.tex:100); [§3.5] (tex:sections/3_new_method.tex:125-126).
- **A.2** puts four agents on Claude Code with Opus 4.8: "the Idea Experiment Coding Agent, the Ablation Study Agent, the Rebuttal Agent, and the Draft Enhancer" [App. A.2]. Fig. 3 draws the Ablation Study Agent as a Planning Agent plus a Coding Agent, and the Peer-Review Agent as a Review Agent plus a Rebuttal Agent [Fig. 3] (image); the text splits them into an Ablation Planner Agent and an Ablation Coding Agent [§3.4], and a Rebuttal Planner Agent and a Rebuttal Coding Agent [§3.5].
- **Unnamed in A.2:** the Baseline Coding Agent, the Subset Engineering Agent, the Full-Set Engineer, the Ablation Planner and the Rebuttal Planner [App. A.2].
- **What leans one way:** A.2 opens "Unless otherwise specified, we employ Gemini 3.6 Flash for all agents", which leaves room for §4.2's rule that Claude Code serves whenever coding is required, and Figure 3's experiment boxes draw only a Coding Agent and a Critic Agent, with no separate engineer [App. A.2] [§4.2] [Fig. 3] (image). That puts the unnamed code-writing agents on Claude Code [inferred]; it settles nothing for the planners, which write no code, so they stay open under both readings (D-7) [ours].
- **Reading 1:** the planners run on Gemini 3.6 Flash, the default. **Reading 2:** they run inside their agent's Claude Code session [ours].
- **Decision it forces:** the model-routing table [ours]. Raised by N-5, N-9 and N-115.
- *Register: A-CFG-1*

### A-NOTE-7 · INCONSISTENT · Idea refinement's share of cost: the caption against the chart

- **Where:** [Fig. 10] (tex:figures/cost.tex:4); [Fig. 10b] (image); [§4.3] (tex:sections/5_discussion.tex:4).
- **Caption:** "Idea refinement accounts for the majority of overall time and computational cost" [Fig. 10].
- **Chart:** Idea Refinement is 44.9% of time and 45.4% of cost; the rest is Initial Implements (19% and 20.1%), Ablation Studies (16.4% and 15.4%), Peer and Meta-Review (15.5% and 15.8%), Initial Drafting (3.6% and 3.1%), and a sliver of Seed Idea Generation [Fig. 10b] (image). The text says "the majority of execution time is concentrated in the Idea Refinement, Dynamic Peer-Review, and Meta-Review stages" [§4.3].
- **Decision it forces:** a cost model built on the per-stage shares, not the caption (TODO task 5) [ours]. Raised by N-107.
- *Register: A-COST-1*

### A-NOTE-8 · AMBIGUOUS · How experimentation rounds are counted, and how many seeds round 0 runs

- **Where:** [App. A.2] (tex:sections/appendix.tex:155); [§3.3] (tex:sections/3_new_method.tex:63) (tex:sections/3_new_method.tex:67); [Fig. 9b] (image).
- **A.2:** "In each idea experimentation round, we evaluate two candidates: one selected from the seed ideas and the other an evolved idea", and the loop runs "for up to four rounds" [App. A.2].
- **§3.3:** round 0 runs the top `N_0` seed ideas and has no evolved idea; evolution starts at refinement round k ≥ 1 [§3.3].
- **Reading 1:** round 0 plus four refinement rounds (`K` = 4): up to 10 ideas if `N_0` = 2, and 9 if `N_0` = 1. **Reading 2:** four rounds in all, round 0 included (up to 8 ideas). Neither gives `N_0` [ours].
- **Figure 9 favours reading 1:** its rounds are labelled *Initial*, then *Round 1* to *Round 4*, and 4 of the 49 tasks pick their best idea in *Round 4* [Fig. 9b] (image). Had round 0 been one of the four, there would be no Round 4, so the paper's runs follow reading 1; A.2's sentence alone stays ambiguous, which keeps the class (D-1; A-EVO-2) [App. A.2] [ours].
- **Decision it forces:** `N_0`, and whether A.2's four rounds follow round 0, as the paper's runs did [ours]. Raised by N-110 and N-106.
- *Register: A-EVO-2*; its `N_0` half is named in the row of A-EVO-1 [ours].

### A-NOTE-9 · AMBIGUOUS · Whether the two-round engineering limit also covers the full set

- **Where:** [App. A.2] (tex:sections/appendix.tex:155); [§3.2] (tex:sections/3_new_method.tex:41) (tex:sections/3_new_method.tex:47) (tex:sections/3_new_method.tex:52).
- **A.2:** "If the Idea Critic Agent flags an idea for engineering refinement, we apply engineering techniques for at most two rounds" [App. A.2]; §3 has no agent of that name.
- **§3.2:** the Subset Critic Agent's loop has the budget `N_eng` [§3.2], while "A Full-Set Critic Agent and Full-Set Engineer perform final validation and engineering against the full benchmark" with no budget stated [§3.2].
- **Reading 1:** the limit applies to the subset critic only, leaving the full-set loop unbounded. **Reading 2:** it applies to both critics [ours]. The readings are numbered as in A-FULL-2; the first version numbered them the other way (F-13) [ours].
- **Decision it forces:** the full-set engineering limit [ours]. Raised by N-1 and N-106.
- *Register: A-FULL-2*

### A-NOTE-10 · INCONSISTENT · Is the CoE audit a post-hoc measurement, or a gate inside the run?

- **Where:** [§4.2] (tex:sections/4_experiment.tex:41) (tex:sections/4_experiment.tex:43); [App. B] (tex:sections/appendix.tex:236-238); [Tab. 15] (tex:sections/appendix.tex:186); [Tab. 16] (tex:sections/appendix.tex:313).
- **§4.2:** the audit "is a post-hoc evaluation framework", and the pipeline guards the four properties with "three dedicated refinement agents alongside careful agent prompt design" [§4.2]; the source Table 7 follows calls its audit "a post-hoc audit that checks whether claims in a completed paper are supported by the underlying artifacts" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:16).
- **App. B:** "ScientistTwo instead blocks both structurally, via a reproduction re-run (I1), a protocol-immutability audit (I2)" and a method–code audit, "rather than a prompt-level list of prohibitions" [App. B]; Tab. 15 marks changes to the evaluation protocol as "forbidden (audit)", and Tab. 16 says the audits "make this class of edit inadmissible" [Tab. 15] [Tab. 16]. The labels I1, I2 and I4 appear only in App. B, and I3 is never named [App. B].
- **Enforcement classes:** in the classes of [stages/07-integrity.md](stages/07-integrity.md), as fix F-AN-11 fixes them (prompt, LLM filter, LLM fixer, post-hoc LLM audit, setup), §4.2's mechanisms are a prompt, an LLM filter and two LLM fixers, the audit behind Table 7 is a post-hoc LLM audit, and nothing is enforced by the setup; App. B's structural blocking rests on audits, not on the setup [§4.2] [Tab. 7] [App. B] [ours].
- **Decision it forces:** whether our audit only measures, or also blocks results inside the run (TODO task 6) [ours]. Decided in register row A-INT-1 of [unspecified.md](unspecified.md), whose full entry is in [stages/07-integrity.md](stages/07-integrity.md): a locked harness computes every metric (U-INT-4), because a re-run used as a gate proves only that the code is deterministic, as Table 7's first row shows by passing a reward-hacked codebase on score verification [Tab. 7] [fn. 2]; the register row adds gates inside the run, where the harness re-executes each result before a critic reads it, and an audit before export, repeated at evaluation [ours]. Raised by N-15, N-76 and N-103.
- *Register: A-INT-1*

### U-NOTE-1 · UNSPECIFIED · Separating the data that selects ideas from the data that is reported

- **Where:** [§3.3] (tex:sections/3_new_method.tex:90); [§3.4] (tex:sections/3_new_method.tex:112); [§3.5] (tex:sections/3_new_method.tex:119); [§3.6] (tex:sections/3_new_method.tex:147).
- **What the paper says:** the Selector compares ideas "evaluated on the full benchmark" [§3.3]; the Result Comparison Agent decides updates on the same kind of results [§3.4] [§3.6]; the drafter writes up the main benchmark results [§3.5]. No held-out split appears in §3 or in App. A.2 [App. A.2].
- **Nearby:** the example audit lists test and OOD leakage among specification violations [p. 48] (image); that checks code, not a data split [ours].
- **Decision it forces:** a validation/test split per task, and which numbers each agent may see (TODO task 6) [ours]. Raised by N-90 to N-92.
- *Register: U-NOTE-1*

### U-NOTE-2 · UNSPECIFIED · How a relative gain is computed

- **Where:** [§4.1] (tex:sections/4_experiment.tex:19); [Tab. 4]; [§1] (tex:sections/1_introduction.tex:21).
- **What the paper says:** "we parse the main tables for 10 times using Gemini 3.6 Flash and averaged them" [§4.1]; the headline 25.2% equals Tab. 4's ScientistTwo average [§1] [Tab. 4].
- **Not given:** the formula (per metric or pooled; how datasets and metrics are averaged; the sign for lower-is-better metrics), which tables count as main, and the baseline (A-NOTE-5) [ours].
- **Decision it forces:** a deterministic gain definition computed from result files (TODO task 6) [ours]. Raised by N-93 and N-94.
- *Register: U-EVAL-1*

### U-NOTE-3 · UNSPECIFIED · Each task's subset, full set and metrics, and who defines them

- **Where:** [§3.2] (tex:sections/3_new_method.tex:37); [§1] (tex:sections/1_introduction.tex:16); [App. A.1]; [App. B] (tex:sections/appendix.tex:238-239); [Tab. 6] (tex:tables/ablation_review_refine.tex:3).
- **What the paper says:** the baseline is reproduced on the benchmark subset [§3.2]; ideas are screened on representative benchmark slices [§1]; ScientistTwo evaluates "on the paper's full benchmark grid" [App. B]; Tab. 6 shows benchmark results generated by ScientistTwo itself [Tab. 6]; App. A.1 lists titles only [App. A.1].
- **Not given:** any task's subset, its full set, its metrics, and whether a person or the Baseline Coding Agent chooses them [ours].
- **Decision it forces:** task packaging (TODO tasks 4 and 5) [ours]. Raised by N-12, N-27 and N-28.
- *Register: U-BASE-1*

### U-NOTE-4 · UNSPECIFIED · The audit's parameters, and the evaluator it presumes

- **Where:** [§4.2] (tex:sections/4_experiment.tex:41); [Tab. 7]; [p. 47] (image); [p. 48] (image); [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:23-44).
- **What the paper says:** score verification compares "reported scores against those obtained from re-executing the repository" [§4.2]; the one example shows a single re-run whose numbers matched exactly [p. 47] (image), and one report with a verdict per dimension [p. 48] (image).
- **Given by reference:** Table 7 follows ScientistOne [Tab. 7], whose audit definition re-runs the solution on the golden evaluator and passes it within an adaptive tolerance, judges specification and alignment by majority vote over several LLM runs, resolves references through four APIs, and counts code as misaligned only for a fundamentally different algorithm [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:23-44). In ScientistOne's own runs, each evaluator ran five times against max(1%, 3σ/\|s̄\|) [Ref: meng2026scientistone §6] (ref:2605.26340v1:sections/06a_setup.tex:10), the I2 counts took 3 of 5 judges [Ref: meng2026scientistone App. E] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:302), and humans reviewed the flagged I1 to I3 cases [Ref: meng2026scientistone App. D] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:53-57); those are its practice, not its definition [ours]. The details are at N-40 to N-43.
- **Not given:** which evaluator is the golden one for ScientistTwo's tasks, where the coding agents produce the results [§3.2], while ScientistOne presumes that "Each task provides a fixed evaluator, starter code, and scoring metric" [Ref: meng2026scientistone §6] (ref:2605.26340v1:sections/06a_setup.tex:8); whether Table 7 used ScientistOne's run count, tolerance and human review; and why the one example is a single exact re-run: if p. 47 is the CoE audit (A-INT-1), it states no tolerance, where the definition calls for an adaptive one, and it departs from ScientistOne's own practice of five runs [p. 47] (image) [ours]. The first version listed the run count, the tolerance, the votes and the reference lookup as not given; the definition gives the adaptive tolerance, the votes and the lookup, and ScientistOne's own runs give the run count and the formula (F-NC-1; closure error 2) [ours].
- **Decision it forces:** the audit's thresholds and procedure, starting from ScientistOne's, and a fixed evaluator for each task (TODO task 6) [ours].
- *Register: U-NOTE-4*

### U-NOTE-5 · UNSPECIFIED · How many ablation plans and rebuttal tasks

- **Where:** [§3.4] (tex:sections/3_new_method.tex:100); [§3.5] (tex:sections/3_new_method.tex:125); [Tab. 15] (tex:sections/appendix.tex:188).
- **What the paper says:** the Ablation Planner writes `N_p` plans and the Rebuttal Planner `N_t` tasks [§3.4] [§3.5]; A.2 sets neither [App. A.2]; Tab. 15 reports 5 to 6 ablations per paper, for the four ICLR papers only [Tab. 15].
- **Decision it forces:** `N_p` and `N_t`, which drive cost (special case C) [ours]. Raised by N-106.
- *Register: U-ABL-1*; its `N_t` half is named in the row of U-PEER-1 [ours].

### U-NOTE-6 · UNSPECIFIED · How many tasks had a second review round

- **Where:** [Tab. 5]; [App. A.2] (tex:sections/appendix.tex:155); [§4.2] (tex:sections/4_experiment.tex:34).
- **What the paper says:** the review loop stops early "if the ScholarPeer review score reaches 8" [App. A.2]; Tab. 5 reports review rounds 0, 1 and 2 over 49 tasks [Tab. 5].
- **Not given:** how many of the 49 had a second round, so the change from round 1 to round 2 rests on an unknown subset [ours].
- **Decision it forces:** when we compare rounds, we report n per round [ours]. Raised by N-96.
- *Register: A-EVAL-5*

### U-NOTE-7 · UNSPECIFIED · Which runs the cost figures cover, and at what prices

- **Where:** [§4.3] (tex:sections/5_discussion.tex:4); [Tab. 3]; [Fig. 10] (image).
- **What the paper says:** cost and time are analysed "on the 33 target problems sourced from NeurIPS 2025 papers", including token and virtual-machine costs [§4.3]; 33 is also the number of successful NeurIPS runs [Tab. 3].
- **Not given:** whether the five failed NeurIPS runs are included, token prices, machine types, and GPUs per task [ours].
- **Decision it forces:** our cost model and its sample (TODO task 5) [ours]. Raised by N-58 to N-60.
- *Register: U-COST-1*
