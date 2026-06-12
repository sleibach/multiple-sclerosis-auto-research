# Metadata Missingness Scorer V45

Status: metadata-only reporting helper. No expression data, module scores, or
outcome labels are read by this script.

Purpose: operationalize
`docs/validation/BATCH_QC_STEROID_MISSINGNESS_RUBRIC_V45.md` by mapping metadata
field presence/missingness to green/yellow/orange/red report constraints before
final validation wording.

## Commands

Score a received metadata file:

```bash
.venv/bin/python scripts/v45_metadata_missingness_scorer.py score \
  --metadata data/quarantine/<cohort>/metadata/sample_metadata.tsv \
  --outdir analysis/validation_command_runs/metadata_missingness/<cohort>
```

Synthetic check:

```bash
.venv/bin/python scripts/v45_metadata_missingness_scorer.py synthetic-check \
  --outdir analysis/v45_metadata_missingness_scorer
```

## Current Synthetic Verification

| Fixture | Overall report status | Meaning |
|---|---|---|
| complete synthetic metadata | `METADATA_SUPPORTS_CLEAN_INTERPRETATION` | metadata do not impose an added reporting downgrade |
| weak synthetic metadata | `METADATA_WEAK_FOR_CLEAN_PASS` | a positive result could not be described as clean |

The weak fixture omits exact timing, major batch fields, direct steroid fields,
core QC fields, and direct composition counts. It remains scoreable only as a
metadata/reporting exercise and is not biological evidence.

## Panels Scored

The scorer writes one row per panel:

- core pairing;
- early timepoint;
- batch diagnostic;
- steroid metadata;
- QC metadata;
- composition context;
- overall.

## Interpretation

A green overall status means metadata missingness does not add a separate
reporting downgrade. It still does not make the cohort pass the locked rule.

Yellow/orange statuses constrain wording in the future validation report. In
particular, `METADATA_WEAK_FOR_CLEAN_PASS` means a favorable raw score cannot be
called a clean technical/confounder-adjusted pass.

Red status blocks scoring or clean interpretation and should be handled as a
repair/unscoreable-data path under the V45 failure taxonomy.

## Guardrail

This script is additive and blind. It does not:

- alter the locked score or threshold;
- drop samples based on scores/outcomes;
- impute missing technical metadata;
- open raw expression data;
- infer steroid or batch status from module behavior.
