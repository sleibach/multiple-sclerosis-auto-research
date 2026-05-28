# V6 Pregnancy Generativity Sidecar

Timestamp: 2026-05-28  
Scope: Tier -1 refinements of the MS/RA/SLE pregnancy axis. Local-only scan; no internet used. Inputs read: `meta/TIER_MINUS_1_RULEBOOK.md`, `meta/ROADMAP_V6.md`, `knowledge/hypotheses/HYP_V6_001_MS_PREGNANCY_ERYTHROID_PLATELET_AXIS.md`, `HYP_V6_002_PDC_DEPLETION_ISG_SOURCE_SWITCH.md`, `HYP_V6_003_POSTPARTUM_TCELL_TRAFFICKING.md`, `HYP_V6_007_SLE_PREGNANCY_HLAII_CD64_DECOUPLING.md`, pregnancy reports under `results/pregnancy_dimension/`, and local pregnancy hostile critique/status files.

## Operating Frame

Tier -1 should not rescue the old broad claim that pregnancy uniformly suppresses APC/HLA-II biology. The useful V6 move is to split the pregnancy axis into compartment-specific, time-specific hypotheses that are weak but concrete enough for Tier 0 tests.

The key local constraint is now clear:

- `GSE17410` MS month-9 PBMC IFN/APC signal is robust to leave-one-out but composition-confounded.
- `E-MTAB-12260` sorted MS T cells do not reproduce late-pregnancy IFN/APC or MIF/CD74 activation, but show a postpartum trafficking signal.
- `GSE235508` seropositive RA shows late-pregnancy APC/HLA-II trough and postpartum rebound.
- `GSE108497` SLE shows outcome-dependent HLA-II/CD64 decoupling.

## Candidate Tier -1 Hypotheses

### HYP-PREG-A: MS Late-Pregnancy Hematologic-ISG Composite

Refinement of `HYP_V6_001` and `HYP_V6_002`.

Hypothesis:
In `GSE17410`, MS month-9 pregnancy is not primarily an APC/MIF-CD74 activation state. It is a hematologic-shift state in which erythroid, platelet, and neutrophil signals co-occur with ISG induction, producing an apparent IFN/APC module increase in bulk PBMC.

Opening evidence:
- `results/pregnancy_dimension/gse17410_ms_sensitivity/REPORT.md`
- `ifn_apc` month-9 versus pre: delta `0.6358630063022481`, Hedges g `1.0723962239804705`, p `0.03686721892111262`, FDR `0.07217826907245593`.
- Leave-one-out does not remove direction: minimum delta `0.5244798389255969`, maximum p `0.07691764159175278`.
- Composition markers are large: erythroid delta `2.791872935925154`, p `0.009582015527605712`; platelet delta `0.8206577388359371`, p `0.043306961443473554`; neutrophil delta `0.3145609478083351`, p `0.02622644650507269`.
- All available composition residualization reduces `ifn_apc` to delta `0.09491044766501967`, p `0.37852840121224257`.

Interpretation:
The signal is not a single-sample artifact, but it is probably not cell-intrinsic APC activation. Tier -1 should treat the adjusted-away variables as biology: pregnancy hematology, coagulation/endothelial activation, neutrophil/platelet immune crosstalk, or sample fraction changes.

Public datasets to test:
- `GSE17410` and metadata/superseries `GSE17449`: reprocess raw arrays if possible; inspect sample-level metadata for relapse, infection, steroid, DMT washout, collection date.
- `GSE235508`: test whether erythroid/platelet/neutrophil modules track RA/SLE timepoints and whether they explain APC/HLA-II trough/rebound.
- `GSE108497`: test whether uncomplicated versus complicated SLE differs in hematologic residuals.
- `E-MTAB-12260`: negative control, because sorted T cells should not carry erythroid/platelet composition signal.

