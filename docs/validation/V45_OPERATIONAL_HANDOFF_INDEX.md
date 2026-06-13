# V45 Operational Handoff Index

Status: compact operator index. No biological claim.

Machine-readable index:

`docs/validation/input_schemas/V45_operational_handoff_index.tsv`

Purpose: list the current top-level V45 operational artifacts in execution order
so medical-team operators can navigate the readiness package without reading the
full artifact corpus.

## Execution Order

| Order | Phase | Artifact |
|---:|---|---|
| 0 | local smoke test | `docs/validation/OPERATOR_SMOKE_TEST_BUNDLE_V46.md` |
| 1 | current action | `docs/validation/CURRENT_ACTION_CARD_V45.md` |
| 2 | cold-start sequence | `docs/validation/COLD_START_OPERATOR_SEQUENCE_V45.md` |
| 3 | current status | `docs/validation/READINESS_STATUS_DASHBOARD_V45.md` |
| 4 | current blockers | `docs/validation/EXTERNAL_BLOCKER_BOARD_V45.md` |
| 5 | blocker escalation | `docs/validation/EXTERNAL_BLOCKER_ESCALATION_MATRIX_V45.md` |
| 6 | follow-up escalation packets | `docs/validation/FOLLOWUP_ESCALATION_PACKETS_V45.md` |
| 7 | outbound packet integrity | `docs/validation/OUTBOUND_REQUEST_PACKET_INTEGRITY_V45.md` |
| 8 | request/follow-up | `docs/validation/FOLLOWUP_DUE_BOARD_V45.md` |
| 9 | request/follow-up drafts | `docs/validation/FOLLOWUP_MESSAGE_TEMPLATES_V45.md` |
| 10 | author-run bundle dry-run | `docs/validation/AUTHOR_RUN_BUNDLE_DRYRUN_MANIFEST_V45.md` |
| 11 | send-log intake | `docs/validation/SEND_LOG_INTAKE_TEMPLATE_V45.md` |
| 12 | route arrival | `docs/validation/ROUTE_ARRIVAL_COMMAND_PACKETS_V45.md` |
| 13 | route packet integrity | `docs/validation/ROUTE_PACKET_INTEGRITY_MANIFEST_V45.md` |
| 14 | cross-route readiness | `docs/validation/CROSS_ROUTE_READINESS_LINTER_V45.md` |
| 15 | no-score gate linter | `docs/validation/NO_SCORE_BEFORE_GATES_LINTER_V45.md` |
| 16 | state machine | `docs/validation/VALIDATION_STATE_MACHINE_V45.md` |
| 17 | transition consistency | `docs/validation/STATE_MACHINE_TRANSITION_VALIDATOR_V45.md` |
| 18 | received package decision tree | `docs/validation/RECEIVED_PACKAGE_DECISION_TREE_V45.md` |
| 19 | received package gates | `docs/validation/FIRST_24H_RECEIVED_DATA_OPERATOR_CHECKLIST_V45.md` |
| 20 | frozen-harness readiness | `docs/validation/HARNESS_READY_DECISION_TEMPLATE_V45.md` |
| 21 | author-run fallback | `docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md` |
| 22 | secondary route freeze | `docs/validation/SECONDARY_ROUTE_NO_DOF_CHECKLIST_V45.md` |
| 23 | result reporting | `docs/validation/VALIDATION_RESULT_REPORT_TEMPLATE_V45.md` |
| 24 | interpretation | `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md` |
| 25 | integrity refresh | `docs/validation/PRECOMMIT_READINESS_CHECKLIST_V45.md` |
| 26 | freshness check | `docs/validation/READINESS_STALE_OUTPUT_DETECTOR_V45.md` |

## Current Headline

The current operational state remains:

`READY_AWAITING_EXTERNAL_DATA`

The immediate operational action is external: send or approve the live request
routes listed in `docs/validation/CURRENT_ACTION_CARD_V45.md`. No cohort is
harness-ready.
