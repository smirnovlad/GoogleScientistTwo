"""The arithmetic behind docs/paper/claims.md: every consistency check on the paper's numbers.

Each input is a number printed in arXiv:2609.19644v1; its table, figure or section is named beside it.
Numbers read from figure images (Figs. 9 and 10) are marked (image). Nothing here is estimated from
outside the paper, except where a line says "assumption".

Usage: python3 playground/paper/claims_arithmetic.py
"""

import itertools
import math
import statistics as st


def section(title):
    print(f"\n== {title} ==")


def k_for(rate, n):
    """Every count k whose k/n rounds to the printed percentage."""
    return [k for k in range(n + 1) if round(100 * k / n, 1) == rate]


section("Rates against their n (Tabs. 2, 3, 5, 8; Fig. 1 caption)")
for label, n, rate in [
    ("Tab.2 ScientistOne ScholarPeer", 21, 14.3),
    ("Tab.3 human ICLR 2026 (both reviewers)", 5, 60.0),
    ("Tab.3 human NeurIPS 2025 ScholarPeer", 38, 65.8), ("Tab.3 human NeurIPS 2025 Stanford", 38, 76.3),
    ("Tab.3 human ICML 2026 ScholarPeer", 64, 79.7), ("Tab.3 human ICML 2026 Stanford", 64, 96.9),
    ("Tab.3 S2 ICLR ScholarPeer", 4, 100.0), ("Tab.3 S2 ICLR Stanford", 4, 75.0),
    ("Tab.3 S2 NeurIPS ScholarPeer", 33, 87.9), ("Tab.3 S2 NeurIPS Stanford", 33, 75.8),
    ("Tab.3 S2 ICML ScholarPeer (= Tab.5 round 2)", 49, 93.9), ("Tab.3 S2 ICML Stanford (= Tab.5 round 2)", 49, 69.4),
    ("Tab.3 S2 Overall ScholarPeer", 86, 91.9), ("Tab.3 S2 Overall Stanford", 86, 72.1),
    ("Tab.5 round 0 ScholarPeer", 49, 46.9), ("Tab.5 round 0 Stanford", 49, 49.0),
    ("Tab.5 round 1 ScholarPeer", 49, 79.6), ("Tab.5 round 1 Stanford", 49, 73.5),
    ("Tab.8 Claude Code SR", 5, 80.0), ("Tab.8 Antigravity SR", 5, 60.0),
    ("Tab.8 Antigravity acceptance (both)", 3, 66.7), ("Fig.1 caption success", 107, 80.4),
]:
    print(f"  {label:45s} {rate:5.1f}% of {n:3d} -> k = {k_for(rate, n)}")
print("  Overall accepted = venue sum? ScholarPeer 4+29+46 =", 4 + 29 + 46, "; Stanford 3+25+34 =", 3 + 25 + 34)
print("  Human papers accepted by each reviewer (Tab.3): ScholarPeer 3+25+51 =", 3 + 25 + 51,
      f"of 107 = {100 * 79 / 107:.1f}%; Stanford 3+29+62 =", 3 + 29 + 62, f"of 107 = {100 * 94 / 107:.1f}%")
print(f"  S2 Stanford acceptances per input task: 62/107 = {100 * 62 / 107:.1f}%")

section("Weighted averages across the venue rows (Tab. 3)")
for name, w, vals in [("S2 ScholarPeer rating", [4, 33, 49], [7.0, 7.3, 7.6]),
                      ("S2 Stanford rating", [4, 33, 49], [5.4, 5.6, 5.7]),
                      ("human ScholarPeer rating", [5, 38, 64], [6.8, 6.2, 6.9]),
                      ("human Stanford rating", [5, 38, 64], [5.2, 5.5, 6.1])]:
    n = sum(w)
    nom = sum(a * b for a, b in zip(w, vals)) / n
    lo = sum(a * (b - 0.05) for a, b in zip(w, vals)) / n
    hi = sum(a * (b + 0.05) for a, b in zip(w, vals)) / n
    print(f"  {name:26s} n={n:3d} nominal {nom:.3f}  (rounding range {lo:.3f}-{hi:.3f})")

