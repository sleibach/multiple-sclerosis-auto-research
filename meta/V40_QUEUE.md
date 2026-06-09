# V40 Queue: Dimension-Scouting

Block start UTC: 2026-06-09T19:21:12Z
Target UTC (+240 min): 2026-06-09T23:21:12Z

## Iterations

| Iteration | Start UTC | End UTC | Status | Notes |
|---|---:|---:|---|---|
| 1 | 2026-06-09T19:21:12Z | 2026-06-09T19:24:23Z | done | Initialized V40; OpenGWAS HTTP 200, JWT valid until 2026-06-19 12:28 UTC and flagged near-expiry. Claude and Gemini smoke-passed; RPT schema unavailable. Phase 1 dimension map written. |

## Backlog

| Priority | Item | Status | Notes |
|---:|---|---|---|
| 1 | Phase 1: tooling health check | done | Claude and Gemini work; RPT is not implemented in Python client. |
| 2 | Phase 1: map unexplored computational dimensions | done | `meta/DIMENSION_SCOUT_V40.md`; model proposal files under `analysis/v40_dimension_scout_*`. |
| 3 | Phase 2: probe top feasible dimension 1 | in-progress | Protective/resilience-direction genetics. |
| 4 | Phase 2: probe top feasible dimension 2 | todo | Perturbation causal-discovery / module network, unless dimension 1 is blocked. |
| 5 | Phase 2: write `docs/history/DIMENSION_PROBES_V40.md` | todo | Value-complete after at least one grounded probe. |
| 6 | Phase 3: deepen best dimension if time remains | todo | Optional, after probes. |
