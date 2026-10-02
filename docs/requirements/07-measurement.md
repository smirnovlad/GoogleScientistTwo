# Requirements 7 · What the replication measures and reports

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
These requirements cover the numbers a run produces about itself: success, gains, review scores, cost
and time [§4] [ours]. How each is defined is mostly task 6's to decide, or task 5's for cost; these
requirements fix what must be recorded, so that any definition chosen later can be computed from the
records [ours]. `docs/paper/traceability.md` Part 3 says which of the paper's numbers are fair
targets; matching the paper's own numbers is not part of the goal [ours].

### R-MEAS-1 · Success is reported under all three readings

- **Requirement.** For every task, the report states three facts, each from the run's records [Fig. 1] [Tab. 3] [Tab. 15] [§3.3] [ours]:
  - at least one idea was `Good` on the full set [§3.3];
  - the gain over the human state of the art, from the report-role records of the test event, passes the success test that task 6 sets, pre-registered and one-sided, never the sign of a point estimate (A-EVAL-1, U-EVAL-1; U-TOP-5) [Fig. 1] [ours];
  - the gain is attributed: the exported pass ended with an ablation `Good` that stood, the export is not marked *attribution not established*, and at the test event *ours* minus its mechanism-off control, paired per report seed, passes the same kind of pre-registered one-sided test (R-STG-9; A-EVAL-1) [Tab. 15] [App. B] [ours].

  A run with no test event has no measured gain, and counts as a failure in the second and third readings. A run that ends after its test event without export, or with a frozen artifact lost, or that is abandoned or still suspended, counts as a failure in every reading, whatever its gain (task 6's IR-39.3, IR-18.6). Exports are counted as Table 3 counts papers, unapproved ones apart. Which reading is the headline is task 6's (A-EVAL-1). A task that failed the integrity audit counts as a failure in every reading and stays in every denominator (IR-25.2; A-INT-1) [Tab. 3] [ours].
- **Traces.** P-EVAL-1 [Fig. 1] [Tab. 3] [Tab. 15].
- **Why ours.** The register reads success three ways, after §3.3's `Good` idea, Figure 1's comparison with the human state of the art and Table 15's attributed gain (A-EVAL-1) [§3.3] [Fig. 1] [Tab. 15]. A positive sign is a coin flip when the method changes nothing, and an ablation `Reject` ends a task before its test event, so the first revision's fixture needed a test number that cannot exist (the Codex review, P1; the integrity closure, EI-3). The in-loop precondition reads records the vetoes selected, so only the test event's report fits of *ours* and its control, which no decision has read, can attribute a gain (the integrity closure's second pass, ND-1) [ours].
- **Depends on.** A-EVAL-1, U-EVAL-1, U-TOP-5 and A-INT-1, task 6 [ours].
- **Test.** Logic, with fixture outcomes and a fixture success test, the report gives [ours]:
  - an accepted export whose gain passes the test, with no mark: yes, yes, yes [ours];
  - an ablation reject: yes, no, as not measured and counted a failure, no [ours];
  - an export marked *attribution not established* whose gain passes: yes, yes, no [ours];
  - an export whose ablation `Good` stood, but whose paired difference from its control at the report seeds does not pass the test: yes, yes, no [ours];
  - a run whose gain passes the test and whose tail then ends with *test event done, not exported*: no, no, no, as IR-39.3 counts it [ours];
  - a positive gain that does not pass the test: the second reading is no [ours];
  - no `Good` idea: no, no, no; a task that failed the audit: no, no, no, and it stays in the denominator [ours];
  - an unapproved export appears in its own count [ours].

### R-MEAS-2 · A task's gain is computed from result records, never read from a paper

- **Requirement.** Each task's gain is computed by locked engine code, committed before the first reported run, from the harness's report-role records of the test event (U-INT-4, U-TOP-5), under the rule's metric fields (R-RUN-6), against the references and by the formula that task 6 decides (U-EVAL-1), and whether a tuned baseline is a further reference is task 6's too (U-SUB-2). No reported gain is read from a manuscript, and every reported number names its result record, its hash, the harness commit and the manifest's hash [§4.1] [ours].
- **Traces.** P-EVAL-2 [§4.1].
- **Departs from.** P-EVAL-2: the gain is computed from result records, not parsed from the generated paper by an LLM [§4.1] [ours].
- **Why ours.** The paper parses the generated paper's tables ten times with Gemini and averages them, under no stated formula; on p. 41's numbers, the choice of rule alone moves one task's gain more than a hundredfold (claims.md, P-EVAL-2) [§4.1] [p. 41] (image). CLAUDE.md computes gains deterministically from result files, and a gain nobody can re-run is not shown to be deterministic (EI-24). Which references a gain is taken against is task 6's matter, so this requirement names none of its own (the integrity closure, NEW-15) [ours].
- **Depends on.** U-EVAL-1, U-TOP-5, U-INT-4 and U-SUB-2, task 6 [ours].
- **Test.** Logic: fixture result records give the hand-computed gain against each reference of a fixture formula; editing the numbers in the manuscript's tables changes no reported gain; re-running the gain code from the stored records in a fresh environment gives identical numbers, each naming its record and hashes [ours].

