# The engine: components, contracts and decisions

**For** whoever builds, runs or extends the engine. It replicates ScientistTwo (arXiv:2609.19644)
as `docs/paper/analysis.md` describes it. Section numbers in brackets cite the paper; "analysis
§n" cites `docs/paper/analysis.md`; gap IDs (A-…, U-…) are rows of `docs/paper/unspecified.md`.

Set by Vlad on 2026-10-02: every agent runs through `claude -p` on his subscription, never the
API, and the engine is delivered without questions to him (`DEVELOPMENT_PROCESS.md`).

## 1. Shape

One run maps a task G to a paper and a codebase, (P+, C+) = A(G) [§3, Eq. 1]. The orchestrator is
analysis §4's control flow as plain Python. Every critic–refine loop is one parameterised **stage
primitive** (analysis §3.4–3.5) with its parameters in data: limitations, A_Coder's two levels,
ablation, peer review and meta-review. The seed pool and the evolution rounds have a different
shape (a scoring critic and a count stop, analysis §3.3) and are plain loops whose limits are
data. Every agent is a prompt, a schema and a route, in data. Everything the run produces is a
file in the run directory, so a crashed run resumes.

```
scientisttwo/                 the engine package (python -m scientisttwo)
  cli.py                      run | resume | status | agents
  orchestrator.py             scientist_two(G): analysis §4, stage by stage; prepare, lock, resume
  primitive.py                the stage primitive
  state.py                    Baseline, Trace, Core: the state between stages
  stages/                     one module per paper section
    limitations.py  coder.py  evolution.py  ablation.py  writing.py  meta.py  export.py
    shared.py                 steps several stages take: spec filter, A_FullEng, run_variants
    roles.py                  each critic's verdict map, checked against its schema at start
    manuscript.py  common.py  the manuscript's numbers and files; the run context
  runtime/                    agent runtime: spec, render, call, validate, memoise, account
    agents.py  store.py  budget.py  procs.py
    backends/                 __init__ (registry), base (Backend, SubprocessBackend), claude_cli, mock
  harness/                    the locked evaluation harness and everything that confines a process
    harness.py  sandbox.py  policies.py  egress.py  checks.py
  task.py  workspace.py  config.py
  agents/<agent>/             DATA: agent.json, system.md, prompt.md, schema.json (28 agents)
  config/                     DATA: profiles (paper.json, quick.json), routing.json
tasks/<task-id>/              a task G (section 6)
tests/                        mock mode: the whole engine for $0
playground/engine/            the probes, checkers and golden cases behind the claims here
```

## 2. Components and their contracts

