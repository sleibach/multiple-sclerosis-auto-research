# Contribution Examples By Type

These examples are fictional communication fixtures. No dataset, method,
visual, or countertest below has been run. “Ready” means ready for review or
design freeze, not scientifically supported. `[E01-E03]`

## Data Source

### Repair needed

> I found a paper with MS patients before and after treatment. The data should
> validate the biomarker.

**Why it cannot be counted yet**

- “Before and after” does not prove same-person baseline/early pairing.
- “Response” may mean a molecular change rather than a person-level outcome.
- Sample-to-person mapping, timing, required genes, source/batch fields, and
  use terms are unknown.
- A paper is not an accessible package.
- Calling the provisional score “the biomarker” silently upgrades it. `[M01,
  A01-A04]`

### Ready for metadata triage

```markdown
Contribution type: data-source candidate
Decision role: independent outside test of the fixed early-change monitor
Permanent records: <persistent publication identifier>; <repository landing page>; accessed <date>
Independent unit: person; no overlap with named development cohorts found
Pairing: sample-person-baseline-early mapping documented at <location>
Outcome: person-level response definition and assessment time documented at <location>
Features: required module genes listed as present / missing / not yet verified
Confound fields: site, source, batch, treatment timing, steroid metadata listed
Access: open / controlled / author-returned; exact lawful next step
Current status: access candidate, not usable and not evidence
Missing field that blocks readiness: <one exact field, or none>
```

**Why this is reviewable:** Every eligibility statement points to a stable
record, and an unresolved field remains unresolved rather than inferred.

Use [Contribute A Data Source](CONTRIBUTE_A_DATA_SOURCE.md).

## Computational Or Analytical Method

### Repair needed

> A graph neural network should beat the simple score because biology is a
> network.

**Why it cannot run fairly**

- The method is supplied before the missing distinction.
- Tested flexible and coupled variants did not improve the scalar in the held
  small data. `[M03, D02]`
- No independent unit, baseline, search family, or untouched evaluation is
  named.
- “Biology is a network” does not predict a measurable performance difference.

### Ready for method evaluation

```markdown
Method role: predictor transport test
Decision changed: whether a pre-specified graph representation merits future development
Fixed target: the same person-level outcome, timing, and eligible fields as the comparator
Observation: the simple score may miss an interaction that transports across cohorts
Baseline: locked scalar under the identical eligible participants and outcome
Independent unit: cohort for the primary transport claim; person within development
Development: tune only in named development cohorts
Untouched evaluation: one eligible outside cohort, opened after freeze
Null/search family: all graph variants and hyperparameters counted; label permutations preserve cohort/person structure
Confound/leak checks: source, batch, timing, repeated people, preprocessing, immune tone
Drop rule: stop if the graph is not better calibrated or does not improve the pre-specified metric within uncertainty
Status: method proposal; no biological claim
```

**Why this is reviewable:** The complex method receives no extra labels or
post-hoc target choice, and a simpler equivalent result stops it.

Use [Contribute A Method](CONTRIBUTE_A_METHOD.md).

## Documentation Or Visual

### Repair needed

> Show the APC pathway in green, put failed genes in red, and end the diagram at
> “personalized treatment.”

**Why it misleads**

- Green/red alone is inaccessible and reads as success/failure rather than
  evidence status.
- The coupled APC pattern is context, not a causal pathway or target. `[D01]`
- The monitoring lead has no personalized-treatment use. `[M01, M05]`
- Closed routes need scoped labels, not “failed genes.”

### Ready for communication review

```markdown
Reader task: distinguish monitor, coupled context, target, and closed route
Claim IDs: M01, M05, D01, G03-G05
Sources: <controlling project artifacts>
Current status labels: provisional monitor / supported context / closed route
Decisive caveat: no treatment selection or target follows
Visual design: text labels plus shape and border style; color is redundant
Semantics: SVG title/description, useful alt text, full Markdown equivalent
Delivery: responsive viewBox, grayscale/narrow-screen/print review, lightweight file
Dangerous overread check: a reader cannot reach “personalized treatment” from the diagram
Evidence impact: none
```

**Why this is reviewable:** Meaning is frozen before styling, and the design
tests the overread it could create.

Use [Contribute Documentation Or A Visual](CONTRIBUTE_DOCUMENTATION_OR_VISUAL.md).

## Adversarial Challenge

### Repair needed

> A respected review says this pathway matters, so the project's negative must
> be wrong.

**Why it is not a countertest**

- Authority does not identify which project claim is challenged.
- “Matters” may refer to a different population, compartment, outcome, or
  direction.
- No real-data result could make the challenge lose.
- Outside-source context cannot override a rerunnable project result. `[E02]`

### Ready for adversarial triage

```markdown
Exact challenged claim: <claim ID, bounded wording, controlling source>
Strongest rival: <alternative explanation>
Different predictions: original expects <A>; rival expects <B>
Eligible data: <population, compartment, timing, outcome, independent unit>
Fair countertest: <one primary test, null/control, confound and multiplicity plan>
Original claim weakens if: <pre-specified outcome>
Challenge fails if: <pre-specified outcome>
Inconclusive if: <interval, overlap, power, or data condition>
Status consequence: <narrow / retain / close / request data>; no larger claim
```

**Why this is reviewable:** The challenge and the original can both lose, and
the consequence is set before the result.

Use [Challenge The Project](CHALLENGE_THE_PROJECT.md).

## One Pattern Across All Four Types

| weak submission | reviewable submission |
|---|---|
| Starts with a solution or authority. | Starts with the missing distinction and current boundary. |
| Assumes access, labels, or independence. | Verifies each required field and unit. |
| Makes every outcome encouraging. | Precommits failure, invalid, data-blocked, and inconclusive paths. |
| Uses workflow words as evidence. | Keeps proposal, runnable, merged, supported, and validated separate. |
| Hides the nearest failed route. | Names it and states exactly what changes. |
| Says the tool should work. | Names the fair comparator and a result that stops it. |

For full issue examples, continue with
[Public Issue Examples](PUBLIC_ISSUE_EXAMPLES.md). For a bounded first task,
use [Starter Contributions](STARTER_CONTRIBUTIONS.md).
