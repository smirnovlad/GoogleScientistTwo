# Requirements 2 · The stage primitive

Part of [requirements.md](../requirements.md), whose section *How to read* defines the fields [ours].
The paper abstracts every stage with one pseudocode, Listing 1, and task 1 concluded that every way a
stage departs from it is a parameter value of one primitive (`docs/paper/analysis.md` sections 3.4
and 3.5) [§3] [Lst. 1] [ours]. These requirements state what that primitive must do and express;
[03-stages.md](03-stages.md) gives each stage's values as data [ours]. How its parameters are cut,
and how it is built, is task 3's (A-NOTE-1) [ours].

### R-PRIM-1 · Every stage, A_Coder, the tail and the run's sequence are configurations of one primitive

- **Requirement.** Each of Table 1's eleven stages, the unified coder A_Coder, the run's tail and the run's sequence run through one generic primitive, each with a configuration that is data. No stage has code of its own: a new stage, or a changed limit, verdict, at-limit value or place in the sequence, is a change of data only [§3] [Tab. 1] [§3.2, Eq. 2] [ours]. How the primitive is built is task 3's (A-NOTE-1) [ours].
- **Traces.** P-TOP-3 [Tab. 1] [§3].
- **Why ours.** The paper claims the abstraction, and analysis.md section 3.5 shows that it holds once the behaviours of R-PRIM-2 exist; CLAUDE.md makes behaviour data, run by generic code [§3] [ours]. A test of one toy stage would pass beside eleven hand-written loops, so the test reaches every stage (the architect's review, SA-11) [ours].
- **Depends on.** A-NOTE-1, task 3, which designs the primitive as a component [ours].
- **Test.** Logic, in mock mode: one conformance test, with no stage-specific test code, loads every stage of the default configuration, A_Coder, the tail and the run's sequence from data, and runs each through the one primitive [ours]:
  - each stage's recorded calls match what its configuration implies [ours];
  - changing a stage's limit, verdict map or at-limit value in data changes its recorded calls, with no code change [ours];
  - a static check finds no stage key (LIM, SEED, BASE, SUB, FULL, EVO, SEL, ABL, DRAFT, PEER, META, TAIL) in engine code outside its configuration files [ours].

### R-PRIM-2 · What the primitive must be able to express

- **Requirement.** A stage configuration can express at least the behaviours below. This is a floor, and how the parameters are cut is task 3's (A-NOTE-1) [Tab. 1] [ours]:
  - a generator that is one agent, a deterministic operation, a sequence of steps, or another stage; the top N_0 seeds and the next unevaluated seed are deterministic operations over the sorted pool [§3.1] [§3.3] [§3.4] [§3.5];
  - a fan-out over the items of a previous step, such as one coding session per ablation plan or per rebuttal task [§3.4] [§3.5];
  - the judged object and the refiner, each bound to named objects of the run state, so that a guarded stage keeps the run's core state, never a copy of its own [§3.4] [§3.6] [ours];
  - an assessor of one kind: an LLM verdict; a score against a threshold; a score with no verdict; a deterministic check; a choice among options; or a nested stage, A_Coder, whose outcomes are aggregated [§3.1] [§3.3] [§3.5] [Tab. 1] [ours];
  - a deterministic precondition over the harness's records (U-INT-4), which an LLM's accept must pass and which narrows the options a choice may pick, so that the LLM can only be stricter than the numbers (task 6's IR-7) [ours];
  - a verdict map onto accept, refine and reject, and an aggregation of a fan-out's outcomes, such as a count of `Good` [Lst. 1] [§3.2] [§3.3];
  - an update that replaces the candidate, or appends to a population [§3.1] [§3.3];
  - an optional guard, with its failure branch (R-PRIM-5) [§3.4] [§3.6];
  - a limit: what it counts, its value, and its scope, per invocation by default (R-PRIM-3) [App. A.2] [ours];
  - stop tests: a count stop, a round limit, and the point at which each is tested [§3.1] [§3.3];
  - an at-limit value (R-PRIM-4) [Lst. 1] [§3.5];
  - hook points, declared by the kind of step, at which the cross-cutting checks run (R-INT-10) [§4.2] [ours];
  - for a stage that can end the run, the outcome it declares (R-RUN-5) [ours].
- **Traces.** P-TOP-2 [Lst. 1]; P-TOP-3 [Tab. 1]; P-SEED-3 [§3.1]; P-EVO-2, P-EVO-3, P-EVO-5 [§3.3].
- **Why ours.** The split into parameters is task 1's reading (analysis.md section 3.4). The first draft closed these lists, and the architect's review showed that they could not hold the draft's own stage table: the idea rounds, the vetoes, the Selector's choice, A_Coder, and the plan-then-execute steps of ablation and rebuttal (SA-1) [§3.3] [§3.4] [§3.5] [ours]. Listing 1 is one configuration: a critic that reads only the candidate, three verdicts, no guard, a limit on critic calls, and discard at the limit [Lst. 1] [ours].
- **Depends on.** A-NOTE-1, task 3; U-INT-4, task 6, the records a precondition reads [ours].
- **Test.** Logic, in mock mode: each behaviour above has a toy configuration and a scripted run whose recorded calls it predicts, all under the same test code [ours]. With Listing 1's own values and a scripted critic [Lst. 1] [ours]:
  - an accept on the first call returns the candidate [ours];
  - a reject returns nothing [ours];
  - a critic that always asks for refinement makes `max_rounds` critic calls and `max_rounds` refinements, the last one never judged, and returns nothing [ours].

### R-PRIM-3 · A limit counts judged refinements

- **Requirement.** In every default stage configuration, a limit N counts refinements, and every refinement is judged: a stage makes at most N refinements and N + 1 assessor calls, and the verdict on the last refinement applies. The limitation stage's N is 15, since App. A.2's 16 rounds of extraction include the first (R-STG-1). Listing 1's convention, a limit on critic calls, stays available as a value, and no default stage uses it [Lst. 1] [App. A.2] [ours].
- **Traces.** P-TOP-2 [Lst. 1]; P-LIM-4 [§3.1]; P-SUB-4 [§3.2]; P-ABL-6 [§3.4]; P-PEER-6 [§3.5]; P-META-7 [§3.6].
- **Why ours.** App. A.2 states three of its limits as refinements, Table 5 counts review rounds 0, 1 and 2 under a limit of 2, and Figure 9 counts four rounds after the initial one; under Listing 1's convention the last refinement is made and never judged [App. A.2] [Tab. 5] [Fig. 9] (image) [Lst. 1] [ours]. App. A.2 counts its limitation rounds with the first included, and no table or figure places a round 0 outside that count (SA-14) [App. A.2] [ours].
- **Decides.** A-TOP-2 [ours].
- **Test.** Logic, in mock mode: an assessor scripted to ask for refinement every time, under a limit of 2, gives 2 refinements, 3 assessor calls, and the third verdict decides; under a limit of 0, 1 assessor call and no refinement [ours].

### R-PRIM-4 · What a stage keeps at its limit is one value per stage

- **Requirement.** The at-limit value is one of these, set per stage in [03-stages.md](03-stages.md) [Lst. 1] [§3.3] [§3.5] [ours]:
  - discard: nothing passes on, as Listing 1 does [Lst. 1];
  - keep the last candidate, flagged as having reached the limit [§3.5];
  - keep the current best, the candidate the guard last accepted [§3.4] [§3.6];
  - keep the accepted items of a population, and stop the run when there are none [§3.3];
  - stop the run, with the outcome the stage declares [ours].
- **Traces.** P-TOP-2 [Lst. 1]; P-SUB-4 [§3.2]; P-EVO-6 [§3.3]; P-PEER-6 [§3.5]; P-META-7 [§3.6].
- **Why ours.** Listing 1 discards at the limit, §3.5 keeps the last manuscript, §3.4 and §3.6 imply keeping (the register's D-5), and §3.3 goes on with the successful ideas; one value per stage settles it, last or best included [Lst. 1] [§3.3] [§3.4] [§3.5] [§3.6] [ours].
- **Decides.** A-TOP-1, with its aliases U-TOP-7, A-LIM-1 and U-ABL-4 [ours].
- **Test.** Logic, in mock mode, one scripted stage per value, each run to its limit [ours]:
  - discard: no candidate passes on [ours];
  - keep the last: the last refinement passes on, flagged [ours];
  - keep the current best: the guard's last accepted candidate passes on, not the last refinement [ours];
  - keep the accepted items: the population's accepted items pass on, and with none the run ends with the declared outcome [ours];
  - stop the run: the run ends with the declared outcome [ours].

### R-PRIM-5 · A guarded refinement replaces the kept candidate only when the guard accepts it

- **Requirement.** In a guarded stage, a refinement replaces the kept candidate, and the stage runs its generator again on it, only when the guard accepts the refinement; otherwise the kept candidate stays and the stage's failure branch runs [§3.4] [§3.6].
- **Traces.** P-ABL-5 [§3.4]; P-META-4, P-META-5, P-META-6 [§3.6]; P-STATE-9 [§3.4].
- **Test.** Logic, in mock mode: a guard scripted to accept replaces the core state, and the stage's generator runs again on the new candidate; scripted to reject, the core state is unchanged, and the configured failure branch runs [ours].

### R-PRIM-6 · The guard's rule is deterministic, over the harness's records

- **Requirement.** A guard decides by its entry of the task's comparison rule (R-RUN-6), over search-role records that the harness wrote (U-INT-4, U-TOP-5): the new result must beat the kept one beyond the entry's margin, and a tie keeps the kept one. The Result Comparison Agent still runs; its reading is recorded beside the rule's result and never decides [§3.4] [§3.6] [ours].
- **Traces.** P-ABL-5 [§3.4]; P-META-4 [§3.6]; P-ROSTER-19 [§3.4] [§3.6].
- **Departs from.** P-ABL-5, P-META-4 and P-ROSTER-19: the agent's preference no longer decides [§3.4] [§3.6] [ours].
- **Why ours.** §3.4 says both "strictly outperforms" and preferred by the agent, and results span several datasets and metrics [§3.4] (tex:sections/3_new_method.tex:111-112); CLAUDE.md requires gains computed deterministically from result files [ours].
- **Decides.** A-ABL-3 [ours].
- **Depends on.** U-INT-4 and U-TOP-5, task 6: the harness and the role the rule reads [ours].
- **Test.** Logic, with fixture result records: a new result better beyond the margin replaces the kept one; one within the margin does not; an agent scripted to prefer the new result while the rule keeps the old one leaves the old one, and the record shows both readings [ours].

### R-PRIM-7 · Assessors and verdict vocabularies are data

- **Requirement.** Each stage's assessor kind, from the list of R-PRIM-2, its rule, its precondition and its verdict words are configuration [§3.1] [§3.2] [§3.3, Eq. 4] [§3.4] [§3.5] [§3.6] [ours].
- **Traces.** P-LIM-2 [§3.1]; P-SEED-2 [§3.1]; P-SUB-2 [§3.2]; P-FULL-3 [§3.2]; P-SEL-1 [§3.3, Eq. 4]; P-ABL-3 [§3.4]; P-PEER-2 [§3.5]; P-META-1 [§3.6].
- **Test.** Logic, in mock mode: a threshold assessor at 8 maps a score of 7.9 to refine and 8.0 to accept; a score-only assessor ranks its candidates and emits no verdict; renaming a verdict in the configuration renames it in the record, with no code change [ours].

### R-PRIM-8 · Stages nest and fan out, and the result does not depend on completion order

- **Requirement.** Any role of a stage can be another stage configuration, and a stage can fan out over independent items: the candidates of a round, the ablation plans, the rebuttal tasks. Items may run in parallel, which is task 3's to decide (U-TOP-4), and neither the stage's result nor the order in which its outcomes enter the traces depends on the order in which they finish [§3.2, Eq. 2] [§3.3, Eq. 3] [§3.4] [§3.5] [§3.6] [ours].
- **Traces.** P-CODER-1 [§3.2, Eq. 2]; P-EVO-4 [§3.3, Eq. 3]; P-ABL-1, P-ABL-2 [§3.4]; P-PEER-3, P-PEER-4 [§3.5]; P-META-5 [§3.6].
- **Depends on.** U-TOP-4, task 3: what runs in parallel [ours].
- **Test.** Logic, in mock mode [ours]:
  - A_Coder nested in the idea rounds' fan-out, and the downstream pass nested in the meta stage, both from data, give the call counts of R-STG-7 and R-STG-12 [ours];
  - a fan-out of three items, run twice with the items finishing in two different orders, gives identical stage records apart from timestamps, and identical traces and inputs for A_Evolve [ours].

### R-PRIM-9 · Every stage leaves records from which its run can be re-executed

- **Requirement.** Each stage records, in the one record per unit of work (R-OPS-5), whose format is task 3's (U-ART-10) [ours]:
  - every verdict with its feedback, and every refinement [ours];
  - every guard decision, with the rule's result and the agent's reading [ours];
  - the counters, and the at-limit value if it applied [ours];
  - every skipped step, with its reason [ours].

  A mock that answers every agent call from these records re-executes the run [§3] [ours].
- **Traces.** P-TOP-4 [§3].
- **Why ours.** No page of Appendices C and D prints a verdict from §3's vocabulary, so the paper's own runs cannot be replayed [pp. 34–71] [ours]. Rebuilding a sequence from records that list it would prove nothing, so the test re-executes (SA-11) [ours].
- **Depends on.** U-ART-10, task 3: the record's format and the run layout [ours].
- **Test.** Logic: re-executing a mock run with a mock that answers each agent call from the run's records gives the same stage records, and no call goes unanswered [ours].

### R-PRIM-10 · Every step fails closed

- **Requirement.** Every step has a failure branch for an agent error, a timeout, an empty output, an output outside its schema or vocabulary, and an outage of a tool. It retries under the policy of R-OPS-7, whose values are task 3's (U-TOP-2), then maps onto the primitive's own outcomes, per role, as data [§3] [ours]:
  - drop the item, for one ablation plan or one rebuttal task, after one re-run by a fresh session; the dropped item and its reason stay in what the next judge reads (R-STG-9) [ours];
  - reject the candidate, for an idea, which becomes `Bad` with the reason *error* [ours];
  - stop the run with *error after retries*, for the baseline, the selection or the draft [ours].

  An assessor's output that cannot be parsed is a failed attempt, and never maps to accept or `Good` [ours].
- **Traces.** none.
- **Why ours.** Every stage file of the analysis reads *On failure: UNSPECIFIED* (U-TOP-2). A judge that defaulted to accept on a malformed answer would pass any candidate, and one crashing ablation session would otherwise end a run that already has its idea (SA-5); an item that silently disappears can hide an inconvenient ablation (EI-7) [§3] [ours].
- **Depends on.** U-TOP-2, task 3: the retry policy and its values [ours].
- **Test.** Logic, in mock mode [ours]:
  - an ablation session scripted to fail every time is re-run once, then dropped, and the Ablation Critic's recorded input lists it with its reason [ours];
  - a critic scripted to answer an unknown word, `Good!!`, or nothing is retried, then takes its configured branch, and is never read as accept [ours];
  - each fault above, injected at each kind of step, ends in its recorded outcome, and the run never hangs [ours].
