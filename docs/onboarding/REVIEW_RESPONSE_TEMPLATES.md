# Review Response Templates For Contributor Ideas

These templates make idea review specific, respectful, and evidence-safe. They
grade a proposal or result, never the contributor. Replace every angle-bracket
field; do not send a template with unresolved placeholders.

An operational status is not an evidence grade. “Runnable” does not mean
likely true, and “received” does not mean supported. Project evidence changes
only after a valid rerunnable test. `[E01-E03]`

## Rules For Every Response

Every response should contain:

1. the current workflow or result status;
2. the strongest reason for that status;
3. what is useful in the contribution;
4. the exact next repair, data need, test, or stopping decision;
5. the nearest project claim or closure;
6. what would change the decision; and
7. one sentence preventing the nearest overread.

Avoid judging intelligence, expertise, motivation, or effort. “This idea is
weak” is not actionable. “The proposed comparison cannot separate source from
diagnosis because one outcome has no within-source overlap” is.

## 1. Receipt

```markdown
Status: Received for triage

Boundary addressed:
<one current project question or open-problem number>

What we recorded:
- Proposal: <one neutral sentence>
- Required data or method: <one sentence>
- Sources/context: <links or none supplied>
- Nearest existing route: <claim ID, closure, or not yet identified>

Next review:
We will check safety, permission, duplication, therapeutic direction where
relevant, and whether an observable result can make the proposal fail.

Important limit:
Receipt does not make the proposal project evidence or promise execution.
```

## 2. Design Repair

```markdown
Status: Design repair

What is useful:
<the exact insight, method transfer, dataset lead, or falsification angle>

Strongest blocker:
<one missing claim / prediction / comparator / null / holdout / drop rule>

Please add:
1. <field-specific request>
2. <field-specific request>
3. <the result that would make the idea fail or narrow>

Nearest project boundary:
<claim IDs and source-linked prior route>

What this status does not mean:
It does not say <broader idea or biology> is false. It says this version cannot
yet distinguish the stated claim from <main alternative>.
```

## 3. Data Request

```markdown
Status: Data request

The testable prediction:
<one sentence>

Why it cannot run now:
The current package lacks or has not verified <pairing / labels / outcome /
time / source / genes / permissions / sample map>.

Minimum acceptable package:
- <required unit and identifiers>
- <required measurements and times>
- <required outcome and definition>
- <required confound/source fields>
- <access and use terms>

Near-matches that do not answer the question:
<one or more tempting substitutes>

Decision after receipt:
Eligibility is checked blind to the outcome result. Missing data are not
evidence that the biology is absent. [A04 / P01 as applicable]
```

## 4. Duplicate Or Closed Route

```markdown
Status: Duplicate or closed in current form

Nearest prior route:
<link to finding, workup, failure mode, or closure>

Why it closed:
<causal-gene uncertainty / wrong functional direction / confounding /
no improvement / failed validation gate / missing design>

What the new proposal currently repeats:
<specific assumption or evidentiary test>

Evidence that could reopen it:
<specific causal, direction, assay, cohort, or design evidence>

Important limit:
Closure applies to the tested route. It does not mean the named gene, process,
or broader biology is universally irrelevant.
```

For therapeutic proposals, do not accept “there is a pocket” or “the class is
usually inhibited” as a repair for an unresolved causal entity or restoration
direction. `[G02-G05]`

## 5. Parked

```markdown
Status: Parked

Why the idea is not being run now:
<no current decision changes / lower value than another executable test /
depends on a named future condition>

What remains useful:
<method, context, data lead, or future comparison retained>

Reopening condition:
<specific data arrival, status change, or new independent evidence>

Important limit:
Parked is a workflow priority, not a negative scientific result.
```

## 6. Out Of Scope Or Unsafe

```markdown
Status: Out of scope or unsafe in current form

Boundary triggered:
<medical advice / patient-specific recommendation / identifying data /
unauthorized access / incompatible use terms / locked-rule tuning /
outside context treated as evidence>

What can be retained safely:
<a non-clinical research question, public source, or de-identified method idea,
if any>

What must not be submitted or run:
<specific material or operation>

Possible safe reformulation:
<bounded option, or “none under the current request”>
```

Do not debate a patient's treatment in an issue. Do not request personal health
details to make a proposal more concrete.

## 7. Runnable Now

