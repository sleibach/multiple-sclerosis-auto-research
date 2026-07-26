# Case Study: A Snapshot Cannot Show A Progression Movie

Progression is a change over time. To test whether a molecular state predicts
that change, the state must be measured before later disability accumulates and
remains confirmed. A disease-stage label, lesion image, or one-time disability
score can be informative without answering that longitudinal question.

This page restates the V54 progression boundary. It adds no new scientific
claim. `[B02, P01-P06]`

## The Short Version

The project audited seven held progression-adjacent datasets. Some contain
brain or lesion snapshots. Two contain repeated transcriptomes. Some contain a
baseline disability score, relapse follow-up, or treatment timepoints. None
links repeated molecular state to changing MS stage plus repeated confirmed
disability or an adjudicated conversion event. `[P01, P03]`

Therefore the project did **not** establish:

- a molecular predictor of disability progression;
- a relapsing-to-progressive transition state;
- a causal progression mechanism;
- a direction-resolved progression target;
- a treatment effect on progression; or
- a means of halting MS progression. `[P02]`

This is a data-design boundary, not evidence that progression biology does not
exist.

## Snapshot And Movie

A snapshot can answer:

- What differs between groups at one observed time?
- What molecular state appears in a lesion or cell compartment?
- Which stage label was assigned to a donor?

A progression movie must answer:

- What molecular state was present first?
- What happened to disability afterward?
- Was the change repeated and confirmed?
- When did relapses, steroids, treatment switches, missed visits, censoring,
  and competing events occur?
- Does the relationship transport across sites and compartments?

The second set cannot be reconstructed reliably from the first.

## The Intended Question

The progression question has a time order:

```text
earlier molecular state
    -> later disability accumulation
        -> repeat assessment confirms the change
```

The arrow is not established merely because two groups differ after years of
disease. A cross-sectional difference can reflect cause, consequence,
treatment history, duration, survival, tissue source, or another linked
factor.

## Six Tempting Substitutions That Do Not Work

### 1. Progressive Subtype At One Time

A PPMS-versus-SPMS comparison can describe a cross-sectional stage association.
It cannot observe a person's transition from relapsing to progressive disease
or estimate progression rate. In the held source-restricted comparison, no
pre-existing module passed the full portability gate. `[P02-P03]`

### 2. Postmortem Lesion Morphology

Chronic-active lesion edges or foamy-microglia morphology can describe tissue
context at death. They do not show the earlier state of a living person or
whether that state predicted subsequent confirmed disability. The attractive
OXPHOS/lysosomal morphology result weakened under global multiplicity and
within-donor checks. `[P04]`

### 3. Repeated Expression Plus Relapse Follow-Up

GSE24427 contains repeated blood measurements and two-year relapse outcomes,
but its disability score is baseline-only and no subtype conversion is
observed. Relapse activity and disability progression are related but not
interchangeable endpoints. `[B02, P03]`

### 4. Treatment-Response Timepoints

Repeated samples after treatment can measure pharmacodynamic change. They do
not become progression data unless later confirmed disability is measured
under a compatible longitudinal design. The V22 monitoring lead remains a
separate question. `[M05, P05]`

### 5. One Disability Score

A single EDSS or other disability value describes one assessment. Progression
requires change and confirmation. Without repeated components and dates, the
project cannot distinguish persistent accumulation from baseline severity,
temporary worsening, relapse-associated change, or measurement noise.

### 6. A Familiar Score In The Wrong Compartment

The exact `CD44`/`CXCR4` microglia score is preserved as a future candidate by
identity only. Its old disease-association model and thresholds do not transfer
to progression. It is not licensed for PBMC, whole blood, bulk CSF, substitute
genes, or another compartment just because those genes can be measured.
`[P06]`

## What The Held Data Could Test

V54 allowed only bounded questions the designs could identify:

- source-restricted cross-sectional PPMS-versus-SPMS module differences;
- donor-aware lesion and morphology contrasts;
- source, donor, multiplicity, and transport sensitivity; and
- whether an existing package met the metadata contract for a future role.

