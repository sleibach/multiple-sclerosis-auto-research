# Follow-Up Message Templates V45

Status: unsent acquisition-operation drafts. No request is marked sent by these
templates.

Script:

`scripts/v45_followup_message_template_generator.py`

Purpose: generate unsent draft messages from `followup_due_board.tsv` status
classes. The drafts help operators prepare initial requests or follow-ups while
keeping sent-state changes controlled by the request-sent log.

## Commands

Live current board:

```bash
.venv/bin/python scripts/v45_followup_message_template_generator.py \
  --board analysis/v45_followup_due_board/live_template/followup_due_board.tsv \
  --outdir analysis/v45_followup_message_templates/live_template
```

Synthetic overdue board:

```bash
.venv/bin/python scripts/v45_followup_message_template_generator.py \
  --board analysis/v45_followup_due_board/synthetic_overdue/followup_due_board.tsv \
  --outdir analysis/v45_followup_message_templates/synthetic_overdue
```

Current outputs:

- live board: `4` unsent drafts, all `not_sent_ready`;
- synthetic overdue board: `4` drafts, including `1` overdue follow-up.

## Guardrail

Creating a draft does not:

- send a request;
- update the request tracker;
- mark data received;
- start any validation gate.

After a real send, use the request-sent log and updater.
