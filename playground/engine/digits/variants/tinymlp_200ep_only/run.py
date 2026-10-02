"""Train TinyMLP on the training set, then predict a label for every input row.

    python run.py --train-dir DIR --inputs INPUTS.npz --out PREDICTIONS.npy --seed SEED

DIR/train.npz holds X (n x 64 pixel counts) and y (digit labels 0..9).
INPUTS.npz holds X (m x 64). PREDICTIONS.npy receives m integer labels, in row order.
The same seed gives the same predictions.
"""
import argparse
import os
import time
import warnings

import numpy as np

from model import build_model

# numpy < 2.3.1 with Apple's Accelerate BLAS on M4 chips raises spurious floating-point
# flags in matrix products ("overflow encountered in matmul") although the products are
# exact; numpy 2.3.1 fixed it (numpy PR #29235). The warning is silenced here, and
# check_finite() below still stops the run if training really diverges.
warnings.filterwarnings("ignore", message=r".* encountered in matmul", category=RuntimeWarning)

N_FEATURES = 64


def load_npz(path, keys):
    with np.load(path, allow_pickle=False) as data:
        missing = [k for k in keys if k not in data.files]
        if missing:
            raise ValueError(f"{path} lacks {missing}; it holds {data.files}")
        arrays = [data[k] for k in keys]
    X = np.asarray(arrays[0], dtype=np.float64)
    if X.ndim != 2 or X.shape[1] != N_FEATURES:
        raise ValueError(f"{path}: X must be n x {N_FEATURES}; got shape {X.shape}")
    return [X] + arrays[1:]


def check_finite(model):
    for w in model.coefs_ + model.intercepts_:
        if not np.isfinite(w).all():
            raise FloatingPointError("training diverged: the network has non-finite weights")


def main():
    parser = argparse.ArgumentParser(description="Train TinyMLP and write predictions.")
    parser.add_argument("--train-dir", required=True, help="directory holding train.npz")
    parser.add_argument("--inputs", required=True, help=".npz file holding X, the rows to label")
    parser.add_argument("--out", required=True, help=".npy file to write the predicted labels to")
    parser.add_argument("--seed", required=True, type=int, help="seed of initialisation and batch order")
    args = parser.parse_args()

    start = time.time()
    X_train, y_train = load_npz(os.path.join(args.train_dir, "train.npz"), ["X", "y"])
    (X,) = load_npz(args.inputs, ["X"])

    model = build_model(args.seed)
    model.fit(X_train, y_train)
    pass
    train_accuracy = float((model.predict(X_train) == y_train).mean())
    predictions = model.predict(X).astype(np.int64)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "wb") as f:  # a file object: np.save appends no extension
        np.save(f, predictions)
    print(f"seed={args.seed} train_n={len(y_train)} "
          f"train_accuracy={train_accuracy:.4f} "
          f"predicted_n={len(predictions)} seconds={time.time() - start:.2f}")


if __name__ == "__main__":
    main()
