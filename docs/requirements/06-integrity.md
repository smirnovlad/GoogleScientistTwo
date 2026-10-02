# Requirements 6 · Integrity inside the run and after it

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The paper's integrity rests on prompts and LLM checks, and nothing in its setup enforces them
(`docs/paper/stages/07-integrity.md`) [§4.2] [ours]. CLAUDE.md's integrity rules make these
requirements. Task 6 owns four decisions they rest on: U-INT-4, the harness; U-TOP-5, the data
roles; A-INT-1, gates or audit; A-INT-3, who checks [ours]. Its second version,
`docs/integrity/blocking-decisions.md` at dd4b3de on its own branch, the final version of its P0 part,
applies its first review's fix list and states rules IR-1 to IR-41, the gates G2 to G5 and the hooks G1, G6 and G7; these
requirements cite them by ID, list the four rows under *Depends on*, and decide only task 2's rows,
U-INT-1 and U-INT-3, with the values task 6 leaves to task 2 (IR-7.1, IR-21.1) [ours]. Every test
here that proves a guard is an enforcement test, with a twin or a positive control for each of its
clauses (*How to read*) [ours].

### R-INT-1 · The locked harness computes every number a decision reads or a report states

- **Requirement.** Every number about a row's performance that a decision in the loop reads, or that a manuscript, a table, a gain or a report gives, is a value of a result record the harness released, or a deterministic function of such values computed by engine code. Agent code computes none of them, for the baseline, candidates, engineering rounds, ablations, controls, A_FullEng refinements and rebuttal tasks alike (task 6's IR-1.1, IR-1.2, IR-5.1; U-INT-4) [§4.2] [ours]. Agent code hands the harness a code tree whose entry points follow the manifest's interface, and runs only inside harness jobs, without network and with no write path that an agent session can read (IR-2.1, IR-11.2; U-TOP-5) [ours]. A code version with no runnable entry point yields no result. Which checks block in the run and which measure after it is task 6's (A-INT-1) [ours].
- **Traces.** P-INT-1 [§4.2]; P-BASE-1, P-SUB-1, P-SUB-3, P-FULL-1, P-FULL-2 [§3.2]; P-ABL-2, P-ABL-4 [§3.4]; P-PEER-4 [§3.5]; P-META-3 [§3.6].
- **Departs from.** P-INT-1, P-BASE-1, P-SUB-1, P-SUB-3, P-FULL-1, P-FULL-2, P-ABL-2, P-ABL-4, P-PEER-4 and P-META-3: the agents produce code, and the harness, not the agent, produces each E [§3.2] [§3.4] [§3.5] [§3.6] [§4.2] [ours].
- **Why ours.** In the paper, the agent's own script scores both methods and writes the report [p. 42] (image), and score verification passed a codebase that held reward hacking [Tab. 7] [fn. 2]; CLAUDE.md allows metrics only from the locked harness [ours].
- **Depends on.** U-INT-4, U-TOP-5 and A-INT-1, task 6 [ours].
- **Test.** Enforcement, on the toy task, five planted attacks, each beside its twin [ours]:
  - a coding session writes a result record claiming 0.99 where the harness scores 0.60 [ours];
  - agent code run by the harness overwrites the result's path [ours];
  - agent code patches the metric at import time, through a module that shadows the scorer's [ours];
  - agent code run by the harness opens a connection to a local endpoint; as its positive control, the same request, made just before from a role allowed network in the same environment, succeeds [ours];
  - a code version with no runnable entry point [ours].

  With the guard on, each write or connection is refused or has no effect, the critic and the report read the harness's number, and the attempt is recorded; the last version yields no result, and its idea is `Bad` with the reason. In the twin that scores in the agent's environment, with the run directory writable and the network open, each of the first four changes the next decision [ours].

### R-INT-2 · Evaluation code is read-only and evaluation data unreachable, hash-checked at every job

