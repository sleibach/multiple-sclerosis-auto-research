# Therapeutic Candidate Register

**Registration time:** 2026-05-26, before inspecting expression values for candidate targets in `GSE284005`.

## Inputs Used For Nomination

- `GSE284005_RAW.tar` structure and 500-gene panel only: author cell labels and spatial coordinates are available; gene presence/absence was inspected, not candidate-expression differences.
- Feng et al. source paper/code: chronic-active MS lesion spatial design, known sterol-efflux intervention (`DHCR24` inhibitor `SH42`), and author T-cell-neighborhood strategy.
- Adjacent-field literature retrieved before testing:
  - Huynh et al., *Biomolecules* 2024, DOI `10.3390/biom14101301`: ACAT1/SOAT1 inhibition in myelin-debris-treated microglial cell lines increases `ABCA1`.
  - Gouna et al., *Journal of Experimental Medicine* 2021, DOI `10.1084/jem.20210227`: `TREM2`-dependent lipid-droplet biogenesis, including `SOAT1`, is required for remyelination after focal demyelination.

## Registered Primary Candidate: `SOAT1` Modulation

`SOAT1` (also known as ACAT1) is measured in the MERFISH panel and encodes the enzyme that esterifies cholesterol for lipid-droplet storage. It is nominated because chronic-active MS lesions contain lipid/sterol-loaded pathological microglia, while myelin-debris microglia in an adjacent neurodegeneration model respond to SOAT1 inhibition with increased cholesterol-efflux transporter expression.

This is a **candidate target**, not a therapeutic claim. The intended modality is not yet fixed: direct inhibition is biologically hazardous unless pathological storage can be separated from required remyelination-associated lipid handling.

### Prospective Spatial Tests

In demyelinated white-matter (`DMWM`) cells using deposited author labels:

1. Compare `SOAT1` expression in pathological microglia (`Micro Foamy`, `Micro SPP1`, `Micro Stress`) against `Micro Homeo`, using sample pseudobulks aggregated to donor-level contrasts.
2. Define T-cell proximity using the author-code-compatible rule: a microglial cell is T-near if it lies among the 100 nearest non-self neighbors of any author-labelled T cell in the same specimen. Compare `SOAT1` in pathological T-near versus T-far microglia using within-donor contrasts.
3. Assess pathway coherence with measured sterol/lysosome genes (`PLIN2`, `LIPA`, `ABCA1`, `ABCG1`, `NR1H3`, `LAMP1`, `CTSD`) and benchmark published disease-state markers (`GPNMB`, `SPP1`, `APOE`).

### Required Positive Observation

The candidate survives the spatial stage only if `SOAT1` is directionally elevated in the pathological state and/or T-near pathological microglia in at least half of informative donors, with donor-level effect size `|standardized paired difference| >= 0.5` and Benjamini-Hochberg `FDR < 0.05` within the registered target/pathway family.

### Immediate Falsifiers

- Lack of enrichment in pathological/T-near microglia in the spatial dataset.
- Directionally incompatible independent human lesion evidence.
- No realistic CNS-capable SOAT1 pharmacology.
- Evidence that therapeutically relevant inhibition worsens myelin clearance or remyelination without a separable treatment window or cell-selective modality. The Gouna et al. result makes this a live, not hypothetical, failure mode.

## Comparators And Reserve Targets

| Target/pathway | Role before testing | Reason |
|---|---|---|
| `ABCA1`, `ABCG1`, `NR1H3` | Published-mechanism coherence controls | Sterol efflux/LXR biology is already part of Feng et al.; it cannot become the new claim. |
| `GPNMB`, `SPP1`, `APOE`, `PLIN2` | Pathological-state controls | Expected MIMS/foamy markers, not intervention discoveries. |
| `RIPK1` | Excluded from novelty | A CNS-penetrant RIPK1 inhibitor (`SAR443820`/`DNL788`) has already entered an MS phase 2 trial. |
| `BTK` | Excluded from novelty | CNS-active BTK inhibition is already an MS clinical-development strategy. |
| `C3AR1`/`C5AR1` | Reserve only | Complement receptor lesion biology and a proposed MS treatment target have already been published; CNS-capable repurposing remains unproven. |
| `LIPA` | Mechanistic reserve only | It can explain lysosomal cholesteryl-ester handling, but no verified CNS-delivered activating therapy is presently registered here. |

## Interpretation Boundary

Expression enrichment would not establish SOAT1 activity, causality, or net benefit of inhibition. A target cannot be promoted without independent human validation, pharmacology/exposure review, full novelty review, and an experiment explicitly measuring remyelination harm.

## Pivot 1 Outcome: `SOAT1` Rejected

The registered spatial analysis rejected `SOAT1`: neither pathological-versus-homeostatic DMWM microglia nor T-near-versus-T-far pathological DMWM microglia showed consistent donor-level `SOAT1` elevation (`FDR=0.9453` and `0.8438`, respectively; six informative donors). It is not pursued further.

## Candidate 2 From Target-Agnostic ABPP Screen: `PLA2G7`/Lp-PLA2 Inhibition

**Selection point:** after the prespecified spatial target failed, an orthogonal target-agnostic screen was run across deposited activity-based protein profiling (ABPP), lipidomics, and proteomics in the independent foamy-lesion cohort. Models adjusted foamy versus non-foamy morphology for active-versus-mixed lesion category and clustered correlation by donor; FDR was corrected within each modality.

### Discovery Observation

- Active `PLA2G7` protein in ABPP is elevated in foamy lesions: adjusted coefficient `+1.2353` log2 LFQ, `p=0.000709`, `FDR=0.007741`, 28 eligible specimens from 18 donors.
- The canonical Lp-PLA2 product class is represented by increased `LPC(20:3)` in lipidomics: adjusted coefficient `+0.3783`, `p=0.000211`, `FDR=0.002666`, 29 specimens from 20 donors. Product coupling still requires sample-level testing; co-enrichment alone is not flux proof.

