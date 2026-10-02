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
   PDF, or a key of main.bib. Every location in a tag counts: the ends of a range ([Tab. 1–3])
   and a second location ([§3.3, Eq. 4]) too. [§999.999], [Tab. 1–99], [§3.2, Fig. 99] or an
   unclosed "[§" fail. A [Ref: key §5] tag must name a cached delegated source, and a section
   or appendix that source has.
3. ANCHORS. Every TeX anchor `tex:<path>:<line>[-<line>]` names a file under docs/paper/source/
   and a line range inside it; a path that climbs out of that folder fails, and so does a
   `ref:` anchor that climbs out of its source.
4. QUOTES. Every double-quoted passage of five words or more, within one content unit or
   heading and so across line breaks, appears verbatim (letters and digits only, case-folded)
   in the paper's TeX or PDF text. Two other sources count only where they are named:
   - a source the paper delegates to by reference (.cache/refs/<arXiv id>/src/, fetched by
     fetch_sources.sh), on a unit that cites that very source: by a valid [Ref: key …] tag,
     not one shown as code, whose main.bib entry gives the source's arXiv id, or by its
     `ref:<arXiv id>:<path>:<line>` anchor. A missing cache fails the anchor, since a check
     that cannot run has not passed;
   - the initial note, in note-check.md only: in the claim cell of an N- row, or in a heading,
     since that file's headings quote the note's sections. Anywhere else, the evidence cells
     of the same rows included, the note's wording would pass as the paper's.
   Separate a quote's parts with "..." or "[...]" and each part is checked on its own.

Usage:
  python3 playground/paper/check_citations.py            # checks docs/paper/ and docs/requirements*, exit 1 on any failure
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
from float_numbering import norm, pdf_floats  # noqa: E402  (the one reader of the PDF's float captions)

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
PAPER = ROOT / "docs/paper"
SOURCE = PAPER / "source"
PDF_TEXT = ROOT / ".cache/paper/2609.19644v1/paper.pdf.txt"
NOTE = ROOT / "docs/inputs/2026-09-27-initial-replication-note.md"
REFS = ROOT / ".cache/refs"

HEADS = r"§|Tab\.|Lst\.|Fig\.|Eq\.|App\.|pp?\.|fn\.|Abstract|Title|Bib:|Ref:"
TAG = re.compile(rf"\[({HEADS})")
TAG_FULL = re.compile(rf"\[({HEADS})([^\]\n]*)(\])?")
LOCATION = {"§": r"\d+(?:\.\d+)?", "Tab.": r"\d+", "Fig.": r"\d+[a-z]?", "Lst.": r"\d+",
            "Eq.": r"\d+", "App.": r"[A-Z](?:\.\d+)?", "fn.": r"\d+", "p.": r"\d+"}
