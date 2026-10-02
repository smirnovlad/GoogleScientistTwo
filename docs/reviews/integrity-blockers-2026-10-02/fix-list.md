# Fix list: the four blocking decisions, wave 1 (2026-10-02)

**For** the owner, the `evaluation-integrity-engineer` persona, who applies it to `docs/integrity/`
in one pass; and for the reviewers, whose closure checks follow it.

**Sources.** Three reviews of `docs/integrity/blocking-decisions.md` at `a2e7eb0`, kept verbatim in
this folder: `research-engineer.md` (RE), `system-architect.md` (SA) and `paper-analyst.md` (PA).
CO marks the coordinator's own findings.
- Every finding of every review appears below exactly once. Where two reviews found the same
  defect, the fixes are merged into one entry.
- **Apply** means the reviewer's fix, as written in its review.
- **Apply, changed** gives the change.
- **None is declined.**

**The two reviews that judge the design** (RE, SA) each found a BLOCKER, and they are different
ones. The paper-fidelity review (PA) found none.

## 0. Structure

| ID | Source | Fix | Decision |
|---|---|---|---|
| F-0 | CO, from the size of the fixes | The fixes below add well over 180 lines to a 419-line file. Split by decision: `blocking-decisions.md` becomes the index, and each decision gets a file of its own under `docs/integrity/decisions/`. **The index holds:** how to read, the terms, a one-line map of every rule ID, the cross-cutting rules (identities and attempts, F-3; the tail stage and its pseudocode, F-5; the gates on the primitive, F-5), the brief's questions, what stays open, and the attacks not stopped. **Each decision file holds:** its rules, attacks, controls, roads not taken, its relation to the paper and the register, the rows it constrains, and its costs. Every file stays under 600 lines, and none is half of a pair that must be read together. | Apply. The coordinator updates R1 and R10 in `README.md` to match. |

## 1. Blockers

