"""Tamper detection and durable event recovery."""

from __future__ import annotations

import json
import shutil
import tempfile
from decimal import Decimal
from pathlib import Path

from scientist_two.run_journal import Charge, CorruptJournal, RunJournal, Succeeded
from tests.support import KEY, JournalTestCase, MockExecutor, manifest


class RunJournalIntegrityTests(JournalTestCase):
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
