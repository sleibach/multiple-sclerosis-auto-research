# Convergence Check 75 - HLA-II Route Closure Hygiene

Timestamp: 2026-05-28 08:36 CEST

## Question

Does HLA-DPB1/HLA-DPA1/HLA-DRA provide a viable intervention point for the
shared lipid-lysosomal myeloid module?

## Evidence

- Wave116 selected HLA-DPB1 only after previous closures removed stronger
  candidates.
- Wave91 classified HLA-DPB1/HLA-DPA1 as
  `PARK_RESPONSE_DIRECTIONS_WEAK_OR_UNDERPOWERED`.
- The recommended test for HLA-DPB1/HLA-DPA1 was
  `UNSPECIFIED_ROUTE_NOT_AUDITED`.
- HLA-DRA carried `NO_GO_BROAD_MHC_CLASS_II`.
- Prior analysis repeatedly treated broad antigen-presentation suppression as
  unsafe and nonselective for a therapeutic V3 claim.

## Decision

Close HLA-DPA1, HLA-DPB1, and HLA-DRA as intervention routes.

## Reranker Reformulation

Wave116 now counts no-go/blocker text in `recommended_next_test` as a
`no_go_source`. This fixes a failure mode where blocked rows were selected
because their explicit no-go status lived outside the `source_call` column.

## Next Forcing Question

Rerun Wave116. If only low-scoring parked wet-lab-only rows remain, decide
whether one is worth a strict closure audit or whether to pivot into a fresh
target-class search outside the current survivor maps.
