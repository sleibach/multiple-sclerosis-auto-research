# V57 Independent Dependence-Cluster Count Boundary

Status: **conditional synthetic planning boundary; no MS evidence**

## Frozen Test

After a 12-site design reduced to only three independent four-site clusters and
failed the cluster-e power gate, the pre-outcome
[`V57_DEPENDENCE_CLUSTER_COUNT_PLAN.md`](../plans/V57_DEPENDENCE_CLUSTER_COUNT_PLAN.md)
varied only the number of mutually independent clusters. Cluster size `4`,
within-cluster correlation `0.75`, p-value marginals, e-calibrators, and
threshold remained fixed.

The extension used 2.4 million new-seed synthetic sequences.

## Result

| Independent clusters | Nominal sites | Maximum null crossing | Minimum strong crossing | Status |
|---:|---:|---:|---:|---|
| 3 | 12 | `0.00331` | `0.69518` | fail power |
| 4 | 16 | `0.00434` | `0.81782` | first pass |
| 5 | 20 | `0.00532` | `0.89149` | pass |
| 6 | 24 | `0.00614` | `0.93675` | pass |

Verdict: **four independent clusters are the first all-seed passing point in
the tested worst-case dependence generator.**

## Interpretation

The evidence unit is the independent cluster, not the nominal site. This
boundary does not mean every future project needs 16 cohorts, nor does it
estimate real overlap or effect size. It says that, under one deliberately
severe dependence structure and strong synthetic alternative, three
independent units did not meet the fixed 75% power requirement while four did.

Operationally:

- declare participant, center, biobank, source-study, and preprocessing overlap
  before outcomes;
- combine known dependent sites once at cluster completion;
- require independence between clusters for product evidence;
- treat fewer than four independent clusters as a power warning, not as an
  invalid p/e process;
- abstain when dependence cannot be bounded or declared honestly.
