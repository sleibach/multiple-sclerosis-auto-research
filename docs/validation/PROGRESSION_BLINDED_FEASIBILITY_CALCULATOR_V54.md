# V54 Blinded Progression Feasibility Calculator

Status: frozen metadata-only routing contract. It changes no locked rule,
endpoint, or pre-registration.

## Purpose

This calculator composes the V54 intake boundaries into one blinded design
classification. It reads no molecular values and no subject-level outcomes. A
result says whether a received design is valid enough for cohort-specific
power work and how it compares with the assumption-labeled V54 reference. It
does not determine whether a molecular score works or whether a study will be
positive.

## Required Inputs

The declaration supplies:

- a package ID, blind-freeze source, role, and explicit score/outcome access
  flags;
- paths to the actual combined-intake, event-time, and site-score gate summary
  JSON files;
- blinded aggregate planned enrollment, analyzable count, confirmed-event
  target, event-probability assumption, site targets, visit interval, follow-up,
  score-reliability assumption, repeat plan, and independent-error status;
- confirmation that cohort-specific power will be rerun and that the primary
  site/source/treatment-stratified model is pre-specified.

The three upstream summaries must exist, carry the same package ID, and have an
allowed pass decision. A copied decision string is insufficient.

## Classification

- `FAIL_CLOSED`: an upstream gate fails, package IDs do not bind, fields are
  malformed, scores/outcomes were inspected before freeze, or the primary
  stratified/power-rerun plan is absent.
- `REFERENCE_ALIGNED_FOR_COHORT_SPECIFIC_POWER`: all validity gates pass and
  the blind plan meets the tested reference cells: at least 450 analyzable,
  135 confirmed events, three equal targets of at least 150, event assumption
  at least 0.30, quarterly-or-more-frequent visits, at least two years of
  follow-up, and a reliability/repeat plan inside the audited envelope.
- `REFERENCE_ALIGNED_SENSITIVITY_REQUIRED`: the same alignment holds, but the
  event-time gate requires its pre-frozen sensitivity panel.
- `VALID_BELOW_REFERENCE_REPARAMETERIZE`: validity gates pass but one or more
  numerical reference cells do not. This is not failure; rerun the frozen
  cohort-specific power/null grids before accessing scores or outcomes.

Reference alignment is not validation readiness, transport, efficacy, or
evidence. The reference is synthetic and conditional, not a universal minimum.

## Machine Check

```bash
.venv/bin/python scripts/v54_progression_blinded_feasibility.py
```

For a quarantined package:

```bash
.venv/bin/python scripts/v54_progression_blinded_feasibility.py \
  --declaration path/to/blind_feasibility_declaration.json \
  --output-dir path/to/feasibility_result --fail-on-error
```

The default regression uses nine explicitly synthetic packages and synthetic
upstream summaries. It covers reference alignment, sensitivity-required
alignment, four below-reference routes, and three fail-closed routes. It tests
software behavior only.
