# Closure check 2: task 2's requirements at fd9bcf9, against task 6 at adc3484

**Reviewer:** evaluation-integrity-engineer, 2026-10-02. This was read-only: I edited nothing and ran no git command that changes state. I copied task 6's adc3484 files to the session scratchpad and read them there.

**What I read:**
- `docs/requirements.md` and `docs/requirements/01–08` at fd9bcf9.
- The "From the integrity closure" table in `fix-list.md:210-233`.
- adc3484's `blocking-decisions.md` and its four files under `decisions/`. Below, `bd:` means `blocking-decisions.md`, `u4:` `u-int-4-who-computes.md`, `ut5:` `u-top-5-which-split.md`, `ai1:` `a-int-1-gates-or-audit.md` and `ai3:` `a-int-3-checker-and-auditor.md`.

**Checks run:** `requirement_coverage.py` gives "0 problem(s)", and `--selftest` passes every case. The checker now enforces a test's tier (`requirement_coverage.py:239-240`). It does not check that each clause has a twin.

## 1. NEW-1 to NEW-10

| Item | Status | Evidence | What remains |
|---|---|---|---|
| NEW-1 · blocker · seed luck through the tail | **closed** | R-RUN-7 step 1: every frozen row except E_base is fitted again at report seeds, disjoint from the search seeds; E_base's report results come from admission (`01-run.md:104`). This matches IR-14.4 and IR-15.1 (`ut5:42`, `:46`). An enforcement test plants seed-dependent training noise, with a twin (`01-run.md:120`). R-INT-3's twin now uses evaluation noise only, with its expected value stated (`06-integrity.md:51`) | Minor: the twin's "about half the search gain" holds only when fit noise equals evaluation noise. State σ_a = σ_e, or task 6's formula (`ut5:137`). The partial seed game stays detection only (`bd:285`) |
| NEW-2 · the precondition decides nothing exported | **closed** as a mechanism | ABL's at-limit cell and the *Attribution* bullet mark the export *attribution not established* (`03-stages.md:31`, `:162`). R-MEAS-1's third reading reads that mark (`07-measurement.md:15`). Tests at `03-stages.md:174`, `:177` and `07-measurement.md:24` | The mark is only as good as the precondition it reads, so the third reading inherits NEW-3's bias |
| NEW-3 · the precondition re-reads E_best | **partly closed; not implementable as written** | R-STG-9 calls for paired fits "on the same seeds" and "never reads E_best" (`03-stages.md:156`, `:158`). See the note below the table | Fix and control under *The NEW-3 issue* below |
| NEW-4 · the author scopes the switch | **partly closed** | A scope check at the code hook, against the description recorded before scoring, before any veto (`03-stages.md:105`; `06-integrity.md:119`). A floor against E_base (`03-stages.md:158`). No text edit repairs a switch finding (`06-integrity.md:77`). A sabotage enforcement test with its twin (`03-stages.md:184`) | (1) The scope check is an LLM judgement, but IR-31.1 does not list it (`ai3:30`). So fix-list `:217`'s "the planted corpus is task 6's (IR-31)" is not true at adc3484. Either make it part of G2, or ask task 6 to add it. (2) Its only test uses a mock scripted to fail (`03-stages.md:113`). There is no enforcement control of the TeCh-shaped bundle. (3) Unstated residual: an idea whose recorded description itself bundles EMA and label smoothing passes both the scope check and the floor. Only the critic's rubric, plus U-SUB-2's tuned baseline once task 6 adds it, can catch it. Say this is detection only |
| NEW-5 · prose binds any cell after the test event | **closed** | A number in the text binds only to *ours* or a reference row. Other rows appear only in rendered tables, before the freeze and after the final fill (`06-integrity.md:94`). The planted tail abstract has a twin (`:102`, `:104`) | None. It is stricter than G3 at IR-21.2 (`ai1:27`) and does not contradict it. Task 6 must carry it into G3's mechanism (the requirement depends on A-INT-1) |
| NEW-6 · the floor measures nothing | **closed** | The spread is taken across search seeds, each a separate fit, at admission, on each gate's settings and aggregate. The margin is derived from α given the scorings the loop allows (IR-13.4). A run whose floor cannot be computed does not start (`01-run.md:91`). Test at `:98` | Minor: (a) σ comes from s seeds, so a margin derived from the point estimate gives more than α at small s. Use an upper bound, or rely on R-MEAS-10's α check. (b) "α" collides with task 6's success-test α (`bd:271`); see §3 |
| NEW-7 · the null is empty | **closed** | The null re-draws its randomness, runs through the real loop, and its rate is stated beforehand. An exact copy is refused. The floor-off twin is a guard-off build (IR-38) (`07-measurement.md:98`). Test at `:102` | Minor: the test runs "at one gate". The end-to-end rate that the report prints beside every success rate has no test of its own; R-STG-9's and R-RUN-7's nulls cover two of its gates |
| NEW-8 · failing on purpose | **closed** | Agent-code failures are released and never retried (IR-33.4) (`08-operation.md:62`; `02-primitive.md:121`). Completeness names seeds (`01-run.md:89`). Compute is counted for every attempt (`08-operation.md:65`; `01-run.md:88`). Enforcement test with its twin (`08-operation.md:69`) | Minor wording in R-RUN-2's envelope; see §3 |
| NEW-9 · reporting judge on the authors' family | **closed** | R-OPS-12 states its scope (`08-operation.md:108`). R-MEAS-5 compares the judge with the authors' families, applies IR-29.1's hiding rule, and adds a transfer control with a positive control (`07-measurement.md:56`, `:58`, `:62`). R-INT-7 cites IR-29.3 and IR-29.4 (`06-integrity.md:86`) | Minor: "outside everything any … development session reads" (`07-measurement.md:56`) cannot be enforced in a public repository. Mark it a process rule, as IR-29.5 does |
| NEW-10 · one twin per test | **partly closed** | The rule is in *How to read* (`requirements.md:31`). Twins or positive controls are now in R-INT-1 (`06-integrity.md:26`, `:29`), R-INT-2 (`:38-40`), R-INT-3 (`:50`), R-INT-8 (`:104`), R-OPS-8 (`08-operation.md:78-81`) and R-RUN-2 (`01-run.md:34-36`) | (1) R-INT-3's scan clause (`06-integrity.md:49`) still reports a zero with no positive control. Plant a report value in a critic's prompt and show that the scan finds it. (2) The checker enforces tiers but does not count clauses against twins (NEW-15's ask) |

**The NEW-3 issue: what the revision's guard actually reads.**
- **Only one search seed list exists.** IR-10.2 has two seed lists, search and report. IR-9.3 has "one list per role, shared by all rows" (`ut5:13`; `u4:58`). A search fit given a report seed is refused (`ut5:119`).
- **The "fresh" fit is E_best's record.** C_best's fit at a search seed, with its default job arguments, has the same identity as the fit that produced E_best (IR-32.1, `bd:113`). And "asking again for a released identity returns that record" (IR-33.1, `bd:116`).
- **A new identity would not help.** The same seed gives back the same luck, as task 6 itself says (`ut5:147`).
- **So the guarded arm is my model B's middle row.** That is about 0.515 at 1 SD, not 0.24. The guarded arm and the twin of `03-stages.md:183` are the same computation, so the test cannot produce its stated outcome.

## 2. The four contradictions of check 1

| Contradiction | Status | Evidence |
|---|---|---|
| 1 · R-INT-10 against G3, G4 and G5 | **closed** | After any repair, every check of the hook runs again; at most 2 repairs per invocation (`06-integrity.md:122`). The tail runs its gates on the final version (`01-run.md:106`). The typed-number repair has a twin (`06-integrity.md:129`). This matches IR-39's sketch (`bd:169`) |
| 2 · R-INT-3's test against the sealed check | **closed** | The scan covers only what agents, prompts and manuscripts read. It allows the sealed check, and plants a candidate's report job with a twin (`06-integrity.md:49-50`). The four kinds of report job match IR-14.6 (`ut5:44`) |
| 3 · R-INT-3's first sentence | **closed** | Rewritten to "no value computed on the report role … beyond the pass or fail", with roles and published labels (`06-integrity.md:44`). The reads of the test split are decided in place by task 6, section 7 (`bd:217-227`) |
| 4 · R-STATE-7 at the test event | **closed** | Released identities are reused, and an unreleased one runs again under the same identity, which "is not a second use" (`05-state.md:65`). The test kills the run during the test event and expects one count (`:74`). This matches IR-33.1 and IR-33.3 (`bd:116-118`) |

## 3. IR- citations and task 6 rules stated differently

I checked every IR- citation in the nine files: 85 distinct IDs and sub-IDs. Everything not listed below matches adc3484.

| Where | Defect | Fix |
|---|---|---|
| R-STG-9, `03-stages.md:156`, `:158`, `:183` | Under IR-32.1, IR-33.1 and IR-9.3, the "paired fresh fits" are E_best's released fits (the major in §1, NEW-3) | As in §4 |
| R-STG-3, `03-stages.md:88` | "once per manifest version". IR-15.2 says once per **baseline key**: "another manifest edit … keeps the key and does not repeat the check" (`ut5:47`). Its WHY-NOT names per-manifest counting as the attack (`ut5:110`) | Say "once per baseline key" |
| R-STG-3, `03-stages.md:89`; also `requirements.md:71` | "the roles' index files unchanged across versions" is stricter than IR-15.2, and it blocks the only remedy when IR-10.3 refuses the task for role overlap (`ut5:14`) | "unchanged after the first sealed-check attempt" |
| R-MEAS-7, `07-measurement.md:74`; R-RUN-2, `01-run.md:21` | IR-3.6's flag has no "declared deterministic" exemption (`u4:26`). R-RUN-2 cites IR-9.3 and IR-10.2 for a determinism declaration that neither rule contains | Mark the exemption and the field `[ours]`, with its reason. The ratio test already cannot flag anything when the baseline's variance is 0 |
| R-MEAS-3, `07-measurement.md:40` | It cites IR-39.3 while counting a run that failed after its test event "at no more than that gain". IR-39.3 counts that run as a failure in the failure-inclusive gain and reports its results "only as diagnostics of a failed run" (`bd:189`) | Keep the rule. It is listed as a presumption on U-EVAL-1 (`requirements.md:219`). Cite that, not IR-39.3, and send it to task 6 |
| R-RUN-6 `01-run.md:91`; R-STG-13 `03-stages.md:230`; `requirements.md:116` | "α … default 0.05, ours (IR-7.1)". Task 6 keeps "α and the success test" for its own `P1` part (`bd:271`). These are two different α's | Rename the gate bound, e.g. α_gate, and say it is not task 6's α |
| R-RUN-2, `01-run.md:26`, `:36` | "the harness stops a job that exceeds it, and the row has no result". IR-33.4 makes a timeout against the manifest's limit a released failed result (`bd:119`). "No result" reads as an unreleased identity, which IR-33.3 runs again: a way to re-roll by exceeding the envelope on purpose | "released as failed; the row's aggregate is invalid (IR-33.4, IR-9.4)" |
| fix-list `:217`, behind R-STG-4 and R-INT-10 | "the planted corpus is task 6's (IR-31)", but IR-31.1 does not list the switch-scope check (`ai3:30`) | As in NEW-4 |

## 4. New blocker or major defects introduced by the revision

**ND-1 · major · R-STG-9's guard and its enforcement control cannot work under adc3484 (this is NEW-3's remainder).**
- **The attack:** a null mechanism that changes the random stream, which nearly every real mechanism does, for instance by adding parameters.
  - Its control is an unselected draw. Under IR-33.1 it is compared with the selected E_best record.
  - At the subset veto's margin, the precondition passes in about half of the runs.
  - So R-MEAS-1's third reading reports "attributed" for gains the method did not cause.