- **Requirement.** The evaluation entry points, the harness code and the task rules are read-only to every agent, and the index files and labels of the search and report roles are absent from every agent's sandbox (task 6's IR-11; U-TOP-5). The harness checks every hash it depends on at the start of every job; on a mismatch it refuses the job and releases nothing, and the run halts with its class, an integrity halt ending it (IR-6.3, IR-6.5, IR-35; U-INT-4) [App. B] [Tab. 15] [ours]. Two paths stay detection only, as task 6 records: public labels fetched over a session's network and carried in the code tree, and a predict step that adapts on the inputs it scores; the specification filter and the audit look for both (A-INT-1) [ours].
- **Traces.** P-STATE-2 [App. B] [Tab. 15].
- **Why ours.** The paper forbids changing the protocol, and enforces the rule only by an audit afterwards [Tab. 15] [App. B]. CLAUDE.md checks evaluation code and data against hashes, and a label file that is only read-only can still be read (EI-2) [ours].
- **Depends on.** U-INT-4, U-TOP-5 and A-INT-1, task 6 [ours].
- **Test.** Enforcement, on the toy task [ours]:
  - an agent's write to an evaluation file fails in its real sandbox; in the twin with the evaluation mount writable, the write succeeds, and the hash check at the next job still refuses it; in the twin with both guards off, the next scoring uses the edited file [ours];
  - its attempt to open a label file finds no such file; in the twin with the labels mounted read-only, a planted solution that reads them scores perfectly [ours];
  - with one evaluation file changed on disk by an agent identity, the next harness job refuses to run, nothing is released, and the run ends with *integrity halt*; in the twin with no check at the start of a job, the job runs on the changed file [ours].

### R-INT-3 · No value computed on the report role reaches the loop

- **Requirement.** Before the freeze, no value computed on the report role reaches an agent, a prompt, a manuscript or a decision, beyond the pass or fail that the sealed baseline check releases; every value the harness writes carries its role, and every published number is labelled as published (task 6's IR-1.3, IR-15.6, IR-16; U-TOP-5) [§3.2] [§3.3] [§3.4] [ours]. The report role is read only by task 6's four kinds of report job: the baseline's report fit and sealed check at admission, the one test event, a correction event, and the audit's re-fits; any other request is refused, and the run ends with *integrity halt* (IR-14.6, IR-35.1). Task 6 reads CLAUDE.md's one use of the test set as the test event, since none of the other reads can reach a decision, and flags CLAUDE.md's narrower wording to the coordinating session; when the test event happens, and what may change after it, are task 6's (IR-14, IR-17) [ours].
- **Traces.** P-SUB-2, P-FULL-2 [§3.2]; P-SEL-1 [§3.3, Eq. 4]; P-ABL-5 [§3.4]; P-META-4 [§3.6].
- **Why ours.** In the paper every decision reads the benchmark that is then reported, and the one trace's search was steered by test-set numbers [p. 46] [§3.3]; CLAUDE.md makes every number seen while searching a validation number. Agents read the fit role and published numbers by design, so the first revision's rule that every number they see comes from search was false, and its test forbade the sealed check that R-STG-3 requires (the integrity closure, check 1; the Codex review, P1) [ours].
- **Depends on.** U-TOP-5, task 6 [ours].
- **Test.** Enforcement, on the toy task [ours]:
  - every value the harness writes carries its role; a scan of everything an agent, a prompt or a manuscript reads before the freeze finds no value computed on the report role, while the sealed check's job runs at admission and releases pass or fail only; as the scan's positive control, a report value planted in a critic's prompt in a copy of the run is found [ours];
  - a report job requested for a candidate before the freeze is refused, and the run ends with *integrity halt*; in the twin that runs it, its number reaches the next critic's input [ours];
  - in the twin that lets the critics read report numbers, a search over 20 candidates that do nothing, with evaluation noise only, reports a gain of about 1.87 SD, as stated before the run; with the guard on, the reported gain is 0 within ±3 SE [ours].

### R-INT-4 · The specification filter judges every result before any decision reads it

- **Requirement.** After every code-producing unit of work, the harness's scoring and then the specification filter run, before any critic, guard, Selector or writer reads the result (task 6's G2, IR-21; A-INT-1, U-INT-4). Every unit means R-INT-10's hook point, which covers each subset or full-set run, engineering round, ablation run, rebuttal task and A_FullEng refinement, and any new code-producing step, with no list to edit [§4.2] [ours]. The filter checks the code against the manifest's task rules, whose form is task 3's (U-TOP-1); which agent runs it is task 6's (A-INT-3). Its verdict and the result each name the snapshot's hash, and a decision reads a result only when they match [§4.2] [ours]. A discarded result is invalid, and its author is told only which rule it broke (IR-27.3). The values task 6 leaves to task 2 are these (IR-21.1) [§4.2] [fn. 2] [ours]:
  - an idea with a discarded result is `Bad`, *filter discard*, and no engineering round repairs it [ours];
  - a refinement with a discarded result is discarded [ours];
  - a discarded ablation or rebuttal item is re-run once by a fresh session, on the item's own counter, whose limit is that one re-run (R-STG-13), as IR-40.1 gives each candidate one counter; it never spends its parent stage's refinement; a second discard drops it, and it stays listed in what the next judge reads (R-STG-9) [ours];
  - a filter that fails after its retries counts as a discard [ours].
