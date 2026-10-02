"""Small durable store for one event stream per external operation."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import stat
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from .model import CorruptJournal, InputConflict, RunManifest, WorkInput


ZERO_HASH = "0" * 64


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ValueError("work values must be finite JSON data") from error


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    hasher = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError(f"artifact must be a regular file: {path}")
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def ensure_directory(path: Path) -> None:
    """Create each missing directory and sync the parent entry."""
    missing: list[Path] = []
    current = path
    while not current.exists():
        missing.append(current)
        current = current.parent
    for directory in reversed(missing):
        directory.mkdir(exist_ok=True)
        fsync_directory(directory.parent)


def publish(path: Path, data: bytes, *, immutable: bool = False) -> None:
    """Publish complete bytes, then sync the containing directory."""
    ensure_directory(path.parent)
    if immutable and path.exists():
        if path.read_bytes() != data:
            raise CorruptJournal(f"immutable file changed: {path}")
        return
    temporary = path.parent / f".{path.name}.{uuid.uuid4().hex}.tmp"
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def exclusive_lock(path: Path) -> Iterator[None]:
    ensure_directory(path.parent)
    with path.open("a+b") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


@contextmanager
def try_exclusive_lock(path: Path) -> Iterator[bool]:
    """Give observers a prompt unknown result while a paid call holds the lock."""
    ensure_directory(path.parent)
    with path.open("a+b") as stream:
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def input_snapshot(work_input: WorkInput) -> tuple[bytes, str]:
    artifacts: dict[str, dict[str, str]] = {}
    for name, path_value in sorted(work_input.artifacts.items()):
        if not isinstance(name, str) or not name:
            raise ValueError("artifact names must be nonempty strings")
        path = Path(path_value)
        artifacts[name] = {"path": str(path.resolve()), "sha256": file_digest(path)}
    snapshot = canonical({"payload": work_input.payload, "artifacts": artifacts})
    captured = json.loads(snapshot)
    identity = canonical({
        "payload": captured["payload"],
        "artifacts": {
            name: value["sha256"] for name, value in captured["artifacts"].items()
        },
    })
    return snapshot, digest(identity)


class FileStore:
    def __init__(self, root: Path, manifest: RunManifest):
        self.root = Path(root)
        self.work_root = self.root / "work"
        self.registry_path = self.root / "registry.json"
        ensure_directory(self.root)
        manifest_bytes = canonical(vars(manifest))
        self.manifest_hash = digest(manifest_bytes)
        with exclusive_lock(self.root / ".manifest.lock"):
            path = self.root / "manifest.json"
            if path.exists():
                if path.read_bytes() != manifest_bytes:
                    raise InputConflict("run manifest differs from the existing run")
            else:
                publish(path, manifest_bytes, immutable=True)

    def work_dir(self, key: tuple[str, ...]) -> Path:
        if not key or any(not isinstance(part, str) or not part for part in key):
            raise ValueError("work key must contain nonempty string segments")
        return self.work_root / digest(canonical(list(key)))

    def _read_registry(self) -> dict[str, dict[str, Any]]:
        if not self.registry_path.exists():
            if self.work_root.exists() and any(
                (child / "events").exists() or (child / "input.json").exists()
                for child in self.work_root.iterdir() if child.is_dir()
            ):
                raise CorruptJournal("work exists without the run registry")
            return {}
        try:
            registry_bytes = self.registry_path.read_bytes()
            record = json.loads(registry_bytes)
            claims = record["claims"]
            if not isinstance(claims, dict) or record["checksum"] != digest(canonical(claims)):
                raise CorruptJournal("run registry failed its checksum")
            return claims
        except (ValueError, UnicodeDecodeError, KeyError, TypeError) as error:
            raise CorruptJournal("run registry is unreadable") from error

    def _write_registry(self, registry: dict[str, dict[str, Any]]) -> None:
        # One atomic rename publishes both the registry and its checksum.
        publish(self.registry_path, canonical({
            "claims": registry,
            "checksum": digest(canonical(registry)),
        }))

    def registry(self) -> dict[str, dict[str, Any]]:
        with exclusive_lock(self.root / ".registry.lock"):
            return self._read_registry()

    def claim(self, key: tuple[str, ...], work_dir: Path) -> bool:
        """Return whether this operation crossed the durable dispatch boundary."""
        work_id = work_dir.name
        with exclusive_lock(self.root / ".registry.lock"):
            registry = self._read_registry()
            claim = registry.get(work_id)
            if claim is None:
                if (work_dir / "events").exists() or (work_dir / "head.json").exists():
                    raise CorruptJournal("event history exists without a registry claim")
                registry[work_id] = {"work_key": list(key), "dispatched": False}
                self._write_registry(registry)
                return False
            if claim.get("work_key") != list(key) or not isinstance(claim.get("dispatched"), bool):
                raise CorruptJournal("run registry claim is invalid")
            if claim["dispatched"] and not (work_dir / "events" / "000001.json").is_file():
                raise CorruptJournal("dispatched operation directory is missing")
            return claim["dispatched"]

    def mark_dispatched(self, work_dir: Path) -> None:
        """Durably publish the last boundary before calling a paid executor."""
        with exclusive_lock(self.root / ".registry.lock"):
            registry = self._read_registry()
            claim = registry.get(work_dir.name)
            if claim is None:
                raise CorruptJournal("cannot dispatch unclaimed work")
            if not claim["dispatched"]:
                claim["dispatched"] = True
                self._write_registry(registry)

    def staged_input(self, work_dir: Path, snapshot: bytes, work_input: WorkInput) -> WorkInput:
        """Copy referenced files to hashed, read-only paths before dispatch."""
        descriptor = json.loads(snapshot)
        staged: dict[str, Path] = {}
        for name, record in descriptor["artifacts"].items():
            expected = record["sha256"]
            destination = work_dir / "inputs" / f"{digest(canonical(name))}-{expected}.bin"
            if destination.exists():
                if file_digest(destination) != expected:
                    raise CorruptJournal("staged input artifact changed")
            else:
                ensure_directory(destination.parent)
                source = Path(work_input.artifacts[name])
                temporary = destination.parent / f".{destination.name}.{uuid.uuid4().hex}.tmp"
                try:
                    source_fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW)
                    with os.fdopen(source_fd, "rb") as source_stream, temporary.open("xb") as out:
                        hasher = hashlib.sha256()
                        for chunk in iter(lambda: source_stream.read(1024 * 1024), b""):
                            out.write(chunk)
                            hasher.update(chunk)
                        if hasher.hexdigest() != expected:
                            raise InputConflict("artifact changed while preparing the operation")
                        out.flush()
                        os.fchmod(out.fileno(), 0o400)
                        os.fsync(out.fileno())
                    os.replace(temporary, destination)
                    fsync_directory(destination.parent)
                finally:
                    temporary.unlink(missing_ok=True)
            staged[name] = destination
        # Reparse JSON to detach a caller-owned mutable payload from the call.
        return WorkInput(descriptor["payload"], staged)

    def verify_staged_input(self, work_dir: Path, snapshot: bytes) -> None:
        descriptor = json.loads(snapshot)
        for name, record in descriptor["artifacts"].items():
            destination = work_dir / "inputs" / f"{digest(canonical(name))}-{record['sha256']}.bin"
            try:
                valid = destination.exists() and file_digest(destination) == record["sha256"]
            except (OSError, ValueError):
                valid = False
            if not valid:
                raise CorruptJournal("staged input artifact changed")

    def save_input(self, work_dir: Path, snapshot: bytes, *, uncommitted: bool = False) -> str:
        path = work_dir / "input.json"
        if path.exists():
            try:
                old = json.loads(path.read_bytes())
                new = json.loads(snapshot)
                old_artifacts = {k: v["sha256"] for k, v in old["artifacts"].items()}
                new_artifacts = {k: v["sha256"] for k, v in new["artifacts"].items()}
            except (ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError) as error:
                raise CorruptJournal("saved input is unreadable") from error
            if old["payload"] != new["payload"] or old_artifacts != new_artifacts:
                if not uncommitted:
                    raise InputConflict("work key has different input or artifact bytes")
                publish(path, snapshot)
                return digest(snapshot)
            return digest(path.read_bytes())
        publish(path, snapshot, immutable=True)
        return digest(snapshot)

    def load_events(self, work_dir: Path) -> tuple[dict[str, Any], ...]:
        event_dir = work_dir / "events"
        paths = sorted(event_dir.glob("*.json")) if event_dir.exists() else []
        head_path = work_dir / "head.json"
        if not paths:
            if head_path.exists():
                raise CorruptJournal("head references missing events")
            return ()
        events: list[dict[str, Any]] = []
        previous_hash = ZERO_HASH
        for sequence, path in enumerate(paths, 1):
            if path.name != f"{sequence:06d}.json":
                raise CorruptJournal("event sequence has a gap or unexpected name")
            try:
                event = json.loads(path.read_bytes())
                recorded_hash = event.pop("event_hash", None)
            except (ValueError, UnicodeDecodeError, TypeError, AttributeError) as error:
                raise CorruptJournal(f"unreadable event {sequence}") from error
            if (
                event.get("sequence") != sequence
                or event.get("previous_hash") != previous_hash
                or recorded_hash != digest(canonical(event))
            ):
                raise CorruptJournal(f"event {sequence} failed hash-chain verification")
            event["event_hash"] = recorded_hash
            previous_hash = recorded_hash
            events.append(event)
        if len(events) > 3 or events[0].get("kind") != "STARTED":
            raise CorruptJournal("invalid event transition")
        if len(events) >= 2 and events[1].get("kind") not in {
            "SUCCEEDED", "FAILED_CONFIRMED", "UNUSABLE_RESULT", "INPUT_INTEGRITY_FAILED"
        }:
            raise CorruptJournal("invalid terminal event")
        if len(events) == 3 and events[2].get("kind") != "CHARGE_RESOLVED":
            raise CorruptJournal("invalid charge-resolution event")
        if any(event.get("operation_id") != events[0].get("operation_id") for event in events[1:]):
            raise CorruptJournal("event has a different operation ID")
        if head_path.exists():
            try:
                head = json.loads(head_path.read_bytes())
                sealed_sequence = head["sequence"]
                sealed_hash = head["event_hash"]
            except (ValueError, UnicodeDecodeError, KeyError, TypeError) as error:
                raise CorruptJournal("unreadable head seal") from error
            if (
                not isinstance(sealed_sequence, int)
                or sealed_sequence < 1
                or sealed_sequence > len(events)
                or events[sealed_sequence - 1]["event_hash"] != sealed_hash
            ):
                raise CorruptJournal("head seal disagrees with committed history")
        else:
            sealed_sequence = 0
        if sealed_sequence < len(events):
            # A complete event was published before its head update. Adopting it
            # is safe; STARTED is published before any executor dispatch.
            self._seal(work_dir, events[-1])
        return tuple(events)

    def append(self, work_dir: Path, kind: str, operation_id: str, **details: Any) -> dict[str, Any]:
        events = self.load_events(work_dir)
        sequence = len(events) + 1
        if sequence > 3 or (sequence == 1 and kind != "STARTED") or (
            sequence == 2 and kind not in {
                "SUCCEEDED", "FAILED_CONFIRMED", "UNUSABLE_RESULT", "INPUT_INTEGRITY_FAILED"
            }
        ) or (sequence == 3 and kind != "CHARGE_RESOLVED"):
            raise CorruptJournal("invalid append transition")
        if events and operation_id != events[0]["operation_id"]:
            raise CorruptJournal("terminal operation ID differs from start")
        event = {
            "sequence": sequence,
            "previous_hash": events[-1]["event_hash"] if events else ZERO_HASH,
            "kind": kind,
            "operation_id": operation_id,
            "at": datetime.now(timezone.utc).isoformat(),
            **details,
        }
        event["event_hash"] = digest(canonical(event))
        publish(work_dir / "events" / f"{sequence:06d}.json", canonical(event), immutable=True)
        self._seal(work_dir, event)
        return event

    def _seal(self, work_dir: Path, event: dict[str, Any]) -> None:
        publish(work_dir / "head.json", canonical({
            "sequence": event["sequence"], "event_hash": event["event_hash"]
        }))
