# MIF/CD74 Orthogonal Evidence Sidecar

Timestamp: 2026-05-28 20:29 CEST

Scope: local-only audit for MIF/CD74 stratification evidence beyond simple cross-sectional transcriptomics. I read `meta/ROADMAP_V5.md`, `knowledge/candidates/MIF_CD74_STRATIFICATION.md`, local pregnancy reports, treatment-response reports, foundation/perturbation summaries, genetics/druggability/prior-art tables, and relevant V3 sidecar notes. I did not use internet in this sidecar.

## Bottom Line

`MIF_CD74_STRATIFICATION` has enough orthogonal signal to justify the V5-mandated Tier 1 attempt, but not enough to advance to Tier 2 on current local evidence. The strongest positive channel is the pregnancy/natural-experiment axis in seropositive RA, where MIF/CD74-HLA-II/APC modules fall during pregnancy and rebound postpartum. The strongest MS-specific support remains a nominal residual white-matter microglia signal and a prior-art-compatible stratification rationale. The strongest negative constraint is that independent MS pregnancy T-cell RNA-seq does not reproduce a MIF/CD74 increase, and IBD anti-TNF response gives directionally conflicted baseline-versus-dynamic behavior.

Recommended Tier 1 decision after this scan: continue, but make the next analysis component-resolved and MS/progressive-MS-specific. Do not claim pan-autoimmune MIF/CD74 therapeutic dependency.

## Evidence Matrix

| Dimension | Local evidence | Direction for MIF/CD74 stratification | Strength |
|---|---|---:|---|
| Natural experiment: RA/SLE pregnancy | `GSE235508` and timecourse reports | Supports disease-specific kinetic APC/MIF-CD74 regulation, especially seropositive RA | moderate positive |
| Natural experiment: MS pregnancy PBMC | `GSE17410` report | Weak/non-significant MIF/CD74 rise; IFN/APC stronger than MIF/CD74 | weak mixed |
| Independent MS pregnancy T cells | `E-MTAB-12260` report | Does not support pan-lymphocyte MIF/CD74 pregnancy effect | negative/constraint |
| SLE pregnancy/postpartum | `GSE108497` report | MIF/CD74 signal differs by complication status and is not a clean SLE-wide axis | mixed/constraint |
| Treatment response | `GSE282122` anti-TNF IBD report | Conflicted: lower baseline predicts remission in one adjusted model, but remission increases post-treatment state | mixed negative |
| Perturbation/foundation | V3 Wave18 Geneformer/readout concordance | CD74 has model/readout support but recommendation is triage-only, not promotion-grade | weak supportive constraint |
| Druggability/prior art | V3 Wave39 and Galileo audit | CD74 is reachable/druggable/prior-art heavy; V4 contribution survives only as stratification | feasible but crowded |
| Genetics/coloc | V4 Tier 0 audit and Wave39 notes | No target-resolved coloc/MR support found locally | negative/absent |
| Failed-trial/post-hoc | Galileo audit | SPRINT-MS/ibudilast exists; no local receptor-state treatment-by-biomarker analysis | high-value gap |

## Traceable Evidence For

### 1. Natural Experiment: Seropositive RA Pregnancy Suppresses MIF/CD74 State

Files:
- `results/pregnancy_dimension/gse235508_modules/REPORT.md`
- `results/pregnancy_dimension/gse235508_timecourse/REPORT.md`
- `knowledge/candidates/PREGNANCY_REMISSION_AXIS.md`

Traceable numbers:
- In seropositive RA (`SPRA`), pregnancy versus nonpregnant/postpartum `mif_cd74_receptor_state`: delta `-0.4850522024358721`, Hedges g `-0.5860997928281567`, Welch p `0.006276097402756851`.
- `SPRA` `hla_ii_only`: delta `-0.5039563377463558`, p `0.009608482720167235`.
- `SPRA` `ifn_apc`: delta `-0.41565175202081406`, p `0.04384852719658707`.
- Timecourse in `SPRA` shows late-pregnancy trough and postpartum rebound:
  - `mif_cd74_receptor_state`: T3-T0 `-0.6424432741594277`, T4-T3 `0.5257536055434748`, T5-T3 `0.7805233800580105`, T6-T3 `1.1619638346454728`.
  - `hla_ii_only`: T3-T0 `-0.6457936633424115`, T6-T3 `1.3943411658318148`.
  - `ifn_apc`: T3-T0 `-0.5513304775594587`, T6-T3 `1.2666698095003408`.

