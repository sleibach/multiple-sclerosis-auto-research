# POSTPARTUM APC-ARM PREREGISTRATION V44

Status: frozen validation-readiness plan for a future postpartum MS cohort.
Date: 2026-06-12

This is a preparation artifact, not a finding. It freezes how the project will
test the postpartum HLA-II/CD64 APC-arm hypothesis if suitable data arrive. No
real postpartum MS validation data were read while writing it.

## Hypothesis

Pregnancy-phase project data support an HLA-II/CD64 APC-arm imbalance in MS
PBMCs, but the decisive postpartum relapse-window test is missing. The frozen
test is:

> MS subjects who relapse within the early postpartum window will show a weaker
> rebound, or continued suppression, of `HLA-II minus CD64` from late pregnancy
> to early postpartum than subjects who remain relapse-free.

The primary score is oriented so higher values predict relapse:

`postpartum_apc_risk_score = -[(postpartum_6w_HLAII_minus_CD64) - (late_pregnancy_HLAII_minus_CD64)]`

## Required Cohort

Human MS pregnancy/postpartum immune-expression cohort with:

- late-pregnancy sample, preferably trimester 3;
- early postpartum sample, target 4-8 weeks postpartum;
- relapse status through 3 months postpartum, with 6 months recorded if
  available;
- expression adequate to score HLA-II and CD64 arms;
- steroid exposure, infection, DMT stop/restart, breastfeeding/lactation,
  batch/QC, and cell-count metadata where available.

Acceptable assays:

- bulk PBMC/whole blood expression;
- sorted myeloid/APC expression;
- single-cell/CITE-seq pseudobulk by APC/myeloid compartment.

Not acceptable for primary validation:

- pregnancy-only data without postpartum samples;
- postpartum data without relapse-window labels;
- cytometry-only data lacking HLA-II and CD64-equivalent readouts.

## Frozen Modules

HLA-II arm:

`HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`, `HLA-DQB1`

CD64 arm:

`FCGR1A`, `FCGR1B`, `FCGR1C`

Module coverage:

- HLA-II scoreable if at least 50% of genes/features map.
- CD64 scoreable if at least one FCGR1/CD64 feature maps.
- If FCGR1 isoforms are not distinguishable but a validated CD64 protein or
  feature score is supplied, report it as a pre-specified alternate CD64 arm and
  keep the primary gene-based result marked unavailable.

## Frozen Analysis

1. Map genes/features before looking at relapse association.
2. Z-score genes across eligible late-pregnancy and early-postpartum samples.
3. Compute HLA-II and CD64 arm scores separately.
4. Compute `HLAII_minus_CD64` at late pregnancy and early postpartum.
5. Compute `postpartum_apc_risk_score` as the negative rebound.
6. Compare relapse versus no-relapse subjects with fixed orientation:
   relapsers predicted higher.
7. Report HLA-II, CD64, and difference components separately. The difference
   score alone cannot be interpreted without the arms.

## Confounder And Technical Audits

Report raw primary score first. Then audit:

- steroid exposure;
- infection;
- DMT stop/restart timing;
- breastfeeding/lactation;
- batch/QC metadata;
- monocyte/myeloid composition if available.

If the raw score passes but is explained by steroid exposure, infection, or
batch, the result is non-specific, not a clean validation.

## Success, Failure, And Inconclusive Criteria

Clean pass for `n >= 30` labeled subjects:

- AUC `>= 0.70`;
- Hedges g `>= 0.50`;
- lower bootstrap 95% AUC CI `> 0.55`;
- residual AUC after steroid + DMT restart adjustment `>= 0.65`;
- HLA-II and CD64 components are reportable.

Small-n directional pass:

- same AUC/g direction criteria, but either response group has fewer than 15
  subjects. This remains provisional.

Fail:

- `n >= 30` with AUC `< 0.60` or Hedges g `< 0.20`; or
- direction opposite to the locked prediction with AUC `< 0.45`; or
- no HLA-II/CD64 module coverage.

Inconclusive:

- insufficient sample size;
- missing relapse labels;
- missing postpartum timepoint;
- confounder/technical structure prevents specific interpretation.

## Synthetic Harness Check

Script:

- `scripts/v44_secondary_lead_harnesses.py`

Outputs:

- `analysis/v44_secondary_lead_harnesses/secondary_harness_summary.json`
- `analysis/v44_secondary_lead_harnesses/secondary_harness_metrics.tsv`
- `analysis/v44_secondary_lead_harnesses/synthetic/postpartum_null_synthetic.tsv`
- `analysis/v44_secondary_lead_harnesses/synthetic/postpartum_planted_synthetic.tsv`

Synthetic result:

- null synthetic: AUC `0.551`, Hedges g `0.157`, expected fail, observed fail;
- planted synthetic: AUC `0.933`, Hedges g `2.305`, expected pass, observed
  pass.

Synthetic data are method checks only and are not evidence about MS.

## Interpretation Grid

| Future result | Interpretation |
|---|---|
| Clean pass | Supports postpartum APC-arm rebound failure as a relapse-window monitoring hypothesis; still needs independent replication. |
| Raw pass but confounded | Biologically interesting but not specific; prioritize resolving steroid/DMT/infection/batch explanation. |
| Adequate-power fail | Demote postpartum APC-arm hypothesis; pregnancy-phase APC movement remains context only. |
| Inconclusive | Use effect size and CI for acquisition/power planning; do not promote. |

