# V57 Dependent-Site E-Process Stress Plan

Status: **frozen before simulation outcomes**

## Purpose and Boundary

The federated combiner assumes independent cohorts and rejects duplicate
declared independence groups. Partial participant, center, biobank, or source-
study overlap can nevertheless create positively correlated valid p-values if
it is misdeclared. This probe quantifies the optional-stopping risk and tests a
conservative rule for sites that are known to share a dependence cluster.

This is seeded synthetic method characterization. It is not MS evidence.

## Fixed Generator

- 12 arriving sites;
- seeds `57141`, `57142`, `57143`;
- 50,000 sequences per cell;
- cluster sizes `1`, `2`, `3`, and `4` (12 is divisible by each);
- independent baseline: cluster size `1`, correlation `0`;
- within-cluster Gaussian-copula correlations `0.25`, `0.50`, `0.75` for
  sizes `2-4`; clusters remain mutually independent;
- p-value marginals: uniform null, `Beta(0.5,1)` moderate alternative, and
  `Beta(0.25,1)` strong alternative;
- unchanged V57 mixture e-process and threshold `20`.

Two paths are computed:

1. **naive path:** treat every site as independent;
2. **known-cluster guard:** replace all p-values in a declared dependence
   cluster by their maximum and enter that maximum once when the cluster is
   complete.

The maximum is a valid conservative p-value under arbitrary within-cluster
dependence because `P(max(P_i) <= t) <= P(P_j <= t) <= t` for any valid member
p-value. It does not protect overlap that is hidden or falsely declared across
clusters.

## Method-Behavior Gate

1. independent-baseline naive null crossing by arrival 12 must be `<=0.055`
   in every seed;
2. known-cluster guarded null crossing must be `<=0.055` for every tested
   cluster size, correlation, and seed.

Naive correlated-site inflation and guarded alternative power are descriptive.
No observed result may change the e-calibrator, threshold, cluster grid, or
maximum-p rule. Operational use requires an auditable source-family,
participant-overlap, center, and biobank declaration; unknown dependence
remains a reason to abstain.
