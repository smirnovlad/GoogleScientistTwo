"""Probe: can a process under the engine's own evaluation policy read the task's ORIGINAL labels?
Builds the policy exactly as scientisttwo/harness/harness.py:129 does, with the engine's sandbox.py
(loaded read-only by file path), around a stand-in run directory."""
import importlib.util, os, shutil, subprocess, sys
E, T, W = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("sbx", os.path.join(E, "scientisttwo/harness/sandbox.py"))
sbx = importlib.util.module_from_spec(spec); sys.modules["sbx"] = sbx; spec.loader.exec_module(sbx)
run = os.path.join(W, "run"); copy = os.path.join(run, "harness", "files", "labels")
os.makedirs(copy, exist_ok=True); shutil.copy(os.path.join(T, "harness/labels/test.npz"), copy)
evald, ws, public = (os.path.join(run, d) for d in ("evals/k", "workspaces/v1", "public_data"))
for d in (evald, ws, public): os.makedirs(d, exist_ok=True)
policy = sbx.SandboxPolicy.build(writable=[evald], readonly=[ws, public], denied=[os.path.join(run, "harness")],
                                 protected=[run, T], network=False)
reader = "import sys, numpy as np; y = np.load(sys.argv[1])['y']; print('READ', len(y), 'labels, first 10:', y[:10].tolist())"
for name, path in [("control: the run's denied harness copy", os.path.join(copy, "test.npz")),
                   ("the task's ORIGINAL test labels", os.path.join(T, "harness/labels/test.npz")),
                   ("the task's ORIGINAL full labels", os.path.join(T, "harness/labels/full.npz"))]:
    p = subprocess.run(sbx.wrap([sys.executable, "-c", reader, path], policy), capture_output=True, text=True, cwd=ws)
    out = (p.stdout + p.stderr).strip().splitlines()
    print(f"{name}: exit {p.returncode}: {out[-1][:110] if out else ''}")
