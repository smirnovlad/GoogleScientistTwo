# The engine: components, contracts and decisions

**For** whoever builds, runs or extends the engine. It replicates ScientistTwo (arXiv:2609.19644)
as `docs/paper/analysis.md` describes it. Section numbers in brackets cite the paper; "analysis
§n" cites `docs/paper/analysis.md`; gap IDs (A-…, U-…) are rows of `docs/paper/unspecified.md`.

Set by Vlad on 2026-10-02: every agent runs through `claude -p` on his subscription, never the
API, and the engine is delivered without questions to him (`DEVELOPMENT_PROCESS.md`).

## 1. Shape

One run maps a task G to a paper and a codebase, (P+, C+) = A(G) [§3, Eq. 1]. The orchestrator is
analysis §4's control flow as plain Python. Every stage is one parameterised **stage primitive**
(analysis §3.4–3.5), with its parameters in data. Every agent is a prompt, a schema and a route,
in data. Everything the run produces is a file in the run directory, so a crashed run resumes.

```
scientisttwo/                 the engine package (python -m scientisttwo)
  cli.py                      run | resume | status | report
  orchestrator.py             scientist_two(G): analysis §4, stage by stage
  primitive.py                the stage primitive
  stages/                     one module per paper section, each a use of the primitive
    limitations.py  seeds.py  coder.py  evolution.py  ablation.py  writing.py  meta.py  integrity.py
  runtime/                    agent runtime: spec, render, call, validate, memoise, account
    agents.py  backends/{base,claude_cli,mock}.py  store.py  budget.py
  harness/                    the locked evaluation harness and the sandbox
    harness.py  sandbox.py
  task.py  workspace.py  config.py
  agents/<agent>/             DATA: agent.json, system.md, prompt.md, schema.json
  config/                     DATA: profiles (paper.json, quick.json), routing.json
tasks/<task-id>/              a task G (section 6)
tests/                        mock mode: the whole engine for $0
```

## 2. Components and their contracts

| Component | Input | Output | Failure modes, and what happens |
|---|---|---|---|
| **Backend** (interface) | an `AgentCall`: system text, user text, output schema, model, effort, tools, working dir, sandbox profile, timeout | an `AgentResult`: structured output, raw text, transcript path, equivalent cost (or `None` = unknown), tokens, duration, session id | transient error → retried by the runtime; rate limit → `RateLimited(reset_at)`; timeout → `AgentTimeout`; invalid output → `InvalidOutput` |
| `ClaudeCLIBackend` | as above | as above, from `claude -p --output-format json` | see section 3 |
| `MockBackend` | as above | scripted outputs, keyed by agent and call index; coding mocks edit files | none: it is deterministic |
| **Agent runtime** | agent name, template variables, a unit key | the validated output | renders `prompt.md`; validates against `schema.json`; on `InvalidOutput` retries once with the error appended; records the unit |
| **Run store** | unit key, inputs hash | a stored result, or nothing | a unit is written atomically (temp file, rename) only when it completes, so a crash leaves no half-unit; on resume, a completed unit is returned without a call: **a retry never spends twice** |
| **Budget guard** | each unit's cost and time | continue, or `BudgetExceeded` | caps per run: agent calls, coding sessions, wall-clock hours, equivalent USD; an unknown cost counts as unknown, never zero |
| **Task** | `tasks/<id>/task.json` | a validated `Task`, and the sha256 manifest of its harness | missing file or schema error → refuses to start |
| **Workspace** | a parent codebase version | a new version: a copy, under git, so every change is a diff | a coding unit that fails leaves no version behind |
| **Harness** (locked) | a codebase version, a split, seeds | metrics computed by the task's own metric on the code's predictions | crash, timeout or missing predictions → a `failed` result, with the log tail, that critics see; a changed harness file → `HarnessTampered`, the run stops |
| **Sandbox** | a policy: writable dirs, denied dirs, network | a `sandbox-exec` profile | not macOS → refuses unless `--allow-unsandboxed` |
| **Stage primitive** | generator, critic, refiner, verdict map, guard, limit, exhaustion policy | the kept candidate, or `None` | as its parameters say; an agent failure inside a stage is the unit's failure (above) |
| **Orchestrator** | a task, a profile | `export/`: the manuscript, the codebase, the verified results, the audit | ends in one of analysis §4.3's branches, recorded in `run.json` |

