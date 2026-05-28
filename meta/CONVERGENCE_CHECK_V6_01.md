# V6 Convergence Check 01

Timestamp: 2026-05-28 21:08 CEST

## What Changed

V6 added Tier -1 exploration and mined V5 failure modes instead of treating
them as endpoints.

Reproducible outputs:
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/REPORT.md`
  scanned `351` patterns and flagged `121`.
- `analysis/tier_minus_1_exploration/v6_promotion_ranking/REPORT.md` ranked
  first Tier 0 attempts.
- `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/REPORT.md` refined
  the pregnancy decoupling branch.
- `analysis/tier_0_triage/hyp_v6_006_gse282122_ifn_apc_predictors/REPORT.md`
  promoted an IFN/APC-HLA-II treatment-response remodeling branch to Tier 0
  candidate.

## Agreements Across Tracks

- MIF/CD74 is not rescued as a receptor-specific therapeutic target.
- The CD74 collapse into APC/size covariates is useful because it points to
  upstream APC-state controllers and state remodeling.
- Pregnancy is not a uniform APC suppression model. It splits into hematologic
  composition, pDC/ISG source, T-cell trafficking, and postpartum APC-axis
  decoupling hypotheses.
- The strongest immediate treatment-response lead is not MIF/CD74 but
  IFN/APC-HLA-II remodeling in `GSE282122`.

## Disagreements / Ambiguities

- `HYP_V6_007` did not fully replicate from `GSE108497` into `GSE235508` SLE:
  SLE showed CD64 down and decoupling positive, but HLA-II down rather than up.
- SPRA showed strong HLA-II rebound and decoupling but not CD64 suppression.
- Same-day DAS28/LAI-P correlations do not support the APC-axis split as a
  simple disease-activity biomarker.

## Current Best Lead

`HYP_V6_006`: anti-TNF response involves IFN/APC decrease with HLA-II remodeling
in myeloid/DC compartments. Major monocyte/macrophage delta IFN/APC LOOCV AUC
is `0.7799999999999999`, stronger than receptor-only CD74/CD44/CXCR4 AUC
`0.6311111111111112`. Major DC shows the same ordering (`0.712719298245614`
versus `0.4144736842105262`).

## Next Forcing Question

Does IFN/APC-HLA-II remodeling replicate in an independent treatment-response
setting, preferably MS IFN-beta response (`GSE24427`, `GSE138064`) or another
autoimmune therapeutic perturbation?

Decision: download `GSE24427` and `GSE138064` GEO SOFT files and attempt an MS
treatment-response replication. If response labels are not extractable, route
to psoriasis `GSE228421` or additional IBD treatment-response datasets.