### R-MEAS-3 · Gains across tasks: the median and two means, each with its n

- **Requirement.** Across tasks, the report gives the median gain, the mean over successes, and a mean that includes the failed tasks, each with its n, computed by the locked gain code from the per-task gains of R-MEAS-2 on the report role (U-TOP-5). What gain a failed task counts at is task 6's (U-EVAL-1); whatever it is, a failed run that has a measured test gain, such as one that ended after its test event without export, counts at no more than that gain, and its test-event records are reported; this rule is a presumption on U-EVAL-1, listed for task 6. A run suspended when the report is computed, or abandoned, counts as a failure, flagged (R-RUN-8) [Tab. 4] [ours].
- **Traces.** P-EVAL-3 [Tab. 4].
- **Why ours.** Table 4's mean covers successes only, and a few outliers pull it up (claims.md, C-HEAD-2) [Tab. 4]. A failed gate after the test event would otherwise replace a negative measured gain with the convention's value (the integrity closure, NEW-13) [ours].
- **Depends on.** U-EVAL-1 and U-TOP-5, task 6 [ours].
- **Test.** Logic: a fixture set of gains, failures included, gives the hand-computed median, success-only mean and failure-inclusive mean, each with its n, under the failed-task convention that the fixture names; a run with a negative test gain whose tail writer is scripted to fail a gate counts at its measured gain, and in the twin that applies the convention to it the mean rises [ours].

### R-MEAS-4 · Ratings and acceptance are defined per reviewer, and every review is kept raw

- **Requirement.** For each reviewer whose numbers are reported, the report states the rating's form, the acceptance rule and the SD convention, and every raw review is on disk. The in-loop threshold of 8 is not reported as an acceptance rule unless task 6 defines it so (A-EVAL-3), and whether a rating is one review or several is task 6's too (A-EVAL-4); the in-loop reviewer is task 4's (U-PEER-3) [§3.5] [Tab. 3] [ours].
- **Traces.** P-EVAL-4 [Tab. 3] [§3.5]; P-EVAL-5 [Tab. 3] [§3.5].
- **Why ours.** Table 3's ScholarPeer acceptance rates cannot come from a rating of 8 or more (A-EVAL-3), and whether a rating is one review or several, and which SD, is unstated (A-EVAL-4) [Tab. 3] [ours].
- **Depends on.** A-EVAL-3 and A-EVAL-4, task 6; U-PEER-3, task 4 [ours].
- **Test.** Logic: the mock report states each reviewer's rating form, acceptance rule and SD convention, and every rated paper has its raw review on disk [ours].

### R-MEAS-5 · The judge whose numbers are reported is held out from the loop and from its authors

- **Requirement.** The reviewer whose ratings and acceptances are reported is held out from every in-loop judge of the manuscript, the in-loop reviewer, the Meta-Reviewer, and the reference and alignment checkers, and from every model family that wrote the manuscript. It is never the same system as any of them, and differs from each in model family and prompt lineage where another family runs on a subscription (R-OPS-12); where none does, the report carries a flag, as task 6's IR-29.3 does for the auditor [§4] [fn. 1] [ours]. Its prompts, routing and verdicts sit outside everything any engine job or engine agent reads, and are hashed before the first reported run, under IR-29.1's rule (A-INT-3); keeping them from development sessions is a process rule, recorded and not enforced, as IR-29.5 is [ours]. Every query to it is logged with its purpose, and a query outside a final evaluation flags the report; where the log cannot be enforced, it is recorded as a process rule. Each reported review carries its system, its version, its query date and its raw output. Which judge reports, and its rule, are task 6's (U-EVAL-3) [ours].

  Beside every rating, a transfer control is reported: for a sample of exports, a writer revises the final manuscript against the in-loop reviewer's comments, with the method, the code and every bound number fixed. The in-loop reviewer, the positive control, rates the revision higher; the reporting judge's shift on the same pairs is reported with its n and interval, and if it is not clearly below the in-loop reviewer's, the judge's ratings are reported as in-distribution [ours].
