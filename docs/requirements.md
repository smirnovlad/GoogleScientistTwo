# Requirements: the ScientistTwo research engine

Written 2026-10-02 for TODO task 2 [ours].

**For** task 3, which designs the components that meet these requirements, and for tasks 4 to 8.
**Holds** the goal, every requirement with its acceptance test, the decisions on the 33 rows of the
decision register that task 2 owns, and the paper elements left out, each with its reason [ours].
The paper is arXiv:2609.19644v1; everything said about it rests on `docs/paper/`, whose conventions
this file follows [ours].

## Goal

**Goal.** From one task, an accepted paper with its code, the engine runs ScientistTwo's research pipeline unattended and returns an improved paper and codebase, or a recorded failure, every reported number computed by a locked harness, every run bounded in cost, resumable and reproducible [§3] [§3, Eq. 1] [ours].

## How to read

- **IDs.** A requirement is `R-<AREA>-n`, defined by its heading; a decision to leave a paper element out is `X-n`. The areas, in reading order, are RUN (the run as a whole), PRIM (the stage primitive), STG (the stages), AGT (agents and outside systems), STATE (run state), INT (integrity), MEAS (measurement) and OPS (operation) [ours].
- **Fields.** Each requirement has the same fields, in this order [ours]:
  - *Requirement*: what must hold, in one or a few sentences [ours];
  - *Traces*: the paper elements (P- IDs of `docs/paper/traceability.md`) it meets, each with its location, or `none` [ours];
  - *Why ours*: the reason for every part the paper does not say, required when *Traces* is `none` [ours];
  - *Decides*: the rows of the decision register (`docs/paper/unspecified.md`) whose decision it carries, all owned by task 2 [ours];
  - *Depends on*: rows owned by tasks 3 to 7 that it rests on, pending there [ours];
  - *Test*: one acceptance test, whose cases a reader can run by hand or as code [ours].
- **Paper or ours.** A location tag means the paper says it; `[ours]` marks our decision or reading, and a requirement that departs from the paper says so under *Why ours*. `python3 playground/paper/check_citations.py` holds these files to `docs/paper/`'s citation rules [ours].
- **Tests.** Most tests run in mock mode (R-OPS-1): scripted mock agents, a mock harness that returns fixture results, and counters on every call. A test names its scripted inputs and what it observes, usually a count of calls, a verdict or a record [ours].
- **Values.** A value the paper sets is a default in the configuration; a value another task owns is named, never guessed, and the configuration refuses to load without it (R-STG-13) [App. A.2] [ours].
- **What this does not decide.** Components, contracts and storage are task 3's; the four blocking integrity rows are task 6's; values and budgets are task 5's; the test strategy is task 7's. Each requirement names the rows it waits on [ours].

## Controls

- **Coverage.** `python3 playground/paper/requirement_coverage.py` checks that every one of the 177 paper elements is traced by a requirement or left out by an X- decision; that each requirement has its fields, a test, and either a trace or a reason; that `traceability.md`'s requirement column matches the requirements; that each of task 2's 33 register rows is decided here, in the table below, in the requirements that carry it, and in its register row; and that no requirement decides a row another task owns [ours].
- **It can fail.** `--selftest` plants each defect beside a clean twin, and `--write` fills `traceability.md`'s requirement column from the requirements, so that the column is never edited by hand [ours].
- **Citations.** `python3 playground/paper/check_citations.py` checks this file and `docs/requirements/` with the folder `docs/paper/`: every statement cites the paper or says `[ours]`, every location exists, and every quote is the paper's [ours].

## The requirements, by area

