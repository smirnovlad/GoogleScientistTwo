"""Black-box tests for durable, single-charge external operations."""

from __future__ import annotations

import json
import hashlib
import multiprocessing
import shutil
import tempfile
import time
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from scientist_two.run_journal import (
    Charge,
    ConfirmedFailure,
    CorruptJournal,
    FailedConfirmed,
    InDoubt,
    InputConflict,
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


def _race_process(root, calls, gate, results):
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


def _slow_run_process(root, entered, release, results):
    try:
        result = RunJournal(Path(root), manifest()).run(
            KEY, WorkInput({"prompt": "slow"}), SlowExecutor(entered, release)
        )
        results.put(("ok", result.operation_id))
    except BaseException as exc:
        results.put(("error", type(exc).__name__, str(exc)))


def _summary_process(root, results):
    try:
        summary = RunJournal(Path(root), manifest()).summary()
        results.put(("ok", summary.known_totals, summary.unknown_work_keys))
    except BaseException as exc:
        results.put(("error", type(exc).__name__, str(exc)))


class RunJournalTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.journal = RunJournal(self.root, manifest())
        self.work_input = WorkInput({"prompt": "solve this"})

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

    def test_deleted_claimed_work_directory_is_detected_by_run_ledger(self):
        executor = MockExecutor()
        self.journal.run(KEY, self.work_input, executor)
        start = next(self.root.rglob("000001.json"))
        shutil.rmtree(start.parent.parent)

        reopened = RunJournal(self.root, manifest())
        with self.assertRaises(CorruptJournal):
            reopened.run(KEY, self.work_input, executor)
        with self.assertRaises(CorruptJournal):
            reopened.summary()
        self.assertEqual(len(executor.calls), 1)

    def test_valid_json_registry_claim_edit_fails_closed(self):
        executor = MockExecutor()
        self.journal.run(KEY, self.work_input, executor)
        registry_path = self.root / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        self.assertEqual(set(registry), {"claims", "checksum"})
        self.assertEqual(len(registry["claims"]), 1)
        claim = next(iter(registry["claims"].values()))
        self.assertTrue(claim["dispatched"])
        claim["dispatched"] = False
        registry_path.write_text(json.dumps(registry), encoding="utf-8")

        reopened = RunJournal(self.root, manifest())
        with self.assertRaises(CorruptJournal):
            reopened.summary()
        with self.assertRaises(CorruptJournal):
            reopened.run(KEY, self.work_input, executor)
        self.assertEqual(len(executor.calls), 1)

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

    def test_mutated_output_artifact_fails_closed(self):
        marker = "unique-output-marker-2479"
        executor = MockExecutor(Succeeded({"answer": marker}, Charge(Decimal("1.00"))))
        self.journal.run(KEY, self.work_input, executor)
        artifact = next(self.root.rglob("output.json"))
        self.assertIn(marker.encode(), artifact.read_bytes())
        artifact.write_bytes(artifact.read_bytes().replace(marker.encode(), b"modified-output-marker"))
        with self.assertRaises(CorruptJournal):
            RunJournal(self.root, manifest()).run(KEY, self.work_input, executor)
        self.assertEqual(len(executor.calls), 1)

    def test_valid_json_event_edit_fails_hash_chain_check(self):
        self.journal.run(KEY, self.work_input, MockExecutor())
        event_file = next(
            path
            for path in self.root.rglob("*")
            if path.is_file() and b"STARTED" in path.read_bytes()
        )
        raw = event_file.read_bytes()
        changed = raw.replace(b"STARTED", b"STARTEx", 1)
        self.assertNotEqual(changed, raw)
        # A syntactically valid edit must still fail verification.
        for line in changed.splitlines():
            if line.strip():
                json.loads(line)
        event_file.write_bytes(changed)
        with self.assertRaises(CorruptJournal):
            RunJournal(self.root, manifest()).events(KEY)

    def test_missing_committed_tail_and_truncated_event_fail_closed(self):
        for damage in ("delete", "truncate"):
            with self.subTest(damage=damage), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                journal = RunJournal(root, manifest())
                journal.run(KEY, self.work_input, MockExecutor())
                terminal = next(root.rglob("000002.json"))
                if damage == "delete":
                    terminal.unlink()
                else:
                    terminal.write_bytes(terminal.read_bytes()[:12])
                with self.assertRaises(CorruptJournal):
                    RunJournal(root, manifest()).events(KEY)

    def test_complete_event_before_head_seal_is_adopted(self):
        executor = MockExecutor()
        first = self.journal.run(KEY, self.work_input, executor)
        start = next(self.root.rglob("000001.json"))
        head = start.parent.parent / "head.json"
        started_event = json.loads(start.read_text(encoding="utf-8"))
        head.write_text(
            json.dumps({"sequence": 1, "event_hash": started_event["event_hash"]}),
            encoding="utf-8",
        )

        replay = RunJournal(self.root, manifest()).run(KEY, self.work_input, executor)
        self.assertEqual(replay.operation_id, first.operation_id)
        self.assertTrue(replay.replayed)
        self.assertEqual(len(executor.calls), 1)
        self.assertEqual(json.loads(head.read_text(encoding="utf-8"))["sequence"], 2)

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

    def test_two_processes_claim_one_key_once(self):
        context = multiprocessing.get_context("spawn")
        calls = context.Value("i", 0)
        gate = context.Barrier(2)
        results = context.Queue()
        processes = [
            context.Process(target=_race_process, args=(str(self.root), calls, gate, results))
            for _ in range(2)
        ]
        try:
            for process in processes:
                process.start()
            reported = [results.get(timeout=15) for _ in processes]
            for process in processes:
                process.join(timeout=5)
            self.assertTrue(all(process.exitcode == 0 for process in processes), reported)
            self.assertTrue(all(item[0] == "ok" for item in reported), reported)
            self.assertEqual({item[1] for item in reported}, {reported[0][1]})
            self.assertEqual(sorted(item[2] for item in reported), [False, True])
            self.assertEqual(calls.value, 1)
            self.assertEqual(len(self.journal.events(KEY)), 2)
        finally:
            for process in processes:
                if process.is_alive():
                    process.terminate()
                process.join(timeout=1)

    def test_summary_reports_in_flight_call_without_waiting_for_execute(self):
        context = multiprocessing.get_context("spawn")
        entered = context.Event()
        release = context.Event()
        run_results = context.Queue()
        summary_results = context.Queue()
        running = context.Process(
            target=_slow_run_process, args=(str(self.root), entered, release, run_results)
        )
        reader = context.Process(target=_summary_process, args=(str(self.root), summary_results))
        try:
            running.start()
            self.assertTrue(entered.wait(10), "executor never entered its external call")
            reader.start()
            reader.join(timeout=3)
            self.assertFalse(reader.is_alive(), "summary blocked behind an in-flight call")
            self.assertEqual(reader.exitcode, 0)
            reported = summary_results.get(timeout=1)
            self.assertEqual(reported, ("ok", {}, (KEY,)))
            self.assertTrue(running.is_alive(), "executor finished before summary returned")
        finally:
            release.set()
            for process in (reader, running):
                process.join(timeout=5)
                if process.is_alive():
                    process.terminate()
                    process.join(timeout=1)
        self.assertEqual(run_results.get(timeout=1)[0], "ok")


if __name__ == "__main__":
    unittest.main()
