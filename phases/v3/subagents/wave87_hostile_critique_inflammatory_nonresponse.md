# Wave87 Hostile Critique: TREM1/IL1B/CXCL8/OSM Inflammatory Myeloid Nonresponse Pivot

Timestamp: 2026-05-27 CEST

Role: hostile critique sidecar. This document does **not** claim a finding.

## Verdict

`NO_CLAIM_YET`

The pivot from residual `lysosomal_apc__resid_inflammatory_nfkb` anti-TNF response to a `TREM1`/`IL1B`/`CXCL8`/`OSM` inflammatory myeloid nonresponse circuit is biologically plausible but currently overstates the evidence. Wave86 identifies a strong **bulk intestinal anti-TNF nonresponse expression pattern** in old mucosal biopsy cohorts. It does not yet establish a circuit, a myeloid-specific mechanism, treatment specificity, cross-autoimmune breadth, a novel intervention point, or any V3 DoD-grade therapeutic claim.

## Evidence Under Review

Primary local artifacts reviewed:

- `results_v3/wave84_stratification_first_audit/REPORT.md`
- `results_v3/wave84_response_prediction_audit/REPORT.md`
- `results_v3/wave85_external_geo_antitnf_validation/REPORT.md`
- `results_v3/wave86_external_geo_antitnf_gene_driver/REPORT.md`
- `PLAN_V3.md`
- `CONVERGENCE_CHECK_45.md`
- `CRITIQUE_V3.md`

Wave84 result:

- Residual lysosomal/APC response signal was parked only.
- Predictive audit: RA synovium delta AUC `0.07018`, permutation p `0.122`, bootstrap CI low `-0.04925`; IBD DC delta AUC `0.1587`, permutation p `0.116`, bootstrap CI low `-0.05055`.
- Correct call was `PARK_STRATIFICATION_WEAK_PREDICTIVE_SIGNAL`, not promotion.

Wave85 result:

- External IBD mucosal validation failed for the primary residual lysosomal/APC signal.
- Independent-overlap weighted mean Hedges g for the primary residual module was `-0.1285`; median AUC `0.4993`; supportive nominal independent groups `0`.
- Unexpected signal: generic `inflammatory_nfkb` and IFN/inflammatory modules were higher in nonresponders.

Wave86 result:

- Gene-level decomposition tested 45 preselected module genes in four primary contexts: `GSE12251_UC_ACT1_baseline`, `GSE14580_UC_Leuven_baseline`, `GSE16879_Crohn_colitis_Leuven_baseline`, `GSE16879_Crohn_ileitis_Leuven_baseline`.
- Top genes were all inflammatory/nonresponse-high: `IL1B`, `CXCL8`, `TREM1`, `CCL4`, `CCL3`, `CD44`, `CCL2`, `ACSL1`, `IFI30`, `OSM`.
- For the proposed pivot genes:
  - `IL1B`: weighted mean Hedges g responder-minus-nonresponder `-1.695`, median nonresponse AUC `0.897`, nominal nonresponse contexts `3/4`, FDR10 contexts `3/4`.
  - `CXCL8`: weighted mean Hedges g `-1.702`, median nonresponse AUC `0.885`, nominal contexts `3/4`, FDR10 contexts `3/4`.
  - `TREM1`: weighted mean Hedges g `-1.629`, median nonresponse AUC `0.883`, nominal contexts `3/4`, FDR10 contexts `3/4`.
  - `OSM`: weighted mean Hedges g `-1.431`, median nonresponse AUC `0.815`, nominal contexts `2/4`, FDR10 contexts `2/4`.

This is a real signal, but it is a signal inside bulk IBD treatment-response data, not a V3-grade cross-autoimmune mechanism.

## Main Attacks

### 1. Gene-level anchors are collinear, not independent mechanistic nodes.

