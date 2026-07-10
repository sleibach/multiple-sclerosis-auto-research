# Received Package Intake Safety Audit Regression Fixture V52

Date: 2026-07-10

Status: operational regression note. This document adds no biological evidence
and does not inspect raw received-package data.

## Purpose

This fixture records the expected behavior of
`scripts/v52_received_intake_safety_audit.py` on the current synthetic intake
directory. Rerun it after edits to the intake README, synthetic intake manifest,
route-classifier output, or safety-audit script.

## Command

```bash
python3 scripts/v52_received_intake_safety_audit.py --fail-on-error
```

## Expected Result

The current expected result is:

- tracked intake files: 3
- audit checks: 14
- failures: 0

Recorded TSV:

`analysis/v52_received_intake_safety_audit/intake_safety_audit.tsv`

## Expected File Set

| tracked file | expected role |
|---|---|
| `analysis/received_package_intake/README.md` | local intake boundary note |
| `analysis/received_package_intake/20260710_synthetic_monitoring_manifest/manifest.tsv` | synthetic safe manifest |
| `analysis/received_package_intake/20260710_synthetic_monitoring_manifest/route_classification.tsv` | synthetic route-classifier output |

## Boundary

This regression fixture tests the commit-safety audit only. It does not
authorize analysis of future real packages and does not certify access terms,
labels, pairing, or route-specific harness readiness.
