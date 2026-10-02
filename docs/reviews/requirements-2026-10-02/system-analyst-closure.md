# Closure check: the system-analyst elicitation against the revision c2ad177

- **Persona:** system-analyst, looking for what is missing. **Date:** 2026-10-02.
- **Mode:** read-only.
  - I changed no file in the worktree and no git state. The untracked `docs/reviews/requirements-2026-10-02/codex-review.md` that `git status` now shows is another session's.
  - I planted defects only in copies in the session scratchpad, then deleted them.
- **Read:**
  - `fix-list.md`;
  - `docs/requirements.md` and `docs/requirements/01-run.md` … `08-operation.md`;
  - my `system-analyst-elicitation.md`;
  - Vlad's instruction, `DEVELOPMENT_PROCESS.md:511-512`;
  - on other branches, read with `GIT_OPTIONAL_LOCKS=0 git show`:
    - task 6's `docs/integrity/blocking-decisions.md`. It is unchanged between d5d0d61 and the branch head 04522df.
    - task 6's review fix list at 04522df, `docs/reviews/integrity-blockers-2026-10-02/fix-list.md`, F-0 to F-46. It landed after the revision.
    - RJ-1…7, BA-1…6 and the reuse survey.
- **Paths.** Requirement files are cited without `docs/requirements/`. The other documents are cited by name.

## Proof that the checks ran, and that each can fail

**On the real files at c2ad177**, each checker exits 0, and its self-test passes.

| Checker | Last lines | Self-test |
|---|---|---|
| `requirement_coverage.py` | `total 177 172 23 5`; `requirements: 82 (RUN 8, PRIM 10, STG 13, AGT 9, STATE 10, INT 10, MEAS 10, OPS 12); leave-out decisions: 5`; `task-2 register rows: 33; decided by a requirement: 33; in the decisions table: 15 confirmed, 18 refined`; `0 problem(s)` | 40 cases ok, last: `ok   --write fills the column: before ['column'], after no problem, identical to the clean file: True` |
| `check_citations.py` | `27 file(s) checked, 0 problem(s)` | 46 cases ok |
| `trace_coverage.py` | `total 177 177`; `16 source document(s); 21 key(s)`; `0 problem(s)` | 16 cases ok |
| `register_coverage.py` | `Register lines: 143 of 143 full entries carry exactly one`; `0 problem(s)` | 18 cases ok |

**Each zero can be non-zero on the real data.** In scratch copies of the real files, one planted defect per checker gives exit 1:

| Checker | Planted defect | Result |
|---|---|---|
| `requirement_coverage.py` | R-STG-2's trace of `P-SEED-1 … 4` removed | `unmapped: P-SEED-1 is traced by no requirement and left out by no decision` |
| `check_citations.py` | a clean copy of `08-operation.md` first, then `[§9.9]`, `[App. Z.9]` and an invented quote | the clean copy gives 0 problems; the plants give `no such location: [§9.9]`, `no such location: [App. Z.9]` and `quote not in the paper` |
| `trace_coverage.py` | P-SEL-1's row deleted | `missing: P-SEL-1 … has no row in Part 2` |
| `register_coverage.py` | A-EVAL-1 renamed A-EVAL-99 | `FAIL: line 191: A-EVAL-99 is not defined in any gap section` |

**The checker claims I tested myself:**
- caught, exit 1:
  - a trace left only inside a code fence;
  - one ID traced twice while another goes missing;
  - a range that runs past the last ID (`P-SEED-1 … 9`).
- **not** caught, exit 0:
  - a trace hidden in `<!-- -->`;
  - an en dash in a register ID under *Depends on* (`U–EVO–2`).
- My own scan of the *Depends on* fields:
  - 174 IDs are attributed to their owning task, with 0 mismatches;
  - a planted wrong attribution, U-INT-4 to task 5, is flagged.

## 1. My items

Totals over 89 items: 60 closed, 25 partly closed, 4 open, 0 regressed.

### MISS

