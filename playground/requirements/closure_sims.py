"""Simulations behind models A to C of the integrity closure check of the requirements (2026-10-02).

Copied verbatim from docs/reviews/requirements-2026-10-02/evaluation-integrity-engineer-closure-2.md,
appendix, so the numbers there can be re-run: python3 playground/requirements/closure_sims.py
"""
# Closure-check simulations (2026-10-02). Model: true gain 0 for every candidate; each harness scoring
# is a unit-variance draw; E_base is one draw per task; a gate passes when record - reference >= m.
import random, statistics as st
random.seed(12345)
g = random.gauss

def veto(base, m, tries):                     # blocked Good -> Engineer: up to `tries` scorings
    for _ in range(tries):
        x = g(0, 1)
        if x - base >= m:
            return x
    return None

N = 200_000
print("A  null idea, subset veto: pass rate")
for m in (0, 1, 2):
    one = sum(veto(g(0, 1), m, 1) is not None for _ in range(N)) / N
    three = sum(veto(g(0, 1), m, 3) is not None for _ in range(N)) / N
    print(f"   margin {m}: 1 scoring {one:.3f}, up to 3 scorings {three:.3f}  (n={N})")

print("B  ablation precondition for a null idea that passed the full-set veto (ablation margin = veto margin)")
for m in (1, 2):
    a = b = c = n = 0
    while n < 50_000:
        base = g(0, 1); best = veto(base, m, 3)
        if best is None:
            continue
        n += 1
        a += best - base >= m                   # control reproduces E_base exactly (same seeds, same code path)
        b += best - g(0, 1) >= m                # control is an independent fresh draw
        c += g(0, 1) - g(0, 1) >= m             # fresh re-fit of C_best vs fresh control, independent noise
    print(f"   margin {m}: vs E_best, control = E_base {a/n:.3f}; vs E_best, fresh control {b/n:.3f}; "
          f"fresh re-fit vs fresh control {c/n:.3f}  (n={n})")

print("C  20 null candidates, winner chosen on search, scored on report with the same fitted artifact")
for sf in (1.0, 0.0):
    s, r = [], []
    for _ in range(20_000):
        cands = [(g(0, sf), g(0, 1), g(0, 1)) for _ in range(20)]   # (fit noise, search eval, report eval)
        f, es, er = max(cands, key=lambda c: c[0] + c[1])
        s.append(f + es); r.append(f + er)
    print(f"   fit sd {sf}, eval sd 1: search gain {st.mean(s):.2f}, report gain {st.mean(r):.2f}  (n=20000)")
