# Worked Example: From Outside Idea To Bounded Verdict

This is a **fictional process example**. No analysis below was run, no numbers
are reported, and none of the branches is biological evidence. The example
shows how a useful outsider idea can be repaired and evaluated without being
promoted merely because it sounds plausible.

The scenario uses a real project lesson: source and diagnosis were entangled in
one microglia partition, so source-aware checks are necessary before a stronger
disease interpretation. The lesson is grounded; the submission and every
future-result branch below are illustrative only. `[C01, C02]`

## 1. The Initial Submission

> **Idea:** Train an adversarial classifier to predict sample source. If it can
> predict source, remove source information from the expression data and rerun
> the disease analysis. This should prove whether the signal is real.

This is a useful direction hidden inside an unsafe claim. It imports a method
from domain adaptation and points at a known failure mode. It is not runnable
yet.

## 2. Intake Record

| intake field | review record |
|---|---|
| Proposed contribution | A source-predictability diagnostic plus a source-aware sensitivity analysis. |
| Boundary addressed | Source or acquisition process may masquerade as disease. `[C02]` |
| Nearest prior work | Brain-bank source-balance audit and prospective source-balance addendum. |
| Evidence status | Proposal only. No new dataset or result was supplied. |
| Safety and privacy | Can be discussed without patient details; any real run must use legitimately held data and approved metadata. |
| Immediate overread | “Remove source” may remove biology or fail to restore overlap; no adjustment can prove the residual signal is causal. |

**Intake status:** received; design repair required.

## 3. Hard-Gate Review

| gate | result | reason |
|---|---|---|
| Evidence language | repair | “Prove whether real” exceeds what a source diagnostic or adjustment can establish. |
| Safety and scope | pass | No medical advice or personal health request. |
| Locked analysis | pass with condition | The diagnostic must not tune a frozen validation rule after outcomes are visible. |
| Data permission | repair | No actual dataset or terms were named. |
| Duplicate or closure | pass | It extends the known source-confound lesson rather than ignoring it. |
| Therapeutic direction | not applicable | The proposal is a diagnostic method, not a target. |
| Testability | repair | No unit, overlap criterion, null, holdout, or failure condition was stated. |

The strongest reason is not “we dislike the method.” It is that the proposed
verb, **prove**, is stronger than the design, and the test is underspecified.

**Action class:** design repair.

## 4. The Field-Specific Repair Response

```markdown
Status: Design repair

What is useful:
The proposal addresses the documented source/diagnosis failure mode and imports
a potentially relevant domain-shift diagnostic.

What prevents a run:
The independent unit, source-overlap requirement, null, holdout, and bounded
interpretation are missing. “Remove source and prove the signal is real” is not
an allowed conclusion.

Please add:
1. the person/donor-level unit and exact source labels;
2. a pre-analysis overlap table for source by outcome;
3. a source-prediction test evaluated on held-out donors;
4. a label-permutation null that preserves source and donor structure;
5. a within-source or overlap-restricted disease contrast;
6. a rule for declaring the contrast non-identifiable; and
7. separate wording for survives, attenuates, source-sensitive, and invalid.

Nearest boundary:
C02. Adjustment can narrow a source explanation; it cannot prove causality.
```

This response evaluates the proposal, not the contributor.

## 5. The Repaired Test Card

The contributor returns a narrower version.

### Claim

In a named, legally usable dataset, does the proposed cell-state contrast
remain estimable among donors with source/outcome overlap, or is source too
aligned with outcome for that dataset to identify the contrast?

### Units And Inputs

- Independent unit: donor, not cell.
- Required fields: donor ID, outcome label, source/site/brain-bank label,
  expression-derived score fixed before this test, and quality covariates.
- Eligibility: one donor cannot appear in both training and held-out folds.
- Source/outcome cells and missing labels are tabulated before modeling.

### Pre-Specified Checks

1. Source/outcome overlap and concentration.
2. Donor-held-out source predictability from the candidate expression features.
3. A structure-preserving null that repeats every feature-selection and model
   step used in the diagnostic.
4. Raw, source-aware, and within-source or overlap-restricted outcome
   contrasts.
5. Leave-one-source-out sensitivity where the design permits it.

### Decision Rules

The exact numerical thresholds, model, feature set, and multiplicity family
must be fixed in the committed test plan before outcome inspection. This
worked example deliberately does not invent them.

