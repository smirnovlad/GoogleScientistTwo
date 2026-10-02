# Review: agent-engineer, wave 2 (2026-09-27)

- **Reviewed:** `docs/paper/analysis.md` §4.2, §7 and §8, `stages/*.md`, and `artifacts.md`, at
  commit `13477a0`.
- **Lens:** agents as contracts (prompt, output schema, model route, inputs, success test), judged
  by behaviour on traces.
- **Record:** the reviewer's final message, verbatim below.

---

# Review: TODO task 1 analysis, agent-contract lens, 2026-09-27

**Verdict.** The roster, the verdict sets and the split between LLM judgements and numeric tests are correct. The analysis is not yet enough for task 3, though. It records what each agent is, but never how an agent behaved, and behaviour is what golden sets and success tests are built from. There is no BLOCKER.

**Where each question is answered.** Q1: right, with m1–m2. Q2: the table below; the LLM/numeric split is right. Q3: M2–M6. Q4: the table's last column. Q5: the Routing section at the end.

**What is right**
- **Names and merges (analysis.md §7, §7.1):**
  - A_Coder is recorded as a composite.
  - App. A.2's "Idea Critic Agent" is read as the Subset Critic, marked [inferred].
  - The Ablation Critic is kept separate from the Ablation Study Agent.
  - The split between coding and reasoning agents holds.
- **§1.1 item 2 (every gate is an LLM reading) is right,** and the paper says it outright, so it can move from [ours] to SPECIFIED: "ScientistTwo has no target metric" [Tab. 15] (tex:sections/appendix.tex:176). The review threshold is numeric only after an LLM has produced the score.

## MAJOR

**M1 · analysis.md §7: the roster has no success-evidence field.** It gives four of the five contract fields (inputs, outputs, verdicts, model) and leaves out success evidence.
- Evidence: the paper tests agents only through end-to-end ablations:
  - the Rebuttal Agent [Tab. 5];
  - the Meta-Review Agent, n = 1 [Tab. 6];
  - the integrity agents [Tab. 7];
  - the coding backend [Tab. 8];
  - the Selector and Evolver: "Evolved Idea Selected: 27" of 49 [Fig. 9b] (image).
- No rate of any §3 verdict is reported anywhere.
- Fix: add the column, and a U-TOP item "no per-agent success criterion".

**M2 · stages/04-ablation.md: the Ablation Critic has no criterion item** (the other critics have U-SUB-1, U-SEL-1 and U-META-2). It is the gate that decides what counts as a contribution, and the paper's worked cases conflict.
- The rule is that ScientistTwo "requires the gain to be attributable to the proposed mechanism" [Tab. 15].
- TeCh was rejected because "the gains were primarily driven by general training controls" [App. B] (tex:sections/appendix.tex:222-224).
- On p. 46 none of the five components works as designed: "The performance actually relies heavily on X-Maha's trace-variance factor rather than HSKP itself" [p. 46].
- Yet that idea was refined (Refine is inferred, A-ART-1), not rejected. Every component was changed and one was removed [p. 40] (image).
- So the same failure met opposite verdicts [ours].
- Fix: add U-ABL-5, the boundary between Refine and reject, pinned by three cases: TeCh, LC-FTT and p. 46.

**M3 · artifacts.md A-ART-4 misattributes a case.** "an earlier variant was rejected by our own critic as statistically inert" [Tab. 16] (tex:sections/appendix.tex:324-325) names no critic, and a subset `Bad` fits it equally well. It also shows a critic claiming significance, while the runs shown use `seed=0` [p. 40] (image).
- Fix: file it as its own item, with the owner unknown.

**M4 · artifacts.md P-ART-3 misses a self-contradiction.**
- The component table on p. 41 gives these 6-set averages: 99.16/4.17 (X-Maha) → 99.07/4.28 → 99.02/4.48 → 99.56/2.17.
- Two of the three additions make the average worse; they help only on CIFAR-10.
- The report still says "Every component contributes", "directly rebutting" the critic [p. 41] (image).
- It is the only case in the paper that prints both an agent's claim and its full evidence, which makes it the best test for a sycophantic critic.
- Fix: record it, and make it golden case 1.

**M5 · analysis.md §7 and §4.2 have no map of judge family against author family.** App. A.2's "Gemini 3.6 Flash for all agents, except…" [App. A.2] puts author and judge in one family at several gates:
- the Idea Generator and the Novelty Checker;
- the Ablation Critic and the Result Comparison Agent, which judges a refinement its own family asked for;
- the §4.2 audits, which use "the Coding Agent", the same backend that wrote the code (A-INT-3).

ScholarPeer's backbone is not stated (U-PEER-3).
- Fix: add a table with the columns decision, author family, judge family, independence required, and swap-family control.

