# Convergence Check 78 - Fresh Scan And Boyle Candidate Kill Audit

Timestamp: 2026-05-28 09:20 CEST

## Question

After closing the survivor-map branch, does a fresh local breadth scan or
Boyle's advisory route list reveal a candidate worth reopening?

## Evidence

- Wave122 scanned 32,096 genes across local cell-state, MS, response,
  genetics/target-resolution, perturbation/model, and modality evidence.
- Wave122 branch call: `NO_FRESH_ROUTE_FROM_LOCAL_SCAN`.
- Boyle independently suggested `NRCAM`, `CD200`, `MERTK`, `CHI3L1`, and `LIPA`
  as least-bad routes, while also stating no route survives V3 promotion gates.
- Wave123 tested those five suggestions and called
  `NO_REOPEN_ANY_SIDECAR_CANDIDATE`.

## Decision

Do not reopen any Boyle candidate.

## Residual Signal

Wave122's top gene is `NCF2`, with four support channels, but it carries a major
NOX2 host-defense/CGD directionality blocker and Wave62 target-resolution no-go.

## Next Forcing Question

Run a strict `NCF2` / NOX2 route audit. If it fails safety, directionality, or
target-resolution gates, close it and pivot to either a new data modality or a
non-gene-level mechanism search.
