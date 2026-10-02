"""The self-test of requirement_coverage.py: a clean miniature of the real files, and one planted
defect per problem kind. Each planted twin must yield exactly its expected kinds, and the clean twin
none; a last case shows that --write fills traceability.md's column and leaves it clean.

Run it through the checker: python3 playground/paper/requirement_coverage.py --selftest

⛔ WHY NOT keep it inside requirement_coverage.py: with its fixtures the file passed CLAUDE.md's cap of
600 lines, and the control that proves the checker can fail is a job of its own.
"""

import tempfile
from pathlib import Path

from requirement_coverage import DEPARTS, PLACEHOLDER, STAGE_COLUMNS, STAGE_KEYS, check


SOURCE = """# A source
## A stage · P-AAA-1 … 2
### P-BBB-1 · a definition
### P-CCC-1 · a value
- P-AAA-2 uses P-CCC-1 [ours].
- **U-AAA-1 · a gap.**
"""
TRACE = f"""# Traceability
## Part 2
| ID | Element | Requirement | Component |
|---|---|---|---|
| P-AAA-1 | a step | R-RUN-1{DEPARTS} | x |
| P-AAA-2 | a step | R-RUN-1, R-STG-1 | x |
| P-BBB-1 | a figure | X-1 | x |
| P-CCC-1 | a value | R-STG-1 | x |
## Part 3
"""
REGISTER = """# Register
## The register
| ID (entry) | Class | Question | Decision it forces [ours] | Task | Priority | Aliases (entry) |
|---|---|---|---|---|---|---|
| U-AAA-1 (an) | UNSPECIFIED | q | d **Task 2 decided it: confirmed, in R-STG-1.** | 2 | blocks 1 | U-AAA-2 (an) |
| U-BBB-1 (an) | UNSPECIFIED | q | d | 3 | later | none |
| U-INT-4 (an) | UNSPECIFIED | q | d | 6 | blocks 3 | U-ART-16 (an) |
| U-CCC-1 (an) | UNSPECIFIED | q | d | 5 | later | none |
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
- **Why.** Nothing to reproduce, as U-CCC-1 decides [ours].
- **Depends on.** U-CCC-1, task 5 [ours].
## What the requirements leave to other tasks
| Task | Rows the requirements depend on |
|---|---|
| 3 · components | U-BBB-1 |
| 5 · scope | U-CCC-1 |
| 6 · integrity | U-INT-4 |
"""
STAGES = ("## The default stage configuration\n| " + " | ".join(STAGE_COLUMNS) + " |\n|" + "---|" * len(STAGE_COLUMNS)
          + "\n" + "".join(f"| {k} |" + " v |" * (len(STAGE_COLUMNS) - 1) + "\n" for k in STAGE_KEYS))
AREA1 = "# Area\n" + STAGES + """## The requirements
### R-RUN-1 · A run
- **Requirement.** It runs [§3].
- **Traces.** P-AAA-1 … 2 [§3].
- **Departs from.** P-AAA-1: done another way [ours].
- **Test.** Logic: it ran [ours].
### R-STG-1 · A stage
- **Requirement.** It stages as U-BBB-1 decides, scored by the harness (U-INT-4) [ours].
- **Traces.** P-AAA-2, P-CCC-1 [§3.1].
- **Why ours.** A reason [ours].
- **Decides.** U-AAA-2 [ours].
- **Depends on.** U-BBB-1, task 3; U-INT-4, task 6 [ours].
- **Test.** Logic, in mock mode: it staged:
  - first case [ours].
"""
OURS_REQ = "### R-OPS-1 · Ours\n- **Requirement.** x [ours].\n- **Traces.** {traces}.\n{why}- **Test.** Logic: y [ours].\n"


