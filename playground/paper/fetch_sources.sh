#!/usr/bin/env bash
# Fetch the three sources of arXiv:2609.19644v1 into the gitignored cache, verify them, and check
# that the TeX committed in docs/paper/source/ is the archive's text.
#
# Usage: bash playground/paper/fetch_sources.sh   (from anywhere inside the repository)
#
# Produces, under .cache/paper/2609.19644v1/:
#   src.tar.gz  the TeX source archive      (sha256 verified, must match)
#   paper.pdf   the arXiv-compiled PDF      (sha256 verified, must match)
#   paper.html  the arXiv HTML (LaTeXML)    (sha256 compared; arXiv may regenerate HTML, so a
#                                            mismatch is a warning, never a silent pass)
#   src/        the extracted archive, figures included
#   paper.pdf.txt  `pdftotext -layout` of the PDF, for grepping; PDF page N is the Nth form feed
#
# ⛔ WHY NOT fetch the unversioned URLs (arxiv.org/src/2609.19644): they follow the latest
# version, so a v2 would silently change what every citation in docs/paper/ points at.
set -euo pipefail

VERSION="2609.19644v1"
ROOT="$(git rev-parse --show-toplevel)"
CACHE="$ROOT/.cache/paper/$VERSION"
SOURCE="$ROOT/docs/paper/source"
UA="Mozilla/5.0 (paper replication; source fetch)"

SHA_SRC="60e05f1188a289bc1ec1fd44f1432b7b2dc4d910effb502dc272953924822980"
SHA_PDF="98fb7802ec28beea159895a3de219307e019867b16296dfe4a79e68daaef9a17"
SHA_HTML="23f93180ac10e5b4e1cbdf9f1e532aa80c33351b7968345752ec7c6d12925aa3"   # fetched 2026-09-27
# The one line of docs/paper/source/ that differs from the archive: main.tex line 46, whose
# e-mail addresses this public repository must not hold. It is checked to be exactly this text.
REDACTED_46='\correspondingauthor{[redacted in this copy: two e-mail addresses; see the arXiv original]}'

mkdir -p "$CACHE"
cd "$CACHE"

sha() { shasum -a 256 "$1" | cut -d' ' -f1; }

fetch() {  # fetch <url> <file> <expected-sha> <strict:1|0>
  local url="$1" file="$2" want="$3" strict="$4"
  if [[ -f "$file" && "$(sha "$file")" == "$want" ]]; then
    echo "ok (cached)  $file"
    return
  fi
  curl -sSfL -A "$UA" -o "$file" "$url"
  local got; got="$(sha "$file")"
  if [[ "$got" == "$want" ]]; then
    echo "ok (fetched) $file"
  elif [[ "$strict" == 1 ]]; then
    echo "FAIL $file: sha256 $got, expected $want" >&2
    exit 1
  else
    echo "WARN $file: sha256 $got differs from the 2026-09-27 fetch ($want)." >&2
    echo "     arXiv regenerates HTML; re-check the float numbering before trusting it." >&2
  fi
}

fetch "https://arxiv.org/src/$VERSION"  src.tar.gz "$SHA_SRC"  1
fetch "https://arxiv.org/pdf/$VERSION"  paper.pdf  "$SHA_PDF"  1
fetch "https://arxiv.org/html/$VERSION" paper.html "$SHA_HTML" 0

rm -rf src && mkdir src && tar -xzf src.tar.gz -C src
pdftotext -layout paper.pdf paper.pdf.txt 2>/dev/null
echo "ok           src/ extracted, paper.pdf.txt written ($(grep -c $'\f' paper.pdf.txt) pages)"

# The committed TeX must be the archive's text. The one permitted difference is the redaction of
# the corresponding authors' e-mail addresses on main.tex line 46 (docs/paper/source/README.md).
status=0
while IFS= read -r -d '' committed; do
  rel="${committed#"$SOURCE"/}"
  if [[ ! -f "src/$rel" ]]; then
    echo "FAIL docs/paper/source/$rel is not in the archive" >&2; status=1; continue
  fi
  if [[ "$rel" == "main.tex" ]]; then
    diffs="$(diff <(sed '46d' "src/$rel") <(sed '46d' "$committed") || true)"
    [[ "$(wc -l < "src/$rel")" == "$(wc -l < "$committed")" ]] || diffs="line count differs"
    # Excluding line 46 from the diff is not enough: anything could sit there, the original
    # addresses included. So the archive's line 46 must be the line redacted, and ours the redaction.
    [[ "$(sed -n 46p "src/$rel")" == '\correspondingauthor{'* ]] \
      || diffs="${diffs}${diffs:+$'\n'}the archive's line 46 is not the \\correspondingauthor line"
    [[ "$(sed -n 46p "$committed")" == "$REDACTED_46" ]] \
      || diffs="${diffs}${diffs:+$'\n'}line 46 is not the expected redaction (its text is not printed: it may hold an address)"
  else
    diffs="$(diff "src/$rel" "$committed" || true)"
  fi
  if [[ -n "$diffs" ]]; then
    echo "FAIL docs/paper/source/$rel differs from the archive:" >&2; echo "$diffs" >&2; status=1
  fi
done < <(find "$SOURCE" -type f \( -name '*.tex' -o -name '*.bib' \) -print0)
[[ "$status" == 0 ]] && echo "ok           docs/paper/source/ matches the archive (main.tex:46 redacted)"

# Sources the paper delegates to by reference (docs/paper/README.md, "Sources the paper delegates
# to"). ScientistOne defines the integrity audit that Table 7 follows ("following Meng et al.").
# Its TeX is read for what ScientistTwo delegates to it, and the citation checker verifies quotes
# from it; it is CC BY 4.0, but not committed, since only a few paragraphs are cited.
REF_ID="2605.26340v1"
SHA_REF_SRC="0655a648b6dca95979204e19939aedae232e99e98862cc62898f0b8c5e7da9db"
mkdir -p "$ROOT/.cache/refs/$REF_ID" && cd "$ROOT/.cache/refs/$REF_ID"
fetch "https://arxiv.org/src/$REF_ID" src.tar.gz "$SHA_REF_SRC" 1
rm -rf src && mkdir src && tar -xzf src.tar.gz -C src
echo "ok           ScientistOne ($REF_ID) extracted to .cache/refs/$REF_ID/src/"
exit "$status"
