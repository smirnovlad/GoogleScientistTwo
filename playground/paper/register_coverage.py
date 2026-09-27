"""Check that docs/paper/unspecified.md, the decision register, covers every gap item exactly once.

The gap items are the U-<KEY>-n and A-<KEY>-n IDs DEFINED in six places (README.md, "IDs"):
  1. analysis.md section 10.1 (cross-cutting items, in full)
  2. analysis.md section 10.2 (the index of every engine-side gap)
  3. stages/*.md, "Gaps found here"
  4. claims.md, "Gaps found here"
  5. note-check.md, "Gaps found here"
  6. artifacts.md, "Gaps found here"
An ID is DEFINED where its full entry (or its index row) starts: a list item "- **ID · ...", a heading
"### ID · ...", or a table row "| ID | ...". A mere mention elsewhere does not define it.

Checks on the register (section "## The register" of unspecified.md), each a failure (exit 1):
  - every defined ID appears exactly once, as a row's canonical ID or among its aliases;
  - no canonical or alias cell names an undefined ID;
  - each canonical ID follows the register's rule: the engine-side ID (analysis.md 10.1, then
    stages/01..07) whose full entry comes first; if none, the ID whose full entry comes first in
    claims.md, then note-check.md, then artifacts.md;
  - class, task and priority values are valid, rows are grouped by task in the order 2..7 then 1,
    and within a task "blocks" rows come first, then "number", then "later".
Also printed, never a failure: IDs found per location, class counts before and after merging,
rows per task and priority, index-versus-entry mismatches, and mentions of undefined IDs.

Usage:
  python3 playground/paper/register_coverage.py            # check, exit 1 on any failure
  python3 playground/paper/register_coverage.py --selftest # proves each check can fail
"""

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "docs/paper"
REGISTER = PAPER / "unspecified.md"

ID = r"[UA]-[A-Z]+-\d+"
ID_RE = re.compile(rf"\b{ID}\b")
DEF_RE = re.compile(rf"^(?:\s*[-*]\s+\*\*|###\s+|\|\s*)({ID})(?:\s+·|\s*\|)")
CLASS_RE = re.compile(r"\b(UNSPECIFIED|AMBIGUOUS|INCONSISTENT)\b")
CLASSES = ("UNSPECIFIED", "AMBIGUOUS", "INCONSISTENT")
PRIORITIES = ("blocks", "number", "later", "none")
TASK_ORDER = [2, 3, 4, 5, 6, 7, 1]   # task 1 = settled in docs/paper, listed last


def section(text: str, start: str, stop: str | None = None) -> tuple[str, int]:
    """The text from the line matching `start` to the line matching `stop` (or the end), and its
    first line number."""
    lines = text.split("\n")
    begin = next((i for i, l in enumerate(lines) if re.match(start, l)), None)
    if begin is None:
        return "", 0
    end = len(lines)
    if stop:
        end = next((i for i in range(begin + 1, len(lines)) if re.match(stop, lines[i])), end)
    return "\n".join(lines[begin:end]), begin + 1


def definitions(text: str, first_line: int = 1) -> list[tuple[str, str, int]]:
    """(id, class as filed, line) for every ID defined in `text`; an A- ID with no class word is
    reported with class '?'."""
    found = []
    for n, line in enumerate(text.split("\n"), first_line):
        m = DEF_RE.match(line)
        if not m:
            continue
        ident = m.group(1)
        c = CLASS_RE.search(line)
        cls = c.group(1) if c else ("UNSPECIFIED" if ident.startswith("U-") else "?")
        found.append((ident, cls, n))
    return found


def locations(paper: Path) -> list[tuple[str, str, bool, list[tuple[str, str, int]]]]:
    """(location name, file shown, engine-side?, definitions) for the six locations, in the
    register's reading order."""
    out = []
    analysis = (paper / "analysis.md").read_text(encoding="utf-8")
    s101, l101 = section(analysis, r"^### 10\.1", r"^### 10\.2")
    s102, l102 = section(analysis, r"^### 10\.2", r"^#{1,3} (?!10\.)")
    out.append(("analysis.md 10.1", "analysis.md", True, definitions(s101, l101)))
    stage_defs = []
    for f in sorted((paper / "stages").glob("*.md")):
        s, l = section(f.read_text(encoding="utf-8"), r"^## Gaps found here")
        stage_defs += [(i, c, n) for i, c, n in definitions(s, l)]
    out.append(("stages/*.md", "stages/", True, stage_defs))
    for name in ("claims.md", "note-check.md", "artifacts.md"):
        s, l = section((paper / name).read_text(encoding="utf-8"), r"^## Gaps found here")
        out.append((name, name, False, definitions(s, l)))
    out.insert(1, ("analysis.md 10.2 (index)", "analysis.md", True, definitions(s102, l102)))
    return out


