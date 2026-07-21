# V54 Blinded P1/P2 Progression Pre-Registration Contract

Status: frozen process contract. It does not pre-register a cohort that has not
arrived, create a progression finding, or alter any locked project rule. A
cohort-specific copy must be completed and committed while molecular scores and
individual outcome labels remain unread.

## Purpose

The P1 question is whether one pre-existing molecular state precedes confirmed
disability accumulation. The optional P2 question is whether that same
association differs between paired or prospectively harmonized CNS/CSF and
peripheral compartments. Neither question may be replaced by relapse activity,
cross-sectional disease stage, lesion morphology, imaging alone, or a
pharmacodynamic expression change.

This contract closes the gap between inventory completeness and endpoint
meaning. The inventory gate proves that named fields exist. The semantic gate
proves that the declared endpoint is an executable repeated-disability outcome.
Neither gate inspects or validates the biological result.

## Required Order Of Operations

1. Quarantine the received package and record its immutable manifest, checksum,
   access terms, and package identifier.
2. Run `scripts/v54_progression_package_eligibility_validator.py` without
   opening expression values or individual outcome labels.
3. From protocol documentation and data dictionaries only, complete a copy of
   `V54_progression_endpoint_declaration_template.tsv`.
4. Run `scripts/v54_progression_outcome_semantic_checker.py`. Any failure keeps
   the package context-only and triggers a source clarification request.
5. Use only blinded aggregate counts needed for a cohort-specific power
   simulation: total eligible subjects, event count, follow-up distribution,
   missingness, and planned covariate count. Do not inspect score distributions
   or subject-level score-outcome pairs.
6. Fill and commit every decision below, including one primary molecular state,
   one estimand, one analysis family, and pass/fail/inconclusive rules.
7. Record that scores and individual outcomes remained unread, rerun both
   gates, and only then execute the frozen analysis.

When follow-up is unequal or right-censored, the cohort-specific plan must use
the event-time route rather than silently collapsing to an equal-window binary
label. Source and treatment handling must be frozen from blinded metadata. The
V54 synthetic stress test shows that an unadjusted route can be anti-conservative
when the score is imbalanced across source/treatment; this is a method guard,
not a statement that a future cohort has that structure.

Any reversal of this order invalidates confirmatory status. The resulting work
may be reported only as explicitly post hoc and cannot satisfy P1 or P2.

## P1 Declaration

The cohort-specific declaration must freeze all of the following:

| decision | required content | fail-closed condition |
|---|---|---|
| outcome identity | exact CDP or PIRA protocol name and version | undocumented derived label |
| semantic basis | repeated measured disability | relapse, stage, morphology, imaging-only, or pharmacodynamic proxy |
| raw components | baseline and repeated EDSS plus T25FW/9HPT where collected | derived label without auditable components |
| confirmation | exact threshold, confirming measurement, and positive interval in days | transient or unconfirmed worsening |
| follow-up | baseline plus at least two independent post-baseline assessments | fewer than two follow-ups |
| window | start and end relative to molecular baseline | selected after score access |
| PIRA attribution | exact relapse and steroid exclusion, with event dates | absent dates or undefined exclusion |
| acute context | infection rule | outcome-dependent exclusion |
| treatment | switch, discontinuation, and adherence rule | post-result treatment handling |
| censoring | event, administrative, death, dropout, and missing rules | undocumented informative loss |
| molecular predictor | one pre-existing state, exact committed genes/formula, baseline and primary timepoint | feature search or replacement of missing genes |
| estimand | effect scale and fitted model, including event-time route when follow-up varies | changing endpoint or scale after seeing results |
| adjustment | fixed covariates, including source/batch and composition where available | outcome-driven covariate selection |
| multiplicity | positive integer analysis budget and exact correction | opportunistic secondary expansion |
| interpretation | exact pass, fail, and inconclusive rules | result-dependent narrative |

