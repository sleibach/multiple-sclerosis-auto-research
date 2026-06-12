# Send-Log Intake Template V45

Status: acquisition operations template. No biological claim.

Purpose: generate a draft request-sent log from the current action card so a
human can record the exact sent copy, timestamp, sender, recipient role, and
follow-up dates after a request is actually sent.

This is read-only by default. It does not mark a request as sent, update the
tracker, update the triage board, mark data received, or make a cohort
harness-ready.

## Command

```bash
.venv/bin/python scripts/v45_send_log_intake_template.py \
  --outdir analysis/v45_send_log_intake_template
```

Dry-run the generated template through the request-sent updater:

```bash
.venv/bin/python scripts/v45_request_sent_updater.py \
  --sent-log analysis/v45_send_log_intake_template/send_log_intake_template.tsv \
  --outdir analysis/v45_send_log_intake_template/request_sent_updater_dryrun
```

## Current Result

Current generated rows: `4`.

All rows are `draft`, so the request-sent updater dry-run should propose:

- `0` accepted sent rows;
- `0` tracker updates;
- `0` triage-board updates;
- `0` hard failures.

Machine-readable outputs:

- `analysis/v45_send_log_intake_template/send_log_intake_template.tsv`
- `analysis/v45_send_log_intake_template/send_log_intake_template_summary.json`
- `analysis/v45_send_log_intake_template/request_sent_updater_dryrun/request_sent_update_summary.json`
- `analysis/v45_send_log_intake_template/request_sent_updater_dryrun/request_sent_log_audit.tsv`
- `analysis/v45_send_log_intake_template/request_sent_updater_dryrun/request_tracker.proposed.tsv`
- `analysis/v45_send_log_intake_template/request_sent_updater_dryrun/received_data_triage_status.proposed.tsv`

## Fill Rules

Only after a request is actually sent:

1. save the exact non-sensitive sent copy under the path recorded in
   `exact_sent_copy_path`;
2. replace placeholder UTC timestamps with concrete ISO UTC timestamps;
3. keep `recipient_private_details_committed=no`;
4. set `status` to an accepted sent status documented in
   `docs/validation/REQUEST_SENT_UPDATER_V45.md`;
5. run the request-sent updater without write flags first;
6. use write flags only after reviewing the proposed tracker and triage changes.

## Interpretation Boundary

A generated send-log template is not evidence that any request was sent. It is
only a structured place to record a send event after it happens.
