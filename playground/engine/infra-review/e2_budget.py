from common import *
import json, time, types
from scientisttwo.runtime.agents import AgentRuntime, AgentSpec, Routing, UnitFailed
from scientisttwo.runtime.backends.mock import MockBackend
from scientisttwo.runtime.budget import Budget, BudgetExceeded, Caps
from scientisttwo.runtime.store import RunStore
SCHEMA = {"type": "object", "properties": {"verdict": {"type": "string", "enum": ["Good", "Bad"]}},
          "required": ["verdict"]}
SPEC = AgentSpec(name="critic", kind="coding", tools=(), paper_ref="", description="", variables=("x",),
                 system="s", prompt="judge {{x}}", schema=SCHEMA)

def rt_for(d, rules, caps=Caps()):
    b = MockBackend({"rules": rules})
    return AgentRuntime(b, RunStore(d), Budget(d, caps, time.time()), Routing({"default": {"model": "sonnet"}}),
                        d, specs={"critic": SPEC}, max_wait_minutes=10, sleep=lambda s: None), b

print("== A. retries are invisible to the ledger and to the caps (cap: 1 agent call, 1 coding session)")
for label, rules in (("2 transient then ok", [{"agent": "critic", "raise": "transient", "times": 2}]),
                     ("1 invalid then ok", [{"agent": "critic", "output": {"verdict": "Maybe"}, "times": 1}]),
                     ("1 usage-limit wait then ok", [{"agent": "critic", "raise": "rate_limit", "times": 1}])):
    d = fresh_dir("e2-" + label.replace(" ", "_"))
    rt, b = rt_for(d, rules, Caps(max_agent_calls=1, max_coding_sessions=1))
    rt.run("a/1", "critic", {"x": 1})
    lines = [json.loads(l) for l in (d / "ledger.jsonl").read_text().splitlines()]
    print(f"  {label:28s} backend calls={len(b.calls)}  ledger agent entries={sum(e.get('type') == 'agent' for e in lines)}"
          f"  budget.agent_calls={rt.budget.totals.agent_calls}")
d = fresh_dir("e2-exhausted")
rt, b = rt_for(d, [{"agent": "critic", "raise": "transient"}])
try:
    rt.run("a/1", "critic", {"x": 1})
except UnitFailed as e:
    print(f"  transient x3 -> UnitFailed: backend calls={len(b.calls)}, ledger exists={(d / 'ledger.jsonl').exists()}, unit stored={rt.store.has('a/1')}")

print("== B. a torn last ledger line (power loss / ENOSPC mid-append) blocks every resume")
d = fresh_dir("e2-torn")
(d / "ledger.jsonl").write_text('{"type": "agent", "key": "a/1", "kind": "coding", "seconds": 5, "equiv_usd": 0.1}\n{"type": "agent", "key": "a/2", "ki')
try:
    Budget(d, Caps(), time.time()); print("  loaded")
except Exception as e:
    print("  Budget() on resume ->", type(e).__name__, str(e)[:80])

print("== C. max_hours counts calendar time since created_at, so a usage-window pause eats it")
import scientisttwo.runtime.budget as bmod
created = time.time()
b = Budget(fresh_dir("e2-hours"), Caps(max_hours=96, max_seven_day_utilization=0.95), created)
b.windows = {"unifiedWindows": {"seven_day": {"utilization": 0.96, "resetsAt": created + 5 * 86400}}}
try:
    b.check("coding")
except BudgetExceeded as e:
    print("  day 0:", e, "| resume_after in %.1f days" % ((e.resume_after - created) / 86400))
real_time = time.time
bmod.time = types.SimpleNamespace(time=lambda: real_time() + 5 * 86400 + 120)   # resumed after the reset
try:
    b.check("coding"); print("  day 5: proceeds")
except BudgetExceeded as e:
    print("  day 5, after the window reset:", e)
