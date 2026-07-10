# Package Route Classifier Intake Fixture V52

Date: 2026-07-10

Status: synthetic intake smoke test. This document and its associated TSVs use
synthetic package metadata only. They add no biological evidence, read no real
package, and do not run validation.

## Purpose

The V52 route classifier is a pre-analysis guard. This fixture proves that its
minimum-field logic can be exercised mechanically before any real data package
arrives.

## Command

```bash
python3 scripts/v52_package_route_classifier.py \
  --manifests analysis/v52_package_route_classifier/synthetic_package_manifests.tsv \
  --out analysis/v52_package_route_classifier/synthetic_route_classification.tsv
```

## Current Fixture Result

The synthetic manifest set contains six package shapes:

- full monitoring package;
- chr1 target-resolution package;
- structure-context package;
- metadata/aggregate-only context package;
- access/terms-blocked package;
- deliberately incomplete monitoring package.

The current result is five full matches and one intentional
`partial_or_unscoreable` case. The incomplete monitoring fixture is assigned to
the monitoring route as the closest route but is not marked `matched`; its
missing fields are:

`early_treatment_expression;response_label;module_gene_coverage;batch_QC_metadata`

## Boundary

This script only checks presence of the classifier's `minimum_fields`. It does
not inspect raw data, does not score V22, does not judge package quality, and
does not replace the preflight checklist, field dictionary, acceptance criteria,
or route-specific operator cards.

## Artifacts

- `scripts/v52_package_route_classifier.py`
- `analysis/v52_package_route_classifier/synthetic_package_manifests.tsv`
- `analysis/v52_package_route_classifier/synthetic_route_classification.tsv`