| ID | Status | Evidence | Still missing |
|---|---|---|---|
| MISS-1 | partly closed | `01-run.md:93-99` (R-RUN-7); `requirements.md:109` (Q-1) | Q-1's second half has no decision: what the export does when a test number contradicts a claim written from validation numbers. Task 6 lists this as an attack its rules do not stop: "after the final fill, text written against validation numbers can overclaim on test. Detection only" (`blocking-decisions.md:417`). R-RUN-7's test (`01-run.md:104`) has no fixture whose validation shows a gain and whose test does not. **Proposed fix:** the export record lists each frozen row whose search and report gains differ in sign; the tail's writer receives that list; an export where *ours* is such a row is marked and counted apart. |
| MISS-2, MISS-4, MISS-9 to 17, MISS-23, MISS-25, MISS-27 | closed | MISS-2: `06-integrity.md:17-18`. MISS-4: `05-state.md:60-70`, `requirements.md:112`. MISS-9: `01-run.md:79-89`. MISS-10: `08-operation.md:52,56`, with C+'s re-execution tested at `06-integrity.md:82`. MISS-11: `08-operation.md:12,16`. MISS-12: `08-operation.md:76,80`. MISS-13: `03-stages.md:193`, `08-operation.md:20`. MISS-14: `02-primitive.md:12-19`. MISS-15: `08-operation.md:28,32`. MISS-16: `08-operation.md:68`, `06-integrity.md:99`. MISS-17: `06-integrity.md:86`, `07-measurement.md:24`. MISS-23: `02-primitive.md:95,100`. MISS-25: `04-agents.md:56`. MISS-27: `08-operation.md:91` | MISS-4: task 6's F-3 is pending. MISS-15: a second real backend under R-OPS-12, see NEW-9. MISS-9: where the noise floor comes from, see NEW-8. |
| MISS-18 | closed | `08-operation.md:84,87` | G's own papers and README files carry author e-mail addresses. Unless verbatim task content is allow-listed, the scan fails on the first real task. |
| MISS-3 | partly closed | `02-primitive.md:118-121` | The map from role to outcome covers five roles. See NEW-3. |
| MISS-5 | partly closed | `05-state.md:82,86` | The trail lacks: the precondition's result, with the hash of the rule it used; the filter's verdict; each `Good` idea's rank in the band; and, for the chosen idea, its ablation, control, guard and meta decisions. The test checks only "each of the parts above". |
| MISS-6 | partly closed | `05-state.md:28`: "leaves an audit row with its cause" | The row's content is not stated: old and new hashes, the guard's inputs, the rule's hash. A row that says only "guard" passes `05-state.md:30`. A person's resume leaves no row (NEW-4). |
| MISS-7 | partly closed | `08-operation.md:36,40` | The budget has no unit under the subscription (NEW-5). |
| MISS-8 | partly closed | `04-agents.md:47` | The default configuration still holds 8 (NEW-6). |
| MISS-19 | partly closed | `01-run.md:108` | It contradicts R-OPS-4, R-OPS-12 and R-RUN-5 (NEW-4). |
| MISS-20 | **open** | `fix-list.md:50` reads "Accepted: R-STG-2 and R-STG-7"; `03-stages.md:24,49,106` | Neither requirement bounds attempts or rejects duplicates. No requirement file contains "duplicate" or "distinct". **Fix:** SEED and EVO reject an idea that a stated rule finds equal to one in the pool or the traces. The seed loop ends after M attempts with a recorded outcome; M is task 5's. Test it with a generator scripted to repeat itself. |
| MISS-21 | partly closed | `01-run.md:17-24,31` | R-RUN-2's field list omits fields that other requirements read from the manifest. The seed list (`07-measurement.md:65`: "taken from the manifest's list"). The settings a rebuttal may use (`03-stages.md:164`: "settings the manifest registers"). The declaration that a method is deterministic (`07-measurement.md:65`). IR-4's packaging diff. A manifest without a seed list therefore loads. |
| MISS-22 | partly closed | `08-operation.md:60,64` | No outcome is defined for a task that reaches its wall-clock bound; none of R-RUN-5's nine fits. No rule says whether a usage-window pause (`08-operation.md:99`) counts toward the bound. The test covers only a harness job. |
| MISS-24 | partly closed | `04-agents.md:56,60` | The score is "recorded as unknown, never as zero", but SEED sorts "by score, descending" (`03-stages.md:24`) with no place for unknown. That place decides whether the idea enters round 0. |
| MISS-26 | partly closed | `04-agents.md:80,90` | The test checks only "one per judge", so nothing shows that the other agents' acceptance cases exist. The Meta-Reviewer, a judge, has no first case: the elicitation's DynaSpec-RAG case, a "strict do-no-harm" claim while 2 of 7 datasets regress, expected `Refine`. |

