# Status Decoder: Workflow Is Not Evidence

This page prevents a common category error: treating what the project will do
with an idea as if it were a scientific verdict on that idea.

Three separate questions must be answered:

1. **Workflow:** What happens next?
2. **Test validity:** Did a fair, interpretable test run?
3. **Evidence:** What did an eligible test establish, within its limits?

Only the third question can change a scientific evidence grade. A proposal can
be runnable and still be wrong. It can be parked and still be biologically
plausible. It can complete a computation and still yield no interpretable
biological result. `[E01-E03]`

## The 30-Second Decoder

| phrase | layer | what it means | what it does **not** mean |
|---|---|---|---|
| Received | Workflow | The proposal entered triage. | Supported, promised, or scheduled. |
| Design repair | Workflow | One or more fields needed for a fair test are missing. | The biology is false. |
| Data request | Workflow | The required package is absent or not verified. | The effect is absent. |
| Runnable | Workflow | Inputs and a frozen test are sufficient to execute. | Likely true or already supported. |
| External test | Workflow | A distinct cohort, assay, or holder-side run is required. | Independently validated. |
| Parked | Workflow | A named condition or higher-value dependency comes first. | Negative result. |
| Duplicate or closed in current form | Workflow | This version repeats a tested route or misses known reopening evidence. | Every broader question involving the same biology is false. |
| Eligible completed test | Test validity | The planned analysis ran on suitable data and can support interpretation. | A positive result. |
| Invalid or non-identifiable | Test validity | The design could not separate the claim from its main alternative. | A biological null. |
| Data-blocked | Test validity | Required observations were unavailable or unusable. | Evidence of no biology. |
| Supported but bounded | Evidence | The result supports one exact claim within stated limits. | Mechanism, target, clinical utility, or universal truth. |
| Provisional | Evidence | Internal support exists, but a decisive outside test is still pending. | Validated or ready for clinical use. |
| Attenuated or narrowed | Evidence | A harder check reduced the effect or claim scope. | The original stronger story survives unchanged. |
| Negative-established | Evidence | A fair test did not support the bounded route at the detectable scale. | Every related mechanism is impossible. |
| Inconclusive | Evidence | Uncertainty is too large to choose support or rejection. | Weak confirmation or weak disproof. |

## Layer 1: Workflow Status

Workflow labels route work. They are operational decisions, not biological
judgments.

| workflow status | next action | evidence consequence |
|---|---|---|
| Received | Check safety, permission, duplication, direction, data, and falsifiability. | None. |
| Design repair | Ask for the exact missing prediction, comparator, null, holdout, or drop rule. | None. |
| Data request | Name the minimum acceptable package and reject tempting substitutes. | None. |
| Runnable after freeze | Lock the claim, inputs, analysis, correction, and interpretation rules before running. | None until an eligible run finishes. |
| External test required | Transfer only the frozen object and precommitted return package. | Existing evidence stays unchanged while pending. |
| Parked | Record a specific reopening condition. | Existing evidence stays unchanged. |
| Duplicate or closed in current form | Point to the prior route and the evidence that would reopen it. | Uses the prior grade; it creates no new result. |
| Out of scope or unsafe | Remove patient advice, identifying data, unauthorized access, or rule tuning. | None. |

“Accepted for review” therefore cannot be shortened to “accepted.” The shorter
word sounds like scientific endorsement. “Runnable” must always retain “after
freeze” or an equivalent limit.

## Layer 2: Test Validity

A computation finishing is not enough. Before reading a biological result,
ask whether the test was eligible:

- Were the required units, labels, times, and permissions present?
- Was the analysis frozen before the outcome was inspected?
- Did the design separate the claim from its main confounder or alternative?
- Was the holdout unit truly independent?
- Were multiplicity and small-sample uncertainty handled as planned?
- Did any precommitted invalidation rule trigger?

An **eligible completed test** may change evidence. An **invalid**,
**non-identifiable**, or **data-blocked** attempt cannot. These labels explain
why interpretation stops; they are not softer names for a null.

## Layer 3: Evidence Status

Evidence labels describe what a valid run supports. They always travel with
scope: population, compartment, time, outcome, uncertainty, confound checks,
and validation level.

| evidence status | permissible sentence | nearest forbidden upgrade |
|---|---|---|
| No grade yet | “This is a proposal awaiting a valid test.” | “The project has a new lead.” |
| Supported but bounded | “The pre-specified result supports this exact claim under these conditions.” | “The mechanism or target is established.” |
| Provisional | “Internal evidence supports the bounded claim; outside confirmation is pending.” | “It is validated.” |
| Attenuated or narrowed | “The result survives only in this reduced scope after the harder check.” | “The original interpretation held.” |
| Negative-established | “The fair test did not support this route within its tested scope.” | “The broader biology does not exist.” |
| Inconclusive | “The estimate and interval do not settle the question.” | “It trends toward confirmation.” |

