# Returned-Package Documentation Cross-Link Linter V46

Status: operator navigation infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_returned_package_doc_crosslink_linter.py` proves that the V46
returned-package guard stack is navigable: every required returned-package
script has a committed script file, a committed documentation file, a direct
reference from that documentation file to the script, and at least one
operator-facing route reference.

The linter is intentionally narrow. It checks documentation reachability only.
It does not open returned score tables, expression matrices, labels, or
quarantined cohorts.

## Command

```bash
.venv/bin/python scripts/v46_returned_package_doc_crosslink_linter.py \
  --outdir analysis/v46_returned_package_doc_crosslink_linter \
  --fail-on-error
```

## Current Result

- scripts checked: `24`
- lint checks: `96`
- script/doc/operator-reference failures: `0`
- all `score_values_read`: `false`
- overall status: `PASS`

Machine-readable outputs:

- `analysis/v46_returned_package_doc_crosslink_linter/returned_package_doc_crosslink_summary.json`
- `analysis/v46_returned_package_doc_crosslink_linter/returned_package_doc_crosslink.tsv`
- `analysis/v46_returned_package_doc_crosslink_linter/returned_package_doc_crosslink_lint.tsv`
- `analysis/v46_returned_package_doc_crosslink_linter/RETURNED_PACKAGE_DOC_CROSSLINK_LINTER.md`

## Boundary

A `PASS` means the returned-package scripts are reachable from the documented
operator path. It does not mean data have arrived, terms permit processing, or
any validation result is interpretable.
