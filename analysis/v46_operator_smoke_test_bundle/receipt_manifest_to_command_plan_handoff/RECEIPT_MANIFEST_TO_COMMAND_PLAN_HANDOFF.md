# Receipt Manifest To Command Plan Handoff V46

This generated handoff table links the receipt-manifest schema outcome to the next allowed returned-package command.
It is synthetic operations infrastructure only: it reads receipt manifests and generated summaries, never returned score values, expression data, labels, or quarantined cohorts.

## Current Result

- Overall status: `PASS`
- Synthetic handoff cases: `8`
- Lint checks: `64`
- Lint failures: `0`
- All score values read false: `true`

## Handoff Table

| Case | Schema | First-30 Scenario | Plan Status | Terminal Stage | Next Action |
|---|---:|---|---:|---|---|
| schema_fail_missing_required_column | `FAIL` | `NOT_RUN` | `NOT_RUN` | `STOP_RECEIPT_MANIFEST_REPAIR` | `STOP` |
| schema_fail_raw_path | `FAIL` | `NOT_RUN` | `NOT_RUN` | `STOP_RECEIPT_MANIFEST_REPAIR` | `STOP` |
| scored_canonical_to_plan | `PASS` | `scored_canonical_aggregate` | `PASS` | `COMMAND_PLAN_WRITTEN` | `classify_manifest_then_plan` |
| scored_noncanonical_to_adapter_branch | `PASS` | `scored_noncanonical_aggregate` | `PASS` | `COMMAND_PLAN_WRITTEN` | `classify_manifest_then_plan` |
| partial_label_to_plan_with_label_classifier | `PASS` | `partial_label_scored_aggregate` | `PASS` | `COMMAND_PLAN_WRITTEN` | `classify_manifest_then_plan` |
| unscoreable_author_run_aggregate_to_preflight_only | `PASS` | `unscoreable_aggregate` | `PASS` | `COMMAND_PLAN_WRITTEN` | `classify_manifest_then_plan` |
| terms_blocked_after_shape | `PASS` | `terms_blocked_return` | `BLOCKED` | `STOP_TERMS_BLOCK` | `classify_manifest_then_plan` |
| unknown_score_like_filename_stops_at_schema | `FAIL` | `NOT_RUN` | `NOT_RUN` | `STOP_RECEIPT_MANIFEST_REPAIR` | `STOP` |

## Operator Rule

If receipt-manifest schema lint is not `PASS`, stop before shape classification and request manifest repair.
If it is `PASS`, run the generated shape-classifier command, then pass its package-state and metric-format state to the generated command-order planner.
The planner's own `stop_if` fields remain the source of truth for downstream hard stops.

Primary generated table: `analysis/v46_receipt_manifest_to_command_plan_handoff/receipt_manifest_to_command_plan_handoff.tsv`.
