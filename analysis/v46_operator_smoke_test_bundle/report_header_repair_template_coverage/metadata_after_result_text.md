# Report-Header Repair Request: metadata_after_result_text

Status: report-header repair template. No validation result and no biological
claim.

Blocked header field: `all_required_fields`

Failure trigger: metadata_before_result_text fails

Temporary safe class: `BLOCKED_METADATA_CONTRADICTION`

Requested repair:

- Move all required provenance fields before any result heading or score-bearing language.

Required return:

- corrected report header ordering only

Forbidden action:

- Do not leave score-bearing language above missing or late provenance metadata.

Boundary:

- This request concerns provenance/header metadata only.
- It does not ask for rerunning the locked rule, changing the locked rule,
  changing thresholds, changing labels, changing timepoints, or interpreting
  returned scores.
- No score-bearing text may appear before the corrected header passes the V46
  report-header metadata linter.
