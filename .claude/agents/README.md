# The personas: pick one by the QUESTION, not the topic

Each persona judges work by a different measure. Route a task to the one whose question it is,
automatically, and run reviews in parallel, one lens each. A review that nobody owns is a class of
failure nobody catches, so when you add a persona, ask which failure is unowned.

| Persona | Judges by | Route here for |
|---|---|---|
| `paper-analyst` | what the paper **actually says** | reading the paper; SPECIFIED vs UNSPECIFIED vs AMBIGUOUS; checking any secondary source against the paper; traceability |
| `system-architect` | what a change **costs** across the engine | components, contracts, data flow, the stage primitive, resumability, what is data vs code |
| `research-engineer` | whether a **number can be trusted** | task environments, baselines, metrics, splits, seeds and variance, ablations, compute budgets |
| `evaluation-integrity-engineer` | whether an agent **can cheat unnoticed** | the locked harness, validation/test separation, the audit, every guard and its control |
| `agent-engineer` | how an agent **behaves on traces** | the reasoning agents: prompts as data, output schemas, model routing, context, failure modes |
| `infrastructure-engineer` | whether a multi-day run **survives and resumes** | containers, GPU queue, run state, crash recovery, cost ledger, mock mode, CI |

⭐ **A requirements file comes first.** Before several personas design or review something, write
its requirements with an acceptance test each, and point every persona at that one file.

**The review gate for any change:** two or three of these in parallel, each reviewing the whole
change through its own lens. Collect the findings, deduplicate them, and fix them in one commit.
Then re-review, aiming for two or three waves. Scope the gate to the stakes: a reversible doc gets
one pass; the evaluation harness, anything that spends money, and anything that could corrupt a
result get the full fan-out.

⚠️ **General-purpose personas may also resolve on a machine,** from `~/.claude/agents`: a
requirements analyst, a technical writer, a security engineer and others. Use them for their own
lenses. They are shared across projects, not versioned here, and they may carry another project's
examples, so check what you get.
