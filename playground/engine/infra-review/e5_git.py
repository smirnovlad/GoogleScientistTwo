"""A coding agent may write its workspace's .git (the sandbox allows the whole workdir)."""
from common import *
import subprocess
from scientisttwo.orchestrator import prepare, run
from scientisttwo.runtime.backends.mock import MockBackend

class AgentTouchesGit(MockBackend):
    def __init__(self, action, times=1, **kw):
        super().__init__(**kw); self.action, self.left = action, times
    def call(self, call):
        out = super().call(call)
        if call.agent == "subset_coder" and call.key.startswith("evo/r0/s1/") and self.left > 0:
            self.left -= 1
            if self.action == "lock":       # e.g. a git command killed mid-way, or the agent's own git use
                (call.cwd / ".git" / "index.lock").write_text("")
            else:                            # the agent "cleans up" history: rm -rf .git && git init && commit
                subprocess.run(f"rm -rf .git && git init -q && git add -A && git -c user.name=a -c user.email=a@b "
                               f"commit -qm agent", shell=True, cwd=call.cwd, check=True)
        return out

for action in ("lock", "reinit"):
    base = fresh_dir("e5-" + action); task = build_toy_task(base / "task")
    for incarnation in (1, 2):
        b = AgentTouchesGit(action, times=1 if incarnation == 1 else 0)
        ctx = prepare(base / "run", task if incarnation == 1 else None, quick() if incarnation == 1 else None, b,
                      sleep=lambda s: None)
        try:
            rec = run(ctx); status = rec["status"]
        except Exception as e:
            status = f"error: {type(e).__name__}: {str(e)[:110]}"
        print(f"{action:6s} incarnation {incarnation}: {status}")
        print(f"         subset_coder s1 paid this incarnation: {sum(k == 'evo/r0/s1/subset/code' for _, k in b.calls)}")
