# V57 Multivariate Cell-State Transport-Map Probe: Frozen Plan

Status: **frozen before outcomes**

## Question

Is treatment response associated with the geometry of cell-state displacement
between paired samples, even though marginal Wasserstein distances and global
energy distances were not supported?

This is a method-feasibility probe in anti-TNF-treated IBD, not MS evidence.

## Fixed Map

- Use five fixed module scores, robust-scaled globally.
- Analyze DC and Mono compartments separately.
- Under seeds 57141, 57142, and 57143, take exactly 50 cells from each paired
  pre/post sample-compartment.
- Solve the balanced minimum-cost Euclidean assignment with the Hungarian
  algorithm; each pre cell maps to one post cell.

Freeze four displacement-field summaries:

1. mean matched transport cost;
2. directional coherence, the norm of mean displacement divided by mean
   displacement norm;
3. anisotropy, largest displacement-covariance eigenvalue divided by trace;
4. displacement-norm median absolute deviation.

## Test

Aggregate repeated patient-compartment pairs by median. Compare remission with
non-remission using disease-stratified patient-label permutations and max-T
across all estimable compartment-summary pairs. A residualized analysis adjusts
for disease, sequencing-depth transport cost, module mean-shift norm, and
inflammation-score change.

## Gate

A summary passes only if raw and residualized max-T p<=0.10, signs agree,
directions agree in CD and UC, and all three cell-subsampling seeds pass. Cells
are never outcome replicates. Any isolated seed or analysis pass is rejected.
