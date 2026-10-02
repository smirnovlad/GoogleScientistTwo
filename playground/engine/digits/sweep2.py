# Finer baseline design sweep, VALIDATION only (full and its subset). Test is not read.
import sys, time, warnings
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", message=r".* encountered in matmul", category=RuntimeWarning)
T = sys.argv[1]
tr = np.load(f"{T}/data/public/train.npz"); X, y = tr["X"], tr["y"]
Xf = np.load(f"{T}/harness/inputs/full.npz")["X"]; yf = np.load(f"{T}/harness/labels/full.npz")["y"]
Xs = np.load(f"{T}/harness/inputs/subset.npz")["X"]; ys = np.load(f"{T}/harness/labels/subset.npz")["y"]
seeds = range(20)
print(f"train n={len(y)}, full n={len(yf)}, subset n={len(ys)}, seeds 0..19; sd = sample sd (ddof=1)")
print(f"{'hidden':>6} {'epochs':>6} | {'full mean':>9} {'sd(20)':>7} {'min':>6} {'max':>6} {'sd(0,1,2)':>9} | {'subset mean':>11} {'sd(20)':>7} | {'fit s':>6}")
for h in (16, 32, 64):
    for it in (30, 40, 50, 60, 80, 100):
        af, as_, ts = [], [], []
        for s in seeds:
            t0 = time.perf_counter()
            m = MLPClassifier(hidden_layer_sizes=(h,), max_iter=it, random_state=s).fit(X, y)
            ts.append(time.perf_counter() - t0)
            af.append((m.predict(Xf) == yf).mean()); as_.append((m.predict(Xs) == ys).mean())
        af, as_ = np.array(af), np.array(as_)
        print(f"{h:6d} {it:6d} | {af.mean():9.4f} {af.std(ddof=1):7.4f} {af.min():6.3f} {af.max():6.3f} {af[:3].std(ddof=1):9.4f} | {as_.mean():11.4f} {as_.std(ddof=1):7.4f} | {np.mean(ts):6.3f}")
