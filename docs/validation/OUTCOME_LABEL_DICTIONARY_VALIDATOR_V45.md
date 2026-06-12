# Outcome-Label Dictionary Validator V45

Status: outcome-definition metadata validator. No expression data or labels are
scored by this script.

Purpose: verify that a filled outcome-label dictionary is complete and frozen
before any response scoring or cohort-specific addendum is finalized.

## Filled Dictionary Formats

The validator accepts either:

1. long format with columns `field` and `value`; or
2. one-row wide format with the template field names as columns.

The field definitions come from:

`docs/validation/input_schemas/V45_outcome_label_dictionary_template.tsv`

## Commands

Validate a received dictionary:

```bash
.venv/bin/python scripts/v45_outcome_label_dictionary_validator.py check \
  --dictionary data/quarantine/<cohort>/metadata/outcome_label_dictionary.tsv \
  --outdir analysis/validation_command_runs/outcome_dictionary/<cohort> \
  --fail-on-error
```

Synthetic validator check:

```bash
.venv/bin/python scripts/v45_outcome_label_dictionary_validator.py synthetic-check \
  --outdir analysis/v45_outcome_label_dictionary_validator
```

## Current Synthetic Verification

| Fixture | Expected | Observed |
|---|---|---|
| frozen synthetic dictionary | `PASS` | `PASS` |
| ambiguous synthetic dictionary | `FAIL` | `FAIL` |

The failing fixture is deliberately not frozen and has overlapping raw positive
and negative values. This verifies the validator blocks ambiguous orientation
before scoring.

## What Is Checked

The validator checks:

- all required template fields have values;
- enum fields use allowed values;
- UTC date fields use `YYYY-MM-DD`;
- `status=frozen_ready_for_addendum` before scoring;
- raw positive and negative values do not overlap;
- harness positive and negative classes are not identical.

It does not:

- open expression matrices;
- inspect outcome tables beyond the dictionary itself;
- count responders/nonresponders;
- choose an endpoint;
- change the locked score or V42 thresholds.

## Guardrail

If validation fails, stop before scoring. The repair is to request or document
the missing outcome-definition information blind to module scores. Do not infer
orientation from a favorable AUC or from module behavior.
