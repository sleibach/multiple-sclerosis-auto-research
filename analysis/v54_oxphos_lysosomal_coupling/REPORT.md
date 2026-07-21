# V54 OXPHOS-Lysosomal Foamy-State Coupling

> Later evidential-grade update: neither endpoint passes Holm correction across
> the complete 12-test V54 post-result morphology sequence (both `p=0.0960`).
> See `analysis/v54_post_result_morphology_multiplicity/REPORT.md`. The local
> coefficients below remain reproducible, but the two-endpoint claim is
> exploratory rather than globally gate-passing.

Verdict: **BOTH_MORPHOLOGY_ASSOCIATIONS_SEPARABLE_UNDER_TESTED_MODEL**.

This post-result sensitivity mutually adjusted the two disjoint transcript
scores within the 54-sample, 21-donor GSE279972 morphology model.

| endpoint | base beta | mutual-adjusted beta | retention | cluster CI | wild p | max-endpoint p | survives |
|---|---:|---:|---:|---:|---:|---:|---|
| oxphos | -0.622 | -0.562 | 0.902 | [-1.003, -0.120] | 0.01066 | 0.01138 | True |
| lysosomal_unique | 0.517 | 0.463 | 0.897 | [0.111, 0.816] | 0.01077 | 0.05183 | True |

Persistence means only that neither fixed transcript score statistically
subsumes the other under these measured covariates. Both remain properties of
one foamy-morphology cohort and lack orthogonal chronic-active-edge support.
No progression, causal, metabolic-flux, target, or treatment inference follows.
