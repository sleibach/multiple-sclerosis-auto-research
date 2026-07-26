# What Happens After You Submit An Idea

A submitted idea is a proposal, not a finding. This page explains how the
project turns a contribution into a reviewable decision without rewarding
confidence, credentials, length, or agreement with the current interpretation.

There is no guaranteed response time, execution slot, or positive outcome. The
commitment is narrower: when an idea is reviewed, its status and strongest
reason should be visible, and a proposal cannot silently become project
evidence. `[E01-E03]`

## The Short Version

```text
received
  -> safety, permission, provenance, and duplicate screen
  -> normalize into a falsifiable test card
  -> repair, request data, park, close, test externally, or run now
  -> if run: freeze the test before seeing its result
  -> supported, bounded, null, inconclusive, invalid, or data blocked
  -> update the issue and the appropriate project artifact
```

“Accepted for review” means only that an idea entered this process. “Runnable”
means a fair test can begin. “Supported” can be assigned only after a valid,
rerunnable test, and it remains limited to what that test measured.

## Stage 1: Intake Without Promotion

The first response should record:

- the contributor's exact proposal;
- the project boundary it is meant to address;
- any sources, data locations, code, and use restrictions;
- the nearest existing or closed route; and
- whether patient-specific information or medical advice must be removed.

At this point the idea remains a proposal. A citation, model suggestion,
predicted structure, or expert endorsement may motivate a test, but it cannot
support a project conclusion by itself. `[E01-E03]`

Possible status: **received** or **needs an intake repair**.

## Stage 2: Hard-Gate Review

