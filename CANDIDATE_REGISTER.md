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

### Prospective `GSE301908` Survival Rule

This rule is fixed before opening the expression object. The primary contrast is deposited `Micro2` (foamy/MIMS2) versus deposited `Micro0` (homeostatic/HMG), analysed as library-size-normalized pseudobulk expression for each specimen and then averaged within donor where donor identity can be recovered from deposited metadata. `TBXAS1` is the single targeted validation test. `GPNMB`, `APOE`, `LPL`, `SPP1`, and the published comparator `MGLL` are state-mapping checks rather than replacement discoveries.

The intervention branch survives this stage only if all of the following are met:

1. At least eight paired donors each contribute at least 20 nuclei to both `Micro2` and `Micro0`.
2. `TBXAS1` is higher in `Micro2` with mean paired delta `>0`, positive direction in at least two thirds of paired donors, and paired standardized effect `dz >= 0.5`.
3. A two-sided paired Wilcoxon test for the prospectively single target gives `p < 0.05`.
4. At least three of the four state controls (`GPNMB`, `APOE`, `LPL`, `SPP1`) are directionally higher in `Micro2`; otherwise the deposited-label interpretation is suspect.

If donor IDs cannot be recovered, coverage is below threshold, or any required target criterion fails, `GSE301908` cannot support promotion of `TBXAS1`/thromboxane-directed intervention. No alternate gene from this readout will be promoted without a new registered branch and independent evidence.

## Pivot 3 Outcome: `TBXAS1` Rejected By Therapeutic Prior Art

The independent cell-state readout is no longer a route to a new `TBXAS1` therapeutic claim. Google Patents retrieval of `WO2004028339A2` (publication 2004-04-08, priority 2002-09-27) showed that the patent's MS CNS expression tables list `M80647 Thromboxane synthase` as increased, while its treatment claims describe decreasing gene products increased in those tables. This is direct target-level therapeutic prior art for lowering thromboxane synthase in MS.

The protein-to-`thromboxane_B2` association remains a reproducible observation from the deposited lesion multi-omics data, but it is not novel enough for the required translational finding. `GSE301908` acquisition may be reused only for a newly registered candidate or as a documented confirmation of known lesion biology; it cannot revive this branch.

## Rapid Prior-Art Triage: `NAAA` Rejected Before Registration

`NAAA` was elevated in the unbiased lesion proteomic results (`coef=0.6152`, `FDR=0.002107`, 31 specimens/19 donors), making preservation of its anti-inflammatory substrate `PEA` superficially attractive. However, `PEA` was not significantly depleted in the human lipidomic comparison (`coef=-0.3033`, `FDR=0.2792`), and literature retrieval immediately identified direct NAAA-inhibition experiments in EAE/MS-model disease (Pontis et al. 2020, DOI `10.1016/j.phrs.2020.105064`; Sgroi et al. 2021, DOI `10.1016/j.phrs.2021.105816`; combination therapy in Sgroi et al. 2024, DOI `10.1016/j.biopha.2024.116677`). This candidate is rejected before any new validation endpoint is registered.

## Rapid Safety Triage: `FYN` Rejected Before Registration

`FYN` was enriched in foamy human lesion proteomics (`coef=0.4773`, `FDR=4.87e-06`, 32 specimens/20 donors) and has CNS-relevant inhibitor chemical matter such as saracatinib. Primary myelination evidence makes the direction unacceptable without cell-selective delivery: Fyn activation is required for oligodendrocyte morphological differentiation, and Src-family/Fyn inhibitors reduce myelin membrane formation (Osterhout et al., *J Cell Biol* 1999, PMID `10366594`; Perez et al., *J Neurosci Res* 2013, PMID `23797152`). Because this dataset does not yet establish microglia-specific pathogenic Fyn or a microglia-selective inhibitor, broad inhibition risks suppressing repair and is rejected.

## Candidate 4 Registered Before Cell-State Testing: `EGLN1`-High Foamy-Lesion Stratification For `EHP-101`

**Candidate form:** stratification biomarker, not a novel drug or novel PHD2/HIF mechanism. `EHP-101` (`VCE-004.8`) is existing chemical matter whose MS phase IIa study `NCT04909502` is listed by ClinicalTrials.gov as `SUSPENDED` after a recruitment pause to reassess eligibility criteria. The proposed delta is that a foamy/chronic-active-lesion-enriched `EGLN1` state could identify the mechanistically aligned population that the broad relapsing-MS design did not select.

### Nomination Evidence Available Before New Testing

- `EGLN1`/PHD2 protein is elevated in foamy active/mixed human MS lesions in the existing donor-aware proteomic screen: adjusted coefficient `+0.3595` log2 LFQ, `p=1.43e-05`, `FDR=0.0005111`, 30 specimens from 20 donors.
- VCE-004.8 prior work already reports modulation of the PP2A/B55alpha/PHD2/HIF pathway and notes its MS phase II programme (Navarrete et al., *Journal of Neuroinflammation* 2022, DOI `10.1186/s12974-022-02540-9`). This is mechanism prior art supporting feasibility, not novelty.
- The deposited `GSE284005` 500-gene MERFISH panel does not measure `EGLN1`; no new spatial target localization can be claimed from that panel.