section("Pooled SD of the S2 Overall row from the venue rows (Tab. 3; population SDs assumed)")
for name, sds, means, overall in [("ScholarPeer", [1.2, 1.7, 1.0], [7.0, 7.3, 7.6], 7.457),
                                  ("Stanford", [0.2, 0.7, 0.6], [5.4, 5.6, 5.7], 5.648)]:
    w = [4, 33, 49]
    var = sum(n * (s ** 2 + (m - overall) ** 2) for n, s, m in zip(w, sds, means)) / 86
    print(f"  {name}: pooled SD {math.sqrt(var):.2f}")

section("Can ScholarPeer 'Accept' mean a rating >= 8 (the in-loop threshold of §3.5)?")
for label, n, k, mean, sd in [("Tab.3 ICML / Tab.5 round 2", 49, 46, 7.6, 1.0), ("Tab.3 Overall", 86, 79, 7.5, 1.3)]:
    best = None
    for m in (mean - 0.05, mean, mean + 0.0499):
        x = (n * m - 8 * k) / (n - k)          # accepted papers all at exactly 8, rejected ones all at x
        if x >= 1:
            sd_min = math.sqrt((k * (8 - m) ** 2 + (n - k) * (x - m) ** 2) / n)
            best = sd_min if best is None else min(best, sd_min)
    print(f"  {label}: smallest possible (population) SD {best:.2f}; printed SD {sd} (so below {sd + 0.05:.2f})")

section("Which ratings reproduce Tab.2 AI Scientist-v2 ScholarPeer 2.0 +/- 1.0 (n=3)?")
for name, scale in [("integers 1..10", range(1, 11)),
                    ("assumption: ICLR score set {1,3,5,6,8,10}", [1, 3, 5, 6, 8, 10])]:
    fits = [(t, round(st.stdev(t), 2), round(st.pstdev(t), 2))
            for t in itertools.combinations_with_replacement(scale, 3) if round(sum(t) / 3, 1) == 2.0]
    print(f"  {name}: (triple, sample SD, population SD) = {fits}")

section("Relative gain: Tab. 4 decomposed, and Fig. 9a (image)")
nom = (86 * 25.2 - 33 * 13.9 - 4 * 3.8) / 49
lo = (86 * 25.15 - 33 * 13.95 - 4 * 3.85) / 49
hi = (86 * 25.25 - 33 * 13.85 - 4 * 3.75) / 49
print(f"  implied ICML mean gain (n=49): {nom:.2f}% (rounding range {lo:.2f}-{hi:.2f}); Fig. 9a final round: 33.4% (image)")
print(f"  25.2% over 86 successes = {25.2 * 86 / 107:.1f}% over all 107 tasks if a failure counts as 0%")
fig9a = [20.6, 30.8, 32.4, 32.8, 33.4]
print("  Fig.9a increments", [round(b - a, 1) for a, b in zip(fig9a, fig9a[1:])], "total", round(fig9a[-1] - fig9a[0], 1))

section("AutoSOTA's ICLR column of Tab. 4 from its per-paper deltas in Tab. 16")
four = {"Pinet (latency -16.7%, as a gain)": 16.7, "DMSQD": 7.3, "T-SAE": 2.25, "RALI": 2.68}
print(f"  four papers without TeCh: mean {st.mean(four.values()):.2f}, median {st.median(four.values()):.2f}  (Tab.4: 7.2 / 5.0)")
five = list(four.values()) + [4.45]
print(f"  all five: mean {st.mean(five):.2f}, median {st.median(five):.2f}")
print(f"  TeCh 0.8806/0.8431 = +{100 * (0.8806 / 0.8431 - 1):.2f}%; RALI 0.8012/0.7803 = +{100 * (0.8012 / 0.7803 - 1):.2f}%;"
      f" emitters 20/15 = +{100 * (20 / 15 - 1):.1f}%; T-SAE re-evaluation 0.7557/0.7586 = {100 * (0.7557 / 0.7586 - 1):.2f}%")

