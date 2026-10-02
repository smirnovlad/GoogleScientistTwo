# Closure check of the evaluation-integrity review: task 2's requirements at c2ad177

- **Reviewer:** `evaluation-integrity-engineer`, 2026-10-02. This checks the closure of my review of ff1faaa, `evaluation-integrity-engineer.md` (EI-1 to EI-24).
- **What I checked:** `docs/requirements.md` and `docs/requirements/01-run.md` to `08-operation.md` at c2ad177, against the dispositions in `fix-list.md`, section "From the evaluation-integrity-engineer review".
- **What else I read:**
  - Task 6's first version, `docs/integrity/blocking-decisions.md` on `claude/integrity-blockers`. The branch head is 04522df, and the file has not changed since d5d0d61, the version the requirements cite.
  - Task 6's review fix list on the same branch, `docs/reviews/integrity-blockers-2026-10-02/fix-list.md`. It holds F-0 to F-46, and none is declined.
  - The Codex review of c2ad177, `codex-review.md` in this folder (untracked; 4 P1, 6 P2).
  - The paper's TeX: §4's setup, App. B's TeCh case, and Table 5.
  - ScientistOne's §5 and §6.1, from `.cache/refs/2605.26340v1/`.
- **Read-only:**
  - I edited nothing in the repository and ran no git command that changes state.
  - Two scratch copies (task 6's decisions file and the self-test's output) went to the session's temporary directory, outside the repository.
- **Conventions:**
  - Paths are relative to the repository root.
  - `blocking-decisions.md:n` means that file on `claude/integrity-blockers`. `F-n` means an entry of task 6's fix list.
- **Severities** are the first review's:
  - a **blocker** lets a reported number move without a better method while every acceptance test stays green;
  - a **major** is an open attack path, or a guard whose control does not work;
  - a **minor** is a tightening.

## Checks run

- **`python3 playground/paper/requirement_coverage.py`** (2026-10-02, at c2ad177) exits 0.
  - Its summary lines:
    ```
    total           177     172       23         5
    requirements: 82 (RUN 8, PRIM 10, STG 13, AGT 9, STATE 10, INT 10, MEAS 10, OPS 12); leave-out decisions: 5
    task-2 register rows: 33; decided by a requirement: 33; in the decisions table: 15 confirmed, 18 refined
    ```
  - Its last lines:
    ```
      pending, task 6: 17 row(s): A-ART-7, A-EVAL-1, A-EVAL-3, A-EVAL-4, A-EVAL-5, A-INT-1, A-INT-3, U-ART-12, U-EVAL-1, U-EVAL-3, U-EVAL-4, U-EVAL-5, U-EVAL-8, U-INT-4, U-NOTE-4, U-SUB-2, U-TOP-5
      pending, task 7: 1 row(s): U-TOP-6
    0 problem(s)
    ```
- **`python3 playground/paper/requirement_coverage.py --selftest`** exits 0. All 40 cases print `ok`, and none fails. Its last line:
  ```
  ok   --write fills the column: before ['column'], after no problem, identical to the clean file: True
  ```
- **What these two prove through this lens:** only the bookkeeping of the boundary with task 6.
  - No requirement decides another task's row.
  - Every row under *Depends on* is named in the requirement's text.
  - A requirement that names the harness, a role, a gain or the table depends on U-INT-4 or U-TOP-5.
  - They cannot see test tiers, twins, or an IR- citation that lacks its row, because the rule matches words (`playground/paper/requirement_coverage.py:87-88`).
- **My own scan:** I listed every requirement whose *Requirement* field cites an IR- rule or a gate, against its *Depends on*.
  - 31 requirements cite one.
  - 3 of them depend on none of the four blocking rows (NEW-15).
- **Simulations:** run inline with seed 12345. The code is in the appendix, as models A to C.

## 1. The EI findings

Summary: 14 closed, 10 partly closed, none open, none regressed. EI-5's remaining gap now reaches the test split (NEW-5).

