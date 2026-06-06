# Therapeutic Discovery Tool Inventory

**Date:** 2026-05-26  
**Principle:** Use genuinely different data/analysis classes. A candidate surviving several transcript correlations is not convergence.

## Human Disease Compartment Data

| Resource | Planned role | Feasibility/status |
|---|---|---|
| GEO `GSE284005` | Human MERFISH spatial transcriptomics in chronic-active MS lesions; identify actionable genes/pathways in pathological neighborhoods and spatial proximity to immune cells. | Public; `RAW.tar` is 31.4 MB and feasible. |
| GEO `GSE301908` | Paired human snRNA-seq atlas from 14 MS and 3 controls; cell-state annotation/reference for MERFISH interpretation if accessible without excessive preprocessing. | Public; processed RDS is 1.3 GB and raw archive 1.8 GB. Use only if necessary and resource-justified; first inspect authors' code/metadata. |
| GEO `GSE279972` + Zenodo `10.5281/zenodo.19352263` | Independent human white-matter multi-omics and lesion morphology/progression resource: transcriptome, proteome, lipidome, chemical proteomics, histological labels. | Already downloaded; computationally feasible. |
| GEO `GSE180759` | Older independent human chronic-active lesion snRNA-seq; targeted independent validation where sufficient cell counts exist. | Already downloaded; useful for target expression, not sparse cell-cell spatial claims. |
| GEO `GSE301696` / `GSE301824` | IFN-gamma/myelin microglia culture MERFISH and EAE scRNA data from Feng et al.; test whether candidate pathway changes in experimentally induced/treated pathology when accessible. | Public; use after candidate nomination if files are manageable. |

## Spatial And Single-Cell Analysis

| Tool/method | Planned role |
|---|---|
| `pandas`, `numpy`, `scipy`, `statsmodels` | Reproducible processing, donor-aware tests, permutation/bootstrap inference. |
| `scanpy` / `anndata` / `h5py` if needed | Read sparse H5 single-cell inputs and annotate/query relevant cell states. Install only if the RDS/raw path is needed. |
| Custom spatial neighborhood permutation | Test enrichment of candidate-positive microglia near immune cells within each donor/region while preserving cell abundance. Required to avoid bulk proxy-satisficing. |
| Marker-based annotation checked against authors' code | Only if deposited MERFISH raw files lack labels. Any de novo label must be validated against deposited signature/annotation information before mechanistic claims. |

## Multi-Omics And Cross-Disease Transfer

| Resource | Planned role |
|---|---|
| Van der Vliet deposited workbook | Quantify lipid/protein/transcript relationships for candidate pathways in foamy versus non-foamy lesions and available progression metadata. |
| Feng full text/supplementary data | Identify already validated targets (`DHCR24`/sterol efflux) and avoid relabelling published findings as discovery. |
| Parkinson/Gaucher/lysosomal literature and clinical datasets | Evaluate lysosomal rescue candidates such as GCase chaperoning only if MS data reveal the relevant substrate/stress mechanism. |
| Alzheimer/aging microglial literature | Evaluate lipid-droplet, lysosome, inflammasome, and CNS PK precedents; treat analogies as supporting or rejecting evidence, not MS proof. |

## Target And Drug Intelligence

| Resource | Planned role | Notes |
|---|---|---|
| ChEMBL REST API | Retrieve target-compound bioactivities and clinical phase for nominated targets. | Primary source for chemical matter. |
| Open Targets Platform/API | Retrieve disease-target evidence and known drug programs. | Use to identify existing MS claims and avoid novelty inflation. |
| DGIdb / Pharos where accessible | Secondary druggability and interaction lookup. | Confirmation only. |
| PubChem / DrugBank-public records | Chemical identity, approved indication, referenced pharmacology. | DrugBank use limited to publicly visible content. |
| ClinicalTrials.gov API | Determine existing MS/progressive-MS trials for compound or target. | Mandatory for final candidate. |

## Perturbational And Genetics Resources

| Resource | Planned role | Pivot condition |
|---|---|---|
| LINCS/CMap or accessible signature API/processed dataset | Ask whether candidate intervention reverses the human lesion cell-state signature in an appropriate myeloid/glial context. | Do not use cancer-cell reversal alone as central evidence; report unusable context if only unrelated lines exist. |
| GWAS Catalog / Open Targets genetics | Check whether nominated target/pathway is supported by MS risk genetics or progression-associated genetics. | Lack of genetics is not fatal for a state-driven somatic lesion target, but must be explicit. |
| GTEx / Human Protein Atlas / single-cell expression atlases | Assess tissue expression and off-target risk of candidate target. | Required for safety/druggability interpretation where available. |

## Structure And Medicinal Chemistry

| Tool/resource | Planned role | Guardrail |
|---|---|---|
| PDB / AlphaFold Database | Verify structural tractability of a nominated protein target if small-molecule or antibody modality is proposed. | No new structure prediction will be represented unless actually executed. |
| RDKit | Compound descriptor, BBB-likeness heuristics, structural deduplication after a candidate exists. | Heuristics do not replace measured CNS exposure. |
| ChEMBL/primary PK literature | Verify achieved CNS/CSF exposure relative to biochemical potency. | Required for a drug-repurposing claim. |
| Docking tools | Not planned as evidence by default. | Docking will not be used to rescue a weak biological target or substitute for known pharmacology. |

## Novelty And Prior Art

| Resource | Required search |
|---|---|
| PubMed and Europe PMC full text | Compound/target + MS/progressive MS/lesion/PRL/microglia; mechanism-specific queries. |
| bioRxiv and medRxiv | Same, including preprints and biomarker/trial proposals. |
| ClinicalTrials.gov | Target/compound/alias and MS/progressive MS. |
| Google Patents | Compound/target with multiple sclerosis, demyelination, microglia, remyelination, lesion terms. |
| Espacenet | Same patent-family verification where accessible. |

## Compute Envelope

- Local machine observed: Apple arm64, Python `3.13.3`, 48 GiB RAM, approximately 155 GiB free disk.
- Acceptable downloads: public files up to several GB only where they materially enable a spatial or cell-state test.
- No GPU-dependent model training or de novo protein structure prediction is planned.
- If spatial annotations cannot be recovered from the public resource without an unjustified reannotation, the target line will be marked blocked or restricted to robust measured endpoints.