- **Traces.** P-EVAL-6 [§4] [fn. 1]; P-EVAL-7 [§4]; P-ROSTER-50 [§4] [fn. 1].
- **Why ours.** CLAUDE.md never reports the judge the loop optimises against; the paper itself calls ScholarPeer in-distribution, since it refines the drafts, and holds the Stanford Agentic Reviewer out [§4]. The loop optimises against the Meta-Reviewer too, and in review round 2 ScholarPeer's acceptance rises while the held-out reviewer's falls (EI-12) [Tab. 5]. On the subscription every author is Claude, and a flag alone says nothing about whether a rating moved (the integrity closure, NEW-9) [ours].
- **Depends on.** U-EVAL-3 and A-INT-3, task 6 [ours].
- **Test.** Logic: a configuration whose reporting judge is the same system as the Meta-Reviewer fails validation; one that shares only its model family with the authors loads, and the report carries the flag; a configuration whose judge's prompt sits under a path an engine job reads fails validation; a query made outside a final evaluation appears in the log and flags the next report; in mock mode, every reported review carries its system, version, query date and raw output, and with a mock judge scripted to follow the in-loop reviewer, the transfer control labels its ratings in-distribution [ours].

### R-MEAS-6 · The rounds leave the records that the round ablations need

- **Requirement.** Each review round records its index, its score and its stop reason; each idea round records the best search-role gain so far (U-TOP-5). The report rebuilds a score per review round and a best gain per idea round, each with its n; in-loop scores are labelled in-distribution, and report-role numbers per round exist only as diagnostic rows of the freeze (IR-14) [Tab. 5] [Fig. 9a] (image) [ours]. Whether a paper that stopped early counts in later rounds, and how a round's gain is defined, are task 6's (A-EVAL-5, U-EVAL-8) [ours].
- **Traces.** P-EVAL-8 [Tab. 5]; P-EVAL-13 [Fig. 9a] (image).
- **Why ours.** Table 5 does not say whether a paper that stopped early counts in later rounds, and Figure 9a's per-round gain is undefined (A-EVAL-5, U-EVAL-8) [Tab. 5] [Fig. 9a] (image) [ours].
- **Depends on.** A-EVAL-5, U-EVAL-8 and U-TOP-5, task 6 [ours].
- **Test.** Logic: from the records of a mock run with two review rounds and three idea rounds, a script rebuilds the score per review round, labelled in-distribution, and the best search-role gain per idea round, each with its n [ours].

### R-MEAS-7 · Every number carries its seeds and its spread