section("Fig. 9b (image)")
n = [14, 16, 12, 3, 4]
evolved = [0, 0.875, 0.75, 0.667, 0.5]
e = [round(a * b) for a, b in zip(n, evolved)]
print(f"  tasks {sum(n)}; evolved per round {e} = {sum(e)} ({100 * sum(e) / 49:.1f}%); seed {49 - sum(e)} ({100 * (49 - sum(e)) / 49:.1f}%)")
print(f"  best idea from Initial or Round 1: {14 + 16}/49 = {100 * 30 / 49:.1f}%; evolved after Initial: {sum(e)}/35 = {100 * sum(e) / 35:.1f}%")

section("Fig. 10 (image)")
hist = [6, 11, 5, 5, 4, 2]
print(f"  tasks {sum(hist)}; shares {[round(100 * k / 33, 1) for k in hist]}; 2.51 d = {2.51 * 24:.1f} h")
print(f"  mean from bin midpoints (>=5 d taken as 6 d): {(6 * .5 + 11 * 1.5 + 5 * 2.5 + 5 * 3.5 + 4 * 4.5 + 2 * 6) / 33:.2f} d;"
      f" lowest possible mean {(11 * 1 + 5 * 2 + 5 * 3 + 4 * 4 + 2 * 5) / 33:.2f} d")
time = {"Seed Idea Generation": 0.6, "Initial Implements": 19.0, "Idea Refinement": 44.9,
        "Ablation Studies": 16.4, "Initial Drafting": 3.6, "Peer&Meta-Review": 15.5}
cost = {"Seed Idea Generation": 0.3, "Initial Implements": 20.1, "Idea Refinement": 45.4,
        "Ablation Studies": 15.4, "Initial Drafting": 3.1, "Peer&Meta-Review": 15.8}
print(f"  time shares sum {sum(time.values()):.1f}; cost shares sum {sum(cost.values()):.1f}")
print(f"  Idea Refinement + Peer&Meta-Review time {time['Idea Refinement'] + time['Peer&Meta-Review']:.1f}%;"
      f" Initial Implements + Idea Refinement time {time['Initial Implements'] + time['Idea Refinement']:.1f}%,"
      f" cost {cost['Initial Implements'] + cost['Idea Refinement']:.1f}%")
print("  dollars per stage at $3765:", {k: round(3765 * v / 100) for k, v in cost.items()})

section("Single cases (Fig. 2, Tabs. 6, 7, 9, 11)")
print(f"  Fig.2 embedded paper: speedup 1.123x -> time reduction {100 * (1 - 1 / 1.123):.2f}% "
      f"(range {100 * (1 - 1 / 1.1225):.2f}-{100 * (1 - 1 / 1.1235):.2f}); throughput gain 12.3%")
print(f"  Tab.9 compounded over the human baseline: {100 * (1.109 * 1.096 * 1.082 - 1):.1f}%")
print(f"  Tab.6 Overall: FCD-Engram +{100 * (0.916 / 0.705 - 1):.1f}%, LFR-Engram +{100 * (0.897 / 0.705 - 1):.1f}%;"
      f" EM (lower is better) FCD 0.071 vs Engram 0.004 = {71 / 4:.2f}x")
