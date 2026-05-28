# HYP_V6_004 - APC-State Controller Upstream Of CD74

Status: alive  
Tier: Tier -1  
Opened: 2026-05-28 20:51 CEST

## Hypothesis

The useful biology behind repeated MIF/CD74 observations is not CD74 as a
standalone target, but an upstream APC-state controller that jointly regulates
CD74, HLA-II, IFN/APC state, antigen processing, and cell-size/library-size
features in lesion and treatment-response contexts.

## Opening Evidence

V5 MS pseudobulk component testing found immune `CD74` almost entirely explained
by broad APC/size covariates:

- covariate R2 `0.9702062941435217`;
- immune residual CD74 contrasts were not significant;
- treatment-response data in GSE282122 showed HLA-II and IFN/APC behavior
  rather than receptor-specific MIF/CD74 behavior.

## Tier -1 Interpretation

The collapse of CD74 into APC/size covariates is mechanistic information. It
argues for testing upstream controllers such as CIITA/RFX/Mediator/JAK-STAT or
myeloid differentiation state, not rerunning raw CD74 screens.

## First Independent Checks

- Mine existing perturbation tables for genes whose perturbation changes
  HLA-II/CD74 more than generic IFN.
- Reuse CIITA/Mediator pharmacologic-gap outputs as candidate controller
  sources.
- Test whether APC controller residuals predict treatment response better than
  CD74 in GSE282122.
