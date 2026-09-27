# Initial replication note (UNVERIFIED input)

> **What this is.** A note Vlad pasted on 2026-09-27. It was written by an AI assistant in another
> chat, about how hard it would be to replicate ScientistTwo (arXiv:2609.19644). It is kept
> VERBATIM below, because a summary would already be an interpretation.
>
> ⛔ **It is a secondary source, and none of it is verified.** TODO task 1 checks every claim
> against the paper's own text and marks it true, false, or not in the paper. Until then, cite the
> paper, never this note.
>
> Already known to need checking: the note calls the stage pattern "Listing 1", while the paper's
> HTML shows the stage pseudocode as a figure (Figure 4).
>
> Two closing parts of the original are omitted: a note on the wording of Vlad's request, and an
> offer to scaffold the repository. Nothing else is changed.

---

## Where the difficulty actually is

| Component | What the paper gives you | Difficulty |
|---|---|---|
| Control flow | A full spec: Section 3, Table 1, the Listing 1 stage pattern, and the loop limits in Appendix A.2 | Easy |
| ~15 reasoning agents (extractor, critics, evolver, selector, planners, meta-reviewer) | Their roles, inputs and outputs, but no prompts | Easy to write, hard to make good |
| Coding stages (baseline, subset and full coders, engineer, ablation, rebuttal, enhancer) | "Claude Code with Opus 4.8" | Medium. Wiring them up is simple; keeping dozens of long sessions reliable isn't |
| Task environments | The list of 107 papers, with no subset or metric definitions | Hard, and manual for every task |
| Evaluation integrity | Self-contained scripts plus an LLM validation filter | Hard, because it has to be enforced by the setup, not by prompts |
| Drafting | PaperOrchestra | Easy, since it's open source |
| In-loop reviewer | ScholarPeer | Medium: you'd rebuild it from its paper |
| Integrity audit | The CoE audit, specified in the ScientistOne paper | Medium |

The benchmark gap is real. Take the AI Engram paper. AutoSOTA's packaged version of that task optimizes an approximate ToW score on CIFAR-10 with ResNet-18. ScientistTwo's Table 6 evaluates the same paper on TOFU with Llama-3.2-1B. Same paper, different benchmark. ScientistTwo never published its subset and full-set definitions, so you'll have to define your own.

## Reuse before you build

- **Drafting.** Google Research open-sourced PaperOrchestra, which turns idea summaries and experiment logs into LaTeX manuscripts using outline, literature-review, section-writing, refinement and plotting agents. That's exactly what ScientistTwo's drafter wraps. A community port notes that the paper's appendix includes the prompts for every agent.
- **Task environments.** All 107 of ScientistTwo's target papers came from AutoSOTA's benchmark or its filtering process (Appendix A.1). AutoSOTA maintains a leaderboard of automatically optimized research codebases and ships a CLI.
  - Its ICML-2026 folder has slimmed code for hundreds of papers, with datasets and weights stripped, plus a final report for each.
  - The AI Engram folder also records the eval command, the baseline scores and the files that must not be modified.
  - Use these folders as your template for packaging a task.
- **Integrity audit.** The ScientistOne paper specifies it precisely:
  - Re-run the solution on the reference evaluator five times; it passes if the reported score is within max(1%, 3σ/|mean|).
  - Judge spec violations and method–code alignment by majority vote of several LLM judges.
  - Resolve every reference against Semantic Scholar, arXiv, OpenAlex and Crossref.
- **Coding backend.** The Claude Agent SDK gives you the same tools, agent loop and context management as Claude Code, from Python or TypeScript. The SDK packages support structured outputs and tool-approval callbacks, and they respect CLAUDE.md files, skills and hooks. So you can block any edit to the evaluation files at the tool level.
- **Reviewers.** I couldn't find released code for ScholarPeer, but its design is documented: a historian agent builds the field's context, a baseline scout looks for missing comparisons, and a Q&A engine checks claims against current literature. For an independent (held-out) reviewer, paperreview.ai is free, but it only accepts PDFs and reads at most 15 pages. Its tech overview describes its workflow, which grounds reviews in searched arXiv papers, if you'd rather build your own version.
- **Ablation logic.** MLE-STAR, by the same lead authors, is open source, and its refinement loop already uses ablations over individual code blocks. Its prompts are worth borrowing.

## Scope: replicate the system, not the 107-task numbers

At the paper's average of $3,765 per task, running the full benchmark would cost about $400k and take roughly 270 machine-days. Your numbers would differ anyway, because your models, prompts and benchmark definitions will differ.

A better target: build on three cheap development tasks, then use the five ICLR 2026 tasks as your test set. Appendix B documents what ScientistTwo did on each of them:
- It produced accepted methods for Pinet, DMSQD, T-SAE and RALI, and those four generated papers are on the project site.
- It rejected its own idea for TeCh, because its ablation critic traced the gain to EMA and label smoothing rather than the new mechanism.
- It also shows what AutoSOTA did on the same five papers.

