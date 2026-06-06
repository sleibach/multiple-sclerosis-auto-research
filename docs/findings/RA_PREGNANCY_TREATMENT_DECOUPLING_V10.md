# RA_PREGNANCY_TREATMENT_DECOUPLING_V10

Status: V10 audit of RA pregnancy-near versus APC/treatment-far disagreement.

## Question

Why is RA near MS on pregnancy modulation but far on blood IFN/APC and
treatment-response architecture?

Supported V8 placements:

- `axis_01_ifn_apc`: RA `far/supported/medium`.
- `axis_07_treatment_response`: RA `far/supported/medium`.
- `axis_08_tissue_repair_resolution`: RA `far/supported/medium`.
- `axis_09_sex_hormonal_pregnancy`: RA `near/supported/medium`.

## Evidence

### RA Blood IFN/APC Is Far From MS

Local single-cell/blood myeloid evidence:

- `mixscale_validated_ifng_readout`: delta `-0.0178`, Hedges g `-0.182`,
  p `0.580`, FDR `0.686`, `18` RA and `18` controls.
- `ifn_apc`: delta `-0.0460`, Hedges g `-0.249`, p `0.450`, FDR `0.572`.

Interpretation:

- The blood myeloid/APC cross-sectional IFN/APC state that supported MS/IBD
  proximity is absent or negative in RA blood.

### RA Blood Treatment-Response Rule Fails

Locked/follow-on V7 validation:

- `GSE12051` RA blood baseline IFN/APC: AUC `0.382`, Hedges g `-0.339`, n
  `44`.
- `GSE138746_CD14` RA anti-TNF baseline CD14 monocytes: AUC `0.485`, Hedges g
  `-0.099`, n `78`.
- `GSE8350` RA infliximab 2-week blood `-delta_IFN_APC`: AUC `0.450`, Hedges g
  `-0.356`, n `18`.

Interpretation:

- RA blood does not transfer the IBD dynamic IFN/APC response architecture.

### RA Pregnancy Modulation Is Near MS As A Natural Experiment

GSE235508 seropositive RA timecourse:

| Module | Late pregnancy T3 - early T1 | 6wk postpartum T4 - T3 | 6mo postpartum T5 - T3 | Later postpartum T6 - T3 |
| --- | ---: | ---: | ---: | ---: |
| `mif_cd74_receptor_state` | `-0.642` | `0.526` | `0.781` | `1.162` |
| `hla_ii_only` | `-0.646` | `0.493` | `0.844` | `1.394` |
| `ifn_apc` | `-0.551` | `0.137` | `0.651` | `1.267` |
| `lysosomal_apc` | `-0.566` | `0.309` | `0.496` | `0.835` |

Interpretation:

- Seropositive RA has a pregnancy trough and postpartum rebound in APC/HLA-II
  modules.
- This resembles a hormonal/natural-experiment immune-kinetic axis, not a
  therapy-response biomarker axis.

## Artifact Audit

Compartment:

- RA treatment-response evidence is blood/CD14/blood.
- RA pregnancy evidence is blood.
- Compartment mismatch is lower for treatment-response versus pregnancy than
  for IFN/APC cross-sectional versus pregnancy, but cell composition remains
  possible because pregnancy whole blood shifts immune and hematologic
  composition.

Perturbation class:

- Strong mismatch. Anti-TNF treatment perturbation is not pregnancy.
- Pregnancy is systemic endocrine, immunologic, vascular, and hematologic
  remodeling.

Measurement class:

- Treatment-response uses response classification and baseline/early therapy
  features.
- Pregnancy uses timecourse module kinetics, not treatment outcome prediction.

## Mechanistic Interpretation

The RA disagreement survives as a perturbation-class biological candidate:

> RA shares with MS a pregnancy/postpartum immune-kinetic axis but not the
> blood APC treatment-response architecture tested in V7.

This means RA is not globally far from MS. It is far from MS specifically as a
blood APC treatment-response comparator.

## MS Transfer Consequence

What transfers:

- Pregnancy/postpartum timing logic.
- Hormonal/natural-experiment immune-resolution and rebound hypotheses.
- RA as a comparator for postpartum immune rebound.

What does not transfer:

- RA blood anti-TNF APC response biomarkers.
- RA blood IFN/APC cross-sectional state as a model for MS/IBD mucosal APC
  proximity.

## Falsifiable Prediction

If the RA/MS pregnancy adjacency is real and perturbation-class specific:

- RA and MS pregnancy/postpartum data should share timing-sensitive rebound or
  suppression patterns in some immune modules, but those modules should not
  rescue the failed RA blood anti-TNF IFN/APC response rule.

Stop-loss:

- If matched RA/MS pregnancy datasets show no shared timing architecture after
  composition adjustment, or if RA anti-TNF response becomes predictable by the
  same pregnancy modules in independent cohorts, this decoupling is downgraded.

## Current Tier

Tier 1 biological disagreement candidate, but not a therapeutic claim.

Main blocker:

- Need matched cell-composition-adjusted RA/MS pregnancy/postpartum datasets,
  ideally with monocyte/APC resolution and clinical activity timecourses.
