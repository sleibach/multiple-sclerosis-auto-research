# First 30 Minutes Returned-Package Decision Table V46

Status: operations infrastructure. No validation result and no biological claim.

This table sequences the first 30 minutes after a returned aggregate package arrives.
Every row is pre-interpretation and has `score_values_read=false`.

Scenarios: `6`; rows: `46`; lint failures: `0`.

| Scenario | Window | Step | Action | Stop route |
|---|---|---:|---|---|
| `scored_canonical_aggregate` | `00-03` | 1 | Run local returned-package regression guard before touching package content | repair local software/readiness guard |
| `scored_canonical_aggregate` | `03-06` | 2 | Record non-sensitive receipt metadata and file listing only | keep package outside git and run no-raw scanner |
| `scored_canonical_aggregate` | `06-10` | 3 | Capture or resolve data-use terms class | repair template terms_or_receipt_not_cleared |
| `scored_canonical_aggregate` | `10-13` | 4 | Generate route-specific command order | matching repair template from blocked safe class |
| `scored_canonical_aggregate` | `17-21` | 5 | Run redaction and completeness return gate | repair template redaction_or_private_content_block or missing_score_bearing_aggregate_outputs |
| `scored_canonical_aggregate` | `21-24` | 6 | Run aggregate schema validator | repair template schema_or_metric_format_mismatch |
| `scored_canonical_aggregate` | `24-27` | 7 | Count analyzable response pairs and classify partial-label state | small-n language table plus repair template response_labels_absent_or_unmapped or below_planning_floor_labeled_pairs |
| `scored_canonical_aggregate` | `27-30` | 8 | Run safe-interpretation classifier or route to repair template without reading score values | matching repair template; no result report yet |
| `scored_noncanonical_aggregate` | `00-03` | 1 | Run local returned-package regression guard before touching package content | repair local software/readiness guard |
| `scored_noncanonical_aggregate` | `03-06` | 2 | Record non-sensitive receipt metadata and file listing only | keep package outside git and run no-raw scanner |
| `scored_noncanonical_aggregate` | `06-10` | 3 | Capture or resolve data-use terms class | repair template terms_or_receipt_not_cleared |
| `scored_noncanonical_aggregate` | `10-13` | 4 | Generate route-specific command order | matching repair template from blocked safe class |
| `scored_noncanonical_aggregate` | `13-17` | 5 | Normalize accepted noncanonical aggregate aliases if needed | repair template schema_or_metric_format_mismatch |
| `scored_noncanonical_aggregate` | `17-21` | 6 | Run redaction and completeness return gate | repair template redaction_or_private_content_block or missing_score_bearing_aggregate_outputs |
| `scored_noncanonical_aggregate` | `21-24` | 7 | Run aggregate schema validator | repair template schema_or_metric_format_mismatch |
| `scored_noncanonical_aggregate` | `24-26` | 8 | Refresh small-n conclusion language constraints | repair local planning artifact before report drafting |
| `scored_noncanonical_aggregate` | `27-30` | 9 | Run safe-interpretation classifier or route to repair template without reading score values | matching repair template; no result report yet |
| `scored_unknown_alias_aggregate` | `00-03` | 1 | Run local returned-package regression guard before touching package content | repair local software/readiness guard |
| `scored_unknown_alias_aggregate` | `03-06` | 2 | Record non-sensitive receipt metadata and file listing only | keep package outside git and run no-raw scanner |
| `scored_unknown_alias_aggregate` | `06-10` | 3 | Capture or resolve data-use terms class | repair template terms_or_receipt_not_cleared |
| `scored_unknown_alias_aggregate` | `10-13` | 4 | Generate route-specific command order | matching repair template from blocked safe class |
| `scored_unknown_alias_aggregate` | `13-17` | 5 | Normalize accepted noncanonical aggregate aliases if needed | repair template schema_or_metric_format_mismatch |
| `scored_unknown_alias_aggregate` | `17-21` | 6 | Run redaction and completeness return gate | repair template redaction_or_private_content_block or missing_score_bearing_aggregate_outputs |
| `scored_unknown_alias_aggregate` | `21-24` | 7 | Run aggregate schema validator | repair template schema_or_metric_format_mismatch |
| `scored_unknown_alias_aggregate` | `24-26` | 8 | Refresh small-n conclusion language constraints | repair local planning artifact before report drafting |
| `scored_unknown_alias_aggregate` | `27-30` | 9 | Run safe-interpretation classifier or route to repair template without reading score values | matching repair template; no result report yet |
| `unscoreable_aggregate` | `00-03` | 1 | Run local returned-package regression guard before touching package content | repair local software/readiness guard |
| `unscoreable_aggregate` | `03-06` | 2 | Record non-sensitive receipt metadata and file listing only | keep package outside git and run no-raw scanner |
| `unscoreable_aggregate` | `06-10` | 3 | Capture or resolve data-use terms class | repair template terms_or_receipt_not_cleared |
| `unscoreable_aggregate` | `10-13` | 4 | Generate route-specific command order | matching repair template from blocked safe class |
| `unscoreable_aggregate` | `17-21` | 5 | Run redaction and completeness return gate | repair template redaction_or_private_content_block or missing_score_bearing_aggregate_outputs |
| `unscoreable_aggregate` | `21-24` | 6 | Run aggregate schema validator | repair template schema_or_metric_format_mismatch |
| `unscoreable_aggregate` | `24-26` | 7 | Refresh small-n conclusion language constraints | repair local planning artifact before report drafting |
| `unscoreable_aggregate` | `27-30` | 8 | Run safe-interpretation classifier or route to repair template without reading score values | matching repair template; no result report yet |
| `partial_label_scored_aggregate` | `00-03` | 1 | Run local returned-package regression guard before touching package content | repair local software/readiness guard |
| `partial_label_scored_aggregate` | `03-06` | 2 | Record non-sensitive receipt metadata and file listing only | keep package outside git and run no-raw scanner |
| `partial_label_scored_aggregate` | `06-10` | 3 | Capture or resolve data-use terms class | repair template terms_or_receipt_not_cleared |
| `partial_label_scored_aggregate` | `10-13` | 4 | Generate route-specific command order | matching repair template from blocked safe class |
| `partial_label_scored_aggregate` | `17-21` | 5 | Run redaction and completeness return gate | repair template redaction_or_private_content_block or missing_score_bearing_aggregate_outputs |
| `partial_label_scored_aggregate` | `21-24` | 6 | Run aggregate schema validator | repair template schema_or_metric_format_mismatch |
| `partial_label_scored_aggregate` | `24-27` | 7 | Count analyzable response pairs and classify partial-label state | small-n language table plus repair template response_labels_absent_or_unmapped or below_planning_floor_labeled_pairs |
| `partial_label_scored_aggregate` | `27-30` | 8 | Run safe-interpretation classifier or route to repair template without reading score values | matching repair template; no result report yet |
| `terms_blocked_return` | `00-03` | 1 | Run local returned-package regression guard before touching package content | repair local software/readiness guard |
| `terms_blocked_return` | `03-06` | 2 | Record non-sensitive receipt metadata and file listing only | keep package outside git and run no-raw scanner |
| `terms_blocked_return` | `06-10` | 3 | Capture or resolve data-use terms class | repair template terms_or_receipt_not_cleared |
| `terms_blocked_return` | `10-12` | 4 | Stop at terms blocker; do not run package gates | repair template terms_or_receipt_not_cleared |

If any row stops, use the named repair template or local guard repair and rerun
the same first-30-minute sequence from the beginning for the repaired package.
