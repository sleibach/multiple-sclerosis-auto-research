# Validation Harness README V45

## Purpose

Make future validation runs mechanical and auditable. This document points to
the frozen plans, exact runnable commands, expected input schemas, and output
locations. It does not change any locked rule or pre-registration.

## Immutable Inputs

Primary treatment-response validation:

- locked rule: `docs/locked_rules/LOCKED_RULE_V22.md`
- frozen preregistration: `docs/validation/PREREGISTRATION_V42.md`
- interpretation grid: `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- executable harness: `scripts/v42_gafson_validation_harness.py`
- batch-hardening addendum: `docs/validation/BATCH_GUARD_V44.md`

Secondary live leads:

- postpartum APC-arm preregistration:
  `docs/validation/POSTPARTUM_APC_ARM_PREREGISTRATION_V44.md`
- T/B compartment preregistration:
  `docs/validation/TB_COMPARTMENT_PREREGISTRATION_V44.md`
- synthetic mechanics harness:
  `scripts/v44_secondary_lead_harnesses.py`

## Quarantine Rule

Any newly received cohort must first be placed under a quarantined data path and
checksummed before analysis. Do not inspect outcome-associated expression
patterns manually before running the frozen harness.

Suggested layout:

```text
data/quarantine/<cohort_name>/
  raw/
  processed/
  metadata/
  checksums.sha256
```

## Primary V22/V42 Harness

### Synthetic Self-Test

Run this before any real validation:

```bash
.venv/bin/python scripts/v42_gafson_validation_harness.py synthetic-check \
  --outdir analysis/v42_harness_validation
```

Required behavior:

- synthetic null does not pass;
- synthetic planted signal passes;
- all expected output tables are written.

### Real Cohort Command Template

```bash
.venv/bin/python scripts/v42_gafson_validation_harness.py run \
  --expression data/quarantine/<cohort>/processed/expression.tsv \
  --metadata data/quarantine/<cohort>/metadata/sample_metadata.tsv \
  --outdir analysis/validation_runs/<cohort> \
  --expression-type auto
```

Allowed `--expression-type` values:

- `auto`
- `raw_counts`
- `normalized_log`

### Primary Inputs

Schema files:

- `docs/validation/input_schemas/V45_primary_expression_schema.tsv`
- `docs/validation/input_schemas/V45_primary_metadata_schema.tsv`

Expression matrix:

- TSV;
- rows are genes/features;
- columns are sample IDs;
- first column is the gene identifier;
- raw counts or normalized log expression are acceptable if declared.

Metadata:

- TSV;
- one row per sample;
- required columns: `sample_id`, `patient`, `timepoint`, `response`;
- strongly required for interpretability: `days_since_treatment`, batch/QC,
  steroid exposure, prior/concomitant therapy, and clinical outcome window.

### Primary Outputs

The harness writes:

- `validation_summary.json`
- `paired_module_deltas.tsv`
- `gene_mapping_coverage.tsv`
- `sample_attrition.tsv`
- `locked_rule_metrics.tsv`
- `confounder_adjustment_metrics.tsv`
- `joint_confounder_metrics.tsv`
- `batch_diagnostic_metrics.tsv`

Interpretation must follow `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
and the V44/V45 batch-diagnostic notes. A raw pass with batch flags is not a
clean validation.

## Secondary Lead Inputs

The V44 secondary lead harness currently verifies synthetic mechanics. The real
cohort ingestion schemas are frozen here so implementation can be mechanical
when suitable data arrive.

Schema files:

- `docs/validation/input_schemas/V45_postpartum_apc_arm_schema.tsv`
- `docs/validation/input_schemas/V45_tb_compartment_schema.tsv`

### Postpartum APC-Arm Expected Table

One row per subject, with late-pregnancy and early-postpartum APC-arm scores or
the expression/features needed to compute them. Required outcome is relapse
status through the pre-specified postpartum window.

Primary fixed score:

```text
postpartum_apc_risk_score =
  -[(postpartum_6w_HLAII_minus_CD64) - (late_pregnancy_HLAII_minus_CD64)]
```

### T/B Compartment Expected Table

One row per subject, with baseline-to-early-treatment locked deltas separately
for B/plasma-like and T-like compartments plus compartment fractions/counts.

Primary fixed readouts:

```text
B/plasma-like locked_delta = delta_HLAII - delta_IFN_APC
T-like locked_delta        = delta_HLAII - delta_IFN_APC
```

## Non-Negotiable Diagnostics

Every validation package must include enough metadata to assess:

- response-correlated batch;
- steroid/glucocorticoid exposure;
- immune-tone/confounder panels where expression supports them;
- missing timepoints;
- gene/module coverage;
- outliers and normalization pathologies;
- cell composition or compartment fraction shifts where relevant.

## Current Implementation Status

Primary V22/V42 real-cohort harness is executable now.

Secondary lead real-cohort ingestion is executable through
`scripts/v45_secondary_real_cohort_harness.py`; see
`docs/validation/SECONDARY_REAL_INGEST_HARNESS_V45.md`. The harness consumes the
frozen V45 subject-level schemas and passed synthetic null/planted checks for
both postpartum APC-arm and T/B compartment readouts. It remains future-data
infrastructure only; no real matching cohort has been opened by this checkpoint.

Pharmacodynamic-only context cohorts are executable through
`scripts/v45_pharmacodynamic_only_harness.py`; see
`docs/validation/PHARMACODYNAMIC_ONLY_HARNESS_V45.md`. This harness summarizes
frozen V22 module trajectories and QC context only. It explicitly reports
`response_validation_performed: false` and must not be used for response,
NEDA, relapse, remission, or patient-stratification claims.
