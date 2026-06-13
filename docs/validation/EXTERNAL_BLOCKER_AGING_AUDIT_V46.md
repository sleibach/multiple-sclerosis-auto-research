# External Blocker Aging Audit V46

Status: operational infrastructure. No validation result and no biological
claim.

## Purpose

`scripts/v46_external_blocker_aging_audit.py` combines the external blocker
board, follow-up due board, escalation matrix, and sent-log entries into a
route-specific aging table. It distinguishes:

- requests not yet sent, where the external response clock has not started;
- sent requests that are waiting;
- follow-ups due soon;
- overdue follow-ups;
- overdue escalation.

It does not read cohort data, private correspondence, or validation outputs.

## Command

Live audit:

```bash
.venv/bin/python scripts/v46_external_blocker_aging_audit.py audit \
  --as-of-utc <YYYY-MM-DDTHH:MM:SSZ> \
  --outdir analysis/v46_external_blocker_aging_audit/live
```

Synthetic regression:

```bash
.venv/bin/python scripts/v46_external_blocker_aging_audit.py synthetic-check \
  --outdir analysis/v46_external_blocker_aging_audit
```

## Current Live Result

As of `2026-06-13T10:06:32Z`, all four tracked routes are
`clock_not_started` because no request is logged as sent:

- Gafson DMF/NEDA-4;
- Karolinska DMF ROS labels/map;
- GSE228330 optional labels/context route;
- author-run fallback.

The immediate next action remains sending or approving the prepared requests,
not follow-up escalation.

Machine-readable outputs:

- `analysis/v46_external_blocker_aging_audit/live/external_blocker_aging_audit_summary.json`
- `analysis/v46_external_blocker_aging_audit/live/external_blocker_aging_audit.tsv`

## Verified Synthetic Result

The synthetic check passed four aging bands:

- `clock_not_started`;
- `followup_due_soon`;
- `followup_overdue`;
- `escalation_overdue`.

Machine-readable outputs:

- `analysis/v46_external_blocker_aging_audit/external_blocker_aging_synthetic_summary.json`
- `analysis/v46_external_blocker_aging_audit/external_blocker_aging_synthetic_expectations.tsv`
- `analysis/v46_external_blocker_aging_audit/synthetic_audit/external_blocker_aging_audit.tsv`

## Boundary

This audit is a routing aid. It does not send messages, mark requests as sent,
or change acquisition state. It only reports the next operational action implied
by committed boards and sent-log entries.

