"""Check that every paper element maps to a requirement, or to a recorded decision to leave it out.

The completeness control of TODO task 2 (docs/requirements.md, section "Controls"). It reads:
  - docs/requirements.md and docs/requirements/*.md: requirements, each a heading
    "### R-<AREA>-n · <title>" followed by its fields as top-level list items
    ("- **Requirement.** ...", then Traces, Departs from, Why ours, Decides, Depends on, Test, in
    that order);
    decisions to leave an element out, "### X-n · <title>" with "Leaves out", "Why" and, when it rests
    on another task's row, "Depends on"; the table of
    decisions on the register's task-2 rows; and the table of rows left to other tasks;
  - docs/paper/traceability.md, Part 2, whose "Requirement" column must name, for each P- ID, the
    requirements and leave-outs that trace it;
  - docs/paper/unspecified.md, the register, whose task-2 rows must each point to their decision;
  - the paper elements, defined as trace_coverage.py defines them, and the value-and-mechanism pairs
    of analysis.md section 6 ("P-LIM-4 uses P-CFG-1").

Problem kinds (any one makes the exit status 1):
  unmapped          a defined P- ID that no requirement traces and no X- decision leaves out
  left-and-traced   a P- ID that an X- decision leaves out and a requirement also traces
  dangling-trace    a Traces or Leaves-out field names a P- ID that nothing defines
  duplicate-id      an R- or X- ID defined twice
  fields            a missing, repeated, unknown or out-of-order field, or text outside a field
  no-test           a requirement whose Test field is empty
  no-source         a requirement that traces no P- ID and gives no reason under "Why ours"
  no-reason         an X- decision with no element under "Leaves out", or no reason under "Why"
  placeholder       a Requirement or Test field that holds only a placeholder (TBD, TODO, ?, —)
  malformed-id      a P- ID in a trace field, or a U-/A- ID under Decides or Depends on, written with a
                    dash, case or padding of the wrong kind, or a
                    range whose endpoint is padded, zero or before its start ("P-ABL-1 … 02", "P-ABL-3 … 1")
  departs           a "Departs from" field names a P- ID that the requirement does not trace
  split-pair        a value and the mechanism that uses it (analysis.md section 6) share no requirement
  stage-table       the default stage configuration lacks a stage (Table 1's eleven, A_Coder and the tail) or a
                    parameter column, or has an empty cell
  column            a Requirement cell of traceability.md that differs from what the requirements say
  unknown-ref       a cell of a table here names an R- or X- ID that is not defined
  unknown-row       a Decides or Depends-on field names an ID that no register row holds
  boundary          a requirement decides a row that task 2 does not own, or depends on one it does
  inline-dependency a Depends-on row that the Requirement text (an X- decision's Why) does not name
  task-attribution  a Depends-on clause that names a row as one task's ("U-TOP-2, task 3") when the
                    register gives it to another
  integrity-dependency  a Requirement that names the harness, a data role, a gain or the verified
                    table, and depends on neither U-INT-4 nor U-TOP-5 (task 6's blocking rows); or one
                    that cites a rule of task 6's (IR-n) and depends on none of its four blocking rows
  test-tier         a Test field that does not open with its tier, "Logic" or "Enforcement"
  undecided         a task-2 register row that no requirement decides
  decision-table    the decisions table: a missing, repeated or foreign row, a bad status, or a
                    "Carried by" cell that differs from the requirements that decide the row
  pointer           a task-2 register row without its pointer, or whose pointer disagrees with the table
  pending-table     the table of rows left to other tasks differs from the Depends-on fields
  structure         a file, a section or a table column is missing, a table row has more or fewer cells
                    than its header, or a file of docs/requirements/ defines no requirement

Usage:
  python3 playground/paper/requirement_coverage.py             # check the real files
  python3 playground/paper/requirement_coverage.py --write     # fill traceability.md's column, then check
  python3 playground/paper/requirement_coverage.py --selftest  # plants each defect, shows it is caught
                                                               # (requirement_coverage_selftest.py)
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace_coverage import RANGE, collect, ids_in, part2_bounds, sort_key  # noqa: E402  (one definition of a P- ID)

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
R_FIELDS = ["Requirement", "Traces", "Departs from", "Why ours", "Decides", "Depends on", "Test"]
R_REQUIRED = {"Requirement", "Traces", "Test"}
X_FIELDS = ["Leaves out", "Why", "Depends on"]
AREAS = ["RUN", "PRIM", "STG", "AGT", "STATE", "INT", "MEAS", "OPS"]   # reading order, then X-
STATUSES = ("confirmed", "refined", "replaced")
PLACEHOLDER = "— (task 2)"
FILLER = re.compile(r"^(?:tbd|todo|tba|\?+|—|–|-|…)$", re.I)
# A P- ID with the wrong dash, case or padding: "P–ABL–1", "p-abl-1", "P-ABL-01". Only the strict form counts.
LOOSE_PID = re.compile(r"\bP[-‐–—][A-Z]+[-‐–—]\d+\b", re.I)
STRICT_PID = re.compile(r"^P-[A-Z]+-[1-9]\d*$")
LOOSE_GAP = re.compile(r"\b[UA][-‐–—][A-Z]+[-‐–—]\d+\b", re.I)
STRICT_GAP = re.compile(r"^[UA]-[A-Z]+-[1-9]\d*$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
USES = re.compile(r"(P-[A-Z]+-\d+) uses (P-[A-Z]+-\d+(?: and P-[A-Z]+-\d+)*)")
STAGE_TABLE = r"^##\s+The default stage configuration"
STAGE_KEYS = ["LIM", "SEED", "BASE", "SUB", "FULL", "CODER", "EVO", "SEL", "ABL", "DRAFT", "PEER", "META", "TAIL"]
# Words that put a requirement on task 6's ground (the evaluation integrity review, EI-18): such a requirement
# must name U-INT-4 or U-TOP-5 under "Depends on", so that task 6's decisions reach it when they land.
INTEGRITY_TERMS = re.compile(r"\bharness\b|\bsplits?\b|\bgains?\b|\bverified (?:results )?table\b|\bvalidation\b"
                             r"|\b(?:search|report)[- ]role\b|\btest (?:event|split|set)\b", re.I)
TASK6_BLOCKING = {"U-INT-4", "U-TOP-5"}
# A clause that states one of task 6's rules cites it as IR-n, and rests on one of its four blocking rows.
IR_CITE = re.compile(r"\bIR-\d+")
TASK6_ALL = TASK6_BLOCKING | {"A-INT-1", "A-INT-3"}
TIER = re.compile(r"(?:Logic|Enforcement)\b")
STAGE_COLUMNS = ["Stage", "Generator", "Judged", "Assessor", "Verdict", "Guard", "Limit", "At the limit", "Nesting"]
DEPARTS = " (departs)"
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
        text = HTML_COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), path.read_text(encoding="utf-8"))
        for n, line in enumerate(text.split("\n"), 1):
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
    """Field rules for every block; returns {P- ID: {R-/X- IDs that trace it}} and
    {P- ID: {R- IDs that depart from it}}."""
    traced, departs = defaultdict(set), defaultdict(set)
    for rid, b in blocks.items():
        where, f = f"{b['file']}:{b['line']} {rid}", b["fields"]
        allowed = X_FIELDS if rid.startswith("X-") else R_FIELDS
        unknown = [name for name in b["order"] if name not in allowed]
        if unknown:
            problems.append(("fields", f"{where}: unknown field(s) {unknown}"))
        known = [name for name in b["order"] if name in allowed]
        if known != sorted(known, key=allowed.index):
            problems.append(("fields", f"{where}: fields out of order {known}"))
        for name in ("Traces", "Leaves out", "Departs from"):
            for token in LOOSE_PID.findall(f.get(name, "")):
                if not STRICT_PID.match(token):
                    problems.append(("malformed-id", f"{where}: {name} writes {token!r}; write P-<KEY>-<n>"))
            for m in RANGE.finditer(f.get(name, "")):     # ids_in() would read "… 02" as 2, and "3 … 1" as 1 … 3
                first, last = m.group(2), m.group(3)
                if not re.fullmatch(r"[1-9]\d*", last) or int(last) <= int(first):
                    problems.append(("malformed-id", f"{where}: {name} writes the range {m.group(0)!r}"))
        for name in ("Decides", "Depends on"):
            for token in LOOSE_GAP.findall(f.get(name, "")):
                if not STRICT_GAP.match(token):
                    problems.append(("malformed-id", f"{where}: {name} writes {token!r}; write U-<KEY>-<n> or A-<KEY>-<n>"))
        for name in ("Requirement", "Test"):
            bare = TAGS.sub("", f.get(name, "")).strip()
            core = bare.rstrip(" .").strip()                # "TBD [ours]." and "..." are placeholders too
            if name in f and ((bare and (not core or FILLER.match(core))) or (name == "Requirement" and not bare)):
                problems.append(("placeholder", f"{where}: the {name} field holds only a placeholder"))
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
            test = TAGS.sub("", f.get("Test", "")).strip()
            if test and not FILLER.match(test.rstrip(" .").strip()) and not TIER.match(test):
                problems.append(("test-tier", f"{where}: the Test field opens with neither Logic nor Enforcement"))
            for pid in ids_in(f.get("Departs from", "")):
                if pid not in ids_in(f.get("Traces", "")):
                    problems.append(("departs", f"{where}: departs from {pid}, which it does not trace"))
                else:
                    departs[pid].add(rid)
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
    return traced, departs


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
            if len(row) != len(header):
                problems.append(("structure", f"{path.name}:{i + 1}: a register row has {len(row)} cells, its header {len(header)}"))
                continue
            m = GAP.match(row[c_id])
            if not m:
                continue
            canon, task = m.group(0), row[c_task]
            for gap in [canon] + GAP.findall(row[c_alias]):
                owner[gap] = (canon, task)
            if task == "2":
                task2[canon] = (i, row[c_dec])
    return owner, task2, lines


def expected_cell(pid: str, traced: dict, departs: dict) -> str:
    """The cell's text: the requirements and leave-outs in reading order, a departure marked."""
    refs = sorted(traced.get(pid, ()), key=id_key)
    return ", ".join(r + (DEPARTS if r in departs.get(pid, ()) else "") for r in refs) or PLACEHOLDER


