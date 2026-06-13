# Safe-Wording Fixture Linter V46

Status: validation-readiness governance. No validation result and no biological
claim.

## Purpose

`scripts/v46_safe_wording_fixture_linter.py` generates one synthetic report
wording fixture for each V46 returned-package safe-interpretation class and
lints the fixtures for premature result language.

The guard exists because returned packages can arrive in states where scoring
language is not yet allowed. Blocked and no-score classes must not mention AUC,
Hedges, p-values, effect estimates, confidence intervals, permutation results,
or pass/fail validation verdicts. The linter verifies that boundary before any
operator-facing report fragment is reused.

The linter does not inspect expression data, labels, validation metrics, or any
quarantined cohort. It reads only the synthetic V46 safe-interpretation class
table and writes synthetic wording fixtures.

## Command

```bash
.venv/bin/python scripts/v46_safe_wording_fixture_linter.py \
  --outdir analysis/v46_safe_wording_fixture_linter \
  --fail-on-error
```

## Verified Synthetic Result

The committed run passed:

- expected-pass fixtures: `11`;
- expected-fail fixtures: `1`;
- live fixture failures: `0`;
- expected bad fixture caught: `1`;
- overall status: `PASS`.

Machine-readable outputs:

- `analysis/v46_safe_wording_fixture_linter/safe_wording_fixture_summary.json`
- `analysis/v46_safe_wording_fixture_linter/safe_wording_fixture_index.tsv`
- `analysis/v46_safe_wording_fixture_linter/safe_wording_fixture_lint.tsv`
- per-class synthetic fixtures under `analysis/v46_safe_wording_fixture_linter/fixtures/`

## Boundary

This is a no-score-before-gates wording check. A passing linter means the
synthetic wording fragments respect the V46 safe-interpretation boundary. It
does not make a validation claim, does not change `LOCKED_RULE_V22.md`, and
does not change the frozen V42 pre-registration.