| Area | File | What it requires | Paper elements |
|---|---|---|---|
| RUN | [01-run.md](requirements/01-run.md) | one task in, one paper and codebase out; the task manifest; chained runs; the stage order; one outcome record per task [§3] [ours] | TOP, BENCH-2, BENCH-4, STATE-1, STATE-2, STATE-17 [ours] |
| PRIM | [02-primitive.md](requirements/02-primitive.md) | one primitive for every stage, with its parameters: counting, at-limit policy, guard, assessors, nesting, records [Lst. 1] [Tab. 1] [ours] | TOP-2, TOP-3, and the loop mechanics of each stage [ours] |
| STG | [03-stages.md](requirements/03-stages.md) | the default configuration of the eleven stages as data, and each stage's own requirement and test [Tab. 1] [App. A.2] [ours] | LIM, SEED, BASE, SUB, FULL, CODER, EVO, SEL, ABL, DRAFT, PEER, META, CFG-1 … 16, CFG-18 [ours] |
| AGT | [04-agents.md](requirements/04-agents.md) | the roster as data, model routing, names and aliases, the coding backend, reviewer, search and drafting interfaces, output records, judges' test cases [§3] [App. A.2] [ours] | ROSTER, CFG-17, CFG-19, ART-1 … 8 [ours] |
| STATE | [05-state.md](requirements/05-state.md) | read-only inputs, append-only records, the guarded core state, code snapshots, the fixed export, resume, the run layout [§3] [ours] | STATE, ART-11 [ours] |
| INT | [06-integrity.md](requirements/06-integrity.md) | the locked harness, read-only evaluation, validation-only search, the specification filter, reference and alignment checks, the post-hoc audit, verified results for writers, read-only judges [§4.2] [ours] | INT, ROSTER-26 … 28, EVAL-10 [ours] |
| MEAS | [07-measurement.md](requirements/07-measurement.md) | success under three readings, computed gains, per-reviewer definitions, a held-out reporting judge, per-round records, seeds, the cost ledger, task selection [§4] [ours] | EVAL, BENCH-1, BENCH-3, COST [ours] |
| OPS | [08-operation.md](requirements/08-operation.md) | mock mode, behaviour as data, interfaces with mocks, budgets, logs, reproducibility, retries, sandboxes, recorded cuts [ours] | ART-8, and CLAUDE.md's rules [ours] |

## Decisions on the register's task-2 rows

`docs/paper/unspecified.md` proposes a decision for each of its rows, and the owning task confirms or
replaces it [ours]. Each of task 2's 33 rows is decided below [ours]:
- *confirmed*: the register's proposal, unchanged [ours];
- *refined*: the same decision, made precise, or with a case the proposal left open [ours];
- *replaced*: a different decision [ours].

None is replaced [ours]. Each register row points back here [ours].

