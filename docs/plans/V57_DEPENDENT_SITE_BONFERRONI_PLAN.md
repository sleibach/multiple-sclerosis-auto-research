# V57 Known-Dependence Bonferroni Cluster Remediation Plan

Status: **frozen after maximum-p power loss was observed and before remediation
outcomes**

## Fixed Failure to Address

Maximum-p collapse controlled null crossing but strong-alternative crossing
fell to `0.02990-0.03102` for four-site clusters at correlation `0.25`. The
rule is safe but may be unusable.

## Fixed Remediation

For each declared dependence cluster of size `m`, compute:

```text
p_cluster = min(1, m * min(p_1, ..., p_m))
```

This Bonferroni-minimum p-value is valid under arbitrary within-cluster
dependence by the union bound. Enter each completed cluster once into the
unchanged mixture e-process. Keep the original maximum-p rule as a comparator,
not as a selector.

Retain the complete V57 dependent-site generator unchanged except for new
seeds `57151`, `57152`, `57153`. Use 50,000 sequences per cell, 12 source sites,
cluster sizes `2-4`, correlations `0.25`, `0.50`, `0.75`, the same three beta
marginals, fixed e-calibrators, and boundary `20`.

## Gate

The Bonferroni cluster rule passes only if:

1. null crossing is at most `0.055` in every cluster/correlation/seed cell;
2. strong-alternative crossing is at least `0.75` in every cell; and
3. strong-alternative crossing is no lower than maximum-p collapse in any
   corresponding cell.

No observed result may select between cluster rules, change the family
correction, or weaken the gate. Cross-cluster independence and truthful cluster
declaration remain required.