def check_trace(path: Path, defined: set, traced: dict, departs: dict, all_ids: set, problems: list, write: bool):
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
            want = expected_cell(pid, traced, departs)
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
                if len(row) != len(header):
                    problems.append(("decision-table", f"{main.name}:{i + 1}: the row has {len(row)} cells, its header {len(header)}"))
                    continue
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
        return decided, table_rows
    for header, body in tables(lines, *bounds):
        c_task, c_rows = column(header, "Task"), column(header, "Rows")
        if None in (c_task, c_rows):
            continue
        for i, row in body:
            if len(row) != len(header):
                problems.append(("structure", f"{main.name}:{i + 1}: a row of the pending table has {len(row)} cells"))
                continue
            m = re.match(r"(\d+)", row[c_task])
            if m:
                got[m.group(1)] |= set(GAP.findall(row[c_rows]))
    for task in sorted(set(want) | set(got)):
        if want[task] != got[task]:
            missing, extra = sorted(want[task] - got[task]), sorted(got[task] - want[task])
            problems.append(("pending-table", f"{main.name}: task {task}: missing {missing}, not depended on {extra}"))
    return decided, table_rows


def check_dependencies(blocks: dict, owner: dict, problems: list):
    """A requirement names each row it depends on beside the clause that rests on it, and one on task 6's
    ground depends on U-INT-4 or U-TOP-5 (the evaluation integrity review, EI-18 and EI-19)."""
    for rid, b in blocks.items():
        is_x = rid.startswith("X-")
        where, text = f"{b['file']}:{b['line']} {rid}", b["fields"].get("Why" if is_x else "Requirement", "")
        deps = GAP.findall(b["fields"].get("Depends on", ""))
        named = set(GAP.findall(text))
        for gap in sorted(set(deps) - named):
            problems.append(("inline-dependency", f"{where}: depends on {gap}, which its "
                             f"{'Why' if is_x else 'Requirement'} text does not name"))
        for clause in b["fields"].get("Depends on", "").split(";"):    # "U-TOP-2, task 3; U-INT-4, task 6"
            said = re.search(r"\btask (\d+)\b", clause)
            for gap in GAP.findall(clause) if said else []:
                task = owner.get(gap, (gap, None))[1]
                if task is not None and task != said.group(1):
                    problems.append(("task-attribution", f"{where}: gives {gap} to task {said.group(1)}; "
                                     f"the register gives it to task {task}"))
        if is_x:
            continue
        canon = {owner.get(gap, (gap, ""))[0] for gap in deps}
        term = INTEGRITY_TERMS.search(text)
        if term and not canon & TASK6_BLOCKING:
            problems.append(("integrity-dependency", f"{where}: names {term.group(0)!r} and depends on neither "
                             f"{' nor '.join(sorted(TASK6_BLOCKING))}"))
        cite = IR_CITE.search(text)
        if cite and not canon & TASK6_ALL:
            problems.append(("integrity-dependency", f"{where}: cites {cite.group(0)} and depends on none of "
                             f"{', '.join(sorted(TASK6_ALL))}"))