| EI | Status | Evidence | What remains |
|---|---|---|---|
| EI-1 · blocker | partly closed | Two test tiers, `docs/requirements.md:28-30`. Enforcement tests with twins at `01-run.md:31`, `03-stages.md:70` and `:150`, `05-state.md:14` and `:78`, `06-integrity.md:21-27`, `:35`, `:43`, `:90-95` and `:103`, and `08-operation.md:72`. The harness sits behind an interface with a mock, `08-operation.md:28` | Twins cover one clause per test, and the network clause passes in a CI that has no network (NEW-10). Two tests cannot produce their stated outcome: R-STATE-1 and R-INT-9 (check 3). The harness's contract tests carry no attack. The checker sees neither tiers nor twins (NEW-15) |
| EI-2 · blocker | closed | Labels and index files are absent from every agent sandbox, `06-integrity.md:31`, with a twin that mounts the labels, `:35`. Agent code runs only in harness jobs, without network, `06-integrity.md:16`. Also `01-run.md:20`, `05-state.md:10`, `08-operation.md:68` | Two leftover attack paths that only detection catches. Task 6 records them, but no requirement names them: (1) public labels fetched over a session's network and carried in the code tree (`blocking-decisions.md:413`; F-2's lineage rule narrows it); (2) transductive use of inputs in a predict step (`:415`). Name both where R-INT-4 relies on detection |
| EI-3 · blocker | partly closed | The invariant, with the timing left to task 6, `06-integrity.md:39`. R-STATE-6 says nothing of timing, `05-state.md:53`. Entries stay search-role until the test event, `06-integrity.md:86`. Every entry carries its split role, `05-state.md:90`. The tail, `01-run.md:93-99` | (a) R-MEAS-1's fixture "an ablation reject with a positive gain, no, yes, no" (`07-measurement.md:20`) needs a report-role gain for a task that never reaches the tail. IR-18 counts such a run as a failure (`blocking-decisions.md:135`). The fixture passes only through an unauthorised report job, or by labelling a search gain as reading (b), which is EI-3's mislabel. Codex found this too (P1). (b) R-INT-3's first sentence is false by design, and its test forbids the sealed baseline check (check 1). (c) No planted draft presents a search number as a test number; NEW-5's binding rule closes this |
| EI-4 · blocker | closed | The harness computes; agent code runs only in harness jobs, with no write path a session can read, `06-integrity.md:16`. Three of EI-4's attacks are planted with twins, `:21-27`. Sessions writing a result, a verdict and a margin are refused, with a twin, `05-state.md:74`, `:78`. Also `08-operation.md:20`, `:68` | Agent code that behaves differently at the test event is stopped by IR-11: every job sees the same paths and environment (`blocking-decisions.md:118`). That rule's control is task 6's, not a requirement's |
| EI-5 · major | partly closed | Measurements are inserted by engine code from a named entry, and the main table is rendered from the method's own entries, `06-integrity.md:86`. Three planted drafts beside a twin that only checks the value, `:90-95`. Result figures are rendered by engine code, `03-stages.md:154` | A number typed in the last hook's repair escapes G3 (R-INT-10; check 1; Codex P1). Attribution in prose is still caught only by detection (`blocking-decisions.md:417`), and after the final fill it reaches the test split (NEW-5) |
| EI-6 · major | closed | Each rebuttal declares its evaluation from registered settings, scored on search; every row is kept; omitted rows go in the export record, `03-stages.md:164-165`. Test at `:172` | None |
| EI-7 · major | partly closed | Switches, `03-stages.md:76`. A control the harness runs, `:127`. The precondition, `:129`. A failed item is re-run once, then listed, `06-integrity.md:50`. The switch audit, `:69`. U-SUB-2 is named, `03-stages.md:136`, `07-measurement.md:24`. Enforcement twin, `03-stages.md:150` | The control is real and no agent writes it. But the precondition: decides nothing exported or reported (NEW-2); re-reads a selected record (NEW-3); is only as honest as a switch its author scopes (NEW-4). Attribution still rests on the critic's `Reject` |
| EI-8 · major | partly closed | The noise floor, `01-run.md:85`. Search scorings per candidate are counted, IR-13 (`blocking-decisions.md:130`). The null idea, and its rate beside every success rate, `07-measurement.md:89`, `:93` | The floor, in my own first-review wording, can be about 0 and does not exist when the configuration loads (NEW-6). The null control is empty as an exact copy, and its test expects one draw (NEW-7) |
| EI-9 · major | partly closed | Guardrails with non-inferiority bounds, and completeness, `01-run.md:82-83`. A fixture twin, `:89` | Completeness names settings, not seeds (NEW-8). Nothing records every metric of the benchmark beside the primary one, so a trade-off on an unlisted metric stays unseen; the fix list points to IR-9, which covers settings only (`blocking-decisions.md:45`). The reference of a bound is unstated: E_base for a veto, E_best for a guard |
| EI-10 · major | partly closed | Compute is a guardrail, read from recorded compute, `01-run.md:82`. The envelope, `01-run.md:24`. The content rule stays a prompt, `03-stages.md:49` | The envelope is named but not enforced: nothing stops a job at it, and no test plants a row beyond it. Which compute is recorded (fit, predict, every attempt) is unstated, and retries escape it (NEW-8) |
| EI-11 · major | partly closed | An LLM can only be stricter than the numbers, `02-primitive.md:28`. Golden-set cases with twins addressed to the judge, and pass rates recorded with every reported run, `04-agents.md:85`. A weakened prompt scores below its twin, `:90` | No pass rate gates a run (U-TOP-6, task 7). Judges with no numeric precondition can still be swayed both ways: the filter, the alignment audit, the reviewer, the Meta-Reviewer. A switch's scope adds one more judged surface (NEW-4) |
| EI-12 · major | partly closed | Every in-loop judge of the manuscript is compared by system, model family and prompt lineage, with a flag and a query log, `07-measurement.md:49`, `:53`. In-loop scores are labelled in-distribution, `:57`. Also `04-agents.md:47` | NEW-9 |
| EI-13 · major | closed | IR-22 to IR-31 are cited, and the audit records which parts follow ScientistOne and which are ours, `06-integrity.md:78`. A post-hoc auditor equal to the in-loop one fails validation, `:82` | R-INT-7's account of what is ours omits IR-23's re-fit (NEW-15). Under R-OPS-12, IR-29's family rule always falls back to its flag (NEW-9) |
| EI-14 · major | closed | Three kinds of report job, `06-integrity.md:39` (IR-14). Runs are registered and aggregated, IR-18 (`blocking-decisions.md:135`). No report-role number enters a chained run, and every link's test event is counted, `01-run.md:35`. Budgets are fixed before the first run, `08-operation.md:36` | The early-report-job clause has no twin (NEW-10). Budget raises, resumptions and chain links can be chosen after seeing results (NEW-12) |
| EI-15 · major | closed | Behaviour files are hashed and frozen before the first reported run on a final-test task, and every reported number names its configuration hash, `08-operation.md:20`, `:24`. Each task is development or final test, and a removed task stays in the report, `07-measurement.md:81` | A leftover gap that task 6 records: the freeze before final-test tasks is recorded, not enforced (`blocking-decisions.md:418`) |
| EI-16 · major | partly closed | The manifest is pinned by a hash registered outside the run, with versions, `01-run.md:17`. Every decision names both hashes, `:85`. Hashes are checked at the start of every job, `06-integrity.md:31`, `05-state.md:10` | R-STATE-1's guard-on clause cannot pass: "a task file edited and restored between two harness jobs makes the second job refuse to run" (`05-state.md:14`). A restored file matches its hash when the next job starts. Run the second job while the file is still changed (Codex P2; I concur). R-INT-2's changed-file clause has no twin of its own (NEW-10) |
| EI-17 · major | closed | E_base comes from the pinned code; the check is sealed and one-sided; no agent repairs the baseline, `03-stages.md:59-62`. Enforcement twin, `:70` | NEW-11. Also F-6 moves the check to admission, so *baseline not reproduced* stops being a run outcome (R-RUN-5) |
| EI-18 · major | closed | The *Rests on task 6* column marks 11 rows, including the six EI-18 named, `docs/requirements.md:65-99`. The integrity-dependency rule, `docs/requirements.md:36`, implemented at `requirement_coverage.py:391-406`, with its self-test case | Three requirements cite an IR- rule without a blocking row, and the checker cannot see it (NEW-15) |
| EI-19 · minor | closed | The rule, `docs/requirements.md:27`, enforced at `requirement_coverage.py:399-401`, with the self-test "a dependency the text does not name". R-INT-7, R-INT-8 and R-STG-3 now cite their rows | R-MEAS-1's "is positive" and R-MEAS-2's two references still state task 6's matter as their own text (check 1; NEW-15) |
| EI-20 · minor | closed | Seeds come from the manifest, and identical results across seeds are flagged, `07-measurement.md:65`. Twin at `:69` | F-16's seed floor ("never 1") will replace "or is marked as resting on one" |
| EI-21 · minor | closed | Each verdict and result names its snapshot's hash, and a mismatch blocks the decision, `06-integrity.md:47`, `:56`. A result is reused on retry, `05-state.md:61`, `:70` | A failure in place of a result is still a fresh draw (NEW-8) |
| EI-22 · minor | closed | `03-stages.md:115`, `:121` | None |
| EI-23 · minor | closed | `06-integrity.md:60`, `:65` | None |
| EI-24 · minor | closed | The gain code is locked and committed before the first reported run. Each number names its record, hash, harness commit and manifest hash, `07-measurement.md:24`. A re-run in a fresh environment, `:29` | None |

