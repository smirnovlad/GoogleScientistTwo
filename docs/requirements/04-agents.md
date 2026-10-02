# Requirements 4 · Agents, their names, and the systems they call

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The stage requirements say which agent acts where ([03-stages.md](03-stages.md)); these say what every
agent is, how it is routed to a model, and which outside systems the engine calls [§3] [App. A.2]
[ours]. Each agent's contract, its prompt, schema and failure modes, is task 3's [ours].

### R-AGT-1 · Every agent the paper names is an entry of a roster, which is data

- **Requirement.** The roster lists every agent of `docs/paper/analysis.md` section 7, the 24 stage agents and the 3 integrity agents. Each entry gives a canonical name, a kind, a role, inputs, outputs, a versioned prompt, an output schema, a model route and a tool policy [§3] [App. A.2] [ours]. The kinds are reasoning, judge, planning, coding, writing and search [ours]. N_a is the roster's size, not a parameter, and A_Coder is a composite stage (R-STG-6), not an entry [§3, Eq. 1] [§3.2, Eq. 2] [ours].
- **Traces.** P-ROSTER-1 … 28 [§3.1] [§3.2] [§3.3] [§3.4] [§3.5] [§3.6] [§4.2]; P-CFG-17 [§3, Eq. 1].
- **Why ours.** CLAUDE.md makes behaviour data: a new agent is mostly a prompt and a schema, not a new code path [ours].
- **Depends on.** U-TOP-3, A-SEED-2, task 3: the prompts and schemas, and whether the first idea has an agent of its own [ours].
- **Test.** The roster loads, and each of its 27 entries validates against the entry schema; every agent named by a stage configuration resolves to one entry; in mock mode, a toy agent added as an entry, a prompt and a schema, with no code change, is called by a toy stage [ours].

### R-AGT-2 · Model routing is data, and the default is App. A.2's

- **Requirement.** Each roster entry routes to a provider, a model and, for coding, a backend. The default routes every agent to Gemini 3.6 Flash, except the Idea Experiment Coding Agent, the Ablation Study Agent, the Rebuttal Agent and the Draft Enhancer, which run on Claude Code with Opus 4.8 [App. A.2] [§4.2]. Every call's record names its provider, model and version [ours].
- **Traces.** P-CFG-19 [App. A.2] [§4] [§4.2].
- **Why ours.** Which other coding agents run on Claude Code is open (A-CFG-1); a routing file makes it one line per agent whatever the answer [App. A.2] [§4.2] [ours].
- **Depends on.** A-CFG-1 and U-CFG-1, task 3: the routes App. A.2 leaves open, and the runtime settings [ours].
- **Test.** Loading the default routing gives the routes above; changing one agent's model is a one-line change of the routing file; in mock mode, every call record carries a provider, a model and a version [ours].

### R-AGT-3 · One canonical name per agent; every other name is an alias

- **Requirement.** Every other name the paper gives an agent or a group of agents is an alias in the roster, resolving to one or more canonical agents: Figure 3's boxes, App. A.2's group names, and the generic Coding Agent and Critic Agent. A group name is a name, never a component [Fig. 3] (image) [App. A.2] [§4.2] [ours].
- **Traces.** P-ROSTER-29 … 44 [Fig. 3] (image) [App. A.2] [§4.2].
- **Why ours.** The paper uses one name for two things three times: Peer-Review Agent, Idea Generator and Idea Refiner (A-ROSTER-1) [§1] [Fig. 3] (image) [ours].
- **Depends on.** A-ROSTER-1, task 3: the canonical names [ours].
- **Test.** Each of the 16 names of P-ROSTER-29 … 44 resolves to the agents analysis.md section 7.1 gives it; no canonical name is also an alias of another agent [ours].

### R-AGT-4 · Coding backends sit behind one interface, and swapping one is configuration

- **Requirement.** Every coding session goes through one coding-backend interface. Claude Code with Opus 4.8 is the default backend, and the engine runs end to end through a second backend, selected by configuration alone, as Table 8 runs it with Antigravity [§4.2] [App. A.2] [Tab. 8] [ours].
- **Traces.** P-ROSTER-48 [§4.2] [App. A.2]; P-ROSTER-49 [§4.2] [Tab. 8].
- **Why ours.** The requirement is the swap, not Antigravity itself, whose Gemini version is open (A-CFG-2) and which task 5 may leave out [Tab. 8] [ours].
- **Depends on.** A-CFG-2, task 5 [ours].
- **Test.** In mock mode, the whole run passes through two coding-backend adapters in turn, switched by configuration only, and their stage records match in structure [ours].