| ID | Source | Fix | Decision |
|---|---|---|---|
| F-1 | RE B1 | **Training-seed luck survives the held-out split.** The test event must re-fit each frozen row from its code hash, with report seeds disjoint from the search seeds, and only then score the report split once. Where search was carved from fit (IR-19 option 2), re-fit on fit ∪ search. IR-15's baseline uses the same report fit, and I1 re-fits with the report seeds. The null control plants seed-dependent noise in the fitted model. `playground/integrity/reviews/research-engineer/null_control.py` reproduces the numbers: at equal fit and evaluation noise, the winner keeps +1.32 of its +2.65 search gain on report. | Apply. For a post-hoc method on a shared backbone, the report fit of the backbone is the baseline's report fit for the same seed, so the comparison stays paired (with F-2). |
| F-2 | RE B2 | **Weights placed in the code tree carry no provenance.** Add a lineage rule. A fit job reads only the fit role, weights pinned in the manifest, and artifacts of other recorded jobs named by hash. When the code tree is hashed, an array or binary file, or any file over a size bound, that no recorded job produced is refused. A reused checkpoint is shared with the baseline at the same seed. Re-plant the IR-2/IR-3 and IR-23 controls with the weights inside the tree. | Apply, changed: also decide external weights that a rebuttal needs, such as p. 51's second backbone. Either a recorded acquisition job brings them in by source and hash, or the manifest pins them at packaging and anything else is refused. Say which, and why. |
| F-3 | SA B1 | **A crash cannot be told from a second use.** Count released results per identity, not jobs. An attempt that releases no result is re-run under the same identity, a bounded number of times, and every attempt is logged. What agent code produces (an invalid output, a failure, a timeout against the manifest's limit) is a released result and is never re-run. A run resumes from its last finished stage, before or after the freeze. A halt records its class, integrity or infrastructure, with the ⛔ WHY NOT that SA gives. The audit's identity is (bundle hash, configuration hash), and an audit under a new configuration is reported beside the first, never in its place. Add the kill-the-test-event control. | Apply. RE M3's line also holds: a crash, timeout or out-of-memory error that agent code causes is a run failure, not infrastructure. |

## 2. Majors

| ID | Source | Fix | Decision |
|---|---|---|---|
| F-4 | SA M1 (T1, T10) | **What the freeze holds.** *ours* is C_best's row at the freeze, which is the code exported as C+. The freeze lists exactly *ours*, the baseline, every row of the last downstream pass, and the controls registered in advance, all computed from run state and never from the manuscript. For an IR-8 (a) time metric, the baseline is measured again in the test event's job. | Apply. |
| F-5 | SA M2 (T2, T3), PA M2 (on IR-21) | **The gates set the stage primitive without saying how.** Add the table "Gates on the primitive" (a *filters* parameter for G2 and G3; G4 and G5 as a nested primitive). A candidate has one counter: a G2 retry, if task 2 allows one, uses a refinement. Record the tail (freeze, test event, final fill, gates, export) as a stage, with SA's pseudocode, a failure branch for every step, and its new end state, "test event done, not exported", together with how that end state counts. | Apply, changed: G2's default is §4.2's, discard. A retry and the exhaustion values before the freeze are task 2's; IR-21 must not decide them (§3.6's U-INT-1 row). Only the tail's exhaustion value is decided here: the run ends without export, and counts as a failure. |
| F-6 | SA M3 (T5, T12), RE M5, SA B1 (b) | **Per-task events, and the sealed baseline check.** The baseline's fits, its search scoring and the sealed check all run at admission, with records and ledger entries of task scope that runs only refer to. "Once per task" is keyed on the fields that can change the baseline's score. Before the first attempt, the manifest fixes the seed count and the tolerance formula. The check fails only when the baseline is worse than published by more than the tolerance. A task gets at most k attempts across manifest versions, all reported; packaging iterates on search. Include the ⛔ WHY NOT "before round 0" (parallel runs race). | Apply. This changes U-BASE-2's branch: a baseline that fails is never admitted, so no run starts. List that among the rows constrained. |
| F-7 | SA M4 (T7) | **The audit's results land in engine stores.** A harness job writes to the store of the identity that asked for it. The audit's re-runs go to the audit store and its own ledger, and the run's ledger closes at export. Move IR-5's "audit re-run" kind and IR-14's count of it to the audit side. | Apply. |
| F-8 | SA M5 | **One name covers the enforcer and what it enforces.** Split the harness into the scoring runner (engine code, the same for every task) and a task's scoring items (hashed in its manifest). The runner makes IR-6's check, never an item it checks. A change to the runner is a change of engine version, never of manifest. | Apply. |
| F-9 | SA M6 | **A setup control can test the mock instead of the guard.** Mode becomes "scripted agents, production setup, CPU, $0". Add the rule: a control of a setup guard runs against the production sandbox, mounts, identities, stores and runner; a control run against a mock of the component it tests does not count. Replace the toy task's definition with SA's list of fixtures, as requirements on task 7. | Apply. |
| F-10 | RE M3, SA M7, SA B1 (a) | **Repeated runs, and the configuration key.** Before the first reported run, a record fixes the final-test tasks with their manifest hashes, the number of runs per task, the configuration hash (widened to code, prompts, schemas, routing, limits and budgets), the reporting auditor's configuration hash, and the aggregate registered in advance. Aggregate per (manifest hash, configuration hash). No run is restarted, re-seeded or dropped because of any result, search or report. Retries are allowed only for causes on a list written in advance, are bounded, and are all reported; resume follows F-3. Development tasks' report numbers are validation for the engine, and never evidence. Add the control "a run registered after the others' test events is refused". | Apply. |
| F-11 | RE M1, RE's R4 notes | **The null-idea control, and every other stochastic control, must be decidable.** Run the null control through the engine's own loop in mock mode, so m is whatever the loop does. Plant fit noise (F-1), use a fixed seed list and R ≥ 100 replications, and pass within ±3 SE. Record the search optimism as the bias that section 6 measures. Add the second null control, on the false-success rate. Every other stochastic control (IR-3's flag, IR-7's sway, IR-8 (a) and (c), IR-23, IR-31) states its threshold, seeds and sample size before it runs. | Apply. |
| F-12 | RE M2 | **Success at the null is a coin flip.** Success is never the sign of a point estimate. It is a pre-registered one-sided test on the paired report gain, with the baseline's variance counted once per task, so that the false-success rate at the null is at most α. "No detectable gain" is reported apart from failures. | Apply, changed: state this as the constraint on A-EVAL-1 and U-EVAL-1, task 6's `number` rows. Choosing α and the test belongs to task 6's `P1` part. |
| F-13 | RE M4, PA M3 | **I1 checks values, not gains.** I1 re-derives the paired gain from its re-fits. Its tolerance comes from measured re-fit noise and must lie below the reported gain; otherwise the gain is "not verifiable". Each row's audit budget is fixed before the audit. If *ours* or the baseline is not verified, the task is not a success in the primary count. IR-22 reads "as §5 defines them, except I1's scope (IR-23)". IR-23's scope (every reported row) and its re-fit are marked `[ours]`, settling A-ART-3 and U-ART-6 for U-NOTE-4. A headline-only I1 count is reported beside the every-row count, for comparison with Table 7. | Apply. |
| F-14 | RE M6 | **Role construction for each kind of data.** Temporal data: contiguous blocks with a gap of at least T + L, and the overlap checked on target timestamps. Grouped data: split by group. OOD: (3a) validation sources disjoint from the test OOD sets come before (3b) a carve-out, which every gain then discloses. Option (2) uses F-1's re-fit. State the power formula 1/√(1−f) beside the rule. | Apply, changed: an external fact (TALENT, OpenOOD, Time-Series-Library) is either verified from the source's own text (the arXiv source or PDF, or the raw file fetched with `curl`, never a summarising fetch) and cited with its URL and date, or stated as our reasoning without a quote. |
| F-15 | RE M7, SA m9 | **The agent's adaptation C_base is never scored.** C_base is scored as a row and frozen as a control. ours − C_base is shown beside ours − E_base, and a C_base − E_base difference outside the baseline's seed noise is flagged before any idea is scored. | Apply RE's fix. |
| F-16 | RE M8 | **Seeds and variance.** A seed floor for every reported row (task 5 sets it, never 1). One seed list per role, shared by all rows, with gains computed per seed pair. A failed seed invalidates its row. Per-item predictions and raw judge outputs are stored, hashed in the record, and readable only by engine code and the audit. IR-3's flag becomes the statistical test RE gives. | Apply. |
| F-17 | RE M9, RE m5, PA m6, PA m7 | **Costs.** One cost table per decision, with the multipliers RE lists: runs per task, seeds per scoring, re-fits of every reported row at the test event and in I1, the planted corpus with the people who write it, and judge metrics. Each line carries its sample, and "unknown" where it is unknown. Recompute I1's cost from what p. 62 actually says: module training only, and the baseline is frozen. Mark "five fits" as our assumption. Table 15 covers 4 of 5 papers. "$3765" is over the 33 NeurIPS successes [§4.3]. | Apply. |
| F-18 | PA M1 | **A-INT-1's readings are misattributed and quoted in part.** Rewrite both roads not taken against what §4.2 and Appendix B actually claim. Quote Table 15, and say what "both" refers to. Quote §5's sentence on other evaluation forms in full. Record the reconciling reading, and why INCONSISTENT stands. | Apply. |
| F-19 | PA M2, PA M5, PA m9, PA's R6 note | **Departures that are never named.** Give each decision a "Where we depart" list, one bullet per departure with its quote. Decision 3 lists G2's branch, G4's detector, G3, G1, G6, G7, IR-24 and IR-25. Decisions 1 and 2 list IR-7, IR-11 with IR-13, the tail, and the rebuttal's data. Decide whether §4.2's reproducibility prompt (P-INT-1) is kept as guidance or dropped, and say which; no rule may rest on it. Where a gate keeps what §4.2 specifies, cite §4.2, not only `[ours]`. Section 2.6 also lists the audit's report reads after export as a change from the proposal. | Apply. |
| F-20 | PA M4 | **§5's native provenance check.** ScientistOne's §5 defines a native Claim Provenance Rate beside the four checks. Cite it as the precedent for IR-24 (c) and G3, and report it as a fifth, native number beside the four, so that the four stay comparable with Table 7. | Apply, changed: CPR sits in the delegated section, but it is not among the four checks that ScientistTwo's audit "comprises" [§4.2], so call it a precedent from the delegated source, never a specification by reference. |
| F-21 | PA M6 | **p. 44's γ setting.** Task 1 withdrew this reading (F-AR-2). Either drop the line, or move it under the first attack with its verdict: the opportunity existed and was not taken. | Apply. |

## 3. Minors

| ID | Source | Fix | Decision |
|---|---|---|---|
| F-22 | SA m1, SA's R2 gaps (a)–(c) | Give the bundled rules sub-IDs (IR-5.1 and so on), so that each invariant can be cited with one test. G1, G6 and G7 become names of hooks that point to IR-6, IR-14 and IR-17. Each clause about people ("seen its verdicts", "written apart", "no prompt was developed on") either becomes checkable against a record, or is marked as a process rule that is recorded and not enforced. | Apply. |
| F-23 | SA m2 (T8) | The author role excludes the fixer. IR-27 lists each check's own inputs: G2 the code and rules, G5 the manuscript too, G4 the bibliography and the lookup records. | Apply. |
| F-24 | SA m3 (T9, T11) | IR-1 covers "every number about a row's performance". IR-17 covers "no decision of analysis.md section 4.2", so that G4 and G5 can still block export. | Apply. |
| F-25 | SA m4 | Spell out what a change of routing sets off: new corpus items when the author model changes, the checker's routing naming a concrete model, IR-29's family check computed per run from the recorded routing, a definition of "seen its verdicts", and the cost of retiring the reporting auditor. | Apply. |
| F-26 | SA m5, CO | G3 states the invariant: every measured number is bound to a cell and equals it. Insertion by engine code is its mechanism, with a ⛔ WHY NOT against validating evidence tags as ScientistOne's writer does. Figures are covered: plotted values come from records, rendered by engine code. | Apply. |
| F-27 | SA m6 | IR-7's precondition becomes data: a value of the assessor parameter, over harness records (metric, settings, margin, seeds). | Apply, changed: what a three-verdict critic does when the precondition fails is a proposal to task 2's U-SUB-1, and is not decided here. |
| F-28 | SA m7 | IR-5's "aggregates only" and IR-11's "no search inputs" are cuts of what a model reads. Each says, on the same line, who chose it (task 6) and what it loses (per-item error analysis on search, which stays available on fit's own validation part). | Apply. |
| F-29 | SA m8 | Define the reporter, the reported table and the run registry in the terms, with who reads and writes each. | Apply. |
| F-30 | SA m10 | A defect found in a locked scoring item after a test event: a correction event re-scores the frozen identities. It is reported beside the original values, never in their place, with its cause, and with a control that shows the defect. | Apply, under F-46. |
| F-31 | RE m1 | Near-duplicates: plant one in IR-10's control, and state the detector and its threshold. | Apply. |
| F-32 | RE m2 | The harness reads no parameter from the code tree. Plant T-SAE's case as a configuration value. | Apply. |
| F-33 | RE m3 | Timing: the manifest records the machine's configuration, and the repeat count comes from a measured noise floor. | Apply. |
| F-34 | RE m4 | IR-31 uses Wilson or Clopper–Pearson intervals. The corpus is sized from the precision each reported count needs, and the control states an upper bound with the number of misses that bound needs. | Apply. |
| F-35 | RE m6, SA M2, PA (outside its lens) | **Add the rows constrained but missing:** U-PEER-2 (keep the rebuttal code); A-TOP-4 (a chained run's baseline); U-TOP-2 (resume, F-3); U-COST-1 (the new cost lines); A-BASE-1 (E_base once per task, IR-4; whether A_Coder re-runs C_base per idea stays task 2's); A-NOTE-1 (the *filters* parameter and the tail's row); A-TOP-2 (it sets IR-13's cap). | Apply. |
| F-36 | RE m7 | A short screen of App. B's five ICLR tasks against the rules, so that task 5 sees which are admissible, and at what cost. | Apply, keeping it short. |
| F-37 | RE m8 | A record from a build with a guard removed is never reportable. The run registry carries the engine commit and the guard configuration. | Apply. |
| F-38 | PA m1 | The cherry-picking writer was Sakana's, found by ScientistOne's audit; it was not ScientistOne's own. | Apply. |
| F-39 | PA m2 | ScientistOne's reviewers corrected the automated verdicts, so IR-25 keeps a person's review "unlike ScientistOne", a departure from its practice. | Apply. |
| F-40 | PA m3 | Mark as `[inferred]` "the checker runs on the coding backend, as §4.2 reads", and add App. A.2's routing as a second ambiguity in section 4.6 (A-CFG-1). Mark the critic's steering `[inferred]`, and CIFAR-100-LT as external. | Apply. |
| F-41 | PA m4 | Replace "No task input provides an evaluator" with the register's wording. | Apply. |
| F-42 | PA m5 | p. 47: the page also says that the ablation table, whose first row is the baseline, "all match". The re-run did re-fit the method on the shared backbone. | Apply. |
| F-43 | PA m8 | Quote evidence in full, not by halves: p. 41's near-OOD justification, p. 42's two gains, and what p. 47's "test features" shows. | Apply. |
| F-44 | PA m10 | Add the two items next to the gap in section 2.6: p. 49's leakage check, and p. 69's subset test split. | Apply. |
| F-45 | CO | IR-4's "by a person": say what it guards. The packaging diff is fixed outside any engine run, and a person signs it off; whether an assistant helps write it is not the rule's concern. | Apply. |
| F-46 | CO, RE M5, PA (outside its lens) | **`CLAUDE.md` says "The test set is used once, at the end."** Three reads of report go beyond that wording: IR-15's sealed baseline check, the audit's re-fits after export (IR-23), and F-30's correction event. None of the three can reach a decision that changes the method or the frozen rows. The document states the three as proposed exceptions awaiting Vlad's confirmation. It never edits `CLAUDE.md`. | Apply. The coordinator puts the question to Vlad. |

## 4. Amendments after wave 1 (2026-10-02)

Two facts arrived after this list was written, through a message from the task 2 session. The
coordinator verified each before acting on it, and sent the owner five amendments, A1 to A5.

- **Vlad's goal, recorded verbatim on `origin/claude/engine`'s `DEVELOPMENT_PROCESS.md`:** "As a
  result I expect to see working engine for auto research which replicates engine from paper
  ScientistTwo. I am going to use it based on my claude subscription – "claude -p" backend in
  future, take it into account. I don't wanna pay for API. Don't ask me anything, deliver
  replicated engine."
- **The engine is already being built** on `claude/engine`. It folds in the outputs of tasks 2 and
  6 when they land.

| ID | Changes | Amendment |
|---|---|---|
| A1 | F-46 | Decided in place, not put to Vlad. IR-14's test event is the one use that `CLAUDE.md`'s "used once, at the end" names. The other three reads are not uses in that rule's sense: none can reach a decision that changes the method or the frozen rows, and none releases a number in place of the test event's. `CLAUDE.md`'s narrower wording is flagged to the coordinating session, and this branch does not edit it. |
| A2 | F-17, IR-29, IR-31 | Every agent runs through `claude -p` on the subscription, and nothing may bill the API. The reporting auditor's non-Claude family must therefore run on a subscription too. The candidate is the Codex CLI on the ChatGPT subscription, which task 4 verifies; until then the flag applies. Costs count LLM work as calls and tokens against the usage windows, and any dollar figure is an API-equivalent. |
| A3 | F-3 | When an identity's attempts are exhausted, it is released as failed, or the run is suspended, as the owner of U-TOP-2 decides (task 2 chose to suspend). Either way every attempt is logged and reported, and IR-33.2 and IR-33.4 hold. |
| A4 | F-3, F-32 | A job's identity includes the job arguments that engine code passes to the entry points, such as task 2's mechanism switches. Those arguments reach only the agent's own entry points, never a scoring item. |
| A5 | F-15 | C_base is scored as a row, unless its code hash equals E_base's, in which case E_base's records stand for it. Task 2 keeps C_base as the pinned code, so the equality is the setup check. |
| A6 | A1 | The coordinating session reached the same decision, relayed through task 2, and asked for one clause to be stated: any read of the report split that could feed a decision is a violation. The runner refuses it, the run halts as an integrity failure, and the audit counts it. Its engine contract (`docs/architecture/engine.md` §5 on `origin/claude/engine`) gives the same reading. |

## 5. Outcome of the fix round (2026-10-02)

The owner applied F-0 to F-46 and A1 to A6, and wrote the second version: the index and four
decision files. The citation checker finds 0 problems in the 5 files, and each file is under 600
lines. The owner contested seven points of the list, and the coordinator accepts all seven:

1. **F-24.** Read literally, it would stop G4 and G5 after the test event, since analysis.md
   section 4.2 lists their questions as decisions. IR-17 makes the exception explicit: G3 to G5
   run in the tail, and their fixes edit text only.
2. **F-14.** The T+L gap applies at every boundary that packaging builds. A boundary that the
   protocol itself defines keeps its borders, so the published comparison stays on the same data.
3. **F-17.** §4.3 says "33 target problems"; that they are Table 3's 33 successes is inferred, and
   marked so.
4. **F-5's sketch.** It listed G4 and G5 as filters, against its own table, which makes them a
   nested primitive. The sketch now follows the table.
5. **F-10 against F-3.** A late fresh start is allowed only for a cause on the campaign's list,
   within its bound, and the old run counts as a failure.
6. **A3.** The register gives U-TOP-2 to task 3, not task 2. IR-33.3 defers to "U-TOP-2's owner",
   and task 2's choice to suspend is recorded as its own statement.
7. **The corpus cost.** The review's "970 × 7 × 3" overcounts. The owner counts 11
   check-configurations: about 33,000 calls, or about 100,000 with the false-positive sizing.

## 6. The closure checks, and the last fixes (2026-10-02)

Each wave-1 reviewer checked its own findings against the second version (`adc3484`). The three
reports are kept verbatim as `closure-*.md`.

| Reviewer | Wave-1 findings fixed | New defects |
|---|---|---|
| `system-architect` | all 30, findings and tensions | 5 MINOR (N1–N5) |
| `research-engineer` | 16 of 19; B1 holds; B2 and m3 partly fixed | 1 MAJOR (N1), 3 MINOR (N2–N4) |
| `paper-analyst` | all 16, and the R6 note | 3 MINOR (N1–N3) |

The paper-analyst also read the three external sources from their own text, and found each
paraphrase faithful.

The last fixes, all applied by the owner (SA = system-architect, RE = research-engineer, PA =
paper-analyst):

| ID | Source | Fix |
|---|---|---|
| C-1 | RE B2 residual (MAJOR) | IR-3.3 also bounds the total size of a code tree's content that is neither pinned nor produced by a job, not only each file. The control also plants weights chunked into many small text files. |
| C-2 | RE N1 (MAJOR) | IR-10.3: a near-duplicate across a boundary that packaging built is removed from the role packaging built, and the count is recorded; it never refuses the task. Across a boundary the protocol defines, flagged pairs are reported, with an optional purged report scored beside the full one. The threshold is calibrated against the expected number of false flags over all cross-role pairs, or each flag is confirmed by a stricter second check. |
| C-3 | RE M4 residual | IR-23.4: a paired gain's tolerance carries the re-fit noise of both rows, √2 × σ_r per pair. |
| C-4 | RE N2 | IR-3.6's control: give each honest row its own baseline draw, or set the pass bound from the shared-denominator distribution by simulation. Note the same overdispersion of the flag in production. |
| C-5 | RE N3 | The null control's guard-removed arms pass on "above 3 SE" alone, and the formula's prediction is recorded as a diagnostic. The guarded arm's test, 0 ± 3 SE, stays as it is. |
| C-6 | RE N4 | IR-8.1's repeat count is n = ⌈2(3σ/δ)²⌉, or σ is defined as the SD of the per-repeat difference of interleaved pairs. |
| C-7 | SA N1 | E_base's corrected records are of task scope, released once per (new baseline key, identity), and every run refers to them. A correction's manifest version inherits the task's admission with no new sealed check, and is not counted against k. IR-14.5 names the correction kind as its exception. |
| C-8 | SA N2 | On a change to the runner, E_base is re-scored on search under the new runner, with no read of report. Its admission records are kept only if the two agree within the seed noise; otherwise the task is admitted again. |
| C-9 | SA N3 | The reporter gets an identity of its own: it runs outside every run, and its output never reaches a run. "Engine job" is defined as a job of a run. |
| C-10 | SA N4 | The run ledger closes when the run ends, whatever its end state. |
| C-11 | SA N5 | A listed cause gives a fresh start that is mandatory, exactly once per halted run, so that nobody chooses which runs to restart. |
| C-12 | PA N1 | IR-19.4: OpenOOD pairs (3a) for its OOD validation with (3b) for its ID validation, so IR-19.6's disclosure applies to the ID part. |
| C-13 | PA N2 | Cite ScientistOne's value mismatches as evidence that seed variance biases headline numbers in general. The training-seed claim rests on the null-control simulation. |
| C-14 | PA N3 | The cost is split per stage in Figure 10(b); what the paper lacks is the split between tokens and machines. |