## 2. The three checks

### Check 1 · Does a requirement contradict task 6's first version, or decide one of its rows?

**No requirement decides U-INT-4, U-TOP-5, A-INT-1 or A-INT-3.**
- Each clause that states one of task 6's rules cites its IR- or G- ID.
- The four rows sit under *Depends on* in 28 of the 31 requirements that cite task 6.
- The checker's boundary rule finds no decision of another task's row, and my reading agrees.

**Four contradictions with the first version:**

1. **R-INT-10 against G3, G4 and G5.**
   - R-INT-10 says: "A repair does not start the sequence over; only the compile check runs again after the last hook" (`06-integrity.md:111`).
   - Task 6 runs G3 on "every manuscript version, before any reviewer reads it and before export", and G4 and G5 "always after the final fill, before export" (`blocking-decisions.md:234-236`).
   - So a repair made by the last hook, alignment, is a manuscript version that G3 and G4 never see. A typed number or a bad citation it introduces is exported.
   - Codex found this (P1), and I concur. It reopens part of EI-5.
   - Guard: every gate passes on the final version, under one overall repair bound.
   - Control: a scripted alignment repair that types a number is blocked under the guard, and exported as written.
2. **R-INT-3's test against IR-15 and R-STG-3.**
   - The test expects that "a scan of every record, prompt and manuscript version written before the freeze finds no report-role value; a report job requested before the freeze is refused" (`06-integrity.md:43`).
   - But R-STG-3 requires the sealed check, which is a report job before any candidate (`03-stages.md:61`). IR-15 also keeps that check's values as a report-role record until the freeze (`blocking-decisions.md:132`).
   - So a compliant engine fails the test (Codex P1; I concur).
   - Fix: scan only what an agent, a prompt or a manuscript can read; allow exactly the sealed job; and plant an unauthorised report job for a candidate, beside a twin (NEW-10).
3. **R-INT-3's first sentence against IR-1, IR-10 and IR-11.**
   - The sentence: "Every number that an agent, a prompt or a manuscript sees before the freeze comes from the search role" (`06-integrity.md:39`).
   - Task 6's design makes it false. Agent sessions read the fit role and compute on it (`blocking-decisions.md:117-118`). Every agent reads G's published numbers (IR-1, `:37`).
   - The test checks a weaker invariant: no report-role value.
   - Rewrite as:
     - no value computed on the report role reaches an agent, a prompt, a manuscript or a decision before the freeze, beyond the pass or fail that IR-15 releases;
     - every harness value carries its role;
     - every published number is labelled as published.
4. **R-STATE-7 against IR-14, IR-18 and IR-20, at the test event.**
   - R-STATE-7's test kills the run "during a harness job" and expects "the unit in flight at most once more" (`05-state.md:70`).
   - At the test event, that second attempt is a report job beyond IR-14's one per run. The harness refuses it, and IR-20 halts the run as an integrity failure (`blocking-decisions.md:131`, `:227`).
   - IR-18 allows a retry "only for a run that never reached its freeze" (`:135`).
   - Task 6's own review found this conflict (F-3: "A crash cannot be told from a second use"). F-3 resolves it toward R-STATE-7, by counting released results per identity.
   - Until F-3 is applied, R-STATE-7's test either halts at the test event or breaks IR-14.

**Text that decides matter of task 6's other rows instead of citing it:**
- R-MEAS-1's reading (b), "the gain over the human state of the art is positive, under the task's rule" (`07-measurement.md:14`), defines success by a sign.
  - Success is A-EVAL-1's to define.
  - A sign is a coin flip when the method changes nothing; F-12 replaces it with a pre-registered one-sided test.
- R-MEAS-2's "against two references: the published number and the pinned baseline's sealed result (IR-15)" (`07-measurement.md:24`) fixes U-EVAL-1's references.
- R-MEAS-5 restates IR-29's separation rule for the reporting judge.
  - It cites IR-29 only for the flag, and does not depend on A-INT-3.
  - Task 6 already applies IR-29 to U-EVAL-3 (`blocking-decisions.md:371`).

**Not contradictions, but worth recording:**
- R-STG-3 narrows IR-4: C_base is "the pinned code, unchanged" (`03-stages.md:60`), where IR-4 lets the Baseline Coding Agent prepare it (`blocking-decisions.md:40`).
  - A-BASE-1 is task 2's row, so this is allowed.
  - It makes F-15's C_base row trivial.
- R-OPS-12 makes IR-29's flagged fallback the only possible configuration for the reporting auditor (NEW-9).

**Task 6's review will move 14 requirements.** F-0 to F-46 change rules these requirements cite:

| Fix | Requirements it moves |
|---|---|
| F-1 | R-RUN-7; R-INT-3's test; R-STG-3's report fit of the baseline |
| F-3 | R-STATE-7; R-OPS-7; R-RUN-5's halt classes |
| F-5 | R-RUN-5's new end state, "test event done, not exported" |
| F-6 | R-STG-3 and R-RUN-5: the sealed check moves to admission, with at most k attempts |
| F-10 | R-OPS-2; R-RUN-3; R-MEAS-9 |
| F-12 | R-MEAS-1 |
| F-13 | R-INT-7 |
| F-16 | R-RUN-6; R-MEAS-7 |
| F-27 | R-STG-4 |
| F-46 | R-INT-3; R-STG-3 |

The *Rests on task 6* marks (`docs/requirements.md:65-99`) and the re-check rule (`:194`) are the right mechanism for these. Section 4 says which of my findings the fix list already moves.

**Bookkeeping:** R-MEAS-5 (citing IR-29), and R-MEAS-9 and R-OPS-2 (both citing IR-18), depend on none of the four rows. The re-check rule catches them by citation; the checker does not (NEW-15).

### Check 2 · Do the new pieces open a hole?

