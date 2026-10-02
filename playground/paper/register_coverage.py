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
    and within a task "blocks" rows come first, then "number", then "later";
  - a "blocks" row carries its rank in the system architect's list of what task 3 needs decided
    first ("blocks 1" to "blocks 8"), and within a task the blocking rows follow that rank.
Checks on the full entries (every place above except the 10.2 index), each a failure too:
  - each entry carries exactly one Register line, "*Register: X ...*", where X, the ID the line
    starts with, is the canonical ID of the register row that holds the entry's ID, as canonical
    or alias. A line that starts with no ID ("not yet indexed ... A-TOP-1") names no row, even if
    it cites the right one later; an alias or another row's ID fails too. Only the rows of the
    register tables count as holders: a table elsewhere in unspecified.md, such as "Why these rows
    merge", and IDs cited in a row's question or decision never do (a scratch version that read
    every table in the file flagged U-PEER-1 falsely).
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
PRIORITY_RE = re.compile(r"^(blocks|number|later|none)(?:\s+(\d+))?$")
RANKS = range(1, 9)   # system-architect.md, "What task 3 needs decided first", items 1-8
TASK_ORDER = [2, 3, 4, 5, 6, 7, 1]   # task 1 = settled in docs/paper, listed last
HEADING_RE = re.compile(r"^#{1,3}\s")                # ends a full entry, like the next definition
REGISTER_MARK = re.compile(r"\*Register:\s*([^*\n]*?)\s*\*")
LEAD_ID = re.compile(rf"^({ID})\b")


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


def full_entry_sections(paper: Path) -> list[tuple[str, str, bool, str, int]]:
    """(location name, file, engine-side?, section text, its first line) for every gap section that
    holds full entries, in the register's reading order: analysis.md 10.1, stages/01..07,
    claims.md, note-check.md, artifacts.md."""
    analysis = (paper / "analysis.md").read_text(encoding="utf-8")
    out = [("analysis.md 10.1", "analysis.md", True) + section(analysis, r"^### 10\.1", r"^### 10\.2")]
    for f in sorted((paper / "stages").glob("*.md")):
        out.append(("stages/*.md", f"stages/{f.name}", True)
                   + section(f.read_text(encoding="utf-8"), r"^## Gaps found here"))
    for name in ("claims.md", "note-check.md", "artifacts.md"):
        out.append((name, name, False)
                   + section((paper / name).read_text(encoding="utf-8"), r"^## Gaps found here"))
    return out


def locations(paper: Path) -> list[tuple[str, str, bool, list[tuple[str, str, int]]]]:
    """(location name, file shown, engine-side?, definitions) for the six locations, in the
    register's reading order; the stage files form one location."""
    out = []
    for name, _, engine, text, first in full_entry_sections(paper):
        if out and out[-1][0] == name:
            out[-1][3].extend(definitions(text, first))
        else:
            out.append((name, "stages/" if name == "stages/*.md" else name, engine, definitions(text, first)))
    analysis = (paper / "analysis.md").read_text(encoding="utf-8")
    s102, l102 = section(analysis, r"^### 10\.2", r"^#{1,3} (?!10\.)")
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
                     "priority": cells[5], "rank": None, "aliases": ID_RE.findall(cells[6])})
        m = PRIORITY_RE.match(cells[5])
        if m:
            rows[-1]["priority"], rows[-1]["rank"] = m.group(1), int(m.group(2)) if m.group(2) else None
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
        elif r["priority"] == "blocks" and r["rank"] not in RANKS:
            problems.append(f"line {r['line']}: a blocks row needs its rank, blocks 1 to blocks 8")
        elif r["priority"] != "blocks" and r["rank"] is not None:
            problems.append(f"line {r['line']}: only a blocks row carries a rank")
    for i in order:
        if seen[i] == 0:
            problems.append(f"missing: {i} is in no row, as canonical or alias")
        elif seen[i] > 1:
            problems.append(f"duplicate: {i} appears in {seen[i]} rows")
    keys = [(TASK_ORDER.index(int(r["task"])), PRIORITIES.index(r["priority"]), r["rank"] or 0, r["line"])
            for r in rows if "error" not in r and r["task"].isdigit()
            and int(r["task"]) in TASK_ORDER and r["priority"] in PRIORITIES]
    for (a, b) in zip(keys, keys[1:]):
        if b[:3] < a[:3]:
            problems.append(f"line {b[3]}: out of order (tasks 2..7 then 1; blocks by rank, number, later)")
    return problems


def register_marks(text: str, first_line: int = 1) -> list[tuple[str, int, list[tuple[int, str]]]]:
    """(entry ID, its line, [(line, text)] of its Register lines) for every full entry in a gap
    section. An entry runs from its defining line to the next defining line or heading."""
    entries: list[tuple[str | None, int, list[tuple[int, str]]]] = []
    for n, line in enumerate(text.split("\n"), first_line):
        m = DEF_RE.match(line)
        if m or HEADING_RE.match(line):
            entries.append((m.group(1) if m else None, n, []))
        if entries and entries[-1][0] is not None:
            entries[-1][2].extend((n, t) for t in REGISTER_MARK.findall(line))
    return [e for e in entries if e[0] is not None]


