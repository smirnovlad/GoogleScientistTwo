# Requirements 6 · Integrity inside the run and after it

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The paper's integrity rests on prompts and LLM checks, and nothing in its setup enforces them
(`docs/paper/stages/07-integrity.md`) [§4.2] [ours]. CLAUDE.md's integrity rules make these
requirements. Task 6 owns four decisions they rest on: U-INT-4, the harness; U-TOP-5, the split;
A-INT-1, gates or audit; A-INT-3, an independent checker [ours]. They are named under *Depends on*
and decided there, never here [ours].

### R-INT-1 · The locked harness computes every number a decision reads or a report states

- **Requirement.** Every metric that a decision in the loop reads, or that a report states, baselines included, comes from the locked evaluation harness's own result files. Agent code only produces what the harness runs, and every code version declares an entry point that the harness can run, which makes §4.2's reproducibility prompt a property that the setup checks [§4.2] [ours].
- **Traces.** P-INT-1 [§4.2].
- **Why ours.** In the paper, the agent's own script scores both methods and writes the report [p. 42] (image); CLAUDE.md allows metrics only from the locked harness. Departs from the paper [ours].
- **Depends on.** U-INT-4 and A-INT-1, task 6 [ours].
- **Test.** In mock mode, a coding agent scripted to write a fabricated score into its own results file changes nothing: the critic's input and the report carry the harness's number. A code version with no runnable entry point yields no result, and its idea is `Bad`, with the reason recorded [ours].

### R-INT-2 · Evaluation code and data are read-only to every agent, and hash-checked

- **Requirement.** The evaluation protocol of each task, its code and its data, is read-only in every agent's sandbox, and the harness checks its hashes against the manifest before every run [App. B] [Tab. 15] [ours].
- **Traces.** P-STATE-2 [App. B] [Tab. 15].
- **Why ours.** The paper forbids changing the protocol, and enforces the rule only by an audit afterwards [Tab. 15] [App. B]; CLAUDE.md checks evaluation code and data against hashes [ours].
- **Depends on.** U-INT-4, task 6 [ours].
- **Test.** In mock mode, an agent's write to an evaluation file fails in its sandbox; with one evaluation file changed on disk, the hash check fails before the harness runs, no result is produced, and the run stops with its record [ours].

### R-INT-3 · While searching, agents see only validation numbers; the test split is scored once

- **Requirement.** Every number that an agent sees during the run is a validation number. The test split is scored once per exported run, by the harness, after the export [§3.2] [§3.3] [§3.4] [ours].
- **Traces.** P-SUB-2, P-FULL-2 [§3.2]; P-SEL-1 [§3.3, Eq. 4]; P-ABL-5 [§3.4]; P-META-4 [§3.6].
- **Why ours.** In the paper every decision reads the benchmark that is then reported, and the one trace's search was steered by test-set numbers [p. 46] [§3.3]; CLAUDE.md makes every number seen while searching a validation number [ours].
- **Depends on.** U-TOP-5, task 6 [ours].
- **Test.** The mock harness tags every value with its split. A scan of every record an agent could read during a mock run finds no test value, and the harness's test evaluation is called once per exported run, after the export [ours].

### R-INT-4 · The specification filter checks every experiment before any decision reads its result

- **Requirement.** After every experiment, the specification filter checks the code that produced the result against the manifest's task rules, before any critic, guard, selector or writer reads the result. Every experiment means each subset or full-set run, engineering round, ablation run, rebuttal task and A_FullEng refinement [§4.2] [ours]. A discarded result is invalid [§4.2] [fn. 2] [ours]:
  - an idea left with no valid result is `Bad` [ours];
  - a refinement left with no valid result is discarded [ours];
  - a discarded ablation or rebuttal result is dropped from what the critic or the writer reads, and the discard is recorded [ours].
- **Traces.** P-INT-2 [§4.2] [fn. 2]; P-ROSTER-26 [§4.2] [Tab. 7].
- **Why ours.** §4.2 filters after experimentation without saying which experiments, or what a discard does (U-INT-1). Filtering before a decision reads the result keeps a rule-breaking number from ever steering the search [§4.2] [ours].
- **Decides.** U-INT-1 [ours].
- **Depends on.** U-TOP-1, task 3, the task rules in the manifest; A-INT-3, task 6, which agent runs the filter [ours].
- **Test.** In mock mode, a solution planted at the subset step whose code reads the test labels is discarded before the subset critic is called: the critic is never called on that result, and the idea's trace says `Bad`, *filter discard*. A planted rule-breaking ablation run is dropped, and the Ablation Critic reads the other runs [ours].

