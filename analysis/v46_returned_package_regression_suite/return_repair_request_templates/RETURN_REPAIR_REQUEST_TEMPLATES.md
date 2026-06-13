# Return Repair Request Templates V46

Status: operations infrastructure. No validation result and no biological claim.

These templates map blocked returned-package states to safe author-facing
repair requests. They do not inspect returned scores and do not authorize
interpretation.

| Template | Safe class | Failure code | Path |
|---|---|---|---|
| `terms_or_receipt_not_cleared` | `BLOCKED_TERMS_OR_RECEIPT_GATES` | `TERMS_NOT_APPROVED` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/terms_or_receipt_not_cleared.md` |
| `redaction_or_private_content_block` | `BLOCKED_REDACTION` | `RAW_DATA_GIT_HARD_FAIL` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/redaction_or_private_content_block.md` |
| `missing_score_bearing_aggregate_outputs` | `BLOCKED_COMPLETENESS` | `UNSCOREABLE_MISSING_LOCKED_RULE_METRICS` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/missing_score_bearing_aggregate_outputs.md` |
| `schema_or_metric_format_mismatch` | `BLOCKED_SCHEMA` | `METADATA_REQUIRED_COLUMN_MISSING` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/schema_or_metric_format_mismatch.md` |
| `response_labels_absent_or_unmapped` | `CONTEXT_ONLY_OR_LABELS_NEEDED` | `OUTCOME_DICTIONARY_MISSING` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/response_labels_absent_or_unmapped.md` |
| `response_label_orientation_ambiguous` | `BLOCKED_METADATA_CONTRADICTION` | `OUTCOME_DICTIONARY_AMBIGUOUS` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/response_label_orientation_ambiguous.md` |
| `below_planning_floor_labeled_pairs` | `BELOW_V45_PLANNING_FLOOR` | `UNDERPOWERED_GROUP_SIZE` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/below_planning_floor_labeled_pairs.md` |
| `metadata_or_pairing_contradiction` | `BLOCKED_METADATA_CONTRADICTION` | `EXPRESSION_SAMPLE_MISMATCH` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/metadata_or_pairing_contradiction.md` |
| `primary_module_coverage_block` | `UNSCOREABLE_DATA` | `PRIMARY_MODULE_COVERAGE_FAIL` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/primary_module_coverage_block.md` |
| `batch_or_confounder_metadata_needed` | `CAUTION_BATCH_OR_CONFOUNDER` | `BATCH_DIAGNOSTIC_WARNING` | `analysis/v46_returned_package_regression_suite/return_repair_request_templates/templates/batch_or_confounder_metadata_needed.md` |

Use the first failing returned-package gate to choose the template. If a
package has multiple blockers, request the earliest blocking repair first
and rerun the same gates after receipt.
