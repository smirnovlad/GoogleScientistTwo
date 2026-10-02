#!/usr/bin/env python3
"""Check the agent data in scientisttwo/agents/ against section 7 of docs/architecture/engine.md.

For every agent folder it proves:
  1. the folder holds exactly agent.json, system.md, prompt.md and schema.json, and each loads;
  2. agent.json has its six keys, and its name, paper_ref, kind, tools and variables match the
     agent's row of section 7; kind and tools follow KIND_TOOLS;
  3. the {{placeholders}} of prompt.md equal agent.json's variables, and system.md has none;
  4. schema.json is valid under Draft 2020-12 and under Draft 7, plain enough for
     `claude -p --json-schema` (a keyword allowlist: no $schema, $ref or $defs), closed at every
     object level (additionalProperties false, every field required), and its fields, enums,
     bounds and IDEA objects match the Output column;
  5. under both drafts, the schema accepts a minimal valid output and rejects every mutation of
     it: an unexpected field at each object level, each required field removed, each enum, bound
     and type broken;
  6. the prompt names every output field; the reasoning prompt says the answer is the structured
     output; and the "Rules of the workspace" section is word for word the same across the agents
     of one kind, since the four-file contract forces a copy of it into each.
Across agents: the 27 names equal section 7's, and the held-out judge never mentions the in-loop
review loop. A self-test then corrupts a temporary copy in known ways and shows that each
corruption is caught, so a pass comes from a check that can fail.

Run: python3 playground/engine/check_agents.py      exit 0 = pass, 1 = problems
"""
import copy
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = ROOT / "scientisttwo" / "agents"
ENGINE_MD = ROOT / "docs" / "architecture" / "engine.md"

FILES = {"agent.json", "system.md", "prompt.md", "schema.json"}
AGENT_KEYS = {"name", "kind", "tools", "paper_ref", "description", "variables"}
KIND_TOOLS = {  # set by the task brief of 2026-10-02; reasoning extras come from section 7's row
    "reasoning": [],
    "coding": ["Bash", "Read", "Edit", "Write", "Glob", "Grep"],
    "writer": ["Read", "Edit", "Write", "Glob", "Grep", "Bash"],
    "readonly": ["Read", "Glob", "Grep", "Bash"],
}
# Only these keywords were exercised against the CLI; anything else needs its own smoke test.
# No "$schema": claude 2.1.287 refuses the 2020-12 meta-schema URI with 'no schema with key or ref
# "https://json-schema.org/draft/2020-12/schema"' (smoke test, 2026-10-02), the message of a
# validator on another draft [inferred]. So every schema is checked under Draft 2020-12 (the brief)
# and Draft 7, and these keywords mean the same in both.
SCHEMA_KEYWORDS = {"type", "properties", "required", "additionalProperties", "items", "enum",
                   "minimum", "maximum", "minItems", "maxItems", "anyOf", "description"}
VALIDATORS = (jsonschema.Draft202012Validator, jsonschema.Draft7Validator)
SHARED_HEADING = "## Rules of the workspace"
REQUIRED_PHRASES = {
    "reasoning": ["structured output"],
    "coding": ["Operation not permitted", "holdout", "entrypoint", "structured output"],
    "writer": ["\\input", "Operation not permitted", "structured output"],
    "readonly": ["read-only", "line numbers", "Operation not permitted", "structured output"],
}
# The judge we report is not the reviewer we optimise against (CLAUDE.md): its prompt must not
# know the review loop exists.
HELD_OUT_FORBIDDEN = {"final_judge": ["scholarpeer", "peer review", "peer-review", "peer reviewer",
                                      "rebuttal", "in-loop", "meta-review", "optimis", "optimiz"]}
PLACEHOLDER = re.compile(r"\{\{(.*?)\}\}", re.S)
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


# ---------------------------------------------------------------- section 7 of engine.md

