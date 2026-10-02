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
if scenario == "crash":
    sys.stderr.write("segfault-ish\n")
    sys.exit(2)
if scenario == "error429":
    emit({"type": "result", "subtype": "error", "is_error": True, "api_error_status": 429,
          "result": "Claude AI usage limit reached"})
    sys.exit(1)
if scenario == "overloaded":
    emit({"type": "result", "subtype": "error", "is_error": True, "api_error_status": 529,
          "result": "Overloaded"})
    sys.exit(1)
structured = None if scenario == "noschema" else {"verdict": "Good", "feedback": "fine"}
emit({"type": "result", "subtype": "success", "is_error": False, "result": json.dumps(structured),
      "structured_output": structured, "total_cost_usd": 0.0123, "num_turns": 2,
      "usage": {"input_tokens": 10, "output_tokens": 20}, "session_id": "s-1"})
