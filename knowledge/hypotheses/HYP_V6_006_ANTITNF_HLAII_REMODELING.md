# HYP_V6_006 - Anti-TNF HLA-II Remodeling Versus Receptor-Only CD74 Decline

Status: alive  
Tier: Tier -1  
Opened: 2026-05-28 20:51 CEST

## Hypothesis

Successful anti-TNF response in IBD myeloid/DC compartments may involve a shift
from inflammatory IFN/APC state toward antigen-presentation/remodeling biology,
while receptor-only CD74/CD44/CXCR4 trafficking-like state decreases.

## Opening Evidence

In `GSE282122`:

- major monocyte/macrophage HLA-II-without-CD74 raw remission-associated
  post-treatment delta `0.49146107002316664`, Hedges g
  `0.9957102949370042`, p `0.0011501724707556477`, raw FDR
  `0.011501724707556477`;
- major DC HLA-II-without-CD74 raw delta `0.2019702828200248`, p
  `0.007276149452464594`, raw FDR `0.03118349765341969`;
- major monocyte/macrophage receptor-only `CD74/CD44/CXCR4` raw delta
  `-0.23482858080007848`, Hedges g `-0.6528959302199949`, p
  `0.038295191538057154`;
- these effects lose support after IFN/APC adjustment, making them Tier -1
  remodeling hypotheses rather than Tier 1 claims.

## First Independent Checks

- Search for independent anti-TNF or JAK-inhibitor single-cell datasets with
  pre/post response labels.
- Separate inflammatory IFN/APC, HLA-II remodeling, and CD74/CD44/CXCR4
  trafficking components rather than using a single combined score.

## V6 Tier 0 Attempt - GSE282122 IFN/APC Predictors

Analysis:
`analysis/tier_0_triage/hyp_v6_006_gse282122_ifn_apc_predictors/REPORT.md`.

Result:
- Major monocyte/macrophage delta IFN/APC predicts remission with LOOCV AUC
  `0.7799999999999999`; delta HLA-II-only AUC `0.7555555555555555`;
  delta receptor-only CD74/CD44/CXCR4 AUC `0.6311111111111112`.
- Major DC delta IFN/APC AUC `0.712719298245614`; delta HLA-II-only AUC
  `0.6864035087719298`; delta receptor-only AUC `0.4144736842105262`.
- Major monocyte/macrophage baseline IFN/APC AUC `0.7488888888888888`;
  baseline HLA-II-only AUC `0.7555555555555555`; baseline receptor-only AUC
  `0.5711111111111111`.
- Major DC baseline IFN/APC AUC `0.7390350877192983`; baseline HLA-II-only
  AUC `0.6798245614035088`; baseline receptor-only AUC `0.4605263157894737`.
- Adjusted logistic models are directionally compatible for IFN/APC and HLA-II
  in both major monocyte/macrophage and DC states. Receptor-only behavior is
  weaker by AUC and not consistent across DC.

V6 interpretation:
- This supports promotion of a treatment-response analysis branch centered on
  IFN/APC-HLA-II remodeling, not on MIF/CD74 receptor-specific biology.
- The biological pattern is: responders start with higher IFN/APC and lower
  HLA-II-only scores, then during anti-TNF response IFN/APC falls while HLA-II
  rises. This looks like state remodeling rather than simple suppression.
- Tier 0 promotion requires independent treatment-response replication before
  becoming a Tier 1 mechanism candidate.

## V6 Independent Check - GSE138064 MS IFN-Beta

Analysis:
`analysis/tier_0_triage/hyp_v6_006_gse138064_ms_ifnb_replication/REPORT.md`.

Result:
- Complete responders have higher baseline HLA-II-only than partial responders
  in pooled stable/all 8MU/16MU comparisons:
  - all dose, 4h-pair baseline contrast delta `0.4449570323496644`, Hedges g
    `0.7047761390526338`, p `0.005078303980688954`;
  - all dose, 24h-pair baseline contrast delta `0.4104450356920983`, Hedges g
    `0.6742592815098308`, p `0.008391461023739622`;
  - stable all-dose 24h-pair baseline contrast delta `0.3921334350686166`,
    Hedges g `0.5885030804086917`, p `0.035547151499872046`.
- IFN/APC baseline and acute delta do not show comparable complete-responder
  enrichment; most p values are non-significant and effects smaller.
- Receptor-only CD74/CD44/CXCR4 is not a consistent baseline predictor, though
  one stable all-dose 4h delta contrast is nominal (delta
  `0.31948769395433857`, Hedges g `0.6084492242852696`, p
  `0.0327644119808477`).

V6 interpretation:
- This is independent treatment-response support for an APC/HLA-II remodeling
  axis, but not for a universal IFN/APC-dominant predictor.
- The direction differs from `GSE282122`: anti-TNF remission in gut myeloid/DC
  states associated with higher baseline IFN/APC and lower HLA-II, while
  IFN-beta complete response in MS PBMCs associates more clearly with higher
  baseline HLA-II.
- Refine the hypothesis: different therapies may act through different
  positions on the APC response architecture. Anti-TNF response may require
  inflammatory IFN/APC downshift plus HLA-II restoration, whereas IFN-beta
  response may require intact baseline antigen-presentation/APC competence.
- Keep at Tier 0 candidate; do not promote to Tier 1 until a second independent
  dataset clarifies whether HLA-II competence or IFN/APC remodeling is the
  conserved predictor.

## V6 Independent Check - GSE24427 MS IFN-Beta Longitudinal

Analysis:
`analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/REPORT.md`.

Result:
- Baseline HLA-II-only does not separate patients relapse-free at 2 years from
  those with relapses: delta relapse-free minus not `-0.09640626138025757`,
  Hedges g `-0.409376558072003`, p `0.3026482329504239`.
- Month-1 HLA-II-only increase from baseline is larger in 2-year relapse-free
  patients: delta `0.22896300080351073`, Hedges g `1.0089237828082185`, p
  `0.022387938191276928`.
- IFN/APC deltas do not separate relapse-free patients in this screen.
- Receptor-only baseline has a nominal negative association with relapse-free
  status (delta `-0.1812560007415615`, Hedges g `-0.7234423774846679`, p
  `0.08038933917104127`) but does not dominate longitudinal response.

V6 interpretation:
- `GSE24427` supports a longitudinal HLA-II/APC remodeling branch, not baseline
  HLA-II competence alone and not IFN/APC dominance.
- Together with `GSE138064`, MS IFN-beta datasets point to HLA-II/APC module
  competence or induction as the more reproducible MS treatment-response
  feature.
- Together with `GSE282122`, cross-therapy convergence is best stated as:
  successful treatment is associated with reorganization of IFN/APC and HLA-II
  states, but the conserved measurable component may differ by therapy and
  tissue.
- Status remains Tier 0 candidate. Tier 1 would require a stronger mechanistic
  formulation of why HLA-II induction/competence predicts IFN-beta response
  while anti-TNF gut remission shows IFN/APC downshift with HLA-II restoration.