`IL1B`, `CXCL8`, `TREM1`, `CCL2`, `CCL3`, `CCL4`, `TNF`, `NFKBIA`, and `OSM` sit inside one broad inflammatory/neutrophil-myeloid/stromal injury axis. Wave86 ranks individual genes but does not test whether any one gene contributes information beyond the others, beyond neutrophil/myeloid/fibroblast abundance, or beyond histologic ulceration.

Failure mode: the top gene list is a correlated module decomposed into many apparently strong "anchors." The count of 16 `GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR` calls is itself suspicious: too many genes pass because the same latent tissue-state factor drives them.

Required before promotion: multivariable model or dimension reduction showing that a named central node retains predictive/mechanistic signal after controlling the shared inflammatory component and cell composition.

### 2. The apparent replication is less independent than the table implies.

Wave86 counts four primary contexts, but they come from three GEO series, two old Affymetrix GPL570 response programs, and at least partly overlapping Leuven data structures:

- `GSE14580` and the UC subset of `GSE16879` share GSM accessions and were correctly not counted independently in Wave85.
- `GSE16879_Crohn_colitis` and `GSE16879_Crohn_ileitis` are from the same series and may share lab processing, response adjudication, and possibly patients across biopsy sites. Patient overlap across `CDc*` and `CDi*` identifiers must be explicitly verified before treating them as independent biological replications.
- `GSE12251` and `GSE14580` both map to PubMed ID `19700435` in the Wave85 report, so they may share publication-level methods, endpoint definitions, and preprocessing assumptions even if the patients differ.

Failure mode: leave-one-publication or leave-one-series-out could collapse the signal to one old IBD expression-response ecosystem.

### 3. Wave86 uses bulk biopsy expression, so "myeloid circuit" is not shown.

Bulk mucosal gene expression cannot tell whether:

- `TREM1` is from inflammatory monocytes, neutrophils, macrophages, or mixed infiltrate;
- `IL1B` is monocyte/macrophage-derived versus epithelial/stromal injury-associated;
- `CXCL8` reflects epithelial/stromal chemokine output, neutrophil abundance, or both;
- `OSM` is leukocyte-derived and acting on fibroblasts/endothelium, as prior work suggests;
- the genes are coexpressed in one cell type, coordinated across interacting cell types, or merely co-vary with ulcerated tissue.

Calling this a `TREM1/IL1B/CXCL8/OSM circuit` requires cell-resolved or spatial ligand-receptor evidence. Wave86 currently supports only "baseline inflamed mucosa from nonresponders has high expression of these genes."

### 4. Treatment-confounding is unresolved.

The pivot risks mistaking severe baseline tissue pathology, mucosal drug loss, or pharmacokinetic nonresponse for pharmacodynamic anti-TNF resistance.

Known confounders not controlled in Wave86 primary contexts:

- baseline histologic severity;
- ulceration and epithelial loss;
- neutrophil and fibroblast abundance;
- fecal calprotectin/CRP;
- baseline anti-TNF exposure risk, dose escalation, albumin, fecal drug loss, anti-drug antibodies;
- steroid/immunomodulator co-treatment;
- tissue site and disease subtype beyond coarse cohort splitting.

Recent work explicitly warns that mucosal cytokine signals should be interpreted after accounting for mucosal drug exposure, because insufficient anti-TNF at the tissue can bias inflammatory nonresponse signatures. See Journal of Crohn's and Colitis 2025, "Anti-TNF nonresponse in ulcerative colitis: correcting for mucosal drug exposure reveals distinct cytokine profiles" ([Oxford Academic](https://academic.oup.com/ecco-jcc/article/19/1/jjae200/7941826)).

Failure mode: high `TREM1`/`IL1B`/`CXCL8`/`OSM` may mark tissue where anti-TNF never reached effective mucosal exposure or where ulceration drives neutrophil/stromal inflammation independent of TNF biology.

### 5. The signal may be general therapy refractoriness, not anti-TNF-specific.

