# Run journal

This component records one billable external operation per hierarchical work
key. It is the first executable slice of the ScientistTwo engine, not the
six-stage controller. `docs/requirements/run-journal.md` lists its acceptance
tests and source decisions.

```python
from decimal import Decimal
from pathlib import Path
from scientist_two.run_journal import (
    Charge, RunJournal, RunManifest, Succeeded, Unknown, WorkInput,
)

class MockCoder:
    identity = "mock-coder:v1"

    def execute(self, operation_id, work_input):
        return Succeeded({"code_revision": "abc123"}, Charge(Decimal("0"), source="mock"))

    def reconcile(self, operation_id):
        return Unknown("mock has no remote job to recover")

run = RunJournal(
    Path("runs/demo"),
    RunManifest("demo", "task-1", "config-sha256", "abc123", "image-digest", 17),
)
result = run.run(
    ("task-1", "pass-0", "round-0", "idea-1", "subset", "coder-0"),
    WorkInput({"prompt_version": "v1", "task": "task-1"}),
    MockCoder(),
)
```

Repeat the `run` call with the same manifest, key and input to replay the
verified output. A changed input or artifact file under the same key raises
`InputConflict`. A transport exception leaves the operation `InDoubt`; the next
call invokes `reconcile` with the original operation ID and never calls
`execute` again. `recover(key, executor)` can do this even after an original
source artifact is moved or removed. `resolve_charge(key, executor)` reconciles
an unknown amount on a terminal event. A backend should use the operation ID
as its own idempotency or job key.

Every work unit stores its canonical input, staged artifact copies, an
append-only event stream, a head seal and, after success, a content-hashed
output. A run-level registry records claimed/dispatched work. Each work unit
has a process lock. The manifest includes the run's task, configuration, code,
environment image and seed; callers must supply *verified, pinned* values.
Referenced artifacts are regular files copied to read-only snapshots and
hashed by content. Large
codebases and datasets should be represented by an immutable manifest file
or a future content-addressed store, not by a mutable path alone.

File mode `0400` and post-call hashing catch ordinary changes; they do not
secure a file from an executor with the same filesystem authority, which could
change and restore bytes between checks. Coding agents must run in a separate
sandbox that mounts these inputs read-only and cannot write the run directory.

`summary()` returns totals by currency and names every operation whose charge
is unknown or still in doubt, including an active call. A later budget guard
must stop new paid work
while unresolved charges remain. No provider, evaluator or GPU is invoked by
this component.

The summary is an observation, not an atomic spending decision across newly
claimed operations. The future budget guard must coordinate claims and quota
reservations before dispatch.

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 examples/mock_run.py
```

The file-lock implementation requires POSIX `fcntl` (macOS or Linux). Keep the
run directory on one filesystem with reliable atomic rename and fsync. Do not
delete or edit run files to retry an operation; choose a new work key after an
explicit decision and account for any prior charge.