def check_stage_table(files: list[Path], problems: list):
    """The default stage configuration: every stage a row, every parameter a column, no empty cell."""
    for path in files:
        lines = path.read_text(encoding="utf-8").split("\n")
        bounds = section(lines, STAGE_TABLE)
        if bounds is None:
            continue
        for header, body in tables(lines, *bounds):
            if [h for h, want in zip(header, STAGE_COLUMNS) if not h.startswith(want)] or len(header) != len(STAGE_COLUMNS):
                problems.append(("stage-table", f"{path.name}: the columns are {header}, the parameters are {STAGE_COLUMNS}"))
            seen = [row[0] for _, row in body]
            for key in STAGE_KEYS:
                if seen.count(key) != 1:
                    problems.append(("stage-table", f"{path.name}: stage {key} has {seen.count(key)} row(s)"))
            for i, row in body:
                if row[0] not in STAGE_KEYS:
                    problems.append(("stage-table", f"{path.name}:{i + 1}: {row[0]!r} is not a stage of the default configuration"))
                if len(row) != len(header) or any(not TAGS.sub("", c).strip() for c in row):
                    problems.append(("stage-table", f"{path.name}:{i + 1}: stage {row[0]} has a missing or empty cell"))
            return
    problems.append(("structure", "no requirement file has the section 'The default stage configuration'"))


