# Returned-Package Safe Interpretation V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_returned_package_safe_interpretation.py` classifies how a returned
validation package may be discussed before any returned score is interpreted. It
combines only pre-score signals:

- data-use/receipt terms status;
- author-run redaction and completeness gate;
- aggregate schema validation status;
- analyzable-pair planning band;
- metadata contradiction status;
- batch/confounder warning status.

The classifier does **not** read expression data, private labels, locked-rule
metric values, AUCs, p-values, effect sizes, or result reports. Its output is
safe wording and forbidden wording for the package state.

## Command

After the V45 return gate, schema validator, metadata contradiction audit, and
route analyzable-pair calculator have run:

```bash
.venv/bin/python scripts/v46_returned_package_safe_interpretation.py classify \
  --gate-summary analysis/v45_author_run_return_gate_runner/<cohort>/author_run_return_gate_summary.json \
  --schema-summary analysis/v45_author_run_schema_validator/<cohort>/author_run_schema_validation_summary.json \
  --analyzable-summary analysis/v45_route_analyzable_pair_calculator/<cohort>/analyzable_pair_summary.json \
  --metadata-summary analysis/v45_metadata_contradiction_stress/<cohort>/metadata_contradiction_summary.json \
  --batch-confounder-summary <pre_score_batch_or_confounder_warning_summary.json> \
  --terms-status PASS \
  --outdir analysis/v46_returned_package_safe_interpretation/<cohort>
```

Use `--terms-status FAIL` or `UNKNOWN` if data-use terms, package receipt, or
operator-status evidence has not cleared. That blocks interpretation regardless
of other signals.

Synthetic regression:

```bash
.venv/bin/python scripts/v46_returned_package_safe_interpretation.py synthetic-check \
  --outdir analysis/v46_returned_package_safe_interpretation
```

## Verified Synthetic Result

The committed synthetic check covers 11 routing classes and passed with zero
expectation failures:

- `ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION`
- `INCONCLUSIVE_SMALL_COHORT`
- `MINIMUM_DECISION_GRADE_CAUTION`
- `BELOW_V45_PLANNING_FLOOR`
- `CONTEXT_ONLY_OR_LABELS_NEEDED`
- `BLOCKED_TERMS_OR_RECEIPT_GATES`
- `BLOCKED_REDACTION`
- `BLOCKED_COMPLETENESS`
- `BLOCKED_SCHEMA`
- `BLOCKED_METADATA_CONTRADICTION`
- `CAUTION_BATCH_OR_CONFOUNDER`

Machine-readable outputs:

- `analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_summary.json`
- `analysis/v46_returned_package_safe_interpretation/safe_interpretation_synthetic_cases.tsv`
- per-case `safe_interpretation_summary.json`
- per-case `safe_interpretation_signals.tsv`

## Class Meanings

| Class | Safe interpretation | Hard boundary |
|---|---|---|
| `BLOCKED_TERMS_OR_RECEIPT_GATES` | package terms or receipt evidence blocks interpretation | do not inspect or interpret returned scores |
| `BLOCKED_REDACTION` | redaction failed; request aggregate-only redacted return | do not continue to completeness/schema/scoring |
| `BLOCKED_COMPLETENESS` | required aggregate outputs are missing | do not interpret partial metrics |
| `BLOCKED_RETURN_GATE` | combined return gate failed | use gate step table for repair only |
| `BLOCKED_SCHEMA` | aggregate outputs are malformed or internally invalid | request repaired tables before interpretation |
| `BLOCKED_METADATA_CONTRADICTION` | metadata contradictions invalidate readiness | request corrected metadata before interpretation |
| `CONTEXT_ONLY_OR_LABELS_NEEDED` | pharmacodynamic/context use only | do not call a response-validation result |
| `BELOW_V45_PLANNING_FLOOR` | too few labeled pairs for validation interpretation | do not call pass/fail/inconclusive from returned scores |
| `INCONCLUSIVE_SMALL_COHORT` | effect-size-with-CI language only; likely underpowered | do not over-read favorable or unfavorable scores |
| `MINIMUM_DECISION_GRADE_CAUTION` | V42 grid can be applied only if effect and diagnostics are clean | do not broaden beyond the frozen route |
| `CAUTION_BATCH_OR_CONFOUNDER` | V42 grid only with explicit diagnostic caveat | do not present a clean validation claim |
| `ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION` | mechanical V42/V45 interpretation allowed | no post-hoc thresholds, modules, timepoints, or analyses |

## Interpretation Boundary

This classifier answers only: "what wording is safe before interpreting returned
scores?" It is not a validation harness, does not change `LOCKED_RULE_V22.md`,
does not change the V42 pre-registration, and does not make a biological claim.

