# Requirements review through the evaluation-integrity lens (task 2, first draft)

- **Reviewer:** `evaluation-integrity-engineer`, 2026-10-02.
- **What was reviewed:** `git diff claude/paper-analysis...HEAD` on `claude/requirements` at ff1faaa. That is `docs/requirements.md` and `docs/requirements/01-run.md` to `08-operation.md`.
- **The question:** can a coding agent, or we, move a number that a decision reads or a report states without a better method? And would we notice?
- **What I read:**
  - CLAUDE.md's integrity rules, and the draft.
  - `docs/paper/stages/07-integrity.md`, `claims.md`, `artifacts.md`, `unspecified.md`, and `analysis.md` §4.2 and §7.3.
  - The paper's TeX: §3, §4, App. A.2, App. B, and Tables 5, 6, 7 and 16.
  - The PDF's pages 40, 41, 42, 47 and 51, viewed directly.
  - ScientistOne's §5, its setup, and its audit appendix (`.cache/refs/2605.26340v1/`).
  - Task 6's brief, `docs/integrity/README.md` on `claude/integrity-blockers` (8377a99). Task 6 has decided nothing yet.
- **Checks run** (2026-10-02, at ff1faaa):
  - `python3 playground/paper/requirement_coverage.py` finds 0 problems: 177 elements, 71 requirements, 33 rows.
  - `--selftest` catches every planted defect.
  - Neither check covers anything in this review except the *Decides*-field boundary (see EI-19).
- **Read-only:** I edited no file and ran no git command that changes state. Paths are relative to the repository root.
- **Conventions:**
  - *Paper* is what arXiv:2609.19644v1 or ScientistOne says, with its location. *Draft* is what the requirements say. *Guard (proposal)* is mine [ours].
  - **Blocker:** a design that meets the requirements as written could let a reported number move without a better method while every acceptance test stays green. Also a blocker: a requirement that decides one of task 6's blocking rows.
  - **Major:** an open attack path, or a guard with no control.
  - **Minor:** a tightening.

## Summary

| ID | Severity | Finding |
|---|---|---|
| EI-1 | blocker | The integrity tests prove the plumbing, never the guard |
| EI-2 | blocker | The test split is protected as read-only, not as unreachable |
| EI-3 | blocker | R-INT-3 and R-STATE-6 decide when the test split is scored, so the exported paper reports validation numbers, unlabelled |
| EI-4 | blocker | Nothing keeps agents, or agent code run by the harness, away from the results, the verdicts and the rules |
| EI-5 | major | The manuscript can launder another entry's number as the method's |
| EI-6 | major | The rebuttal picks its own datasets, test caps and metrics, and no locked scorer exists for them |
| EI-7 | major | Attribution rests on one LLM verdict, over ablations that the pipeline chooses, codes and can drop |
| EI-8 | major | No control shows that the numeric guards stop noise |
| EI-9 | major | The comparison rule can be gamed through what it does not read |
| EI-10 | major | Compute scaling passes every guard |
| EI-11 | major | Judges read what the judged agent wrote, and no judge's detection rate gates a run |
| EI-12 | major | The reported judge is kept apart from too little |
| EI-13 | major | The post-hoc audit is kept apart from the wrong agent, and ScientistOne's procedure is not separated from ours |
| EI-14 | major | "Used once" has no refusal and no ledger |
| EI-15 | major | Development-time overfitting |
| EI-16 | major | The manifest, its rule and the evaluator are pinned by a hash checked after the fact, against itself |
| EI-17 | major | The baseline is agent-written, unfiltered and unaudited, and checked on an unnamed split |
| EI-18 | major | Task 6's blocking rows are missing where requirements rest on them, and six decisions are marked final |
| EI-19 | minor | Requirement text adopts task 6's proposals, and the boundary check cannot see it |
| EI-20 | minor | Seeds are the agent's to choose |
| EI-21 | minor | Verdicts are not bound to the code the harness ran, and a failure after a result can re-roll it |
| EI-22 | minor | The Selector's band is never tested against an out-of-band choice |
| EI-23 | minor | The in-loop reference check is weaker than ScientistOne's I3 |
| EI-24 | minor | Nothing shows a gain can be re-run, or traces a reported number to its file |

## 1. Threat model, by stage

| Stage and agents | Controls and writes | Reads (per the draft) | Rewarded for | Can move without a better method | Findings |
|---|---|---|---|---|---|
| Limitations and seeds: the Extractor, the Verifier, the Idea Generator, the Novelty Checker | idea text; the pool, which is append-only | G, whose paper prints published test numbers; the pool | a high rank; being run | which ideas run; an idea that only scales compute | EI-10 |
| Baseline: the Baseline Coding Agent | C_base. Nothing excludes the run directory | G's code; the benchmark; the test split, which is only "read-only" | passing the tolerance | E_base, and with it every in-loop margin and the gain against "our reproduction" | EI-2, EI-4, EI-17 |
| Subset and full set: the coders, the engineers, the critics | code, hyperparameters, seeds and compute; which settings run or crash; logs and reports; the shared run directory | validation results, feedback, evaluation code; the test split, which is only read-only | `Good`: a margin over E_base | the validation gain, through tuning, seeds, compute, crashes, test reads, scorer tampering or persuasion | EI-2, EI-4, EI-8 to EI-11, EI-20 |
| Rounds and selection: A_Evolve, the Selector | which ideas exist; the choice among near-ties | every trace, code and logs included | nothing of its own | h_best, within the margin | EI-11, EI-22 |
| Ablation: the planner, the ablation coders, the critic, A_FullEng, the Result Comparison Agent | which ablations exist and how they are coded; the verdict; the refinement | ablation results, code, the agents' own reports | no `Reject`, which is success reading (c); a promotion | the attribution verdict; E_best | EI-7, EI-9, EI-21 |
| Drafting and peer review: the Drafter, the Enhancer (Claude Code), ScholarPeer, the Rebuttal Planner and Coder | which numbers the paper shows; its figures; the rebuttal experiments and their data | the verified table, the reviews, C_best. The Enhancer's file access is unbounded | a ScholarPeer score of 8 or more | the paper's numbers; the rebuttal evidence | EI-3, EI-5, EI-6 |
| Meta-review: the Meta-Reviewer, A_FullEng | the restart; the approval | the manuscript, the review, the verified table | `Accept` | the count of approved exports; a second pass with fresh budgets | EI-8, EI-12 |
| In-loop checks: the specification filter, the reference check, the alignment audit | keep or discard; flags | code and manuscript, including text the judged agent wrote | nothing of its own | which results count | EI-11, EI-13, EI-21 |
| Final evaluation and reporting: the harness, the gain script, the reporting judge, the audit, and us | which tasks, rules, margins, configurations, runs and attempts count; when the test split is touched | everything, test numbers included | the headline numbers | every reported number, by selection | EI-12 to EI-16, EI-24 |

