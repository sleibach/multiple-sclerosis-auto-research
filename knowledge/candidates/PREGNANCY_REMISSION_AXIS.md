# Pregnancy Remission Axis

Status: parked  
V4 tier: Tier 0  
Last updated: 2026-05-28

## Rationale

Pregnancy is a natural experiment across MS and several autoimmune diseases.
V3 did not systematically use this dimension.

## V4 Contribution Hypothesis

Pregnancy-induced remission may reveal endogenous immune-resolution programs
that distinguish causal disease drivers from cross-sectional inflammation.

## Next Tier 0 Test

Catalog public pregnancy/postpartum autoimmune transcriptomic,
immune-repertoire, and clinical trajectory datasets.

## V4 Dataset Scout

Sidecar completed: Zeno (`019e6e35-771a-7900-80b4-9f007184588e`).

Highest-value verified starting datasets:

| Dataset | Disease coverage | Modality | Tier 0 use |
|---|---|---|---|
| `GSE235508` | RA, SLE, healthy pregnancy | longitudinal blood bulk plus scRNA/cell-type-adjusted transcriptomics | strongest immediate RA/SLE natural-experiment anchor |
| `GSE17410` | MS pregnancy | PBMC expression array before pregnancy vs ninth month | usable MS pregnancy Tier 0 screen, older bulk PBMC |
| `GSE17449` | MS pregnancy-related superseries | expression array, likely overlapping with `GSE17410` | support/metadata only unless independent samples are verified |
| `GSE153459` | healthy pregnancy reference mapped to MS/RA/SLE methylation | CD4 T-cell DNA methylation by trimester | cross-disease hormonal immune-regulation reference, not disease-outcome data |
| `GSE122894` | EAE/MS model pregnancy | mouse TCR-beta repertoire in Tcon/Treg, pregnant vs non-pregnant EAE | cross-species MS mechanistic support |

Blockers:
- no verified public MS single-cell pregnancy/postpartum dataset yet;
- no verified public psoriasis pregnancy/postpartum autoimmune omics dataset;
- IBD pregnancy microbiome evidence needs accession/access confirmation.

Tier 0 direction: populate a pregnancy-remission module screen using
`GSE235508` and `GSE17410` first, then test whether candidate programs from V4
move toward pregnancy remission in RA/MS and diverge in SLE where pregnancy may
worsen disease.

## GSE235508 First-Pass Result

Screen completed:
`results/pregnancy_dimension/gse235508_modules/REPORT.md`.

Result:
- Seropositive RA (`SPRA`) shows pregnancy-associated reduction of
  `mif_cd74_receptor_state`: delta `-0.4850522024358721`, Hedges g
  `-0.5860997928281567`, Welch p `0.006276097402756851`.
- `SPRA` also shows reduced `hla_ii_only`: delta `-0.5039563377463558`,
  p `0.009608482720167235`, and reduced `ifn_apc`: delta
  `-0.41565175202081406`, p `0.04384852719658707`.
- SLE trends opposite for `lysosomal_apc` and `hif_nampt_metabolic`.
- Disease-activity correlations with DAS28 or LAI(P) were not significant.

Interpretation: this validates pregnancy as a useful V4 natural-experiment
dimension and raises an APC/HLA-II suppression hypothesis in seropositive RA,
but it is not yet a clinical biomarker or target claim.

## GSE17410 MS First-Pass Result

Screen completed:
`results/pregnancy_dimension/gse17410_ms_modules/REPORT.md`.

Result:
- MS month-9 pregnancy does not replicate the seropositive-RA APC/HLA-II
  suppression direction.
- `ifn_apc` is higher at month 9 than pre-pregnancy: delta
  `0.6358630063022481`, Hedges g `1.0723962239804705`, Welch p
  `0.03686721892111262`.
- `mif_cd74_receptor_state` is also directionally higher but not significant:
  delta `0.12194807085829851`, p `0.20974913196132225`.

Interpretation: pregnancy remission cannot be treated as a uniform
cross-disease APC/HLA-II suppression mechanism. The axis remains valuable, but
the mechanism is disease-, tissue-, or cell-composition-dependent and requires a
more careful longitudinal/cell-type model.

## GSE235508 Timecourse Result

Screen completed:
`results/pregnancy_dimension/gse235508_timecourse/REPORT.md`.

Result:
- Seropositive RA shows a late-pregnancy trough and postpartum rebound in
  `mif_cd74_receptor_state`, HLA-II-only, IFN/APC, and lysosomal/APC modules.
- SLE differs: IFN/APC, lysosomal/APC, and HIF/NAMPT rise by late pregnancy
  versus pre-pregnancy and fall postpartum.

Interpretation: the V5 pregnancy lead should be framed kinetically. Pregnancy
does not uniformly suppress inflammatory APC biology across autoimmune
diseases. MS month-9 PBMC IFN/APC increase may represent peripheral
late-pregnancy priming that is uncoupled from CNS relapse risk until postpartum.

## V5 Independent MS T-cell Check: E-MTAB-12260

Analysis completed:
`results/pregnancy_dimension/emt12260_ms_tcells/REPORT.md`.

Data handling:
- Downloaded 202 BioStudies sample files listed by `E-MTAB-12260.sdrf.txt`.
- Excluded four SDRF-listed files because they were CpG/beta methylation tables,
  not RNA `gene/count` tables: `Sample76.txt`, `Sample80.txt`, `Sample94.txt`,
  `Sample127.txt`.
- Analyzed 198 sorted CD4/CD8 T-cell RNA count samples from MS and normal
  pregnancy.

