# Status Board Markdown Round-Trip Renderer V46

Status: operator-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_status_board_markdown_roundtrip_renderer.py` regenerates the
first-30 returned-package status-board Markdown from the canonical TSV and fails
if the live Markdown drifts. This prevents manual team-update edits from
changing route status, blocker, next-action, or repair-template wording outside
the generated TSV.

The renderer reads only the first-30 status-board TSV, its generated Markdown,
and its summary. It does not read returned score values, expression data,
response labels, or quarantined cohorts.

## Command

```bash
.venv/bin/python scripts/v46_status_board_markdown_roundtrip_renderer.py \
  --outdir analysis/v46_status_board_markdown_roundtrip_renderer \
  --fail-on-error
```

## Current Result

- board rows: `6`
- lint checks: `12`
- lint failures: `0`
- synthetic manual-drift fixture detected: yes
- all `score_values_read`: `false`
- overall status: `PASS`

Machine-readable outputs:

- `analysis/v46_status_board_markdown_roundtrip_renderer/status_board_markdown_roundtrip_summary.json`
- `analysis/v46_status_board_markdown_roundtrip_renderer/status_board_markdown_roundtrip_lint.tsv`
- `analysis/v46_status_board_markdown_roundtrip_renderer/FIRST30_STATUS_BOARD_DRYRUN.roundtrip.md`
- `analysis/v46_status_board_markdown_roundtrip_renderer/synthetic_manual_drift.md`
- `analysis/v46_status_board_markdown_roundtrip_renderer/first30_status_board_roundtrip.diff`

## Boundary

A `PASS` means the team-facing Markdown status board is mechanically
regenerable from the TSV and a synthetic manual drift is caught. It does not
authorize any validation interpretation.
