# Returned-Package Operator Pocket Card V46

Status: generated operator pocket card. No validation result and no biological claim.

## First Rule

Do not open score-bearing files, labels, expression matrices, or quarantined cohorts until the route gates say the package is reviewable.

## Minimal Command Path

| Order | Artifact | Command |
|---:|---|---|
| 1 | `current_action_card` | `.venv/bin/python scripts/v45_current_action_card.py --outdir analysis/v45_current_action_card` |
| 2 | `cold_start_operator_sequence` | `.venv/bin/python scripts/v45_cold_start_operator_sequence.py --outdir analysis/v45_cold_start_operator_sequence` |
| 3 | `receipt_manifest_schema_linter` | `.venv/bin/python scripts/v46_receipt_manifest_schema_linter.py lint --manifest <receipt_manifest.tsv> --outdir analysis/v46_receipt_manifest_schema_linter/<cohort>_<date> --fail-on-error` |
| 4 | `package_manifest_shape_classifier` | `.venv/bin/python scripts/v46_package_manifest_shape_classifier.py classify --manifest <receipt_manifest.tsv> --terms-class <TERMS_CLASS> --outdir analysis/v46_package_manifest_shape_classifier/<cohort>_<date> --fail-on-error` |
| 7 | `first30_status_board` | `.venv/bin/python scripts/v46_first30_returned_package_status_board_dryrun.py --outdir analysis/v46_first30_returned_package_status_board_dryrun --fail-on-error` |
| 11 | `command_order_planner` | `.venv/bin/python scripts/v46_returned_package_command_order_planner.py plan --cohort-token <cohort>_<date> --package-root <returned_package_dir> --terms-capture <terms_capture_tsv> --terms-class <TERMS_CLASS> --package-kind author_run_aggregate --package-state <package_state> --metric-format-state <metric_format_state> --outdir analysis/v46_returned_package_command_order_planner/<cohort>_<date> --expect-status <PASS_or_BLOCKED>` |
| 13 | `safe_interpretation_classifier` | `.venv/bin/python scripts/v46_returned_package_safe_interpretation.py classify --gate-summary <gate_summary> --schema-summary <schema_summary> --analyzable-summary <analyzable_summary> --metadata-summary <metadata_summary> --batch-confounder-summary <batch_summary> --terms-status PASS --outdir analysis/v46_returned_package_safe_interpretation/<cohort>_<date>` |

## First-30-Minute Branches

| Scenario | Status | Next action | Safe wording |
|---|---|---|---|
| `scored_canonical_aggregate` | `ROUTE_READY_FOR_GATED_REVIEW` | Generate route-specific command order | Returned package is in pre-result gated review; no validation interpretation is available yet. |
| `scored_noncanonical_aggregate` | `FORMAT_NORMALIZATION_REQUIRED` | Normalize accepted noncanonical aggregate aliases if needed | Returned package requires format normalization before any result interpretation is available. |
| `scored_unknown_alias_aggregate` | `FORMAT_ALIAS_TRIAGE_REQUIRED` | Normalize accepted noncanonical aggregate aliases if needed | Returned package is in format triage; no validation interpretation is available yet. |
| `unscoreable_aggregate` | `UNSCOREABLE_AGGREGATE_PREFLIGHT` | Run redaction and completeness return gate | Returned package is not result-reviewable unless required aggregate outputs are supplied. |
| `partial_label_scored_aggregate` | `PARTIAL_LABEL_PAIR_COUNT_REQUIRED` | Count analyzable response pairs and classify partial-label state | Returned package needs response-label coverage classification before any validation interpretation is available. |
| `terms_blocked_return` | `BLOCKED_TERMS_OR_RECEIPT` | Stop at terms blocker; do not run package gates | Returned package is blocked at terms or receipt clearance; no package review is permitted yet. |

## Safe-Class Boundaries

| Safe class | Report mode | Meaning |
|---|---|---|
| `BLOCKED_TERMS_OR_RECEIPT_GATES` | `STOP_ONLY` | Terms or receipt evidence blocks interpretation. |
| `BLOCKED_COMPLETENESS` | `STOP_ONLY` | Required aggregate outputs are missing. |
| `CONTEXT_ONLY_OR_LABELS_NEEDED` | `STOP_ONLY` | Package can support context only; response labels are absent or insufficient. |
| `INCONCLUSIVE_SMALL_COHORT` | `RESULT_SKELETON_ALLOWED_AFTER_GATES` | Effect-size-with-CI placeholders only, with small-n caution. |
| `CAUTION_BATCH_OR_CONFOUNDER` | `RESULT_SKELETON_ALLOWED_AFTER_GATES` | V42 grid may be applied only with diagnostic caveat language. |
| `ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION` | `RESULT_SKELETON_ALLOWED_AFTER_GATES` | Mechanical V42 interpretation skeleton is available. |

Boundary: this pocket card is generated from quickstart commands, the
first-30 status board, and the safe-class map. It is navigation only.