### CONT

| ID | Status | Evidence | Still missing |
|---|---|---|---|
| CONT-1, 2, 4, 6, 7, 8, 9, 10, 12, 13, 15, 16, 18 | closed | CONT-1: `01-run.md:20`, `03-stages.md:88`. CONT-2: departure recorded at `01-run.md:101`. CONT-4: `03-stages.md:61-62`. CONT-6: `requirements.md:112`. CONT-7: `01-run.md:79-85`. CONT-8: `requirements.md:193`. CONT-9: `requirements.md:120-133`. CONT-10: `02-primitive.md:47`, `03-stages.md:40`. CONT-12: `05-state.md:22,45`. CONT-13: `08-operation.md:76`. CONT-15: `03-stages.md:193`. CONT-16: `requirements.md:26`. CONT-18: `requirements.md:135-162` | CONT-10: the fix list contradicts itself (NEW-15). |
| CONT-3 | partly closed | `01-run.md:35,39` | A child run has nothing to run its sealed check against (NEW-11). |
| CONT-5 | partly closed | `04-agents.md:47-49` | NEW-6. |
| CONT-11 | **open** | `fix-list.md:60` promises that "`docs/requirements.md` says that the requirements supersede the candidates where they differ" | No such sentence exists: "supersed" matches nothing under `docs/requirements*`. `traceability.md:204` still gives P-META-2 "accept → export", against R-RUN-7. `traceability.md:153` still offers "nesting once per task, or inside each A_Coder call (A-BASE-1)", which R-STG-3 decided. |
| CONT-14 | partly closed | `01-run.md:108` | NEW-4. |
| CONT-17 | partly closed | `fix-list.md:77` | Decided only in the fix list; absent from `requirements.md:107-118` (NEW-15). |
| CONT-19 | **open** | `07-measurement.md:15`; `05-state.md:53` | The ablation's exit is still unmarked, and reading 3 still counts an unaccepted `Refine` as survival. The revision's precondition sends more ideas down that path (NEW-1). |

### ORPH

| ID | Status | Evidence | Still missing |
|---|---|---|---|
| ORPH-1, ORPH-3 | closed | ORPH-1: `requirements.md:114,120-133`, and the checker's "a file with no requirement". ORPH-3: `03-stages.md:106,134` | none |
| ORPH-2 | partly closed | `traceability.md:313` now agrees with IR-6 | The general rule it needed is CONT-11's missing sentence. |
| ORPH-4 | partly closed | `03-stages.md:77,84` | "the idea's component list" has no declared source. The switches at `03-stages.md:76` are the obvious source, but nothing names them. The FULL engineer (`03-stages.md:27`, "tunes and repairs only") has no refusal case in R-STG-5's test. |

### The elicitation's Part 2 flags, Parts 4 and 5, and the quantities table

| ID | Status | Evidence | Still missing |
|---|---|---|---|
| U-EVO-4 flag | **open** | `fix-list.md:69` accepts "Human abort; the failing unit's ID" into R-RUN-5 | The nine outcomes (`01-run.md:60-68`) include no abort. The record "gives the stage, the reason, the last valid core state and the cost" (`01-run.md:70`), with no unit ID. A run that a person abandons has no outcome, and drops out of every denominator. |
| U-BASE-2 flag | partly closed | `03-stages.md:61` | "within the manifest's tolerance" names no owner for the value. R-RUN-6's "every value of the rule is task 5's" does not cover it. |
| A-ABL-1 flag | partly closed | `03-stages.md:133` | NEW-12. |
| U-META-2, U-ABL-5 and U-SEED-3 flags | partly closed | `04-agents.md:80-85` | See MISS-26. |
| A-TOP-1 flags, and the other flags | closed | `03-stages.md:40,45`; `06-integrity.md:47-51,111`; `03-stages.md:115,121` | The ablation's exit: CONT-19. |
| Quantities table | partly closed | `01-run.md:85`, `08-operation.md:36,60` | The baseline tolerance has no owner. The seed loop's attempt bound has neither value nor owner (MISS-20). |
| Part 4.1, the leave-outs and the *replaces* status | closed | `requirements.md:135-162`; 23 elements carry *Departs from* | Four more departures are missing (NEW-9). |
| Part 5 | partly closed | `traceability.md:287-288` | 9 of the 11 cells trace to the requirement that carries their decision. P-ROSTER-32 (gap U-BASE-1) is not traced by R-RUN-2. P-ROSTER-33 (gap U-ABL-2) is not traced by R-STG-9. |

