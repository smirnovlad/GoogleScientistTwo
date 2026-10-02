# Requirements 7 · What the replication measures and reports

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
These requirements cover the numbers a run produces about itself: success, gains, review scores, cost
and time [§4] [ours]. How each is defined is mostly task 6's to decide, or task 5's for cost; these
requirements fix what must be recorded, so that any definition chosen later can be computed from the
records [ours]. `docs/paper/traceability.md` Part 3 says which of the paper's numbers are fair
targets [ours].

### R-MEAS-1 · Success is reported under all three readings

- **Requirement.** For every task, the report states three facts [Fig. 1] [Tab. 3] [Tab. 15] [ours]:
  - a paper was exported, as Table 3 counts papers [Tab. 3];
  - the gain over the human state of the art is positive, under the task's rule [Fig. 1] [ours];
  - the gain survived the ablation, with no `Reject` [Tab. 15] [App. B].

  Which reading is the headline is task 6's, and unapproved exports are counted apart [ours].
- **Traces.** P-EVAL-1 [Fig. 1] [Tab. 3] [Tab. 15].
- **Depends on.** A-EVAL-1, task 6 [ours].
- **Test.** With fixture outcomes, the report gives: an accepted export with a positive gain, yes, yes, yes; an ablation reject with a positive gain, no, yes, no; no `Good` idea, no, no, no; and an unapproved export appears in its own count [ours].

### R-MEAS-2 · A task's gain is computed from result files, never read from a paper

- **Requirement.** Each task's gain is computed by the harness from its test-split result files, under the task's rule fixed before the run (metric, datasets, direction, aggregation), against two references: the published number and our reproduction. No reported gain is read from a manuscript [§4.1] [ours].
- **Traces.** P-EVAL-2 [§4.1].
- **Why ours.** The paper parses the generated paper's tables ten times with Gemini and averages them, under no stated formula; on p. 41's numbers, the choice of rule alone moves one task's gain more than a hundredfold (claims.md, P-EVAL-2) [§4.1] [p. 41] (image); CLAUDE.md computes gains deterministically from result files [ours].
- **Depends on.** U-EVAL-1 and U-TOP-5, task 6 [ours].
- **Test.** Fixture result files give the hand-computed gain against each reference; editing the numbers in the manuscript's tables changes no reported gain [ours].

### R-MEAS-3 · Gains across tasks: the median and two means, each with its n

- **Requirement.** Across tasks, the report gives the median gain, the mean over successes, and a mean that includes the failed tasks, each with its n [Tab. 4] [ours].
- **Traces.** P-EVAL-3 [Tab. 4].
- **Why ours.** Table 4's mean covers successes only, and a few outliers pull it up (claims.md, C-HEAD-2) [Tab. 4] [ours].
- **Depends on.** U-EVAL-1, task 6, including what gain a failed task counts at [ours].
- **Test.** A fixture set of gains, failures included, gives the hand-computed median, success-only mean and failure-inclusive mean, each with its n, under the failed-task convention that the fixture names [ours].

### R-MEAS-4 · Ratings and acceptance are defined per reviewer, and every review is kept raw

- **Requirement.** For each reviewer whose numbers are reported, the report states the rating's form, the acceptance rule and the SD convention, and every raw review is on disk. The in-loop threshold of 8 is not reported as an acceptance rule unless task 6 defines it so [§3.5] [Tab. 3] [ours].
- **Traces.** P-EVAL-4 [Tab. 3] [§3.5]; P-EVAL-5 [Tab. 3] [§3.5].
- **Why ours.** Table 3's ScholarPeer acceptance rates cannot come from a rating of 8 or more (A-EVAL-3), and whether a rating is one review or several, and which SD, is unstated (A-EVAL-4) [Tab. 3] [ours].
- **Depends on.** A-EVAL-3 and A-EVAL-4, task 6; U-PEER-3, task 4 [ours].
- **Test.** The mock report states each reviewer's rating form, acceptance rule and SD convention, and every rated paper has its raw review on disk [ours].

### R-MEAS-5 · The judge whose numbers are reported is held out from the loop

