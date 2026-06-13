# Author-Run Return Operator Checklist V45

Status: human operator checklist. No validation result and no biological claim.

Use this when a collaborator returns aggregate outputs from a local author-run
of the frozen harness.

Machine-readable checklist:

`docs/validation/input_schemas/V45_author_run_return_operator_checklist.tsv`

## Required Order

0. Generate the package-specific command order before running any gate:

```bash
.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan \
  --cohort-token <cohort>_<date> \
  --package-root <returned_aggregate_package_dir> \
  --terms-capture <terms_capture_tsv> \
  --terms-class <resolved_terms_class> \
  --package-kind author_run_aggregate \
  --package-state scored \
  --metric-format-state unknown \
  --outdir analysis/v46_returned_package_command_order_planner/<cohort>_<date> \
  --expect-status PASS
```

Use `docs/validation/RETURNED_PACKAGE_COMMAND_ORDER_PLANNER_V46.md` for route
states and hard-stop rules.

Before handling a real aggregate return, the local composition check can be
rerun:

```bash
.venv/bin/python scripts/v46_aggregate_only_returned_package_composition_dryrun.py \
  --outdir analysis/v46_aggregate_only_returned_package_composition_dryrun \
  --fail-on-error
```

It should pass and end in the documented synthetic below-floor safe wording class
from `docs/validation/AGGREGATE_ONLY_RETURNED_PACKAGE_COMPOSITION_DRYRUN_V46.md`.

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
5. If completeness fails, stop and request the missing aggregate outputs. If the
   package appears complete but uses recognizable non-canonical aggregate file
   names or column names, run the V46 metric-format adapter and rerun the return
   gate on the normalized package:

```bash
.venv/bin/python scripts/v46_author_run_metric_format_adapter.py adapt \
  --root <returned_aggregate_package_dir> \
  --outdir analysis/v46_author_run_metric_format_adapter/<cohort>_<date> \
  --fail-on-error
```

The normalized package is:

`analysis/v46_author_run_metric_format_adapter/<cohort>_<date>/normalized_package`

If the adapter blocks, request the missing canonical aggregate output. Do not
infer missing metrics.

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
8. If schema validation passes, run the V46 safe-interpretation classifier
   before reading or discussing returned scores:

```bash
.venv/bin/python scripts/v46_returned_package_safe_interpretation.py classify \
  --gate-summary analysis/v45_author_run_return_gate_runner/<cohort>_<date>/author_run_return_gate_summary.json \
  --schema-summary analysis/v45_author_run_schema_validator/<cohort>_<date>/author_run_schema_validation_summary.json \
  --analyzable-summary analysis/v45_route_analyzable_pair_calculator/<cohort>_<date>/analyzable_pair_summary.json \
  --metadata-summary analysis/v45_metadata_contradiction_stress/<cohort>_<date>/metadata_contradiction_summary.json \
  --batch-confounder-summary <pre_score_batch_or_confounder_warning_summary.json> \
  --terms-status PASS \
  --outdir analysis/v46_returned_package_safe_interpretation/<cohort>_<date>
```

9. If the V46 classifier blocks or cautions interpretation, run the safe-wording
   fixture linter before drafting report language:

```bash
.venv/bin/python scripts/v46_safe_wording_fixture_linter.py \
  --outdir analysis/v46_safe_wording_fixture_linter \
  --fail-on-error
```

Use only wording compatible with the classifier's safe class, and do not
escalate the claim beyond that class.

10. If the package is eligible for pre-registered interpretation, fill:

`docs/validation/VALIDATION_RESULT_REPORT_TEMPLATE_V45.md`

11. Interpret only under:

`docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`

12. Run precommit/readiness guards before any commit:

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
| V46 metric-format adapter | accepted aggregate file/column aliases normalize to canonical V45 outputs | request the missing canonical aggregate output; never infer values |
| V46 command-order planner | terms, adapter branch, gate, schema, partial-label, and safe-interpretation steps are ordered | stop at the first blocked step; do not skip ahead |
| schema validator | aggregate values are internally consistent and in allowed ranges | request repaired aggregate tables before interpretation |
| V46 safe-interpretation classifier | pre-score gates and cohort-structure allow a specific safe wording class | use the classifier's blocked/caution wording and do not over-interpret |
| V46 safe-wording fixture linter | report fragments avoid premature score and pass/fail language for blocked/no-score classes | repair wording before any report draft is committed |
| result report | all reported values trace to returned aggregate files | repair report or request missing values |
| outcome grid | result is classified using precommitted V42 meanings | do not reinterpret post hoc |
| precommit readiness | repository guards are clean after report preparation | repair before commit |

Passing this checklist makes the return package interpretable as an aggregate
author-run result. It does not create a new rule and does not relax the V42
pre-registration.
