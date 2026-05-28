# Decision 0001 - Freeze V1-V3 By Pointer

Date: 2026-05-28

## Decision

V4 will archive V1-V3 by index and pointer rather than moving or duplicating
historical files.

## Rationale

- V3 scripts and notebooks reference existing paths.
- `results_v3/`, `scripts/v3_*.py`, and `subagents_v3/` are large enough that
  duplication would worsen hygiene.
- The V4 knowledge base should be canonical going forward, but historical
  reproducibility should remain intact.

## Consequence

`archive/ARCHIVE_INDEX.md` maps prior artifacts to their original paths.
V4 writes new canonical state under `knowledge/`, `meta/`, `analysis/`,
`results/`, and unsuffixed future scripts.
