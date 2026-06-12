# Request-Sent Updater V45

Status: acquisition operations helper. No cohort is received, scoreable, or
validated by this script.

Script:

`scripts/v45_request_sent_updater.py`

Purpose: convert an explicitly filled request-sent log into proposed updates for:

- `analysis/v45_outbound_data_requests/request_tracker.tsv`
- `analysis/v45_received_data_triage/received_data_triage_status.tsv`

The updater never infers that a request was sent from a ready-to-send packet. A
row is accepted only when the request-sent log has a sent status, concrete UTC
timestamps, a concrete sent-copy path that exists, and no committed private
recipient details.

## Inputs

Fill a copy of:

`docs/validation/input_schemas/V45_request_sent_log_template.tsv`

The current generated draft template is:

`docs/validation/SEND_LOG_INTAKE_TEMPLATE_V45.md`

Required operational fields include:

- `cohort`
- `request_packet_path`
- `exact_sent_copy_path`
- `sent_timestamp_utc`
- `sender_or_owner`
- `recipient_role`
- `recipient_private_details_committed`
- `next_followup_due_utc`
- `escalation_due_utc`
- `status`

Accepted sent statuses:

- `sent`
- `sent_logged`
- `sent_waiting_response`
- `sent_no_response_yet`
- `sent_followup_pending`

Draft/not-sent rows are ignored, not treated as failures.

## Dry-Run Commands

Live template check, expected to propose zero updates while all rows remain
draft:

```bash
.venv/bin/python scripts/v45_request_sent_updater.py \
  --outdir analysis/v45_request_sent_updater/template_no_sends
```

Synthetic positive-path check:

```bash
.venv/bin/python scripts/v45_request_sent_updater.py \
  --sent-log analysis/v45_request_sent_updater/synthetic_sent_log.tsv \
  --outdir analysis/v45_request_sent_updater/synthetic_sent_fixture
```

Current verification outputs:

- live draft template: `0` accepted sent rows, `0` tracker updates, `0` hard failures;
- generated current-action template: `4` draft rows, `0` accepted sent rows,
  `0` tracker updates, `0` triage-board updates, `0` hard failures;
- synthetic sent fixture: `1` accepted sent row, `1` tracker update, `1` triage-board update, `0` hard failures.

## Write Mode

By default the script writes only proposed outputs under the chosen `--outdir`.
After human review, explicit write flags are available:

```bash
.venv/bin/python scripts/v45_request_sent_updater.py \
  --sent-log <filled_request_sent_log.tsv> \
  --outdir analysis/v45_request_sent_updater/live_<cohort>_<date> \
  --write-tracker \
  --write-triage-board
```

Do not use write mode until the sent-copy path and private-data redaction state
have been reviewed.

## Guardrail

A sent request changes acquisition status only. It does not mean:

- data were received;
- data-use terms are captured;
- files are quarantined or checksummed;
- metadata passed preflight;
- labels are frozen;
- any frozen harness can run.

Those later gates remain controlled by the received-data triage workflow.
