# Package Route Output Schema No-Output Fixture V52

Date: 2026-07-10

Status: synthetic expected-fail fixture. This document adds no biological
evidence, does not inspect raw package data, and does not alter any validation
rule or therapeutic verdict.

## Purpose

The route-output schema audit should not silently pass if the scan finds no
route-classifier outputs. This fixture provides a manifest-like TSV without the
`assigned_route` output marker. When scanned as a synthetic directory, the audit
should discover zero route outputs and fail under `--fail-on-error`.

Default production scans exclude the named synthetic negative fixture
directories; this fixture is included only when explicitly passed with
`--scan-root` and `--all-files`.

## Fixture

- Fixture root:
  `analysis/v52_route_output_schema_no_output_fixture/`
- Fixture file:
  `analysis/v52_route_output_schema_no_output_fixture/manifest_only.tsv`

## Verification Command

```bash
python3 scripts/v52_route_output_schema_audit.py \
  --scan-root analysis/v52_route_output_schema_no_output_fixture \
  --out analysis/v52_route_output_schema_no_output_fixture_audit/no_output_schema_audit.tsv \
  --all-files \
  --fail-on-error
```

Expected result: nonzero exit, because the synthetic scan should find zero
route-classifier outputs. The committed audit output is:

`analysis/v52_route_output_schema_no_output_fixture_audit/no_output_schema_audit.tsv`

## Boundary

This is a method-behavior test only. It proves the route-output schema audit
cannot pass vacuously when no route output is discovered. It is not evidence
about MS, any cohort, or any real received package.
