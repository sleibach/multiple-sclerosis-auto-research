# GSE235508 Pregnancy Timecourse Analysis

Random seed: `20260528`

## Question

Does the coarse pregnancy-versus-postpartum result hide trajectory structure
that can explain the V5 MS-versus-RA inconsistency?

## Result

Using GEO numeric timepoints as coded in sample metadata, seropositive RA
(`SPRA`) shows a late-pregnancy trough and postpartum rebound in APC/HLA-II
modules:

| Module | T3 - T0 | T4 - T3 | T5 - T3 | T6 - T3 |
|---|---:|---:|---:|---:|
| `mif_cd74_receptor_state` | -0.6424432741594277 | 0.5257536055434748 | 0.7805233800580105 | 1.1619638346454728 |
| `hla_ii_only` | -0.6457936633424115 | 0.49332466806661124 | 0.8439979693509585 | 1.3943411658318148 |
| `ifn_apc` | -0.5513304775594587 | 0.1372470258403542 | 0.6512447533034429 | 1.2666698095003408 |
| `lysosomal_apc` | -0.5662370859013741 | 0.3093805692625864 | 0.49611183151097826 | 0.8348912395304886 |

SLE behaves differently: IFN/APC, lysosomal/APC, and HIF/NAMPT rise by late
pregnancy versus pre-pregnancy and then fall postpartum.

| Module | T3 - T0 | T4 - T3 | T5 - T3 | T6 - T3 |
|---|---:|---:|---:|---:|
| `ifn_apc` | 0.6971567029514993 | -0.532900415413021 | -0.5837257009718169 | -0.6088541662968279 |
| `lysosomal_apc` | 0.6362256991756912 | -0.44849852206424146 | -0.38668229879008464 | -0.31872947194023205 |
| `hif_nampt_metabolic` | 0.9358559540737126 | -0.5996896634648188 | -0.5721495108813226 | -0.6015762352901444 |

## Interpretation

This supports a kinetic framing rather than a single pregnancy-suppression
framing. In seropositive RA, late pregnancy suppresses the APC/HLA-II axis and
postpartum releases it. In SLE, late pregnancy is already high for IFN/APC-like
and metabolic inflammatory modules, consistent with pregnancy being less
protective or flare-prone in SLE.

The MS `GSE17410` month-9 PBMC IFN/APC increase therefore need not be a simple
artifact. It may be closer to an SLE-like peripheral late-pregnancy priming
state while clinical MS relapse risk is still suppressed by CNS, trafficking,
hormonal, or regulatory-cell mechanisms. This is now the core V5 forcing
question.

## Caveats

- Timepoint labels are inferred from GEO numeric metadata and must be confirmed
  against the source paper.
- The analysis is unadjusted for cell composition except insofar as whole-blood
  module behavior is the object of study.
- T6 sample counts are small in several groups.

## Trace

- Script: `scripts/analyze_gse235508_timecourse.py`
- Input: `results/pregnancy_dimension/gse235508_modules/sample_module_scores.tsv`
- Outputs:
  - `module_timepoint_means.tsv`
  - `timepoint_contrasts.tsv`
  - `timepoint_ols_terms.tsv`
  - `summary.json`