LOCATION_TOKEN = re.compile(r"(§|Tab\.|Fig\.|Lst\.|Eq\.|App\.|pp?\.|fn\.)\s*([^\s,;\]]+(?:\s*[–-]\s*[^\s,;\]]+)?)")
QUOTED = re.compile(r"\"[^\"]*\"|“[^”]*”")
NOTE_ROW = re.compile(r"^\|\s*N-\d+\s*\|((?:\\\||[^|])*)\|")   # the claim cell of a note-check row
# What a tag may leave unparsed after its locations: prose, never a bare number or a location keyword.
UNPARSED_LOCATION = re.compile(r"(?<![\w.])\d+(?!\w)|§|\b(?:Tab|Fig|Lst|Eq|App|pp?|fn)\.")
# Panels printed only in a figure's image, which the TeX never names (read from the rendered page):
# Fig. 1, "(a) Expanded Frontier by ScientistTwo" and "(b) Relative Gain compared to Human SOTA".
IMAGE_PANELS = {"1": {"a", "b"}}
OURS = re.compile(r"\[ours\]", re.I)
ANCHOR = re.compile(r"tex:([\w./-]+\.(?:tex|bib)):(\d+)(?:-(\d+))?")
REF_ANCHOR = re.compile(r"ref:(\d{4}\.\d{4,5}v\d+):([\w./-]+\.(?:tex|bib)):(\d+)(?:-(\d+))?")
# Match every quoted string, however short, so that quotes pair up left to right; a minimum
# length here would let a short quote's closing mark open a false "quote" of the prose after it.
QUOTE = re.compile(r"\"([^\"\n]*)\"|“([^”\n]*)”")
CODE_SPAN = re.compile(r"`[^`]*`")
ID_OR_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)|\b[PUACN]-[A-Z0-9]+(?:-\d+)*\b|`[^`]*`")
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


def expand(root: Path, name: str) -> str:
    """A TeX file with its \\input files spliced in, recursively, comments removed: the document
    in the order LaTeX numbers it."""
    path = root / (name if name.endswith((".tex", ".bib")) else name + ".tex")
    body = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
    return re.sub(r"\\input\{([^}]*)\}", lambda m: expand(root, m.group(1)), body)


def structure(root: Path) -> dict[str, set[str]]:
    """The section and appendix numbers of a TeX tree (§3.2, App. A.2), counted as LaTeX numbers
    them: starred and commented-out sections do not count."""
    found = {"§": set(), "App.": set()}
    body, _, appendix = expand(root, "main.tex").partition("\\appendix")
    for part, key in ((body, "§"), (appendix, "App.")):
        sec = sub = 0
        for m in re.finditer(r"\\(sub)?section\{", part):
            if m.group(1):
                sub += 1
                found[key].add(f"{chr(64 + sec) if key == 'App.' else sec}.{sub}")
            else:
                sec, sub = sec + 1, 0
                found[key].add(chr(64 + sec) if key == "App." else str(sec))
    return found


def figure_panels(doc: str) -> dict[str, set[str]]:
    """The panel letters of each figure, by its PDF number. The TeX names a figure's panels in its
    caption or body, "(a)", "(b)"; panels printed only in the image are in IMAGE_PANELS. Figures are
    numbered in source order, as LaTeX numbers them, and each caption is matched to the PDF's caption
    of that number: if the two orders ever disagree, the panel check stops rather than guess."""
    pdf = {label.split()[1]: norm(caption) for label, caption in pdf_floats() if label.startswith("Figure")}
    panels, number = {}, 0
    for env in re.finditer(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", doc, re.S):
        caption = re.search(r"\\caption\{(.*)", env.group(1), re.S)
        if not caption:
            continue
        number += 1
        if pdf and norm(tex_to_plain(caption.group(1))) != pdf.get(str(number)):
            raise SystemExit(f"figure {number}: the TeX and the PDF number their figures differently; "
                             "the panel check cannot run")
        letters = set(re.findall(r"\(([a-h])\)", env.group(1)))
        if letters:
            panels[str(number)] = letters
    for figure, letters in IMAGE_PANELS.items():
        panels.setdefault(figure, set()).update(letters)
    return panels


def inventory() -> dict:
    """Every location a tag may name. Sections, appendices, equations and footnotes are counted in
    the TeX as LaTeX numbers them; floats come from the PDF's own captions (float_numbering.py) and
    pages from the PDF text; keys from main.bib. Without the PDF text those kinds stay empty, and
    every tag of those kinds fails: a location that cannot be verified is not verified."""
    inv = {k: set() for k in ("Eq.", "fn.", "Tab.", "Fig.", "Lst.", "p.", "Bib:")}
    inv.update(structure(SOURCE))
    doc = expand(SOURCE, "main.tex")
    inv["Eq."] = {str(i) for i in range(1, len(re.findall(r"\\begin\{equation\}", doc)) + 1)}
    inv["fn."] = {str(i) for i in range(1, len(re.findall(r"\\footnote\{", doc)) + 1)}
    bib = (SOURCE / "main.bib").read_text(encoding="utf-8")
    inv["Bib:"] = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib))   # the key may sit on the next line
    inv["panels"] = figure_panels(doc)
    if PDF_TEXT.exists():
        pages = PDF_TEXT.read_text(encoding="utf-8").split("\f")
        count = len(pages) - (1 if not pages[-1].strip() else 0)
        inv["p."] = {str(i) for i in range(1, count + 1)}
        for label, _ in pdf_floats():
            kind, number = label.split()
            inv[{"Table": "Tab.", "Figure": "Fig.", "Listing": "Lst."}[kind]].add(number)
    return inv


def references() -> dict[str, dict]:
    """The sources the paper delegates to, as fetch_sources.sh caches them: for each arXiv id with
    its version, the text a quote is looked up in and the sections a [Ref: …] tag may name."""
    refs = {}
    for tree in sorted(REFS.glob("*/src")):
        text = "\n".join(tex_to_plain(t.read_text(encoding="utf-8", errors="replace"))
                         for t in sorted(tree.rglob("*.tex")))
        has_main = (tree / "main.tex").exists()
        refs[tree.parent.name] = {"corpus": alnum(text),
                                  "structure": structure(tree) if has_main else {"§": set(), "App.": set()}}
    return refs


def arxiv_ids() -> dict[str, str]:
    """main.bib key to arXiv id (without version), for the entries that give one."""
    bib = (SOURCE / "main.bib").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", bib, re.S):
        arxiv = re.search(r"arXiv:(\d{4}\.\d{4,5})", m.group(2))
        if arxiv:
            out[m.group(1)] = arxiv.group(1)
    return out


def sources() -> dict:
    """The corpora a quote may be found in, and the inventory of locations."""
    parts = [tex_to_plain(p.read_text(encoding="utf-8")) for p in sorted(SOURCE.rglob("*.tex"))]
    if PDF_TEXT.exists():
        parts.append(re.sub(r"-\n\s*", "", PDF_TEXT.read_text(encoding="utf-8")))
    note = NOTE.read_text(encoding="utf-8") if NOTE.exists() else ""
    return {"paper": "\n".join(alnum(p) for p in parts), "note": alnum(note), "inv": inventory(),
            "refs": references(), "arxiv": arxiv_ids()}


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


def rank(label: str) -> tuple:
    """Order of two locations of one kind: 3.2 before 3.10, A.2 before B."""
    return tuple(int(x) if x.isdigit() else ord(x) for x in re.findall(r"\d+|[A-Za-z]", label))


def locations_ok(head: str, text: str, inv: dict[str, set[str]]) -> bool:
    """One location of one kind, or a range of two, or for pages a list of both, every one in the
    paper: [§3.2], [Tab. 1–3], [pp. 34, 41–42]."""
    kind = "p." if head in ("p.", "pp.") else head
    pattern = LOCATION[kind]
    for item in text.split(",") if head == "pp." else [text]:
        m = re.fullmatch(rf"\s*({pattern})(?:\s*[–-]\s*({pattern}))?\s*", item)
        if not m:
            return False
        ends = [m.group(1), m.group(2) or m.group(1)]
        for end in ends:
            number, panel = re.fullmatch(r"(\w+?(?:\.\d+)?)([a-z]?)", end).groups() if kind == "Fig." else (end, "")
            if number not in inv[kind] or (panel and panel not in inv["panels"].get(number, set())):
                return False
        if rank(ends[0]) > rank(ends[1]):
            return False
    return True


def further_locations_ok(rest: str, allowed: dict[str, set[str]]) -> bool:
    """Every location a tag names after its first ([§3.3, Eq. 4], [§3.2, Fig. 5]) must exist too.
    A name in quotes ("Common Setup") is a title, not a location."""
    rest = QUOTED.sub(" ", rest)
    for t in LOCATION_TOKEN.finditer(rest):
        kind = "p." if t.group(1) == "pp." else t.group(1)
        if kind not in allowed or not locations_ok(t.group(1), t.group(2), allowed):
            return False
    return not UNPARSED_LOCATION.search(LOCATION_TOKEN.sub(" ", rest))   # [Tab. 1, 99], [§3.2, Fig.]


def ref_ids(src: dict, key: str) -> list[str]:
    """The cached versions of the source a bib key names, if the paper delegates to it."""
    arxiv = src["arxiv"].get(key)
    return [rid for rid in src["refs"] if arxiv and rid.split("v")[0] == arxiv]


def ref_tag_ok(body: str, src: dict) -> bool:
    """[Ref: key §5] must name a source that is cached, and each section or appendix it names must
    exist in that source."""
    key = re.match(r"[\w-]+", body)
    if not key or key.group(0) not in src["inv"]["Bib:"] or not ref_ids(src, key.group(0)):
        return False
    return further_locations_ok(body[key.end():], src["refs"][ref_ids(src, key.group(0))[0]]["structure"])


def tag_ok(head: str, body: str, src: dict) -> bool:
    inv = src["inv"]
    if head in ("Abstract", "Title"):
        return body == ""
    if head == "Bib:":
        return body in inv["Bib:"]
    if head == "Ref:":
        return ref_tag_ok(body, src)
    if head == "pp.":
        return locations_ok(head, body, inv)
    kind = "p." if head == "p." else head
    first = re.match(rf"{LOCATION[kind]}(?:\s*[–-]\s*{LOCATION[kind]})?(?![\w.])", body)
    return bool(first) and locations_ok(head, first.group(0), inv) and further_locations_ok(body[first.end():], inv)


def tag_problems(where: str, text: str, src: dict) -> list[str]:
    out = []
    for m in TAG_FULL.finditer(CODE_SPAN.sub(" ", text)):
        if not m.group(3):
            out.append(f"{where}: unclosed tag: {m.group(0)[:40]}")
        elif not tag_ok(m.group(1), m.group(2).strip(), src):
            out.append(f"{where}: no such location: {m.group(0)}")
    return out


def cited_refs(text: str, src: dict) -> set[str]:
    """The delegated sources a unit cites, by a valid [Ref: …] tag outside code or by a ref:
    anchor. A quote is looked up in those sources only, never in every cached one."""
    visible = CODE_SPAN.sub(" ", text)
    ids = {m.group(1) for m in REF_ANCHOR.finditer(visible) if m.group(1) in src["refs"]}
    for m in TAG_FULL.finditer(visible):
        body = m.group(2).strip()
        if m.group(1) == "Ref:" and m.group(3) and ref_tag_ok(body, src):
            ids.update(ref_ids(src, re.match(r"[\w-]+", body).group(0)))
    return ids


def quote_problems(where: str, text: str, src: dict, note_span: tuple[int, int] | None) -> list[str]:
    """note_span is the part of the text where the note may be quoted: an N- row's claim cell, or
    a heading of note-check.md. Anywhere else, a quote of the note is not evidence."""
    refs = cited_refs(text, src)
    out = []
    for m in QUOTE.finditer(text):
        quote = m.group(1) if m.group(1) is not None else m.group(2)
        note_ok = note_span is not None and note_span[0] <= m.start() < note_span[1]
        parts = re.split(r"\.\.\.|…|\[\.\.\.\]", quote)
        if sum(len(part.split()) for part in parts) < 5:   # the whole quotation, not each fragment
            continue
        for part in parts:
            if not alnum(part):
                continue
            a = alnum(part)
            if a in src["paper"] or any(a in src["refs"][r]["corpus"] for r in refs) or (note_ok and a in src["note"]):
                continue
            named = ["the paper"] + [f"reference {r}" for r in sorted(refs)] + (["the note"] if note_ok else [])
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
        problems += tag_problems(where, unit, src)
        row = NOTE_ROW.match(unit) if note_file else None
        problems += quote_problems(where, unit, src, (row.start(1), row.end(1)) if row else None)
    for n, line in enumerate(lines, 1):
        where = f"{path.name}:{n}"
        if line.lstrip().startswith("#"):
            problems += tag_problems(where, line, src)
            problems += quote_problems(where, line, src, (0, len(line)) if note_file else None)
        for m in ANCHOR.finditer(line):
            target = (SOURCE / m.group(1)).resolve()
            first, last = int(m.group(2)), int(m.group(3) or m.group(2))
            if not target.is_relative_to(SOURCE.resolve()):
                problems.append(f"{where}: anchor outside docs/paper/source/: {m.group(0)}")
                continue
            if not target.exists():
                problems.append(f"{where}: anchor to a missing file: {m.group(0)}")
                continue
            length = len(target.read_text(encoding="utf-8").split("\n"))
            if not 1 <= first <= last <= length:
                problems.append(f"{where}: anchor outside 1..{length}: {m.group(0)}")
        for m in REF_ANCHOR.finditer(line):
            root = (REFS / m.group(1) / "src").resolve()
            target = (root / m.group(2)).resolve()
            first, last = int(m.group(3)), int(m.group(4) or m.group(3))
            if not target.is_relative_to(root):
                problems.append(f"{where}: anchor outside its reference's source: {m.group(0)}")
                continue
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
    files += sorted((PAPER / "stages").glob("*.md")) + sorted((PAPER / "claims").glob("*.md"))
    # The requirements (TODO task 2) cite the paper too, and mix its statements with our decisions,
    # which is where a reading of ours could pass as the paper's.
    # ⛔ WHY NOT a checker of their own: these rules are the paper folder's, and one copy of them stays true.
    requirements = ROOT / "docs/requirements.md"
    return files + ([requirements] if requirements.exists() else []) + sorted((ROOT / "docs/requirements").glob("*.md"))


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
        "note quote in a row's evidence cell": (f'| N-99 | "{note_quote}" | TRUE | The paper requires "{note_quote}" [§4.2] |\n', 1, "note-check.md"),
        "the paper notes, in note-check.md": (f'The paper notes "{note_quote}" [§4.2].\n', 1, "note-check.md"),
        "a range with a missing end": ("The tables show the whole matter [Tab. 1–99].\n", 1, "case.md"),
        "a real range": ("The tables show the whole matter [Tab. 1–3].\n", 0, "case.md"),
        "a second location checked": ("The figure shows the whole matter [§3.2, Fig. 99].\n", 1, "case.md"),
        "reference of a key with no cached source": ('It holds that "We run each evaluator five times" [Ref: jiang2026incremental §9].\n', 1, "case.md"),
        "reference section that does not exist": ("ScientistOne defines the whole audit there [Ref: meng2026scientistone §99].\n", 1, "case.md"),
        "a [Ref:] shown as code unlocks nothing": ('Tags look like `[Ref:]`, and "We run each evaluator five times" [§4.2].\n', 1, "case.md"),
        "empty straight quotes": ('An empty result is written as "" in the log [ours].\n', 0, "case.md"),
        "empty curly quotes": ("An empty result is written as “” in the log [ours].\n", 0, "case.md"),
        "a bare number after the location": ("The table shows the whole matter [Tab. 1, 99].\n", 1, "case.md"),
        "a bare number after a second location": ("The coder is defined there in full [§3.2, Eq. 4, 99].\n", 1, "case.md"),
        "a location keyword with no location": ("The figure shows the whole matter [§3.2, Fig.].\n", 1, "case.md"),
        "a panel the figure lacks": ("The panel shows the whole matter [Fig. 9c].\n", 1, "case.md"),
        "a panel range written backwards": ("The panels show the whole matter [Fig. 9b–9a].\n", 1, "case.md"),
        "real panels": ("The panels show the whole matter [Fig. 9a–9b] [Fig. 1b] [Fig. 10a].\n", 0, "case.md"),
        "pages after a section": ("The section and its pages show it [§3.2, pp. 7–8].\n", 0, "case.md"),
        "a fabricated fragment in a long quote": ('It says "If performance is substantially inferior [...] the critic always approves" [§3.2].\n', 1, "case.md"),
        "a long quote whose fragments are real": ('It says "If performance is substantially inferior [...] baseline" [§3.2].\n', 0, "case.md"),
        "anchor climbing out of the source": ("The setup is quoted from there [§4.2] "
                                              "(tex:../../../.cache/refs/2605.26340v1/src/sections/06a_setup.tex:10).\n", 1, "case.md"),
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
