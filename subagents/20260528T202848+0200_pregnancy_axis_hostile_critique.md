# Pregnancy Axis Hostile Critique

Timestamp: 2026-05-28T20:28:48+0200  
Role: V5 hostile critique sidecar  
Scope: current interpretation that MS PBMC month-9 IFN/APC up despite clinical pregnancy remission reflects late peripheral priming / postpartum kinetic divergence.

## Bottom Line

The current interpretation is plausible but not yet strong. The strongest hostile reading is simpler: the MS signal may be a small, old, bulk-PBMC, two-timepoint artifact that does not replicate in the independent MS pregnancy T-cell cohort, while the RA and SLE comparators are different diseases, assays, tissues, time grids, and clinical states. The kinetic-divergence model should remain a working hypothesis only if it survives composition correction, timepoint-label verification, independent MS replication, and module deconstruction.

## Main Attacks

### 1. The central MS result rests on `GSE17410`, and `GSE17410` is fragile

The MS month-9 IFN/APC increase is based on 8 pre-pregnancy and 9 month-9 PBMC array samples. The reported `ifn_apc` contrast is large (`delta 0.6358630063022481`, Hedges g `1.0723962239804705`, Welch p `0.03686721892111262`), but this is an uncorrected Tier 0 module result from a small bulk dataset.

What could be wrong:

- One or two high-IFN month-9 samples could drive the effect.
- Pre-pregnancy samples may not be comparable to month-9 samples if treatment withdrawal, infection, steroid exposure, relapse proximity, or sampling season differs.
- PBMC composition can create an apparent IFN/APC signal without any per-cell transcriptional activation.
- The module combines interferon genes with antigen-presentation/APC genes, so the effect could be pure ISG induction, pure monocyte fraction shift, or probe/platform behavior.

Concrete fixes:

- Add leave-one-out and robust regression sensitivity for `GSE17410`.
- Plot per-sample module values with sample IDs, not only group means.
- Run component-separated modules: ISG-only, HLA-II-only, CD74-only, monocyte markers, plasmacytoid dendritic markers, neutrophil contamination markers.
- Reprocess raw CEL files if available and compare against the current SOFT VALUE table.
- Test whether housekeeping/RIN-like surrogate PCs or batch-associated probes explain the module.

Kill criterion:

- If leave-one-out removes the direction or if ISG-only/monocyte-composition controls absorb the effect, the late-priming mechanism should be downgraded to a single-study artifact.

### 2. Independent MS validation is currently negative or weak

`E-MTAB-12260` is the best independent MS pregnancy omics dataset found so far. It does not reproduce a broad late-pregnancy inflammatory increase in sorted T cells. In MS samples, the `ifn_apc` 3rd-trimester versus before-pregnancy contrast is small and null (`delta 0.08253030355335625`, p `0.7472263368329753`). Covariate-adjusted 3rd-trimester IFN/APC is also null (`coef 0.07763195300970843`, p `0.7330877956715298`). Postpartum-versus-3rd-trimester `trafficking_th` is the only notable reported MS contrast (`delta 0.3020256988998088`, p `0.03795138383060487`), and even this is not yet multiple-testing corrected.

The current report says a T-cell null does not refute a monocyte/APC PBMC mechanism. That is fair, but it also means `E-MTAB-12260` cannot be counted as positive independent validation of the MS PBMC IFN/APC claim.

Concrete fixes:

- Treat `E-MTAB-12260` as negative for a pan-lymphocyte late-pregnancy IFN/APC mechanism.
- Use it to refine the model: if late priming exists, it should be monocyte/DC/pDC-biased, not generic T-cell activation.
- Test T-cell trafficking and activation separately, because the only suggestive independent signal is postpartum trafficking.

Kill criterion:

- If no independent monocyte, serum IFN, cytokine, or postpartum MS dataset supports late pregnancy or postpartum peripheral priming, the MS kinetic-divergence claim should not advance beyond Tier 1.

### 3. Cross-disease comparability is poor

The current narrative compares:

- MS PBMC array, pre-pregnancy versus month 9 (`GSE17410`);
- RA/SLE whole-blood RNA-seq, multiple pregnancy/postpartum timepoints (`GSE235508`);
- SLE whole-blood Illumina array, gestational intervals and postpartum (`GSE108497`);
- MS sorted T-cell RNA-seq (`E-MTAB-12260`).

These datasets differ in platform, sample processing, cell mixture, disease, medication history, timepoint definitions, and clinical phenotype. A shared word like "late pregnancy" does not make the contrasts biologically equivalent.

Specific problem:

- The RA `GSE235508` trajectory has late-pregnancy trough and postpartum rebound, but `GSE108497` SLE uncomplicated pregnancies show HLA-II down late and up postpartum while monocyte CD64 falls postpartum. This does not cleanly match the earlier `GSE235508` SLE interpretation of late-pregnancy IFN/APC-like rise and postpartum fall.
- The SLE result is complication-stratified and sensitive to whether the analysis uses raw group contrasts or OLS over all SLE samples.

Concrete fixes:

- Standardize time bins across datasets before biological interpretation: pre, early, mid, late, 6-12 week postpartum, 6 month postpartum, 12 month postpartum.
- Analyze controls and disease cohorts within each dataset using the same module definitions and contrast templates.
- Avoid saying "SLE-like" for the MS month-9 state until SLE signals are consistent across `GSE235508` and `GSE108497` under identical module and time-bin definitions.

Kill criterion:

- If SLE direction flips depending on dataset or model specification, it cannot be used as a mechanistic analog for MS late-pregnancy priming.

### 4. Module validity is not yet adequate for mechanism claims

The `ifn_apc` module name embeds a mechanistic interpretation. It may be a mixture of:

- type I/II interferon signaling;
- HLA-II antigen presentation;
- CD74/MIF receptor state;
- monocyte abundance;
- pDC abundance;
- infection response;
- platelet/leukocyte mixture artifacts;
- pregnancy hematology shifts.

The `mif_cd74_receptor_state` and `hla_ii_only` modules are more interpretable than the broad `ifn_apc` module, but the central MS finding is strongest in `ifn_apc`, not in MIF/CD74 or HLA-II. In `GSE17410`, `mif_cd74_receptor_state` is only directional and nonsignificant (`delta 0.12194807085829851`, p `0.20974913196132225`).

Concrete fixes:

- Decompose every reported module into submodules and single-gene loadings.
- Report gene coverage per dataset beside each effect; do not compare module scores if gene coverage differs materially.
- Use deconvolution or marker residualization before interpreting cell-state activation in whole blood/PBMC.
- Add negative-control modules: erythroid, platelet, neutrophil, cell-cycle, mitochondrial/ribosomal, pregnancy hormone response.

Kill criterion:

- If the MS effect is carried by a generic ISG or composition signal rather than APC/CD74/HLA-II components, it cannot support the MIF/CD74/postpartum-flare therapeutic path.

### 5. Clinical remission is being treated too coarsely

The model assumes clinical MS activity decreases during pregnancy while PBMC IFN/APC rises. But the data being analyzed do not directly link the assayed samples to relapse status, MRI activity, postpartum flare, treatment withdrawal, breastfeeding, or steroid exposure.

Without subject-level clinical linkage, "PBMC priming despite clinical remission" is an ecological contrast: population-level MS pregnancy epidemiology is being overlaid on an old transcriptomic cohort.

Concrete fixes:

- Search specifically for subject-level relapse/postpartum flare annotations for `GSE17410`/related publications.
- If unavailable, phrase the claim as "in a small MS pregnancy PBMC dataset sampled at month 9" rather than "despite clinical remission."
- Prioritize datasets with postpartum relapse outcomes, breastfeeding, DMT washout, corticosteroid use, MRI, or serum neurofilament.

Kill criterion:

- If month-9 high-IFN samples are enriched for relapse-proximal, infected, untreated, or otherwise clinically atypical subjects, the mechanism changes from pregnancy kinetics to confounded immune activation.

