"""IR-23.4's audit tolerance, simulated (docs/integrity/decisions/a-int-1-gates-or-audit.md).

Rule under test: for each kind of fit, packaging measures M same-seed difference pairs on a
reference whose seeding is known; s_k^2 = mean(d^2) over the M pairs (M degrees of freedom).
A row with n comparisons (report seeds x settings) is flagged when any |d| > c * s_k, with
c = t_{1-q/2, M} and q = 1 - (1 - alpha)^(1/n) (Sidak). A paired gain uses c * (s_o + s_b).

Standard library only, fixed seeds. Run: python3 playground/integrity/audit_tolerance.py
"""
import math
import random

ALPHA, N_CMP, M = 0.0027, 5, 20


def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-300 else 1e-300
        de = d * c; h *= de
        if abs(de - 1) < 1e-12:
            break
    return h


def betai(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * betacf(b, a, 1 - x) / b


def t_two_sided_tail(t, df):
    return betai(df / 2, 0.5, df / (df + t * t))


def t_quantile(p_two_sided, df):
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_two_sided_tail(mid, df) > p_two_sided: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def s_hat(rng, sigma, m):
    return math.sqrt(sum(rng.gauss(0, sigma) ** 2 for _ in range(m)) / m)


def flagged(rng, s, c, tau, n=N_CMP):
    return any(abs(rng.gauss(0, tau)) > c * s for _ in range(n))


def main():
    q = 1 - (1 - ALPHA) ** (1 / N_CMP)
    c = t_quantile(q, M)
    print(f"alpha={ALPHA} n={N_CMP} M={M}: per-comparison q={q:.6f}, c=t(1-q/2,{M})={c:.3f}")

    rng = random.Random(20261002)
    R = 200_000
    honest = sum(flagged(rng, s_hat(rng, 1.0, M), c, 1.0) for _ in range(R)) / R
    print(f"A honest row, own packaging estimate, {R} rows: flag rate {honest:.5f} (target <= {ALPHA})")

    rng = random.Random(20261003)
    tasks, counts = 20_000, []
    for _ in range(tasks):
        s = s_hat(rng, 1.0, M)
        counts.append(sum(flagged(rng, s, c, 1.0) for _ in range(100)))
    for b in (2, 4, 5, 6, 8):
        print(f"B 100 honest rows sharing one estimate, {tasks} tasks: P(count > {b}) = {sum(k > b for k in counts) / tasks:.4f}")

    rng = random.Random(20261004)
    for tau in (5.0, 10.0):
        det = sum(flagged(rng, s_hat(rng, 1.0, M), c, tau) for _ in range(R)) / R
        p95 = sum(math.comb(100, k) * det ** k * (1 - det) ** (100 - k) for k in range(95, 101))
        print(f"C clock-seeded row, same-seed SD {tau:.0f}x the floor: detection {det:.4f}; P(>= 95 of 100) = {p95:.4f}")

    rng = random.Random(20261005)
    for rho in (0.0, -1.0, 1.0):
        hits = 0
        for _ in range(R):
            so, sb = s_hat(rng, 1.0, M), s_hat(rng, 1.0, M)
            bad = False
            for _ in range(N_CMP):
                zo = rng.gauss(0, 1)
                zb = rho * zo + math.sqrt(max(0.0, 1 - rho * rho)) * rng.gauss(0, 1)
                if abs(zo - zb) > c * (so + sb):
                    bad = True
            hits += bad
        print(f"D paired gain, correlation {rho:+.0f}: flag rate {hits / R:.5f} (target <= {ALPHA})")

    rng = random.Random(20261006)
    old, oldclock = 0, 0
    z = 3.46
    for _ in range(R):
        s = max(0.1, s_hat(rng, 1.0, 2))
        old += flagged(rng, s, z, 1.0)
        s2 = max(0.1, s_hat(rng, 10.0, 2))
        oldclock += flagged(rng, s2, z, 10.0)
    print(f"E the replaced rule (own estimate from c = 2 pairs, floor 0.1, z = 3.46): honest flag rate {old / R:.3f}; clock-seeded detection {oldclock / R:.3f}")


if __name__ == "__main__":
    main()