These tests produced useful negatives and boundaries. They did not inherit a
progression interpretation merely because progression motivated them.

## The Three Required Evidence Roles

### P1: Predict The Longitudinal Outcome

Follow people over time. Test whether a frozen molecular state measured first
predicts later confirmed disability under precommitted endpoint, covariate,
null, and interpretation rules.

### P2: Localize The State

Only after P1, use a compatible phenotype and harmonized compartments to test
where the state resides. A different cohort cannot localize the P1 result if it
does not share the phenotype and timing logic.

### P3: Establish Functional Direction

Only after P1/P2, perturb the relevant state or node. Require a selective,
direction-matched effect with collateral-function controls before discussing a
target.

Among ten known candidate packages, zero currently qualifies for P1, P2, or
P3. That is an acquisition result, not a biological null. `[P05]`

## The Minimum Useful Progression Movie

The shortest credible P1 package needs:

1. Stable person identifiers and repeated molecular samples.
2. Baseline plus at least two follow-up disability assessments.
3. Raw disability components and dates, not only a derived label.
4. A documented confirmed-disability or PIRA adjudication procedure.
5. Relapse, steroid, treatment, switch, attendance, censoring, and death dates.
6. Site, batch, source, quality, and composition provenance.
7. Enough events and site overlap for the frozen analysis and holdout checks.
8. A microglia-compatible compartment if the exact `CD44`/`CXCR4` candidate is
   being tested. `[A02, P06]`

Receipt of these fields would permit blinded eligibility checks. It would not
guarantee a positive result.

## What A Valid Future Result Could Mean

### Bounded Pass

The frozen state predicts the pre-specified confirmed-disability outcome in
that cohort and survives the required controls. This would be predictive
association transport, not a mechanism, target, treatment effect, or halt
strategy.

### Fail

The state does not satisfy the frozen progression gate in an eligible cohort.
That would close or narrow this candidate, not prove all progression biology
absent.

### Inconclusive

The effect and uncertainty do not satisfy pass or fail. Report both and use
them to plan a later cohort; do not change score, endpoint, subgroup, or time
window after seeing the result.

### Invalid Or Unscoreable

The package lacks required timing, endpoint, compartment, provenance, or
process integrity. No biological conclusion is allowed.

## Questions A New Method Must Answer

A clever algorithm cannot repair a missing time order. Before proposing a
progression analysis, ask:

1. Which variable is measured before the outcome?
2. What exactly counts as disability accumulation?
3. How and when is it confirmed?
4. Which events can mimic or obscure progression?
5. Are repeated samples and outcomes linked to the same person?
6. Can source, site, treatment, and follow-up patterns be separated from the
   proposed molecular effect?
7. Is the cell or tissue compartment compatible with the frozen state?
8. What result would close the candidate?

If the dataset cannot answer those questions, the useful contribution is a
better acquisition or design plan, not a more flexible model.

## The Honest Frontier

The project has one identity-only microglial candidate and a mature frozen
intake/analysis path, but no eligible progression cohort and no progression
finding. The next move is new longitudinal data with the right outcome and
provenance. More analysis of unmatched snapshots cannot substitute. `[P01-P06,
A02]`

## Trace The Evidence

- [V54 progression frontier](../history/PROGRESSION_FRONTIER_V54.md)
- [V54 run summary](../history/V54_RUN_SUMMARY.md)
- [Transition identifiability audit](../../analysis/v54_transition_identifiability/REPORT.md)
- [Progression cohort role matrix](../validation/PROGRESSION_COHORT_ROLE_MATRIX_V54.md)
- [P1 candidate-state identity handoff](../validation/PROGRESSION_P1_CANDIDATE_STATE_HANDOFF_V54.md)
- [Claim-source contract](CLAIM_SOURCE_MATRIX_V55.md), rows `B02`, `P01-P06`,
  and `A02`
