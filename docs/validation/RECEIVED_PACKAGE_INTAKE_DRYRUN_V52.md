# Received Package Intake Dry Run V52

Date: 2026-07-10

Status: synthetic metadata-only dry run. This document adds no evidence, reads no
real package, and does not run validation. It verifies that the V52 received
package file-naming policy and route-classifier command work together.

## Synthetic Package ID

`20260710_synthetic_monitoring_manifest`

## Input

`analysis/received_package_intake/20260710_synthetic_monitoring_manifest/manifest.tsv`

This is synthetic metadata only. It contains no raw expression, clinical,
genotype, or restricted package data.

## Command

```bash
python3 scripts/v52_package_route_classifier.py \
  --manifests analysis/received_package_intake/20260710_synthetic_monitoring_manifest/manifest.tsv \
  --out analysis/received_package_intake/20260710_synthetic_monitoring_manifest/route_classification.tsv
```

## Output

`analysis/received_package_intake/20260710_synthetic_monitoring_manifest/route_classification.tsv`

Observed result:

- `assigned_route`: `monitoring_validation`
- `status`: `matched`
- `matched_required_count`: `7`
- `required_count`: `7`

## Interpretation

The prescribed received-package path and route-classifier command work for a
safe synthetic metadata manifest. This does not imply any real package is
scoreable. Real packages still require terms review, quarantine/checksum,
preflight, and route-specific operator cards before analysis.