| Row | Priority | Status | Decision, as adopted | Reason | Carried by |
|---|---|---|---|---|---|
| A-TOP-1 | blocks 1 | confirmed | One at-limit value per stage: the subset and full set discard as `Bad`; limitations keep the last set; ablation keeps the current best, a second `Refine` with N_abl spent included; peer review keeps the last manuscript; meta-review exports the last pass's outputs, unapproved [ours] | §3.5 keeps the manuscript explicitly and §3.4 and §3.6 imply keeping; keeping the best-scoring manuscript would select on the reviewer the loop optimises against [§3.4] [§3.5] [§3.6] [ours] | R-PRIM-4, R-STG-1, R-STG-9, R-STG-11, R-STG-12 |
| A-TOP-2 | blocks 1 | confirmed | Every default limit counts judged refinements: at most N refinements and N + 1 assessor calls; Listing 1's count of critic calls stays a value that no default uses [ours] | App. A.2's three refinement sentences, Table 5's rounds 0 to 2 and Figure 9's four rounds after the initial one all count refinements; under Listing 1 the last refinement goes unjudged [App. A.2] [Tab. 5] [Lst. 1] [ours] | R-PRIM-3 |
| U-BASE-2 | blocks 1 | refined | The harness checks the baseline, on the subset and the full benchmark, against the manifest's reference numbers within the manifest's tolerance; outside it, the task ends with *baseline not reproduced*; no repair loop [ours] | The paper's numbers are for the full benchmark, so the subset's reference must come from the manifest; a computed check, not an agent's reading, decides; tasks are reproduced when they are packaged, so a failure here is worth stopping on [§3.2] [ours] | R-STG-3 |
| U-FULL-1 | blocks 1 | confirmed | The full-set row takes the subset's verdicts, `Good`, `Engineer` and `Bad`; at the limit, `Bad`; a full-set `Bad` enters the traces [ours] | Figure 5 draws the subset's loop again at full scale, with *Good or Bad* as output [Fig. 5] (image) [ours] | R-STG-5 |
| A-ABL-2 | blocks 1 | confirmed | After a refinement the guard rejects, drafting follows with the unchanged h_best [ours] | Figure 7 draws that edge; TeCh's end was the critic's rejection, which `Reject` now carries (A-ABL-1) [Fig. 7] (image) [App. B] [ours] | R-STG-9 |
| A-ABL-3 | blocks 1 | refined | The guard applies the task's comparison rule (primary metric, datasets, direction, aggregation, margin) to the harness's validation results; a tie keeps the old result; the Result Comparison Agent's reading is recorded and never decides [ours] | §3.4's strict outperformance read as a numeric test, as CLAUDE.md's deterministic gains require; the margin keeps noise from passing as improvement [§3.4] [§3.6] [ours] | R-PRIM-6 |
| U-EVO-1 | blocks 1 | confirmed | The S test runs at the end of each round [ours] | The formula sums whole rounds, and a test after each idea would make the result depend on which idea finished first [§3.3] [ours] | R-STG-7 |
| A-BASE-1 | blocks 5 | confirmed | The baseline runs once per task, before round 0, and A_Coder receives its results and code, an extension of Eq. 2 [ours] | §3.2 runs it first, and Table 1 gives it a row of its own; once per task saves up to 9 sessions a run and gives every idea one reference [§3.2] [Tab. 1] [ours] | R-STG-3, R-STG-6 |
| A-FULL-1 | blocks 5 | confirmed | The baseline stage also reproduces the baseline on the full benchmark, once per task; the full-set critic judges against it; the published numbers stay beside it, for reporting [ours] | Judging against the published number credits an idea with the gap between two machines: 0.41 of 1.99 points in the one trace [p. 41] [p. 42] (image) [ours] | R-STG-3, R-STG-5 |
| A-ABL-1 | blocks 5 | confirmed | A third ablation verdict, `Reject`, for a gain the ablation does not attribute to the idea; it ends the task with *ablation reject*; ⛔ no fall-back to the next `Good` idea [ours] | App. B's TeCh case ended its task; a fall-back adds a loop the paper never describes, on an idea the Selector ranked lower [App. B] [ours] | R-STG-9 |
| U-ABL-2 | blocks 5 | confirmed | A_FullEng's refinement is one call, which the harness scores and the guard judges; no nested full-set loop [ours] | The guard already judges the result, and Figure 3's loop would add up to three sessions per refinement under no stated limit [§3.4] [Fig. 3] (image) [ours] | R-STG-9 |
| A-META-1 | blocks 6 | confirmed | An accepted meta refinement starts a whole downstream pass at ablation planning, the ablation critic included [ours] | Figures 7 and 3 draw the path through the critic, and skipping it would leave the refined idea's ablation unjudged [Fig. 7] [Fig. 3] (image) [ours] | R-RUN-4, R-STG-12 |
| A-META-2 | blocks 6 | confirmed | The Meta-Reviewer is asked again after the restart, and a second `Refine` exports that pass's P_new and C_best, marked unapproved [ours] | §3.6's loop implies a second verdict, and N_meta = 1 forbids a second refinement [§3.6] [App. A.2] [ours] | R-STG-12 |
| U-META-1 | blocks 6 | confirmed | N_abl and N_peer reset for each downstream pass, and the run state keeps a counter per pass [ours] | A pass without budgets of its own could neither refine nor rebut the refined idea [§3.6] [ours] | R-STG-12 |
| U-BASE-1 | blocks 7 | confirmed | The subset and the full benchmark are manifest fields, fixed by us before the run and never by an agent; the harness reports every setting of the full benchmark [ours] | In the one trace, the agent decided what the full set covered [p. 40] (image) [ours] | R-RUN-2 |
| U-INT-1 | blocks 8 | refined | The specification filter runs after every experiment, before any decision reads its result; a discard invalidates the result: the idea is `Bad`, the refinement discarded, an ablation or rebuttal result dropped [ours] | The register's placement, with the order made explicit, so that a rule-breaking number never steers the search [§4.2] [ours] | R-INT-4 |
| U-INT-3 | blocks 8 | confirmed | The reference check and the method–code audit run after every manuscript revision, and before export [ours] | The reviewers then read a repaired draft, and the export is checked [§4.2] [§3.5] [ours] | R-INT-5, R-INT-6 |
| A-TOP-3 | number | confirmed | N_meta = 1 and §3.6's exit stand; every export carries its last meta verdict, and unapproved exports are counted apart [ours] | The paper's own limit, with the conflict made visible in the counts [§3] [§3.6] [ours] | R-STG-12, R-STATE-6 |
| A-SEED-1 | number | confirmed | Novelty ranks the seed pool and never filters it; a threshold stays an optional ablation [ours] | §3.1 sorts the pool and drops nothing [§3.1] [ours] | R-STG-2 |
| U-SEED-3 | number | confirmed | The Idea Generator reads G, the limitations and the scored pool, under a written rule that excludes pure compute or budget scaling [ours] | App. B's account of what the generator does not propose [App. B] [ours] | R-STG-2 |
| U-SUB-1 | number | refined | The Subset Critic's `Good` stands only if the harness's validation gain over E_base exceeds the task's margin; a vetoed `Good` counts as `Engineer` while the budget lasts [ours] | The register's numeric guard, with the vetoed case decided [§3.2] [ours] | R-STG-4 |
| A-FULL-2 | number | confirmed | The full-set engineering limit is 2, as the subset's [ours] | Figure 5 draws the same loop at both levels, and both session bounds of task 1 use this reading [Fig. 5] (image) [ours] | R-STG-5 |
| A-EVO-1 | number | confirmed | Round 0 runs N_0 = 2 seeds, as many candidates as each later round [ours] | App. A.2's two candidates per round [App. A.2] [ours] | R-STG-7 |
| A-EVO-2 | number | confirmed | K = 4 rounds after round 0 [ours] | Figure 9 labels the rounds *Initial* to *Round 4*, and 4 of 49 tasks picked their idea in Round 4 [Fig. 9b] (image) [ours] | R-STG-7 |
| U-EVO-4 | number | refined | Every task ends with one outcome record, from a fixed list of seven, with its stage, reason, last valid core state and cost [ours] | The register's list, with *budget exhausted* and *error after retries* added by our own guards [§3.3] [ours] | R-RUN-5 |
| U-SEL-1 | number | refined | The validation metric ranks the `Good` ideas; the Selector chooses only among those within the task's margin of the best, and records why [ours] | The register's near-ties, defined by the task's margin [§3.3] [ours] | R-STG-8 |
| A-PEER-1 | number | confirmed | N_peer = 2 rebuttal cycles, so up to three reviews [ours] | Table 5's review rounds 0, 1 and 2 [Tab. 5] [ours] | R-STG-11 |
| U-META-2 | number | confirmed | A written rubric for the venue bar; the Meta-Reviewer also reads the verified results table [ours] | A `Refine` then rests on evidence, not on prose alone [§3.6] [ours] | R-STG-12 |
| U-ABL-5 | number | confirmed | A written boundary between `Refine` and `Reject`, with TeCh, p. 46 and LC-FTT as its first test cases [ours] | The three cases the paper gives [App. B] [p. 46] [Tab. 16] [ours] | R-STG-9, R-AGT-9 |
| U-EVO-3 | later | refined | Once the seeds run out, the evolved idea runs alone; the configuration refuses an N_seed below N_0 + K·N_e [ours] | The register's rule, enforced when the configuration loads [§3.3] [ours] | R-STG-2, R-STG-7 |
| U-DRAFT-2 | later | confirmed | A compile-and-format check after every draft and revision; figures made by scripts from result files [ours] | App. D's figure is a raster diagram unlike the method it shows [p. 59] (image) [ours] | R-STG-10 |
| U-ART-11 | later | refined | Evolved ideas, and refinements that replace a component, get a novelty score, which is recorded and decides nothing; a renamed idea keeps its lineage [ours] | The register's re-scoring, kept as a record, since no decision reads novelty after the seed pool [§3.1] [p. 47] [ours] | R-STG-7, R-STG-9 |
| A-ART-5 | later | confirmed | The §3.2 engineers tune and repair code only; replacing a component is A_FullEng's, in §3.4 and §3.6 [ours] | §3.2's trigger is tuning or code adjustment, and artifacts.md attributes the one redesign shown to A_FullEng after an ablation `Refine` [§3.2] [p. 40] (image) [ours] | R-STG-4 |

