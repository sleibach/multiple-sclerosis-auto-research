# Validation State Machine V45

Status: operational state-machine summary. No rule change and no biological
claim.

Machine-readable table:

`docs/validation/input_schemas/V45_validation_state_machine.tsv`

Purpose: give operators one consolidated map from request preparation through
receipt, preflight, optional author-run return, reporting, and interpretation.
The table summarizes existing gates only; it does not create new gates or alter
the V22/V42 locked analysis.

## State Order

| Order | State | Exit condition | Next allowed action |
|---:|---|---|---|
| 1 | request packet ready | exact request text and target route exist | send request only after human contact approval |
| 2 | request sent | sent copy and follow-up date logged | wait, follow up, or receive package |
| 3 | package received | receipt path, terms, and checksums are captured | quarantine/preflight only |
| 4 | metadata preflight | schema, subject map, label dictionary, and module coverage gates pass | finalize required addendum before scoring |
| 5 | frozen harness ready | all required gates pass and locked artifacts match hashes | run only the matching frozen harness |
| 6 | aggregate author-run return | redaction and completeness gates pass | fill result report from aggregate outputs only |
| 7 | result report complete | metrics and counts trace to frozen outputs | classify under the precommitted outcome grid |
| 8 | interpreted result | outcome-grid classification complete | update status/dashboard and define next external action |

## Forbidden Transitions

| From | Forbidden jump | Reason |
|---|---|---|
| request packet ready | frozen harness run | no data are available |
| request sent | validation claim | request state is not receipt or scoring |
| package received | module scoring | terms/checksum/preflight may still fail |
| metadata preflight | rule tuning | locked V22/V42 rule is immutable |
| author-run return | interpretation before redaction/completeness | aggregate package may leak private data or lack required metrics |
| result report | post-hoc threshold adjustment | outcome grid was precommitted blind |

## Linked Gate Artifacts

- `docs/validation/OUTBOUND_DATA_REQUEST_TRACKER_V45.md`
- `docs/validation/FOLLOWUP_DUE_BOARD_V45.md`
- `docs/validation/EXTERNAL_BLOCKER_BOARD_V45.md`
- `docs/validation/FIRST_24H_RECEIVED_DATA_OPERATOR_CHECKLIST_V45.md`
- `docs/validation/VALIDATION_INTAKE_PREFLIGHT_V45.md`
- `docs/validation/HARNESS_READY_DECISION_TEMPLATE_V45.md`
- `docs/validation/AUTHOR_RUN_RETURN_GATE_RUNNER_V45.md`
- `docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md`
- `docs/validation/VALIDATION_RESULT_REPORT_TEMPLATE_V45.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`

## Current State

The current dashboard state is `READY_AWAITING_EXTERNAL_DATA`: internal guards
are ready, but all live routes remain before or at request-send/follow-up state
and `0` cohorts are harness-ready.