| New piece | What holds, with its proof | What opens |
|---|---|---|
| Mechanism-off control and switches (R-STG-4, R-STG-9) | The harness fits and scores the control from C_best's switches, and "no agent writes or omits it" (`03-stages.md:127`). Its enforcement twin shows that a weak control written by an agent changes nothing (`:150`). A version with no switch cannot pass the veto (`:76`) | The precondition decides nothing that is exported or reported (NEW-2). It re-reads the record the vetoes selected (NEW-3). Its honesty is the switch's, which the author scopes; only an LLM checks it, after the verdict, and the fix rewrites the method (NEW-4) |
| Sealed baseline check, and C_base as pinned code (R-STG-3) | E_base comes from the pinned code, so a weakened reproduction moves no gain, shown by a twin (`03-stages.md:70`). The check releases only pass or fail. It is one-sided, so a stronger baseline only makes gains harder | The refusal of a changed C_base has no control of its own, and repackaging is unbounded and may re-draw the report split (NEW-11). A report read before the search departs from CLAUDE.md's wording, unflagged (NEW-14). R-INT-3's test forbids the check outright (check 1) |
| The tail (R-RUN-7) | It is one stage of the sequence, and runs for unapproved exports too. Nothing after the test event branches on a result. A request for an experiment is refused (`01-run.md:104`) | The winner's seed luck reaches every reported test gain (NEW-1, a blocker). After the final fill, the writer can bind any frozen row's report cell to the method (NEW-5). A run with a test event but no export has no place in the report (NEW-13). The last repair escapes G3 and G4 (check 1) |
| The null idea (R-MEAS-10) | It runs as configuration, and its rate is printed beside the success rate | As defined, it can be an exact copy that passes nothing. Its test expects one draw per idea. R-RUN-6's floor stops its zero-margin twin from loading (NEW-7; Codex P2) |
| The comparison rule (R-RUN-6) | One rule, read by hash, with an entry per gate. A missing setting or a non-finite value passes no gate, and compute is a guardrail, shown by a fixture twin (`01-run.md:89`) | Completeness names settings, not seeds, and compute misses failed attempts (NEW-8). The floor reads a spread that is about 0 under fixed seeds and does not exist at load (NEW-6). Not every metric is recorded, and a bound's reference is unstated (EI-9) |
| A reporting judge on one model family (R-MEAS-5, R-OPS-12) | A judge equal to an in-loop judge fails validation. Queries are logged. In-loop scores are labelled in-distribution | Under R-OPS-12 the flag is always set, for the reporting auditor too. The judge is not compared with the authors' family, its prompt is not kept from the engine's developers, and nothing measures what the shared family costs (NEW-9) |

### Check 3 · Tests that still prove the plumbing where they claim a guard

| Test | Why it proves less than it claims | See |
|---|---|---|
| R-STG-9: "`Good`, with the control within the margin: counted as `Refine`" (`03-stages.md:144`) | It stops at the relabel. It never asserts that the idea is not exported as an attributed gain | NEW-2 |
| R-INT-3's twin (`06-integrity.md:43`) | "with the guard on the reported gain is zero within its noise" holds only if the noise model has no fit noise | NEW-1 |
| R-MEAS-10 (`07-measurement.md:93`) | Its expected rates assume one scoring per idea. Its null may be an exact copy. Its zero-margin twin cannot load | NEW-7 |
| R-RUN-6: "a margin below k times the fixture spread fails to load" (`01-run.md:89`) | The spread is given, never measured, so the test cannot show that a run's measured spread is about 0 | NEW-6 |
| R-STG-3's enforcement test (`03-stages.md:70`) | Its twin proves IR-4, not the refusal of a changed C_base | NEW-11 |
| R-INT-6: "a switch scripted to turn off a general training control as well is flagged" (`06-integrity.md:74`) | This is the only check of a switch's scope. It uses a mock scripted to flag, at a hook after the verdict | NEW-4 |
| R-OPS-8, R-INT-1, R-INT-2, R-INT-3, R-INT-8, R-RUN-2 | A clause with no twin of its own. The network clause passes in a CI without network | NEW-10 |
| R-STATE-1: "a task file edited and restored between two harness jobs makes the second job refuse to run" (`05-state.md:14`) | This cannot happen with a check at the start of each job, since the restored file matches its hash (Codex P2; I concur) | EI-16 |
| R-INT-9's twin: "with the judge's workspace writable, the planted verdict is counted" (`06-integrity.md:103`) | The requirement's second guard, "a verdict found anywhere else has no standing" (`06-integrity.md:99`), still holds in the twin, so the twin cannot produce its stated outcome. Give each guard its own twin (Codex P2; I concur) | this check |
| R-MEAS-5 (`07-measurement.md:53`) | It checks which configurations load. Nothing measures whether the judge is held out | NEW-9 |
| R-INT-5 and R-INT-6 (`06-integrity.md:65`, `:74`) | Detection by mocks scripted to flag. Unlike R-INT-4, they do not say that the real rate is IR-31's | NEW-15 |

**Tests that do prove their guard, each with its attack and a twin.** Keep these:
- R-INT-1, `06-integrity.md:21-27`;
- R-INT-2's label clause, `:35`;
- R-INT-8's three drafts, `:90-95`;
- R-STATE-8, `05-state.md:78`;
- R-STG-9's enforcement case, `03-stages.md:150`;
- R-RUN-2's dropped setting, `01-run.md:31`;
- R-RUN-6's completeness and guardrails, `01-run.md:89`;
- R-MEAS-7, `07-measurement.md:69`;
- R-STG-8, `03-stages.md:121`;
- R-PRIM-6, `02-primitive.md:85`;
- R-MEAS-2, `07-measurement.md:29`.

## 3. New findings

NEW-6 and NEW-7 are defects in my own first-review wording, which the revision copied faithfully.

