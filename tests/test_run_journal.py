"""Replay, reconciliation, and cost accounting for external operations."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from scientist_two.run_journal import (
    Charge, ConfirmedFailure, FailedConfirmed, InDoubt, RunJournal,
    Succeeded, Unknown, WorkInput,
)
from tests.support import KEY, JournalTestCase, MockExecutor, TimeoutAfterSideEffect, manifest


class RunJournalCoreTests(JournalTestCase):
    def test_replay_after_reopen_uses_one_operation_and_one_charge(self):
        executor = MockExecutor()
        first = self.journal.run(KEY, self.work_input, executor)
        reopened = RunJournal(self.root, manifest())
        replay = reopened.run(KEY, self.work_input, executor)

        self.assertEqual(first.output, {"answer": "done"})
        self.assertEqual(replay.output, first.output)
        self.assertEqual(replay.operation_id, first.operation_id)
        self.assertFalse(first.replayed)
        self.assertTrue(replay.replayed)
        self.assertEqual(executor.calls, [first.operation_id])
        self.assertEqual(
            [event["kind"] for event in reopened.events(KEY)],
            ["STARTED", "SUCCEEDED"],
        )
        self.assertEqual(reopened.summary().known_totals, {"USD": Decimal("1.25")})
        self.assertEqual(reopened.summary().unknown_work_keys, ())

    def test_start_is_visible_before_executor_is_called(self):
        journal = self.journal
        root = self.root

        class InspectingExecutor(MockExecutor):
            def execute(self, operation_id, work_input):
                # The runner holds the work lock during execute; inspect durable
                # files directly so this assertion cannot block on that lock.
                start = next(root.rglob("000001.json"))
                visible = json.loads(start.read_text(encoding="utf-8"))
                head = json.loads((start.parent.parent / "head.json").read_text(encoding="utf-8"))
                self_test.assertEqual(visible["kind"], "STARTED")
                self_test.assertEqual(visible["operation_id"], operation_id)
                self_test.assertEqual(head["event_hash"], visible["event_hash"])
                return super().execute(operation_id, work_input)

        self_test = self
        journal.run(KEY, self.work_input, InspectingExecutor())

    def test_timeout_reconciles_existing_operation_without_reexecution(self):
        executor = TimeoutAfterSideEffect()
        with self.assertRaises(InDoubt):
            self.journal.run(KEY, self.work_input, executor)
        self.assertEqual(self.journal.summary().known_totals, {})
        self.assertEqual(self.journal.summary().unknown_work_keys, (KEY,))

        recovered = RunJournal(self.root, manifest()).run(KEY, self.work_input, executor)
        self.assertEqual(recovered.output, {"answer": "already charged"})
        self.assertEqual(recovered.charge.amount, Decimal("2.40"))
        self.assertEqual(executor.calls, [recovered.operation_id])
        self.assertEqual(executor.reconciliations, [recovered.operation_id])
        self.assertEqual(self.journal.summary().known_totals, {"USD": Decimal("2.40")})
        self.assertEqual(self.journal.summary().unknown_work_keys, ())

    def test_unknown_reconciliation_blocks_further_execution(self):
        executor = TimeoutAfterSideEffect()
        with self.assertRaises(InDoubt):
            self.journal.run(KEY, self.work_input, executor)
        executor.reconciled = Unknown("provider cannot locate operation yet")

        with self.assertRaises(InDoubt):
            RunJournal(self.root, manifest()).run(KEY, self.work_input, executor)
        self.assertEqual(len(executor.calls), 1)
        self.assertEqual(len(executor.reconciliations), 1)
        self.assertEqual(self.journal.summary().known_totals, {})
        self.assertEqual(self.journal.summary().unknown_work_keys, (KEY,))

    def test_published_output_without_terminal_event_reconciles_without_reexecution(self):
        executor = TimeoutAfterSideEffect()
        with self.assertRaises(InDoubt):
            self.journal.run(KEY, self.work_input, executor)
        start = next(self.root.rglob("000001.json"))
        work_dir = start.parent.parent
        output = executor.reconciled.output
        (work_dir / "output.json").write_bytes(
            json.dumps(output, sort_keys=True, separators=(",", ":")).encode("utf-8")
        )
        self.assertFalse((start.parent / "000002.json").exists())

        recovered = RunJournal(self.root, manifest()).run(KEY, self.work_input, executor)
        self.assertEqual(recovered.output, output)
        self.assertEqual(len(executor.calls), 1)
        self.assertEqual(executor.reconciliations, [recovered.operation_id])
        self.assertEqual([event["kind"] for event in self.journal.events(KEY)], ["STARTED", "SUCCEEDED"])

    def test_confirmed_failure_is_terminal_and_charged_once(self):
        executor = MockExecutor(
            FailedConfirmed("invalid request", Charge(Decimal("0.35")))
        )
        with self.assertRaises(ConfirmedFailure):
            self.journal.run(KEY, self.work_input, executor)
        with self.assertRaises(ConfirmedFailure):
            RunJournal(self.root, manifest()).run(KEY, self.work_input, executor)
        self.assertEqual(len(executor.calls), 1)
        self.assertEqual(
            [event["kind"] for event in self.journal.events(KEY)],
            ["STARTED", "FAILED_CONFIRMED"],
        )
        self.assertEqual(self.journal.summary().known_totals, {"USD": Decimal("0.35")})
        self.assertEqual(self.journal.summary().unknown_work_keys, ())

    def test_cost_summary_separates_currencies_and_unknown_calls(self):
        executor = MockExecutor(Succeeded({"ok": 1}, Charge(Decimal("1.10"), "USD", "mock")))
        self.journal.run(KEY, self.work_input, executor)
        euro_key = KEY[:-1] + ("euro",)
        executor.outcome = Succeeded({"ok": 2}, Charge(Decimal("0.70"), "EUR", "mock"))
        self.journal.run(euro_key, self.work_input, executor)
        unknown_key = KEY[:-1] + ("unknown",)
        uncertain = TimeoutAfterSideEffect()
        with self.assertRaises(InDoubt):
            self.journal.run(unknown_key, self.work_input, uncertain)

        self.journal.run(KEY, self.work_input, executor)
        summary = RunJournal(self.root, manifest()).summary()
        self.assertEqual(summary.known_totals, {"USD": Decimal("1.10"), "EUR": Decimal("0.70")})
        self.assertEqual(summary.unknown_work_keys, (unknown_key,))

    def test_unknown_amount_on_terminal_result_remains_unknown(self):
        executor = MockExecutor(Succeeded({"ok": True}, Charge(None, "USD", "mock")))
        self.journal.run(KEY, self.work_input, executor)
        self.journal.run(KEY, self.work_input, executor)
        summary = RunJournal(self.root, manifest()).summary()
        self.assertEqual(summary.known_totals, {})
        self.assertEqual(summary.unknown_work_keys, (KEY,))
        self.assertEqual(len(executor.calls), 1)

    def test_recover_settles_timeout_when_original_artifact_is_gone(self):
        source = self.root / "source.txt"
        source.write_bytes(b"original input")
        work_input = WorkInput({"prompt": "use artifact"}, {"data": source})
        executor = TimeoutAfterSideEffect()
        with self.assertRaises(InDoubt):
            self.journal.run(KEY, work_input, executor)
        source.unlink()

        recovered = RunJournal(self.root, manifest()).recover(KEY, executor)
        self.assertEqual(recovered.output, {"answer": "already charged"})
        self.assertEqual(recovered.charge.amount, Decimal("2.40"))
        self.assertEqual(executor.calls, [recovered.operation_id])
        self.assertEqual(executor.reconciliations, [recovered.operation_id])
        self.assertEqual(self.journal.summary().known_totals, {"USD": Decimal("2.40")})

    def test_resolve_terminal_unknown_charge_without_second_execute(self):
        executor = MockExecutor(
            Succeeded({"answer": "done"}, Charge(None, "USD", "mock")),
            Succeeded({"answer": "done"}, Charge(Decimal("1.75"), "USD", "mock")),
        )
        original = self.journal.run(KEY, self.work_input, executor)
        self.assertEqual(self.journal.summary().unknown_work_keys, (KEY,))

        reopened = RunJournal(self.root, manifest())
        reopened.resolve_charge(KEY, executor)
        reopened.resolve_charge(KEY, executor)
        replay = reopened.run(KEY, self.work_input, executor)
        self.assertEqual(replay.operation_id, original.operation_id)
        self.assertEqual(replay.charge.amount, Decimal("1.75"))
        self.assertEqual(executor.calls, [original.operation_id])
        self.assertEqual(executor.reconciliations, [original.operation_id])
        self.assertEqual(reopened.summary().known_totals, {"USD": Decimal("1.75")})
        self.assertEqual(reopened.summary().unknown_work_keys, ())

    def test_non_json_success_output_retains_confirmed_charge(self):
        executor = MockExecutor(
            Succeeded({"unsupported": {1, 2}}, Charge(Decimal("3.00"), "USD", "mock"))
        )
        with self.assertRaises(ConfirmedFailure):
            self.journal.run(KEY, self.work_input, executor)
        with self.assertRaises(ConfirmedFailure):
            RunJournal(self.root, manifest()).run(KEY, self.work_input, executor)
        self.assertEqual(len(executor.calls), 1)
        events = self.journal.events(KEY)
        self.assertEqual([event["kind"] for event in events], ["STARTED", "UNUSABLE_RESULT"])
        self.assertEqual(events[1]["reason"], "unserializable output")
        self.assertEqual(events[1]["charge"]["amount"], "3.00")
        self.assertEqual(self.journal.summary().known_totals, {"USD": Decimal("3.00")})
