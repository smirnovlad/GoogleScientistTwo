# Requirements 7 · What the replication measures and reports

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
These requirements cover the numbers a run produces about itself: success, gains, review scores, cost
and time [§4] [ours]. How each is defined is mostly task 6's to decide, or task 5's for cost; these
requirements fix what must be recorded, so that any definition chosen later can be computed from the
records [ours]. `docs/paper/traceability.md` Part 3 says which of the paper's numbers are fair
targets; matching the paper's own numbers is not part of the goal [ours].

### R-MEAS-1 · Success is reported under all three readings

- **Requirement.** For every task, the report states three facts, each computed from the report-role records of the test event (task 6's constraint on A-EVAL-1; U-TOP-5) [Fig. 1] [Tab. 3] [Tab. 15] [ours]:
  - a paper was exported, as Table 3 counts papers [Tab. 3];
  - the gain over the human state of the art is positive, under the task's rule [Fig. 1] [ours];
  - the gain survived the ablation, with no `Reject` [Tab. 15] [App. B].

  Which reading is the headline is task 6's (A-EVAL-1). Unapproved exports are counted apart, and a task that failed the integrity audit counts as a failure in every reading and stays in every denominator (IR-25; A-INT-1) [ours].
- **Traces.** P-EVAL-1 [Fig. 1] [Tab. 3] [Tab. 15].
- **Depends on.** A-EVAL-1, U-TOP-5 and A-INT-1, task 6 [ours].
- **Test.** Logic, with fixture outcomes, the report gives: an accepted export with a positive gain, yes, yes, yes; an ablation reject with a positive gain, no, yes, no; no `Good` idea, no, no, no; a task that failed the audit, no, no, no, and it stays in the denominator; and an unapproved export appears in its own count [ours].

### R-MEAS-2 · A task's gain is computed from result records, never read from a paper

- **Requirement.** Each task's gain is computed by locked engine code, committed before the first reported run, from the harness's report-role records of the test event (U-INT-4, U-TOP-5), under the rule's metric fields (R-RUN-6), against two references: the published number and the pinned baseline's sealed result (IR-15). The formula is task 6's (U-EVAL-1), and so is whether a tuned baseline is a third reference (U-SUB-2). No reported gain is read from a manuscript, and every reported number names its result record, its hash, the harness commit and the manifest's hash [§4.1] [ours].
- **Traces.** P-EVAL-2 [§4.1].
- **Departs from.** P-EVAL-2: the gain is computed from result records, not parsed from the generated paper by an LLM [§4.1] [ours].
- **Why ours.** The paper parses the generated paper's tables ten times with Gemini and averages them, under no stated formula; on p. 41's numbers, the choice of rule alone moves one task's gain more than a hundredfold (claims.md, P-EVAL-2) [§4.1] [p. 41] (image). CLAUDE.md computes gains deterministically from result files, and a gain nobody can re-run is not shown to be deterministic (EI-24) [ours].
- **Depends on.** U-EVAL-1, U-TOP-5, U-INT-4 and U-SUB-2, task 6 [ours].
- **Test.** Logic: fixture result records give the hand-computed gain against each reference; editing the numbers in the manuscript's tables changes no reported gain; re-running the gain code from the stored records in a fresh environment gives identical numbers, each naming its record and hashes [ours].

### R-MEAS-3 · Gains across tasks: the median and two means, each with its n

- **Requirement.** Across tasks, the report gives the median gain, the mean over successes, and a mean that includes the failed tasks, each with its n, computed by the locked gain code from the per-task gains of R-MEAS-2 on the report role (U-TOP-5). What gain a failed task counts at is task 6's (U-EVAL-1) [Tab. 4] [ours].
- **Traces.** P-EVAL-3 [Tab. 4].
- **Why ours.** Table 4's mean covers successes only, and a few outliers pull it up (claims.md, C-HEAD-2) [Tab. 4] [ours].
- **Depends on.** U-EVAL-1 and U-TOP-5, task 6 [ours].
- **Test.** Logic: a fixture set of gains, failures included, gives the hand-computed median, success-only mean and failure-inclusive mean, each with its n, under the failed-task convention that the fixture names [ours].

### R-MEAS-4 · Ratings and acceptance are defined per reviewer, and every review is kept raw

- **Requirement.** For each reviewer whose numbers are reported, the report states the rating's form, the acceptance rule and the SD convention, and every raw review is on disk. The in-loop threshold of 8 is not reported as an acceptance rule unless task 6 defines it so (A-EVAL-3), and whether a rating is one review or several is task 6's too (A-EVAL-4); the in-loop reviewer is task 4's (U-PEER-3) [§3.5] [Tab. 3] [ours].
- **Traces.** P-EVAL-4 [Tab. 3] [§3.5]; P-EVAL-5 [Tab. 3] [§3.5].
- **Why ours.** Table 3's ScholarPeer acceptance rates cannot come from a rating of 8 or more (A-EVAL-3), and whether a rating is one review or several, and which SD, is unstated (A-EVAL-4) [Tab. 3] [ours].
- **Depends on.** A-EVAL-3 and A-EVAL-4, task 6; U-PEER-3, task 4 [ours].
- **Test.** Logic: the mock report states each reviewer's rating form, acceptance rule and SD convention, and every rated paper has its raw review on disk [ours].

### R-MEAS-5 · The judge whose numbers are reported is held out from the loop

- **Requirement.** The reviewer whose ratings and acceptances are reported is held out from every in-loop judge of the manuscript: the in-loop reviewer, the Meta-Reviewer, and the reference and alignment checkers. It is never the same system as any of them, and it differs from each in model family and prompt lineage where another family is available; on the subscription alone none may be, and the report then carries a flag, as task 6's IR-29 does for the auditor [§4] [fn. 1] [ours]. Every query to it is logged with its purpose, and a query outside a final evaluation flags the report. Each reported review carries its system, its version, its query date and its raw output. Which judge reports, and its rule, are task 6's (U-EVAL-3); whether an outside service may be used is task 4's [ours].
- **Traces.** P-EVAL-6 [§4] [fn. 1]; P-EVAL-7 [§4]; P-ROSTER-50 [§4] [fn. 1].
- **Why ours.** CLAUDE.md never reports the judge the loop optimises against; the paper itself calls ScholarPeer in-distribution, since it refines the drafts, and holds the Stanford Agentic Reviewer out [§4]. The loop optimises against the Meta-Reviewer too, and in review round 2 ScholarPeer's acceptance rises while the held-out reviewer's falls (EI-12) [Tab. 5] [ours].
- **Depends on.** U-EVAL-3, task 6 [ours].
- **Test.** Logic: a configuration whose reporting judge is the same system as the Meta-Reviewer fails validation; one that shares only its model family loads, and the report carries the flag; a query made outside a final evaluation appears in the log and flags the next report; in mock mode, every reported review carries its system, version, query date and raw output [ours].

### R-MEAS-6 · The rounds leave the records that the round ablations need

- **Requirement.** Each review round records its index, its score and its stop reason; each idea round records the best search-role gain so far (U-TOP-5). The report rebuilds a score per review round and a best gain per idea round, each with its n; in-loop scores are labelled in-distribution, and report-role numbers per round exist only as diagnostic rows of the freeze (IR-14) [Tab. 5] [Fig. 9a] (image) [ours]. Whether a paper that stopped early counts in later rounds, and how a round's gain is defined, are task 6's (A-EVAL-5, U-EVAL-8) [ours].
- **Traces.** P-EVAL-8 [Tab. 5]; P-EVAL-13 [Fig. 9a] (image).
- **Why ours.** Table 5 does not say whether a paper that stopped early counts in later rounds, and Figure 9a's per-round gain is undefined (A-EVAL-5, U-EVAL-8) [Tab. 5] [Fig. 9a] (image) [ours].
- **Depends on.** A-EVAL-5, U-EVAL-8 and U-TOP-5, task 6 [ours].
- **Test.** Logic: from the records of a mock run with two review rounds and three idea rounds, a script rebuilds the score per review round, labelled in-distribution, and the best search-role gain per idea round, each with its n [ours].

### R-MEAS-7 · Every number carries its seeds and its spread

- **Requirement.** Every harness result carries its seeds, taken from the manifest's list and never chosen by an agent, and their spread; a result whose seeds give identical values, for a method not declared deterministic, is flagged (task 6's IR-3; U-INT-4). A comparison reported as a gain rests on repeated runs, or is marked as resting on one; the numbers of seeds and runs are task 6's (U-ART-12, U-EVAL-4) [Tab. 2] [§4] [ours].
- **Traces.** P-EVAL-9 [Tab. 2] [§4].
- **Why ours.** The paper's ± values are spreads across papers, and it reports no run-to-run variance (U-EVAL-4); one critic rejected a variant as statistically inert, a verdict that needs repeated runs (U-ART-12); the one trace's report fixes the seed of its fine-tuning recipe [pp. 40–42] (image), and a seed that an agent fixes can be tried until it is lucky (EI-20) [Tab. 2] [Tab. 16] [ours].
- **Depends on.** U-EVAL-4, U-ART-12 and U-INT-4, task 6 [ours].
- **Test.** Logic: the result schema rejects a result with no seed list; a scripted solution that ignores the seed it is passed is flagged, while in the twin without the flag it passes with a spread of 0; the mock report marks a comparison from one run as single-run [ours].

