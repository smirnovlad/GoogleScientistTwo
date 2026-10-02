"""Can Tab. 4's S2 ICLR cells (median 2.2, mean 3.8, n=4) be rebuilt from Tab. 16's S2 column?
Known relative deltas in Tab. 16: DMSQD +0.61% mean QD, T-SAE +3.4%. RALI is absolute (+0.006 PLCC,
+0.008 SRCC). Pinet has no single relative number. Solve for the two unknowns."""
import itertools
known = {"DMSQD": 0.61, "T-SAE": 3.4}
sols = []
for rali in [x / 100 for x in range(0, 3001)]:          # 0 .. 30 %
    for pinet in [x / 10 for x in range(-1000, 1001)]:  # -100 .. 100 %
        v = sorted([known["DMSQD"], known["T-SAE"], rali, pinet])
        med = (v[1] + v[2]) / 2
        mean = sum(v) / 4
        if 2.15 <= med < 2.25 and 3.75 <= mean < 3.85:
            sols.append((rali, pinet))
ra = [s[0] for s in sols]; pi = [s[1] for s in sols]
print(f"solutions: {len(sols)}; RALI gain range {min(ra):.2f}-{max(ra):.2f}%; Pinet gain range {min(pi):.1f}-{max(pi):.1f}%")
print("RALI +0.006 PLCC is 1.0% only if the PLCC baseline is ~0.6; +0.008 SRCC is 1.0% if SRCC ~0.8")
# ICML implied mean with plain-mean assumption
lo = (86*25.15 - 33*13.95 - 4*3.85)/49; hi = (86*25.25 - 33*13.85 - 4*3.75)/49
print(f"implied ICML mean {lo:.2f}-{hi:.2f}")
# trimmed mean of Fig 1b without 5 bars >100% (bin midpoints)
print(f"Fig.1b: mean of the 81 bars below 100% at bin midpoints = {1172.5/81:.1f}%; at lower edges {625/81:.1f}%; at upper edges {1720/81:.1f}%")
# Tab.9 compounding under two conventions
print(f"Tab.9 compounded as ratio gains: {100*(1.109*1.096*1.082-1):.1f}%; as time reductions: {100*(1-0.891*0.904*0.918):.1f}% "
      f"(= speedup {1/(0.891*0.904*0.918):.3f})")
# Tab.6 EM ratio with rounding
print(f"Tab.6 EM ratio FCD/Engram: {0.0705/0.0045:.1f}-{0.0715/0.0035:.1f} (printed 17.75)")
# McNemar best case for SAR round1->round2 (36->34), min discordant = 2
from math import comb
p = 2*sum(comb(2,i) for i in range(0,1))/2**2
print(f"Tab.5 SAR 36->34: minimum discordant pairs 2 (b=2,c=0): exact two-sided McNemar p = {min(1,p):.2f}")
# X-Maha: reproduced vs paper baseline share of the claimed gain (p.41 numbers as read by artifacts.md)
print(f"X-Maha FPR95: gain vs reproduced 1.99pp, vs paper 1.58pp -> reproduction shortfall 0.41pp = {100*0.41/1.99:.0f}% of the gain vs reproduction")
# cost per success if failures cost the implementation+refinement share
share = 0.201+0.454
for venue, s, f in [("NeurIPS",33,5),("ICML",49,15),("all",86,21)]:
    print(f"cost per success, {venue}: failures at $0 -> $3765; failures at {share:.3f}x$3765=${share*3765:.0f} -> ${3765 + f*share*3765/s:.0f}; failures at $3765 -> ${3765*(s+f)/s:.0f}")
