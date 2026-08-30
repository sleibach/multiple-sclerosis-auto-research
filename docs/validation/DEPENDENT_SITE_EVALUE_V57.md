# V57 Known-Dependence Cluster E-Value Remediation

Status: **synthetic method test failed its complete gate; no MS evidence**

## Fixed Test

The separately frozen
[`V57_DEPENDENT_SITE_EVALUE_PLAN.md`](../plans/V57_DEPENDENT_SITE_EVALUE_PLAN.md)
averaged valid p-to-e factors within each known dependence cluster, multiplied
only across independent completed clusters, and mixed the three original fixed
calibrators. This is e-valid under arbitrary within-cluster dependence when
clusters are independent.

The test used 4.05 million new-seed synthetic sequences.

## Result

- null crossing: `0.00238-0.00644`; null gate passed;
- strong crossing: `0.69502-0.96088`; required minimum `0.75`;
- gain over Bonferroni-minimum: `0.00634-0.03732`; dominance gate passed;
- overall verdict: **`DEPENDENCE_CLUSTER_E_RULE_NOT_VERIFIED`**.

The only failing configuration was four-site clusters at correlation `0.75`,
where strong crossing was `0.69502-0.69726`. With 12 nominal sites, that design
contains only three independent clusters. No valid within-cluster transform can
recreate independent evidence units that are absent.

## Consequence

The cluster-e rule is calibrated and more efficient than the tested
Bonferroni-minimum rule, but V57 does not nominate it without a cluster-count
requirement. A frozen extension now varies only the number of independent
four-site clusters under the worst tested correlation. The result will be a
conditional design boundary, not a claim about any real cohort.

That extension resolved the tested boundary: three clusters failed at minimum
strong crossing `0.69518`, while four were the first all-seed pass at `0.81782`
with maximum null crossing `0.00434`. See
[`DEPENDENCE_CLUSTER_COUNT_V57.md`](DEPENDENCE_CLUSTER_COUNT_V57.md).
