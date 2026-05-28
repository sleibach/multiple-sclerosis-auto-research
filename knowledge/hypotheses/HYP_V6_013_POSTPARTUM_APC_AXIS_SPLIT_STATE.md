# HYP_V6_013 - Postpartum APC-Axis Split State

Status: alive  
Tier: Tier -1  
Opened: 2026-05-28 20:59 CEST

## Hypothesis

Postpartum immune rebound across autoimmune diseases separates into at least two
APC-state arms: an inflammatory Fc-receptor/CD64 arm and an HLA-II/regulatory
antigen-presentation rebound arm. Healthy pregnancy couples HLA-II rebound with
CD64 suppression; autoimmune diseases may uncouple the two arms, producing
disease-specific flare or remission trajectories.

## Parent Hypothesis

Refinement of `HYP_V6_007`.

## Opening Evidence

`GSE108497`:
- uncomplicated SLE postpartum versus late pregnancy shows HLA-II rebound and
  monocyte-CD64 fall.

`GSE235508` independent check:
- healthy controls show full HLA-II-up/CD64-down direction with mean postpartum
  HLA-II delta `0.13906061527240574`, CD64 delta `-0.3197314246209488`, and
  decoupling delta `0.4587920398933544`;
- SLE shows CD64 down and positive decoupling but HLA-II down;
- seropositive RA shows strong HLA-II and decoupling rebound but not CD64 down.

## Tier -1 Interpretation

The exact SLE-specific pattern did not replicate cleanly, but the split between
HLA-II and CD64 arms is itself a stronger hypothesis than the original
single-disease claim. It predicts that postpartum risk may depend on which arm
rebounds first and whether tissue-trafficking gates are open.

## First Independent Checks

- In `GSE235508`, correlate HLA-II, CD64, and HLA-minus-CD64 decoupling with
  DAS28 in RA and LAI-P in SLE by timepoint.
- Test whether postpartum T-cell trafficking in `E-MTAB-12260` aligns with the
  HLA-II arm, the CD64 arm, or neither.
- Search for postpartum MS relapse cohorts with blood expression, serum
  chemokines, or immune-cell composition.

## V6 GSE235508 Disease-Activity Check

Analysis:
`analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/disease_activity_correlations.tsv`.

Result:
- SPRA DAS28 correlations are weak for HLA-II, CD64, and the decoupling index
  (`|rho| <= 0.085`, all p `>0.42`).
- SLE LAI-P correlations are weak for HLA-II, CD64, and decoupling (`|rho| <=
  0.119`, all p `>0.24`).
- SNRA has a nominal regulatory-pregnancy correlation with DAS28 (`rho
  0.3144437325741744`, p `0.02950687828379952`), but this is not the central
  APC-axis split.

Interpretation:
- The APC-axis split is visible as pregnancy/postpartum state biology, but
  `GSE235508` does not show a simple cross-sectional disease-activity
  correlation. This keeps the hypothesis at Tier -1 rather than promoting it
  as a Tier 0 disease-activity biomarker.
- Next refinement should focus on flare timing or treatment state, not same-day
  DAS28/LAI-P correlation.
