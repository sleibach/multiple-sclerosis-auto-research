# Report-Header Repair Request: missing_cohort_token

Status: report-header repair template. No validation result and no biological
claim.

Blocked header field: `cohort_token`

Failure trigger: required_field:cohort_token fails or token format is invalid

Temporary safe class: `BLOCKED_METADATA_CONTRADICTION`

Requested repair:

- Provide the cohort token used in the receipt manifest and status board, without changing any returned metrics.

Required return:

- corrected report header only; receipt manifest if the cohort token is ambiguous

Forbidden action:

- Do not infer cohort identity from score values, labels, or expression data.

Boundary:

- This request concerns provenance/header metadata only.
- It does not ask for rerunning the locked rule, changing the locked rule,
  changing thresholds, changing labels, changing timepoints, or interpreting
  returned scores.
- No score-bearing text may appear before the corrected header passes the V46
  report-header metadata linter.
