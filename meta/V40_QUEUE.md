# V40 Queue: Dimension-Scouting

Block start UTC: 2026-06-09T19:21:12Z
Target UTC (+240 min): 2026-06-09T23:21:12Z

## Iterations

| Iteration | Start UTC | End UTC | Status | Notes |
|---|---:|---:|---|---|
| 1 | 2026-06-09T19:21:12Z | 2026-06-09T19:24:23Z | done | Initialized V40; OpenGWAS HTTP 200, JWT valid until 2026-06-19 12:28 UTC and flagged near-expiry. Claude and Gemini smoke-passed; RPT schema unavailable. Phase 1 dimension map written. |
| 2 | 2026-06-09T19:28:29Z | 2026-06-09T19:29:32Z | done | Ran two grounded Phase 2 probes via `scripts/v40_dimension_probes.py`. Protective/resilience genetics found 0 right-direction tractable targets in 8 genetics/target-like rows. APC-axis topology found a correction-surviving `mixscale_validated_ifng_readout` hub only, supporting mechanism mapping but not target nomination or controllability. |

## Backlog

| Priority | Item | Status | Notes |
|---:|---|---|---|
| 1 | Phase 1: tooling health check | done | Claude and Gemini work; RPT is not implemented in Python client. |
| 2 | Phase 1: map unexplored computational dimensions | done | `meta/DIMENSION_SCOUT_V40.md`; model proposal files under `analysis/v40_dimension_scout_*`. |
| 3 | Phase 2: probe top feasible dimension 1 | done | Protective/resilience-direction genetics: not supported in held frame; 0/8 right-direction tractable genetics/target-like rows. |
| 4 | Phase 2: probe top feasible dimension 2 | done | APC-axis network topology / mechanism mapping: supported as readout topology signal only; corrected hub is `mixscale_validated_ifng_readout`. |
| 5 | Phase 2: write `docs/history/DIMENSION_PROBES_V40.md` | done | Value-complete after two grounded probes. |
| 6 | Phase 3: deepen best dimension if time remains | done | Deepened by interpreting the corrected topology signal conservatively: pursue mechanism mapping, not controllability or target nomination. |