- **Requirement.** Every reported row is fitted and scored at every seed of its role's list, one list per role, taken from the manifest and never chosen by an agent, and passed to a fit as a seed the runner derives from it (IR-11.5), and every harness result carries its seeds and their spread; the number of seeds is at least the seed floor, which is task 5's (task 6's IR-9.3, IR-10.2; U-INT-4). A row whose spread across seeds is implausibly small is flagged, by IR-3.6's rule; we exempt a method the manifest declares deterministic, an exemption of ours that IR-3.6 does not have, since its ratio test flags nothing when the baseline's spread is 0 anyway. The number of repeated runs is task 6's (U-ART-12, U-EVAL-4) [Tab. 2] [§4] [ours].
- **Traces.** P-EVAL-9 [Tab. 2] [§4].
- **Why ours.** The paper's ± values are spreads across papers, and it reports no run-to-run variance (U-EVAL-4); one critic rejected a variant as statistically inert, a verdict that needs repeated runs (U-ART-12); the one trace's report fixes the seed of its fine-tuning recipe [pp. 40–42] (image), and a seed that an agent fixes can be tried until it is lucky (EI-20) [Tab. 2] [Tab. 16] [ours].
- **Depends on.** U-EVAL-4, U-ART-12 and U-INT-4, task 6 [ours].
- **Test.** Logic: the result schema rejects a result with no seed list, or with fewer seeds than the floor; a scripted solution that ignores the seed it is passed is flagged, while in the twin without the flag it passes with a spread of 0 [ours].

### R-MEAS-8 · A ledger records cost and time per unit, stage and task, with its billing mode

- **Requirement.** The ledger, derived from the one record per unit of work (R-OPS-5), records per agent call, harness job (U-INT-4), stage and task: the billing mode, subscription or metered; for a subscription call, its tokens and the API-equivalent estimate the backend reports, as a diagnostic and never as a bill; for a metered charge, the amount from its authoritative source; the machine-hours; and per stage the wall-clock time and the busy time. Every run is in it, failed runs included, and a price or a duration that is not known is recorded as unknown, never as zero. Prices and the cost model are task 5's (U-COST-1, U-COST-3, A-COST-1) [§4.3] [Fig. 10] (image) [ours].
- **Traces.** P-COST-1 … 4 [§4.3] [Fig. 10] (image).
- **Why ours.** The paper's $3765 per task is a mean over its 33 NeurIPS successes, with no prices and no split between tokens and machines (U-COST-1); CLAUDE.md bounds and records cost. The engine runs on a subscription, whose calls are not billed per token, so a cost without its billing mode would mix two currencies (SA-6, BA-5) [§4.3] [ours].
- **Depends on.** U-COST-1, U-COST-3 and A-COST-1, task 5; U-INT-4, task 6, the compute a harness job records [ours].
- **Test.** Logic: in a mock run with priced calls, the per-stage sums equal the per-unit records; a subscription call carries its tokens and its estimate as a diagnostic, and a billed amount of zero; a call with no price is recorded as unknown, and so is every total it enters; a failed run's cost is in the ledger [ours].

### R-MEAS-9 · Tasks come from the paper's benchmark lists, under a rule fixed before any run

- **Requirement.** Every task we run comes from the paper's benchmark lists, under a written selection rule fixed before the first run. The task list records each task's source table, the rule with its date, and whether the task serves development or a final test (task 6's IR-18.1, IR-18.5; U-EVAL-4, U-TOP-5). A task added or removed after the first run is flagged, and a removed one stays in the report with its reason. How many tasks, and which, is task 5's (U-BENCH-2) [App. A.1] [ours].
- **Traces.** P-BENCH-1 [App. A.1] [Tab. 12] [Tab. 13] [Tab. 14]; P-BENCH-3 [App. A.1].
- **Why ours.** The paper chose its 64 ICML tasks by AutoSOTA's filter without stating it (U-BENCH-2) [App. A.1]. Tuning prompts and margins on the tasks we report would fit their test sets with no agent misbehaving (EI-15) [ours].
- **Depends on.** U-BENCH-2, task 5; U-EVAL-4 and U-TOP-5, task 6 [ours].
- **Test.** Logic: the task list names each task's source table, its role, and the selection rule with its date; a task added after the first run is flagged, and a task removed after it still appears in the report with its reason [ours].

### R-MEAS-10 · A null idea measures how often the guards pass a change that does nothing

- **Requirement.** The engine can run a null idea end to end as configuration, through every gate a real idea passes: a change that leaves the expected score unchanged but draws its randomness anew, such as a component that only consumes random draws or a permuted data order. It runs through the real loop on the toy task, with the critics scripted at their most permissive, an engineer's change that does nothing in each round, then selection and the ablation. Its expected pass rate is computed before the run from the number of scorings the loop allows, and the report gives the measured rate beside every success rate [ours]. A null whose scores equal the baseline's is refused as a control. A twin that turns R-RUN-6's floor validation off, to run at a margin of 0, is a guard-off build, never reportable (task 6's IR-38; U-INT-4). The protocol for real tasks, the number of runs and how the rate is used are task 6's (U-EVAL-4, U-ART-12) [ours].
- **Traces.** none.
- **Why ours.** The paper reports no run-to-run variance [Tab. 2], and claims.md already gives task 6 a null-idea control (P-EVAL-2). With a margin below the noise, a change that does nothing passes the veto, the Selector takes the luckiest draw, and a success is recorded (EI-8). An exact copy of the baseline reproduces it on the shared seeds and passes nothing, and a rate computed for one scoring misses the loop's repeated ones (the integrity closure, NEW-7) [ours].
- **Depends on.** U-EVAL-4, U-ART-12 and U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode, over 200 seeded runs at one gate with noisy fixture records: with the floor validation off, a null scored once passes a margin of 0 in 0.5 ± 0.106 of runs (3 SE); through the loop's three subset scorings it passes a margin of 1 SD in about 0.45, against 0.24 for one scoring (the integrity closure, model A); at the derived margin, its rate lies within 3 SE of α. An exact-copy null is refused; a run of the floor-off twin is refused by the reporter; the report prints the measured rate beside the success rate [ours].
