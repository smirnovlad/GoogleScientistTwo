import sys, warnings
import numpy as np
T = sys.argv[1]
X = np.load(f"{T}/data/public/train.npz")["X"]
rng = np.random.RandomState(0)

# 1. minimal: finite operands, plain matmul, shapes as in the MLP forward pass
def flags(a, b):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        r = a @ b
    ref = np.einsum("ij,jk->ik", a, b, optimize=False)   # numpy's own loop, no BLAS
    return [str(x.message) for x in w], bool(np.isfinite(r).all()), float(np.abs(r - ref).max())
for (m, k, n) in [(200, 64, 16), (79, 64, 16), (200, 16, 10), (1079, 64, 16), (359, 64, 16), (64, 64, 64), (8, 8, 8)]:
    a = X[:m, :k] if k == 64 else rng.rand(m, k); b = rng.uniform(-0.27, 0.27, (k, n))
    msgs, fin, err = flags(np.ascontiguousarray(a), b)
    print(f"matmul {m}x{k} @ {k}x{n}: warnings={len(msgs)} {sorted(set(msgs))} finite={fin} max|BLAS-einsum|={err:.2e}")

# 2. does any warning coincide with a non-finite operand or result during MLP training?
from sklearn.utils import extmath
import sklearn.neural_network._multilayer_perceptron as mlp
orig = extmath.safe_sparse_dot
stats = {"calls": 0, "flagged": 0, "nonfinite_in": 0, "nonfinite_out": 0, "max_err": 0.0}
def checked(a, b, *, dense_output=False):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        r = orig(a, b, dense_output=dense_output)
    stats["calls"] += 1
    if w:
        stats["flagged"] += 1
    if not (np.isfinite(a).all() and np.isfinite(b).all()): stats["nonfinite_in"] += 1
    if not np.isfinite(r).all(): stats["nonfinite_out"] += 1
    ref = np.einsum("ij,jk->ik", np.asarray(a), np.asarray(b), optimize=False) if np.ndim(b) == 2 else np.asarray(a) @ np.asarray(b)
    stats["max_err"] = max(stats["max_err"], float(np.abs(r - ref).max()))
    return r
mlp.safe_sparse_dot = checked
from sklearn.neural_network import MLPClassifier
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)
y = np.load(f"{T}/data/public/train.npz")["y"]
for h, it in [(16, 50), (32, 100)]:
    for k in stats: stats[k] = 0 if k != "max_err" else 0.0
    m = MLPClassifier(hidden_layer_sizes=(h,), max_iter=it, random_state=0).fit(X, y)
    fin = all(np.isfinite(c).all() for c in m.coefs_ + m.intercepts_)
    print(f"MLP h={h} epochs={it}: {stats}  params finite={fin}  final loss={m.loss_:.4f}")
