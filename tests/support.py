"""Shared fixtures and process workers for run-journal tests."""

from __future__ import annotations

import tempfile
import time
import unittest
from decimal import Decimal
from pathlib import Path

from scientist_two.run_journal import (
    Charge,
    RunJournal,
    RunManifest,
    Succeeded,
    Unknown,
    WorkInput,
)


KEY = ("task-1", "pass-1", "round-1", "candidate-1", "A_Coder", "call-1")


def manifest() -> RunManifest:
    return RunManifest(
        run_id="run-1",
        task_id="task-1",
        config_digest="sha256:config",
        code_revision="abc123",
        environment_image="local-test:1",
        seed=17,
    )


class MockExecutor:
    identity = "mock:v1"

    def __init__(self, outcome=None, reconciled=None):
        self.calls = []
        self.reconciliations = []
        self.outcome = outcome or Succeeded({"answer": "done"}, Charge(Decimal("1.25")))
        self.reconciled = reconciled

    def execute(self, operation_id, work_input):
        self.calls.append(operation_id)
        return self.outcome

    def reconcile(self, operation_id):
        self.reconciliations.append(operation_id)
        return self.reconciled or Unknown("not visible to provider")


class TimeoutAfterSideEffect(MockExecutor):
    def execute(self, operation_id, work_input):
        self.calls.append(operation_id)
        self.reconciled = Succeeded(
            {"answer": "already charged"}, Charge(Decimal("2.40"))
        )
        raise TimeoutError("response lost after provider completed")


class JournalTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.journal = RunJournal(self.root, manifest())
        self.work_input = WorkInput({"prompt": "solve this"})


class RaceExecutor:
    identity = "race-mock:v1"

    def __init__(self, calls):
        self.calls = calls

    def execute(self, operation_id, work_input):
        with self.calls.get_lock():
            self.calls.value += 1
        time.sleep(0.2)
        return Succeeded({"winner": operation_id}, Charge(Decimal("0.10")))

    def reconcile(self, operation_id):
        return Unknown("should not need reconciliation")


def race_process(root, calls, gate, results):
    try:
        journal = RunJournal(Path(root), manifest())
        gate.wait(10)
        result = journal.run(KEY, WorkInput({"prompt": "race"}), RaceExecutor(calls))
        results.put(("ok", result.operation_id, result.replayed))
    except BaseException as exc:  # Report child failures to the test process.
        results.put(("error", type(exc).__name__, str(exc)))


class SlowExecutor:
    identity = "slow-mock:v1"

    def __init__(self, entered, release):
        self.entered = entered
        self.release = release

    def execute(self, operation_id, work_input):
        self.entered.set()
        if not self.release.wait(15):
            raise TimeoutError("test did not release slow executor")
        return Succeeded({"done": True}, Charge(Decimal("0.50")))

    def reconcile(self, operation_id):
        return Unknown("no reconciliation expected")


def slow_run_process(root, entered, release, results):
    try:
        result = RunJournal(Path(root), manifest()).run(
            KEY, WorkInput({"prompt": "slow"}), SlowExecutor(entered, release)
        )
        results.put(("ok", result.operation_id))
    except BaseException as exc:
        results.put(("error", type(exc).__name__, str(exc)))


def summary_process(root, results):
    try:
        summary = RunJournal(Path(root), manifest()).summary()
        results.put(("ok", summary.known_totals, summary.unknown_work_keys))
    except BaseException as exc:
        results.put(("error", type(exc).__name__, str(exc)))