- **The evidence:** the rules in the NEW-3 note (§1), and model B's middle row (`evaluation-integrity-engineer-closure-2.md:222`).
- **Would we notice?** Only when task 7 tries to build the guarded arm of `03-stages.md:183`, and finds it is the same computation as its twin.
- **The guard. Either is enough for the reported number:**
  - **(a) No change to task 6.** Compute the third reading from the test event. The mechanism-off control is a frozen row (IR-14.3, `ut5:41`), fitted again at the report seeds (IR-14.4). So *ours* minus the control, paired per report seed, is an unbiased number. The third reading requires that difference to pass a one-sided test registered in advance, the machinery A-EVAL-1 sets. This is measurement after the freeze, not a decision, so IR-17 is not touched. The in-loop precondition stays a search-side filter, and its bias is then stated.
  - **(b) Ask task 6** for search seeds that no veto or selection reads: a third list, or a held-back part of the search list. That needs a change to IR-9.3 and IR-10.2.
- **The control:** the null of `03-stages.md:183`. Under (a), the reported attribution rate is at most α within ±3 SE over at least 100 runs. In the twin that reads the in-loop precondition, it is about 0.5 at a 1 SD margin.

No other new blocker or major. One minor is noted only because it contradicts a decision in the same file:
- R-RUN-8 lets a person end a suspended run "whose outcome is then *abandoned*" outside the rule (`01-run.md:124`).
- `requirements.md:119` (Q-9) says an abandonment follows a rule fixed in advance.
- Runs suspend at every usage window. An abandoned run counts at the failure convention, not at the negative test gain it would have had (R-MEAS-3's cap needs a measured gain). So abandoning on poor search records can raise the failure-inclusive mean.
- Put abandonment under R-RUN-8's rule, with a flag outside it.

## Verdict

**Task 3 can design against these files now, with one contract marked pending.**

What is closed:
- The blocker NEW-1 is closed. It cites IR-14.4 correctly, and its control plants seed-dependent training noise with a twin.
- All four contradictions with task 6 are resolved.
- NEW-5 to NEW-9 are closed, apart from minor remainders.
- No requirement contradicts adc3484 except the identity collision of ND-1. The other citation defects in §3 are wording.

What must change first:
- R-STG-9's ablation precondition, and R-MEAS-1's third reading that depends on it, cannot work under IR-33.1, IR-32.1 and IR-9.3 as written. Task 3 should mark them pending until ND-1 is fixed. Option (a) needs no change to task 6.

What can follow, with no effect on the design:
- Assign an owner and an IR-31 measurement to the switch-scope check (NEW-4).
- Add R-INT-3's positive control for the scan (NEW-10).
- Make the text fixes in §3.

Files:
- `docs/requirements/03-stages.md`
- `docs/requirements/07-measurement.md`
- `docs/requirements/01-run.md`
- `docs/requirements/06-integrity.md`
- `docs/reviews/requirements-2026-10-02/fix-list.md`
