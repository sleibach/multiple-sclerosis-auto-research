# V57 Competitive Matched-Module Null Plan

## Question

Is the bounded frozen V22 module unusually associated with response compared
with arbitrary same-size modules that have similar measurable expression
properties in both cohorts?

This is a competitive same-data specificity audit, not discovery and not a
replacement-score search.

## Frozen construction

- Use the full common measured-gene universe from the existing local
  `GSE235357` and `GSE253006` source files; no quarantined data.
- For each frozen gene, identify its 200 nearest non-V22 genes by four
  outcome-blind properties: mean and standard deviation in each cohort.
- Generate 50,000 matched module pairs under each of three seeds.
- Preserve the exact module topology: seven IFN/APC slots, six HLA-II slots,
  one shared slot corresponding to `HLA-DRA`, and no duplicated random gene
  within a module pair.
- Preserve the locked therapy-class formulas: HLA-II minus IFN/APC for the DMF
  cohort and negative IFN/APC for the anti-TNF cohort.
- Primary statistic: pooled AUC after outcome-blind within-cohort percentile
  transformation, matching the V57 selective and influence audits.
- Random module identities are not retained or interpreted; aggregate null
  distributions are sufficient and prevent turning this falsification test
  into a search.

## Gate

Competitive specificity requires, under every seed:

1. empirical upper-tail p below `0.05`; and
2. intact V22 AUC above the random-module 95th percentile.

No favorable seed may rescue a failure.

### Mandatory match-quality amendment

The first outcome-blind matching diagnostic showed broad 200-neighbor distance
for `CD74` and several HLA-II genes. Before treating the competitive result as
final, the candidate neighborhoods are therefore frozen at `25`, `50`, `100`,
and `200` nearest genes and the entire null is rerun. This amendment is
triggered by covariate-match quality, not by selecting an outcome. The final
gate requires every neighborhood and seed to pass; no favorable neighborhood
can rescue a failure.

## Boundary

Passing excludes a broad class of expression/variance-matched arbitrary modules
as a sufficient explanation in the same bounded data. It does not provide
external replication, functional matching, mechanistic specificity, or
clinical validation. Failing means the observed performance is not exceptional
against this competitive null and must be downgraded accordingly.
