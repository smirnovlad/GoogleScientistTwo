"""Fixtures: a toy task small enough to evaluate in milliseconds, built fresh for each test.

The toy task: x ~ U(0, 1), label = x > 0.3. The released "method" thresholds at 0.5 (accuracy
about 0.8); an idea that moves the threshold to 0.3 reaches 1.0. So a mock coding agent that
edits `params.json` changes the harness's numbers for real, and every branch can be driven.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

RUN_PY = '''import argparse, json, pathlib
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument("--train-dir"); ap.add_argument("--inputs"); ap.add_argument("--out"); ap.add_argument("--seed", type=int)
a = ap.parse_args()
params = json.loads((pathlib.Path(__file__).parent / "params.json").read_text())
train = np.load(pathlib.Path(a.train_dir) / "train.npz")
X = np.load(a.inputs)["X"]
rng = np.random.default_rng(a.seed)
noise = params.get("noise", 0.0) * rng.standard_normal(len(X))
np.save(a.out, ((X[:, 0] + noise) > params["threshold"]).astype(np.int64))
'''

METRIC_PY = '''import numpy as np
def score(predictions_path, labels_path):
    p = np.load(predictions_path); y = np.load(labels_path)["y"]
    if p.shape != y.shape:
        raise ValueError(f"expected {y.shape} predictions, got {p.shape}")
    return {"primary": float((p == y).mean()), "n": int(len(y))}
'''


def build_toy_task(root: Path) -> Path:
    rng = np.random.default_rng(0)

    def split(n: int):
        x = rng.uniform(0, 1, size=(n, 1))
        return x, (x[:, 0] > 0.3).astype(np.int64)

    (root / "code").mkdir(parents=True)
    (root / "data" / "public").mkdir(parents=True)
    for d in ("inputs", "labels"):
        (root / "harness" / d).mkdir(parents=True)
    x, y = split(200)
    np.savez(root / "data" / "public" / "train.npz", X=x, y=y)
    for name, n in (("subset", 100), ("full", 300), ("test", 300)):
        x, y = split(n)
        np.savez(root / "harness" / "inputs" / f"{name}.npz", X=x)
        np.savez(root / "harness" / "labels" / f"{name}.npz", y=y)
    (root / "harness" / "metric.py").write_text(METRIC_PY)
    (root / "code" / "run.py").write_text(RUN_PY)
    (root / "code" / "params.json").write_text(json.dumps({"threshold": 0.5}))
    (root / "code" / "README.md").write_text("Threshold classifier. `run.py` reads params.json.\n")
    (root / "paper.md").write_text("# Thresholding\n\nWe classify x by x > 0.5. Accuracy 0.80.\n")
    (root / "rules.md").write_text("Do not change the data, the splits or the metric.\n")
    (root / "task.json").write_text(json.dumps({
        "id": "toy", "title": "Toy thresholding", "paper": "paper.md", "rules": "rules.md",
        "code": "code", "public_data": "data/public",
        "entrypoint": "{python} run.py --train-dir {train_dir} --inputs {inputs} --out {out} --seed {seed}",
        "metric": {"name": "accuracy", "direction": "max", "module": "harness/metric.py"},
        "splits": {"subset": {"inputs": "harness/inputs/subset.npz", "labels": "harness/labels/subset.npz", "seeds": [0]},
                   "full": {"inputs": "harness/inputs/full.npz", "labels": "harness/labels/full.npz", "seeds": [0, 1]},
                   "test": {"inputs": "harness/inputs/test.npz", "labels": "harness/labels/test.npz", "seeds": [0, 1]}},
        "timeouts": {"evaluation_seconds": 60, "coding_session_seconds": 60},
        "reported": "Accuracy 0.80 with threshold 0.5."}))
    return root


@pytest.fixture
def toy_task(tmp_path: Path) -> Path:
    return build_toy_task(tmp_path / "toy_task")


def params(threshold: float, noise: float = 0.0) -> str:
    return json.dumps({"threshold": threshold, "noise": noise})