def split_top(text):
    """Split at commas that are not nested in (), [] or {}."""
    parts, depth, cur = [], 0, ""
    for ch in text:
        depth += ch in "([{"
        depth -= ch in ")]}"
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def closing(text, start):
    depth = 0
    for i in range(start, len(text)):
        depth += text[i] in "([{"
        depth -= text[i] in ")]}"
        if depth == 0:
            return i
    raise ValueError(f"unbalanced: {text!r}")


def parse_object(text):
    """Parse section 7's notation, e.g. `{verdict: Good|Bad, refs: [{title}] (≤ 2), n: 1–10}`."""
    text = text.strip()
    if not (text.startswith("{") and text.endswith("}")):
        raise ValueError(f"not an object: {text!r}")
    fields = {}
    for part in split_top(text[1:-1]):
        key, sep, spec = part.partition(":")
        fields[key.strip()] = parse_value(spec.strip() if sep else "")
    return {"kind": "object", "fields": fields}


def parse_value(spec):
    if not spec:
        return {"kind": "any"}
    m = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", spec)
    if m:
        return {"kind": "int", "min": int(m[1]), "max": int(m[2])}
    if spec in ("IDEA", "IDEA or null"):
        return {"kind": "idea", "nullable": spec != "IDEA"}
    if spec.startswith("["):
        end = closing(spec, 0)
        inner, rest = spec[1:end].strip(), spec[end + 1:].strip()
        max_items = None
        if rest:
            m = re.fullmatch(r"\(≤\s*(\d+)\)", rest)
            if not m:
                raise ValueError(f"unknown array suffix: {rest!r}")
            max_items = int(m[1])
        items = parse_object(inner) if inner.startswith("{") else None
        return {"kind": "array", "items": items, "max": max_items}
    if re.fullmatch(r"\w+(\|\w+)+", spec):
        return {"kind": "enum", "values": spec.split("|")}
    raise ValueError(f"unknown output notation: {spec!r}")


def parse_section7(text):
    sec = text.split("## 7. Agents", 1)[1].split("\n## ", 1)[0]
    m = re.search(r"An `IDEA` object is `(\{.*?\})`", " ".join(sec.split()))
    idea = parse_object(m.group(1))
    rows = {}
    for line in sec.splitlines():
        if not line.startswith("| ") or line.startswith("| Agent") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        name, paper, kind_tools, variables, output = cells
        kind_part, _, extra = kind_tools.partition(",")
        kind = kind_part.strip().replace("read-only", "readonly")
        tools = list(KIND_TOOLS.get(kind, []))
        if kind == "reasoning" and extra.strip():
            tools = extra.strip().split("/")
        out = re.search(r"`(\{.*?\})`", output).group(1).replace("\\|", "|")
        rows[name] = {"paper_ref": paper, "kind": kind, "tools": tools,
                      "variables": [v.strip() for v in variables.split(",")],
                      "output": parse_object(out)}
    return rows, idea


# ---------------------------------------------------------------- schema checks

def walk(node, path="$"):
    yield path, node
    if not isinstance(node, dict):
        return
    for key, sub in node.get("properties", {}).items():
        yield from walk(sub, f"{path}.{key}")
    if isinstance(node.get("items"), dict):
        yield from walk(node["items"], f"{path}[]")
    for i, alt in enumerate(node.get("anyOf", [])):
        yield from walk(alt, f"{path}|{i}")


def check_plain(schema, say):
    if schema.get("type") != "object":
        say("$: the top level must be an object (the CLI requires it)")
    if "$schema" in schema:
        say("$: no $schema key: the CLI refuses the 2020-12 meta-schema URI")
    for path, node in walk(schema):
        extra = set(node) - SCHEMA_KEYWORDS
        if extra:
            say(f"{path}: keywords outside the CLI-tested allowlist: {sorted(extra)}")
        if node.get("type") == "object" or "properties" in node:
            if node.get("additionalProperties") is not False:
                say(f"{path}: object without additionalProperties: false")
            if set(node.get("required", [])) != set(node.get("properties", {})):
                say(f"{path}: required {sorted(node.get('required', []))} != fields "
                    f"{sorted(node.get('properties', {}))}")


