"""Check that every paper element maps to a requirement, or to a recorded decision to leave it out.

The completeness control of TODO task 2 (docs/requirements.md, section "Controls"). It reads:
  - docs/requirements.md and docs/requirements/*.md: requirements, each a heading
    "### R-<AREA>-n · <title>" followed by its fields as top-level list items
    ("- **Requirement.** ...", then Traces, Why ours, Decides, Depends on, Test, in that order);
    decisions to leave an element out, "### X-n · <title>" with "Leaves out" and "Why"; the table of
    decisions on the register's task-2 rows; and the table of rows left to other tasks;
  - docs/paper/traceability.md, Part 2, whose "Requirement" column must name, for each P- ID, the
    requirements and leave-outs that trace it;
  - docs/paper/unspecified.md, the register, whose task-2 rows must each point to their decision;
  - the paper elements, defined as trace_coverage.py defines them.

Problem kinds (any one makes the exit status 1):
  unmapped          a defined P- ID that no requirement traces and no X- decision leaves out
  left-and-traced   a P- ID that an X- decision leaves out and a requirement also traces
  dangling-trace    a Traces or Leaves-out field names a P- ID that nothing defines
  duplicate-id      an R- or X- ID defined twice
  fields            a missing, repeated, unknown or out-of-order field, or text outside a field
  no-test           a requirement whose Test field is empty
  no-source         a requirement that traces no P- ID and gives no reason under "Why ours"
  no-reason         an X- decision with no element under "Leaves out", or no reason under "Why"
  column            a Requirement cell of traceability.md that differs from what the requirements say
  unknown-ref       a cell of a table here names an R- or X- ID that is not defined
  unknown-row       a Decides or Depends-on field names an ID that no register row holds
  boundary          a requirement decides a row that task 2 does not own, or depends on one it does
  undecided         a task-2 register row that no requirement decides
  decision-table    the decisions table: a missing, repeated or foreign row, a bad status, or a
                    "Carried by" cell that differs from the requirements that decide the row
  pointer           a task-2 register row without its pointer, or whose pointer disagrees with the table
  pending-table     the table of rows left to other tasks differs from the Depends-on fields
  structure         a file, a section or a table column is missing

Usage:
  python3 playground/paper/requirement_coverage.py             # check the real files
  python3 playground/paper/requirement_coverage.py --write     # fill traceability.md's column, then check
  python3 playground/paper/requirement_coverage.py --selftest  # plants each defect, shows it is caught
"""

import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace_coverage import collect, ids_in, part2_bounds, sort_key  # noqa: E402  (one definition of a P- ID)

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "docs/paper"
REQ_MAIN = ROOT / "docs/requirements.md"
REQ_DIR = ROOT / "docs/requirements"

HEAD = re.compile(r"^###\s+(R-[A-Z]+-\d+|X-\d+)\s+·\s+\S")
ANY_HEADING = re.compile(r"^#{1,6}\s")
FIELD = re.compile(r"^- \*\*([A-Za-z ]+)\.\*\*(.*)$")
REQ_ID = re.compile(r"\b(?:R-[A-Z]+-\d+|X-\d+)\b")
GAP = re.compile(r"\b[UA]-[A-Z]+-\d+\b")
TAGS = re.compile(r"\[[^\]]*\]|\([^)]*\)")
R_FIELDS = ["Requirement", "Traces", "Why ours", "Decides", "Depends on", "Test"]
R_REQUIRED = {"Requirement", "Traces", "Test"}
X_FIELDS = ["Leaves out", "Why"]
AREAS = ["RUN", "PRIM", "STG", "AGT", "STATE", "INT", "MEAS", "OPS"]   # reading order, then X-
STATUSES = ("confirmed", "refined", "replaced")
PLACEHOLDER = "— (task 2)"
# The pointer a task-2 register row carries in its decision cell, e.g.
# "**Task 2 decided it: confirmed, in R-PRIM-4, R-STG-1.**"
POINTER = re.compile(r"\*\*Task 2 decided it: ([a-z]+), in ([^*]+?)\.\*\*")
DECISIONS = r"^##\s+Decisions on the register's task-2 rows"
PENDING = r"^##\s+What the requirements leave to other tasks"


