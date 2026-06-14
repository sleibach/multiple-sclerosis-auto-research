# V48 Active-Time Accounting Audit

Status: governance/navigation only. This card documents the V48 timing rule so
future summaries report cumulative active work separately from wall-clock span.
It does not validate external claims, change findings, or alter any evidence
grade.

- timing rules: `5`
- audit checks: `6`
- required linked controls: `4`

## Required Controls

- `meta/V48_QUEUE.md`
- `knowledge_external/catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md`
- `knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md`
- `scripts/v47_provenance_gate.py`

## Timing Rules

| rule | requirement |
|---|---|
| `session_interval_sum` | Active time is the sum of recorded session intervals. |
| `exclude_resume_gaps` | Idle gaps between sessions are excluded from active time. |
| `open_session_current_time` | For an open session, current active time is current UTC minus session start. |
| `separate_wall_clock` | Wall-clock span must be reported separately from active time. |
| `target_metric` | The V48 stop target is 21600 active seconds, not calendar elapsed time. |

## Audit Checks

| check | current V48 status |
|---|---|
| Block start recorded. | `2026-06-14T13:22:03Z` in `meta/V48_QUEUE.md`. |
| Active target recorded. | `21600` seconds in `meta/V48_QUEUE.md`. |
| Session intervals table present. | One open session is recorded. |
| Resume-gap exclusion rule recorded. | Present in queue timing section. |
| Latest active checkpoint before this card. | `20723` seconds at `2026-06-14T19:07:26Z`. |
| Required provenance gate still separate. | V47 gate remains the enforcement control. |

## Reporting Template

```text
active_runtime_seconds:
active_runtime_hours:
wall_clock_span:
block_start_utc:
block_end_utc:
session_intervals_count:
target_met:
stop_condition:
```

## Boundary

This audit card is operational timing metadata only. It prevents active-time
misreporting and does not affect external knowledge provenance, project
findings, locked rules, validation plans, or evidence grades.