| Component | Input | Output | Failure modes, and what happens |
|---|---|---|---|
| **Backend** (interface; registry in `backends/__init__.py`) | an `AgentCall`: system text, user text, output schema, model, effort, tools, working dir, sandbox policy, TMPDIR, timeout, attempt | an `AgentResult`: structured output, raw text, equivalent cost (or `None` = unknown), tokens, duration, session id | rate limit → `RateLimited(reset_at)`; transient → `TransientError`; timeout → `AgentTimeout`; invalid output → `InvalidOutput`; machine fault → `EnvironmentFault`; refusal → `AgentFailed` |
| `SubprocessBackend` (base) | a call and its argv | a started, watched, recorded process tree | refuses to start without a sandbox policy; kills the whole tree at the end of every call |
| `ClaudeCLIBackend` | as above | as above, from `claude -p --output-format stream-json` | see section 3 |
| `MockBackend` | as above | scripted outputs, keyed by agent and call index; coding mocks edit files | none: it is deterministic |
| **Agent runtime** | agent name, template variables, a unit key | the validated output | refuses undeclared variables; replays a finished unit only if its inputs hash matches; one ledger line per attempt; retries as section 3 says; records the unit and its prompt |
| **Run store** | unit key, inputs hash | a stored result, or nothing | a unit is written atomically (temp file, rename) only when it completes, so a crash leaves no half-unit; on resume, a completed unit is returned without a call: **a retry never spends twice** |
| **Budget guard** | each attempt's cost and time | continue, or `BudgetExceeded` (a `RunPaused`) | caps per run: attempts, coding sessions, hours of running time, equivalent USD, usage-window ceilings; an unknown cost counts as unknown, never zero; a torn last ledger line is repaired |
| **Task** | `tasks/<id>/task.json` | a validated `Task`, and the sha256 manifest of its harness | missing file or schema error → refuses to start |
| **Workspace** | a parent codebase version | a new version: a copy reset to its parent's commit, under git, so every change is a diff | a failed coding unit still leaves its version, marked failed, for the harness to judge; a git failure is the machine's (`WorkspaceError`), since agents cannot write `.git` |
| **Harness** (locked) | a codebase version, a split, seeds | metrics computed by the task's own metric on the code's predictions | crash, timeout or missing predictions → a `failed` result, with the log tail, that critics see; a changed harness file → `HarnessTampered`, the run stops |
| **Sandbox** and **policies** | a process kind and its directories | a `sandbox-exec` profile (section 5) | not macOS → refuses unless `--allow-unsandboxed` |
| **Egress proxy** | CONNECT requests from agents | a tunnel to an allowlisted host, or 403; every request logged | the only network path out of an agent's sandbox |
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
  `Read,Glob,Grep,Bash` for read-only agents (the specification filter, the method-code auditor
  and the ablation planner), and `Bash,Read,Edit,Write,Glob,Grep` for coding and writer agents;
  - ⛔ WHY NOT the ablation planner as a reasoning agent with `Read,Glob,Grep`: a reasoning agent's
    sandbox reads no version and runs in scratch, so the planner could not read the code its
    prompt sends it to, and planned from the diff summary alone (Codex review 2026-10-02, P2);
  - ⛔ WHY NOT read-only agents without `Bash`: an auditor ties a claim to the version that made
    it with `git log`, `git show` and `git diff`. The sandbox, not the tool list, stops the writes
    (section 5), so `Bash` adds reading and nothing else;
- reasoning agents: `--system-prompt <system.md>`, replacing Claude Code's own; coding agents:
  `--append-system-prompt <system.md>`, keeping Claude Code's tool instructions;
- coding agents: `--permission-mode bypassPermissions`, inside the sandbox (section 5);
- `--no-session-persistence`: the run directory keeps the record, not `~/.claude/projects`.

