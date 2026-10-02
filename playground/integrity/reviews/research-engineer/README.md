# The research-engineer reviewer's checks (wave 1, 2026-10-02)

Written by the `research-engineer` reviewer of `docs/integrity/blocking-decisions.md` at
`a2e7eb0`. Kept verbatim so that the review
(`docs/reviews/integrity-blockers-2026-10-02/research-engineer.md`) can be re-run.

| Script | Shows |
|---|---|
| `null_control.py` | the expected maximum of m null candidates (m = 2 to 40); whether one run of the null-idea control can decide anything; how much training-seed luck the selected row carries from search to report when the same fitted artifact is scored on both (finding B1); the success rule's false-success rate at the null; the planted-corpus sizes behind IR-31; and what carving part of the official test set into search costs in power |
| `costs_and_flags.py` | the F(4,4) quantile behind a seed-spread flag, and the order-of-magnitude compute and money arithmetic of finding M9 |

Each runs with `python3 <script>`, needs nothing outside the standard library, and uses fixed
seeds. `null_control.py` takes about a second.