| ID | Severity | Finding | Where |
|---|---|---|---|
| NEW-1 | blocker | Seed luck survives the tail, and R-INT-3's twin cannot show it | R-RUN-7, R-INT-3 |
| NEW-2 | major | The ablation precondition decides nothing that is exported or reported | R-STG-9, R-MEAS-1 |
| NEW-3 | major | The ablation precondition re-reads E_best, a record the vetoes selected | R-STG-9 |
| NEW-4 | major | A switch is scoped by its author, checked after the verdict, and repaired by rewriting the method | R-STG-4, R-STG-9, R-INT-6 |
| NEW-5 | major | After the test event, prose can bind any frozen row's report cell to the method | R-RUN-7, R-INT-8 |
| NEW-6 | major | The noise floor can measure nothing, and does not exist when checked | R-RUN-6 |
| NEW-7 | major | The null idea is empty as defined, and its test expects one draw | R-MEAS-10 |
| NEW-8 | major | Agent code can choose which draws count, and take uncounted compute, by failing on purpose | R-OPS-7, R-STATE-7, R-RUN-6 |
| NEW-9 | major | The reporting judge and the reporting auditor run on the authors' model family, and nothing measures the cost | R-MEAS-5, R-OPS-12, R-INT-7 |
| NEW-10 | major | Enforcement twins cover one clause per test; the network clause passes with no guard | How to read; R-OPS-8, R-INT-1, R-INT-2, R-INT-3, R-INT-8, R-RUN-2 |
| NEW-11 | minor | R-STG-3: the refusal of a changed C_base has no control; repackaging is unbounded | R-STG-3 |
| NEW-12 | minor | People can choose which runs finish after seeing their results | R-OPS-4, R-RUN-8, R-RUN-3 |
| NEW-13 | minor | A run with a test event but no export has no place in the report | R-RUN-5, R-MEAS-2, R-MEAS-3 |
| NEW-14 | minor | Three report reads against CLAUDE.md's "used once, at the end", unflagged | R-INT-3, R-STG-3 |
| NEW-15 | minor | Bookkeeping: the checker, the fix list, and four texts | checker; R-INT-5, R-INT-6, R-INT-7, R-MEAS-1, R-MEAS-2, R-MEAS-5, R-MEAS-9, R-OPS-2 |

### Blocker

**NEW-1 · blocker · Seed luck survives the tail, and R-INT-3's twin cannot show it**
- **Where:**
  - R-RUN-7's first step: "the freeze, the one test event and the final fill, as task 6 sets them (IR-14, IR-17; U-TOP-5)" (`01-run.md:94`).
  - IR-14's test event "scores each row of the freeze once" (`blocking-decisions.md:131`). IR-3 scores only the artifact that a recorded fit job produced (`:39`). So the report score belongs to the very artifact that was chosen on search.
  - R-INT-3's twin: "a null-idea search of 20 candidates reports the best one's noise as a gain, while with the guard on the reported gain is zero within its noise" (`06-integrity.md:43`).
- **Attack:** none is needed.
  - Selecting on search picks the candidate whose fitted artifact got lucky, through its training seed, its initialisation or its data order, as well as through noise in the evaluation itself.
  - The report split removes the evaluation luck. The training luck stays in the artifact, and is scored again on report.
- **Evidence:**
  - Task 6's research-engineer review found this as its blocker B1, accepted as F-1: "at equal fit and evaluation noise, the winner keeps +1.32 of its +2.65 search gain on report".
  - Model C reproduces it. With 20 null candidates, and training and evaluation noise of unit sd each, the search gain is 2.64 and the report gain 1.33 (n = 20,000).
  - With evaluation noise only, the report gain is −0.01.
  - The share that survives is the training variance over the total variance.
- **Would we notice:** no.
  - R-INT-3's twin does not say where its noise comes from.
  - Built the way task 6's own control plants it, "20 candidates whose true gain is 0 and whose scores are unit-variance noise" (`blocking-decisions.md:174`), the gain with the guard on is zero and the test is green.
  - Meanwhile every reported test gain carries about half the winner's search luck.
- **Guard:** task 6's F-1.
  - The test event re-trains each frozen row from its code hash, with report seeds disjoint from the search seeds, then scores the report split once.
  - The baseline uses the same report re-training.
  - R-RUN-7 cites F-1 once it is applied, and is marked provisional on it now.
- **Control:** R-INT-3's twin plants seed-dependent training noise in the toy task: a model whose quality depends on its training seed. It states its outcomes before it runs:
  - without the re-training, the report gain with the guard on is about half the search gain;
  - with it, the gain is zero within ±3 SE over a pre-registered number of seeded runs (F-11 asks for at least 100).

### Majors

**NEW-2 · major · The ablation precondition decides nothing that is exported or reported**
- **Where:**
  - R-STG-9: "`Good` stands only if the control was scored and loses to C_best by at least the rule's ablation margin, on the search role (R-RUN-6; U-TOP-5); a `Good` it blocks counts as `Refine`" (`03-stages.md:129`).
  - R-STG-9: "If it rejects, or if a second `Refine` comes once N_abl is spent, drafting follows with the current h_best" (`03-stages.md:132`).
  - The ABL row's value at the limit: "keep the current best, and go on to drafting" (`03-stages.md:30`).
  - R-MEAS-1's reading (c): "the gain survived the ablation, with no `Reject`" (`07-measurement.md:15`).
- **Attack:** none is needed. Take an idea whose mechanism-off control scores as well as C_best, a gain made of general training controls, as in TeCh's case.
  1. A lenient or swayed critic gives it `Good`.
  2. The precondition turns that into `Refine`, and A_FullEng refines once.
  3. The guard rejects the refinement, or a second `Refine` meets the spent N_abl.
  4. Drafting follows with the same h_best, and the paper is exported.
  5. Reading (c) counts it as surviving the ablation, since nobody said `Reject`.

  Only the critic's `Reject` can stop it, which is exactly the state EI-7 described. The subset veto, by contrast, has teeth: a blocked `Good` becomes `Engineer`, and `Bad` at the limit (`03-stages.md:26`).
- **Would we notice:** only by reading the ablation record. R-STG-9's own test stops at the relabel: "`Good`, with the control within the margin: counted as `Refine`" (`03-stages.md:144`).
- **Guard:** this is task 2's to decide (A-ABL-1, U-ABL-5). Either option works:
  - a precondition still unmet when N_abl is spent is treated as `Reject`, in both of its branches: the selected idea ends with *ablation reject*, and a promotion is undone;
  - or, keeping Figure 7's edge to drafting, the export record marks *attribution not shown*, and reading (c) reads the precondition on the exported pass instead of the absence of `Reject`.
- **Control:** a fixture whose control stays within the margin of C_best in both passes, with the critic scripted to `Good`.
  - Under the guard: *ablation reject*, or reading (c) "no" with the mark.
  - Twin, as written: an export, and reading (c) "yes".

**NEW-3 · major · The ablation precondition re-reads E_best, a record the vetoes selected**
- **Where:**
  - R-STG-9 says the control must lose "to C_best" (`03-stages.md:129`).
  - The control is a fresh fit (`03-stages.md:127`).
  - The only result of C_best in the run is E_best, which the selection sets (`05-state.md:28`).
- **Attack:** none is needed.
  - E_best is the record with which the idea passed the full-set veto, after up to three scorings, and then won the selection.
  - So by construction E_best exceeds E_base by at least the veto's margin.
  - For an idea whose mechanism-off code behaves like the baseline, the control scores about E_base. This covers a null mechanism, and a mechanism with no other change.
  - "loses to C_best by at least the margin" then only restates the veto the idea has already passed.
  - By default, R-RUN-6 gives every entry the task's margin (`01-run.md:81`).
