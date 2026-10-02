"""Child processes: each in its own group, recorded on disk while it lives, killed as a whole tree.

An agent session starts processes of its own (its Bash tool's shell runs in a new session, so it
leaves the CLI's process group), and so can evaluated code. Killing the CLI's group alone left
such a child running and writing (infrastructure review 2026-10-02, I5). So:

- a watcher samples the process tree while a child runs, and remembers every descendant group;
- each child carries a marker in its environment (MARKER), and the end of the call also finds,
  by that marker, a descendant that detached and was re-parented before a sample saw it (this
  works for any process whose environment `ps -E` may read: not for Apple's platform binaries);
- the end of every call, normal or not, kills every remembered or marked group still alive;
- each live child is recorded under `<run>/procs/`, so an engine that crashed leaves a record,
  and the next `prepare` kills what it left behind before anything else starts.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import threading
import time
import uuid
from pathlib import Path
from typing import Iterable, Optional

MARKER = "SCIENTISTTWO_UNIT"


def new_marker(key: str) -> str:
    return f"{key}#{uuid.uuid4().hex}"


def marked(marker: str) -> set[tuple[int, int]]:
    """(pid, pgid) of every process whose environment holds MARKER=marker."""
    try:
        out = subprocess.run(["ps", "-A", "-E", "-ww", "-o", "pid=,pgid=,command="], capture_output=True,
                             text=True, timeout=20).stdout
    except (OSError, subprocess.SubprocessError):
        return set()
    needle = f"{MARKER}={marker}"
    found = set()
    for line in out.splitlines():
        if needle in line:
            parts = line.split(None, 2)
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                found.add((int(parts[0]), int(parts[1])))
    return found


def _table() -> list[tuple[int, int, int]]:
    """(pid, ppid, pgid) of every process, from `ps`."""
    try:
        out = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,pgid="], capture_output=True, text=True,
                             timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 3 and all(p.lstrip("-").isdigit() for p in parts):
            rows.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return rows


def descendants(root: int) -> set[tuple[int, int]]:
    """(pid, pgid) of `root` and everything under it, now."""
    rows = _table()
    children: dict[int, list[tuple[int, int]]] = {}
    pgid_of = {}
    for pid, ppid, pgid in rows:
        children.setdefault(ppid, []).append((pid, pgid))
        pgid_of[pid] = pgid
    found: set[tuple[int, int]] = set()
    if root in pgid_of:
        found.add((root, pgid_of[root]))
    stack = [root]
    while stack:
        for pid, pgid in children.get(stack.pop(), []):
            if (pid, pgid) not in found:
                found.add((pid, pgid))
                stack.append(pid)
    return found


def started(pid: int) -> Optional[str]:
    """When `pid` started, as `ps` prints it: with the pid, it names one process for good, so a
    recorded group is never confused with a later group that reuses its number."""
    try:
        out = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)], capture_output=True, text=True,
                             timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    return out or None


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _group_alive(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def kill_groups(groups: Iterable[int], grace: float = 3.0) -> None:
    """SIGTERM every group, wait up to `grace` seconds, then SIGKILL what is left."""
    own = os.getpgrp()
    groups = {g for g in groups if g > 1 and g != own}
    for g in groups:
        try:
            os.killpg(g, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass
    deadline = time.time() + grace
    while time.time() < deadline and any(_group_alive(g) for g in groups):
        time.sleep(0.1)
    for g in groups:
        try:
            os.killpg(g, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


class TreeWatcher:
    """Samples the tree under `root` every `interval` seconds and remembers every group in it,
    with its leader's start time; `on_new(groups)` hears of each new group as it appears."""

    def __init__(self, root: int, interval: float = 0.25, on_new=None):
        self.root = root
        self.interval = interval
        self.groups: dict[int, Optional[str]] = {}
        self.on_new = on_new
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True, name=f"tree-{root}")

    def start(self) -> "TreeWatcher":
        self.sample()
        self._thread.start()
        return self

    def sample(self) -> None:
        new = False
        for _, pgid in descendants(self.root):
            if pgid not in self.groups:
                self.groups[pgid] = started(pgid)
                new = True
        if new and self.on_new is not None:
            self.on_new(dict(self.groups))

    def _loop(self) -> None:
        while not self._stop.wait(self.interval):
            self.sample()

    def stop(self) -> set[int]:
        self._stop.set()
        self.sample()
        return set(self.groups)


class ProcRegistry:
    """`<run>/procs/<pid>.json` for every live child of this engine, so a crash leaves a record."""

    def __init__(self, run_dir: Path):
        self.dir = Path(run_dir) / "procs"
        self.dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def record(self, pid: int, key: str, groups: dict[int, Optional[str]]) -> None:
        """`groups`: each process group of the child's tree, with its leader's start time."""
        data = {"pid": pid, "key": key, "groups": {str(g): t for g, t in groups.items()},
                "time": time.time()}
        with self._lock:
            tmp = self.dir / f"{pid}.json.tmp"
            tmp.write_text(json.dumps(data))
            os.replace(tmp, self.dir / f"{pid}.json")

    def forget(self, pid: int) -> None:
        with self._lock:
            try:
                (self.dir / f"{pid}.json").unlink()
            except FileNotFoundError:
                pass

    def reap_orphans(self, log=None) -> list[dict]:
        """Kill what a previous engine process left running in this run, then clear the records."""
        reaped = []
        for f in sorted(self.dir.glob("*.json")):
            try:
                data = json.loads(f.read_text())
            except (OSError, json.JSONDecodeError):
                f.unlink(missing_ok=True)
                continue
            # a group is killed only if its leader is the very process recorded (same start time)
            live = [int(g) for g, t in (data.get("groups") or {}).items()
                    if t and _group_alive(int(g)) and started(int(g)) == t]
            if live:
                kill_groups(live)
                reaped.append({**data, "killed_groups": live})
                if log is not None:
                    log(f"killed {len(live)} process group(s) left by a previous engine: {data.get('key')}")
            f.unlink(missing_ok=True)
        return reaped


def run_tree(argv: list[str], *, cwd: Path, env: dict, timeout: float, output: Path,
             registry: Optional[ProcRegistry] = None, key: str = "", grace: float = 3.0) -> tuple[int, bool]:
    """Run argv with its output to a file, kill its whole tree at the end. Returns (rc, timed_out).

    The output goes to a file, never a pipe: a pipe kept open by a detached grandchild blocked the
    harness for that child's whole lifetime after a timeout (infrastructure review, I6)."""
    marker = new_marker(key)
    env = {**env, MARKER: marker}
    with open(output, "wb") as out:
        proc = subprocess.Popen(argv, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL, stdout=out,
                                stderr=subprocess.STDOUT, start_new_session=True)
    on_new = (lambda groups: registry.record(proc.pid, key, groups)) if registry is not None else None
    watcher = TreeWatcher(proc.pid, on_new=on_new).start()
    timed_out = False
    try:
        try:
            rc = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            rc = -9
    finally:
        groups = watcher.stop() | {proc.pid} | {g for _, g in marked(marker)}
        kill_groups(groups, grace=grace if timed_out else 0.5)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass
        if registry is not None:
            registry.forget(proc.pid)
    return rc, timed_out
