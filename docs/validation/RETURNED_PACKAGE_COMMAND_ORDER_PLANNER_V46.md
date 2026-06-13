# Returned-Package Command-Order Planner V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_returned_package_command_order_planner.py` generates the command
sequence for a collaborator-returned aggregate validation package before any
returned score is read. It sequences the existing gates and V46 classifiers:

1. data-use terms governance;
2. metric-format adapter when aliases are declared or suspected;
3. author-run redaction/completeness gate;
4. aggregate schema validator;
5. partial-label classifier;
6. safe-interpretation classifier.

The planner does not execute the validation harness, read expression data, read
score values, or interpret biology. Its output is an operator command plan and
hard-stop conditions.

## Command

For an aggregate author-run return with canonical file names:

```bash
.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan \
  --cohort-token <cohort>_<date> \
  --package-root <returned_aggregate_package_dir> \
  --terms-capture <terms_capture_tsv> \
  --terms-class AGGREGATE_ONLY_LOCAL_PREFLIGHT \
  --package-kind author_run_aggregate \
  --package-state scored \
  --metric-format-state canonical \
  --outdir analysis/v46_returned_package_command_order_planner/<cohort>_<date> \
  --expect-status PASS
```

Use `--metric-format-state noncanonical` when the returned aggregate package is
known to use accepted aliases. Use `unknown` when this is not clear; the plan
then includes a conditional adapter branch after an initial completeness failure.

Use `--terms-class AUTHOR_RUN_ONLY` only for aggregate author-run returns. It
does not permit local individual-level processing.

## Verified Synthetic Result

The committed synthetic check passes:

```bash
.venv/bin/python scripts/v46_returned_package_command_order_planner.py \
  synthetic-check \
  --outdir analysis/v46_returned_package_command_order_planner
```

Current summary:

- cases: `6`
- failures: `0`
- overall status: `PASS`

Machine-readable outputs:

- `analysis/v46_returned_package_command_order_planner/returned_package_command_order_synthetic_summary.json`
- `analysis/v46_returned_package_command_order_planner/returned_package_command_order_synthetic_cases.tsv`
- per-case `returned_package_command_plan.tsv`
- per-case `returned_package_command_plan_summary.json`

## Route Rules

| Route state | Planner behavior |
|---|---|
| canonical aggregate package | terms -> return gate -> schema -> partial-label -> safe interpretation |
| declared noncanonical aliases | terms -> metric adapter -> return gate on normalized package -> schema -> partial-label -> safe interpretation |
| unknown alias state | terms -> conditional metric adapter branch -> initial return gate -> conditional rerun gate on normalized package -> schema -> partial-label -> safe interpretation |
| `AUTHOR_RUN_ONLY` terms with aggregate return | aggregate return handling may proceed; individual-level local processing remains blocked |
| ambiguous or no-processing terms | stop after terms; do not run package gates or score interpretation |

Every row in the generated plan has `score_values_read=false`. A returned AUC,
effect size, p-value, or pass/fail result is not read until the safe
interpretation classifier has emitted the allowed wording class.

## Interpretation Boundary

This planner answers only: "which gate command is next, and where must the
operator stop?" It does not change `LOCKED_RULE_V22.md`, the V42
pre-registration, thresholds, module genes, or outcome definitions. A `PASS`
plan means an ordered set of gates can be attempted; it does not mean a returned
package is valid or clinically interpretable.
