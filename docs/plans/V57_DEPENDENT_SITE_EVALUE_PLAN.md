# V57 Known-Dependence Cluster E-Value Plan

Status: **frozen after Bonferroni power failure and before cluster-e outcomes**

## Rationale

For each fixed calibrator `k`, every site contributes a valid e-factor
`e_i,k = k * p_i^(k-1)`. Under arbitrary dependence within a declared cluster,
their arithmetic mean remains a valid e-variable because its expectation is at
most one. If the resulting clusters are mutually independent, products of
cluster means remain valid. Averaging e-factors can retain more signal than
first converting the cluster to an adjusted p-value.

## Fixed Rule

At completion of each declared cluster `c`, compute separately for every fixed
calibrator:

```text
E_c,k = mean_i-in-c [k * p_i^(k-1)]
```

Multiply `E_c,k` across independent completed clusters and average the three
fixed calibrator products exactly as in the original mixture. Use threshold
`20`. Never look within a partially received cluster and never treat its
members as separate arrivals.

Retain the complete dependence generator, site counts, cluster sizes,
correlations, beta marginals, and 50,000 sequences per cell. Use new seeds
`57161`, `57162`, `57163`. Bonferroni-minimum is a fixed comparator.

## Gate

The cluster-e rule passes only if:

1. null crossing is at most `0.055` in every cell;
2. strong-alternative crossing is at least `0.75` in every cell; and
3. strong-alternative crossing is no lower than Bonferroni-minimum in every
   corresponding cell.

Truthful cluster declaration and independence between completed clusters are
still required. The method cannot repair hidden cross-cluster overlap.
