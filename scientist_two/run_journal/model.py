"""Values and explicit outcomes at the paid-operation boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class RunManifest:
    run_id: str
    task_id: str
    config_digest: str
    code_revision: str
    environment_image: str
    seed: int

    def __post_init__(self) -> None:
        for name in ("run_id", "task_id", "config_digest", "code_revision", "environment_image"):
            if not getattr(self, name) or not isinstance(getattr(self, name), str):
                raise ValueError(f"{name} must be a nonempty string")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise ValueError("seed must be an integer")


@dataclass(frozen=True)
class WorkInput:
    payload: Any
    artifacts: Mapping[str, Path] = field(default_factory=dict)


@dataclass(frozen=True)
class Charge:
    """Unknown amount is None, never an assumed zero."""

    amount: Decimal | None
    currency: str = "USD"
    source: str = "provider"

    def __post_init__(self) -> None:
        if self.amount is not None:
            amount = Decimal(str(self.amount))
            if not amount.is_finite() or amount < 0:
                raise ValueError("charge must be finite and nonnegative")
            object.__setattr__(self, "amount", amount)
        if not self.currency or not self.source:
            raise ValueError("charge currency and source are required")


@dataclass(frozen=True)
class Succeeded:
    output: Any
    charge: Charge


@dataclass(frozen=True)
class FailedConfirmed:
    reason: str
    charge: Charge


@dataclass(frozen=True)
class Unknown:
    reason: str = "backend cannot establish an outcome"


class OperationExecutor(Protocol):
    identity: str

    def execute(self, operation_id: str, work_input: WorkInput) -> Succeeded | FailedConfirmed: ...

    def reconcile(self, operation_id: str) -> Succeeded | FailedConfirmed | Unknown: ...


@dataclass(frozen=True)
class WorkResult:
    output: Any
    charge: Charge
    operation_id: str
    replayed: bool


@dataclass(frozen=True)
class CostSummary:
    known_totals: dict[str, Decimal]
    unknown_work_keys: tuple[tuple[str, ...], ...]


class InputConflict(ValueError):
    """A stable work key or run root was reused with different inputs."""


class CorruptJournal(RuntimeError):
    """History or a published artifact failed verification."""


class InDoubt(RuntimeError):
    def __init__(self, operation_id: str, reason: str):
        self.operation_id = operation_id
        super().__init__(f"operation {operation_id} is in doubt: {reason}")


class ConfirmedFailure(RuntimeError):
    def __init__(self, operation_id: str, reason: str, charge: Charge):
        self.operation_id = operation_id
        self.reason = reason
        self.charge = charge
        super().__init__(f"operation {operation_id} failed: {reason}")
