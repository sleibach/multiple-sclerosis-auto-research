# Therapeutic Discovery Execution Plan

**Date locked:** 2026-05-26  
**Question:** Is there a translationally credible, previously unclaimed intervention point in the spatially defined chronic-active MS lesion niche that is supported by independent human multi-omics and existing CNS-capable pharmacology?

`PLAN.md` remains the record of the completed execution-phase negative test. This plan governs the therapeutic discovery phase.

## Candidate Classes And Prior-Art Controls

| Class | Role |
|---|---|
| MAGL inhibition / `RO7268489` | Positive translational benchmark and exclusion: already reported and in a progressive-MS Phase 2 program. |
| DHCR24 inhibition / desmosterol-LXR-efflux enhancement (`SH42`) | Positive mechanistic benchmark and exclusion: already shown in EAE and covered by inventor patent disclosure in Feng et al. |
| Lysosomal rescue imported from Gaucher/Parkinson biology (for example `GBA1`/GCase chaperoning with ambroxol) | Candidate line only if MS data demonstrate a corresponding lysosomal/substrate failure spatially and independently. |
| Inflammasome/lipid-crystal sensing interventions (`NLRP3`, `P2RX7`, related) | Candidate line only if the spatial lesion niche and independent multi-omics support the target beyond general inflammation, and prior MS work does not pre-empt it. |
| Immune-to-microglia spatial signals with CNS-capable inhibitors | Target-agnostic discovery line; candidate selected only after spatial evidence. |

## Line 1: Human Spatial Target Discovery

### Data

- GEO `GSE284005`: MERFISH raw TSV files from 14 chronic-active MS donor specimens/regions (17 samples).
- Authors' code repository/Zenodo metadata for mapping of cell annotations and tissue domains, if publicly exposed.

### Methods

1. Download and checksum the manageable raw archive plus relevant authors' code/metadata.
2. Inspect deposited file structure before choosing annotation strategy.
3. If deposited cell labels/domain labels are available, use them unchanged.
4. If only cell-by-gene and coordinates are provided, construct a conservative marker-based classification restricted to broad cell types required for the question (microglia/myeloid, T lymphocytes, B lymphocytes, oligodendrocyte lineage, astrocytes), and validate marker separation internally and, where possible, against author-described proportions/labels.
5. Define pathological microglia using pre-specified markers rooted in the two published human studies: `GPNMB`, `SPP1`, `APOE`, `LPL`, `C1Q*`, `PLIN2` where present, and interferon-response genes reported in the panel.
6. Perform per-donor spatial neighborhood testing: identify druggable genes/pathways enriched in pathological microglia within a fixed radius or nearest-neighbor window of T/B-cell neighborhoods versus pathological microglia outside those neighborhoods. Use within-sample label permutation and control FDR across tested actionable targets.

### Spatial Gate

A new target enters the shortlist only if:

- it is measured by the panel or reliable paired cell-state data;
- target/pathway enrichment near immune-cell neighborhoods is directionally concordant in at least half of informative donors/regions and survives pooled donor-aware inference at `FDR < 0.05`;
- the finding is not simply `MGLL`, `DHCR24`, `ABCA1/G1`, or another mechanism already explicitly developed in the source studies.

### Pivot

If raw spatial data cannot support trustworthy cell/domain assignment, do not substitute bulk signature correlation. Pivot to a candidate explicitly supported by deposited cell-resolved labels or write a blocker for this discovery line.

## Line 2: Independent Human Multi-Omics Validation

### Data

- `GSE279972` and Zenodo `10.5281/zenodo.19352263`: morphology, donor, lesion class, transcriptomics, proteomics, lipidomics, chemical proteomics, and any progression variables present.
- `GSE180759`: targeted expression localization where adequate cell counts exist.

### Methods

1. For spatially shortlisted targets only, extract transcript/protein abundance and target-linked lipids or chemical-proteomic signals, without broadly scanning for a successful substitute after outcome inspection.
2. Compare foamy versus non-foamy and lesion classes using donor-aware models.
3. Use progression or CSF biomarker associations only if deposited data provide explicit outcome definitions.
4. Use `GSE180759` only as a targeted independent expression/state check; it cannot validate spatial proximity.

### Independent Human Gate

The central target/pathway observation must reproduce in at least one independent human data source or modality with compatible direction and non-trivial effect size; evidence must not depend solely on a candidate-picked p-value from one bulk cohort.

## Line 3: Drug/Target/Exposure/Genetics Translation

### Methods

For each candidate surviving Lines 1 and 2:

1. Retrieve compound-target evidence from ChEMBL and/or primary pharmacology sources.
2. Identify existing clinical-stage or approved agents and assess CNS/CSF exposure relative to target potency from primary PK/PD literature.
3. Query ClinicalTrials.gov and Open Targets for MS programs and known trial failure.
4. Query GWAS Catalog/Open Targets genetics; state whether genetic support exists. Absence is acceptable for a lesion-state target but reduces confidence.
5. Query context-appropriate perturbation evidence (microglia/macrophage/brain models) where accessible; reject reversal evidence derived only from unrelated cancer cells as insufficient.

### Translational Gate

A therapeutic candidate requires:

- existing chemical matter or a realistic modality;
- measurable CNS exposure or a feasible CNS delivery plan;
- a biomarker that can select the relevant MS subgroup and measure target engagement;
- a defensible safety/failure-mode assessment.

## Line 4: Cross-Domain Transfer

Investigate lesion-compatible mechanisms from:

- Parkinson/Gaucher lysosomal microglia (`GBA1`, lysosomal chaperones, `GPNMB` as stress readout);
- Alzheimer/aging lipid-droplet microglia and CNS drug programs;
- atherosclerotic foam-cell cholesterol/oxylipin resolution;
- oncology immune-neighborhood manipulation only when immunosuppression/toxicity implications are addressed.

Cross-domain analogy can nominate a compound but cannot satisfy a human MS validation gate alone.

## Candidate Calling Rules

A therapeutic finding will be written only if one candidate meets every following condition:

1. human spatial evidence in a lesion-relevant cellular compartment;
2. independent human multi-omic or cell-state validation;
3. an existing agent/modality with credible CNS target engagement;
4. no direct prior art for the same candidate-mechanism-population proposal after full novelty search;
5. a practical falsification experiment and clinical-development path.

Known published targets can serve as validation controls but cannot be promoted as novel findings.

If no candidate passes, `EXHAUSTION.md` will enumerate candidate failures and preserve usable translational leads without overstating them.

## Statistics And Reproducibility

- Fixed random seed for all new stochastic analysis: `20260526`.
- Donor/region, not cells, is the biological replication unit.
- Spatial permutation tests will permute neighbor identities within donor-region while preserving cell counts and coordinate geometry.
- FDR control: Benjamini-Hochberg across tested candidate target/pathway hypotheses in a discovery family; validation tests are separately labelled and corrected if more than one candidate is tested.
- All downloaded inputs must be listed with URL and SHA-256.
- New code will run through a documented therapeutic entry point separate from the completed prior `run_analysis.sh`.

## Major-Step Critique Schedule

After approximately twelve substantive actions (data/tool acquisition, candidate selection decisions, inference steps, or translation checks), append a hostile-review entry to `CRITIQUE.md`. Each unresolved criticism blocks a final positive claim.

