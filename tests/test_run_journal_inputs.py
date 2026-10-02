"""Input identity, staging, and mutation boundaries."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from scientist_two.run_journal import (
    Charge, ConfirmedFailure, InDoubt, InputConflict, RunJournal, Succeeded, WorkInput,
)
from tests.support import KEY, JournalTestCase, MockExecutor, manifest


class RunJournalInputTests(JournalTestCase):
    def test_changed_input_and_artifact_bytes_rejected_under_same_key(self):
        artifact = self.root / "input.txt"
        artifact.write_text("version one", encoding="utf-8")
        original = WorkInput({"prompt": "one"}, {"data": artifact})
        executor = MockExecutor()
        self.journal.run(KEY, original, executor)

        with self.assertRaises(InputConflict):
            self.journal.run(KEY, WorkInput({"prompt": "two"}, {"data": artifact}), executor)
        artifact.write_text("version two", encoding="utf-8")
        with self.assertRaises(InputConflict):
            self.journal.run(KEY, original, executor)
        self.assertEqual(len(executor.calls), 1)

        other_key = KEY[:-1] + ("call-2",)
        self.journal.run(other_key, original, executor)
        self.assertEqual(len(executor.calls), 2)

    def test_source_artifact_mutation_during_execute_cannot_change_claimed_input(self):
        source = self.root / "source.txt"
        source.write_bytes(b"claimed version")
        work_input = WorkInput({"prompt": "use artifact"}, {"data": source})
        test_case = self

        class MutatingExecutor(MockExecutor):
            def execute(self, operation_id, staged_input):
                staged = Path(staged_input.artifacts["data"])
                test_case.assertNotEqual(staged.resolve(), source.resolve())
                test_case.assertEqual(staged.read_bytes(), b"claimed version")
                source.write_bytes(b"changed during execute")
                test_case.assertEqual(staged.read_bytes(), b"claimed version")
                return super().execute(operation_id, staged_input)

        executor = MutatingExecutor()
        self.journal.run(KEY, work_input, executor)
        with self.assertRaises(InputConflict):
            self.journal.run(KEY, work_input, executor)
        self.assertEqual(len(executor.calls), 1)

    def test_staged_artifact_tamper_then_timeout_records_charge_not_success(self):
        source = self.root / "source.txt"
        source.write_bytes(b"claimed bytes")
        work_input = WorkInput({"prompt": "use artifact"}, {"data": source})

        class TamperingTimeout(MockExecutor):
            def execute(self, operation_id, staged_input):
                self.calls.append(operation_id)
                staged = Path(staged_input.artifacts["data"])
                staged.chmod(0o600)
                staged.write_bytes(b"altered after dispatch")
                self.reconciled = Succeeded(
                    {"answer": "provider succeeded"}, Charge(Decimal("2.40"))
                )
                raise TimeoutError("provider completed but response was lost")

        executor = TamperingTimeout()
        with self.assertRaises(InDoubt):
            self.journal.run(KEY, work_input, executor)
        with self.assertRaises(ConfirmedFailure) as recovered:
            RunJournal(self.root, manifest()).recover(KEY, executor)
        self.assertIn("input integrity failed", recovered.exception.reason)
        self.assertEqual(recovered.exception.charge.amount, Decimal("2.40"))
        self.assertEqual(len(executor.calls), 1)
        self.assertEqual(executor.reconciliations, [recovered.exception.operation_id])
        self.assertEqual(
            [event["kind"] for event in self.journal.events(KEY)],
            ["STARTED", "INPUT_INTEGRITY_FAILED"],
        )
        with self.assertRaises(ConfirmedFailure):
            self.journal.run(KEY, work_input, executor)
        self.assertEqual(len(executor.calls), 1)
        self.assertEqual(self.journal.summary().known_totals, {"USD": Decimal("2.40")})

    def test_executor_payload_is_detached_from_mutable_caller_object(self):
        payload = {"tasks": [{"value": "original"}]}
        original = {"tasks": [{"value": "original"}]}

        class MutatingCallerExecutor(MockExecutor):
            def execute(self, operation_id, staged_input):
                self.calls.append(operation_id)
                payload["tasks"][0]["value"] = "changed after snapshot"
                return Succeeded({"seen": staged_input.payload}, Charge(Decimal("0.20")))

        executor = MutatingCallerExecutor()
        first = self.journal.run(KEY, WorkInput(payload), executor)
        self.assertEqual(first.output, {"seen": original})
        self.assertEqual(
            RunJournal(self.root, manifest()).run(KEY, WorkInput(original), executor).output,
            first.output,
        )
        with self.assertRaises(InputConflict):
            self.journal.run(KEY, WorkInput(payload), executor)
        self.assertEqual(executor.calls, [first.operation_id])

    def test_payload_mutation_between_serializations_keeps_start_identity_consistent(self):
        from scientist_two.run_journal import storage

        payload = {"items": [{"value": "before"}]}
        frozen_payload = {"items": [{"value": "before"}]}
        original_canonical = storage.canonical
        mutated = False

        def mutate_after_snapshot(value):
            nonlocal mutated
            encoded = original_canonical(value)
            if not mutated and isinstance(value, dict) and value.get("payload") is payload:
                payload["items"][0]["value"] = "after"
                mutated = True
            return encoded

        class InspectingExecutor(MockExecutor):
            def execute(self, operation_id, staged_input):
                self_test.assertEqual(staged_input.payload, frozen_payload)
                return super().execute(operation_id, staged_input)

        self_test = self
        executor = InspectingExecutor()
        with patch.object(storage, "canonical", side_effect=mutate_after_snapshot):
            result = self.journal.run(KEY, WorkInput(payload), executor)
        self.assertTrue(mutated, "test did not mutate payload after its first serialization")
        self.assertEqual(payload, {"items": [{"value": "after"}]})

        def canonical_bytes(value):
            return json.dumps(
                value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
            ).encode("utf-8")

        saved = next(self.root.rglob("input.json")).read_bytes()
        descriptor = json.loads(saved)
        identity = {
            "payload": descriptor["payload"],
            "artifacts": {name: item["sha256"] for name, item in descriptor["artifacts"].items()},
        }
        expected_digest = hashlib.sha256(canonical_bytes(identity)).hexdigest()
        manifest_digest = hashlib.sha256((self.root / "manifest.json").read_bytes()).hexdigest()
        expected_operation_id = hashlib.sha256(canonical_bytes({
            "manifest": manifest_digest,
            "work_key": list(KEY),
            "input_digest": expected_digest,
            "executor": executor.identity,
        })).hexdigest()
        started = self.journal.events(KEY)[0]
        self.assertEqual(descriptor["payload"], frozen_payload)
        self.assertEqual(started["input_digest"], expected_digest)
        self.assertEqual(started["input_snapshot_hash"], hashlib.sha256(saved).hexdigest())
        self.assertEqual(started["operation_id"], expected_operation_id)
        self.assertEqual(result.operation_id, expected_operation_id)
        self.assertEqual(
            self.journal.run(KEY, WorkInput(frozen_payload), executor).operation_id,
            expected_operation_id,
        )
        with self.assertRaises(InputConflict):
            self.journal.run(KEY, WorkInput(payload), executor)
        self.assertEqual(executor.calls, [expected_operation_id])

    def test_first_result_and_replay_normalize_non_string_json_keys_identically(self):
        executor = MockExecutor(
            Succeeded({7: "seven", 2: "two"}, Charge(Decimal("0.10")))
        )
        first = self.journal.run(KEY, self.work_input, executor)
        replay = RunJournal(self.root, manifest()).run(KEY, self.work_input, executor)
        self.assertEqual(first.output, {"2": "two", "7": "seven"})
        self.assertEqual(replay.output, first.output)
        self.assertEqual(len(executor.calls), 1)
