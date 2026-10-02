"""The digits task's metric. LOCKED: part of the evaluation harness.

    score(predictions_path, labels_path)
        -> {"primary": accuracy, "n": rows, "n_correct": rows right, "macro_f1": float}

predictions_path  a .npy file holding a 1-D integer array: one label in 0..9 per row
                  of the split's inputs, in the inputs' row order.
labels_path       the split's labels: an .npz holding a 1-D integer array "y".

accuracy is n_correct / n. macro_f1 is the unweighted mean, over the classes present
in the labels, of each class's F1 = 2 TP / (2 TP + FP + FN).

Every malformed input raises ValueError with its reason: a missing or unreadable file,
an archive instead of an array, a wrong dtype, shape or length, a label outside 0..9.

Command line: python metric.py PREDICTIONS.npy LABELS.npz   (prints the result as JSON)
"""
import json
import os
import sys

import numpy as np

CLASSES = tuple(range(10))


def _load_array(path, what, key=None):
    """Load one array without executing anything the file holds.

    ⛔ WHY NOT allow_pickle=True: the prediction file is written by agent code, and
    unpickling it would run that code inside the harness.
    mmap_mode="r" reads the header first, so a huge or truncated file is rejected by
    its shape before its data is read.
    """
    path = os.fspath(path)
    if not os.path.isfile(path):
        raise ValueError(f"{what} file not found: {path}")
    try:
        loaded = np.load(path, allow_pickle=False, mmap_mode=None if key else "r")
    except Exception as e:  # numpy raises several types for a malformed file
        raise ValueError(f"{what} file {path} is not a readable numpy file: {e}") from e
    if key is None:
        if not isinstance(loaded, np.ndarray):
            loaded.close()
            raise ValueError(f"{what} file {path} is an .npz archive; expected a .npy array")
        return loaded
    if isinstance(loaded, np.ndarray):
        raise ValueError(f"{what} file {path} is a .npy array; expected an .npz holding {key!r}")
    with loaded:
        if key not in loaded.files:
            raise ValueError(f"{what} file {path} holds {loaded.files}; expected {key!r}")
        return loaded[key]


def _as_labels(a, what, n=None):
    """Check a label array (1-D, integer, values in CLASSES, length n) and return it as int64."""
    if not np.issubdtype(a.dtype, np.integer):
        raise ValueError(f"{what} must be an integer array; got dtype {a.dtype}")
    if a.ndim != 1:
        raise ValueError(f"{what} must be 1-D, one label per row; got shape {a.shape}")
    if n is not None and a.shape[0] != n:
        raise ValueError(f"{what} has {a.shape[0]} rows; the split has {n}")
    if a.shape[0] == 0:
        raise ValueError(f"{what} is empty")
    bad = (a < CLASSES[0]) | (a > CLASSES[-1])
    if bad.any():
        raise ValueError(f"{what} holds {int(bad.sum())} value(s) outside "
                         f"{CLASSES[0]}..{CLASSES[-1]}, e.g. {np.unique(a[bad])[:5].tolist()}")
    return np.array(a, dtype=np.int64)


def score(predictions_path, labels_path):
    y = _as_labels(_load_array(labels_path, "labels", key="y"), "labels")
    pred = _as_labels(_load_array(predictions_path, "predictions"), "predictions", n=y.shape[0])
    n = int(y.shape[0])
    n_correct = int((pred == y).sum())
    f1 = []
    for c in np.unique(y):
        tp = int(((pred == c) & (y == c)).sum())
        fp = int(((pred == c) & (y != c)).sum())
        fn = int(((pred != c) & (y == c)).sum())
        f1.append(2 * tp / (2 * tp + fp + fn))  # c occurs in y, so the denominator is >= 1
    return {"primary": n_correct / n, "n": n, "n_correct": n_correct,
            "macro_f1": float(np.mean(f1))}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python metric.py PREDICTIONS.npy LABELS.npz")
    try:
        print(json.dumps(score(sys.argv[1], sys.argv[2])))
    except ValueError as e:
        print(f"ValueError: {e}", file=sys.stderr)
        sys.exit(2)
