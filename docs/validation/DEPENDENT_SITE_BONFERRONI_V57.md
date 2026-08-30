# V57 Bonferroni Known-Dependence Remediation

Status: **synthetic method test failed its complete gate; no MS evidence**

## Fixed Test

After maximum-p cluster collapse proved too conservative, the separately frozen
[`V57_DEPENDENT_SITE_BONFERRONI_PLAN.md`](../plans/V57_DEPENDENT_SITE_BONFERRONI_PLAN.md)
used `min(1, m * min(p_i))` for each known cluster of size `m`. This p-value is
valid under arbitrary within-cluster dependence. New seeds retained every
generator and e-process setting.

The test comprised 4.05 million synthetic sequences.

## Result

- null crossing: `0.00186-0.00564`; null gate passed;
- strong crossing: `0.65732-0.95186`; required minimum `0.75`;
- strong crossing gain over maximum-p: `0.23716-0.83956`; dominance gate
  passed;
- overall verdict: **`BONFERRONI_DEPENDENCE_CLUSTER_RULE_NOT_VERIFIED`**.

The failure was confined to the fixed power criterion, with four-site clusters
at correlation `0.75` reaching only `0.65732-0.66420`. Good null control and a
large gain over maximum-p do not permit weakening the predeclared gate.

## Consequence

Bonferroni-minimum is a valid conservative fallback, but V57 does not nominate
it as the routine cluster rule. A separately frozen cluster-e method will test
whether valid p-to-e factors can be averaged within a known dependence cluster
and multiplied only across independent clusters. If that also fails, related
sites should remain descriptive or one prespecified site should be selected
without outcome access.
