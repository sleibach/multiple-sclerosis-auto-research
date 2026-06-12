# Metadata Contradiction Stress Test V45

Status: synthetic intake-hardening test. No biological claim.

## Purpose

`scripts/v45_metadata_contradiction_stress.py` tests whether validation-intake
metadata contradictions are caught before any scoring. It complements the V45
intake preflight, which checks schemas and response-column guardrails, by
auditing contradictions inside otherwise present metadata fields.

The guard checks:

- within-patient response-label conflicts;
- missing, duplicated, or non-ordered baseline/follow-up timepoints;
- non-numeric or non-zero baseline treatment-day fields;
- response labels perfectly confounded with batch/processing-batch fields.

It does not inspect expression values, compute module scores, or run validation.

## Command

Synthetic stress test:

```bash
.venv/bin/python scripts/v45_metadata_contradiction_stress.py synthetic-check \
  --outdir analysis/v45_metadata_contradiction_stress
```

Future metadata audit:

```bash
.venv/bin/python scripts/v45_metadata_contradiction_stress.py audit \
  --metadata <filled_metadata.tsv> \
  --outdir analysis/metadata_contradiction/<cohort> \
  --expect-status PASS
```

## Current Synthetic Result

Synthetic status: `PASS` for the expected behavior of all cases.

| Case | Expected | Observed | Hard issues |
|---|---|---|---:|
| clean metadata | PASS | PASS | 0 |
| response-label conflict | FAIL | FAIL | >=1 |
| timepoint conflict | FAIL | FAIL | >=1 |
| response-confounded batch | FAIL | FAIL | >=1 |

Machine-readable outputs:

- `analysis/v45_metadata_contradiction_stress/metadata_contradiction_stress_summary.json`
- `analysis/v45_metadata_contradiction_stress/metadata_contradiction_synthetic_cases.tsv`
- per-case metadata and issue tables under `analysis/v45_metadata_contradiction_stress/`

## Interpretation Boundary

This is synthetic method behavior only. A synthetic failure means the guard
catches a designed contradiction. It is not evidence about MS, treatment
response, or any real cohort. For real incoming packages, a failure is an intake
blocker: repair metadata or report the route as not cleanly harness-ready.