Tier 0 promotion criteria:
- Promote if an independent pregnancy dataset shows the same hematologic-ISG composite with absolute Hedges g `>0.5` or uncorrected p `<0.10`, and the effect is not present in sorted T-cell negative controls.
- Do not promote if erythroid/platelet signal tracks only assay/platform artifacts or sample quality surrogates, or if RA/SLE whole-blood datasets show no comparable hematologic coupling.

First analysis:
Run a shared hematologic module panel across `GSE235508`, `GSE108497`, `GSE17410`, and `E-MTAB-12260`; test whether hematologic modules absorb IFN/APC or ISG signals in each dataset.

### HYP-PREG-B: pDC-Depletion With Non-pDC ISG Source Switch

Refinement of `HYP_V6_002`.

Hypothesis:
MS month-9 PBMCs show higher ISG expression despite lower pDC-marker signal because interferon response is being carried by non-pDC compartments or by recent exposure to interferon rather than increased pDC abundance.

Opening evidence:
- `results/pregnancy_dimension/gse17410_ms_sensitivity/REPORT.md`
- `isg_only` month-9 versus pre: delta `0.8662848708925912`, Hedges g `1.1650466279097202`, p `0.02448853974034433`.
- `pdc_marker`: delta `-0.23162111368749905`, Hedges g `-1.042671101753469`, p `0.03844814819175888`.
- `isg_only` remains after monocyte-only residualization: delta `0.6426874967498273`, p `0.0030739757020159693`.
- `isg_only` remains after monocyte+pDC residualization: delta `0.529175750890881`, p `0.01689510168813591`.
- `isg_only` is largely reduced after all available composition residualization: delta `0.12676088484014358`, p `0.40497182678966404`.

Interpretation:
This is a source-switch hypothesis, not proof of active interferon production. Candidate sources include neutrophils, monocytes, platelets/megakaryocyte contamination, endothelial-associated transcripts, infection exposure, or pDC egress from blood into tissue.

Public datasets to test:
- `GSE235508`: if single-cell or cell-type-adjusted files are locally accessible, test cell-type source of ISGs across RA/SLE/healthy pregnancy.
- `GSE108497`: whole-blood comparator with SLE and postpartum timepoints; test whether pDC marker and ISG module anticorrelate by complication group.
- Search query only if external discovery is later allowed: `multiple sclerosis pregnancy postpartum plasmacytoid dendritic cell interferon GEO`, `MS pregnancy serum interferon pDC postpartum relapse dataset`, `pregnancy pDC interferon single cell RNA-seq GEO`.

Tier 0 promotion criteria:
- Promote if at least one independent pregnancy/postpartum dataset shows ISG up with pDC markers down or unchanged, and source inference implicates non-pDC cells.
- Demote if the ISG/pDC anticorrelation disappears after raw-data reprocessing or is explained by a single probe/sample-quality component.

First analysis:
Create pDC, monocyte, neutrophil, platelet, ISG-I, ISG-II, and infection-response modules; compute partial correlations and residual contrasts by timepoint in `GSE235508` and `GSE108497`.

### HYP-PREG-C: Postpartum T-Cell Trafficking Readiness, Not T-Cell Activation

Refinement of `HYP_V6_003`.

Hypothesis:
In MS pregnancy, postpartum relapse susceptibility may involve restoration of T-cell CNS-trafficking readiness after delivery, while late-pregnancy T-cell IFN/APC activation remains absent or suppressed.

Opening evidence:
- `results/pregnancy_dimension/emt12260_ms_tcells/REPORT.md`
- `E-MTAB-12260` sorted MS T cells, `ifn_apc` third trimester versus before pregnancy: delta `0.08253030355335625`, p `0.7472263368329753`.
- `mif_cd74_receptor_state` third trimester versus before pregnancy: delta `-0.1018077441858431`, p `0.6126888910327701`.
- `trafficking_th` postpartum versus third trimester: delta `0.3020256988998088`, Hedges g `0.5685553671142366`, p `0.03795138383060487`.
- Covariate-adjusted OLS for trafficking postpartum term is not significant: coef `0.1025975624501005`, p `0.5331099978193317`, so this remains Tier -1 only.