def register_rows(text: str) -> list[dict]:
    """The rows of the register tables: every 7-cell table row, under "## The register", whose
    first cell starts with an ID. Cells: ID (entry) | Class | Question | Decision | Task |
    Priority | Aliases (entry)."""
    body, first = section(text, r"^## The register", r"^## (?!The register)")
    rows = []
    for n, line in enumerate(body.split("\n"), first):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        head = re.match(rf"({ID})\b", cells[0]) if cells else None
        if not head:
            continue
        if len(cells) != 7:
            rows.append({"line": n, "error": f"{len(cells)} cells, expected 7"})
            continue
        rows.append({"line": n, "id": head.group(1), "class": cells[1], "task": cells[4],
                     "priority": cells[5], "aliases": ID_RE.findall(cells[6])})
    return rows


def expected_canonical(ids: list[str], order: dict[str, int], engine: set[str]) -> str:
    """The register's rule: the engine-side ID defined first; else the ID defined first."""
    pool = [i for i in ids if i in engine] or list(ids)
    return min(pool, key=lambda i: order.get(i, 10**9))


def check(rows: list[dict], order: dict[str, int], engine: set[str]) -> list[str]:
    """Every problem with the register rows, given the defined IDs in definition order."""
    problems, seen = [], Counter()
    for r in rows:
        if "error" in r:
            problems.append(f"line {r['line']}: {r['error']}")
            continue
        ids = [r["id"]] + r["aliases"]
        seen.update(ids)
        for i in ids:
            if i not in order:
                problems.append(f"line {r['line']}: {i} is not defined in any gap section")
        if all(i in order for i in ids):
            want = expected_canonical(ids, order, engine)
            if want != r["id"]:
                problems.append(f"line {r['line']}: canonical should be {want}, not {r['id']}")
        if r["class"] not in CLASSES:
            problems.append(f"line {r['line']}: class {r['class']!r} not one of {CLASSES}")
        if not r["task"].isdigit() or int(r["task"]) not in TASK_ORDER:
            problems.append(f"line {r['line']}: task {r['task']!r} not one of {TASK_ORDER}")
        if r["priority"] not in PRIORITIES:
            problems.append(f"line {r['line']}: priority {r['priority']!r} not one of {PRIORITIES}")
    for i in order:
        if seen[i] == 0:
            problems.append(f"missing: {i} is in no row, as canonical or alias")
        elif seen[i] > 1:
            problems.append(f"duplicate: {i} appears in {seen[i]} rows")
    keys = [(TASK_ORDER.index(int(r["task"])), PRIORITIES.index(r["priority"]), r["line"])
            for r in rows if "error" not in r and r["task"].isdigit()
            and int(r["task"]) in TASK_ORDER and r["priority"] in PRIORITIES]
    for (a, b) in zip(keys, keys[1:]):
        if b[:2] < a[:2]:
            problems.append(f"line {b[2]}: out of order (tasks 2..7 then 1; blocks, number, later)")
    return problems


def mentions(paper: Path, defined: set[str]) -> dict[str, list[str]]:
    """IDs mentioned in docs/paper but defined nowhere (README's examples excluded)."""
    files = [p for p in sorted(paper.glob("*.md")) if p.name != "README.md"]
    files += sorted((paper / "stages").glob("*.md")) + sorted((paper / "claims").glob("*.md"))
    out = {}
    for f in files:
        stray = sorted(set(ID_RE.findall(f.read_text(encoding="utf-8"))) - defined)
        if stray:
            out[str(f.relative_to(paper))] = stray
    return out