print(f"  Tab.7 references: 1840-1817 = {1840 - 1817}; 1817-1814 = {1817 - 1814}; per paper {1840 / 50:.1f}")
t11 = {
    "DynaSpec-RAG": [(.3467, .3627), (.2399, .2970), (.2803, .3090), (.1428, .2219), (.1397, .1749), (.1135, .2059), (.0615, .1704)],
    "TS-RAG": [(.3557, .3624), (.2451, .2982), (.2906, .3114), (.1466, .2231), (.1454, .1771), (.1120, .2002), (.0627, .1718)],
    "Chronos-Bolt B": [(.3616, .3650), (.2517, .2992), (.3109, .3185), (.1487, .2236), (.1525, .1825), (.1132, .2004), (.0673, .1780)],
    "MOMENT": [(.3920, .4110), (.2742, .3327), (.3506, .3834), (.1703, .2579), (.1801, .2384), (.1967, .3028), (.0979, .2059)],
    "TTM B": [(.3619, .3710), (.2531, .3032), (.3152, .3248), (.1511, .2405), (.1543, .1893), (.1715, .2643), (.0657, .1725)],
    "Moirai B": [(.3686, .3835), (.2547, .3053), (.5399, .4322), (.1958, .2687), (.1711, .1912), (.1832, .2814), (.0663, .1720)],
    "TimesFM": [(.4254, .3825), (.2894, .3233), (.3321, .3326), (.1703, .2552), None, None, (.0695, .1802)],
    "Chronos B": [(.4217, .3806), (.2659, .3136), (.3935, .3695), (.1663, .2522), (.1897, .2107), (.1460, .2237), (.0831, .1879)],
}
printed = {"DynaSpec-RAG": (.1892, .2488), "TS-RAG": (.1940, .2492), "Chronos-Bolt B": (.2008, .2525), "MOMENT": (.2374, .3046),
           "TTM B": (.2104, .2665), "Moirai B": (.2542, .2906), "TimesFM": (.2573, .2948), "Chronos B": (.2380, .2769)}
for model, rows in t11.items():
    rr = [r for r in rows if r]
    mse, mae = st.mean(r[0] for r in rr), st.mean(r[1] for r in rr)
    ok = abs(mse - printed[model][0]) < 5e-5 and abs(mae - printed[model][1]) < 5e-5
    print(f"  Tab.11 {model:15s} over {len(rr)} datasets: {mse:.4f} / {mae:.4f}  printed {printed[model]}  {'ok' if ok else 'MISMATCH'}")
datasets = ["ETTh1", "ETTh2", "ETTm1", "ETTm2", "Weather", "Electricity", "Exchange"]
for i, d in enumerate(datasets):
    for j, metric in enumerate(("MSE", "MAE")):
        best = min((rows[i][j], m) for m, rows in t11.items() if rows[i])
        if best[1] != "DynaSpec-RAG":
            print(f"  Tab.11 DynaSpec-RAG not best on {d} {metric}: {best[1]} {best[0]} vs {t11['DynaSpec-RAG'][i][j]}")
print(f"  Tab.11 average gain over TS-RAG: MSE {100 * (1 - .1892 / .1940):.2f}%, MAE {100 * (1 - .2488 / .2492):.2f}%")

section("Other numbers cited in docs/paper/claims")
print(f"  success per venue (Tab.3): ICLR {100 * 4 / 5:.1f}%, NeurIPS {100 * 33 / 38:.1f}%, ICML {100 * 49 / 64:.1f}%")
print(f"  audit coverage (Tab.7 vs Tab.3): 49 of 86 successes = {100 * 49 / 86:.0f}%")
print(f"  stage share gap, time vs cost (Fig.10b, image): max {max(abs(time[k] - cost[k]) for k in time):.1f} points")


def welch(m1, s1, n1, m2, s2, n2):
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    return se, (m1 - m2) / se


for label, a, b in [("Tab.3 SAR NeurIPS, S2 vs human", (5.6, 0.7, 33), (5.5, 0.7, 38)),
                    ("Tab.3 SAR ICLR, S2 vs human", (5.4, 0.2, 4), (5.2, 0.7, 5)),
                    ("Tab.5 round 0 vs ScientistOne, SP", (5.2, 2.2, 49), (3.8, 1.2, 21)),
                    ("Tab.5 round 0 vs ScientistOne, SAR", (5.6, 0.5, 49), (4.1, 0.7, 21))]:
    se, t = welch(*a, *b)
    print(f"  Welch {label}: difference {a[0] - b[0]:.1f}, SE {se:.2f}, ratio {t:.1f}")