def id_key(rid: str):
    """Reading order: the areas of AREAS, then X- decisions, each by number."""
    if rid.startswith("X-"):
        return len(AREAS) + 1, "", int(rid[2:])
    area, num = rid[2:].rsplit("-", 1)
    return (AREAS.index(area) if area in AREAS else len(AREAS)), area, int(num)


def cells(line: str) -> list[str]:
    """The cells of a Markdown table row; an escaped pipe stays inside its cell."""
    parts = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [c.strip() for c in parts]


def tables(lines: list[str], start: int = 0, end: int | None = None):
    """Yield (header cells, [(line index, cells)]) for every table in lines[start:end]."""
    end = len(lines) if end is None else end
    i = start
    while i < end:
        if lines[i].lstrip().startswith("|"):
            header, body, i = cells(lines[i]), [], i + 1
            while i < end and lines[i].lstrip().startswith("|"):
                if not re.match(r"^\|?[\s:|-]+\|[\s:|-]*$", lines[i].strip()):
                    body.append((i, cells(lines[i])))
                i += 1
            yield header, body
        else:
            i += 1


def section(lines: list[str], heading: str):
    """Line indexes [start, end) of the section whose heading matches, or None."""
    start = next((i for i, line in enumerate(lines) if re.match(heading, line)), None)
    if start is None:
        return None
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    stop = re.compile(rf"^#{{1,{level}}}\s")
    end = next((i for i in range(start + 1, len(lines)) if stop.match(lines[i])), len(lines))
    return start, end


def column(header: list[str], prefix: str) -> int | None:
    return next((i for i, h in enumerate(header) if h.startswith(prefix)), None)


def parse_requirements(files: list[Path], problems: list):
    """Blocks: {id: {"file", "line", "fields": {name: text}, "order": [names]}}."""
    blocks = {}
    for path in files:
        current, field, in_code = None, None, False
        for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            where = f"{path.name}:{n}"
            if line.lstrip().startswith("```"):
                in_code = not in_code
            if in_code:
                continue
            if ANY_HEADING.match(line):
                current = field = None
                m = HEAD.match(line)
                if m:
                    rid = m.group(1)
                    current = {"file": path.name, "line": n, "fields": {}, "order": []}
                    if rid in blocks:              # the first definition stands; the copy is reported
                        problems.append(("duplicate-id", f"{where}: {rid} is also defined at "
                                         f"{blocks[rid]['file']}:{blocks[rid]['line']}"))
                    else:
                        blocks[rid] = current
                continue
            if current is None:
                continue
            m = FIELD.match(line)
            if m:
                field = m.group(1)
                if field in current["fields"]:
                    problems.append(("fields", f"{where}: the field {field!r} is repeated"))
                current["fields"][field] = m.group(2).strip()
                current["order"].append(field)
            elif line.strip() and not line.startswith((" ", "\t")):
                problems.append(("fields", f"{where}: text outside a field: {line[:60]!r}"))
            elif field is not None:
                current["fields"][field] += "\n" + line.strip()
    return blocks


def check_blocks(blocks: dict, defined: set, problems: list):
    """Field rules for every block; returns {P- ID: {R-/X- IDs that trace it}}."""
    traced = defaultdict(set)
    for rid, b in blocks.items():
        where, f = f"{b['file']}:{b['line']} {rid}", b["fields"]
        allowed = X_FIELDS if rid.startswith("X-") else R_FIELDS
        unknown = [name for name in b["order"] if name not in allowed]
        if unknown:
            problems.append(("fields", f"{where}: unknown field(s) {unknown}"))
        known = [name for name in b["order"] if name in allowed]
        if known != sorted(known, key=allowed.index):
            problems.append(("fields", f"{where}: fields out of order {known}"))
        if rid.startswith("X-"):
            ids = ids_in(f.get("Leaves out", ""))
            if not ids or not TAGS.sub("", f.get("Why", "")).strip():
                problems.append(("no-reason", f"{where}: a leave-out needs its elements and a reason"))
        else:
            missing = sorted(R_REQUIRED - set(f))
            if missing:
                problems.append(("fields", f"{where}: missing field(s) {missing}"))
            if "Test" in f and not TAGS.sub("", f["Test"]).strip():
                problems.append(("no-test", f"{where}: the Test field is empty"))
            ids = ids_in(f.get("Traces", ""))
            bare = TAGS.sub("", f.get("Traces", "")).strip().rstrip(".").strip()
            if not ids and bare != "none":
                problems.append(("fields", f"{where}: Traces names no P- ID; write `none`"))
            if "Traces" in f and not ids and not TAGS.sub("", f.get("Why ours", "")).strip():
                problems.append(("no-source", f"{where}: traces no P- ID and gives no reason"))
        for pid in ids:
            if pid not in defined:
                problems.append(("dangling-trace", f"{where}: {pid} is not a defined paper element"))
            traced[pid].add(rid)
    return traced