- **Evidence (model B):** null ideas that passed the full-set veto, with the ablation margin equal to the veto's. How often the precondition passes (n = 50,000 each):

  | What the control is compared with | Margin 1 sd | Margin 2 sd |
  |---|---|---|
  | E_best, when the control reproduces E_base exactly | 100% | 100% |
  | E_best, when the control is an independent draw | 51.5% | 32.3% |
  | A fresh re-fit of C_best | 24.0% | 7.7% |

  The last row is the single-comparison rate the margin was chosen for.
- **Would we notice:** no. The record shows a control that loses by the margin.
- **Guard:** the harness re-fits C_best and the control in one job, with the same seeds. The precondition reads the paired difference of those two fresh fits, never E_best.
- **Control:** model B's null fixtures, on the toy task.
  - Against E_best, the precondition passes in at least a third of runs, and in all of them when the control reproduces E_base.
  - Against the paired re-fit, it passes at the rate the margin was set for.

**NEW-4 · major · A switch is scoped by its author, checked only after the verdict, and repaired by rewriting the method**
- **Where:**
  - R-STG-4: "The idea's code declares its mechanism as switches in its configuration, which turn the mechanism off and leave every other change in place" (`03-stages.md:76`).
  - R-INT-6 compares "each declared switch with the mechanism the method describes", then "The writer then corrects the manuscript, never the code (IR-28)" (`06-integrity.md:69`).
  - That audit runs at R-INT-5's hook points, "after the draft, after every enhancement and re-draft, and after the tail's revision" (`06-integrity.md:60`).
- **Paper:** TeCh's DMC-TeCh variant "beat the baseline on 5 of 6 metrics, but the ablation critic rejected it". The critic's reason was that "the gains were primarily driven by general training controls (EMA and label smoothing) rather than the multi-core architectural innovation itself" [App. B] (tex:sections/appendix.tex:222-224).
- **Attack:** two forms.
  - *Bundling.* The coder, or later an engineer, puts EMA and label smoothing under the mechanism's switch. An engineer is allowed to, because changing what a switch gates changes no component list (`03-stages.md:77`).
    - Switched off, the generic controls go too, so the control falls to about E_base.
    - The precondition then passes, always (NEW-3).
  - *Sabotage.* The switch's off-path also degrades something else, such as a halved learning rate. The control then loses by more than the mechanism is worth.

  Either way, the only check of a switch's scope is an LLM audit at the first manuscript hook, which comes after the ablation verdict has been read. When that audit flags the switch, the fix edits the text:
  1. the writer adds EMA and label smoothing to the method;
  2. the audit passes;
  3. TeCh's case is exported as an attributed gain.
- **Would we notice:** only if the audit flags it and someone reads past the repaired text. R-INT-6's test, "a switch scripted to turn off a general training control as well is flagged" (`06-integrity.md:74`), uses a mock scripted to flag.
- **Guard:**
  1. Check each switch against the idea's own recorded description, written before its code was scored, not against the manuscript.
     - Run the check at the code hook where a switch is declared or changed, alongside G2, before any veto or critic reads the result.
     - A finding about a switch is a finding about the code, and no text edit repairs it.
  2. A numeric floor: a control that scores below E_base by more than the margin fails the precondition and is flagged. An off-path worse than the baseline turns off more than the mechanism.
  3. When task 6 adds U-SUB-2's tuned baseline (`blocking-decisions.md:93`), the precondition reads it too, since generic tuning is what that control measures.
  4. IR-31's planted corpus includes bundled and sabotaged switches.
- **Control:**
  - A TeCh-shaped toy idea: a mechanism that does nothing, plus a generic training control, under one switch.
    - Under the guard, the scope check blocks the ablation `Good` before any verdict reads it.
    - Twin, as written: `Good` stands, the audit flags at drafting, the scripted writer adds the generic control to the method, the audit passes, and the export counts under reading (c).
  - A sabotage fixture, whose off-path halves the learning rate.
    - Under the guard, the floor blocks it.
    - Twin: the precondition passes.

**NEW-5 · major · After the test event, prose can bind any frozen row's report cell to a claim about the method**
- **Where:**
  - R-RUN-7, after the final fill: "one revision of the text by the writer, with no change to code, rows or roles (IR-17)" (`01-run.md:95`).
  - R-INT-8: "Each number a manuscript presents as a measurement is inserted by engine code from a table entry that the writer names". Also: "A misattribution in the prose around a number stays detection only" (`06-integrity.md:86`).