### Why This Is Not Called A Novel Target

Preliminary literature checks found existing prior art:

- Sternberg et al., *Journal of Clinical Immunology* 2012, DOI `10.1007/s10875-011-9642-3`, studied Lp-PLA2 as an inflammatory vascular-risk biomarker in MS.
- A 2026 review of PLA2G7 reports an EAE macrophage-polarization connection; its cited primary intervention evidence must be verified before any novelty statement.

The potential delta is therefore a **stratification/repurposing hypothesis**: high active `PLA2G7` in foamy, progression-associated human lesion tissue may nominate a PRL/foamy-lipid biomarker subgroup for a CNS-exposed Lp-PLA2 inhibitor, not demonstrate that Lp-PLA2 was previously unknown in MS.

### Candidate Compound Class

- `Rilapladib` establishes that oral Lp-PLA2 inhibition has been clinically administered, but its Alzheimer study states that it is not believed to be brain-penetrant; it is not an adequate progressive-lesion candidate.
- `GSK2647544` is the provisional compound because a human PET biodistribution study reports measurable brain exposure. Its potency, safety, target-engaging exposure, development status, and patent/prior-art position remain to be audited before promotion.

### Mandatory Validation And Kill Criteria

1. Test whether active `PLA2G7` tracks `LPC(20:3)` within overlapping human lesion samples after lesion category/morphology adjustment.
2. Test whether `PLA2G7` transcript is enriched in immune nuclei from chronic-active lesion edges in independent `GSE180759`, using donor/pseudobulk inference; no cell-level pseudo-replication.
3. Reject the candidate if the source article already claims Lp-PLA2 inhibition for foamy/progressive MS, if independent human cell-state validation is absent, or if no CNS exposure can meet relevant inhibition potency.

## Pivot 2 Outcome: `PLA2G7` Rejected

The same-cohort mechanistic gate failed. Across 25 overlapping specimens from 18 donors, active `PLA2G7` did not associate with `LPC(20:3)` after adjustment for foamy morphology and active-versus-mixed lesion class (`coef=0.2294`, `p=0.3527`, `FDR=0.7054` across 16 tested LPC species). Its separate enrichment with foamy morphology therefore cannot be interpreted as evidence that Lp-PLA2 drives the relevant lipid state. `PLA2G7` will not be promoted as the therapeutic finding.

## Candidate 3 Under Evaluation: `TBXAS1`/Thromboxane Synthase Inhibition

**Selection point:** examination of robustly covered proteins after the activity-led `PLA2G7` branch failed identified `TBXAS1` as an enzyme with an immediately measurable direct product class. Unlike lysosomal hydrolase hits (`ASAH1`, `LIPA`), inhibition of thromboxane synthase does not prima facie worsen cholesterol clearance or reproduce a known lysosomal storage deficiency.

### Pre-Validation Observation

- `TBXAS1` protein is enriched in foamy active/mixed lesions in the donor-aware proteomic screen (`coef=0.5572` log2 LFQ, `FDR=6.90e-07`, 32 specimens from 20 donors).
- `thromboxane_B2`, the stable hydrolysis product used as a readout of thromboxane A2 production, is increased in the lipidomic screen (`coef=1.5489`, `FDR=0.02529`; exact trace retained in the result table).

### Required Validation And Kill Criteria

1. Test residual `TBXAS1` protein-to-`thromboxane_B2` association among overlapping lesion specimens after adjusting for foamy morphology and lesion group.
2. Search for independent human lesion-cell transcriptional localization (`GSE180759`; spatial panel if measured) before interpreting the enzyme as a lesion-cell target.
3. Reject if the product coupling is absent, independent localization conflicts, prior art already directly proposes CNS thromboxane synthase inhibition in progressive/PRL-positive MS, or no realistic CNS-exposed inhibitor exists.

### Product-Link Result And Prior-Art Restriction

`TBXAS1` passed the product-link gate in the deposited foamy-lesion cohort: across 28 overlapping specimens from 20 donors, `TBXAS1` protein and `thromboxane_B2` were strongly associated (`rho=0.7586`, `p=2.90e-06`); after foamy-morphology and lesion-group adjustment, the donor-aware coefficient was `2.5205` (`p=3.65e-09`).

However, full-text review of Van der Vliet et al. (2026, DOI `10.1038/s41593-026-02302-3`) established that this is **not** a novel target localization: the paper identifies `TBXAS1` in its foamy-microglia lipid-metabolism module and shows TBXAS1 staining at rims of mixed lesions with foamy versus nonfoamy microglia. The only remaining potential novelty is repurposing a thromboxane-synthase-directed intervention for the histologically/biomarker-defined foamy progressive-MS subgroup, if independent data and exposure evidence support it.

### Independent Check To Date

In independent `GSE180759`, the available contrast is chronic-active versus chronic-inactive lesion-edge transcript abundance, not foamy versus nonfoamy state. Only three paired donors meet the minimum-cell criterion. `TBXAS1` is inconsistent in immune and vascular pseudobulks (positive in `1/3` donors in each); an oligodendrocyte observation is positive in `3/3` donors but underpowered (`p=0.25`) and mismatched to the proposed foamy-microglia mechanism. This does not validate the intervention claim.

`GSE301908` is therefore the required matched-state adjudication dataset: it is an independent human snRNA-seq cohort with foamy/pathological microglial states paired to the Feng et al. spatial atlas. Candidate promotion remains blocked pending that result and a pharmacology/novelty audit.
