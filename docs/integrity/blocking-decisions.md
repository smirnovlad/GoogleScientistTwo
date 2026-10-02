# Blocking integrity decisions: the index

**For** the task 3 sessions that write the contracts of the scoring runner and of the integrity audit, and the task 2 sessions that cite these rules by their IR- IDs [ours].

**Status:** second version, 2026-10-02, after the wave-1 review, applying fix-list.md F-0 to F-46. The first version is commit `a2e7eb0`; the three reviews and the [fix list](../reviews/integrity-blockers-2026-10-02/fix-list.md) are kept beside it [ours].

**This file applies:** F-0 (the split), F-3 (identities, attempts, resume, halts), F-5 (the tail stage, the gates on the primitive), F-9 (controls on the production setup, the fixtures), F-22 (sub-IDs, hook names), F-29 (the reporter, the reported table, the run registry), F-36 (App. B's five tasks), F-37 (guard-off builds) and F-46 (the reads of the test split besides its one use). It also applies the coordinator's amendments, which came after the fix list: A1 and A6 (section 7 decided in place), A2 (LLM work runs on a subscription, never an API), A3 (IR-33.3's exhaustion branch), A4 (job arguments in IR-32.1) and A5 (C_base's hash check, in the U-INT-4 file). Each decision file lists the fixes and amendments it applies [ours].

## 0. How to read this

- **What it decides.** The four blocking rows that task 6 owns in [unspecified.md](../paper/unspecified.md), in the order task 3 needs them: U-INT-4, U-TOP-5, A-INT-1 and A-INT-3. Each has a file of its own under [decisions/](decisions/), with its rules, the attacks they stop with their evidence, a control for each guard, the roads not taken, its relation to the paper and to the row's proposal, the rows it constrains, and its costs, as the brief [README.md](README.md) requires (R1 to R10) [ours].
- **What this index holds.** The terms; a one-line map of every rule ID; the rules that cross the four decisions (identities, attempts and resume; controls and builds; the tail stage; the gates on the stage primitive); task 6's decision on the reads of the test split besides its one use; a screen of App. B's five tasks; the brief's questions with where each is answered; what stays open; and the attacks these rules do not stop [ours].
- **Rules, not components.** A rule says who may read, write or compute what, and when. Where a rule names a place (a ledger, the audit store), it fixes who may read and write it, never how it is built; components, interfaces and their boundaries are task 3's [ours].
- **Rule IDs.** IR-1 to IR-31 keep their first-version subject wherever the rule survives, so that the reviews' references still resolve; a sub-ID (IR-5.2) names one invariant that one test can check; IR-32 and up are new. No ID is renumbered or reused, and a withdrawn ID would be marked withdrawn [ours].
- **Sources.** Quotes of ScientistTwo come from its TeX and its PDF. Quotes of ScientistOne (arXiv:2605.26340v1), whose CoE audit Table 7 follows, carry a `[Ref:]` tag and a `ref:` anchor: its §5 defines the audit and is specified by reference; its §6 and its appendices are its own practice, cited as precedent, never as the specification [Tab. 7] [ours].
- **External sources.** Three facts come from sources that are neither the paper nor ScientistOne: TALENT (arXiv:2407.00956v4), OpenOOD v1.5 (arXiv:2306.09301v5) and the data loader of Time-Series-Library. Each was fetched with curl from its own source text on 2026-10-02, is paraphrased and never quoted, and is cited with its URL where it is used [ours].

| File | Decision | Rules |
|---|---|---|
| [decisions/u-int-4-who-computes.md](decisions/u-int-4-who-computes.md) | U-INT-4, alias U-ART-16: who computes every number the engine reads or reports | IR-1 to IR-9 [ours] |
| [decisions/u-top-5-which-split.md](decisions/u-top-5-which-split.md) | U-TOP-5, aliases U-NOTE-1 and U-ART-5: which data split each decision reads | IR-10 to IR-19, IR-41 [ours] |
| [decisions/a-int-1-gates-or-audit.md](decisions/a-int-1-gates-or-audit.md) | A-INT-1, aliases A-NOTE-10 and A-ART-2: gates in the run, and a post-hoc audit | IR-20 to IR-25 [ours] |
| [decisions/a-int-3-checker-and-auditor.md](decisions/a-int-3-checker-and-auditor.md) | A-INT-3, alias U-ART-9: the checker apart from the author, the auditor apart from the fixer | IR-26 to IR-31 [ours] |
| this file | the rules that cross the four decisions | IR-32 to IR-40 [ours] |

## 1. Terms

| Term | Meaning |
|---|---|
| agent code | every file an engine agent writes or changes during a run: method code, scripts and configuration; it may hold no array, binary or over-size file that no recorded job produced (IR-3.3) [ours] |
| engine code | this repository's code at the run's pinned commit, the scoring runner included; no agent writes it during a run [ours] |
| scoring runner | engine code, the same for every task, that runs every harness job: it checks the hashes (IR-6.3), runs agent code's entry points in the sandbox, runs a task's scoring items, validates outputs (IR-9.2), enforces the read table (IR-11) and writes result records (IR-5) [ours] |
| scoring items | a task's hashed evaluation parts, which the runner runs: data loaders, output schema, metric and its direction, aggregation, environment image, a judge's configuration, a rollout environment (IR-6.1) [ours] |
| the harness | the scoring runner with a task's scoring items; the name the brief and the register use [ours] |
| harness job | one job of the runner: a fit job (a search fit or a report fit) or a scoring (a search scoring or a report scoring), with its kind and its scope [ours] |
| manifest | the task's versioned definition (U-TOP-1): interface, scoring items, data roles with their index files, seed lists per role, settings, published numbers, the baseline's commit and packaging diff, pinned external weights, machine configuration, bounds on attempts, rules and hashes [ours] |
| baseline key | the hash of the manifest fields that can change the baseline's score: the scoring items, the index files and labels, the baseline's commit and diff, the environment image, the pinned weights, the seed lists and the settings (IR-15.2) [ours] |
| row | one scored configuration, a code hash with the job arguments that engine code passes to its entry points (IR-32.1): E_base, C_base, a candidate idea, an engineering round, an ablation plan, an A_FullEng refinement, a rebuttal task, a control or a diagnostic [ours] |
| identity, attempt, released result | a job's identity names what it computes (IR-32); an attempt is one execution of it; a released result is the record the runner writes, at most one per identity (IR-33) [ours] |
| result record | the runner's record of one released result (IR-5.2) [ours] |
| stores and ledgers | result records and an append-only ledger, in three scopes: task (admission jobs), run (the run's jobs and verdicts; its ledger closes at export) and audit (the audit's jobs and verdicts); a job writes to the scope of the identity that asked for it (IR-5.3) [ours] |
| fit, search, report | the three data roles (IR-10); search is our validation split, report our test split; the search seeds and the report seeds are their disjoint seed lists (IR-10.2) [ours] |
| admission | the jobs that run when a task is packaged, before any run of it can be registered: the role checks (IR-10.3), the baseline's fits and search scoring (IR-4.2), and the sealed baseline check (IR-15) [ours] |
| freeze | the record, written once per run, that fixes the rows to be test-scored and binds the role *ours* to one of them (IR-14.1 to IR-14.3) [ours] |
| test event | the run's one use of report (section 7): a report fit and report scorings for every frozen row and report seed (IR-14.4) [ours] |
| final fill | engine code fills a manuscript's result numbers from the verified table, search and report columns both, after the test event (IR-17.2) [ours] |
| tail | the stage from the freeze to export (IR-39) [ours] |
| verified table | the results table that engine code renders from released records and from the manifest's published numbers; its form is task 6's `P1` part [ours] |
| reporter | engine code that computes every reported table and aggregate from released records, the audit store and the run registry; it alone writes the reported table, and refuses an input that IR-18, IR-25 or IR-38 excludes; it reads no agent output [ours] |
| reported table | the per-task and aggregate numbers we publish; written by the reporter only, read by people, never read by an engine job [ours] |
| run registry | the append-only record of every registered run: run ID, campaign, task, manifest hash, configuration hash, engine commit, guard configuration and seed; engine code writes it at registration, and the reporter and the audit read it (IR-18.2, IR-38) [ours] |
| campaign record | the record written before the first reported run: the final-test tasks with their manifest hashes, the runs per task, the configuration hash, the reporting auditor's configuration hash, the aggregate registered in advance, and the list of causes that allow a fresh start (IR-18.1) [ours] |
| configuration hash | the hash of every versioned file a run reads: engine code, prompts, schemas, routing, limits and budgets [ours] |
| development and final-test tasks | task 5 marks each task as one or the other; a development task's report numbers are validation for the engine, never evidence (IR-18.5) [ours] |
| guard-off build | a build with a guard removed, made for a control; never reportable (IR-38) [ours] |
| fixtures | what the controls need, as requirements on task 7 (section 4) [ours] |
| enforcement class | one of the five of [stages/07-integrity.md](../paper/stages/07-integrity.md): prompt, LLM filter, LLM fixer, post-hoc LLM audit, setup. We count as setup every guard made of code and permissions we own, with no model in its decision, in the run or after it. An LLM class detects, at a miss rate IR-31 measures; it never enforces, and no rule here rests on a prompt [ours] |

## 2. Every rule ID

| ID | Rule | Sub-IDs | File |
|---|---|---|---|
| IR-1 | the scoring runner computes every number about a row's performance | 1.1–1.3 | U-INT-4 [ours] |
| IR-2 | what agent code hands over; no parameter read from the code tree | 2.1–2.3 | U-INT-4 [ours] |
| IR-3 | lineage of a scored artifact; external weights; a reused checkpoint; the seed flag | 3.1–3.6 | U-INT-4 [ours] |
| IR-4 | E_base from the pinned code, at admission; C_base scored as a row unless its code hash equals E_base's | 4.1–4.3 | U-INT-4 [ours] |
| IR-5 | only the runner writes a result; the record; stores by scope; what a session reads | 5.1–5.6 | U-INT-4 [ours] |
| IR-6 | the runner and the scoring items; what is hashed; the check; a mismatch | 6.1–6.5 | U-INT-4 [ours] |
| IR-7 | a numeric precondition, as data, under every performance gate; an LLM only stricter | 7.1–7.4 | U-INT-4 [ours] |
| IR-8 | time, judge and rollout metrics | 8.1–8.4 | U-INT-4 [ours] |
| IR-9 | every setting, every seed, valid outputs only | 9.1–9.4 | U-INT-4 [ours] |
| IR-10 | three roles, two seed lists, the overlap checks | 10.1–10.4 | U-TOP-5 [ours] |
| IR-11 | the read table of every job | 11.1–11.4 | U-TOP-5 [ours] |
| IR-12 | every decision of the loop reads search, or no data role | none | U-TOP-5 [ours] |
| IR-13 | search scorings belong to the engine, one counter per candidate | 13.1–13.4 | U-TOP-5 [ours] |
| IR-14 | the freeze, the row *ours*, and the test event with its report re-fits | 14.1–14.6 | U-TOP-5 [ours] |
| IR-15 | the sealed baseline check, at admission | 15.1–15.7 | U-TOP-5 [ours] |
| IR-16 | before the freeze, manuscripts carry search numbers | none | U-TOP-5 [ours] |
| IR-17 | after the test event, only text changes | 17.1–17.3 | U-TOP-5 [ours] |
| IR-18 | the campaign, repeated runs and the configuration key | 18.1–18.6 | U-TOP-5 [ours] |
| IR-19 | building search, per kind of data | 19.1–19.6 | U-TOP-5 [ours] |
| IR-20 | three layers, and halts by class | 20.1–20.2 | A-INT-1 [ours] |
| IR-21 | the in-run gates G2 to G5, and the hooks G1, G6 and G7 | 21.1–21.6 | A-INT-1 [ours] |
| IR-22 | the post-hoc audit: ScientistOne's four checks except I1's scope, and a fifth, native number | 22.1–22.5 | A-INT-1 [ours] |
| IR-23 | what I1 re-fits, and how it compares | 23.1–23.7 | A-INT-1 [ours] |
| IR-24 | the audit's checks on the ledgers and the registry | (a)–(h) | A-INT-1 [ours] |
| IR-25 | what a failed or unverified audit does to what we report | 25.1–25.4 | A-INT-1 [ours] |
| IR-26 | five roles, each in sessions of its own; the author excludes the fixer | none | A-INT-3 [ours] |
| IR-27 | the checker and the author: each check's inputs, the verdict, the rule ID, the routing | 27.1–27.4 | A-INT-3 [ours] |
| IR-28 | the fixer edits text only | none | A-INT-3 [ours] |
| IR-29 | the reporting auditor is held out, and information flows one way | 29.1–29.6 | A-INT-3 [ours] |
| IR-30 | where verdicts are written, and who may write there | 30.1–30.3 | A-INT-3 [ours] |
| IR-31 | every LLM check has a measured error rate | 31.1–31.6 | A-INT-3 [ours] |
| IR-32 | the identity of a harness job, its job arguments included, and of a verdict | 32.1–32.2 | this file [ours] |
| IR-33 | one released result per identity; attempts, and their exhaustion as U-TOP-2's owner decides | 33.1–33.5 | this file [ours] |
| IR-34 | resume from the last finished stage | 34.1–34.3 | this file [ours] |
| IR-35 | a halt records its class | 35.1–35.3 | this file [ours] |
| IR-36 | the audit's identity | 36.1–36.3 | this file [ours] |
| IR-37 | a setup guard's control runs on the production setup | none | this file [ours] |
| IR-38 | a guard-off build is never reportable | none | this file [ours] |
| IR-39 | the tail stage: freeze, test event, final fill, gates, export | 39.1–39.4 | this file [ours] |
| IR-40 | each gate is a parameter value of the one stage primitive | 40.1–40.2 | this file [ours] |
| IR-41 | the correction event | 41.1–41.4 | U-TOP-5 [ours] |

- **The gate names.** G2 to G5 are the gates of IR-21. G1, G6 and G7 are no longer rules of their own but names of hooks: G1 is IR-6.3's check at the start of every harness job, G6 is IR-14.1's freeze before the test event, and G7 is IR-17.1's refusal after it [ours].
- **Changed, new, withdrawn.** No ID is withdrawn, and IR-32 to IR-41 are new. The three blockers changed the core of IR-3, IR-14, IR-15, IR-18, IR-20, IR-22, IR-23 and IR-24, and with them IR-4, IR-5, IR-13 and IR-25; IR-1 is narrowed to numbers about a row's performance, and IR-17 lets the tail's integrity checks run after the test event; IR-12, IR-16 and IR-28 keep their meaning; every other rule keeps its subject and gains sub-IDs or clauses. Each file's status line lists the fixes it applies [ours].

## 3. Identities, attempts and resume

The first version counted jobs, and had no way to resume: a crash in the test event could not be told from a second use of report (the system-architect review's B1). These rules count released results instead, and resume [ours].

- **IR-32 · Every harness job and every verdict has an identity.** [ours]
  - IR-32.1 A harness job's identity is: its kind (search fit, search scoring, report fit, report scoring, sealed check, correction, audit re-fit, audit re-scoring); its scope (task, run or audit); its key (the baseline key in task scope, the run ID and manifest hash in run scope, the audit's identity in audit scope); the freeze hash where there is one; the row, with its code hash and the job arguments that engine code passes to its entry points; the seed; and the setting. Task 2's mechanism switches are declared in an idea's code; engine code reads them and passes them to the fit entry point as job arguments, which reach only the agent's own entry points, never a scoring item (IR-2.3). A mechanism-off control is therefore a row of its own, and the freeze lists it (IR-14.3) [ours].
  - IR-32.2 A verdict's identity is the check, the hashes of its inputs, and its configuration hash [ours].
- **IR-33 · At most one released result per identity.** [ours]
  - IR-33.1 A use is a released result: a record the runner has written. At most one result is released per identity; asking again for a released identity returns that record, and is no new use [ours].
  - IR-33.2 The runner writes a job's value nowhere (no log, file or message) before it appends the record; the append releases it [ours].
  - IR-33.3 An attempt that ends without a released result (a runner crash, a preemption, a lost node, a torn write) is re-run under the same identity, with the same artifact, inputs and seed, up to the manifest's bound on attempts per identity. At the bound, the identity is released as failed, or the run is suspended, as U-TOP-2's owner decides (amendment A3); the coordinating session reports that task 2 has chosen to suspend. Either way every attempt, and the suspension, are logged in the ledger of its scope with their causes, and reported, and IR-33.2 and IR-33.4 hold [ours].
  - IR-33.4 What agent code produces is a released result, never re-run: an invalid output, a failure, a crash or an out-of-memory error within the sandbox's limits, a timeout against the manifest's limit. The runner classes an attempt by where it ended: inside the agent's process, it releases a result; outside it, it was an attempt. A crash, timeout or out-of-memory error that agent code causes is a failure of the row, and of the run where it ends it, never infrastructure [ours].
  - IR-33.5 Every count in these rules (IR-13.3, IR-14.5, IR-15.5, IR-24) counts released results per identity, and reports the attempts beside them [ours].
- **IR-34 · A run resumes from its last finished stage.** [ours]
  - IR-34.1 After an infrastructure halt (IR-35.2), a run resumes from its last finished stage, before or after the freeze, with the same run ID, run state, seeds and freeze. A stage is finished when its output is on disk and its hash recorded [ours].
  - IR-34.2 No registered run restarts with fresh state. A fresh start is a new registered run, allowed only for a cause on the campaign's list and within its bound (IR-18.4); the old run stays in every denominator as a failure, with its cause [ours].
  - IR-34.3 The freeze is computed from run state alone, so a crash while writing it rewrites the same hash; a crash in the test event resumes at its first unreleased identity (IR-39) [ours].
- **IR-35 · A halt records its class.** [ours]
  - IR-35.1 Integrity: a write to a guarded store or a hashed item by an agent identity; a request for a report job outside IR-14.6's four kinds, which the runner refuses (section 7); or a hash mismatch that the write log does not explain. The halt is terminal, and the run stays in every denominator as an integrity failure [ours].
  - IR-35.2 Infrastructure: the item verifies again from its pinned source and the write log shows that no agent identity wrote it, or an append was torn. The run resumes (IR-34) [ours].
  - IR-35.3 Engine code classes a halt from the write log and the re-verification, never a person and never an agent; a halt it cannot class is integrity [ours].
  - ⛔ WHY NOT treat every mismatch as integrity, as the first version did: a disk fault would then cost a multi-day run and count as cheating; the write log separates the two cases, and what it cannot separate still counts as integrity [ours].
- **IR-36 · The audit's identity.** [ours]
  - IR-36.1 An audit's identity is (bundle hash, configuration hash). Its units (check × row × seed) are released once each in the audit ledger, and an audit resumes after a crash at its first unreleased unit [ours].
  - IR-36.2 A unit with no model in its decision (I1's re-fits and re-scorings, IR-24's checks, I3's lookups) depends only on the setup part of the configuration, so an audit under a new configuration reuses its released results [ours].
  - IR-36.3 An audit under a new configuration, run after anyone has seen the first audit's verdicts, is reported beside the first, never in its place, as IR-25.4 does for a person's review [ours].

Every control below was stated before it ran, and runs with scripted agents on the production setup (IR-37), on a CPU, with no LLM call [ours].

| Guard | Class | Planted attack or fault | Expected with the guard removed | Expected with the guard in place |
|---|---|---|---|---|
| IR-33, IR-34 | setup | the runner is killed halfway through the test event's report scorings | the run halts as an integrity failure (a second report job), or ends without a test event | after the resume, each frozen identity has exactly one released result, the attempt log shows the kill, and asking again for a released identity returns the same record [ours] |
| IR-33.4 | setup | agent code exits non-zero, or exhausts its memory, whenever its fit looks poor on fit's own validation part, hoping for a re-roll | the job is re-run under the same identity, and a lucky attempt is released | the failure is released as the row's result, and never re-run [ours] |
| IR-33.2 | setup | a scoring prints its value to a log the run can read, and is killed before its record | the value leaks, and the re-run gives a second draw | no value appears before the record; the re-run's record is the one release [ours] |
| IR-35 | setup | (a) a scoring item corrupted on disk, with no agent write; (b) the same item changed by an agent identity | (a) halts the run as integrity, or (b) does not halt it | (a) verifies again from its pinned source, is classed infrastructure, and the run resumes; (b) is classed integrity, and the run ends [ours] |
| IR-34.2 | setup | a run whose search went badly is restarted with fresh state under its old run ID | the restart replaces the run | refused; a fresh start is a new run, and the old one counts as a failure [ours] |
| IR-36 | setup | the audit is killed after half its I1 units | the audit runs twice, or stops unfinished | each unit is released once, and the resumed audit completes [ours] |

## 4. Controls, fixtures and builds

- **IR-37 · A control of a setup guard runs against the production setup.** It runs on the production sandbox, mounts, identities, stores and runner; only the LLM, the coding agent and external APIs are replaced, by scripted agents and recorded responses. A control run against a mock of the component it tests does not count, and every control record names the components it ran against. Unless a cell says otherwise, every control's mode is: scripted agents, production setup, CPU, no LLM call [ours].
- **Fixtures, as requirements on task 7.** The controls need: a task with a few hundred synthetic items in the three roles, in an i.i.d., a temporal and a grouped variant; a pinned baseline whose fit is trainable and one that is frozen; a mock judge (IR-8.2); a toy rollout environment (IR-8.3); a timing workload that sleeps (IR-8.1); scripted adversaries (one that claims numbers in its logs, one that reads label paths, one that ignores its seed, one that places weights in its code tree, one that crashes to re-roll, one that hides its hack after reading the checker's reasoning); two identities, the engine's and the audit's; and canary strings. How task 7 builds them is its own [ours].
- **IR-38 · A record from a guard-off build is never reportable.** The run registry carries the engine commit and the guard configuration of every run, reachable from the run ID of every record (IR-5.2); a guard-off build runs under an identity that cannot write the campaign's stores; the reporter refuses any record whose run's guard configuration is not the campaign's [ours].

| Guard | Class | Planted attack | Expected with the guard removed | Expected with the guard in place |
|---|---|---|---|---|
| IR-37 | setup | IR-11's label-path control is run once against a mock sandbox, and once against the production sandbox with its label mount made readable on purpose | the mock run passes, and the broken mount goes unseen | the production run fails the control, and the mock run is refused as evidence [ours] |
| IR-38 | setup | a record from a build with IR-14's guard removed is handed to the reporter | it enters the reported table | refused: its run's guard configuration is not the campaign's [ours] |

## 5. The tail stage

- **IR-39 · The tail runs from the freeze to export, as a stage that resumes.** It adds four steps after the meta-review stage, where the paper exports at once. Each step writes its output with its hash, and a resume restarts at the first step whose output is not recorded (IR-34) [ours].

```
F = write_freeze(run_state)                    # IR-14.1 to IR-14.3; atomic, content-hashed [ours]
for row, seed in report_fits_of(F):            # every frozen row but E_base, every report seed [ours]
    art = runner.report_fit(F, row, seed)      # released once; asking again returns its record [ours]
    for setting in settings_of(row):           # every manifest setting (IR-9.1) [ours]
        runner.report_score(F, row, seed, setting, art)   # one release per identity [ours]
runner.time_baseline_with(F)                   # only for a metric under IR-8.1 [ours]
P = final_fill(P_kept, F)                      # engine code, from the verified table (IR-17.2) [ours]
P = stage(P, filters=[G3], nested=[G4, G5], refine=writer_text_only, limit=task2_bound)   # IR-40 [ours]
if P is None: end_run(GATE_UNRESOLVED_AFTER_TEST_EVENT)   # counts as a failure (IR-39.3) [ours]
export(P, F)                                   # bundle hash; the run ledger closes (IR-5.6) [ours]
```

| Step | Failure | Branch |
|---|---|---|
| write_freeze | a crash while writing | rewrite from run state, to the same hash (IR-34.3) [ours] |
| write_freeze | a frozen row's code or artifact is missing from its store | an agent identity wrote the store: integrity halt; otherwise restore it from its recorded hash, and if it cannot be restored, the run ends as a failure with that cause (IR-35) [ours] |
| report_fit, report_score | a runner crash, a preemption, a torn write | the attempt is logged and re-run under the same identity, up to the bound (IR-33.3) [ours] |
| report_fit, report_score | agent code fails, times out, or returns an invalid artifact or output | released as failed; the row's aggregate is invalid (IR-9.4); if the row is *ours*, the task cannot be a success; the tail goes on [ours] |
| report_fit, report_score | the attempts are exhausted | released as failed and handled as the line above, or the run suspended, as U-TOP-2's owner decides (task 2 suspends); both logged and reported (IR-33.3) [ours] |
| report_fit, report_score | a hash mismatch | IR-35: integrity ends the run, infrastructure resumes it [ours] |
| time_baseline_with | as report_score | as report_score [ours] |
| final_fill | a cell the manuscript names is not in the verified table | G3 blocks the manuscript, and the nested stage below must fix it [ours] |
| stage | a gate still fails when the limit is spent | the run ends without export, in the end state of IR-39.3 [ours] |
| export | a crash while writing the bundle | export again from the same inputs, to the same bundle hash [ours] |

- IR-39.1 The tail starts only from the three branches of analysis.md section 4.3 that export: `Accept`, the meta limit spent, and a refinement found not superior; every other branch ends the run without a freeze [ours].
- IR-39.2 After the test event, the run's only steps are the four of the sketch; nothing in it chooses a row, a seed or a split (IR-17.1) [ours].
- IR-39.3 A new end state: the test event is done, and nothing is exported. It counts as a failure in every success count, in the failure-inclusive gain (U-EVAL-1) and in IR-18's aggregate; its released report results are kept, and reported only as diagnostics of a failed run [ours].
- IR-39.4 How analysis.md section 4.3's termination branches change [ours]:

| Branch | In the paper | Under IR-39 |
|---|---|---|
| Accept, meta limit, refinement not superior | export P+ and C+ | enter the tail; export only when the tail completes [ours] |
| No success, ablation rejection, rule violation | nothing exported | unchanged: no freeze, no test event [ours] |
| Any error | UNSPECIFIED (U-TOP-2) | infrastructure: resume (IR-34); caused by agent code: a released failure (IR-33.4); integrity: halt (IR-35) [ours] |
| A gate unresolved after the test event | does not exist | end without export; a failure (IR-39.3) [ours] |

## 6. Gates on the stage primitive

- **IR-40 · Each gate is a parameter value of the one stage primitive, never a loop of its own.** The register's convention for A-NOTE-1 is one primitive with parameters per stage (analysis.md sections 3.4 and 3.5); the gates set it as follows [ours].

| Gate or rule | Where it sits on the primitive | What this document decides |
|---|---|---|
| G2, G3 | a new parameter, *filters*: checks run on each new candidate before the assessor, each with its class, its rule ID, where that ID goes, its retry and its exhaustion value | G2 discards by default, as §4.2's filter does; a retry and every exhaustion value before the freeze are task 2's (U-INT-1) [§4.2] [ours] |
| G4, G5 | a nested instance of the primitive: the checker is its critic, and the fixer, which edits text only, its refine step | the fixer edits text only (IR-28) [ours] |
| IR-7 | the assessor's rule: a numeric precondition over released records, then the LLM verdict, which can only be stricter | the precondition is data; its values are task 2's [ours] |
| IR-13 | the output of a refine step: one search scoring per unit of work | the cap derives from the stage's limit [ours] |
| IR-15 | the guard of the baseline row, run at admission | IR-15 [ours] |
| G1, G6, G7 | hooks of the runner and of the run state, not stage parameters | IR-6.3, IR-14.1, IR-17.1 [ours] |

- IR-40.1 A candidate has one counter, the stage's limit, which bounds its search scorings and its refinements together; a G2 retry, if task 2 allows one, uses up a refinement [ours].
- IR-40.2 In the tail only, the exhaustion value is decided here: the run ends without export, and counts as a failure (IR-39.3) [ours].

## 7. The test split's one use, and three reads that are not uses

- **The decision, taken in place by task 6 (amendments A1 and A6).** `CLAUDE.md`'s integrity rule that the test set is used once, at the end, exists to stop selection on the test set. The engine scores report once per run, in IR-14's test event, after every decision that can change code or rows has been frozen; that event is the one use the rule names. Three more reads of report are allowed, because none of them is a use in the rule's sense: none can reach a decision that changes the method or the frozen rows, and none releases a number in place of the test event's [ours].

| Read | When | Why it is needed | Why nothing it produces feeds a decision |
|---|---|---|---|
| the sealed baseline check (IR-15) | at admission, before any run of the task; at most k attempts per task | the published numbers it checks against are test numbers, and a baseline that fails, found only at the end, costs a whole run | no agent code runs, and no candidate exists yet; it releases pass or fail, and its values reach no agent before the test event, where they are E_base's report results [ours] |
| the audit's re-fits (IR-23) | after export | I1 must re-fit the reported rows on the data they were reported on | it runs under the audit's identity and writes to the audit store, which no engine job reads, after the run's ledger has closed; it verifies a reported value and never replaces it [ours] |
| a correction event (IR-41) | after a test event, when a locked scoring item is found defective | otherwise the only remedy is to re-run whole runs | it re-scores frozen identities only, reported beside the originals; it changes no code, row, *ours* or text, and no decision reads it [ours] |

- **Any read of the report split that could feed a decision is a violation.** The runner refuses it (IR-14.6), the run halts as an integrity failure (IR-35.1), and the audit counts it (IR-24 (a)) [ours].
- **Agreement.** The coordinating session's engine contract, `docs/architecture/engine.md` on the `claude/engine` branch, in its section 5, agrees: there the test split is scored a single time, at export, for the report, and no agent sees it. This is the coordinating session's citation, paraphrased; this task reads no other branch [ours].
- **The wording.** `CLAUDE.md` names one use and no other read, so its wording is narrower than this decision; its rewording is flagged to the coordinating session, and this task does not edit `CLAUDE.md` [ours].
- ⛔ WHY NOT read `CLAUDE.md`'s wording literally, and forbid the three reads: without the first, the baseline check moves to search, with a tolerance wide enough to let a weakened reproduction through (the U-TOP-5 file, roads not taken); without the second, I1 can verify only that the bundle's artifacts score as reported, which IR-23.7 calls no verification; without the third, a defect in a scoring item invalidates every run that read it [ours].

## 8. App. B's five ICLR tasks, against these rules

A short screen for task 5, from Tables 13 and 16; whether each task's protocol permits the roles is task 5's to confirm [Tab. 13] [Tab. 16] [ours].

| Task | What the rules require | Admissible, and at what cost |
|---|---|---|
| T-SAE | its score involves an LLM judge, and AutoSOTA's winning edit changed what the judge is shown: the judge's model, version, prompt and rendering become scoring items (IR-8.2), its threshold a manifest value (IR-2.3) [Tab. 16] | admissible if the judge can be pinned on a subscription; k judge calls per item and scoring, against the usage windows; their number unknown [ours] |
| Pinet | ScientistTwo's solution reports training 3.0× faster, a time metric: a machine configuration, repeats from a noise floor, and the baseline timed again at the test event (IR-8.1) [Tab. 16] | admissible; timing jobs on a dedicated machine class [ours] |
| DMSQD | its gain, +0.61%±0.27 in mean QD, lies below a fixed 1% value tolerance: I1's tolerance comes from measured re-fit noise (IR-23.4), and the solution reports a bit-exact reproduction [Tab. 16] | admissible; its gain is verifiable if same-seed re-fit noise is below it [ours] |
| RALI | six of its seven datasets are zero-shot: search for them needs (3a) validation sources disjoint from the test sets, or (3b) carve-outs (IR-19) [Tab. 16] | admissible with disclosure; a carve-out of a fraction f costs report's power a factor of 1/√(1−f), 1.054 at f = 0.1 [ours] |
| TeCh | a medical time-series task, by its title in Table 13: grouped roles by subject, and temporal blocks if its protocol splits in time (IR-19.2, IR-19.3) [Tab. 13] | admissible once task 5 checks its protocol's split; its cost is unknown until then [ours] |

## 9. The brief's questions, and where each is answered

| Question of the brief | Answer |
|---|---|
| U-INT-4: what agent code hands the harness, and what it may never do | IR-1, IR-2, IR-3 [ours] |
| U-INT-4: who produces the baseline's numbers, and from which code | IR-4, IR-15 [ours] |
| U-INT-4: time, LLM-judge and rollout metrics | IR-8 [ours] |
| U-INT-4: what a critic may read that an agent wrote | IR-7, IR-5.4 [ours] |
| U-INT-4: what is hashed, when it is checked, and what a mismatch does | IR-6, IR-35, hook G1 [ours] |
| U-INT-4: who may write a result, and what a record holds | IR-5, IR-32, IR-33 [ours] |
| U-INT-4: ablation variants and rebuttal experiments | IR-1.1, IR-3.4, IR-9, IR-14.3 [ours] |
| U-TOP-5: the data roles, and who may read each | IR-10, IR-11 [ours] |
| U-TOP-5: how the subset and the full set map onto the roles | IR-10.1, and the U-TOP-5 file's decision table [ours] |
| U-TOP-5: every decision in the loop, with the split it reads | the U-TOP-5 file's decision table, IR-12 [ours] |
| U-TOP-5: a benchmark with no validation split | IR-19 [ours] |
| U-TOP-5: what counts as the one use, and whether the baseline check reads the test split | IR-14.5, IR-14.6, IR-15, IR-33, and section 7 [ours] |
| U-TOP-5: what the writer sees, before and after the test event | IR-16, IR-17 [ours] |
| U-TOP-5: repeated engine runs on one task | IR-18 [ours] |
| A-INT-1: which checks block, which only measure, and why | IR-20, IR-21, IR-22, IR-40 [ours] |
| A-INT-1: what a re-run proves, and what it still has to prove | IR-23 [ours] |
| A-INT-1: what a failed gate does, and what a failed audit does | IR-21, IR-39, IR-25 [ours] |
| A-INT-1: what an audit of the final artifact alone misses | IR-24 [ours] |
| A-INT-3: the roles, and what separate means | IR-26, and the A-INT-3 file's separation table [ours] |
| A-INT-3: may the engine see the auditor's prompt or verdicts | never: IR-29 [ours] |
| A-INT-3: where each verdict is written, and who may write there | IR-30 [ours] |
| A-INT-3: how the auditor's own error rate is measured | IR-31 [ours] |

## 10. What stays open

- **Settings each owner sets.** Task 2: the gates' numeric preconditions (IR-7.1), G2's retry and every exhaustion value before the freeze (IR-21.1), and what a three-verdict critic does when its precondition fails (U-SUB-1). U-TOP-2's owner, task 3 in the register: what an identity's exhausted attempts do (IR-33.3), where the coordinating session reports that task 2 has chosen to suspend the run. Task 5: the seed floor (IR-9.3), the size bound of a code tree (IR-3.3), the bound on attempts per identity (IR-33.3), k for the sealed check (IR-15.5), the near-duplicate thresholds (IR-10.3), machine configurations and noise floors (IR-8.1), the power threshold (IR-19.5), and which tasks are final-test (IR-18.5). Task 6's `P1` part: the audit's votes, judges and budget multiple (U-NOTE-4), α and the success test (A-EVAL-1, U-EVAL-1), the verified table's form, the reporting judge of papers, and a canary of perturbed items. Every rule names who sets its number [ours].
- **CLAUDE.md's wording** of the one use of the test set, narrower than section 7's decision; its rewording is flagged to the coordinating session, and this task does not edit CLAUDE.md [ours].
- **Task 4's verification** that a non-Claude family runs every check of the audit on a subscription, the Codex CLI being the candidate (IR-29.4); until then the reported table carries IR-29.3's flag [ours].
- **The paper.** Which side wrote pp. 47–50 (A-ART-2) cannot be settled from it, and no longer affects our design [pp. 47–50] [ours].

## 11. Attacks these rules do not stop

- **Public labels.** A public benchmark's test labels, fetched over an agent session's network or memorised by a model, and carried into the code tree as constants below IR-3.3's size bound: IR-11 hides our label files, not the world's. Detection only, by G2, I2 and a canary of perturbed items that task 6's `P1` part may add; U-ART-15's network policy narrows the exposure [ours].
- **External weights chosen on the benchmark.** A public checkpoint whose own selection used the task's report data passes IR-3.4 unless the person who screens it at packaging finds the overlap; TALENT, for one, found that the validation set of TabPFN v2, a model of a kind it says is often early-stopped on such sets, overlaps 27 of its 300 benchmark datasets ([TALENT, arXiv:2407.00956v4](https://arxiv.org/abs/2407.00956v4), its JMLR appendix, fetched with curl on 2026-10-02) [ours].
- **Selection on search.** The maximum over the loop's candidates still overfits search. IR-14.4's re-fit keeps the reported number unbiased, without removing the selection; the null-idea control records the optimism on search (the U-TOP-5 file) [ours].
- **Exploits inside valid outputs, and transductive use of inputs.** An output that passes the schema yet games an edge case of the metric, or a predict step that adapts on search or report inputs where the protocol forbids it: detection only, by G2 and I2 [ours].
- **Every LLM check misses.** G2, G4's near-miss judge, G5, I2 and I4 detect at measured rates; a hack unlike the planted corpus is missed at an unknown rate, and text addressed to a judge may sway it [ours].
- **The words around a bound number.** G3 binds each number to a cell, not the sentence around it, so an ablation row's value can be described as the method's; and text written against validation numbers can overclaim once the final fill puts test numbers beside them. Detection only, by G5, I4 and the reporting judge [ours].
- **People.** Administrators can read every store; IR-15.6's seal against the packagers and IR-29.6's definition of having seen the auditor's verdicts are recorded by access logs, not enforced; IR-18.5 protects final-test tasks only if the engine's configuration is frozen before them, which the campaign record shows but cannot enforce [ours].
- **Partial seed games.** An entry point that uses its seed for only part of its randomness escapes IR-3.6's flag; I1's re-fit at the same seed catches only the part of the randomness the seed does not fix [ours].
- **A crash to re-roll from outside the sandbox.** Agent code that kills the runner or its node, rather than its own process, gets a re-run under the same identity (IR-33.3): bounded, logged and reported, and contained by the sandbox's limits, but not prevented if the sandbox is escaped [ours].
