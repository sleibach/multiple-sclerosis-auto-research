# V48 AI Core Tooling Health

Status: tooling-health handoff only. This card records which SAP AI Core
client paths are currently reachable from the repository scripts. It is not
biological evidence, not model output, and not a project finding.

- checked UTC: `2026-06-14T17:12:41Z`
- client: `scripts/sap_ai_core_client.py`
- credentials: read from `.env`; no key or bearer token stored here
- spend: not exposed by the client for these smoke checks

## Smoke Results

| route | command | status | observed result | interpretation |
|---|---|---|---|---|
| Claude via SAP AI Core Orchestration | `python3 scripts/sap_ai_core_client.py smoke --model claude --timeout 45` | `PASS` | `anthropic--claude-4.7-opus 1 def854013c7ac379`; response `OK` | Usable for proposal-generation or critique only; model output is never evidence. |
| Gemini via SAP AI Core | `python3 scripts/sap_ai_core_client.py smoke --model gemini --timeout 45` | `PASS` | `gemini-3.1-flash-lite 001 dcb4db8a86040bf7`; response `OK.` | Usable for proposal-generation or critique only; model output is never evidence. |
| SAP RPT tabular route | `python3 scripts/sap_ai_core_client.py smoke --model rpt --timeout 45` | `UNAVAILABLE` | `ERROR: No implemented request schema for model: sap-rpt-1-large` | Do not claim RPT works until the Python client implements and smoke-passes this path. |

## Boundary

- A PASS means the client can send a trivial smoke prompt and receive a response.
- A PASS does not validate any model analysis.
- Model and RPT outputs remain proposal-only unless a later committed project
  run grounds a concrete proposal on real data.
- The current Python client must not advertise RPT as available until
  `sap-rpt-1-large` has an implemented request schema and a passing smoke test.

## Next Actions

1. Keep Claude and Gemini in the optional-lens category only.
2. Implement or document the SAP RPT `/predict` route before using RPT in any
   future structured-data task.
3. Add a freshness linter for this card so queue/status text cannot drift back
   to claiming RPT works while the client returns the unimplemented-schema error.