def check_marks(entries: list[tuple[str, str, int, list[tuple[int, str]]]], rows: list[dict]) -> list[str]:
    """Every entry whose Register line is missing, doubled, names no row, or names a row that does
    not hold the entry's ID. `entries` are (file, ID, line, marks); `rows` come from register_rows,
    which reads only the register tables, so a table elsewhere never makes a row a holder."""
    good = [r for r in rows if "error" not in r]
    canonical = {r["id"] for r in good}
    holder: dict[str, str] = {}   # the last row wins, so a stray table after the register would show
    for r in good:
        for i in [r["id"]] + r["aliases"]:
            holder[i] = r["id"]
    problems = []
    for where, ident, line, marks in entries:
        if len(marks) != 1:
            problems.append(f"{where}:{line}: {ident} has {len(marks)} Register lines, expected 1")
            continue
        n, text = marks[0]
        lead = LEAD_ID.match(text)
        named = lead.group(1) if lead else None
        if named not in canonical:
            what = "no row" if named is None else (
                f"{named}, an alias in row {holder[named]}" if named in holder else f"{named}, no row's ID")
            problems.append(f"{where}:{n}: {ident}'s Register line names {what}: {text!r}")
        elif holder.get(ident) != named:
            problems.append(f"{where}:{n}: {ident}'s Register line names {named}, "
                            f"but {ident} is in row {holder.get(ident, 'none')}")
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
    ranks = Counter(r["rank"] for r in good if r["priority"] == "blocks")
    print("  blocking rows per rank: " + ", ".join(f"{k}: {ranks[k]}" for k in RANKS))
    print("  rows per priority: " + ", ".join(f"{p} {sum(1 for r in good if r['priority'] == p)}" for p in PRIORITIES))
    entries = [(f, i, n, marks) for _, f, _, text, first in full_entry_sections(PAPER)
               for i, n, marks in register_marks(text, first)]
    print(f"Register lines: {sum(1 for e in entries if len(e[3]) == 1)} of {len(entries)} full entries carry exactly one")
    problems = check(rows, order, engine) + check_marks(entries, rows)
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

    def row(i, al, task="2", pri="blocks 1", cls="AMBIGUOUS", q="q [§3]"):
        return f"| {i} (x) | {cls} | {q} | d [ours] | {task} | {pri} | {al} |\n"

    # The Register-line check. A-FOO-3's question cites U-FOO-1, and a merge table after the
    # register lists U-FOO-1 under A-FOO-3: neither may make A-FOO-3 the row that holds U-FOO-1.
    reg = (head + row("U-FOO-1", "A-FOO-2 (x)") + row("A-FOO-3", "none", "3", q="q, unlike U-FOO-1 [§3]")
           + "\n## Why these rows merge\n\n| Row | Merged with | Why |\n|---|---|---|\n"
           + "| A-FOO-3 | none | U-FOO-1's half is named here [ours] |\n")

    def marks(m1="*Register: U-FOO-1.*", m2="- *Register: U-FOO-1 (A-FOO-2 is an alias there)*",
              m3="*Register: A-FOO-3*") -> int:
        gaps = ("## Gaps found here\n\n"
                f"- **U-FOO-1 · UNSPECIFIED · a list-item entry.** {m1}\n"
                "### A-FOO-2 · AMBIGUOUS · a heading entry\n\n"
                f"- its quotes\n{m2}\n\n"
                f"- **A-FOO-3 · INCONSISTENT · another entry.** {m3}\n")
        s2, l2 = section(gaps, r"^## Gaps found here")
        entries = [("x.md", i, n, mk) for i, n, mk in register_marks(s2, l2)]
        return len(check_marks(entries, register_rows(reg)))

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
        "blocks without a rank": (head + row("U-FOO-1", "A-FOO-2 (x)", pri="blocks") + row("A-FOO-3", "none", "3"), 1),
        "rank order broken": (head + row("U-FOO-1", "A-FOO-2 (x)", pri="blocks 5") + row("A-FOO-3", "none", "2", "blocks 2"), 1),
        "rank on a number row": (head + row("U-FOO-1", "A-FOO-2 (x)", pri="number 3") + row("A-FOO-3", "none", "3"), 1),
    }
    mark_cases = {
        "Register lines current, cited IDs and the merge table ignored": marks(),
        "a stale Register line, with the right row cited after no ID": marks(m3="*Register: not yet indexed (new; nearest row A-FOO-3)*"),
        "a Register line naming an alias": marks(m2="- *Register: A-FOO-2*"),
        "a Register line naming another row": marks(m1="*Register: A-FOO-3*"),
        "an entry without a Register line": marks(m3=""),
        "an entry with two Register lines": marks(m2="- *Register: U-FOO-1* and *Register: U-FOO-1*"),
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
    for i, (name, got) in enumerate(mark_cases.items()):
        ok = (got > 0) == (i > 0)     # the first case must pass, every other must fail
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: {got}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(selftest() if sys.argv[1:] == ["--selftest"] else main())
