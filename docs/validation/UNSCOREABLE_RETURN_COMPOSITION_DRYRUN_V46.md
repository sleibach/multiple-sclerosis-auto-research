# Unscoreable Return Composition Dry Run V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_unscoreable_return_composition_dryrun.py` exercises the returned
package path for an aggregate author-run package that is valid to receive but
cannot be scored because score-bearing aggregate outputs are missing. This is
the realistic "repair package" case: the operator needs a failure taxonomy and
safe repair wording, not validation interpretation.

The dry run creates a seeded synthetic aggregate package, removes the
score-bearing outputs, adds `failure_taxonomy_code.txt`, and verifies that the
pipeline stops at completeness before schema validation, safe interpretation, or
any score/result wording.

## Command

```bash
.venv/bin/python scripts/v46_unscoreable_return_composition_dryrun.py \
  --outdir analysis/v46_unscoreable_return_composition_dryrun \
  --fail-on-error
```

## Verified Synthetic Result

The committed run passed:

- steps: `5`;
- checks: `11`;
- expected completeness-block path: `PASS`;
- route class: `UNSCOREABLE_AGGREGATE_PREFLIGHT_ONLY`;
- failure taxonomy: `UNSCOREABLE_MISSING_LOCKED_RULE_METRICS`;
- score values interpreted: `false`;
- sample-level data read: `false`;
- overall status: `PASS`.

Missing score-bearing outputs in the synthetic package:

- `locked_rule_metrics.tsv`
- `confounder_adjustment_metrics.tsv`
- `joint_confounder_metrics.tsv`
- `batch_diagnostic_metrics.tsv`
- `validation_result_report.md`

Machine-readable outputs:

- `analysis/v46_unscoreable_return_composition_dryrun/unscoreable_composition_summary.json`
- `analysis/v46_unscoreable_return_composition_dryrun/unscoreable_composition_steps.tsv`
- `analysis/v46_unscoreable_return_composition_dryrun/unscoreable_composition_checks.tsv`
- `analysis/v46_unscoreable_return_composition_dryrun/unscoreable_safe_wording.md`

## Operator Boundary

For this route, safe wording is repair-only: report the failure taxonomy code,
the failed gate, and the missing aggregate score outputs to request. Do not
mention AUC, p-values, effect estimates, validation pass/fail, or biological
interpretation. The locked V22 rule and frozen V42 pre-registration are
unchanged.
