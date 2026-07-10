# Package Route Classifier Operator Note V52

Date: 2026-07-10

Status: operational note. This document adds no evidence, changes no validation
rule, and does not inspect real data. It defines how an operator uses the V52
route-classifier script on a received manifest before any package analysis.

## Inputs

Use a manifest shaped like:

`docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv`

The required script-consumed columns are:

- `package_id`
- `provided_fields`

The optional but useful column is:

- `expected_route`

Additional columns are allowed and ignored by the script, so data-owner metadata
can remain in the manifest.

Duplicate `package_id` values are not allowed. The classifier exits nonzero with
`manifest_duplicate_package_id` if the same package ID appears more than once in
one manifest.

## Command

Run from the repository root:

```bash
python3 scripts/v52_package_route_classifier.py \
  --manifests RECEIVED_OR_SYNTHETIC_MANIFEST.tsv \
  --out analysis/v52_package_route_classifier/RECEIVED_PACKAGE_ROUTE_CLASSIFICATION.tsv
```

For the synthetic filled-template smoke test:

```bash
python3 scripts/v52_package_route_classifier.py \
  --manifests analysis/v52_package_route_classifier/manifest_template_smoke_input.tsv \
  --out analysis/v52_package_route_classifier/manifest_template_smoke_output.tsv
```

Expected synthetic result:

- `assigned_route`: `monitoring_validation`
- `status`: `matched`
- `matched_required_count`: `7`
- `required_count`: `7`

## Status Interpretation

Machine-readable table:

`docs/validation/PACKAGE_ROUTE_CLASSIFIER_STATUS_DECISION_TABLE_V52.tsv`

| status | meaning | action |
|---|---|---|
| `matched` | all `minimum_fields` for the assigned route are present | continue to the preflight checklist and route-specific operator card |
| `partial_or_unscoreable` | the script found a closest route, but at least one required field is missing | do not run validation; request missing fields or classify as partial/context/unscoreable per preflight |
| `unscoreable_no_route` | no route has any required-field overlap | reject or request a new manifest |

## Boundary

The script checks declared field presence only. It does not inspect raw files,
does not verify labels, does not score modules, does not validate Gafson or
Karolinska, and does not change a closed target verdict.

If the classifier output and operator judgment disagree, stop and record the
discrepancy before any analysis. Do not silently override the route table.
