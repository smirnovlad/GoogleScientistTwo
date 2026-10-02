# Closure check: evaluation-integrity engineer (2026-09-28)

- **Checked:** whether each finding of the integrity reviews EI1 and EI2 is resolved by its fix.
  The documents were claims (`1ea9771`), note-check (`5ac78ea`) and artifacts (`f0823be`), and the
  engine analysis as committed in `23b894e`.
- **Scope:** the reviewer's own findings, plus a scan of all 16 documents for quotes attributed to
  the wrong paper (ScientistOne against ScientistTwo).
- **Record:** the reviewer's final message, verbatim below.

---

# Closure check of EI1 and EI2 (evaluation integrity)

**Checked:** docs/paper as it stands now: commits 1ea9771, 5ac78ea and f0823be, plus the uncommitted analysis.md and stages/. I re-read every `ref:` anchor I cite against `.cache/refs/2605.26340v1`. I wrote nothing to the repository.

## EI1

| Finding | Status | Where it shows | What remains |
|---|---|---|---|
| M1 | RESOLVED in substance | claims.md:252-258; artifacts.md:20, 134, 146, 239, 241; note-check.md:29, 105-108; stages/07:35-44 | errors 1 and 2 below |
| M2 | PARTLY | claims/ablations.md:72; artifacts.md:19, 135 | the summary row, claims.md:28, still says only "internally consistent" |
| M3 | RESOLVED | artifacts.md:21, 99, 196, 249; analysis.md:23; stages/02:83 | nothing |
| M4 | RESOLVED | artifacts.md:24, 104, 268 (A-ART-12) | A-ART-12 is not yet in the decision register |
| M5 | RESOLVED | note-check.md:167, 169 | nothing |
| M6 | RESOLVED | claims.md:214 (and :88) | nothing |
| M7 | RESOLVED | stages/07:24-33; analysis.md:26; note-check.md:70 and A-NOTE-10 | note-check.md:352 still frames A-NOTE-10 as "only measures, or also blocks", while its register row A-INT-1 now decides "a locked harness" (stages/07:59) |
| m1 | RESOLVED | artifacts.md:22, 238 | nothing |
| m2 | RESOLVED | artifacts.md:23, 101-102, 148, 159, 165 | nothing |

## EI2

| Finding | Status | Where it shows | What remains |
|---|---|---|---|
| M1 | RESOLVED | analysis.md:269-290 (the three columns and the "Data and guards" bullet) and :517 (U-TOP-5); a split line in every stage block | U-TOP-5 is not yet in the register; error 3 below |
| M2 | RESOLVED | stages/07:24-33; analysis.md:26 | nothing |
| M3 | RESOLVED | stages/07:35-44, 59, 70; analysis.md:513 | error 1 below; U-INT-4 is not yet in the register |
| M4 | RESOLVED | analysis.md:284-286 | nothing |
| m1, m3 | RESOLVED | stages/07:69, 66 | nothing |
| m2 | RESOLVED | analysis.md:167-168 | nothing |

## Errors the fixes introduced

1. **stages/07-integrity.md:40 cites "[Ref: meng2026scientistone §6.1]"; the section is §6.**
   - ScientistOne's PDF (arXiv 2605.26340v1) prints "6. Experiments". Under it come "Benchmark. … Each task provides a fixed evaluator…" and "We run each evaluator five times…". Only after them does "6.1. CoE Audit Results" begin.
   - The TeX has `\subsection{Setup}` commented out (06a_setup.tex:3).
   - claims.md:254, note-check.md:105-106 and artifacts.md:19 already say §6. Your precision note repeats "§6.1".

2. **The five runs and the max(1%, 3σ/|s̄|) tolerance are ScientistOne's settings for its own benchmark (§6), not part of its audit definition (§5).**
   - The §5 definition says only "within an adaptive tolerance that accounts for evaluator noise" (05_coe_audit.tex:26).
   - stages/07:37, 40 and note-check.md:106 get this right.
   - These places present the §6 settings as the delegated protocol:
     - note-check.md:29 and :383. Line 383 also tags §5 on anchors that are in §6 (06a_setup.tex:10) and App. D (012c:53-57).
     - artifacts.md:239, tagged §5.
     - artifacts.md:134. Of its "departs on four counts", the "one run" count departs from ScientistOne's practice, not its definition. The "no tolerance" count does depart from the definition.
     - claims.md:252 and :254, which put the settings under "the delegated protocol".
   - My EI1-M1 wording caused this. **Fix:** say "in ScientistOne's own runs" and tag it §6.

3. **stages/02-evaluating-ideas.md:30 cites evidence that does not apply.** The subset row cites p. 69's "subset test split". That label belongs to an ablation inside the generated DynaSpec-RAG paper. It says nothing about how §3.2 draws its screening subset.

## Attribution between the two papers

- **Quotes:** no quote is attributed to the wrong paper. I scanned all 16 files:
  - every quoted ScientistOne phrase sits in a sentence tagged `[Ref: meng2026scientistone …]` with a `ref:` anchor;
  - no ScientistTwo quote carries a ScientistOne tag.
- **Untagged ScientistOne statements:** claims.md:258 and stages/07:44 mention ScientistOne's golden evaluator without a tag, but both are marked [ours].
- **Section tags:** the only wrong ones are those in errors 1 and 2.
