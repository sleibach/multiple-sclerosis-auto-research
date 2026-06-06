# Convergence Check 26

Timestamp: 2026-05-27 15:14 CEST.

## Current Question

Does paired disease-tissue anti-TNF perturbation in RA synovium provide a
specific lipid-lysosomal/APC pharmacodynamic signal, or is the signal dominated
by broad inflammatory and tissue-composition shifts?

## New Evidence

Wave65 `GSE198520` audit:

- 92 samples, 46 RA patients, paired baseline and week-12 anti-TNF synovial bulk
  RNA-seq.
- Response classes parsed from sample IDs and GEO metadata: 19 good responders,
  13 moderate responders, 14 nonresponders.
- Histologic pathotypes: 21 Myeloid, 17 Lymphoid, 8 Fibroid.
- Several modules decrease after anti-TNF in all patients:
  - `mixscale_validated_ifng_readout`: -0.404, FDR 0.00927.
  - `mif_cd74_receptor_state`: -0.346, FDR 0.00927.
  - `ifn_apc`: -0.352, FDR 0.0241.
  - `lysosomal_apc`: -0.291, FDR 0.0340.
- None exceed the specificity threshold:
  - target/generic ratios range from 0.275 to 1.148, below the required 2.0.
- No response-specific effect survives generic/pathotype adjustment:
  - adjusted response FDRs range from 0.655 to 0.999.

## Agreement

- RA anti-TNF response contracts a broad inflammatory synovial state.
- The contraction includes APC/lysosomal and MIF/CD74-like signatures, but these
  move with generic IFN/NF-kB rather than as a separable module.
- This is consistent with the hostile-gate warning: treatment-response bulk
  tissue signatures are poor evidence for a cell-intrinsic transition
  controller.

## Disagreement

- Cross-disease observational recurrence still points to a lipid-lysosomal/APC
  inflammatory myeloid state.
- This paired RA perturbation result does not identify an intervention point
  inside that state. It mainly says anti-TNF is too broad and bulk synovium too
  confounded to resolve the controller.

## Decision

Do not promote any target from `GSE198520`.

Do not continue bulk treatment-response scoring as the main route.

Next forcing question:

Can an orthogonal non-expression modality, especially class-level lipidomics or
proteomics across autoimmune diseases, identify whether the shared state is
driven by sphingolipid/cholesterol handling, NAD/HIF metabolism, lysosomal
proteostasis, or another biochemical axis?