def check_pairs(paper: Path, traced: dict, problems: list):
    """A value of App. A.2 and the stage element that uses it share a requirement (analysis.md section 6)."""
    source = paper / "analysis.md"
    text = source.read_text(encoding="utf-8") if source.exists() else ""
    for m in USES.finditer(text):
        mechanism = m.group(1)
        for value in re.findall(r"P-[A-Z]+-\d+", m.group(2)):
            a = {r for r in traced.get(mechanism, ()) if r.startswith("R-")}
            b = {r for r in traced.get(value, ()) if r.startswith("R-")}
            if a and b and not a & b:
                problems.append(("split-pair", f"{mechanism} uses {value}, but they share no requirement: "
                                 f"{sorted(a, key=id_key)} against {sorted(b, key=id_key)}"))


def check(paper: Path, main: Path, req_dir: Path, write: bool = False):
    """Return (problems, summary); a problem is a (kind, message) pair."""
    problems = []
    defined_docs, _referenced, _gaps = collect(paper, [])   # trace_coverage.py reports its own problems
    defined = set(defined_docs)
    files = ([main] if main.exists() else []) + sorted(req_dir.glob("*.md"))
    if not main.exists():
        problems.append(("structure", f"{main} does not exist"))
    blocks = parse_requirements(files, problems)
    for path in sorted(req_dir.glob("*.md")):
        if not any(b["file"] == path.name and r.startswith("R-") for r, b in blocks.items()):
            problems.append(("structure", f"{path.name} defines no requirement: a second scheme, or a stray file"))
    if not any(r.startswith("R-") for r in blocks):
        problems.append(("structure", "no requirement was parsed"))
    traced, departs = check_blocks(blocks, defined, problems)
    check_stage_table(files, problems)
    check_pairs(paper, traced, problems)
    for pid in sorted(defined, key=sort_key):
        refs = traced.get(pid, set())
        if not refs:
            problems.append(("unmapped", f"{pid} is traced by no requirement and left out by no decision"))
        elif any(r.startswith("X-") for r in refs) and any(r.startswith("R-") for r in refs):
            problems.append(("left-and-traced", f"{pid} is left out by {sorted(r for r in refs if r.startswith('X-'))} "
                             f"and traced by {sorted((r for r in refs if r.startswith('R-')), key=id_key)}"))
    owner, task2, reg_lines = parse_register(paper / "unspecified.md", problems)
    check_trace(paper / "traceability.md", defined, traced, departs, set(blocks), problems, write)
    decided, table_rows = check_decisions(main, blocks, owner, task2, reg_lines, problems)
    check_dependencies(blocks, owner, problems)
    summary = {"defined": defined, "blocks": blocks, "traced": traced, "departs": departs,
               "task2": task2, "decided": decided, "owner": owner, "table": table_rows}
    return problems, summary


