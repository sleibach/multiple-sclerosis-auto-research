# Gate Output Bundle Manifest V45

Status: handoff infrastructure. No validation is run by this manifest.

Purpose: create a cohort-specific manifest of required gate outputs and final
validation-report artifacts so operators can hand off a complete evidence bundle
without opening raw data.

## Command

Primary Gafson-style package:

```bash
.venv/bin/python scripts/v45_gate_output_bundle_manifest.py \
  --cohort-id gafson_dmf_2018 \
  --mode primary \
  --outdir analysis/v45_gate_output_bundle_manifest/gafson_primary
```

Pharmacodynamic/context-only package:

```bash
.venv/bin/python scripts/v45_gate_output_bundle_manifest.py \
  --cohort-id gse228330_ocrelizumab \
  --mode pharmacodynamic \
  --outdir analysis/v45_gate_output_bundle_manifest/gse228330_pharmacodynamic
```

Supported modes:

- `primary`
- `pharmacodynamic`
- `postpartum`
- `tb`

## Outputs

Each run writes:

- `gate_output_bundle_manifest.tsv`
- `gate_output_bundle_manifest_summary.json`

## Current Example Results

| Example | Rows | Present now | Missing now | Interpretation |
|---|---:|---:|---:|---|
| Gafson primary | `10` | `2` | `8` | expected before data receipt |
| GSE228330 pharmacodynamic | `11` | `2` | `9` | expected before processed expression/map are available |

The two currently present rows are shared project-level integrity outputs, not
cohort validation outputs. Missing cohort-specific rows are expected until a
package is received and gates are run.

## Guardrail

This manifest does not:

- run checksum, preflight, module coverage, subject-map sanity, or a harness;
- certify that a cohort is harness-ready;
- create biological evidence;
- permit a response claim for context-only cohorts.

It only enumerates what must be present before a validation-result report can be
considered complete.