- **Traces.** P-INT-2 [§4.2] [fn. 2]; P-ROSTER-26 [§4.2] [Tab. 7]; P-ROSTER-43 [§4.2] [Fig. 3] (image).
- **Why ours.** §4.2 filters after experimentation without saying which experiments, or what a discard does (U-INT-1). Filtering before a decision reads the result keeps a rule-breaking number from ever steering the search [§4.2] [ours]. ⛔ WHY NOT let the engineer repair a discarded idea within its budget: each repair is one more draw against the filter's miss rate, so a hack would pass in the end [ours].
- **Decides.** U-INT-1 [ours].
- **Depends on.** U-TOP-1, task 3; A-INT-1, A-INT-3 and U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: a solution planted at the subset step whose code reads a label path is discarded before the subset critic is called; the critic is never called on that result, no engineer call follows, and the idea's trace says `Bad`, *filter discard*; a planted rule-breaking ablation run is re-run once, discarded again, and listed with its reason in the Ablation Critic's input; a filter scripted to fail counts as a discard; a verdict whose hash differs from the result's blocks the decision. The real filter's error rates are task 6's to measure (IR-31) [ours].

### R-INT-5 · References are verified after every manuscript revision

- **Requirement.** At the manuscript hook point (R-INT-10), after the draft, after every enhancement and re-draft, and after the tail's revision, a check resolves each bibliography entry through bibliographic search and compares its title, authors, venue and year with the record it resolves to; an LLM judges only the near misses (task 6's G4, IR-21.3; A-INT-1). An entry that does not resolve, or does not match, is flagged, and the writer corrects the bibliography before the reviewer, the Meta-Reviewer or the export reads the manuscript. Which writer repairs is task 3's (A-INT-2) [§4.2] [ours].
- **Traces.** P-INT-3 [§4.2]; P-ROSTER-27 [§4.2]; P-ROSTER-37 [Fig. 3] (image) [§4.2].
- **Why ours.** §4.2 does not say when the repairs run (U-INT-3). Run before review only, they miss the Enhancer's later edits; run after review only, the paper that was reviewed is not the paper that is exported [§4.2] [§3.5]. ScientistOne's own reference check matches each entry against its record, which catches a real identifier attached to a fabricated description (EI-23) [Ref: meng2026scientistone §5] [ours].
- **Decides.** U-INT-3 [ours].
- **Depends on.** A-INT-2, task 3; A-INT-1, task 6 [ours].
- **Test.** Logic, in mock mode, with a mock judge scripted to flag: a fabricated citation planted in the draft is flagged and corrected before the reviewer is called; one planted by a mock enhancement is caught before the next review; a real DOI attached to a wrong title is flagged; the export holds no unresolved entry. The real check's error rates are task 6's (IR-31) [ours].

### R-INT-6 · Method–code alignment is audited after every revision, and the fix edits the text

