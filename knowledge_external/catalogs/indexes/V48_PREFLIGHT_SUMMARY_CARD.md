# V48 Preflight Summary Card

Status: handoff/navigation only. This card summarizes governance controls; it does not validate external claims or provide biological evidence.

- overall status: `PASS`
- components summarized: `5`
- missing summaries: `0`
- components with failure status: `0`

## Current Status

| component | status | checks/artifacts | failures/missing | summary |
|---|---|---:|---:|---|
| `governance_preflight` | `PASS` | 45 | 0 | `analysis/v48_governance_preflight/v48_governance_preflight_summary.json` |
| `provenance_gate` | `PASS` | 358 | 0 | `analysis/v47_provenance_gate/provenance_gate_summary.json` |
| `governance_navigation` | `PASS` | 57 | 0 | `knowledge_external/catalogs/indexes/v48_governance_navigation_summary.json` |
| `convergence_matrix` | `PASS` |  |  | `knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json` |
| `source_terms_packet` | `PASS` | 9 |  | `knowledge_external/catalogs/indexes/high_priority_source_terms_packet_v48_summary.json` |

## Commands

| check | command |
|---|---|
| `full_preflight` | `python3 scripts/v48_governance_preflight.py` |
| `provenance_gate` | `python3 scripts/v47_provenance_gate.py audit` |
| `governance_navigation` | `python3 scripts/v48_governance_navigation.py` |
| `external_markdown_lint` | `python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error` |
| `public_index_freshness` | `python3 scripts/v48_public_index_freshness_linter.py lint --fail-on-error` |

## Boundary

- Passing checks mean segregation/provenance/navigation controls passed.
- External knowledge remains external-classed and is not project-grounded evidence.
- Grounded findings, locked rules, and validation pre-registrations remain outside this external layer.
