# Convergence Check 60: CD82 Niche-Controller Reopener

Timestamp: 2026-05-27 21:55 CEST

## Current Question

Does the accessible-survivor branch remain closed after the mechanism sidecar's
matched tissue-niche controller test, or does a non-obvious candidate reopen?

## Result

Wave104 branch call: `REOPEN_ACCESSIBLE_SURVIVOR_NICHE_CONTROLLER`.

The reopened candidate is `CD82`, not the Wave101 focus candidates `SEL1L3` or
`FXYD5`.

## Evidence

`CD82` matched tissue-to-myeloid tests:

- adjusted positive disease count: `3`;
- adjusted negative disease count: `0`;
- strongest context:
  `sjogren_gland_stromal -> sjogren_gland_apc | lysosomal_apc`,
  slope `0.500`, p `0.00335`, n `22`;
- IBD contexts:
  `ibd_uc_epithelial -> ibd_uc_myeloid | lipid_loader_repair`,
  slope `0.296`, p `0.00400`, n `12`;
  `ibd_crohn_epithelial -> ibd_crohn_myeloid | lysosomal_apc`,
  slope `1.063`, p `0.0112`, n `12`;
  `ibd_crohn_epithelial -> ibd_crohn_myeloid | lipid_loader_repair`,
  slope `1.061`, p `0.0138`, n `12`.

## Interpretation

This is a reopener, not a finding. `CD82` previously failed as a direct target
marker because it lacked MS anchor strength, perturbation, genetics, and clean
direction. Wave104 suggests a different operationalization: tissue-resident
`CD82` may track or influence matched myeloid lipid-lysosomal state across
Crohn disease, ulcerative colitis, and Sjogren syndrome.

## Main Risk

The adjusted IBD tests use small matched donor counts (`n=12`) and adaptive
covariate trimming. This can create unstable residual correlations. Before any
target story, `CD82` must survive:

- simpler covariate models,
- leave-one-out influence checks,
- permutation tests,
- prior-art and modality review.

## Next Forcing Question

Does the `CD82` niche-controller signal survive robustness tests well enough to
justify target-specific perturbation and modality work?