- **Requirement.** At the same hook points as R-INT-5, an audit compares the manuscript's method with the code version it reports on, each ablation variant's code with its plan, and each declared switch with the mechanism the method describes (task 6's G5, IR-21.4; A-INT-1). The writer then corrects the manuscript, never the code (IR-28). A finding about a switch is a finding about the code, which no text edit repairs: it is recorded, and the export is marked *attribution not established* (R-STG-9); a switch's scope is checked first at the code hook (R-STG-4) [ours]. Which agent audits is task 6's (A-INT-3), and which writer repairs is task 3's (A-INT-2) [§4.2] [ours].
- **Traces.** P-INT-4 [§4.2]; P-ROSTER-28 [§4.2] [p. 47]; P-ROSTER-37 [Fig. 3] (image) [§4.2].
- **Why ours.** §4.2 does not say when the audit runs (U-INT-3). An ablation variant coded to underperform, or a switch that turns off more than the mechanism, would make the ablation's control prove nothing (EI-7); a writer that adds the switch's extra controls to the method would otherwise turn TeCh's case into an attributed gain (the integrity closure, NEW-4) [§4.2] [App. B] [ours].
- **Decides.** U-INT-3 [ours].
- **Depends on.** A-INT-2, task 3; A-INT-1 and A-INT-3, task 6 [ours].
- **Test.** Logic, in mock mode, with a mock auditor scripted to flag: a planted mismatch between the method section and the code is flagged, the revised method section matches the code, and the code version's hash is unchanged; a switch that also turns off a general training control is flagged, the export is marked *attribution not established*, and a revised method text does not lift the mark. The real audit's error rates are task 6's (IR-31) [ours].

### R-INT-7 · Every export is audited after the run, by an auditor held out from the engine

- **Requirement.** Every exported run goes through ScientistOne's four checks after export: score verification, with the harness as its golden evaluator (U-INT-4); specification compliance; reference verification; and method–code alignment [§4.2] [Tab. 7] [Ref: meng2026scientistone §5] [ours]. How the audit runs is task 6's (A-INT-1, A-INT-3; IR-22 to IR-31, IR-36): what it re-fits, its checks of the ledgers and the registry, what a failure does to the report, and an auditor kept apart from every in-loop checker and fixer, with settings from U-EVAL-5 and U-NOTE-4 [ours]. The reporting auditor runs on a model family other than Claude's, on a subscription, never an API; task 4 verifies the Codex CLI for it, and until then every reported count carries task 6's flag (IR-29.3, IR-29.4) [ours]. The audit's record says which parts follow ScientistOne (the four checks, the re-run on a golden evaluator, the majority votes, the lenient rule of alignment) and which are ours (the re-fit of every reported row at every report seed, the checks of the ledgers and the registry, the native number, the harness as the evaluator, the auditor's separation) (IR-22.5, IR-23.2, IR-24) [ours].
- **Traces.** P-INT-5 [§4.2] [Tab. 7]; P-ROSTER-51 [§4.2]; P-EVAL-10 [§4.2] [Tab. 7]; P-ART-6 [p. 47]; P-ART-7 [pp. 48–50].
- **Why ours.** The one audit the paper shows re-ran the agent's own script once, and skipped the baseline [p. 47]; Table 7's first row passes a reward-hacked codebase on score verification, so a re-run shows determinism, not validity [Tab. 7] [fn. 2]. An auditor with the in-loop checker's model and prompt would re-run the gate the loop was optimised against (EI-13). Vlad pays for no API (DEVELOPMENT_PROCESS.md, 2026-10-02), so a family other than Claude's must come through a subscription too, as the coordinating session's amendment A2 to task 6 decided [ours].
- **Depends on.** U-EVAL-5, U-NOTE-4, A-INT-1, A-INT-3 and U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: every export gets four recorded audit results, and four planted defects each fail their own check: a reward-hacked solution, a fabricated citation, a paper–code mismatch, and a reported number that the harness does not reproduce; a configuration whose post-hoc alignment auditor is the in-loop auditor fails validation; a configuration whose reporting auditor shares the authors' family loads, and every reported count carries the flag; one whose auditor bills an API is refused (R-OPS-12) [ours].

### R-INT-8 · Writers see only verified results, and every measurement is the table's

