# V6 Current Status

Last updated: 2026-05-28 20:51 CEST

## Mission State

V6 is active. V4/V5 structure remains canonical, but V6 adds a new
`Tier -1` exploration layer for hypothesis generation. V5 demotions remain
valid at therapeutic-claim tiers, but their failure modes now seed exploration
instead of closing the thread.

Primary V6 objective: mine existing V3-V5 data, confounders, adjusted-away
signals, and negative results for concrete Tier -1 hypotheses, then promote
the strongest to Tier 0 only after independent support and V4 prior-art
contribution checks.

## Active Leads

### Tier -1 Registry

Status: active.

New files:
- `meta/TIER_MINUS_1_RULEBOOK.md`
- `meta/ROADMAP_V6.md`
- `knowledge/hypotheses/INDEX.md`
- `knowledge/hypotheses/HYP_V6_001_*.md` through
  `knowledge/hypotheses/HYP_V6_012_*.md`

Initial Tier -1 hypotheses:
- MS pregnancy erythroid/platelet/neutrophil hematologic axis.
- MS pregnancy pDC-depletion / ISG-source switch.
- Postpartum T-cell trafficking readiness.
- APC-state controller upstream of CD74.
- OPC CD74 lesion-stress state.
- Anti-TNF HLA-II remodeling versus receptor-only CD74 decline.
- SLE pregnancy HLA-II / monocyte-CD64 decoupling.
- CTSS, TREM2, LTA4H, LXR, and TYK2 narrower refinement branches.

### Initial Pattern Mining

Status: completed first pass.

Script:
- `scripts/mine_v6_tier_minus_1_patterns.py`

Outputs:
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/REPORT.md`
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/all_patterns.tsv`
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/tier_minus_1_flagged_patterns.tsv`
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/summary.json`

Result:
- Scanned `351` patterns across V5 pregnancy, lesion pseudobulk, and GSE282122
  treatment-response outputs.
- Flagged `121` patterns under Tier -1 criteria: uncorrected p `<0.10` or
  absolute Hedges g `>0.50`.
- Top openings include SLE postpartum monocyte-CD64/lysosomal-APC suppression,
  GSE282122 IFN/APC-down remission remodeling, raw HLA-II-up remission
  remodeling, and GSE17410 composition-preserved ISG behavior.

### Treatment-Response Remodeling

Status: active Tier 0 candidate.

Candidate:
- `HYP_V6_006` has been reframed from MIF/CD74 to APC response architecture.

Evidence:
- `GSE282122` anti-TNF IBD: IFN/APC and HLA-II components predict/remodel with
  remission better than receptor-only CD74/CD44/CXCR4. Major monocyte/macrophage
  delta IFN/APC LOOCV AUC `0.7799999999999999`; receptor-only AUC
  `0.6311111111111112`.
- `GSE138064` MS IFN-beta: complete responders show higher baseline HLA-II-only
  than partial responders, but IFN/APC does not replicate as dominant predictor.
  All-dose 4h-pair baseline HLA-II delta complete-minus-partial
  `0.4449570323496644`, Hedges g `0.7047761390526338`, p
  `0.005078303980688954`.
- `GSE24427` MS IFN-beta: baseline HLA-II-only does not predict two-year
  relapse-free status, but month-1 HLA-II-only increase is larger in
  relapse-free patients: delta `0.22896300080351073`, Hedges g
  `1.0089237828082185`, p `0.022387938191276928`.

Interpretation:
- Independent support exists for APC/HLA-II response architecture, not for a
  universal IFN/APC predictor and not for CD74 receptor-specific targeting.
- Tier 1 promotion is blocked until the mechanism is sharpened: MS IFN-beta
  response points toward HLA-II/APC competence or induction, while IBD anti-TNF
  response points toward IFN/APC downshift with HLA-II restoration.

### Pregnancy Axis

Status: active Tier -1/Tier 1 boundary.

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

V6 interpretation: the `GSE17410` IFN/APC signal should not be used as a
specific APC/MIF/CD74 claim. The composition shift itself is now a Tier -1
hypothesis source: erythroid, platelet, neutrophil, and pDC-source-switch
biology may be relevant to postpartum risk or may prove technical.

### MIF/CD74 Stratification

Status: demoted as V5 Tier 1 therapeutic mechanism; reopened only as Tier -1
failure-mode source.

Reason:
- V5 forced a real Tier 1 attempt rather than another park.
- Local MS pseudobulk component testing found immune `CD74` almost entirely
  explained by broad APC/size covariates (`R2 0.9702062941435217`), with no
  significant immune residual contrasts.
- GSE282122 anti-TNF myeloid/DC component testing found raw HLA-II/IFN/APC
  response behavior, but receptor-only `CD74/CD44/CXCR4` and full MIF/CD74
  components did not retain adjusted FDR support.

V6 interpretation: the collapse into broad APC/size covariates opens
`HYP_V6_004_APC_STATE_CONTROLLER_UPSTREAM_OF_CD74`; nominal OPC residuals open
`HYP_V6_005_OPC_CD74_LESION_STRESS_STATE`. Neither re-promotes MIF/CD74 as a
therapeutic claim.

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

1. Integrate sidecar reports:
   `subagents/20260528_v6_confounder_mining.md`,
   `subagents/20260528_v6_pregnancy_generativity.md`,
   `subagents/20260528_v6_negative_result_mining.md`, and
   `subagents/20260528_v6_longitudinal_data_scout.md`.
2. Convert top flagged patterns into additional Tier -1 entries where the
   registry lacks coverage.
3. For `HYP_V6_006`, decide whether to formulate a Tier 1 mechanism around
   therapy-specific APC response architecture or to seek one more perturbation
   comparator such as psoriasis `GSE228421`.
4. Rebuild the knowledge index after V6 registry updates.

## Compute / Access Notes

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`.
- Python environment: `.venv_v3_py312`.
- Network: direct Python HTTPS may be sandbox-blocked; `curl` works with
  approved access.
- Local TF-IDF knowledge index exists under `knowledge/.index/`.
