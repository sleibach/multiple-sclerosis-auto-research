# Secondary Real-Cohort Ingest Harness V45

Status: validation infrastructure. This artifact does not change any locked
rule, frozen pre-registration, threshold, or biological claim.

## Purpose

V44 pre-registered two secondary live leads:

- postpartum HLA-II/CD64 APC-arm relapse-window hypothesis;
- T/B-readable treatment-response monitoring state.

V45 froze their subject-level input schemas, but the real-cohort ingestion
scripts were still missing. This checkpoint implements that missing mechanical
layer so a future matching cohort can be run without inventing analysis choices
after the data arrives.

## Script

`scripts/v45_secondary_real_cohort_harness.py`

The script has three subcommands:

```bash
.venv/bin/python scripts/v45_secondary_real_cohort_harness.py postpartum \
  --input data/quarantine/<cohort>/processed/postpartum_apc_arm_subject_table.tsv \
  --outdir analysis/validation_runs/<cohort>_postpartum_apc_arm
```

```bash
.venv/bin/python scripts/v45_secondary_real_cohort_harness.py tb \
  --input data/quarantine/<cohort>/processed/tb_compartment_subject_table.tsv \
  --outdir analysis/validation_runs/<cohort>_tb_compartment
```

```bash
.venv/bin/python scripts/v45_secondary_real_cohort_harness.py synthetic-check \
  --outdir analysis/v45_secondary_real_ingest
```

Input schemas:

- `docs/validation/input_schemas/V45_postpartum_apc_arm_schema.tsv`
- `docs/validation/input_schemas/V45_tb_compartment_schema.tsv`

## Frozen Readouts Implemented

Postpartum APC-arm:

```text
postpartum_apc_risk_score =
  -[(postpartum_6w_HLAII_minus_CD64) - (late_pregnancy_HLAII_minus_CD64)]
```

Primary orientation: higher score predicts postpartum relapse.

T/B compartment:

```text
B/plasma-like locked_delta = delta_HLAII - delta_IFN_APC
T-like locked_delta        = delta_HLAII - delta_IFN_APC
```

Primary orientation: higher B/plasma-like and T-like locked deltas predict
response.

No fitted weights, refitting, or post-hoc feature selection are implemented.

## Diagnostics Implemented

Postpartum:

- AUC, Hedges g, bootstrap AUC CI;
- steroid + DMT restart residual AUC;
- HLA-II/CD64 coverage flag;
- response-correlated batch guard;
- strongly-required metadata completeness audit;
- fixed interpretation label.

T/B compartment:

- B/plasma-like and T-like AUCs, Hedges g, bootstrap AUC CIs;
- B/plasma-like and T-like residual AUCs after compartment fractions;
- B/plasma-like batch guard;
- B/T compartment coverage flag;
- strongly-required metadata completeness audit;
- fixed interpretation label.

Missing strongly-required fields do not erase the raw result, but they prevent a
clean guarded pass. This is an additive readiness hardening consistent with the
V44/V45 diagnostic requirements.

## Outputs

For each real run, the harness writes:

- `validation_summary.json`
- `metrics.tsv`
- `subject_scores.tsv`
- `input_qc.tsv`
- `batch_diagnostic_metrics.tsv`

## Synthetic Verification

Run:

```bash
.venv/bin/python scripts/v45_secondary_real_cohort_harness.py synthetic-check \
  --outdir analysis/v45_secondary_real_ingest --n-boot 300
```

Synthetic outputs are under `analysis/v45_secondary_real_ingest/` and are
clearly labeled synthetic.

Checks:

| Scenario | Expected | Observed |
|---|---|---|
| postpartum null | fail | fail |
| postpartum planted | pass | pass |
| T/B null | fail | fail |
| T/B planted | pass | pass |

Key synthetic metrics:

- postpartum null AUC `0.5078`, guarded clean pass `false`;
- postpartum planted AUC `0.9933`, guarded clean pass `true`;
- T/B null B/plasma AUC `0.4156`, guarded clean pass `false`;
- T/B planted B/plasma AUC `0.9511`, guarded clean pass `true`.

Synthetic data are method checks only. They are not evidence about MS.

## Interpretation

The secondary leads are now mechanically runnable on future subject-level
cohorts matching the frozen V45 schemas. A clean pass from this script would
still be a secondary validation result, not a change to the primary V22 scalar
treatment-response rule.

