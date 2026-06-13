# Report-Header Repair Request: missing_or_wrong_locked_rule_sha256

Status: report-header repair template. No validation result and no biological
claim.

Blocked header field: `locked_rule_sha256`

Failure trigger: required_field:locked_rule_sha256 fails or locked_rule_hash_matches_v45_baseline fails

Temporary safe class: `BLOCKED_METADATA_CONTRADICTION`

Requested repair:

- Use the V45 locked-artifact hash baseline for `docs/locked_rules/LOCKED_RULE_V22.md`.

Required return:

- corrected report header plus locked-artifact hash audit output if mismatch persists

Forbidden action:

- Do not recompute or accept a different hash after seeing returned results.

Boundary:

- This request concerns provenance/header metadata only.
- It does not ask for rerunning the locked rule, changing the locked rule,
  changing thresholds, changing labels, changing timepoints, or interpreting
  returned scores.
- No score-bearing text may appear before the corrected header passes the V46
  report-header metadata linter.
