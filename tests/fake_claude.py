#!/usr/bin/env python3
"""A stand-in for `claude -p --output-format stream-json`, for the backend's tests.

The prompt (stdin) chooses the scenario with a line `SCENARIO=<name>`. Every call records its
argv and environment in `$TMPDIR/fake_claude_last_call.json`.
"""
import json
import os
import sys
import time
from pathlib import Path

prompt = sys.stdin.read()
scenario = "success"
for line in prompt.splitlines():
    if line.startswith("SCENARIO="):
        scenario = line.split("=", 1)[1].strip()
(Path(os.environ.get("TMPDIR", "/tmp")) / "fake_claude_last_call.json").write_text(json.dumps({"argv": sys.argv[1:], "env": dict(os.environ)}))


def emit(event):
    print(json.dumps(event), flush=True)


if scenario == "usage":
    sys.stderr.write("error: unknown option '--frobnicate'\n")
    sys.exit(1)
if scenario == "eperm":
    sys.stderr.write("Error: EPERM: operation not permitted, open '/x/.claude.json'\n")
    sys.exit(1)
if scenario == "context":
    sys.stderr.write("API Error: context limit reached for this model\n")
    sys.exit(1)
source = "ANTHROPIC_API_KEY" if scenario == "apikey" else "none"
emit({"type": "system", "subtype": "init", "apiKeySource": source, "model": "fake-model", "session_id": "s-1"})
window = {"five_hour": {"utilization": 0.4, "resetsAt": int(time.time()) + 3600},
          "seven_day": {"utilization": 0.5, "resetsAt": int(time.time()) + 86400}}
status = "rejected" if scenario == "ratelimit" else "allowed"
emit({"type": "rate_limit_event", "rate_limit_info": {"status": status, "resetsAt": int(time.time()) + 3600,
                                                      "rateLimitType": "five_hour", "unifiedWindows": window}})
if scenario == "apikey":
    time.sleep(5)          # would bill the API: the backend must kill it before the result
if scenario == "slow":
    time.sleep(30)
if scenario == "orphan":
    # a detached grandchild in its own session, as the Bash tool's shell is: it must not outlive the call
    import subprocess
    beat = next((Path(l.split("=", 1)[1].strip()) for l in prompt.splitlines() if l.startswith("BEAT=")),
                Path(os.environ.get("TMPDIR", "/tmp")) / "fake_claude_orphan.txt")
    subprocess.Popen([sys.executable, "-c", (
        "import time, sys\n"
        f"p = {str(beat)!r}\n"
        "while True:\n"
        "    open(p, 'a').write('beat\\n'); time.sleep(0.2)\n")], start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if scenario in ("holder", "escaped_holder"):
    # a descendant in a session of its own that keeps the output pipe open, then a CLI that hangs.
    # "escaped_holder" also drops the unit's environment, so neither the watcher's marker nor a
    # live parent leads to it once its parent is gone: only the bounded reader ends the call
    import subprocess
    pid_file = next((Path(l.split("=", 1)[1].strip()) for l in prompt.splitlines() if l.startswith("PIDFILE=")),
                    Path(os.environ.get("TMPDIR", "/tmp")) / "fake_claude_holder.pid")
    hold = f"import os, time; open({str(pid_file)!r}, 'w').write(str(os.getpid())); time.sleep(30)"
    if scenario == "holder":
        subprocess.Popen([sys.executable, "-c", hold], start_new_session=True)
    else:
        spawn = ("import subprocess, sys; subprocess.Popen([sys.executable, '-c', " + repr(hold)
                 + "], start_new_session=True, env={'PATH': '/usr/bin:/bin'})")
        subprocess.Popen([sys.executable, "-c", spawn], env={"PATH": "/usr/bin:/bin"}).wait()
    time.sleep(30)
if scenario == "crash":
    sys.stderr.write("segfault-ish\n")
    sys.exit(2)
if scenario == "error429":
    emit({"type": "result", "subtype": "error", "is_error": True, "api_error_status": 429,
          "result": "Claude AI usage limit reached"})
    sys.exit(1)
if scenario == "costly_error":
    emit({"type": "result", "subtype": "error_max_turns", "is_error": True, "result": "",
          "total_cost_usd": 12.30, "usage": {"input_tokens": 900, "output_tokens": 100}})
    sys.exit(1)
if scenario == "overloaded":
    emit({"type": "result", "subtype": "error", "is_error": True, "api_error_status": 529,
          "result": "Overloaded"})
    sys.exit(1)
structured = None if scenario == "noschema" else {"verdict": "Good", "feedback": "fine"}
emit({"type": "result", "subtype": "success", "is_error": False, "result": json.dumps(structured),
      "structured_output": structured, "total_cost_usd": 0.0123, "num_turns": 2,
      "usage": {"input_tokens": 10, "output_tokens": 20}, "session_id": "s-1"})
if scenario == "linger":
    time.sleep(30)         # the result is out; a CLI that hangs now must not lose it