The brief's attacks map onto the findings as follows:
- **An agent writing its own results:** EI-4.
- **Touching the evaluator:** EI-2, EI-4, EI-16.
- **Choosing the data:** EI-2, EI-6. R-RUN-2 already closes this for the full benchmark.
- **Tuning against validation until it overfits:** EI-8, EI-15.
- **Steering the margin or the rule:** EI-8, EI-9, EI-16.
- **Laundering through the manuscript:** EI-3, EI-5.
- **A judge editing what it judges:** R-INT-9 is sound, but its test is the problem of EI-1. The converse, an agent editing a verdict, is EI-4.
- **The Selector's choice among near-ties:** EI-11, EI-22.
- **A vetoed `Good` turned into `Engineer`:** EI-7, EI-8.
- **The Result Comparison Agent:** closed by R-PRIM-6, subject to EI-9.
- **The rebuttal agent choosing its datasets:** EI-6.
- **The meta restart:** no new path. It adds validation draws (EI-8), and the Meta-Reviewer is a judge the loop is optimised against (EI-12).

## 2. Task 2's decisions: what they close, and what they leave open

| Row and requirement | Closes | Leaves open | See |
|---|---|---|---|
| A-ABL-3, R-PRIM-6 | the Result Comparison Agent's preference as the gate; a gain inside the margin | missing datasets and non-finite values; secondary metrics; a margin below the noise | EI-8, EI-9 |
| U-SUB-1, R-STG-4 | an LLM `Good` with no number behind it | the margin against the noise. The veto's `Engineer` path feeds generic tuning, and "tunes and repairs only" has no test | EI-7, EI-8 |
| U-BASE-2, A-BASE-1, A-FULL-1: R-STG-3, R-STG-5 | an unchecked reproduction; crediting an idea with the gap between two machines | the split the check reads; a baseline weaker by up to the tolerance; the baseline is neither filtered nor audited | EI-17 |
| U-SEL-1, R-STG-8 | a Selector choosing a clear loser | no test of an out-of-band choice; text planted in logs | EI-11, EI-22 |
| A-ABL-1, U-ABL-5: R-STG-9 | exporting a gain the ablation does not attribute. It also refuses the fall-back to the next idea, which would add selection | one LLM verdict, over ablations the pipeline chooses, codes and can drop | EI-7 |
| A-ABL-2, U-ABL-2: R-STG-9 | an unbounded nested loop | nothing new | none |
| U-INT-1, R-INT-4 | a rule-breaking number steering a decision | the baseline is not in the list; a discard hides an ablation; the verdict is not bound to the code that ran; the detection rate | EI-7, EI-11, EI-17, EI-21 |
| U-INT-3: R-INT-5, R-INT-6 | an Enhancer edit that no check sees; an export that is never checked | the reference check is weaker than ScientistOne's I3; A-INT-1 is not named | EI-18, EI-23 |
| A-TOP-1 (U-TOP-7), R-STG-11 | choosing the manuscript by the optimised reviewer's score | nothing | none |
| U-BASE-1, R-RUN-2 | the agent deciding what "full" covers ("OOD datasets (FULL, 6 of 6)" [p. 40]) | no split fields; how the manifest is pinned | EI-2, EI-16 |
| A-TOP-3: R-STG-12, R-STATE-6 | an unapproved export counted as accepted | the freeze at export fixes which split the paper reports | EI-3 |
| U-EVO-4, R-RUN-5 | a failure without a record; a filtered task leaving the denominator, as it does between Table 7's 50/50 and 49/49 [Tab. 7] [fn. 2] | which attempt of a task counts | EI-14 |
| U-SEED-3, R-STG-2 | nothing: the rule is a prompt | compute scaling | EI-10 |

**Keep these as they are:**
- R-PRIM-6's test contains its own attack: an agent prefers the new result while the rule keeps the old one.
- R-STG-4 and R-STG-8 put a number ahead of the LLM verdict, and both have fixture tests.
- R-STG-11 keeps the last manuscript, never the best-scoring one.
- R-STG-9 refuses a fall-back after `Reject`.
- R-STG-5 judges against our own reproduction, and keeps the published number for reporting.
- R-RUN-2's test: an agent that drops a dataset changes nothing reported.
- R-INT-1's test closes p. 42's attack, where the agent's own report was the evaluation.
- R-INT-6: the fix edits the paper, never the code.
- R-MEAS-2's test: editing the manuscript changes no gain.
- R-RUN-5 and R-MEAS-3 keep failures in the denominators.

## 3. The boundary with task 6

- **A requirement decides part of a blocking row.** R-INT-3, together with R-STATE-6, fixes how often the test split is scored ("once per exported run") and when ("after the export"). Task 6's brief lists both as open under U-TOP-5 (EI-3).
- **Requirements take task 6's proposals as their own text,** while listing the row under *Depends on*:
  - R-INT-7 takes U-EVAL-5's and U-NOTE-4's;
  - R-MEAS-2 and R-MEAS-3 take U-EVAL-1's;
  - R-INT-8 takes A-ART-7's;
  - R-MEAS-1 takes A-EVAL-1's;
  - R-STG-3 and R-STG-6 settle which code produces E_base, which task 6's brief asks under U-INT-4.

  The boundary check cannot see any of these (EI-19).
- **Some requirements are too weak for task 6's decisions to be enforced:**
  - R-INT-2's "read-only" for the test split (EI-2);
  - R-INT-1 and R-STATE-8 on keeping agents away from the harness (EI-4);
  - the tests (EI-1);
  - the *Depends on* graph (EI-18);
  - the pinning of the manifest (EI-16).
- **Not a pre-emption:** R-INT-4 to R-INT-6 put the filter and the two repairs inside the loop. §4.2 already puts them there: the filter discards "immediately after experimentation", and the Writer Agent rectifies [§4.2] (tex:sections/4_experiment.tex:43). Only their timing is task 2's, through U-INT-1 and U-INT-3. They should still name A-INT-1 (EI-18).

## 4. Findings

### Blockers

**EI-1 · blocker · The integrity tests prove the plumbing, never the guard**
- *Where:* `docs/requirements.md`, the *Tests* bullet of "How to read"; R-OPS-1; R-OPS-3; the tests of R-INT-1 to R-INT-9, R-STATE-1 and R-OPS-8.
- *Paper:* §3, §4.2 and App. A.2 describe "no sandbox, no read-only evaluation code, no hash and no harness" (`docs/paper/stages/07-integrity.md`). Every setup guard is therefore ours, and only our tests can show that it exists.
- *Draft:* "Most tests run in mock mode (R-OPS-1): scripted mock agents, a mock harness that returns fixture results", and R-OPS-1 mocks "the sandbox and the harness". So these four tests describe a mock that refuses because it is scripted to:
  - "an agent's write to an evaluation file fails in its sandbox" (R-INT-2);
  - "a judge scripted to write into the workspace it judges fails with a permission error" (R-INT-9);
  - the same for the task's files (R-STATE-1);
  - "an install that the stage's policy forbids fails" (R-OPS-8).

  R-OPS-3 would help, since each mock must pass the real adapter's contract tests. But R-OPS-3 does not list the harness, and nothing puts the attacks into those contract tests. No integrity test has a twin in which the guard is off and the attack succeeds.
