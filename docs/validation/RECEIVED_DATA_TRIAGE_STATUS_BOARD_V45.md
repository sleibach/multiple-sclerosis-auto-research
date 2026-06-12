# V45 Received-Data Triage Status Board

Status: acquisition operations artifact. No data received or analyzed.

## Purpose

This board prevents a common failure mode: treating "data requested" or "data
received" as "ready to analyze." Each cohort must pass a staged operational
state machine before any frozen harness runs.

Machine-readable board:

`analysis/v45_received_data_triage/received_data_triage_status.tsv`

Updater from first-24h operator gate statuses:

`docs/validation/RECEIVED_STATUS_UPDATER_V45.md`

## Status Definitions

| Stage | Meaning |
|---|---|
| `request_packet_ready` | exact request text exists, but may not be sent |
| `request_sent` | human sent the request and logged the sent copy |
| `data_received` | files were received or downloaded |
| `terms_captured` | data-use summary is approved for preflight |
| `quarantined` | files are placed in the agreed raw/quarantine path |
| `checksum_verified` | manifest verification passed |
| `metadata_preflight_passed` | V45 intake preflight passed |
| `subject_map_passed` | subject-map sanity passed when paired deltas are required |
| `outcome_dictionary_frozen` | labels are defined/oriented before scoring |
| `addendum_committed` | cohort-specific preregistration/addendum is committed where needed |
| `harness_ready` | all prior gates pass and only the matching frozen harness remains |

## Current Board

| Cohort | Request packet | Sent | Received | Harness ready | Current blocker |
|---|---|---:|---:|---:|---|
| Gafson DMF PBMC | ready | no | no | no | data not local; request must be sent and package must pass V42/V45 gates |
| Karolinska DMF ROS | ready | no | public partial / labels absent | no | beneficial-response labels and GSM-to-patient/timepoint map absent |
| GSE228330 ocrelizumab | optional ready | no | public partial | no | processed expression, verified subject map, and response labels absent; context-only path also blocked on processing/map |

## Gate Rule

A cohort is `harness_ready=yes` only if:

```text
terms_captured=yes
checksum_verified=yes
metadata_preflight_passed=yes
subject_map_passed=yes when paired deltas are required
outcome_dictionary_frozen=yes when outcomes are scored
addendum_committed=yes when not exact V42 primary Gafson
```

Any `no` or `blocked` before that point means the correct action is acquisition
or metadata repair, not analysis.

## Update Procedure

When a request is sent:

1. save exact sent text under `docs/validation/outbound_requests/`;
2. update `analysis/v45_outbound_data_requests/request_tracker.tsv`;
3. update `analysis/v45_received_data_triage/received_data_triage_status.tsv`.

When data are received:

1. capture data-use terms;
2. place files in raw/quarantine path;
3. verify checksums;
4. run response-column audit where applicable;
5. run intake preflight;
6. run subject-map sanity where paired deltas are required;
7. freeze the outcome-label dictionary and any addendum before scoring.
8. run `scripts/v45_received_status_updater.py` to produce a proposed board
   update from the filled first-24h gate-status TSV.

## Guardrail

This board is operational only. It does not make any cohort validation-ready by
itself and does not change any frozen rule or threshold.