Interpretation:
This is genuine orthogonal evidence because pregnancy is a natural experiment, not another case/control disease signature. It supports a kinetic APC/MIF-CD74 state in seropositive RA. It does not by itself support MS stratification.

### 2. MS Pregnancy PBMC: MIF/CD74 Is Directionally Higher But Not Significant

File:
- `results/pregnancy_dimension/gse17410_ms_modules/REPORT.md`

Traceable numbers:
- `mif_cd74_receptor_state`, month 9 versus pre-pregnancy: delta `0.12194807085829851`, Hedges g `0.6524448023335351`, Welch p `0.20974913196132225`.
- `hla_ii_only`: delta `0.10172657772569593`, p `0.4898578270285561`.
- `ifn_apc`: delta `0.6358630063022481`, Hedges g `1.0723962239804705`, p `0.03686721892111262`.

Interpretation:
This supports the V5 pregnancy inconsistency but does not directly support MIF/CD74. The stronger signal is IFN/APC, not MIF/CD74. MIF/CD74 cannot be promoted from this dataset without component resolution and independent validation.

### 3. Independent MS Pregnancy T Cells: No MIF/CD74 Replication

File:
- `results/pregnancy_dimension/emt12260_ms_tcells/REPORT.md`

Traceable numbers:
- MS sorted T cells, `mif_cd74_receptor_state`, 3rd trimester versus before pregnancy: delta `-0.1018077441858431`, Hedges g `-0.15327801999010318`, Welch p `0.6126888910327701`.
- MS sorted T cells, postpartum versus 3rd trimester: delta `-0.08376121051502036`, Hedges g `-0.13578698209258053`, Welch p `0.6108469491965408`.
- Adjusted OLS, 3rd trimester term for `mif_cd74_receptor_state`: coef `-0.13814738321710288`, p `0.6569105661962384`.
- Adjusted OLS, postpartum term for `mif_cd74_receptor_state`: coef `-0.22313938452244758`, p `0.28589633708574114`.
- `trafficking_th` postpartum versus 3rd trimester is the only notable unadjusted MS contrast listed: delta `0.3020256988998088`, Hedges g `0.5685553671142366`, p `0.03795138383060487`.

Interpretation:
This argues against a pan-lymphocyte MIF/CD74 explanation for the MS PBMC month-9 result. If MIF/CD74 matters in MS pregnancy/postpartum, it is more likely monocyte/APC, CSF, lesion, or compartment-specific rather than sorted T-cell-intrinsic.

### 4. SLE Pregnancy: MIF/CD74 Is Not a Clean Uniform Axis

File:
- `results/pregnancy_dimension/gse108497_sle/REPORT.md`

Traceable numbers:
- Uncomplicated SLE, `mif_cd74_receptor_state`, 32-40 weeks versus <16 weeks: delta `-0.20332580116827784`, Hedges g `-0.25881154237917464`, p `0.22910979600797657`.
- Uncomplicated SLE, 8-20 weeks postpartum versus 32-40 weeks: delta `0.3058115266507866`, Hedges g `0.4111928986334141`, p `0.07221679931479383`.
- Complicated SLE, 32-40 weeks versus <16 weeks: delta `0.27474571161497024`, Hedges g `0.3438052982085321`, p `0.19887004956188656`.
- Complicated SLE, postpartum versus 32-40 weeks: delta `-0.2722551595808476`, p `0.3100050506086394`.
- Covariate-adjusted SLE timepoint terms for `mif_cd74_receptor_state` are not significant; TP5 coefficient `0.029974799610341468`, p `0.7996798384039162`.