**Its environment is an allowlist,** built fresh: `HOME`, `USER`, `LOGNAME`, `SHELL`, `LANG`,
`TERM`, `PATH` (the engine's own Python, `~/.local/bin`, the system directories), the unit's own
`TMPDIR`, the egress proxy (`HTTPS_PROXY`, with `NO_PROXY` empty), and the engine's switches:
`CLAUDE_CODE_DISABLE_AUTO_MEMORY` (else the agent reads and writes the user's own memory folder),
`DISABLE_AUTOUPDATER` (else the binary can change under a running run),
`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`.
Nothing else passes, so no `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL` or launching session's
variable can reach a call, and the call always runs on the subscription's login. The CLI binary
is resolved once and pinned for the run (`run.json`); each resume records the version it ran.

- ⛔ WHY NOT a per-run `CLAUDE_CONFIG_DIR`: the subscription login is bound to the default one; a
  fresh directory answers "Not logged in" (probe of 2026-10-02).

**One call is one process tree.** `SubprocessBackend.spawn` applies the call's sandbox (it refuses
to start a process without one, unless the run was started with `--allow-unsandboxed`), puts the
process in its own session, marks its environment, and records it under `<run>/procs/`. A watcher
samples the tree every 0.25 s; at the end of every call, normal or not, every group seen in the
tree or found by the marker is killed (the agent's Bash tool starts its shell in a new session,
which the CLI's own group does not hold). The next `prepare` of the run kills what a crashed
engine left, matching each recorded group by its leader's start time.

**Errors are classified:** a usage window refused (`RateLimited`, with the reset of the window
actually spent), a transient error (retried twice with backoff, then the run pauses), an
invalid output (retried once with the error shown), a timeout (retried once from a clean start,
then the unit fails), a machine fault such as no space left (the run pauses), an argument the CLI
refuses before any session starts (the unit fails). A result already delivered is kept even if
the CLI then hangs.

**Rate limits.** The subscription has usage windows. A call refused for usage raises
`RateLimited`; the runtime waits for the reset if it is within `max_wait_minutes`, at most
`max_waits` times, else the run stops as `paused`, and `resume` continues it later. No unit is
lost, since none is half-written.

## 4. The stage primitive (analysis §3.4–3.5)

`scientisttwo/primitive.py`, as it runs:

```python
def run_stage(candidate, p):                      # p: the stage's parameters, from data
    best, calls, refinements = candidate, 0, 0
    loop:
        if p.counting == "critic_calls" and calls == p.limit: return exhausted(p, candidate, best)
        verdict, feedback = p.critic(candidate, calls); calls += 1
        outcome = p.verdict_map[verdict]          # accept | refine | reject (stages/roles.py)
        if outcome == "accept":  return candidate                       [accepted]
        if outcome == "reject":  return None                            [rejected]
        if p.counting == "refinements" and refinements == p.limit:
            return exhausted(p, candidate, best)                        [exhausted]
        new = p.refine(candidate, feedback, refinements); refinements += 1
        if p.guard:                                # guarded update (ablation, meta)
            if not p.guard(new, best): return best                      [guard_failed]
            best = new; if p.after_guard: new = best = p.after_guard(new, refinements)
        elif p.rank and p.rank(new) > p.rank(best): best = new          (peer review's keep_best)
        candidate = new

exhausted: discard → None | keep_last → candidate | keep_best → best   (keep_best needs a guard or a rank)
```

Every outcome also carries `last` (the last candidate judged) and `best`, so a caller never needs
a closure to learn what a rejected candidate was. A stage's settings are in
`config/<profile>.json` under `stages`, and `config.validate_profile` refuses any value the
stage's code cannot honour (`STAGE_RULES`): A_Coder's levels discard (§3.2), limitations keep the
last set, ablation and meta keep the best through their guard, peer review keeps the last or the
best-scored (U-TOP-7). The paper's values are `config/paper.json` (App. A.2), with our decisions
for what it leaves unset (section 8).

## 5. Integrity, enforced by the setup

The working rules of `CLAUDE.md`, made true by mechanism (`DEVELOPMENT_PROCESS.md`, probes and
reviews of 2026-10-02). Each process gets its sandbox from its KIND, in one place
(`harness/policies.py`):

| process | writes | reads under $HOME, beyond the backend's own files | network |
|---|---|---|---|
| reasoning agent | scratch, its TMPDIR | Python, the public data | the Anthropic API; any host, logged, with WebFetch |
| read-only agent | scratch, its TMPDIR | + the version it audits | the Anthropic API |
| coding / writer agent | its version, not its `.git`; its TMPDIR | Python, the public data | the Anthropic API, plus the task's `network_allow` |
| evaluated code | its seed's directory | the commit's files, the split's inputs, the public data, Python | none |
| LaTeX build | its build directory | the manuscript version | none |

- **Reads under $HOME are an allowlist.** The home directory holds every copy of every dataset
  (conda environments, package caches, other worktrees, other runs); a denylist cannot be
  complete. The integrity review read one of 9 un-denied copies of the digits data from inside
  the old evaluation sandbox and scored 1.0 on test. A task's `deny_patterns` hide a dataset's
  directory wherever it is, including inside the allowed Python prefix; such a deny names
  `file-read-data`, because a wildcard deny does not override a specific allow (probe).
- **Agents reach only the API.** The sandbox denies every outbound connection but one, to the
  run's egress proxy on 127.0.0.1, which tunnels only to allowlisted hosts and logs every request
  (`egress.jsonl`, summarised in the report). A coding agent with the open internet could fetch a
  public benchmark's labels and bake them into its code, which no check of a diff can reliably see.
- **The user's Claude setup is out of reach.** No agent may write `~/.claude`, `~/.claude.json`
  or `~/Library/Caches`: settings, hooks and `CLAUDE.md` written there would run, unsandboxed, in
  the user's own sessions; and `~/.claude` is not even readable (the CLI does not need it).
- **Metrics come only from the harness.** Agent code writes predictions; the harness runs it, then
  scores the predictions with the task's own `metric.py` against labels the code cannot read.
- **A version is its commit.** The harness evaluates an export of the version's commit, each seed
  in its own directory, so nothing written to a working tree after its commit, and nothing one
  seed leaves, reaches a result. A copy for the next version is reset to its parent's commit.
- **Labels and the metric are unreachable,** and hashed: the task's `harness/` is copied into the
  run once, denied to every process, and re-checked before every evaluation.
- **The baseline is the paper's.** The reproduced baseline must score the task's reported number
  within its tolerance (`baseline_check`, U-BASE-2), or the run ends `baseline_failed`: every gain
  is measured against it, and a weaker baseline would inflate them all.
- **Every decision in the loop reads validation numbers** (the `subset` and `full` splits). The
  `test` split is scored once, at export, after every decision is frozen: the baseline, the
  proposed method and each final ablation or supplementary variant (U-TOP-5). Only two agents read
  test numbers, after that: the test_reporter, which writes them into the text, and the final
  judge; nothing either produces feeds back into a decision.
- **Gains are computed by code,** from the harness's result files. The guarded updates of §3.4
  and §3.6 ("strictly outperforms") are a numeric test: the new mean beats the best by more than
  `min_delta` (A-ABL-3); the critics read the same margin in their gain text.
- **The writer sees only verified results,** and no reader trusts a writer's copy of them: the
  tables are generated by the engine from result files, and every reviewer, the auditor, the
  final judge and the PDF build read them regenerated. An edited copy, or a number in the prose
  that no result holds, is an audit finding.
- **The judge we report is not the reviewer we optimise against:** the in-loop reviewer and the
  final judge differ in prompt and model, and the final judge runs once, after the loop.
- **Auditors cannot write.** The specification filter and the method-code auditor are read-only
  agents (A-INT-3): their sandbox follows their kind, and a fixer gets their report. The ablation
  planner is read-only for the same reason: it reads the selected version to find each component,
  and can never change it.

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
    "test":   {"inputs": "harness/inputs/test.npz",   "labels": "harness/labels/test.npz",   "seeds": [100, 101, 102]}
  },
  "timeouts": {"evaluation_seconds": 600, "coding_session_seconds": 2400},
  "reported": {"text": "what G's paper reports, for the full-set critic's context"}
}
```

`metric.py` exposes `score(predictions_path, labels_path) -> {"primary": float, ...}`. The harness
copies a split's inputs to a fresh directory, runs the entrypoint once per seed in the sandbox,
and reports per-seed scores, their mean and standard deviation.

- **A test seed is never a search seed** (`load_task` refuses it; task 6, blocker B1). With shared
  seeds a deterministic entrypoint trains the same model for validation and test, so the test
  number keeps the training-seed luck that selection exploited. The null control of task 6
  (rerun 2026-10-02): at equal training and evaluation noise, the winner of 20 null candidates
  keeps +1.32 of its +2.65 validation gain on test with shared seeds, and about 0 without.
- **A run pins its task settings.** `run.json` holds the `task.json` the run started with, and a
  resume uses it. A changed `task.json` stops the resume unless `--allow-changed`, which records
  the changed keys (Codex review 2026-10-02, P1: a resume mixed `full` seeds `[0, 1]` and `[7, 8]`).

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
| ablation_planner | §3.4, P-ROSTER-16 | read-only | task_title, idea, best_result, n_plans, diff_summary | `{plans: [{id, component, change, hypothesis}]}` |
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
| U-BASE-2 baseline fails | a baseline that does not run, or misses the task's `baseline_check`, ends the run `baseline_failed` | judging ideas against a broken or weaker baseline: every gain would be measured from the wrong floor |
| U-INT-3 audit after review | the audit and its repair run after the review loop; the repaired manuscript goes to the meta-reviewer and the final judge, not back to the in-loop reviewer | a review round per repair: the repair edits only citations and method descriptions, and costs a rebuttal cycle per pass |
| U-INT-1 spec filter scope | the LLM specification filter judges each Good idea and each admitted refinement; ablation and supplementary variants are not filtered by it, but every evaluated version passes the deterministic checks and the sandbox | an LLM filter on every variant: a variant is never exported as the method, and the sandbox already bounds what its code can read |
| U-ABL-3, U-PEER-2 variants | each final ablation and supplementary variant ships as a patch against C+ (`export/variants/`), and is scored on test once at export | shipping C+ alone: the paper's tables could not be reproduced from the export |
| §3.3 one Good idea | with a single Good idea the Selector is not called; a choice that names no candidate falls back to the largest validated gain, recorded in the event | calling the Selector on one candidate, or failing the run on an invented id |
| A-ABL-1 on a restarted pass | an ablation `Reject` after the meta restart ends only the restart: the previous pass, whose ablation was accepted, is exported (`meta_status: restart_rejected`) | ending the run: it would discard a pass the critic had accepted |
| P-ABL-7 attribution | the ablation critic reads the baseline and the gain over it, and rejects when a variant without the idea's own mechanism keeps more than `reject_share` (0.5) of the gain: App. B's "primarily driven by general training controls" | judging components only against the full method: run 1's critic accepted an idea whose gain was 84% input standardisation |
| §3.6 guard and validation tuning | a meta refinement that removes validation tuning (for example, constants chosen by cross-validation inside the training split) will usually score lower on validation, so the strictly-better guard refuses it; this is the paper's rule, kept, and the report states it | relaxing the guard: it is the paper's mechanism, and its cost is visible in the run record |
| P-ROSTER-47 Google Search | Claude Code's WebSearch tool, two papers per idea (P-CFG-2: fixed in the novelty checker's schema, `maxItems: 2`, not a profile limit) | an API key for a search engine |

## 9. The run directory

```
<run>/
  run.json             the task, profile, routing, backend (pinned CLI binary), engine commit,
                       agents hash, the pinned task.json, status, and a history entry per start,
                       resume and status (`crashed` when an engine died without one)
  heartbeat            the last time the engine was alive, every 30 s while it runs
  run.lock             held by the one engine process driving the run
  agents/              the run's own copy of every agent's prompt and schema; a resume uses it
  .locked-harness/     the locked copy of the task's harness, with its manifest (denied to all)
  public_data/         the training data agents and evaluated code may read
  units/<key>.json     one finished unit: its inputs hash, output, attempts, cost, time
  prompts/<key>.json   what that unit's agent was asked, in full
  transcripts/<key>[.attemptN].jsonl   each attempt's CLI stream; N runs on across resumes
  workspaces/<v>/      codebase versions, each a git repository; a version is its commit
  manuscripts/<v>/     manuscript versions, the same way
  results/<key>.json   the harness's results, one per evaluation, with the commit it scored
  evals/<key>/         an evaluation's export of the commit, inputs, and one directory per seed
  ledger.jsonl         an `attempt_started` line before each call, then one line per ATTEMPT:
                       agent, outcome, model, seconds, equivalent cost or null; an attempt an
                       engine's death cut off is counted on the next start as `interrupted`
  egress.jsonl         every network request the agents made through the proxy, allowed or refused
  events.jsonl         the run's narrative, one event per line
  procs/               the live process trees of this engine, each process by pid and start
                       time, with the unit's marker, so a crash leaves a record to reap
  builds/<v>/          a version's PDF build: its commit exported, the engine's tables over the
                       version's own, compiled there (bibtex writes beside its sources)
  tmp/<key>/           each unit's own TMPDIR
  export/              P+ (paper/), C+ (code/), changes.patch, variants/, results.json,
                       audit.json, report.md
```

A unit key names where in the flow a call sits, such as `evo/r1/e1/subset/critic/1`. `resume`
re-runs the orchestrator from the top; every finished unit returns from disk once its inputs hash
matches, so the run continues exactly where it stopped. A unit whose inputs changed (new engine
code, an edited copy of a prompt) stops the resume, unless `--allow-changed` replays it as
recorded. A unit failure that stopped the run is cleared, so the resume tries it again.
