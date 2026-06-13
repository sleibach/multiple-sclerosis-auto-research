# First-30 Returned-Package Status Board Dry Run V46

Status: operator infrastructure. No validation result and no biological claim.

This dry-run board summarizes the first-30-minute returned-package route
status without reading result values. It is intended for team status updates
before the V46 safe-interpretation classifier and V42 grid permit any result
language.

Rows: `6`; lint checks: `31`; failures: `0`.

| Scenario | Status | Blocker | Next action | Repair template |
|---|---|---|---|---|
| `scored_canonical_aggregate` | `MANUAL_DRIFT_STATUS` | none | Generate route-specific command order | `not_needed` |
| `scored_noncanonical_aggregate` | `FORMAT_NORMALIZATION_REQUIRED` | noncanonical aggregate aliases | Normalize accepted noncanonical aggregate aliases if needed | `schema_or_metric_format_mismatch` |
| `scored_unknown_alias_aggregate` | `FORMAT_ALIAS_TRIAGE_REQUIRED` | unknown aggregate alias state | Normalize accepted noncanonical aggregate aliases if needed | `schema_or_metric_format_mismatch` |
| `unscoreable_aggregate` | `UNSCOREABLE_AGGREGATE_PREFLIGHT` | missing or unscoreable aggregate outputs | Run redaction and completeness return gate | `missing_score_bearing_aggregate_outputs` |
| `partial_label_scored_aggregate` | `PARTIAL_LABEL_PAIR_COUNT_REQUIRED` | partial or unmapped response labels | Count analyzable response pairs and classify partial-label state | `response_labels_absent_or_unmapped` |
| `terms_blocked_return` | `BLOCKED_TERMS_OR_RECEIPT` | terms or receipt clearance missing | Stop at terms blocker; do not run package gates | `terms_or_receipt_not_cleared` |

Every row has `score_values_read=false`. Status sentences are deliberately
pre-result and cannot be used as validation interpretation.
