# Author-Run Return Operator Checklist V45

Status: human operator checklist. No validation result and no biological claim.

Use this when a collaborator returns aggregate outputs from a local author-run
of the frozen harness.

Machine-readable checklist:

`docs/validation/input_schemas/V45_author_run_return_operator_checklist.tsv`

## Required Order

1. Save the returned aggregate package under a non-raw, non-private review path.
2. Do not copy raw expression, clinical labels, private correspondence,
   agreements, credentials, or private URLs into the repository.
3. Run the combined return gate:

```bash
.venv/bin/python scripts/v45_author_run_return_gate_runner.py run \
  --root <returned_aggregate_package_dir> \
  --package-state scored \
  --outdir analysis/v45_author_run_return_gate_runner/<cohort>_<date> \
  --fail-on-error
```

4. If redaction fails, stop and request a redacted aggregate-only return.
5. If completeness fails, stop and request the missing aggregate outputs.
6. If the gate passes, run the aggregate schema validator:

```bash
.venv/bin/python scripts/v45_author_run_schema_validator.py run \
  --root <returned_aggregate_package_dir> \
  --package-state scored \
  --outdir analysis/v45_author_run_schema_validator/<cohort>_<date> \
  --fail-on-error
```

For an unscoreable package, use `--package-state unscoreable`.

7. If schema validation fails, stop and request a repaired aggregate return.
8. If the schema validator passes, fill:

`docs/validation/VALIDATION_RESULT_REPORT_TEMPLATE_V45.md`

9. Interpret only under:

`docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`

10. Run precommit/readiness guards before any commit:

```bash
.venv/bin/python scripts/v45_precommit_readiness_check.py
.venv/bin/python scripts/v45_readiness_status_dashboard.py \
  --outdir analysis/v45_readiness_status_dashboard
```

## Forbidden Shortcuts

Do not:

- accept prose-only "it worked" summaries;
- accept screenshot-only output;
- change module genes, thresholds, score signs, timepoints, or endpoint
  orientation;
- interpret a package that fails redaction, completeness, or schema validation;
- treat aggregate author-run output as equivalent to individual-level
  reproducibility unless the required command/hash metadata are present.

## Expected Gate Outcomes

| Gate | Pass means | Failure response |
|---|---|---|
| redaction | no obvious raw/private leakage in the aggregate package | request a redacted aggregate-only package |
| completeness | minimum aggregate files are present and parseable | request missing aggregate outputs |
| schema validator | aggregate values are internally consistent and in allowed ranges | request repaired aggregate tables before interpretation |
| result report | all reported values trace to returned aggregate files | repair report or request missing values |
| outcome grid | result is classified using precommitted V42 meanings | do not reinterpret post hoc |
| precommit readiness | repository guards are clean after report preparation | repair before commit |

Passing this checklist makes the return package interpretable as an aggregate
author-run result. It does not create a new rule and does not relax the V42
pre-registration.
