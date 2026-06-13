# Result Report Safe-Class Linter V46

Status: validation-readiness report governance. No validation result and no
biological claim.

## Purpose

`scripts/v46_result_report_safe_class_linter.py` checks that a returned-package
or validation report cites the V46 safe-interpretation class being used, and
that blocked/no-score classes do not contain premature score or pass/fail
validation language.

This closes the gap between the V46 safe-interpretation classifier and actual
human report drafts. A report must name the safe class, and if that class is
blocked or no-score, it cannot mention AUC, Hedges, p-values, effect estimates,
confidence intervals, permutation results, `locked_rule_metrics.tsv`, or
validation pass/fail wording.

## Commands

Synthetic regression:

```bash
.venv/bin/python scripts/v46_result_report_safe_class_linter.py synthetic-check \
  --outdir analysis/v46_result_report_safe_class_linter \
  --fail-on-error
```

Lint a report draft:

```bash
.venv/bin/python scripts/v46_result_report_safe_class_linter.py lint \
  --report analysis/validation_runs/<cohort>/VALIDATION_RESULT_REPORT.md \
  --safe-class <V46_SAFE_CLASS> \
  --outdir analysis/v46_result_report_safe_class_linter/<cohort> \
  --expect-status PASS
```

## Verified Synthetic Result

The committed synthetic check passed:

- cases: `5`;
- expected-pass fixtures: blocked-good, eligible-good, caution-good;
- expected-fail fixtures: blocked metric leak, missing safe class;
- failures: `0`;
- overall status: `PASS`.

Machine-readable outputs:

- `analysis/v46_result_report_safe_class_linter/result_report_safe_class_synthetic_summary.json`
- `analysis/v46_result_report_safe_class_linter/result_report_safe_class_synthetic_cases.tsv`
- per-case `result_report_safe_class_lint_summary.json`
- per-case `result_report_safe_class_lint.tsv`

## Boundary

This linter validates report wording only. It does not run the validation
harness, does not inspect score values, does not read quarantined data, and does
not alter the locked V22 rule or frozen V42 pre-registration.