### CHK

| ID | Status | Evidence | Still missing |
|---|---|---|---|
| CHK-1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 14, 15, 16, 19, 20, 21, 22 | closed | `requirement_coverage.py:16-44` and a self-test case each. CHK-10, CHK-19 and CHK-22 shown on the real files above | none |
| CHK-6 | **open** | no disposition: `fix-list.md:79` lists neither CHK-6 nor CHK-9 | An X- decision has no decider, no date, and no field for the rows it rests on (NEW-10). |
| CHK-9 | partly closed | no disposition | The checker accepts any non-empty *Why ours*. In content, all 19 untraced requirements name a source (my scan). |
| CHK-13 | partly closed | | The checker never compares a clause's "task N" with the register. In content, 174 of 174 attributions are right. |
| CHK-17 | partly closed | | Only P- IDs are checked. `U–EVO–2` under *Depends on* is dropped in silence, exit 0. |
| CHK-18 | partly closed | | Fences are excluded. An ID inside `<!-- -->` counts as a trace, exit 0. |

### Q

| ID | Status | Evidence | Still missing |
|---|---|---|---|
| Q-2, 3, 4, 5, 6, 7, 10 to 15, 17 | closed | `requirements.md:110-118`. Q-3 through `03-stages.md:61` (IR-15); Q-10: `08-operation.md:52`; Q-11: `03-stages.md:133`; Q-12: `02-primitive.md:47`; Q-13: `08-operation.md:76` | Q-4's effect on the threshold: NEW-6. |
| Q-1 | partly closed | | See MISS-1. |
| Q-8, Q-9 | partly closed | `requirements.md:115-116` | Both are decided, but they contradict each other through R-RUN-5 (NEW-4). |
| Q-16 | partly closed | `fix-list.md:77` | Missing from `requirements.md:107-118`. |

## 2. New findings

Ordered by what each would cost to discover late.

### NEW-1 · major · An ablation that never establishes attribution is exported unmarked, and counted as having survived

**Location:** `07-measurement.md:12-15,20`; `03-stages.md:129,132`; `05-state.md:53`; `01-run.md:93`.

**What the text says:**
- R-STG-9: "a `Good` it blocks counts as `Refine`", and "if a second `Refine` comes once N_abl is spent, drafting follows with the current h_best".
- R-STATE-6 marks only "the last meta verdict".
- R-MEAS-1's reading 3 is "the gain survived the ablation, with no `Reject`".

**What goes wrong:**
- An idea whose mechanism-off control does not lose, EI-7's case, gets one A_FullEng attempt. It is then drafted, exported unmarked, and counted as having survived.
- R-MEAS-1 also redefines task 6's row. The register's A-EVAL-1 (`unspecified.md:191`) reads: "at least one `Good` idea (§3.3), beating the human SOTA (Figure 1), or a gain the ablation attributes to the mechanism (Table 15)". R-MEAS-1 has "a paper was exported" and "no `Reject`" instead. The presumption table (`requirements.md:181-190`) does not list A-EVAL-1.
- R-MEAS-1's test expects "an ablation reject with a positive gain, no, yes, no". Yet reading 2 is "computed from the report-role records of the test event", and R-RUN-7 runs the tail only "when meta-review ends". A task that ends in an ablation reject never has a test event, so "yes" cannot occur.

