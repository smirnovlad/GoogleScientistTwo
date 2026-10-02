"""Profiles: the loop limits, stage parameters, budgets and routing of a run, as data.

`config/paper.json` is App. A.2; `config/quick.json` extends it with small limits. A profile may
`extends` another; `--set a.b=value` overrides any leaf from the command line. The merged profile
is written into the run directory, so a run is reproducible from its record (CLAUDE.md).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(__file__).resolve().parent / "config"


def deep_merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_profile(name_or_path: str) -> dict:
    p = Path(name_or_path)
    if not p.suffix:
        p = CONFIG_DIR / f"{name_or_path}.json"
    data = json.loads(p.read_text())
    parent = data.pop("extends", None)
    if parent:
        data = deep_merge(load_profile(parent), data)
    return data


def apply_overrides(profile: dict, overrides: list[str]) -> dict:
    out = copy.deepcopy(profile)
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"--set expects key.path=value, got {item!r}")
        path, raw = item.split("=", 1)
        try:
            value: Any = json.loads(raw)
        except json.JSONDecodeError:
            value = raw
        node = out
        keys = path.split(".")
        for k in keys[:-1]:
            node = node.setdefault(k, {})
        node[keys[-1]] = value
    return out


def load_routing(profile: dict) -> dict:
    routing = json.loads((CONFIG_DIR / "routing.json").read_text())
    return deep_merge(routing, profile.get("routing") or {})
