"""The run store: one file per finished unit of work, so a crashed run resumes.

A unit is written only when it has finished, by an atomic rename, so the store never holds half a
unit. On resume the orchestrator runs from the top and every finished unit returns from here,
without a call: a retry never spends twice for the same work (CLAUDE.md).

Unit keys are paths such as `evo/r1/s2/subset/critic/0`, so the store is browsable by stage.
"""
from __future__ import annotations

import json
import os
import re
import tempfile
import threading
from pathlib import Path
from typing import Any, Optional

_KEY = re.compile(r"^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*$")


def atomic_write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, ensure_ascii=False, default=str)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise


def read_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class RunStore:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.units = self.root / "units"
        self.units.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def path(self, key: str) -> Path:
        if not _KEY.match(key) or ".." in key.split("/"):
            raise ValueError(f"bad unit key {key!r}")
        return self.units / f"{key}.json"

    def get(self, key: str) -> Optional[dict]:
        p = self.path(key)
        if not p.exists():
            return None
        return read_json(p)

    def has(self, key: str) -> bool:
        return self.path(key).exists()

    def put(self, key: str, record: dict) -> None:
        atomic_write_json(self.path(key), {"key": key, **record})

    def delete(self, key: str) -> None:
        """Forget a unit, so it runs again (only when its side effects are gone)."""
        self.path(key).unlink(missing_ok=True)

    def keys(self) -> list[str]:
        return sorted(str(p.relative_to(self.units))[:-5] for p in self.units.rglob("*.json")
                      if not p.name.startswith(".tmp-"))
