# Author-Run Metric Format Adapter V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_author_run_metric_format_adapter.py` handles common aggregate
author-run return variants without changing the required V45 outputs. It
normalizes collaborator-facing file names and column aliases into the exact V45
minimum-output schema, then the existing V45 completeness and schema validators
remain the authority.

The adapter does not read raw data, private labels, expression matrices, or
interpret any validation result. It copies or renames aggregate fields only.

## When To Use

Use this only when a collaborator returned aggregate harness outputs under
non-canonical but recognizable names, for example:

- `primary_metrics.tsv` instead of `locked_rule_metrics.tsv`;
- `module_gene_coverage.tsv` instead of `gene_mapping_coverage.tsv`;
- `confounder_adjusted_metrics.tsv` instead of `confounder_adjustment_metrics.tsv`;
- `batch_qc.tsv` instead of `batch_diagnostic_metrics.tsv`;
- column aliases such as `subjects -> n`, `responders -> n_responders`,
  `auc_lower -> auc_ci_low`, or `status -> verdict`.

If a required aggregate output is absent under both canonical and accepted alias
names, the adapter blocks. It does not infer missing metrics.

## Command

Normalize an aggregate package:

```bash
.venv/bin/python scripts/v46_author_run_metric_format_adapter.py adapt \
  --root <returned_aggregate_package_dir> \
  --outdir analysis/v46_author_run_metric_format_adapter/<cohort>_<date> \
  --fail-on-error
```

Then run the standard V45 gates on:

`analysis/v46_author_run_metric_format_adapter/<cohort>_<date>/normalized_package`

Synthetic verification:

```bash
.venv/bin/python scripts/v46_author_run_metric_format_adapter.py synthetic-check \
  --outdir analysis/v46_author_run_metric_format_adapter
```

## Verified Synthetic Result

The committed synthetic check passed:

- accepted alternate file names and column aliases normalize to a canonical
  package;
- the normalized package passes the V45 author-run completeness validator;
- the normalized package passes the V45 author-run schema validator;
- a required missing metric table blocks the adapter.

Machine-readable outputs:

- `analysis/v46_author_run_metric_format_adapter/metric_format_adapter_synthetic_summary.json`
- `analysis/v46_author_run_metric_format_adapter/metric_format_adapter_synthetic_checks.tsv`
- `analysis/v46_author_run_metric_format_adapter/adapter/metric_format_adapter_manifest.tsv`
- `analysis/v46_author_run_metric_format_adapter/adapter/normalized_package/`
- `analysis/v46_author_run_metric_format_adapter/missing_required_adapter/metric_format_adapter_summary.json`

## Boundary

The adapter is not a repair mechanism for invalid content. It only maps accepted
names and columns into the canonical schema. Completeness, value-level schema,
safe interpretation, and V42 outcome meaning remain governed by the existing
V45/V46 gates.

