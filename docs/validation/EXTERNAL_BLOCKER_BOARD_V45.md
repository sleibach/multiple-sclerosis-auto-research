# External Blocker Board V45

Status: acquisition operations dashboard. No biological claim.

Script:

`scripts/v45_external_blocker_board.py`

Escalation matrix:

`docs/validation/EXTERNAL_BLOCKER_ESCALATION_MATRIX_V45.md`

Purpose: merge the live cohort acquisition index, outbound request tracker,
received-data triage board, and follow-up due board into one table that
separates external blockers from internal readiness work.

## Command

```bash
.venv/bin/python scripts/v45_external_blocker_board.py \
  --outdir analysis/v45_external_blocker_board
```

## Current Result

Generated outputs:

- `analysis/v45_external_blocker_board/external_blocker_board.tsv`
- `analysis/v45_external_blocker_board/external_blocker_board_summary.json`

Current state:

- `4` live routes are listed;
- `4/4` are blocked at `external_send_or_author_approval`;
- `0` cohorts are harness-ready.

The four routes are Gafson DMF, Karolinska DMF ROS labels/map, GSE228330
optional outcome labels/context processing, and the author-run fallback route.

## Interpretation Boundary

The board supports operational planning only. It does not mean data have been
received, quarantined, preflighted, scored, or validated.
