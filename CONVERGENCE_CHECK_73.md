# Convergence Check 73 - ABTB2 Rerank Artifact Closure

Timestamp: 2026-05-28 08:16 CEST

## Question

Does ABTB2 deserve an individual forcing test after Wave116 selected it as the
next open route?

## Evidence

- Wave81 parked ABTB2 only because of a Wave37 CRISPR efferocytosis signal.
- The Wave37 signal is not FDR-supported (`efficient_fdr=0.9601`,
  `contrast_fdr=0.9200`) and uses four sgRNAs.
- MS white-matter expression does not support the route (`delta_log2=-0.1477`,
  `p=0.8826`, `fdr=0.9840`).
- Genetics/target-resolution, modality, and IBD response channels are absent.
- Wave71 already called `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.
- Wave110 listed no concrete next test.

## Decision

Close ABTB2 as an orchestration artifact, not a biology finding.

## Reranker Reformulation

Wave116 now requires `has_concrete_next_test=True` for actionable route
selection. This prevents a low-quality PARK row from being selected solely
because many stronger routes were already closed.

## Next Forcing Question

Rerun Wave116 with the stricter actionable filter. If it selects a route with
actual concrete perturbation, disease anchoring, or modality evidence, audit it.
If it only surfaces old `NO_GO` classes, pivot out of the Wave110 route family.