### R-INT-5 · References are verified after every manuscript revision, and before export

- **Requirement.** After the draft, after every enhancement and every re-draft, and once more before export, a search-augmented check flags the citations it cannot resolve, and the writer corrects the bibliography before the reviewer, the Meta-Reviewer or the export reads the manuscript [§4.2] [ours].
- **Traces.** P-INT-3 [§4.2]; P-ROSTER-27 [§4.2]; P-ROSTER-37 [Fig. 3] (image) [§4.2].
- **Why ours.** §4.2 does not say when the repairs run (U-INT-3). Run before review only, they miss the Enhancer's later edits; run after review only, the paper that was reviewed is not the paper that is exported [§4.2] [§3.5] [ours].
- **Decides.** U-INT-3 [ours].
- **Depends on.** A-INT-2, task 3: which writer repairs [ours].
- **Test.** In mock mode, a fabricated citation planted in the draft is flagged and corrected before the reviewer is called; one planted by a mock enhancement is caught before the next review; the export holds no unresolved citation [ours].

### R-INT-6 · Method–code alignment is audited after every revision, and the fix edits the paper

- **Requirement.** At the same points as R-INT-5, an audit compares the manuscript's method with the code version it reports on; the writer then corrects the manuscript, never the code [§4.2] [ours].
- **Traces.** P-INT-4 [§4.2]; P-ROSTER-28 [§4.2] [p. 47].
- **Decides.** U-INT-3 [ours].
- **Depends on.** A-INT-2, task 3, which writer repairs; A-INT-3, task 6, which agent audits [ours].
- **Test.** In mock mode, a planted mismatch between the method section and the code is flagged in the audit report, the revised method section matches the code, and the code version's hash is unchanged [ours].

### R-INT-7 · Every export is audited after the run, by a judge that is not the in-loop fixer

- **Requirement.** Every exported run goes through ScientistOne's four checks as part of the locked evaluation: score verification, with the harness as the golden evaluator; specification compliance; reference verification; and method–code alignment. The audit covers every reported number, baselines included, and its judge is not the agent that repaired the paper in the loop [§4.2] [Tab. 7] [Ref: meng2026scientistone §5] [ours].
- **Traces.** P-INT-5 [§4.2] [Tab. 7]; P-ROSTER-51 [§4.2]; P-EVAL-10 [§4.2] [Tab. 7]; P-ART-6 [p. 47]; P-ART-7 [pp. 48–50].
- **Why ours.** The one audit the paper shows re-ran the agent's own script once, and skipped the baseline [p. 47]; Table 7's first row passes a reward-hacked codebase on score verification, so a re-run shows determinism, not validity [Tab. 7] [fn. 2] [ours].
- **Depends on.** U-EVAL-5, U-NOTE-4, A-INT-1 and A-INT-3, task 6 [ours].
- **Test.** In mock mode, every export gets four recorded audit results. Four planted defects each fail their own check: a reward-hacked solution, a fabricated citation, a paper–code mismatch, and a reported number that the harness does not reproduce [ours].

### R-INT-8 · Writers see only verified results

- **Requirement.** The Initial Drafter and the Paper Enhancer read results only from the verified results table that the harness builds, and every number in a manuscript traces to an entry of that table [§3.5] [ours].
- **Traces.** P-DRAFT-1 [§3.5]; P-PEER-5 [§3.5].
- **Why ours.** CLAUDE.md lets the manuscript writer see only verified results; App. D's paper gives three sets of numbers for one method under one protocol (A-ART-7) [pp. 56–71] [ours].
- **Depends on.** U-DRAFT-1, task 3; A-ART-7, task 6 [ours].
- **Test.** In mock mode, a number planted in an agent's log but absent from the verified results table never reaches a draft, and a draft holding a number with no entry in the table fails its check before export [ours].

### R-INT-9 · A judge cannot change what it judges

- **Requirement.** An agent whose output chooses a branch, such as a critic, a verifier, the Selector, a reviewer, the filter or an auditor, has read-only access to the code, results and manuscript it judges. Its verdict is stored in the run records, never in the workspace it judged [§4.2] [p. 47] [ours].
- **Traces.** P-ROSTER-26 [§4.2]; P-ROSTER-28 [§4.2] [p. 47].
- **Why ours.** Nothing in the paper makes a judge read-only, and the auditor of p. 47 saved its verdict inside the task it audited [p. 47] [ours].
- **Depends on.** A-INT-3, task 6; U-ART-15, task 3: the sandbox policy [ours].
- **Test.** In mock mode, a judge scripted to write into the workspace it judges fails with a permission error, and its verdict is found only in the run records [ours].
