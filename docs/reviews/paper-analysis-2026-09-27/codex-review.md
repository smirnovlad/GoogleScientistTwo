# Codex review of the branch (2026-09-28)

- **Reviewed:** `git diff main...HEAD` on `claude/paper-analysis` at commit `8b34d8a`, excluding
  the paper's verbatim TeX in `docs/paper/source/`.
- **Tool:** the Codex CLI (`codex review`, reasoning effort high, read-only sandbox), run through the
  `/codex` skill, as the parent project's review gate requires.
  - The configured default model was refused for this account, so this run used
    `-c model="gpt-6-astra"`.
  - The skill's `--base main` form does not accept custom instructions in this CLI version, so the
    diff range was named in the instructions instead.
- **Gate:** PASS. There is no [P1] finding; there are seven [P2].
- **Record:** Codex's output, verbatim below, with one change: it named files by absolute path,
  shortened here to repository-relative paths, because this repository never holds a path from
  someone's machine.

---

The current checks pass, but targeted tests demonstrate citation-validation false passes and an impossible rating distribution reported as acceptable. The source verifier also leaves the redacted line unchecked, and two analysis conclusions remain contradictory.

Full review comments:

- [P2] Keep note quotations separate from paper evidence — playground/paper/check_citations.py:71-72
  Adding the unverified note to the paper corpus lets its wording pass as a ScientistTwo quotation. For example, `The paper requires "Self-contained scripts plus an LLM validation filter" [§4.2].` passes with the note present and fails against the paper alone. Restrict note-derived matches to explicitly identified note quotations; otherwise this bypasses the primary-source requirement in [CLAUDE.md:17–19](CLAUDE.md#L17-L19).

- [P2] Validate complete citation tags and their targets — playground/paper/check_citations.py:40-40
  The coverage check accepts `[§999.999]`, `[Tab. 999]`, and even an unfinished `[§` as citations. None receives further validation unless a separate TeX anchor happens to accompany it, so nonexistent locations return zero problems despite the checker's stated guarantee that citations are real. Validate the complete tag and its target against the paper's section, float, page, and bibliography inventory.

- [P2] Check quotations across Markdown line breaks — playground/paper/check_citations.py:144-148
  Quotation matching runs separately on each physical line and explicitly excludes newlines. Consequently, a fabricated quotation rejected on one line passes unchanged when wrapped across two lines, provided the paragraph has a citation. This defeats the five-word quotation check under ordinary Markdown formatting. Match quotations across logical content units while retaining their starting line for diagnostics.

- [P2] Verify the permitted redaction instead of ignoring its line — playground/paper/fetch_sources.sh:69-71
  Deleting line 46 from both comparison inputs allows arbitrary content there, including restoration of the original email addresses, while still reporting that the source matches and is redacted. The line-count comparison does not prevent this. Verify the committed line against the intended sanitized replacement, then compare the remaining text; otherwise the provenance check cannot enforce the repository's explicit no-email rule ([CLAUDE.md:10–11](CLAUDE.md#L10-L11)).

- [P2] Distinguish a passing lower bound from feasible ratings — playground/paper/reviews/research-engineer/sp_threshold.py:52-54
  The current run reports S2 ICLR as `ok` at threshold 7, although that row is impossible: all four ratings must be at least 7, and a mean rounding to 7.0 limits their sum to below 28.2, giving a maximum population SD below 0.087—not the printed 1.2. A minimum-SD bound below the reported SD is necessary but not sufficient for feasibility. Check the achievable variance range or label these results as merely not ruled out by the lower-bound test.

- [P2] Remove the withdrawn inference that a significance test exists — docs/paper/claims/appendix-b.md:68-68
  This assessment says that “statistically inert” implies a significance test, while `analysis.md:288` explicitly withdraws that inference because the phrase establishes only a critic's judgment. `artifacts.md` likewise records that no test is shown. Readers using these deliverables for requirements therefore receive conflicting answers about whether the critic performs a statistical test. Preserve the uncertainty here rather than reinstating the withdrawn inference.

- [P2] Include ICLR among the shared task pools — docs/paper/claims/main-results.md:77-77
  The assessment says only NeurIPS is a shared pool, but the sample description at line 70 states that both NeurIPS and ICLR use the same 33 and four input papers respectively. This incorrectly makes task-pool mismatch appear to invalidate the ICLR comparison; its documented limitations concern different metrics and reproduced baselines instead. State that both venue-specific pools are shared while retaining those comparability caveats.

---

## Outcome (2026-09-28)

All seven [P2] findings were fixed before the PR. None was dismissed.

1. **The note as paper evidence** (`check_citations.py`).
   - The note is now its own corpus. It counts only in `note-check.md`: in a unit that names an
     N- claim or the note, or in a heading.
   - Two self-test cases plant a note quote passed off as the paper's, and one outside
     `note-check.md`.
2. **Unchecked locations** (`check_citations.py`).
   - Every tag's location is checked against an inventory: sections, appendices, equations and
     footnotes from the TeX; floats, from `float_numbering.py`, and pages from the PDF; keys from
     `main.bib`.
   - Nine new self-test cases plant a missing section, table, page, equation or key, a page range
     written backwards, an unclosed tag, and a tag shown as code; one more checks that real
     locations pass.
   - The stricter check found no defect in the documents.
3. **Quotes across line breaks** (`check_citations.py`).
   - Quotes are matched within a whole paragraph, list item or table row, and a list item's
     wrapped lines now belong to it.
   - Self-test cases cover a fake quote and a real one, each wrapped across two lines.
4. **The redacted line** (`fetch_sources.sh`).
   - Line 46 must now be exactly the redaction, and the archive's line 46 must be the
     `\correspondingauthor` line it replaces. The failure message does not print the line.
   - Tamper test: a planted address fails the run (exit 1) without appearing in its output. The
     clean tree passes.
5. **"ok" for an infeasible row** (`sp_threshold.py`). The label now reads "not ruled out by
   this bound", and the script's README records the edit.
6. **The significance-test inference** (`claims/appendix-b.md`). It is withdrawn, as in
   `analysis.md`. The phrase is a critic's verdict worded as a statistical one.
7. **The shared pools** (`claims/main-results.md` and `claims.md`). Both venue pools are shared,
   and only the overall pools differ. The comparability caveats stay, recast as limits of
   measurement.

---

## Second pass (2026-09-28), on commit `28100fc`

Same tool and settings. **Gate: PASS** (no [P1]; five [P2], all in `check_citations.py`). Verbatim, with paths shortened as above:

The committed checks and self-tests pass, and the pinned source hashes and exact redaction match. However, targeted tests expose remaining citation false passes and an empty-quotation crash; the note-isolation and complete-location fixes are incomplete.

Full review comments:

- [P2] Restrict note matches to explicitly identified note quotations — playground/paper/check_citations.py:236-237
  In `note-check.md`, an N-claim ID enables the note corpus for the entire row, including its Evidence cell. A row containing `The paper requires "Self-contained scripts plus an LLM validation filter" [§4.2]` passes, although those words occur only in the note. Even prose beginning `The paper notes...` enables this exception through the substring check. Separate note quotations from paper evidence rather than granting the whole unit access to both corpora; otherwise the original isolation fix remains incomplete under [CLAUDE.md:17–19](CLAUDE.md#L17-L19).

- [P2] Validate the remaining locations inside each citation tag — playground/paper/check_citations.py:193-197
  The new inventory check validates only the leading location and, optionally, the first equation. Both `[Tab. 1–999]` and `[§3.2, Fig. 999]` return zero problems because the remaining text is ignored. Thus nonexistent targets still pass despite the recorded fix for complete-tag validation. Parse and validate every structured location or range endpoint before accepting an explanatory suffix, preserving the paper-location requirement in [CLAUDE.md:17–19](CLAUDE.md#L17-L19).

- [P2] Bind reference quotations to the validated source identity — playground/paper/check_citations.py:210-218
  Any raw `[Ref:` substring unlocks every cached reference. Consequently, the ScientistOne quotation `"We run each evaluator five times"` passes with `[Ref: jiang2026incremental §999]`, an unrelated bibliography entry. It also passes as a ScientistTwo quotation when the paragraph merely includes the code example `` `[Ref:]` ``. Derive permitted corpora from validated, non-code reference tags or anchors and match their source identities, rather than using one pooled corpus. This preserves the primary-source attribution required by [CLAUDE.md:17–19](CLAUDE.md#L17-L19).

- [P2] Handle empty quotations before splitting their contents — playground/paper/check_citations.py:213-215
  A legitimate statement such as `An empty result is represented as "" [ours].` crashes the checker with `TypeError` instead of passing the short-quotation exemption. For an empty straight-quoted match, group 1 is an empty string and group 2 is `None`, so the `or` expression supplies `None` to `re.split`. Select the participating group using an explicit `is not None` check and cover empty straight and curly quotations in the self-test.

- [P2] Enforce the declared source root for citation anchors — playground/paper/check_citations.py:243-246
  Anchor paths allow `..`, but joining them to `SOURCE` does not enforce containment. With the fetched cache present, `tex:../../../.cache/refs/2605.26340v1/src/sections/06a_setup.tex:10` passes as a paper-source anchor even though it points into ScientistOne. Resolve targets and require containment under the appropriate source root before checking existence and line bounds; apply the same restriction to reference anchors. Otherwise the primary-source boundary in [CLAUDE.md:17–19](CLAUDE.md#L17-L19) can be bypassed.

### Outcome of the second pass

All five were fixed. Two of them showed that first-pass fixes were incomplete.

1. **The note, again.** It now counts only in the claim cell of an N- row, or in a heading of
   `note-check.md`. The evidence cells of the same rows are excluded, and so is any unit that
   merely contains "note".
2. **Every location in a tag.** Both ends of a range are checked, and so is every further
   location after the first, such as `, Fig. 5`. Names in quotes are titles, not locations.
3. **References bound to their source.** A `[Ref: key …]` tag must name a key whose `main.bib`
   entry gives the arXiv id of a cached source. Its § or App. must exist in that source's own
   TeX, and only that source's text can match a quote. A `[Ref:]` shown as code unlocks nothing.
4. **Empty quotes** no longer crash the checker.
5. **Anchors** must resolve inside `docs/paper/source/`, or inside their reference's `src/`.

**Tests.** The self-test grows to 37 cases, among them one planted defect for each finding
above. The documents pass unchanged: 18 files, 0 problems.

---

## Third pass (2026-09-28), on commit `6e52d54`

Same tool and settings. **Gate: PASS** (no [P1]; four [P2], all in `check_citations.py`). Verbatim, with paths shortened as above:

The existing checks and all 37 citation self-tests pass, and the pinned source hashes and exact redaction match. However, targeted tests expose three remaining citation/quotation false passes and a valid-citation false failure.

Full review comments:

- [P2] Reject unparsed locations in citation suffixes — playground/paper/check_citations.py:239-243
  Both `[Tab. 1, 99]` and `[§3.2, Eq. 4, 99]` return zero problems because the suffix scanner ignores numbers without a repeated location prefix. `[§3.2, Fig.]` also passes. The second-pass complete-tag fix therefore still accepts nonexistent or incomplete citations, contrary to the paper-location requirement in [CLAUDE.md:17–19](CLAUDE.md#L17-L19). Parse the entire structured suffix, or reject unconsumed location syntax.

- [P2] Validate figure panels before removing their suffixes — playground/paper/check_citations.py:230-231
  `[Fig. 9c]` passes although Figure 9 has only panels (a) and (b); the backwards range `[Fig. 9b–9a]` also passes. Removing the suffix before checking existence and ordering makes any panel letter valid whenever its parent figure exists. Preserve and validate panel identities so panel-level citation mistakes are caught under the location requirement in [CLAUDE.md:17–19](CLAUDE.md#L17-L19).

- [P2] Check short fragments within long ellipsized quotations — playground/paper/check_citations.py:306-308
  `It says "If performance is substantially inferior [...] the critic always approves" [§3.2].` returns zero problems: the first fragment exists, but the fabricated four-word conclusion is skipped. Applying the five-word exemption separately to fragments leaves substantial portions of long quotations unchecked, contrary to the [quotation convention](docs/paper/README.md#L139-L141). Apply the length threshold to the complete quotation, then verify every nonempty fragment.

- [P2] Normalize plural page tags before inventory lookup — playground/paper/check_citations.py:240-242
  A valid combined citation such as `[§3.2, pp. 7–8]` fails with `no such location`, while `[§3.2] [pp. 7–8]` passes. The inventory contains `p.`, not `pp.`, so this membership check rejects plural page tags before `locations_ok()` can normalize them. Normalize the kind before testing inventory membership.

### Outcome of the third pass, and where the reviews stop

All four were fixed:
1. **Unparsed text after a tag's locations** may be prose, but never a bare number or a location
   keyword, so `[Tab. 1, 99]` and `[§3.2, Fig.]` fail. A name such as ScientistOne's "I2" still
   passes.
2. **Figure panels are checked.**
   - The TeX names the panels of three figures, in the caption or the body; the panels printed
     only in Figure 1's image are declared, with their printed labels.
   - The TeX's figure order is matched to the PDF's captions before any panel is trusted.
   - A panel range must run forward.
3. **The five-word threshold applies to the whole quotation,** and then every fragment between
   ellipses is checked.
4. **`pp.` after a first location** is no longer a false failure.

**Tests.** The self-test has 46 cases. The documents pass unchanged: 18 files, 0 problems.

**The stopping rule.** It was set before this pass ran: fix any [P1] before the PR, and fix
further [P2] edge cases when cheap, or record them. All passes gated PASS, and every finding was
fixed. A fourth pass could still find regex edge cases.

**What no pass can settle.** The checker verifies that every cited location, anchor and quote
exists. It cannot tell whether the location supports the statement. That is the job of the six
persona reviews, their closure checks and the blind reader.