- *Attack:* none is needed. The sandbox mounts the evaluation directory writable, or the harness scores inside the agent's container, and every acceptance test stays green.
- *Would we notice:* no. CLAUDE.md's rule "A green check must prove it ran" fails at the level of the acceptance tests.
- *Would each test fail with its guard missing?*

  | Test | The guard | Fails with the guard missing? |
  |---|---|---|
  | R-INT-1 | critics and reports read the harness's files | yes, for a score in the agent's own file. No, for the harness's files or its scoring process, which are mocks |
  | R-INT-2 | read-only evaluation files; the hash check | no, for the mount, because the sandbox is a mock. The hash half fails only if a real component checks a real file |
  | R-INT-3 | no test value before export; the test split used once | partly. An engine that calls test mode early is caught. But no test attempts an early or second call, no agent reaches for test data, and the scan has no planted positive |
  | R-INT-4 to R-INT-7 | the LLM checks | yes, for the order of calls. No, for detection: the judges are mocks scripted to flag |
  | R-INT-6 | the fix never edits code | no, unless the scripted writer tries to edit code |
  | R-INT-8 | writers see only the table; every number traces to it | first half: no, since the writer never reaches for the log. Second half: yes |
  | R-INT-9, R-STATE-1, R-OPS-8 | read-only judges and task files; the sandbox policy | no, because the sandbox is a mock. R-STATE-1's hash equality also misses an edit restored before the run ends |
  | R-MEAS-5 | the reporting judge kept apart | yes, but only for an exact match (EI-12) |
  | R-PRIM-6, R-STG-4, R-RUN-2, R-MEAS-2 | the numeric guards; the fixed benchmark; gains from files | yes: each contains its own attack |
- *Guard (proposal; task 2 states it, task 7 owns the strategy):* a class of *enforcement tests*, one for every guard the setup enforces: a mount, a permission, a hash check, the harness refusing a split, the isolation of scoring, the network policy.
  - Each runs the real sandbox and the real harness on a toy task, with scripted agents whose actions are real file, process and network operations. It still costs $0, so R-OPS-1 holds.
  - Each runs twice. With the guard off, the planted attack must succeed and change the number or file observed. With the guard on, the attack must fail and leave a record.
  - Mock mode keeps proving the plumbing: the order of calls, and what flows where.
  - Add the harness to R-OPS-3, with the attacks in its contract tests.
- *Control:* the twin itself. `requirement_coverage.py` can fail any R-INT or R-STATE test that does not state both outcomes.

**EI-2 · blocker · The test split is protected as read-only, not as unreachable**
- *Where:* R-INT-2; R-INT-3; R-RUN-2, its fields and its test; R-OPS-8; R-INT-4's test.
- *Paper:*
  - In the one trace, the script "extracts the 12 L2-normalised layer features for CIFAR-100 train/test and all 6 SCOOD OOD sets, then scores both" methods [p. 42].
  - The critic steered the redesign with "CIFAR-10 AUROC drops from 96.83% to 88.02%" [p. 46]. CIFAR-10 is a set the final report publishes [p. 41].
  - The auditor "extracted test features fresh from the checkpoint" [p. 47].
  - In ScientistOne, every flagged Sakana paper "imports the canonical evaluator and calls it as an optimisation oracle". Its majority vote missed an exploit "flagged by only 2/5 judges" [Ref: meng2026scientistone, appendix "Failure Cases per Audit Metric"] (ref:2605.26340v1:sections/012c_coe_audit_details.tex:265-271, 234-237).
- *Draft:*
  - Evaluation code and data are "read-only in every agent's sandbox" (R-INT-2, which copies CLAUDE.md's wording).
  - R-INT-3 governs the numbers an agent sees, not the data it can read or compute on.
  - R-RUN-2's manifest has no split fields. Its test ("A manifest without one of the fields above fails to load") therefore passes a manifest that has no validation or test split.
  - The only defence against code that "reads the test labels" is the specification filter, which is an LLM (R-INT-4).
- *Attack:* read access is enough.
  - The code computes its own test metric, and picks a checkpoint, a hyperparameter or a seed by it.
  - Or it fits on the test inputs transductively.
  - With network access, it downloads a public benchmark's test labels.

  No harness number is involved, so R-INT-3's scan finds nothing.
- *Would we notice:* only if the filter or the post-hoc audit flags the code. Nobody measures either one's miss rate (EI-11).
- *Guard (proposal):*
  - R-INT-2 keeps read-only for evaluation code and validation data.
  - R-INT-3 adds that the test split's inputs and labels are absent from every agent sandbox, and unreachable by agent code until the final evaluation.
  - When the harness runs agent code, it has no network and only declared, hashed artefacts.
  - R-RUN-2's fields add "the data roles of each dataset, with the hash of each split's example IDs, as U-TOP-5 defines them".
  - Which roles exist, and who reads each, is task 6's to decide (U-TOP-5). That no agent reads the test split already follows from CLAUDE.md's "used once".
- *Control:*
  - A scripted coder tries four things: it opens the test path, lists its mounts, calls the harness's test mode, and fetches a URL. Each fails and is recorded.
  - Twin, with the test split mounted read-only: the scripted code selects a checkpoint on test, and the final number moves.

**EI-3 · blocker · R-INT-3 and R-STATE-6 decide when the test split is scored, so the exported paper can report only validation numbers, and nothing says so**
- *Where:* R-INT-3, R-STATE-6, R-INT-8, R-STG-10, R-INT-7, R-MEAS-1, R-MEAS-2.
- *Draft:* three rules combine:
  - R-INT-3: "The test split is scored once per exported run, by the harness, after the export".
  - R-STATE-6: "At export, P+ and C+ are hashed and become read-only".
  - R-INT-8: writers read only the verified table, which is built during the run from validation results.

  So P+ holds validation numbers only. The consequences:
  - Nothing requires the paper to say which split a number is on. G's paper, which the writers imitate, reports test numbers.
  - These are the numbers the search selected on. Up to 10 ideas are each judged up to three times per level (R-STG-4, R-STG-5, R-STG-7), and R-STG-8 then takes the maximum. So the numbers carry the winner's curse, and the held-out reviewer rates that paper.
  - R-INT-7's score verification re-runs "every reported number" on no named split.
  - R-MEAS-1's fixture "an ablation reject with a positive gain, no, yes, no" needs a test gain (R-MEAS-2) for a task with no export. R-INT-3 never scores one.
  - R-INT-3's first sentence, "Every number that an agent sees during the run is a validation number", cannot hold as written: G's paper prints test numbers, and every agent reads it.
- *Boundary:* "once per exported run" and "after the export" answer questions that task 6's brief lists as open under U-TOP-5: "What 'the test set is used once' counts", and "What the writer sees, before and after the test set is scored, and what may still change once test numbers exist". CLAUDE.md settles only "used once, at the end".
- *Attack:* none is needed. The selected validation number becomes the paper's headline, presented as a test result.
- *Would we notice:* only by comparing the paper's tables with the harness's test report, which no requirement does.
- *Guard (proposal):*
  - R-INT-3 states the invariant, not the timing: "no test-split evaluation of an artefact produced in the run reaches an agent or a decision before the export, and the test split is evaluated at the point task 6 fixes (U-TOP-5)".
  - R-INT-8 adds that every number in the export carries its split, and that a validation number is never presented as a test number.
  - R-STATE-6 leaves room for one deterministic fill of test numbers by the harness alone, if task 6 chooses it.
  - R-MEAS-1 states reading (b) for an unexported task under task 6's rule.
  - R-STG-10, R-INT-8, R-STATE-6 and R-MEAS-1 list U-TOP-5.
- *Control:* a fixture export whose paper presents a validation entry as a test result fails the export check. Twin without the split label: it exports.

**EI-4 · blocker · Nothing keeps agents, or agent code run by the harness, away from the results, the verdicts and the rules**
- *Where:* R-INT-1, R-STATE-8, R-STATE-2, R-STATE-3, R-OPS-2, R-INT-9.
- *Paper:*
  - The auditor saved its verdict to `./tasks/x_maha/logs/eval_result/repro_check.json`, inside the task it audited [p. 47].
  - The agent's script "scores both Procrustes-DS and the X-Maha baseline and writes this report" [p. 42].
  - ScientistOne found a solver whose hyperparameter tuning loop was "gated on an environment variable": the loop ran during search and was skipped at re-evaluation (ref:2605.26340v1:sections/012c_coe_audit_details.tex:139-146).
- *Draft:*
  - R-STATE-8: "Each task's run writes to one directory with a declared layout: code versions, harness results, stage records, manuscript versions and the ledger".
  - The append-only rule and the core-state guard are refusals by the store (R-STATE-2, R-STATE-3), not limits on what a sandbox mounts.
  - R-INT-1 requires metrics from "the locked evaluation harness's own result files". It does not say that agents cannot write those files, or that agent code never runs where a metric is computed.
  - Prompts, rubrics, margins and limits are files (R-OPS-2), with no stated protection.
  - R-INT-1's test covers one attack only: a fabricated score in the agent's own file.
- *Attacks:*
  - (a) A coding session writes a harness result, or a stage record holding a verdict, in the shared run directory.
  - (b) Agent code run by the harness overwrites the result path. Or it patches the metric at import time, with a `sitecustomize.py` or a module that shadows the scorer's. Or it detects the harness (an environment variable, the split's size) and behaves differently.
  - (c) A session edits a critic's prompt, a rubric or the margin.
