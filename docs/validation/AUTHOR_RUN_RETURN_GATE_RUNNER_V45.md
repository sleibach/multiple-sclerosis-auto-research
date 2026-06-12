# Author-Run Return Gate Runner V45

Status: validation-readiness infrastructure. No biological claim.

Script:

`scripts/v45_author_run_return_gate_runner.py`

Purpose: run the author-run aggregate-return gates in the required order:

1. redaction precheck;
2. output completeness check only if redaction passes.

This runner does not run the frozen validation harness and does not interpret
biological results. It is for returned aggregate packages from the author-run
fallback path.

## Command

For a returned scored aggregate package:

```bash
.venv/bin/python scripts/v45_author_run_return_gate_runner.py run \
  --root <returned_aggregate_package_dir> \
  --package-state scored \
  --outdir analysis/v45_author_run_return_gate_runner/<cohort>_<date> \
  --fail-on-error
```

For an unscoreable package, use `--package-state unscoreable`.

Synthetic branch regression:

```bash
.venv/bin/python scripts/v45_author_run_return_gate_runner.py synthetic-check \
  --outdir analysis/v45_author_run_return_gate_runner
```

Current synthetic verification:

| Case | Redaction | Completeness | Overall |
|---|---|---|---|
| complete aggregate package | `PASS` | `PASS` | `PASS` |
| clean incomplete aggregate package | `PASS` | `FAIL` | `FAIL` |
| risky aggregate package | `FAIL` | `SKIPPED` | `FAIL` |

All `3/3` cases match the expected gate result.

## Outputs

Each run writes:

- `author_run_return_gate_steps.tsv`
- `author_run_return_gate_summary.json`
- subdirectory `redaction_precheck/`
- subdirectory `output_completeness/` if redaction passed

## Guardrail

If redaction fails, completeness is skipped. A package that contains raw
expression, individual labels, private correspondence, or credentials should not
be treated as handoff-complete, even if it happens to include the expected
aggregate metrics.
