# Requirements 6 · Integrity inside the run and after it

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The paper's integrity rests on prompts and LLM checks, and nothing in its setup enforces them
(`docs/paper/stages/07-integrity.md`) [§4.2] [ours]. CLAUDE.md's integrity rules make these
requirements. Task 6 owns four decisions they rest on: U-INT-4, the harness; U-TOP-5, the data
roles; A-INT-1, gates or audit; A-INT-3, who checks [ours]. Its first version,
`docs/integrity/blocking-decisions.md` on its own branch, not yet reviewed, states rules IR-1 to
IR-31 and gates G1 to G7; these requirements cite them by ID, list the four rows under *Depends
on*, and decide only task 2's rows, U-INT-1 and U-INT-3 [ours]. Every test here that proves a guard
is an enforcement test, with a twin in which the guard is off and the attack succeeds (*How to
read*) [ours].

### R-INT-1 · The locked harness computes every number a decision reads or a report states

- **Requirement.** Every number that a decision in the loop reads, or that a manuscript, a table, a gain or a report gives for a row of the run, is a value of a result record the harness wrote, or a deterministic function of such values computed by engine code. Agent code computes none of them, for the baseline, candidates, engineering rounds, ablations, controls, A_FullEng refinements and rebuttal tasks alike (task 6's IR-1, IR-2, IR-5; U-INT-4) [§4.2] [ours]. Agent code hands the harness a code tree whose entry points follow the manifest's interface, and runs only inside harness jobs, without network and with no write path that an agent session can read (IR-3, IR-11; U-TOP-5) [ours]. A code version with no runnable entry point yields no result. Which checks block in the run and which measure after it is task 6's (A-INT-1) [ours].
- **Traces.** P-INT-1 [§4.2]; P-BASE-1, P-SUB-1, P-SUB-3, P-FULL-1, P-FULL-2 [§3.2]; P-ABL-2, P-ABL-4 [§3.4]; P-PEER-4 [§3.5]; P-META-3 [§3.6].
- **Departs from.** P-INT-1, P-BASE-1, P-SUB-1, P-SUB-3, P-FULL-1, P-FULL-2, P-ABL-2, P-ABL-4, P-PEER-4 and P-META-3: the agents produce code, and the harness, not the agent, produces each E [§3.2] [§3.4] [§3.5] [§3.6] [§4.2] [ours].
- **Why ours.** In the paper, the agent's own script scores both methods and writes the report [p. 42] (image), and score verification passed a codebase that held reward hacking [Tab. 7] [fn. 2]; CLAUDE.md allows metrics only from the locked harness [ours].
- **Depends on.** U-INT-4, U-TOP-5 and A-INT-1, task 6 [ours].
- **Test.** Enforcement, on the toy task, four planted attacks, each run twice [ours]:
  - a coding session writes a result record claiming 0.99 where the harness scores 0.60 [ours];
  - agent code run by the harness overwrites the result's path [ours];
  - agent code patches the metric at import time, through a module that shadows the scorer's [ours];
  - a code version with no runnable entry point [ours].

  With the guard on, each write is refused or has no effect, the critic and the report read the harness's number, and the attempt is recorded; the last version yields no result, and its idea is `Bad` with the reason. In the twin that scores in the agent's environment, with the run directory writable, each of the first three changes the next decision [ours].

### R-INT-2 · Evaluation code is read-only and evaluation data unreachable, hash-checked at every job

- **Requirement.** The evaluation entry points, the harness code and the task rules are read-only to every agent, and the index files and labels of the search and report roles are absent from every agent's sandbox (task 6's IR-10, IR-11; U-TOP-5). The harness checks every hash it depends on at the start of every job; on a mismatch it refuses the job, writes no result, and the run ends with *integrity halt* (IR-6; U-INT-4) [App. B] [Tab. 15] [ours].
- **Traces.** P-STATE-2 [App. B] [Tab. 15].
- **Why ours.** The paper forbids changing the protocol, and enforces the rule only by an audit afterwards [Tab. 15] [App. B]. CLAUDE.md checks evaluation code and data against hashes, and a label file that is only read-only can still be read (EI-2) [ours].
- **Depends on.** U-INT-4 and U-TOP-5, task 6 [ours].
- **Test.** Enforcement, on the toy task: an agent's write to an evaluation file fails in its real sandbox, and its attempt to open a label file finds no such file; with one evaluation file changed on disk, the next harness job refuses to run, no result is written, and the run ends with *integrity halt*. In the twin with the labels mounted read-only, a planted solution that reads them scores perfectly [ours].

