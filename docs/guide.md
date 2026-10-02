# Using the engine

**For** whoever runs the engine on their own Claude subscription (Vlad first) or adds a task to
it. The design and its reasons are in [architecture/engine.md](architecture/engine.md); this guide
says how to use it, and what to do when something goes wrong.

Every command below was checked against [`scientisttwo/cli.py`](../scientisttwo/cli.py), or run
on the mock backend, on 2026-10-02.

## In thirty seconds

```sh
python3 -m scientisttwo run --task tasks/digits --profile quick --wait   # in tmux (section 3)
python3 -m scientisttwo status <run-dir>                                  # from another terminal
python3 -m scientisttwo resume <run-dir> --wait                           # after a stop
```

Then read `<run-dir>/export/report.md`.

**Where it stands (2026-10-02).** Three `quick` runs on the demo task have finished `done` on the
subscription, in `runs/digits-quick-{1,2,3}` (local, not committed). Run 2 paused on a usage window
and was resumed; run 3 ran from scratch on `f470f27`. Three changes this guide covers came after
run 3 and have run only on the mock backend: `--wait`, the fallback to a newer `claude` binary, and
the wider inputs hash. The `paper` profile has never run end to end. The HANDOFF in
[DEVELOPMENT_PROCESS.md](../DEVELOPMENT_PROCESS.md) says what is merged and reviewed.

## 1. What it does

A run takes a task (a paper, its code, its rules and a locked evaluation harness) and returns an
improved codebase and a paper about the improvement, as ScientistTwo does [§3, Eq. 1]. It finds
the paper's limitations, proposes ideas, reproduces the baseline, codes and tests each idea, picks
one, ablates it, writes and reviews a paper, audits it, scores everything once on a held-out test
split and exports the result. Every agent is one `claude -p` process on your subscription.

