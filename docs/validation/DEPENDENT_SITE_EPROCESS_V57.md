# V57 Dependent-Site E-Process Stress Test

Status: **synthetic method characterization; no MS evidence accumulated**

## Question

What happens if two or more returned sites share participants, centers,
biobanks, or source-study effects but are incorrectly multiplied as independent
evidence?

## Frozen Test

The pre-outcome design is
[`V57_DEPENDENT_SITE_EPROCESS_PLAN.md`](../plans/V57_DEPENDENT_SITE_EPROCESS_PLAN.md).
It generated 12 valid marginal p-values in Gaussian-copula clusters of size
`2-4` with within-cluster correlation `0.25-0.75`. It compared naive treatment
of all sites as independent with a conservative maximum-p collapse of each
known cluster.

Three seeds and 50,000 sequences per cell produced 4.5 million synthetic
sequences.

## Result

| Path | Null crossing range | Frozen null gate | Outcome |
|---|---:|---:|---|
| Independent baseline, naive | `0.00902-0.00930` | `<=0.055` | pass |
| Correlated sites, naive | `0.01672-0.08214` | descriptive | anti-conservative at the high end |
| Known-cluster maximum-p guard | `0-0.00088` | `<=0.055` | pass |

The worst naive null was cluster size `4`, correlation `0.75`, with crossing
`0.08214`. The same direction was already visible at cluster size `3`,
correlation `0.75` (`0.06150-0.06176`) and size `4`, correlation `0.50`
(`0.05518-0.05600`). A duplicate-token check alone cannot detect this when
overlap is misdeclared.

The maximum-p guard controlled error but was often too conservative: strong-
alternative crossing ranged from `0.02990` to `0.98534`, with the low end in
four-site, weakly correlated clusters.

Verdict: **known dependence must not be multiplied as independent evidence.**
Maximum-p collapse is valid but can discard nearly all power. A separately
frozen Bonferroni-minimum remediation controlled null crossing but failed its
complete power gate (`0.65732` minimum versus `0.75`). See
[`DEPENDENT_SITE_BONFERRONI_V57.md`](DEPENDENT_SITE_BONFERRONI_V57.md). A
cluster-e remediation is frozen next; neither failed/unfinished rule is the
primary combiner.

## Operational Boundary

- A site packet needs an auditable participant/source-family/center/biobank
  overlap declaration, not just a site name.
- Unknown or falsely declared overlap cannot be repaired statistically and is
  a reason to abstain.
- Known clusters may be represented by one valid cluster-level p-value only;
  sites within the cluster must still retain their individual effect sizes and
  diagnostics.
- Independence between the resulting clusters remains required.
- This simulation does not estimate overlap in any real MS cohort.

## Reproduce

```bash
.venv/bin/python scripts/v57_dependent_site_eprocess_probe.py
```

Outputs are under `analysis/v57_dependent_site_eprocess/`.