The strongest prior art does not support strict anti-TNF specificity. Friedrich et al. identified IL-1-driven stromal-neutrophil pathotypes increased in nonresponders to several therapies, not just anti-TNF, using bulk, single-cell, histopathology, and localization across large IBD cohorts ([Nature Medicine 2021](https://www.nature.com/articles/s41591-021-01520-5)). That work specifically links IL-1R-dependent fibroblast-neutrophil biology to therapy failure.

Failure mode: Wave86 rediscovers a general ulcerated refractory pathotype. That could be clinically useful, but it is not a specific anti-TNF resistance mechanism unless compared against vedolizumab, ustekinumab, JAK inhibition, corticosteroids, and untreated inflammation controls.

### 6. Prior art is a major blocker, especially for OSM, TREM1, and IL-1 biology.

Closest prior art found:

- OSM/OSMR: West et al. reported that mucosal `OSM`/`OSMR` predict anti-TNF nonresponse across five datasets and 227 patients, and proposed OSM as an inflammatory driver and therapeutic target ([Nature Medicine 2017](https://www.nature.com/articles/nm.4307), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC5420447/)).
- OSM patent: `US10822406B2` directly claims treating chronic intestinal inflammation/IBD by antagonizing OSM and/or OSMR and includes anti-TNF response-prediction material ([Google Patents](https://patents.google.com/patent/US10822406B2/en)).
- IL-1/stromal-neutrophil pathotype: Friedrich et al. provides a direct IL-1R-dependent therapy-nonresponse framework with cell-state and histologic support ([Nature Medicine 2021](https://www.nature.com/articles/s41591-021-01520-5)).
- TREM1 biomarker: Verstockt et al. reported low whole-blood and mucosal `TREM1` expression as an anti-TNF response biomarker in IBD, including AUCs around `0.78` and `0.77` in the paper summary ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6413341/)).
- TREM1 mechanistic/therapeutic prior art: TREM1+ macrophages and TREM1 blockade, especially together with anti-TNF, have already been proposed in Crohn's disease ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8328300/)).
- TREM1 clinical program: CEL383 is an anti-TREM1 antibody advanced for IBD; Phase 1 healthy-volunteer study `NCT05901883` completed, and Celsius/AbbVie publicly position CEL383 as an IBD TREM1 program ([BusinessWire](https://www.businesswire.com/news/home/20230803586891/en/Celsius-Therapeutics-Announces-Initiation-of-Dosing-in-Phase-1-Clinical-Trial-of-CEL383-an-Anti-TREM1-Antibody-for-the-Treatment-of-Inflammatory-Bowel-Disease), [trial mirror](https://cdek.pharmacy.purdue.edu/trial/NCT05901883/)).
- TREM1 patent space: TREM1 inhibitors and IBD-relevant uses appear in `WO2022061226A1` ([Google Patents](https://patents.google.com/patent/WO2022061226A1/en)).
- Negative/contradictory TREM1 prior art: SERENE UC/CD whole-blood RNA-seq did not validate baseline `TREM1` as an adalimumab response predictor in phase 3 trial datasets ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11037103/)).
- Cell-centred meta-analysis prior art: anti-TNF nonresponse in IBD biopsies/blood has already been framed as myeloid/B-lineage inflammatory pathway biology, including TREM1-related axes ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6580771/)).

Implication: any claim around "OSM-high/TREM1-high/IL1B/CXCL8 inflammatory mucosa predicts anti-TNF failure in IBD" is heavily prior-arted. A novel contribution would need to be much sharper, for example a validated cross-disease biomarker transfer, a non-obvious upstream controller not claimed in prior art, or a treatment-selection interaction not already covered.

### 7. The pivot currently fails V3 DoD on breadth and therapeutic relevance.

V3 requires a cross-autoimmune mechanism with at least five autoimmune diseases, three evidence channels per disease, cross-disease genetic anchoring, foundation-model perturbation prediction, cell-state replication across at least three target tissues, an intervention-point druggability audit, novelty across diseases, and reproducibility.

The current pivot has:

- strong bulk IBD anti-TNF expression association;
- no MS anchor for `TREM1`/`IL1B`/`CXCL8`/`OSM` nonresponse;
- no RA, psoriasis, SLE, T1D, Sjogren, ankylosing spondylitis, thyroid, celiac, or PBC response validation;
- no MR/coloc or genetic causality for the circuit;
- no foundation-model perturbation output;
- no real perturbation validation showing that modulating the node reverses the state while preserving host defense and repair;
- no unblocked novelty for the most obvious therapeutic nodes.

Therefore this branch may be useful as a stress-tested IBD comparator, but it cannot become `FINDING_V3.md` unless it is reformulated and substantially extended.

## Specific Statistical Artifacts To Rule Out

1. Winner's curse after failed Wave85 primary endpoint. Wave86 was opened because the preplanned residual endpoint failed. Gene-level decomposition is exploratory and must be treated as discovery, not validation.

2. Multiple correlated tests. Testing 45 genes from handpicked inflammatory modules yields many highly correlated p-values. Within-cohort FDR does not convert correlated module members into independent mechanistic discoveries.

3. Meta-rank is not a formal meta-analysis. `meta_rank_score` combines direction counts, nominal p-values, FDR counts, effect sizes, and AUCs. It is useful triage but lacks random-effects heterogeneity, confidence intervals, and leave-source-out robustness.

4. Weak fourth context. For several top genes, Crohn ileitis is directionally nonresponse-high but not statistically strong: `IL1B` p `0.1118`, `CXCL8` p `0.1548`, `TREM1` p `0.07229`, `OSM` p `0.1494`, with within-cohort FDR `0.8636` for these rows. Counting "4/4 nonresponse-high contexts" overweights trend-level ileitis support.

5. Endpoint heterogeneity. GSE12251 uses week-8 endoscopic/histologic healing; GSE14580/GSE16879 use 4-6 week endoscopic/histologic response. These are related but not identical clinical phenotypes.

6. Probe/gene robustness is not checked. GPL570 has full nominal coverage for the 45 genes, but Wave86 should check whether top-gene effects are driven by one probe, probe collapsing, or cross-hybridization, especially for chemokines and HLA-adjacent immune genes.

7. No negative-control modules. The branch needs matched inflammatory, neutrophil, epithelial-loss, stromal, and housekeeping controls to show specificity beyond generic tissue damage.

## Why This Might Still Be Useful

The data are not noise. The direction and effect sizes for `IL1B`, `CXCL8`, and `TREM1` are strong across old IBD mucosal anti-TNF cohorts, and the signal is concordant with major prior biology. The best use is as a hostile comparator and possible patient-state axis:

- "ulcerated inflammatory myeloid/stromal mucosa predicts nonresponse to TNF blockade";
- "residual lysosomal/APC responder-high biology is not externally robust";
- "future claims must distinguish inflammatory nonresponse pathotype from actionable target."

That is valuable, but it is not novel therapeutic discovery yet.

## Next Two Strongest Falsifying Analyses

### Analysis 1: Leave-source-out, covariate-adjusted patient-level meta-analysis with cell-composition and severity proxies.

Goal: determine whether the `TREM1`/`IL1B`/`CXCL8`/`OSM` nonresponse signal is more than ulceration/cell-composition/severity.

Design:

- Rebuild Wave86 at patient level.
- Collapse non-independent sources:
  - one Leuven UC representation only;
  - explicitly test whether `GSE16879_Crohn_colitis` and `GSE16879_Crohn_ileitis` share patients; if yes, aggregate per patient or model patient as a random effect.
- Compute gene and module scores for:
  - proposed circuit: `TREM1`, `IL1B`, `CXCL8`, `OSM`;
  - neutrophil/granulocyte markers: e.g. `S100A8`, `S100A9`, `MPO`, `FCGR3B`, `CXCR2`;
  - fibroblast/stromal/ulceration proxies: e.g. `COL1A1`, `COL1A2`, `PDPN`, `VIM`, `MMP3`, `MMP7`;
  - epithelial-loss proxies: epithelial marker depletion;
  - generic inflammation: `TNF`, `NFKBIA`, `IL6`, `CXCL1/2/3` where present.
- Fit per-cohort logistic models and random-effects meta-analysis:
  - baseline: response ~ severity/cell-composition proxies + disease/tissue/source;
  - augmented: baseline + proposed circuit score or individual gene.
- Use nested cross-validation or leave-one-series/publication-out validation.
- Use patient-label permutation within source to estimate empirical p-values for added AUC and log-likelihood.

Falsification rule:

- Falsify the pivot if the proposed circuit adds `delta AUC <= 0.05`, adjusted pooled SMD magnitude `< 0.3`, or any leave-one-source-out run reverses direction.
- Also falsify if neutrophil/stromal/ulceration proxies absorb more than 70% of the effect and individual `TREM1`/`IL1B`/`CXCL8`/`OSM` coefficients become unstable.

Why strongest:

- It directly attacks the most likely artifact: high inflammatory genes are a readout of ulcerated neutrophil/stromal tissue and severity, not a central nonresponse mechanism.

### Analysis 2: Cell-resolved treatment-specificity test across IBD and non-IBD autoimmune tissues.

Goal: determine whether the branch is a cell-cell circuit, an anti-TNF-specific resistance state, or a generic refractory inflammation state.

Design:

- Use cell-resolved IBD anti-TNF data already in the workspace (`GSE282122`) plus any accessible IBD single-cell/spatial response atlases.
- Score the circuit separately in monocytes/macrophages, DCs, neutrophils if available, fibroblasts/stromal cells, endothelial cells, epithelium, T cells, and plasma cells.
- Test ligand-source/target logic:
  - `TREM1`/`IL1B` in inflammatory myeloid/neutrophil compartments;
  - `OSM` source in leukocytes;
  - `OSMR`/`IL1R1` and downstream chemokine response in stromal/endothelial compartments;
  - `CXCL8` source and neutrophil recruitment relation.
- Compare anti-TNF response prediction against non-TNF response contexts:
  - vedolizumab/ustekinumab/JAK inhibitor/corticosteroid if response-labelled data are available;
  - inflamed untreated or active-vs-remission controls as a severity-only comparator.
- Cross-disease stress test:
  - project the same cell-state score into RA synovium, MS lesion myeloid/spatial, psoriasis skin, and Sjogren/other available autoimmune tissues.
  - Require the same cell-state transition and tissue logic, not just high generic inflammation.

Falsification rule:

- Falsify the "circuit" if bulk signal localizes primarily to cell abundance rather than within-cell activation, if ligand and receptor compartments do not spatially/cell-resolved co-occur, or if the score predicts nonresponse equally across unrelated therapies and untreated severity.
- Falsify V3 relevance if the circuit fails in MS and at least two non-IBD autoimmune tissues, or if no cell-resolved compartment shows treatment-response association after donor and disease-severity adjustment.

Why strongest:

- It directly attacks the biological operationalization. If this is truly a `TREM1`/`IL1B`/`CXCL8`/`OSM` circuit, it must be visible as coordinated myeloid-stromal-neutrophil biology in cell-resolved tissue, not only as bulk biopsy expression.

## Bottom Line

The pivot is a legitimate discovery branch but not a finding. The safest current statement is:

> External IBD anti-TNF mucosal cohorts do not validate the residual lysosomal/APC responder-high endpoint; instead, they show a strong, prior-arted inflammatory nonresponse state enriched for `IL1B`, `CXCL8`, `TREM1`, and `OSM`.

Anything stronger would currently violate the V3 constraints on novelty, cross-autoimmune breadth, mechanism, treatment specificity, and therapeutic feasibility.
