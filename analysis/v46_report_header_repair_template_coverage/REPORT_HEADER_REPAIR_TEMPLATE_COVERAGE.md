# Report-Header Repair Template Coverage V46

Status: report-governance infrastructure. No validation result and no biological claim.

This map links every report-header metadata failure to a safe repair request
before any result or score-bearing text may proceed.

| Issue | Field | Safe class | Trigger |
|---|---|---|---|
| `missing_cohort_token` | `cohort_token` | `BLOCKED_METADATA_CONTRADICTION` | required_field:cohort_token fails or token format is invalid |
| `missing_route_class` | `route_class` | `BLOCKED_METADATA_CONTRADICTION` | required_field:route_class fails or route_class_known fails |
| `missing_terms_class` | `terms_class` | `BLOCKED_TERMS_OR_RECEIPT_GATES` | required_field:terms_class fails or terms_class_known fails |
| `missing_safe_class` | `safe_class` | `BLOCKED_METADATA_CONTRADICTION` | required_field:safe_class fails or safe_class_known fails |
| `missing_locked_rule_path` | `locked_rule_path` | `BLOCKED_METADATA_CONTRADICTION` | required_field:locked_rule_path fails or locked_rule_path_exact fails |
| `missing_or_wrong_locked_rule_sha256` | `locked_rule_sha256` | `BLOCKED_METADATA_CONTRADICTION` | required_field:locked_rule_sha256 fails or locked_rule_hash_matches_v45_baseline fails |
| `metadata_after_result_text` | `all_required_fields` | `BLOCKED_METADATA_CONTRADICTION` | metadata_before_result_text fails |

## Templates

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

