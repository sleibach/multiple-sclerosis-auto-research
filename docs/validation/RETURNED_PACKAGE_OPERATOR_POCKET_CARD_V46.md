# Returned-Package Operator Pocket Card V46

Status: generated operator navigation. No validation result and no biological
claim.

## Purpose

`scripts/v46_returned_package_operator_pocket_card.py` generates a compact
one-page operator card from the quickstart command table, first-30-minute status
board, and safe-class report-template map. It is meant for fast orientation when
a returned package arrives in an unexpected shape.

## Command

```bash
.venv/bin/python scripts/v46_returned_package_operator_pocket_card.py \
  --outdir analysis/v46_returned_package_operator_pocket_card \
  --fail-on-error
```

## Current Result

- selected commands: `7`
- first-30 scenarios: `6`
- safe classes shown: `6`
- lint failures: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

## Outputs

- `analysis/v46_returned_package_operator_pocket_card/pocket_card_summary.json`
- `analysis/v46_returned_package_operator_pocket_card/RETURNED_PACKAGE_OPERATOR_POCKET_CARD.md`
- `analysis/v46_returned_package_operator_pocket_card/pocket_card_commands.tsv`
- `analysis/v46_returned_package_operator_pocket_card/pocket_card_first30.tsv`
- `analysis/v46_returned_package_operator_pocket_card/pocket_card_safe_classes.tsv`
- `analysis/v46_returned_package_operator_pocket_card/pocket_card_lint.tsv`

## Boundary

This card is navigation only. It does not read returned score tables, labels,
expression matrices, or quarantined cohorts, and it does not authorize result
wording.
