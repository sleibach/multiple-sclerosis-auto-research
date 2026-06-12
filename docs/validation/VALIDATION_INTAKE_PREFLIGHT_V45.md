# Validation Intake Preflight V45

## Purpose

`scripts/v45_validation_intake_preflight.py` is a quarantine-stage guard that
must run before any frozen validation or context harness touches a newly
received cohort. It checks file integrity, metadata schema compatibility,
optional expression-sample matching, and response-label guardrails. It does not
compute module scores, fit models, or produce biological evidence.

This is infrastructure only. It does not change the locked V22 rule, the V42
pre-registration, or any secondary-lead pre-registration.

## Command Templates

Primary V22/V42 treatment-response validation package:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/<cohort> \
  --mode primary \
  --metadata data/quarantine/<cohort>/metadata/sample_metadata.tsv \
  --expression data/quarantine/<cohort>/processed/expression.tsv \
  --outdir analysis/intake_preflight/<cohort> \
  --write-checksums
```

Secondary postpartum APC-arm package:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/<cohort> \
  --mode postpartum \
  --metadata data/quarantine/<cohort>/metadata/postpartum_subjects.tsv \
  --outdir analysis/intake_preflight/<cohort> \
  --write-checksums
```

Secondary T/B compartment package:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/<cohort> \
  --mode tb \
  --metadata data/quarantine/<cohort>/metadata/tb_subjects.tsv \
  --outdir analysis/intake_preflight/<cohort> \
  --write-checksums
```

Pharmacodynamic-only context package:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/<cohort> \
  --mode pharmacodynamic \
  --metadata data/quarantine/<cohort>/metadata/sample_metadata.tsv \
  --expression data/quarantine/<cohort>/processed/expression.tsv \
  --outdir analysis/intake_preflight/<cohort> \
  --write-checksums
```

For pharmacodynamic-only packages, response-like metadata columns are a hard
failure by default. This prevents an unlabeled context run from silently becoming
a response-validation analysis. The override flag
`--allow-response-columns-for-pharmacodynamic` is reserved for manual audit only;
it must not be used to claim response validation without a separate frozen
pre-registration.

## Outputs

Each preflight run writes:

- `preflight_summary.json`
- `preflight_checks.tsv`
- `checksum_audit.tsv`
- `schema_check.tsv`
- `response_guard.tsv`
- `expression_header_check.tsv`

The frozen harness may run only when `preflight_summary.json` reports
`overall_status: PASS`. A failed preflight is not a biological result; it is an
intake-quality blocker.

## Synthetic Verification

The committed synthetic verification was run with:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py synthetic-check \
  --outdir analysis/v45_validation_intake_preflight
```

Results:

- primary synthetic preflight: `PASS`
- pharmacodynamic-only synthetic preflight without response-like labels: `PASS`
- pharmacodynamic-only synthetic preflight with a response-like column: `FAIL`
- module-score computation: not performed

The assertion file is
`analysis/v45_validation_intake_preflight/synthetic_check_assertions.json`:

```json
{
  "no_module_scores_computed": true,
  "pharmacodynamic_preflight_pass": true,
  "pharmacodynamic_response_label_guard_fails": true,
  "primary_preflight_pass": true,
  "synthetic": true
}
```

## Interpretation

This preflight narrows operational risk before validation:

- checksums make received data packages auditable;
- schema checks catch missing required metadata before any scoring;
- expression-header checks catch sample-ID mismatches;
- pharmacodynamic response-label guardrails preserve the no-response-claim rule
  for open context-only cohorts such as GSE228330.

It is intentionally conservative and additive. It is not a substitute for the
V42 frozen analysis plan or any lead-specific harness.
