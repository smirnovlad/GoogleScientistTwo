#!/usr/bin/env python3
"""MODE=linger: a result, then the process stays 8 s. MODE=spawn: a detached child (new session, as
Claude Code's Bash tool runs) keeps writing a heartbeat; the CLI itself hangs. MODE=slow: hangs."""
import json, os, subprocess, sys, time
mode = os.environ.get("FAKE_MODE") or open(os.path.join(os.path.dirname(__file__), "mode.txt")).read().strip()
sys.stdin.read()
here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, "cli.pid"), "w").write(str(os.getpid()))
def emit(e): print(json.dumps(e), flush=True)
emit({"type": "system", "subtype": "init", "apiKeySource": "none", "model": "fake", "session_id": "s"})
if mode == "linger":
    emit({"type": "result", "subtype": "success", "is_error": False, "result": "{}", "structured_output":
          {"verdict": "Good"}, "total_cost_usd": 1.23, "session_id": "s"})
    time.sleep(8)
elif mode == "spawn":
    hb = os.path.join(here, "heartbeat.txt")
    child = subprocess.Popen([sys.executable, "-c",
        f"import os,time\nopen({hb!r},'w').write(str(os.getpid())+'\\n')\n"
        f"for i in range(60):\n    open({hb!r},'a').write('.')\n    time.sleep(0.5)"],
        start_new_session=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(60)
else:
    time.sleep(25)