Where each stage lives, and the unit keys it leaves in a run directory (the keys are how you find
a stage's files under `units/`, `prompts/`, `transcripts/` and `results/`):

| Paper | Stage | Module | Unit keys |
|---|---|---|---|
| §3.1 | limitations, seed ideas, novelty | [`stages/limitations.py`](../scientisttwo/stages/limitations.py) | `lim/…`, `seeds/<i>/…` |
| §3.2 | reproduce the baseline | [`stages/coder.py`](../scientisttwo/stages/coder.py) | `base/…` |
| §3.2–3.3 | code and judge ideas on `subset`, then `full`; evolve; select | `stages/coder.py`, [`stages/evolution.py`](../scientisttwo/stages/evolution.py) | `evo/r<k>/<idea>/…`, `select` |
| §3.4 | ablation | [`stages/ablation.py`](../scientisttwo/stages/ablation.py) | `abl/p<n>/…` |
| §3.5, §4.2 | draft, peer review, rebuttal; reference and method–code audit | [`stages/writing.py`](../scientisttwo/stages/writing.py) | `write/p<n>/…`, `audit/p<n>/…` |
| §3.6 | meta-review | [`stages/meta.py`](../scientisttwo/stages/meta.py) | `meta/…` |
| ours (U-TOP-5) | test split once, test report, final judge | [`stages/export.py`](../scientisttwo/stages/export.py) | `export/…` |

The control flow is the docstring of [`orchestrator.py`](../scientisttwo/orchestrator.py). The
components, the agent roster and every decision on what the paper leaves open are in
[engine.md](architecture/engine.md) §2, §7 and §8.

## 2. Before the first run

| You need | Why | Check |
|---|---|---|
| macOS with `sandbox-exec` | every agent and every evaluation runs in a `sandbox-exec` profile; without it the engine refuses to start any process | `which sandbox-exec` |
| the `claude` CLI, logged in to your subscription | every agent is `claude -p`; the login is read from the default config and the macOS keychain | `claude --version`; log in once with `claude` |
| Python 3 with `numpy` and `jsonschema` | the engine; without `jsonschema` it skips its own schema check (the CLI still validates) | `python3 -c "import numpy, jsonschema"` |
| the task's own packages, **in the same Python** | evaluated code runs on the engine's interpreter, with no network, so nothing can be installed during a run. Digits needs `numpy` and `scikit-learn` ([`code/requirements.txt`](../tasks/digits/code/requirements.txt)) | `python3 -c "import sklearn"` |
| `latexmk` (optional) | the PDF; without it the run still finishes, with `pdf: false` | `which latexmk` |
| `pytest` (optional) | the test suite | |

Tested on 2026-10-02 with Python 3.13.5, numpy 2.2.6, jsonschema 4.25.1, scikit-learn 1.7.1 and
claude 2.1.287.

The digits data is not in git. The first run generates it with
[`tasks/digits/prepare.py`](../tasks/digits/prepare.py) (scikit-learn's bundled copy, no network).

**Check the install for $0** before you spend a usage window:

```sh
python3 -m pytest -q tests        # all must pass: 123, in about 4 min, on 2026-10-02
python3 -m scientisttwo run --task tasks/digits --backend mock --run-dir /tmp/st2-mock
```

The mock run takes about a minute. It runs the whole pipeline, the sandbox, the harness and the
PDF build, with scripted agents: it should end `"status": "done"` with gains of 0.0.

**How the engine refuses the API.** Three independent layers, all in the backend:

1. The child process gets an allowlisted environment, so `ANTHROPIC_API_KEY` and
   `ANTHROPIC_BASE_URL` never reach it ([`child_env`](../scientisttwo/harness/sandbox.py#L161-L174)).
2. It never passes `--bare`, under which auth is "strictly ANTHROPIC_API_KEY"; `--setting-sources ""`
   loads none of your settings files, where an `apiKeyHelper` would live ([`claude_cli.py`](../scientisttwo/runtime/backends/claude_cli.py#L17-L19), [argv](../scientisttwo/runtime/backends/claude_cli.py#L97-L112)).
3. At the stream's first event, `apiKeySource` must be `"none"`. Anything else kills the call
   before the model is asked anything, and the unit fails with "the CLI would bill the API"
   ([lines 174–178](../scientisttwo/runtime/backends/claude_cli.py#L174-L178), [214–216](../scientisttwo/runtime/backends/claude_cli.py#L214-L216)).

To confirm a run billed nothing, every ledger line records the source:

```sh
grep -o '"api_key_source": [^,}]*' <run-dir>/ledger.jsonl | sort | uniq -c
#   36 "api_key_source": "none"            (run 3)
```

## 3. Running

### Commands

| Command | What it does |
|---|---|
| `run --task <dir>` | start a run |
| `resume <run-dir>` | continue a stopped run; finished units are not re-run |
| `status <run-dir>` | print `run_id`, `status`, `reason`, `resume_after`, `final`, `budget`, then the last 12 events. Reads files only: safe while a run is live |
| `agents` | list the 28 agents, their kind and paper reference, with the models of the **`paper`** profile (not `quick`'s) |

Flags of `run`:

| Flag | Default | Meaning |
|---|---|---|
| `--task <dir>` | required | a task folder (section 7) |
| `--profile <name or file.json>` | `quick` | a name in [`scientisttwo/config/`](../scientisttwo/config/), or a path to your own JSON (it may `"extends": "paper"`) |
| `--run-dir <dir>` | `runs/<task>-<YYYYmmdd-HHMMSS>` | where the run lives; `runs/` is git-ignored. **A directory that already holds a run is resumed, silently, with its recorded task and profile: your `--task`, `--profile` and `--set` are ignored** (checked on the mock backend) |
| `--set key.path=value` | | override one profile value, repeatable; the value is parsed as JSON. An unknown top-level key, limit, stage setting or budget cap is refused |
| `--parallel N` | profile's (2) | workers for a round's ideas |
| `--wait`, `--max-wait-hours H` | off, 24 | sleep through usage-window pauses (below) |
| `--backend claude\|mock`, `--mock-script <rules.json>` | `claude` | `mock` runs scripted agents for $0 |
| `--allow-unsandboxed` | off | run without `sandbox-exec`. **Removes every integrity guarantee in section 6.** For tests on a machine without it, never for a result |

`resume` takes `--allow-changed` (section 4), `--wait`, `--max-wait-hours`, `--backend` and
`--mock-script`. It reads everything else (task, profile, routing, sandbox setting) from the run's
own `run.json`; there is no way to change the profile on resume from the command line.

### What it prints

One line per event on stderr as the run goes (the same events land in `events.jsonl`), then the
run's `status`, `reason`, `resume_after` and `final` as JSON on stdout. Run 2's first start,
abridged:

```
run directory: <run-dir>
15:11:43 run                    status=running task=digits profile=quick
15:13:20 limitations            status=accepted n=6 critic_calls=2
15:16:19 baseline_check         split=full mean=0.9117920148560817 expected=0.9118 tolerance=0.02 ok=True
15:20:02 idea                   id=s3 verdict=Good level=full gain=+0.0594
15:21:38 selected               id=s3 gain=0.0594243268337975 why=Gains: s1 is +0.0613 ...
15:22:24 paused                 reason=subscription five_hour window at 99% (ceiling 98%)
{
 "status": "paused",
 "reason": "subscription five_hour window at 99% (ceiling 98%)",
 "resume_after": 1790942400.0,
 "final": null
}
```

The exit code is `0` for `done`, `no_success` and `ablation_rejected`; `3` for `paused`; `1` for
everything else, including `baseline_failed`, `error` and "not resumed".

### Long runs: tmux and `--wait`

A run spends your five-hour usage window and pauses before it runs out (below). With `--wait`, a
run that pauses on a usage window sleeps until the window resets, plus two minutes, then resumes
itself, until the run ends ([`wait_and_resume`](../scientisttwo/cli.py#L108)). It still stops when
the pause has no known reset (a budget cap, persisting errors, a machine fault) or the reset is
more than `--max-wait-hours` away. The process must stay alive for this, so start it in tmux:

```sh
mkdir -p runs
tmux new -s st2 'python3 -m scientisttwo run --task tasks/digits --profile quick --wait 2>&1 | tee runs/st2.log'
```

Detach with `Ctrl-b d`; `tmux attach -t st2` brings it back.

While it sleeps, `status` shows `paused`, and the run's lock is released. If you `resume` the run
by hand meanwhile, stop the sleeping process first (Ctrl-C in its tmux window): otherwise it wakes
into a lock someone else holds, prints `not resumed after the wait: …` and stops.

### Profiles: `quick` and `paper`

[`paper.json`](../scientisttwo/config/paper.json) is the paper's configuration (App. A.2), with
our values where it sets none. [`quick.json`](../scientisttwo/config/quick.json) extends it: every
stage and branch, small loops (3 seed ideas, 1 round, stop at the first Good idea, 2 ablation
plans, 1 rebuttal task). It is for demos and smoke tests, not results. The JSON files are the full
list; the differences that matter for planning:

| | `quick` | `paper` |
|---|---|---|
| models | every session `sonnet`; the final judge `opus` | reasoning `sonnet`; coding, writing and auditing `opus`; final judge `opus` |
| caps: agent calls / tool sessions / running hours | 150 / 40 / 12 | 800 / 200 / 96 |
| usage-window ceilings: five-hour / seven-day | 0.98 / 0.95 | 0.98 / 0.95 |
| a refused call is waited out in-process for at most | 60 min, 3 times | 300 min, 3 times |
| what a real run cost | run 3: 36 calls, 0.31 h, $2.85 API-equivalent; run 2: 42 calls, 0.31 h running, $3.42. Nothing billed | never run |

How the guard reads these ([`budget.py`](../scientisttwo/runtime/budget.py#L171-L216)):

- **Caps** count every attempt, retries and failures included. Hours are *running* hours: time
  paused or crashed does not count. `max_equiv_usd` is off (`null`); the dollar figure is what the
  CLI reports as API-equivalent, and the subscription bills nothing per call.
- **Ceilings** pause the run once a call reports a window at or above its ceiling, with
  `resume_after` set to that window's reset. In run 2 this, not a refused call, stopped the run:
  the ceiling tripped at 99%, and no call was ever refused.
- **The windows are shared with your own Claude use.** Run 2 started with the five-hour window at
  91%, spent by other sessions, and paused at 99% eleven minutes later. To leave yourself room,
  start the run with a lower ceiling, for example `--set budget.max_five_hour_utilization=0.8`.
- A seven-day window at 95% pauses the run until the weekly reset, usually days away, so `--wait`
  will not wait for it (24 h limit).

## 4. Pauses, crashes and resume

### Statuses

| `status` | Meaning | Resume? |
|---|---|---|
| `running` | an engine is driving it, **or** an engine died and nobody has resumed yet | see "status says running" (section 8) |
| `paused` | stopped on purpose: a usage window, a cap, persisting transient errors, a machine fault | yes |
| `error` | stopped on a unit failure no stage absorbs, or on `InputsChanged`, `HarnessTampered` or `StaleResult`; `reason` says which | yes, after fixing the cause |
| `done` | exported | |
| `no_success` | no idea was judged Good | no: it is an outcome |
| `ablation_rejected` | the ablation critic attributed the gain to generic training changes (App. B) | no: it is an outcome |
| `baseline_failed` | the reproduced baseline did not run, or missed the task's number | no: start a new run once fixed (section 8) |

`crashed` never appears as the current status after a resume; it is a `run.json` history entry.
A resume that finds `running` with the lock free writes `crashed`, timed at the dead engine's last
heartbeat (written every 30 s), so the downtime is not counted as running time
([`_close_crash`](../scientisttwo/orchestrator.py#L257)). A Ctrl-C ends the same way.

### A pause, as run 2 had it

Run 2 paused at 15:22 local, eleven minutes in (the output in section 3). `resume_after` is a Unix
time: `date -r 1790942400` prints `Fri Oct 2 16:00:00 +04 2026`, the window's reset. Run 2 was
resumed by hand at 16:33 and finished at 16:41. With `--wait` it would have resumed at 16:02.

### What a resume does

`resume` runs the pipeline again from the top. Every finished unit returns from disk, without a
call, once its inputs hash matches. In run 2's `events.jsonl`, the whole first half (limitations,
seeds, baseline, both ideas, selection) replays within 0.3 s of the resume, and the first new call
is the ablation critic. A unit that stopped the run is cleared, so the resume tries it again.

### `--allow-changed`

A resume refuses two kinds of change. The flag means something different for each:

| What changed | Without the flag | With `--allow-changed` |
|---|---|---|
| the task's `task.json` (seeds, timeouts, checks, deny lists) | `not resumed: the task's settings changed since this run started (timeouts). Start a new run, or resume with --allow-changed to use the new ones.` Exit 1, nothing runs | the **new** settings are used, and `run.json` history records `task_changed` with the keys |
| a finished unit's inputs: its prompt, output schema, kind, tools, variables, or its route's model, effort or backend | status `error`, reason `InputsChanged: lim/verify/0: this unit's inputs changed since it ran …` | the unit's **recorded** output is replayed; nothing is re-asked. An event `replayed_changed_inputs` records it |

The second case does not come from editing `scientisttwo/agents/`: a run keeps its own copy of
every prompt and schema in `<run-dir>/agents/` and uses only that. It comes from a new engine
version that sends an agent different variables or hashes its inputs differently, or from editing
the run's copy. (The `--backend` flag is not part of it; the route's `backend` key in
`routing.json` is.) Pulling new engine code between a pause and a resume is the realistic cause.
One such change is known: the inputs hash took in the schema, kind and tools after run 3, so a run
made before it (runs 1–3) resumes only with `--allow-changed` (checked on a copy of run 3).

Use the flag only when you know what changed. A changed `task.json` mid-run mixes two evaluation
protocols in one result: that is why the run pins it.

### Raising a cap on a paused run

A cap pause has no reset time, and resuming hits the same cap again. Raise the cap as you resume:

```sh
python3 -m scientisttwo resume <run-dir> --set budget.max_agent_calls=300
```

`resume --set` accepts only `budget.*` keys (a limit or a stage setting changed mid-run would mix
two protocols in one run). The change is validated and recorded in the run's history as a
`budget_changed` entry, with the caps before and after.

## 5. Reading a finished run

Open these in order.

**1. `export/report.md`**, one page. Run 3's, abridged:

```
## Results (computed by the locked harness)

| Split | Baseline (reproduced) | Proposed | Gain (higher is better) |
|---|---|---|---|
| validation (`full`) | 0.9118 ± 0.0170 | 0.9675 ± 0.0064 | 0.0557 |
| test, evaluated once at export | 0.9103 ± 0.0101 | 0.9568 ± 0.0092 | 0.0465 |

| Variant | Test |
|---|---|
| A1: Contrast-direction prototype init (INIT_CONTRAST) | 0.9460 ± 0.0089 |
| A2: Cosine-margin head (HEAD='cosface') | 0.9632 ± 0.0049 |
| S1: Build one variant in the same torch loop with both components off: INIT_CONTRAST=False and HEAD='sof | 0.9139 ± 0.0146 |

## Decisions
- Ablation critic: guard_failed.
- In-loop review score: 3 (threshold 8).
- Meta-review: guard_failed; it accepted the exported manuscript: False.
- Final judge (held-out, read once): 4 / 10, reject
```

How to read it:

- **The test row is the result.** Validation numbers are what the search selected on. Test seeds
  (100–109) are disjoint from search seeds (0–2).
- **An ablation's label names the component it removes.** Removing the init (A1) costs 0.011 on
  test, so the init carries the gain. Removing the cosine head (A2) *gains* 0.006, so the head
  hurts. S1, both off, scores 0.9139, the baseline's level. A paper true to these numbers would
  drop the head.
- **`guard_failed`** means a refinement was tried and did not beat the best version by more than
  the task's `min_delta`, so the best was kept. Run 3's meta refinement gained 0.0074 on
  validation, under digits' 0.02. It is the paper's rule, not an error.
- **"Ideas tried"** can list an idea with a larger validation gain than the chosen one. The
  Selector chooses, not the maximum: in run 2 it picked s3 (+0.0594) over s1 (+0.0613), because
  the difference was smaller than either's seed spread (`selected` event in `events.jsonl`).
- **Low review scores are normal, and worth reading.** The judge gave runs 2 and 3 each 4/10, for
  the reasons above: a component the numbers do not support, and a weak baseline with no stronger
  comparison. The rationale is in `results.json` under `final_judge`.

Runs 1 and 2 predate fixes that change their records: run 2's report says 40 calls where its
`run.json` says 42 (C14), its finished `run.json` still shows its old pause `reason` (R6), and its
PDFs all failed (R5). Run 3 has none of these.

**2. `export/results.json`**: every number in the report, with per-seed scores, the commit each
result scored, the review, the ablations, the rebuttal experiments, the final judge, the budget
and the egress summary. The `pdf` field says whether the engine's own build succeeded.

**3. `export/audit.json`**: the reference check (each entry `verified`, `not_found`, `mismatch` or
`unchecked`), the method–code audit and whether it was repaired, and `final_checks`: numbers in
the prose that no result holds, and whether a writer edited the engine's tables.

**4. `export/paper/`**: `main.tex`, `references.bib`, `results.tex` (the engine's tables) and
`main.pdf`, which is the engine's own build. The export has no `main.pdf` when that build failed
(`"pdf": false`): a writer's own compiled copy never reaches it. Run 2, from before this rule, has
one beside `"pdf": false`; do not trust it.

**5. The code.** `export/code/` is the final codebase (C+). `changes.patch` is C+ against the
reproduced baseline. `variants/<id>.patch` turns C+ into each ablation (`A…`) or rebuttal
experiment (`S…`). Both apply with `git apply` (checked on run 2).

The rest of the run directory is the full record. Its layout is
[engine.md §9](architecture/engine.md#9-the-run-directory). The files you will open most:

| File | For |
|---|---|
| `events.jsonl` | the story of the run, one event per line |
| `ledger.jsonl` | one line per agent attempt: outcome, model, seconds, cost, auth source, usage windows |
| `results/<key>.json` | one evaluation: per-seed scores, the commit, and `log_tail` when it failed |
| `units/<key>.json`, `prompts/<key>.json`, `transcripts/<key>.jsonl` | what an agent answered, what it was asked, and its full session |
| `workspaces/<version>/` | each codebase version as a git repository: `git -C <run-dir>/workspaces/s3.full0 log -p` |

## 6. What it guarantees, and what it does not

Each guarantee is made by a mechanism, not by a prompt. The reasons are in
[engine.md §5](architecture/engine.md#5-integrity-enforced-by-the-setup).

| You can trust | Because | Check it in a run |
|---|---|---|
| every metric came from the task's own `metric.py` | agent code writes predictions only; the harness scores them against labels no process can read | `results/<key>.json` |
| the labels and the metric were not touched | the task's `harness/` is copied into the run, denied to every process, and re-hashed before every evaluation; a change stops the run (`HarnessTampered`) | `.locked-harness/` and its manifest |
| a result belongs to a commit | the harness evaluates an export of the version's commit, each seed in its own directory | `commit` in each result |
| the test split was read once, after every decision | it is scored only in `export/`; its seeds are disjoint from search seeds (`load_task` refuses shared ones) | `export/test/…` keys; `test_set` event |
| the baseline is the paper's | the reproduced baseline must hit the task's `baseline_check`, or the run ends `baseline_failed` | `baseline_check` event |
| gains are arithmetic | computed from result files; "strictly better" is a numeric test against `min_delta` | `results.json` |
| readers saw the true tables | every reviewer, the auditor, the judge and the PDF get tables regenerated from result files; numbers in prose that no result holds are listed | `audit.json` `final_checks` |
| the judge was not the optimised reviewer | a different prompt and model, run once after the loop | `export/final_judge` unit |
| agents reached only the API (plus logged web search) | a sandbox that allows one outbound connection, to the run's proxy, which logs every request | `egress.jsonl`; "Network" in the report |
| nothing was billed | section 2 | `api_key_source` in `ledger.jsonl` |

What it does **not** guarantee:

- **macOS only.** The sandbox is `sandbox-exec`, which Apple marks deprecated. With
  `--allow-unsandboxed` none of the table above holds.
- **The test split is once per run, not once per task.** If you run a task ten times and report
  the best run, the test split has become a validation split. The engine cannot see that.
- **Web access by search agents is logged, not blocked.** The novelty and reference checkers reach
  any host through the open proxy; run 2's reached `arxiv.org` and two other sites.
- **Diff checks are tripwires.** `forbidden_in_diff` catches the obvious routes (a dataset loader,
  a URL); the read allowlist and the proxy are what actually keep the labels out.
- **Evaluated code has a timeout, not resource limits.** CPU and memory are not capped.
- **Author and judge are both Claude.** The paper splits families (Gemini reasoning, Claude
  coding); on the subscription the engine cannot. Numeric gates and a separate final judge are
  the mitigation (engine.md §8, A-CFG-1).
- **A `quick` run is a smoke test.** Three seeds on `full`, one round, small loops: its gains are
  one sample, not a finding.
- **Non-numeric claims** in the paper are checked only by the method–code auditor, an LLM.

## 7. Adding a task

A task is a folder: the contract is [engine.md §6](architecture/engine.md#6-the-task-contract-u-top-1-a-top-4-reading-2),
and [`load_task`](../scientisttwo/task.py#L91-L166) enforces it. It refuses to start when:

- a required key is missing, or the entrypoint lacks any of `{python}`, `{train_dir}`, `{inputs}`,
  `{out}`, `{seed}`;
- `metric.direction` is not `max` or `min`;
- a split (`subset`, `full`, `test`) is missing, or its inputs or labels are absent or outside
  `harness/`; the metric module is outside `harness/`;
- `paper`, `rules` or the metric module is missing, or `code` or `public_data` is not a folder;
- a test seed is also a `subset` or `full` seed;
- `baseline_check` names `test`, or lacks a numeric `expected` and `tolerance`.

[`tasks/digits/`](../tasks/digits/) is the worked example. Its
[`task.json`](../tasks/digits/task.json) uses every optional key, and its `integrity_notes` field
says why each value is what it is. The optional keys:

| Key | What it does | Digits |
|---|---|---|
| `prepare` | command run once if any data file is missing | `{python} prepare.py` |
| `timeouts` | `evaluation_seconds` (per seed), `coding_session_seconds` | 120, 2400 |
| `reported` | the paper's numbers, as text, for the full-set critic | the released code's scores |
| `baseline_check` | `{split, expected, tolerance}` the reproduced baseline must hit | `full`, 0.9118, 0.02 |
| `min_delta` | the noise floor a gain must exceed to count as "strictly better" | 0.02, about 2 standard errors |
| `deny_patterns` | path regexes no process may read, anywhere | every copy of sklearn's bundled data |
| `deny_read` | extra paths no process may read; `{site_packages}` expands | the engine's own sklearn data |
| `forbidden_in_diff` | strings a change may not add | `load_digits`, `urllib`, `https://`, … |
| `allow_data_files` | may a change add a data file | `false` |
| `network_allow` | hosts coding agents may reach beyond the API | none |

Steps:

1. **Build the folder:** `code/` with the entrypoint, `paper.md`, `rules.md` (what an idea may not
   change), `data/public/` (what training may read), `harness/` with each split's inputs and
   labels and `metric.py` exposing `score(predictions_path, labels_path) -> {"primary": float, ...}`.
   Keep generated data out of git, as digits does, and regenerate it with `prepare`.
2. **Find every other copy of the evaluation data** your Python can read (bundled datasets, caches,
   conda environments) and deny it with `deny_patterns`. The integrity review found 9 copies of
   the digits data under one home directory, read one from inside the old sandbox, and scored 1.0
   on test.
3. **Measure the baseline for $0.** Leave out `baseline_check` and run the mock backend:
   `python3 -m scientisttwo run --task tasks/<id> --backend mock --run-dir /tmp/<id>-mock`. The mock
   baseline coder changes nothing, so `results/base/eval/full.json` holds the released code's
   score, run in the real sandbox. Set `expected` from it and `tolerance` from the seed spread.
4. **Set `min_delta`** from the spread of the baseline over more seeds than the search uses.
5. **Mock again** with the full `task.json`: it must pass `baseline_check` and end `done`.
6. **One real `quick` run**, then read it (section 5) before any `paper` run.

Never start a real run with no `baseline_check`: the engine logs `baseline_unchecked` and goes on,
and every gain is then measured from an unverified floor.

## 8. Troubleshooting

Each of these happened during the build (DEVELOPMENT_PROCESS.md, 2026-10-02), or was reproduced
on the mock backend for this guide.

**Paused: `subscription five_hour window at 99% (ceiling 98%)`.** Run 2, at 15:22. Not a fault.
`resume <run-dir> --wait` sleeps until `resume_after` and continues. If your own sessions keep the
window near full, lower the ceiling (section 3).

**Paused: `seven_day window …`.** The weekly window. The reset is usually days away; `--wait` gives
up beyond `--max-wait-hours`. Resume after the date `date -r <resume_after>` prints.

**Paused: `agent-call cap reached (150/150)`**, or `coding-session cap reached`, `running-time cap
reached`. `--wait` will not wait for it, and resuming hits it again. Raise the cap with
`resume --set budget.<cap>=<value>` (section 4).

**Paused: `<key>: the machine failed, not the agent: …`.** No space left, a permission the engine
needs, or the CLI is not logged in. Fix the machine (`df -h`; run `claude` and log in), then
`resume`.

**`not resumed: the task's settings changed since this run started (<keys>)`.** Someone edited
`task.json` after the run started. Put it back, or start a new run, or resume with
`--allow-changed` to adopt the new settings (section 4). Run 2 met the opposite case: it predated
pinning, so its resume pinned the `task.json` of that moment (`task_pinned` in its history).

**`status: error`, `reason: InputsChanged: <key>: this unit's inputs changed since it ran …`.** The
engine code changed between start and resume, and now asks that agent something else (always the
case for runs 1–3, section 4). Either go back to the engine commit the run started on
(`engine_commit` in `run.json`) and resume, or resume with `--allow-changed` to keep the recorded
answer.

**`not resumed: another engine process is running <run-dir>`.** Another engine holds
`<run-dir>/run.lock`. `lsof <run-dir>/run.lock` names it. Two
engines on one run would pay twice for the same units, so the lock is never overridden: wait for
it, or stop it.

**`status` says `running` but nothing moves.** The engine probably died (a reboot, a closed
terminal without tmux). A live engine rewrites `<run-dir>/heartbeat` every 30 s, so
`ls -l <run-dir>/heartbeat` older than a minute means no engine is alive. `resume` records `crashed` and continues; it also kills any process tree the dead
engine left behind.

**`baseline_failed`: `the reproduced baseline scores 0.9118 on full; the task reports 0.95 ± 0.02 (U-BASE-2)`.**
No export is written. Look at `results/base/eval/full.json` (`log_tail` if it did not run), what
the baseline coder changed (`git -C <run-dir>/workspaces/base log -p`) and its answer
(`units/base/coder.json`). If the reproduction is wrong, fix the task's code or paper and start a
new run. If the task's number is wrong, measure it again (section 7, step 3). Do not widen the
tolerance to get past it: a weaker baseline inflates every gain the run reports.

**No PDF, or `"pdf": false`.** The engine's build failed or `latexmk` is missing. The error's last
300 characters are in the `pdf` event in `events.jsonl`; the whole log is
`<run-dir>/builds/<version>/latexmk.out`. Run 2 hit this on every PDF: bibtex writes beside its
sources, which the build sandbox forbade (R5, fixed: builds now compile in a directory of their
own, and run 3 built every PDF). The paper text is unaffected; rebuild it from `export/paper/` with
`latexmk -pdf main.tex`.

**`the run's claude binary <path> is gone (updated since); using the current one`.** A run pins the
real path of the `claude` it started with. The CLI's updater deletes old versions, so a resume days
later may not find it. The resume falls back to the current `claude`, and that start's history
entry records the new path and version. Nothing to do; the warning is the record.

**`<run-dir> is an existing run: continue it with resume <run-dir>`.** `run` refuses a directory
that already holds a run: its task and profile are recorded, and new ones would be ignored. Resume
it, or choose a new directory.

**`ProfileError: limits: missing [], unknown ['k']`, or `ValueError: unknown budget caps ['max_hour']`.**
A mistyped `--set`. The run never started, and no run directory is left behind: fix the key and
run again.

**`status: error`, `reason: unit <key> failed: …`.** An agent failed for good (a refusal, repeated
timeouts, invalid output twice). Read `transcripts/<key>*.jsonl`. The failed unit is cleared, so
`resume` tries it again; if it fails the same way twice, the cause is in its prompt or its inputs.

## What this guide leaves out

- **The design and its reasons:** components, contracts, the sandbox table, every decision on what
  the paper leaves open. [architecture/engine.md](architecture/engine.md).
- **The paper itself, stage by stage:** [paper/analysis.md](paper/analysis.md), with its gaps in
  [paper/unspecified.md](paper/unspecified.md).
- **Adding or changing an agent:** an agent is four files in `scientisttwo/agents/<name>/`
  (engine.md §7); `playground/engine/check_agents.py` checks them against the stage code.
- **The mock script format:** the docstring of
  [`backends/mock.py`](../scientisttwo/runtime/backends/mock.py), and `tests/` for examples.
- **What each run found wrong, and the open work:** [DEVELOPMENT_PROCESS.md](../DEVELOPMENT_PROCESS.md)
  and [TODO.md](../TODO.md).
- **Every profile value:** the JSON files in [`scientisttwo/config/`](../scientisttwo/config/).
  The guide states only the differences that change what a run costs.
