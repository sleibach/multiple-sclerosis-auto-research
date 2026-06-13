# First-30 Repair Template Coverage Linter V46

Status: operations infrastructure. No validation result and no biological claim.

This linter verifies that first-30-minute returned-package stop routes either
stay local to operator software/no-raw repair or map to an existing safe
author-facing repair-request template.

Overall status: `PASS`.
First-30 rows: `46`; coverage rows: `143`; lint failures: `0`.

| Safe class | Template IDs |
|---|---|
| `BELOW_V45_PLANNING_FLOOR` | `below_planning_floor_labeled_pairs` |
| `BLOCKED_COMPLETENESS` | `missing_score_bearing_aggregate_outputs` |
| `BLOCKED_METADATA_CONTRADICTION` | `metadata_or_pairing_contradiction;response_label_orientation_ambiguous` |
| `BLOCKED_REDACTION` | `redaction_or_private_content_block` |
| `BLOCKED_SCHEMA` | `schema_or_metric_format_mismatch` |
| `BLOCKED_TERMS_OR_RECEIPT_GATES` | `terms_or_receipt_not_cleared` |
| `CAUTION_BATCH_OR_CONFOUNDER` | `batch_or_confounder_metadata_needed` |
| `CONTEXT_ONLY_OR_LABELS_NEEDED` | `response_labels_absent_or_unmapped` |
| `UNSCOREABLE_DATA` | `primary_module_coverage_block` |

Dynamic safe-class stop routes are covered by the full template index.
Local operator stops do not contact an author and therefore do not require
a repair-request template.
