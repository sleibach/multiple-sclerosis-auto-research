# Hypothesis Selection

**Date:** 2026-05-26  
**Selection:** Execute a constrained, human-tissue test of prior **Hypothesis 3**: whether an adaptive immune activation/costimulation program co-occurs with the lipid-stressed, complement-rich microglial state in chronic active multiple sclerosis (MS) lesions.

## Why This Hypothesis

The prior hypothesis stated that EBV-conditioned B/T-cell interactions may drive lesion-rim lipid-stressed microglia through interferon and complement signalling. Public data cannot presently establish the EBV-conditioning step in progressive human lesion tissue: the available chronic active lesion atlases do not measure viral infection or EBV-specific receptor clonotypes. They can, however, test a necessary intermediate claim: whether the proposed adaptive-cell and microglial effector programs coexist and quantitatively track each other in human lesions.

This analysis focuses on the `TNFSF9`/`TNFRSF9` (4-1BBL/4-1BB) costimulatory axis because:

1. Laderach et al. reported `TNFSF9` expression in EBV-driven CNS-homing B-cell data and inflammatory T-cell recruitment in a humanized-mouse system.
2. `TNFRSF9` marks activated T cells and provides a concrete adaptive-cell interface that can be queried in human lesion transcriptomes.
3. The axis offers an experimentally perturbable candidate upstream of the lesion-rim CD8/microglial niche.

## Datasets Available for Execution

| Role | Accession | System | Why usable |
|---|---|---|---|
| Cell-resolved discovery | `GSE180759` | snRNA-seq from chronic active/inactive lesions, periplaque white matter, and control white matter; 5 progressive MS and 3 control autopsy donors | Processed expression matrix and annotations are publicly downloadable in manageable files; provides cell-state localization. |
| Independent tissue-level validation | `GSE279972` | Bulk RNA-seq of white-matter lesions and surrounding tissue from 28 MS and 10 control donors | Public, compact raw/processed text archive; independent cohort with foamy-microglia and B-infiltration lesion biology. |
| Mechanistic context only, not primary evidence | `GSE299939` / Zenodo `10.5281/zenodo.15602185` | EBV-infected humanized-mouse B-cell scRNA/BCR data from Laderach et al. | It motivates the costimulatory target but cannot validate a human MS lesion claim and its processed object is large R/Seurat format. |

## Why Not The Other Prior Hypotheses

| Prior hypothesis | Decision |
|---|---|
| Hypothesis 1: CSF EBV-imprinted state predicts paramagnetic rim lesions | Not executable as posed: no located public dataset pairs EBV-imprinted CSF immune measurements with longitudinal paramagnetic rim lesion MRI outcomes. |
| Hypothesis 2: EBV programs BBB-migratory B cells through `EBNA2/TBX21/CXCR3` | A meaningful causal test requires perturbation or comparable infected/control B-cell data; public data can replicate model observations but not test migration causally in humans. |
| Hypothesis 4: CNS EBV reservoir versus virus-negative imprinting | Public transcriptomes are not an adequate orthogonal viral-detection experiment; absence of viral RNA in sparse single-nucleus data would be non-informative. |

## Expected Information Gain

A reproducible positive result would nominate a specific costimulatory circuit for spatial/protein validation and perturbation in chronic lesions. A negative result would reduce priority for the 4-1BB axis as the adaptive-to-microglial bridge, while not rejecting EBV initiation or other adaptive signals such as interferon/complement.

## Honest Scope Boundary

This execution can establish an **association of transcriptomic programs in human MS tissue**. It cannot show that EBV caused the program, that the cells physically interact without spatial/protein follow-up, or that blocking the axis would benefit patients.
