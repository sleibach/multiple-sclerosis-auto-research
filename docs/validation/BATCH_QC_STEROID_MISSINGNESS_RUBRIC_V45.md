# Batch/QC/Steroid Missingness Severity Rubric V45

Status: validation-report interpretation rubric. No data received or analyzed.

Purpose: pre-specify how missing or incomplete batch, QC, steroid, and
cell-composition metadata will constrain interpretation of a future frozen
validation report. This rubric is additive and blind; it does not change
`LOCKED_RULE_V22.md`, `PREREGISTRATION_V42.md`, or any pass/fail threshold.

Machine-readable rubric:

`docs/validation/input_schemas/V45_metadata_missingness_severity_rubric.tsv`

Metadata-only scoring helper:

`docs/validation/METADATA_MISSINGNESS_SCORER_V45.md`

## Why This Exists

V32 found that the V22 signal is not a steroid or cell-composition artifact in
the audited small cohorts, but it remains immune-tone bounded. V43/V44 synthetic
stress tests showed that response-correlated batch structure is the main
method-level false-positive risk. Therefore the future validation report must
state, before seeing results, how missing batch/QC/steroid metadata affects
interpretation.

## Severity Levels

| Severity | Meaning |
|---|---|
| `green` | metadata are sufficient for the named audit |
| `yellow_limited` | metadata are usable but incomplete; interpretation needs a limitation |
| `orange_weak` | metadata are too incomplete for a clean audit, but core scoring may still run |
| `red_unscoreable` | metadata failure blocks scoring or blocks any clean validation interpretation |

## Panel Rules

### Core Pairing

Missing `sample_id`, `subject_id`, or `timepoint` is a hard blocker. Without
those fields, paired baseline/early deltas cannot be established and the package
is `UNSCOREABLE_DATA`.

### Early Timepoint

If exact treatment-relative days are absent but labels uniquely identify
baseline and earliest eligible on-treatment samples, scoring can proceed with a
timing caveat. If multiple early candidates exist and days are absent, stop
before scoring until the author clarifies the earliest eligible sample or a
blind addendum is committed.

### Batch Diagnostic

At least one major technical batch field should be present: `processing_batch`,
`library_prep_batch`, `sequencing_lane`, `plate_or_array_id`, or equivalent.
If no major batch field is present, batch false-positive risk cannot be ruled
out directly. A raw pass under that condition must not be described as
technically clean.

### Steroid Metadata

The preferred clinical steroid fields are `steroid_exposure_recent` and
`steroid_last_dose_days`. If both are absent, the validation can still report
the expression-based glucocorticoid audit, but it must not claim direct clinical
steroid exclusion.

### QC Metadata

RNA quality and sequencing-depth/platform-equivalent QC fields are needed to
interpret technical quality. If missing, report QC audit as unavailable and do
not infer sample quality from a favorable score.

### Composition Context

Direct CBC/cell-count covariates are preferred. If absent, expression-marker
composition scores are acceptable only when marker coverage passes. If both
direct counts and marker coverage are inadequate, no clean composition-adjusted
interpretation is allowed.

## Overall Interpretation

| Overall state | Reporting consequence |
|---|---|
| `METADATA_SUPPORTS_CLEAN_INTERPRETATION` | use the V42 result class from the frozen harness and report rubric status |
| `METADATA_LIMITED` | score can be reported, but limitations must accompany any positive result |
| `METADATA_WEAK_FOR_CLEAN_PASS` | score may be reported, but a positive result is bounded/non-clean under the V42 grid and audit outputs |
| `METADATA_UNSCOREABLE` | stop or classify as `UNSCOREABLE_DATA`; do not report a biological result |

## Guardrail

This rubric constrains wording and readiness only. It does not permit:

- dropping samples based on outcome/score behavior;
- inventing alternative batch corrections after seeing results;
- weakening the frozen V42 thresholds;
- calling a result clean when key confounder metadata are unavailable.
