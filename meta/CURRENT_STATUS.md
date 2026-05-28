# V5 Current Status

Last updated: 2026-05-28 20:33 CEST

## Mission State

V5 is active. V4 structure remains canonical; no restructuring is needed.
Current goal is tiered continuation around concrete V4 leads: pregnancy
dimension, MIF/CD74 Tier 1 resolution, prior-art recalibration, and longitudinal
dimension expansion.

## Active Leads

### Pregnancy Axis

Status: active Tier 1.

Key evidence:
- `GSE17410` MS PBMC month-9 pregnancy shows increased `ifn_apc` versus
  pre-pregnancy: delta `0.6358630063022481`, Hedges g
  `1.0723962239804705`, Welch p `0.03686721892111262`.
- Independent `E-MTAB-12260` MS sorted T-cell RNA-seq does not reproduce broad
  late-pregnancy IFN/APC or MIF/CD74 activation. It shows postpartum T-cell
  trafficking increase versus third trimester: delta `0.3020256988998088`,
  Hedges g `0.5685553671142366`, Welch p `0.03795138383060487`.
- `GSE235508` seropositive RA shows late-pregnancy trough and postpartum
  rebound in MIF/CD74/HLA-II/IFN-APC modules.
- `GSE108497` SLE shows outcome-specific pregnancy/postpartum APC/HLA-II
  kinetics; uncomplicated SLE has HLA-II postpartum rebound, while complicated
  SLE differs.

Interpretation: pregnancy remains a strong natural-experiment dimension, but
the mechanism is compartmental and kinetic, not generic IFN/APC suppression.
Next test: `GSE17410` leave-one-out, component decomposition, and
composition-marker residualization.

### MIF/CD74 Stratification

Status: demoted after V5 Tier 1 failure.

Reason:
- V5 forced a real Tier 1 attempt rather than another park.
- Local MS pseudobulk component testing found immune `CD74` almost entirely
  explained by broad APC/size covariates (`R2 0.9702062941435217`), with no
  significant immune residual contrasts.
- GSE282122 anti-TNF myeloid/DC component testing found raw HLA-II/IFN/APC
  response behavior, but receptor-only `CD74/CD44/CXCR4` and full MIF/CD74
  components did not retain adjusted FDR support.

Preserved value: MIF/CD74 can remain a residualized state readout or exploratory
biomarker label, but it should not consume Tier 2/3 therapeutic resources
without a new MS treatment-by-biomarker dataset.

## Recent Outputs

- `meta/ROADMAP_V5.md`
- `results/pregnancy_dimension/emt12260_ms_tcells/REPORT.md`
- `results/pregnancy_dimension/gse108497_sle/REPORT.md`
- `analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk/REPORT.md`
- `analysis/tier_1_mechanism/mif_cd74_gse282122_component_response/REPORT.md`
- `meta/CONVERGENCE_CHECK_V5_01.md`

## Data Added In V5

- `GSE108497_family.soft.gz`
- `GSE108497_normalized_data.txt.gz`
- `E-MTAB-12260` BioStudies metadata, SDRF, and 202 per-sample files
- `data/manifest.tsv` updated with hashes.

## Next Actions

1. Pregnancy Tier 1 survival test: `GSE17410` leave-one-out, robust/component
   decomposition, and marker residualization.
2. Prior-art recalibration continuation: CTSS, TYK2, TREM2, LXR, MerTK, LRRK2,
   LTA4H.
3. Longitudinal dimension expansion: search for accessible pre-diagnostic MS,
   TEDDY/T1D, and pre-IBD public components.

## Compute / Access Notes

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`.
- Python environment: `.venv_v3_py312`.
- Network: direct Python HTTPS may be sandbox-blocked; `curl` works with
  approved access.
- Local TF-IDF knowledge index exists under `knowledge/.index/`.
