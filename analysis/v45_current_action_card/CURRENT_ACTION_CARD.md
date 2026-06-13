# V45 Current Action Card

Status: generated operational card. No biological claim.

Headline status: `READY_AWAITING_EXTERNAL_DATA`

## Guard Status

| Guard | Status | Source |
|---|---|---|
| precommit_readiness | `PASS` | `analysis/v45_precommit_readiness/precommit_readiness_summary.json` |
| state_machine_transition_validator | `PASS` | `analysis/v45_state_machine_validator/live/state_machine_validator_summary.json` |
| route_packet_integrity | `PASS` | `analysis/v45_route_packet_integrity_manifest/live/route_packet_integrity_summary.json` |
| v46_returned_package_regression_suite | `PASS` | `analysis/v46_returned_package_regression_suite/returned_package_regression_summary.json` |
| v46_operator_smoke_test_bundle | `PASS` | `analysis/v46_operator_smoke_test_bundle/operator_smoke_test_summary.json` |

## Current Actions

| Priority | Route | Action | Request/Packet | Why now |
|---:|---|---|---|---|
| 1 | `gafson_dmf_2018` | `send_request_when_human_approves_contact` | `docs/validation/outbound_requests/gafson_dmf_ready_to_send_V45.md` | route is internally prepared but externally blocked |
| 2 | `karolinska_dmf_ros_2019` | `send_request_when_human_approves_contact` | `docs/validation/outbound_requests/karolinska_dmf_ready_to_send_V45.md` | route is internally prepared but externally blocked |
| 3 | `gse228330_ocrelizumab_pbmc` | `send_request_when_human_approves_contact` | `docs/validation/outbound_requests/gse228330_ocrelizumab_ready_to_send_V45.md` | route is internally prepared but externally blocked |
| 4 | `any_author_run_fallback` | `send_request_when_human_approves_contact` | `docs/validation/outbound_requests/author_run_fallback_ready_to_send_V45.md` | route is internally prepared but externally blocked |

This card does not mark requests as sent, mark data as received, or make any
cohort harness-ready. It is a navigation layer over existing boards.