def report(write: bool) -> int:
    problems, s = check(PAPER, REQ_MAIN, REQ_DIR, write)
    reqs = sorted((r for r in s["blocks"] if r.startswith("R-")), key=id_key)
    leaves = [r for r in s["blocks"] if r.startswith("X-")]
    per_key = defaultdict(lambda: [0, 0, 0, 0])          # defined, traced, departed from, left out
    for pid in s["defined"]:
        key, refs = pid.rsplit("-", 1)[0], s["traced"].get(pid, set())
        row = per_key[key]
        row[0] += 1
        row[1] += any(r.startswith("R-") for r in refs)
        row[2] += bool(s["departs"].get(pid))
        row[3] += bool(refs) and all(r.startswith("X-") for r in refs)
    print(f"{'key':<11}{'defined':>8}{'traced':>8}{'departs':>9}{'left out':>10}")
    for key in sorted(per_key):
        print(f"{key:<11}" + "".join(f"{v:>{w}}" for v, w in zip(per_key[key], (8, 8, 9, 10))))
    totals = [sum(v[i] for v in per_key.values()) for i in range(4)]
    print(f"{'total':<11}" + "".join(f"{v:>{w}}" for v, w in zip(totals, (8, 8, 9, 10))))
    per_area = defaultdict(int)
    for r in reqs:
        per_area[r[2:].rsplit("-", 1)[0]] += 1
    print(f"requirements: {len(reqs)} ({', '.join(f'{a} {n}' for a, n in per_area.items())}); "
          f"leave-out decisions: {len(leaves)}")
    statuses = defaultdict(int)
    for status, _by in s["table"].values():
        statuses[status] += 1
    print(f"task-2 register rows: {len(s['task2'])}; decided by a requirement: {len(set(s['task2']) & set(s['decided']))}; "
          f"in the decisions table: {', '.join(f'{n} {k}' for k, n in sorted(statuses.items())) or 'none'}")
    departures = defaultdict(list)
    for pid, rids in s["departs"].items():
        for rid in rids:
            departures[rid].append(pid)
    for rid in sorted(departures, key=id_key):
        print(f"  departs: {rid} from {', '.join(sorted(departures[rid], key=sort_key))}")
    pending = defaultdict(set)
    for rid, b in s["blocks"].items():
        for gap in GAP.findall(b["fields"].get("Depends on", "")):
            canon, task = s["owner"].get(gap, (gap, "?"))
            pending[task].add(canon)
    for task in sorted(pending):
        print(f"  pending, task {task}: {len(pending[task])} row(s): {', '.join(sorted(pending[task]))}")
    for kind, message in problems:
        print(f"{kind}: {message}")
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--selftest"]:
        from requirement_coverage_selftest import selftest   # the control lives beside the checker it tests
        return selftest()
    if argv[1:] in ([], ["--write"]):
        return report(write=argv[1:] == ["--write"])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