- *Would we notice:* (a) and (c) only after the fact, if someone compared hashes, which nothing requires. (b) not at all.
- *Guard (proposal; the design is task 6's under U-INT-4, and task 3's under U-ART-15):*
  - The harness computes every metric in an environment that runs no agent code.
  - Agent code runs apart, writes only its declared output, and has no network.
  - No agent sandbox and no agent code can write the harness's results, the run records, the ledger or the engine's behaviour files.
  - R-STATE-8's layout becomes a logical one, whose parts carry separate write permissions.
- *Control:* four planted attacks, each run twice:
  - a session writes a result and a verdict;
  - harness-run code overwrites the result path;
  - harness-run code patches the metric;
  - a session edits the margin file.

  With the guard on, each fails, the number is unchanged and the attempt is recorded. With the guard off (scoring in the agent's environment, the run directory mounted writable), each changes the next decision.

### Majors

**EI-5 · major · The manuscript can launder an ablation's, a rebuttal's or another idea's number as the method's**
- *Where:* R-INT-8, R-STG-10.
- *Paper and reference:*
  - The Paper Enhancer revises "narrative claims and updating empirical tables and figures" [§3.5] (tex:sections/3_new_method.tex:130). It runs on Claude Code [App. A.2] (tex:sections/appendix.tex:155).
  - ScientistOne names this failure `cross_stage_cherry_pick`, with 4 confirmed cases: "the writeup LLM receives summaries from all four stages---including ablation---and picks the most favourable score from the entire pool" (ref:2605.26340v1:sections/012c_coe_audit_details.tex:148-160).
  - It also found a paper that "relabels a cost metric as ``utility'' and inverts the optimisation direction" (ibid., 131-134).
- *Draft:*
  - The verified table "holds the main and ablation results" (R-STG-10).
  - "every number in a manuscript traces to an entry of that table" (R-INT-8).
  - Figures are "made by a script from result files" (R-STG-10).
- *Attack:*
  - The writer quotes the best ablation variant, a rebuttal run on friendlier data, or a rejected idea's entry as the method's headline.
  - Or it quotes a derived number, such as a gain over the weakest entry.
  - Or it draws a figure from a raw result file.

  Each traces to an entry or a file, so the check passes.
- *Would we notice:* no. The check tests that a number is present in the table, not what it is attributed to. As written, the first half of R-INT-8's test is vacuous too: unless the scripted writer is made to reach for the log, the planted number cannot reach the draft, whatever the guard.
- *Guard (proposal; A-ART-7 and U-DRAFT-1 own the design):*
  - Each entry carries its role (method, baseline, ablation p_i, rebuttal t_i, other idea), code-snapshot hash, split, dataset, metric and direction, aggregation and seed count.
  - The method has one entry per dataset and metric: the pre-registered aggregate of C_best. There are no per-seed or per-round values to pick from.
  - The check binds each number in the manuscript to an entry. It fails a claim whose role, metric, direction or split differs from that entry's.
  - The harness computes derived numbers, and they become entries too.
  - The harness renders figures from the table.
  - The Enhancer's sandbox holds the manuscript, the table and read-only code, never the run directory.
  - One way to make the binding exact is to insert each number by entry ID and render it. That choice is task 6's.
- *Control:* three planted drafts, each of which fails the check:
  - one presenting an ablation entry as the main result;
  - one with a typed number;
  - one with a figure not rendered from the table.

  Twin with a value-only check: all three pass. A scripted writer that opens the run log fails.

**EI-6 · major · The rebuttal picks its own datasets, test caps and metrics, and no locked scorer exists for them**
- *Where:* R-STG-11, R-INT-1, R-INT-8.
- *Paper:*
  - The Rebuttal Coding Agent "implements and executes each planned task t_i using codebase C_best" [§3.5] (tex:sections/3_new_method.tex:126).
  - The one rebuttal shown chose "50 representative TALENT datasets" and set "Caps ... test <= 2000".
  - It added a new backbone, `tabpfn==2.0.9`, and its own "Inner-CV Self-Calibration Guard", with "margin delta=0.003".
  - From 4 wins, 24 ties and 2 losses in classification, it concluded that "the gains are real" [p. 51].
- *Draft:*
  - R-STG-11 sets the number of tasks and cycles, and says nothing about their data, splits, caps or metrics.
  - R-INT-1 says every reported metric comes from the harness, whose scorers cover only the manifest's benchmark.
  - Rebuttal numbers must then either bypass the harness or never be used. The draft does not say which.
- *Attack:* plan rebuttal experiments where the method wins, by choice of datasets, subsamples, metrics or comparators. Keep the favourable results. Or run the experiments on the test split.
- *Would we notice:* no. The selection happens before any result exists, and a result the paper omits leaves no trace.
- *Guard (proposal):*
  - A rebuttal task declares its evaluation (datasets, metric, split, caps) before it runs.
  - It may use only evaluation settings that the manifest registers with a locked scorer, on the validation split.
  - Every rebuttal result enters the verified table, whatever its sign.
  - The export records which entries the manuscript leaves out.
  - R-STG-11 lists U-INT-4 and U-TOP-5 (task 6). Which extra settings a manifest registers is task 5's.
- *Control:* a rebuttal task on an unregistered dataset is refused before it runs. A negative rebuttal result appears in the table, and the paper's omission of it appears in the export record. Twin without registration: the task runs, and only the favourable result appears.

**EI-7 · major · Attribution, and success reading (c), rest on one LLM verdict over ablations that the pipeline chooses, codes and can drop**
- *Where:* R-STG-9, R-INT-4 (its test), R-STG-4, R-MEAS-1, R-MEAS-2.
- *Paper:*
  - TeCh's variant "beat the baseline on 5/6 metrics", yet the ablation critic found that "the gains were primarily driven by general training controls (EMA and label smoothing)" [App. B] (tex:sections/appendix.tex:222-224).
  - On p. 41 the agent's own report says "Every component contributes ... directly rebutting the previous finding". Its own table shows the first two components making the six-set mean FPR95 worse, from 4.17 to 4.28 to 4.48 [p. 41].
- *Draft:*
  - `Reject` is an LLM verdict under a written rubric (R-STG-9).
  - The planner chooses the plans, and the Ablation Coding Agent writes them.
  - A filter-discarded ablation "is dropped, and the Ablation Critic reads the other runs" (R-INT-4's test).
  - The subset veto turns a marginal `Good` into `Engineer`. Engineering is tuning, which is where generic training controls enter. R-STG-4's "tunes and repairs code; it never replaces a component" has no test.
  - Neither R-STG-9 nor R-MEAS-2 names U-SUB-2, the register's tuned-baseline control.
- *Attack:*
  - No plan removes the mechanism while keeping the generic changes.
  - Or an inconvenient ablation is coded to underperform.
  - Or it breaks a rule and silently disappears.

  The critic then reads the agent's narrative and returns `Good`.
- *Would we notice:* only by reading the ablation code, which nothing requires.
- *Guard (proposal; A-ABL-1, U-ABL-5 and U-INT-1 are task 2's):*
  1. Every ablation pass runs a mechanism-off control. The planner cannot omit it, and the ablation coder cannot write it alone. One way: the idea's code declares its mechanism as configuration switches when it is first implemented. The harness then runs C_best with those switches off, every other change kept.
  2. A numeric veto on the ablation `Good`, like R-STG-4's veto on the subset `Good`: it stands only if the mechanism-off control loses at least the task's margin.
  3. A discarded ablation is re-run once, by a fresh session. If it is discarded again, the critic is told and `Good` is barred.
  4. The method–code audit checks each ablation variant, and each switch, against its plan.
  5. R-STG-9 and R-MEAS-2 list U-SUB-2 (task 6).
- *Control:* fixtures where the mechanism-off control matches C_best within the margin: the scripted critic's `Good` is vetoed. A discarded mechanism-off control bars `Good`. Twin without the veto: `Good` stands.

**EI-8 · major · No control shows that the numeric guards stop noise**
- *Where:* R-RUN-2 (the margin), R-STG-4, R-STG-8, R-PRIM-6.
- *Paper:*
  - No run-to-run variance is reported; the ± values are spreads across papers [§4] [Tab. 2] (claims.md, U-EVAL-4).
  - One critic rejected a variant as "statistically inert" [Tab. 16] (tex:sections/appendix.tex:325).
  - `docs/paper/claims.md` (P-EVAL-2) already gives task 6 "a null-idea control that measures the false-success rate".
- *Draft:* the margin is a manifest number that task 5 fills. Three things are missing:
  - nothing ties the margin to the harness's measured spread;
  - nothing counts the validation evaluations an idea or a session obtains;
  - no requirement measures how often the guards pass an idea that changes nothing.
- *Attack:* up to 10 ideas, each evaluated up to three times on the subset and three times on the full set, plus refinements: every evaluation is a fresh draw. With a margin below the noise, a no-op passes the veto, the Selector takes the luckiest, and reading (a) records a success.
- *Would we notice:* not in the loop. Reading (b), on test, would show a gain near zero, but reading (a) still counts the export.
- *Guard (proposal):*
  - The configuration refuses a margin below k times the baseline's measured run-to-run spread on the same split. The value of k, and the number of runs, are task 6's (U-ART-12, U-EVAL-4).
  - The records count every validation evaluation, per idea and per session.
  - The engine can run a placebo idea end to end, as configuration. The protocol and the rate are task 6's.
- *Control:*
  - Run the numeric guards on the baseline compared with itself, over repeated harness runs. With the margin at 0, about half pass; with the configured margin, almost none do. The measured false-pass rate is reported beside every success rate.
  - Mock twin: noisy fixtures pass at margin 0 and fail at the configured margin.

**EI-9 · major · The comparison rule can be gamed through what it does not read**
- *Where:* R-RUN-2 (the rule), R-PRIM-6, R-STG-4, R-STG-5, R-STG-8, R-MEAS-2.
- *Paper:*
  - App. B names "Unmeasured trade-offs" as a classic failure: on Pinet "the dominant edit removes exactly the solver work that controls constraint violation, which is not in the registered metric" (tex:sections/appendix.tex:229-232).
  - It credits AutoSOTA with a red line against this: "R4 constrains cross-metric trade-offs" (tex:sections/appendix.tex:236).
  - The paper's own LFR-Engram is called "a new state-of-the-art method ... outperforming the human baseline Engram" (tex:sections/4_experiment.tex:38). Yet its EM is 0.084 against Engram's 0.004, and lower is better [Tab. 6] (tex:tables/ablation_review_refine.tex:9-10).
- *Draft:* the rule is "primary metric, datasets, direction, aggregation and margin". Nothing says what a dataset with no result, a NaN, a timeout or a crash counts as.
- *Attack:*
  - Code that crashes or times out on the datasets where it loses, so that an aggregate over the datasets that ran improves.
  - Or a gain on the primary metric, bought with a secondary metric: constraint violation, calibration, memorisation, cost.
- *Would we notice:* the harness "reports every one of its settings" (R-RUN-2), so a crash is in the record. But no decision and no gain is defined to count it.
- *Guard (proposal; A-ABL-3 is task 2's, the values task 5's):*
  - A result that is missing a dataset or setting of the rule, or holds a non-finite value, fails the rule. In the reported gain, it counts under task 6's failure convention (U-EVAL-1).
  - The rule carries guardrail metrics with non-inferiority bounds.
  - The harness reports every metric of the benchmark beside the primary one.
- *Control:* fixtures in which the new result omits its losing dataset, or breaks a guardrail bound, do not replace the kept result. Twin that aggregates only over the datasets available: they do.

**EI-10 · major · Compute scaling passes every guard**
- *Where:* R-STG-2 (the content rule), R-RUN-2 (the compute field), R-STG-4, R-OPS-8.
- *Paper:*
  - App. B contrasts a method with "a pure compute-scaling knob that our idea generator deliberately does not propose" (tex:sections/appendix.tex:243-245).
  - In Table 16, AutoSOTA's gain on DMSQD comes at "+33% evaluations per iteration (unreported)" (tex:sections/appendix.tex:283-284).
- *Draft:*
  - The exclusion is "a written content rule" for the Idea Generator (R-STG-2): a prompt.
  - The engineers may tune.
  - The manifest names "the compute" (R-RUN-2), but no requirement enforces it at evaluation, or records what a result used.
- *Attack:* more epochs, a wider model, more samples or evaluations per step, an ensemble, test-time augmentation. The number moves; the method does not.
- *Would we notice:* no. Compute is not recorded with results.
- *Guard (proposal):*
  - The harness evaluates every candidate, and the baseline, within the manifest's compute envelope.
  - It records the compute each result used: GPU-hours, parameters, evaluations.
  - Compute is a guardrail metric of the rule (EI-9).
  - The content rule stays, as a prompt, but is not counted as a guard.
- *Control:* a scripted idea that only doubles the epochs exceeds the envelope and is refused, or fails the guardrail. Twin without the envelope: it passes the veto.

**EI-11 · major · Judges read what the judged agent wrote, nothing tests them against it, and no judge's detection rate gates a run**
- *Where:* R-AGT-9, R-OPS-9, R-INT-4, R-INT-6, R-INT-7, R-STG-8, R-STG-9, R-STG-12.
- *Paper and reference:*
  - The p. 41 report argues with its critic in its own text [p. 41].
  - ScientistOne's majority vote missed an evaluator exploit seen by "only 2/5 judges" (ref:2605.26340v1:sections/012c_coe_audit_details.tex:234-237).
- *Draft:*
  - Every agent reads everything its stage hands it (R-OPS-9). So the critics, the Selector, the filter and the auditor all read code, logs and reports that the judged agents wrote.
  - The golden sets "run against the mock judge in CI, and against the real model on demand, with the result recorded" (R-AGT-9). That sets no threshold and no gate.
  - The filter must have a golden set, but none of its cases is given.
  - R-INT-4 to R-INT-7 test detection only against scripted mocks.
- *Attack:* text addressed to the judge flips its verdict. It can be a comment, a log line or a README ("reading the labels here is for logging only, which rule 3 permits"), or a persuasive results narrative. The verdicts at risk are the filter's discard, the alignment verdict, the ablation verdict, and the Selector's choice among near-ties.
- *Would we notice:* no. The verdict is recorded with a reason that echoes the planted text.
- *Guard (proposal):*
  - Each judge's golden set holds pairs: the same case with and without text addressed to the judge. The two verdicts must agree.
  - The filter's set holds ScientistOne's documented exploits: evaluator import, environment-gated tuning, edits outside the allowed code, test-label reads, evaluator gaming.
  - A configuration may produce a reported run only if each judge, with its exact prompt and model, has a recorded pass on its set at a stated threshold. The report carries those rates.
- *Control:* the pairs themselves. And a judge whose prompt is weakened on purpose must fail the gate.

**EI-12 · major · The reported judge is kept apart from one reviewer, by an exact match, with nothing during development**
- *Where:* R-MEAS-5, R-AGT-5, R-MEAS-6, R-STG-12.
- *Paper:*
  - The Stanford Agentic Reviewer "serves as a held-out evaluator that was unseen during development by both the baselines and our method" [§4] (tex:sections/4_experiment.tex:5).
  - In review round 2, ScholarPeer's acceptance rises from 79.6% to 93.9%, while the held-out reviewer's falls from 73.5% to 69.4% [Tab. 5] (tex:tables/ablation_rebuttal.tex:13-14).
- *Draft:*
  - R-MEAS-5's test rejects only a reporting judge that is "the in-loop reviewer, the same system and model".
  - It leaves out the Meta-Reviewer. The loop also optimises against its verdict, and its approvals are a reported count (R-STATE-6, R-MEAS-1).
  - It also leaves out model families and prompt lineage.
  - Nothing records or limits queries to the reporting judge during development.
  - R-AGT-5 says ScholarPeer "is never the judge whose numbers are reported", while R-MEAS-6 rebuilds "a score per review round", which is ScholarPeer's score.
- *Attack:*
  - The reporting judge shares a model or a prompt lineage with an in-loop judge.
  - Or we tune prompts while watching the held-out judge, which makes it in-distribution.
  - Or ScholarPeer's numbers reach a report through R-MEAS-6.
- *Would we notice:* no. Queries made during development leave no record.
- *Guard (proposal; which judge to report is task 6's, U-EVAL-3):*
  - R-MEAS-5 covers every in-loop judge of the manuscript: ScholarPeer, the Meta-Reviewer, and the in-loop reference and alignment checkers. It compares system, model family and prompt lineage.
  - Every query to the reporting judge goes into a ledger with its purpose. A query outside a final evaluation is refused, or flags the report.
  - In-loop judges' numbers are reported only labelled as in-distribution. This resolves the conflict between R-AGT-5 and R-MEAS-6.
- *Control:* a configuration whose reporting judge shares the Meta-Reviewer's model fails validation. A query made during development appears in the ledger and flags the next report. Twin without the ledger: nothing records it.

**EI-13 · major · The post-hoc audit is kept apart from the wrong agent, and the draft does not separate ScientistOne's procedure from ours**
- *Where:* R-INT-7.
- *Reference (verified at the source):*
  - **I1** compares "The paper's reported score" with "scores obtained by re-running the submitted solution on the golden evaluator". A paper passes "within an adaptive tolerance that accounts for evaluator noise" [Ref: meng2026scientistone §5] (ref:2605.26340v1:sections/05_coe_audit.tex:25-26). ScientistOne's own runs used five evaluator runs and a tolerance of max(1%, 3σ/|s̄|) (paraphrase) (ref:2605.26340v1:sections/06a_setup.tex:10).
  - **I2** uses LLM judges "with majority vote across multiple runs" (05_coe_audit.tex:32), 3 of 5 (012c_coe_audit_details.tex:302).
  - **I4** counts as misaligned "only cases where the paper describes a fundamentally different algorithm", by majority vote (05_coe_audit.tex:43-44).
  - **I3** queries four academic APIs, and an LLM cross-checks each entry for "near-misses and citation gaming" (05_coe_audit.tex:36-37).
  - **Human review:** "all flagged positives for I1 ..., I2 ..., and I3 ... were manually reviewed and corrected by human reviewers before reporting". I4 was only sampled (012c_coe_audit_details.tex:54-57).
  - **Judge models:** ScientistOne's I2 and I4 judges were Gemini 3.1 Pro (012c_coe_audit_details.tex:46, 48), which was also the backbone of every system it audited (06a_setup.tex:27). It did not keep its judges apart from the authors by model.
- *Draft:* "its judge is not the agent that repaired the paper in the loop", meaning the writer. But the loop optimised the code and the paper against the in-loop filter, reference check and alignment audit (R-INT-4 to R-INT-6), which are the same four kinds of check. A post-hoc judge with their model and prompt re-runs the gate the loop was optimised against. R-INT-7 also states no tolerance; that is U-NOTE-4's, task 6.
- *Attack:* none is needed. The audit passes because it is the in-loop check run again. This breaks CLAUDE.md's rule "The judge we report is never the reviewer we optimise against".
- *Would we notice:* no. The analogue of Table 7 reads zero failures.
- *Guard (proposal, for task 6 under A-INT-3, U-EVAL-5 and U-NOTE-4):*
  - The post-hoc judges differ from every in-loop checker and fixer in model or system.
  - The engine never sees their prompts or verdicts.
  - R-INT-7 records which parts follow ScientistOne: the four checks, the re-run on a golden evaluator, the majority votes, the I3 APIs, and the lenient I4 rule.
  - It also records which parts are ours: every reported number is in scope, where ScientistOne checks "The paper's reported score"; the harness is the golden evaluator; and the judges are kept apart in model.
  - ScientistOne hand-checks flagged positives only. That removes false alarms, but never catches a miss. I propose that task 6 also hand-check a random sample of passes.
- *Control:* a configuration whose post-hoc alignment judge is the in-loop auditor fails validation. A planted misalignment, which the in-loop auditor is scripted to miss, is caught by the post-hoc judge. In the twin where the two judges are the same, it is not caught.

**EI-14 · major · "Used once" has neither a refusal nor a ledger, so repeated runs, re-runs and chained runs can select on the test split**
- *Where:* R-INT-3, R-RUN-3, R-RUN-5, R-OPS-4, R-OPS-7, R-MEAS-7, R-MEAS-8.
- *Reference:* the rule bends even in the reference system.
  - ScientistOne states "No run was re-attempted to improve solver scores" (06a_setup.tex:29).
  - Yet on MLE-Bench it let the agent "query the grading server up to 16 times to obtain evaluation scores on the test data", which "deviates from the official MLE-Bench protocol" (012c_coe_audit_details.tex:567).
- *Draft:*
  - R-INT-3's test counts test calls in a normal run, and never attempts an early or a second call.
  - Nothing records test uses across runs, audits or development.
  - R-MEAS-7 foresees repeated runs, but nothing says which run of a task is reported, or when a task may be run again.
  - Budgets are not fixed before the first run (R-OPS-4).
  - A chained run's G is the previous export (R-RUN-3), and its reference numbers may be test results.
- *Attack:*
  - Run a task again, after a failure, after raising its budget, or for no stated reason, until it succeeds.
  - Or report the best of N runs.
  - Or feed one link's test number into the next link's manifest.
- *Would we notice:* failed attempts are in the ledger (R-MEAS-8), but nothing ties them to the reported numbers.
- *Guard (proposal; U-TOP-5 and U-EVAL-4 are task 6's):*
  - The harness refuses a test evaluation before an export, and a second one for the same export.
  - An append-only test-use ledger records every test-split execution: who ran it, why, the code hash, and the run.
  - Every attempt of a task is reported, and a pre-registered rule names the one that counts.
  - A re-run needs a recorded infrastructure reason.
  - Budgets are fixed before a task's first run.
  - A chained run's manifest carries only the previous link's validation numbers.
- *Control:* an early and a second test call are refused and recorded. Twin without the refusal: the second call returns a number. A report that omits a recorded attempt fails its check.

**EI-15 · major · Development-time overfitting: nothing separates the tasks we tune on from the tasks we report, or freezes the engine first**
- *Where:* R-MEAS-9, R-OPS-2, R-OPS-6.
- *Draft:*
  - Behaviour is data: prompts, rubrics, margins and thresholds (R-OPS-2). We and our coding agents will tune all of it.
  - R-MEAS-9 fixes a selection rule and flags "a task added after the first run". It does not flag a task removed after the first run, and it does not separate development tasks from reported ones.
  - TODO task 5 plans "about three cheap development tasks and a test set", but no requirement carries it.
- *Attack:* we iterate prompts, rubrics and margins on the reported tasks while seeing their test numbers. The engine fits those test sets without any agent misbehaving.
- *Would we notice:* no.
- *Guard (proposal; task 5 chooses the tasks):*
  - Reported tasks are disjoint from development tasks.
  - Every behaviour file is hashed, and the configuration frozen, before the first reported run.
  - Each reported number names the configuration hash that produced it.
  - A task removed after the first run stays in the report, with its reason.
- *Control:* a report that mixes configuration hashes, or lacks a pre-registered task, fails its check. Twin: it passes silently.

**EI-16 · major · The manifest, its rule and margin, and the evaluator are pinned by a hash that is checked after the fact, against itself**
- *Where:* R-STATE-1, R-INT-2, R-RUN-2, R-MEAS-2.
- *Draft:*
  - R-STATE-1's test compares the task files' hashes "after the run as before it". That misses an edit restored before the run ends.
  - R-INT-2 checks the evaluator "against the manifest", which an edit of both passes, and only "before every run", not at every evaluation.
  - "the task's rule fixed before the run" (R-MEAS-2) has no test.
  - No decision records which manifest it read.
- *Attack:* change the margin or the rule mid-run and restore it; or change it after seeing results, which we can do; or edit the evaluator and the manifest's hash together.
- *Would we notice:* only if the mid-run change left a trace, which nothing requires.
- *Guard (proposal):*
  - Manifests are pinned before a task's first run, by hashes recorded outside the run, in a pre-registered list in the repository.
  - Every result and every decision record carries the manifest and evaluator hashes it used. The component that launches the evaluator checks them at every evaluation.
  - A rule or margin changed after the first run makes a new manifest version, and each result is reported under the version it was computed with.
- *Control:* a mid-run edit of the margin fails on the real mount. In the twin with a writable mount, it shows up as a different hash in the next decision record.

**EI-17 · major · The baseline, the reference of every decision in the loop, is agent-written, unfiltered and unaudited, and checked on an unnamed split**
- *Where:* R-STG-3, R-STG-6, R-INT-4.
- *Paper:*
  - The trace's "X-Maha (reproduced)" is "recomputed by this same script" [p. 41]. It trails the paper's FPR95, 4.17 against 3.76, so the stated gain is "1.99pp over the reproduced X-Maha and 1.58pp over the paper" [p. 42].
  - The audit "only audited the Ours method (not the baseline)" [p. 47].
- *Draft:*
  - The Baseline Coding Agent writes C_base.
  - R-INT-4's list of experiments the filter checks leaves out the baseline.
  - R-STG-3 checks the baseline against "the manifest's reference numbers" without naming the split. Its *Depends on* omits U-TOP-5, although task 6's brief asks "whether the check that the baseline reproduces (U-BASE-2) may read the test split".
  - The tolerance reads as two-sided, and is not tied to noise.
- *Attack:* a reproduction weaker by up to the tolerance inflates every in-loop margin and the gain against "our reproduction". The weakness can be fewer epochs, a missing trick, or a protocol slip that every idea inherits and then "fixes".
- *Would we notice:* R-MEAS-2's gain against the published number would show the gap. Nothing in the loop would.
- *Guard (proposal):*
  - The baseline run goes through the filter, and through the method–code audit against G's paper.
  - R-STG-3 names its split by reference to U-TOP-5, and lists U-TOP-5 under *Depends on*.
  - The check is one-sided, with a tolerance set from measured noise. A weaker baseline stops the task; a stronger one passes and is recorded.
- *Control:* a fixture baseline below the reference by more than the tolerance stops the task. A protocol slip planted in C_base is discarded by the filter. Twins without the check and without the filter: round 0 starts.

**EI-18 · major · Task 6's blocking rows are missing where requirements rest on them, and six decisions that task 6 will constrain are marked final**
- *Where:* `docs/requirements.md` (the decisions table, and "What the requirements leave to other tasks"); R-STG-3, R-STG-9, R-STG-10, R-STG-11, R-STG-12, R-INT-4, R-INT-5, R-INT-6, R-INT-8, R-MEAS-2.
- *Draft:*
  - The HANDOFF's rule, for when task 6 lands, is to "check every requirement that lists U-INT-4, U-TOP-5, A-INT-1 or A-INT-3 under *Depends on*".
  - R-STG-9, R-STG-10, R-STG-11, R-STG-12, R-INT-5 and R-INT-8 list none of the four. Yet each either reads or writes harness numbers (the ablation, the draft, the rebuttal, the meta guard, the writers) or is a gate inside the run. R-STG-12 names no dependency at all.
  - R-STG-3 omits U-TOP-5 (EI-17).
  - R-INT-4, R-INT-5 and R-INT-6 omit A-INT-1. Task 6's brief states that row's question as "Which checks block inside the run, which only measure after it".
  - R-MEAS-2 omits U-INT-4 and U-SUB-2.
  - Task 6's brief (its R7) says its decisions will constrain A-FULL-1, U-BASE-1, U-BASE-2, U-INT-1, U-INT-3 and A-ABL-3. The decisions table marks all six confirmed or refined, as if final.
- *Attack:* not an agent's. Task 6 decides, the re-check skips six requirements, and their tests keep the reading from before the decision.
- *Would we notice:* only by a full re-read.
- *Fix (task 2):*
  - Add the missing rows under *Depends on*.
  - Mark those six decisions "provisional on task 6's U-INT-4, U-TOP-5, A-INT-1 and A-INT-3", in the decisions table and in the register's pointers.
- *Control:* `requirement_coverage.py` fails any requirement whose text names the harness, a split, a gain or the verified table, and whose *Depends on* names neither U-INT-4 nor U-TOP-5. Its self-test plants one such requirement.

### Minors

**EI-19 · minor · Requirement text adopts task 6's proposals, and the boundary check cannot see it**
- *Where:*
  - R-INT-7 takes U-EVAL-5's "part of the locked evaluation" and "not the pipeline's fixer", and U-NOTE-4's scope, "every reported number, baselines included".
  - R-MEAS-2 and R-MEAS-3 take U-EVAL-1's two references and three statistics.
  - R-INT-8 takes A-ART-7's "every number traced".
  - R-MEAS-1 takes A-EVAL-1's three counts.
  - R-STG-3 and R-STG-6 settle which code produces E_base (the agent's reproduction), which task 6's brief asks under U-INT-4.
  - `requirement_coverage.py` reads only the *Decides* field. It reports 0 problems, and its self-test plants only a *Decides* defect.
- *Risk:* task 6 decides otherwise, and the requirements silently disagree with it.
- *Fix:* write each such clause as "as task 6 decides (row); the register proposes …", or tag it inline with the row ID. The script then checks that every *Depends on* row appears in the *Requirement* text.

**EI-20 · minor · Seeds are the agent's to choose**
- *Where:* R-MEAS-7. The one trace used a single seed, "seed=0" [p. 40].
- *Attack:* try seeds on validation and hard-code the lucky one. Or ignore the harness's seed, so that N "seeds" are one draw with zero spread, and the margin looks large.
- *Guard and control:*
  - The harness supplies the seeds, and uses fresh ones at the final evaluation.
  - It flags zero spread for any method not declared deterministic.
  - A scripted solution that ignores its seed is flagged. Twin: it passes, with spread 0.

**EI-21 · minor · Verdicts are not bound to the code the harness ran, and a failure after a result can re-roll it**
- *Where:* R-INT-4, R-INT-6, R-STATE-4, R-OPS-7, R-STATE-7.
- *Attack:* the filter inspects one snapshot while the harness ran another. Or a unit that saw a poor result fails (a crash, the budget) and is retried for a fresh draw.
- *Guard and control:*
  - Every result, filter verdict and audit names its snapshot hash, and a decision reads a result only when the hashes match.
  - Once a unit has a harness result, a retry reuses it.
  - Mismatched hashes block the decision, and a retry after a result returns the same result.

**EI-22 · minor · The Selector's band is never tested against an out-of-band choice**
- *Where:* R-STG-8's test.
- *Fix:* add a case with three ideas: the leader, one within the margin, and one outside it. A Selector scripted to choose the third is overridden, and the override is recorded.

**EI-23 · minor · The in-loop reference check is weaker than ScientistOne's I3**
- *Where:* R-INT-5.
- *Draft:* the check "flags the citations it cannot resolve". ScientistOne's I3 also checks the full entry against the record it resolves, to catch "a real DOI attached to a fabricated description" (05_coe_audit.tex:37).
- *Fix:* resolve each entry, then compare its title, authors, venue and year with the record. The post-hoc I3 uses ScientistOne's four APIs (U-NOTE-4, task 6).

**EI-24 · minor · Gains are deterministic, but nothing shows that anyone can re-run them, or traces a reported number to its file**
- *Where:* R-MEAS-2, R-MEAS-3.
- *Fix:*
  - The gain computation is locked code, committed before the first run.
  - A test re-runs it from the stored result files in a fresh environment, and gets identical numbers.
  - Every number in our reports carries its result file, its hash, the harness commit and the manifest hash. A reader can then trace it from the file to the sentence that quotes it.

## 5. Verdict

The draft is not yet ready to be the integrity bar that task 3 designs against.

Where it decides task 2's own rows, the draft moves the right way:
- numbers now gate three decisions the paper leaves to an LLM's preference (R-PRIM-6, R-STG-4, R-STG-8);
- the peer stage never keeps the best-scoring manuscript;
- a `Reject` cannot fall back to another idea;
- the full-set critic judges against our own reproduction;
- failures stay in the denominators;
- several tests (R-PRIM-6, R-STG-4, R-RUN-2, R-MEAS-2) contain the attack they stop.

But a design could meet every integrity requirement as written while:
- agents read the test labels (EI-2);
- agent code shares the scorer's environment and the results directory (EI-4);
- the exported paper reports selected validation numbers as its results (EI-3).

Every acceptance test would stay green, because the tests run against mocks of the very guards they should prove, with no twin in which the guard is off (EI-1). R-INT-3 and R-STATE-6 also decide part of U-TOP-5, one of task 6's blocking rows.

Fix the four blockers before task 3 writes contracts against these files. Most majors cost one clause and one test case each. EI-18 is bookkeeping, and it keeps task 6's decisions from being lost when they arrive.
