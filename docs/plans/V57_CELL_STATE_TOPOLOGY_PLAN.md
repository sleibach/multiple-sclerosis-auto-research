# V57 Paired Cell-State Topology Probe: Frozen Plan

Status: **frozen before outcomes**

## Question

Do paired treatment samples show a response-specific change in the branching
or cluster structure of multivariate immune-cell states that was missed by
mean, marginal-distribution, composition, energy-distance, and tensor probes?

The held eligible data are anti-TNF-treated IBD single cells, not MS. This is a
bounded method-feasibility test and cannot establish MS biology.

## Representation

- Use the five previously fixed module scores and DC/Mono compartments.
- Robust-scale each module globally.
- Deterministically subsample exactly 150 cells per sample-compartment.
- Compute Euclidean distances and the minimum spanning tree. Its edge lengths
  are the exact finite 0-dimensional Vietoris-Rips persistence lifetimes.
- Freeze four summaries: total persistence, maximum lifetime, normalized
  persistence entropy, and 90th-percentile-to-median lifetime ratio.

For every patient/compartment/metric, test post-minus-pre topology. Fixed cell
counts remove sample-size dependence from the topology summaries.

## Controls and Null

- Aggregate repeated patient-compartment pairs by median.
- Raw test: remission versus non-remission studentized difference.
- Residualized test: adjust for disease, the matching topology change in
  sequencing depth, multivariate mean shift, and inflammation-score change.
- Use 200,000 response-label permutations stratified by CD/UC and max-T across
  all eight compartment-metric tests.
- Require concordant signs in CD and UC.
- Repeat all calculations under seeds 57121, 57122, and 57123.

## Promotion Gate

A feature passes only if, under every seed:

1. raw and residualized max-T p-values are <=0.10;
2. raw and residualized effects have the same sign; and
3. raw and residualized effects have that sign in both CD and UC.

Anything less is a corrected null or instability result. No gene or target is
selected in this probe.
