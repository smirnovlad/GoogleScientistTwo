# Requirements 4 · Agents, their names, and the systems they call

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The stage requirements say which agent acts where ([03-stages.md](03-stages.md)); these say what every
agent is, how it is routed to a model, and which outside systems the engine calls [§3] [App. A.2]
[ours]. Each agent's contract, its prompt, schema and failure modes, is task 3's [ours].

### R-AGT-1 · Every agent the paper names is an entry of a roster, which is data

- **Requirement.** The roster lists every agent of `docs/paper/analysis.md` section 7, the 24 stage agents and the 3 integrity agents. Each entry gives a canonical name, a kind, a role, its inputs as references to named objects of the run state, the destination of its output, a versioned prompt, an output schema and its access role (R-OPS-8); the prompts and schemas themselves are task 3's (U-TOP-3) [§3] [App. A.2] [ours]. The kinds are reasoning, judge, planning, coding, writing and search [ours]. N_a is the roster's size, not a parameter, and A_Coder is a composite stage (R-STG-6), not an entry; whether the first idea has an agent of its own is task 3's (A-SEED-2) [§3, Eq. 1] [§3.2, Eq. 2] [ours].
- **Traces.** P-ROSTER-1 … 28 [§3.1] [§3.2] [§3.3] [§3.4] [§3.5] [§3.6] [§4.2]; P-CFG-17 [§3, Eq. 1].
- **Why ours.** CLAUDE.md makes behaviour data: a new agent is mostly a prompt and a schema, not a new code path. An agent whose inputs are assembled in code brings a code path with it (SA-10) [ours].
- **Depends on.** U-TOP-3 and A-SEED-2, task 3 [ours].
- **Test.** Logic: the roster loads, and each of its 27 entries validates against the entry schema; every agent named by a stage configuration resolves to one entry; in mock mode, a toy agent added as an entry, a prompt and a schema, with no code change, reads an existing state object, the traces, and writes its declared record [ours].

### R-AGT-2 · Model routing is data, by stage and agent, and runs on the subscription

- **Requirement.** One routing file routes each agent, and optionally each agent within one stage, to a backend and a model; a stage's rule overrides the agent's default, and each call's record names the rule that matched, with the backend, the model and its version [ours]. Two profiles are kept [App. A.2] [ours]:
  - **subscription**, the default: every agent runs through the Claude subscription (R-OPS-12), coding agents on Claude Code [§4.2] [ours];
  - **paper**: App. A.2's routes, every agent on Gemini 3.6 Flash except the Idea Experiment Coding Agent, the Ablation Study Agent, the Rebuttal Agent and the Draft Enhancer, on Claude Code with Opus 4.8. It is kept as the record of what the paper ran, and R-OPS-12 refuses to start a run with it, since it bills an API [App. A.2] [§4.2] [ours].

  Which agents beyond App. A.2's four run on a coding backend, and the runtime settings, are task 3's (A-CFG-1, U-CFG-1) [ours].
- **Traces.** P-CFG-19 [App. A.2] [§4] [§4.2]; P-ROSTER-33 [Fig. 3] (image); P-ROSTER-35, P-ROSTER-39, P-ROSTER-41 [App. A.2].
- **Departs from.** P-CFG-19: the default profile routes every agent through the Claude subscription, not Gemini [App. A.2] [ours].
- **Why ours.** Vlad will run the engine on his Claude subscription and does not want to pay for an API (DEVELOPMENT_PROCESS.md, 2026-10-02) [ours]. A_FullEng serves three stages, the Result Comparison Agent two and the Novelty Checker three, so a route per agent alone cannot change one stage's model (SA-10) [ours].
- **Depends on.** A-CFG-1 and U-CFG-1, task 3 [ours].
- **Test.** Logic: loading each profile gives the routes above; in mock mode, overriding A_FullEng's model for the meta stage only, by one line of the routing file, changes the model in the next run's META records and leaves its FULL and ABL calls on the default, and every call record names its rule, backend, model and version; a run started with the paper profile is refused before any call, and the message names the routes that would bill an API [ours].

### R-AGT-3 · One canonical name per agent; every other name is an alias

