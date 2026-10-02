# Requirements 8 · Operating the engine: mocks, data, budgets, logs, reproducibility

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The paper describes no test mode, no budget guard, no run log and no reproducibility record for the
engine itself [§3] [App. A.2] [ours]. These requirements come from CLAUDE.md's engineering rules and
from Vlad's instruction to run on his Claude subscription, and most of them trace to no paper
element [ours]. Task 7 owns the test strategy and the mock mode; task 3 owns the components that
meet the rest [ours].

### R-OPS-1 · The whole engine runs in mock mode, for nothing

- **Requirement.** With a mock for every outside system, LLM providers, coding backends, reviewers, search and the drafting system, and for logic tests also the sandbox and the harness (U-INT-4), the whole engine runs end to end, every stage and every outcome of R-RUN-5, at no cost, with no network, and with no ledger entry whose cost is unknown. The test strategy is task 7's (U-TOP-6) [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md requires the engine to run in tests for $0. Enforcement tests keep the sandbox and the harness real, since a mock of a guard proves nothing about the guard (SA-12) [ours].
- **Depends on.** U-TOP-6, task 7; U-INT-4, task 6 [ours].
- **Test.** Logic: in CI with the network disabled, the mock run of each scripted scenario completes, and its ledger reports a total of $0 with no unknown entry [ours].

### R-OPS-2 · Behaviour is data, in versioned files, frozen before reported runs

