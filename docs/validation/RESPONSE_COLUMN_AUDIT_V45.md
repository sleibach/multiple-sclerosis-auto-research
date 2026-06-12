# V45 Response-Column Audit Utility

Status: validation-readiness guardrail. No biological claim.

## Purpose

`scripts/v45_response_column_audit.py` is a lightweight metadata-draft scanner
for pharmacodynamic-only cohorts. It catches response/outcome-like columns before
a collaborator draft or public metadata table is routed through a context-only
harness.

This is intentionally narrower than the full intake preflight. Use it when only
a metadata draft is available and the project needs a quick answer to:

> Does this table contain response-like columns that would invalidate
> pharmacodynamic-only handling?

## Command

```bash
.venv/bin/python scripts/v45_response_column_audit.py audit \
  --metadata path/to/sample_metadata.tsv \
  --outdir analysis/response_column_audit/<cohort> \
  --fail-on-response-like
```

Outputs:

- `response_column_audit.tsv`
- `response_column_audit_summary.json`

## Tokens Scanned

The utility flags columns containing response/outcome terms such as:

`response`, `responder`, `nonresponder`, `neda`, `relapse`, `remission`, `edss`,
`disability`, `progression`, `mri_activity`, `disease_activity`, `outcome`,
`event_free`, `pasi`, or `mayo`.

Known context/QC columns such as `clinical_status`, `use_status`, and `qc_status`
are not flagged by name alone.

## Synthetic Verification

Command run:

```bash
.venv/bin/python scripts/v45_response_column_audit.py synthetic-check \
  --outdir analysis/v45_response_column_audit
```

Result: `PASS`

| Fixture | Expected | Observed |
|---|---:|---:|
| safe pharmacodynamic metadata | pass | pass |
| unsafe metadata with `NEDA4_response` and `relapse_12m` | fail | fail |
| current GSE228330 public draft metadata | pass | pass |

GSE228330 public draft status:

- `21` columns scanned;
- `0` response-like columns found;
- overall response-column audit status `PASS`.

This does not make GSE228330 response-validation ready. It only means the current
draft does not contain response-like columns. GSE228330 still fails subject-map
sanity because the sample pairing is inferred/unverified and it still lacks
public response labels.

## Relationship To Full Preflight

This utility is a quick front-door guard. It does not replace
`scripts/v45_validation_intake_preflight.py`, which still must run on any
received package before a harness runs.

Allowed use:

- collaborator sends a metadata draft before files are transferred;
- public pharmacodynamic-only metadata is being triaged;
- reviewer needs to verify that a context-only run is not quietly using outcomes.

Not allowed:

- using a passing response-column audit as evidence that a cohort is valid;
- treating response-like columns as usable without a cohort-specific
  preregistration;
- bypassing the full intake preflight.