Interpretation:
This is the cleanest way to integrate the independent MS T-cell dataset: it is negative for activation, weakly positive for postpartum trafficking. This refines rather than validates the PBMC IFN/APC story.

Public datasets to test:
- `E-MTAB-12260`: stratify by CD4/CD8 and activated/resting, then FDR-correct trafficking contrasts.
- `GSE122894`: pregnant versus nonpregnant EAE TCR-beta repertoire in Tcon/Treg; use as cross-species immune-repertoire comparator for T-cell state/trafficking readiness, not direct human validation.
- `GSE153459`: healthy pregnancy CD4 methylation by trimester; test whether trafficking loci or migration-related methylation changes reverse postpartum if postpartum exists.
- Search query if external discovery is later allowed: `multiple sclerosis postpartum relapse T cell trafficking transcriptomics`, `multiple sclerosis pregnancy postpartum TCR repertoire`, `MS pregnancy postpartum chemokine CXCR3 CCR6 S1PR1`.

Tier 0 promotion criteria:
- Promote if postpartum trafficking module is positive in MS T cells after donor/cell-type/stimulus adjustment or replicates in another MS/postpartum immune dataset.
- Promote if cross-species EAE pregnancy data shows convergent T-cell trafficking/repertoire readiness consistent with human postpartum signal.
- Do not promote if the signal is confined to unadjusted pooled T-cell contrasts and disappears in CD4/CD8 or donor-stratified analysis.

First analysis:
Re-run `E-MTAB-12260` with trafficking submodules: CNS-homing (`ITGA4`, `CXCR3`), Th17/CCR6, lymph-node egress (`S1PR1`, `SELL`, `CCR7`), activation-independent motility/cytoskeleton. Report CD4/CD8 and activated/resting separately.

### HYP-PREG-D: RA Pregnancy APC Trough/Postpartum Release Is Seropositive-RA Specific

Refinement from `GSE235508` rather than currently registered hypotheses.

Hypothesis:
Seropositive RA remission biology during pregnancy is an APC/HLA-II trough followed by postpartum release, and this kinetic module is not shared by seronegative RA or by MS PBMC.

Opening evidence:
- `results/pregnancy_dimension/gse235508_modules/REPORT.md`
- `results/pregnancy_dimension/gse235508_timecourse/REPORT.md`
- `SPRA` pregnancy versus nonpregnant/postpartum `mif_cd74_receptor_state`: delta `-0.4850522024358721`, Hedges g `-0.5860997928281567`, p `0.006276097402756851`.
- `SPRA` late-pregnancy trough/postpartum rebound:
  - `mif_cd74_receptor_state`: T3-T0 `-0.6424432741594277`, T6-T3 `1.1619638346454728`.
  - `hla_ii_only`: T3-T0 `-0.6457936633424115`, T6-T3 `1.3943411658318148`.
  - `ifn_apc`: T3-T0 `-0.5513304775594587`, T6-T3 `1.2666698095003408`.

Interpretation:
This is likely a real pregnancy natural-experiment signal, but it should be kept separate from MS. It may become a Tier 0 RA postpartum flare/serostatus hypothesis even if the MS branch fails.

Public datasets to test:
- `GSE235508`: confirm exact timepoint labels from source metadata and stratify by seropositive/seronegative RA.
- Search query if needed: `rheumatoid arthritis pregnancy postpartum transcriptome seropositive GEO`, `RA pregnancy postpartum flare PBMC RNA-seq`, `rheumatoid arthritis pregnancy HLA class II postpartum`.

Tier 0 promotion criteria:
- Promote if timepoint labels are verified and the SPRA APC/HLA-II trough/rebound survives cell-composition or available deconvolution controls.
- Promote if another RA pregnancy/postpartum dataset reproduces the direction or if postpartum flare association exists in `GSE235508` metadata.
- Do not promote as pan-autoimmune unless MS and SLE harmonized analyses agree, which they currently do not.

First analysis:
Run `GSE235508` with component and composition panels from `GSE17410` sensitivity: HLA-II-only, CD74-only, receptor-only, ISG-only, monocyte, pDC, neutrophil, platelet, erythroid.

