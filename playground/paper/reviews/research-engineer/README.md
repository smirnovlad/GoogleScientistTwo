# The research-engineer reviewer's checks (wave 1, 2026-09-27)

Written by the `research-engineer` reviewer to check `docs/paper/claims.md` independently of
`playground/paper/claims_arithmetic.py`. Kept verbatim so that the review
(`docs/reviews/paper-analysis-2026-09-27/research-engineer.md`) can be re-run.

| Script | Shows |
|---|---|
| `sp_threshold.py` | which acceptance thresholds a lower bound on the SD rules out, for each ScholarPeer row of Tabs. 2, 3, 5 and 8, with continuous ratings. A threshold it does not rule out may still be infeasible, so it shows only what is excluded; `sp_integer.py` decides feasibility |
| `sp_integer.py` | the same for one integer rating per paper: with the sample SD, only "accept if rating ≥ 6" fits all 11 rows with acceptances |
| `s2_iclr.py` | that Tab. 4's ICLR cells for ScientistTwo cannot be rebuilt from Tab. 16, plus several smaller checks |

Each runs with `python3 <script>` and needs nothing outside the standard library.

**One edit since the review (2026-09-28).** `sp_threshold.py` labelled a row "ok" when its minimum SD stayed below the printed one. The Codex review of the branch showed that this overclaims: S2's ICLR row passes the bound at a threshold of 7, yet four ratings of at least 7 with a mean of 7.0 must all be 7, an SD of 0 against a printed 1.2. The label now reads "not ruled out by this bound". No other line changed, and no conclusion in `docs/paper/` rests on the old label: the claims cite this script only for the rows it rules out at a threshold of 8.
