# V44 Infrastructure And Tooling Status

Date: 2026-06-12

Status: maintenance / reproducibility artifact. No research claim is made here.

## SAP AI Core Health Check

Client:

- `scripts/sap_ai_core_client.py`

Credentials:

- read from `.env` / `SAP_AI_CORE_API_KEY`;
- no service key, client secret, or bearer token is written to committed files.

Smoke checks run during V44:

| Tool / model | Command | Result |
|---|---|---|
| Claude 4.7 Opus via Orchestration | `.venv/bin/python scripts/sap_ai_core_client.py smoke --model anthropic--claude-4.7-opus --timeout 60 --max-output-tokens 64` | PASS; response `OK`; deployment `def854013c7ac379` |
| Gemini 2.5 Pro | `.venv/bin/python scripts/sap_ai_core_client.py smoke --model gemini-2.5-pro --timeout 60 --max-output-tokens 256` | PASS; response `OK`; deployment `d6dc532885507ac7` |
| SAP RPT | `.venv/bin/python scripts/sap_ai_core_client.py rpt-smoke --timeout 120` | PASS; toy row predicted `high`, confidence `0.96`; deployment `d61aae51af327bbc` |

Operational caveat:

- Gemini correctly fails with `MAX_TOKENS` if the smoke test is run with `--max-output-tokens 64`; this is expected after the V34 fix. Use a realistic output-token cap for non-trivial Gemini generations and treat `MAX_TOKENS` as a failed/incomplete response, not usable output.

## SAP RPT True Status

SAP RPT is genuinely implemented in the Python client.

Working functions:

- `rpt_predict(...)`
- CLI smoke command: `rpt-smoke`
- CLI payload command: `rpt-predict --payload-file PAYLOAD.json --output OUT.json`

Working REST shape:

- endpoint: `$DEPLOYMENT_URL/predict`
- method: `POST`
- headers: bearer token, `AI-Resource-Group`, JSON content type
- body: tabular `prediction_config`, `index_column`, `data_schema`, and `rows`

RPT output remains a proposal/ranking lens only. It is not biological evidence and does not override grounded tests.

## Reusable Validation And Simulation Components

| Component | Purpose | Status |
|---|---|---|
| `scripts/v42_gafson_validation_harness.py` | Frozen V22/V42 validation harness with V44 additive batch diagnostics | Active |
| `scripts/v44_batch_guard_simulation.py` | Synthetic robustness evaluation for the V44 batch guard | Active |
| `scripts/v43_method_validation_simulations.py` | Power, robustness, and pipeline self-audit simulation library | Active |
| `scripts/v44_secondary_lead_harnesses.py` | Synthetic mechanics checks for postpartum APC-arm and T/B compartment preregistrations | Active |
| `scripts/v44_alt_cohort_scout.py` | Alternative/replication cohort scout and inventory generator | Active |
| `scripts/v44_self_audit_weak_leg.py` | Joint-vs-recurrence weak-leg analysis | Active |
| `scripts/v44_internal_convergence_validation.py` | Stricter recurrence/convergence null and jackknife checks | Active |
| `scripts/sap_ai_core_client.py` | SAP AI Core Claude/Gemini/RPT access | Active |

## Reproducibility Notes

- Synthetic data outputs are stored under `analysis/v43_*` or `analysis/v44_*` and are explicitly synthetic/method-characterization artifacts.
- The locked V22 rule is not modified by any V44 infrastructure.
- The V42 preregistration was tightened only by an additive blind batch-diagnostic guard.
- No real or quarantined Gafson data was read during V44.
- OpenGWAS access is not required for V44 infrastructure, but the JWT expiry on 2026-06-19 12:28 UTC remains operationally important for any future OpenGWAS-dependent run.