### 6. The postpartum kinetic claim lacks direct MS postpartum evidence

The interpretation invokes postpartum divergence, but the strongest MS PBMC dataset has pre-pregnancy and month-9 only. The independent MS dataset includes postpartum T cells and shows no IFN/APC rebound; the only notable postpartum signal is T-cell trafficking. RA has postpartum rebound, but RA is not MS, and RA rebound could reflect synovial disease biology rather than CNS autoimmune biology.

Concrete fixes:

- Make postpartum evidence mandatory before advancing the pregnancy axis to Tier 2.
- In `E-MTAB-12260`, focus on postpartum-vs-3rd-trimester and postpartum-vs-before-pregnancy for trafficking and regulatory modules, with FDR and donor-level models.
- Look for MS pregnancy/postpartum serum cytokine, flow cytometry, methylation, or immune repertoire datasets if transcriptomics are absent.

Kill criterion:

- If no MS postpartum peripheral immune rebound is found in any modality, the "postpartum kinetic divergence" portion should be removed.

## What Would Strengthen The Mechanism

Minimum credible Tier 1 package:

1. `GSE17410` survives leave-one-out and component decomposition.
2. A composition-adjusted analysis shows ISG/APC activation beyond monocyte/pDC proportion.
3. Independent MS evidence supports either late pregnancy priming or postpartum rebound in a relevant immune compartment.
4. RA and SLE comparator trajectories are reanalyzed with harmonized time bins and do not depend on one dataset-specific coding scheme.
5. The mechanism is narrowed: for example, "MS late pregnancy shows monocyte/pDC-biased ISG priming while T-cell activation is not elevated; postpartum T-cell trafficking rises."

## What Would Kill The Mechanism

The pregnancy-axis mechanism should be demoted if any two of these occur:

- `GSE17410` IFN/APC signal fails leave-one-out or raw-data reprocessing.
- Composition residualization removes the MS month-9 signal.
- `E-MTAB-12260` remains the only independent MS dataset and continues to show no supportive IFN/APC or MIF/CD74 direction.
- SLE comparator direction is inconsistent after harmonization across `GSE235508` and `GSE108497`.
- No subject-level or cohort-level MS postpartum immune rebound evidence is found.

## Concrete Next Analyses

1. `GSE17410` sensitivity report:
   - leave-one-out contrasts;
   - robust regression;
   - submodule decomposition;
   - marker residualization for monocyte, pDC, neutrophil, platelet, erythroid signatures.

2. `E-MTAB-12260` refinement:
   - FDR-correct all module/timepoint contrasts;
   - separate CD4/CD8 and activated/resting strata;
   - test postpartum trafficking as the independent MS signal, not IFN/APC replication.

3. `GSE108497` harmonization:
   - re-run with the exact `GSE235508` module definitions and a shared time-bin table;
   - compare SLE uncomplicated versus complicated pregnancies separately;
   - decide whether SLE is a valid analog or should be excluded from the MS kinetic argument.

4. Clinical metadata search:
   - retrieve original `GSE17410` publication and supplementary tables;
   - search for relapse/postpartum outcomes, DMT status, steroid use, infection exclusion, breastfeeding.

5. Claim tightening:
   - current wording should be downgraded from "MS PBMC late priming/postpartum kinetic divergence" to "a fragile MS PBMC month-9 IFN/ISG signal that motivates a monocyte/pDC versus T-cell compartment test."

## Recommended Orchestrator Decision

Do not advance the pregnancy axis to Tier 2 yet. Keep it in Tier 1 with a strict survival test. The most promising reformulation is not broad IFN/APC rebound; it is a compartment-specific model:

> In MS pregnancy, late peripheral innate antiviral/IFN priming may occur in PBMC monocyte/pDC compartments while T-cell activation remains suppressed or shifts toward trafficking only after delivery.

This reformulation is falsifiable and fits the current negative T-cell validation better than the broader kinetic-divergence narrative.
