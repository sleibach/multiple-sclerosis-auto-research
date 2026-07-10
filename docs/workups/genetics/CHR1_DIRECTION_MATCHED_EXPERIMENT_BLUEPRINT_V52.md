# chr1 Direction-Matched Experiment Blueprint V52

Date: 2026-07-10

Status: future experiment blueprint. This document does not reopen chr1 as a
target. It specifies the staged evidence needed before GPR25 or KIF21B could
move from controlled-data handoff to dedicated target workup.

## Purpose

V52 identifies chr1 KIF21B/GPR25 as the closest biology-to-target bridge, but
not intervention-grade. The missing evidence is a complete direction-matched
chain:

`credible-set genotype -> causal gene -> relevant cell state -> protective
direction -> perturbation phenotype -> feasible modality`

This blueprint defines the minimum staged experiment to test that chain.

## Stage 0: Package Intake And Locks

| requirement | action |
|---|---|
| Data package arrives | Record path, file sizes, checksums, assay type, and access terms before analysis |
| Genotypes present | Verify dosage/imputation quality for V17/V19 chr1 credible-set variants |
| Molecular data present | Verify expression/protein readout for `GPR25`, `KIF21B`, `C1orf106/INAVA`, and local alternatives |
| Metadata present | Verify ancestry PCs, batch/QC, treatment, steroid, relapse, infection, disease activity/stage |
| Perturbation data present | Verify perturbation direction and phenotype readout before viewing target-favorable results |

If any required field is absent, classify the package as partial and run only
the subset of analyses it can support. Do not infer missing direction from
prior preference.

## Stage 1: Causal-Gene Resolution

Primary test:

1. Model genotype dosage against RNA/protein for local candidates by cell state.
2. Include ancestry PCs, batch/QC, treatment, steroid/relapse/infection
   metadata where available.
3. Compare `GPR25`, `KIF21B`, `C1orf106/INAVA`, and other local genes rather
   than testing one favorite.

Decision:

| outcome | consequence |
|---|---|
| One candidate clearly wins in an MS-relevant cell state | Continue to Stage 2 for that gene |
| Multiple local genes move together | Keep chr1 as locus biology; no target workup |
| No candidate shows a relevant genotype-linked effect | Keep chr1 closed for target workup |
| Effect is ancestry/batch/treatment-confounded | Require replication or better covariates before any promotion |

## Stage 2: Protective Direction

For the winning candidate, harmonize allele direction to the V17/V19 disease
effect convention.

| candidate | required protective direction |
|---|---|
| GPR25 | protective haplotype raises or restores GPR25 state/activity |
| KIF21B | protective haplotype raises or restores KIF21B expression/function |
| Other local gene | define direction from harmonized disease and molecular effect before any modality assessment |

If the candidate's feasible modality would move opposite the protective
direction, stop. That is a wrong-direction result, not a therapeutic lead.

## Stage 3: Cell-State And Protein Presence

Required:

1. The genotype-linked effect must occur in a plausible MS-relevant immune, CSF,
   or CNS-adjacent cell state.
2. RNA presence alone is acceptable for causal-gene resolution, but target
   promotion needs protein or functional-state support where technically
   feasible.
3. The signal must survive broad immune-tone and cell-composition checks.

Decision:

| outcome | consequence |
|---|---|
| Direction appears in relevant cell state and protein/function is detectable | Continue to Stage 4 |
| Direction appears only in a generic or irrelevant cell state | Keep as biology, not target |
| RNA exists but protein/function is unmeasurable | Queue assay-development need; no promotion |
| Signal collapses under composition or immune-tone adjustment | Keep closed for target workup |

## Stage 4: Direction-Matched Perturbation

Run perturbations only after Stages 1-3 identify a candidate and direction.

| candidate | positive perturbation | wrong-direction controls |
|---|---|---|
| GPR25 | agonist, positive allosteric modulation, ligand/deorphanization route, CRISPRa/overexpression restoration proxy | antagonist or loss-of-function unless genetics proves lowering is protective |
| KIF21B | CRISPRa, overexpression, state-correction, or function-rescue proxy | inhibition, degradation, ASO, siRNA, or knockdown unless genetics proves lowering is protective |

Readouts must be pre-specified and MS-relevant, such as immune-cell migration,
activation, antigen-presentation context, tissue-residency behavior, or another
explicit phenotype tied to the chr1 mechanism.

Decision:

| perturbation result | consequence |
|---|---|
| Direction-matched perturbation moves phenotype protectively | Continue to Stage 5 |
| Perturbation has no relevant effect | Keep closed pending better model |
| Perturbation moves phenotype adversely | Close target route for that modality |
| Only wrong-direction modality is feasible | Keep closed despite structural tractability |

## Stage 5: Modality Feasibility

Before target promotion, the project needs a plausible therapeutic modality
that can implement the protective direction.

| candidate | modality requirement |
|---|---|
| GPR25 | agonism/restoration route with enough ligand biology or tool compound quality to test specificity |
| KIF21B | restoration/up-function or state-correction route; generic kinesin inhibition is not acceptable |
| PTGER4-like receptor fallback | signal-specific MS-protective direction plus safe EP4 modulation direction |

## Final Decision Classes

| class | criteria | action |
|---|---|---|
| `TARGET_WORKUP_READY` | Stages 1-5 all pass | Start dedicated target workup with locked direction and modality |
| `BIOLOGY_ONLY` | Causal biology holds but cell-state, perturbation, or modality fails | Keep as mechanism, not target |
| `WRONG_DIRECTION` | feasible intervention moves opposite protective direction | Do not pursue as therapeutic target |
| `DATA_INCOMPLETE` | package lacks fields for key stages | Request missing fields; no inference |
| `CLOSED` | causal gene/direction not supported or perturbation fails | Record null and do not rescue with structure |

## Source Artifacts

- `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`
- `docs/reports/THERAPEUTIC_PATH_V52.md`
