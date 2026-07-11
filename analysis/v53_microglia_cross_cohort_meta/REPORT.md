# V53 Cross-Cohort CD44/CXCR4 State Synthesis

Verdict: **POSITIVE_CROSS_SOURCE_EFFECT_WITH_HETEROGENEITY_AND_LOW_SOURCE_FAMILY_COUNT**.

## Commensurate Effects

Each donor-level receptor score was standardized within cohort, then fit with the
same disease, age, quadratic-age, and sex model; both Macnair partitions also
include deposited study or source-bank fixed effects. All three adjusted standardized effects are
positive:

| partition | adjusted standardized beta | HC3 95% CI |
|---|---:|---:|
| GSE111972 | `1.317` | `0.575` to `2.058` |
| Macnair_validation | `1.635` | `0.932` to `2.338` |
| Macnair_discovery | `0.427` | `-0.305` to `1.159` |

## Heterogeneity And Dependence

The conventional three-partition random-effects estimate is `1.130`
(95% CI `0.419` to `1.841`), with
I2 `65.3%` and tau2 `0.258`. This is a
sensitivity only because the two Macnair partitions share one deposition package.

The package-aware analysis gives the Macnair partitions equal weight, varies their
unknown correlation from 0 to 1, and pools that package estimate with GSE111972.
Across the full correlation sweep, the lowest normal-theory CI bound is
`0.654` and the largest p is
`8.826e-06`. However, the exact
two-package sign test is `p=0.500`: two source
families are too few for an independent meta-significance claim.

## Interpretation

The direction is not driven by one analyzed partition, and normal-theory estimates
remain positive under worst-case Macnair dependence. Effect magnitude is strongly
heterogeneous, and the source-family count is small. The defensible result remains a
replicated, quality-qualified state association. It is not a causal receptor
mechanism, stage-specific marker, monitoring rule, therapeutic direction, or target.
