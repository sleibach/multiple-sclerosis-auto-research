# Package Route Classifier Empty Fields Regression V52

Date: 2026-07-10

Status: operational regression. This document adds no biological evidence and
does not inspect real package data.

## Purpose

This regression verifies that a manifest row with empty `provided_fields` does
not get routed into a scoreable package path.

## Synthetic Fixture

Fixture:

`analysis/v52_package_route_classifier/empty_fields_manifest.tsv`

Recorded classifier output:

`analysis/v52_package_route_classifier/empty_fields_route_classification.tsv`

Recorded summary:

`analysis/v52_package_route_classifier/empty_fields_regression_summary.tsv`

## Current Result

Current result: the empty-fields package returns `unscoreable_no_route` with no
assigned route.

## Boundary

This is a manifest-integrity regression only. It does not change any
route-specific validation rule.
