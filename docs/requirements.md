# Requirements: the ScientistTwo research engine

Written 2026-10-02 for TODO task 2, and revised the same day after its review gate [ours].

**For** task 3, which designs the components that meet these requirements, and for tasks 4 to 8.
**Holds** the goal, every requirement with its acceptance test, the decisions on the 33 rows of the
decision register that task 2 owns, the paper elements left out with their reasons, and the
questions the review raised, decided here [ours]. The paper is arXiv:2609.19644v1; everything said
about it rests on `docs/paper/`, whose conventions this file follows [ours].

## Goal

**Goal.** From one task, an accepted paper with its code, the engine runs ScientistTwo's research pipeline unattended on the Claude subscription and returns an improved paper and codebase, or a recorded failure, every reported number computed by a locked harness, every run bounded in cost, resumable and reproducible [§3] [§3, Eq. 1] [ours].

## How to read

- **IDs.** A requirement is `R-<AREA>-n`, defined by its heading; a decision to leave a paper element out is `X-n`. The areas, in reading order, are RUN (the run as a whole), PRIM (the stage primitive), STG (the stages), AGT (agents and outside systems), STATE (run state), INT (integrity), MEAS (measurement) and OPS (operation) [ours].
- **Fields.** Each requirement has the same fields, in this order [ours]:
  - *Requirement*: what must hold, in one or a few sentences [ours];
  - *Traces*: the paper elements (P- IDs of `docs/paper/traceability.md`) it meets, each with its location, or `none` [ours];
  - *Departs from*: the traced elements whose specified behaviour it changes, and how; `traceability.md` marks each such trace as a departure [ours];
  - *Why ours*: the reason for every part the paper does not say, required when *Traces* is `none` [ours];
  - *Decides*: the rows of the decision register (`docs/paper/unspecified.md`) whose decision it carries, all owned by task 2 [ours];
  - *Depends on*: rows owned by tasks 3 to 7 that it rests on, pending there [ours];
  - *Test*: one acceptance test, whose cases a reader can run by hand or as code [ours].