**Fix:**
- The export record carries the last ablation verdict that stood, precondition included. An export without an accepted `Good` is marked *attribution not established* and counted apart.
- R-MEAS-1 states the register's readings, with reading (c) being that the last ablation verdict that stood is `Good`. Add A-EVAL-1 to the presumption table.
- For the reject case, the test expects "no, not measured, no", unless task 6 adds a diagnostic test event. Raise that in task 6's review (IR-14).
- **Test:** an ablation that ends in `Refine` with N_abl spent exports a paper marked *attribution not established*, and reading 3 is "no".

### NEW-2 · major · The last manuscript repair is exported without the number and reference checks

**Location:** `06-integrity.md:111,116`, against task 6's G3 (`blocking-decisions.md:234`).

**What the text says:**
- R-INT-10: "A repair does not start the sequence over; only the compile check runs again after the last hook".
- G3 covers "every manuscript version, before any reviewer reads it and before export", including "every other number is declared, and checked against the manifest or the row's configuration".

**What goes wrong:**
- The alignment repair runs last. It edits method text, and typically changes hyperparameter values to match the code.
- The repaired text then reaches export after compiling only.

**Fix:**
- After any repair, the number-provenance check and the reference lookups run again on the repaired text. Alternatively, a repair diff that adds a numeric token or a citation key is refused.
- **Test:** an alignment repair scripted to add a typed number is caught before export.

### NEW-3 · major · R-PRIM-10 maps five roles, and infrastructure faults become research outcomes

