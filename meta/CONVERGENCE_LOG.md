# V4 Convergence Log

## Checkpoint 001 - V4 Method Reset

Timestamp: 2026-05-28 12:23 CEST

## Converged Lessons From V3

1. Prior art must be graded, not binary. A known target can still support a V4
   contribution if subgroup, modality, combination, direction, or mechanism is
   new.
2. Effort must be tiered. V3 spent too much effort evenly across weak and strong
   candidates.
3. Breadth must become dimensional. V3 was broad across diseases but dominated
   by cross-sectional transcriptomics.

## Current Shared Belief

The first high-yield V4 work is not new discovery. It is recalibrating V3
demotions under the new prior-art rulebook and creating dimensional evidence
channels, especially longitudinal and natural-experiment data.

## Current Disagreement To Resolve

Some V3 demotions may be evidence-driven and should stay closed. Others were
prior-art-driven and should re-enter Tier 0. Phase 2 will classify them.

## Checkpoint 002 - Phase 3 Initial Convergence

Timestamp: 2026-05-28 13:04 CEST

Note: earlier V4 entries include some 13:xx timestamps inherited from the
interrupted session context. Current shell time is `2026-05-28 13:04 CEST`;
active-work time should be interpreted by sequence, not by those inconsistent
wall-clock stamps.

## Current Shared Belief

The Phase 2 prior-art recalibration did not yield an immediately Tier-1-ready
therapeutic candidate.

- `CIITA_SELECTIVE` / `CDK8_CDK19_MEDIATOR`: biologically plausible selective
  APC/MHC-II decoupling, parked because the druggable CDK8/CDK19 route lacks
  human APC pharmacologic phenocopy of the `MED16` benchmark.
- `NAMPT`: demoted from alive Tier 0 by evidence, not prior art. Signal is
  IBD/T1D metabolic-state/readout biology with no MS anchor, no non-IBD retained
  residual, no local genetics, and no non-NAD-depleting modality evidence.
- `MIF_CD74_STRATIFICATION`: parked. MS white-matter residual signal is nominal
  but not FDR-stable; no local treatment-interaction test exists.
- `PREGNANCY_REMISSION_AXIS`: now populated as a V4 natural-experiment
  dimension using `GSE235508` and `GSE17410`.

## New Convergence

`GSE235508` provides a directional natural-experiment signal in seropositive RA:
pregnancy is associated with lower `mif_cd74_receptor_state`, HLA-II-only, and
IFN/APC module scores. `GSE17410` MS PBMCs do not replicate that direction;
month-9 pregnancy has higher `ifn_apc`. This blocks a naive cross-disease
"pregnancy uniformly suppresses APC/HLA-II" claim.

## Current Disagreement To Resolve

Can MIF/CD74/HLA-II stratification be rescued as a disease-specific rather than
pan-autoimmune biomarker by component-resolved and treatment-interaction tests,
or should it remain a readout-only axis?
