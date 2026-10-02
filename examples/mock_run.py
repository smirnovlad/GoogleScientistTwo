"""Run and resume one charged mock operation with no external service.

Run from the repository root: ``python3 examples/mock_run.py``.
"""

from __future__ import annotations

import sys
import tempfile
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scientist_two.run_journal import (  # noqa: E402
    Charge,
    RunJournal,
    RunManifest,
    Succeeded,
    Unknown,
    WorkInput,
)


class MockResearchCall:
    identity = "example-mock:v1"

    def __init__(self):
        self.execute_count = 0

    def execute(self, operation_id, work_input):
        self.execute_count += 1
        return Succeeded(
            {"hypothesis": "A measurable, local example", "operation_id": operation_id},
            Charge(Decimal("0.12"), "USD", "mock"),
        )

    def reconcile(self, operation_id):
        return Unknown("the mock has no outstanding operation")


def main():
    manifest = RunManifest(
        run_id="example-run",
        task_id="example-task",
        config_digest="sha256:example-config",
        code_revision="example-revision",
        environment_image="python-stdlib",
        seed=42,
    )
    work_key = ("example-task", "pass-1", "round-1", "A_Idea", "candidate-1")
    work_input = WorkInput({"question": "What is a testable idea?"})
    executor = MockResearchCall()

    with tempfile.TemporaryDirectory(prefix="scientist-two-journal-") as directory:
        first = RunJournal(Path(directory), manifest).run(work_key, work_input, executor)
        replay = RunJournal(Path(directory), manifest).run(work_key, work_input, executor)
        summary = RunJournal(Path(directory), manifest).summary()
        print("First output:", first.output)
        print("Replayed:", replay.replayed)
        print("Executor calls:", executor.execute_count)
        print("Known cost:", summary.known_totals)
        print("Unknown possible charges:", summary.unknown_work_keys)


if __name__ == "__main__":
    main()