- **Reference:** ScientistOne's audit found a writer that "selects the most favorable score from ablation-stage nodes rather than the score of the node whose code is used as the final solution". It caused 4 of 7 score-verification failures [Ref: meng2026scientistone §6.1] (ref:2605.26340v1:sections/06b_integrity.tex:45). The writer was Sakana's (task 6's F-38).
- **Attack:**
  - After the final fill, the writer reads the report cells of every frozen row.
  - Its revision may rebind a number in its prose, since rebinding is a change of text.
  - It names the best ablation variant's report cell, or a rebuttal row's, in the abstract, under words about the method.
  - G3 checks only that the number is a cell and equals it, so the draft passes.
  - The main results table is safe, because engine code renders it from the method's own entries. The abstract is not.
- **What changed since the first draft:**
  - In the first draft the writer never saw a test number.
  - EI-5's remaining gap now works on the test split, after its one use.
  - Before the freeze, the same move shows the in-loop reviewer the best ablation's search number as the method's.
- **Would we notice:**
  - In the run, no.
  - After it, possibly: IR-24 (c) compares the provenance links with I1's LLM extraction of the paper's numbers (`blocking-decisions.md:242`). That works only as well as the extraction does.
- **Guard:** an invariant for R-INT-8, whose mechanism is task 6's G3.
  - A number in prose binds only to the row *ours*, or to a reference row: the baseline, or a published number.
  - Every other row's values appear only in tables that engine code renders, with captions written from the rows' roles.
  - Alternatively, every inserted number is rendered with its row's role beside it.
- **Control:** a scripted tail writer binds the abstract's headline to the best ablation row's report cell.
  - Under the invariant: blocked.
  - Twin, with G3 as written: exported.

**NEW-6 · major · R-RUN-6's noise floor can measure nothing, and does not exist when it is checked**
- **Where:** "The configuration refuses a margin below k times the baseline's measured run-to-run spread on the same role" (`01-run.md:85`).
  - The wording is mine, from EI-8: "measured run-to-run spread on the same split" (`evaluation-integrity-engineer.md:343`).
  - So is the defect.
- **Attack:** none is needed. Four problems:
  1. **The spread is the wrong one.**
     - Seeds come from the manifest's list (R-MEAS-7, IR-3).
     - Re-running the baseline with its own seeds reproduces it, up to hardware nondeterminism, so its run-to-run spread is close to 0.
     - That is far below its spread across seeds, which is the noise a gate actually faces.
     - So a margin near 0 loads.
  2. **It is measured on the wrong data.** The spread is taken "on the same role", but the subset veto reads the subset, which is a smaller and noisier part of search.
  3. **It ignores how many scorings a gate gets.**
     - A blocked `Good` becomes `Engineer` (`03-stages.md:26`), and each engineering session ends in a scoring (`03-stages.md:78`).
     - So an idea meets the subset veto up to three times.
  4. **It does not exist at load.**
     - The configuration loads at the start of a run, and the baseline is scored later in it, before round 0 (`03-stages.md:58`).
     - On a task's first run, no measured spread exists when the configuration is supposed to refuse.
- **Evidence (model A):** how often a null idea passes the subset veto (n = 200,000 each):

  | Margin | One scoring | Up to three scorings |
  |---|---|---|
  | 0 sd | 0.498 | 0.749 |
  | 1 sd | 0.239 | 0.447 |
  | 2 sd | 0.079 | 0.177 |
- **Would we notice:** no. R-RUN-6's test gives the spread as a fixture: "a margin below k times the fixture spread fails to load" (`01-run.md:89`).
- **Guard:**
  - The floor reads the baseline's spread across the manifest's search seeds, each a separate fit, on the settings and aggregate that the gate's entry reads.
  - It is measured at admission, with the baseline's search fits (task 6's F-6 puts them there).
  - Each gate's margin loads only if the gate's false-pass rate at the null, given the scorings the loop allows it, is at most a stated α. The value of α is task 6's.
  - A run whose floor cannot be computed does not start.
- **Control:** a toy baseline that is deterministic given its seed: its same-seed spread is 0, and its cross-seed spread is σ.
  - As written, the floor is 0, a margin of 0 loads, and a null idea that re-draws its randomness passes the subset veto in about 0.75 of runs.
  - Under the guard, the margin loads only at its computed level, and the measured rate lies within ±3 SE of α.

**NEW-7 · major · The null idea of R-MEAS-10 is empty as defined, and its test expects one draw**
- **Where:**
  - "a null idea, a change that leaves the method as it is, end to end as configuration, through every gate a real idea passes" (`07-measurement.md:89`).
  - Its test: "it passes at a margin of 0 in about half of them and in almost none at the configured margin" (`07-measurement.md:93`).
  - Those expected rates are my EI-8 control's: "With the margin at 0, about half pass" (`evaluation-integrity-engineer.md:347`).
- **Why the control does not work:**
  1. **An exact copy measures nothing.**
     - A change that leaves the method as it is reproduces the baseline's scores on the shared seed list (IR-3; F-16 makes it one list per role), so its gain is exactly 0.
     - It then passes no positive margin, however small that margin is against the noise. The control reads "almost none" whatever the floor's size.
     - Real candidates differ from the baseline in code, so their draws differ.
  2. **"About half at a margin of 0" is the rate for one scoring.**
     - The loop gives an idea up to three subset and three full-set scorings, and selects over up to ten ideas. Model A gives 0.749 on the subset alone.
     - A test that finds "about half" was built with one draw per idea; on the real loop it fails.
  3. **The zero-margin twin cannot start.** With a positive spread, R-RUN-6 refuses a margin of 0 at load (Codex P2; I concur).
- **Would we notice:** no. A green control would then stand as evidence that the guards stop noise, which it does not show.
- **Guard:**
  - The null idea leaves the expected score unchanged but re-draws its randomness. Examples: a component that does nothing but consume random draws, or a permuted data order.
  - It runs through the real loop on the toy task:
    - the critics are scripted at their most permissive;
    - the engineers make a change that does nothing in each round;
    - it goes on through selection and the ablation.
  - Its expected rate is computed beforehand, from the number of scorings the loop allows.
  - A null whose scores equal the baseline's is refused as a control.
  - The zero-margin twin turns off the floor's validation explicitly.
  - Task 6's F-11 asks the same on its side ("through the engine's own loop", at least 100 replications, ±3 SE), and adds a null control on the false-success rate.
- **Control:**
  - The exact-copy null passes nothing at any positive margin, which shows that it is empty.
  - The re-drawing null, run through the loop, passes the subset veto in about 0.45 of runs at a margin of 1 sd, against 0.24 for one scoring (model A). So the test can see the effect of repeated scorings.

**NEW-8 · major · Agent code can choose which draws count, and take uncounted compute, by failing on purpose**
- **Where:**
  - R-OPS-7: "Each unit of work, harness jobs included (U-INT-4), has a timeout and a retry policy" (`08-operation.md:60`).
  - R-STATE-7 reuses a result only where one exists: "a unit with a harness result reuses that result on any retry" (`05-state.md:61`).
  - R-RUN-6's completeness names settings, not seeds: "completeness: a result that lacks a setting of the rule, or holds an invalid or non-finite value, passes no gate (IR-9)" (`01-run.md:83`).
  - The compute guardrail reads "the compute the harness records with each result" (`01-run.md:82`).
- **Attack:**
  - A fit step may read the fit role, including the validation part the protocol uses for model selection (IR-10).
  - It scores itself there, and exits with an error when the score is poor. It takes its randomness from somewhere other than the seed it was passed.
  - Two ways this pays off:
    - *Per seed:* the row averages over the seeds that survived. Its mean rises and its spread shrinks, against a baseline that kept every seed.
    - *Per job:* R-OPS-7 retries the failed harness job, and each retry is a fresh draw, kept by a criterion correlated with search. Its compute lies outside the result's recorded compute, so the compute guardrail that answers EI-10 never sees it.
- **Would we notice:**
  - The failed attempts are in the ledger: "A failed attempt is costed and recorded" (`08-operation.md:60`).
  - But no gate, spread or guardrail reads them.
  - I1's re-training after export (IR-23) may find the row cannot be reproduced.
