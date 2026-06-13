# Package-Manifest Shape Classifier V46

Status: returned-package operations infrastructure. No validation result and no biological claim.

Purpose: classify a returned package from a non-sensitive receipt manifest and terms class before opening any score-bearing output. The classifier maps filenames and manifest metadata to the V46 first-30-minute scenario plus command-order inputs.

## Current Run

Command:

```bash
.venv/bin/python scripts/v46_package_manifest_shape_classifier.py synthetic-check --outdir analysis/v46_package_manifest_shape_classifier
```

Result:

- overall status: `PASS`
- synthetic cases: `6`
- lint checks: `12`
- lint failures: `0`
- all `score_values_read`: `false`

Synthetic scenarios verified:

- canonical scored aggregate -> `scored_canonical_aggregate`
- accepted noncanonical aliases -> `scored_noncanonical_aggregate`
- score-like unknown aliases -> `scored_unknown_alias_aggregate`
- failure-taxonomy/no-score return -> `unscoreable_aggregate`
- partial-label marker -> `partial_label_scored_aggregate`
- blocked terms -> `terms_blocked_return`

## Boundary

The classifier reads only a receipt manifest with fields such as `relative_path_or_external_location`, `file_role`, `terms_status`, and `notes`, plus the operator-supplied terms class. It does not open returned result tables, read AUC/effect values, inspect individual-level data, or process quarantined cohorts.

The output is a routing recommendation only. It does not decide whether a returned package is valid, scoreable, or interpretable; downstream V45/V46 gates still decide those questions.

## Outputs

- `analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_summary.json`
- `analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_cases.tsv`
- `analysis/v46_package_manifest_shape_classifier/package_manifest_shape_synthetic_lint.tsv`
- per-case synthetic classification summaries under `analysis/v46_package_manifest_shape_classifier/<case>/`

For a real received package, run the receipt-manifest schema linter first:

```bash
.venv/bin/python scripts/v46_receipt_manifest_schema_linter.py lint \
  --manifest <receipt_manifest.tsv> \
  --outdir analysis/v46_receipt_manifest_schema_linter/<cohort>_<date> \
  --fail-on-error
```

Only if that linter passes, run:

```bash
.venv/bin/python scripts/v46_package_manifest_shape_classifier.py classify \
  --manifest <receipt_manifest.tsv> \
  --terms-class <TERMS_CLASS> \
  --outdir analysis/v46_package_manifest_shape_classifier/<cohort>_<date> \
  --fail-on-error
```
