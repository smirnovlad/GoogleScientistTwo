# Run journal: first executable engine slice

This is a scoped implementation requirement for `codex/run-journal`, pending
reconciliation with TODO tasks 2, 3 and 6. It does not decide the six-stage
algorithm, evaluation harness or budget guard. The user has asked for an actual
engine; `CLAUDE.md` already requires persistence, resume, cost accounting and
zero-cost mocks. ScientistTwo §3 and Table 1 nest paid calls inside repeated
stages; the paper's persistence protocol is **UNSPECIFIED**. These are our
decisions, reviewed through system-architect and infrastructure lenses.

The unit recorded here is **one external operation**, which may be a child of a
stage. A stable hierarchical work key names its run/task, pass, round,
candidate, stage, loop index and agent as applicable. A parent stage later
aggregates child outcomes. A separate work key is required for an explicit
retry; this component never silently retries a paid operation.

| ID | Requirement | Acceptance test |
|---|---|---|
| RJ-1 | A run manifest fixes task/config identity, code revision, environment image and seed. A work key plus canonical input and content digests of referenced artifacts identify one operation. Inputs are stored for audit; referenced files are staged before dispatch. | Changed input or artifact bytes under the same key are rejected; mutation of the source file during execution cannot change the staged bytes the executor reads. |
| RJ-2 | A root registry claims each work key and seals the dispatch boundary. A single writer records the start event and operation ID durably **before** invoking the executor. | Race two processes on one key: one executor call, one start and one terminal event. Delete a dispatched work directory: run and ledger fail closed. |
| RJ-3 | A successful output artifact is written, fsynced and atomically published before its terminal event is fsynced. Completed output is hash checked and replayed without another call. | Run twice and assert one call; mutate output bytes and assert replay fails. Crash after artifact publication and before terminal publication: adopt a complete event or reconcile, never execute again. |
| RJ-4 | A transport exception is **InDoubt**, not a confirmed failure. `recover(key, executor)` asks the backend to reconcile by operation ID without requiring the original artifact path. `Unknown` blocks execution. | Simulate a charged call followed by timeout and remove the original input; recovery returns the existing result or `InDoubt` with zero new execute calls. |
| RJ-5 | Cost is attached to each operation outcome with amount, currency and source. Unknown and InDoubt charges stay unknown. A terminal unknown charge can be reconciled without execution. A nonserializable paid result records its known charge as unusable. | Aggregate across replay/reconcile once; resolve an unknown terminal charge; reject a non-JSON output while retaining its charge. |
| RJ-6 | Event files are append-only and hash chained; durable event and root-registry seals detect missing committed history. Torn or syntactically valid edits fail closed. A complete event published before its head seal is adopted on recovery. | Edit an earlier event's cost or ID while keeping valid JSON; delete a committed tail or work directory; truncate a file. Each is rejected. |
| RJ-7 | The component runs on Python standard library tools with a mock executor. It makes no model, GPU, search or network call. | A fresh checkout runs meaningful tests and a small example without credentials. |

## Contract proposed for implementation

Input: immutable run manifest, hierarchical work key, JSON input, immutable
artifact references and an executor with `execute(operation_id, input)` and
`reconcile(operation_id)`. Reconciliation returns `Succeeded`,
`FailedConfirmed` or `Unknown`. Output: a typed result with value, charge and
replay status. Failures: changed inputs, corrupted history/artifact, confirmed
execution failure, unusable local output, or unresolved in-flight work. All are
visible to callers. `recover` settles an in-flight operation; `resolve_charge`
settles an unknown terminal amount by operation ID without executing again.

The component exposes known totals and a list of operations with unknown
possible charges for a later budget guard. A future run/task budget guard must
block further spend while such an operation is unresolved; this slice does not
claim to enforce a spending limit.

`⛔ WHY NOT` claim exactly-once provider execution: a process can die after a
provider charges but before local completion is published. The executor must
recover by operation ID, or return `Unknown`; the journal never guesses.

`⛔ WHY NOT` store only stage outcomes: A_Coder and the later loops can contain
several paid calls, so a stage-level record alone cannot resume without
repeating work.

`⛔ WHY NOT` treat a path as an artifact identity: bytes can change at the same
path. Input references carry content hashes and are staged before dispatch.

The run directory must survive intact on one filesystem with atomic rename and
reliable fsync. A broken root-registry seal fails closed and needs explicit
repair from trusted records. The seal detects accidental corruption, not a
malicious writer that can rewrite the entire run directory and every seal.
The staged file mode and post-call hash are not a sandbox boundary against an
executor with write authority over the run directory; task 6 must keep agents
outside that boundary. `summary()` is observational, not a budget reservation.