### R-AGT-5 · The in-loop reviewer is pinned, and its reviews are kept raw

- **Requirement.** The Peer Reviewer is ScholarPeer, or a rebuild of it, behind a reviewer interface, with its model and version pinned and every raw review kept. It is the reviewer the loop optimises against, so it is never the judge whose numbers are reported (R-MEAS-5) [§3.5] [§4] [ours].
- **Traces.** P-ROSTER-46 [§3.5] [§4]; P-EVAL-7 [§4].
- **Depends on.** U-PEER-3, task 4: whether ScholarPeer can be run, or must be rebuilt [ours].
- **Test.** In mock mode, every review is stored raw, with its score and the reviewer's pinned model and version; the score scale and the threshold are read from configuration [ours].

### R-AGT-6 · Novelty is checked against two retrieved papers, behind a search interface

- **Requirement.** The Novelty Checker reads two reference papers retrieved through a literature-search interface, Google Search by default; each idea's record carries its score, its query and its two references [App. A.2] [§3.1] [ours].
- **Traces.** P-ROSTER-47 [App. A.2]; P-CFG-2 [App. A.2].
- **Depends on.** U-SEED-2, task 3: the score's scale and the query [ours].
- **Test.** In mock mode, with a mock search, every seed idea's record holds a score, a query and exactly two references [ours].

### R-AGT-7 · The drafting system sits behind an interface

- **Requirement.** The Initial Drafter wraps PaperOrchestra, or an equivalent that task 4 chooses, behind a drafting interface, and writes in the ICLR 2025 format [§3.5] [§2] [App. A.2] [ours].
- **Traces.** P-ROSTER-45 [§2] [§3.5].
- **Depends on.** U-DRAFT-1, task 3, the drafter's inputs; task 4's reuse survey, the wrapper [ours].
- **Test.** In mock mode, the mock drafting system's manuscript compiles in the ICLR 2025 template, and swapping the drafting system is a configuration change [ours].

### R-AGT-8 · Each agent's output record holds at least what the artifacts show

- **Requirement.** Each agent's output schema holds at least the fields that its artifact shows, as `docs/paper/artifacts.md` section 5 lists them, and the verdict that §3 gives it, which no artifact prints: d^h, d_abl, s_review or d_meta [pp. 34–55] [§3] [ours].
- **Traces.** P-ART-1 … 8 [pp. 34–55].
- **Why ours.** The paper specifies no output format for any agent, so the artifacts are the only floor (U-TOP-3) [App. C] [ours].
- **Depends on.** U-TOP-3, U-ART-10, U-ART-14 and A-ART-1, task 3: the schemas themselves [ours].
- **Test.** A schema-floor test checks each agent's output schema for the fields of artifacts.md section 5 and its verdict, and fails on a schema with one of them removed; in mock mode, every agent output validates against its schema [ours].

### R-AGT-9 · Every judge has acceptance cases, the paper's own pages first

- **Requirement.** Each agent whose output chooses a branch has a golden set of cases with expected verdicts. The first cases come from the paper [p. 41] [p. 46] [p. 47] [App. B] [ours]:
  - the three boundary cases of the Ablation Critic, TeCh, p. 46 and LC-FTT [App. B] [p. 46] [Tab. 16];
  - p. 41's component table, which a critic must find not clean [p. 41] (image);
  - p. 47's audit, which an auditor must fail, since it skipped the baseline and used no tolerance [p. 47].
- **Traces.** P-ART-3 [pp. 40–42]; P-ART-5 [p. 46]; P-ART-6 [p. 47]; P-ROSTER-18 [§3.4] [App. B].
- **Why ours.** The paper tests agents only end to end, and reports no rate for any verdict (U-TOP-6) [Tab. 5] [Tab. 8] [Fig. 9b] (image) [ours].
- **Decides.** U-ABL-5, its test set [ours].
- **Depends on.** U-TOP-6, task 7: the test strategy that runs these cases [ours].
- **Test.** The golden sets exist, one per judge, each case with its expected verdict; they run against the mock judge in CI, and against the real model on demand, with the result recorded [ours].
