# The research-engineer reviewer's checks (wave 1, 2026-09-27)

Written by the `research-engineer` reviewer to check `docs/paper/claims.md` independently of
`playground/paper/claims_arithmetic.py`. Kept verbatim so that the review
(`docs/reviews/paper-analysis-2026-09-27/research-engineer.md`) can be re-run.

| Script | Shows |
|---|---|
| `sp_threshold.py` | which acceptance thresholds each ScholarPeer row of Tabs. 2, 3, 5 and 8 allows, for continuous ratings |
| `sp_integer.py` | the same for one integer rating per paper: with the sample SD, only "accept if rating ≥ 6" fits all 11 rows with acceptances |
| `s2_iclr.py` | that Tab. 4's ICLR cells for ScientistTwo cannot be rebuilt from Tab. 16, plus several smaller checks |

Each runs with `python3 <script>` and needs nothing outside the standard library.
