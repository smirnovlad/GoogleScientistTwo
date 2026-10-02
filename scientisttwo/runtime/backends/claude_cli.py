"""The real backend: one `claude -p` process per agent call, on the user's subscription.

docs/architecture/engine.md, section 3. Every flag below was checked against claude 2.1.287 on
2026-10-02 (DEVELOPMENT_PROCESS.md):
- `--setting-sources ""`, an empty strict MCP config and `--disable-slash-commands` keep the
  user's CLAUDE.md, hooks, plugins, skills and MCP servers away from the agent;
- `--json-schema` makes the CLI validate the output and return it as `structured_output`;
- `--output-format stream-json --verbose` gives a transcript, the `init` event (whose
  `apiKeySource` is "none" on the subscription) and `rate_limit_event`s with the usage windows.

The process runs in the call's sandbox (`SubprocessBackend.spawn`), which reaches the network
only through the engine's egress proxy, reads under $HOME only what `sandbox_reads` names, and
never writes the user's Claude setup. Its environment turns off auto-memory (else the agent
reads and writes the user's own memory folder), the auto-updater (else the binary can change
under a running run) and non-essential traffic (probe of 2026-10-02).

⛔ WHY NOT `--bare`: under it, auth is "strictly ANTHROPIC_API_KEY" and every call bills the API.
⛔ WHY NOT inherit the parent's environment: it may hold ANTHROPIC_API_KEY or ANTHROPIC_BASE_URL
(API billing), or a launching Claude session's own variables. The child gets an allowlist.
⛔ WHY NOT a per-run CLAUDE_CONFIG_DIR: the subscription login is bound to the default one; a
fresh directory answers "Not logged in" (probe of 2026-10-02).
"""
from __future__ import annotations

import json
import os
import re
import select
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, Iterator, Optional

from ...harness.sandbox import child_env
from .base import (AgentCall, AgentFailed, AgentResult, AgentTimeout, BackendError, EnvironmentFault,
                   InvalidOutput, RateLimited, SubprocessBackend, TransientError)

ISOLATION_FLAGS = ["--setting-sources", "", "--strict-mcp-config", "--mcp-config",
                   '{"mcpServers":{}}', "--disable-slash-commands", "--no-session-persistence"]
QUIET_ENV = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_AUTOUPDATER": "1",
             "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "DISABLE_TELEMETRY": "1",
             "DISABLE_ERROR_REPORTING": "1", "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1"}

# A usage-window refusal. Not "limit reached" alone: the CLI also says "context limit reached".
_LIMIT_TEXT = re.compile(r"usage limit|rate[ _-]?limit|too many requests|\b429\b|"
                         r"hit your (?:\w+ )?limit|limit (?:will )?resets?", re.I)
_TRANSIENT_TEXT = re.compile(r"overloaded|internal server error|timed? ?out|connection|ECONNRESET|"
                             r"socket hang up|\b5\d\d\b|temporarily", re.I)
# the machine failed, not the agent: a retry of the same unit would fail the same way
DRAIN_S = 10.0          # how long the reader waits for the rest of the output after a kill
_ENVIRONMENT = re.compile(r"\b(EPERM|EACCES|ENOSPC|EROFS|EMFILE|ENFILE|EDQUOT)\b|no space left", re.I)
# a refusal of the command line itself, before any session started
_USAGE_ERROR = re.compile(r"^error: |^Error: --|is not a valid|unknown option|invalid value", re.I | re.M)


def cli_schema(schema: dict) -> dict:
    """The schema as the CLI accepts it: its validator knows no meta-schema URIs, so `$schema`
    and `$id` are dropped; the engine still validates against the full schema itself."""
    return {k: v for k, v in schema.items() if k not in ("$schema", "$id")}