**Location:** `02-primitive.md:119-121,130`; `08-operation.md:36`; `01-run.md:95` and `03-stages.md:34` (the tail's writer).

**Gap 1: most roles have no mapping.**
- The roles with no mapping:
  - the Idea Generator, A_Evolve, the Ablation Planner and the Ablation Critic;
  - A_FullEng, in ABL and in META;
  - the Result Comparison Agent;
  - the Peer Reviewer, the Rebuttal Planner, the Paper Enhancer and the Meta-Reviewer;
  - the tail's "writer", which no roster entry (`04-agents.md:10`) names;
  - the reference and alignment checkers;
  - LIM, which only R-STG-1 states.
- For those roles the test, "each fault … ends in its recorded outcome", has no expected value, so it cannot fail.

**Gap 2: infrastructure faults are treated as research outcomes.**
- "reject the candidate, for an idea, which becomes `Bad` with the reason *error*" also applies to an outage of the harness host.
- A_Evolve then learns from the outage, and the task can end with *no Good idea*, counted as a research failure.

**Gap 3: a session stopped at its budget has no next step.** "A session that reaches its budget is stopped and recorded" says nothing of what the stage does next.

**Fix:**
- Make the role-to-outcome table total, as data, and fail at load when any roster role lacks an entry.
- Keep infrastructure faults apart from faults of agent output or agent code. An infrastructure fault pauses the run, or ends it with *error after retries* marked as infrastructure. It never marks a candidate `Bad`.
- Name the roster entry of the tail's writer.
- **Test:** a harness host scripted to be unavailable pauses the run, and no idea becomes `Bad`.

### NEW-4 · major · Stop, resume and the single outcome record contradict each other

**Location:** `01-run.md:57,108`; `08-operation.md:36,99`; `05-state.md:64`; `requirements.md:115-116`.

**What the text says:**
- R-RUN-5: "Every task ends with exactly one outcome record".
- R-OPS-4: a budget is "fixed before the task's first run", yet a task "ends with *budget exhausted* … and resumes from its record once the budget is raised".
- R-STATE-7 reads "the configuration versions … its record names, never the files as they now are on disk". A budget raised on disk is therefore ignored on resume.
- R-RUN-8: "Every stop … ends the run with its outcome record … a person may resume a stopped or paused run". That covers *ablation reject*, *manuscript gate failed* (re-buying R-INT-10's 2 repairs) and *error after retries*, which are re-rolls that IR-18 bounds.
- R-OPS-12 pauses "until the environment is fixed", which needs a person. Q-9's "No" and R-RUN-8 allow only the usage-window pause.

**What is missing:** no audit row records who resumed the run, or what changed.

**Fix:**
- A closed list of resumable stops: *budget exhausted*, infrastructure *error after retries*, and the two pauses. Every other outcome is final.
- A resume appends an audit row to the run's record, and R-STATE-7 reads it: who, when, and the change (budget from X to Y).
- The outcome record becomes append-only, and its last entry is the task's one outcome.
- R-RUN-8 lists the billing pause.
- **Test:**
  - resuming *ablation reject* is refused;
  - a budget amendment written into the run's record is honoured, while an edit on disk is ignored;
  - the task ends with one final outcome, and both the stop and the resume rows are recorded.

### NEW-5 · major · The budget has no unit under the subscription

**Location:** `08-operation.md:36,40,99`; `07-measurement.md:73,77`.

**What the text says:**
- R-OPS-4 gives "a budget" and "its declared reservation" in no unit.
- R-MEAS-8's test requires "a billed amount of zero" for every subscription call.
- R-OPS-12 permits no metered call.

**What goes wrong:**
- A money budget can therefore never bind.
- The GPU-hours of harness jobs sit in no budget.
- The BA contract's unit, `claude_calls`, is not adopted.

**Fix:**
- R-OPS-4 names its budgeted resources, per session and per task:
  - subscription calls, with their reported tokens;
  - harness GPU-hours;
  - wall-clock;
  - metered money, fixed at 0.
- The values are task 5's (U-COST-1).
- **Test, in subscription mode with every call billed at $0:**
  - a budget of k calls refuses call k + 1 before dispatch;
  - a GPU-hour budget refuses the harness job that would exceed it.

### NEW-6 · major · The threshold 8 is guessed for a reviewer it was never calibrated on

**Location:** `03-stages.md:32,163,193`; `02-primitive.md:91`; `04-agents.md:47,52`; `requirements.md:31`.

**What the text says:**
- R-STG-13's defaults include "the threshold 8".
- R-AGT-5: "The threshold is stored with the reviewer's version and derived by a recorded calibration rule, which is task 6's (A-EVAL-3)".
- How to read: "a value another task owns is named, never guessed, and the configuration refuses to load without it".
- `traceability.md:193,233` call the value "reviewer-dependent, to calibrate", yet P-CFG-9 and P-PEER-2 trace as met.
- R-AGT-5's test, "a second mock reviewer … runs the review stage unchanged", passes when the threshold is not recalibrated.

**What else is affected:** the refusal to load also omits the budgets, the retry policy and the wall-clock bounds, which other tasks own.

**Fix:**
- 8 stays in the paper profile only, bound to ScholarPeer.
- The subscription profile refuses to load without a calibration record for the configured reviewer's version.
- Mark P-CFG-9, P-PEER-1 and P-PEER-2 as departures.
- Extend R-STG-13's refusal to every value that another task owns.
- **Test:** a reviewer version with no calibration record fails to load, and the message names A-EVAL-3.

### NEW-7 · major · An unit in doubt that cannot be settled has no branch, and R-STATE-7's test passes a blind retry

**Location:** `05-state.md:62,70`; `02-primitive.md:130`; RJ-4 on `codex/run-journal`.

**What the text says:**
- R-STATE-7: a unit in doubt "is reconciled before any retry, never retried blind".
- RJ-4: "`Unknown` blocks execution."
- R-PRIM-10 requires that "the run never hangs".
- R-RUN-8 allows no person to step in.
- R-RUN-5 has no outcome for an unresolved operation.

**The test cannot fail on a blind retry.** It allows "the unit in flight at most once more" even for a kill between a call's return and its record, where RJ-3 expects "never execute again".

**Fix:**
- Reconciliation is automatic and bounded.
- At the bound, a unit still `Unknown` is settled as spent, with its cost unknown. Then either it is re-run once with the duplicate recorded, or the run ends with a named outcome added to R-RUN-5.
- **Test:** zero further calls after a kill that follows the call's return; at most one after a kill before it.

### NEW-8 · minor · The baseline belongs to the task, but each run carries it

**Location:** `03-stages.md:58,61`; `01-run.md:46,85`; `06-integrity.md:43`.

**What the text says:** "The baseline stage runs once per task, before round 0", and the check runs "once per manifest version".

**What is missing:**
- No requirement says that a task's second run, which IR-18 allows, reuses E_base, C_base and the check.
- Nothing says what happens when two runs start together (R-OPS-11). A second sealed check is a report job outside IR-14, which R-INT-3's test turns into *integrity halt*.
- R-RUN-6 "refuses a margin below k times the baseline's measured run-to-run spread", but at a task's first load no spread exists, so the check passes without input.

**Fix:**
- The baseline's records are task-scoped and measured at packaging, as task 6's F-6 proposes. They are stored in the manifest version, and every run reads them by hash.
- A manifest with no recorded spread fails to load.
- **Test:** two runs of one task, one after the other and side by side, leave one sealed check and one baseline scoring.

### NEW-9 · minor · Departures that R-OPS-12 forces are not recorded

**Location:** `04-agents.md:39-40,56-57,64`; `03-stages.md:66`.

R-OPS-12 requires: "Every LLM call, agents and judges alike, goes through the Claude subscription".

The following still trace as if met:
- P-ROSTER-49, Antigravity, Table 8's backend, by R-AGT-4;
- P-ROSTER-47, Google Search, by R-AGT-6, where "the adapter meets R-OPS-12" without saying how;
- P-ROSTER-45, by R-AGT-7, although the reuse survey (§1) says PaperOrchestra needs "model credentials";
- P-ROSTER-6 under R-STG-3, although the agent now reproduces nothing.

**Fix:**
- Add these elements to *Departs from*.
- Admit PaperOrchestra only if task 4's trial shows that its model calls go through the subscription.

### NEW-10 · minor · Other tasks' proposals are presumed but not listed

**Location:** `requirements.md:139-157,170-176,181-190`; `07-measurement.md:33`.

**What goes wrong:**
- X-3 says that a comparison added later "compares only on shared tasks, metric, hardware and gain rule, by U-EVAL-10's decision". That is task 6's proposal, stated as if decided.
- The X- decisions rest on U-EVAL-6, U-EVAL-7 and U-EVAL-9 (task 5), and on U-EVAL-10 and A-EVAL-8 (task 6). None of these appears in the pending table.
- R-MEAS-3 presumes U-EVAL-1's aggregates, and R-MEAS-1 presumes A-EVAL-1. Neither appears in the presumption table.

**Fix:** give X- decisions a *Rests on* field that the pending-table check reads, and list the presumed proposals.

### NEW-11 · minor · A chained run has nothing to run its sealed check against

**Location:** `01-run.md:21,35`; `03-stages.md:61`.

**What the text says:**
- R-RUN-3: "The conversion carries no number of the report role into the next G".
- R-RUN-2 requires "the published reference numbers" as a manifest field.

**What goes wrong:** the child's only published numbers are the parent's report-role results.

**Fix:**
- The conversion writes the parent's report-role results into the child's manifest as its published numbers, sealed from every agent (IR-15).
- **Test:** the child's sealed check reads them, and the scan of the child's agent inputs still finds none.

### NEW-12 · minor · A `Reject` in the second downstream pass is ambiguous

**Location:** `03-stages.md:133,184-189`.

**What the text says:** "of a candidate promoted in this downstream pass, it undoes the promotion".

**What goes wrong:** the meta refinement was promoted by META, not in pass 2. Read literally, a `Reject` in pass 2 ends a task that already holds pass 1's draft.

**Fix:**
- A `Reject` in pass k ≥ 2 undoes the meta promotion, and sends pass k − 1's outputs to the tail, unapproved.
- Add this case to R-STG-12's test.

### NEW-13 · minor · The manuscript cannot show the published numbers, or the baseline row

**Location:** `05-state.md:90`; `06-integrity.md:86`.

**What the text says:**
- The table "is written only by engine code from the harness's result records", and "each entry cites its records by ID and hash".
- The main results table is "rendered … from the method's own entries, so that no other row's entry can stand there".
- Task 6 defines the table as rendered "from result records and from the manifest's published numbers" (`blocking-decisions.md:27`).

**Fix:**
- Entries come from harness records or from the manifest, each labelled with its source.
- The main table renders each row from that row's own entries.
- **Test:** a published number inserted from its entry passes; the same value typed by the writer fails.

### NEW-14 · minor · Tests that cannot settle what they guard

**Location:** `07-measurement.md:93`; `06-integrity.md:43`; `08-operation.md:102`.

**What goes wrong:**
- R-MEAS-10 accepts a pass rate of "about half" and "almost none".
- R-INT-3 accepts a gain "zero within its noise".
- R-OPS-12's guard against API billing is tested only against a mock.

**Fix:**
- State the bounds: at 200 runs, 0.5 ± 0.106 (3 standard errors), and at most the normal tail at k plus 3 standard errors. For R-INT-3, adopt task 6's +1.87 against 0.
- Add a $0 enforcement case: with the real CLI adapter and an invalid key planted in the environment, no `claude -p` process is spawned. In the twin with the check off, it is spawned.

### NEW-15 · minor · Bookkeeping

**Location:** `fix-list.md:64,79,98`; `requirements.md:103,107-118`.

**What goes wrong:**
- `fix-list.md:64` reads "Kept: 16 judged refinements", while `:98` and R-STG-1 have 15 refinements and 16 rounds.
- "The review raised ten questions for Vlad", but there were 17.
- Q-16 is missing from the table, and Q-3, Q-10 to Q-13 and Q-15 have no pointer there.
- CHK-6 and CHK-9 have no disposition.

**Fix:** correct line 64, and list all 17 questions, each with where it is answered.

### NEW-16 · minor · Two defects in the checker

**Location:** `requirement_coverage.py:66-71,196-199,308`.

**What goes wrong:** both were shown on copies of the real files, each with exit 0.
- A trace inside `<!-- -->` counts.
- A malformed register ID under *Decides* or *Depends on* disappears in silence.

**Fix:** strip HTML comments before parsing, and match U- and A- IDs loosely, then report every non-strict form.

### NEW-17 · minor · Task 6's review already schedules changes to rules the requirements cite

**Location:** `requirements.md:27`; `06-integrity.md:8`; task 6's `fix-list.md` at 04522df.

The requirements call task 6's rules "not yet reviewed". The review has since landed, and its fix list will change these points:
- **F-6** moves the baseline check to admission: "a baseline that fails is never admitted, so no run starts". This touches R-STG-3, R-RUN-4 and R-RUN-5.
- **F-3** resumes "from its last finished stage", which touches R-STATE-7.
- **F-12** says "Success is never the sign of a point estimate", which touches R-MEAS-1.
- **F-32** says "The harness reads no parameter from the code tree", which touches the switches in R-STG-4 and R-STG-9.
- **F-46** says "The coordinator puts the question to Vlad", against "Don't ask me anything" (`DEVELOPMENT_PROCESS.md:512`).

**Fix:**
- List each of these as a known incoming change, beside the requirement it will reopen.
- Send F-46's conflict to the coordinating session, not to Vlad.

## 3. Verdict

Task 2 should not close yet, but nothing found needs a redesign.

**Strengths of the revision:**
- 60 of my 89 items are closed.
- Every checker runs, and each is shown to fail on a planted defect in the real files.
- The boundary with task 6 holds: 174 of 174 attributions are correct.

**What must change before task 2 closes:**
- **The seven majors.** Each is a local edit of a sentence or two, plus a test case:
  - NEW-1: the ablation's exit and reading 3;
  - NEW-2: re-check after the last repair;
  - NEW-3: a total failure map, with infrastructure kept apart;
  - NEW-4: resume semantics;
  - NEW-5: the budget's unit;
  - NEW-6: the threshold;
  - NEW-7: units in doubt.
- **The dispositions the fix list accepted but the text does not carry:**
  - MISS-20: duplicates and the attempt bound;
  - U-EVO-4: human abort and the failing unit's ID;
  - CONT-11: the supersede sentence;
  - Q-16.

**Then:** run a narrow closure check on those items only. The minors can be fixed in the same pass, or ticked into `TODO.md` as open work. Before the PR, record task 6's 04522df fix list as known incoming changes (NEW-17), so the closure does not certify text that is already scheduled to change.
