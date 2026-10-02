#!/usr/bin/env python3
"""Regenerate the digits task's data/ and harness/ files, deterministically.

Source: scikit-learn's bundled copy of the test set of the UCI "Optical
Recognition of Handwritten Digits" data (sklearn.datasets.load_digits):
1797 images of 8x8 pixels, integer values 0..16, 10 classes. No network.

Splits, drawn per class with one fixed seed (SPLIT_SEED):

  train   60 % of each class    data/public/train.npz       X, y
  full    20 % of each class    harness/inputs/full.npz      X   (the validation split)
                                harness/labels/full.npz      y
  test    20 % of each class    harness/inputs/test.npz      X
                                harness/labels/test.npz      y
  subset  40 % of each class    harness/inputs/subset.npz    X   (a sample of full)
          of full               harness/labels/subset.npz    y

X is float64 (n x 64), y is int64. Each split's rows are in a random order.

Usage:
  python prepare.py           write every file, then check it against EXPECTED
  python prepare.py --check   check the existing files only, writing nothing

Exit status: 0 when every array matches EXPECTED, 1 otherwise.
"""
import argparse
import hashlib
import os
import sys

import numpy as np
from sklearn.datasets import load_digits

HERE = os.path.dirname(os.path.abspath(__file__))

SPLIT_SEED = 2026
N_CLASSES = 10
# Shares as exact fractions (numerator, denominator), rounded half up per class.
TEST_SHARE = (1, 5)     # 20 % of each class
FULL_SHARE = (1, 5)     # 20 % of each class; train keeps the remaining 60 %
SUBSET_SHARE = (2, 5)   # 40 % of each class of the full (validation) split

# File -> the arrays it holds. Inputs never hold labels; labels never hold inputs.
LAYOUT = {
    "data/public/train.npz": ("X", "y"),
    "harness/inputs/subset.npz": ("X",),
    "harness/labels/subset.npz": ("y",),
    "harness/inputs/full.npz": ("X",),
    "harness/labels/full.npz": ("y",),
    "harness/inputs/test.npz": ("X",),
    "harness/labels/test.npz": ("y",),
}

# Content sha256 (dtype, shape and bytes, see content_sha256) of every array this
# script writes, recorded on 2026-10-02 with numpy 2.2.6 and scikit-learn 1.7.1.
# A mismatch means the task's data changed: the source data, the split, or a library.
EXPECTED = {
    "data/public/train.npz:X": "e8b69cfdd035609ece3e3d4fe1eb51cc7bbc5dacf46709b48a4bd0a375516417",
    "data/public/train.npz:y": "6e377fb542374310d48d139e7242808c7e58ec217b8ee025bfd261e53a9d6867",
    "harness/inputs/subset.npz:X": "77a03f265e5576337673d3fabb6af1a245ed2e78cc044900d44a1516688df651",
    "harness/labels/subset.npz:y": "9f4f53205ce06c898de0290ff478dabef6ed9e5d82135707c5c4658b7dac1963",
    "harness/inputs/full.npz:X": "ded0f0a6aebd685ad5c4ad49f3f3c0c983cf3c09b93fcd9303d43f3e3f6a5071",
    "harness/labels/full.npz:y": "820c503b872e3a97e86a8c6db7d1c8cc03e306a20dd00409dbc917d37d2a5284",
    "harness/inputs/test.npz:X": "cc5c84def7b9320a2796f1dda095ee9228411e7cd433eac2aef972d27df29072",
    "harness/labels/test.npz:y": "a4302304916a6e2d3982f86ee14777b7b992ea9b5fbda220e98b0ddfe4f7c6cc",
}


def share(n, fraction):
    """n * num / den rounded half up, in integer arithmetic."""
    num, den = fraction
    return (2 * n * num + den) // (2 * den)


def content_sha256(a):
    """sha256 of an array's dtype, shape and C-order bytes: the data, not its file."""
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(f"{a.dtype.str}|{a.shape}|".encode())
    h.update(a.tobytes())
    return h.hexdigest()


def split_indices(y, rng):
    """Row indices of each split, drawn per class; every split's rows shuffled."""
    train, full, test = [], [], []
    for c in range(N_CLASSES):
        idx = rng.permutation(np.flatnonzero(y == c))
        n_test, n_full = share(len(idx), TEST_SHARE), share(len(idx), FULL_SHARE)
        test.append(idx[:n_test])
        full.append(idx[n_test:n_test + n_full])
        train.append(idx[n_test + n_full:])
    subset = [rng.permutation(f)[:share(len(f), SUBSET_SHARE)] for f in full]
    # ⛔ WHY NOT keep the source order: load_digits' labels run partly in sequence
    # (0, 1, ..., 9, 0, 1, ...), so a row's position would leak its label.
    splits = {}
    for name, parts in (("train", train), ("full", full), ("test", test), ("subset", subset)):
        splits[name] = rng.permutation(np.concatenate(parts))
    return splits


def write_npz(rel, **arrays):
    """Write an uncompressed .npz atomically: a crash leaves the old file or the new one."""
    path = os.path.join(HERE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:  # a file object: np.savez appends no extension
        np.savez(f, **arrays)
    os.replace(tmp, path)


def build():
    digits = load_digits()
    X = np.asarray(digits.data, dtype=np.float64)
    y = np.asarray(digits.target, dtype=np.int64)
    # ⛔ WHY NOT sklearn's train_test_split: its internals may change between versions;
    # numpy's legacy RandomState stream is frozen, and this split is short enough to read.
    splits = split_indices(y, np.random.RandomState(SPLIT_SEED))

    disjoint = np.concatenate([splits["train"], splits["full"], splits["test"]])
    assert np.array_equal(np.sort(disjoint), np.arange(len(y))), "train/full/test must partition the data"
    assert np.isin(splits["subset"], splits["full"]).all(), "subset must lie inside full"

    train = splits["train"]
    write_npz("data/public/train.npz", X=X[train], y=y[train])
    for name in ("subset", "full", "test"):
        idx = splits[name]
        write_npz(f"harness/inputs/{name}.npz", X=X[idx])
        write_npz(f"harness/labels/{name}.npz", y=y[idx])
    for name in ("train", "full", "subset", "test"):
        counts = np.bincount(y[splits[name]], minlength=N_CLASSES).tolist()
        print(f"{name:6s} n={len(splits[name]):4d}  per class {counts}")


def check():
    """Compare every array on disk with EXPECTED; return the list of problems."""
    problems = []
    for rel, keys in LAYOUT.items():
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            problems.append(f"{rel}: missing")
            continue
        with np.load(path, allow_pickle=False) as z:
            if sorted(z.files) != sorted(keys):
                problems.append(f"{rel}: holds {sorted(z.files)}, expected {sorted(keys)}")
                continue
            for k in keys:
                got, want = content_sha256(z[k]), EXPECTED.get(f"{rel}:{k}")
                if want is None:
                    problems.append(f"{rel}:{k}: no expected hash recorded; got {got}")
                elif got != want:
                    problems.append(f"{rel}:{k}: content sha256 {got}, expected {want}")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true",
                        help="check the existing files against EXPECTED; write nothing")
    args = parser.parse_args()
    if not args.check:
        build()
    problems = check()
    for p in problems:
        print("MISMATCH", p)
    if problems:
        print("The task's data differs from the recorded split. Do not evaluate on it until "
              "the cause (source data, split code or library version) is understood.")
        return 1
    print(f"OK: all {sum(len(k) for k in LAYOUT.values())} arrays in {len(LAYOUT)} files "
          "match their recorded content sha256")
    return 0


if __name__ == "__main__":
    sys.exit(main())
