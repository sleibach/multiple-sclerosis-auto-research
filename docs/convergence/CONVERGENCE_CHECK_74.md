# Convergence Check 74 - CD44 Parser-Bug Closure

Timestamp: 2026-05-28 08:26 CEST

## Question

Does CD44 remain open as a lipid-lysosomal module intervention point?

## Evidence

- Wave91 already called CD44 `NO_GO_ROUTE_BLOCKED`.
- The Wave91 blocker is
  `NO_GO_ADHESION_MATRIX_PRIOR_ART_AND_BROAD_BIOLOGY`.
- MS white-matter support is nominal only and not FDR-supported
  (`delta_log2=1.3447`, `p=0.0332`, `fdr=0.8507`).
- Wave62 target-resolution call is `NO_GO_WAVE62_TARGET_RESOLUTION`.
- Prior sidecars repeatedly demoted the SPP1/CD44 axis for broad matrix,
  trafficking, repair, oncology, EAE, and autoimmune prior art.

## Decision

Do not reopen CD44. Close CD44 and SPP1 in Wave116.

## Reranker Reformulation

Wave116 now parses Wave91-specific fields:

- `wave91_call`
- `route_blocker`
- `module_intervention_score`

This prevents no-go Wave91 rows from being selected as if they were open rows
with zero score.

## Next Forcing Question

Rerun Wave116 after the parser fix. If only old no-go classes remain, leave the
route family and run a fresh breadth-first search over target classes rather
than repeatedly mining already-closed survivor maps.
