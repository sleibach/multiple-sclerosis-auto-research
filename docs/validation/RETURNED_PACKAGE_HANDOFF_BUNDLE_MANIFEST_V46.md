# Returned-Package Handoff Bundle Manifest V46

Status: operator navigation infrastructure. No validation result and no biological claim.

Purpose: provide one deterministic navigation artifact for returned-package handling. It links the current-action card, cold-start sequence, receipt-manifest linter, manifest classifier, first-30 decision table, first-30 status board, command-order planner, safe interpretation, small-n/power language, repair templates, repair-template coverage, and report guard.

## Current Run

Command:

```bash
.venv/bin/python scripts/v46_returned_package_handoff_bundle_manifest.py --outdir analysis/v46_returned_package_handoff_bundle_manifest --fail-on-error
```

Result:

- overall status: `PASS`
- ordered manifest rows: `14`
- lint checks: `56`
- lint failures: `0`
- all `score_values_read`: `false`

## Boundary

This manifest is navigation only. It verifies that referenced scripts, docs, and primary generated outputs exist. It does not run validation, read returned scores, inspect expression data, read private labels, or authorize interpretation.

The interpretation boundary remains the V46 safe class and the frozen V42 pre-registration. The V22 locked rule remains unchanged.

## Outputs

- `analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_summary.json`
- `analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_manifest.tsv`
- `analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_lint.tsv`
- `analysis/v46_returned_package_handoff_bundle_manifest/RETURNED_PACKAGE_HANDOFF_BUNDLE_MANIFEST.md`
