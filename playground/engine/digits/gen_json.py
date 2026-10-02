"""One-off generator: writes agent.json and schema.json for every agent of engine.md section 7.

Kept in the scratchpad, not the repository: the checked-in data is the JSON it writes, and
playground/engine/check_agents.py checks that data against section 7 independently.
"""
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
AGENTS = ROOT / "scientisttwo" / "agents"
ENGINE = ROOT / "docs" / "architecture" / "engine.md"

TOOLS = {
    "coding": ["Bash", "Read", "Edit", "Write", "Glob", "Grep"],
    "writer": ["Read", "Edit", "Write", "Glob", "Grep", "Bash"],
    "readonly": ["Read", "Glob", "Grep", "Bash"],
    "reasoning": [],
}

DESCRIPTIONS = {
    "limitation_extractor": "Extracts the core limitations of the task's method from its paper and code, and expands the set on the verifier's feedback.",
    "limitation_verifier": "Judges whether the set of limitations is sufficient to guide novel, concrete improvements, and names what is missing.",
    "initial_idea_generator": "Proposes the first seed idea, designed to resolve the identified limitations.",
    "novelty_checker": "Finds the two most related papers by web search and scores the idea's novelty against them, 1 to 10.",
    "idea_generator": "Adds one new seed idea to the pool, distinct from every idea in it and aiming at higher novelty.",
    "baseline_coder": "Makes the task's codebase a faithful, runnable reproduction of the paper's method under the entrypoint contract.",
    "subset_coder": "Implements one idea by modifying the baseline codebase, for screening on the benchmark subset.",
    "subset_critic": "Judges an idea's subset result against the reproduced baseline: Good, Engineer or Bad.",
    "subset_engineer": "Fixes the engineering defect the subset critic named, changing the idea only where the fix requires it.",
    "full_set_coder": "Prepares a subset-validated idea's codebase to run on the full benchmark.",
    "full_set_critic": "Gives an idea its verdict on the full benchmark against the reproduced baseline: Good, Engineer or Bad.",
    "full_set_engineer": "Revises the idea and its code on full-set, ablation or meta-review feedback, aiming to beat the best result.",
    "idea_evolver": "Proposes one new idea from all execution traces, learning from failures and combining what worked.",
    "selector": "Chooses the best idea among those validated as Good on the full benchmark.",
    "ablation_planner": "Plans one-component ablations of the selected idea, reading its codebase, so that the gain can be attributed.",
    "ablation_coder": "Turns the selected codebase into one ablation variant, as one plan describes.",
    "ablation_critic": "Judges whether the gain is attributable to the idea's components: Good, Refine or Reject.",
    "initial_drafter": "Writes the manuscript (main.tex, references.bib) from the selected idea and the verified results.",
    "peer_reviewer": "Writes an ICLR-style review of the manuscript with a 1 to 10 score; the reviewer the loop optimises against.",
    "rebuttal_planner": "Plans the supplementary experiments that answer the review's concerns.",
    "rebuttal_coder": "Turns the selected codebase into the variant one rebuttal experiment needs.",
    "paper_enhancer": "Revises the manuscript to answer the review with the rebuttal results, and fixes what the audit found.",
    "meta_reviewer": "Decides whether the reviewed manuscript meets the venue bar: Accept, or Refine with feedback for the method.",
    "spec_filter": "Audits a solution's code, read-only, for violations of the task rules and for reward hacking.",
    "reference_checker": "Verifies each bibliography entry by web search: verified, not_found or mismatch.",
    "method_code_auditor": "Audits, read-only, whether the code implements the method the manuscript describes.",
    "final_judge": "Held-out judge: scores the final manuscript once, after the loop, on its own rubric.",
}


def s(desc=None):
    out = {"type": "string"}
    if desc:
        out["description"] = desc
    return out


def strings(desc=None, min_items=0):
    out = {"type": "array", "items": {"type": "string"}}
    if min_items:
        out["minItems"] = min_items
    if desc:
        out["description"] = desc
    return out


def obj(props, desc=None):
    out = {"type": "object"}
    if desc:
        out["description"] = desc
    out["properties"] = props
    out["required"] = list(props)
    out["additionalProperties"] = False
    return out


def top(props):
    # No "$schema": claude 2.1.287 refuses the 2020-12 meta-schema URI (smoke test, 2026-10-02).
    return obj(props)


def enum(values, desc=None):
    out = {"type": "string", "enum": list(values)}
    if desc:
        out["description"] = desc
    return out


def integer(lo, hi, desc=None):
    out = {"type": "integer", "minimum": lo, "maximum": hi}
    if desc:
        out["description"] = desc
    return out