TeCh doubles as a test of your own system: your ablation critic should reject that idea too. Check compute before you commit. T-SAE trains sparse autoencoders on Pythia-160m and Gemma-2-2b, and RALI spans seven image-quality datasets. The other three look lighter.

## Repo design

```
scientist2-repro/
├── SPEC.md, CLAUDE.md     # paper-to-module map; rules for the coding agent
├── configs/               # loop limits (App. A.2), model routing, budgets
├── tasks/<id>/            # task.yaml, Dockerfile, eval/ (read-only), subset spec
├── s2/core/               # stage primitive, run state, budget guard
├── s2/agents/             # one module + JSON schema per agent
├── s2/coder/              # Agent SDK adapter (OpenHands/Codex as fallback)
├── s2/sandbox/            # containers, GPU queue, clean re-runs
├── s2/writing/, s2/review/  # PaperOrchestra wrapper; in-loop + held-out reviewers
├── s2/audit/              # I1–I4 checks
├── prompts/               # versioned prompt files
└── runs/<run_id>/         # artifacts, a git worktree per idea, traces, costs
```

Seven rules that decide whether this works:

1. **Build one stage primitive.** Listing 1's pattern covers every row of Table 1: generate, let a critic accept, refine or reject, and stop after N rounds. Implement it once and configure each stage.
2. **Make runs resumable.** Every stage writes its output to files, every idea lives on its own git branch, and a crash resumes from the last finished stage. Runs take days. In ScientistOne's evaluation, 16 of 75 runs needed an infrastructure retry.
3. **Metrics come only from the locked evaluation harness.** Agent code never writes results. The harness runs in its own container, with the evaluation code and data splits mounted read-only and checked against hashes. This has to be enforced by the setup, not by prompts. In ScientistOne's scaling experiments, the share of attempts flagged for gaming the metric rose from about 0% to about 70% as the per-attempt budget grew.
4. **The paper writer sees only verified numbers.** ScientistOne caught Sakana's AI Scientist writer picking better scores from ablation runs. Pass PaperOrchestra a single verified results table and nothing else.
5. **Search on validation data, test once.** I couldn't find where the paper separates the data used to pick ideas from the final test data. Make every number an agent can see a validation number, and report test results only at the end.
6. **Compute gains deterministically and use a separate judge.** Calculate gains directly from the results files; the paper instead had Gemini parse its tables 10 times and averaged. Never evaluate with the reviewer you optimize against: in Table 5, a second review round raised the in-loop reviewer's acceptance rate while the held-out reviewer's rate dropped.
7. **Add a budget guard and a mock mode.** Put hard cost caps on each session and each task. Add a fake LLM and fake coding agent so you can test the whole state machine for free.

## Build plan

| Phase | Time | Build | Done when |
|---|---|---|---|
| 0 | Week 1 | Environments for 3 dev tasks; locked evaluation harness | The baseline reproduces in a fresh container |
| 1 | Week 2 | Stage primitive, run state, model routing with JSON schemas, Agent SDK adapter, sandbox, mock mode | A hand-written idea runs end to end: subset run, critic, full run |
| 2 | Weeks 3–4 | Limitation loop, seed ideas with novelty check, engineering loop, idea evolution and selection, ablation loop | It finds, without supervision, one improvement that survives its own ablations |
| 3 | Week 5 | PaperOrchestra drafting, review-and-rebuttal loop, meta-review | A compiled PDF with its review history |
| 4 | Week 6 | I1–I4 audit, gain calculator, held-out reviewing | All four checks pass on the dev tasks |
| 5 | Weeks 7–8 | Prompt tuning from traces, the five ICLR tasks, ablations of your own loops | A replication report against Appendix B |

These durations are rough estimates for one person working with heavy AI assistance.

## Budget and models

By my count from the paper's loop limits, each task runs several dozen long coding-agent sessions. The paper says idea refinement accounts for most of its cost.

For development, use a cheap profile and measure cost on your first task before scaling:
- two evolution rounds instead of four,
- one review round,
- no meta-review refinement,
- a cheaper coding model for subset screening,
- hard caps on turns per session.

The paper used Opus 4.8 for coding and Gemini Flash for everything else. Through the Agent SDK you can point the coding stages at Opus 5.5 or Sonnet 5, and use Haiku 4.5 or a Flash-class model for the reasoning agents. If you run on a Claude subscription, note that since June 15, 2026, Agent SDK and headless usage draws from a separate monthly Agent SDK credit. At this volume, plan for API billing.

## How to vibe-code it

Let Claude Code write the plumbing: orchestration, adapters, sandbox and audit. Give it a SPEC.md that maps each paper section to a module and a JSON schema, and a CLAUDE.md with rules like "never edit `tasks/*/eval`". Build in order of risk: environments and sandbox first, agents last. Have it write the mock-mode tests before any real model runs. Write the prompts yourself. They're what the paper didn't release, and they'll decide whether the system finds real gains or just produces well-formatted noise.
