"""Check that docs/paper/traceability.md lists every paper element exactly once.

The completeness control behind Part 2 of traceability.md (TODO task 1; ID conventions in
docs/paper/README.md, section "IDs").

DEFINED. A P- ID is defined where a Markdown heading of a source document declares it, singly
("### P-EVAL-3 · Gain across papers") or as a range ("### Ablation study [...] · P-ABL-1 … 6").
Every source document introduces its elements that way, after the README's stage template
("### <stage> [...] · P-<KEY>-1 … n"). Anywhere else (a list item, a table cell, a code
comment) the ID is a reference. Lines inside fenced code blocks are never headings.

Problem kinds (any one makes the exit status 1):
  missing      a defined ID has no row of its own in Part 2
  duplicated   a defined ID occurs more than once in Part 2 (a second row, or a mention in a cell)
  not-alone    a Part 2 body row whose first cell is not exactly one P- ID
  orphan       Part 2 names a P- ID that no source document defines
  collision    two source documents declare the same ID
  numbering    a key's defined numbers have a hole (P-ABL-1, 2, 4)
  range        a range runs backwards (P-ABL-4 … 2)
  dangling     a source document, or traceability.md outside Part 2, names an undefined P- ID
  unknown-gap  Part 2 cites a U- or A- ID that no source document's gap list defines
  columns      a Part 2 row has a different number of cells from its table's header
  structure    traceability.md or its "## Part 2" section is absent

Usage:
  python3 playground/paper/trace_coverage.py               # the real files
  python3 playground/paper/trace_coverage.py --trace FILE  # another copy of traceability.md
  python3 playground/paper/trace_coverage.py --selftest    # plants each defect, shows it is caught
"""

import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "docs/paper"

PID = re.compile(r"\bP-([A-Z]+)-(\d+)\b")
# "P-ABL-1 … 6", "P-LIM-1..4", "P-ART-3 to P-ART-8", "P-CFG-4–7" all name every ID in between.
RANGE = re.compile(r"\bP-([A-Z]+)-(\d+)\s*(?:…|\.\.\.|\.\.|–|to\s+P-\1-)\s*(\d+)\b")
GAP_ID = re.compile(r"\b[UA]-[A-Z]+-\d+\b")
# A gap is defined where its full entry starts: "- **A-LIM-1 · ..." or "### U-EVAL-1 · ...".
GAP_DEF = re.compile(r"^\s*(?:#{1,6}\s+|[-*]\s+\*\*)([UA]-[A-Z]+-\d+)\b")
SEPARATOR = re.compile(r"^\|?[\s:|-]+\|[\s:|-]*$")


def source_files(paper: Path) -> list[Path]:
    """The documents that define paper elements.

    ⛔ WHY NOT every .md in the folder: README.md shows IDs as examples, traceability.md is the
    map under test, and unspecified.md is a register built from the gap lists; none of them
    introduces a paper element.
    """
    names = ["analysis.md", "artifacts.md", "claims.md", "note-check.md"]
    files = [paper / n for n in names if (paper / n).exists()]
    return files + sorted((paper / "stages").glob("*.md")) + sorted((paper / "claims").glob("*.md"))


def scan(path: Path):
    """Yield (line number, text, is_heading, in_code) for every line of a Markdown file."""
    in_code = False
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            yield n, line, False, True
            continue
        yield n, line, (not in_code and re.match(r"^#{1,6}\s", line) is not None), in_code


def ids_in(text: str, problems: list | None = None, where: str = "") -> list[str]:
    """Every P- ID a line names, ranges expanded: 'P-ABL-1 … 3' names P-ABL-1, -2 and -3."""
    found, spans = [], []
    for m in RANGE.finditer(text):
        key, first, last = m.group(1), int(m.group(2)), int(m.group(3))
        if last < first and problems is not None:
            problems.append(("range", f"{where}: backwards range {m.group(0)!r}"))
        found += [f"P-{key}-{i}" for i in range(min(first, last), max(first, last) + 1)]
        spans.append(m.span())
    for m in PID.finditer(text):
        if not any(start <= m.start() < end for start, end in spans):
            found.append(m.group(0))
    return found


def sort_key(pid: str):
    key, num = pid.rsplit("-", 1)
    return key, int(num)


