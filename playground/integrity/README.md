# Scripts behind the integrity decisions

Each script backs a claim in `docs/integrity/`. Each runs with `python3 <script>`, needs nothing
outside the standard library, and uses fixed seeds.

| Script | Backs |
|---|---|
| `audit_tolerance.py` | IR-23.4's finite-sample tolerance for I1, and its control: the flag rate of honest rows, the detection of clock-seeded randomness, and paired gains under any correlation. Written by the owner for the second Codex pass, 2026-10-02; about 12 seconds |
| `reviews/research-engineer/` | the research-engineer reviewer's checks, kept verbatim: the null-idea control and training-seed luck (B1), cost arithmetic, and the closure's checks |
