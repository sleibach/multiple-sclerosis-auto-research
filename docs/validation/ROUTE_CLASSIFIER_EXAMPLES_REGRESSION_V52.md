# Route Classifier Examples Regression V52

Date: 2026-07-10

Status: synthetic/examples regression. This document adds no biological evidence
and does not inspect real package data.

## Purpose

This regression converts
`docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv` into a
manifest-shaped table and runs `scripts/v52_package_route_classifier.py` against
all examples.

## Initial Finding

The first regression pass found 2 example-table mismatches:

- `example_02_no_response_label` expected `pharmacodynamic_context_only` but did
  not list the generic `expression_or_immune_profile` field required for that
  route.
- `example_03_missing_baseline` expected `metadata_only_or_aggregate_only`, but
  the classifier correctly treated it as a partial `monitoring_validation`
  intake because it overlaps the monitoring route and is blocked specifically by
  the absent baseline sample.

The examples table was corrected; the classifier logic was not changed.

## Recorded Outputs

- Manifest-shaped examples:
  `analysis/v52_route_classifier_examples_regression/examples_as_manifest.tsv`
- Classifier output:
  `analysis/v52_route_classifier_examples_regression/examples_route_classification.tsv`
- Summary:
  `analysis/v52_route_classifier_examples_regression/examples_regression_summary.tsv`

## Current Result

Current result: 10 examples, 0 expected-route failures after the examples-table
fix, 0 unexpected status failures.

## Boundary

This regression checks package-routing examples only. It does not change any
route-specific validation rule, target verdict, or locked monitoring rule.