IDEA = obj({
    "title": s("A short descriptive name, with an acronym"),
    "summary": s("Two to four sentences: the idea, its components, and the limitations it resolves"),
    "addresses": strings("Ids of the limitations the idea addresses, such as L2", min_items=1),
    "method": s("The method, component by component: what each does, the limitation it addresses, "
                "its equations or algorithm, and the default value of every new hyperparameter"),
    "implementation_plan": strings("Ordered steps that change the codebase, naming files and "
                                   "functions where known", min_items=1),
    "expected_effect": s("Which metric should move, in which direction, on which inputs, and why"),
    "risks": s("What could make the idea fail, and how a failure would show in results or logs"),
})


def idea(desc=None):
    out = copy.deepcopy(IDEA)
    if desc:
        out = {"description": desc, **out}
    return out


VERDICT_FEEDBACK = "Begins with the deciding numbers; then what to do or what was learnt"

SCHEMAS = {
    "limitation_extractor": top({
        "limitations": {
            "type": "array", "minItems": 1,
            "description": "The full set: earlier limitations under their ids, plus new ones",
            "items": obj({
                "id": s("L1, L2, ...: stable across calls"),
                "title": s("One line naming the limitation"),
                "description": s("The flaw, why it limits the method, and the opportunity"),
                "evidence": s("Where the inputs show it, quoted briefly; begins with 'inferred:' "
                              "for a reasoned inference"),
            }),
        },
    }),
    "limitation_verifier": top({
        "verdict": enum(["sufficient", "insufficient"]),
        "feedback": s("For insufficient: a numbered list of gaps; for sufficient: why it suffices"),
    }),
    "initial_idea_generator": top({"idea": idea()}),
    "novelty_checker": top({
        "references": {
            "type": "array", "maxItems": 2,
            "description": "The two most related papers, taken from this session's search results",
            "items": obj({
                "title": s("Title as shown in the search results"),
                "url": s("URL as shown in the search results"),
                "relation": s("What the paper shares with the idea, and what the idea adds"),
            }),
        },
        "novelty_score": integer(1, 10, "1-2 published; 3-4 close variant; 5-6 partial overlap; "
                                        "7-8 new mechanism here; 9-10 no close prior work"),
        "rationale": s("Why this score, against each reference; begins with 'SEARCH FAILED:' if "
                       "the search tool failed"),
    }),
    "idea_generator": top({"idea": idea()}),
    "baseline_coder": top({
        "faithful": {"type": "boolean",
                     "description": "True when the code implements the paper's method, with only "
                                    "rule-forced deviations, all listed in changes"},
        "changes": strings("One item per change: the file, what changed, and why"),
        "notes": s("What was verified and how, every deviation and its reason"),
    }),
    "subset_coder": top({
        "summary": s("What was implemented, component by component, and where"),
        "files_changed": strings("Paths changed or added, relative to the working directory"),
        "self_checks": strings("One item per check run: what it did and what it showed; holdout "
                               "numbers marked as debug only"),
        "notes": s("Deviations from the idea, the component switches, caveats for the critic"),
    }),
    "subset_critic": top({
        "verdict": enum(["Good", "Bad", "Engineer"]),
        "feedback": s(VERDICT_FEEDBACK),
    }),
    "subset_engineer": top({
        "idea": {"description": "null if the idea is unchanged; otherwise the complete revised idea",
                 "anyOf": [idea(), {"type": "null"}]},
        "summary": s("The problem, its cause, the fix, and how it was verified"),
        "files_changed": strings("Paths changed or added, relative to the working directory"),
    }),
    "full_set_coder": top({
        "summary": s("What was checked and changed, and the runtime estimate with its method"),
        "files_changed": strings("Paths changed or added, relative to the working directory"),
        "notes": s("Every changed setting and why; risks for the full run"),
    }),
    "full_set_critic": top({
        "verdict": enum(["Good", "Bad", "Engineer"]),
        "feedback": s(VERDICT_FEEDBACK),
    }),
    "full_set_engineer": top({
        "idea": idea("The complete revised idea, describing the code as it now is"),
        "summary": s("What the feedback asked, what changed and why, and how it was verified"),
        "files_changed": strings("Paths changed, added or deleted, relative to the working directory"),
    }),
    "idea_evolver": top({"idea": idea()}),
    "selector": top({
        "choice": s("The id of the chosen candidate, exactly as given"),
        "rationale": s("The comparison that decided it, with each contender's gain and spread"),
    }),
    "ablation_planner": top({
        "plans": {
            "type": "array", "minItems": 1,
            "description": "Exactly n_plans plans, each changing one component",
            "items": obj({
                "id": s("A1, A2, ..."),
                "component": s("The component removed or replaced, named as the idea names it"),
                "change": s("Exactly what to change in the code, by what, and where"),
                "hypothesis": s("What the result shows if the component matters, and if it does not"),
            }),
        },
    }),
    "ablation_coder": top({
        "summary": s("What changed, where, and how the component was confirmed off"),
        "files_changed": strings("Paths changed, relative to the working directory"),
        "notes": s("Departures from the plan and why; anything that makes the comparison less clean"),
    }),
    "ablation_critic": top({
        "verdict": enum(["Good", "Refine", "Reject"]),
        "feedback": s("Each component's effect, numbers and class; then what to do"),
    }),
    "initial_drafter": top({
        "title": s("The paper's title, as in main.tex"),
        "abstract": s("The abstract, as in main.tex"),
        "notes": s("Whether it compiled and how that was checked; packages; open issues"),
    }),
    "peer_reviewer": top({
        "summary": s("What the paper claims and does, without judgement"),
        "strengths": strings("One item per strength", min_items=1),
        "weaknesses": strings("One item per weakness: what, where, and what evidence would "
                              "resolve it; most important first", min_items=1),
        "questions": strings("Questions whose answers could change the assessment"),
        "score": integer(1, 10, "ICLR scale: 1, 3, 5, 6, 8 or 10"),
        "confidence": integer(1, 5, "ICLR confidence, 1 to 5"),
    }),
    "rebuttal_planner": top({
        "tasks": {
            "type": "array", "minItems": 1,
            "description": "Exactly n_tasks tasks, each one code variant the harness can run",
            "items": obj({
                "id": s("T1, T2, ..."),
                "concern": s("The reviewer's point, quoted or paraphrased, with its place in the review"),
                "experiment": s("The one variant to build, what it is compared with, and why it "
                                "settles the concern"),
                "expected_outcome": s("The result that would answer the concern, and the one that "
                                      "would confirm it"),
            }),
        },
    }),
    "rebuttal_coder": top({
        "summary": s("The variant built, where, and how it was checked"),
        "files_changed": strings("Paths changed or added, relative to the working directory"),
        "notes": s("Departures from the plan; begins with 'NOT FEASIBLE:' if nothing was changed"),
    }),
    "paper_enhancer": top({
        "changes": strings("One item per edit: where, and what changed"),
        "responses": strings("One item per weakness or question, in order: the point, then how "
                             "the revision answers it or why it does not"),
    }),
    "meta_reviewer": top({
        "decision": enum(["Accept", "Refine"]),
        "feedback": s("For Refine: the critical method weakness first, then presentation; for "
                      "Accept: why it meets the bar"),
    }),
    "spec_filter": top({
        "compliant": {"type": "boolean", "description": "True if and only if violations is empty"},
        "violations": {
            "type": "array",
            "items": obj({
                "rule": s("The rule or check broken, quoted or named"),
                "evidence": s("File and line numbers, and what the code does there"),
            }),
        },
    }),
    "reference_checker": top({
        "entries": {
            "type": "array",
            "description": "One item per bibliography entry, each exactly once",
            "items": obj({
                "key": s("The BibTeX key"),
                "status": enum(["verified", "not_found", "mismatch"]),
                "evidence": s("The matched record's URL and, for a mismatch, the correct values; "
                              "for not_found, the searches run"),
            }),
        },
    }),
    "method_code_auditor": top({
        "consistent": {"type": "boolean",
                       "description": "True if there is no critical and no major issue"},
        "issues": {
            "type": "array",
            "items": obj({
                "severity": enum(["critical", "major", "minor"]),
                "claim": s("The manuscript's statement, quoted briefly with its section or equation"),
                "evidence": s("File and line numbers, and what the code does there"),
            }),
        },
    }),
    "final_judge": top({
        "score": integer(1, 10, "Overall score on the judge's own rubric"),
        "decision": enum(["accept", "reject"], "accept if and only if the score is 6 or more"),
        "rationale": s("First line: the five rubric scores; then the justification"),
    }),
}


def section7_rows(text):
    sec = text.split("## 7. Agents", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in sec.splitlines():
        if not line.startswith("| ") or line.startswith("| Agent") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        rows.append(cells)
    return rows


def main():
    rows = section7_rows(ENGINE.read_text())
    assert len(rows) == 27, len(rows)
    for name, paper, kind_tools, variables, _output in rows:
        kind_part, _, extra = kind_tools.partition(",")
        kind = kind_part.strip().replace("read-only", "readonly")
        tools = list(TOOLS[kind])
        if kind == "reasoning" and extra.strip():
            tools = extra.strip().split("/")
        folder = AGENTS / name
        assert folder.is_dir(), folder
        spec = {
            "name": name,
            "kind": kind,
            "tools": tools,
            "paper_ref": paper,
            "description": DESCRIPTIONS[name],
            "variables": [v.strip() for v in variables.split(",")],
        }
        (folder / "agent.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
        (folder / "schema.json").write_text(
            json.dumps(SCHEMAS[name], indent=2, ensure_ascii=False) + "\n")
        print(f"{name:24s} {kind:9s} tools={tools} vars={len(spec['variables'])}")


main()
