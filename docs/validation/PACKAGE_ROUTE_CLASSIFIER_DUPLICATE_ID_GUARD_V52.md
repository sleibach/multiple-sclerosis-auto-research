# Package Route Classifier Duplicate ID Guard V52

Date: 2026-07-10

Status: operational guard. This document adds no biological evidence and does
not inspect real package data.

## Purpose

`scripts/v52_package_route_classifier.py` now rejects incoming manifests with
duplicate `package_id` values. Duplicate package IDs make route outputs
ambiguous and could cause one package's route decision to be confused with
another.

## Synthetic Fixture

Fixture:

`analysis/v52_package_route_classifier/duplicate_package_id_manifest.tsv`

Recorded expected-fail result:

`analysis/v52_package_route_classifier/duplicate_package_id_negative_check.tsv`

Current result: duplicate `package_id` manifests exit nonzero and report
`manifest_duplicate_package_id`.

## Boundary

This is an intake-manifest integrity guard only. It does not change any
route-specific validation rule or therapeutic verdict.
