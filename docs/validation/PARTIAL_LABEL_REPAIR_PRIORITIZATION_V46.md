# Partial-Label Repair Prioritization V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_partial_label_repair_prioritization.py` maps each V46
partial-label returned-package class to a repair priority, analyzable-pair
confidence band, safe repair-request template, and next operator action.

It joins existing method-only artifacts:

- `analysis/v46_partial_label_return_classifier/partial_label_synthetic_cases.tsv`
- `analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope.tsv`
- `analysis/v46_return_repair_request_templates/repair_request_template_index.tsv`

It does not open returned score tables, expression matrices, labels, or
quarantined cohorts.

## Command

```bash
.venv/bin/python scripts/v46_partial_label_repair_prioritization.py \
  --outdir analysis/v46_partial_label_repair_prioritization \
  --fail-on-error
```

## Current Result

- prioritization rows: `7`
- lint checks: `35`
- lint failures: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

Machine-readable outputs:

- `analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization_summary.json`
- `analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization.tsv`
- `analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization_lint.tsv`
- `analysis/v46_partial_label_repair_prioritization/PARTIAL_LABEL_REPAIR_PRIORITIZATION.md`

## Boundary

The priority is a repair-routing priority only. It does not authorize pass/fail,
AUC, effect-size, kill, or clinical interpretation language.
