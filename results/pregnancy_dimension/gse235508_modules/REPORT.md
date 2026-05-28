# GSE235508 Pregnancy Module Screen

Random seed: `20260528`

## Dataset

`GSE235508`: 335 whole-blood RNA-seq samples from RA, SLE, and healthy-control
pregnancies. GEO metadata states samples cover before pregnancy, trimesters,
6 weeks postpartum, 6 months postpartum, and 12 months postpartum. This first
pass uses numeric GEO `timepoint` values as given and groups `1,2,3` as
pregnancy and `0,4,5,6` as pre/postpartum; exact label mapping remains to be
confirmed from the source paper.

## Result

Seropositive RA (`SPRA`) shows a pregnancy-associated decrease in the
MIF/CD74-HLA-II/IFN APC axis:

| Module | n pregnancy | n nonpreg/post | delta pregnancy - nonpreg/post | Hedges g | Welch p |
|---|---:|---:|---:|---:|---:|
| `mif_cd74_receptor_state` | 44 | 49 | -0.4850522024358721 | -0.5860997928281567 | 0.006276097402756851 |
| `hla_ii_only` | 44 | 49 | -0.5039563377463558 | -0.5521686482759153 | 0.009608482720167235 |
| `ifn_apc` | 44 | 49 | -0.41565175202081406 | -0.4188179134905435 | 0.04384852719658707 |

Seronegative RA (`SNRA`) does not show this decrease. SLE trends in the
opposite direction for several inflammatory/metabolic modules:

- `SLE` `lysosomal_apc`: delta `0.4078224853076211`, Hedges g
  `0.4667998699735174`, p `0.019983579752313813`.
- `SLE` `hif_nampt_metabolic`: delta `0.5469869581731981`, Hedges g
  `0.6464070940706913`, p `0.0014594275165510694`.

Disease-activity correlations are not significant:

- `SPRA` DAS28 versus `mif_cd74_receptor_state`: rho
  `-0.0031974023225797327`, p `0.9761394042342714`.
- Combined RA DAS28 versus `mif_cd74_receptor_state`: rho
  `0.054184190035440144`, p `0.5279134937064944`.
- SLE LAI(P) versus `mif_cd74_receptor_state`: rho `0.08159862517867626`,
  p `0.42686879132333144`.

## Interpretation

This supports the pregnancy axis as a useful V4 natural-experiment dimension,
not yet a therapeutic finding. The signal is consistent with pregnancy reducing
an APC/antigen-presentation module in seropositive RA while SLE follows a
different inflammatory trajectory. It does not show that the module predicts
clinical activity in the current simple correlation test.

## Caveats

- Timepoint coding needs source-paper confirmation before stronger claims.
- This is whole blood; cell composition can drive module changes.
- The screen uses a small hardcoded Ensembl gene panel for auditability.
- No multiple-testing correction has been applied in this first pass.

## Trace

- Script: `scripts/analyze_gse235508_pregnancy_modules.py`
- Metadata: `data/derived/GSE235508/sample_metadata.tsv`
- Counts: `data/raw/GSE235508/GSE235508_mRNA_counts.txt.gz`
- Outputs:
  - `sample_module_scores.tsv`
  - `pregnancy_contrasts.tsv`
  - `disease_activity_correlations.tsv`
  - `summary.json`
