"""The egress proxy: the only way out of an agent's sandbox.

An agent session must reach the Anthropic API, and nothing else. A coding agent with the open
internet can fetch a public benchmark's evaluation labels and bake them into its code, which no
check of its diff can reliably see (integrity review 2026-10-02, finding 2). So the sandbox denies
every outbound connection except one, to this proxy on 127.0.0.1, and the proxy opens a tunnel
only to an allowlisted host. Every request is logged, allowed or not.

⛔ WHY NOT filter by host in the sandbox profile: SBPL's network filters accept only `localhost`
or `*` as the host, so a profile can allow "port 443 anywhere" or "nothing", never "this host".
⛔ WHY NOT an HTTP proxy that reads the traffic: the agent's API traffic is TLS; a CONNECT tunnel
needs no certificate and sees the host it is asked for, which is all the policy needs.
"""
from __future__ import annotations

import json
import logging
import socket
import threading
import time
from pathlib import Path
from typing import Iterable, Optional

log = logging.getLogger("scientisttwo")

# What Claude Code needs on the subscription: the API, OAuth refresh and its own services
# (probe of 2026-10-02, DEVELOPMENT_PROCESS.md). A task may add hosts (task.json `network_allow`).
DEFAULT_ALLOW = ("api.anthropic.com", "*.anthropic.com", "claude.ai", "*.claude.ai",
                 "claude.com", "*.claude.com")
_HEADER_LIMIT = 16384


def host_allowed(host: str, allow: Iterable[str]) -> bool:
    host = host.lower().rstrip(".")
    for pattern in allow:
        p = pattern.lower().rstrip(".")
        if p == "*":                                  # discovery only: every host
            return True
        if p.startswith("*."):
            if host.endswith(p[1:]) and host != p[2:]:
                return True
        elif host == p:
            return True
    return False


class EgressProxy:
    """A CONNECT-only proxy on 127.0.0.1. `start()` returns its port."""

    def __init__(self, allow: Iterable[str] = DEFAULT_ALLOW, log_path: Optional[Path] = None,
                 ports: Iterable[int] = (443,)):
        self.allow = tuple(allow)
        self.ports = tuple(ports)
        self.log_path = Path(log_path) if log_path else None
        self.port = 0
        self._sock: Optional[socket.socket] = None
        self._stop = threading.Event()
        self._log_lock = threading.Lock()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def start(self) -> int:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 0))
        s.listen(64)
        self._sock, self.port = s, s.getsockname()[1]
        threading.Thread(target=self._accept, name="egress-proxy", daemon=True).start()
        return self.port

    def stop(self) -> None:
        self._stop.set()
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass

    # ---- internals ------------------------------------------------------------------------------
    def _accept(self) -> None:
        assert self._sock is not None
        while not self._stop.is_set():
            try:
                conn, _ = self._sock.accept()
            except OSError:
                return
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()

    def _record(self, **entry) -> None:
        if self.log_path is None:
            return
        line = json.dumps({"time": round(time.time(), 3), **entry})
        with self._log_lock:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

    def _handle(self, conn: socket.socket) -> None:
        upstream = None
        try:
            conn.settimeout(30)
            head = b""
            while b"\r\n\r\n" not in head:
                chunk = conn.recv(4096)
                if not chunk or len(head) > _HEADER_LIMIT:
                    return
                head += chunk
            request_line = head.split(b"\r\n", 1)[0].decode("latin-1")
            parts = request_line.split()
            if len(parts) < 2 or parts[0].upper() != "CONNECT":
                self._record(request=request_line[:200], allowed=False, why="only CONNECT is served")
                conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\nContent-Length: 0\r\n\r\n")
                return
            host, _, port_s = parts[1].rpartition(":")
            port = int(port_s) if port_s.isdigit() else -1
            host = host.strip("[]")
            if port not in self.ports or not host_allowed(host, self.allow):
                self._record(host=host, port=port, allowed=False)
                conn.sendall(b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n")
                return
            upstream = socket.create_connection((host, port), timeout=30)
            self._record(host=host, port=port, allowed=True)
            conn.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
            rest = head.split(b"\r\n\r\n", 1)[1]
            if rest:
                upstream.sendall(rest)
            conn.settimeout(None)
            upstream.settimeout(None)
            t = threading.Thread(target=_pipe, args=(upstream, conn), daemon=True)
            t.start()
            _pipe(conn, upstream)
            t.join(timeout=5)
        except (OSError, ValueError) as e:
            log.debug("egress proxy: %s", e)
        finally:
            for s in (conn, upstream):
                if s is not None:
                    try:
                        s.close()
                    except OSError:
                        pass


def _pipe(src: socket.socket, dst: socket.socket) -> None:
    try:
        while True:
            data = src.recv(65536)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except OSError:
            pass
