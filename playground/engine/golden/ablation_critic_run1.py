#!/usr/bin/env python3
"""Golden case: the ablation critic, given run 1's real inputs, must answer `Reject`.

LIVE: one `claude -p` call per case, on the subscription, through the engine's own runtime (spec,
render, routing, CLI backend). It is NOT part of the $0 suite: run it by hand whenever the ablation
critic's prompt, schema or route changes, and record the verdict with its sample.

Why `Reject` [App. B; engine.md §7, `reject_share`]. In run digits-quick-1 (engine commit 7e3f0c3,
2026-10-02) the selected idea, PCS-Init, scored 0.987929 on the full validation split against the
reproduced baseline's 0.911792, a gain of 0.076137. Its ablation A1 sets INIT=glorot and keeps
FOLD_STD: the idea's own mechanism is off (the PCS hidden initialisation, and the ridge head, which
is unused in that branch), and only input standardisation, a generic control, is left. A1 scores
0.975859: it keeps 84.1% of the gain, above reject_share = 0.5, so the gain is "primarily driven by
general training controls" (App. B, the TeCh case). Run 1's own critic, which was not given the
baseline, answered `Good` (units/abl/p0/critic/0.json).

The control case (--with-control) is SYNTHETIC: numbers made up in the shape the paper describes for
LC-FTT (Tab. 16: the critic stripped the machinery "down to the lone component that carried the
gain"). One own component carries the gain, three are useless, and there is no generic control.
It must stay `Refine`, so that a `Reject` on run 1 shows the rule rather than a critic that rejects
everything.

The run-1 inputs are frozen below in exactly the shape the stage passes (stages/ablation.py,
critic()), built from run 1's result files with the engine's own summarize() and gain_text().
`runs/` is not in git, so the copy here is what makes the case re-runnable; `--check-fixture`
rebuilds it from a run directory, for $0, and fails if anything differs.

  python3 playground/engine/golden/ablation_critic_run1.py [--with-control] [--model M] [--effort E]
  python3 playground/engine/golden/ablation_critic_run1.py --check-fixture runs/digits-quick-1

Exit 0: every case gave its expected verdict. 1: a verdict differed. 2: a call could not be made.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import statistics
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
AGENT = "ablation_critic"
# The profile value the engine passes (engine.md §7: stages.ablation.reject_share). Run 1 predates
# the variable, so the case supplies it; --reject-share overrides it.
REJECT_SHARE = 0.5

RUN1 = json.loads(r"""{
 "task_title": "TinyMLP: A 2,410-Parameter Perceptron for Low-Resolution Handwritten Digits",
 "metric": {
  "name": "accuracy",
  "direction": "max",
  "better": "higher is better"
 },
 "idea": {
  "title": "Prototype-Initialised, Class-Conditional Subspace Hidden Layer (PCS-Init MLP)",
  "summary": "Replace random Glorot initialisation of the 64-32-10 MLP with a data-derived, class-conditional PCA-subspace initialisation: the 32 hidden units start as discriminative directions computed in closed form from train.npz (per-class principal directions plus Fisher/LDA directions), and the output layer starts at the least-squares solution on those hidden features. Fine-tuning then starts from a near-solved point, so the short budget no longer decides the result and seed variance collapses. It targets L1, L2 and L3 through a deterministic structured initialisation, which is a different mechanism from the pool's augmentation, ensembling and distillation ideas.",
  "addresses": [
   "L1",
   "L2",
   "L3"
  ],
  "method": "All code in model.py and run.py; torch or numpy, CPU. Architecture stays 64-32-10 ReLU (2,410 parameters).\n\nC1 Input conditioning folded into layer 1: compute train mean mu and std sd (floor 1e-2). Standardised z=(x-mu)/sd is absorbed into W1,b1 after init, so the network still reads raw counts. Switch: FOLD_STD.\n\nC2 Discriminative hidden init (L1, L3): on z, compute (a) the top K_LDA=9 Fisher/LDA directions (sklearn LinearDiscriminantAnalysis with solver='eigen', shrinkage=0.1), and (b) for each class c, the top 2 principal directions of that class's z (20 directions), giving 29 directions. Add 3 further directions: the top global PCs 1-3. Total 32 rows, each L2-normalised and scaled to norm sqrt(2) (He scale). Each row is paired with a sign: to let ReLU keep both polarities, the 9 LDA directions use +w, and the other rows use +w. The bias is set so each unit's pre-activation on train has mean +0.5 std (b=-w.mean + 0.5*std). The seed enters only through a random orthogonal rotation of the class-PCA rows in the tie-breaking subspace plus small Gaussian noise (sd 0.05 of row norm) added to all rows, so seeds still differ slightly but start near the same solution. Switch: INIT=pcs vs glorot.\n\nC3 Closed-form output layer (L2): compute H=relu(Z W1^T+b1) on train, then solve ridge regression to one-hot targets (lambda=1.0), scaled by 4 to give logits, as the initial W2,b2. Switch: RIDGE_HEAD.\n\nC4 Fine-tuning: Adam lr 1e-3 (unchanged), batch 200, L2 1e-4, the original 50 epochs, so the compute budget is unchanged and the original training loop is kept. Implement in torch (or via sklearn MLPClassifier with warm_start=True, setting coefs_ and intercepts_ after one partial_fit call). Prediction is argmax; each row depends only on the trained model and that row. Only train statistics are used.\n\nAblations: glorot init + same standardisation fold; PCS init without fine-tuning (diagnostic); RIDGE_HEAD off.",
  "implementation_plan": [
   "In model.py add compute_init(X_train, y_train, seed) returning W1, b1, W2, b2 following C1-C3 using numpy and sklearn LDA/PCA.",
   "Add a build_model(seed) wrapper that creates MLPClassifier(warm_start=True, max_iter=EPOCHS), calls a one-step partial_fit with classes to allocate, overwrites coefs_ and intercepts_, then continues fit; or implement an equivalent torch loop with the same hyperparameters.",
   "Update run.py to call the wrapper, keeping the CLI, the output format and the check_finite check; log the pre-fine-tune train accuracy.",
   "Expose the switches FOLD_STD, INIT and RIDGE_HEAD as constants at the top of model.py.",
   "Run seeds 0-2 on subset and full, test determinism by running twice, and run the ablations."
  ],
  "expected_effect": "Accuracy on subset, full and test should rise from about 0.91 to roughly 0.94-0.96 at the same parameter count and epoch budget, with seed sd falling below about 0.008, because initialisation sits near a good discriminative solution and the seed only perturbs it. The gain should be largest where the baseline underfits (seeds with high final loss). Macro-F1 should follow.",
  "risks": "The ridge/LDA init may overfit the 1,079 training images, so fine-tuning from a low-train-loss point could generalise no better; this would show as train accuracy near 1.0 with an unchanged held-out gap. ReLU units with the +0.5 std bias may be dead for some classes; check the fraction of active units in the logs. Part of the gain may come from standardisation alone, so ablate with standardised Glorot init. Seed variance may be reduced only because the init is near-deterministic, which is the intended effect."
 },
 "best_result": {
  "split": "full",
  "status": "ok",
  "error": null,
  "metric": "accuracy",
  "direction": "max",
  "mean": 0.9879294336118849,
  "std": 0.003216436040053641,
  "n_seeds": 3,
  "scores": [
   {
    "seed": 0,
    "primary": 0.9860724233983287,
    "n": 359,
    "n_correct": 354,
    "macro_f1": 0.9861095032906724
   },
   {
    "seed": 1,
    "primary": 0.9860724233983287,
    "n": 359,
    "n_correct": 354,
    "macro_f1": 0.9861095032906724
   },
   {
    "seed": 2,
    "primary": 0.9916434540389972,
    "n": 359,
    "n_correct": 356,
    "macro_f1": 0.9916655947863742
   }
  ]
 },
 "baseline_result": {
  "split": "full",
  "status": "ok",
  "error": null,
  "metric": "accuracy",
  "direction": "max",
  "mean": 0.9117920148560817,
  "std": 0.017019779739854593,
  "n_seeds": 3,
  "scores": [
   {
    "seed": 0,
    "primary": 0.9080779944289693,
    "n": 359,
    "n_correct": 326,
    "macro_f1": 0.9083123821675283
   },
   {
    "seed": 1,
    "primary": 0.8969359331476323,
    "n": 359,
    "n_correct": 322,
    "macro_f1": 0.8971088462813673
   },
   {
    "seed": 2,
    "primary": 0.9303621169916435,
    "n": 359,
    "n_correct": 334,
    "macro_f1": 0.9310006614315144
   }
  ]
 },
 "gain": "+0.076137 in accuracy (an improvement; higher is better); new mean 0.987929 ± 0.003216 over 3 seed(s), reference mean 0.911792 ± 0.017020 over 3 seed(s); the engine counts a gain as real only above its margin of 0, and this one is above it",
 "ablations": [
  {
   "id": "A1",
   "plan": {
    "id": "A1",
    "component": "Class-conditional PCS hidden-layer initialisation (C2: LDA + per-class PCA + global PC directions)",
    "change": "In model.py set INIT = \"glorot\" while keeping FOLD_STD = True, so build_model still returns PCSMLP and compute_init takes the glorot branch (Glorot weights in standardised space, folded into W1/b1, zero b2). RIDGE_HEAD is unused in that branch. Training loop, 50 epochs, Adam lr 1e-3, batch 200, L2 1e-4 and seeds 0-2 are unchanged.",
    "hypothesis": "If the discriminative subspace init matters, full-split accuracy falls clearly below 0.988 and seed std rises. If accuracy stays near 0.985-0.99, the gain comes from standardisation or from fine-tuning, not from the PCS init."
   },
   "result": {
    "split": "full",
    "status": "ok",
    "error": null,
    "metric": "accuracy",
    "direction": "max",
    "mean": 0.9758588672237698,
    "std": 0.0016082180200267884,
    "n_seeds": 3,
    "scores": [
     {
      "seed": 0,
      "primary": 0.9777158774373259,
      "n": 359,
      "n_correct": 351,
      "macro_f1": 0.9777724158931953
     },
     {
      "seed": 1,
      "primary": 0.9749303621169917,
      "n": 359,
      "n_correct": 350,
      "macro_f1": 0.9750320632017904
     },
     {
      "seed": 2,
      "primary": 0.9749303621169917,
      "n": 359,
      "n_correct": 350,
      "macro_f1": 0.9749908405966673
     }
    ]
   },
   "delta_vs_full_method": -0.0120705663881151,
   "agent_error": null
  },
  {
   "id": "A2",
   "plan": {
    "id": "A2",
    "component": "Closed-form ridge output layer (C3, RIDGE_HEAD)",
    "change": "In model.py set RIDGE_HEAD = False with INIT = \"pcs\" and FOLD_STD = True. compute_init then keeps the PCS hidden layer and uses the random Glorot-uniform W2 with zero b2 (the existing else branch). Everything else is unchanged.",
    "hypothesis": "If the ridge head matters, accuracy drops and seed variance rises, and pre-fine-tune train accuracy falls to near chance. If accuracy is unchanged, 50 epochs of fine-tuning recover the head and the ridge solve is redundant."
   },
   "result": {
    "split": "full",
    "status": "ok",
    "error": null,
    "metric": "accuracy",
    "direction": "max",
    "mean": 0.9712163416898792,
    "std": 0.005798512533331865,
    "n_seeds": 3,
    "scores": [
     {
      "seed": 0,
      "primary": 0.9777158774373259,
      "n": 359,
      "n_correct": 351,
      "macro_f1": 0.9777253737500112
     },
     {
      "seed": 1,
      "primary": 0.9693593314763231,
      "n": 359,
      "n_correct": 348,
      "macro_f1": 0.9694708695558966
     },
     {
      "seed": 2,
      "primary": 0.9665738161559888,
      "n": 359,
      "n_correct": 347,
      "macro_f1": 0.9665798380652125
     }
    ]
   },
   "delta_vs_full_method": -0.016713091922005652,
   "agent_error": null
  }
 ]
}""")


def derive(run_dir: Path) -> dict:
    """Rebuild the run-1 inputs from a run directory, as stages/ablation.py's critic() builds them."""
    from scientisttwo.harness.harness import gain, summarize
    from scientisttwo.stages.common import gain_text
    from scientisttwo.task import load_task

    def read(rel: str) -> dict:
        return json.loads((run_dir / rel).read_text())

    run = read("run.json")
    task = load_task(run["task_path"] if Path(run["task_path"]).is_absolute() else ROOT / run["task_path"])
    min_delta = float(run["profile"].get("guard", {}).get("min_delta", 0.0))
    chosen = read("units/select.json")["output"]["choice"]
    idea = next(t["idea"] for t in read("traces.json") if t["id"] == chosen)
    core = read(f"results/evo/r0/{chosen}/full/eval0.json")
    base = read("results/base/eval/full.json")
    plans = read("units/abl/p0/a0/plan.json")["output"]["plans"]
    ablations = []
    for plan in plans:
        result = read(f"results/abl/p0/a0/{plan['id']}/eval.json")
        ablations.append({"id": plan["id"], "plan": plan, "result": summarize(result),
                          "delta_vs_full_method": gain(result, core), "agent_error": None})
    return {"task_title": task.title, "metric": task.metric_info, "idea": idea,
            "best_result": summarize(core), "baseline_result": summarize(base),
            "gain": gain_text(core, base, task, min_delta), "ablations": ablations}