Interpretation:
SLE is a useful comparator but not a clean MIF/CD74-supporting disease here. The direction appears complication-dependent and weaker than HLA-II/monocyte/regulatory modules.

### 5. MS-Specific Residual Evidence Is Nominal, Not FDR-Stable

Files:
- `analysis/tier_0_triage/mif_cd74_stratification/REPORT.md`
- `knowledge/candidates/MIF_CD74_STRATIFICATION.md`

Traceable numbers:
- MS white-matter residual delta `0.45572407980566854`.
- Hedges g `1.247930189567055`.
- p `0.007887505384977308`.
- FDR `0.4417003015587293`.
- No `mif_cd74_receptor_state` residual test survives FDR `<=0.10`.

Interpretation:
This is the core reason the candidate was parked in V4. Under V5 it justifies a Tier 1 attempt because it repeatedly reappears, but it cannot support a claim by itself.

### 6. Treatment Response: IBD Anti-TNF Is Conflicted

Files:
- `analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/REPORT.md`
- `analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/mif_cd74_remission_interaction.tsv`
- `analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/mif_cd74_baseline_predictive.tsv`

Traceable numbers:
- Major monocyte/macrophage remission is associated with larger post-treatment `mif_cd74_receptor_state` increase: adjusted delta `0.4840720173619233`, adjusted p `0.03473492719224309`.
- Major DC same direction but not significant: adjusted delta `0.1954004175949041`, adjusted p `0.21222452353534355`.
- Lower baseline monocyte/macrophage `mif_cd74_receptor_state` predicts remission in one adjusted model: logit coefficient `-4.088480806349443`, p `0.009857151903175113`.
- Raw baseline remission-versus-nonremission difference is not significant: Hedges g `-0.38734765558900636`, p `0.22965575235386465`.

Interpretation:
This is not a positive treatment-response channel for MIF/CD74 inhibition. It does support a stratification question: baseline state and pharmacodynamic state may have opposite meanings. Any V5 MIF/CD74 claim must explicitly separate baseline risk/enrichment from on-treatment response-state remodeling.

### 7. Perturbation/Foundation: CD74 Has Triage-Grade Model Support, Not Promotion-Grade Support

Files:
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave18_foundation_rescue/readout_concordance_by_candidate.tsv`
- `results_v3/wave18_foundation_rescue/readout_concordance_detail.tsv`

Traceable numbers:
- In `foundation_rescue_candidate_rank.tsv`, `CD74` has `total_support_contexts` `2`, `total_strong_support_contexts` `1`, `total_disease_cells_with_token` `247`, `best_context_cosine_z` `2.184406319356157`, and `best_context_projection_minus_random` `0.1334118285468625`.
- Best Geneformer source/context: `broad_residual_delete`, `IBD_epithelial`.
- Best direct readout source: `GSE162464_mouse_macrophage_RNAseq`, perturbation `Med16_IFNg_vs_NTC_IFNg`, readout min log2FC `-2.459210478390288`.
- Foundation recommendation: `triage_only_gse162463_not_promotion_grade`.
- Readout concordance for CD74 includes `GSE162464_mouse_macrophage_RNAseq`, `GSE294918_human_ruxolitinib`, and `Mixscale_GSE281048`.

Interpretation:
This supports CD74 as a responsive antigen-presentation-state readout, not as a validated intervention node. The best perturbation evidence is upstream IFN/Mediator/JAK-style modulation, which risks collapsing into generic HLA-II/IFN biology.

### 8. Druggability And Prior Art: Feasible But Crowded

Files:
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/chembl_druggability.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/clinicaltrials_prior_counts.tsv`
- `subagents_v3/cd74_mif_novelty_galileo_report.md`