### R-INT-3 · No number of the report role reaches the loop

- **Requirement.** Every number that an agent, a prompt or a manuscript sees before the freeze comes from the search role, and carries its role's label. The report role is scored only in task 6's three kinds of report job: the sealed baseline check, the one test event after the freeze, and the audit's re-run (IR-14, IR-15; U-TOP-5). When the test event happens, and what may change after it, are task 6's (IR-14, IR-17) [§3.2] [§3.3] [§3.4] [ours].
- **Traces.** P-SUB-2, P-FULL-2 [§3.2]; P-SEL-1 [§3.3, Eq. 4]; P-ABL-5 [§3.4]; P-META-4 [§3.6].
- **Why ours.** In the paper every decision reads the benchmark that is then reported, and the one trace's search was steered by test-set numbers [p. 46] [§3.3]; CLAUDE.md makes every number seen while searching a validation number. The first draft also fixed when the test split is scored, which is task 6's to decide (EI-3) [ours].
- **Depends on.** U-TOP-5, task 6 [ours].
- **Test.** Enforcement, on the toy task: every value the harness writes carries its role; a scan of every record, prompt and manuscript version written before the freeze finds no report-role value; a report job requested before the freeze is refused, and the run ends with *integrity halt*. In the twin that lets the critics read report numbers, a null-idea search of 20 candidates reports the best one's noise as a gain, while with the guard on the reported gain is zero within its noise [ours].

### R-INT-4 · The specification filter judges every result before any decision reads it

- **Requirement.** After every code-producing unit of work, the harness's scoring and then the specification filter run, before any critic, guard, Selector or writer reads the result (task 6's G2 and IR-21; A-INT-1, U-INT-4). Every unit means R-INT-10's hook point, which covers each subset or full-set run, engineering round, ablation run, rebuttal task and A_FullEng refinement, and any new code-producing step, with no list to edit [§4.2] [ours]. The filter checks the code against the manifest's task rules, whose form is task 3's (U-TOP-1); which agent runs it is task 6's (A-INT-3). Its verdict and the result each name the snapshot's hash, and a decision reads a result only when they match [§4.2] [ours]. A discarded result is invalid, and its author is told only which rule it broke (IR-27) [§4.2] [fn. 2] [ours]:
  - an idea with a discarded result is `Bad`, *filter discard*, and no engineering round repairs it [ours];
  - a refinement with a discarded result is discarded [ours];
  - a discarded ablation or rebuttal item is re-run once by a fresh session; a second discard drops it, and it stays listed in what the next judge reads (R-STG-9) [ours];
  - a filter that fails after its retries counts as a discard [ours].
- **Traces.** P-INT-2 [§4.2] [fn. 2]; P-ROSTER-26 [§4.2] [Tab. 7]; P-ROSTER-43 [§4.2] [Fig. 3] (image).
- **Why ours.** §4.2 filters after experimentation without saying which experiments, or what a discard does (U-INT-1). Filtering before a decision reads the result keeps a rule-breaking number from ever steering the search [§4.2] [ours]. ⛔ WHY NOT let the engineer repair a discarded idea within its budget: each repair is one more draw against the filter's miss rate, so a hack would pass in the end [ours].
- **Decides.** U-INT-1 [ours].
- **Depends on.** U-TOP-1, task 3; A-INT-1, A-INT-3 and U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: a solution planted at the subset step whose code reads a label path is discarded before the subset critic is called; the critic is never called on that result, no engineer call follows, and the idea's trace says `Bad`, *filter discard*; a planted rule-breaking ablation run is re-run once, discarded again, and listed with its reason in the Ablation Critic's input; a filter scripted to fail counts as a discard; a verdict whose hash differs from the result's blocks the decision. The real filter's miss rate is task 6's to measure (IR-31) [ours].

### R-INT-5 · References are verified after every manuscript revision

