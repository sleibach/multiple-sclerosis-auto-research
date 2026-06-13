# Report-Header Repair Request: missing_safe_class

Status: report-header repair template. No validation result and no biological
claim.

Blocked header field: `safe_class`

Failure trigger: required_field:safe_class fails or safe_class_known fails

Temporary safe class: `BLOCKED_METADATA_CONTRADICTION`

Requested repair:

- Provide the V46 safe-interpretation class emitted by the safe-interpretation classifier.

Required return:

- corrected report header plus safe-interpretation summary

Forbidden action:

- Do not invent a safe class manually from the result text.

Boundary:

- This request concerns provenance/header metadata only.
- It does not ask for rerunning the locked rule, changing the locked rule,
  changing thresholds, changing labels, changing timepoints, or interpreting
  returned scores.
- No score-bearing text may appear before the corrected header passes the V46
  report-header metadata linter.