def check_spec(node, spec, idea, path, say):
    kind = spec["kind"]
    if kind == "object":
        if node.get("type") != "object":
            return say(f"{path}: section 7 has an object here")
        have, want = set(node.get("properties", {})), set(spec["fields"])
        if have != want:
            say(f"{path}: fields {sorted(have)} != section 7's {sorted(want)}")
        for key in want & have:
            check_spec(node["properties"][key], spec["fields"][key], idea, f"{path}.{key}", say)
    elif kind == "int":
        if (node.get("type"), node.get("minimum"), node.get("maximum")) != \
                ("integer", spec["min"], spec["max"]):
            say(f"{path}: want an integer in [{spec['min']}, {spec['max']}]")
    elif kind == "enum":
        if node.get("type") != "string" or set(node.get("enum", [])) != set(spec["values"]):
            say(f"{path}: enum {node.get('enum')} != section 7's {spec['values']}")
    elif kind == "array":
        if node.get("type") != "array":
            return say(f"{path}: section 7 has an array here")
        if spec["max"] is not None and node.get("maxItems") != spec["max"]:
            say(f"{path}: maxItems {node.get('maxItems')} != section 7's {spec['max']}")
        if spec["items"] is not None:
            check_spec(node.get("items", {}), spec["items"], idea, f"{path}[]", say)
    elif kind == "idea":
        target = node
        if spec["nullable"]:
            alts = node.get("anyOf")
            if not (isinstance(alts, list) and len(alts) == 2 and {"type": "null"} in alts):
                return say(f"{path}: want anyOf [IDEA, {{'type': 'null'}}]")
            target = next(a for a in alts if a != {"type": "null"})
        check_spec(target, idea, idea, f"{path}<IDEA>", say)


def example(node):
    """A minimal instance that the schema must accept."""
    if "enum" in node:
        return node["enum"][0]
    if "anyOf" in node:
        return example(node["anyOf"][0])
    kind = node.get("type")
    if kind == "object":
        return {k: example(v) for k, v in node.get("properties", {}).items()}
    if kind == "array":
        n = min(max(1, node.get("minItems", 0)), node.get("maxItems", 1))
        return [example(node["items"]) for _ in range(n)]
    return {"string": "x", "integer": node.get("minimum", 0), "boolean": True,
            "null": None}[kind]


def mutants(node, value):
    """(label, instance) pairs that the schema must reject."""
    if "anyOf" in node:
        yield from mutants(node["anyOf"][0], value)
        return
    if "enum" in node:
        yield "a value outside the enum", "__not_allowed__"
        return
    kind = node.get("type")
    if kind == "object":
        yield "an unexpected field", {**value, "__unexpected__": "x"}
        for key in node.get("required", []):
            yield f"'{key}' removed", {k: v for k, v in value.items() if k != key}
        for key, sub in node.get("properties", {}).items():
            for label, bad in mutants(sub, value[key]):
                yield f"{key}: {label}", {**value, key: bad}
    elif kind == "array":
        if "maxItems" in node:
            yield "too many items", [value[0]] * (node["maxItems"] + 1)
        if node.get("minItems", 0) >= 1:
            yield "no items", []
        for label, bad in mutants(node["items"], value[0]):
            yield f"[0]: {label}", [bad] + value[1:]
    elif kind == "integer":
        if "minimum" in node:
            yield "below the minimum", node["minimum"] - 1
        if "maximum" in node:
            yield "above the maximum", node["maximum"] + 1
        yield "not an integer", 1.5
    elif kind == "string":
        yield "not a string", 7
    elif kind == "boolean":
        yield "not a boolean", "yes"