def collect(paper: Path, problems: list):
    """Definitions, references and gap IDs across the source documents."""
    defined = defaultdict(set)        # P- ID -> the documents whose headings declare it
    referenced = defaultdict(list)    # P- ID -> "file:line" of every other mention
    gaps = set()
    for path in source_files(paper):
        rel = path.relative_to(paper).as_posix()
        for n, text, heading, in_code in scan(path):
            for pid in ids_in(text, problems, f"{rel}:{n}"):
                if heading:
                    defined[pid].add(rel)
                else:
                    referenced[pid].append(f"{rel}:{n}")
            match = None if in_code else GAP_DEF.match(text)
            if match:
                gaps.add(match.group(1))
    return defined, referenced, gaps


def part2_bounds(lines: list[str]):
    """Line indexes [start, end) of the '## Part 2' section, or None."""
    start = next((i for i, line in enumerate(lines) if re.match(r"^##\s+Part 2\b", line)), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^##\s", lines[i])), len(lines))
    return start, end


def check(paper: Path, trace: Path):
    """Return (problems, defined, rows); a problem is a (kind, message) pair."""
    problems = []
    defined, referenced, gaps = collect(paper, problems)
    for pid in sorted(defined, key=sort_key):
        if len(defined[pid]) > 1:
            problems.append(("collision", f"{pid} is declared in {', '.join(sorted(defined[pid]))}"))
    numbers = defaultdict(set)
    for pid in defined:
        key, num = pid.rsplit("-", 1)
        numbers[key].add(int(num))
    for key in sorted(numbers):
        holes = sorted(set(range(1, max(numbers[key]) + 1)) - numbers[key])
        if holes:
            problems.append(("numbering", f"{key}: nothing defines {', '.join(f'{key}-{h}' for h in holes)}"))
    for pid in sorted(referenced, key=sort_key):
        if pid not in defined:
            where = referenced[pid]
            problems.append(("dangling", f"{pid} is named at {where[0]} ({len(where)} place(s)) but never defined"))

    rows = defaultdict(list)
    if not trace.exists():
        problems.append(("structure", f"{trace} does not exist"))
        return problems, defined, rows
    lines = trace.read_text(encoding="utf-8").split("\n")
    bounds = part2_bounds(lines)
    if bounds is None:
        problems.append(("structure", f"{trace.name} has no '## Part 2' section"))
        return problems, defined, rows
    start, end = bounds
    occurrences = defaultdict(list)
    columns, previous_was_row = None, False
    for i in range(start, end):
        n, text, stripped = i + 1, lines[i], lines[i].strip()
        for pid in ids_in(text, problems, f"{trace.name}:{n}"):
            occurrences[pid].append(n)
        is_row = stripped.startswith("|")
        if not is_row:
            previous_was_row = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not previous_was_row:                       # a table's first row is its header
            columns, previous_was_row = len(cells), True
            continue
        if SEPARATOR.match(stripped):
            continue
        if len(cells) != columns:
            problems.append(("columns", f"{trace.name}:{n}: {len(cells)} cells, the header has {columns}"))
        if re.fullmatch(r"P-[A-Z]+-\d+", cells[0]):
            rows[cells[0]].append(n)
        else:
            problems.append(("not-alone", f"{trace.name}:{n}: first cell is not one P- ID: {cells[0][:50]!r}"))
        for gap in GAP_ID.findall(text):
            if gap not in gaps:
                problems.append(("unknown-gap", f"{trace.name}:{n}: {gap} is in no source's gap list"))
    for pid in sorted(defined, key=sort_key):
        where = ", ".join(sorted(defined[pid]))
        if not rows.get(pid):
            problems.append(("missing", f"{pid} (defined in {where}) has no row in Part 2"))
        if len(occurrences.get(pid, [])) > 1:
            lines_at = ", ".join(map(str, occurrences[pid]))
            problems.append(("duplicated", f"{pid} occurs {len(occurrences[pid])} times in Part 2, lines {lines_at}"))
    for pid in sorted(occurrences, key=sort_key):
        if pid not in defined:
            problems.append(("orphan", f"{pid} is in Part 2 (line {occurrences[pid][0]}) but no source defines it"))
    for n, text, _heading, _code in scan(trace):
        if start < n <= end:
            continue                                   # Part 2's own names are checked above
        for pid in ids_in(text, problems, f"{trace.name}:{n}"):
            if pid not in defined:
                problems.append(("dangling", f"{trace.name}:{n}: {pid} is not defined"))
    return problems, defined, rows


def report(paper: Path, trace: Path) -> int:
    problems, defined, rows = check(paper, trace)
    per_key = defaultdict(lambda: [0, 0])
    for pid in defined:
        per_key[pid.rsplit("-", 1)[0]][0] += 1
    for pid, at in rows.items():
        per_key[pid.rsplit("-", 1)[0]][1] += len(at)
    print(f"{'key':<10}{'defined':>8}{'rows':>6}")
    for key in sorted(per_key):
        d, r = per_key[key]
        print(f"{key:<10}{d:>8}{r:>6}{'' if d == r else '   <-- differs'}")
    print(f"{'total':<10}{sum(v[0] for v in per_key.values()):>8}{sum(v[1] for v in per_key.values()):>6}")
    print(f"{len(source_files(paper))} source document(s); {len(per_key)} key(s)")
    for kind, message in problems:
        print(f"{kind}: {message}")
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


SOURCE = """# A source document
## A stage · P-AAA-1 … 2
- P-AAA-1: a step [§3.1].
### P-BBB-1 · a definition
- **U-AAA-1 · a gap.**
"""
TRACE = """# Traceability
## Part 1
P-AAA-1 … 2 and P-BBB-1 are covered.
## Part 2
| ID | Element | Gaps |
|---|---|---|
| P-AAA-1 | a step | U-AAA-1 |
| P-AAA-2 | another step | none |
| P-BBB-1 | a definition | none |
## Part 3
"""
ROW2 = "| P-AAA-2 | another step | none |\n"


def selftest() -> int:
    """Each planted defect must produce exactly the expected problem kinds; the clean twin none."""
    fence = "```\n# P-DDD-1 looks like a heading inside a code block\n```\n"
    cases = {  # name: (source text, extra source file or None, trace text, expected kinds)
        "clean": (SOURCE, None, TRACE, set()),
        "a row deleted": (SOURCE, None, TRACE.replace(ROW2, ""), {"missing"}),
        "a row repeated": (SOURCE, None, TRACE.replace(ROW2, ROW2 * 2), {"duplicated"}),
        "an ID named again in a cell": (SOURCE, None, TRACE.replace("another step", "like P-AAA-1"), {"duplicated"}),
        "a row for nothing": (SOURCE, None, TRACE.replace(ROW2, ROW2 + "| P-CCC-1 | x | none |\n"), {"orphan"}),
        "two IDs in one cell": (SOURCE, None, TRACE.replace("| P-AAA-1 | a step | U-AAA-1 |\n" + ROW2,
                                "| P-AAA-1, P-AAA-2 | both | none |\n"), {"not-alone", "missing"}),
        "one ID in two documents": (SOURCE, "## Again · P-AAA-1\n", TRACE, {"collision"}),
        "a hole in the numbers": (SOURCE.replace("P-AAA-1 … 2", "P-AAA-1, P-AAA-3"), None,
                                  TRACE.replace("P-AAA-2", "P-AAA-3").replace("P-AAA-1 … 2 and", "P-AAA-1 and"), {"numbering"}),
        "a reference to nothing": (SOURCE + "- see P-AAA-9 [§3.1].\n", None, TRACE, {"dangling"}),
        "a range is expanded": (SOURCE.replace("P-AAA-1 … 2", "P-AAA-1 … 3"), None, TRACE, {"missing"}),
        "a backwards range": (SOURCE.replace("P-AAA-1 … 2", "P-AAA-2 … 1"), None, TRACE, {"range"}),
        "a fenced line defines nothing": (SOURCE + fence, None, TRACE, {"dangling"}),
        "an unknown gap ID": (SOURCE, None, TRACE.replace("U-AAA-1", "U-AAA-7"), {"unknown-gap"}),
        "a row with an extra cell": (SOURCE, None, TRACE.replace(ROW2, "| P-AAA-2 | another | none | x |\n"), {"columns"}),
        "Part 1 names nothing real": (SOURCE, None, TRACE.replace("are covered", "and P-EEE-1 are covered"), {"dangling"}),
        "no Part 2": (SOURCE, None, TRACE.replace("## Part 2", "## Part Two"), {"structure"}),
    }
    failed = 0
    for name, (source, extra, trace, want) in cases.items():
        with tempfile.TemporaryDirectory() as tmp:
            paper = Path(tmp)
            (paper / "analysis.md").write_text(source, encoding="utf-8")
            if extra:
                (paper / "artifacts.md").write_text(extra, encoding="utf-8")
            (paper / "traceability.md").write_text(trace, encoding="utf-8")
            got = {kind for kind, _ in check(paper, paper / "traceability.md")[0]}
        ok = got == want
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: got {sorted(got) or 'no problem'}, expected {sorted(want) or 'no problem'}")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--selftest"]:
        return selftest()
    if len(argv) == 3 and argv[1] == "--trace":
        return report(PAPER, Path(argv[2]))
    if len(argv) > 1:
        print(__doc__)
        return 2
    return report(PAPER, PAPER / "traceability.md")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
