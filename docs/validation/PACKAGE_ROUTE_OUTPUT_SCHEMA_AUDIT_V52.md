# Package Route Output Schema Audit V52

Date: 2026-07-10

Status: operational schema audit. This document adds no biological evidence,
does not inspect raw package data, and does not alter any validation rule or
therapeutic verdict.

## Purpose

The V52 package route classifier emits route-output TSVs that downstream intake
steps read mechanically. This audit checks every committed route-classifier
output discovered by the `assigned_route` column marker and requires the exact
9-column output schema.

Default production scans exclude the named synthetic expected-fail fixture
directories:

- `analysis/v52_route_output_schema_negative_fixture/`
- `analysis/v52_route_output_schema_no_output_fixture/`

Those fixtures are included only when explicitly passed with `--scan-root` and
`--all-files`.

## Expected Output Schema

```text
package_id
expected_route
assigned_route
status
matched_required_count
required_count
missing_required_fields
candidate_full_routes
expected_matches_assigned
```

## Verification Command

```bash
python3 scripts/v52_route_output_schema_audit.py --fail-on-error
```

Committed output:

`analysis/v52_route_output_schema_audit/route_output_schema_audit.tsv`

## Result

The audit found seven committed route-classifier outputs and zero schema
failures. Every output has the exact 9-column schema and no extra columns.

## Boundary

This is a route-output shape check only. It does not decide whether a package is
usable, does not inspect raw data, and does not run any monitoring or genetics
analysis.
