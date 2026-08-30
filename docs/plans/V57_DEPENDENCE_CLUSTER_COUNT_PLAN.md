# V57 Independent Dependence-Cluster Count Plan

Status: **frozen after three-cluster power failure and before count outcomes**

## Fixed Question

Under the worst tested known-dependence configuration, how many genuinely
independent clusters are required for the unchanged cluster-e process to clear
its strong-signal power gate?

## Design

- four sites per dependence cluster;
- within-cluster Gaussian-copula correlation `0.75`;
- mutually independent clusters;
- cluster counts `3`, `4`, `5`, `6` (12, 16, 20, 24 nominal sites);
- uniform null and `Beta(0.25,1)` strong alternative;
- seeds `57171`, `57172`, `57173`;
- 100,000 sequences per seed/scenario/count;
- unchanged site p-to-e calibrators, within-cluster arithmetic mean,
  across-cluster products, calibrator mixture, and threshold `20`.

## Boundary

The first eligible count must have, in every seed:

1. null ever-crossing at most `0.055`; and
2. strong-alternative crossing at least `0.75`.

No intermediate outcomes can change the grid or gate. The resulting count is
conditional on this synthetic generator and does not substitute for an overlap
audit or empirical cohort effects.