The interpretation categories are fixed now:

- **survives source-aware checks**;
- **attenuates but leaves a bounded association**;
- **source-sensitive or non-identifiable**;
- **not supported under the eligible design**; or
- **invalid/unscoreable input**.

### Drop Rule

Drop the strong disease-specific interpretation if source/outcome overlap is
insufficient or if the eligible within-source estimate cannot separate the
proposed contrast from source. Do not relabel that outcome as “biology absent.”

## 6. Second Review

After the repaired card, the gates may pass **only if** the actual dataset,
permissions, fields, overlap, and frozen code are verified. A well-written card
without reachable inputs remains a data request, not a runnable analysis.

Possible action sequence:

```text
design repair -> data request -> frozen runnable test
```

No step in that sequence increases scientific support.

## 7. Hypothetical Outcome Branches

These branches teach interpretation. They are not observed outcomes.

### Branch A: The Contrast Survives

**Hypothetical pattern:** source/outcome overlap is adequate; the diagnostic
does not reveal a source-only explanation; and the fixed contrast remains in
the same direction under eligible within-source and leave-source checks.

**Allowed response:**

> The association survived the pre-specified source diagnostics in this
> dataset. This narrows source-only explanations within the observed overlap.
> It remains an association and still requires donor replication and any
> claim-specific progression or mechanism evidence.

**Forbidden upgrade:** “The classifier proved the cell state causes MS or
progression.”

### Branch B: The Result Attenuates

**Hypothetical pattern:** adjustment and within-source analysis reduce the
contrast, but uncertainty still permits a smaller association.

**Allowed response:**

> The original effect was partly source-sensitive. A smaller, quality-qualified
> association remains possible; the broad interpretation is downgraded.

**Decision:** narrow the claim and size a source-balanced replication. Do not
select the least attenuated model as the new primary analysis.

### Branch C: Source And Outcome Cannot Be Separated

**Hypothetical pattern:** one outcome is concentrated in one source, overlap is
insufficient, or a source-held-out contrast cannot be estimated.

**Allowed response:**

> This package cannot identify the disease contrast separately from source.
> The result is source-sensitive or data blocked, not a biological null.

**Decision:** stop biological interpretation for this package and request a
source-balanced donor design. `[C02]`

### Branch D: A Fair Eligible Test Is Null

**Hypothetical pattern:** overlap and quality are adequate, but the fixed
within-source contrast does not support the proposed association at the
detectable scale.

**Allowed response:**

> The pre-specified eligible test did not support this association in the
> tested dataset. This is evidence against transport of the stated contrast,
> not proof that every related biological process is absent.

**Decision:** close or narrow this exact transport claim. Do not repeat model
variants until one passes.

### Branch E: The Package Is Invalid

**Hypothetical pattern:** donor IDs, source labels, permissions, or required
measurements are missing or inconsistent.

**Allowed response:**

> The input is invalid or unscoreable for this test. No biological conclusion
> is permitted.

**Decision:** repair intake or stop. Invalid is different from null.

## 8. Example Public Closure Note

```markdown
Proposal status: Grounded test completed
Action before run: Runnable after design repair and data verification
Observed result class: <one fixed category>
Evidence source: <committed real-data run and artifact links>
Permitted claim: <one bounded sentence>
Nearest overread rejected: <cause / target / progression / absent biology>
Decision: <advance / narrow / request data / close / repair>
Reopening evidence: <specific new design or result>
```

The phrase “observed result” must not be filled from one of this page's
hypothetical branches. It belongs only to a real, committed run.

## 9. What This Example Teaches

1. A valuable outside method can arrive wrapped in an overclaim.
2. Repair should name missing fields rather than ask for vague “more detail.”
3. Workflow progress does not increase evidence.
4. Source adjustment is not a machine for manufacturing causal truth.
5. Every valid branch changes a decision, including null, non-identifiable, and
   invalid outcomes.
6. The final response grades the tested claim, not the contributor.

## Continue

- [Submit an idea](HOW_TO_CONTRIBUTE_IDEAS.md)
- [Read the response lifecycle](WHAT_HAPPENS_TO_YOUR_IDEA.md)
- [Use the triage rubric](IDEA_TRIAGE_RUBRIC.md)
- [Read the real brain-bank confound case](CASE_STUDY_BRAIN_BANK_CONFOUND.md)