def check_behaviour(schema, say, validator_cls):
    """Accept the minimal output (and each anyOf branch at the top), reject every mutant."""
    validator = validator_cls(schema)
    draft = validator_cls.__name__.replace("Validator", "")
    try:
        good = [example(schema)]
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        say(f"cannot build an example output to test the schema ({type(exc).__name__}: {exc})")
        return 0
    for key, sub in schema.get("properties", {}).items():
        for alt in sub.get("anyOf", [])[1:]:
            good.append({**good[0], key: example(alt)})
    for instance in good:
        errors = list(validator.iter_errors(instance))
        if errors:
            say(f"{draft} rejects a valid output: {errors[0].message}")
    count = 0
    for label, bad in mutants(schema, good[0]):
        count += 1
        if validator.is_valid(bad):
            say(f"{draft} accepts an invalid output: {label}")
    return count


# ---------------------------------------------------------------- one agent, then all

def section(text, heading):
    if heading not in text:
        return None
    after = text.split(heading, 1)[1]
    nxt = re.search(r"\n## ", after)
    return heading + (after[:nxt.start()] if nxt else after)


def check_agent(folder, row, idea, say):
    names = {p.name for p in folder.iterdir() if not p.name.startswith(".")}
    if names != FILES:
        say(f"files {sorted(names)} != {sorted(FILES)}")
        if not FILES <= names:
            return None
    try:
        spec = json.loads((folder / "agent.json").read_text())
        schema = json.loads((folder / "schema.json").read_text())
    except json.JSONDecodeError as exc:
        say(f"invalid JSON: {exc}")
        return None
    system = (folder / "system.md").read_text()
    prompt = (folder / "prompt.md").read_text()

    if set(spec) != AGENT_KEYS:
        say(f"agent.json keys {sorted(spec)} != {sorted(AGENT_KEYS)}")
    if spec.get("name") != folder.name:
        say(f"agent.json name {spec.get('name')!r} != folder {folder.name!r}")
    for key in ("paper_ref", "kind", "variables"):
        if spec.get(key) != row[key]:
            say(f"agent.json {key} {spec.get(key)!r} != section 7's {row[key]!r}")
    if set(spec.get("tools", [])) != set(row["tools"]) or \
            len(spec.get("tools", [])) != len(row["tools"]):
        say(f"agent.json tools {spec.get('tools')} != {row['tools']} for kind {row['kind']}")
    desc = spec.get("description", "")
    if not isinstance(desc, str) or not desc.strip() or "\n" in desc or len(desc) > 160:
        say("description must be one non-empty line of at most 160 characters")

    found = PLACEHOLDER.findall(prompt)
    bad = [p for p in found if not IDENT.match(p)]
    if bad:
        say(f"prompt.md has malformed placeholders: {bad}")
    if set(found) != set(spec.get("variables", [])):
        say(f"prompt.md placeholders {sorted(set(found))} != variables "
            f"{sorted(spec.get('variables', []))}")
    if "{{" in PLACEHOLDER.sub("", prompt) or "}}" in PLACEHOLDER.sub("", prompt):
        say("prompt.md has an unmatched {{ or }}")
    if "{{" in system or "}}" in system:
        say("system.md must have no placeholders: only prompt.md is rendered")

    for validator_cls in VALIDATORS:
        try:
            validator_cls.check_schema(schema)
        except jsonschema.SchemaError as exc:
            say(f"schema.json fails the {validator_cls.__name__} metaschema: {exc.message}")
            return None
    check_plain(schema, say)
    check_spec(schema, row["output"], idea, "$", say)
    counts = [check_behaviour(schema, say, cls) for cls in VALIDATORS]
    count = min(counts)

    for field in schema.get("properties", {}):
        if not re.search(rf"\b{re.escape(field)}\b", system + prompt):
            say(f"no prompt text names the output field '{field}'")
    kind = spec.get("kind")
    for phrase in REQUIRED_PHRASES.get(kind, []):
        if phrase.lower() not in system.lower():
            say(f"system.md lacks the {kind} phrase {phrase!r}")
    for phrase in HELD_OUT_FORBIDDEN.get(folder.name, []):
        if phrase in (system + prompt).lower():
            say(f"the held-out judge's prompt mentions {phrase!r}")
    shared = section(system, SHARED_HEADING) if kind != "reasoning" else None
    if kind != "reasoning" and shared is None:
        say(f"system.md lacks the shared section '{SHARED_HEADING}'")
    return {"kind": kind, "vars": len(spec.get("variables", [])), "mutants": count,
            "fields": list(schema.get("properties", {})), "shared": shared,
            "idea": [{k: v for k, v in n.items() if k != "description"}  # per-use wording
                     for _, n in walk(schema)
                     if set(n.get("properties", {})) == set(idea["fields"])]}