**M6 · The threshold of 8 and "reviewer independence".** analysis.md §6 P-CFG-9 says "none: A.2 fixes the example value", and §7.2 is headed "Reviewer independence, SPECIFIED".
- 8 is a point on ScholarPeer's own scale, where accepted human papers average 6.2–6.9 [Tab. 3].
- In round 2, ScholarPeer's accept rate rises from 79.6 to 93.9 while the held-out reviewer's falls from 73.5 to 69.4 [Tab. 5].
- claims.md already holds this (C-ABLX-4, A-EVAL-3), but stages/05 and §7 do not.
- Fix: mark the threshold as dependent on the reviewer and calibrate it; retitle §7.2 "ScholarPeer is not independent"; link C-ABLX-4.

## MINOR

- **m1 · The §7 "Model" column merges backend and model.** Reading 1 of A-CFG-1 puts agents that run code on "Gemini 3.6 Flash" with no harness named. The paper's only Gemini harness is Antigravity, in one 5-task experiment [§4.2] [Tab. 8].
  - Fix: split the column into backend and model.
- **m2 · A-CFG-1 misses evidence.**
  - Figure 3's *Ablation Study Agent* box holds the *Planning Agent*, and the ablation stage's *New Idea* re-enters the *Full-Set Experiment Agent* [Fig. 3] (image).
  - artifacts.md P-ART-3 asserts Claude Code for A_FullEng, which analysis.md leaves undetermined.
  - P-ROSTER-17 and P-ROSTER-23 cite App. A.2 without [inferred].
- **m3 · Input bounds.** Only A_Evolve's input has a bound item (U-EVO-2). But:
  - the Selector receives every C^h through Eq. 4 [§3.3, Eq. 4];
  - the Ablation Critic read implementation detail ("forcing the practical implementation" [p. 46]).
  - Fix: add input-bound items for both.
- **m4 · Judges are labelled "coding"** (P-ROSTER-26, P-ROSTER-28), and nothing makes them read-only. The p. 47 auditor saved `repro_check.json` inside the task it audited [p. 47].

## Contracts

| Agent | What the paper gives | What we must define | Test: seed → expected decision |
|---|---|---|---|
| Limitation Verifier | set → confirm or insufficient; at most 16 rounds | criterion, schema, what happens at the limit (A-LIM-1) | sets with planted omissions → insufficient |
| Novelty Checker | idea + 2 papers → score | scale, query, independence from the generator | G's own method re-proposed → lowest score |
| Subset Critic | E_sub vs E_base → Bad, Good or Engineer, plus r | margin, seeds, fail closed on a malformed verdict | single-seed ties → not Good; a confusion matrix weighted by cost |
| Full-Set Critic | a terminal Good or Bad | reference (A-FULL-1), rule for trade-offs | LFR-Engram: Overall 0.705→0.897 but EM↓ 0.004→0.084 [Tab. 6] → flag |
| Selector | the Good tuples → h_best | criterion, a ranking for fallback, input bound | dominance pairs; input order swapped → same pick |
| Ablation Critic | E_abl → Good or Refine; a reject in [App. B] | the Refine/reject boundary (M2) | TeCh → not Good; LC-FTT → Refine, naming the components to strip [Tab. 16]; p. 41 → breakdown not clean |
| Result Comparison | E_new vs E_best → keep or not | strictness rule; an "incomparable" verdict | FCD-Engram vs LFR-Engram, better on all six metrics → keep; different scopes → incomparable |
| ScholarPeer | P → strengths, weaknesses, questions, score 1–10 | which reviewer; a calibrated threshold | the 107 accepted input papers vs Tab. 3's means; Tab. 2's AI papers (7 scored 1.0) → reject |
| Meta-Reviewer | P and R → Accept or Refine | criterion; it sees no results | DynaSpec-RAG draft: "strict do-no-harm fall-back" [p. 57] vs "2/7" datasets regressing [p. 70] → flag |
| Spec filter, auditors | keep or discard; a report | task rules, tolerance, independence | AutoSOTA's T-SAE evaluation-harness edit → discard [Tab. 16]; baseline not audited [p. 47] → fail |
| Reference checker | flags | how a reference is resolved | every DynaSpec-RAG reference resolved; Tab. 7 claims 0/1814 hallucinated |
| Coders, planners, writers | symbols only; four groups on Claude Code | backend and model, session resume, write scope | TABHARMONY: "real and backbone-transferable" at 4/24/2 [p. 51] → no claim of a classification gain |

## Routing

**Settled by rule, not by measurement:**
- the judge we report is never the in-loop reviewer;
- an auditor's model family differs from the coder's.

**Settled by measurement:**
- the planners' backends (π and ρ, two sessions per pass, analysis.md §9);
- the coding models, by baseline reproduction success per dollar;
- whether a Flash-class model is good enough for the expensive gates (the Ablation Critic, Result Comparison, and a meta-review Refine), judged from their confusion matrices on the golden sets.

A-CFG-2 does not matter.
