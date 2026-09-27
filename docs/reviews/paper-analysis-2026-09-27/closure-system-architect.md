# Closure check: system-architect (2026-09-28)

- **Checked:** whether each of the system-architect's findings is resolved by its fix, in the
  engine analysis as committed in `23b894e` (the reviewer compared the working tree with
  `3be24ad`).
- **Scope:** the reviewer's own findings only, and the two points the orchestrator raised, which
  the reviewer was asked to confirm or reject.
- **Record:** the reviewer's final message, verbatim below.

---

**Closure check of my findings.** B1 is only partly resolved; every other fix is resolved. Your two points both hold, and the fixes introduced two new errors. Line numbers (l.) refer to `docs/paper/analysis.md` in the working tree, compared against commit 3be24ad.

| Finding → fix | Status | Where it shows | What remains |
|---|---|---|---|
| B1 → F-AN-0 | PARTLY | §3.3 l.113, 117; §3.4 l.119–135; §3.5 l.137–142 | points (a) and (b); l.100 still calls evolution a "SPECIFIED deviation" |
| B1 → F-AN-21 | RESOLVED | U-TOP-7 l.521–523; l.134; l.450 | U-TOP-7 is not yet in the decision register (l.521 says so) |
| M1 → F-AN-22 | RESOLVED | §8 l.433–459; README l.176 adds the `STATE` key | none |
| M2 → F-AN-1 | RESOLVED | l.19, 278, 288 | new error 1 below |
| m1 → F-AN-23 | RESOLVED | l.174, 177 | none |
| m2 → F-AN-24 | RESOLVED | l.251 | §3.5 contradicts it; see (a) |
| m3 → F-AN-25 | RESOLVED | l.84 | none |
| m4 → F-AN-26 | RESOLVED | l.251, 265 | new error 2 below |
| m5 → F-AN-27 | RESOLVED | l.339 | none |

**Your two points**

- **(a) Confirmed, and it goes further than you stated.**
  - l.140 says "the subset row takes exactly" Listing 1's values, and one of those is "a limit that counts critic calls". But §3.4's subset cell counts "engineering refinements, N_eng = 2" (l.128), and §4 does the same (l.251).
  - The same cell treats what the critic judges (E_sub^h) as separate from what gets refined (h and C_sub^h). l.140 says the opposite: "the judged object equal to the refined one". In the paper, the engineer "refines h and C_sub^h" and produces new results (tex:sections/3_new_method.tex:45).
  - The "exact fit" claim also appears at l.18, l.98 and l.109 ("Exact fit, SPECIFIED").
  - Fix: say the subset row keeps Listing 1's verdicts and its discard at the limit, but counts differently (A-TOP-2). Mark the comparison [ours].
- **(b) Confirmed.** l.18 opens "Read this first" with the conclusion §3.3 now withdraws, and it repeats the "exactly" claim.
  - Fix: say Listing 1 is one setting of the parameters, that most stages keep their candidate at the limit (A-TOP-1), and point to §3.4–3.5.

**Errors the fixes introduced**

1. **l.19**: "The only fixed numeric test is ScholarPeer's score against 8". The old text also listed the loop counters, and this sentence drops them.
   - The stop at S successes is also a fixed numeric test: the idea rounds end once the count of Good ideas reaches S (paraphrase, tex:sections/3_new_method.tex:85).
   - The analysis's own §4.2 row says "a counter … ≥ S, or k = K" (l.275).
2. **l.251**: "Figure 3 routes its *New Idea* back through the full-set critic" applies this to both uses of A_FullEng, but Figure 3 does not.
   - In Figure 3 (image), only the ablation-stage refiner (in the Analyzer box) sends its idea back to the full-set critic.
   - The Meta-Review Agent's *Idea Refiner* sends its idea into the ablation stage instead. l.265 states this correctly.
3. **Point (a) itself**, which is new text in §3.5.

**Does §3.4 give task 3 item 1?** In structure, yes. Its columns are the full parameter set, and l.142 makes each listed open question a per-stage setting rather than code. Four cells are still missing:
- U-ABL-4 is named at l.142 but appears in no row.
- U-EVO-1 is likewise named at l.142 but appears in no row.
- The evolution row's "rounds after round 0, K = 4" (l.130) settles A-EVO-2 without citing it.
- A-TOP-2 is tagged on only two of the six loops that have limits (l.125, l.128), although its own entry applies it to all six (l.502).

Once those cells are tagged and (a) is corrected, task 3 can design the primitive from §3.4 alone.
