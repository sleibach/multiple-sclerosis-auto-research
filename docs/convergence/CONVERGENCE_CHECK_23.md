# Convergence Check 23

Timestamp: 2026-05-27 12:38 UTC.

## Current Question

Can target-resolved cross-autoimmune genetics identify a central node of the
lipid-lysosomal myeloid module that is also intervention-grade?

## New Evidence

Wave62 queried Open Targets Platform credible sets, L2G predictions, and QTL
colocalisation rows across 12 autoimmune disease labels.

Counts:

- Study rows: 539.
- Eligible GWAS studies: 95.
- Credible sets: 2506.
- L2G rows: 4821.
- QTL colocalisation rows: 16823.
- Target summaries: 2028.
- Reopen calls: 0.
- Park calls: 32.

## Agreement Across Tracks

- Genetics agrees that cross-autoimmune target resolution is real for several
  loci: examples include `RGS1`, `INAVA`, `ANKRD55`, `IL7R`, `STAT4`,
  `PTGER4`, `SP140`, and `GALC`.
- Cell-state/module evidence continues to point to a lipid-lysosomal,
  antigen-processing, inflammatory myeloid state rather than one clean
  druggable genetics hit.
- Perturbation-first evidence does not rescue the broad genetics hits; the
  prior Wave61 gate found zero intervention-grade candidates.

## Disagreement

- The strongest genetics rows are not the strongest lipid-lysosomal module
  rows.
- The module-linked rows (`SP140`, `GALC`, `IFI30`) either lack intervention
  modality, have insufficient breadth, or are blocked by host-defense biology.
- Broad and druggable immune-axis rows (`IL7R`, `STAT4`, `PTGER4`, `IL2RA`)
  are prior-art or directionality blocked.

## Decision

Do not promote a Wave62 target as the V3 finding.

Next forcing question: do the parked target-resolved rows define a shared,
controllable state transition or pathway node that can be attacked upstream or
downstream, instead of nominating the genetics gene itself?

Immediate next branch:

- Build a transition-controller intersection table for parked Wave62 genes
  against prior state, residual, perturbation, Geneformer, L1000, and
  druggability outputs.
- Require a candidate to improve over Wave62 by adding a real intervention
  point, not just another association layer.
