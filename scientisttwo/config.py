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


# What each stage may set, and the exhaustion rules its code can honour (architecture review
# 2026-10-02, finding 2: a setting the code ignores must be refused, not accepted silently).
STAGE_RULES = {
    "limitations": {"exhaustion": ("keep_last",)},             # a set is needed to go on (§3.1)
    "subset": {"exhaustion": ("discard",)},                    # exhausted → Bad (§3.2)
    "full": {"exhaustion": ("discard",)},
    "ablation": {"exhaustion": ("keep_best",), "extra": ("reject_ends_run", "reject_share")},
    "peer_review": {"exhaustion": ("keep_last", "keep_best")},  # U-TOP-7's two readings
    "meta": {"exhaustion": ("keep_best",)},
}
LIMITS = ("limitation_rounds", "n_seed", "n0", "n_eng_subset", "n_eng_full", "n_k", "n_e", "K", "S",
          "n_p", "n_abl", "review_threshold", "n_t", "n_peer", "n_meta")
TOP_KEYS = {"name", "description", "limits", "stages", "guard", "integrity", "parallel", "budget",
            "rate_limit", "retries", "routing", "export"}


class ProfileError(ValueError):
    pass


def validate_profile(profile: dict) -> None:
    """Refuse a profile whose settings the engine would not honour."""
    unknown = set(profile) - TOP_KEYS
    if unknown:
        raise ProfileError(f"unknown profile keys {sorted(unknown)}")
    limits = profile.get("limits", {})
    missing = [k for k in LIMITS if k not in limits]
    extra = [k for k in limits if k not in LIMITS]
    if missing or extra:
        raise ProfileError(f"limits: missing {missing}, unknown {extra}")
    bad = [k for k in LIMITS if not isinstance(limits[k], int) or limits[k] < 0]
    if bad:
        raise ProfileError(f"limits must be integers >= 0: {bad}")
    for name, cfg in (profile.get("stages") or {}).items():
        rules = STAGE_RULES.get(name)
        if rules is None:
            raise ProfileError(f"unknown stage {name!r}")
        allowed_keys = {"counting", "exhaustion", *rules.get("extra", ())}
        if set(cfg) - allowed_keys:
            raise ProfileError(f"stages.{name}: unknown keys {sorted(set(cfg) - allowed_keys)}")
        if "exhaustion" in cfg and cfg["exhaustion"] not in rules["exhaustion"]:
            raise ProfileError(f"stages.{name}.exhaustion must be one of {rules['exhaustion']}, "
                               f"not {cfg['exhaustion']!r}: the stage's code cannot honour it")
        if cfg.get("counting", "refinements") not in ("refinements", "critic_calls"):
            raise ProfileError(f"stages.{name}.counting must be 'refinements' or 'critic_calls'")
    share = (profile.get("stages") or {}).get("ablation", {}).get("reject_share")
    if share is not None and not (isinstance(share, (int, float)) and 0 < share <= 1):
        raise ProfileError("stages.ablation.reject_share must be in (0, 1]")