def main() -> int:
    locs = locations(PAPER)
    print("IDs defined, per location:")
    for name, _, engine, defs in locs:
        print(f"  {name:28s} {len(defs):3d}  ({'engine-side' if engine else 'other'})")
    index = {i: c for i, c, _ in next(d for n, _, _, d in locs if n.startswith("analysis.md 10.2"))}
    full = [(i, c) for n, _, _, d in locs if not n.startswith("analysis.md 10.2") for i, c, _ in d]
    order = {}
    for i, _ in full:
        order.setdefault(i, len(order))
    engine = {i for n, _, e, d in locs if e and not n.startswith("analysis.md 10.2") for i, _, _ in d}
    filed = dict(full)
    dup_defs = [i for i, k in Counter(i for i, _ in full).items() if k > 1]
    print(f"distinct IDs defined: {len(order)} (full entries: {len(full)}; defined twice: {dup_defs or 'none'})")
    print("  as filed: " + ", ".join(f"{c} {k}" for c, k in Counter(filed.values()).most_common()))
    miss_idx = sorted(engine - set(index))
    extra_idx = sorted(set(index) - engine)
    cls_diff = sorted(i for i in index if i in filed and index[i] != filed[i])
    print(f"analysis.md 10.2 index against its full entries: missing {miss_idx or 'none'}, "
          f"extra {extra_idx or 'none'}, class mismatches {cls_diff or 'none'}")
    stray = mentions(PAPER, set(order))
    print(f"mentions of undefined IDs (README examples excluded): {stray or 'none'}")
    if not REGISTER.exists():
        print(f"FAIL: {REGISTER.relative_to(ROOT)} does not exist")
        return 1
    rows = register_rows(REGISTER.read_text(encoding="utf-8"))
    good = [r for r in rows if "error" not in r]
    print(f"register rows: {len(rows)}; IDs they cover: {sum(1 + len(r['aliases']) for r in good)}")
    print("  rows per class: " + ", ".join(f"{c} {k}" for c, k in Counter(r['class'] for r in good).most_common()))
    per = Counter((r["task"], r["priority"]) for r in good)
    for t in TASK_ORDER:
        n = sum(v for (tt, _), v in per.items() if tt == str(t))
        split = ", ".join(f"{p} {per[(str(t), p)]}" for p in PRIORITIES if per[(str(t), p)])
        ids = sum(1 + len(r["aliases"]) for r in good if r["task"] == str(t))
        print(f"  task {t}: {n:2d} rows, {ids:3d} IDs  ({split or 'no rows'})")
    print("  rows per priority: " + ", ".join(f"{p} {sum(1 for r in good if r['priority'] == p)}" for p in PRIORITIES))
    problems = check(rows, order, engine)
    for p in problems:
        print("FAIL:", p)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


def selftest() -> int:
    """Each check must fail on a planted defect and pass on its corrected twin."""
    doc = ("# X\n\nMentions U-FOO-9 outside the gaps.\n\n## Gaps found here\n\n"
           "- **U-FOO-1 · UNSPECIFIED · a list-item entry.**\n"
           "### A-FOO-2 · AMBIGUOUS · a heading entry\n"
           "| A-FOO-3 | INCONSISTENT | an index row |\n"
           "- see A-FOO-4 in running text, not an entry\n")
    s, l = section(doc, r"^## Gaps found here")
    found = [i for i, _, _ in definitions(s, l)]
    order = {"A-FOO-2": 0, "U-FOO-1": 1, "A-FOO-3": 2}          # A-FOO-2 is defined first ...
    engine = {"U-FOO-1"}                                          # ... but U-FOO-1 is engine-side
    head = ("## The register\n\n| ID | Class | Question | Decision | Task | Priority | Aliases |\n"
            "|---|---|---|---|---|---|---|\n")

    def row(i, al, task="2", pri="blocks", cls="AMBIGUOUS"):
        return f"| {i} (x) | {cls} | q [§3] | d [ours] | {task} | {pri} | {al} |\n"

    cases = {
        "collector finds the three entries only": (found == ["U-FOO-1", "A-FOO-2", "A-FOO-3"], True),
        "complete register": (head + row("U-FOO-1", "A-FOO-2 (x)") + row("A-FOO-3", "none", "3"), 0),
        "an ID missing": (head + row("U-FOO-1", "A-FOO-2 (x)"), 1),
        "an ID in two rows": (head + row("U-FOO-1", "A-FOO-2 (x)") + row("A-FOO-3", "A-FOO-2 (x)", "3"), 1),
        "an undefined alias": (head + row("U-FOO-1", "A-FOO-2 (x), U-FOO-7 (x)") + row("A-FOO-3", "none", "3"), 1),
        "canonical against the rule": (head + row("A-FOO-2", "U-FOO-1 (x)") + row("A-FOO-3", "none", "3"), 1),
        "task order broken": (head + row("A-FOO-3", "none", "3") + row("U-FOO-1", "A-FOO-2 (x)"), 1),
        "priority order broken": (head + row("A-FOO-3", "none", "2", "later") + row("U-FOO-1", "A-FOO-2 (x)"), 1),
        "bad class value": (head + row("U-FOO-1", "A-FOO-2 (x)", cls="VAGUE") + row("A-FOO-3", "none", "3"), 1),
    }
    failed = 0
    for name, (body, want) in cases.items():
        if isinstance(want, bool):
            ok, got = body is want, found
        else:
            got = len(check(register_rows(body), order, engine))
            ok = (got > 0) == bool(want)
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: {got}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(selftest() if sys.argv[1:] == ["--selftest"] else main())