### Prospective Independent Cell-State Test

In independent human snRNA-seq `GSE301908`, use deposited `Micro2` (foamy/MIMS2) versus `Micro0` (homeostatic/HMG) labels. Aggregate raw counts to specimen pseudobulks and then donor-level contrasts if deposited specimen identifiers recover donors. `EGLN1` is the single candidate validation target; `GPNMB`, `APOE`, `LPL`, and `SPP1` are state-identity controls and cannot become replacement claims.

The biomarker branch survives only if:

1. At least eight paired donors each have at least 20 nuclei in `Micro2` and `Micro0`.
2. `EGLN1` is higher in `Micro2` with mean paired delta `>0`, positive direction in at least two thirds of paired donors, paired `dz >= 0.5`, and two-sided paired Wilcoxon `p < 0.05`.
3. At least three of four state controls are directionally elevated in `Micro2`.

### Mandatory Later Gates

Even if the expression test passes, promotion requires verification that EHP-101 exposure/target engagement is feasible in CNS tissue or CSF, a biomarker assay usable in living patients rather than post-mortem tissue alone, and a novelty search showing no published or patented `EGLN1`/foamy/PRL-based enrichment design for EHP-101. Failure of any gate rejects the branch.

### Pre-Result Safety Conflict

The pathway polarity is not assumed favorable. Rosiewicz et al., *Glia* 2023 (DOI `10.1002/glia.24380`), reports that astrocytic HIF prolyl-hydroxylase 2/3 deletion disrupts astrocytic integrity and exacerbates neuroinflammation. Thus an `EGLN1`-high lesion signal cannot justify broad PHD2 inhibition; the only surviving proposition would be empirical enrichment for the multitarget compound EHP-101, with astrocyte safety and mechanistic target-engagement experiments required before translation.

## Pivot 4 Outcome: `EGLN1` Rejected By Independent Cell-State Direction

The exact deposited-label test could not be run because the public `GSE301908_sn_all.rds` object lacks the authors' `sub` microglial subcluster field and contains only normalized expression. A reformulated high-confidence state test used author-code markers to define MIMS2-like (`GPNMB`/`APOE`) and HMG-like (`P2RY12`/`CX3CR1`/`TMEM119`/`SALL1`) cells, with `EGLN1` excluded from the state definition.

The reconstructed state passed identity checks, but the target moved in the wrong direction: across 10 paired MS donors, `EGLN1` was lower in MIMS2-like cells (mean delta `-0.0507`, paired `dz=-0.568`, positive in `2/10`, Wilcoxon `p=0.126`). The `EGLN1`-high EHP-101 stratification branch is rejected.

## Final Exhaustive Screen Rule Before Stopping

Because individually nominated branches have repeatedly failed novelty, safety, product-link, or cross-dataset validation gates, the remaining defensible move is a narrow convergence screen rather than another hand-picked target. The screen is registered after `EGLN1` rejection and before inspecting transcriptome-wide `GSE301908` state statistics.

The discovery family is restricted to proteins already elevated in foamy active/mixed lesions in the donor-aware Van der Vliet proteomic screen (`FDR < 0.05`, positive coefficient, adequate reporting coverage). For those proteins only, test whether the corresponding transcript is higher in the reconstructed `GSE301908` MIMS2-like state. A candidate can enter translational audit only if:

1. foamy-lesion proteomics: `FDR < 0.01`, positive coefficient, adequate coverage;
2. independent MIMS2-like transcript state: mean delta `>0`, positive in at least `8/10` paired donors, paired `dz >= 0.8`, and targeted Wilcoxon `p < 0.05`;
3. existing chemical matter or modality can plausibly modulate the target in CNS tissue without obvious remyelination or lysosomal-clearance harm;
4. prior-art search does not find direct MS intervention or biomarker-stratification claims.

Failure of this restricted screen will trigger `EXHAUSTION.md` rather than a weaker narrative claim.

## Candidate 5 Outcome: `ACSL1` Survives As A Constrained Target Hypothesis

The restricted screen produced 11 convergent proteome/snRNA genes. Triage rejected marker-only and lysosomal-clearance genes as immediate therapeutic claims. `ACSL1` survives as the best target hypothesis:

- foamy-lesion proteomics: `coef=0.3662`, `FDR=0.000837`, 32 specimens/20 donors;
- independent MIMS2-like microglia transcript validation: mean delta `0.1975`, `dz=1.169`, positive in `10/10` donors, Wilcoxon `p=0.00592`;
- spatial MERFISH: compatible but underpowered direction, strongest in T-near pathological microglia (`dz=0.800`, positive in `5/6`, `p=0.0625`);
- adjacent causal support: ACSL1 perturbation in non-MS microglia models affects lipid-droplet accumulation and neuroinflammation.

Promotion boundary: `ACSL1` is not a repurposing claim because no selective CNS-engaged clinical ACSL1 inhibitor was found. It is a novel drug-discovery target hypothesis requiring human microglia/myelin-debris knockdown, rescue, and repair-safety falsification before animal or clinical translation.
