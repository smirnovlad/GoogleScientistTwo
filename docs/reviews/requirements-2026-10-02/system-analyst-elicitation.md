# What the requirements must cover: a completeness elicitation for TODO task 2

- **Persona:** system-analyst, judging by what is missing. **Date:** 2026-10-02.
- **Mode:** read-only. I edited no file and changed no git state. I inspected the other worktrees with `GIT_OPTIONAL_LOCKS=0`.
- **Purpose:** an independent list of what `docs/requirements.md` must cover, made before any requirement is written. Each item has an acceptance test.
- **Boundary kept:** I decide none of task 6's rows (U-INT-4, U-TOP-5, A-INT-1, A-INT-3). Where a test depends on one of them, the test is written as conditional on it.

## How to read this

- **Labels.** None of these collides with an ID scheme the project uses.
  - `MISS-n`: a need that no P- element captures.
  - `CONT-n`: a contradiction among the inputs.
  - `ORPH-n`: a design element with no requirement behind it.
  - `CHK-n`: a kind of defect the coverage checker must plant and catch.
  - `Q-n`: a question only a human can answer.
- **Three voices, kept apart.**
  - "The paper" is arXiv:2609.19644v1 (2026-09-17). Every quote below was checked against `docs/paper/source/` on 2026-10-02.
  - "The register proposes" means a row's decision in `docs/paper/unspecified.md`. It is a proposal to the owning task, never a decision.
  - "I propose" marks my own proposals.
- **Ranking.** Within each part, rows are ordered by what they would cost to discover late, highest first.

## The inputs, and their state on 2026-10-02

| Input | Where | State |
|---|---|---|
| Task 1's deliverables | `docs/paper/` on `claude/requirements`, at `fb4c8b1` | PR #1 is open. `main` holds only the scaffold, `97f8e35`. |
| Working rules | `CLAUDE.md`, `TODO.md`, `DEVELOPMENT_PROCESS.md`, `.claude/brief.md` | The integrity and engineering rules are unchanged since the first commit, `97f8e35`, of 2026-09-27. |
| Task 1's persona reviews | `docs/reviews/paper-analysis-2026-09-27/` | Read for the needs they raised. |
| Task 4's reuse survey | `docs/findings/2026-10-02-reuse-survey.md`, on `codex/reuse-survey` at `3daceb3` | Done, but not on this branch. It changes what five P- elements can require (CONT-5). |
| A second requirements file, and engine code | the `codex/run-journal` worktree: `docs/requirements/run-journal.md` (RJ-1 to RJ-7), `scientist_two/run_journal/`, `tests/`, `examples/` | Untracked and uncommitted. Task 2's brief does not mention it (ORPH-1). |
| Task 6's four blocking decisions | `claude/integrity-blockers`, at `dad24ff` | None taken yet. The worktree holds no uncommitted file. |

## Summary: the ten findings that would cost most to find late

1. **No requirement covers the end of a run, when the test set is scored once** (MISS-1, CONT-2, Q-1).
   - CLAUDE.md shows agents validation numbers only, and scores the test set "once, at the end". The paper's own generated papers report test numbers.
   - So either the manuscript that was reviewed is not the one exported, or P+ reports validation numbers. No requirement says which.
   - Nor does any say what happens when a test number contradicts a claim written from validation numbers.
   - Found late, this means adding a new stage at the tail of the pipeline.
2. **The paper's "full benchmark" puts test numbers in front of agents, and so do its chained runs** (CONT-1, CONT-3, Q-2).
   - The full-set stage, the Selector and the register's proposal for A-FULL-1 all read "the full benchmark".
   - A chained run hands P+, with its test numbers, to the next run's agents.
3. **Task 6 has not yet taken the decisions that many task 2 rows rest on.**
   - Seven of task 2's 17 blocking rows depend on them, and at least four of its 12 `number` rows.
   - No decision exists on `claude/integrity-blockers` on 2026-10-02.
   - Each dependent requirement needs an explicit pending marker that the checker counts (CHK-13). Without one, task 2 decides task 6's rows silently, by assuming the register's proposals.
4. **The current coverage check cannot fail on task 2's condition.**
   - `trace_coverage.py` reports 0 problems today with all 177 Requirement cells still reading `— (task 2)`, because it never reads that column. I ran it and counted the cells.
   - Part 6 lists the defects a new checker must plant.
5. **The paper's in-loop reviewer cannot be run, and its stop threshold means nothing until recalibrated** (CONT-5, MISS-8, Q-4).
   - Task 4 found no author-published ScholarPeer implementation.
   - App. A.2's threshold of 8 is a point on ScholarPeer's own scale.
   - The question U-PEER-3 put to task 4 now has its answer, and the decision that follows has no owner.
6. **No stage has a failure branch, and the resume granularity is in dispute** (MISS-3, MISS-4, CONT-6, Q-5).
   - Every stage file reads "On failure: UNSPECIFIED".
   - CLAUDE.md's "resumes from the last finished stage" comes from the initial note (N-81). It predates the analysis's finding that the checkpoint unit must sit inside A_Coder, where most of the cost is.
7. **Observability is filed as a configuration detail** (MISS-5, MISS-6).
   - Two capabilities are requirements with tests: the step-by-step decision trail of each idea, and an audit row for every change of the core state.
   - The nearest register row, U-ART-10, is filed under task 3 as `later`.
8. **Four numeric gates each say "pre-registered", and nothing ties them together or owns their values** (MISS-9, CONT-7, Q-6).
   - The four rows are A-ABL-3, U-SEL-1 and U-SUB-1 (task 2) and U-EVAL-1 (task 6).
   - Three of the values they need have neither a value nor an owner: the margin, the near-tie band and the tolerance.
9. **A second home for requirements, and engine code, exist outside task 2** (ORPH-1, CONT-9, Q-7).
   - `codex/run-journal` defines RJ-1 to RJ-7 and code that implements them, all untracked.
   - It also decides the unit of work, which is task 3's blocking row U-CFG-2.
10. **The integrity-hook proposals roughly double the session count that task 5 will price** (CONT-8).
    - Read widely, U-INT-1 and U-INT-3 add up to 70 + 4N_p + 4N_t coding sessions.
    - analysis.md §9 sets the bound at 68 + 4N_p + 4N_t and counts none of them.
    - At N_p = 6 and N_t = 3, the bound rises from 104 to as much as 210.

## Part 1. Needs that no P- element captures

**Integrity rules: a boundary note.** The seven integrity rules in CLAUDE.md (lines 43-49) are task 6's to turn into requirements. Task 2's requirements need to reference each one. A stage requirement whose behaviour depends on one must name it, which is what MISS-2 does for the first rule.

