# Follow-Up Due Board V45

Status: acquisition operations artifact. No data receipt, scoring, or
validation claim.

Script:

`scripts/v45_followup_due_board.py`

Purpose: merge the outbound request tracker with an explicit request-sent log
and produce a due board for request sending and follow-up actions.

## Commands

Live draft-template board:

```bash
.venv/bin/python scripts/v45_followup_due_board.py \
  --outdir analysis/v45_followup_due_board/live_template
```

Synthetic overdue-path check:

```bash
.venv/bin/python scripts/v45_followup_due_board.py \
  --sent-log analysis/v45_request_sent_updater/synthetic_sent_log.tsv \
  --outdir analysis/v45_followup_due_board/synthetic_overdue \
  --as-of-utc 2026-06-27T18:00:00Z
```

Current verification:

- live draft request-sent template: `4` tracker rows, `0` sent events,
  all `4` rows `not_sent_ready`;
- synthetic sent log as of `2026-06-27T18:00:00Z`: `1` overdue follow-up
  and `3` ready-unsent rows.

## Output

`followup_due_board.tsv` includes:

- cohort and priority;
- tracker status;
- explicit request-sent state;
- follow-up due timestamp and due status;
- recommended acquisition action;
- recipient/path, prepared request, external blocker, and target raw path.

## Interpretation

The board is operational only. It can recommend:

- send request after human contact approval;
- prepare follow-up;
- wait until due date;
- send follow-up or escalate if terms allow;
- repair a malformed sent log.

It does not mark data received, terms captured, files quarantined, or harness
readiness.
