# Validation Handoff Bundle Template V45

Status: handoff template. No validation has been run by this template.

Purpose: define the complete non-sensitive bundle that should accompany any
future validation result or unscoreable-data report.

Machine-readable template:

`docs/validation/input_schemas/V45_validation_handoff_bundle_template.tsv`

Executable completeness checker:

```bash
.venv/bin/python scripts/v45_handoff_completeness_check.py \
  --cohort <cohort_id> \
  --package-state <not_received|received|scored|unscoreable>
```

See `docs/validation/HANDOFF_COMPLETENESS_CHECK_V45.md`.

## Bundle Rule

A validation result is not handoff-ready until the bundle includes:

- gate outputs;
- locked-hash audit;
- regression/pre-commit readiness evidence;
- frozen harness outputs when a harness ran;
- V45 result report or unscoreable/blocker report;
- redaction check.

## Required Bundle Sections

| Section | Required for | Examples |
|---|---|---|
| receipt and terms | all received packages | receipt manifest, terms summary |
| integrity gates | all packages | checksum, no-raw scan, locked-hash audit |
| intake gates | all packages | preflight, module coverage, subject-map sanity |
| preregistration evidence | all scored packages | V42 preregistration or blind addendum |
| software readiness | all scored packages | pre-commit readiness, regression aggregator |
| harness outputs | scored packages only | validation summary, metrics, attrition, confounders, batch diagnostics |
| report | all packages | V45 validation result report or unscoreable-data explanation |
| redaction | all handoffs | sensitive-data checklist |

## If Data Are Unscoreable

Still create a handoff bundle, but include:

- the failed gate output;
- failure taxonomy code;
- allowed repair requested;
- statement that no biological validation occurred.

Do not include invented metrics or partial response claims.

## Guardrail

The bundle is a packaging standard. It does not change the result class, rescue
a failed result, or permit reporting outside the V42 interpretation grid.