def parse_register(path: Path, problems: list):
    """{any ID: (canonical ID, task)}, and {canonical task-2 ID: (line index, decision cell)}."""
    if not path.exists():
        problems.append(("structure", f"{path} does not exist"))
        return {}, {}, []
    lines = path.read_text(encoding="utf-8").split("\n")
    bounds = section(lines, r"^##\s+The register")
    if bounds is None:
        problems.append(("structure", f"{path.name} has no '## The register' section"))
        return {}, {}, lines
    owner, task2 = {}, {}
    for header, body in tables(lines, *bounds):
        c_id, c_task, c_alias, c_dec = (column(header, p) for p in ("ID", "Task", "Aliases", "Decision"))
        if None in (c_id, c_task, c_alias, c_dec):
            continue
        for i, row in body:
            m = GAP.match(row[c_id])
            if not m:
                continue
            canon, task = m.group(0), row[c_task]
            for gap in [canon] + GAP.findall(row[c_alias]):
                owner[gap] = (canon, task)
            if task == "2":
                task2[canon] = (i, row[c_dec])
    return owner, task2, lines


def expected_cell(pid: str, traced: dict) -> str:
    return ", ".join(sorted(traced.get(pid, ()), key=id_key)) or PLACEHOLDER


def check_trace(path: Path, defined: set, traced: dict, all_ids: set, problems: list, write: bool):
    """The Requirement column of traceability.md, Part 2; with write, fill it first."""
    if not path.exists():
        problems.append(("structure", f"{path} does not exist"))
        return
    lines = path.read_text(encoding="utf-8").split("\n")
    bounds = part2_bounds(lines)
    if bounds is None:
        problems.append(("structure", f"{path.name} has no '## Part 2' section"))
        return
    seen = set()
    for header, body in tables(lines, *bounds):
        col = column(header, "Requirement")
        if col is None:
            problems.append(("structure", f"{path.name}: a Part 2 table has no Requirement column"))
            continue
        for i, row in body:
            pid = row[0]
            if pid not in defined or col >= len(row):
                continue                       # trace_coverage.py owns these defects
            seen.add(pid)
            want = expected_cell(pid, traced)
            if write and row[col] != want:
                row[col] = want
                lines[i] = "| " + " | ".join(row) + " |"
            for ref in REQ_ID.findall(row[col]):
                if ref not in all_ids:
                    problems.append(("unknown-ref", f"{path.name}:{i + 1}: {pid} names {ref}, which is not defined"))
            if row[col] != want:
                problems.append(("column", f"{path.name}:{i + 1}: {pid} reads {row[col]!r}, the requirements say {want!r}"))
    if write:
        path.write_text("\n".join(lines), encoding="utf-8")
    for pid in sorted(defined - seen, key=sort_key):
        problems.append(("structure", f"{path.name}: {pid} has no row in Part 2"))


