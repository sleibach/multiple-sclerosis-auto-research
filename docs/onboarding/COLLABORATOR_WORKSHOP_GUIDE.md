# Collaborator Workshop: From Fresh Perspective To Testable Direction

This guide runs a structured session with smart contributors who do not need a
medical background. The output is a set of research-direction drafts the
project can evaluate, not new scientific findings.

## What The Session Is For

By the end, each participant should be able to:

1. State the project's honest frontier: one provisional monitoring lead, no
   intervention-grade target, and no established progression result.
   `[M01, M05, P02]`
2. Distinguish a fresh question from a scientific claim.
3. Name a prediction, reachable data, comparator or null, correction, and drop
   rule.
4. Identify which known dead end the idea avoids.
5. Submit the result through the research-direction issue template.

The session does not seek a vote on what is true. Agreement among participants
does not become evidence.

## Recommended Format

- **Length:** 75 minutes.
- **Group:** 3-8 contributors plus one facilitator.
- **Background:** mixed disciplines are preferred.
- **Mode:** shared screen plus individual writing space.
- **Output:** one to three issue-template-ready directions.

For a shorter session, use the 45-minute variant below.

## Before The Session

Send these four links:

1. [Two-minute project explanation](MS_RESEARCH_EXPLAINED.md#the-two-minute-version)
2. [Research map](visuals/RESEARCH_MAP_V55.svg)
3. [Four-case learning path](CASE_STUDY_LEARNING_PATH.md#ten-minutes)
4. [Open-problem board](OPEN_PROBLEMS_FOR_COLLABORATORS.md#pick-a-puzzle)

Ask participants to bring:

- one method, system, or failure pattern from their own field;
- one question they found confusing; and
- no patient-identifiable or access-restricted data.

## Non-Negotiable Safety And Evidence Rules

Read these aloud at the start:

- This is research design, not medical advice.
- Do not share identifiable patient information, secrets, credentials, or data
  whose use terms are unknown.
- Project-grounded, provisional, negative, data-blocked, and outside-context
  material keep their labels. `[E01-E02]`
- Literature, databases, and model suggestions can motivate a test but cannot
  become a project conclusion merely through discussion.
- Claude, Gemini, RPT, and other models can help phrase or challenge an idea;
  their agreement is not evidence. `[E03]`
- Closed routes may reopen only with the specific missing evidence, not with a
  more enthusiastic version of the same argument.
- A null, invalid package, or decision to stop is an acceptable designed
  outcome.

## The 75-Minute Agenda

### 0-8 Minutes: Establish The Frontier

Show the [research map](visuals/RESEARCH_MAP_V55.svg) with its
[text equivalent](VISUAL_INDEX.md#1-the-research-terrain).

Facilitator script:

> The live clinical route is a provisional early-treatment monitor awaiting an
> outside test. It is not a target or clinical tool. The genetics routes did not
> produce an intervention-grade target. Progression remains blocked by the
> missing longitudinal molecular-to-confirmed-disability design. Today we are
> looking for better questions and tests, not declaring answers.

Ask one check question: **What has the project not achieved?**

Expected answer: no validated clinical monitor, no intervention-grade target,
and no progression mechanism or halt strategy. `[M01, P02]`

### 8-18 Minutes: Choose One Inference Lesson

Assign or let the group choose one case:

- source and diagnosis entanglement;
- real locus versus actionable target;
- predictive monitor versus causal control point; or
- snapshot versus progression movie.

Use the [four-case learning path](CASE_STUDY_LEARNING_PATH.md). Ask:

1. What was the attractive shortcut?
2. Which comparison or evidence link was missing?
3. What new design would create it?

Do not spend this segment proposing mechanisms.

### 18-30 Minutes: Silent Divergent Generation

Each participant writes three directions independently. Silence matters: it
reduces anchoring on the first confident speaker.

Use prompts such as:

- What method from your field detects a failure mode earlier?
- What data linkage would make an unidentifiable question identifiable?
- What invariant, negative control, or adversarial case would expose a false
  pattern?
- How would you design a restoration/up-function intervention rather than
  default inhibition?
- How would you preserve uncertainty in a small-cohort decision?
- What would make a coupled system controllable without assuming one magic
  node?

Ideas may be unusual. They do not need to be biologically correct yet. They do
need a path to grounding.

### 30-42 Minutes: Boundary Filter

For each direction, answer five questions:

1. Does it repeat a documented closed route?
2. Is it asking monitoring, mechanism, target, utility, or progression?
3. Does the proposed data match that verb?
4. Is the idea internally testable or dependent on named external data?
5. What result would make the group drop it?

Move any idea that cannot answer question 5 into a repair pile. Do not discard
it; rewrite it until failure is possible.

### 42-60 Minutes: Build The Fair Test

Complete one card per surviving idea:

```text
Problem and current boundary:
Proposed direction, not conclusion:
Exact prediction:
Independent unit:
Required data and access status:
Comparator / negative control:
Null or permutation scheme:
Holdout or cross-validation:
Confounders and multiplicity:
Precommitted drop / narrow rule:
Known dead end avoided:
Decision changed if supported:
What the result still would not establish:
```

Use the [confound quick reference](CONFOUND_CHECK_QUICK_REFERENCE.md),
[null/boundary guide](HOW_TO_READ_NULLS_AND_BOUNDARIES.md), and
[idea triage rubric](IDEA_TRIAGE_RUBRIC.md).

### 60-70 Minutes: Adversarial Swap

Exchange cards. The reviewer must name:

- the strongest competing explanation;
- one missing field or comparison;
- one way the test could overfit;
- one status inflation in the proposed interpretation; and
- the single cheapest discriminating test.

The author revises the card. Review is successful when it makes the decision
rule sharper, even if it makes the idea less exciting.

### 70-75 Minutes: Route The Output

Classify each card:

- ready for a research-direction issue;
- repairable with named missing fields;
- needs external data or permission;
- overlaps active work;
- duplicates a closed route; or
- out of scope or unsafe.

Submit only the first category. Record the others so the same ambiguity is not
repeated later.

## The 45-Minute Variant

1. Frontier and rules: 5 minutes.
2. One case correction: 5 minutes.
3. Silent generation: 8 minutes.
4. Boundary filter: 7 minutes.
5. Fair-test card: 12 minutes.
6. Adversarial swap and route: 8 minutes.

Do not shorten by removing the drop rule, confounder plan, or adversarial
review. Reduce the number of ideas instead.

## Discipline-Specific Starting Prompts

| background | useful starting question |
|---|---|
| Software/testing | Which scientific claims need fail-closed input contracts or metamorphic tests? |
| Causal inference | Which required overlap, timing, or negative control is absent? |
| Control systems | Which state is observable, controllable, and reachable under constrained input? |
| Reliability/safety | What failure mode produces a plausible but wrong pass? |
| Human factors | How could a monitor communicate uncertainty without becoming an automatic treatment command? |
| Data engineering | Which join or provenance field is needed before the intended comparison exists? |
| Security/adversarial modeling | How would leakage, source fingerprinting, or adaptive search imitate biological signal? |
| Design/visualization | Which mental model causes newcomers to confuse observation, cause, target, and utility? |
| Statistics | What small-sample null and multiplicity family matches the actual search? |
| Operations | Which acquisition bottleneck can be converted into an exact, low-friction data request? |

These are prompts, not conclusions. A familiar method still needs a concrete
prediction and eligible data.

## Facilitator Interventions

Use these when discussion drifts:

| drift | intervention |
|---|---|
| “This pathway is important, so target it.” | Which causal node and protective direction does the held evidence support? |
| “The model agrees.” | What real-data test would distinguish the proposal from its strongest alternative? |
| “We can infer progression from stage.” | Where are the earlier molecular measure and later confirmed disability? |
| “The cohort is small, so tune the threshold.” | Which decision was frozen before labels, and what result is inconclusive? |
| “Adjust for batch and continue.” | Is there outcome overlap within batch/source, or is the effect unidentifiable? |
| “A negative wastes the session.” | Which decision or resource does the scoped negative save? |
| “Let us collect every possible variable.” | Which minimum field changes eligibility or the causal comparison? |

## Output Quality Check

A card is ready only if a reviewer can answer **yes** to all:

- The current project boundary is stated accurately.
- The idea is labeled as a proposal.
- One prediction and one failure condition are explicit.
- Data identity and access are concrete.
- The independent unit is correct.
- Comparator/null and holdout are named.
- Confounding and multiplicity are addressed.
- Known closed routes are acknowledged.
- The decision consequence is bounded.
- No patient data, secret, or unsupported scientific claim appears.

## After The Session

1. Follow the [submission checklist](HOW_TO_CONTRIBUTE_IDEAS.md#before-you-submit)
   and open a research-direction issue.
2. Link the relevant onboarding claim IDs and controlling artifacts.
3. Mark external data, permission, or literature dependencies explicitly.
4. Let project triage return **ground now**, **repair**, **data request**,
   **park**, or **close** without treating only the first as success.
5. Update the idea if a harder source or test changes its scope.

The workshop succeeds when it produces clearer discriminating tests, not when
it produces the largest number of ideas.
