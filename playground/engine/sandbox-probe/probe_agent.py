"""Probe: can a coding agent run on the subscription inside a tighter sandbox?

Usage: python probe_agent.py <mode> [<mode> ...]   (modes below; each is one cheap haiku call)
  net       outbound network only to the egress proxy (HTTPS_PROXY), proxy in discovery mode
  env       `net` plus CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 and DISABLE_AUTOUPDATER=1
  config    `env` plus CLAUDE_CONFIG_DIR=<a fresh directory>
  homeread  `env` plus reads under $HOME denied except an allowlist (see HOME_ALLOW)
  nostate   `env` with no write at all to ~/.claude or ~/.claude.json
  minimal   `nostate` and `homeread` together, and no write to ~/Library/Caches either

Prints the init event's auth source and memory paths, the result, and the hosts the proxy saw.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scientisttwo.harness.egress import EgressProxy          # noqa: E402
from scientisttwo.runtime.backends.claude_cli import ISOLATION_FLAGS, child_env   # noqa: E402

HOME = Path(os.path.realpath(Path.home()))
DROP = {str(HOME / x) for x in os.environ.get("PROBE_DROP", "").split(",") if x}
EXTRA = [HOME / x for x in os.environ.get("PROBE_EXTRA", "").split(",") if x]
CLAUDE = os.path.realpath(shutil.which("claude") or str(HOME / ".local/bin/claude"))


def q(p):
    return '"' + str(p).replace('"', '\\"') + '"'


def profile(work: Path, port: int, mode: str, config_dir: Path | None) -> str:
    lines = ["(version 1)", "(allow default)"]
    if mode in ("homeread", "minimal"):
        allow = [work, HOME / ".claude", HOME / ".claude.json", HOME / ".local", HOME / ".gitconfig",
                 HOME / ".config/git", Path(sys.prefix), *EXTRA]
        allow = [a for a in allow if str(a) not in DROP]
        if config_dir:
            allow.append(config_dir)
        lines.append(f"(deny file-read* (subpath {q(HOME)}))")
        lines.append("(allow file-read* " + " ".join(f"(subpath {q(os.path.realpath(p))})" for p in allow)
                     + f" (literal {q(HOME)}))")
    lines.append("(deny file-write*)")
    writable = [work, "/private/tmp", "/private/var/folders", "/dev"]
    if mode != "minimal":
        writable.append(HOME / "Library/Caches")
    if mode not in ("nostate", "minimal"):
        writable.append(HOME / ".claude")
    if config_dir:
        writable.append(config_dir)
    claude_json = "" if mode in ("nostate", "minimal") else f" (regex #\"^{re.escape(str(HOME / '.claude.json'))}\")"
    lines.append("(allow file-write* " + " ".join(f"(subpath {q(os.path.realpath(p))})" for p in writable)
                 + claude_json + ")")
    lines.append("(deny network-outbound)")
    lines.append(f"(allow network-outbound (remote ip \"localhost:{port}\"))")
    return "\n".join(lines)


def run(mode: str) -> None:
    work = Path(tempfile.mkdtemp(prefix=f"probe-{mode}-"))
    (work / "hello.txt").write_text("hi\n")
    log_path = work.parent / f"probe-{mode}-egress.jsonl"
    proxy = EgressProxy(allow=("*",), log_path=log_path)
    port = proxy.start()
    env = child_env()
    env.update({"HTTPS_PROXY": proxy.url, "HTTP_PROXY": proxy.url, "https_proxy": proxy.url,
                "http_proxy": proxy.url, "NO_PROXY": "", "no_proxy": ""})
    config_dir = None
    if mode in ("env", "config", "homeread", "nostate", "minimal"):
        env.update({"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_AUTOUPDATER": "1"})
    if mode == "config":
        config_dir = Path(tempfile.mkdtemp(prefix="probe-config-"))
        env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    argv = [CLAUDE, "-p", "--output-format", "stream-json", "--verbose", *ISOLATION_FLAGS,
            "--model", "haiku", "--tools", "Bash", "--append-system-prompt",
            "You are a test agent. Follow the instruction exactly.",
            "--permission-mode", "bypassPermissions"]
    prompt = "Run this exact Bash command: cat hello.txt && echo BASH_OK. Then reply with one word: DONE."
    sb = ["sandbox-exec", "-p", profile(work, port, mode, config_dir), *argv]
    t0 = time.time()
    p = subprocess.run(sb, input=prompt, capture_output=True, text=True, cwd=work, env=env, timeout=240)
    proxy.stop()
    init, result, tool_out = {}, {}, []
    for line in p.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            init = ev
        elif ev.get("type") == "result":
            result = ev
        elif ev.get("type") == "user":
            for c in (ev.get("message") or {}).get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    tool_out.append(str(c.get("content"))[:200])
    hosts = {}
    if log_path.exists():
        for line in log_path.read_text().splitlines():
            e = json.loads(line)
            hosts[e.get("host")] = hosts.get(e.get("host"), 0) + 1
    print(f"== mode {mode}: exit {p.returncode} in {time.time() - t0:.1f}s")
    print("   apiKeySource:", init.get("apiKeySource"), "| memory_paths:", init.get("memory_paths"))
    print("   result:", result.get("subtype"), result.get("is_error"), repr(str(result.get("result"))[:120]))
    print("   tool output:", tool_out[:2])
    print("   hosts via proxy:", hosts)
    if p.returncode != 0 or not result:
        print("   stderr tail:", p.stderr[-800:])
    shutil.rmtree(work, ignore_errors=True)
    if config_dir:
        print("   config dir after:", sorted(x.name for x in config_dir.iterdir())[:20])
        shutil.rmtree(config_dir, ignore_errors=True)


if __name__ == "__main__":
    for m in sys.argv[1:] or ["net"]:
        run(m)