## Elements left out

Five paper elements become no requirement; the other 172 are traced by at least one [ours].

### X-1 · The human evaluation

- **Leaves out.** P-EVAL-11 [§4.3] [Tab. 10].
- **Why.** Its protocol is not given (U-EVAL-6), and a human study is not part of the engine; task 5 may add one, with a written protocol [ours].

### X-2 · Figure 1a's radar

- **Leaves out.** P-EVAL-12 [Fig. 1a] (image).
- **Why.** No sentence defines the quantity it plots (U-EVAL-7), so there is nothing to reproduce [ours].

### X-3 · Other systems' numbers

- **Leaves out.** P-EVAL-14 [Tab. 2] [Tab. 4] [Tab. 16].
- **Why.** No comparison with other research agents is planned (U-EVAL-9); one added later compares only on shared tasks, metric, hardware and gain rule, by U-EVAL-10's decision [ours].

### X-4 · Table 9's rating

- **Leaves out.** P-EVAL-15 [Tab. 9].
- **Why.** The reviewer behind the rating is unnamed (A-EVAL-8); chained runs themselves are kept, by R-RUN-3 [ours].

### X-5 · The generated-paper pages of Figures 2 and 8

- **Leaves out.** P-ART-10 [Fig. 2] [Fig. 8].
- **Why.** They illustrate output, and the format they show is the ICLR 2025 template that R-STG-10 already requires, from P-ART-9 and P-CFG-18 [ours].

