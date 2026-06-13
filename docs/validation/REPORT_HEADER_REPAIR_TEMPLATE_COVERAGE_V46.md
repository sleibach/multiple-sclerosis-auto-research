# Report-Header Repair Template Coverage V46

Status: returned-package report-governance infrastructure. No validation result
and no biological claim.

`scripts/v46_report_header_repair_template_coverage.py` maps report-header
metadata failures to safe repair requests before any result text is allowed.
It does not read returned score tables, expression matrices, labels, raw data,
or quarantined cohorts.

## Command

```bash
.venv/bin/python scripts/v46_report_header_repair_template_coverage.py \
  --outdir analysis/v46_report_header_repair_template_coverage \
  --fail-on-error
```

## Current Result

- issue templates: `7`
- required header fields covered: `6/6`
- lint failures: `0`
- score values read: `false`
- overall status: `PASS`

Outputs:

- `analysis/v46_report_header_repair_template_coverage/report_header_repair_template_coverage.tsv`
- `analysis/v46_report_header_repair_template_coverage/report_header_required_field_coverage.tsv`
- `analysis/v46_report_header_repair_template_coverage/report_header_repair_template_lint.tsv`
- `analysis/v46_report_header_repair_template_coverage/REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE.md`

## Covered Failures

The coverage map includes repair requests for:

- missing or invalid `cohort_token`;
- missing or unknown `route_class`;
- missing or unknown `terms_class`;
- missing or unknown `safe_class`;
- missing or non-exact `locked_rule_path`;
- missing or wrong `locked_rule_sha256`;
- required metadata appearing after result text.

## Boundary

These templates request provenance/header repair only. They forbid choosing
metadata from score behavior, changing the locked rule, changing thresholds,
changing labels, changing timepoints, or interpreting returned scores. A report
draft remains blocked until the corrected header passes
`scripts/v46_report_header_metadata_linter.py`.