def _result(metric: str, scores: list[float]) -> dict:
    return {"split": "full", "status": "ok", "error": None, "metric": metric, "direction": "max",
            "mean": statistics.fmean(scores), "std": statistics.stdev(scores), "n_seeds": len(scores),
            "scores": [{"seed": i, "primary": s} for i, s in enumerate(scores)]}


def lcftt_shape() -> dict:
    """SYNTHETIC control, in LC-FTT's shape (Tab. 16): the expected verdict is `Refine`."""
    m = "qd_score"
    base, full = _result(m, [100.0, 101.0, 99.0]), _result(m, [110.2, 109.8, 110.0])
    variants = [
        ("A1", "C1 dimension-adaptive smoothness penalty", "Set the penalty weight to 0 (SMOOTH=False).",
         [100.8, 101.2, 101.0]),
        ("A2", "C2 Fisher-Rao warping of the measure space", "Use the Euclidean metric (FISHER_RAO=False).",
         [110.1, 109.9, 110.3]),
        ("A3", "C3 tensor-train factorisation of the discount model",
         "Replace the tensor train by the original dense MLP (TT=False).", [109.7, 110.3, 110.0]),
        ("A4", "C4 Legendrian contact constraint", "Drop the constraint term (CONTACT=False).",
         [110.4, 110.0, 110.2]),
    ]
    ablations = []
    for vid, comp, change, scores in variants:
        r = _result(m, scores)
        ablations.append({"id": vid, "plan": {"id": vid, "component": comp, "change": change,
                                              "hypothesis": f"If {comp} matters, the QD score falls."},
                          "result": r, "delta_vs_full_method": r["mean"] - full["mean"], "agent_error": None})
    g = full["mean"] - base["mean"]
    idea = {"title": "Smooth, Factorised, Contact-Constrained Discount Model (SFC-DM)",
            "summary": "Four components for the discount model of a quality-diversity search: a "
                       "dimension-adaptive smoothness penalty (C1), Fisher-Rao warping of the measure "
                       "space (C2), a tensor-train factorisation (C3) and a Legendrian contact constraint (C4).",
            "addresses": ["L1", "L2", "L3"],
            "method": "C1 adds a gradient-norm penalty on the discount model, scaled with the measure "
                      "dimension. C2 warps distances by the Fisher-Rao metric. C3 factorises the "
                      "model as a tensor train of rank 4. C4 adds a contact-form constraint term.",
            "implementation_plan": ["Add C1 to the loss.", "Add C2 to the distance.",
                                    "Replace the MLP by a tensor train.", "Add the C4 term."],
            "expected_effect": "Higher QD score in high-dimensional measure spaces.",
            "risks": "The factorisation may underfit."}
    return {"task_title": "Quality-diversity search with a learned discount model",
            "metric": {"name": m, "direction": "max", "better": "higher is better"}, "idea": idea,
            "best_result": full, "baseline_result": base,
            "gain": (f"{g:+.6f} in {m} (an improvement; higher is better); new mean {full['mean']:.6f} ± "
                     f"{full['std']:.6f} over 3 seed(s), reference mean {base['mean']:.6f} ± "
                     f"{base['std']:.6f} over 3 seed(s); the engine counts a gain as real only above its "
                     f"margin of 0, and this one is above it"),
            "ablations": ablations}


