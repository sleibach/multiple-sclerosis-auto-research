# Report-Header Metadata Linter V46

Status: returned-package report-governance infrastructure. No validation result
and no biological claim.

`scripts/v46_report_header_metadata_linter.py` verifies that a returned-package
report draft contains the required provenance header before any result section
or score-bearing language appears.

Required header fields:

- `cohort_token`
- `route_class`
- `terms_class`
- `safe_class`
- `locked_rule_path`
- `locked_rule_sha256`

The locked-rule path must be exactly `docs/locked_rules/LOCKED_RULE_V22.md`.
The locked-rule hash must match
`docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv` for that path. This
does not alter the locked rule; it only verifies report provenance.

## Synthetic Check

```bash
.venv/bin/python scripts/v46_report_header_metadata_linter.py synthetic-check \
  --outdir analysis/v46_report_header_metadata_linter \
  --fail-on-error
```

Current synthetic result:

- cases: `6`
- expected pass cases: complete eligible header; complete blocked header
- expected fail cases: missing cohort token; metadata after result heading;
  wrong locked-rule hash; unknown safe class
- checks per case: `13`
- score values read: `false`
- overall status: `PASS`

## Lint A Report Draft

```bash
.venv/bin/python scripts/v46_report_header_metadata_linter.py lint \
  --report <returned_report.md> \
  --outdir analysis/v46_report_header_metadata_linter/<cohort> \
  --expect-status PASS
```

The command writes:

- `report_header_metadata_lint.tsv`
- `report_header_metadata_lint_summary.json`

## Boundary

This linter reads report text only. It does not open returned score tables,
expression matrices, labels, raw data, or quarantined cohorts. It blocks
metadata drift before result wording but does not decide pass/fail/inconclusive
outcomes. Result interpretation remains bounded by the immutable V22 rule, the
V42 pre-registration, and the V46 safe class.