The leading progression-adjacent state currently eligible for a future P1 test
is the pre-existing two-gene `CD44/CXCR4` state, because it replicated as an MS
microglial disease-state association in V53. That eligibility is not a claim
that it predicts progression: V54 found no portable cross-sectional stage
association and no intervention direction. A future declaration must identify
the exact committed scoring artifact and must not rebuild the score in the new
cohort. If the received compartment cannot validly measure that frozen state,
P1 fails closed rather than substituting another state.

## P1 Outcome Interpretation

The cohort-specific plan must instantiate numerical thresholds from a blinded
power simulation. The interpretation classes are fixed now:

- **Pass:** the frozen effect has its pre-specified direction, passes the full
  corrected family, its uncertainty excludes the frozen null boundary, and all
  mandatory source/batch/composition and influence checks retain direction.
- **Fail:** the primary effect is wrong-direction, or its interval excludes the
  pre-specified minimum material effect in the favorable direction. This does
  not prove progression biology is absent; it rejects transport of the frozen
  state under the declared design.
- **Inconclusive:** the interval includes both the null and the minimum material
  effect, event count is below the pre-declared information floor, or a required
  data-quality sensitivity is unresolved. Only effect size and interval may be
  carried forward for study design.
- **Invalid:** semantic, provenance, source/batch, or blindness gates fail. No
  biological interpretation is permitted.

Fewer than 10 independent progression events is descriptive-only. Ten events is
an eligibility floor, not a power claim. The cohort-specific simulation decides
whether any confirmatory interpretation is possible.

## P2 Declaration

P2 is optional and cannot run unless the same package first passes P1 endpoint
semantics. It must additionally freeze:

1. paired-subject or prospectively harmonized compartment design;
2. identical endpoint definition and outcome window in both compartments;
3. subject/sample pairing and collection-time tolerance;
4. source, batch, cell-composition, treatment, age, and sex adjustment;
5. at least 10 independent subjects per outcome group in each compartment,
   followed by a cohort-specific interaction-power simulation;
6. one direct compartment-by-outcome interaction and its multiplicity budget.

Separate significance in one compartment and non-significance in another is not
a localization result. Only the frozen interaction is eligible. A P2 null with
wide uncertainty is inconclusive, not evidence of compartment equivalence.

## Explicitly Prohibited Analyses

- Treating relapse count or NEDA activity as disability progression.
- Ordering RRMS, SPMS, and PPMS cross-sections as a patient trajectory.
- Treating foamy/non-foamy morphology or chronic-active lesion class as elapsed
  progression time.
- Treating a treatment-induced expression change as clinical benefit.
- Reconstructing an undocumented progression label from whichever components
  yield the strongest association.
- Selecting molecular timepoints, transformations, covariates, compartments,
  or thresholds after inspecting score-outcome relationships.
- Calling different p-values across compartments an interaction.

## Machine Enforcement

The declaration schema and template are:

- `docs/validation/input_schemas/V54_progression_endpoint_declaration_fields.tsv`
- `docs/validation/input_schemas/V54_progression_endpoint_declaration_template.tsv`

Run:

```bash
.venv/bin/python scripts/v54_progression_outcome_semantic_checker.py
```

The default command runs synthetic regression fixtures. For a received package:

```bash
.venv/bin/python scripts/v54_progression_outcome_semantic_checker.py \
  --declaration path/to/frozen_endpoint_declaration.tsv \
  --expected-role P1 --output-dir path/to/semantic_audit --fail-on-error
```

Synthetic pass fixtures contain valid CDP, PIRA, and paired-compartment
declarations. Synthetic fail fixtures cover relapse-only, stage-only,
morphology-only, pharmacodynamic-only, unconfirmed, derived-label-only,
date-incomplete PIRA, interaction-free P2, and score-unblinded declarations.
These fixtures test method behavior only and contain no biological evidence.

## Boundary

Passing this pre-registration and semantic gate establishes only that a future
analysis is interpretable as a blinded test of longitudinal disability
progression. It does not establish that a molecular state predicts progression,
localizes to a compartment, identifies a causal mechanism, or can halt MS.
