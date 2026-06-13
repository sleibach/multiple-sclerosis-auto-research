# Report-Header Repair Request: missing_locked_rule_path

Status: report-header repair template. No validation result and no biological
claim.

Blocked header field: `locked_rule_path`

Failure trigger: required_field:locked_rule_path fails or locked_rule_path_exact fails

Temporary safe class: `BLOCKED_METADATA_CONTRADICTION`

Requested repair:

- Use the exact locked rule path `docs/locked_rules/LOCKED_RULE_V22.md` in the report header.

Required return:

- corrected report header only

Forbidden action:

- Do not substitute a successor, sensitivity, or local copy of the locked rule.

Boundary:

- This request concerns provenance/header metadata only.
- It does not ask for rerunning the locked rule, changing the locked rule,
  changing thresholds, changing labels, changing timepoints, or interpreting
  returned scores.
- No score-bearing text may appear before the corrected header passes the V46
  report-header metadata linter.
