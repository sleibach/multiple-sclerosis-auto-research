# Receipt Manifest To Command Plan Handoff V46

This is returned-package operations infrastructure. It connects:

- `scripts/v46_receipt_manifest_schema_linter.py`
- `scripts/v46_package_manifest_shape_classifier.py`
- `scripts/v46_returned_package_command_order_planner.py`

The handoff is intentionally pre-score. It reads only synthetic receipt
manifests, non-sensitive filenames, and generated gate summaries. It does not
read returned metric values, expression data, labels, or quarantined cohorts.

## Current Result

Command:

```bash
.venv/bin/python scripts/v46_receipt_manifest_to_command_plan_handoff.py \
  --outdir analysis/v46_receipt_manifest_to_command_plan_handoff \
  --fail-on-error
```

Current synthetic verification:

- Overall status: `PASS`
- Synthetic cases: `8`
- Schema-fail hard-stop cases: `3`
- Schema-pass command-plan cases: `5`
- Lint checks: `64`
- Lint failures: `0`
- Score values read: `false`

## Operator Rule

If receipt-manifest schema lint is not `PASS`, stop before shape
classification and request manifest repair.

If receipt-manifest schema lint is `PASS`, run the generated shape-classifier
command, then pass the classifier's package-state and metric-format state to
the generated command-order planner.

The command-order planner's `stop_if` fields remain the source of truth for
downstream stops. A terms-blocked package can pass receipt schema lint and
shape classification, but it still stops at `stop_terms_block` before any
package gate, schema check, score reading, or interpretation.

## Generated Artifacts

- `analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff_summary.json`
- `analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff.tsv`
- `analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff_lint.tsv`
- `analysis/v46_receipt_manifest_to_command_plan_handoff/RECEIPT_MANIFEST_TO_COMMAND_PLAN_HANDOFF.md`

This artifact is included in the V46 regression suite, operator smoke bundle,
returned-package handoff manifest, documentation cross-link linter, stale-output
detector, and synthetic artifact index.
