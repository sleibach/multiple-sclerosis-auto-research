# V57 Overlapping-Neighborhood Differential-Abundance Probe: Frozen Plan

Status: **frozen before outcomes**

## Question

Can a cluster-free neighborhood representation detect a response-specific
treatment shift that hard cell-category composition, marginal transport, and
global multivariate geometry missed?

The held data are paired anti-TNF IBD single cells, not MS. This tests method
feasibility only.

## Outcome-Blind Neighborhoods

- Use the five fixed module scores and analyze DC and Mono separately.
- Robust-scale modules globally.
- Build one fixed reference per compartment by taking 50 cells from every
  eligible sample, using seed 57130 without outcome labels.
- Select 20 farthest-point landmarks per compartment.
- Define each overlapping neighborhood as the 100 nearest reference cells to
  its landmark; freeze the resulting radius and center.

## Paired Abundance

Under count seeds 57131, 57132, and 57133, take exactly 50 cells from every
eligible sample-compartment. For each neighborhood, compute the arcsine-square-
root transformed proportion and post-minus-pre change. Aggregate repeated
patient pairs by median.

Neighborhoods are estimable only when both outcomes occur in CD and UC. No
cell is an inferential replicate; the patient is the unit.

## Test and Gate

- Raw remission-versus-non-remission studentized difference.
- Residualized test adjusts for disease, mean module shift, sequencing-depth
  change, and inflammation-score change.
- 200,000 disease-stratified label permutations per seed and analysis.
- max-T over every estimable compartment-neighborhood.
- Require raw and residualized max-T p<=0.10, matching signs, matching CD/UC
  directions, and passage under all three count seeds.

Anything else is not supported. A held IBD result cannot be promoted as MS
biology or a target.