Result:
- The sorted T-cell cohort does **not** reproduce a broad MS late-pregnancy
  IFN/APC increase. MS `ifn_apc` third trimester versus before pregnancy:
  delta `0.08253030355335625`, Hedges g `0.11054038575480594`, Welch p
  `0.7472263368329753`.
- MS `mif_cd74_receptor_state` third trimester versus before pregnancy:
  delta `-0.1018077441858431`, Hedges g `-0.15327801999010318`, Welch p
  `0.6126888910327701`.
- The strongest MS T-cell kinetic signal is postpartum increase in the
  `trafficking_th` module versus third trimester: delta
  `0.3020256988998088`, Hedges g `0.5685553671142366`, Welch p
  `0.03795138383060487`.

Interpretation:
- This does not refute the GSE17410 PBMC result because E-MTAB-12260 lacks
  monocyte/APC fractions, but it argues against a pan-lymphocyte explanation.
- The pregnancy mechanism should be split into at least two compartments:
  peripheral APC/monocyte inflammatory state in PBMC and T-cell trafficking
  readiness around postpartum.

## V5 SLE Pregnancy Outcome Check: GSE108497

Analysis completed:
`results/pregnancy_dimension/gse108497_sle/REPORT.md`.

Data handling:
- Downloaded and validated `GSE108497_normalized_data.txt.gz`.
- Parsed platform `GPL10558` probe-to-gene symbols from the SOFT family file.
- Mapped 510 whole-blood array samples to pregnancy timepoint, SLE status,
  donor, batch, and pregnancy complication labels.

Result:
- In uncomplicated SLE pregnancies, HLA-II and MIF/CD74 trend down by late
  pregnancy and rebound postpartum. HLA-II postpartum versus 32-40 weeks:
  delta `0.45249907969308445`, Hedges g `0.5969596448077331`, Welch p
  `0.010299858620469296`; MIF/CD74 postpartum versus 32-40 weeks: delta
  `0.3058115266507866`, Hedges g `0.4111928986334141`, Welch p
  `0.07221679931479383`.
- In complicated SLE pregnancies, the same MIF/CD74 direction is reversed or
  blunted around late pregnancy: MIF/CD74 postpartum versus 32-40 weeks delta
  `-0.2722551595808476`, Hedges g `-0.37173253637682424`, Welch p
  `0.3100050506086394`.
- Uncomplicated SLE also shows a marked postpartum fall in `monocyte_cd64`
  versus 32-40 weeks: delta `-0.49523149353081186`, Hedges g
  `-0.8823987894426097`, Welch p `0.0005479290964762998`.

Interpretation:
- The pregnancy axis is disease- and outcome-specific. It is not a generic
  IFN/APC suppression model.
- A plausible V5 working model is kinetic uncoupling: protective pregnancy
  biology can reduce clinical inflammatory access to target tissue while
  peripheral immune modules prepare for postpartum rebound. The testable
  next step is whether MIF/CD74 stratifies the rebound-prone state in MS or
  instead belongs mainly to RA/SLE pregnancy biology.

## V5 GSE17410 Sensitivity Check

Analysis completed:
`results/pregnancy_dimension/gse17410_ms_sensitivity/REPORT.md`.

Reason:
The hostile critique correctly identified `GSE17410` as fragile: small
(`8` pre-pregnancy, `9` month-9), bulk PBMC, and two timepoints. V5 therefore
tested whether the MS month-9 IFN/APC signal survives component decomposition,
leave-one-out analysis, and marker-based composition residualization.

Result:
- Component decomposition shows the main signal is ISG-like, not CD74/HLA-II:
  `isg_only` month-9 versus pre delta `0.8662848708925912`, Hedges g
  `1.1650466279097202`, Welch p `0.02448853974034433`, FDR
  `0.07217826907245593`; `cd74_alone` delta `0.06085962069444406`, p
  `0.6696070367084628`; `hla_ii_without_cd74` delta
  `0.10172657772569593`, p `0.4898578270285561`.
- Leave-one-out does not kill the broad `ifn_apc` direction: minimum
  leave-one-out delta `0.5244798389255969`, maximum leave-one-out p
  `0.07691764159175278`.
- Blood-composition markers are also strongly shifted at month 9: erythroid
  delta `2.791872935925154`, p `0.009582015527605712`; platelet delta
  `0.8206577388359371`, p `0.043306961443473554`; neutrophil delta
  `0.3145609478083351`, p `0.02622644650507269`; pDC marker decreases
  (`-0.23162111368749905`, p `0.03844814819175888`).
- IFN/APC remains after monocyte-only residualization (delta
  `0.45484260574946556`, p `0.004113314623137636`) and monocyte+pDC
  residualization (delta `0.4103645639382041`, p `0.01106843658907962`), but
  is largely removed by all available composition markers: delta
  `0.09491044766501967`, Hedges g `0.4310631558347344`, p
  `0.37852840121224257`.

Interpretation:
- The original MS PBMC month-9 IFN/APC signal is robust to single-sample
  deletion but not robust to broad hematologic composition adjustment.
- It should no longer be interpreted as evidence for a specific APC/MIF/CD74
  late-priming mechanism.
- The remaining pregnancy-axis value is broader: pregnancy and postpartum are
  useful natural experiments that expose disease-specific immune kinetics, but
  the MS `GSE17410` PBMC signal is now best classified as a composition-
  confounded ISG/hematologic-shift observation unless an independent monocyte,
  serum, CSF, or postpartum MS dataset supports it.
