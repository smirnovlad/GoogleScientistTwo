# Requirements 8 · Operating the engine: mocks, data, budgets, logs, reproducibility

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The paper describes no test mode, no budget guard, no run log and no reproducibility record for the
engine itself [§3] [App. A.2] [ours]. These requirements come from CLAUDE.md's engineering rules,
and most of them trace to no paper element [ours]. Task 7 owns the test strategy and the mock
mode; task 3 owns the components that meet the rest [ours].

### R-OPS-1 · The whole engine runs in mock mode, for nothing

- **Requirement.** With a mock for every outside system (LLM providers, coding backends, reviewers, search, the drafting system, the sandbox and the harness), the whole engine runs end to end, every stage and every outcome of R-RUN-5, at no cost and with no network [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md requires the engine to run in tests for $0; every test in these files assumes it [ours].
- **Depends on.** U-TOP-6, task 7: the test strategy [ours].
- **Test.** In CI with the network disabled, the mock run of each scripted scenario completes, and its ledger reports a total of $0 [ours].

### R-OPS-2 · Behaviour is data, in versioned files

- **Requirement.** Prompts, output schemas, stage configurations, loop limits, model routes and budgets live in versioned data files. Changing any of them needs no code change, and every run records the version of each file it read [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md makes behaviour data run by generic code; TODO task 3's test is that a new agent, backend, task, limit or model touches one component or only data [ours].
- **Test.** In mock mode, changing N_eng, one prompt and one model route in their files, with no code change, changes the next run's call counts, prompt text and recorded model, and its record names the new file versions [ours].

### R-OPS-3 · Every outside system sits behind an interface with a mock

- **Requirement.** LLM providers, coding backends, reviewers, search, the drafting system, sandboxes and tasks are each reached through an interface, and each interface has a mock that passes the same contract tests as the real adapter [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md puts every outside dependency behind an interface with a mock, and expects a second implementation of each, never a copy [ours].
- **Test.** A static check finds each provider's library imported only inside its adapter, and each adapter and its mock pass the same contract tests [ours].

### R-OPS-4 · A budget guard per session and per task

- **Requirement.** Each coding session and each task has a budget. A session that reaches its budget is stopped and recorded, and a task never starts a unit of work it cannot afford: it ends with the outcome *budget exhausted* [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md bounds cost per session and per task; the paper gives averages only, with no limit on a session or a task [§4.3] [Fig. 10] (image) [ours].
- **Depends on.** U-TOP-2, task 3; U-COST-1, task 5, the prices behind the budget [ours].
- **Test.** In mock mode, with a task budget below the scenario's cost, the run stops before the first unit it cannot afford, with *budget exhausted* and its ledger; a session scripted to overrun its budget is stopped, and the stop is recorded [ours].

### R-OPS-5 · Every unit of work is logged, as data that can be queried

- **Requirement.** Each stage, agent call and run is logged with its inputs, outputs, cost and timing, as records that can be queried, not only as text [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md keeps run history as data that can be queried [ours].
- **Test.** After a mock run, a query over its log returns per-stage call counts and costs equal to the stage records and the ledger [ours].

### R-OPS-6 · A run can be reproduced from its record

- **Requirement.** Every run records its configuration and file versions, its seeds, the engine's code commit, the container image, and each model's version, and can be run again from that record [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md makes every run reproducible from these four things; the paper reports none of them for its runs (U-EVAL-4, U-CFG-1) [§4] [App. A.2] [ours].
- **Depends on.** U-CFG-1, task 3: the runtime configuration that the record must hold [ours].
- **Test.** A mock run started again from its record yields the same stage records and ledger, apart from timestamps [ours].

### R-OPS-7 · A unit of work that fails is retried, within a policy

- **Requirement.** Each unit of work has a timeout and a retry policy. A failed attempt is costed and recorded, and a unit that still fails after its retries ends the task with *error after retries* [ours].
- **Traces.** none.
- **Why ours.** The paper says nothing about a crash, a timeout or code that never runs (U-TOP-2) [§3] [§4.3] [ours].
- **Depends on.** U-TOP-2 and U-CFG-2, task 3 [ours].
- **Test.** In mock mode, a coding session scripted to fail twice and then succeed is retried within the policy, and both failed attempts are in the ledger; one scripted to fail every time ends the task with *error after retries* [ours].

### R-OPS-8 · Coding sessions run in sandboxes with a declared policy

- **Requirement.** Each coding session runs in a sandbox whose policy for package installs, network, GPUs and file access is declared per stage, with the evaluation protocol read-only in every one [p. 51] [p. 55] (image) [ours].
- **Traces.** P-ART-8 [pp. 51–55].
- **Why ours.** In the paper's one rebuttal, the agent installed packages, downloaded weights and ran on eight GPUs, with nothing stating what it was allowed (U-ART-15) [p. 51] [p. 55] (image) [ours].
- **Depends on.** U-ART-15, task 3: the policy's values [ours].
- **Test.** In mock mode, an install that the stage's policy forbids fails, and so does a request for more GPUs than the stage allows [ours].

### R-OPS-9 · A cut in what an agent reads is a recorded decision

- **Requirement.** By default an agent reads everything its stage hands it. Any cut, such as a summary in place of code or a top-k, is configuration that names who chose it and what it loses [§3.3] [§3.4] [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md makes a bound on model-bound content a product decision; A_Evolve, the Selector and the Ablation Critic are handed whole codebases, with no bound stated (U-EVO-2, U-SEL-2, U-ABL-6) [§3.3, Eq. 4] [§3.4] [ours].
- **Depends on.** U-EVO-2, U-SEL-2 and U-ABL-6, task 3 [ours].
- **Test.** A context configuration with a cut but no named chooser, or no stated loss, fails validation; in mock mode, an agent with no cut receives the whole input its stage hands it [ours].
