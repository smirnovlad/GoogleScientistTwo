"""F-quantile for a seed-spread flag, and order-of-magnitude compute arithmetic. Fixed seed."""
import random, math
rng=random.Random(7)
def chi2(k): return sum(rng.gauss(0,1)**2 for _ in range(k))
N=400000; k=4
r=sorted((chi2(k)/k)/(chi2(k)/k) for _ in range(N))
q01=r[int(0.01*N)]
print(f"F(4,4) 1% quantile ~ {q01:.4f}  (1/15.977 = {1/15.977:.4f}); SD-ratio threshold ~ {math.sqrt(q01):.3f}")

fit_h=30.6/60  # App. D draft, self-reported, n=1 [p. 62]
print(f"\nfit time {fit_h:.2f} h (n=1, self-reported, unaudited)")
sessions=104   # analysis.md sec. 9 ceiling at N_p=6, N_t=3, N_0=2
for seeds in (1,5):
    print(f"search fits, ceiling {sessions} units x {seeds} seed(s): {sessions*seeds*fit_h:.1f} A100-h")
rows=10        # ours, baseline, 6 ablations, tuned-baseline control, 1 rebuttal row
for reruns in (1,5):
    print(f"I1 re-fits: {rows} rows x 5 seeds x {reruns} re-run(s): {rows*5*reruns*fit_h:.1f} A100-h; doc's figure: 2 rows x 5 = {2*5*fit_h:.1f}")
print(f"test event re-fit (proposed): {rows-1} rows x 5 seeds: {(rows-1)*5*fit_h:.1f} A100-h")
print(f"p.51 rebuttal alone: 50 datasets x 5 seeds = {50*5} fit+eval jobs per re-run")
per_run=3765   # USD, mean over 33 successful NeurIPS 2025 runs [sec. 4.3]
for n in (1,3,5): print(f"IR-18 at the paper's mean: {n} run(s)/task = ${n*per_run:,}")
print(f"planted corpus: 194 items x 5 votes = {194*5} calls per check and configuration; x 7 LLM checks x 3 configurations = {194*5*7*3:,}")