### HYP-PREG-E: SLE HLA-II Restoration / CD64 Inflammatory Deactivation Decoupling

Refinement of `HYP_V6_007`.

Hypothesis:
Uncomplicated SLE pregnancy/postpartum shows a decoupled postpartum transition: antigen-presentation modules rebound while CD64 inflammatory activation falls. Complicated SLE blunts or reverses this coupling, suggesting pregnancy outcome state rather than SLE diagnosis alone determines immune kinetics.

Opening evidence:
- `results/pregnancy_dimension/gse108497_sle/REPORT.md`
- Uncomplicated SLE, HLA-II postpartum versus 32-40 weeks: delta `0.45249907969308445`, Hedges g `0.5969596448077331`, p `0.010299858620469296`.
- Uncomplicated SLE, MIF/CD74 postpartum versus 32-40 weeks: delta `0.3058115266507866`, Hedges g `0.4111928986334141`, p `0.07221679931479383`.
- Uncomplicated SLE, monocyte CD64 postpartum fall: delta `-0.49523149353081186`, Hedges g `-0.8823987894426097`, p `0.0005479290964762998`.
- Complicated SLE: HLA-II postpartum versus 32-40 weeks delta `-0.47281608821760407`, p `0.07808896442031851`; MIF/CD74 delta `-0.2722551595808476`, p `0.3100050506086394`.

Interpretation:
This is not simply “SLE IFN high.” It suggests separable antigen-presentation restoration and Fc-receptor inflammatory deactivation. It could distinguish physiologic postpartum immune normalization from complication-associated immune pathology.

Public datasets to test:
- `GSE235508`: test whether SLE has matching or opposite HLA-II/CD64 decoupling under the same time bins.
- `GSE108497`: primary dataset; analyze healthy controls and complication strata with donor-clustered models.
- Search query if needed: `SLE pregnancy postpartum CD64 HLA class II transcriptome GEO`, `lupus pregnancy complications postpartum monocyte CD64 HLA-DR`.

Tier 0 promotion criteria:
- Promote if `GSE235508` reproduces HLA-II up / CD64 down around postpartum in uncomplicated SLE or healthy pregnancy.
- Promote if decoupling distinguishes complicated from uncomplicated pregnancies with interaction p `<0.10` or absolute interaction effect `>0.5` SD.
- Do not promote if the pattern disappears under donor-clustered modeling or if time-bin harmonization flips direction.

First analysis:
Define a decoupling score: z(`hla_ii_only`) minus z(`monocyte_cd64`). Test late-pregnancy-to-postpartum change and complication interaction in `GSE108497`, then replicate in `GSE235508`.

### HYP-PREG-F: MS PBMC Signal Is Pregnancy-Hematology Plus Antiviral Exposure, Not Disease Remission Biology

Refinement integrating the hostile critique.

Hypothesis:
The `GSE17410` MS month-9 IFN/APC increase reflects pregnancy hematology and transient antiviral/infection-like exposure rather than a mechanism explaining MS remission or postpartum relapse.

Opening evidence:
- Strong ISG-only signal with pDC marker decrease.
- All-composition residualization removes most IFN/APC.
- No subject-level relapse, infection, steroid, DMT, breastfeeding, or postpartum outcome linkage is currently available locally.
- Independent sorted T-cell dataset is negative for late-pregnancy activation.

Interpretation:
This is a necessary null-generating hypothesis. Tier -1 should explicitly test it because killing the overinterpreted MS branch would improve the project.

Public datasets to test:
- `GSE17410` / `GSE17449`: metadata and raw reprocessing.
- Any public MS pregnancy serum/flow/cytokine/postpartum cohort discovered later. Search queries to use if internet is allowed:
  - `GSE multiple sclerosis pregnancy postpartum cytokine`
  - `ArrayExpress multiple sclerosis pregnancy postpartum PBMC`
  - `multiple sclerosis pregnancy postpartum serum neurofilament cytokine dataset`
  - `PROXIMUS multiple sclerosis pregnancy postpartum transcriptome`