- **Requirement.** At the manuscript hook point (R-INT-10), after the draft, after every enhancement and re-draft, and after the tail's revision, a check resolves each bibliography entry through a literature search and compares its title, authors, venue and year with the record it resolves to. An entry that does not resolve, or does not match, is flagged, and the writer corrects the bibliography before the reviewer, the Meta-Reviewer or the export reads the manuscript (task 6's G4; A-INT-1). Which writer repairs is task 3's (A-INT-2) [§4.2] [ours].
- **Traces.** P-INT-3 [§4.2]; P-ROSTER-27 [§4.2]; P-ROSTER-37 [Fig. 3] (image) [§4.2].
- **Why ours.** §4.2 does not say when the repairs run (U-INT-3). Run before review only, they miss the Enhancer's later edits; run after review only, the paper that was reviewed is not the paper that is exported [§4.2] [§3.5]. ScientistOne's own reference check matches each entry against its record, which catches a real identifier attached to a fabricated description (EI-23) [Ref: meng2026scientistone §5] [ours].
- **Decides.** U-INT-3 [ours].
- **Depends on.** A-INT-2, task 3; A-INT-1, task 6 [ours].
- **Test.** Logic, in mock mode: a fabricated citation planted in the draft is flagged and corrected before the reviewer is called; one planted by a mock enhancement is caught before the next review; a real DOI attached to a wrong title is flagged; an entry the writer fails to fix in 2 repairs ends the run with *manuscript gate failed*; the export holds no unresolved entry [ours].

### R-INT-6 · Method–code alignment is audited after every revision, and the fix edits the text

- **Requirement.** At the same hook points as R-INT-5, an audit compares the manuscript's method with the code version it reports on, each ablation variant's code with its plan, and each declared switch with the mechanism the method describes (task 6's G5; A-INT-1). The writer then corrects the manuscript, never the code (IR-28). Which agent audits is task 6's (A-INT-3), and which writer repairs is task 3's (A-INT-2) [§4.2] [ours].
- **Traces.** P-INT-4 [§4.2]; P-ROSTER-28 [§4.2] [p. 47]; P-ROSTER-37 [Fig. 3] (image) [§4.2].
- **Why ours.** §4.2 does not say when the audit runs (U-INT-3). An ablation variant coded to underperform, or a switch that turns off more than the mechanism, would make the ablation's control prove nothing (EI-7) [§4.2] [ours].
- **Decides.** U-INT-3 [ours].
- **Depends on.** A-INT-2, task 3; A-INT-1 and A-INT-3, task 6 [ours].
- **Test.** Logic, in mock mode: a planted mismatch between the method section and the code is flagged, the revised method section matches the code, and the code version's hash is unchanged; a switch scripted to turn off a general training control as well is flagged; a mismatch the writer fails to fix in 2 repairs ends the run with *manuscript gate failed* [ours].

### R-INT-7 · Every export is audited after the run, by an auditor held out from the engine

- **Requirement.** Every exported run goes through ScientistOne's four checks after export: score verification, with the harness as its golden evaluator (U-INT-4); specification compliance; reference verification; and method–code alignment [§4.2] [Tab. 7] [Ref: meng2026scientistone §5] [ours]. How the audit runs is task 6's (A-INT-1, A-INT-3; IR-22 to IR-31): what it re-runs, its checks of the ledger, what a failure does to the report, and an auditor kept apart from every in-loop checker and fixer, with settings from U-EVAL-5 and U-NOTE-4 [ours]. The audit's record says which parts follow ScientistOne (the four checks, the re-run on a golden evaluator, the majority votes, the lenient rule of alignment) and which are ours (every reported number in scope, the harness as the evaluator, the auditor's separation) [ours].
- **Traces.** P-INT-5 [§4.2] [Tab. 7]; P-ROSTER-51 [§4.2]; P-EVAL-10 [§4.2] [Tab. 7]; P-ART-6 [p. 47]; P-ART-7 [pp. 48–50].
- **Why ours.** The one audit the paper shows re-ran the agent's own script once, and skipped the baseline [p. 47]; Table 7's first row passes a reward-hacked codebase on score verification, so a re-run shows determinism, not validity [Tab. 7] [fn. 2]. An auditor with the in-loop checker's model and prompt would re-run the gate the loop was optimised against (EI-13) [ours].
- **Depends on.** U-EVAL-5, U-NOTE-4, A-INT-1, A-INT-3 and U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: every export gets four recorded audit results, and four planted defects each fail their own check: a reward-hacked solution, a fabricated citation, a paper–code mismatch, and a reported number that the harness does not reproduce; a configuration whose post-hoc alignment auditor is the in-loop auditor fails validation [ours].

### R-INT-8 · Writers see only verified results, and every measurement is the table's

