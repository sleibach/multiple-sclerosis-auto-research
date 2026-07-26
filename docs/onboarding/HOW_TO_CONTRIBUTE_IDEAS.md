# How To Contribute Research-Direction Ideas

You do not need medical credentials to contribute a useful direction. You do
need to make the idea testable enough that the project can distinguish it from
a persuasive story.

This guide is for research directions, methods, data leads, analytical
reframes, and falsification tests. It is not a route for medical advice or
patient-specific treatment recommendations.

## The Fast On-Ramp

1. Read the [two-minute explanation](MS_RESEARCH_EXPLAINED.md#the-two-minute-version).
2. Scan the [research terrain](visuals/RESEARCH_MAP_V55.svg) so you do not
   accidentally reopen a closed path.
3. Choose one of the eight
   [open collaborator problems](OPEN_PROBLEMS_FOR_COLLABORATORS.md#pick-a-puzzle).
4. Read that problem's “already tried” and “known non-solutions” sections.
5. Fill in the idea template below. A concise, falsifiable idea is better than
   a long review.

## Know Which Kind Of Statement You Are Making

The repository keeps evidence types separate. The
[evidence-lanes visual](visuals/EVIDENCE_LANES_V55.svg) is the shortest guide.

| your input | how it enters the project |
|---|---|
| A method from another field | A proposal until it makes a concrete prediction and survives a data test. |
| A paper or database claim | Outside-source context with a citation; never project evidence merely because it is published. |
| An AI-model suggestion | A question-generating proposal; model confidence or agreement has no evidentiary weight. |
| A dataset lead | An access candidate until pairing, labels, genes, subject mapping, and provenance are verified. |
| A rerunnable analysis or code change | Method work until its output passes the relevant null, holdout, correction, and interpretation gate. |
| A negative result | Valuable when the test was specified fairly and its scope is stated. |

The formal policy lives in
[EPISTEMIC_CLASSES.md](../knowledge/EPISTEMIC_CLASSES.md). The practical rule is:
**ideas choose what to test; data decide what the project can say.** `[E01-E03]`

## Copy-Ready Idea Template

Paste this into a GitHub issue or pull-request description. Delete prompts in
parentheses, but do not delete the fields.

```markdown
# Direction: <short, neutral title>

## Problem
- Open-problem number: <1-8>
- Existing claim IDs: <for example M04, C02>
- Current boundary this addresses: <one sentence>

## Proposal
- Method, mechanism, dataset, or reframe: <one paragraph>
- Why it is not a known closed path: <name the distinction>
- Assumptions: <what must be true for this to work>

## Falsifiable prediction
- If the idea is useful, we should observe: <specific observable result>
- A competing explanation predicts: <different observable result>
- We should drop the idea if: <precommitted failure condition>

## Data and access
- Required data fields: <samples, time, outcomes, covariates, modality>
- Unit of analysis: <person, sample, gene, site, etc.>
- Data location or access path: <verified URL/accession/holder, if known>
- Is the required data actually reachable? <yes/no/unknown and why>
- Any use restrictions or privacy constraints: <state explicitly>

## Test design
- Primary estimand or score: <one definition>
- Null or negative control: <what chance/confounding looks like>
- Holdout unit: <person, cohort, site, modality, or other>
- Multiple-testing budget: <number of planned tests and correction>
- Small-sample plan: <uncertainty/CV/permutation strategy>
- Confounders and source/batch checks: <fixed before outcome inspection>

## Decision consequence
- If supported: <the next bounded step, not a larger claim>
- If not supported: <what closes or changes>
- If inconclusive: <what estimate or data requirement remains useful>

## Provenance
- Sources used for context: <citation/URL/date accessed>
- Code or artifact to reproduce the test: <path or proposed location>
- No medical or intervention claim is made: <yes>
```

## What Makes An Idea High Value?

An idea gets attention faster when it has all of these properties:

| property | strong version | weak version |
|---|---|---|
| **Specific** | Names one current boundary and one changed prediction. | “Study inflammation more.” |
| **Discriminating** | Competing explanations predict different outcomes. | Every possible outcome is called support. |
| **Groundable** | Required fields and a reachable data path are named. | Depends on unspecified future data. |
| **Error-aware** | Null, holdout, multiplicity, confounding, and small-n behavior are explicit. | Reports only a fitted association. |
| **Direction-aware** | Therapeutic sign, cell/state, and modality match are addressed. | Names a bindable protein as a target. |
| **Decision-relevant** | A null changes what the project should do. | Failure simply triggers another version of the same idea. |
| **Non-duplicative** | Explains why it differs from a documented closed route. | Repeats a lead without addressing why it closed. |

## Common Contribution Types

### A Method From Another Field

Explain the method without assuming its vocabulary is familiar. Then identify
the exact held or incoming table it would consume, the prediction it makes, and
the null comparison. A method is not valuable here merely because it is novel;
it must change a decision under a fair test.

Examples of potentially useful families, not endorsed findings, include system
identification, information-value analysis, informative-missingness methods,
domain-shift diagnostics, privacy-preserving validation, and failure-safe human
interfaces. See the [problem board](OPEN_PROBLEMS_FOR_COLLABORATORS.md) for the
specific boundaries they might address.

### A Dataset Lead

Do not submit only a title or repository search result. Verify as many of these
as possible:

- disease and treatment;
- baseline and follow-up timepoints;
- whether the same people are paired;
- exact response or confirmed-disability outcome;
- sample-to-subject mapping;
- molecular modality and gene coverage;
- batch, site, source, treatment, steroid, and timing metadata;
- access tier and use terms; and
- whether the dataset was already used by this project.

A longitudinal dataset without the required outcome may be useful context but
is not validation-ready. `[A04]`

### A Therapeutic Direction

Start with the required **sign**, not with target popularity. State whether the
evidence implies inhibition, activation, restoration, context-dependent
modulation, or unresolved direction. Then state the relevant cell/state and why
the proposed modality can deliver that sign there. A structure or pocket is
context; it does not resolve causal gene or therapeutic direction. `[G02-G04]`

### A Visualization Or Interface

Name the decision and failure mode it serves. Show uncertainty, status,
invalid-input conditions, and abstention. Do not turn a provisional score into
a green/red recommendation. `[M01, M05, A01]`

### A Falsification Test

These are especially welcome. State the strongest alternative explanation,
the test that favors it over the current interpretation, and what result would
force a downgrade. The project treats a well-established negative as a result,
not as an inconvenience.

## How The Project Will Evaluate A Direction

1. **Provenance check:** Is every factual premise linked to a project artifact
   or clearly separated outside-source context?
2. **Duplicate/closure check:** Does the direction answer why the nearest prior
   route failed?
3. **Feasibility check:** Are the data and tools present or reachable?
4. **Prefilter check:** Is therapeutic direction compatible? Is the result
   likely to collapse into context, source, composition, or broad immune tone?
5. **Freeze:** Can prediction, null, search budget, holdout, and interpretation
   be fixed before the outcome is seen?
6. **Ground:** Run the strongest fair test on real data, or a clearly labeled
   synthetic method test when only method behavior is at issue.
7. **Grade:** Supported, not supported, inconclusive, data blocked, or closed.
   Proposal enthusiasm does not enter the grade.

This sequence means an idea may be excellent even if its first result is null.
It contributed by closing uncertainty under a fair test.

## Language That Preserves Trust

Prefer:

- “The project supports this association within these cohorts.”
- “This is a candidate for external validation.”
- “The required data are missing, so the question is not identifiable here.”
- “The result is sensitive to source balance.”
- “This structure suggests a possible geometry; it does not establish a
  target.”

Avoid:

- “proven,” “validated,” or “clinical” when evidence is internal or
  provisional;
- “causes” when the analysis shows association;
- “druggable” without the required therapeutic direction;
- “no biology” when the data design is missing; and
- “AI consensus” as support.

## Before You Submit

Use this final checklist:

- [ ] I chose an open problem or explained why this is a genuinely different
  one.
- [ ] I read the nearest closed or negative route.
- [ ] I stated one falsifiable prediction and one drop condition.
- [ ] I named the required data and checked whether they are reachable.
- [ ] I included a null or negative control and a holdout strategy.
- [ ] I addressed sample size, multiplicity, confounding, and source/batch.
- [ ] I kept monitoring, mechanism, target, clinical benefit, and progression
  as separate claims.
- [ ] I separated outside-source context from project evidence.
- [ ] I made no medical recommendation.

You are not expected to have every implementation detail. You are expected to
make the uncertainty and missing pieces visible. That is enough for the project
to decide whether the next step is a runnable test, a data request, or an honest
closure.