## What the requirements leave to other tasks

Every row below is pending in the task that owns it, and named under *Depends on* by the requirements
that rest on it. The table lists every such row, so that each task sees what waits on it [ours].

| Task | Rows the requirements depend on |
|---|---|
| 3 · components | A-ART-1, A-CFG-1, A-INT-2, A-NOTE-1, A-ROSTER-1, A-SEED-2, A-TOP-4, U-ABL-3, U-ABL-6, U-ART-10, U-ART-14, U-ART-15, U-CFG-1, U-CFG-2, U-CODER-1, U-DRAFT-1, U-EVO-2, U-LIM-1, U-PEER-4, U-SEED-2, U-SEL-2, U-TOP-1, U-TOP-2, U-TOP-3, U-TOP-4 |
| 4 · reuse | U-PEER-3 |
| 5 · scope and budget | A-CFG-2, A-COST-1, U-ABL-1, U-BENCH-2, U-COST-1, U-COST-3, U-PEER-1, U-SEED-1 |
| 6 · integrity | A-ART-7, A-EVAL-1, A-EVAL-3, A-EVAL-4, A-EVAL-5, A-INT-1, A-INT-3, U-ART-12, U-EVAL-1, U-EVAL-3, U-EVAL-4, U-EVAL-5, U-EVAL-8, U-INT-4, U-NOTE-4, U-SUB-2, U-TOP-5 |
| 7 · tests and mocks | U-TOP-6 |

- **Task 6's four blocking rows** are U-INT-4, U-TOP-5, A-INT-1 and A-INT-3 [ours]. CLAUDE.md already settles the first two in principle, and R-INT-1 and R-INT-3 state that principle; the design is task 6's [ours].
- **Task 3 starts from the blocking rows of task 2,** now decided above, in the architect's order of `docs/paper/unspecified.md`: rank 1, the primitive's parameters, is R-PRIM-3 to R-PRIM-6 and the default stage configuration [ours].
