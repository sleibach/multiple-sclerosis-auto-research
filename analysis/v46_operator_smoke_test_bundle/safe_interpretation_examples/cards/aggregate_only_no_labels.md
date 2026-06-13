# aggregate_only_no_labels

Status: safe wording example. No validation result and no biological claim.

Scenario: Aggregate package has module context but no mapped response labels.
Safe class: `CONTEXT_ONLY_OR_LABELS_NEEDED`.
Report mode: `STOP_ONLY`.
Planning band: `no_mapped_response_groups` (`0_or_single_class`).
Allowed sentence: This return is context-only because paired response labels are absent or not mapped; no response-validation result is available.
Report boundary: Stop before result wording.
Next action: Request sample-mapped response labels or a valid aggregate author-run return containing the locked-rule metrics.
Skeleton: `analysis/v46_safe_class_report_template_readiness/fixtures/context_only_or_labels_needed.md`.
