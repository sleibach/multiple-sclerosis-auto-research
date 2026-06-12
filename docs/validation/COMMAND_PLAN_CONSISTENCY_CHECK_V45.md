# Command Plan Consistency Check V45

Status: software/readiness guardrail. No biological claim.

Purpose: detect accidental drift in generated command-runner plans, especially
loss or reordering of required gates such as module coverage or
response-column audit.

## Command

```bash
.venv/bin/python scripts/v45_command_plan_consistency_check.py \
  --outdir analysis/v45_command_plan_consistency
```

Outputs:

- `analysis/v45_command_plan_consistency/command_plan_consistency.tsv`
- `analysis/v45_command_plan_consistency/command_plan_consistency_summary.json`

## Current Result

Current status: `PASS`.

| Mode | Expected gates | Status |
|---|---:|---|
| `primary` | `7` | `PASS` |
| `pharmacodynamic` | `8` | `PASS` |
| `postpartum` | `5` | `PASS` |
| `tb` | `5` | `PASS` |

The primary and pharmacodynamic plans both include
`module_coverage_precheck`. The pharmacodynamic plan also includes
`response_column_audit`.

## Guardrail

This checker does not execute any gate and does not read quarantined data. It
only verifies that generated plans contain the expected gate sequence for each
mode. A failure means the command-runner implementation or expected-gate table
must be reconciled before relying on generated plans.
