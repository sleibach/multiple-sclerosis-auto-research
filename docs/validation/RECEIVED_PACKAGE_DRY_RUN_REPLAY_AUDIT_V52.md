# Received Package Dry-Run Replay Audit V52

Date: 2026-07-10

Status: synthetic-only replay audit. This document adds no biological evidence
and does not inspect real package data.

## Purpose

This audit reruns the current route classifier on the committed synthetic
received-package manifest and compares the regenerated output to the committed
dry-run route output.

## Command

```bash
python3 scripts/v52_received_package_dry_run_replay_audit.py --fail-on-error
```

## Recorded Outputs

- Replay summary:
  `analysis/v52_received_package_dry_run_replay/dry_run_replay_summary.tsv`
- Replayed route output:
  `analysis/v52_received_package_dry_run_replay/replayed_route_classification.tsv`

## Current Result

Current result: exact row match is `True`.

The replayed classifier output matches
`analysis/received_package_intake/20260710_synthetic_monitoring_manifest/route_classification.tsv`
for the synthetic dry-run package.

## Boundary

This replay checks deterministic behavior of the synthetic received-package dry
run only. It does not validate or classify any real package.