class ClaudeCLIBackend(SubprocessBackend):
    name = "claude_cli"

    def __init__(self, claude_bin: Optional[str] = None, allow_unsandboxed: bool = False,
                 require_subscription: bool = True, python: str = sys.executable):
        found = claude_bin or shutil.which("claude") or str(Path.home() / ".local/bin/claude")
        # pinned: the binary this run started with, even if the user's own install updates later
        self.claude_bin = os.path.realpath(found)
        self.allow_unsandboxed = allow_unsandboxed
        self.require_subscription = require_subscription
        self.python = python
        self.last_rate_limit: dict[str, Any] = {}
        self._lock = threading.Lock()

    def describe(self) -> dict[str, Any]:
        try:
            version = subprocess.run([self.claude_bin, "--version"], capture_output=True, text=True,
                                     timeout=30, env=child_env(self.python, QUIET_ENV)).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            version = "unknown"
        return {"backend": self.name, "claude_bin": self.claude_bin, "claude_version": version}

    def sandbox_reads(self) -> list[Path]:
        """Under $HOME, the CLI reads its own binary, its config file and the login keychain, and
        git its config: nothing else (probe of 2026-10-02; `~/.claude` itself is not needed)."""
        home = Path.home()
        reads = [Path(self.claude_bin), Path(self.claude_bin).parent, home / ".claude.json",
                 home / "Library" / "Keychains"]
        reads += [p for p in (home / ".gitconfig", home / ".config" / "git") if p.exists()]
        return reads

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
        return argv

    def env(self, call: AgentCall) -> dict[str, str]:
        extra = dict(QUIET_ENV)
        if call.tmpdir is not None:
            extra.update(TMPDIR=str(call.tmpdir), CLAUDE_CODE_TMPDIR=str(call.tmpdir))
        sb = call.sandbox
        if sb is not None and sb.network == "proxy":
            url = f"http://127.0.0.1:{sb.proxy_port}"
            extra.update(HTTPS_PROXY=url, HTTP_PROXY=url, https_proxy=url, http_proxy=url,
                         NO_PROXY="", no_proxy="")
        return child_env(self.python, extra)

    # ---- one call -------------------------------------------------------------------------------
    def call(self, call: AgentCall) -> AgentResult:
        transcript = open(call.transcript, "w", encoding="utf-8") if call.transcript else None
        started = time.time()
        spawned = self.spawn(call, self.argv(call), self.env(call))
        proc = spawned.proc
        killed: dict[str, Any] = {}

        def _kill(reason: str) -> None:
            if "reason" not in killed:
                killed.update(reason=reason, at=time.time())
            spawned.kill_now()                         # the whole tree, not only the CLI's group

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

        threading.Thread(target=_feed, daemon=True).start()

        def _left() -> float:
            # the reader is bounded on its own: a process that escaped every kill and still holds
            # the pipe ends the read DRAIN_S after the kill, never at that process's own exit
            end = killed["at"] + DRAIN_S if "at" in killed else started + call.timeout_s + DRAIN_S
            return end - time.time()

        try:
            assert proc.stdout is not None
            for line in _lines(proc.stdout.fileno(), _left):
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
                    break                      # the answer is in: a lingering CLI cannot lose it
        finally:
            timer.cancel()
            if transcript:
                transcript.close()
            spawned.finish(grace=1.0 if result else 3.0)
        # the tree is dead, so stderr is at its end, unless a process that escaped every kill holds
        # it: then the thread is left to that process's exit, never waited for
        err_thread.join(timeout=1.0)
        stderr = "".join(stderr_chunks)[-2000:]
        duration = time.time() - started
        if rate:
            with self._lock:
                self.last_rate_limit = rate
        return self._interpret(call, init, result, rate, stderr, proc.returncode, killed, duration)

    def _interpret(self, call: AgentCall, init: dict, result: dict, rate: dict, stderr: str,
                   returncode: Optional[int], killed: dict, duration: float) -> AgentResult:
        try:
            return self._classify(call, init, result, rate, stderr, returncode, killed, duration)
        except BackendError as e:
            # a failed result can still report its spending: the ledger keeps it, so the caps see
            # it (Codex review 2026-10-02, P2: a result reporting $12.30 was counted as unknown)
            cost = result.get("total_cost_usd")
            e.cost_usd = float(cost) if isinstance(cost, (int, float)) else None
            e.tokens = result.get("usage") or None
            e.rate_limit = rate or None                # so the window ceilings see a failed call too
            raise

    def _classify(self, call: AgentCall, init: dict, result: dict, rate: dict, stderr: str,
                  returncode: Optional[int], killed: dict, duration: float) -> AgentResult:
        if killed.get("reason", "").startswith("apiKeySource="):
            raise AgentFailed(f"{call.agent}: refused, the CLI would bill the API ({killed['reason']}); "
                              "the engine runs only on the subscription login")
        if rate.get("status") == "rejected":
            raise RateLimited(f"{call.agent}: subscription usage limit ({rate.get('rateLimitType')})",
                              reset_at=_reset_at(rate))
        if not result:
            if killed.get("reason") == "timeout":
                raise AgentTimeout(f"{call.agent}: no result after {call.timeout_s}s")
            text = stderr or f"exit code {returncode}"
            if _ENVIRONMENT.search(text):
                raise EnvironmentFault(f"{call.agent}: {text[-500:]}")
            if not init and _USAGE_ERROR.search(text):
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
            if "not logged in" in text.lower():
                raise EnvironmentFault(f"{call.agent}: the CLI is not logged in: {text[:200]}")
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
                 "model_usage": result.get("modelUsage"), "cli_version": init.get("claude_code_version")})


def _lines(fd: int, left: Callable[[], float]) -> Iterator[str]:
    """The lines on `fd` until EOF, or until `left()` reaches 0 (then a partial line is dropped)."""
    buf = b""
    while True:
        wait = left()
        if wait <= 0:
            return
        ready, _, _ = select.select([fd], [], [], min(wait, 1.0))
        if not ready:
            continue
        chunk = os.read(fd, 1 << 16)
        if not chunk:
            if buf:
                yield buf.decode("utf-8", errors="replace")
            return
        buf += chunk
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            yield line.decode("utf-8", errors="replace") + "\n"


def _reset_at(rate: dict) -> Optional[float]:
    """When the spent window resets: the refused window's own reset when the CLI names it, else
    the earliest reset among exhausted windows, else the earliest reset of any window."""
    now = time.time()
    top = rate.get("resetsAt")
    if rate.get("status") == "rejected" and isinstance(top, (int, float)) and top > now:
        return float(top)
    windows = [w for w in (rate.get("unifiedWindows") or {}).values()
               if isinstance(w, dict) and isinstance(w.get("resetsAt"), (int, float)) and w["resetsAt"] > now]
    spent = [w for w in windows if isinstance(w.get("utilization"), (int, float)) and w["utilization"] >= 1]
    pool = spent or windows
    if pool:
        return float(min(w["resetsAt"] for w in pool))
    return float(top) if isinstance(top, (int, float)) and top > now else None