def check_decisions(main: Path, blocks: dict, owner: dict, task2: dict, reg_lines: list, problems: list):
    """Decides and Depends-on fields, the decisions table, the register pointers, the pending table."""
    decided, pending = defaultdict(set), defaultdict(set)
    for rid, b in blocks.items():
        where = f"{b['file']}:{b['line']} {rid}"
        for name in ("Decides", "Depends on"):
            for gap in GAP.findall(b["fields"].get(name, "")):
                if gap not in owner:
                    problems.append(("unknown-row", f"{where}: {name} names {gap}, which no register row holds"))
                    continue
                canon, task = owner[gap]
                if name == "Decides" and task != "2":
                    problems.append(("boundary", f"{where}: decides {gap}, a row of task {task}"))
                elif name == "Depends on" and task == "2":
                    problems.append(("boundary", f"{where}: depends on {gap}, a task-2 row, which it should decide or cite by requirement"))
                (decided if name == "Decides" else pending)[canon if name == "Decides" else (task, canon)].add(rid)
    for canon in sorted(set(task2) - set(decided)):
        problems.append(("undecided", f"register row {canon} (task 2) is decided by no requirement"))

    lines = main.read_text(encoding="utf-8").split("\n") if main.exists() else []
    table_rows = {}
    bounds = section(lines, DECISIONS)
    if bounds is None:
        problems.append(("structure", f"{main.name} has no section 'Decisions on the register's task-2 rows'"))
    else:
        found = False
        for header, body in tables(lines, *bounds):
            c_row, c_status, c_by = (column(header, p) for p in ("Row", "Status", "Carried by"))
            if None in (c_row, c_status, c_by):
                continue
            found = True
            for i, row in body:
                where, canon = f"{main.name}:{i + 1}", row[c_row]
                if canon not in task2:
                    problems.append(("decision-table", f"{where}: {canon!r} is not a task-2 row of the register"))
                    continue
                if canon in table_rows:
                    problems.append(("decision-table", f"{where}: {canon} is listed twice"))
                status, by = row[c_status], set(REQ_ID.findall(row[c_by]))
                table_rows[canon] = (status, by)
                if status not in STATUSES:
                    problems.append(("decision-table", f"{where}: {canon} has status {status!r}"))
                for ref in sorted(by - set(blocks)):
                    problems.append(("unknown-ref", f"{where}: {canon} is carried by {ref}, which is not defined"))
                if by != decided.get(canon, set()):
                    problems.append(("decision-table", f"{where}: {canon} lists {sorted(by, key=id_key)}, "
                                     f"the requirements that decide it are {sorted(decided.get(canon, ()), key=id_key)}"))
        if not found:
            problems.append(("structure", f"{main.name}: the decisions section has no table with Row, Status and Carried by"))
        for canon in sorted(set(task2) - set(table_rows)):
            problems.append(("decision-table", f"{main.name}: register row {canon} (task 2) is not in the decisions table"))

    for canon, (i, cell) in sorted(task2.items()):
        m = POINTER.search(cell)
        where = f"unspecified.md:{i + 1}"
        if not m:
            problems.append(("pointer", f"{where}: {canon} carries no 'Task 2 decided it' pointer"))
        else:
            status, refs = m.group(1), set(REQ_ID.findall(m.group(2)))
            table_status = table_rows.get(canon, (None, None))[0]
            if refs != decided.get(canon, set()):
                problems.append(("pointer", f"{where}: {canon}'s pointer names {sorted(refs, key=id_key)}, the "
                                 f"requirements that decide it are {sorted(decided.get(canon, ()), key=id_key)}"))
            if table_status in STATUSES and status != table_status:
                problems.append(("pointer", f"{where}: {canon}'s pointer says {status}, the decisions table {table_status}"))

    want = defaultdict(set)
    for task, canon in pending:
        want[task].add(canon)
    got = defaultdict(set)
    bounds = section(lines, PENDING)
    if bounds is None:
        problems.append(("structure", f"{main.name} has no section 'What the requirements leave to other tasks'"))
        return decided
    for header, body in tables(lines, *bounds):
        c_task, c_rows = column(header, "Task"), column(header, "Rows")
        if None in (c_task, c_rows):
            continue
        for i, row in body:
            m = re.match(r"(\d+)", row[c_task])
            if m:
                got[m.group(1)] |= set(GAP.findall(row[c_rows]))
    for task in sorted(set(want) | set(got)):
        if want[task] != got[task]:
            missing, extra = sorted(want[task] - got[task]), sorted(got[task] - want[task])
            problems.append(("pending-table", f"{main.name}: task {task}: missing {missing}, not depended on {extra}"))
    return decided


