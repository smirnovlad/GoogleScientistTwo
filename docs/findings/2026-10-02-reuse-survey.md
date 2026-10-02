# Reuse survey for the ScientistTwo engine

Checked 2026-10-02. This is TODO task 4. The target is the engine in
[ScientistTwo](https://arxiv.org/html/2609.19644v1), not a rerun of its benchmark.
The candidate list came from the unverified initial note. A project web page,
paper, and source repository answer different questions; a paper describing a
method does not imply that runnable, licensed code exists.

Repository snapshots inspected: PaperOrchestra
[`ca1b3fa`](https://github.com/google-research/paper-orchestra/tree/ca1b3fa01c2970fc7cda32d16245db38d57b3f56),
AutoSOTA [`d39ac9e`](https://github.com/tsinghua-fib-lab/AutoSOTA/tree/d39ac9e03cf999589be196f06a26cc8449bb3031),
MLE-STAR [`d33445d`](https://github.com/jaehyun513/MLE-STAR/tree/d33445de01d66b42cf3e5093bc0623502393864c),
and Claude Agent SDK for Python
[`bfb895c`](https://github.com/anthropics/claude-agent-sdk-python/tree/bfb895c6ef46e095191938b4eda798a025957c09).

## Decision summary

| Candidate | Decision for this engine | Confidence |
|---|---|---|
| PaperOrchestra | Trial as a drafting backend behind our own contract; admit only verified results to its input. | Medium |
| AutoSOTA | Use its catalog as a lead for task selection. Package and verify tasks ourselves. | High |
| ScientistOne CoE audit | Implement the four checks as our own audit; use its protocol as a reference. | High for protocol, low for reusable code |
| MLE-STAR | Borrow the idea of targeted ablations, not code. | High |
| ScholarPeer | Define a reviewer contract and mock; implement or license a reviewer after a reproducibility decision. | Medium |
| Claude Agent SDK / `claude -p` | Trial as one coding-backend adapter inside an external sandbox, including a local subscription mode. | High for capability, medium for fit |
| paperreview.ai | Manual held-out feedback only; do not put the website in an automated run. | High |

## 1. PaperOrchestra

- **Source and maintenance.** The [Google Research repository](https://github.com/google-research/paper-orchestra)
  is public, Apache-2.0, and contains `methods/`, `templates/`, a Python CLI and a
  Streamlit demo. Its repository showed two commits and no releases when checked;
  the README says the paper-writing dataset is absent and will be released later.
  The [paper](https://arxiv.org/abs/2604.05018) is the method reference.
- **Coverage.** The CLI takes a raw-materials directory and LaTeX template, then
  runs outline, literature, writing, refinement and optional plotting agents.
  This covers the initial-draft part of ScientistTwo §3.5, not the experiment,
  rebuttal or meta-review stages.
- **Use.** Wrap the CLI behind `DraftingBackend`. Prepare a restricted materials
  directory containing the selected idea, source paper and a single verified
  results table, including ablations. Record the exact repository commit,
  template, model routing and output. Validate that produced citations and
  quantitative claims resolve to approved evidence before export.
- **Cost and terms.** Repository code is Apache-2.0. Its README requires Python
  3.11, model credentials and optionally Semantic Scholar; inference, search and
  TeX compilation cost time or money. There is no published fixed per-paper cost.
- **Trust limit.** A runnable CLI exists, but a two-commit repository and missing
  dataset do not establish a stable library API or reproduction of the paper's
  results. Run a small fixture before depending on it. `⛔ WHY NOT` pass raw agent
  logs to the drafter: they contain unverified scores that could enter the paper.

## 2. AutoSOTA

- **Source and maintenance.** The [AutoSOTA repository](https://github.com/tsinghua-fib-lab/AutoSOTA)
  is public under MIT and showed 138 commits, with a 2026-07-27 v0.3.1 CLI news
  item when checked. Its [CLI guide](https://github.com/tsinghua-fib-lab/AutoSOTA/blob/main/cli_guide.md)
  describes local setup. ScientistTwo Appendix A.1 says its 38 NeurIPS and five
  ICLR tasks came from AutoSOTA benchmarks; its 64 ICML tasks followed AutoSOTA's
  filtering process.
- **Coverage.** The repository publishes a curated leaderboard and optimized
  papers, plus CLI tarballs. The CLI requires an already cloned runnable research
  codebase, working evaluation environment and a user-supplied target metric.
  It does **not** turn the leaderboard into a ready-to-run, independently locked
  ScientistTwo task suite.
- **Use.** Treat the catalog as a list of possible source papers. For each chosen
  task, create our own pinned code revision, dataset manifest, baseline,
  validation/test split and evaluator contract. Do not import leaderboard gains
  as our baseline or ground truth.
- **Cost and terms.** Repository files are MIT. The CLI guide says users accept
  service terms via `autosota login`; those terms need separate review before
  running its tarball. A run needs local compute and model/research API access.
- **Trust limit.** The catalog is actively updated but contains successful
  optimization records, not a controlled sample of all attempts. Its CLI solves
  code optimization, not the whole ScientistTwo research and drafting workflow.
  `⛔ WHY NOT` use its evaluator as ours: task-specific evaluation and a held-out
  test policy must be fixed independently of an optimizing agent.

## 3. ScientistOne Chain-of-Evidence audit

- **Source and maintenance.** [ScientistOne §5](https://arxiv.org/html/2605.26340v1)
  is a paper protocol (v1, 2026-05-25, CC BY 4.0 in its HTML), not a software
  dependency. No runnable audit package was identified in this survey.
- **Coverage.** An adapter normalizes paper, solution code and references; four
  independent checks then verify scores by rerunning on a golden evaluator,
  detect task-specification violations, resolve citations through academic APIs,
  and compare the method description with code. The latter two judgment tasks
  use repeated LLM votes; the paper also defines a native claim-provenance check
  when a system records source links while writing.
- **Use.** Implement those checks against our locked harness and provenance
  records. Keep deterministic rerun and score comparison separate from LLM
  judgments. Record every input, verdict and evidence reference. Task 6 owns
  exact thresholds and failure gates.
- **Cost and terms.** Paper text is CC BY 4.0; implement from the protocol rather
  than copy an unidentified codebase. Costs include evaluator reruns, academic
  lookups and repeated model judgments, scaling with manuscripts and references.
- **Trust limit.** The protocol is a useful audit definition, not proof that our
  evaluator is golden or our judges are reliable. ScientistOne's own run settings
  should not be mistaken for universally prescribed thresholds. `⛔ WHY NOT` make
  the audit the only integrity guard: a post-hoc check cannot protect a search
  loop that has already optimized on test feedback.

## 4. MLE-STAR

- **Source and maintenance.** The [MLE-STAR paper](https://arxiv.org/abs/2506.15692)
  describes search-led model selection and refinement guided by code-block
  ablations. An [author repository](https://github.com/jaehyun513/MLE-STAR)
  exists, but when checked it contained only example intermediate/final outputs
  and a one-line README, with no LICENSE or runnable implementation visible.
- **Coverage.** Its ablations help prioritize components of an ML solution. It
  does not supply ScientistTwo's idea critic, full-set experiment, manuscript or
  peer-review workflow.
- **Use.** Use targeted component ablations as a design reference for our
  `AblationPlan` and result records. Implement and test the loop in our own
  engine, under the locked evaluator.
- **Cost and terms.** Reading/citing the paper costs nothing; no reusable code
  license was established from the inspected author repository. Ablation compute
  varies by task and must be capped in task 5.
- **Trust limit.** The initial note's claim that MLE-STAR is reusable open-source
  code is unsupported by the checked author repository. `⛔ WHY NOT` vendor its
  examples: outputs are neither an engine nor a licensed library.

## 5. ScholarPeer

- **Source and maintenance.** The [ScholarPeer paper](https://arxiv.org/abs/2601.22638)
  was revised in May 2026. A search of public GitHub repositories and the
  expected Google Research repository found no author-published implementation;
  search absence is not proof that none exists elsewhere. The third-party
  `open-scholar-peer` project is not evidence of fidelity to the paper.
- **Coverage.** The paper specifies a sub-domain historian, baseline scout and
  multi-aspect Q&A review of technical soundness and literature. ScientistTwo
  §3.5 uses ScholarPeer in its revision loop and §4 also uses it for evaluation.
- **Use.** Define a versioned `ReviewerBackend` contract with score, comments,
  cited evidence, model configuration, scoring rubric, scale, aggregation rule
  and raw response. Start with a mock; a concrete implementation needs its own
  acceptance tests and calibration. ScientistTwo's stop threshold of 8 cannot
  be transferred to a new reviewer until its score scale is calibrated
  (`A-EVAL-3` in the paper analysis).
- **Cost and terms.** The paper is available to read. No code license, hosted API
  or price was verified. A local reproduction would incur search and model costs.
- **Trust limit.** Exact prompts, model route and score calibration remain open
  (`U-PEER-3` in the paper analysis). The in-loop reviewer is an optimization
  target, so it cannot serve as the independent reported judge. `⛔ WHY NOT`
  substitute a community clone without calibration: identical names do not
  imply identical scores or failure modes.

## 6. Claude Agent SDK

- **Source and maintenance.** The [official SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview)
  and [Python repository](https://github.com/anthropics/claude-agent-sdk-python)
  describe a maintained Python/TypeScript library for running the Claude Code
  agent loop. The Python repository is MIT, had 890 commits when checked, and
  installs with `pip install claude-agent-sdk`.
- **Coverage.** Built-in file/command tools, sessions, hooks, permissions and
  project configuration fit a coding-backend adapter. It does not implement our
  research stages, evaluator, GPU queue or cost ledger.
- **Use.** Put it behind `CodingBackend` and pass a task-scoped working directory,
  model, turn and budget limits. Capture the session ID and transcript, plus the
  workspace revision, generated artifacts, evaluator inputs, call outcome and
  cost record; all are needed to resume a research stage without repeating paid
  work. A local subscription adapter may use an authenticated Claude Code CLI
  with `claude -p`; keep the evaluator and test data outside the agent's writable
  environment. Routing all research roles to Claude would be our model-routing
  decision, since ScientistTwo Appendix A.2 also uses Gemini.
- **Cost and terms.** The SDK repository is MIT, but the official overview says
  usage is governed by Anthropic Commercial Terms. The
  [Claude plan guidance](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)
  says a proposed June 2026 billing change was paused: Agent SDK and `claude -p`
  still count against a user's subscription limits. The
  [Claude Code billing guide](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
  says an `ANTHROPIC_API_KEY` overrides plan authentication and incurs API
  charges. The [SDK quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart)
  instructs third-party product developers to use API-key authentication unless
  Anthropic approves otherwise. A personal local engine can trial the plan
  route; a shared product needs separate terms. Task 5 must model plan limits,
  monetary charges and any non-Claude services separately.
- **Trust limit.** The repository says `allowed_tools` auto-approves tools; it is
  **not** a deny list. `disallowed_tools` and hooks can restrict requests, but
  neither replaces OS/container isolation for protected files. `⛔ WHY NOT`
  rely on a prompt or permission callback alone: an agent with command execution
  must not be able to write the locked harness by another route.

## 7. paperreview.ai / Stanford Agentic Reviewer

- **Source and maintenance.** The [live service](https://paperreview.ai/) identifies
  Stanford ML Group and offers free PDF reviews. Its
  [technical overview](https://paperreview.ai/tech-overview) explains the search,
  document extraction and review workflow. No public API, source license,
  retention terms or service-level commitment was visible on those pages.
- **Coverage.** It reads an uploaded English-language PDF, optionally a target
  venue, grounds feedback in searched arXiv work, and returns a review. The site
  says max 10 MB and only the first 15 pages are analyzed; score display is
  described for ICLR submissions in the technical overview.
- **Use.** A human may submit an eligible released or approved PDF as a separate,
  held-out qualitative check. Record the PDF hash, submission date, output and
  which pages were analyzed. Keep it out of the optimization loop.
- **Cost and terms.** The page advertises free reviews but requires an email and
  uploads the PDF to an external service. Operational limits and data terms are
  not established from the inspected pages.
- **Trust limit.** No verified automation interface or version pin means it
  cannot be a reproducible CI gate or numeric acceptance metric. The service
  itself warns that generated reviews may contain errors. `⛔ WHY NOT` automate
  browser uploads as an engine backend: service behavior, privacy terms and
  scoring can change without a versioned contract.

## Consequences for implementation

1. Implement our own task and evaluator contracts first. AutoSOTA is a source of
   candidate tasks, not our benchmark package.
2. Keep drafting, coding and reviewing behind separate interfaces; use mocks to
   run the state machine at zero model cost.
3. Treat the locked harness, provenance store and audit as owned components.
   No external candidate supplies their trust boundary.
4. Pin every external repository commit and model route in a run manifest before
   claiming reproducibility. Recheck service terms and prices when task 5 sets
   the budget and when an integration is first executed.
5. Task 6 must source or build and calibrate an independent reporting judge
   (`U-EVAL-3`). Manual paperreview.ai feedback can supplement that judge, but
   cannot fill a versioned, reproducible reporting contract by itself.
6. Expose API and local Claude subscription backends separately. The latter
   must detect API-key override, stop at plan limits and resume through the run
   journal; a subscription is not an unlimited compute budget.
