"""IR-23.4's audit tolerance, simulated (docs/integrity/decisions/a-int-1-gates-or-audit.md).

Rule under test: for each kind of fit, packaging measures M same-seed difference pairs on a
reference whose seeding is known; s_k^2 = mean(d^2) over the M pairs (M degrees of freedom).
A row with n comparisons (report seeds x settings) is flagged when any |d| > c * s_k, with
c = t_{1-q/2, M} and q = 1 - (1 - alpha)^(1/n) (Sidak). A paired gain uses c * (s_o + s_b).
The t threshold assumes independent, zero-mean Gaussian differences. A pre-registered check on
the M reference differences (no zero, no tie, |skewness| and excess kurtosis within their
Gaussian 99.5% bounds at M) sends a kind that fails it to the empirical path: a comparison is
flagged when |d| exceeds the largest reference |d|, and a flag there makes the row not
verified instead of an I1 failure. Sections F to H test the check.

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
    for rho in (0.0, -1.0, 1.0):
        hits = 0
        for _ in range(R):
            s = s_hat(rng, 1.0, M)
            bad = False
            for _ in range(N_CMP):
                zo = rng.gauss(0, 1)
                zb = rho * zo + math.sqrt(max(0.0, 1 - rho * rho)) * rng.gauss(0, 1)
                if abs(zo - zb) > c * (s + s):
                    bad = True
            hits += bad
        print(f"D' paired gain, both rows of one kind (shared estimate), correlation {rho:+.0f}: flag rate {hits / R:.5f} (target <= {ALPHA})")

    rng = random.Random(20261006)
    old, oldclock = 0, 0
    z = 3.46
    for _ in range(R):
        s = max(0.1, s_hat(rng, 1.0, 2))
        old += flagged(rng, s, z, 1.0)
        s2 = max(0.1, s_hat(rng, 10.0, 2))
        oldclock += flagged(rng, s2, z, 10.0)
    print(f"E the replaced rule (own estimate from c = 2 pairs, floor 0.1, z = 3.46): honest flag rate {old / R:.3f}; clock-seeded detection {oldclock / R:.3f}")


    # The packaging check, its bounds pre-registered by simulation of Gaussian references.
    rng = random.Random(20261007)
    sk, ku = [], []
    for _ in range(100_000):
        a, b = moments([rng.gauss(0, 1) for _ in range(M)])
        sk.append(abs(a)); ku.append(b)
    sk.sort(); ku.sort()
    SK, KU = sk[int(0.995 * len(sk))], ku[int(0.995 * len(ku))]
    print(f"check bounds at M={M}: |skewness| <= {SK:.3f}, excess kurtosis <= {KU:.3f}")

    def run_kind(draw, label, seed, reps=100_000):
        rng = random.Random(seed)
        gauss_path = fail_i1 = not_verified = 0
        for _ in range(reps):
            ref = [draw(rng) for _ in range(M)]
            ok = passes(ref, SK, KU)
            cand = [draw(rng) for _ in range(N_CMP)]
            if ok:
                gauss_path += 1
                s = math.sqrt(sum(d * d for d in ref) / M)
                fail_i1 += any(abs(d) > c * s for d in cand)
            else:
                top = max(abs(d) for d in ref)
                not_verified += any(abs(d) > top for d in cand)
        print(f"{label}: kinds on the t path {gauss_path / reps:.3f}; honest rows failing I1 {fail_i1 / reps:.5f}; honest rows not verified {not_verified / reps:.4f}")

    bern = lambda r: (r.random() < 0.01) - (r.random() < 0.01)
    rng = random.Random(20261008)
    plain = 0
    for _ in range(100_000):
        s = math.sqrt(sum(bern(rng) ** 2 for _ in range(M)) / M)
        plain += any(abs(bern(rng)) > c * s for _ in range(N_CMP))
    print(f"F Bernoulli(0.01) fit disturbances, t rule with no check: honest rows flagged {plain / 100_000:.4f}")
    run_kind(bern, "F' Bernoulli(0.01) disturbances, with the check", 20261009)
    run_kind(lambda r: r.gauss(0, 1), "G Gaussian kind, with the check", 20261010)
    cont = lambda r: r.gauss(0, 1) + (r.gauss(0, 10) if r.random() < 0.01 else 0.0) - (r.gauss(0, 10) if r.random() < 0.01 else 0.0)
    run_kind(cont, "H Gaussian with 1% of fits disturbed at 10x, with the check (residual)", 20261011)


def moments(xs):
    n = len(xs); m = sum(xs) / n
    v = sum((x - m) ** 2 for x in xs) / n
    if v == 0: return 0.0, 0.0
    sk = sum((x - m) ** 3 for x in xs) / n / v ** 1.5
    ku = sum((x - m) ** 4 for x in xs) / n / v ** 2 - 3
    return sk, ku


def passes(ref, SK, KU):
    if any(d == 0 for d in ref) or len({abs(d) for d in ref}) < len(ref):
        return False
    a, b = moments(ref)
    return abs(a) <= SK and b <= KU


if __name__ == "__main__":
    main()
