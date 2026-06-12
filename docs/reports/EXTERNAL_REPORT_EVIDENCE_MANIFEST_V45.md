# External Report Evidence Manifest V45

Status: external-report citation governance. No new analysis or validation
claim.

## Purpose

`scripts/v45_external_report_evidence_manifest.py` scans the external-facing
report docs and maps every cited `docs/`, `analysis/`, `scripts/`, or `meta/`
artifact to its V45 evidence class when available.

The goal is to keep report citations inside their allowed interpretation
boundary. Synthetic/readiness artifacts stay method/readiness evidence; they do
not become biological validation evidence by being cited in a report.

## Command

```bash
.venv/bin/python scripts/v45_external_report_evidence_manifest.py \
  --outdir analysis/v45_external_report_evidence_manifest
```

## Current Result

Current status: `PASS`.

| Metric | Value |
|---|---:|
| source reports scanned | `3` |
| artifact references | `80` |
| V45-indexed references | `57` |
| existing non-V45/historical references | `23` |
| missing references | `0` |

Machine-readable outputs:

- `analysis/v45_external_report_evidence_manifest/external_report_evidence_manifest.tsv`
- `analysis/v45_external_report_evidence_manifest/external_report_evidence_manifest_summary.json`

## Interpretation

A pass means the external-facing report citations resolve and are classified
where the V45 artifact index covers them. It does not validate any cited
biological result. Existing non-V45 references must still be interpreted under
their own committed evidence grade.
