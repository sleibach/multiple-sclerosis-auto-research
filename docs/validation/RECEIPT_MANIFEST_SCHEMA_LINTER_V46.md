# Receipt-Manifest Schema Linter V46

Status: returned-package operations infrastructure. No validation result and no
biological claim.

## Purpose

This linter checks a returned-package receipt manifest before the V46
package-manifest shape classifier runs. It verifies required non-sensitive
manifest columns, relative aggregate-output paths, safe sensitivity classes, and
commit-safe metadata values. It blocks raw/private paths, absolute local paths,
private URLs, restricted sensitivity classes, and unexpected score-like
filenames.

## Commands

For synthetic verification:

```bash
.venv/bin/python scripts/v46_receipt_manifest_schema_linter.py synthetic-check \
  --outdir analysis/v46_receipt_manifest_schema_linter
```

For a real receipt manifest:

```bash
.venv/bin/python scripts/v46_receipt_manifest_schema_linter.py lint \
  --manifest <receipt_manifest.tsv> \
  --outdir analysis/v46_receipt_manifest_schema_linter/<cohort>_<date> \
  --fail-on-error
```

## Current Result

- synthetic cases: `9`
- expected pass cases: `1`
- expected fail cases: `8`
- status mismatches: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

Negative fixtures caught:

- missing required column;
- raw expression/counts path;
- private agreement/correspondence path;
- absolute local path;
- private remote URL;
- restricted sensitivity class plus non-commit-safe value;
- unexpected score-like filename;
- empty manifest.

Outputs:

- `analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_summary.json`
- `analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_cases.tsv`
- `analysis/v46_receipt_manifest_schema_linter/receipt_manifest_schema_synthetic_lint.tsv`
- per-case lint outputs under `analysis/v46_receipt_manifest_schema_linter/<case>/`

## Boundary

The linter reads only receipt-manifest metadata. It does not open returned
tables, result values, expression matrices, labels, or quarantined cohorts. A
`PASS` only means the manifest is safe to hand to the shape classifier; it does
not mean the package is scoreable or interpretable.