def check(paper: Path, main: Path, req_dir: Path, write: bool = False):
    """Return (problems, summary); a problem is a (kind, message) pair."""
    problems = []
    defined_docs, _referenced, _gaps = collect(paper, [])   # trace_coverage.py reports its own problems
    defined = set(defined_docs)
    files = ([main] if main.exists() else []) + sorted(req_dir.glob("*.md"))
    if not main.exists():
        problems.append(("structure", f"{main} does not exist"))
    blocks = parse_requirements(files, problems)
    traced = check_blocks(blocks, defined, problems)
    for pid in sorted(defined, key=sort_key):
        refs = traced.get(pid, set())
        if not refs:
            problems.append(("unmapped", f"{pid} is traced by no requirement and left out by no decision"))
        elif any(r.startswith("X-") for r in refs) and any(r.startswith("R-") for r in refs):
            problems.append(("left-and-traced", f"{pid} is left out by {sorted(r for r in refs if r.startswith('X-'))} "
                             f"and traced by {sorted((r for r in refs if r.startswith('R-')), key=id_key)}"))
    owner, task2, reg_lines = parse_register(paper / "unspecified.md", problems)
    check_trace(paper / "traceability.md", defined, traced, set(blocks), problems, write)
    decided = check_decisions(main, blocks, owner, task2, reg_lines, problems)
    summary = {"defined": len(defined), "blocks": blocks, "traced": traced, "task2": task2, "decided": decided}
    return problems, summary


def report(write: bool) -> int:
    problems, s = check(PAPER, REQ_MAIN, REQ_DIR, write)
    reqs = [r for r in s["blocks"] if r.startswith("R-")]
    leaves = [r for r in s["blocks"] if r.startswith("X-")]
    by_r = {p for p, refs in s["traced"].items() if any(r.startswith("R-") for r in refs)}
    by_x = {p for p, refs in s["traced"].items() if all(r.startswith("X-") for r in refs)}
    per_area = defaultdict(int)
    for r in reqs:
        per_area[r[2:].rsplit("-", 1)[0]] += 1
    print(f"paper elements: {s['defined']} defined; {len(by_r)} traced by a requirement; {len(by_x)} left out")
    print(f"requirements: {len(reqs)} ({', '.join(f'{a} {per_area[a]}' for a in sorted(per_area, key=lambda a: id_key(f'R-{a}-0')))}); "
          f"leave-out decisions: {len(leaves)}")
    print(f"task-2 register rows: {len(s['task2'])}; decided by a requirement: {len(set(s['task2']) & set(s['decided']))}")
    for kind, message in problems:
        print(f"{kind}: {message}")
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


# ---------------------------------------------------------------------------------------------
# Self-test: a clean miniature of the real files, and one planted defect per problem kind.

SOURCE = "# A source\n## A stage · P-AAA-1 … 2\n### P-BBB-1 · a definition\n- **U-AAA-1 · a gap.**\n"
TRACE = """# Traceability
## Part 2
| ID | Element | Requirement | Component |
|---|---|---|---|
| P-AAA-1 | a step | R-RUN-1 | x |
| P-AAA-2 | a step | R-RUN-1, R-STG-1 | x |
| P-BBB-1 | a figure | X-1 | x |
## Part 3
"""
REGISTER = """# Register
## The register
| ID (entry) | Class | Question | Decision it forces [ours] | Task | Priority | Aliases (entry) |
|---|---|---|---|---|---|---|
| U-AAA-1 (an) | UNSPECIFIED | q | d **Task 2 decided it: confirmed, in R-STG-1.** | 2 | blocks 1 | U-AAA-2 (an) |
| U-BBB-1 (an) | UNSPECIFIED | q | d | 3 | later | none |
## Why these rows merge
"""
MAIN = """# Requirements
## Decisions on the register's task-2 rows
| Row | Priority | Status | Decision | Reason | Carried by |
|---|---|---|---|---|---|
| U-AAA-1 | blocks 1 | confirmed | d | r | R-STG-1 |
## Elements left out
### X-1 · A figure
- **Leaves out.** P-BBB-1 [Fig. 1].
- **Why.** Nothing to reproduce [ours].
## What the requirements leave to other tasks
| Task | Rows the requirements depend on |
|---|---|
| 3 · components | U-BBB-1 |
"""
AREA1 = """# Area
### R-RUN-1 · A run
- **Requirement.** It runs [§3].
- **Traces.** P-AAA-1 … 2 [§3].
- **Test.** It ran [ours].
### R-STG-1 · A stage
- **Requirement.** It stages [ours].
- **Traces.** P-AAA-2 [§3.1].
- **Why ours.** A reason [ours].
- **Decides.** U-AAA-2 [ours].
- **Depends on.** U-BBB-1 [ours].
- **Test.** It staged:
  - first case [ours].
"""


