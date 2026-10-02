"""The real backend: one `claude -p` process per agent call, on the user's subscription.

docs/architecture/engine.md, section 3. Every flag below was checked against claude 2.1.287 on
2026-10-02 (DEVELOPMENT_PROCESS.md):
- `--setting-sources ""`, an empty strict MCP config and `--disable-slash-commands` keep the
  user's CLAUDE.md, hooks, plugins, skills and MCP servers away from the agent;
- `--json-schema` makes the CLI validate the output and return it as `structured_output`;
- `--output-format stream-json --verbose` gives a transcript, the `init` event (whose
  `apiKeySource` is "none" on the subscription) and `rate_limit_event`s with the usage windows.

⛔ WHY NOT `--bare`: under it, auth is "strictly ANTHROPIC_API_KEY" and every call bills the API.
⛔ WHY NOT inherit the parent's environment: it may hold ANTHROPIC_API_KEY or ANTHROPIC_BASE_URL
(API billing), or a launching Claude session's own variables. The child gets an allowlist.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Optional

from ...harness import sandbox as sbx
from .base import (AgentCall, AgentFailed, AgentResult, AgentTimeout, Backend, InvalidOutput,
                   RateLimited, TransientError)

ISOLATION_FLAGS = ["--setting-sources", "", "--strict-mcp-config", "--mcp-config",
                   '{"mcpServers":{}}', "--disable-slash-commands", "--no-session-persistence"]

_LIMIT_TEXT = re.compile(r"usage limit|rate limit|limit reached|too many requests|\b429\b", re.I)
_TRANSIENT_TEXT = re.compile(r"overloaded|internal server error|timed? ?out|connection|ECONNRESET|"
                             r"\b5\d\d\b|temporarily", re.I)


# a refusal of the command line itself: retrying the same arguments cannot help
_USAGE_ERROR = re.compile(r"^error: |Error: --|is not a valid|unknown option|invalid value", re.I | re.M)


def cli_schema(schema: dict) -> dict:
    """The schema as the CLI accepts it: its validator knows no meta-schema URIs, so `$schema`
    and `$id` are dropped; the engine still validates against the full schema itself."""
    return {k: v for k, v in schema.items() if k not in ("$schema", "$id")}


def child_env(python: str = sys.executable) -> dict[str, str]:
    """The allowlisted environment of every agent process."""
    home = str(Path.home())
    path = [str(Path(python).parent), str(Path(home) / ".local" / "bin"), "/opt/homebrew/bin",
            "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin"]
    env = {"HOME": home, "USER": os.environ.get("USER", ""), "LOGNAME": os.environ.get("USER", ""),
           "SHELL": "/bin/zsh" if Path("/bin/zsh").exists() else "/bin/sh",
           "LANG": os.environ.get("LANG", "en_US.UTF-8"), "TERM": "xterm-256color",
           "PATH": os.pathsep.join(dict.fromkeys(path))}
    if os.environ.get("TMPDIR"):
        env["TMPDIR"] = os.environ["TMPDIR"]
    return env


class ClaudeCLIBackend(Backend):
    name = "claude_cli"

    def __init__(self, claude_bin: Optional[str] = None, allow_unsandboxed: bool = False,
                 require_subscription: bool = True):
        self.claude_bin = claude_bin or shutil.which("claude") or str(Path.home() / ".local/bin/claude")
        self.allow_unsandboxed = allow_unsandboxed
        self.require_subscription = require_subscription
        self.last_rate_limit: dict[str, Any] = {}
        self._lock = threading.Lock()

    def describe(self) -> dict[str, Any]:
        try:
            version = subprocess.run([self.claude_bin, "--version"], capture_output=True, text=True,
                                     timeout=30, env=child_env()).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            version = "unknown"
        return {"backend": self.name, "claude_bin": self.claude_bin, "claude_version": version}

    # ---- command line -------------------------------------------------------------------------
    def argv(self, call: AgentCall) -> list[str]:
        argv = [self.claude_bin, "-p", "--output-format", "stream-json", "--verbose",
                *ISOLATION_FLAGS, "--model", call.model, "--tools", ",".join(call.tools)]
        if call.effort:
            argv += ["--effort", call.effort]
        if call.kind == "reasoning":
            argv += ["--system-prompt", call.system]
            if call.tools:
                # print mode denies a tool that needs approval: approve exactly the declared ones
                argv += ["--allowedTools", ",".join(call.tools)]
        else:
            # keep Claude Code's own tool instructions; the sandbox, not prompts, bounds the agent
            argv += ["--append-system-prompt", call.system, "--permission-mode", "bypassPermissions"]
        if call.schema is not None:
            argv += ["--json-schema", json.dumps(cli_schema(call.schema))]
        return sbx.wrap(argv, call.sandbox, self.allow_unsandboxed)

    # ---- one call -------------------------------------------------------------------------------
    def call(self, call: AgentCall) -> AgentResult:
        argv = self.argv(call)
        cwd = str(call.cwd) if call.cwd else None
        transcript = open(call.transcript, "w", encoding="utf-8") if call.transcript else None
        started = time.time()
        proc = subprocess.Popen(argv, cwd=cwd, env=child_env(), stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                start_new_session=True)
        killed: dict[str, str] = {}

        def _kill(reason: str) -> None:
            killed["reason"] = reason
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

        timer = threading.Timer(call.timeout_s, _kill, args=("timeout",))
        timer.start()
        init: dict = {}
        result: dict = {}
        rate: dict = {}
        stderr_chunks: list[str] = []
        err_thread = threading.Thread(target=lambda: stderr_chunks.append(proc.stderr.read()), daemon=True)
        err_thread.start()
        def _feed() -> None:
            # its own thread: a prompt larger than the pipe buffer must not block the reader
            try:
                assert proc.stdin is not None
                proc.stdin.write(call.user)
                proc.stdin.close()
            except (BrokenPipeError, OSError):
                pass

        feeder = threading.Thread(target=_feed, daemon=True)
        feeder.start()
        try:
            assert proc.stdout is not None
            for line in proc.stdout:
                if transcript:
                    transcript.write(line)
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                kind = event.get("type")
                if kind == "system" and event.get("subtype") == "init":
                    init = event
                    source = event.get("apiKeySource")
                    if self.require_subscription and source not in (None, "none"):
                        _kill(f"apiKeySource={source}")
                elif kind == "rate_limit_event":
                    rate = event.get("rate_limit_info") or {}
                elif kind == "result":
                    result = event
            proc.wait()
        finally:
            timer.cancel()
            if transcript:
                transcript.close()
        err_thread.join(timeout=5)
        stderr = "".join(stderr_chunks)[-2000:]
        duration = time.time() - started
        if rate:
            with self._lock:
                self.last_rate_limit = rate

        if killed.get("reason") == "timeout":
            raise AgentTimeout(f"{call.agent}: no result after {call.timeout_s}s")
        if killed.get("reason", "").startswith("apiKeySource="):
            raise AgentFailed(f"{call.agent}: refused, the CLI would bill the API ({killed['reason']}); "
                              "the engine runs only on the subscription login")
        if rate.get("status") == "rejected":
            raise RateLimited(f"{call.agent}: subscription usage limit ({rate.get('rateLimitType')})",
                              reset_at=_reset_at(rate))
        if not result:
            text = stderr or f"exit code {proc.returncode}"
            if _USAGE_ERROR.search(text):
                raise AgentFailed(f"{call.agent}: the CLI refused its arguments: {text[-500:]}")
            if _LIMIT_TEXT.search(text):
                raise RateLimited(f"{call.agent}: {text[-300:]}", reset_at=_reset_at(rate))
            raise TransientError(f"{call.agent}: the CLI ended without a result: {text[-500:]}")
        if result.get("is_error"):
            text = str(result.get("result") or result.get("subtype") or "")
            status = result.get("api_error_status")
            if status == 429 or _LIMIT_TEXT.search(text):
                raise RateLimited(f"{call.agent}: {text[:300]}", reset_at=_reset_at(rate))
            if (isinstance(status, int) and status >= 500) or _TRANSIENT_TEXT.search(text):
                raise TransientError(f"{call.agent}: {text[:500]}")
            if result.get("subtype") == "error_max_structured_output_retries":
                raise InvalidOutput(f"{call.agent}: {text[:500]}")
            raise AgentFailed(f"{call.agent}: {result.get('subtype')}: {text[:500]}")

        output = result.get("structured_output")
        if call.schema is not None and not isinstance(output, dict):
            raise InvalidOutput(f"{call.agent}: no structured output in the result")
        cost = result.get("total_cost_usd")
        return AgentResult(
            output=output, text=str(result.get("result") or ""),
            cost_usd=float(cost) if isinstance(cost, (int, float)) else None,
            duration_s=duration, tokens=result.get("usage") or {},
            session_id=result.get("session_id") or init.get("session_id"),
            raw={"model": init.get("model"), "api_key_source": init.get("apiKeySource"),
                 "num_turns": result.get("num_turns"), "rate_limit": rate,
                 "model_usage": result.get("modelUsage")})


def _reset_at(rate: dict) -> Optional[float]:
    for value in (rate.get("resetsAt"), *(w.get("resetsAt") for w in
                                         (rate.get("unifiedWindows") or {}).values()
                                         if isinstance(w, dict))):
        if isinstance(value, (int, float)) and value > time.time():
            return float(value)
    return None