```markdown
Status: Runnable after freeze

Bounded claim:
<one sentence>

Verified inputs:
<data, permissions, unit, pairing, fields, coverage>

Frozen test:
- Estimand or feature: <definition>
- Primary outcome: <definition>
- Null/comparator: <definition>
- Holdout unit: <person / donor / site / cohort / modality>
- Multiplicity: <family and correction>
- Confound/source checks: <fixed list>
- Pass/fail/inconclusive rules: <links or definitions>

Drop rule:
<precommitted condition>

Important limit:
Runnable means the test is fair enough to execute. It does not mean the idea is
likely to be supported.
```

## 8. External Test

```markdown
Status: External test required

Frozen object:
<rule, assay, feature, outcome, or preregistration link>

Why internal analysis is insufficient:
<independent cohort / holder-side execution / perturbation / prospective use>

What the external party may do:
<mechanical permitted operations>

What may not change after outcomes are seen:
<features, threshold, exclusions, outcome, confound plan>

Return package:
<minimum aggregate or sample-level outputs, provenance, and quality report>

Interpretation grid:
Pass, fail, and inconclusive retain their precommitted meanings. Independent
execution does not guarantee a positive result. [A01]
```

## 9. Supported But Bounded Result

Use only after a real, valid, committed run.

```markdown
Result: Supported but bounded

Test that ran:
<committed plan/code and eligible input>

Observed estimate and uncertainty:
<effect, interval, null result, multiplicity, holdout>

Permitted claim:
<one exact sentence within population, time, compartment, and outcome>

Remaining limits:
<confounders, sample size, validation level, transport, mechanism>

Decision:
<replicate / external validation / next distinct gate / bounded use>

Forbidden upgrade:
This result does not establish <nearest target / clinical / causal /
progression overread>.
```

## 10. Attenuated Or Narrowed Result

```markdown
Result: Attenuated or narrowed

Original interpretation tested:
<one sentence>

Check that changed it:
<source / batch / baseline / immune tone / composition / sensitivity>

What survives:
<smaller bounded statement, or none>

What is withdrawn:
<stronger interpretation>

Decision:
<rewrite claim / source-balanced replication / stop strong route>

Important limit:
Do not choose the least attenuated sensitivity as the new primary result.
```

## 11. Null Or Not Supported Result

```markdown
Result: Not supported under the pre-specified test

Fair-test evidence:
<eligibility, detectable scale, effect/interval, null, holdout, correction>

Claim closed or narrowed:
<exact tested prediction>

What remains outside scope:
<broader biology, other contexts, effects below detection, different designs>

Decision:
<stop spending / retain bounded context / reopen only with named new evidence>

Important limit:
A scoped null is not proof that an entire pathway, gene, or disease process is
irrelevant.
```

## 12. Inconclusive Result

```markdown
Result: Inconclusive

Estimate and interval:
<continuous estimate, uncertainty, event/class counts>

Why no pass/fail decision is possible:
<interval spans both meaningful support and meaningful null / quality limit>

What remains informative:
<effect-size bound, variance, failure rate, cohort-size or data-quality need>

Next package required:
<specific n, events, timing, fields, source overlap, or platform condition>

Important limit:
Inconclusive is not weak support and not evidence of absence.
```

## 13. Invalid Or Data-Blocked Result

```markdown
Result: Invalid/unscoreable OR data blocked

Failed requirement:
<identity / pairing / permission / coverage / source overlap / outcome /
longitudinal design / execution check>

Why biology cannot be interpreted:
<the failure breaks the frozen test or prevents identification>

Decision:
<repair intake / reacquire data / request missing design / stop package use>

No permitted biological claim:
The package did not produce a valid null, negative, or positive result.
```

## Final Reviewer Check

- [ ] The response names one strongest reason rather than a vague impression.
- [ ] The proposal, workflow action, and evidence grade are separate.
- [ ] Any repair asks for exact fields or design changes.
- [ ] Null, inconclusive, invalid, and data blocked are not collapsed.
- [ ] The nearest tempting overread is explicitly rejected.
- [ ] The response evaluates no personal trait of the contributor.
- [ ] Links and private-data boundaries are correct.
- [ ] A status change requires the evidence named in the response.

## Continue

- [Read the full response lifecycle](WHAT_HAPPENS_TO_YOUR_IDEA.md)
- [Follow the worked fictional example](WORKED_SUBMISSION_LIFECYCLE.md)
- [Use the detailed triage rubric](IDEA_TRIAGE_RUBRIC.md)
- [Read numbers without overreading](HOW_TO_READ_NUMBERS_WITHOUT_OVERREADING.md)