def selftest() -> int:
    """Each planted defect must produce exactly the expected problem kinds; the clean twin none."""
    def edit(text, old, new):
        assert old in text, old
        return text.replace(old, new)
    cases = {  # name: ({file: text} changes to the clean set, expected kinds)
        "clean": ({}, set()),
        "an element nobody traces": ({"area": edit(AREA1, "P-AAA-1 … 2 [§3]", "P-AAA-2 [§3]"),
                                      "trace": edit(TRACE, "| P-AAA-1 | a step | R-RUN-1 |", f"| P-AAA-1 | a step | {PLACEHOLDER} |")},
                                     {"unmapped"}),
        "a placeholder left in the column": ({"trace": edit(TRACE, "| R-RUN-1 | x |", f"| {PLACEHOLDER} | x |")}, {"column"}),
        "a one-way link": ({"trace": edit(TRACE, "| R-RUN-1, R-STG-1 |", "| R-RUN-1 |")}, {"column"}),
        "a requirement that does not exist": ({"trace": edit(TRACE, "| R-RUN-1, R-STG-1 |", "| R-RUN-1, R-STG-9 |")},
                                              {"column", "unknown-ref"}),
        "left out and traced": ({"area": edit(AREA1, "P-AAA-2 [§3.1]", "P-AAA-2, P-BBB-1 [§3.1]"),
                                 "trace": edit(TRACE, "| X-1 |", "| R-STG-1, X-1 |")}, {"left-and-traced"}),
        "a trace to nothing": ({"area": edit(AREA1, "P-AAA-2 [§3.1]", "P-AAA-2, P-CCC-1 [§3.1]")}, {"dangling-trace"}),
        "an ID defined twice": ({"area": AREA1 + "### R-RUN-1 · Again\n- **Requirement.** x [ours].\n"
                                 "- **Traces.** P-AAA-1 [§3].\n- **Test.** y [ours].\n"}, {"duplicate-id"}),
        "a missing field": ({"area": edit(AREA1, "- **Traces.** P-AAA-1 … 2 [§3].\n", "")},
                            {"fields", "unmapped", "column"}),
        "fields out of order": ({"area": edit(AREA1, "- **Why ours.** A reason [ours].\n- **Decides.** U-AAA-2 [ours].\n",
                                              "- **Decides.** U-AAA-2 [ours].\n- **Why ours.** A reason [ours].\n")}, {"fields"}),
        "text outside a field": ({"area": edit(AREA1, "- **Test.** It ran [ours].\n", "- **Test.** It ran [ours].\nStray text.\n")},
                                 {"fields"}),
        "an empty test": ({"area": edit(AREA1, "- **Test.** It ran [ours].", "- **Test.** [ours]")}, {"no-test"}),
        "no trace and no reason": ({"area": AREA1 + "### R-OPS-1 · Ours\n- **Requirement.** x [ours].\n"
                                    "- **Traces.** none.\n- **Test.** y [ours].\n"}, {"no-source"}),
        "a leave-out with no reason": ({"main": edit(MAIN, "- **Why.** Nothing to reproduce [ours].", "- **Why.** [ours]")},
                                       {"no-reason"}),
        "deciding another task's row": ({"area": edit(AREA1, "- **Decides.** U-AAA-2 [ours].", "- **Decides.** U-AAA-2, U-BBB-1 [ours]."),
                                         "main": edit(MAIN, "| 3 · components | U-BBB-1 |", "| 3 · components | U-BBB-1 |")},
                                        {"boundary"}),
        "depending on a task-2 row": ({"area": edit(AREA1, "- **Depends on.** U-BBB-1 [ours].", "- **Depends on.** U-BBB-1, U-AAA-1 [ours].")},
                                      {"boundary", "pending-table"}),
        "a row the register lacks": ({"area": edit(AREA1, "- **Depends on.** U-BBB-1 [ours].", "- **Depends on.** U-BBB-1, U-ZZZ-9 [ours].")},
                                     {"unknown-row"}),
        "a task-2 row nobody decides": ({"area": edit(AREA1, "- **Decides.** U-AAA-2 [ours].\n", ""),
                                         "main": edit(MAIN, "| R-STG-1 |\n", "|  |\n"),
                                         "register": edit(REGISTER, " **Task 2 decided it: confirmed, in R-STG-1.**", "")},
                                        {"undecided", "pointer"}),
        "a bad status": ({"main": edit(MAIN, "| confirmed |", "| agreed |")}, {"decision-table"}),
        "a table that disagrees": ({"main": edit(MAIN, "| R-STG-1 |\n", "| R-RUN-1 |\n")}, {"decision-table"}),
        "a row missing from the table": ({"main": edit(MAIN, "| U-AAA-1 | blocks 1 | confirmed | d | r | R-STG-1 |\n", "")},
                                         {"decision-table"}),
        "a register row without its pointer": ({"register": edit(REGISTER, " **Task 2 decided it: confirmed, in R-STG-1.**", "")},
                                               {"pointer"}),
        "a pointer that disagrees": ({"register": edit(REGISTER, "confirmed, in R-STG-1", "refined, in R-STG-1")}, {"pointer"}),
        "a pending table that drifts": ({"main": edit(MAIN, "| 3 · components | U-BBB-1 |", "| 3 · components | U-BBB-1, U-AAA-1 |")},
                                        {"pending-table"}),
        "no decisions section": ({"main": edit(MAIN, "## Decisions on the register's task-2 rows", "## Decisions")},
                                 {"structure"}),
        "a pointer naming the wrong requirement": ({"register": edit(REGISTER, "confirmed, in R-STG-1", "confirmed, in R-RUN-1")},
                                                   {"pointer"}),
    }
    failed = 0
    for name, (changes, want) in cases.items():
        texts = {"source": SOURCE, "trace": TRACE, "register": REGISTER, "main": MAIN, "area": AREA1} | changes
        with tempfile.TemporaryDirectory() as tmp:
            paper, req_dir = Path(tmp) / "paper", Path(tmp) / "requirements"
            paper.mkdir()
            req_dir.mkdir()
            (paper / "analysis.md").write_text(texts["source"], encoding="utf-8")
            (paper / "traceability.md").write_text(texts["trace"], encoding="utf-8")
            (paper / "unspecified.md").write_text(texts["register"], encoding="utf-8")
            (Path(tmp) / "requirements.md").write_text(texts["main"], encoding="utf-8")
            (req_dir / "01-area.md").write_text(texts["area"], encoding="utf-8")
            got = {kind for kind, _ in check(paper, Path(tmp) / "requirements.md", req_dir)[0]}
        ok = got == want
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: got {sorted(got) or 'no problem'}, expected {sorted(want) or 'no problem'}")
    with tempfile.TemporaryDirectory() as tmp:     # --write fills the column, and the result is clean
        paper, req_dir = Path(tmp) / "paper", Path(tmp) / "requirements"
        paper.mkdir()
        req_dir.mkdir()
        (paper / "analysis.md").write_text(SOURCE, encoding="utf-8")
        blank = TRACE.replace("| R-RUN-1 |", f"| {PLACEHOLDER} |").replace("| R-RUN-1, R-STG-1 |", f"| {PLACEHOLDER} |")
        (paper / "traceability.md").write_text(blank, encoding="utf-8")
        (paper / "unspecified.md").write_text(REGISTER, encoding="utf-8")
        (Path(tmp) / "requirements.md").write_text(MAIN, encoding="utf-8")
        (req_dir / "01-area.md").write_text(AREA1, encoding="utf-8")
        before = {k for k, _ in check(paper, Path(tmp) / "requirements.md", req_dir)[0]}
        after = {k for k, _ in check(paper, Path(tmp) / "requirements.md", req_dir, write=True)[0]}
        filled = (paper / "traceability.md").read_text(encoding="utf-8") == TRACE
    ok = before == {"column"} and after == set() and filled
    failed += not ok
    print(f"{'ok  ' if ok else 'FAIL'} --write fills the column: before {sorted(before)}, after {sorted(after) or 'no problem'}, "
          f"identical to the clean file: {filled}")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--selftest"]:
        return selftest()
    if argv[1:] in ([], ["--write"]):
        return report(write=argv[1:] == ["--write"])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
