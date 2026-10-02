"""A task G: an accepted paper, its codebase, its rules and its locked harness.

The contract is docs/architecture/engine.md, section 6 (U-TOP-1, A-TOP-4 reading 2: every
experiment in the paper starts from a paper with its code). `load_task` refuses to start on any
missing piece, since a run that finds out after a day that its labels are missing has wasted a day.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

REQUIRED = ("id", "title", "paper", "rules", "code", "public_data", "entrypoint", "metric", "splits")
ENTRYPOINT_FIELDS = ("{python}", "{train_dir}", "{inputs}", "{out}", "{seed}")
SPLITS = ("subset", "full", "test")


class TaskError(ValueError):
    pass


@dataclass(frozen=True)
class Split:
    name: str
    inputs: str          # relative to the task folder; must be inside harness/
    labels: str
    seeds: tuple[int, ...]


@dataclass(frozen=True)
class Task:
    root: Path
    id: str
    title: str
    paper_text: str
    rules_text: str
    code_dir: Path
    public_data_dir: Path
    harness_dir: Path
    entrypoint: str
    metric_name: str
    direction: str                     # "max" or "min"
    metric_module: str                 # relative to the task folder, inside harness/
    splits: dict[str, Split]
    eval_timeout_s: int
    coding_timeout_s: int
    reported: str
    deny_read: tuple[Path, ...] = ()           # more paths no agent and no evaluated code may read
    forbidden_in_diff: tuple[str, ...] = ()    # strings an evaluated change may not add
    allow_data_files: bool = False             # may a change add data files (binary, .npz, .csv …)?
    min_delta: Optional[float] = None          # the task's noise floor for "strictly better"
    raw: dict = field(default_factory=dict)

    @property
    def metric_info(self) -> dict[str, Any]:
        return {"name": self.metric_name, "direction": self.direction,
                "better": "higher is better" if self.direction == "max" else "lower is better"}


def ensure_prepared(root: Path, d: dict) -> None:
    """Run the task's `prepare` command once if any data file it generates is missing.

    Generated data stays out of git: it is rebuilt deterministically, and the run pins it by hash.
    """
    command = d.get("prepare")
    if not command:
        return
    wanted = [root / s[p] for s in d.get("splits", {}).values() for p in ("inputs", "labels")]
    public = root / d.get("public_data", "data/public")
    if all(p.exists() for p in wanted) and public.is_dir() and any(public.iterdir()):
        return
    import subprocess
    import sys
    r = subprocess.run(command.format(python=sys.executable), shell=True, cwd=root,
                       capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        raise TaskError(f"the task's prepare command failed: {(r.stdout + r.stderr)[-1500:]}")


def load_task(path: Path | str) -> Task:
    root = Path(path).expanduser().resolve()
    manifest = root / "task.json"
    if not manifest.exists():
        raise TaskError(f"no task.json in {root}")
    d = json.loads(manifest.read_text())
    ensure_prepared(root, d)
    missing = [k for k in REQUIRED if k not in d]
    if missing:
        raise TaskError(f"task.json lacks {missing}")
    for token in ENTRYPOINT_FIELDS:
        if token not in d["entrypoint"]:
            raise TaskError(f"entrypoint must contain {token}: {d['entrypoint']!r}")
    metric = d["metric"]
    if metric.get("direction") not in ("max", "min"):
        raise TaskError("metric.direction must be 'max' or 'min'")
    harness_dir = (root / "harness").resolve()
    splits = {}
    for name in SPLITS:
        s = d["splits"].get(name)
        if not s:
            raise TaskError(f"task.json lacks split {name!r}")
        for part in ("inputs", "labels"):
            p = (root / s[part]).resolve()
            if not p.exists():
                raise TaskError(f"split {name}: {s[part]} does not exist")
            if harness_dir not in p.parents:
                raise TaskError(f"split {name}: {s[part]} must be inside harness/, which agents cannot read")
        seeds = tuple(int(x) for x in s.get("seeds", [0]))
        if not seeds:
            raise TaskError(f"split {name}: no seeds")
        splits[name] = Split(name, s["inputs"], s["labels"], seeds)
    module = metric.get("module", "harness/metric.py")
    if harness_dir not in (root / module).resolve().parents:
        raise TaskError("metric.module must be inside harness/")
    for rel in (d["paper"], d["rules"], module):
        if not (root / rel).exists():
            raise TaskError(f"{rel} does not exist")
    for rel in (d["code"], d["public_data"]):
        if not (root / rel).is_dir():
            raise TaskError(f"{rel} is not a directory")
    timeouts = d.get("timeouts", {})
    reported = d.get("reported", "")
    if isinstance(reported, dict):
        reported = reported.get("text") or json.dumps(reported)
    deny_read = tuple(Path(_expand(x)).expanduser() for x in d.get("deny_read", []))
    return Task(root=root, id=d["id"], title=d["title"],
                paper_text=(root / d["paper"]).read_text(), rules_text=(root / d["rules"]).read_text(),
                code_dir=(root / d["code"]).resolve(), public_data_dir=(root / d["public_data"]).resolve(),
                harness_dir=harness_dir, entrypoint=d["entrypoint"], metric_name=metric.get("name", "metric"),
                direction=metric["direction"], metric_module=module, splits=splits,
                eval_timeout_s=int(timeouts.get("evaluation_seconds", 600)),
                coding_timeout_s=int(timeouts.get("coding_session_seconds", 2400)),
                reported=str(reported), deny_read=deny_read,
                forbidden_in_diff=tuple(str(x) for x in d.get("forbidden_in_diff", [])),
                allow_data_files=bool(d.get("allow_data_files", False)),
                min_delta=float(d["min_delta"]) if d.get("min_delta") is not None else None, raw=d)


def _expand(template: str) -> str:
    """`{site_packages}`: the engine's own Python's packages, which evaluated code also uses."""
    import sysconfig
    return template.format(site_packages=sysconfig.get_paths()["purelib"])


TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".cfg", ".sh", ".ini", ".rst"}
# ⛔ WHY NOT the whole codebase in every prompt: a real codebase runs to megabytes. The overview
# carries the tree and every text file up to OVERVIEW_FILE_CHARS each, OVERVIEW_TOTAL_CHARS in all
# (our choice, 2026-10-02); what it loses is the tail of large files, which the coding agents read
# themselves from their workspace.
OVERVIEW_FILE_CHARS = 12000
OVERVIEW_TOTAL_CHARS = 60000


def code_overview(code_dir: Path) -> str:
    code_dir = Path(code_dir)
    files = sorted(p for p in code_dir.rglob("*") if p.is_file() and ".git" not in p.parts
                   and "__pycache__" not in p.parts)
    tree = "\n".join(str(p.relative_to(code_dir)) for p in files)
    parts, total = [f"File tree:\n{tree}\n"], 0
    readmes = [p for p in files if p.name.lower().startswith("readme")]
    for p in readmes + [p for p in files if p not in readmes]:
        if p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = p.read_text(errors="replace")
        if len(text) > OVERVIEW_FILE_CHARS:
            text = text[:OVERVIEW_FILE_CHARS] + f"\n[... {len(text) - OVERVIEW_FILE_CHARS} more characters]"
        if total + len(text) > OVERVIEW_TOTAL_CHARS:
            parts.append(f"\n[{p.relative_to(code_dir)} and later files omitted: overview cap reached]")
            break
        parts.append(f"\n===== {p.relative_to(code_dir)} =====\n{text}")
        total += len(text)
    return "\n".join(parts)