## 3. The `claude -p` backend

Every call is one `claude -p` process with:

- `--output-format json`, and `--json-schema <the agent's schema>`: the CLI validates the output
  and returns it as `structured_output` (checked 2026-10-02, `DEVELOPMENT_PROCESS.md`);
- `--setting-sources ""`, `--strict-mcp-config --mcp-config '{"mcpServers":{}}'` and
  `--disable-slash-commands`: the agent sees only the engine's prompt, never Vlad's `CLAUDE.md`,
  hooks, plugins, skills or MCP servers (probe of 2026-10-02);
  - ⛔ WHY NOT `--bare`: under it, auth is "strictly ANTHROPIC_API_KEY", which bills the API;
- `--model` and `--effort` from `config/routing.json`;
- `--tools`: `""` for a pure reasoning agent, `WebSearch` for the novelty and reference checks,
  `Read,Glob,Grep` for the ablation planner, `Read,Glob,Grep,Bash` for read-only agents, and
  `Bash,Read,Edit,Write,Glob,Grep` for coding and writer agents;
  - ⛔ WHY NOT read-only agents without `Bash`: an auditor ties a claim to the version that made
    it with `git log`, `git show` and `git diff`. The sandbox, not the tool list, stops the writes
    (section 5), so `Bash` adds reading and nothing else;
- reasoning agents: `--system-prompt <system.md>`, replacing Claude Code's own; coding agents:
  `--append-system-prompt <system.md>`, keeping Claude Code's tool instructions;
- coding agents: `--permission-mode bypassPermissions`, inside the sandbox (section 5);
- `--no-session-persistence`: the run directory keeps the record, not `~/.claude/projects`.

**Its environment is an allowlist,** built fresh: `HOME`, `USER`, `LOGNAME`, `SHELL`, `LANG`,
`TERM`, `TMPDIR`, and a `PATH` of the engine's own Python, `~/.local/bin` and the system
directories. Nothing else passes, so no `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL` or launching
session's variable can reach a call, and the call always runs on the subscription's login.

**Rate limits.** The subscription has usage windows. A call refused for usage raises
`RateLimited`; the runtime waits for the reset if it is within `max_wait_minutes`, else the run
stops as `paused`, and `resume` continues it later. No unit is lost, since none is half-written.

## 4. The stage primitive (analysis §3.4–3.5)

```python
def run_stage(candidate, p):                      # p: the stage's parameters, from data
    best, kept = candidate, candidate
    for refinements in range(p.limit + 1):        # A-TOP-2 reading 2: limit counts judged refinements
        verdict, feedback = p.critic(kept)
        outcome = p.verdict_map[verdict]          # accept | refine | reject
        if outcome == "accept":  return kept
        if outcome == "reject":  return None      # or the stage's reject branch
        if refinements == p.limit: break          # exhausted
        new = p.refine(kept, feedback)
        if p.guard and not p.guard(new, best):    # guarded update (ablation, meta)
            return p.on_guard_failure(best)
        kept = new; best = new if p.guard else best
    return p.on_exhaustion(kept, best)            # discard | keep_last | keep_best
```

Each stage's values are in `config/<profile>.json` under `stages`; the paper's values are
`config/paper.json` (App. A.2), with our decisions for what it leaves unset (section 8).

## 5. Integrity, enforced by the setup

The working rules of `CLAUDE.md`, made true by mechanism (`DEVELOPMENT_PROCESS.md`, probes of
2026-10-02):

- **Metrics come only from the harness.** Agent code writes predictions; the harness runs it, then
  scores the predictions with the task's own `metric.py` against labels the code cannot read.
- **Labels and the metric are unreachable.** The task's `harness/` directory is copied into the
  run once, hashed, and denied, for reading and writing, to every agent session and to every
  process the harness runs, by `sandbox-exec`. The hashes are re-checked before every evaluation.
