# Report-Header Repair Request: missing_terms_class

Status: report-header repair template. No validation result and no biological
claim.

Blocked header field: `terms_class`

Failure trigger: required_field:terms_class fails or terms_class_known fails

Temporary safe class: `BLOCKED_TERMS_OR_RECEIPT_GATES`

Requested repair:

- Provide the terms-governance class from the receipt/terms preflight before any report interpretation proceeds.

Required return:

- corrected report header plus terms-governance preflight output

Forbidden action:

- Do not inspect or summarize score-bearing outputs until terms handling is cleared.

Boundary:

- This request concerns provenance/header metadata only.
- It does not ask for rerunning the locked rule, changing the locked rule,
  changing thresholds, changing labels, changing timepoints, or interpreting
  returned scores.
- No score-bearing text may appear before the corrected header passes the V46
  report-header metadata linter.