Project-grounded, provisional, negative, and outside-source context are not
synonyms. Outside literature, databases, and model suggestions may motivate a
test, but citation or agreement alone does not change a project evidence
grade. `[E01-E03]`

## The Two-Axis Matrix

The same workflow state can coexist with different prior evidence. Read across
both columns rather than compressing them into one label.

| situation | workflow / validity | evidence now | correct interpretation |
|---|---|---|---|
| A new idea has just arrived. | Received; not run. | No grade. | Triage it without endorsing or rejecting it. |
| A complete test card can run on held data. | Runnable after freeze; not run. | No new grade. | Execution eligibility is not support. |
| A promising question lacks paired outcome labels. | Data request; data-blocked. | No new grade. | Missing labels do not imply an absent effect. |
| A lower-priority test awaits another dependency. | Parked. | Prior grade unchanged, or no grade. | Priority is not truth. |
| A proposal repeats a direction-closed route. | Duplicate or closed in current form. | Prior bounded closure remains. | Reopening requires the named missing evidence. |
| A planned comparison cannot separate source from diagnosis. | Completed or attempted; non-identifiable. | No biological grade from this run. | Repair the design; do not call it a null. |
| A pre-specified eligible test finishes. | Completed and eligible. | Supported, attenuated, negative, or inconclusive according to the frozen grid. | Now, and only now, report an evidence outcome. |
| A frozen outside validation is waiting for data. | External test required. | Existing internal status remains provisional. | Pending validation is not validation. |

## Current Project Examples

### The monitoring score

- **Evidence:** one live, provisional early-treatment monitoring signal with
  bounded internal support.
- **Workflow:** a frozen independent validation is required.
- **Do not say:** “The biomarker is accepted” or “external validation is under
  way” unless an eligible package is actually available and running.
- **Correct:** “The provisional monitoring signal awaits a pre-registered
  independent test.” `[M01-M05, A01, A03-A04]`

### Progression

- **Evidence:** no progression biomarker, transition mechanism, target, or
  means of halting progression was established by the held analyses.
- **Workflow:** the next candidate test is data-blocked pending a specifically
  structured longitudinal microglia-compatible package.
- **Do not say:** “Progression biology was disproved.”
- **Correct:** “The held data could not identify the required molecular-to-
  confirmed-disability relationship; the missing design is specified.”
  `[P01-P06, A02]`

### Direction-closed genetics routes

- **Evidence:** some tested regions or genes remain biological context, while
  the simple therapeutic route is closed because causal assignment,
  protective direction, or modality fit failed.
- **Workflow:** a near-duplicate proposal should be marked closed in current
  form unless it supplies the exact reopening evidence.
- **Do not say:** “The gene is irrelevant” or “a pocket reopens the target.”
  `[G02-G05]`

## Transitions That Are Allowed

```text
received -> design repair -> runnable after freeze -> eligible run
eligible run -> supported / attenuated / negative / inconclusive

received -> data request -> data-blocked pending receipt
received -> parked -> reopened only when the named condition occurs
received -> duplicate/closed -> reopened only by the named missing evidence
attempted run -> invalid/non-identifiable -> redesign, not biological verdict
```

Transitions that are **not** allowed:

```text
received -> supported
runnable -> likely true
parked -> negative
data-blocked -> absent biology
invalid -> null
outside agreement -> project-grounded
model agreement -> evidence
```

## Use This In A Review

Write two separate lines:

```markdown
Workflow: <received / repair / data request / runnable / external test /
parked / duplicate-closed / out-of-scope>

Evidence: <no grade yet / existing grade unchanged / supported-bounded /
provisional / attenuated / negative-established / inconclusive /
no biological grade because invalid or data-blocked>
```

Then state the reason, next action, and the evidence that would change the
decision. Use the [review-response templates](REVIEW_RESPONSE_TEMPLATES.md)
for exact wording and the [contributor lifecycle](WHAT_HAPPENS_TO_YOUR_IDEA.md)
for the complete process.

## Limits

- This decoder governs language and routing; it does not validate an analysis.
- A correct status label cannot repair a weak design.
- “Supported” never travels without scope and uncertainty.
- “Closed” applies to a tested route, not an unlimited biological universe.
- Human reviewers remain responsible for checking the controlling artifacts.

Continue with [how to read nulls and boundaries](HOW_TO_READ_NULLS_AND_BOUNDARIES.md)
or [how to contribute an idea](HOW_TO_CONTRIBUTE_IDEAS.md).
