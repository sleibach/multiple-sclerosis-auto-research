# Report-Header Repair Request: missing_route_class

Status: report-header repair template. No validation result and no biological
claim.

Blocked header field: `route_class`

Failure trigger: required_field:route_class fails or route_class_known fails

Temporary safe class: `BLOCKED_METADATA_CONTRADICTION`

Requested repair:

- Provide the route class emitted by the returned-package command plan or preflight dry run.

Required return:

- corrected report header plus the command-plan summary that produced the route

Forbidden action:

- Do not choose a route based on whether returned metrics look favorable.

Boundary:

- This request concerns provenance/header metadata only.
- It does not ask for rerunning the locked rule, changing the locked rule,
  changing thresholds, changing labels, changing timepoints, or interpreting
  returned scores.
- No score-bearing text may appear before the corrected header passes the V46
  report-header metadata linter.