| ID | The need, in one line | Source | One acceptance test | Owner, and boundary |
|---|---|---|---|---|
| MISS-1 | At the end the test split is scored once. The manuscript is then reconciled with it: which numbers P+ reports, and what happens when a test number contradicts a claim written from validation numbers. | CLAUDE.md "Research integrity": the test set "is used once, at the end", and the writer "sees only verified results". Register U-TOP-5 (task 6). App. D's generated paper reports every result on test (artifacts.md P-ART-9, [p. 61]). | A fixture whose validation results show a gain and whose test results do not. The harness log shows exactly one test-scoring job per task. The export follows the branch chosen in Q-1. The reviewed and exported manuscript versions are both recorded, with their hashes. | A stage nobody has written yet. It depends on task 6's split decision, and on Q-1. |
| MISS-2 | Every coding step returns code, and the harness returns E. If U-INT-4 is confirmed, the outputs of ten P- elements change: P-BASE-1, P-SUB-1, P-SUB-3, P-FULL-1, P-FULL-2, P-ABL-2, P-ABL-4, P-PEER-4, P-META-3 and P-CODER-1. | CLAUDE.md: "Metrics come only from the locked evaluation harness". Register U-INT-4 (task 6, `blocks 3`), undecided. The paper has the coder "producing the resulting logs" [§3.2] (tex:sections/3_new_method.tex:40). | Conditional on U-INT-4. A mock coder writes a fabricated results file. Every critic, guard and Selector logs input numbers equal to the harness's, and the fabricated file is never read. | Task 6 decides. Task 2 references the decision in all ten requirements, with a pending marker (CHK-13). |
| MISS-3 | Every step has a failure branch, for an agent exception, a timeout, an empty output, a verdict outside the vocabulary, and a tool outage. | CLAUDE.md "Engineering rules": "the failure branch of every step". Every stage file reads "On failure: UNSPECIFIED (U-TOP-2)". Register U-TOP-2 (task 3, `blocks 2`). | Inject each fault at each type of step. The specified branch runs: at most n retries, then a recorded outcome. The run never hangs. A judge's malformed verdict never maps to accept or `Good`. | Task 3 sets the policy. Task 2 requires that every branch exists and ends in a recorded outcome. |
| MISS-4 | A crash never re-spends paid work that completed, at a granularity finer than a stage. | CLAUDE.md "Long runs resume" (2026-09-27, worded as the note's N-81). analysis.md §8: the unit "must sit inside A_Coder". Register U-CFG-2 (task 3, `blocks 2`). | Kill a mock run after its k-th paid operation, for every k. After restart, each paid operation appears exactly once in the ledger, and the export's hashes equal those of an uninterrupted run. | Task 3 decides the unit of work. Q-5 decides CLAUDE.md's wording. |
| MISS-5 | Each idea has a decision trail: why it was pruned, promoted or selected, step by step, with the numbers each judge read. | CLAUDE.md: "Log each unit of work" and "Keep run history as data you can query". The paper calls its process "measurable, reproducible, and transparent" [§1] (tex:sections/1_introduction.tex:10). Register U-ART-10, filed under task 3 as `later`. | For any idea ID in a finished mock run, one query returns the whole trail. It holds the idea's origin (seed rank, or the traces it evolved from), its novelty score with references, and every verdict with its feedback and the harness numbers the judge read. It also holds every engineering step with its code version, the full-set verdict, and the Selector's reasons. A pruned idea's trail ends at the verdict that pruned it. Every stage exit, skips included, has a reason. | Task 2 states it. U-ART-10's priority understates it. |
| MISS-6 | Every paid operation and every state change leaves a durable audit row. | P-STATE-9: the core state is replaced only when the Result Comparison Agent prefers the new result [§3.4] (tex:sections/3_new_method.tex:112). CLAUDE.md "Cost is bounded and recorded". | Every replacement of (h_best, E_best, C_best) has one row: the old and new versions by hash, the guard's inputs, the rule's version, and the decision. A write that bypasses the guard is refused in a test. Every paid call has exactly one ledger row. | Task 2 states it. Task 3 designs the store. |
| MISS-7 | A budget guard runs per session and per task. An unknown cost stays unknown. The branch taken at the limit is defined. | CLAUDE.md "Cost is bounded and recorded" (from the note's N-97). Register U-COST-1 (task 5). | (a) With a per-task budget B and mock costs, no operation starts once committed plus in-flight spend would exceed B, and the task record says "budget exhausted". (b) A per-session cap stops a running mock coding session. (c) One operation of unknown cost makes the task total read "incomplete, at least X", never just X. | Task 5 sets the values. Q-8 decides the branch at the limit. |
| MISS-8 | The in-loop reviewer is a stand-in for ScholarPeer, and its stop threshold is calibrated to the stand-in's own scale. | App. A.2: the loop stops "if the ScholarPeer review score reaches 8" (tex:sections/appendix.tex:155). Task 4 (2026-10-02) found no author-published implementation, and wrote that the threshold "cannot be transferred to a new reviewer until its score scale is calibrated". Register A-EVAL-3 (task 6). | The paper profile's threshold is derived by a recorded rule from a recorded calibration set. One such set is the stand-in's scores on accepted papers of the task's venue. The threshold is stored with the reviewer's version. A change of reviewer version without recalibration fails configuration validation. | No owner. Task 4 has answered U-PEER-3's question. Q-4. |
| MISS-9 | One per-task comparison rule serves every numeric gate: metric, datasets, direction, aggregation, margin, seeds and tie rule. | Register A-ABL-3, U-SEL-1 and U-SUB-1 (task 2) and U-EVAL-1 (task 6) each say "pre-registered". Table 15 says the engine "has no target metric" (tex:sections/appendix.tex:176). | Four consumers read the same rule object, by hash, from the task manifest: the subset guard, the Selector's pre-selection, the Result Comparison guard, and the reported gain. In a fixture, changing one field of the rule changes all four decisions consistently. | Split across tasks 2, 5 and 6. Q-6. |
| MISS-10 | "Reproducible" is defined so that it can fail. | CLAUDE.md: "Every run is reproducible from its recorded configuration, seed, code commit and container image". The paper asks that C+ maintain "execution reproducibility" [§3] (tex:sections/3_new_method.tex:12). | (a) Replay: a recorded run, re-executed with its recorded model and tool outputs, reproduces every decision and every artifact hash. (b) Re-execution: the harness re-runs C+ and reproduces every reported number within the task's tolerance. The run manifest records the engine commit, the image digest, the config hashes, the seeds, the model IDs the providers returned, and the external tools' commits. | Task 2 states it. Q-10 decides which level. |
| MISS-11 | The whole engine runs for $0 on mocks. | CLAUDE.md: "The whole engine must run in tests for $0". TODO task 7. Note N-98. | In a network-denied sandbox, an end-to-end run on a fixture task completes, with mocks for the LLM, the coding backend, search, drafting, the reviewer and the harness. Across fixtures, every termination branch is reached. No network call is attempted. The ledger totals $0 and holds no unknown entry. | Task 7 designs it. Task 2 states the requirement. |
| MISS-12 | When "everything" exceeds a model's context, the engine either fails loudly or applies a recorded bound. | CLAUDE.md: "The default is everything." Register U-EVO-2, U-SEL-2 and U-ABL-6 (task 3) hand one agent the whole codebases of up to 10 ideas. | A mock model with a small context limit gets an oversized input. Either the call fails with a recorded reason, or a bound is applied and recorded with who chose it and what it dropped. Silent truncation never happens. | Q-13 |
| MISS-13 | Behaviour is data, with named profiles: a "paper" profile equal to App. A.2, and cheaper development profiles. | CLAUDE.md: "Behaviour is DATA". TODO task 3's five changes. Note N-108 to N-114. | Two profiles run the same code. The call counts under each equal that profile's values. Each run records its profile and the hash of every data file it used: prompts, schemas, limits, routing and budgets. | Task 3 designs it. Task 5 sets the development values. |
| MISS-14 | Every stage is a configuration of one primitive, including any stage we add, and Listing 1 is itself one configuration. | analysis.md §3.4–3.5. The brief. | One parametrized conformance test covers all eleven Table 1 rows, plus A-FULL-1's full-set baseline if it is adopted. It also covers Listing 1's own values: discard at the limit, and `max_rounds` counting critic calls. It contains no stage-specific test code. | Task 2 states it. Task 3 designs it. |
| MISS-15 | A second coding backend, LLM provider or reviewer can be swapped in by configuration alone. | CLAUDE.md: a second implementation is "an interface or a base class, never a copy". The paper's §4.2 and Table 8 (P-ROSTER-48, P-ROSTER-49). | Swapping each in turn, the end-to-end fixture runs with the same control flow. A second task fixture runs with no code change. | Task 3 |
| MISS-16 | Least privilege. Judges cannot write. Each stage declares and enforces its sandbox policy for network, installs and GPUs. | CLAUDE.md: "Evaluation code and data are read-only to every agent". analysis.md §7: "Judges can write". The p. 47 auditor saved `repro_check.json` inside the task it audited. Register U-ART-15 (task 3). | A judge's write into the task tree is refused. A disallowed install or network call from a stage fails. The run record shows the policy in force. | Tasks 3 and 6 |
| MISS-17 | The export carries the provenance of every number in P+. | The paper pairs P+ with "a reproducible codebase" C+ [§3] (tex:sections/3_new_method.tex:7). Register U-ABL-3 (task 3) and A-ART-7 (task 6). | The export holds a manifest that maps every number in P+ to a harness result file and its hash. C+ holds the script behind each number. One unmapped number fails the export check. | Tasks 3 and 6 |
| MISS-18 | Run artifacts never carry a secret, an e-mail address or a local path. | CLAUDE.md: the repository "is public on GitHub". | Plant secrets in a run's environment. The logs, transcripts and exports contain none of them, and no absolute home path. Committed fixtures pass the same scan. | Task 2 states it. A leak, once pushed, cannot be undone. |
| MISS-19 | The autonomy boundary: which human steps, if any, may happen between launch and export. | The paper runs "an end-to-end discovery cycle without human intervention" [Abstract] (tex:sections/0_abstract.tex:2), repeated in [§5] (tex:sections/6_conclusion.tex:3). RJ-4: "`Unknown` blocks execution". | Between launch and export, the run log holds no human-input event, except stops of the kinds Q-9 allows, each recorded. | Q-9 |
| MISS-20 | Generation loops are bounded, and they reject duplicates. | §3.1 adds "distinct, higher-novelty ideas" until N_seed are gathered (tex:sections/3_new_method.tex:25-26). It sets no bound on attempts and gives no distinctness check. A_Evolve can re-propose an idea already evaluated. | A mock generator returns duplicates. The seed stage ends within M attempts, with a recorded outcome. A duplicate, by a stated rule, is never added or re-evaluated. | M has no value and no owner. |
| MISS-21 | G is validated at launch. | Register U-TOP-1 (task 3). P-STATE-1, P-BENCH-2. | Take each required manifest field in turn: evaluator, splits, subset, full set, rules, comparison rule, budget. With that field missing, the engine refuses to start before any spend, and names the field. | Task 3 owns the schema. |
| MISS-22 | Wall-clock bounds apply per session, per harness job and per task. | Fig. 10a gives only a mean of 2.51 days (claims.md P-COST-3). U-TOP-2. | Each coding session and each harness job has a timeout taken from the profile. Exceeding it takes MISS-3's branch. Wall-clock and busy time are recorded per stage (U-COST-3). | Task 5 sets the values. |
| MISS-23 | Parallel results enter the traces in a deterministic order. | Register U-TOP-4 (task 3). CLAUDE.md's reproducibility rule. | Two replays in which a round's A_Coder calls finish in different orders produce identical traces and identical A_Evolve inputs. | Task 3 |
| MISS-24 | A score that cannot be computed is unknown, not zero. | CLAUDE.md says this of cost: "never as zero". The same holds for the novelty score (U-SEED-2). | A search outage leaves the idea's novelty score "unknown". The sort places it by a stated rule, never as 0. | Task 3 |
| MISS-25 | Novelty retrieval excludes G's own paper, and records each reference's date. | Register U-SEED-2 (task 3) asks whether G's own paper is among the comparisons. A search run today can also return G's own follow-up papers. | No retrieved reference is G's paper. Each reference carries its date. Whether references dated after G are excluded follows Q-17. | Task 3. Q-17 |
| MISS-26 | Each agent has a success test. | TODO task 7: "A test per agent is therefore our own requirement". U-TOP-6. | Each judge has a golden set and a pass rule. The first cases come from artifacts.md §5. | Task 7 |
| MISS-27 | Concurrent runs share GPUs safely. | TODO task 3 lists "the sandbox and GPU queue" as a candidate. `docs/process/worktrees-and-sessions.md` says parallel sessions share GPUs. | Two concurrent mock runs on one GPU pool finish with disjoint run directories and correct ledgers. Queue time is recorded apart from busy time. | Task 3. Task 5 sets the values. |

### Quantities the requirements need, with no value or no owner today

| Quantity | Needed by | Value today | Owner today |
|---|---|---|---|
| Baseline reproduction tolerance | U-BASE-2 | none | none |
| Margin before the subset critic may say `Good` | U-SUB-1 | none | none |
| The Selector's near-tie band | U-SEL-1 | none | none |
| Aggregation across datasets and metrics, and what "strictly" means | A-ABL-3, U-EVAL-1 | none | task 6 or task 5 (Q-6) |
| The stand-in reviewer's stop threshold | P-CFG-9, MISS-8 | 8, on ScholarPeer's scale | none (Q-4) |
| Maximum attempts in the seed loop | MISS-20 | unbounded in the paper | none |
| Budget per task, and per session (dollars, turns) | MISS-7, note N-114 | none | task 5 |
| Timeouts per coding session, harness job and task | MISS-22 | a mean only, 2.51 days | task 5 |
| Seeds per harness number | U-ART-12 | none | task 6 |
| Retries per step | MISS-3 | none | task 3 (U-TOP-2) |
| N_seed, N_p, N_t | P-CFG-12, 15, 16 | none. Table 15 reports 5–6 ablations per paper. | task 5 |
| Development tasks, test tasks, and runs per task | the goal | the note proposes 3 + 5 | task 5 |
| Concurrent runs, and the GPUs available | MISS-27 | none | task 5 |

## Part 2. Task 2's 33 register rows

**Flags.**
- C: the proposal contradicts another source.
- U: underdetermined, meaning a value, a branch or an owner is missing.
- B: depends on another task's row.
- O: orphan, a mechanism that no decision consumes.

"Testable as written" means a pass/fail test can be written from the proposal's text alone, with no further decision.

| Row | Register proposes, in brief | Testable as written? | The acceptance test I would write | Flags |
|---|---|---|---|---|
| A-TOP-1 (`blocks 1`) | One exhaustion value per stage. SUB and FULL discard the idea as `Bad`. LIM keeps its last set. ABL and META keep the best, through their guard. PEER keeps the last manuscript, never the best-scoring one. | Yes | One parametrized test, with a mock assessor that never accepts, drives every stage config to its limit and checks the exit by hash. SUB and FULL: the idea is recorded `Bad` and its trace is kept. LIM: the last set reaches SEED. ABL: drafting receives h_best and the last pass's E_abl. PEER: the meta-reviewer receives the last enhancement, even when the mock gave an earlier version a higher score. META: the export is marked unapproved. | U: "discard" must not delete the trace, because A_Evolve reads the failure logs of `Bad` ideas [§3.3] (tex:sections/3_new_method.tex:68). U: no value is given if LIM's set is empty at the limit. C: ABL's spent-budget exit is not marked, though META's is (CONT-19). |
| A-TOP-2 (`blocks 1`) | Each limit counts judged refinements, "for all six" limits. | Yes | Run with mocks that never accept, and count calls. SUB and FULL: 1 coder call, 2 engineer calls, 3 critic calls. ABL: at most 1 A_FullEng call per pass. PEER: 3 reviews, 2 rebuttal cycles. META: 1 A_FullEng call, 2 meta-reviews. LIM: 17 extractor calls with 17 verifier calls, or with 16 under the critic-call reading. | C: register D-4 settled that LIM and PEER count rounds, and analysis.md §4 reads LIM as counting critic calls (CONT-10, Q-12). |
| U-BASE-2 (`blocks 1`) | Check E_base against the paper's reported numbers, with a per-task tolerance. On failure, end the task and record the reason. | Partly | Give a fixture a harness baseline outside the tolerance. The task record says "baseline not reproduced", and the ledger shows 0 idea-coding sessions. Inside the tolerance, the run proceeds. | U: no tolerance value, no owner, and no retry: one failed reproduction ends the task. C: the subset baseline on validation data has no published counterpart (CONT-4, Q-3). C: it leaves unguarded the full-set reproduction behind every reported gain. B: U-INT-4 and U-TOP-5. |
| U-FULL-1 (`blocks 1`) | FULL uses the subset's verdict map. At the limit the idea is discarded as `Bad`. A full-set `Bad` enters the traces. | Yes | Drive a mock full-set critic three ways. {`Good`} gives `Good`. {`Bad`} gives `Bad` with no engineering. {`Engineer` ×3} gives `Bad` after exactly 2 engineering sessions. Each outcome leaves a trace record holding the full-set E, C, d and r. | None beyond MISS-3's malformed-verdict branch. |
| A-ABL-2 (`blocks 1`) | When the guard fails, go on to drafting with h_best unchanged, as Figure 7 draws. Decide together with A-ABL-1. | Yes | Drive Refine, then A_FullEng, then a "not preferred" from the guard. The drafter's input hashes for h_best and C_best equal the pre-refinement ones. No second ablation pass runs. The stage exit is recorded as "refinement rejected". | U: unlike META's unapproved export, this exit is not marked, so the draft rests on a breakdown the critic did not accept (CONT-19). |
| A-ABL-3 (`blocks 1`) | A deterministic rule over the harness's validation results, with the metric, datasets and direction fixed per task. The agent's reading is logged, not decisive. | No: "strictly" has no aggregation, margin, seed count, tie rule or owner. | Once those are set: use fixtures where E_new beats E_best on the aggregate but not on one dataset, and the reverse. The guard's decision equals the rule's output whether the mock Result Comparison Agent prefers E_new or not, and the agent's reading is in the log. | C: §3.4 lets the agent's preference decide (tex:sections/3_new_method.tex:112). Record that P-ROSTER-19 becomes advisory, as a departure. B: U-INT-4, U-TOP-5, U-EVAL-1, U-ART-12. U: MISS-9. |
| U-EVO-1 (`blocks 1`) | Run the stop test after each round. | Yes | Script the 4th `Good` verdict to arrive as round 2's first candidate. Round 2's second candidate still runs, so A_Coder is called 2 + 2 + 2 = 6 times, and then selection starts. | None. It sets register D-2's failed-task floor of 17 at N_0 = 1. |
| A-BASE-1 (`blocks 5`) | Reproduce the baseline once per task, before round 0. A_Coder receives E_base and C_base, a recorded extension of Eq. 2. | Yes | Run with 10 ideas. The baseline coder is called once, before the first subset coder. Every A_Coder input record cites the same E_base and C_base hashes. The meta pass makes no baseline call. | B: U-SUB-2 (task 6) proposes "a refine value of the baseline row", so traceability's "zero rounds" for BASE would no longer hold (CONT-11). A-FULL-1 adds a second baseline. |
| A-FULL-1 (`blocks 5`) | Reproduce the baseline on the full benchmark, once per task and in the harness, and judge against it. Keep the paper's numbers for reporting. | Partly | The full-set critic's logged input holds the harness's reproduced full-set baseline, by hash, and never the agent's in-script baseline. A fixture with a weak in-script baseline does not change the decision. | C: "full benchmark" must mean the validation side of the grid (CONT-1). U: someone must write the full-set baseline code: a coding session, not the harness. U: this adds a stage that Table 1 lacks and a session that §9 omits, with no reproduction guard (CONT-4). B: U-INT-4, U-TOP-5, U-EVAL-1. |
| A-ABL-1 (`blocks 5`) | Add a `Reject` verdict that ends the task with a reason, and "weigh the alternative, a fall-back to the next `Good` idea". | No: the proposal leaves its own effect open between two options. | Once one is chosen, a mock critic returns `Reject`. Under "end", the task record says "ablation reject" and the drafter is never called. Under "fall back", the Selector's next choice enters ablation and the rejected idea is marked. | U: `Reject` is unspecified on a re-ablation after an update, and in the meta-restart pass, which runs the critic (A-META-1). Could a `Reject` after a meta refinement discard a draft that already exists? Q-11. |
| U-ABL-2 (`blocks 5`) | One A_FullEng call, whose results the harness scores. No nested critic loop. | Yes | On `Refine`: exactly one A_FullEng coding session, then one harness scoring job, then the guard. No full-set critic is called on that path. | B: U-INT-4. U-INT-1's filter also applies here, and a discard means the guard fails. |
| A-META-1 (`blocks 6`) | Re-enter at the start of the ablation row and run the whole pass, critic included. | Yes | After a meta `Refine` that passes the guard, the calls run in order: planner, N_p coders, ablation critic, drafter, reviewer. Pass 2 calls the ablation critic. | Interacts with A-ABL-1, if a `Reject` comes in pass 2. |
| A-META-2 (`blocks 6`) | Ask the meta-reviewer again. A second `Refine` exports that pass's P_new and C_best, marked unapproved. | Yes | Pass 2 calls the meta-reviewer. On `Refine`, with N_meta spent, the export's hashes equal pass 2's P_new and C_best. The record says "unapproved", and A_FullEng is not called again. | None |
| U-META-1 (`blocks 6`) | Budgets reset for each pass. The run state keeps a counter per pass. | Yes | In pass 2 an ablation `Refine` triggers one more A_FullEng call, and the pass runs up to 3 reviews. | B: "the run state keeps a counter" is task 3's design, so state only the observable count. It adds 7 sessions at N_p = 6 (register D-2), which task 5 must count. |
| U-BASE-1 (`blocks 7`) | The subset and the full set are manifest fields, fixed before the run, by us and never by an agent. The harness reports every setting of the full set. | Yes | (a) The manifest is hashed at launch and unchanged at export, and an agent's write to it is refused. (b) A fixture full set has 3 settings and the mock coder runs only 2. The harness report still lists all 3, with the missing one marked failed, so the A-ART-12 case cannot pass silently. | C: the proposal must place the subset inside the validation split (U-TOP-5). B: the manifest schema is U-TOP-1, task 3's. |
| U-INT-1 (`blocks 8`) | Filter after every experiment "that produces a reported number". A discarded result is invalid. An idea or refinement left with no valid result is `Bad`. | Partly | A mock filter returns "discard" after each type of experiment in turn: baseline, subset, full set, ablation plan, rebuttal task, A_FullEng. A filter call follows each experiment, and each discard has its specified effect. | U: subset results are never reported, yet they decide promotion. U: no effect is given for discarding an ablation plan or a rebuttal task, and no branch for the filter's own failure. C: §9's bound assumes φ = 0 (CONT-8). B: A-INT-3 and A-INT-1. |
| U-INT-3 (`blocks 8`) | Run the audits after every manuscript revision, and before export. | Yes | A mock Enhancer plants a fabricated citation in revision 2. The reference check after revision 2 flags it. The next review and the export carry the corrected entry. The exported P+'s hash equals the last audited version's. A run makes at most 6 method–code audits. | U: there is no branch for a repair that fails, or for a misalignment the writer cannot fix. C: §9's bound assumes μ = 0. B: A-INT-1 (task 6) and A-INT-2 (task 3). |
| A-TOP-3 (`number`) | Keep N_meta = 1 and §3.6's exit. Mark every export with its last meta verdict. | Yes | Run one fixture per termination branch. Every export record carries its last meta verdict and its branch, and a query counts approved and unapproved exports. | Extend the same mark to ablation exits (CONT-19). |
| A-SEED-1 (`number`) | Rank only. A novelty threshold is an optional ablation. | Yes | A mock Novelty Checker scores one idea far below the rest. The idea stays in H_0, last, and N_seed is unchanged. | Records §3.1's reading over §3's "filtering for those with high novelty" (tex:sections/3_new_method.tex:5). |
| U-SEED-3 (`number`) | The generator reads G, the limitations and the scored pool. A written rule excludes pure compute or budget scaling. | Inputs, yes. Behaviour, no. | The logged inputs hold the hashes of G, the limitations and the pool, and the rule is in the versioned prompt. Behaviour: at most k of n ideas on a golden set are pure scaling. | U: no judge of compliance and no pass rate. |
| U-SUB-1 (`number`) | An LLM verdict with a numeric guard: no `Good` without a pre-registered margin over E_base. | No | Once set: a mock critic says `Good` on a result below E_base + margin, and the recorded verdict is not `Good`. | U: the margin, its owner, and what the guard substitutes (`Engineer` while budget remains, or `Bad`?). B: U-INT-4 and U-ART-12. C: if U-SUB-2 tunes the baseline, the margin is over the tuned baseline. |
| A-FULL-2 (`number`) | The full-set engineering limit is 2. | Yes | `Engineer` ×3 at the full set gives exactly 2 full-set engineering sessions, then `Bad`. | None |
| A-EVO-1 (`number`) | A.2's rounds are k ≥ 1. Round 0 runs N_0 = 2. | Yes | Round 0 makes exactly 2 A_Coder calls, on the 2 top-scored seeds. Each later round makes 1 evolved call and 1 on the next unevaluated seed. | B: N_0 drives cost, and task 2 sets it while task 5 owns N_seed, N_p and N_t. Task 5's cost model must include it. |
| A-EVO-2 (`number`) | K = 4 rounds after round 0. | Yes | With every verdict `Bad`, A_Coder is called 10 times (2 + 4×2), and the task ends with "no `Good` idea". | None |
| U-EVO-4 (`number`) | Every task ends with a record: outcome, stage, a reason from a fixed list, and cost. | Yes, once the list is closed | Each termination branch gives exactly one task record, with a reason from the closed list and a cost that is either known or "unknown". | U: the list lacks budget exhausted, dependency unavailable, unresolved in-doubt operation (RJ-4) and human abort. "Error" needs the failing unit's ID. The success branches need reasons too. |
| U-SEL-1 (`number`) | A numeric pre-selection on the pre-registered validation metric. The LLM picks among near-ties and records why. | No | A dominant idea is chosen whatever the mock LLM says. Two ideas inside the band: the LLM picks and its reasons are logged. Outside the band, shuffling the input order does not change the pick. | C: under Eq. 4 the LLM chooses, so record this as a departure. U: the band and the rule for several metrics. B: U-TOP-5 and U-EVAL-1. |
| A-PEER-1 (`number`) | Two rebuttal cycles, so up to three reviews. | Yes | A mock reviewer that always scores below the threshold gives 3 reviews, 2 rebuttal cycles and 2 Enhancer calls. A first score at or above the threshold triggers no rebuttal. | C: the threshold belongs to ScholarPeer, which cannot be run (CONT-5, MISS-8). |
| U-META-2 (`number`) | A written rubric for the venue bar. The meta-reviewer also reads the verified results table. | Inputs, yes | The logged inputs hold the table's hash and the rubric's version. Golden case: DynaSpec-RAG claims a "strict do-no-harm" fall-back while 2 of 7 datasets regress, and the expected verdict is `Refine`. | B: the verified results table is task 6's design, and the golden-set pass rule is task 7's. |
| U-ABL-5 (`number`) | A written line between `Refine` and `Reject`, with three first cases. | Partly | Build three fixtures, each run k times, passing when at least m of k are right. A gain carried by EMA and label smoothing: `Reject`. A gain carried by one component, as in LC-FTT: `Refine`, naming what to strip. A p. 41-like breakdown: not `Good`. | U: the paper prints no TeCh numbers (traceability.md Part 3), so the fixture must be built, and k and m are unset. Depends on A-ABL-1. |
| U-EVO-3 (`later`) | Run the evolved idea alone. With N_seed ≥ N_0 + K·N_e this cannot happen. | Yes | With N_seed = N_0 in a mock profile, round 1 makes one A_Coder call and raises no error. | B: N_seed is task 5's. |
| U-DRAFT-2 (`later`) | Check compiling and format after every draft and revision. Make figures by code from result files, and check them against the method. | Partly | A mock drafter emits LaTeX that fails to compile, and the check fails into a defined branch. Every figure in P+ has a recorded script and the hash of its input. | U: no branch is given for a failed compile. The check against the method overlaps A-ART-7 (task 6). |
| U-ART-11 (`later`) | Re-score a refined idea that replaced a component, and perhaps rename it. Evolved ideas likewise. | Partly | An h_new whose component list differs from h_best's triggers a Novelty Checker call, and its score is recorded. | O: no decision reads the new score. U: no rule for renaming (ORPH-3). |
| A-ART-5 (`later`) | §3.2's engineers tune and repair code only. Changing components belongs to A_FullEng. | No | If kept: an engineering step whose component list changes is refused, or recorded. | C: §3.2 lets the engineer refine h (tex:sections/3_new_method.tex:45). U: no detector and no branch (ORPH-4). |

**Rows that hang on task 6.** Seven blocking rows depend on a task 6 decision: U-BASE-2, A-ABL-3, A-FULL-1, U-ABL-2, U-BASE-1, U-INT-1 and U-INT-3. So do four `number` rows: U-SUB-1, U-SEL-1, U-META-2 and A-PEER-1, which depends on A-EVAL-3. U-ABL-5 depends on task 7.

## Part 3. Contradictions among the inputs

| ID | Side A, with source and date | Side B, with source and date | What the requirements must do |
|---|---|---|---|
| CONT-1 | CLAUDE.md, 2026-09-27: "Every number an agent sees while searching is a VALIDATION number. The test set is used once, at the end." | The paper: the Selector compares ideas "evaluated on the full benchmark" [§3.3] (tex:sections/3_new_method.tex:90). App. B: the engine "evaluates on the paper's full benchmark grid rather than the single registered split" (tex:sections/appendix.tex:238-239). Register A-FULL-1, 2026-09-28: reproduce and judge "on the full benchmark". | Define the in-loop full set as every setting of the full grid, on the validation side. The test side is scored once, by MISS-1's step. Benchmarks with only train and test splits (SCOOD, per artifacts.md U-ART-5) need a validation split built, by task 5 or task 6. |
| CONT-2 | CLAUDE.md: the test set is used once at the end, and the writer "sees only verified results". | Register U-INT-3, 2026-09-28: when repairs run late, "the reviewed paper is not the exported one". App. D's paper reports every result on test [p. 61]. | If test numbers enter P+ after the review loop, the exported paper is not the one the reviewers judged. If they never enter, P+ reports validation numbers. No row covers this. Q-1. |
| CONT-3 | CLAUDE.md, the same rule. | The paper: "When VD-STrans is subsequently provided as context in the next discovery cycle" [§4.3] (tex:sections/5_discussion.tex:9). Register A-TOP-4 (task 3): the schema "also accepts a previous run's (P+, C+) as G". | A child run's agents read the parent's P+, which reports test numbers. Over three chained runs the test set is used three times, and two of the searches run on it. Q-2. |
| CONT-4 | Register U-BASE-2: "E_base checked against the paper's reported numbers with a per-task tolerance". | The paper runs the baseline "on the benchmark subset" [§3.2] (tex:sections/3_new_method.tex:37). U-TOP-5 (task 6) puts in-loop decisions on validation data. Research engineer, wave 2: "a subset inside the validation split, disjoint from test". | A validation-side subset has no published numbers to compare with. Checking a reproduction against published numbers means scoring on test before the search starts. The full-set reproduction that every reported gain is measured against stays unguarded. That is where the weak-baseline attack sits: in the one trace shown, the agent's own weaker reproduction widened the claimed FPR95 gain from 1.58 to 1.99 points (U-ART-16, U-ART-20). Q-3. |
| CONT-5 | The paper names ScholarPeer as the Peer-Reviewer Agent [§3.5] (tex:sections/3_new_method.tex:123). App. A.2 stops "if the ScholarPeer review score reaches 8" (tex:sections/appendix.tex:155). | Task 4, 2026-10-02: no author-published implementation was found, and the threshold cannot be transferred until it is calibrated. | P-PEER-1, P-PEER-2, P-ROSTER-21, P-ROSTER-46 and P-CFG-9 cannot be met as written. They map to MISS-8, as a recorded departure. Q-4. |
| CONT-6 | CLAUDE.md, 2026-09-27, in the wording of note N-81: "a crash resumes from the last finished stage". | analysis.md §8, 2026-09-28: "must sit inside A_Coder". Register U-CFG-2 (task 3): one session per coding call. RJ, 2026-10-02, untracked: "one external operation". | Read literally, CLAUDE.md would let a crash re-spend a whole stage. Idea refinement alone takes 45.4% of the cost [Fig. 10b] (image). Three authors have proposed three granularities. Task 3 decides; Q-5 settles CLAUDE.md's wording. |
| CONT-7 | Register A-ABL-3, U-SEL-1 and U-SUB-1 (task 2): a deterministic rule, a pre-registered metric, a pre-registered margin. | Register U-EVAL-1 (task 6): "A pre-registered rule per task (metric, datasets, direction)". | Four gates use four phrasings, with no shared object and no owner of the values. One rule object must serve all four (MISS-9). Q-6. |
| CONT-8 | Register U-INT-1, a filter after every experiment, and U-INT-3, an audit after every revision. | analysis.md §9: "Whole run, excluding integrity sessions (φ = μ = 0)", which is 68 + 4N_p + 4N_t. | Read widely, the filter adds sessions for: 6 coding steps per idea (60 over 10 ideas), the baseline, 4N_p ablation plans, 3 A_FullEng calls and 4N_t rebuttal tasks. The audit adds up to (1 + N_peer)(1 + N_meta) = 6. The bound becomes 138 + 8N_p + 8N_t, which is 210 rather than 104 at N_p = 6 and N_t = 3. A-FULL-1's extra baseline and its filter come on top. Task 5 must not price from §9's figure. |
| CONT-9 | TODO.md: "Phase 0 … (no engine code yet)". CLAUDE.md principle 3: "Requirements before code". | Vlad, 2026-10-02, recorded on `codex/reuse-survey`: "Btw do you understand that goal is to implement engine from that paper?" That session's handoff: a separate slice can be built "then reconcile it against tasks 2, 3 and 6". | There are now two homes for requirements and two ID schemes. A design decision, the unit of work, was taken before task 3. Vlad's words state the goal, but not whether code may come before requirements. Q-7. |
| CONT-10 | Register A-TOP-2: "judged refinements for all six". | Register D-4: "the limitation loop and the peer-review loop count rounds". analysis.md §4: "its 16th expansion is never judged". | The readings differ by one verifier call (17 against 16). Pick one and record why. Q-12. |
| CONT-11 | traceability.md's component column, 2026-09-28. P-BASE-1: "zero rounds". P-STATE-2: "read-only and hash-checked by the setup". P-ROSTER-19: the agent decides, per §3.4. P-TOP-3: eleven stages. | U-BASE-2 adds a guard to BASE, and U-SUB-2 adds a refine value. P-STATE-2's cell pre-decides U-INT-4 and A-INT-1. A-ABL-3 makes P-ROSTER-19 advisory. A-FULL-1 adds a stage. | Requirements copied from the component column would inherit four contradictions with the register. Record each departure, with its reason. |
| CONT-12 | traceability.md: P-STATE-13 is "overwritten each round", and for P-STATE-12 "each enhancement replaces it". | CLAUDE.md: "Keep run history as data you can query". | The paper's semantics fix what an agent sees: the meta-reviewer reads the last review. They do not fix what is kept. Each state requirement needs two parts: the view passed to agents, and the record retained. |
| CONT-13 | CLAUDE.md: "The default is everything." | Register U-SEL-2, U-EVO-2, U-ABL-6: whole codebases, for up to 10 ideas. | "Everything" will exceed the model's context window, and no requirement says what happens then. Q-13. |
| CONT-14 | The paper: "without human intervention" [Abstract] (tex:sections/0_abstract.tex:2) [§5] (tex:sections/6_conclusion.tex:3). | RJ-4: "`Unknown` blocks execution". CLAUDE.md's budget guard stops a run. | Our engine adds stops that wait for a person. The requirements must list the allowed ones, or autonomy cannot be tested. Q-9. |
| CONT-15 | App. A.2's values, P-CFG-1 to P-CFG-11. | The note's N-108 to N-114 (a development profile), PROPOSALs routed to task 5. TODO task 5: "cheap development tasks". | Both sets are needed. Make profiles data, with the paper profile equal to App. A.2 exactly (MISS-13). |
| CONT-16 | CLAUDE.md calls the note "unverified". | CLAUDE.md's integrity and engineering rules match the note's PROPOSALs almost word for word: N-81, N-84, N-85, N-87, N-92, N-93, N-95, N-97 and N-98. | These rules are design choices that Vlad committed on 2026-09-27, so this is not a conflict in substance. But a requirement that cites CLAUDE.md should also cite this origin, so the choice can still be questioned. CONT-6 shows why it matters. |
| CONT-17 | TODO task 2, and the brief: fill the column, "or map it from your file". | `trace_coverage.py` flags a P- ID that appears a second time in Part 2 ("duplicated"), and a gap ID that is in no source document's gap list ("unknown-gap"). README: "A writer edits only the files it owns". | A Requirement cell cannot say "as P-CFG-1". A gap that task 2 discovers cannot be cited in traceability.md until it is filed in a file under `docs/paper/`, which paper-analyst owns. Q-16. |
| CONT-18 | CLAUDE.md: "Each element of the paper maps to a requirement". | TODO task 2: "or to a recorded decision to leave it out". | A leave-out must be a recorded status that can be checked. |
| CONT-19 | Register A-TOP-3 marks unapproved meta exports. | Register A-ABL-2 and U-ABL-4 send an ablation the critic did not accept on to drafting, unmarked. | A-EVAL-1's reading (c) of success needs the ablation's exit verdict, so the record must carry it. |

## Part 4. P- elements to leave out, and mappings that are not obvious

### 4.1 Candidates to leave out of the engine's requirements

| P- ID | Element | Why it can be left out | Who decides | What still maps |
|---|---|---|---|---|
| P-EVAL-11 | The human evaluation [Tab. 10] | An evaluation with an unspecified protocol, not engine behaviour. | Task 5 (U-EVAL-6) | nothing |
| P-EVAL-12 | Figure 1a's radar | The quantity it plots is undefined. | Task 5 (U-EVAL-7) | nothing |
| P-EVAL-14 | Other systems' numbers | A comparison with other agents. None is planned. | Task 5 (U-EVAL-9) | nothing |
| P-EVAL-15 | Table 9's rating | No reviewer is named for it. | Task 6 (A-EVAL-8) | P-TOP-6 itself stays. |
| P-CFG-17 | N_a, the number of agents | No behaviour depends on the count. | Task 2 | The roster requirements. |
| P-ROSTER-50 | The Stanford Agentic Reviewer | Held out by definition [§4], and usable only by hand (task 4). | Task 6 (U-EVAL-3) | CLAUDE.md's separate-judge rule. |
| P-ART-10 | The generated pages in Figures 2 and 8 | They duplicate P-ART-9's evidence. | Task 2 | P-ART-9's format requirement. |
| P-ART-11 | One task's run layout | artifacts.md §4 calls it "a reference for our own design and not a specification". | Task 3 (U-ART-17) | nothing |
| P-BENCH-1 | The 107 tasks | Scope, not engine behaviour. | Task 5 | MISS-21: the engine runs any manifest that passes launch validation. |
| P-BENCH-3 | How the 64 ICML tasks were chosen | A process for task 5's own choice of tasks. | Task 5 (U-BENCH-2) | nothing |
| P-INT-5, P-ROSTER-51, P-EVAL-10 | The post-hoc CoE audit | Evaluation, not a stage, unless task 6 makes the checks gates. | Task 6 (A-INT-1) | Pending. Not a leave-out until A-INT-1 is decided. |

The checker needs a third status besides "implements" and "left out": **"replaces"**, a departure recorded with its reason. It applies to P-INT-1 (if U-INT-4 is confirmed), P-EVAL-2 (gains parsed by an LLM), the decisive role of P-ROSTER-19, ScholarPeer in P-ROSTER-21 and P-ROSTER-46, and the LLM choice of P-SEL-1.

### 4.2 Mappings that are not obvious

| P- ID(s) | The lazy reading | Where it actually belongs |
|---|---|---|
| P-TOP-1 | "The engine outputs P+ and C+" | Several places. The goal and the output requirements. P+ "should identify and resolve key ... bottlenecks" (tex:sections/3_new_method.tex:12), which the engine cannot test: that is a matter for task 6's reporting judge. C+'s reproducibility maps to MISS-10. "Measurable performance gains" maps to MISS-1 and MISS-17. |
| P-TOP-2 | "Implement Listing 1" | A conformance configuration of the primitive (MISS-14). No stage uses its values. |
| P-TOP-4 | "The pipeline" | The stage graph's nesting and fan-out fields. Test: a mock run's call sequence equals the reconstructed pseudocode, under the readings chosen. |
| P-TOP-5 | "Termination" | U-EVO-4's task record, plus A-TOP-3's mark, with one test per branch. |
| P-TOP-6 | "The schema accepts (P+, C+)" | The task interface, plus Q-2. The child run inherits the parent's harness, splits and rules. |
| P-CODER-1 | "A coder" | Composition: SUB and FULL in one call per idea, plus A-BASE-1's extension and U-CODER-1's trace for a pruned idea. |
| P-STATE-2 | "The harness" | Pending task 6. Its component cell already pre-decides task 6's rows (ORPH-2). |
| P-STATE-12, P-STATE-13 | "Run state" | Two requirements: the view an agent receives, and the record kept (CONT-12). |
| P-EVAL-1 | "Task 6's" | The engine records what all three readings of success need: a `Good` idea, the gain under the rule, and the ablation's exit verdict (CONT-19). |
| P-EVAL-7, P-EVAL-8 | "Reviewers" | The PEER assessor, the separate-judge rule, and MISS-8. Per-round review records (MISS-5). |
| P-EVAL-13 | "Figure 9a" | Leave the figure out, but map the capability: the gain logged at named checkpoints (U-EVAL-8, task 6). |
| P-BENCH-2, P-BENCH-4 | "The benchmark" | The task manifest with MISS-21; the task record (U-EVO-4, whose alias is U-BENCH-3). |
| P-COST-1 … 4 | "Cost" | Ledger fields: tokens and machine cost by stage (with A-COST-1's mapping onto §3's stages), failed runs included, wall-clock and busy time. Every number is a reference, not a target. |
| P-ROSTER-49 | "Antigravity" | MISS-15's swap requirement, not the named product (A-CFG-2). |
| P-ROSTER-45, P-DRAFT-1 | "PaperOrchestra" | A drafting backend behind an interface (task 4: a trial). It receives only verified results. |
| P-ART-1 … 9 | "Outputs look like the appendix" | The schema floors of artifacts.md §5, plus negative golden cases: p. 41 is not a clean breakdown; p. 47's auditor must fail; TABHARMONY's 4/24/2 must not become a claim of a classification gain. P-ART-9 is a defective artifact, not a target. |

## Part 5. Coverage risks: groups likely to be mapped lazily

| Group | The lazy mapping | What a real requirement must say | Test shape |
|---|---|---|---|
| P-ROSTER-29 … 44 (16 names) | One "canonical names" requirement | 11 of the 16 carry a decision owned elsewhere, and must map to that decision's requirement: 31 (A-BASE-1), 32 (U-BASE-1), 33 (A-CFG-1, U-ABL-2), 34 (U-ABL-2), 35, 39 and 41 (A-CFG-1: the planners' backends, and which coders run on Claude Code), 37 (A-INT-2), 42 (A-FULL-2), 43 (A-INT-3), 44 (A-ART-1). Five are names only: 29, 30, 36, 38 and 40. | The routing file resolves each group to its agents and their backends. A record that uses an alias fails validation. |
| P-ROSTER-1 … 28 (agents) | "An agent runtime runs them" | For each agent: its inputs and their bound, its output schema floor, its model route, its vocabulary with a malformed-output branch, and a golden-set test. The 12 judges also need fail-closed parsing and read-only access: 2, 4, 8, 11, 15, 18, 19, 21, 25, 26, 27 and 28. | Per agent, a schema and route check. Per judge, a malformed verdict never maps to accept. |
| P-ROSTER-45 … 51 (external systems) | "Interfaces exist" | Each has an interface, a mock and a pinned version. Task 4 changed the status of 46 and 50. 49 maps to the swap requirement. 51 is pending A-INT-1. | Swap and mock tests (MISS-11, MISS-15). |
| P-CFG-1 … 19 (values) | "Limits are config" | For each value: the number, what it counts (A-TOP-2), its at-limit policy (A-TOP-1), and an owner for the six left unset. Each value-and-mechanism pair maps to one requirement (traceability.md §1.4, item 8). | Call counts on mocks (Part 3 of traceability.md, row 1). |
| P-STATE-1 … 17 | "Run state stores it" | The invariants. P-STATE-1 and P-STATE-5 are read-only. P-STATE-4's record and P-STATE-7 are append-only. P-STATE-9 changes only through the guard. P-STATE-16 is copied, never edited in place. P-STATE-17 is fixed at export. P-STATE-12 and P-STATE-13 get a view and a record (CONT-12). | For each object, a test that a forbidden write fails; for example, C_best's hash is unchanged after an ablation run. |
| P-EVAL-1 … 15 | "Task 6 owns measurement" | Split three ways. (a) The engine must record: 1, 8, 13, and the harness results behind 2 and 3. (b) Task 6's protocol: 2, 3, 4, 5, 6, 7, 9, 10. (c) Leave-outs: 11, 12, 14, 15. | (a) A query test over the run history. |
| P-ART-1 … 11 | "Outputs follow the artifacts" | The schema floors of artifacts.md §5, plus negative cases, with App. D's contradictions (A-ART-7 to A-ART-10) used as consistency-check fixtures. 10 and 11 are leave-out candidates. | Schema validation, and the golden cases. |
| P-INT-1 … 5 | "Task 6's" | Task 2 owns where the hooks go (U-INT-1, U-INT-3). Task 6 owns who checks and what counts (A-INT-1, A-INT-3, U-INT-4). Task 3 owns which writer repairs (A-INT-2). A lazy "task 6" mapping drops task 2's two blocking rows. | The tests for U-INT-1 and U-INT-3 in Part 2. |
| P-TOP-1 … 6 | "The pipeline" | See Part 4.2. The untestable clause of P-TOP-1 must be converted into a test or marked evaluation-only. | Conformance, and a check of the call sequence. |

## Part 6. What the coverage checker must catch

It must read three things: traceability.md's Requirement column, the trace lists in requirements.md, and the register's 33 task 2 rows. Its `--selftest` should follow `trace_coverage.py`'s pattern: a clean twin yields 0 problems, and each planted twin yields exactly its own kind.

| Kind | What it catches | The defect to plant |
|---|---|---|
| CHK-1 placeholder | A cell still reads `— (task 2)`, "TBD", "TODO", "?" or nothing. | One of each, in a Requirement cell and in a test cell. |
| CHK-2 unknown requirement | Traceability names a requirement ID that is not defined. | R-999 |
| CHK-3 one-way link, forward | P-X maps to R-1, but R-1's trace list omits P-X. | Delete P-X from R-1's list. |
| CHK-4 one-way link, backward | R-1 lists P-X, but P-X's row names R-2 or a leave-out. | Change the row. |
| CHK-5 double status | P-X is both mapped and left out. | Both, on one row. |
| CHK-6 bare leave-out | A leave-out with no reason, no decider or no date. | Plant each of the three. |
| CHK-7 test count | A requirement has zero acceptance tests, a placeholder test, or two tests. | All three cases. |
| CHK-8 orphan requirement | A requirement traces to no P- ID and is not marked as ours. | Plant one. |
| CHK-9 own requirement without a source | Marked as ours, but with no source (a CLAUDE.md section, a TODO task, a register row, or a dated statement) or no reason. | Plant each. |
| CHK-10 dangling P- ID | A typo, such as P-ABL-8, or a range that runs past the last ID (P-ABL-1 … 9). | Plant both. |
| CHK-11 register row unaddressed | One of the 33 task 2 rows has no status: confirmed, replaced, or deferred with an owner. | Delete one. |
| CHK-12 boundary breach | A row owned by task 3, 5 or 6 is given a "decided" status instead of a "per task N" reference. | U-INT-4, marked decided. |
| CHK-13 pending marker | A dependency names a row that does not exist, or a row that another task owns. The checker also prints every pending dependency, grouped by owning task. | Cite U-INT-9, or "per task 5 (U-INT-4)". |
| CHK-14 duplicate requirement ID | One requirement ID is defined twice. | Plant it. |
| CHK-15 split pair | A value and its mechanism map to different requirements, for example P-CFG-1 and P-LIM-4. | Split one pair. |
| CHK-16 stage field missing | A stage requirement lacks one of the primitive's fields: generator, judged and refined objects, assessor and rule, verdict map, guard with its failure branch, limit with what it counts, at-limit policy, nesting and fan-out. | Delete one stage's at-limit field. |
| CHK-17 malformed ID | An en dash (P–ABL–1), zero padding (P-ABL-01) or lower case is reported, never skipped. | Plant each. |
| CHK-18 fenced text | IDs inside code fences or comments do not count. | A fenced "P-ABL-1 → R-1", with the real mapping deleted, must still yield "missing". |
| CHK-19 masked count | The totals match but the IDs do not: one ID mapped twice and another missing. | Swap two. |
| CHK-20 structure | requirements.md is missing, renamed, or holds no requirement table. Parsing zero requirements is an error, never "0 problems". | Rename the heading. |
| CHK-21 second home | A requirement ID scheme defined outside the chosen home, such as RJ-n. It is read or flagged, as Q-7 decides. | An RJ table. |
| CHK-22 invalid paper location | A location tag in requirements.md that does not exist. `check_citations.py` checks only `docs/paper/` by default, but it accepts files by name. | [§9.9] |

**Proof that it ran.**
- The checker prints, per key: defined, mapped, replaced, left out and pending.
- It prints the number of requirements parsed, the number of task 2 rows addressed (33), and the pending dependencies grouped by task.
- It exits 1 on any problem.

## Part 7. Orphans: design with no requirement behind it

| ID | Element | Why it is an orphan | What to do |
|---|---|---|---|
| ORPH-1 | RJ-1 to RJ-7, and `scientist_two/run_journal/` (`codex/run-journal`, untracked, 2026-10-02) | They trace to CLAUDE.md's rules, but to no task 2 requirement. They decide task 3's U-CFG-2 ("one external operation", a hierarchical work key), and RJ-4 adds a stop that waits for a human (CONT-14). Its own text says it is "pending reconciliation with TODO tasks 2, 3 and 6". | Q-7. RJ-2, RJ-3 and RJ-5 are good acceptance tests for MISS-4 and MISS-7, and could be adopted as such. |
| ORPH-2 | P-STATE-2's component cell: "read-only and hash-checked by the setup" | It pre-decides U-INT-4 and A-INT-1, two of task 6's blocking rows. | Mark it as pending task 6. |
| ORPH-3 | Register U-ART-11: re-score a refined idea for novelty | No decision reads the score: a paid call with no consumer. | Say that it is a record only, or name the decision it feeds. |
| ORPH-4 | Register A-ART-5: the engineers may only tune | A restriction with no detector and no branch. It also narrows §3.2. | Define the detector and the branch, or drop the rule. |

## Part 8. Questions only a human can answer

Each question has an answer that can be decided.

1. **Q-1.** After the single test scoring, what does P+ report? Choose one:
   - (a) test numbers, inserted after the review loop by a deterministic table regeneration, with the reviewed version kept beside it;
   - (b) validation numbers, with the test numbers in a separate harness report;
   - (c) something else.

   And when a test number contradicts a claim, does the engine correct the claim, mark the export, or not export at all?
2. **Q-2.** In a chain of runs, may a child run's agents see the parent run's test numbers? Yes or no.
3. **Q-3.** May the harness score the baseline on the test split before the search, if agents see only pass or fail? Yes or no. If no, what does U-BASE-2's tolerance compare against?
4. **Q-4.** Which reviewer replaces ScholarPeer? Choose one:
   - (a) a re-implementation from its paper;
   - (b) another reviewer behind the contract;
   - (c) a licensed reviewer.

   And which task owns the threshold's calibration rule: 2, 4 or 6?
5. **Q-5.** May a crash re-spend paid work inside a stage? Yes keeps CLAUDE.md's wording. No means amend it to resume at the level of each paid operation.
6. **Q-6.** Who owns the per-task gate values (margin, near-tie band, tolerance, aggregation): task 5 or task 6?
7. **Q-7.** For RJ-1 to RJ-7 and their code, choose one:
   - (a) absorb them into `docs/requirements.md`;
   - (b) keep them as a prototype until task 3 decides U-CFG-2;
   - (c) discard them.

   And is `docs/requirements.md` the single home for requirements? Yes or no.
8. **Q-8.** When the per-task budget runs out, choose one:
   - (a) stop and record, with no export;
   - (b) export the best outputs, marked as a budget stop;
   - (c) pause for a human.
9. **Q-9.** Which human steps are allowed between launch and export? Answer yes or no for each: none at all; raising the budget; resolving an in-doubt cost; reviewing a baseline that failed to reproduce.
10. **Q-10.** Does "reproducible" mean (a) replay reproduces every decision, (b) re-executing C+ reproduces every number within tolerance, or (c) both?
11. **Q-11.** On an ablation `Reject`, does the task end, or fall back to the next `Good` idea?
12. **Q-12.** The limitation loop's 16: verifier calls, or judged expansions?
13. **Q-13.** When an agent's full input exceeds its context, does the call fail, or does a bound apply? If a bound, who sets the default?
14. **Q-14.** Is matching any number the paper reports part of the goal: 80.4% success, 25.2% gain, or the acceptance rates? Yes or no.
15. **Q-15.** Confirm each leave-out in Part 4.1, yes or no: P-EVAL-11, P-EVAL-12, P-EVAL-14, P-EVAL-15, P-CFG-17, P-ROSTER-50, P-ART-10, P-ART-11, P-BENCH-1, P-BENCH-3.
16. **Q-16.** Where does task 2 file a gap it discovers? Choose one:
   - (a) in `docs/paper/`, through paper-analyst;
   - (b) in `docs/requirements.md`, with the checkers extended to read it.
17. **Q-17.** Should novelty retrieval exclude papers published after G? Yes or no.
