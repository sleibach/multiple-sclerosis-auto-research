# V47 Queue: External Knowledge Segregation and Expansion

Block start UTC: 2026-06-13T18:35:06Z
Target UTC (+360 min): 2026-06-14T00:35:06Z

## Stop Conditions

Valid stops only:

1. cumulative measured runtime >= 360 minutes and clean resumable point;
2. external termination;
3. documented all-fronts block after every internally executable alternative is exhausted.

Backlog exhaustion is not a stop. When executable todo items drop below five,
generate more internally executable tasks before continuing.

## Phase 0 Rule

No external knowledge integration occurs until:

- `docs/knowledge/EPISTEMIC_CLASSES.md` exists;
- `knowledge_external/` exists;
- `scripts/v47_provenance_gate.py synthetic-check --fail-on-error` passes;
- `scripts/v47_provenance_gate.py audit --fail-on-error` passes.

## Iterations

| Iteration | Start UTC | End UTC | Status | Notes |
|---|---:|---:|---|---|
| 1 | 2026-06-13T18:35:06Z | 2026-06-13T18:43:20Z | done | Built Phase 0 epistemic-class definitions, separate external storage tree, JSON schema, and provenance gate with synthetic and real audit PASS before external integration. |

## Live Backlog

| Priority | Front | Item | Status | Notes |
|---:|---|---|---|---|
| 1 | Phase 0 segregation | Define epistemic classes and external storage boundary | done | `docs/knowledge/EPISTEMIC_CLASSES.md`, `knowledge_external/README.md`, schema, and placeholder external record/synthesis dirs added. |
| 2 | Phase 0 segregation | Implement provenance gate with synthetic pass/fail fixtures | done | `scripts/v47_provenance_gate.py`; synthetic check PASS (`4` cases, `3` expected failures caught); real audit PASS (`0` failures, `0` external records). |
| 3 | Phase 0 segregation | Integrate provenance gate into generated-checker/stale-output governance | todo | Only after the gate itself passes. |
| 4 | Competitor/source cataloging | Create classed competitor-source catalog skeleton without external claims | todo | Structure only until Phase 0 passes. |
| 5 | Navigation/index | Create class-aware external knowledge index generator | todo | Must read only `knowledge_external` records and preserve class labels. |
| 6 | External integration | MSGD resource metadata record and source catalog entry | todo | Phase 0 passed; requires source verification before record creation. |
| 7 | External integration | MS Data Alliance Catalogue resource metadata record and source catalog entry | todo | Phase 0 passed; requires source verification before record creation. |
| 8 | External integration | MSBase/NARCOMS/IMSGC/GWAS Catalog comparator records | todo | Phase 0 passed; requires source verification before record creation. |

## Running Notes

- 2026-06-13T18:35:06Z: V47 started. OpenGWAS check passed with JWT valid to
  `2026-06-19 12:28 UTC` (`RENEW_SOON`). SAP AI Core health passed for Claude,
  Gemini, and RPT. No external knowledge has been integrated.
- 2026-06-13T18:43:20Z: Phase 0 segregation verification complete. Provenance
  gate synthetic check PASS (`4` synthetic cases, `3` intentional failure
  cases caught: missing source, external marker in grounded tree, and external
  as project evidence). Real repository audit PASS (`1` check, `0` failures,
  `0` external JSON records). External integration is now permitted only under
  `knowledge_external/` with the gate passing every iteration.