- **Requirement.** The Initial Drafter and the Paper Enhancer read results only from the verified results table (R-STATE-10; U-INT-4); their sandbox holds the manuscript, the table and read-only code, never the run directory. Each number a manuscript presents as a measurement is inserted by engine code from a table entry that the writer names (task 6's G3, IR-21.2; A-INT-1), and every table of results is rendered by engine code, each row from that row's own entries, its caption written from the rows' roles. Until the test event, every entry is a search-role entry (IR-16; U-TOP-5) [§3.5] [ours]. A number in the text, outside a rendered table, binds only to the row *ours* or to a reference row, the baseline or a published number; every other row's values appear only in rendered tables, before the freeze and after the final fill alike [ours]. The rest of the prose around a number stays detection only, by the alignment check and the audit, as task 6 records. What the drafter reads is task 3's (U-DRAFT-1), and the consistency check before export task 6's (A-ART-7) [ours].
- **Traces.** P-DRAFT-1 [§3.5]; P-PEER-5 [§3.5].
- **Why ours.** CLAUDE.md lets the manuscript writer see only verified results; App. D's paper gives three sets of numbers for one method under one protocol (A-ART-7) [pp. 56–71]. A check that a number appears somewhere in the table passes an ablation's number quoted as the method's (EI-5); after the final fill, a writer that can bind any row's cell in the abstract can present the best ablation's test number as the method's, as ScientistOne's audit found a writer doing with ablation scores (the integrity closure, NEW-5) [Ref: meng2026scientistone §6.1] [ours].
- **Depends on.** U-DRAFT-1, task 3; A-ART-7, A-INT-1, U-INT-4 and U-TOP-5, task 6 [ours].
- **Test.** Enforcement, on the toy task, four planted drafts [ours]:
  - one whose main results table holds an ablation entry [ours];
  - one with a number typed by the writer, the published number among them [ours];
  - one with a result figure not rendered from the table [ours];
  - a tail revision whose abstract binds its headline number to the best ablation row's report cell [ours].

  With the guard on, each fails its check before any reviewer reads it or the run exports, and the published number inserted from its entry passes; in the twin whose check only looks for the value somewhere in the table, all four pass. A writer scripted to open the run log finds no such path in its sandbox; in the twin with the run directory mounted, it reads the log [ours].

### R-INT-9 · A judge cannot change what it judges

- **Requirement.** An agent whose output chooses a branch, such as a critic, a verifier, the Selector, a reviewer, the filter or an auditor, has read-only access to the code, results and manuscript it judges, in a fresh session of its own (task 6's IR-26, IR-27.1; A-INT-3). Engine code writes its verdict into the run's records from its output; the judge's session has no write path there, and a verdict found anywhere else has no standing (IR-30). The sandbox policy is task 3's (U-ART-15) [§4.2] [p. 47] [ours].
- **Traces.** P-ROSTER-26 [§4.2]; P-ROSTER-28 [§4.2] [p. 47].
- **Why ours.** Nothing in the paper makes a judge read-only, and the auditor of p. 47 saved its verdict inside the task it audited [p. 47] [ours].
- **Depends on.** A-INT-3, task 6; U-ART-15, task 3 [ours].
- **Test.** Enforcement, on the toy task [ours]:
  - within one subset stage, the coder's write to its workspace succeeds and the filter's write to the same workspace fails on the real sandbox; in the permission twin, with the judge's workspace writable, the filter's write succeeds [ours];
  - a judge scripted to write a passing verdict into the task tree is refused, and the reporter counts only the verdict engine code recorded; in the permission twin the write succeeds and the reporter still ignores it; in the provenance twin, a reporter that reads verdicts from the task tree counts it [ours].

### R-INT-10 · Cross-cutting checks run at hook points declared as data, and each repair is bounded

- **Requirement.** The checks that no stage owns run at hook points declared in data by the kind of step, not by stage, in a stated order; they are the *filters* of task 6's gates on the primitive, and a stage may add a check, never remove one (G2 to G5, IR-40; A-INT-1) [§4.2] [ours]:
  - after a code-producing step: the component-list check (R-STG-4), the switch-scope check where a switch is declared or changed (R-STG-4), the registered-settings check of a rebuttal task's declared evaluation (R-STG-11), the harness's scoring, then the specification filter (U-INT-4) [ours];
  - after a manuscript-producing step, the tail's revision included: compile, number provenance, references, then method–code alignment [ours].

  Each check's failure maps onto the primitive's outcomes (R-PRIM-2): nothing passed on for a candidate, a refinement discarded into its guard's failure branch, or an item dropped; or the hook's nested instance repairs it, which is that instance's refine step, not an outcome. Each invocation of a manuscript hook is one nested instance of the primitive, with its own counter: after any repair, every check of the hook runs again, in order, and at most 2 repairs are made per invocation [ours]. When they are spent before the freeze, the manuscript version is discarded and the last version that passed every check is kept; with none, the run ends with *manuscript gate failed*. In the tail, the run ends without export, *test event done, not exported* (IR-21.6, IR-39.3) [ours].
- **Traces.** none.
- **Why ours.** §4.2 names the checks without placing them in the pipeline, and the first draft ran them at points no stage owned, from a list of stages, with repair loops of no limit (SA-3) [§4.2] [ours]. Two repairs follow the paper's own bound on engineering, N_eng = 2 [App. A.2]. The first revision re-ran only compile after the last hook, so an alignment repair could type a number or a citation that no check saw again (the Codex review, P1; the integrity closure, check 1) [ours].
- **Decides.** U-INT-3, the hooks' order and bound [ours].
- **Depends on.** A-INT-1 and U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode [ours]:
  - a toy result-producing stage added by data has its results checked, scored and filtered with no code change [ours];
  - an alignment repair scripted to type a number is caught by the provenance check, which runs again after it; in the twin that re-runs only compile after the last hook, the number is exported [ours];
  - an unfixable planted citation in a revision before the freeze discards that version, and the last passing version goes on; with no passing version, the run ends with *manuscript gate failed*; in the tail, it ends with *test event done, not exported* [ours];
  - each hook invocation's record holds its own counter, and no invocation makes a third repair [ours].
