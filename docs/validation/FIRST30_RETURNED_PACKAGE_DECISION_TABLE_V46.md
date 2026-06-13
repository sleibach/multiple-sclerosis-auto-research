# First 30 Minutes Returned-Package Decision Table V46

Status: operations infrastructure. No validation result and no biological claim.

## Purpose

`scripts/v46_first30_returned_package_decision_table.py` generates a
scenario-specific operator table for the first 30 minutes after a returned
aggregate package arrives. It covers scored canonical aggregate returns,
noncanonical/unknown alias returns, unscoreable returns, partial-label returns,
and terms-blocked returns.

The table sequences only existing frozen V45/V46 gates and never authorizes
score interpretation. Every generated row has `score_values_read=false`.

## Command

```bash
.venv/bin/python scripts/v46_first30_returned_package_decision_table.py \
  --outdir analysis/v46_first30_returned_package_decision_table \
  --fail-on-error
```

## Current Result

Current status: `PASS`.

The generated decision table covers:

- scenarios: `6`
- rows: `46`
- lint checks: `92`
- lint failures: `0`
- all first-30-minute rows have `score_values_read=false`

Machine-readable outputs:

- `analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_summary.json`
- `analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_table.tsv`
- `analysis/v46_first30_returned_package_decision_table/first30_returned_package_decision_lint.tsv`
- `analysis/v46_first30_returned_package_decision_table/FIRST30_RETURNED_PACKAGE_DECISION_TABLE.md`

## Boundary

If any first-30-minute row stops, the operator uses the named repair template or
local guard repair and reruns the same sequence after the package is repaired.
The first 30 minutes are for receipt, terms, gate ordering, redaction,
completeness, schema, partial-label, small-n, and safe-class routing only. They
are not for reading returned scores or assigning a validation result.