- **Requirement.** The reviewer whose ratings and acceptances are reported is never the reviewer the loop optimises against; each reported review carries its system, its version, its query date and its raw output [§4] [fn. 1] [ours].
- **Traces.** P-EVAL-6 [§4] [fn. 1]; P-EVAL-7 [§4]; P-ROSTER-50 [§4] [fn. 1].
- **Why ours.** CLAUDE.md never reports the judge the loop optimises against; the paper itself calls ScholarPeer in-distribution, since it refines the drafts, and holds the Stanford Agentic Reviewer out [§4] [ours].
- **Depends on.** U-EVAL-3, task 6, which reporting judge and its rule; task 4, whether the service can be used [ours].
- **Test.** A configuration whose reporting judge is the in-loop reviewer, the same system and model, fails validation; in mock mode, every reported review carries its system, version, query date and raw output [ours].

### R-MEAS-6 · The rounds leave the records that the round ablations need

- **Requirement.** Each review round records its index, its score and its stop reason; each idea round records the best validation gain so far. The report rebuilds a score per review round and a best gain per idea round, each with its n [Tab. 5] [Fig. 9a] (image) [ours].
- **Traces.** P-EVAL-8 [Tab. 5]; P-EVAL-13 [Fig. 9a] (image).
- **Why ours.** Table 5 does not say whether a paper that stopped early counts in later rounds, and Figure 9a's per-round gain is undefined (A-EVAL-5, U-EVAL-8) [Tab. 5] [Fig. 9a] (image) [ours].
- **Depends on.** A-EVAL-5 and U-EVAL-8, task 6 [ours].
- **Test.** From the records of a mock run with two review rounds and three idea rounds, a script rebuilds the score per review round and the best validation gain per idea round, each with its n [ours].

### R-MEAS-7 · Every number carries its seeds and its spread

- **Requirement.** Every harness result carries its number of seeds and their spread, and a comparison reported as a gain rests on repeated runs, or is marked as resting on one [Tab. 2] [§4] [ours].
- **Traces.** P-EVAL-9 [Tab. 2] [§4].
- **Why ours.** The paper's ± values are spreads across papers, and it reports no run-to-run variance (U-EVAL-4); one critic rejected a variant as statistically inert, a verdict that needs repeated runs (U-ART-12) [Tab. 2] [Tab. 16] [ours].
- **Depends on.** U-EVAL-4 and U-ART-12, task 6 [ours].
- **Test.** The harness's result schema rejects a result with no seed count, and the mock report marks a comparison from one run as single-run [ours].

### R-MEAS-8 · A ledger records cost and time per stage and task, failed runs included

- **Requirement.** The ledger records, per call, stage and task, the tokens times their price and the machine-hours times theirs, and per stage the wall-clock time and the busy time. Every run is in it, failed runs included, and a price or a duration that is not known is recorded as unknown, never as zero [§4.3] [Fig. 10] (image) [ours].
- **Traces.** P-COST-1 … 4 [§4.3] [Fig. 10] (image).
- **Why ours.** The paper's $3765 per task is a mean over its 33 NeurIPS successes, with no prices and no split between tokens and machines (U-COST-1); CLAUDE.md bounds and records cost [§4.3] [ours].
- **Depends on.** U-COST-1, U-COST-3 and A-COST-1, task 5 [ours].
- **Test.** In a mock run with priced calls, the per-stage sums equal the per-call log; a call with no price is recorded as unknown, and so is every total it enters; a failed run's cost is in the ledger [ours].

### R-MEAS-9 · Tasks come from the paper's benchmark lists, under a rule fixed before any run

- **Requirement.** Every task we run comes from the paper's benchmark lists, under a written selection rule fixed before the first run; the task list records each task's source table, and the rule with its date [App. A.1] [ours].
- **Traces.** P-BENCH-1 [App. A.1] [Tab. 12] [Tab. 13] [Tab. 14]; P-BENCH-3 [App. A.1].
- **Why ours.** The paper chose its 64 ICML tasks by AutoSOTA's filter without stating it (U-BENCH-2); how many tasks we run, and which, is task 5's [App. A.1] [ours].
- **Depends on.** U-BENCH-2, task 5 [ours].
- **Test.** The task list names each task's source table and the selection rule with its date; a task added after the first run is flagged in the report [ours].
