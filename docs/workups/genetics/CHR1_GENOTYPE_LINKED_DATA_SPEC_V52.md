# chr1 KIF21B/GPR25 Genotype-Linked Data Specification V52

Date: 2026-07-10

Status: future data-acquisition specification. This document does not reopen
the chr1 lead, change the V19 verdict, or create a therapeutic target claim.

## Purpose

V52 concludes that chr1 KIF21B/GPR25 is the closest biology-to-target bridge,
but still not intervention-grade. The missing evidence is no longer generic
association. The missing evidence is genotype-linked, cell-state-resolved
direction and perturbation.

This specification defines the minimum dataset that would make a future chr1
re-examination decision-useful.

## Decision To Be Resolved

The future dataset must answer three questions:

1. **Causal gene:** does the protective/risk haplotype act primarily through
   `GPR25`, `KIF21B`, both, or another local gene?
2. **Relevant cell state:** in which MS-relevant immune or CNS-adjacent cell
   subset is the genotype-linked effect visible?
3. **Therapeutic direction:** does the protective direction require increased
   GPR25 signaling, increased KIF21B expression/function, or a different
   modality?

Without all three, the lead remains a controlled-data handoff rather than a
target.

## Required Sample Fields

| field | required | reason |
|---|---|---|
| Subject identifier | yes | link genotype, expression/protein, phenotype, and metadata |
| MS/control/comparator status | yes | distinguish MS-specific effects from generic immune eQTLs |
| Disease stage / activity | strongly preferred | test relapsing/progressive or active/inactive context |
| Treatment status and timing | yes | separate baseline genetics from DMT pharmacodynamics |
| Steroid / relapse / infection metadata | strongly preferred | avoid immune-tone confounding |
| Ancestry or genotype PCs | yes | prevent LD/eQTL direction artifacts |
| Batch/QC metadata | yes | separate genotype effects from technical structure |

## Required Genotype Fields

The dataset must include direct genotypes or high-quality imputation for the
V17/V19 chr1 credible-set variants, including at minimum:

- `rs12132349`
- `rs55838263`
- `rs7554511`
- the V19 KIF21B exact shared credible-set variants used in the QTD000021
  direction check

If only tag SNPs are available, the dataset must provide imputation quality,
reference panel, and LD ancestry information sufficient to map to the project
credible set.

## Required Molecular Readouts

At least one of the following is required; more is better:

| readout | minimum requirement | why |
|---|---|---|
| Single-cell RNA-seq | enough cells per genotype group in T, B, monocyte/APC, NK, and relevant rare subsets to test `GPR25`, `KIF21B`, `C1orf106/INAVA`, and local genes | resolves cell-state and gene-direction ambiguity |
| Sorted-cell bulk RNA-seq | sorted immune subsets with genotype labels | less granular but still direction-informative |
| CITE-seq / surface protein | markers for immune subsets plus any available GPR25-compatible protein assay | distinguishes RNA-only signal from actionable protein state |
| CSF immune single-cell / protein | genotype-linked CSF immune state if available | higher MS relevance than peripheral-only blood |
| Perturb-seq / CRISPR / ligand perturbation | perturb `GPR25` and/or `KIF21B` in relevant immune model with direction-matched readouts | needed before target promotion |

## Minimum Analyses For A Future Re-Examination

The future analysis should be pre-specified before looking at target results:

1. Map genotype dosage to expression/protein for `GPR25`, `KIF21B`,
   `C1orf106/INAVA`, and nearby genes, stratified by cell type.
2. Test whether the protective haplotype increases or decreases each candidate
   gene in MS-relevant cells.
3. Adjust for ancestry PCs, batch, treatment status, steroid/relapse/infection
   metadata where available, and broad immune-tone modules.
4. Compare blood and CSF/lesion-adjacent readouts if both are available.
5. Require direction consistency with V16/V19 before any druggability inference.
6. If perturbation data exist, test whether moving the candidate gene in the
   genetically protective direction shifts an MS-relevant immune phenotype.

## Reopen Criteria

The chr1 lead can move from "hard-target handoff" to "worth dedicated target
workup" only if all are true:

1. One candidate gene has a genotype-linked effect stronger and more specific
   than local alternatives in an MS-relevant cell state.
2. The effect direction matches the genetically protective direction.
3. The gene product is present at RNA and preferably protein level in the
   relevant cell state.
4. A plausible modality exists for the protective direction:
   - GPR25: agonism/restoration, not generic receptor inhibition.
   - KIF21B: restoration/up-function or state correction, not generic kinesin
     inhibition/degradation/knockdown.
5. Perturbation or orthogonal evidence shows that moving the gene in the
   protective direction changes a relevant immune phenotype.

## No-Go Criteria

Keep chr1 closed as a target route if any of these hold:

- genotype effects are not cell-state specific;
- the strongest effect maps to a non-actionable local gene;
- the protective direction requires a modality with no plausible safe route;
- perturbation moves the relevant phenotype in the wrong direction;
- signal disappears after ancestry, batch, treatment, or immune-tone adjustment.

## Practical Data Ask

The most useful acquisition would be:

> MS and control PBMC plus, ideally, CSF immune single-cell data with genotype
> dosages at the chr1 credible set, treatment/steroid/relapse metadata,
> ancestry PCs, and enough subjects per genotype group to test candidate-gene
> expression direction within T, B, monocyte/APC, and NK compartments.

If perturbation is feasible, prioritize a small direction-matched perturbation
screen only after the genotype-linked expression/protein result identifies a
winning gene and cell state.
