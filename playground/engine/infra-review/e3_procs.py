from common import *
import os, signal, subprocess, sys, time, pathlib
from scientisttwo.runtime.backends.claude_cli import ClaudeCLIBackend
from scientisttwo.runtime.backends.base import AgentCall, AgentTimeout
HERE = pathlib.Path(__file__).parent
FAKE = str(HERE / "fake_cli.py")
def call(timeout):
    return AgentCall(agent="a", kind="coding", system="s", user="u", schema={"type": "object"}, model="m",
                     effort=None, tools=(), cwd=None, sandbox=None, timeout_s=timeout, transcript=None, key="k")
def alive(pid):
    try: os.kill(pid, 0); return True
    except ProcessLookupError: return False

print("== D. a result arrives at t=0, the CLI lingers past the timeout")
(HERE / "mode.txt").write_text("linger")
t = time.time()
try:
    r = ClaudeCLIBackend(claude_bin=FAKE).call(call(3)); print("  returned the result", r.output)
except AgentTimeout as e:
    print("  after %.1fs: AgentTimeout (%s), the delivered result ($1.23) is discarded" % (time.time() - t, e))

print("== E. timeout kill vs. a child in its own session (Claude Code's Bash tool does this)")
(HERE / "mode.txt").write_text("spawn"); hb = HERE / "heartbeat.txt"; hb.unlink(missing_ok=True)
try:
    ClaudeCLIBackend(claude_bin=FAKE).call(call(2))
except AgentTimeout:
    pass
child = int(hb.read_text().splitlines()[0]); n0 = len(hb.read_text()); time.sleep(2); n1 = len(hb.read_text())
print("  after AgentTimeout: CLI alive=%s, its child alive=%s, child still writing=%s" %
      (alive(int((HERE / "cli.pid").read_text())), alive(child), n1 > n0))
os.kill(child, signal.SIGKILL)

print("== F. the engine is SIGKILLed mid-call (crash, OOM, closed terminal): the claude child")
(HERE / "mode.txt").write_text("slow"); (HERE / "cli.pid").unlink(missing_ok=True)
driver = subprocess.Popen([sys.executable, "-c",
    "import sys; sys.path.insert(0, %r); from e3_procs_lib import go; go()" % str(HERE)])
for _ in range(50):
    if (HERE / "cli.pid").exists(): break
    time.sleep(0.1)
time.sleep(0.5); driver.kill(); driver.wait()
pid = int((HERE / "cli.pid").read_text()); time.sleep(0.5)
print("  engine dead; its claude child (pid %d) alive=%s" % (pid, alive(pid)))
if alive(pid): os.kill(pid, signal.SIGKILL)