- **Guard:**
  - A failure caused by agent code is a released result with its status (IR-5), and is never retried. Such failures are a non-zero exit of its entry point, an invalid output, or hitting its own time or memory limit.
  - Only a failure of the harness itself is retried, under the same identity and seed (F-3).
  - A failed seed invalidates its row, and R-RUN-6's completeness names seeds (F-16).
  - The compute guardrail reads the compute of every attempt of a row.
- **Control:** toy agent code that exits with an error when its own score on the fit role's validation part is below its running median, using internal randomness, plus a variant that fails only its worst seed.
  - Under the guard, the first failure is the row's result, and no gate passes.
  - Twin, with retries and an average over the surviving seeds: the recorded mean exceeds the honest one by about the expected maximum over the attempts. That value is stated before the run.

**NEW-9 · major · The reporting judge and the reporting auditor run on the authors' model family, and nothing measures the cost**
- **Where:**
  - R-OPS-12: "Every LLM call, agents and judges alike, goes through the Claude subscription" (`08-operation.md:99`).
  - R-MEAS-5: the judge "differs from each in model family and prompt lineage where another family is available; on the subscription alone none may be, and the report then carries a flag". Also: "whether an outside service may be used is task 4's" (`07-measurement.md:49`).
  - R-INT-7 keeps the auditor apart by IR-29 (`06-integrity.md:78`; `blocking-decisions.md:315`).
- **Paper:**
  - "Conversely, Stanford Agentic Reviewer serves as a held-out evaluator that was unseen during development by both the baselines and our method" [§4] (tex:sections/4_experiment.tex:5). It is an outside service, footnoted as paperreview.ai [fn. 1] (same line).
  - In review round 2, ScholarPeer's acceptance rises from 79.6% to 93.9%, while the held-out reviewer's falls from 73.5% to 69.4% [Tab. 5] (tex:tables/ablation_rebuttal.tex:13-14).
  - So optimising against the in-loop reviewer moved that reviewer's number, but not the held-out one.
- **Attack:** none is needed, if R-OPS-12 binds evaluation too.
  - Then every author, in-loop judge, reporting judge and reporting auditor is a Claude model.
  - A manuscript revised by Claude against a Claude reviewer is rated by a Claude judge. What the revision learned to please may carry over to the judge, and Table 5's kind of divergence would no longer show.
  - R-MEAS-5 compares the judge only with the in-loop judges, not with the family that wrote the manuscript. IR-29 requires that comparison for the auditor.
  - The judge's prompt is a behaviour file (R-OPS-2). It would sit in this public repository, which the engine's developers and their agents read.
    - IR-29 keeps the auditor's prompts "outside everything that any engine job or engine agent can read". R-MEAS-5 has no such rule.
  - The query log covers queries made through the engine's interface. A prompt over a public model can be run anywhere.
- **Would we notice:**
  - The flag says the judge shares a family. It says nothing about whether the rating moved.
  - R-MEAS-5's test loads that configuration, with its flag (`07-measurement.md:53`).
- **Guard:**
  1. **R-OPS-12 states its scope.** It says whether it binds the post-run reporting judge and auditor, with its reason and the alternative not taken.
     - Vlad's instruction is about running the engine: "I am going to use it based on my claude subscription ... I don't wanna pay for API" (`DEVELOPMENT_PROCESS.md`, section "2026-10-02: the review gate opens").
     - The paper's own held-out reviewer is an outside service.
     - If R-OPS-12 does bind evaluation, R-MEAS-5 and R-INT-7 must say that IR-29's flagged fallback is then the only configuration, and every reported rating and integrity count carries the flag.
  2. **R-MEAS-5 is tightened:**
     - it also compares the judge with the families that wrote the manuscript;
     - it keeps the judge's prompt, routing and verdicts where no engine job, agent or development session can read them, hashed before the reported runs (IR-29's rule; depend on A-INT-3);
     - it marks the query log as a process rule wherever it cannot be enforced.
  3. **A measured transfer control**, below, is reported beside every rating.
- **Control:** prose-only pairs.
  - For a sample of exported runs, a writer revises the final manuscript against the in-loop reviewer's comments, with the method, the code and every bound number fixed.
  - The in-loop reviewer, as the positive control, rates the revision higher, as ScholarPeer did in Table 5.
  - The reporting judge's shift on the same pairs is measured, with its n and interval.
  - If that shift is not clearly below the in-loop reviewer's, the judge's ratings are reported as in-distribution, not as held out.

**NEW-10 · major · Enforcement twins cover one clause per test, and the network clause passes with no guard**
- **Where:**
  - `docs/requirements.md:30`: "Each runs beside a twin with the guard off, in which the planted attack succeeds".
  - R-OPS-8's test: "agent code run by the harness cannot reach the network. In the twin with one policy per stage, the filter's write succeeds" (`08-operation.md:72`).
  - R-OPS-1 runs its tests "in CI with the network disabled" (`08-operation.md:16`).
- **Why the test does not work:**
  - In a CI without network, "cannot reach the network" holds with no guard at all.
  - R-OPS-8's twin exercises only the write clause.
  - The same gap, a clause with no twin of its own, appears in five more places:
    - R-INT-1 requires agent code to run "without network" (`06-integrity.md:16`), but none of its four planted attacks tries the network.
    - R-INT-2: "an agent's write to an evaluation file fails in its real sandbox" (`06-integrity.md:35`). Nothing shows that the write succeeds with the guard off.
    - R-INT-3: "a report job requested before the freeze is refused" (`06-integrity.md:43`). No twin in which the job returns a number that reaches a critic.
    - R-INT-8: "A writer scripted to open the run log finds no such path in its sandbox" (`06-integrity.md:95`). No twin with the run directory mounted.
    - R-RUN-2: "a manifest edited after its hash was registered makes the next harness job refuse to run" (`01-run.md:31`). No twin.
    - R-OPS-8's install and GPU clauses have no twin either.
- **Would we notice:** no. CLAUDE.md's rule "A green check must prove it ran" fails clause by clause.
- **Guard:**
  - Every clause of an enforcement test gets its own twin, or a positive control: the same operation succeeding in the same environment just before the guarded attempt.
    - For the network clause: the same request succeeds, against a local endpoint, from a role allowed network.
    - For a write clause: the same write succeeds with the guard off.
  - Each enforcement test states its clauses as attack, outcome with the guard on, and outcome of the twin, so the checker can count them (NEW-15).
- **Control:** remove the network guard and run the clause in the CI without network.
  - As written, the test passes.
  - With its positive control, the test fails, as it must.


---

*Continued in `evaluation-integrity-engineer-closure-2.md`. The report is split at "### Minors" only to keep each file under 600 lines; nothing else is changed.*
