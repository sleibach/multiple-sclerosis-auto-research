# Pharmacodynamic-Only Harness V45

Status: context-only validation infrastructure. This artifact does not validate
or falsify the locked V22 treatment-response rule.

## Purpose

Open longitudinal cohorts such as `GSE228330` can reduce single-cohort
dependence for platform and pharmacodynamic context, but they lack public
sample-mapped response labels. The V45 pharmacodynamic-only harness makes those
cohorts usable without crossing into response-validation claims.

## Script

`scripts/v45_pharmacodynamic_only_harness.py`

Allowed real-cohort command:

```bash
.venv/bin/python scripts/v45_pharmacodynamic_only_harness.py run \
  --metadata data/quarantine/<cohort>/metadata/pharmacodynamic_metadata.tsv \
  --expression data/quarantine/<cohort>/processed/expression.tsv \
  --outdir analysis/pharmacodynamic_context/<cohort> \
  --expression-type auto
```

If frozen module scores have already been computed without response labels:

```bash
.venv/bin/python scripts/v45_pharmacodynamic_only_harness.py run \
  --metadata data/quarantine/<cohort>/metadata/pharmacodynamic_metadata.tsv \
  --module-scores data/quarantine/<cohort>/processed/module_scores.tsv \
  --outdir analysis/pharmacodynamic_context/<cohort>
```

Input schema:

- `docs/validation/input_schemas/V45_pharmacodynamic_only_schema.tsv`

## Frozen Modules

The harness uses the frozen V22 modules for context-only scoring:

- IFN/APC: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`
- HLA-II: `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`,
  `HLA-DQB1`
- receptor-only: `CD74`, `CD44`, `CXCR4`

For expression-matrix input, genes are z-scored across analyzed samples and
module scores are arithmetic means of available z-scored module genes. A module
is scoreable only if at least 50% of frozen genes are present. Precomputed
module-score input is accepted only for trajectory context and records module
coverage as not assessed from raw expression.

## Outputs

The harness writes:

- `module_gene_coverage.tsv`
- `paired_pharmacodynamic_module_deltas.tsv`
- `timepoint_summary.tsv`
- `batch_qc_diagnostic_summary.tsv`
- `input_qc.tsv`
- `validation_summary.json`
- `pharmacodynamic_context_summary.md`

Required language appears in the generated summary:

> This cohort lacks sample-mapped response labels. Results are pharmacodynamic
> context only and do not validate or falsify the locked V22 treatment-response
> rule.

## Explicit Non-Validation

The harness reports:

- `context_only: true`
- `response_validation_performed: false`

It does not compute responder/nonresponder AUC, NEDA, relapse, remission, or
patient-stratification metrics. If response-like columns are present in the
metadata, they are listed as ignored and not used.

## Synthetic Verification

Run:

```bash
.venv/bin/python scripts/v45_pharmacodynamic_only_harness.py synthetic-check \
  --outdir analysis/v45_pharmacodynamic_only_harness
```

Synthetic check result:

- samples: `36`
- subjects: `12`
- paired non-baseline deltas: `24`
- source mode: `precomputed_module_scores`
- context-only check: pass
- response validation performed: `false`
- required output files: all present

Synthetic outputs:

- `analysis/v45_pharmacodynamic_only_harness/synthetic_check/`

Synthetic data are method checks only and are not biological evidence.

## Use On GSE228330-Like Cohorts

`GSE228330` remains pharmacodynamic context only unless author-provided
sample-mapped outcome labels are obtained and a cohort-specific response
validation preregistration addendum is written before scoring those labels.