### R-MEAS-8 · A ledger records cost and time per unit, stage and task, with its billing mode

- **Requirement.** The ledger, derived from the one record per unit of work (R-OPS-5), records per agent call, harness job (U-INT-4), stage and task: the billing mode, subscription or metered; for a subscription call, its tokens and the API-equivalent estimate the backend reports, as a diagnostic and never as a bill; for a metered charge, the amount from its authoritative source; the machine-hours; and per stage the wall-clock time and the busy time. Every run is in it, failed runs included, and a price or a duration that is not known is recorded as unknown, never as zero. Prices and the cost model are task 5's (U-COST-1, U-COST-3, A-COST-1) [§4.3] [Fig. 10] (image) [ours].
- **Traces.** P-COST-1 … 4 [§4.3] [Fig. 10] (image).
- **Why ours.** The paper's $3765 per task is a mean over its 33 NeurIPS successes, with no prices and no split between tokens and machines (U-COST-1); CLAUDE.md bounds and records cost. The engine runs on a subscription, whose calls are not billed per token, so a cost without its billing mode would mix two currencies (SA-6, BA-5) [§4.3] [ours].
- **Depends on.** U-COST-1, U-COST-3 and A-COST-1, task 5; U-INT-4, task 6, the compute a harness job records [ours].
- **Test.** Logic: in a mock run with priced calls, the per-stage sums equal the per-unit records; a subscription call carries its tokens and its estimate as a diagnostic, and a billed amount of zero; a call with no price is recorded as unknown, and so is every total it enters; a failed run's cost is in the ledger [ours].