Traceable numbers and local claims:
- CD74 ChEMBL target found as `CHEMBL4692`; local table lists `25` ChEMBL activity records.
- CD74 location/features include cell membrane, endosome, late endosome, lysosome, and secreted annotations.
- CD74 surfaceome rescue call is `NO_GO_SURFACEOME_RESCUE`, but reason includes state-positive-control/druggability facts: reachable protein class, ChEMBL exact target found, and Wave15 residual state support in 8 diseases.
- Local clinicaltrials prior count for `CD74 autoimmune`: `4`, including `NCT01845740` milatuzumab in SLE.
- Galileo audit records SPRINT-MS/ibudilast `NCT01982942`, 255 randomized, 96 weeks, and prior-art documents including `US11083713B2`, `WO2007142924A1`, `CA3174413A1` / `WO2021207054`, `US10525101B2`, and `US9643922B2`.

Interpretation:
V4 prior-art rules mean this is not a binary kill. The surviving contribution must be new subgroup/biomarker/mechanism specificity, not “MIF/CD74 modulation for progressive MS” broadly.

## Evidence Against Or Gaps

1. No local target-resolved genetic anchor.
   - `knowledge/candidates/MIF_CD74_STRATIFICATION.md` and Wave39 notes state no target-resolved coloc/MR support; surfaceome table explicitly records “no_target_resolved_coloc_or_mr” in the prior demotion text.

2. MS natural-experiment evidence is not MIF/CD74-specific.
   - `GSE17410` supports IFN/APC month-9 increase more strongly than MIF/CD74.
   - `E-MTAB-12260` sorted T cells do not replicate a MIF/CD74 rise.

3. Treatment-response direction is conflicted.
   - In IBD anti-TNF, lower baseline MIF/CD74 may predict remission in one adjusted model, but remission increases post-treatment MIF/CD74 state. This could mean repair/remodeling, residual inflammation, cell-composition shift, or model confounding.

4. Perturbation support is mostly upstream and non-selective.
   - CD74 suppression is observed with IFN/JAK/Mediator perturbation contexts, but that does not prove MIF/CD74-axis blockade is the right therapeutic direction.

5. Prior art occupies broad MIF/CD74 progressive-MS use.
   - Any V5 program centered on ibudilast without receptor-state enrichment would likely be non-novel locally.

## Recommended Next Analysis

1. Run component-resolved MIF/CD74 analysis in all local pregnancy outputs:
   - `CD74` alone
   - `CD74/CD44/CXCR4` receptor-only score
   - `HLA-II-only`
   - full `mif_cd74_receptor_state`
   - `ifn_apc` residualized component

2. Apply this first to:
   - `GSE17410` PBMC MS pregnancy
   - `E-MTAB-12260` sorted MS T cells, as a negative/compartment control
   - `GSE235508` SPRA/SNRA/SLE/healthy timecourse
   - `GSE108497` SLE with complication status

3. For MS-specific Tier 1, prioritize progressive-MS or SPRINT-MS-accessible biomarker search:
   - Local query to run before internet: RAG query for `SPRINT-MS CD74 MIF receptor state serum CSF lesion ibudilast biomarker`.
   - If internet is allowed later, use search queries rather than asserting:
     - `SPRINT-MS CD74 CD44 CXCR4 biomarker ibudilast`
     - `NCT01982942 CD74 MIF serum CSF biomarker brain atrophy`
     - `progressive multiple sclerosis CD74 CD44 CXCR4 lesion microglia`

4. Treat IBD anti-TNF as a hostile-control channel:
   - Refit the GSE282122 baseline/remission model with component-resolved scores and cell-composition/donor controls.
   - Explicitly test whether the baseline effect is driven by HLA-II-only or receptor-only components.

5. Tier 1 pass/fail rule I recommend:
   - Pass to Tier 2 only if receptor-only (`CD74/CD44/CXCR4`) or CD74-specific residual, not HLA-II-only, shows an MS/progressive-MS or pregnancy/postpartum-relevant association and at least one treatment/perturbation channel gives directionally coherent support.
   - Demote if component resolution shows the whole signal is generic IFN/HLA-II APC state or if treatment-response remains directionally irreconcilable.

## Sidecar Verdict

`MIF_CD74_STRATIFICATION` should remain active in V5 Tier 1, but the evidence standard should tighten around component resolution and MS-specific treatment-by-biomarker interaction. The current orthogonal evidence supports “candidate worth a decisive Tier 1 test,” not “candidate ready for Tier 2.”
