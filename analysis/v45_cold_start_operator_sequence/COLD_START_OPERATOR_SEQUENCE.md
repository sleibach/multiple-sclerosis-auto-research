# V45 Cold-Start Operator Sequence

Status: generated operational plan. No biological claim and no scoring authorization.

Use this when resuming from a clean checkout or when a package arrives. It is derived from the current action card, route-arrival packet index, received-package decision tree, and command-plan outputs.

Hard rule: if `may_score_now` is `no`, do not run module scoring, outcome scoring, or interpretation.

| Priority | Cohort | Current blocker | Operator now | If package arrives | Gate / command plan | May score now |
|---:|---|---|---|---|---|---|
| 1 | `gafson_dmf_2018` | `data_not_local` | send_request_when_human_approves_contact | quarantine files, capture terms, write checksums, fill first-24h operator status, then run received-status updater | `analysis/v45_validation_command_runner/gafson_primary_plan/command_plan.md` | `no` |
| 2 | `karolinska_dmf_ros_2019` | `labels_and_subject_map_absent_publicly` | send_request_when_human_approves_contact | quarantine files, capture terms, write checksums, fill first-24h operator status, then run received-status updater | `analysis/v45_validation_command_runner/karolinska_primary_plan/command_plan.md` | `no` |
| 3 | `gse228330_ocrelizumab_pbmc` | `public_response_labels_absent_and_subject_map_unverified` | send_request_when_human_approves_contact | quarantine files, capture terms, write checksums, fill first-24h operator status, then run received-status updater | `analysis/v45_validation_command_runner/gse228330_pharmacodynamic_plan/command_plan.md` | `no` |
| 4 | `any_author_run_fallback` | `local_run_of_frozen_harness_plus_non_sensitive_aggregate_outputs` | send_request_when_human_approves_contact | run author-run return redaction/completeness gate on aggregate output package only | `docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md` | `no` |

## Required Source Artifacts

- `analysis/v45_current_action_card/current_action_card.tsv`
- `analysis/v45_received_package_decision_tree/live/received_package_decision_tree.tsv`
- `analysis/v45_route_arrival_packets/route_arrival_packet_index.tsv`

This generated sequence is an operator convenience layer. The linked route packet and frozen preregistration remain authoritative.
