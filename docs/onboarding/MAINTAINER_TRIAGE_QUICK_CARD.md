# Maintainer Triage Quick Card

Use this card for the first review of a research-direction issue. It condenses
the existing [triage rubric](IDEA_TRIAGE_RUBRIC.md),
[status decoder](STATUS_DECODER.md), and
[response templates](REVIEW_RESPONSE_TEMPLATES.md). It creates no new status
or evidence rule. `[E01-E03]`

## The 60-Second Rule

Always write three separate lines:

```text
Workflow: what happens next
Validity: whether an eligible test has run
Evidence: what an eligible run established
```

For a new submission, validity is `not run` and evidence is `no new grade`.
Receipt, discussion, model agreement, citations, a predicted structure, merge,
and runnable code do not change that.

## Screen In This Order

Stop at the first unresolved hard gate. Ask for one named repair when repair is
possible.

1. **Safety:** no medical advice, personal health information, credentials,
   private data, or unsafe patient handling.
2. **Permission:** data and code have a lawful, documented use path.
3. **Evidence language:** outside context and proposals are not presented as
   project findings.
4. **Frozen work:** no outcome-aware change to a locked rule or
   preregistration.
5. **Nearest route:** the issue names the closest tested, negative, or closed
   route and what materially changes.
6. **Therapeutic direction:** if relevant, causal entity, required functional
   sign, cell/state, modality, delivery, and direction-matched assay are named.
7. **Falsifiability:** at least one result drops or narrows the proposal.

Do not average away a failed hard gate with novelty, confidence, credentials,
or expected impact.

## Choose Exactly One Workflow Action

| action | use when | first response |
|---|---|---|
| `RUNNABLE_NOW` | Hard gates pass; data, prediction, null/holdout, confounds, and drop rule are sufficient. | Freeze before execution. State that runnable is not support. |
| `DESIGN_REPAIR` | The idea may be testable, but one or more design fields are missing. | Name the single strongest missing distinction and exact repair. |
| `DATA_REQUEST` | The test is credible, but the required package or field is absent or unverified. | List the minimum acceptable fields and near-matches that do not substitute. |
| `EXTERNAL_TEST` | A frozen object needs a distinct cohort, holder-side run, assay, or prospective execution. | Link the immutable object and precommitted return package. |
| `DUPLICATE_OR_CLOSED` | The issue repeats a tested route without addressing its failure reason. | Link the closure and name the evidence that could reopen it. |
| `OUT_OF_SCOPE_OR_UNSAFE` | Safety, permission, medical-advice, or evidence-class handling stops execution. | Remove/restrict unsafe material; offer only a safe general reformulation. |
| `PARKED_LOW_VALUE` | The issue may run, but no outcome changes a current decision. | Record one reopening condition; do not imply a negative result. |

If two actions seem necessary, choose the earliest blocker. Example: use
`DATA_REQUEST` before `EXTERNAL_TEST` until the external package is verified.

## If A Run Is Claimed

Before reading the biological interpretation, verify:

- eligible unit, labels, times, fields, provenance, and permission;
- frozen claim, feature/estimand, outcome, exclusions, and thresholds;
- independent holdout unit and no leakage;
- structure-preserving null or fair negative control;
- multiplicity and small-sample uncertainty;
- source, batch, composition, timing, and other precommitted confound checks;
  and
- no invalidation or data-block rule triggered.

If any required condition fails, use `invalid/non-identifiable` or
`data-blocked`. Neither is a biological null.

## Eligible Result Words

Only after a valid, rerunnable test:

| result class | bounded meaning |
|---|---|
| Supported but bounded | The fixed result held only in its tested scope. |
| Attenuated or narrowed | A harder check reduced the effect or interpretation. |
| Negative-established | The fair test did not support this bounded route at the detectable scale. |
| Inconclusive | Uncertainty cannot distinguish support from a meaningful null. |
| Invalid/non-identifiable | The design cannot support a biological interpretation. |
| Data-blocked | Required observations were absent or unusable. |

Never translate data-blocked into absent biology, invalid into null, supported
into mechanism/target/clinical benefit, or provisional into validated.

## Minimum Public Response

```markdown
Workflow: <one action class>
Validity: <not run / eligible / invalid / data-blocked>
Evidence: <no new grade / existing grade unchanged / bounded result class>

Safety: no personal health information, credentials, private data, or medical
advice is reproduced in this response.

Strongest reason:
<one concrete sentence>

Useful part:
<the retained observation, method, data lead, or challenge>

Next action or repair:
<one executable request, frozen command, data field list, or stop>

Nearest project boundary:
<claim IDs and controlling artifact or closure>

What would change this decision:
<specific evidence or completed check>

Overread prevented:
<one sentence stating what this status/result does not mean>

Evidence boundary:
This workflow response changes no scientific grade unless it reports a
separately committed eligible run under the existing evidence process.
```

Grade the contribution, not the contributor. Do not leave unresolved template
placeholders in a public response.

## Escalate Instead Of Improvising

- Unsafe personal information: follow
  [Patient And Public Safety](PATIENT_AND_PUBLIC_SAFETY.md) without quoting the
  material.
- Unclear evidence language: use the [Status Decoder](STATUS_DECODER.md).
- Complex/high-cost design: use the full
  [Idea Triage Rubric](IDEA_TRIAGE_RUBRIC.md) and two independent reviewers.
- Missing exact wording: use [Review Response Templates](REVIEW_RESPONSE_TEMPLATES.md).
- A claimed result: require committed code, inputs, outputs, uncertainty, and
  the frozen interpretation grid before any evidence update.

Return to the [contributor lifecycle](WHAT_HAPPENS_TO_YOUR_IDEA.md) or the
[onboarding landing page](README.md).
