"""Float numbering of arXiv:2609.19644v1 in the PDF and in the HTML, matched by caption.

Why this exists: the two renderings number the floats differently. The TeX puts the stage
pseudocode in a minted `listing` float, which pdflatex numbers "Listing 1"; LaTeXML (the HTML)
turns it into "Figure 4", so every later HTML figure number is one higher than the PDF's.
docs/paper/ cites the PDF numbering; this script is the evidence and re-runs in a second.

Usage: python3 playground/paper/float_numbering.py   (after playground/paper/fetch_sources.sh)
Prints a Markdown table: PDF label | HTML label | caption start | agree?
Exits 1 if a float found in one rendering has no caption match in the other.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
CACHE = ROOT / ".cache/paper/2609.19644v1"


def norm(text: str) -> str:
    """Caption key: the first four words, lower-cased, ASCII letters and digits only.
    Four, because inline math renders differently in the two (PDF "ACoder", HTML "𝒜Coder") and
    the first math symbol in any caption comes after its fourth word; main() fails on a clash."""
    words = re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()
    return " ".join(words[:4])


def pdf_floats() -> list[tuple[str, str]]:
    """Captions of the paper itself. Floats inside embedded generated papers use 'Table N:'
    (a colon) and are indented; the paper's own captions start the line with 'Table N |'."""
    text = (CACHE / "paper.pdf.txt").read_text(encoding="utf-8")
    found = []
    for m in re.finditer(r"^(Table|Figure|Listing) (\d+) \| (.+)$", text, re.M):
        found.append((f"{m.group(1)} {m.group(2)}", m.group(3).strip()))
    return found


def html_floats() -> list[tuple[str, str]]:
    page = (CACHE / "paper.html").read_text(encoding="utf-8")
    found = []
    page = re.sub(r"<annotation[^>]*>.*?</annotation>", "", page, flags=re.S)  # TeX alt-text
    for m in re.finditer(r"<figcaption[^>]*>(.*?)</figcaption>", page, re.S):
        caption = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip()
        head = re.match(r"(Table|Figure|Listing) (\d+):\s*(.*)", caption)
        if head:
            found.append((f"{head.group(1)} {head.group(2)}", head.group(3)))
    return found


def main() -> int:
    pdf, htm = pdf_floats(), html_floats()
    for name, floats in (("PDF", pdf), ("HTML", htm)):
        keys = [norm(caption) for _, caption in floats]
        if len(set(keys)) != len(keys):
            print(f"{name}: two captions share a key; lengthen norm()", file=sys.stderr)
            return 1
    by_caption = {norm(caption): label for label, caption in htm}
    print("| PDF (cite this) | HTML | caption starts | same number? |")
    print("|---|---|---|---|")
    missing = 0
    for label, caption in pdf:
        other = by_caption.pop(norm(caption), None)
        missing += other is None
        same = "yes" if other == label else "**no**"
        print(f"| {label} | {other or '(not found)'} | {caption[:48]} | {same} |")
    for key, label in by_caption.items():
        missing += 1
        print(f"| (not found) | {label} | {key[:48]} | **no** |")
    print(f"\nPDF floats: {len(pdf)}; HTML floats: {len(htm)}; unmatched: {missing}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