def call_critic(variables: dict, model: str | None, effort: str | None) -> tuple[dict, dict]:
    """One call, as the engine makes it: the agent's own spec, the routing table, the CLI backend.

    ⛔ WHY NOT the engine's sandbox and egress proxy: this agent has no tools and runs no command,
    so they would add nothing to the test of its judgement; the backend still applies the CLI
    isolation flags, the environment allowlist and the subscription-only guard.
    """
    from scientisttwo.runtime.agents import AgentSpec, Routing
    from scientisttwo.runtime.backends.base import AgentCall
    from scientisttwo.runtime.backends.claude_cli import ClaudeCLIBackend

    spec = AgentSpec.load(ROOT / "scientisttwo" / "agents" / AGENT)
    route = Routing(json.loads((ROOT / "scientisttwo" / "config" / "routing.json").read_text())).route(spec)
    model, effort = model or route.model, effort or route.effort
    version = hashlib.sha256((spec.system + spec.prompt + json.dumps(spec.schema, sort_keys=True))
                             .encode()).hexdigest()[:16]
    with tempfile.TemporaryDirectory() as tmp:
        call = AgentCall(agent=AGENT, kind=spec.kind, system=spec.system, user=spec.render(variables),
                         schema=spec.schema, model=model, effort=effort, tools=spec.tools,
                         cwd=Path(tmp), sandbox=None, timeout_s=route.timeout_s,
                         transcript=Path(tmp) / "transcript.jsonl", key=f"golden/{AGENT}")
        result = ClaudeCLIBackend(allow_unsandboxed=True).call(call)
    record = {"model": result.raw.get("model"), "effort": effort, "prompt_version": version,
              "tokens": result.tokens, "equiv_usd": result.cost_usd,
              "seconds": round(result.duration_s, 1), "num_turns": result.raw.get("num_turns"),
              "api_key_source": result.raw.get("api_key_source")}
    return result.output or {}, record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--with-control", action="store_true", help="also run the synthetic LC-FTT control")
    ap.add_argument("--model"), ap.add_argument("--effort")
    ap.add_argument("--reject-share", type=float, default=REJECT_SHARE)
    ap.add_argument("--check-fixture", metavar="RUN_DIR", help="rebuild run 1's inputs ($0) and compare")
    args = ap.parse_args()

    if args.check_fixture:
        rebuilt = derive(Path(args.check_fixture))
        same = json.dumps(rebuilt, sort_keys=True) == json.dumps(RUN1, sort_keys=True)
        print(json.dumps({"fixture_matches_run": same, "run_dir": args.check_fixture}))
        return 0 if same else 1

    cases = [("run1", RUN1, "Reject")] + ([("lcftt_shape (synthetic)", lcftt_shape(), "Refine")]
                                          if args.with_control else [])
    status = 0
    for name, variables, expected in cases:
        try:
            output, record = call_critic({**variables, "reject_share": args.reject_share},
                                         args.model, args.effort)
        except Exception as exc:  # any backend failure: the case could not be judged
            print(json.dumps({"case": name, "error": f"{type(exc).__name__}: {exc}"[:500]}))
            return 2
        verdict = output.get("verdict")
        status = max(status, 0 if verdict == expected else 1)
        print(json.dumps({"case": name, "expected": expected, "verdict": verdict,
                          "pass": verdict == expected, "reject_share": args.reject_share,
                          "date": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                          **record, "feedback": output.get("feedback")}, ensure_ascii=False, indent=1))
    return status


if __name__ == "__main__":
    sys.exit(main())
