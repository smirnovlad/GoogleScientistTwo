"""Check that every statement in docs/paper/ cites the paper, and that the citations are real.

This is the control behind TODO task 1's "every statement there cites its location in the paper"
(conventions: docs/paper/README.md). Three checks:

1. COVERAGE. Every content unit (a paragraph, a list item, a table body row, a blockquote, a
   line of a code block) carries a paper location tag such as [§3.2], [Tab. 1], [Lst. 1],
   [Fig. 9b], [Eq. 2], [App. A.2], [p. 41], [fn. 1], [Abstract] or [Bib: key], or the marker
   [ours] for our own statement. Exempt: headings, table header rows, rules, blank lines,
   units of fewer than four words once IDs and links are removed, and code lines that are pure
   control flow (else:, return None, ...).
2. ANCHORS. Every TeX anchor `tex:<path>:<line>[-<line>]` names a file under docs/paper/source/
   and a line range inside it.
3. QUOTES. Every double-quoted passage of five words or more appears verbatim (letters and
   digits only, case-folded) in the TeX, in the PDF text, or in the initial note. Separate a
   quote's parts with "..." or "[...]" and each part is checked on its own.

Usage:
  python3 playground/paper/check_citations.py            # checks the deliverables, exit 1 on any failure
  python3 playground/paper/check_citations.py FILE...    # checks the given files
  python3 playground/paper/check_citations.py --selftest # proves each check can fail
Needs .cache/paper/2609.19644v1/paper.pdf.txt (playground/paper/fetch_sources.sh) for check 3.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
PAPER = ROOT / "docs/paper"
SOURCE = PAPER / "source"
PDF_TEXT = ROOT / ".cache/paper/2609.19644v1/paper.pdf.txt"
NOTE = ROOT / "docs/inputs/2026-09-27-initial-replication-note.md"

TAG = re.compile(r"\[(§|Tab\.|Lst\.|Fig\.|Eq\.|App\.|pp?\.|fn\.|Abstract|Title|Bib:)")
OURS = re.compile(r"\[ours\]", re.I)
ANCHOR = re.compile(r"tex:([\w./-]+\.(?:tex|bib)):(\d+)(?:-(\d+))?")
# Match every quoted string, however short, so that quotes pair up left to right; a minimum
# length here would let a short quote's closing mark open a false "quote" of the prose after it.
QUOTE = re.compile(r"\"([^\"\n]*)\"|“([^”\n]*)”")
ID_OR_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)|\b[PUACN]-[A-Z0-9]+(?:-\d+)*\b|`[^`]*`")
CONTROL_FLOW = re.compile(r"^\s*(else:|try:|pass|break|continue|return( None)?|end|[)}\]]+|#.*)?\s*$")


def alnum(text: str) -> str:
    """Letters and digits only, case-folded: survives line breaks, hyphenation and markup."""
    return re.sub(r"[^0-9a-z]", "", text.lower())


def tex_to_plain(tex: str) -> str:
    tex = re.sub(r"(?<!\\)%.*", "", tex)                  # comments
    tex = re.sub(r"\\sname\b\s*~?", "ScientistTwo ", tex)
    tex = re.sub(r"\\(?:cite[pt]?|citealp|ref|label|eqref)\{[^}]*\}", " ", tex)
    tex = re.sub(r"\\[a-zA-Z]+\*?", " ", tex)             # other commands; keep their arguments
    return tex


def corpus() -> str:
    parts = [tex_to_plain(p.read_text(encoding="utf-8")) for p in sorted(SOURCE.rglob("*.tex"))]
    if PDF_TEXT.exists():
        parts.append(re.sub(r"-\n\s*", "", PDF_TEXT.read_text(encoding="utf-8")))
    if NOTE.exists():
        parts.append(NOTE.read_text(encoding="utf-8"))
    return "\n".join(alnum(p) for p in parts)


def units(lines: list[str]):
    """Yield (line_number, text) for every content unit that must carry a citation."""
    in_code, para, para_start = False, [], 0

    def flush():
        if para:
            yield para_start, " ".join(para)
        para.clear()

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
        if stripped.startswith("|") or re.match(r"^([-*+]|\d+\.)\s", stripped):
            yield from flush()
            yield i, stripped
            continue
        if not para:
            para_start = i
        para.append(stripped)
    yield from flush()


def check_file(path: Path, text_corpus: str) -> list[str]:
    problems = []
    lines = path.read_text(encoding="utf-8").split("\n")
    for n, unit in units(lines):
        bare = ID_OR_LINK.sub(" ", unit)
        if len(re.findall(r"[A-Za-z]{2,}", bare)) < 4:
            continue
        if not (TAG.search(unit) or OURS.search(unit)):
            problems.append(f"{path.name}:{n}: no citation: {unit[:90]}")
    for n, line in enumerate(lines, 1):
        for m in ANCHOR.finditer(line):
            target = SOURCE / m.group(1)
            first, last = int(m.group(2)), int(m.group(3) or m.group(2))
            if not target.exists():
                problems.append(f"{path.name}:{n}: anchor to a missing file: {m.group(0)}")
                continue
            length = len(target.read_text(encoding="utf-8").split("\n"))
            if not 1 <= first <= last <= length:
                problems.append(f"{path.name}:{n}: anchor outside 1..{length}: {m.group(0)}")
        for m in QUOTE.finditer(line):
            quote = m.group(1) or m.group(2)
            for part in re.split(r"\.\.\.|…|\[\.\.\.\]", quote):
                if len(part.split()) >= 5 and alnum(part) not in text_corpus:
                    problems.append(f"{path.name}:{n}: quote not in the paper or the note: \"{part.strip()[:80]}\"")
    return problems


def default_files() -> list[Path]:
    names = ["analysis.md", "traceability.md", "unspecified.md", "claims.md", "note-check.md",
             "artifacts.md"]
    files = [PAPER / n for n in names if (PAPER / n).exists()]
    # Documents split into a folder keep their parts there (README: "Keep a file under about 600 lines").
    return files + sorted((PAPER / "stages").glob("*.md")) + sorted((PAPER / "claims").glob("*.md"))


def selftest() -> int:
    """Each check must fail on a planted defect and pass on its corrected twin."""
    text_corpus = corpus()
    cases = {
        "uncited paragraph": ("The subset critic compares the idea with the baseline results.\n", 1),
        "cited paragraph": ("The subset critic compares the idea with the baseline [§3.2].\n", 0),
        "ours paragraph": ("We will define the subset ourselves for every task [ours].\n", 0),
        "bad anchor": ("A stage has a critic [Lst. 1] (tex:tables/pseudo_code.tex:999).\n", 1),
        "good anchor": ("A stage has a critic [Lst. 1] (tex:tables/pseudo_code.tex:26-35).\n", 0),
        "fake quote": ('It says "the critic always accepts every single idea" [§3.2].\n', 1),
        "real quote": ('It says "If performance is substantially inferior to the baseline" [§3.2].\n', 0),
        "short quotes pair correctly": ('Verdicts "Good" and "Bad" are two of the three it may return [§3.2].\n', 0),
    }
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, (body, want) in cases.items():
            doc = Path(tmp) / "case.md"
            doc.write_text(body, encoding="utf-8")
            got = len(check_file(doc, text_corpus))
            ok = (got > 0) == bool(want)
            failed += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {name}: {got} problem(s), expected {'some' if want else 'none'}")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--selftest"]:
        return selftest()
    files = [Path(a) for a in argv[1:]] or default_files()
    if not PDF_TEXT.exists():
        print("note: no PDF text; quotes are checked against the TeX and the note only", file=sys.stderr)
    text_corpus = corpus()
    problems = [p for f in files for p in check_file(f, text_corpus)]
    for p in problems:
        print(p)
    print(f"{len(files)} file(s) checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