- **Requirement.** The Initial Drafter and the Paper Enhancer read results only from the verified results table (R-STATE-10; U-INT-4); their sandbox holds the manuscript, the table and read-only code, never the run directory. Each number a manuscript presents as a measurement is inserted by engine code from a table entry that the writer names (task 6's G3; A-INT-1), and the main results table is rendered by engine code from the method's own entries, so that no other row's entry can stand there. Until the test event, every entry is a search-role entry (IR-16; U-TOP-5). A misattribution in the prose around a number stays detection only, by the alignment check and the audit, as task 6 records [§3.5] [ours]. What the drafter reads is task 3's (U-DRAFT-1), and the consistency check before export task 6's (A-ART-7) [ours].
- **Traces.** P-DRAFT-1 [§3.5]; P-PEER-5 [§3.5].
- **Why ours.** CLAUDE.md lets the manuscript writer see only verified results; App. D's paper gives three sets of numbers for one method under one protocol (A-ART-7) [pp. 56–71]. A check that a number appears somewhere in the table passes an ablation's number quoted as the method's (EI-5) [ours].
- **Depends on.** U-DRAFT-1, task 3; A-ART-7, A-INT-1, U-INT-4 and U-TOP-5, task 6 [ours].
- **Test.** Enforcement, on the toy task, three planted drafts [ours]:
  - one whose main results table holds an ablation entry [ours];
  - one with a number typed by the writer [ours];
  - one with a result figure not rendered from the table [ours].

  With the guard on, each fails its check before any reviewer reads it; in the twin whose check only looks for the value somewhere in the table, all three pass. A writer scripted to open the run log finds no such path in its sandbox [ours].

### R-INT-9 · A judge cannot change what it judges

- **Requirement.** An agent whose output chooses a branch, such as a critic, a verifier, the Selector, a reviewer, the filter or an auditor, has read-only access to the code, results and manuscript it judges, in a fresh session of its own (task 6's IR-26; A-INT-3). Engine code writes its verdict into the run's records from its output; the judge's session has no write path there, and a verdict found anywhere else has no standing (IR-30). The sandbox policy is task 3's (U-ART-15) [§4.2] [p. 47] [ours].
- **Traces.** P-ROSTER-26 [§4.2]; P-ROSTER-28 [§4.2] [p. 47].
- **Why ours.** Nothing in the paper makes a judge read-only, and the auditor of p. 47 saved its verdict inside the task it audited [p. 47] [ours].
- **Depends on.** A-INT-3, task 6; U-ART-15, task 3 [ours].
- **Test.** Enforcement, on the toy task: within one subset stage, the coder's write to its workspace succeeds and the filter's write to the same workspace fails on the real sandbox; a judge scripted to write a passing verdict into the task tree is refused, and the reporter counts only the verdict engine code recorded. In the twin with the judge's workspace writable, the planted verdict is counted [ours].

### R-INT-10 · Cross-cutting checks run at hook points declared as data, and each repair is bounded

- **Requirement.** The checks that no stage owns run at hook points declared in data by the kind of step, not by stage, in a stated order (task 6's G2 to G5; A-INT-1) [§4.2] [ours]:
  - after a code-producing step: the harness's scoring, then the specification filter (U-INT-4) [ours];
  - after a manuscript-producing step, the tail's revision included: compile, number provenance, references, then method–code alignment [ours].

  Each check's failure maps onto the primitive's outcomes: reject the candidate, fail a refinement into its guard's failure branch, drop an item, or repair. A repair is a bounded instance of the primitive: within a hook, the check runs again after each repair, at most 2 repairs per hook and manuscript version, after which the run ends with *manuscript gate failed* (IR-21). A repair does not start the sequence over; only the compile check runs again after the last hook [ours].
- **Traces.** none.
- **Why ours.** §4.2 names the checks without placing them in the pipeline, and the first draft ran them at points no stage owned, from a list of stages, with repair loops of no limit (SA-3) [§4.2] [ours]. Two repairs follow the paper's own bound on engineering, N_eng = 2 [App. A.2] [ours].
- **Decides.** U-INT-3, the hooks' order and bound [ours].
- **Depends on.** A-INT-1 and U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: a toy result-producing stage added by data has its results scored and filtered with no code change; an unfixable planted citation ends at the repair limit with *manuscript gate failed*; a repair of a reference re-runs the reference check, not the whole sequence, and compile runs once more after the alignment check [ours].