The [triage rubric](IDEA_TRIAGE_RUBRIC.md#step-1-hard-gates) checks seven
non-negotiable conditions:

1. Evidence language does not upgrade a proposal.
2. Safety and privacy boundaries are respected.
3. A locked analysis is not tuned after outcomes are visible.
4. Data access and use are lawful and explicit.
5. The idea addresses the nearest duplicate or closure.
6. A therapeutic idea states the required functional direction and modality.
7. At least one observable outcome can make the idea fail or narrow.

Each gate receives **pass**, **repair**, or **stop**. Strong performance on one
dimension cannot compensate for a failure here. A highly original idea with no
lawful data path is not runnable; an elegant target proposal with the wrong
functional direction is not rescued by structural tractability. `[G02-G04,
A01]`

Possible status: **gate passed**, **needs repair**, or **stopped in current
form**.

## Stage 3: Turn The Thought Into A Test Card

The reviewer and contributor may need to rewrite the idea into the smallest
fair test. The card records:

- one bounded claim;
- the unit, population, compartment, and time;
- a prediction and a competing explanation;
- reachable data and required fields;
- a null or negative control;
- holdout, multiplicity, small-sample, source, batch, and confound plans;
- a drop rule; and
- what pass, fail, and inconclusive outcomes would change.

This is a design repair, not a rejection. The original insight may be useful
while its first wording is too broad to test. Worked rewrites are in
[Idea Transformations](IDEA_TRANSFORMATIONS.md).

Possible status: **test card ready** or **needs a field-specific repair**.

## Stage 4: Choose One Action Class

The action class says what happens next. It is not an evidence grade.

| action | what it means | what the contributor should expect |
|---|---|---|
| **Run now** | The hard gates pass, suitable data are reachable, and the error controls are adequate. | The exact test is frozen before execution. No positive result is promised. |
| **Design repair** | The core idea may be testable, but scope, prediction, comparator, or controls are incomplete. | A specific repair request, not “add more detail.” |
| **Data request** | The prediction is credible but the required package or fields are absent or unverified. | A precise acquisition checklist. Missing data are not called absent biology. `[A04, P01-P05]` |
| **External test** | A frozen route needs an independent cohort, holder-side run, assay, or other outside execution. | The rule remains unchanged; the external result may pass, fail, or be inconclusive. `[A01]` |
| **Duplicate or closed** | The idea repeats a tested route without resolving its documented failure. | A link to the closure and the exact evidence that could reopen it. |
| **Out of scope or unsafe** | The proposal requires medical advice, unsafe patient handling, unauthorized access, or evidence-class mixing. | It is not executed; the boundary is explained without evaluating the contributor. |
| **Parked** | The idea may be executable, but no possible result would currently change a meaningful decision. | It is recorded with a reopening condition rather than repeatedly rerun. |

Parking is not a hidden negative, and a data request is not support. These
labels describe the next operation only.

## Stage 5: Freeze Before Running

For a runnable analysis, the project records the feature or estimand, eligible
inputs, exclusions, outcome, split or holdout, null, correction, confounders,
and decision thresholds before looking at the result. Locked rules and existing
preregistrations are not changed to help a contributed idea succeed. `[A01]`

The issue should link to the frozen plan or committed code and state which
result would stop the route. If the inputs later fail identity, permission,
pairing, timing, coverage, or source-balance checks, the result is invalid or
data blocked rather than a biological null.

Possible status: **frozen and queued**, **blocked on named input**, or
**ineligible input**.

## Stage 6: Grounding Can End Six Different Ways

The project does not force every result into “works” or “does not work.”

| result | permitted interpretation | typical next decision |
|---|---|---|
| **Supported but bounded** | The pre-specified result held in the tested scope. It may still be provisional or need independent validation. | Replicate, validate, or run the next distinct gate without enlarging the claim. |
| **Attenuated or narrowed** | A confounder, subgroup, source, or sensitivity analysis reduces the original interpretation but leaves a smaller one. | Rewrite the claim to the surviving scope. |
| **Null or not supported** | A fair test did not support the stated prediction at the detectable scale. | Stop that tested route or revise only if genuinely new evidence changes the test. |
| **Inconclusive** | Uncertainty is too wide to distinguish support from a meaningful null. | Use the estimate to specify the sample size or data quality needed next. |
| **Invalid or unscoreable** | The inputs or execution do not satisfy the frozen test. | Repair the input or method; do not interpret biology. |
| **Data blocked** | The held design cannot identify the claim. | Request the missing design; do not translate “not measurable here” into “not present.” `[P01-P05]` |

Read [How To Read Nulls And Boundaries](HOW_TO_READ_NULLS_AND_BOUNDARIES.md)
for the full distinction.

## Stage 7: Close The Loop Publicly

The final issue or review note should contain:

1. the action class and strongest reason;
2. the exact test or blocker;
3. links to code, inputs, and generated artifacts that may be public;
4. the result class and its narrow permitted wording;
5. uncertainty, confounders, and failed checks;
6. the decision: advance, narrow, acquire data, repair, park, or close; and
7. what specific new evidence could change that decision.

A result is added to a findings or report tree only under the repository's
existing evidence discipline. Outside context stays in its segregated area.
Private, controlled, or identifying data are never posted merely to make a
review complete.

## What A Useful Project Response Looks Like

```markdown
Status: Design repair

Strongest reason:
The proposal does not yet distinguish source imbalance from the claimed cell
state.

What is needed:
Specify a source-overlap diagnostic, a within-source comparison, and the result
that would make the state claim fail.

Nearest project boundary:
C02 (source/diagnosis entanglement); P01 (progression design boundary).

What this status does not mean:
It does not say the biology is absent or that the contributor's broader idea is
false. It says this version cannot identify it.
```

## How To Revise Or Challenge A Review

A contributor can reopen a review by addressing the named reason, not by
restating confidence. Useful revisions include:

- a verified dataset with the missing fields and lawful access;
- a comparator that separates the main alternative explanation;
- a direction-matched assay or modality;
- a fixed null, holdout, or correction plan;
- evidence that the proposal differs materially from the cited closure; or
- a smaller claim that the available design can actually identify.

Reviewer disagreement should be resolved by naming the disputed assumption or
missing evidence. It should not be averaged into a vague middle score.

## The Contributor Promise And Its Limit

The project can promise a legible process, explicit boundaries, and credit for
useful ideas or falsification work. It cannot promise that every submission is
run, that an idea will remain open, or that a null will be retried until it
becomes positive.

The most valuable contribution may be a method that survives grounding, a
dataset that makes a frozen test possible, a decisive null, or a clear reason
not to spend scarce clinical or laboratory resources. Ideas choose candidate
directions; valid data and design determine the verdict.

## Continue

- [Submit or repair an idea](HOW_TO_CONTRIBUTE_IDEAS.md)
- [Use a review-response template](REVIEW_RESPONSE_TEMPLATES.md)
- [See the detailed triage rubric](IDEA_TRIAGE_RUBRIC.md)
- [Choose an open puzzle](OPEN_PROBLEMS_FOR_COLLABORATORS.md)
- [Learn the evidence outcomes](HOW_TO_READ_NULLS_AND_BOUNDARIES.md)
