"""Stand-in for the engine's locked harness (docs/architecture/engine.md section 6), which
is not built yet: per split, copy the code, the public data and the split's inputs to fresh
directories, run the task's entrypoint once per seed, score with the task's metric.py.
Each (split, seed) runs `--repeat` times to check that the predictions are identical."""
import argparse, hashlib, importlib.util, json, os, shlex, shutil, subprocess, sys, tempfile, time
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("task"); ap.add_argument("--code", default=None)
ap.add_argument("--splits", default="subset,full,test"); ap.add_argument("--repeat", type=int, default=2)
ap.add_argument("--python", default=sys.executable); ap.add_argument("--seeds", default=None); ap.add_argument("--out", required=True)
a = ap.parse_args()
task = json.load(open(os.path.join(a.task, "task.json"))) if os.path.exists(os.path.join(a.task, "task.json")) else None
spec = importlib.util.spec_from_file_location("metric", os.path.join(a.task, "harness/metric.py"))
metric = importlib.util.module_from_spec(spec); spec.loader.exec_module(metric)
entry = "{python} run.py --train-dir {train_dir} --inputs {inputs} --out {out} --seed {seed}"
seeds = {"subset": [0], "full": [0, 1, 2], "test": [0, 1, 2]}
if task:
    entry = task["entrypoint"]; seeds = {k: v["seeds"] for k, v in task["splits"].items()}
    timeout = task["timeouts"]["evaluation_seconds"]
else:
    timeout = 120
env = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "SHELL", "LANG", "TERM", "TMPDIR") if k in os.environ}
env["PATH"] = os.path.dirname(a.python) + ":/usr/bin:/bin:/usr/sbin:/sbin"
if a.seeds:
    lo, hi = map(int, a.seeds.split("-")); seeds = {k: list(range(lo, hi + 1)) for k in seeds}
records = []
for split in a.splits.split(","):
    for seed in seeds[split]:
        hashes = []
        for rep in range(a.repeat):
            root = tempfile.mkdtemp(prefix=f"h_{split}_{seed}_{rep}_")
            ws, train_dir, inp_dir, out_dir = (os.path.join(root, d) for d in ("ws", "train", "in", "out"))
            shutil.copytree(a.code or os.path.join(a.task, "code"), ws)
            shutil.copytree(os.path.join(a.task, "data/public"), train_dir)
            os.makedirs(inp_dir); os.makedirs(out_dir)
            inputs = os.path.join(inp_dir, "inputs.npz"); shutil.copy(os.path.join(a.task, f"harness/inputs/{split}.npz"), inputs)
            out = os.path.join(out_dir, "predictions.npy")
            cmd = entry.format(python=shlex.quote(a.python), train_dir=shlex.quote(train_dir), inputs=shlex.quote(inputs), out=shlex.quote(out), seed=seed)
            t0 = time.perf_counter()
            p = subprocess.run(cmd, shell=True, cwd=ws, env=env, capture_output=True, text=True, timeout=timeout)
            wall = time.perf_counter() - t0
            if p.returncode != 0:
                print(f"FAILED {split} seed {seed}: rc={p.returncode}\n{p.stderr[-2000:]}"); sys.exit(1)
            r = metric.score(out, os.path.join(a.task, f"harness/labels/{split}.npz"))
            h = hashlib.sha256(open(out, "rb").read()).hexdigest(); hashes.append(h)
            stderr_lines = [l for l in p.stderr.splitlines() if l.strip()]
            records.append({"split": split, "seed": seed, "rep": rep, **r, "wall_s": round(wall, 3),
                            "pred_sha256": h[:16], "stdout": p.stdout.strip(), "stderr_lines": stderr_lines})
            print(f"{split:6s} seed={seed} rep={rep} acc={r['primary']:.4f} ({r['n_correct']}/{r['n']}) macro_f1={r['macro_f1']:.4f} wall={wall:.2f}s pred={h[:12]} | {p.stdout.strip()}")
            for l in stderr_lines: print(f"         stderr: {l[:160]}")
            shutil.rmtree(root)
        print(f"         determinism {split} seed {seed}: {'IDENTICAL' if len(set(hashes)) == 1 else 'DIFFERENT'} predictions over {len(hashes)} runs")
json.dump(records, open(a.out, "w"), indent=1)
print("\nSUMMARY (rep 0; sd = sample sd, ddof=1)")
for split in a.splits.split(","):
    rs = [r for r in records if r["split"] == split and r["rep"] == 0]
    acc = np.array([r["primary"] for r in rs]); f1 = np.array([r["macro_f1"] for r in rs]); wall = np.array([r["wall_s"] for r in rs])
    sd = lambda v: v.std(ddof=1) if len(v) > 1 else float("nan")
    print(f"{split:6s} n={rs[0]['n']} seeds={[r['seed'] for r in rs]} acc={[round(x, 4) for x in acc]} mean={acc.mean():.4f} sd={sd(acc):.4f} "
          f"macro_f1 mean={f1.mean():.4f} sd={sd(f1):.4f} | wall per run mean={wall.mean():.2f}s max={wall.max():.2f}s, split total={wall.sum():.2f}s")