### R-MEAS-9 · Tasks come from the paper's benchmark lists, under a rule fixed before any run

- **Requirement.** Every task we run comes from the paper's benchmark lists, under a written selection rule fixed before the first run. The task list records each task's source table, the rule with its date, and whether the task serves development or a final test (task 6's IR-18; U-EVAL-4). A task added or removed after the first run is flagged, and a removed one stays in the report with its reason. How many tasks, and which, is task 5's (U-BENCH-2) [App. A.1] [ours].
- **Traces.** P-BENCH-1 [App. A.1] [Tab. 12] [Tab. 13] [Tab. 14]; P-BENCH-3 [App. A.1].
- **Why ours.** The paper chose its 64 ICML tasks by AutoSOTA's filter without stating it (U-BENCH-2) [App. A.1]. Tuning prompts and margins on the tasks we report would fit their test sets with no agent misbehaving (EI-15) [ours].
- **Depends on.** U-BENCH-2, task 5; U-EVAL-4, task 6 [ours].
- **Test.** Logic: the task list names each task's source table, its role, and the selection rule with its date; a task added after the first run is flagged, and a task removed after it still appears in the report with its reason [ours].

### R-MEAS-10 · A null idea measures how often the guards pass a change that does nothing

- **Requirement.** The engine can run a null idea, a change that leaves the method as it is, end to end as configuration, through every gate a real idea passes, and the report gives the guards' measured false-pass rate beside every success rate. The protocol, the number of runs and how the rate is used are task 6's (U-EVAL-4, U-ART-12) [ours].
- **Traces.** none.
- **Why ours.** The paper reports no run-to-run variance [Tab. 2], and claims.md already gives task 6 a null-idea control (P-EVAL-2). With a margin below the noise, a change that does nothing passes the veto, the Selector takes the luckiest draw, and a success is recorded (EI-8) [ours].
- **Depends on.** U-EVAL-4 and U-ART-12, task 6 [ours].
- **Test.** Logic, in mock mode: a null idea configured by data alone runs through the subset and full-set vetoes; over 200 seeded runs with noisy fixture records, it passes at a margin of 0 in about half of them and in almost none at the configured margin, and the report prints the measured rate beside the success rate [ours].
