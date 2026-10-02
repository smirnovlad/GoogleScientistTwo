"""Execute or reconcile one paid operation without an implicit retry."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from .model import (
    Charge,
    ConfirmedFailure,
    CorruptJournal,
    CostSummary,
    FailedConfirmed,
    InDoubt,
    InputConflict,
    OperationExecutor,
    RunManifest,
    Succeeded,
    Unknown,
    WorkInput,
    WorkResult,
)
from .storage import (
    FileStore, canonical, digest, exclusive_lock, input_snapshot, publish, try_exclusive_lock,
)


def _charge_record(charge: Charge) -> dict[str, str | None]:
    return {
        "amount": str(charge.amount) if charge.amount is not None else None,
        "currency": charge.currency,
        "source": charge.source,
    }


def _charge_from_record(value: Any) -> Charge:
    try:
        return Charge(
            Decimal(value["amount"]) if value["amount"] is not None else None,
            value["currency"],
            value["source"],
        )
    except (KeyError, TypeError, ValueError, ArithmeticError) as error:
        raise CorruptJournal("invalid recorded charge") from error


class RunJournal:
    """One root holds immutable run identity and independently locked operations.

    A work key must name exactly one externally billable call. A parent stage can
    use many hierarchical work keys; this class does not decide stage control flow.
    """

    def __init__(self, root: Path, manifest: RunManifest):
        self.store = FileStore(Path(root), manifest)

    def run(
        self,
        work_key: tuple[str, ...],
        work_input: WorkInput,
        executor: OperationExecutor,
    ) -> WorkResult:
        if not getattr(executor, "identity", None) or not isinstance(executor.identity, str):
            raise ValueError("executor.identity is required for recovery")
        work_dir = self.store.work_dir(work_key)
        snapshot, input_digest = input_snapshot(work_input)
        with exclusive_lock(work_dir / ".lock"):
            dispatched = self.store.claim(work_key, work_dir)
            events = self.store.load_events(work_dir)
            if not events:
                staged = self.store.staged_input(work_dir, snapshot, work_input)
                snapshot_hash = self.store.save_input(work_dir, snapshot, uncommitted=True)
                operation_id = digest(canonical({
                    "manifest": self.store.manifest_hash,
                    "work_key": list(work_key),
                    "input_digest": input_digest,
                    "executor": executor.identity,
                }))
                self.store.append(
                    work_dir,
                    "STARTED",
                    operation_id,
                    manifest_hash=self.store.manifest_hash,
                    work_key=list(work_key),
                    input_digest=input_digest,
                    input_snapshot_hash=snapshot_hash,
                    executor=executor.identity,
                )
            else:
                snapshot_hash = self.store.save_input(work_dir, snapshot)
                start = events[0]
                operation_id = start["operation_id"]
                if start.get("input_snapshot_hash") != snapshot_hash:
                    raise CorruptJournal("saved input differs from the start event")
                if (
                    start.get("manifest_hash") != self.store.manifest_hash
                    or start.get("work_key") != list(work_key)
                    or start.get("input_digest") != input_digest
                    or start.get("executor") != executor.identity
                ):
                    raise InputConflict("work key, input or executor differs from the recorded call")
                if len(events) >= 2:
                    return self._replay(work_dir, events)

            first_call = not dispatched
            if first_call:
                if events:
                    staged = self.store.staged_input(work_dir, snapshot, work_input)
                # This registry transition is fsynced after STARTED and before
                # any external side effect. A missing operation directory can
                # then never be mistaken for fresh work.
                self.store.mark_dispatched(work_dir)

            # The STARTED event and its head seal have both been fsynced before
            # this boundary. Any ambiguous exception keeps it pending.
            if first_call:
                try:
                    outcome = executor.execute(operation_id, staged)
                except Exception as error:
                    raise InDoubt(operation_id, f"execute raised {type(error).__name__}") from error
                replayed = False
            else:
                try:
                    outcome = executor.reconcile(operation_id)
                except Exception as error:
                    raise InDoubt(operation_id, f"reconcile raised {type(error).__name__}") from error
                replayed = True
            if isinstance(outcome, Unknown):
                raise InDoubt(operation_id, outcome.reason)
            return self._settle(work_dir, operation_id, outcome, replayed)

    def recover(self, work_key: tuple[str, ...], executor: OperationExecutor) -> WorkResult:
        """Settle existing work without the original caller artifact paths."""
        work_dir = self.store.work_dir(work_key)
        claim = self.store.registry().get(work_dir.name)
        if claim is None or claim.get("work_key") != list(work_key):
            raise InputConflict("work key was never claimed")
        if claim.get("dispatched") and not work_dir.is_dir():
            raise CorruptJournal("dispatched operation directory is missing")
        with exclusive_lock(work_dir / ".lock"):
            events = self.store.load_events(work_dir)
            if not events:
                raise ValueError("operation was claimed but not started")
            start = events[0]
            if start.get("executor") != getattr(executor, "identity", None):
                raise InputConflict("recovery executor differs from the original")
            if len(events) >= 2:
                return self._replay(work_dir, events)
            operation_id = start["operation_id"]
            try:
                outcome = executor.reconcile(operation_id)
            except Exception as error:
                raise InDoubt(operation_id, f"reconcile raised {type(error).__name__}") from error
            if isinstance(outcome, Unknown):
                raise InDoubt(operation_id, outcome.reason)
            return self._settle(work_dir, operation_id, outcome, True)

    def resolve_charge(self, work_key: tuple[str, ...], executor: OperationExecutor) -> Charge:
        """Reconcile an unknown terminal charge without executing again."""
        work_dir = self.store.work_dir(work_key)
        claim = self.store.registry().get(work_dir.name)
        if claim is None or claim.get("work_key") != list(work_key):
            raise InputConflict("work key was never claimed")
        with exclusive_lock(work_dir / ".lock"):
            events = self.store.load_events(work_dir)
            if len(events) < 2:
                raise ValueError("operation has no terminal outcome")
            if events[0].get("executor") != getattr(executor, "identity", None):
                raise InputConflict("recovery executor differs from the original")
            charge = self._effective_charge(events)
            if charge.amount is not None:
                return charge
            operation_id = events[0]["operation_id"]
            try:
                outcome = executor.reconcile(operation_id)
            except Exception as error:
                raise InDoubt(operation_id, f"charge reconciliation raised {type(error).__name__}") from error
            if isinstance(outcome, Unknown) or outcome.charge.amount is None:
                raise InDoubt(operation_id, "charge remains unknown")
            terminal = events[1]
            if terminal["kind"] == "SUCCEEDED":
                if not isinstance(outcome, Succeeded) or digest(canonical(outcome.output)) != terminal["output_hash"]:
                    raise CorruptJournal("reconciled result differs from recorded output")
            elif terminal["kind"] == "FAILED_CONFIRMED" and not isinstance(outcome, FailedConfirmed):
                raise CorruptJournal("reconciled outcome differs from recorded failure")
            self.store.append(
                work_dir, "CHARGE_RESOLVED", operation_id, charge=_charge_record(outcome.charge)
            )
            return outcome.charge

    def _saved_input(self, work_dir: Path) -> bytes:
        events = self.store.load_events(work_dir)
        path = work_dir / "input.json"
        if not path.is_file():
            raise CorruptJournal("recorded input is missing")
        snapshot = path.read_bytes()
        if not events or digest(snapshot) != events[0].get("input_snapshot_hash"):
            raise CorruptJournal("recorded input failed content verification")
        return snapshot

    def _settle(
        self,
        work_dir: Path,
        operation_id: str,
        outcome: Succeeded | FailedConfirmed,
        replayed: bool,
    ) -> WorkResult:
        if not isinstance(outcome, (Succeeded, FailedConfirmed)):
            raise TypeError("executor returned an invalid outcome")
        try:
            self.store.verify_staged_input(work_dir, self._saved_input(work_dir))
        except CorruptJournal as error:
            reason = f"input integrity failed: {error}"
            self.store.append(
                work_dir, "INPUT_INTEGRITY_FAILED", operation_id,
                reason=reason, charge=_charge_record(outcome.charge),
            )
            raise ConfirmedFailure(operation_id, reason, outcome.charge) from error
        return self._finish(work_dir, operation_id, outcome, replayed)

    def _finish(
        self,
        work_dir: Path,
        operation_id: str,
        outcome: Succeeded | FailedConfirmed,
        replayed: bool,
    ) -> WorkResult:
        if isinstance(outcome, Succeeded):
            try:
                output_bytes = canonical(outcome.output)
            except ValueError as error:
                reason = "unserializable output"
                self.store.append(
                    work_dir, "UNUSABLE_RESULT", operation_id,
                    reason=reason, charge=_charge_record(outcome.charge),
                )
                raise ConfirmedFailure(operation_id, reason, outcome.charge) from error
            output_hash = digest(output_bytes)
            # Output publication is durable before the terminal event.
            publish(work_dir / "output.json", output_bytes, immutable=True)
            self.store.append(
                work_dir,
                "SUCCEEDED",
                operation_id,
                output_hash=output_hash,
                charge=_charge_record(outcome.charge),
            )
            return WorkResult(json.loads(output_bytes), outcome.charge, operation_id, replayed)
        if isinstance(outcome, FailedConfirmed):
            self.store.append(
                work_dir,
                "FAILED_CONFIRMED",
                operation_id,
                reason=outcome.reason,
                charge=_charge_record(outcome.charge),
            )
            raise ConfirmedFailure(operation_id, outcome.reason, outcome.charge)
        raise TypeError("executor must return Succeeded, FailedConfirmed or Unknown")

    def _effective_charge(self, events: tuple[dict[str, Any], ...]) -> Charge:
        return _charge_from_record(events[-1].get("charge"))

    def _replay(self, work_dir: Path, events: tuple[dict[str, Any], ...]) -> WorkResult:
        terminal = events[1]
        operation_id = terminal["operation_id"]
        charge = self._effective_charge(events)
        if terminal["kind"] in {
            "FAILED_CONFIRMED", "UNUSABLE_RESULT", "INPUT_INTEGRITY_FAILED"
        }:
            raise ConfirmedFailure(operation_id, terminal["reason"], charge)
        self.store.verify_staged_input(work_dir, self._saved_input(work_dir))
        path = work_dir / "output.json"
        if not path.is_file():
            raise CorruptJournal("completed output is missing")
        output_bytes = path.read_bytes()
        if digest(output_bytes) != terminal.get("output_hash"):
            raise CorruptJournal("completed output failed content verification")
        try:
            output = json.loads(output_bytes)
        except (ValueError, UnicodeDecodeError) as error:
            raise CorruptJournal("completed output is unreadable") from error
        if canonical(output) != output_bytes:
            raise CorruptJournal("completed output is not canonical JSON")
        return WorkResult(output, charge, operation_id, True)

    def events(self, work_key: tuple[str, ...]) -> tuple[dict[str, Any], ...]:
        work_dir = self.store.work_dir(work_key)
        claim = self.store.registry().get(work_dir.name)
        if claim and claim.get("dispatched") and not work_dir.is_dir():
            raise CorruptJournal("dispatched operation directory is missing")
        with exclusive_lock(work_dir / ".lock"):
            return self.store.load_events(work_dir)

    def summary(self) -> CostSummary:
        known: dict[str, Decimal] = {}
        unknown: list[tuple[str, ...]] = []
        registry = self.store.registry()
        for work_id, claim in sorted(registry.items()):
            work_dir = self.store.work_root / work_id
            if not work_dir.is_dir():
                if claim.get("dispatched"):
                    raise CorruptJournal("dispatched operation directory is missing")
                continue
            with try_exclusive_lock(work_dir / ".lock") as acquired:
                if not acquired:
                    unknown.append(tuple(claim["work_key"]))
                    continue
                events = self.store.load_events(work_dir)
                if not events:
                    if claim.get("dispatched"):
                        raise CorruptJournal("dispatched operation history is missing")
                    continue
                key = tuple(events[0]["work_key"])
                if len(events) == 1:
                    unknown.append(key)
                    continue
                charge = self._effective_charge(events)
                if charge.amount is None:
                    unknown.append(key)
                else:
                    known[charge.currency] = known.get(charge.currency, Decimal(0)) + charge.amount
        return CostSummary(known, tuple(unknown))
