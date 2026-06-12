# V45 Governance Refresh

Status: governance infrastructure. No biological claim.

Purpose: rerun the V45 artifact index, synthetic/method artifact index, and
compute/storage summary together so handoff counts do not drift after continued
V45 checkpoints.

## Command

```bash
.venv/bin/python scripts/v45_refresh_governance_summaries.py
```

Outputs:

- `analysis/v45_governance_refresh/governance_refresh_summary.json`
- refreshed `analysis/v45_artifact_index/`
- refreshed `analysis/v45_synthetic_artifact_index/`
- refreshed `analysis/v45_compute_storage_summary/`

## Current Result

Current combined refresh status: `PASS`.

Headline counts from the latest run:

| Summary | Current value |
|---|---:|
| artifact-index paths | `746` |
| artifact-index fronts | `8` |
| artifact-index evidence classes | `9` |
| V43-V45 method/governance directories | `62` |
| V45 analysis directories in storage summary | `56` |
| V45 analysis files in storage summary | `582` |
| V45 analysis footprint | `85.053 MiB` |
| V45 synthetic/method-behavior footprint | `84.335 MiB` |

## Interpretation

This refresh is accounting only. It does not run validation, read quarantined
data, compute biological metrics, or modify locked rules. A `PASS` means the
three governance generators executed and wrote their expected summary files.