Tier 0 promotion criteria:
- Promote as a negative Tier 0 mechanism-class test if raw reprocessing confirms the signal but independent MS/postpartum datasets fail to show immune rebound and metadata suggests composition/infection confounding.
- Promote a positive branch only if independent MS data show matching non-pDC ISG/hematologic signal before postpartum clinical activity.

First analysis:
Retrieve or parse `GSE17410` original sample annotations and related publication supplements locally if already downloaded; otherwise queue accession/publication discovery.

## Cross-Hypothesis Test Matrix

| Test | HYP-A | HYP-B | HYP-C | HYP-D | HYP-E | HYP-F |
|---|---:|---:|---:|---:|---:|---:|
| `GSE17410` raw/reprocessed arrays | primary | primary | no | no | no | primary |
| `GSE235508` harmonized time bins | support/contrast | support | weak | primary | replication | contrast |
| `GSE108497` complication-aware model | support/contrast | support | no | no | primary | contrast |
| `E-MTAB-12260` CD4/CD8 stratified | negative control | negative control | primary | no | no | negative control |
| `GSE122894` EAE TCR repertoire | no | no | cross-species support | no | no | no |
| `GSE153459` healthy CD4 methylation | no | no | hormonal reference | no | comparator | no |

## Public Dataset Queue

Locally identified and immediately actionable:
- `GSE17410`: MS PBMC pre-pregnancy versus ninth month.
- `GSE17449`: MS pregnancy-related superseries; likely metadata/support for `GSE17410`, independence must be verified.
- `E-MTAB-12260`: MS/healthy sorted CD4/CD8 T-cell RNA-seq across pregnancy/postpartum.
- `GSE235508`: RA/SLE/healthy longitudinal pregnancy blood RNA-seq and related outputs.
- `GSE108497`: SLE/healthy pregnancy/postpartum whole-blood Illumina array with complication labels.
- `GSE153459`: healthy pregnancy CD4 methylation reference.
- `GSE122894`: pregnant versus nonpregnant EAE TCR-beta repertoire.

Discovery queries to run only if internet is needed:
- `multiple sclerosis pregnancy postpartum transcriptomics GEO`
- `multiple sclerosis pregnancy postpartum serum cytokine dataset`
- `multiple sclerosis pregnancy pDC interferon PBMC`
- `rheumatoid arthritis pregnancy postpartum transcriptome seropositive`
- `SLE pregnancy postpartum CD64 HLA-DR transcriptome GEO`
- `pregnancy autoimmune postpartum flare single cell RNA-seq`

## Recommended Tier -1 Prioritization

1. Highest priority: HYP-PREG-A and HYP-PREG-B together. They directly explain the composition-confounded MS month-9 IFN/APC result and produce falsifiable alternatives.
2. Second priority: HYP-PREG-C. It is the only independent MS pregnancy signal that is not just a refutation, but it needs donor/cell-type adjusted survival.
3. Third priority: HYP-PREG-E. SLE HLA-II/CD64 decoupling is mechanistically interesting and has a clear replication target in `GSE235508`.
4. Keep HYP-PREG-D as RA-specific unless another disease reproduces the APC trough/rebound under harmonized bins.
5. Keep HYP-PREG-F as the necessary skeptical branch; a rigorous negative result here would prevent further overfitting to `GSE17410`.

## Promotion Summary

No pregnancy hypothesis here is currently Tier 0-ready as a therapeutic claim. Several are Tier 0-ready as analysis questions. The first promotion attempt should be:

> Does a hematologic-ISG composite, rather than APC/MIF-CD74 activation, explain MS month-9 PBMC IFN/APC and reproduce as a pregnancy/postpartum immune kinetic axis in RA/SLE whole-blood cohorts while remaining absent in sorted MS T cells?

Pass criteria: independent support in `GSE235508` or `GSE108497`, negative-control absence in `E-MTAB-12260`, and explicit decomposition showing which component carries the signal.
