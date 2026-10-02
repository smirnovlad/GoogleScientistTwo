# Closure check: agent-engineer (2026-09-28)

- **Checked:** whether each of the agent-engineer's findings is resolved by its fix. The engine
  analysis was checked in the working tree, identical to commit `23b894e`; artifacts.md at
  `f0823be`.
- **Scope:** the reviewer's own findings only, not a new review.
- **Record:** the reviewer's final message, verbatim below.

---

# Closure check: agent-engineer findings, 2026-09-28

I checked each fix in the working tree. The analysis.md and stages/* fixes are still uncommitted; artifacts.md is at `f0823be`. F-AR-1 adds new numbers from p. 44, and they are right: the trace-only row is 99.52/2.46 against 99.56/2.17 for the full method. I wrote nothing to the repository.

| Finding → fix | Status | Shown at | What remains |
|---|---|---|---|
| M1 → F-AN-4 | RESOLVED | analysis.md:351, :382, :520 | errors 2–4 |
| M2 → F-AN-5 | RESOLVED | stages/04-ablation.md:54-58 | none |
| M3 → F-AR-9 | RESOLVED | artifacts.md:245, :260, :269 | analysis.md still uses the RALI case as evidence (error 6) |
| M4 → F-AR-1 | RESOLVED | artifacts.md:23, :101-102, :113, :228 | none |
| M5 → F-AN-6 | PARTLY | analysis.md:420-431 | row 2 (error 1) |
| M6 → F-AN-7 | RESOLVED | analysis.md:336, :418; stages/05-drafting-peer-review.md:36, :46 | error 7 |
| m1, m2 → F-AN-8, F-AR-10 | RESOLVED | analysis.md:351, :369, :375, :527-528; artifacts.md:93, :219 | none |
| m3 → F-AN-9 | RESOLVED | stages/03-refining-ideas.md:63; stages/04-ablation.md:59 | none |
| m4 → F-AN-10, F-AR-11 | RESOLVED | analysis.md:378, :380, :383; artifacts.md:130, :151 | none |
| §1.1 item 2 → F-AN-1 | PARTLY | analysis.md:19, :288 | errors 5–6 |

Also remaining: U-TOP-6, U-ABL-5, U-ABL-6, U-SEL-2 and A-ART-13 are not yet in unspecified.md or traceability.md. Each carries a "not yet indexed" mark.

## Errors the fixes introduced

1. **analysis.md:427, the §7.3 table, row 2, marks independence "met already: two families".** That silently takes reading 2 of A-CFG-1. After an `Engineer` verdict, the code the critic reads is written by the engineering agent, which "refines h and" the code [§3.2] (tex:sections/3_new_method.tex:45). App. A.2 never names that agent (tex:sections/appendix.tex:155). Fix: write "met under A-CFG-1's reading 2 only".
2. **analysis.md:370, P-ROSTER-18, says "one verdict is reported".** It leaves out LC-FTT: "The ablation critic stripped … down to the lone component that carried the gain" [Tab. 16] (tex:sections/appendix.tex:291-292). stages/04:57 counts that case.
3. **analysis.md:365, P-ROSTER-13, gives A_Coder the success rate from Table 8.** Table 8 reports the whole pipeline's success after "we replace Claude Code with Antigravity" [§4.2] (tex:sections/4_experiment.tex:46) [Tab. 8].
4. **analysis.md:371, P-ROSTER-19, "one reported keep", needs [inferred].** The paper says only that FCD-Engram "consistently outperforms LFR-Engram" [§4.2] (tex:sections/4_experiment.tex:38), and never names the Result Comparison Agent there.
5. **analysis.md:19 says "The only fixed numeric test is ScholarPeer's score".** Row :275 of the same file lists the counter test on S and K [§3.3] (tex:sections/3_new_method.tex:84-85).
6. **analysis.md:19 and :288 cite "statistically inert" [Tab. 16] (tex:sections/appendix.tex:324-325) as showing that the numbers include statistics.** It shows only a critic's judgement, and A-ART-13 notes that no page shows a statistical test. Better evidence: the reported spreads "+0.61%±0.27" (tex:sections/appendix.tex:288) and "+3.4%±0.2" (tex:sections/appendix.tex:311).
7. **analysis.md:336, P-CFG-9, states claims.md's "≥ 6" as fact.** claims.md marks it [inferred] and says the argument fails if ScholarPeer averages several reviews [Tab. 3]. P-CFG-9 also cites C-ABLX-4 for it, but C-ABLX-4 is the round-2 divergence [Tab. 5].
