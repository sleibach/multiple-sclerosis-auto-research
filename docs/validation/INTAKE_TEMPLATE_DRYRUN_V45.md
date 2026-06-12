# Intake Template Dry Run V45

Status: infrastructure dry run. Synthetic packages only; no biological evidence.

## Purpose

The V45 intake preflight documentation includes command templates for future
quarantined cohorts. This checkpoint verifies that the documented command shape
works on separate synthetic primary and pharmacodynamic packages using
`--write-checksums`, metadata schema checks, expression header checks, and the
frozen preflight output layout.

## Command

```bash
.venv/bin/python scripts/v45_intake_template_dryrun.py
```

The script creates:

- `analysis/v45_intake_template_dryrun/synthetic_primary_quarantine/`
- `analysis/v45_intake_template_dryrun/synthetic_pharmacodynamic_quarantine/`

and runs `scripts/v45_validation_intake_preflight.py check` against each package.

## Result

Committed output:

- `analysis/v45_intake_template_dryrun/template_dryrun_summary.json`

Summary:

| Check | Result |
|---|---|
| Primary template preflight passes | pass |
| Pharmacodynamic template preflight passes | pass |
| Primary checksums written | pass |
| Pharmacodynamic checksums written | pass |
| Primary expression header checked | pass |
| Pharmacodynamic expression header checked | pass |

Overall status: `PASS`.

## Interpretation

This verifies the operational command template before real cohort receipt. It is
not a module-scoring run and not a validation. If a future cohort fails the same
preflight, that is an intake blocker, not a biological result.
