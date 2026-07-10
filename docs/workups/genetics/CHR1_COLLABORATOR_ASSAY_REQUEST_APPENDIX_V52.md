# chr1 Collaborator Assay Request Appendix V52

Date: 2026-07-10

Status: collaborator-facing request appendix. This document adds no evidence,
does not reopen chr1 as a target, and does not change the V19/V52 verdict. It
translates the chr1 data specification into concrete assay and metadata asks.

## Purpose

The chr1 KIF21B/GPR25 locus is the closest biology-to-target bridge, but it
remains closed for therapeutic promotion because the project lacks a complete
direction-matched chain:

`genotype -> causal gene -> cell state -> protective direction -> perturbation
phenotype -> feasible modality`

This appendix is the practical request to a collaborator who may have or could
generate the missing data.

## Preferred Package

| component | preferred assay | minimum acceptable substitute | decision it supports |
|---|---|---|---|
| Genotype | direct genotype or high-quality imputed dosage for V17/V19 chr1 credible-set variants | tag SNPs with imputation quality, ancestry-specific LD, and reference panel | protective haplotype and allele direction |
| Cell-state RNA | single-cell RNA-seq in PBMC plus, if possible, CSF immune cells | sorted-cell RNA-seq in T, B, monocyte/APC, NK, and myeloid subsets | causal gene and relevant cell state |
| Protein / surface state | CITE-seq or targeted protein readout where technically feasible | validated flow/CyTOF panel for cell state and candidate-associated phenotype | whether RNA signal is actionable at protein/state level |
| Perturbation | direction-matched perturbation after genotype result identifies the winning gene | archived ligand/CRISPRa/overexpression/knockdown data with direction recorded | whether moving the candidate changes an MS-relevant phenotype |
| Metadata | ancestry PCs, batch/QC, treatment, steroid, relapse, infection, disease activity/stage | enough covariates to separate genotype effects from technical and immune-tone structure | interpretability and no-go checks |

## Required Genotype Targets

Please include direct or high-quality imputed dosage for:

- `rs12132349`
- `rs55838263`
- `rs7554511`
- the V19 KIF21B exact shared credible-set variants used in the QTD000021
  direction check
- any local fine-mapping variants used by the collaborator that tag the same
  LD block

If direct variants are unavailable, provide:

1. imputation quality per variant;
2. reference panel;
3. ancestry labels or genotype PCs;
4. LD mapping to the requested variants.

## Candidate Genes To Report

Do not report only the collaborator's favored gene. The package must support a
local comparison among:

- `GPR25`
- `KIF21B`
- `C1orf106/INAVA`
- nearby chr1 local genes with measurable RNA/protein in the assayed cells

For each gene, report whether it is detected, in which cell states, and whether
genotype dosage changes RNA or protein abundance.

## Cell-State Coverage

Minimum useful immune coverage:

| compartment | why needed |
|---|---|
| CD4 T cells and activated/memory subsets | plausible immune-state readout for KIF21B/GPR25 biology |
| CD8 T cells | comparator lymphocyte context |
| B cells / plasmablasts if present | distinguish lymphocyte-specific from broad immune effects |
| monocytes/APC/myeloid subsets | test whether chr1 effects intersect the APC/HLA monitoring biology |
| NK cells | control for broad cytotoxic/lymphocyte composition effects |
| CSF immune cells if available | higher MS relevance than peripheral-only blood |

Report cell counts per subject, per genotype group, and per compartment so
underpowered cell states are not overinterpreted.

## Perturbation Request

Only run or interpret perturbations after the genotype-linked molecular result
identifies a candidate gene and protective direction.

| candidate | useful perturbation | wrong-direction perturbation unless genetics proves otherwise |
|---|---|---|
| GPR25 | agonist, positive allosteric modulation, ligand/deorphanization assay, CRISPRa/overexpression restoration proxy | antagonist, receptor knockdown, or loss-of-function |
| KIF21B | CRISPRa, expression/function restoration, state-correction proxy | kinesin inhibition, degradation, ASO, siRNA, or knockdown |

Useful readouts should be pre-specified and tied to an MS-relevant phenotype,
such as immune-cell migration, activation state, antigen-presentation context,
tissue-residency behavior, or another collaborator-justified chr1 mechanism.

## Metadata Checklist

| metadata | required level |
|---|---|
| subject ID | links genotype, assay, phenotype, and metadata |
| disease/control/comparator label | MS-specificity and comparator interpretation |
| ancestry/genotype PCs | required for genotype-direction interpretation |
| treatment status and timing | separates baseline genetics from therapy response |
| relapse/steroid/infection timing | prevents immune-tone or acute-inflammation artifacts |
| disease stage/activity | relapsing/progressive or active/inactive context |
| batch/QC metrics | required before any direction claim |
| sample source | PBMC, sorted blood, CSF, lesion-adjacent, or other |

## Package Classifications

| received package | classification | allowed interpretation |
|---|---|---|
| genotype + cell-state RNA/protein + metadata + direction-matched perturbation | complete chr1 target-development package | can test the full reopen chain |
| genotype + cell-state RNA/protein + metadata, no perturbation | causal-biology package | can resolve gene/cell/direction, not target readiness |
| genotype + bulk RNA only | partial-context package | can screen direction, not cell-state or protein/actionability |
| perturbation without genotype-linked direction | non-counting target context | cannot reopen chr1 |
| structure or class tractability only | non-counting target context | cannot reopen chr1 |
| missing ancestry, batch, or genotype-quality fields | incomplete | no direction conclusion |

## Sendable Request Text

Please provide chr1 genotype-linked immune or CSF molecular data for the
KIF21B/GPR25 locus, including direct or high-quality imputed dosage for the
requested chr1 credible-set variants, cell-state-resolved RNA and preferably
protein readouts for GPR25, KIF21B, C1orf106/INAVA, and local genes, ancestry
PCs, treatment/steroid/relapse/infection metadata, batch/QC metrics, and any
direction-matched perturbation readouts. The key decision is whether the
protective haplotype acts through GPR25, KIF21B, both, or another local gene in
an MS-relevant cell state, and whether the protective direction can be
implemented by a plausible modality.

## Source Artifacts

- `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`
- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`
- `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`
