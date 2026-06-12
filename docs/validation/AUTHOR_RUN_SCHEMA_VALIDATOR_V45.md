# Author-Run Aggregate Schema Validator V45

Status: validation-readiness infrastructure. No biological claim.

## Purpose

`scripts/v45_author_run_schema_validator.py` checks value-level schema
constraints for non-sensitive aggregate output packages returned by an
author-run frozen harness. It complements the author-run completeness and
redaction gates:

- redaction gate: rejects private/raw material;
- completeness gate: verifies the minimum files are present/readable;
- schema validator: verifies aggregate values are internally consistent before
  interpretation.

The validator does not run a harness, inspect raw expression, inspect private
labels, or interpret biology.

## Command

For a scored aggregate package:

```bash
.venv/bin/python scripts/v45_author_run_schema_validator.py run \
  --root <returned_aggregate_package_dir> \
  --package-state scored \
  --outdir analysis/v45_author_run_schema_validator/<cohort>_<date> \
  --fail-on-error
```

For an unscoreable aggregate package, use `--package-state unscoreable`; a
non-empty `failure_taxonomy_code.txt` is then required.

Synthetic verification:

```bash
.venv/bin/python scripts/v45_author_run_schema_validator.py synthetic-check \
  --outdir analysis/v45_author_run_schema_validator
```

## Current Synthetic Result

Synthetic status: `PASS`.

| Case | Expected | Observed |
|---|---|---|
| complete aggregate package | `PASS` | `PASS` |
| bad numeric/count metrics | `FAIL` | `FAIL` |
| unscoreable package missing failure code | `FAIL` | `FAIL` |

## Checked Constraints

- `validation_summary.json`: verdict/count fields, non-negative counts, response
  counts summing to labeled count, AUC/CI ranges.
- `locked_rule_metrics.tsv`: required V22 primary row, AUC/CI/p-value ranges,
  and count consistency with the summary.
- `gene_mapping_coverage.tsv`: count ranges, thresholds, and boolean
  scoreability.
- confounder, joint-confounder, and batch tables: aggregate AUC/p-value ranges
  and non-empty verdict fields.
- `sample_attrition.tsv`: parseable inclusion flags and included-count
  consistency where applicable.
- unscoreable packages: required `failure_taxonomy_code.txt`.

## Machine-Readable Outputs

- `analysis/v45_author_run_schema_validator/synthetic_author_run_schema_summary.json`
- `analysis/v45_author_run_schema_validator/synthetic_author_run_schema_cases.tsv`
- `analysis/v45_author_run_schema_validator/good/author_run_schema_validation.tsv`
- `analysis/v45_author_run_schema_validator/bad_metrics/author_run_schema_validation.tsv`
- `analysis/v45_author_run_schema_validator/unscoreable_missing_code/author_run_schema_validation.tsv`

## Interpretation Boundary

A schema `PASS` only means the aggregate return package is structurally
consistent enough to proceed to the pre-registered interpretation grid. It does
not mean the result passes validation and does not support a biological claim.