- **Requirement.** Every other name the paper gives an agent or a group of agents is an alias in the roster, resolving to one or more canonical agents: Figure 3's boxes, App. A.2's group names, and the generic Coding Agent and Critic Agent. A group name is a name, never a component; which name is canonical is task 3's (A-ROSTER-1) [Fig. 3] (image) [App. A.2] [§4.2] [ours].
- **Traces.** P-ROSTER-29 … 44 [Fig. 3] (image) [App. A.2] [§4.2].
- **Why ours.** The paper uses one name for two things three times: Peer-Review Agent, Idea Generator and Idea Refiner (A-ROSTER-1) [§1] [Fig. 3] (image) [ours]. A group name that carries a decision also traces to the requirement that makes it, such as App. A.2's routing groups to R-AGT-2 [ours].
- **Depends on.** A-ROSTER-1, task 3 [ours].
- **Test.** Logic: each of the 16 names of P-ROSTER-29 … 44 resolves to the agents analysis.md section 7.1 gives it; no canonical name is also an alias of another agent [ours].

### R-AGT-4 · Coding backends sit behind one interface, and swapping one is configuration

- **Requirement.** Every coding session goes through one coding-backend interface. Claude Code, run through the subscription, is the default backend, and the engine runs end to end through a second backend selected by configuration alone, as Table 8 runs it with Antigravity [§4.2] [App. A.2] [Tab. 8] [ours]. Stage configurations and roster entries hold engine-level session settings only; a backend's own settings, its tools, permissions and turn limits, live in its adapter's configuration (U-CFG-1). Which second backend runs for real is task 5's (A-CFG-2) [ours].
- **Traces.** P-ROSTER-48 [§4.2] [App. A.2]; P-ROSTER-49 [§4.2] [Tab. 8].
- **Why ours.** The requirement is the swap, not Antigravity itself, whose Gemini version is open (A-CFG-2); a backend setting that leaks into stage data makes every stage a part of the next swap (SA-10) [Tab. 8] [ours].
- **Depends on.** A-CFG-2, task 5; U-CFG-1, task 3 [ours].
- **Test.** Logic, in mock mode: the whole run passes through two coding-backend adapters in turn, switched by configuration only, and their stage records match in structure; a static check finds no backend-specific key outside the adapters' own configuration [ours].

### R-AGT-5 · The in-loop reviewer sits behind a contract, pinned, its reviews kept raw

- **Requirement.** The Peer Reviewer is reached through a reviewer contract: a score on a declared scale, comments, the model and its version, the rubric, and the raw response. Task 4 chooses what fills it (U-PEER-3). The threshold is stored with the reviewer's version and derived by a recorded calibration rule, which is task 6's (A-EVAL-3). It is the reviewer the loop optimises against, so its numbers are reported only as in-distribution, never as the held-out judge's (R-MEAS-5, R-MEAS-6) [§3.5] [§4] [ours].
- **Traces.** P-ROSTER-21 [§3.5]; P-ROSTER-46 [§3.5] [§4]; P-EVAL-7 [§4].
- **Departs from.** P-ROSTER-21 and P-ROSTER-46: task 4 found no published implementation of ScholarPeer, and every agent runs on the subscription, so the in-loop reviewer is a stand-in behind ScholarPeer's place; if task 4 finds ScholarPeer runnable on the subscription, it fills the contract and this departure is removed [§3.5] [ours].
- **Why ours.** A score of 8 means something only on the scale it was calibrated on, and the paper's acceptance rates cannot come from a rating of 8 or more (A-EVAL-3) [Tab. 3] [ours].
- **Depends on.** U-PEER-3, task 4; A-EVAL-3, task 6 [ours].
- **Test.** Logic, in mock mode: every review is stored raw, with its score, scale and the reviewer's pinned model and version; the threshold is read from the reviewer's configuration with its calibration record; a second mock reviewer, swapped in by configuration, runs the review stage unchanged; the report labels every in-loop score as in-distribution [ours].

### R-AGT-6 · Novelty is checked against two retrieved papers, behind a search interface

- **Requirement.** The Novelty Checker reads two reference papers retrieved through a literature-search interface; App. A.2 uses Google Search, and the adapter meets R-OPS-12. Retrieval excludes G's own paper and its versions; each idea's record carries its score, its query, and its two references with their dates; a score that cannot be computed is recorded as unknown, never as zero. No date cut-off applies, and the recorded dates let one be applied later. The score's scale and the query are task 3's (U-SEED-2) [App. A.2] [§3.1] [ours].
- **Traces.** P-ROSTER-47 [App. A.2]; P-CFG-2 [App. A.2].
- **Why ours.** G's own paper would make every idea look unoriginal or derivative of itself, and a missing score read as zero would rank an idea as the least novel (MISS-24, MISS-25) [ours].
- **Depends on.** U-SEED-2, task 3 [ours].
- **Test.** Logic, in mock mode, with a mock search: every seed idea's record holds a score, a query and exactly two references, each with a date, none of them G's paper; a search scripted to fail gives a score recorded as unknown [ours].