def check_all(agents_dir, engine_text):
    rows, idea = parse_section7(engine_text)
    problems, results = [], {}
    folders = sorted(p for p in agents_dir.iterdir() if p.is_dir()
                     and not p.name.startswith((".", "_")))
    names = {p.name for p in folders}
    if names != set(rows):
        problems.append(f"agents: missing {sorted(set(rows) - names)}, "
                        f"not in section 7 {sorted(names - set(rows))}")
    for folder in folders:
        if folder.name not in rows:
            continue
        def say(msg, name=folder.name):
            problems.append(f"{name}: {msg}")
        results[folder.name] = check_agent(folder, rows[folder.name], idea, say)

    by_kind = {}
    for name, res in results.items():
        if res and res["shared"] is not None:
            by_kind.setdefault(res["kind"], {})[name] = res["shared"]
    for kind, texts in by_kind.items():
        if len(set(texts.values())) > 1:
            first = sorted(texts)[0]
            drift = sorted(n for n, t in texts.items() if t != texts[first])
            problems.append(f"{kind}: '{SHARED_HEADING}' differs from {first}'s in {drift}")
    ideas = [json.dumps(n, sort_keys=True) for r in results.values() if r for n in r["idea"]]
    if len(set(ideas)) > 1:
        problems.append(f"the IDEA object differs between schemas ({len(set(ideas))} variants)")
    return problems, results, len(ideas)


# ---------------------------------------------------------------- self-test

def _json_edit(path, fn):
    data = json.loads(path.read_text())
    fn(data)
    path.write_text(json.dumps(data))


def _text_edit(path, old, new):
    text = path.read_text()
    assert old in text, (path, old)
    path.write_text(text.replace(old, new, 1))


