# V45 Compute and Storage Summary

Status: storage/transparency artifact. No biological claim.

## Purpose

V45 generated many synthetic and regression outputs. This summary records the
analysis-output footprint so reviewers can see what was produced, how large it
is, and how it should be interpreted.

Generator:

`scripts/v45_compute_storage_summary.py`

Outputs:

- `analysis/v45_compute_storage_summary/v45_analysis_storage_by_dir.tsv`
- `analysis/v45_compute_storage_summary/v45_analysis_storage_by_class.tsv`
- `analysis/v45_compute_storage_summary/summary.json`

## Current Footprint

| Metric | Value |
|---|---:|
| V45 analysis directories | 84 |
| files | 799 |
| total size | 85.969 MiB |
| synthetic/method-behavior size | 84.379 MiB |

By class:

| Class | Directories | Files | Size MiB |
|---|---:|---:|---:|
| synthetic / method behavior | 16 | 300 | 84.379 |
| infrastructure / documentation | 47 | 408 | 0.637 |
| public metadata / operations | 9 | 40 | 0.245 |
| internal / governance | 12 | 51 | 0.634 |

Largest directories:

| Directory | Class | Files | Size MiB |
|---|---|---:|---:|
| `analysis/v45_tb_compartment_pathology` | synthetic/method behavior | 4 | 24.176 |
| `analysis/v45_multiconfounder_batch_guard` | synthetic/method behavior | 5 | 21.311 |
| `analysis/v45_postpartum_pathology` | synthetic/method behavior | 4 | 20.358 |
| `analysis/v45_seed_variation_stability` | synthetic/method behavior | 5 | 8.763 |
| `analysis/v45_secondary_batch_calibration` | synthetic/method behavior | 3 | 4.098 |

## Interpretation Boundary

The large V45 footprint is mostly synthetic method-characterization and
regression infrastructure. It supports statements about:

- harness behavior under null/planted/pathology conditions;
- software guardrail reproducibility;
- acquisition/readiness operations;
- storage and auditability.

It does **not** support statements about:

- MS biology;
- clinical validation;
- treatment efficacy;
- response prediction in any real patient cohort.

## Retention Note

These outputs are useful during the delayed-data period because they make the
validation boundary reproducible. If storage pressure arises later, prioritize
retaining:

1. scripts/generators;
2. summaries and metrics TSVs;
3. synthetic seeds/configs;
4. docs explaining interpretation.

Large per-subject synthetic tables can be regenerated from committed scripts if
needed, but should not be pruned during the active V45 block.
