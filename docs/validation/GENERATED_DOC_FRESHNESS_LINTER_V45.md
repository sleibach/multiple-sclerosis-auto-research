# Generated-Doc Freshness Linter V45

Status: documentation-governance guard. No biological claim.

## Purpose

`scripts/v45_generated_doc_freshness_linter.py` checks selected human-facing V45
governance docs against their machine-readable JSON/TSV summaries. It exists
because V45 has many generated count/timing artifacts, and manual count refreshes
are a drift risk.

The linter compares docs against generated outputs only. It does not inspect
raw data, update governance summaries, or run validation.

Operationally, run it after generated summaries have been refreshed. It is kept
as a post-refresh drift detector rather than embedded inside
`scripts/v45_precommit_readiness_check.py`, because that wrapper writes its own
summary only after all wrapper steps finish.

## Command

```bash
.venv/bin/python scripts/v45_generated_doc_freshness_linter.py \
  --outdir analysis/v45_generated_doc_freshness_linter
```

## Current Result

Current status: `PASS`.

Machine-readable outputs:

- `analysis/v45_generated_doc_freshness_linter/generated_doc_freshness_lint.tsv`
- `analysis/v45_generated_doc_freshness_linter/generated_doc_freshness_summary.json`

## Scope

The current linter covers the main human-facing count/timing docs:

- `V45_GOVERNANCE_REFRESH.md`
- `V45_ARTIFACT_INDEX.md`
- `V45_COMPUTE_STORAGE_SUMMARY.md`
- `PRECOMMIT_READINESS_CHECKLIST_V45.md`
- `V45_READINESS_CHANGELOG.md`
- `SYNTHETIC_ARTIFACT_RETENTION_INDEX_V45.md`
- `SYNTHETIC_OUTPUT_RETENTION_POLICY_V45.md`
- `V45_REGRESSION_AGGREGATOR.md`
- `READINESS_STALE_OUTPUT_DETECTOR_V45.md`

## Interpretation Boundary

A pass means the checked documentation matches the current generated summaries
and configured generated-artifact counts. It does not mean those summaries are
fresh relative to the filesystem; that is the job of
`scripts/v45_refresh_governance_summaries.py` and
`scripts/v45_readiness_stale_output_detector.py`.
