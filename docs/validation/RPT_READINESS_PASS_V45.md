# V45 RPT Structured Readiness Pass

## Status

SAP RPT was used only as a structured proposal lens. Its predictions are not
evidence and do not change any result, rule, or pre-registration.

## Question

Can the tabular RPT lens surface a different prioritization from the structured
V44/V45 readiness tables?

## Method

Script:

- `scripts/v45_rpt_readiness_pass.py`

Outputs:

- `analysis/v45_rpt_readiness/rpt_readiness_payload.json`
- `analysis/v45_rpt_readiness/rpt_readiness_predictions.json`
- `analysis/v45_rpt_readiness/rpt_readiness_grounded_predictions.tsv`
- `analysis/v45_rpt_readiness/summary.json`

The payload encoded known readiness decisions as training rows and asked RPT to
classify four proposal rows. Each prediction was then checked against the
artifact-derived expected action.

## Result

| Proposal row | RPT prediction | Confidence | Artifact-grounded expected action | Match |
|---|---|---:|---|---|
| Batch diagnostic over-flag calibration | `HARDEN_METHOD` | `1.00` | `HARDEN_METHOD` | yes |
| Secondary lead real-ingest scripts | `IMPLEMENT_INFRA` | `0.64` | `IMPLEMENT_INFRA` | yes |
| `GSE85034` MTX arm | `CONTEXT_ONLY` | `0.94` | `CONTEXT_ONLY` | yes |
| Karolinska label request | `REQUEST_LABELS` | `1.00` | `REQUEST_LABELS` | yes |

## Interpretation

RPT did not surface a new grounded finding or change a priority. It reproduced
the current artifact-derived action classes:

- harden methods where synthetic diagnostics exposed sensitivity costs;
- implement missing infrastructure for secondary leads;
- keep `GSE85034` MTX as context/stress-test only;
- pursue Karolinska labels as a low-barrier acquisition path.

This is useful as a tooling check, but it adds no biological or validation
evidence.