- **Requirement.** Prompts, output schemas, stage configurations, loop limits, model routes, budgets and profiles live in versioned data files, which no agent can write (R-STATE-8). Changing any of them needs no code change, and every run records the hash of each file it read. A named profile is a set of these files, and the paper profile holds App. A.2's values and routes [App. A.2] [ours]. Before the first reported run on a final-test task, the files are hashed and frozen, and every reported number names the configuration hash that produced it (task 6's IR-18; U-EVAL-4) [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md makes behaviour data run by generic code; TODO task 3's test is that a new agent, backend, task, limit or model touches one component or only data. Tuning these files on the tasks we report would fit their test sets with no agent misbehaving (EI-15) [ours].
- **Depends on.** U-EVAL-4, task 6 [ours].
- **Test.** Logic, in mock mode: changing N_eng, one prompt and one model route in their files, with no code change, changes the next run's call counts, prompt text and recorded model, and its record names the new file hashes; a report whose final-test tasks ran under different configuration hashes fails its check [ours].

### R-OPS-3 · Every outside system sits behind an interface with a mock

- **Requirement.** LLM providers, coding backends, reviewers, search, the drafting system, sandboxes and the harness (U-INT-4) are each reached through an interface, and each interface has a mock that passes the same contract tests as the real adapter; swapping one is configuration. A task is a manifest and a package, never an adapter (R-RUN-2) [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md puts every outside dependency behind an interface with a mock, and expects a second implementation of each, never a copy [ours].
- **Depends on.** U-INT-4, task 6 [ours].
- **Test.** Logic: a static check finds each provider's library imported only inside its adapter; each adapter and its mock pass the same contract tests; swapping a reviewer, a search or a drafting system by configuration changes the next run's records for that system only [ours].

### R-OPS-4 · A budget guard per session and per task, which counts what is in flight

- **Requirement.** Each coding session and each task has a budget, fixed before the task's first run. A unit of work, an agent call, a coding session or a harness job (U-INT-4), starts only if the remaining budget, net of the reservations of units in flight and units in doubt, covers its declared reservation; an unknown cost holds its reservation until it is resolved [ours]. A session that reaches its budget is stopped and recorded; a task that cannot afford its next unit ends with *budget exhausted* and no export, and resumes from its record once the budget is raised. The failure policy is task 3's (U-TOP-2), and the prices task 5's (U-COST-1) [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md bounds cost per session and per task; the paper gives averages only, with no limit on a session or a task [§4.3] [Fig. 10] (image). A budget read from settled spend alone lets two units in flight both see room (SA-4, BA-3), and a budget raised after a failure could run a task again until it succeeds (EI-14) [ours].
- **Depends on.** U-TOP-2, task 3; U-COST-1, task 5; U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: with a task budget below the scenario's cost, the run stops before the first unit it cannot afford, with *budget exhausted* and its ledger, and resumes from its record once the budget is raised; two units started together under a budget that covers one admit only one; a unit in doubt keeps its reservation; a session scripted to overrun its budget is stopped, and the stop is recorded [ours].

### R-OPS-5 · One record per unit of work, from which every log derives

- **Requirement.** Each unit of work, a stage, an agent call, a coding session, a harness job (U-INT-4) or a run, has one record that holds its key, inputs, outputs, cost, timing and outcome. The stage records, the ledger, the log and every query derive from these records, which are data that can be queried, not only text; their format is task 3's (U-ART-10) [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md keeps run history as data that can be queried; five records that each hold the same facts about a unit would give every new field five writers (SA-17) [ours].
- **Depends on.** U-ART-10, task 3; U-INT-4, task 6 [ours].
- **Test.** Logic: after a mock run, the stage records and the ledger rebuilt from the unit records alone equal the ones the run wrote, and a query over the unit records returns per-stage call counts and costs equal to both [ours].

### R-OPS-6 · A run can be reproduced from its record

- **Requirement.** Every run records its configuration and file hashes, its seeds, the engine's code commit, the container image and each model's version; it can be replayed from its records and re-executed from that record. The runtime configuration the record must hold is task 3's (U-CFG-1) [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md makes every run reproducible from these four things; the paper reports none of them for its runs (U-EVAL-4, U-CFG-1) [§4] [App. A.2]. A re-run that reads the same files from disk would pass even if the record named the wrong versions (SA-11) [ours].
- **Depends on.** U-CFG-1, task 3 [ours].
- **Test.** Logic: after a mock run, every configuration file is edited on disk; started again from its record, the run uses the versions its record names and yields the same stage records and ledger, apart from timestamps [ours].

### R-OPS-7 · A unit of work that fails is retried, within a policy and a time bound

- **Requirement.** Each unit of work, harness jobs included (U-INT-4), has a timeout and a retry policy, and each session, harness job and task has a wall-clock bound. A failed attempt is costed and recorded; a unit in doubt is reconciled before any retry (R-STATE-7); a unit that still fails after its retries maps onto the primitive's outcomes by its role (R-PRIM-10), and the task ends with *error after retries* only where that role stops the run. The policy and its values are task 3's (U-TOP-2, U-CFG-2) [ours].
- **Traces.** none.
- **Why ours.** The paper says nothing about a crash, a timeout or code that never runs (U-TOP-2) [§3] [§4.3]. One crashing ablation session would otherwise end a run that already has its idea (SA-5) [ours].
- **Depends on.** U-TOP-2 and U-CFG-2, task 3; U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: a coding session scripted to fail twice and then succeed is retried within the policy, and both failed attempts are in the ledger; a baseline step scripted to fail every time ends the task with *error after retries*, while an ablation session scripted the same way is dropped and the run goes on; a harness job that exceeds its wall-clock bound is stopped and recorded [ours].

### R-OPS-8 · Every agent role has one access policy, as data, enforced by its sandbox

- **Requirement.** Each agent role has one access policy, as data: its read and write sets over named run-state objects, network, package installs and GPUs. A stage may only narrow it, and the policy in force is in each unit's record [p. 51] [p. 55] (image) [ours]. In every policy the evaluation code is read-only; the data roles' index files and labels are absent; results, records, verdicts, the ledger and behaviour files cannot be written; and agent code that the harness runs has no network (task 6's IR-11; U-TOP-5, U-INT-4). The policies' values are task 3's (U-ART-15) [ours].
- **Traces.** P-ART-8 [pp. 51–55].
- **Why ours.** In the paper's one rebuttal, the agent installed packages, downloaded weights and ran on eight GPUs, with nothing stating what it was allowed (U-ART-15) [p. 51] [p. 55] (image). A policy per stage cannot keep the filter from writing where the coder of the same stage writes (SA-8) [ours].
- **Depends on.** U-ART-15, task 3; U-TOP-5 and U-INT-4, task 6 [ours].
- **Test.** Enforcement, on the toy task: within one subset stage, the coder's write succeeds and the filter's fails; an install the role forbids fails, and so does a request for more GPUs than it allows; agent code run by the harness cannot reach the network. In the twin with one policy per stage, the filter's write succeeds [ours].

### R-OPS-9 · A cut in what an agent reads is a recorded decision

- **Requirement.** By default an agent reads everything its stage hands it. Any cut, such as a summary in place of code or a top-k, is configuration that names who chose it and what it loses; an input larger than the model's context fails loudly, or applies such a recorded cut, and is never truncated in silence. Which cuts A_Evolve, the Selector and the Ablation Critic get is task 3's (U-EVO-2, U-SEL-2, U-ABL-6) [§3.3] [§3.4] [ours].
- **Traces.** none.
- **Why ours.** CLAUDE.md makes a bound on model-bound content a product decision; A_Evolve, the Selector and the Ablation Critic are handed whole codebases, with no bound stated [§3.3, Eq. 4] [§3.4] [ours].
- **Depends on.** U-EVO-2, U-SEL-2 and U-ABL-6, task 3 [ours].
- **Test.** Logic: a context configuration with a cut but no named chooser, or no stated loss, fails validation; in mock mode, an agent with no cut receives the whole input its stage hands it, and an input scripted to exceed the mock context fails, with its size and the limit in the record [ours].

### R-OPS-10 · Run artifacts never carry a secret, an e-mail address or a local path

- **Requirement.** Logs, transcripts, records and exports hold no secret, no e-mail address and no absolute path of a machine, and the fixtures committed to the repository pass the same scan [ours].
- **Traces.** none.
- **Why ours.** The repository is public, and a leak, once pushed, cannot be taken back (CLAUDE.md) [ours].
- **Test.** Logic: with secrets planted in a mock run's environment, a scan of every file the run wrote finds none of them, no e-mail address and no home path; the committed fixtures pass the same scan [ours].

### R-OPS-11 · Concurrent runs share a GPU pool without interfering

- **Requirement.** Several runs can share one pool of GPUs: each keeps its own records and ledger, and time spent waiting in the queue is recorded apart from busy time. What runs in parallel is task 3's (U-TOP-4) [ours].
- **Traces.** none.
- **Why ours.** TODO task 3 lists a GPU queue, and parallel sessions share GPUs (`docs/process/worktrees-and-sessions.md`) [ours].
- **Depends on.** U-TOP-4, task 3 [ours].
- **Test.** Logic: two mock runs started together on one mock GPU pool finish with disjoint records, ledgers that each equal their own unit records, and queue time recorded apart from busy time [ours].

### R-OPS-12 · Every agent runs on the Claude subscription, and nothing bills an API

- **Requirement.** Every LLM call, agents and judges alike, goes through the Claude subscription, by `claude -p` or the Agent SDK in its subscription mode, and no component calls a metered API [ours]. Before each call, the backend confirms that the call will count against the subscription: a key or credential in the environment that would switch it to API billing, or a backend that reports API billing, makes the call refused before dispatch, and the run pauses with its reason until the environment is fixed. A usage-limit answer from the subscription pauses the run too, which resumes from its record when the window resets (R-STATE-7), never falling back to a metered API [ours].
- **Traces.** none.
- **Why ours.** Vlad's instruction of 2026-10-02: he will run the engine on his Claude subscription, through `claude -p`, and does not want to pay for an API. Task 4's reuse survey cites Claude Code's billing guide: an API key in the environment overrides the subscription and incurs API charges [ours].
- **Test.** Logic, in mock mode: with an API key planted in the environment, the first call is refused before dispatch and the run pauses with its reason; a mock backend that reports API billing is refused the same way; a mock usage-limit answer pauses the run, which resumes after the mock window resets with no call repeated [ours].
