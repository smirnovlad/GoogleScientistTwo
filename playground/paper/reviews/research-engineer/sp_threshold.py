"""Independent re-check: which acceptance thresholds t (accept <=> rating >= t) are consistent with
each ScholarPeer row of Tabs. 2, 3, 5, 8, given printed mean, SD (+-0.05 rounding) and accept rate.

Part A: continuous ratings in [1,10] (no integer assumption). Min population SD for accept<=>r>=t:
 accepted k values >= t, rejected n-k values in [1, t) -- closed form lower bound when mean < t.
Part B: integer ratings 1..10, exact DP, sample or population SD.
"""
import math
rows = [  # label, n, mean, sd, k_accepted
 ("T2 ScientistOne", 21, 3.8, 1.2, 3),
 ("T3 human ICLR", 5, 6.8, 1.6, 3),
 ("T3 human NeurIPS", 38, 6.2, 1.9, 25),
 ("T3 human ICML", 64, 6.9, 1.5, 51),
 ("T3 S2 ICLR (=T8 CC)", 4, 7.0, 1.2, 4),
 ("T3 S2 NeurIPS", 33, 7.3, 1.7, 29),
 ("T3 S2 ICML (=T5 r2)", 49, 7.6, 1.0, 46),
 ("T3 S2 Overall", 86, 7.5, 1.3, 79),
 ("T5 round 0", 49, 5.2, 2.2, 23),
 ("T5 round 1", 49, 6.9, 1.6, 39),
 ("T8 Antigravity", 3, 6.3, 1.5, 2),
]
print("== Part A: continuous ratings; min population SD if accept <=> rating >= t ==")
for t in (6, 7, 8):
    print(f" t = {t}")
    for lab, n, m, sd, k in rows:
        # min variance: accepted at max(t, .), rejected at min(<t, .); with mean m.
        best = None
        for mm in [m - 0.05 + i * 0.001 for i in range(100)]:
            # all accepted equal a >= t, all rejected equal r in [1, t]; k a + (n-k) r = n mm
            # minimize k(a-mm)^2 + (n-k)(r-mm)^2 over a>=t, r<=t, r>=1
            cands = []
            if k == n:
                a = mm
                if a >= t: cands.append(0.0)
                else: cands.append(None)
            elif k == 0:
                r = mm
                cands.append(0.0 if r <= t else None)
            else:
                # unconstrained optimum a=r=mm; if mm >= t, set r = t (boundary) ... solve generally
                for a in [t + i * 0.01 for i in range(0, 901)]:
                    r = (n * mm - k * a) / (n - k)
                    if 1 <= r <= t:
                        cands.append((k * (a - mm) ** 2 + (n - k) * (r - mm) ** 2) / n)
            cands = [c for c in cands if c is not None]
            if cands:
                v = min(cands)
                best = v if best is None else min(best, v)
        if best is None:
            print(f"   {lab:22s} INFEASIBLE (mean cannot be reached)")
        else:
            s = math.sqrt(best)
            flag = "CONTRADICTS" if s >= sd + 0.05 else "ok"
            print(f"   {lab:22s} min pop SD {s:5.2f} vs printed {sd} (<{sd+0.05:.2f})  {flag}")