- **Paper or ours.** A location tag means the paper says it; `[ours]` marks our decision or reading. CLAUDE.md's integrity and engineering rules, which many requirements cite, began as proposals of the initial note (N-81, N-84, N-85, N-87, N-92, N-93, N-95, N-97 and N-98 of `docs/paper/note-check.md`); Vlad committed them on 2026-09-27, so they bind as our decisions, never as the paper's (the elicitation's CONT-16) [ours].
- **Clauses that rest on another task.** A clause that rests on a row another task owns names that row beside it, and lists it under *Depends on*; a clause that states one of task 6's rules cites it by its IR- ID. Task 6's first version, `docs/integrity/blocking-decisions.md` on its own branch, is not yet reviewed, so these clauses are provisional, and the decisions table marks the rows that rest on it [ours].
- **Tests, in two tiers.** Each test says its tier [ours]:
  - *logic* tests mock every outside system, the sandbox and the harness included, and check control flow, counts and records (R-OPS-1) [ours];
  - *enforcement* tests mock only the agents and the paid services, and run the sandbox, the file permissions, the hashing and the harness for real, on the toy task, a CPU task of a few hundred items. Each runs beside a twin with the guard off, in which the planted attack succeeds, so that a green test proves the guard and not only the plumbing (SA-12, EI-1) [ours].
- **Values.** A value the paper sets is a default in the configuration; a value another task owns is named, never guessed, and the configuration refuses to load without it (R-STG-13) [App. A.2] [ours].
- **What this does not decide.** Components, contracts and storage are task 3's; the four blocking integrity rows are task 6's; values and budgets are task 5's; the test strategy is task 7's. Each requirement names the rows it waits on [ours].

## Controls

- **Coverage.** `python3 playground/paper/requirement_coverage.py` checks that every one of the 177 paper elements is traced by a requirement or left out by an X- decision; that each requirement has its fields, a test, and either a trace or a reason; that each departure is from an element it traces; that `traceability.md`'s requirement column matches the requirements; that each of task 2's 33 register rows is decided here, in the table below, in the requirements that carry it, and in its register row; that no requirement decides a row another task owns; that each row under *Depends on* is named in the requirement's text; and that a requirement naming the harness, a data role, a gain or the verified table depends on U-INT-4 or U-TOP-5 [ours].
- **It can fail.** `--selftest` plants each defect beside a clean twin, 40 cases, and `--write` fills `traceability.md`'s requirement column from the requirements, so that the column is never edited by hand [ours].
- **Citations.** `python3 playground/paper/check_citations.py` checks this file and `docs/requirements/` with the folder `docs/paper/`: every statement cites the paper or says `[ours]`, every location exists, and every quote is the paper's [ours].

## The requirements, by area

| Area | File | What it requires | Paper elements |
|---|---|---|---|
| RUN | [01-run.md](requirements/01-run.md) | one task in, one paper and codebase out; the task manifest; chained runs; the run's sequence as data; one outcome record per task; the comparison rule; the tail; no person between launch and export [§3] [ours] | TOP, BENCH-2, BENCH-4, STATE-1, STATE-2, STATE-17, META-2 [ours] |
| PRIM | [02-primitive.md](requirements/02-primitive.md) | one primitive for every stage, with the floor of what it expresses: counting, at-limit values, the guard and its rule, assessors, nesting, records, failing closed [Lst. 1] [Tab. 1] [ours] | TOP-2, TOP-3, and the loop mechanics of each stage [ours] |
| STG | [03-stages.md](requirements/03-stages.md) | the default configuration of the eleven stages and the tail as data, and each stage's own requirement and test [Tab. 1] [App. A.2] [ours] | LIM, SEED, BASE, SUB, FULL, CODER, EVO, SEL, ABL, DRAFT, PEER, META, CFG-1 … 16, CFG-18 [ours] |
| AGT | [04-agents.md](requirements/04-agents.md) | the roster as data, routing by stage and agent on the subscription, names and aliases, the coding backend, reviewer, search and drafting interfaces, output records, acceptance cases [§3] [App. A.2] [ours] | ROSTER, CFG-17, CFG-19, ART-1 … 8 [ours] |
| STATE | [05-state.md](requirements/05-state.md) | read-only inputs, append-only records, the guarded core state, code snapshots, the fixed export, resume, the parts of a run and their writers, the decision trail, the verified table [§3] [ours] | STATE, ART-11 [ours] |
| INT | [06-integrity.md](requirements/06-integrity.md) | the locked harness, unreachable evaluation data, no report-role number in the loop, the specification filter, reference and alignment checks, the post-hoc audit, verified results for writers, read-only judges, hook points [§4.2] [ours] | INT, ROSTER-26 … 28, EVAL-10, and the agents' outputs that become the harness's [ours] |
| MEAS | [07-measurement.md](requirements/07-measurement.md) | success under three readings, computed gains, per-reviewer definitions, a held-out reporting judge, per-round records, seeds, the cost ledger with its billing mode, task selection, a null-idea control [§4] [ours] | EVAL, BENCH-1, BENCH-3, COST [ours] |
| OPS | [08-operation.md](requirements/08-operation.md) | mock mode, behaviour as data, interfaces with mocks, budgets, one record per unit, reproducibility, retries, access per role, recorded cuts, no secrets, shared GPUs, the subscription only [ours] | ART-8, and CLAUDE.md's rules [ours] |

## Decisions on the register's task-2 rows

`docs/paper/unspecified.md` proposes a decision for each of its rows, and the owning task confirms or
replaces it [ours]. Each of task 2's 33 rows is decided below [ours]:
- *confirmed*: the register's proposal, unchanged [ours];
- *refined*: the same decision, made precise, or with a case the proposal left open [ours];
- *replaced*: a different decision [ours].

None is replaced [ours]. The column *Rests on task 6* names the rules of task 6's first version that
a decision adopts; those decisions are provisional until task 6's review closes, and each register
row points back here with the same mark [ours].

| Row | Priority | Status | Rests on task 6 | Decision, as adopted | Reason | Carried by |
|---|---|---|---|---|---|---|
| A-TOP-1 | blocks 1 | confirmed | no | One at-limit value per stage: the subset and full set discard as `Bad`; limitations keep the last set; ablation keeps the current best, a second `Refine` with N_abl spent included; peer review keeps the last manuscript; meta-review sends the last pass's outputs to the tail, unapproved [ours] | §3.5 keeps the manuscript explicitly and §3.4 and §3.6 imply keeping; keeping the best-scoring manuscript would select on the reviewer the loop optimises against [§3.4] [§3.5] [§3.6] [ours] | R-PRIM-4, R-STG-1, R-STG-9, R-STG-11, R-STG-12 |
| A-TOP-2 | blocks 1 | refined | no | Every default limit counts judged refinements: at most N refinements and N + 1 assessor calls; the limitation stage's N is 15, so 16 rounds of extraction; Listing 1's count of critic calls stays a value that no default uses [ours] | App. A.2's three refinement sentences, Table 5's rounds 0 to 2 and Figure 9's four rounds after the initial one count refinements, while App. A.2's 16 limitation rounds include the first [App. A.2] [Tab. 5] [Lst. 1] [ours] | R-PRIM-3 |
| U-BASE-2 | blocks 1 | refined | IR-4, IR-15 | Task 6's sealed check of the pinned code against the published numbers, once per manifest version and before any candidate; one-sided, within the manifest's tolerance; on failure the task ends with *baseline not reproduced*, no agent repairs it, and a person may repackage it as a new version [ours] | The published numbers are test numbers, which task 6 checks sealed; a stronger baseline only makes the loop's gains harder; an agent that repaired the baseline would set its own reference [§3.2] [ours] | R-STG-3 |
| U-FULL-1 | blocks 1 | confirmed | no | The full-set row takes the subset's verdicts, `Good`, `Engineer` and `Bad`; at the limit, `Bad`; a full-set `Bad` enters the traces [ours] | Figure 5 draws the subset's loop again at full scale, with *Good or Bad* as output [Fig. 5] (image) [ours] | R-STG-5 |
| A-ABL-2 | blocks 1 | confirmed | no | After a refinement the guard rejects, drafting follows with the unchanged h_best [ours] | Figure 7 draws that edge; TeCh's end was the critic's rejection, which `Reject` now carries (A-ABL-1) [Fig. 7] (image) [App. B] [ours] | R-STG-9 |
| A-ABL-3 | blocks 1 | refined | IR-5, IR-12 | The guard applies its entry of the task's comparison rule (R-RUN-6), completeness and guardrails included, to the harness's search-role records; a tie keeps the old result; the Result Comparison Agent's reading is recorded and never decides [ours] | §3.4's strict outperformance read as a numeric test, as CLAUDE.md's deterministic gains require; the margin keeps noise from passing as improvement [§3.4] [§3.6] [ours] | R-PRIM-6 |
| U-EVO-1 | blocks 1 | confirmed | no | The S test runs at the end of each round [ours] | The formula sums whole rounds, and a test after each idea would make the result depend on which idea finished first [§3.3] [ours] | R-STG-7 |
| A-BASE-1 | blocks 5 | refined | IR-4 | The baseline runs once per task, before round 0: E_base is the harness's score of the pinned code, C_base the pinned code with the Baseline Coding Agent's notes; A_Coder receives both, an extension of Eq. 2 [ours] | §3.2 runs it first, and Table 1 gives it a row of its own; once per task saves up to 9 sessions a run; a copy the agent could change would pass its changes to every idea [§3.2] [Tab. 1] [ours] | R-STG-3, R-STG-6 |
| A-FULL-1 | blocks 5 | refined | IR-1, IR-4, IR-10 | The full-set critic judges against E_base on every full-set setting of the search role; a published number is never an operand of a verdict, and appears only in reporting [ours] | Judging against the published number credits an idea with the gap between two machines: 0.41 of 1.99 points in the one trace [p. 41] [p. 42] (image) [ours] | R-STG-3, R-STG-5 |
| A-ABL-1 | blocks 5 | refined | no | A third ablation verdict, `Reject`, for a gain the ablation does not attribute to the idea: of the selected idea, it ends the task with *ablation reject*; of a candidate promoted in the same pass, it undoes the promotion; ⛔ no fall-back to the next `Good` idea [ours] | App. B's TeCh case ended its task; a fall-back adds a loop the paper never describes, on an idea the Selector ranked lower; a promotion the critic rejects is a refinement that failed [App. B] [ours] | R-STG-9 |
| U-ABL-2 | blocks 5 | confirmed | no | A_FullEng's refinement is one call, which the harness scores and the guard judges; no nested full-set loop [ours] | The guard already judges the result, and Figure 3's loop would add up to three sessions per refinement under no stated limit [§3.4] [Fig. 3] (image) [ours] | R-STG-9 |
| A-META-1 | blocks 6 | refined | no | An accepted meta refinement starts a whole downstream pass at ablation planning, the ablation critic included; the behaviour is required, and its mechanism is task 3's [ours] | Figures 7 and 3 draw the path through the critic, and the first draft gave the restart three mechanisms (SA-2) [Fig. 7] [Fig. 3] (image) [ours] | R-RUN-4, R-STG-12 |
| A-META-2 | blocks 6 | confirmed | no | The Meta-Reviewer is asked again after the restart, and a second `Refine` sends that pass's P_new and C_best to the tail, marked unapproved [ours] | §3.6's loop implies a second verdict, and N_meta = 1 forbids a second refinement [§3.6] [App. A.2] [ours] | R-STG-12 |
| U-META-1 | blocks 6 | confirmed | no | N_abl and N_peer reset for each downstream pass, and the run state keeps a counter per pass [ours] | A pass without budgets of its own could neither refine nor rebut the refined idea [§3.6] [ours] | R-STG-12 |
| U-BASE-1 | blocks 7 | refined | IR-9, IR-10 | The subset and the full benchmark are fixed in the manifest when the task is packaged, never by an agent: the subset a named part of the search role, the full benchmark every listed setting, all of which the harness scores [ours] | In the one trace, the agent decided what the full set covered [p. 40] (image) [ours] | R-RUN-2 |
| U-INT-1 | blocks 8 | refined | IR-21, IR-27 | The specification filter runs after every code-producing unit, before any decision reads its result: an idea with a discarded result is `Bad`, with no repair; a refinement is discarded; an ablation or rebuttal item is re-run once, then dropped and listed; a failed filter counts as a discard [ours] | A rule-breaking number never steers the search, and a repair would be one more draw against the filter's miss rate [§4.2] [ours] | R-INT-4 |
| U-INT-3 | blocks 8 | refined | IR-21 | The manuscript hooks, compile, number provenance, references and alignment, run after every manuscript revision and after the tail's, with at most 2 repairs per hook and version; at the bound the run ends with *manuscript gate failed* [ours] | The reviewers then read a repaired draft, the export is checked, and no repair loop runs without a limit [§4.2] [§3.5] [ours] | R-INT-5, R-INT-6, R-INT-10 |
| A-TOP-3 | number | confirmed | no | N_meta = 1 and §3.6's exit stand; every export carries its last meta verdict, and unapproved exports are counted apart [ours] | The paper's own limit, with the conflict made visible in the counts [§3] [§3.6] [ours] | R-STG-12, R-STATE-6 |
| A-SEED-1 | number | confirmed | no | Novelty ranks the seed pool and never filters it; a threshold stays an optional ablation [ours] | §3.1 sorts the pool and drops nothing [§3.1] [ours] | R-STG-2 |
| U-SEED-3 | number | confirmed | no | The Idea Generator reads G, the limitations and the scored pool, under a written rule that excludes pure compute or budget scaling [ours] | App. B's account of what the generator does not propose; the rule is a prompt, and R-RUN-6's compute guardrail is the guard [App. B] [ours] | R-STG-2 |
| U-SUB-1 | number | refined | IR-7, IR-13 | The Subset Critic's `Good` stands only if the rule's subset entry passes over the harness's search-role records against E_base; a blocked `Good` counts as `Engineer` while the budget lasts; the idea's code declares its mechanism's switches [ours] | The register's numeric guard, with the blocked case decided, and the switches the ablation's control needs [§3.2] [ours] | R-STG-4 |
| A-FULL-2 | number | confirmed | no | The full-set engineering limit is 2, as the subset's [ours] | Figure 5 draws the same loop at both levels, and both session bounds of task 1 use this reading [Fig. 5] (image) [ours] | R-STG-5 |
| A-EVO-1 | number | confirmed | no | Round 0 runs N_0 = 2 seeds, as many candidates as each later round [ours] | App. A.2's two candidates per round [App. A.2] [ours] | R-STG-7 |
| A-EVO-2 | number | confirmed | no | K = 4 rounds after round 0 [ours] | Figure 9 labels the rounds *Initial* to *Round 4*, and 4 of 49 tasks picked their idea in Round 4 [Fig. 9b] (image) [ours] | R-STG-7 |
| U-EVO-4 | number | refined | IR-6, IR-20, IR-21 | Every task ends with one outcome record, from the union of the stages' declared outcomes and the operational ones, nine in all, with its stage, reason, last valid core state and cost [ours] | The register's list, with *budget exhausted* and *error after retries* from our guards, and *manuscript gate failed* and *integrity halt* from task 6's gates and setup [§3.3] [ours] | R-RUN-5 |
| U-SEL-1 | number | refined | IR-7 | The rule's band entry ranks the `Good` ideas on search-role records; the Selector chooses only among those within the band's margin of the leader and records why, and a choice outside it is overridden [ours] | The register's near-ties, defined by the task's rule [§3.3] [ours] | R-STG-8 |
| A-PEER-1 | number | confirmed | no | N_peer = 2 rebuttal cycles, so up to three reviews [ours] | Table 5's review rounds 0, 1 and 2 [Tab. 5] [ours] | R-STG-11 |
| U-META-2 | number | confirmed | no | A written rubric for the venue bar; the Meta-Reviewer also reads the verified results table [ours] | A `Refine` then rests on evidence, not on prose alone [§3.6] [ours] | R-STG-12 |
| U-ABL-5 | number | refined | IR-7 | A written boundary between `Refine` and `Reject`, with TeCh, p. 46 and LC-FTT as its first test cases, each with a twin addressed to the judge; `Good` stands only if the harness's mechanism-off control loses at least the rule's ablation margin [ours] | The three cases the paper gives; a clean breakdown is a performance gate, which task 6's IR-7 gives a numeric precondition [App. B] [p. 46] [Tab. 16] [ours] | R-STG-9, R-AGT-9 |
| U-EVO-3 | later | refined | no | Once the seeds run out, the evolved idea runs alone; no check at load ties N_seed to the rounds [ours] | The register's rule had two mechanisms, and its load check left the other unreachable (SA-15) [§3.3] [ours] | R-STG-7 |
| U-DRAFT-2 | later | refined | no | The compile check is a manuscript hook, after every draft and revision, with bounded repairs; every result figure is rendered by engine code from the verified table's entries [ours] | App. D's figure is a raster diagram unlike the method it shows, and a figure drawn from a raw result file can show a number the table does not hold [p. 59] (image) [ours] | R-STG-10 |
| U-ART-11 | later | refined | no | Evolved ideas, and refinements that replace a component, get a novelty score, which is recorded and decides nothing; a renamed idea keeps its lineage [ours] | The register's re-scoring, kept as a record, since no decision reads novelty after the seed pool [§3.1] [p. 47] [ours] | R-STG-7, R-STG-9 |
| A-ART-5 | later | refined | no | The §3.2 engineers tune and repair code only, and a step that changes the idea's component list is refused and counted; replacing a component is A_FullEng's, in §3.4 and §3.6 [ours] | §3.2's trigger is tuning or code adjustment, and artifacts.md attributes the one redesign shown to A_FullEng after an ablation `Refine` [§3.2] [p. 40] (image) [ours] | R-STG-4 |

## Decided here, not asked

The review raised ten questions for Vlad. His instruction to the coordinating session, recorded on
2026-10-02, is not to ask him anything, so each is decided here, with its reason; the elicitation's
numbering is kept [ours].

| Question | Decision | Reason | Where |
|---|---|---|---|
| Q-1 · After the single test scoring, what does P+ report? | What task 6's final fill puts there: search and report columns, filled by engine code, after which only text changes (IR-17) [ours] | Task 6 owns the split, and its first version answers it [ours] | R-RUN-7 |
| Q-2 · May a chained run's agents see the parent's test numbers? | No: the conversion of an export into the next G carries no report-role number [ours] | A chain would otherwise search on the data it reports [ours] | R-RUN-3 |
| Q-4 · Which reviewer stands where ScholarPeer is? | Task 4 chooses it (U-PEER-3); the contract and the departure are recorded, and the threshold's calibration is task 6's (A-EVAL-3) [ours] | Which system to reuse is task 4's question [ours] | R-AGT-5 |
| Q-5 · CLAUDE.md resumes from the last finished stage, R-STATE-7 from the last unit of work | R-STATE-7 stands, and CLAUDE.md is left as it is [ours] | A finer grain meets the rule as written [ours] | R-STATE-7 |
| Q-6 · Who owns the comparison rule? | Its gate entries are task 2's, the reported gain's formula task 6's (U-EVAL-1), its values task 5's, set before the task's first run [ours] | Each owner already holds the matching rows [ours] | R-RUN-6 |
| Q-7 · RJ-1 to RJ-7 are a second requirements file, with engine code | `docs/requirements.md` is the one home of requirements; RJ, BA and VT are component contracts, mapped below, and on merge they move beside their components [ours] | Two homes of one requirement drift apart [ours] | the next section |
| Q-8 · What happens when a task's budget runs out? | The run stops with its record and no export, and resumes from it once the budget is raised; a usage window of the subscription pauses it instead [ours] | A run cut short exports nothing half-done, and a pause loses nothing [ours] | R-OPS-4, R-OPS-12 |
| Q-9 · May a person act between launch and export? | No [ours] | The paper's engine runs without one, and a stop that waits for a person makes that untestable [Abstract] [ours] | R-RUN-8 |
| Q-14 · Is matching the paper's numbers part of the goal? | No [ours] | `traceability.md` Part 3 names the fair targets: the mechanics and the planted behaviours [ours] | R-MEAS, its opening |
| Q-17 · Should novelty retrieval exclude papers published after G? | No cut-off; every reference's date is recorded [ours] | A cut-off can be applied later from the dates, and none can be undone [ours] | R-AGT-6 |

## Component contracts written elsewhere

Codex branches hold four component contracts beside engine code, three with IDs of their own, and
none is merged here. They refine requirements of this file; they are not a second set of
requirements. On merge, each moves beside its component, keeping its IDs, and
`requirement_coverage.py` fails on any file of `docs/requirements/` that defines no R- requirement
[ours].

| Contract | Branch | IDs | Refines | Folded into the requirements |
|---|---|---|---|---|
| run journal | `codex/run-journal` | RJ-1 to RJ-7 | R-STATE-7 (RJ-1 to RJ-4, RJ-6), R-MEAS-8 (RJ-5), R-OPS-1 (RJ-7) [ours] | RJ-4's in-doubt state, and RJ-1's key from the unit's place, are R-STATE-7's [ours] |
| budget admission | `codex/budget-admission` | BA-1 to BA-6 | R-OPS-4 (BA-1 to BA-4), R-MEAS-8 and R-OPS-12 (BA-5), R-OPS-1 (BA-6) [ours] | BA-3's reservations are R-OPS-4's, and BA-5's billing mode R-MEAS-8's [ours] |
| verified results tables | `codex/verified-tables` | VT-1 to VT-5 | R-STATE-10, R-INT-8, R-MEAS-2 [ours] | a presenter only; who may write a result is R-STATE-8's [ours] |
| runtime integration | `codex/engine-integration` | none | R-STATE-7 and R-OPS-4 (each CLI attempt an operation), R-OPS-12 (the subscription checked before a result is accepted), R-INT-2 (labels denied to every agent sandbox), R-INT-8 and R-STATE-10 (the drafter's tables) [ours] | its check of the subscription, which fails closed when the signal is missing, is how R-OPS-12 can be met [ours] |

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

Every row below is pending in the task that owns it, and named under *Depends on*, and in the text,
by the requirements that rest on it. The table lists every such row, so that each task sees what
waits on it [ours].

| Task | Rows the requirements depend on |
|---|---|
| 3 · components | A-ART-1, A-CFG-1, A-INT-2, A-NOTE-1, A-ROSTER-1, A-SEED-2, A-TOP-4, U-ABL-3, U-ABL-6, U-ART-10, U-ART-14, U-ART-15, U-CFG-1, U-CFG-2, U-CODER-1, U-DRAFT-1, U-EVO-2, U-LIM-1, U-PEER-4, U-SEED-2, U-SEL-2, U-TOP-1, U-TOP-2, U-TOP-3, U-TOP-4 |
| 4 · reuse | U-PEER-3 |
| 5 · scope and budget | A-CFG-2, A-COST-1, U-ABL-1, U-BENCH-2, U-COST-1, U-COST-3, U-PEER-1, U-SEED-1 |
| 6 · integrity | A-ART-7, A-EVAL-1, A-EVAL-3, A-EVAL-4, A-EVAL-5, A-INT-1, A-INT-3, U-ART-12, U-EVAL-1, U-EVAL-3, U-EVAL-4, U-EVAL-5, U-EVAL-8, U-INT-4, U-NOTE-4, U-SUB-2, U-TOP-5 |
| 7 · tests and mocks | U-TOP-6 |

Some requirement texts presume a register proposal of another task, cut to what can be tested; each
stays open in its task, which may decide it otherwise and then revises the requirement (SA-7) [ours]:

| Row (task) | What the requirements presume | Where |
|---|---|---|
| U-TOP-2 (3) | a budget, a timeout and a retry policy per unit of work, and resume from the last finished unit [ours] | R-OPS-4, R-OPS-7, R-STATE-7 |
| U-CFG-2 (3) | the unit of work sits below a stage, inside A_Coder [ours] | R-STATE-7, R-OPS-5 |
| U-CODER-1 (3) | a pruned idea's trace also keeps its results and its code version [ours] | R-STATE-9 |
| U-ABL-3 (3) | C+ holds the code of every row of the freeze, as task 6 asks [ours] | R-STATE-4 |
| A-TOP-4, U-TOP-1 (3) | G is a paper with its code at a commit, and an export can become G [ours] | R-RUN-2, R-RUN-3 |
| U-ART-15 (3) | access is declared per agent role, and a stage may only narrow it [ours] | R-OPS-8 |
| A-NOTE-1 (3) | the stage table's cells, written in R-PRIM-2's vocabulary, such as the meta stage's nested pass [ours] | 03-stages.md |
| U-INT-4, U-TOP-5, A-INT-1, A-INT-3 (6) | task 6's first version, IR-1 to IR-31, before its review [ours] | every clause that cites an IR- rule |

- **Task 3 starts from the blocking rows of task 2,** decided above, in the architect's order of `docs/paper/unspecified.md`: rank 1, the primitive, is R-PRIM-1 to R-PRIM-10 with the default stage configuration and R-RUN-4's sequence [ours].
- **Task 5 prices more sessions than analysis.md section 9 counts.** Its bound excludes the integrity sessions, while R-INT-4 runs the filter after every code-producing unit and R-INT-10 the manuscript hooks after every revision; the elicitation (CONT-8) and task 6's section 3.7 count them [ours].
- **When task 6's review closes,** every requirement that cites an IR- rule, and every row the decisions table marks, is checked against the reviewed rules [ours].
