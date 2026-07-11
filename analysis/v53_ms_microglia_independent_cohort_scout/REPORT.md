# V53 Independent MS Microglia Cohort Scout And Frozen Test

Verdict: **replicated MS microglial CD44/CXCR4 state association with a
microglia-depth quality qualification**. This is not a causal mechanism,
monitoring rule, intervention direction, or therapeutic target.

## What Was Run

The public Macnair et al. Zenodo release (`10.5281/zenodo.8338963`) supplies
complete cell metadata, donor covariates, and two deposited count matrices. A
streaming C++ extractor scanned `2,012,213,369` real Matrix Market entries while
retaining only the 16 frozen V53 genes, microglial library totals, and deposited
microglia annotations. The compressed matrices (`1.70` and `4.56` GB) were not
stored or committed.

Every primary and secondary model used donor-level aggregation, age, quadratic
age, sex, study/batch where applicable, HC3 intervals, and `100,000` seeded wild
null replicates per test (`seed=53507`). Cross-study duplicate donor codes in
the validation composite were resolved before outcome modeling by retaining the
source with the most eligible microglia.

## Results

| cohort | independent units | frozen primary | depth/QC sensitivity | component sensitivity | honest verdict |
|---|---:|---|---|---|---|
| Macnair validation composite | 18 MS, 13 controls; 11,222 microglia | beta `1.414`; standardized effect `2.212`; wild `p<0.00001`; CI `0.806-2.022` | score/log-cell rho `0.666`, but cell-count-adjusted beta `1.075`, wild `p=0.00480`; all 10-100-cell thresholds positive | joint HLA/MIF/IFN/lysosomal-adjusted beta `0.919`, wild `p=0.00335` | Frozen and tightened gates pass; formal secondary decoupling passes, with sparse MIF/DDT warning. |
| Macnair discovery | 54 MS, 26 controls; 51,677 microglia | beta `0.510`; standardized effect `0.669`; wild `p=0.00461`; CI `0.142-0.879` | score/log-cell rho `0.389`; cell-count-adjusted beta `0.341`, wild `p=0.05398`; every 10-100-cell threshold remains positive and corrected | joint component-adjusted beta `0.420`, wild `p=0.00751` | Frozen primary passes; conservative depth tightening is borderline, so quality-sensitive rather than clean. |

The discovery result is not being rescued by a favorable threshold: the full
fixed `1/10/25/50/100` sensitivity grid is reported, and the explicit
cell-count model is retained even though it narrowly crosses `0.05`. Conversely,
the signal is not explained away by sparse controls: direction and corrected
inference persist at every executable minimum-cell threshold and after joint
APC-state adjustment in both cohorts.

## Interpretation

Together with the original, separately deposited GSE111972 result, these analyses reject the
single-cohort-artifact explanation for the **state association**. They do not
establish a CD44/CXCR4-specific causal mechanism. GSE111972 failed its strict
component-specificity gate, the Macnair MIF/DDT control genes are sparsely
detected, and prior art already places both receptor components in MS myeloid
activation biology. The defensible update is therefore:

> A CD44/CXCR4-high microglial state recurs across separate MS brain source
> families and both analyzed partitions of the Macnair package,
> but its independence from broader APC activation and its therapeutic
> direction remain unresolved.

The Macnair discovery and validation matrices share one Zenodo/manuscript
package. Their anonymized donor-token sets do not collide, but person-level
independence cannot be proven across cohort-specific identifier namespaces.
See `analysis/v53_microglia_source_lineage_audit/REPORT.md` for the counting
boundary.

A later deposited-source sensitivity adds a material qualification. Macnair
discovery has strong disease/brain-bank association (Cramer's V `0.773`); after
source-bank fixed effects its standardized beta is `0.427` with wild `p=0.245`
and a CI crossing zero. The validation composite remains robust after study
fixed effects and leave-one-study checks. See
`analysis/v53_macnair_source_influence/REPORT.md`.

The next useful analysis is cross-cohort disease-stage and lesion-context
heterogeneity under fixed scores, followed by a third donor-balanced cohort or
prospective tissue assay with pre-specified minimum microglial yield.
