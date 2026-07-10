# Package Route Output Schema Negative Fixture V52

Date: 2026-07-10

Status: synthetic expected-fail fixture. This document adds no biological
evidence, does not inspect raw package data, and does not alter any validation
rule or therapeutic verdict.

## Purpose

The route-output schema audit must reject route-classifier outputs with extra or
missing columns. The production audit scans committed `analysis/` TSVs by
default. For regression testing, `scripts/v52_route_output_schema_audit.py`
supports `--scan-root` and `--all-files`, which lets a synthetic malformed
fixture be scanned without treating it as a production route output. Default
production scans exclude the named synthetic negative fixture directories.

## Fixture

- Fixture root:
  `analysis/v52_route_output_schema_negative_fixture/`
- Fixture file:
  `analysis/v52_route_output_schema_negative_fixture/malformed_route_output.tsv`

The fixture contains the normal route-output columns plus one synthetic
`unexpected_extra_column`; it must fail the exact-schema audit.

## Verification Command

```bash
python3 scripts/v52_route_output_schema_audit.py \
  --scan-root analysis/v52_route_output_schema_negative_fixture \
  --out analysis/v52_route_output_schema_negative_fixture_audit/malformed_schema_audit.tsv \
  --all-files \
  --fail-on-error
```

Expected result: nonzero exit, because the synthetic route output contains an
extra column. The committed audit output is:

`analysis/v52_route_output_schema_negative_fixture_audit/malformed_schema_audit.tsv`

## Boundary

This is a method-behavior test only. It proves the route-output schema audit
detects schema drift in a synthetic output fixture. It is not evidence about MS,
any cohort, or any real received package.