CORRUPTIONS = [  # (what is broken, the problem text that must report it, how)
    ("a placeholder dropped", "prompt.md placeholders", lambda d: _text_edit(
        d / "limitation_verifier/prompt.md", "{{limitations}}", "LIMITATIONS")),
    ("an unknown placeholder", "prompt.md placeholders", lambda d: _text_edit(
        d / "selector/prompt.md", "Return the", "{{bogus}} Return the")),
    ("a placeholder in system.md", "system.md must have no placeholders", lambda d: _text_edit(
        d / "selector/system.md", "You are", "{{task_title}} You are")),
    ("a wrong kind", "agent.json kind", lambda d: _json_edit(
        d / "spec_filter/agent.json", lambda a: a.update(kind="coding"))),
    ("a tool removed", "agent.json tools", lambda d: _json_edit(
        d / "novelty_checker/agent.json", lambda a: a.update(tools=[]))),
    ("a variable removed", "agent.json variables", lambda d: _json_edit(
        d / "selector/agent.json", lambda a: a["variables"].remove("metric"))),
    ("a nested object opened", "accepts an invalid output", lambda d: _json_edit(
        d / "reference_checker/schema.json",
        lambda s: s["properties"]["entries"]["items"].pop("additionalProperties"))),
    ("the top level opened", "object without additionalProperties", lambda d: _json_edit(
        d / "limitation_verifier/schema.json", lambda s: s.pop("additionalProperties"))),
    ("a required field dropped", "required", lambda d: _json_edit(
        d / "selector/schema.json", lambda s: s.update(required=["choice"]))),
    ("an enum value dropped", "enum", lambda d: _json_edit(
        d / "ablation_critic/schema.json",
        lambda s: s["properties"]["verdict"].update(enum=["Good", "Refine"]))),
    ("a bound moved", "integer in [1, 10]", lambda d: _json_edit(
        d / "peer_reviewer/schema.json", lambda s: s["properties"]["score"].update(maximum=9))),
    ("maxItems moved", "maxItems", lambda d: _json_edit(
        d / "novelty_checker/schema.json",
        lambda s: s["properties"]["references"].update(maxItems=3))),
    ("a $schema key added", "no $schema key", lambda d: _json_edit(
        d / "limitation_verifier/schema.json",
        lambda s: s.update({"$schema": "https://json-schema.org/draft/2020-12/schema"}))),
    ("an invalid schema", "metaschema", lambda d: _json_edit(
        d / "meta_reviewer/schema.json", lambda s: s.update(type="strng"))),
    ("a $ref used", "allowlist", lambda d: _json_edit(
        d / "initial_idea_generator/schema.json",
        lambda s: s["properties"].update(idea={"$ref": "#/$defs/IDEA"}))),
    ("an IDEA field removed", "<IDEA>", lambda d: _json_edit(
        d / "idea_evolver/schema.json", lambda s: (
            s["properties"]["idea"]["properties"].pop("risks"),
            s["properties"]["idea"]["required"].remove("risks")))),
    ("an agent removed", "missing ['final_judge']", lambda d: shutil.rmtree(d / "final_judge")),
    ("an extra file", "files [", lambda d: (d / "selector" / "notes.txt").write_text("x")),
    ("the shared rules drifted", "differs from", lambda d: _text_edit(
        d / "ablation_coder/system.md", "of your own", "of yours")),
    ("the judge told of the loop", "held-out judge", lambda d: _text_edit(
        d / "final_judge/system.md", "You are", "Unlike the in-loop peer reviewer, you are")),
    ("an output field unnamed", "names the output field", lambda d: (
        d / "selector/system.md").write_text(
            (d / "selector/system.md").read_text().replace("choice", "pick"))),
]


def self_test(agents_dir, engine_text):
    """Each corruption, on a fresh copy, must raise the problem it names; returns the misses."""
    missed = []
    for label, expected, corrupt in CORRUPTIONS:
        with tempfile.TemporaryDirectory() as tmp:
            copy_dir = Path(tmp) / "agents"
            shutil.copytree(agents_dir, copy_dir)
            corrupt(copy_dir)
            problems, _, _ = check_all(copy_dir, engine_text)
            if not any(expected in p for p in problems):
                missed.append(f"{label} (want {expected!r}, got {problems[:3]})")
    return missed


def main():
    engine_text = ENGINE_MD.read_text()
    problems, results, n_ideas = check_all(AGENTS_DIR, engine_text)
    total_mutants = 0
    print(f"checking {AGENTS_DIR.relative_to(ROOT)} against {ENGINE_MD.relative_to(ROOT)} §7")
    for name, res in sorted(results.items()):
        if res is None:
            print(f"  FAIL {name}")
            continue
        total_mutants += res["mutants"]
        mark = "FAIL" if any(p.startswith(name + ":") for p in problems) else "ok  "
        print(f"  {mark} {name:23s} {res['kind']:9s} vars={res['vars']} "
              f"mutants rejected={res['mutants']:3d} fields={','.join(res['fields'])}")
    print(f"{len(results)} agents; {total_mutants} schema mutants, each rejected under "
          f"{' and '.join(v.__name__ for v in VALIDATORS)}; {n_ideas} inlined IDEA objects")
    missed = self_test(AGENTS_DIR, engine_text)
    print(f"self-test: {len(CORRUPTIONS) - len(missed)}/{len(CORRUPTIONS)} corruptions caught, "
          f"each by the problem it should raise")
    for miss in missed:
        print(f"MISSED {miss}")
    for problem in problems:
        print(f"PROBLEM {problem}")
    print(f"{len(problems)} problems")
    return 1 if problems or missed else 0


if __name__ == "__main__":
    sys.exit(main())
