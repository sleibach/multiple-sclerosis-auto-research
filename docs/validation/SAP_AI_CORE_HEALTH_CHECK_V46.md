# V46 SAP AI Core Health Check

Status: **PASS** on 2026-06-13.

This is infrastructure/readiness evidence only. It verifies model access paths;
it does not create biological evidence, does not inspect real cohort data, and
does not change any locked rule or pre-registration.

## Committed Checker

- Script: `scripts/v46_sap_ai_core_health_check.py`
- Output directory: `analysis/v46_sap_ai_core_health_check/`
- Summary: `analysis/v46_sap_ai_core_health_check/sap_ai_core_health_summary.json`
- Detail table: `analysis/v46_sap_ai_core_health_check/sap_ai_core_health_checks.tsv`

Run:

```bash
python3 scripts/v46_sap_ai_core_health_check.py \
  --outdir analysis/v46_sap_ai_core_health_check \
  --fail-on-error
```

## Result

| Family | Model | Required command path | Status |
|---|---|---|---|
| Claude via Orchestration | `anthropic--claude-4.7-opus` | `sap_ai_core_client.py smoke` | PASS |
| Gemini native | `gemini-2.5-pro` | `sap_ai_core_client.py smoke` | PASS |
| SAP RPT `/predict` | `sap-rpt-1-large` | `sap_ai_core_client.py rpt-smoke` | PASS |

## Operational Rule

Use `rpt-smoke` or `rpt-predict` for `sap-rpt-1-large`.

Do **not** use the generic `smoke` command for RPT. The generic command is for
LLM-style text generation and correctly rejects `sap-rpt-1-large` with
`No implemented request schema for model: sap-rpt-1-large`. That rejection is
not evidence that RPT is unavailable; it is evidence that the wrong command path
was used.

RPT output remains a proposal/prioritization lens only. It is never evidence and
does not override grounded checks.