section("Fig. 1b bins (image; counts from playground/paper/fig1b_bars.py) against the 25.2% mean")
bins = {"0-10": (52, 0, 10), "10-25": (15, 10, 25), "25-50": (10, 25, 50), "50-75": (3, 50, 75), "75-100": (1, 75, 100)}
below = sum(n * (lo + hi) / 2 for n, lo, hi in bins.values())
n_below = sum(n for n, _, _ in bins.values())
print(f"  {n_below} bars below 100% at bin midpoints sum to {below:.1f} points; 25.2 x 86 = {25.2 * 86:.1f}")
print(f"  so the 5 bars above 100% must average {(25.2 * 86 - below) / 5:.0f}%")

# ---- Checks added after the persona review (docs/reviews/paper-analysis-2026-09-27/fix-list.md) ----
import contextlib
import io
import runpy
from pathlib import Path

REVIEW = Path(__file__).resolve().parent / "reviews/research-engineer"
SP_ROWS = [("Tab.2 ScientistOne", 21, 3.8, 1.2, 3), ("Tab.3 human ICLR", 5, 6.8, 1.6, 3),
           ("Tab.3 human NeurIPS", 38, 6.2, 1.9, 25), ("Tab.3 human ICML", 64, 6.9, 1.5, 51),
           ("Tab.3 S2 ICLR (= Tab.8 Claude Code)", 4, 7.0, 1.2, 4), ("Tab.3 S2 NeurIPS", 33, 7.3, 1.7, 29),
           ("Tab.3 S2 ICML (= Tab.5 round 2)", 49, 7.6, 1.0, 46), ("Tab.3 S2 Overall", 86, 7.5, 1.3, 79),
           ("Tab.5 round 0", 49, 5.2, 2.2, 23), ("Tab.5 round 1", 49, 6.9, 1.6, 39), ("Tab.8 Antigravity", 3, 6.3, 1.5, 2)]


def min_sd_accept_at(t, n, m, k):
    """Smallest population SD of n ratings in [1, 10] with mean m and exactly k ratings >= t (m < t):
    accepted ratings sit at t, the others share one value. None if the mean cannot be reached."""
    if k == n:
        return None
    x = (n * m - k * t) / (n - k)
    return None if x < 1 else math.sqrt((k * (t - m) ** 2 + (n - k) * (x - m) ** 2) / n)


section("F-CL-1: 'accept <=> rating >= 8' against all 11 ScholarPeer rows with acceptances")
# The bound is the infimum over the printed mean's rounding interval, reached at its upper limit; the
# sample SD (ddof = 1) of the same ratings is the population SD times sqrt(n / (n - 1)).
ruled = {"population": 0, "sample": 0}
for label, n, mean, sd, k in SP_ROWS:
    pops = [s for s in (min_sd_accept_at(8, n, m, k) for m in (mean - 0.05, mean + 0.05)) if s is not None]
    if not pops:
        for convention in ruled:
            ruled[convention] += 1
        print(f"  {label:36s} impossible: {k} of {n} accepted at >= 8 needs a mean >= 8, printed {mean}")
        continue
    pop = min(pops)
    bounds = (("population", pop), ("sample", pop * math.sqrt(n / (n - 1))))
    limit = sd + 0.05
    for convention, value in bounds:
        ruled[convention] += value >= limit
    margins = {c: v - limit for c, v in bounds}
    if label == "Tab.3 S2 NeurIPS":
        edge = margins
    shown = ", ".join(f"{c} {v:.4f} {'rules out' if v >= limit else 'allows'}" for c, v in bounds)
    print(f"  {label:36s} smallest SD: {shown}; printed {sd}, so below {limit:.2f}")
print(f"  rows that rule out '>= 8': population SD {ruled['population']} of {len(SP_ROWS)}, "
      f"sample SD {ruled['sample']} of {len(SP_ROWS)}")
print(f"  knife edge: S2 NeurIPS rules it out by {edge['population']:.4f} under the population SD, "
      f"by {edge['sample']:.4f} under the sample SD")
with contextlib.redirect_stdout(io.StringIO()):          # the reviewer's script prints on import
    sp = runpy.run_path(str(REVIEW / "sp_integer.py"))
