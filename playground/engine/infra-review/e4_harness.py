"""Harness._run: after the timeout kill, communicate() has no bound; a child in its own session that
holds stdout keeps the engine thread blocked for as long as it lives."""
from common import *
import json, time
from scientisttwo.task import load_task
from scientisttwo.harness.harness import Harness
from scientisttwo.workspace import Workspaces
base = fresh_dir("e4"); root = build_toy_task(base / "task")
d = json.loads((root / "task.json").read_text()); d["timeouts"]["evaluation_seconds"] = 2
(root / "task.json").write_text(json.dumps(d))
task = load_task(root); h = Harness(task, base / "run"); h.install()
ws = Workspaces(base / "run"); ws.init_from(task.code_dir, "base", "b")
tmp = ws.fresh("base", "daemon")
(tmp / "run.py").write_text("import subprocess, time\n"
                            "subprocess.Popen(['/bin/sleep', '15'], start_new_session=True)\n"
                            "time.sleep(60)\n")
ws.finalize(tmp, "daemon", "d")
t = time.time()
r = h.evaluate("x", ws.path("daemon"), "subset")
print("eval timeout 2 s; evaluate() returned after %.1f s; status=%s error=%s" % (time.time() - t, r["status"], r["error"]))