- **Writes are confined.** A coding session may write only its workspace and temporary
  directories (and Claude's own state); the harness's evaluation process may write only its
  output directory, and has no network.
- **Every decision in the loop reads validation numbers** (the `subset` and `full` splits). The
  `test` split is scored once, at export, for the report; no agent sees it (U-TOP-5).
- **Gains are computed by code,** from the harness's result files. The guarded updates of §3.4
  and §3.6 ("strictly outperforms") are a numeric test: the new mean beats the best by more than
  `min_delta` (A-ABL-3).
- **The writer sees only verified results:** the results tables of the manuscript are generated
  by the engine from result files and `\input` by the drafter, who writes the prose.
- **The judge we report is not the reviewer we optimise against:** the in-loop reviewer and the
  final judge differ in prompt and model, and the final judge runs once, after the loop.
- **Auditors cannot write.** The specification filter and the method-code auditor run with the
  workspace read-only (A-INT-3); a fixer gets their report.

## 6. The task contract (U-TOP-1, A-TOP-4 reading 2)

```
tasks/<id>/
  task.json        manifest, below
  paper.md         G's paper: problem, method, reported results
  rules.md         what an idea may not change: data, protocol, metric; allowed packages; time
  code/            G's codebase, which implements the entrypoint
  data/public/     what the code may read for training
  harness/         LOCKED: split inputs, labels, metric.py; never copied into a workspace
  prepare.py       regenerates data/ and harness/ deterministically
```

`task.json`:

```json
{
  "id": "…", "title": "…",
  "paper": "paper.md", "rules": "rules.md", "code": "code", "public_data": "data/public",
  "entrypoint": "{python} run.py --train-dir {train_dir} --inputs {inputs} --out {out} --seed {seed}",
  "metric": {"name": "accuracy", "direction": "max", "module": "harness/metric.py"},
  "splits": {
    "subset": {"inputs": "harness/inputs/subset.npz", "labels": "harness/labels/subset.npz", "seeds": [0]},
    "full":   {"inputs": "harness/inputs/full.npz",   "labels": "harness/labels/full.npz",   "seeds": [0, 1, 2]},
    "test":   {"inputs": "harness/inputs/test.npz",   "labels": "harness/labels/test.npz",   "seeds": [0, 1, 2]}
  },
  "timeouts": {"evaluation_seconds": 600, "coding_session_seconds": 2400},
  "reported": {"text": "what G's paper reports, for the full-set critic's context"}
}
```

`metric.py` exposes `score(predictions_path, labels_path) -> {"primary": float, ...}`. The harness
copies a split's inputs to a fresh directory, runs the entrypoint once per seed in the sandbox,
and reports per-seed scores, their mean and standard deviation.

## 7. Agents (data in `scientisttwo/agents/`)

Each agent folder holds `agent.json` (kind, tools, paper reference), `system.md`, `prompt.md`
(with `{{variable}}` placeholders) and `schema.json`. An `IDEA` object is
`{title, summary, addresses: [limitation ids], method, implementation_plan: [steps],
expected_effect, risks}`.

| Agent | Paper | Kind, tools | Variables | Output |
|---|---|---|---|---|
| limitation_extractor | §3.1, P-ROSTER-1 | reasoning | task_title, paper, code_overview, rules, current_limitations, feedback | `{limitations: [{id, title, description, evidence}]}` |
| limitation_verifier | §3.1, P-ROSTER-2 | reasoning | task_title, paper, limitations | `{verdict: sufficient\|insufficient, feedback}` |
| initial_idea_generator | §3.1, P-ROSTER-3 | reasoning | task_title, paper, code_overview, rules, limitations | `{idea: IDEA}` |
| novelty_checker | §3.1, App. A.2, P-ROSTER-4 | reasoning, WebSearch | task_title, idea | `{references: [{title, url, relation}] (≤ 2), novelty_score: 1–10, rationale}` |
| idea_generator | §3.1, P-ROSTER-5 | reasoning | task_title, paper, code_overview, rules, limitations, pool | `{idea: IDEA}` |
| baseline_coder | §3.2, P-ROSTER-6 | coding | task_title, paper, rules, entrypoint | `{faithful, changes, notes}` |
| subset_coder | §3.2, P-ROSTER-7 | coding | task_title, rules, entrypoint, idea | `{summary, files_changed, self_checks, notes}` |
| subset_critic | §3.2, P-ROSTER-8 | reasoning | task_title, metric, idea, baseline_result, idea_result, gain, log_tail, diff_summary | `{verdict: Good\|Bad\|Engineer, feedback}` |
| subset_engineer | §3.2, P-ROSTER-9 | coding | task_title, rules, entrypoint, idea, feedback, idea_result, log_tail | `{idea: IDEA or null, summary, files_changed}` |
| full_set_coder | §3.2, P-ROSTER-10 | coding | task_title, rules, entrypoint, idea, subset_result | `{summary, files_changed, notes}` |
| full_set_critic | §3.2, P-ROSTER-11 | reasoning | task_title, metric, idea, baseline_result, idea_result, gain, reported, log_tail | `{verdict: Good\|Bad\|Engineer, feedback}` |
| full_set_engineer | §3.2, §3.4, §3.6, P-ROSTER-12 | coding | task_title, rules, entrypoint, idea, feedback, best_result | `{idea: IDEA, summary, files_changed}` |
| idea_evolver | §3.3, P-ROSTER-14 | reasoning | task_title, limitations, traces | `{idea: IDEA}` |
| selector | §3.3, P-ROSTER-15 | reasoning | task_title, metric, candidates | `{choice, rationale}` |
| ablation_planner | §3.4, P-ROSTER-16 | reasoning, Read/Glob/Grep | task_title, idea, best_result, n_plans, diff_summary | `{plans: [{id, component, change, hypothesis}]}` |
| ablation_coder | §3.4, P-ROSTER-17 | coding | task_title, rules, entrypoint, idea, plan | `{summary, files_changed, notes}` |
| ablation_critic | §3.4, P-ROSTER-18 | reasoning | task_title, metric, idea, best_result, baseline_result, gain, ablations, reject_share | `{verdict: Good\|Refine\|Reject, feedback}` |
| initial_drafter | §3.5, P-ROSTER-20 | writer | task_title, paper, idea, limitations, references, results_tex, results_json | `{title, abstract, notes}`, and `main.tex`, `references.bib` |
| peer_reviewer | §3.5, P-ROSTER-21 | reasoning | manuscript | `{summary, strengths, weaknesses, questions, score: 1–10, confidence: 1–5}` |
| rebuttal_planner | §3.5, P-ROSTER-22 | reasoning | task_title, idea, review, results_json, n_tasks | `{tasks: [{id, concern, experiment, expected_outcome}]}` |
| rebuttal_coder | §3.5, P-ROSTER-23 | coding | task_title, rules, entrypoint, idea, task | `{summary, files_changed, notes}` |
| paper_enhancer | §3.5, P-ROSTER-24 | writer | review, rebuttal_results_json, audit | `{changes, responses}` |
| meta_reviewer | §3.6, P-ROSTER-25 | reasoning | manuscript, review | `{decision: Accept\|Refine, feedback}` |
| spec_filter | §4.2, P-ROSTER-26 | read-only | task_title, rules, idea, diff | `{compliant, violations: [{rule, evidence}]}` |
| reference_checker | §4.2, P-ROSTER-27 | reasoning, WebSearch/WebFetch | bibliography | `{entries: [{key, status: verified\|not_found\|mismatch\|unchecked, evidence}]}` |
| method_code_auditor | §4.2, P-ROSTER-28 | read-only | manuscript, diff | `{consistent, issues: [{severity, claim, evidence}]}` |
| test_reporter | ours, U-TOP-5 | writer | task_title, metric, test_results, validation_results | `{changes, notes}` |
| final_judge | §4, held-out | reasoning | manuscript | `{score: 1–10, decision: accept\|reject, rationale}` |

The Result Comparison Agent (P-ROSTER-19) is a numeric test, not an agent (section 5, A-ABL-3).

## 8. Decisions on what the paper leaves open

| Gap | Decision | ⛔ WHY NOT |
|---|---|---|
| A-TOP-1, U-TOP-7 exhaustion | per stage, as data: limitations keep the last set; experiments discard (`Bad`); ablation and meta keep the best, through their guard; peer review keeps the last manuscript in `paper.json` (§3.5) | one rule for all: the text and Listing 1 disagree, stage by stage |
| A-TOP-2 counting | a limit counts judged refinements (N + 1 critic calls), except the limitation loop, which counts critic calls (16) | Listing 1's count everywhere: App. A.2 words three limits as refinements |
| A-TOP-3 loop until approval | export after N_meta = 1, marking whether the meta-reviewer accepted | looping until approval: App. A.2 caps it at one |
| U-TOP-1, A-TOP-4 what G is | section 6's task folder: a paper, a codebase, rules, a locked harness | a natural-language challenge: every experiment in the paper uses a paper and code |
| U-TOP-2 failures | retry transient errors twice; a failed experiment is a `failed` result the critic judges; a usage limit pauses the run | stopping the run on any error: a multi-day run must survive one bad call |
| U-TOP-4 parallelism | `parallel` workers, default 2 (a round's two candidates) | serial only: halves wall-clock time for nothing |
| U-TOP-5 splits, U-INT-4 harness | section 5 | the paper's practice: every decision reads the reported benchmark |
| A-CFG-1 routing | every coding agent on `opus` through Claude Code (reading 2); reasoning agents on `sonnet`; the final judge on `opus` with its own rubric | Gemini: the subscription runs Claude only; the author/judge family split of analysis §7.3 is lost, mitigated by numeric gates and a separate final judge |
| U-SEED-1 N_seed | 6 | none: the paper sets no value |
| A-EVO-1 N_0 | 2: App. A.2's "two candidates" per round | 1: leaves round 0 with one candidate |
| A-EVO-2, U-EVO-1 K, stop test | K = 4 rounds after round 0; the S test runs at the end of each round | a test after every idea: rounds are the unit App. A.2 counts |
| A-BASE-1 baseline | once per task, first, on `full` and `subset`; each idea starts from a copy | per idea: same code, same numbers, paid again |
| A-FULL-1 full-set reference | the reproduced baseline on `full`, with the paper's reported numbers as context | the reported number: another split, another run |
| A-FULL-2 full-set limit | 2, as the subset's | none: the paper sets no value |
| U-ABL-1 N_p | 5, the low end of Table 15's "5–6" | none |
| A-ABL-1 ablation reject | `Reject` ends the run with "no contribution" (App. B) | ignoring App. B: it reports this branch happening |
| A-ABL-2 failed comparison | go on to drafting (Figure 7) | — |
| U-PEER-1 N_t | 3 | none |
| P-ROSTER-45 PaperOrchestra | our drafter writes LaTeX; the engine supplies the results tables | PaperOrchestra itself: not available to us |
| P-ROSTER-46 ScholarPeer | our reviewer, scoring 1–10 against the threshold 8 (App. A.2) | ScholarPeer itself: not available; the threshold is its scale's (P-CFG-9) |
| U-TOP-5 the test split in the paper | after the one test evaluation, the test_reporter (writer) puts the test results into the text: abstract, results and limitations, as they came out | appending the table alone: run 1's final judge found the text saying "no test split" beside the test table; keeping the test out of the paper: a reader would see only validation numbers that the search selected on |
| P-ROSTER-47 Google Search | Claude Code's WebSearch tool, two papers per idea | an API key for a search engine |

## 9. The run directory

```
<run>/
  run.json          the task, profile, engine commit, CLI version, status, final branch
  harness/          the locked copy of the task's harness, with manifest.sha256
  units/<key>.json  one completed unit of work: inputs hash, output, cost, time
  transcripts/      each coding session's stream, for audit
  workspaces/<v>/   codebase versions, each a git repository
  results/          harness results, one JSON per evaluation
  ledger.jsonl      every unit: agent, model, seconds, equivalent cost or null
  paper/            the manuscript workspace
  export/           P+ (main.tex, main.pdf), C+ (the codebase), results.json, audit.json, report.md
```

A unit key names where in the flow a call sits, such as `evo/r1/i2/subset/critic/1`. `resume`
re-runs the orchestrator from the top; every completed unit returns from disk, so the run
continues exactly where it stopped.