### R-AGT-7 · The drafting system sits behind an interface

- **Requirement.** The Initial Drafter wraps PaperOrchestra, or an equivalent that task 4 chooses, behind a drafting interface, and writes in the ICLR 2025 format; what it reads is task 3's (U-DRAFT-1) [§3.5] [§2] [App. A.2] [ours].
- **Traces.** P-ROSTER-45 [§2] [§3.5].
- **Why ours.** The reuse survey recommends trying PaperOrchestra behind our own contract, with only verified results in its input [ours].
- **Depends on.** U-DRAFT-1, task 3 [ours].
- **Test.** Logic, in mock mode: the mock drafting system's manuscript compiles in the ICLR 2025 template; after the drafting system is swapped by a configuration change, the next run's records name the new system, for the drafter only [ours].

### R-AGT-8 · Each agent's output record holds at least what the artifacts show

- **Requirement.** Each agent's output schema holds at least the fields that its artifact shows, as `docs/paper/artifacts.md` section 5 lists them, and the verdict that §3 gives it, which no artifact prints: d^h, d_abl, s_review or d_meta. The schemas themselves are task 3's (U-TOP-3, U-ART-10, U-ART-14), and so is which critic wrote App. C's page of feedback (A-ART-1) [pp. 34–55] [§3] [ours].
- **Traces.** P-ART-1 … 8 [pp. 34–55]; P-ROSTER-44 [Fig. 3] (image) [App. C].
- **Why ours.** The paper specifies no output format for any agent, so the artifacts are the only floor (U-TOP-3) [App. C] [ours].
- **Depends on.** U-TOP-3, U-ART-10, U-ART-14 and A-ART-1, task 3 [ours].
- **Test.** Logic: a schema-floor test checks each agent's output schema for the fields of artifacts.md section 5 and its verdict, and fails on a schema with one of them removed; in mock mode, every agent output validates against its schema [ours].

### R-AGT-9 · Every agent has acceptance cases, and every judge a pass rule

- **Requirement.** Each agent has acceptance cases; each agent whose output chooses a branch has a golden set of cases with expected verdicts and a pass rule. The first cases come from the paper [p. 41] [p. 46] [p. 47] [App. B] [ours]:
  - the three boundary cases of the Ablation Critic, TeCh, p. 46 and LC-FTT [App. B] [p. 46] [Tab. 16];
  - p. 41's component table, which a critic must find not clean [p. 41] (image);
  - p. 47's audit, which an auditor must fail, since it skipped the baseline and used no tolerance [p. 47].

  Each case has a twin that adds text addressed to the judge, in a comment, a log line or a report, and the two verdicts must agree [ours]. A judge's pass rate on its set, with its n, date and exact prompt and model, is recorded with every reported run; the threshold that gates a run, and how the sets run, are task 7's (U-TOP-6). The integrity checks' sets are task 6's planted corpus (IR-31; A-INT-3) [ours].
- **Traces.** P-ART-3 [pp. 40–42]; P-ART-5 [p. 46]; P-ART-6 [p. 47]; P-ROSTER-18 [§3.4] [App. B].
- **Why ours.** The paper tests agents only end to end, and reports no rate for any verdict (U-TOP-6) [Tab. 5] [Tab. 8] [Fig. 9b] (image). A scripted mock passes its own set by construction, and text addressed to a judge can flip a verdict while its reason echoes the text (SA-11, EI-11) [ours].
- **Decides.** U-ABL-5, its test set [ours].
- **Depends on.** U-TOP-6, task 7; A-INT-3, task 6 [ours].
- **Test.** Logic: the golden sets exist, one per judge, each case with its expected verdict and its twin; in mock mode the sets run, and the mock run checks only that they run. Against the real model, on demand: each judge's pass rate is recorded with its n, date, prompt hash and model, and a judge whose prompt is weakened on purpose scores below its unweakened twin [ours].
