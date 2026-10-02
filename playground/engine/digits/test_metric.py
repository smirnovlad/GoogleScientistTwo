import os, pickle, sys
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

T = sys.argv[1]; W = sys.argv[2]
sys.path.insert(0, os.path.join(T, "harness"))
import metric

def save(name, a):
    p = os.path.join(W, name)
    with open(p, "wb") as f: np.save(f, a)
    return p

lab = os.path.join(T, "harness/labels/full.npz")
y = np.load(lab)["y"]; n = len(y)
rng = np.random.RandomState(0)

# 1. values agree with sklearn on several prediction vectors
for name, pred in [("perfect", y.copy()), ("all-zero", np.zeros(n, np.int64)),
                   ("random", rng.randint(0, 10, n)), ("90%-noisy", np.where(rng.rand(n) < 0.9, y, rng.randint(0, 10, n)))]:
    r = metric.score(save(name + ".npy", pred), lab)
    acc, f1 = accuracy_score(y, pred), f1_score(y, pred, average="macro", labels=np.unique(y), zero_division=0)
    ok = abs(r["primary"] - acc) < 1e-12 and abs(r["macro_f1"] - f1) < 1e-12 and r["n"] == n
    print(f"VALUE {name:10s} primary={r['primary']:.6f} sklearn_acc={acc:.6f} macro_f1={r['macro_f1']:.6f} sklearn_f1={f1:.6f} n={r['n']} -> {'AGREE' if ok else 'DISAGREE'}")

# int32 / uint8 predictions are integers too: accepted
for dt in (np.int32, np.uint8):
    r = metric.score(save(f"dt_{dt.__name__}.npy", y.astype(dt)), lab)
    print(f"ACCEPT dtype {dt.__name__}: primary={r['primary']}")

# 2. each malformed input raises ValueError
pk = os.path.join(W, "pickled.npy")
with open(pk, "wb") as f: pickle.dump(list(y), f)
txt = os.path.join(W, "text.npy"); open(txt, "w").write("0 1 2\n")
npz = os.path.join(W, "archive.npy")
with open(npz, "wb") as f: np.savez(f, pred=y)
cases = {
    "missing file": (os.path.join(W, "nope.npy"), lab),
    "wrong length (n-1)": (save("short.npy", y[:-1]), lab),
    "wrong length (n+1)": (save("long.npy", np.append(y, 0)), lab),
    "wrong dtype float64": (save("float.npy", y.astype(np.float64)), lab),
    "wrong dtype bool": (save("bool.npy", y > 4), lab),
    "wrong dtype str": (save("str.npy", y.astype(str)), lab),
    "object array": (save("obj.npy", np.array(list(y), dtype=object)) if False else None, lab),
    "2-D column": (save("col.npy", y.reshape(-1, 1)), lab),
    "label 10": (save("ten.npy", np.where(np.arange(n) == 0, 10, y)), lab),
    "label -1": (save("neg.npy", np.where(np.arange(n) == 0, -1, y)), lab),
    "empty": (save("empty.npy", np.array([], dtype=np.int64)), lab),
    "pickle file": (pk, lab),
    "text file": (txt, lab),
    "npz instead of npy": (npz, lab),
    "labels missing": (save("ok.npy", y), os.path.join(W, "nolabels.npz")),
}
# an object array cannot even be saved without pickle; build it with allow_pickle (np.save default)
op = os.path.join(W, "obj.npy")
with open(op, "wb") as f: np.save(f, np.array(list(y), dtype=object), allow_pickle=True)
cases["object array"] = (op, lab)
raised = 0
for name, (p, l) in cases.items():
    try:
        metric.score(p, l)
        print(f"ERROR-CASE {name:22s} -> NO EXCEPTION (bad)")
    except ValueError as e:
        raised += 1
        print(f"ERROR-CASE {name:22s} -> ValueError: {str(e).replace(W, '<tmp>').replace(T, '<task>')[:150]}")
    except Exception as e:
        print(f"ERROR-CASE {name:22s} -> {type(e).__name__} (NOT ValueError): {e}")
print(f"{raised}/{len(cases)} malformed inputs raised ValueError")
