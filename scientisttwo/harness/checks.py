"""Checkable task rules, applied by code to a version before anything of it runs.

A change may not add a string the task forbids (a dataset loader, a URL …), nor a data file unless
the task allows it. These are tripwires for the obvious routes; the sandbox's read allowlist and
the egress proxy are what make the labels unreachable (sandbox.py, egress.py).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..task import Task
from ..workspace import Workspaces

DATA_SUFFIXES = {".npz", ".npy", ".csv", ".tsv", ".gz", ".zip", ".bz2", ".xz", ".tar", ".pkl",
                 ".pickle", ".joblib", ".pt", ".pth", ".ckpt", ".h5", ".hdf5", ".parquet",
                 ".feather", ".arrow", ".mat", ".bin", ".safetensors", ".onnx"}
MAX_ADDED_BYTES = 1_000_000              # no added file this large is code (our choice, 2026-10-02)


def change_violation(ws: Workspaces, task: Task, task_commit: str, name: str) -> Optional[str]:
    """Why version `name` may not run, or None."""
    if not task_commit:
        return None
    lines, files = ws.added(name, task_commit)
    low = lines.lower()
    for s in task.forbidden_in_diff:
        if s.lower() in low:
            return f"the change adds {s!r}, which the task forbids (rules.md)"
    if not task.allow_data_files:
        for f in files:
            if f["binary"] or Path(f["path"]).suffix.lower() in DATA_SUFFIXES or f["bytes"] > MAX_ADDED_BYTES:
                return (f"the change adds the data file {f['path']} ({f['bytes']} bytes); "
                        "data may come only from the training split")
    return None
