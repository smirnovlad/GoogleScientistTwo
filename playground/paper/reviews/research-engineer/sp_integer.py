"""Exact check with integer ratings 1..10 (one score per paper), sample SD (n-1), printed values +-0.05.
For each row and threshold t, is there a multiset of n integer ratings with the printed mean, SD and
exactly k ratings >= t?  DP over accepted part and rejected part separately: sum -> bitmask of sumsq."""
import math
rows = [
 ("T2 ScientistOne", 21, 3.8, 1.2, 3), ("T3 human ICLR", 5, 6.8, 1.6, 3),
 ("T3 human NeurIPS", 38, 6.2, 1.9, 25), ("T3 human ICML", 64, 6.9, 1.5, 51),
 ("T3 S2 ICLR", 4, 7.0, 1.2, 4), ("T3 S2 NeurIPS", 33, 7.3, 1.7, 29),
 ("T3 S2 ICML", 49, 7.6, 1.0, 46), ("T3 S2 Overall", 86, 7.5, 1.3, 79),
 ("T5 round 0", 49, 5.2, 2.2, 23), ("T5 round 1", 49, 6.9, 1.6, 39),
 ("T8 Antigravity", 3, 6.3, 1.5, 2),
 # zero-accept rows
 ("T2 AI-Researcher", 7, 1.0, 0.0, 0), ("T2 CycleResearcher", 6, 1.0, 0.0, 0),
 ("T2 AI Scientist-v2", 3, 2.0, 1.0, 0), ("T2 AutoResearchClaw", 4, 2.5, 1.0, 0),
 ("T2 Zochi", 2, 3.0, 0.0, 0), ("T2 DeepScientist", 3, 3.0, 0.0, 0), ("T3 Agent4Science", 4, 3.0, 0.0, 0),
]
def dp(count, lo, hi):
    """achievable (sum -> bitmask of sumsq) for `count` integers in [lo, hi]"""
    cur = {0: 1}
    for _ in range(count):
        nxt = {}
        for s, mask in cur.items():
            for v in range(lo, hi + 1):
                nxt[s + v] = nxt.get(s + v, 0) | (mask << (v * v))
        cur = nxt
    return cur
def feasible(n, m, sd, k, t, sample=True):
    A = dp(k, t, 10) if k else {0: 1}
    R = dp(n - k, 1, t - 1) if n - k else {0: 1}
    if t - 1 < 1 and n - k > 0: return False
    Slo, Shi = math.ceil(n * (m - 0.05) - 1e-9), math.floor(n * (m + 0.05) - 1e-9)
    den = (n - 1) if sample else n
    for sa, ma in A.items():
        for S in range(Slo, Shi + 1):
            sr = S - sa
            if sr not in R: continue
            mr = R[sr]
            vlo, vhi = max(0, sd - 0.05) ** 2, (sd + 0.05) ** 2
            Qlo = S * S / n + den * vlo
            Qhi = S * S / n + den * vhi
            qa = ma
            base = 0
            while qa:
                if qa & 1:
                    lo_i = math.ceil(Qlo - base - 1e-9); hi_i = math.floor(Qhi - base - 1e-9)
                    # need exact rounding: SD rounds to printed sd -> var in [vlo, vhi)
                    for q in range(max(lo_i, 0), hi_i + 1):
                        if (mr >> q) & 1:
                            var = (base + q - S * S / n) / den
                            if vlo - 1e-12 <= var < vhi - 1e-12 or (sd == 0 and var < 1e-12):
                                return True
                qa >>= 1; base += 1
    return False
for sample in (True, False):
    print("== integer ratings,", "sample SD" if sample else "population SD", "==")
    for lab, n, m, sd, k in rows:
        ok = [t for t in range(2, 11) if feasible(n, m, sd, k, t, sample)]
        print(f"  {lab:22s} n={n:3d} k={k:3d}  thresholds t consistent: {ok}")
