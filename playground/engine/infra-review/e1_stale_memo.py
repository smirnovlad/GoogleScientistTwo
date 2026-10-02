"""A coding unit whose transient retries run out leaves a version but no unit record; resume
re-runs it, replaces the version, and the harness returns the old version's memoised result."""
from common import *
from scientisttwo.orchestrator import prepare, run
from scientisttwo.runtime.backends.mock import MockBackend
from scientisttwo.runtime.store import read_json

base = fresh_dir("e1"); task = build_toy_task(base / "task")
rules1 = [{"agent": "subset_coder", "key": "^evo/r0/s1/subset/code", "raise": "transient"},
          {"agent": "subset_critic", "key": "^evo/r0/s1/", "raise": "rate_limit"}]
b1 = MockBackend({"rules": rules1})
ctx = prepare(base / "run", task, quick(), b1, sleep=lambda s: None)
rec = run(ctx)
print("incarnation 1:", rec["status"], "|", rec.get("reason"))
print("  coder attempts:", sum(k == "evo/r0/s1/subset/code" for _, k in b1.calls),
      "| unit record:", ctx.rt.store.get("evo/r0/s1/subset/code"),
      "| ledger has it:", "evo/r0/s1/subset/code" in (ctx.run_dir / "ledger.jsonl").read_text(),
      "| version s1.sub0 exists:", ctx.ws.exists("s1.sub0"))
r1 = read_json(ctx.run_dir / "results/evo/r0/s1/subset/eval0.json")
print("  eval0 memo: mean=%.4f commit=%s" % (r1["mean"], r1["commit"][:10]))

rules2 = [{"agent": "subset_coder", "key": "^evo/r0/s1/", "edits": {"params.json": params(0.3)}},
          {"agent": "subset_critic", "key": "^evo/r0/s1/", "raise": "rate_limit"}]
b2 = MockBackend({"rules": rules2})
ctx2 = prepare(base / "run", None, None, b2, sleep=lambda s: None)
rec2 = run(ctx2)
print("incarnation 2 (resume):", rec2["status"])
print("  coder paid again:", [k for _, k in b2.calls if k == "evo/r0/s1/subset/code"])
head = ctx2.ws.commit("s1.sub0")
r2 = read_json(ctx2.run_dir / "results/evo/r0/s1/subset/eval0.json")
print("  version s1.sub0 now: HEAD=%s params=%s" % (head[:10], (ctx2.ws.path("s1.sub0") / "params.json").read_text()))
print("  eval0 the critic reads: mean=%.4f commit=%s  -> matches HEAD: %s" % (r2["mean"], r2["commit"][:10], r2["commit"] == head))
real = ctx2.harness.evaluate("probe/now", ctx2.ws.path("s1.sub0"), "subset", commit=head)
print("  what s1.sub0 really scores on subset: mean=%.4f" % real["mean"])
