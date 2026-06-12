# V45 Primary Harness Regression Tests

Status: synthetic infrastructure regression. This is not biological evidence.

## Purpose

`scripts/v45_primary_harness_regression_tests.py` wraps the existing V42
Gafson synthetic null/planted harness check and asserts the primary validation
path still behaves as pre-registered before any real Gafson-like data are
opened.

This regression test does not change `LOCKED_RULE_V22.md`,
`PREREGISTRATION_V42.md`, or any validation threshold.

## Command

```bash
.venv/bin/python scripts/v45_primary_harness_regression_tests.py
```

The wrapper regenerates seeded synthetic fixtures under:

`analysis/v45_primary_harness_regression_tests/v42_primary_synthetic/`

and writes:

`analysis/v45_primary_harness_regression_tests/regression_summary.json`

## Assertions

The wrapper fails if any of these invariants break:

1. synthetic null cohort does not pass as validation;
2. synthetic planted cohort passes cleanly;
3. both null and planted cohorts contain `60` paired subjects;
4. null AUC remains near random (`0.35-0.65`);
5. planted AUC remains high (`>=0.95`);
6. each result directory writes the expected V42 artifacts:
   - `validation_summary.json`
   - `paired_module_deltas.tsv`
   - `gene_mapping_coverage.tsv`
   - `sample_attrition.tsv`
   - `locked_rule_metrics.tsv`
   - `confounder_adjustment_metrics.tsv`
   - `joint_confounder_metrics.tsv`
   - `batch_diagnostic_metrics.tsv`

## Result

Run status: `PASS`

| Scenario | Expected | Observed verdict | n | AUC | Hedges g | Receptor AUC |
|---|---|---|---:|---:|---:|---:|
| synthetic null | fail / not pass | `FAIL_ADEQUATE_POWER` | 60 | 0.520 | 0.029 | 0.309 |
| synthetic planted | pass cleanly | `PASS_CLEAN` | 60 | 1.000 | 6.979 | 0.282 |

All expected result files were present for both fixtures.

## Interpretation

This checkpoint makes the primary V42/Gafson harness regression-testable in the
same way V45 already made the secondary and pharmacodynamic-only harnesses
regression-testable. It proves only that the synthetic method checks still
behave as intended; it does not validate the biological APC/HLA-II rule.