for sample in (True, False):
    fits = [{t for t in range(2, 11) if sp["feasible"](n, m, sd, k, t, sample)} for _, n, m, sd, k in SP_ROWS]
    none = [r[0] for r in sp["rows"] if not any(sp["feasible"](r[1], r[2], r[3], r[4], t, sample) for t in range(2, 11))]
    print(f"  one integer rating per paper, {'sample' if sample else 'population'} SD: thresholds fitting all 11 rows "
          f"{sorted(set.intersection(*fits))}; rows (of {len(sp['rows'])}) with no integer solution: {none}")

section("F-CL-3: Tab. 4's S2 ICLR cells (median 2.2, mean 3.8, n = 4) from Tab. 16's printed gains")
known = [0.61, 3.4]              # DMSQD mean QD and T-SAE, the two S2 gains Tab. 16 prints as relative gains
pairs = []
for i in range(0, 3001):         # the two unprinted gains (RALI, Pinet), smaller one first, in 0.01% steps
    for j in range(max(i, 1099 - i), min(3000, 1139 - i) + 1):
        v = sorted(known + [i / 100, j / 100])
        if 2.15 <= (v[1] + v[2]) / 2 < 2.25 and 3.75 <= sum(v) / 4 < 3.85:
            pairs.append((i / 100, j / 100))
small, large = [p[0] for p in pairs], [p[1] for p in pairs]
print(f"  the unprinted gains must be {min(small):.2f}-{max(small):.2f}% and {min(large):.2f}-{max(large):.2f}%")
rali = (100 * 0.0055 / 0.7803, 100 * 0.0065 / 0.7803)   # RALI's PLCC +0.006 on AutoSOTA's printed 0.7803
print(f"  RALI's printed PLCC gain is {rali[0]:.2f}-{rali[1]:.2f}%, outside that range: with Pinet above 3.4 the "
      f"median is {(rali[0] + 3.4) / 2:.2f}-{(rali[1] + 3.4) / 2:.2f}, not 2.2, so no Pinet value fits")
print("  Pinet's printed S2 results: RS lower on 3/4 (up to -69%), CV 4e-4 -> 2e-14, training 3.0x faster")

section("F-CL-5, F-CL-7, F-CL-8, F-CL-9, F-CL-10")
print(f"  Tab.5 SAR round 1 -> 2, 36 -> 34 of 49: exact two-sided McNemar p for discordant pairs (b, c) = "
      + ", ".join(f"({b},{c}) {min(1, 2 * sum(math.comb(b + c, i) for i in range(c + 1)) / 2 ** (b + c)):.3f}"
                  for b, c in ((2, 0), (3, 1), (4, 2))))
print(f"  Fig.10b residual for Seed Idea Generation from the five large labels: time {100 - 99.4:.1f}%, "
      f"cost {100 - 99.8:.1f}%; its printed labels, 0.6% and 0.3% (image, fig10_seed_labels.py), sum to 100.0 and 100.1")
print(f"  Tab.6 EM, FCD-Engram vs Engram: +{0.071 - 0.004:.3f} absolute; the ratio lies in "
      f"{0.0705 / 0.0045:.1f}-{0.0715 / 0.0035:.1f} within rounding")
print(f"  Tab.9 chain: as ratio gains {100 * (1.109 * 1.096 * 1.082 - 1):.1f}%; as time reductions "
      f"{100 * (1 - 0.891 * 0.904 * 0.918):.1f}% (a {1 / (0.891 * 0.904 * 0.918):.2f}x speedup)")
auroc = (100 * (99.56 / 99.30 - 1), 100 * (99.56 / 99.16 - 1))
fpr = (100 * (1 - 2.17 / 3.76), 100 * (1 - 2.17 / 4.17))
print(f"  p.41 (image): AUROC gain +{auroc[0]:.2f}% (vs paper) to +{auroc[1]:.2f}% (vs reproduced); relative FPR95 "
      f"{fpr[0]:.1f}% to {fpr[1]:.1f}%; smallest ratio of the two rules {fpr[0] / auroc[1]:.0f}-fold")
