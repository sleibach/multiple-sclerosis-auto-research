# Request-Sent Log Template V45

Status: acquisition operations template. No request is marked sent by this
template alone.

Purpose: record exactly when a validation data/label request was sent, which
packet was used, who owns follow-up, and when the next action is due.

Machine-readable template:

`docs/validation/input_schemas/V45_request_sent_log_template.tsv`

Dry-run/proposed-update helper:

`docs/validation/REQUEST_SENT_UPDATER_V45.md`

## Required Fields

Every sent request should record:

- cohort;
- request packet path;
- exact sent-copy path;
- sent timestamp UTC;
- sender/owner;
- recipient role, not private address if committing would expose private data;
- next follow-up due date;
- escalation path;
- linked evidence gates.

Private email addresses and private reply text should not be committed unless
terms and correspondence permissions allow it. Prefer role-level recipient
labels in committed logs.

## Update Targets

After a request is sent, update:

1. `analysis/v45_outbound_data_requests/request_tracker.tsv`;
2. `analysis/v45_received_data_triage/received_data_triage_status.tsv`;
3. a copied live request-sent log derived from the TSV template;
4. follow-up calendar rows for the cohort.

## Guardrail

Sending a request does not make the cohort received, preflighted, scoreable, or
validated. It only changes acquisition status.
