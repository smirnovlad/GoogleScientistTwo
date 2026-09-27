"""Check that every statement in docs/paper/ cites the paper, and that the citations are real.

This is the control behind TODO task 1's "every statement there cites its location in the paper"
(conventions: docs/paper/README.md). Four checks:

1. COVERAGE. Every content unit (a paragraph, a list item with its wrapped lines, a table body
   row, a blockquote, a line of a code block) carries a paper location tag such as [§3.2],
   [Tab. 1], [Lst. 1], [Fig. 9b], [Eq. 2], [App. A.2], [p. 41], [fn. 1], [Abstract] or
   [Bib: key], or the marker [ours] for our own statement. A tag shown as code (`[§3.2]`) is an
   example, not a citation. Exempt: headings, table header rows, rules, blank lines, units of
   fewer than four words once IDs and links are removed, and code lines that are pure control
   flow (else:, return None, ...).
2. LOCATIONS. Every tag names a location the paper has: a section or appendix of the TeX, a
   table, figure or listing the PDF captions, an equation or footnote of the TeX, a page of the
   PDF, or a key of main.bib. [§999.999], [Tab. 99] or an unclosed "[§" fail.
3. ANCHORS. Every TeX anchor `tex:<path>:<line>[-<line>]` names a file under docs/paper/source/
   and a line range inside it.
4. QUOTES. Every double-quoted passage of five words or more, within one content unit or
   heading and so across line breaks, appears verbatim (letters and digits only, case-folded)
   in the paper's TeX or PDF text. Two other sources count only where they are named:
   - a source the paper delegates to by reference (.cache/refs/<arXiv id>/src/, fetched by
     fetch_sources.sh), on a unit that cites it with [Ref: …] or a `ref:<arXiv id>:<path>:<line>`
     anchor; a missing cache fails the anchor, since a check that cannot run has not passed;
   - the initial note, in note-check.md only, on a unit that names a note claim (N-12) or the
     note, or in a heading, since that file's headings quote the note's sections. Anywhere else
     the note's wording would pass as the paper's.
   Separate a quote's parts with "..." or "[...]" and each part is checked on its own.

Usage:
  python3 playground/paper/check_citations.py            # checks the deliverables, exit 1 on any failure
  python3 playground/paper/check_citations.py FILE...    # checks the given files
  python3 playground/paper/check_citations.py --selftest # proves each check can fail
Needs .cache/ (playground/paper/fetch_sources.sh): the PDF text for checks 2 and 4, the refs for 4.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from float_numbering import pdf_floats  # noqa: E402  (the one reader of the PDF's float captions)

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
PAPER = ROOT / "docs/paper"
SOURCE = PAPER / "source"
PDF_TEXT = ROOT / ".cache/paper/2609.19644v1/paper.pdf.txt"
NOTE = ROOT / "docs/inputs/2026-09-27-initial-replication-note.md"
REFS = ROOT / ".cache/refs"

HEADS = r"§|Tab\.|Lst\.|Fig\.|Eq\.|App\.|pp?\.|fn\.|Abstract|Title|Bib:|Ref:"
TAG = re.compile(rf"\[({HEADS})")
TAG_FULL = re.compile(rf"\[({HEADS})([^\]\n]*)(\])?")
LOCATION = {"§": r"(\d+(?:\.\d+)?)", "Tab.": r"(\d+)", "Fig.": r"(\d+)[a-z]?", "Lst.": r"(\d+)",
            "Eq.": r"(\d+)", "App.": r"([A-Z](?:\.\d+)?)", "fn.": r"(\d+)", "p.": r"(\d+)"}
OURS = re.compile(r"\[ours\]", re.I)
ANCHOR = re.compile(r"tex:([\w./-]+\.(?:tex|bib)):(\d+)(?:-(\d+))?")
REF_ANCHOR = re.compile(r"ref:(\d{4}\.\d{4,5}v\d+):([\w./-]+\.(?:tex|bib)):(\d+)(?:-(\d+))?")
# Match every quoted string, however short, so that quotes pair up left to right; a minimum
# length here would let a short quote's closing mark open a false "quote" of the prose after it.
QUOTE = re.compile(r"\"([^\"\n]*)\"|“([^”\n]*)”")
CODE_SPAN = re.compile(r"`[^`]*`")
ID_OR_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)|\b[PUACN]-[A-Z0-9]+(?:-\d+)*\b|`[^`]*`")
NOTE_CLAIM = re.compile(r"\bN-\d+\b")
CONTROL_FLOW = re.compile(r"^\s*(else:|try:|pass|break|continue|return( None)?|end|[)}\]]+|#.*)?\s*$")


def alnum(text: str) -> str:
    """Letters and digits only, case-folded: survives line breaks, hyphenation and markup."""
    return re.sub(r"[^0-9a-z]", "", text.lower())


def strip_comments(tex: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", tex)


def tex_to_plain(tex: str) -> str:
    tex = strip_comments(tex)
    tex = re.sub(r"\\sname\b\s*~?", "ScientistTwo ", tex)
    tex = re.sub(r"\\(?:cite[pt]?|citealp|ref|label|eqref)\{[^}]*\}", " ", tex)
    tex = re.sub(r"\\[a-zA-Z]+\*?", " ", tex)             # other commands; keep their arguments
    return tex


def expand(name: str) -> str:
    """A TeX file with its \\input files spliced in, recursively, comments removed: the document
    in the order LaTeX numbers it."""
    path = SOURCE / (name if name.endswith((".tex", ".bib")) else name + ".tex")
    body = strip_comments(path.read_text(encoding="utf-8"))
    return re.sub(r"\\input\{([^}]*)\}", lambda m: expand(m.group(1)), body)


def inventory() -> dict[str, set[str]]:
    """Every location a tag may name. Sections, appendices, equations and footnotes are counted in
    the TeX as LaTeX numbers them; floats come from the PDF's own captions (float_numbering.py) and
    pages from the PDF text; keys from main.bib. Without the PDF text those kinds stay empty, and
    every tag of those kinds fails: a location that cannot be verified is not verified."""
    inv = {k: set() for k in ("§", "App.", "Eq.", "fn.", "Tab.", "Fig.", "Lst.", "p.", "Bib:")}
    doc = expand("main.tex")
    body, _, appendix = doc.partition("\\appendix")
    for part, key in ((body, "§"), (appendix, "App.")):
        sec = sub = 0
        for m in re.finditer(r"\\(sub)?section\{", part):
            if m.group(1):
                sub += 1
                inv[key].add(f"{chr(64 + sec) if key == 'App.' else sec}.{sub}")
            else:
                sec, sub = sec + 1, 0
                inv[key].add(chr(64 + sec) if key == "App." else str(sec))
    inv["Eq."] = {str(i) for i in range(1, len(re.findall(r"\\begin\{equation\}", doc)) + 1)}
    inv["fn."] = {str(i) for i in range(1, len(re.findall(r"\\footnote\{", doc)) + 1)}
    bib = (SOURCE / "main.bib").read_text(encoding="utf-8")
    inv["Bib:"] = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib))   # the key may sit on the next line
    if PDF_TEXT.exists():
        pages = PDF_TEXT.read_text(encoding="utf-8").split("\f")
        count = len(pages) - (1 if not pages[-1].strip() else 0)
        inv["p."] = {str(i) for i in range(1, count + 1)}
        for label, _ in pdf_floats():
            kind, number = label.split()
            inv[{"Table": "Tab.", "Figure": "Fig.", "Listing": "Lst."}[kind]].add(number)
    return inv


def sources() -> dict:
    """The corpora a quote may be found in, and the inventory of locations."""
    parts = [tex_to_plain(p.read_text(encoding="utf-8")) for p in sorted(SOURCE.rglob("*.tex"))]
    if PDF_TEXT.exists():
        parts.append(re.sub(r"-\n\s*", "", PDF_TEXT.read_text(encoding="utf-8")))
    refs = [tex_to_plain(t.read_text(encoding="utf-8", errors="replace"))
            for t in sorted(REFS.glob("*/src/**/*.tex"))]
    note = NOTE.read_text(encoding="utf-8") if NOTE.exists() else ""
    return {"paper": "\n".join(alnum(p) for p in parts), "refs": "\n".join(alnum(r) for r in refs),
            "note": alnum(note), "inv": inventory()}


def units(lines: list[str]):
    """Yield (line_number, text) for every content unit that must carry a citation. A paragraph
    or a list item runs until a blank line, a heading, a table row or the next list item, so a
    wrapped line belongs to the unit it continues."""
    in_code, block, start = False, [], 0

    def flush():
        if block:
            yield start, " ".join(block)
        block.clear()

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip()
        if line.lstrip().startswith("```"):
            yield from flush()
            in_code = not in_code
            continue
        if in_code:
            if not CONTROL_FLOW.match(line):
                yield i, line
            continue
        stripped = line.strip()
        is_header_row = (stripped.startswith("|") and i < len(lines)
                         and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i]))
        if (not stripped or stripped.startswith("#") or re.match(r"^[-*_]{3,}$", stripped)
                or re.match(r"^\|?[\s:|-]+\|[\s:|-]*$", stripped) or is_header_row):
            yield from flush()
            continue
        if stripped.startswith("|"):
            yield from flush()
            yield i, stripped
            continue
        if re.match(r"^([-*+]|\d+\.)\s", stripped):
            yield from flush()
            start = i
        elif not block:
            start = i
        block.append(stripped)
    yield from flush()


def tag_ok(head: str, body: str, inv: dict[str, set[str]]) -> bool:
    if head in ("Abstract", "Title"):
        return body == ""
    if head in ("Bib:", "Ref:"):
        key = re.match(r"[\w-]+", body)
        return bool(key) and key.group(0) in inv["Bib:"]
    if head == "pp.":
        for item in body.split(","):
            r = re.fullmatch(r"\s*(\d+)(?:\s*[–-]\s*(\d+))?\s*", item)
            if not r:
                return False
            first, last = int(r.group(1)), int(r.group(2) or r.group(1))
            if first > last or not {str(first), str(last)} <= inv["p."]:
                return False
        return True
    m = re.match(LOCATION[head] + r"(?![\d.])", body)
    if not m or m.group(1) not in inv[head]:
        return False
    equation = re.match(r",\s*Eq\.\s*(\d+)", body[m.end():])   # [§3.3, Eq. 4]
    return not equation or equation.group(1) in inv["Eq."]


def tag_problems(where: str, text: str, inv: dict[str, set[str]]) -> list[str]:
    out = []
    for m in TAG_FULL.finditer(CODE_SPAN.sub(" ", text)):
        if not m.group(3):
            out.append(f"{where}: unclosed tag: {m.group(0)[:40]}")
        elif not tag_ok(m.group(1), m.group(2).strip(), inv):
            out.append(f"{where}: no such location in the paper: {m.group(0)}")
    return out


def quote_problems(where: str, text: str, src: dict, note_ok: bool) -> list[str]:
    cites_ref = "[Ref:" in text or REF_ANCHOR.search(text) is not None
    out = []
    for m in QUOTE.finditer(text):
        for part in re.split(r"\.\.\.|…|\[\.\.\.\]", m.group(1) or m.group(2)):
            if len(part.split()) < 5:
                continue
            a = alnum(part)
            if a in src["paper"] or (cites_ref and a in src["refs"]) or (note_ok and a in src["note"]):
                continue
            named = ["the paper"] + (["the cited reference"] if cites_ref else []) + (["the note"] if note_ok else [])
            out.append(f"{where}: quote not in {' or '.join(named)}: \"{part.strip()[:80]}\"")
    return out


def check_file(path: Path, src: dict) -> list[str]:
    problems = []
    lines = path.read_text(encoding="utf-8").split("\n")
    note_file = path.name == "note-check.md"
    for n, unit in units(lines):
        where = f"{path.name}:{n}"
        bare = ID_OR_LINK.sub(" ", unit)
        visible = CODE_SPAN.sub(" ", unit)
        if len(re.findall(r"[A-Za-z]{2,}", bare)) >= 4 and not (TAG.search(visible) or OURS.search(visible)):
            problems.append(f"{where}: no citation: {unit[:90]}")
        problems += tag_problems(where, unit, src["inv"])
        note_ok = note_file and (NOTE_CLAIM.search(unit) is not None or "note" in unit.lower())
        problems += quote_problems(where, unit, src, note_ok)
    for n, line in enumerate(lines, 1):
        where = f"{path.name}:{n}"
        if line.lstrip().startswith("#"):
            problems += tag_problems(where, line, src["inv"])
            problems += quote_problems(where, line, src, note_ok=note_file)
        for m in ANCHOR.finditer(line):
            target = SOURCE / m.group(1)
            first, last = int(m.group(2)), int(m.group(3) or m.group(2))
            if not target.exists():
                problems.append(f"{where}: anchor to a missing file: {m.group(0)}")
                continue
            length = len(target.read_text(encoding="utf-8").split("\n"))
            if not 1 <= first <= last <= length:
                problems.append(f"{where}: anchor outside 1..{length}: {m.group(0)}")
        for m in REF_ANCHOR.finditer(line):
            target = REFS / m.group(1) / "src" / m.group(2)
            first, last = int(m.group(3)), int(m.group(4) or m.group(3))
            if not target.exists():
                problems.append(f"{where}: cannot verify {m.group(0)}: no such file in "
                                f".cache/refs (run playground/paper/fetch_sources.sh)")
                continue
            length = len(target.read_text(encoding="utf-8", errors="replace").split("\n"))
            if not 1 <= first <= last <= length:
                problems.append(f"{where}: anchor outside 1..{length}: {m.group(0)}")
    return problems


def default_files() -> list[Path]:
    names = ["analysis.md", "traceability.md", "unspecified.md", "claims.md", "note-check.md",
             "artifacts.md"]
    files = [PAPER / n for n in names if (PAPER / n).exists()]
    # Documents split into a folder keep their parts there (README: "Keep a file under about 600 lines").
    return files + sorted((PAPER / "stages").glob("*.md")) + sorted((PAPER / "claims").glob("*.md"))


def selftest() -> int:
    """Each check must fail on a planted defect and pass on its corrected twin."""
    src = sources()
    note_quote = "Self-contained scripts plus an LLM validation filter"   # the note's words, not the paper's
    cases = {   # name: (document, problems expected?, file name)
        "reference quote without [Ref:]": ('The paper says "We run each evaluator five times" [§4.2].\n', 1, "case.md"),
        "uncited paragraph": ("The subset critic compares the idea with the baseline results.\n", 1, "case.md"),
        "cited paragraph": ("The subset critic compares the idea with the baseline [§3.2].\n", 0, "case.md"),
        "ours paragraph": ("We will define the subset ourselves for every task [ours].\n", 0, "case.md"),
        "a tag shown as code is no citation": ("We write tags such as `[§3.2]` into every line of text.\n", 1, "case.md"),
        "wrapped list item cites once": ("- The subset critic compares the idea\n  with the baseline [§3.2].\n", 0, "case.md"),
        "no such section": ("The critic decides the whole matter [§999.999].\n", 1, "case.md"),
        "no such table": ("The table shows the whole matter [Tab. 99].\n", 1, "case.md"),
        "no such page": ("The draft shows the whole matter [p. 999].\n", 1, "case.md"),
        "page range backwards": ("The draft shows the whole matter [pp. 50–41].\n", 1, "case.md"),
        "no such equation": ("The coder is defined by its equation [§3.2, Eq. 9].\n", 1, "case.md"),
        "no such bib key": ("The reviewer follows that design [Bib: nosuchpaper2026].\n", 1, "case.md"),
        "unclosed tag": ("The critic decides the whole matter [§\n", 1, "case.md"),
        "real locations": ("Seen in [§3.3, Eq. 4] [Tab. 16] [Fig. 10b] [App. A.2] [pp. 41–42] [fn. 2] [Lst. 1].\n", 0, "case.md"),
        "bad anchor": ("A stage has a critic [Lst. 1] (tex:tables/pseudo_code.tex:999).\n", 1, "case.md"),
        "good anchor": ("A stage has a critic [Lst. 1] (tex:tables/pseudo_code.tex:26-35).\n", 0, "case.md"),
        "fake quote": ('It says "the critic always accepts every single idea" [§3.2].\n', 1, "case.md"),
        "fake quote across lines": ('It says "the critic always accepts\nevery single idea" [§3.2].\n', 1, "case.md"),
        "real quote": ('It says "If performance is substantially inferior to the baseline" [§3.2].\n', 0, "case.md"),
        "real quote across lines": ('It says "If performance is substantially\ninferior to the baseline" [§3.2].\n', 0, "case.md"),
        "short quotes pair correctly": ('Verdicts "Good" and "Bad" are two of the three it may return [§3.2].\n', 0, "case.md"),
        "note quote passed off as the paper's": (f'The paper requires "{note_quote}" [§4.2].\n', 1, "case.md"),
        "note quote outside note-check.md": (f'| N-99 | "{note_quote}" | TRUE [ours] |\n', 1, "case.md"),
        "note quote in a note-check row": (f'| N-99 | "{note_quote}" | TRUE [ours] |\n', 0, "note-check.md"),
        "reference quote and anchor": ('ScientistOne says "We run each evaluator five times" [Ref: meng2026scientistone §6] '
                                       '(ref:2605.26340v1:sections/06a_setup.tex:10).\n', 0, "case.md"),
        "bad reference anchor": ('ScientistOne defines the audit [Ref: meng2026scientistone §5] '
                                 '(ref:2605.26340v1:sections/nope.tex:3).\n', 1, "case.md"),
    }
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, (body, want, filename) in cases.items():
            doc = Path(tmp) / filename
            doc.write_text(body, encoding="utf-8")
            got = len(check_file(doc, src))
            doc.unlink()
            ok = (got > 0) == bool(want)
            failed += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {name}: {got} problem(s), expected {'some' if want else 'none'}")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--selftest"]:
        return selftest()
    files = [Path(a) for a in argv[1:]] or default_files()
    if not PDF_TEXT.exists():
        print("note: no PDF text, so float and page tags cannot be verified and fail; run "
              "playground/paper/fetch_sources.sh", file=sys.stderr)
    src = sources()
    problems = [p for f in files for p in check_file(f, src)]
    if not REFS.exists():
        print("note: no .cache/refs; quotes of delegated sources cannot be checked", file=sys.stderr)
    for p in problems:
        print(p)
    print(f"{len(files)} file(s) checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