def selftest() -> int:
    """Each planted defect must produce exactly the expected problem kinds; the clean twin none."""
    def edit(text, old, new):
        assert old in text, old
        return text.replace(old, new)
    traces_1 = "- **Traces.** P-AAA-1 … 2 [§3].\n- **Departs from.** P-AAA-1: done another way [ours].\n"
    cases = {  # name: ({file: text} changes to the clean set, expected kinds)
        "clean": ({}, set()),
        "an element nobody traces": ({"area": edit(AREA1, traces_1, "- **Traces.** P-AAA-2 [§3].\n"),
                                      "trace": edit(TRACE, f"| R-RUN-1{DEPARTS} |", f"| {PLACEHOLDER} |")}, {"unmapped"}),
        "a placeholder left in the column": ({"trace": edit(TRACE, f"| R-RUN-1{DEPARTS} |", f"| {PLACEHOLDER} |")}, {"column"}),
        "a one-way link": ({"trace": edit(TRACE, "| R-RUN-1, R-STG-1 |", "| R-RUN-1 |")}, {"column"}),
        "a requirement that does not exist": ({"trace": edit(TRACE, "| R-RUN-1, R-STG-1 |", "| R-RUN-1, R-STG-9 |")},
                                              {"column", "unknown-ref"}),
        "left out and traced": ({"area": edit(AREA1, "P-AAA-2, P-CCC-1 [§3.1]", "P-AAA-2, P-CCC-1, P-BBB-1 [§3.1]"),
                                 "trace": edit(TRACE, "| X-1 |", "| R-STG-1, X-1 |")}, {"left-and-traced"}),
        "a trace to nothing": ({"area": edit(AREA1, "P-AAA-2, P-CCC-1 [§3.1]", "P-AAA-2, P-CCC-1, P-DDD-1 [§3.1]")},
                               {"dangling-trace"}),
        "a malformed ID": ({"area": edit(AREA1, "P-AAA-2, P-CCC-1 [§3.1]", "P-AAA-2, P-CCC-1, P–AAA–1 [§3.1]")}, {"malformed-id"}),
        "a padded range endpoint": ({"area": edit(AREA1, "P-AAA-1 … 2 [§3]", "P-AAA-1 … 02 [§3]")}, {"malformed-id"}),
        "a backwards range": ({"area": edit(AREA1, "P-AAA-1 … 2 [§3]", "P-AAA-2 … 1 [§3]")}, {"malformed-id"}),
        "a truncated decision row": ({"main": edit(MAIN, "| U-AAA-1 | blocks 1 | confirmed | d | r | R-STG-1 |",
                                                   "| U-AAA-1 | blocks 1 | confirmed | d | r |")}, {"decision-table"}),
        "a truncated register row": ({"register": edit(REGISTER, "| 3 | later | none |", "| 3 |")},
                                     {"structure", "unknown-row", "pending-table"}),
        "a truncated pending row": ({"main": edit(MAIN, "| 3 · components | U-BBB-1 |", "| 3 · components |")},
                                    {"structure", "pending-table"}),
        "an ID defined twice": ({"area": AREA1 + "### R-RUN-1 · Again\n- **Requirement.** x [ours].\n"
                                 "- **Traces.** P-AAA-1 [§3].\n- **Test.** Logic: y [ours].\n"}, {"duplicate-id"}),
        "a missing field": ({"area": edit(AREA1, traces_1, "- **Departs from.** P-AAA-1: done another way [ours].\n")},
                            {"fields", "unmapped", "column", "departs"}),
        "fields out of order": ({"area": edit(AREA1, "- **Why ours.** A reason [ours].\n- **Decides.** U-AAA-2 [ours].\n",
                                              "- **Decides.** U-AAA-2 [ours].\n- **Why ours.** A reason [ours].\n")}, {"fields"}),
        "text outside a field": ({"area": edit(AREA1, "- **Test.** Logic: it ran [ours].\n", "- **Test.** Logic: it ran [ours].\nStray text.\n")},
                                 {"fields"}),
        "an empty test": ({"area": edit(AREA1, "- **Test.** Logic: it ran [ours].", "- **Test.** [ours]")}, {"no-test"}),
        "a placeholder test": ({"area": edit(AREA1, "- **Test.** Logic: it ran [ours].", "- **Test.** TBD [ours].")}, {"placeholder"}),
        "a placeholder requirement": ({"area": edit(AREA1, "- **Requirement.** It runs [§3].", "- **Requirement.** TODO.")},
                                      {"placeholder"}),
        "no trace and no reason": ({"area": AREA1 + OURS_REQ.format(traces="none", why="")}, {"no-source"}),
        "a departure it does not trace": ({"area": edit(AREA1, "- **Traces.** P-AAA-2, P-CCC-1 [§3.1].\n",
                                                        "- **Traces.** P-AAA-2, P-CCC-1 [§3.1].\n- **Departs from.** P-AAA-1: x [ours].\n")},
                                          {"departs"}),
        "a departure the column misses": ({"trace": edit(TRACE, f"| R-RUN-1{DEPARTS} |", "| R-RUN-1 |")}, {"column"}),
        "a split pair": ({"area": edit(AREA1, "P-AAA-2, P-CCC-1 [§3.1]", "P-AAA-2 [§3.1]")
                          + OURS_REQ.format(traces="P-CCC-1 [§3]", why="- **Why ours.** r [ours].\n"),
                          "trace": edit(TRACE, "| P-CCC-1 | a value | R-STG-1 |", "| P-CCC-1 | a value | R-OPS-1 |")},
                         {"split-pair"}),
        "a stage missing from the table": ({"area": edit(AREA1, "| TAIL |" + " v |" * 8 + "\n", "")}, {"stage-table"}),
        "an empty stage cell": ({"area": edit(AREA1, "| SEED | v |", "| SEED |  |")}, {"stage-table"}),
        "no stage table": ({"area": edit(AREA1, "## The default stage configuration", "## Stages")}, {"structure"}),
        "a file with no requirement": ({"extra": "# Another scheme\n| RJ-1 | something | a test |\n"}, {"structure"}),
        "a leave-out with no reason": ({"main": edit(MAIN, "- **Why.** Nothing to reproduce, as U-CCC-1 decides [ours].",
                                                     "- **Why.** [ours] (U-CCC-1)")},
                                       {"no-reason"}),
        "deciding another task's row": ({"area": edit(AREA1, "- **Decides.** U-AAA-2 [ours].", "- **Decides.** U-AAA-2, U-BBB-1 [ours].")},
                                        {"boundary"}),
        "depending on a task-2 row": ({"area": edit(edit(AREA1, "- **Depends on.** U-BBB-1, task 3;", "- **Depends on.** U-BBB-1, task 3; U-AAA-1;"),
                                                    "as U-BBB-1 decides", "as U-BBB-1 and U-AAA-1 decide")},
                                      {"boundary", "pending-table"}),
        "a row the register lacks": ({"area": edit(edit(AREA1, "- **Depends on.** U-BBB-1, task 3;", "- **Depends on.** U-BBB-1, task 3; U-ZZZ-9;"),
                                                   "as U-BBB-1 decides", "as U-BBB-1 and U-ZZZ-9 decide")},
                                     {"unknown-row"}),
        "a dependency the text does not name": ({"area": edit(AREA1, "It stages as U-BBB-1 decides,", "It stages,")},
                                                {"inline-dependency"}),
        "a leave-out's dependency it does not name": ({"main": edit(MAIN, "Nothing to reproduce, as U-CCC-1 decides [ours].",
                                                                   "Nothing to reproduce [ours].")}, {"inline-dependency"}),
        "a row given to a two-digit task": ({"area": edit(AREA1, "U-BBB-1, task 3;", "U-BBB-1, task 10;")}, {"task-attribution"}),
        "a decision row short of a middle cell": ({"main": edit(MAIN, "| U-AAA-1 | blocks 1 | confirmed | d | r | R-STG-1 |",
                                                                "| U-AAA-1 | blocks 1 | confirmed | d | R-STG-1 |")}, {"decision-table"}),
        "a row given to the wrong task": ({"area": edit(AREA1, "U-BBB-1, task 3;", "U-BBB-1, task 5;")}, {"task-attribution"}),
        "a malformed row ID under Depends on": ({"area": edit(edit(AREA1, "U-BBB-1, task 3;", "U–BBB–1, task 3;"),
                                                              "as U-BBB-1 decides", "as U–BBB–1 decides")},
                                                {"malformed-id", "pending-table"}),
        "a test with no tier": ({"area": edit(AREA1, "- **Test.** Logic: it ran [ours].", "- **Test.** It ran [ours].")},
                                {"test-tier"}),
        "an IR- rule with no task-6 row": ({"area": edit(AREA1, "It runs [§3].", "It runs, as task 6's IR-3 sets it [§3].")},
                                           {"integrity-dependency"}),
        "an IR- rule beside its task-6 row": ({"area": edit(AREA1, "scored by the harness (U-INT-4)",
                                                            "scored by the harness (IR-5; U-INT-4)")}, set()),
        "a trace inside an HTML comment": ({"area": edit(AREA1, "P-AAA-2, P-CCC-1 [§3.1]", "P-AAA-2 <!-- , P-CCC-1 --> [§3.1]")},
                                           {"unmapped", "column"}),
        "the harness without task 6's rows": ({"area": edit(edit(AREA1, "- **Depends on.** U-BBB-1, task 3; U-INT-4, task 6 [ours].",
                                                                  "- **Depends on.** U-BBB-1, task 3 [ours]."), " (U-INT-4)", ""),
                                               "main": edit(MAIN, "| 6 · integrity | U-INT-4 |\n", "")},
                                              {"integrity-dependency"}),
        "a task-6 row named by its alias": ({"area": edit(edit(AREA1, "- **Depends on.** U-BBB-1, task 3; U-INT-4, task 6 [ours].",
                                                                "- **Depends on.** U-BBB-1, task 3; U-ART-16, task 6 [ours]."), "(U-INT-4)", "(U-ART-16)")},
                                            set()),
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
        "a pointer naming the wrong requirement": ({"register": edit(REGISTER, "confirmed, in R-STG-1", "confirmed, in R-RUN-1")},
                                                   {"pointer"}),
        "a pending table that drifts": ({"main": edit(MAIN, "| 3 · components | U-BBB-1 |", "| 3 · components | U-BBB-1, U-AAA-1 |")},
                                        {"pending-table"}),
        "no decisions section": ({"main": edit(MAIN, "## Decisions on the register's task-2 rows", "## Decisions")},
                                 {"structure"}),
    }

    def run(texts: dict, write: bool = False):
        with tempfile.TemporaryDirectory() as tmp:
            paper, req_dir = Path(tmp) / "paper", Path(tmp) / "requirements"
            paper.mkdir()
            req_dir.mkdir()
            (paper / "analysis.md").write_text(texts["source"], encoding="utf-8")
            (paper / "traceability.md").write_text(texts["trace"], encoding="utf-8")
            (paper / "unspecified.md").write_text(texts["register"], encoding="utf-8")
            (Path(tmp) / "requirements.md").write_text(texts["main"], encoding="utf-8")
            (req_dir / "01-area.md").write_text(texts["area"], encoding="utf-8")
            if "extra" in texts:
                (req_dir / "09-other.md").write_text(texts["extra"], encoding="utf-8")
            kinds = {kind for kind, _ in check(paper, Path(tmp) / "requirements.md", req_dir, write)[0]}
            return kinds, (paper / "traceability.md").read_text(encoding="utf-8")

    clean = {"source": SOURCE, "trace": TRACE, "register": REGISTER, "main": MAIN, "area": AREA1}
    failed = 0
    for name, (changes, want) in cases.items():
        got, _ = run(clean | changes)
        ok = got == want
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: got {sorted(got) or 'no problem'}, expected {sorted(want) or 'no problem'}")
    blank = clean | {"trace": TRACE.replace(f"| R-RUN-1{DEPARTS} |", f"| {PLACEHOLDER} |")
                     .replace("| R-RUN-1, R-STG-1 |", f"| {PLACEHOLDER} |")}
    before, _ = run(blank)
    after, filled = run(blank, write=True)
    ok = before == {"column"} and after == set() and filled == TRACE
    failed += not ok
    print(f"{'ok  ' if ok else 'FAIL'} --write fills the column: before {sorted(before)}, after {sorted(after) or 'no problem'}, "
          f"identical to the clean file: {filled == TRACE}")
    return 1 if failed else 0
