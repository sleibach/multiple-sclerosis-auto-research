# GPR25 Direction-Matched Modality Specification V52

Date: 2026-07-10

Status: future evidence gate. GPR25 remains a conditional causal-biology
candidate, not an intervention-grade MS target.

## Current State

GPR25 is structurally plausible and genetically interesting, but not actionable:

- V16/V19 support a protective-higher-expression interpretation for the chr1
  GPR25 signal in blood eQTL contexts.
- V18/V19 later public immune-QTL and cell-state checks weakened GPR25 as a
  clean causal-gene assignment relative to local alternatives.
- V51 AlphaFold context supports a GPCR-like receptor core, but structure does
  not resolve disease causality, ligand biology, or direction.
- V52 keeps GPR25 below target-grade because the required direction is
  restoration/agonism and the chemical/functional biology is immature.

## Direction-Matched Modality Requirement

GPR25 can move toward target workup only if the future evidence supports this
chain:

`protective haplotype -> higher/recovered GPR25 state -> protective immune
phenotype -> plausible agonism/restoration modality`

Each arrow must be tested; none can be assumed from GPCR target class.

## Required Evidence

| gate | required evidence | acceptable form |
|---|---|---|
| Causal-gene resolution | GPR25 must beat KIF21B/local alternatives for the disease-relevant signal. | Genotype-linked expression/protein or fine-mapping/QTL data with ancestry, LD, and effect-direction fields. |
| Cell-state presence | GPR25 must be present in a relevant immune/CSF cell state at RNA and preferably protein level. | Single-cell RNA plus protein/CITE/flow/targeted assay, with enough cells by genotype group. |
| Protective direction | The protective haplotype must raise or restore the GPR25 state in that cell context. | Allele/dosage association with expression/protein or activity readout. |
| Functional readout | Increasing GPR25 signaling must move an MS-relevant phenotype protectively. | Ligand, overexpression, CRISPRa, or other restoration perturbation in a relevant model. |
| Modality feasibility | A safe way to raise/restored GPR25 function must exist. | Agonist, positive allosteric modulator, ligand/deorphanization route, or validated restoration technology. |

## What Does Not Count

Do not promote GPR25 based on:

- GPCR class membership;
- AlphaFold receptor-core confidence;
- target-database presence;
- association without direction;
- an antagonist/inhibitor-like modality when the genetics suggests restoration;
- generic immune-cell expression without genotype-linked effect;
- ligand activity in a non-relevant cell system without MS-relevant phenotype.

## Minimal Future Experiment

The most efficient future package:

1. Genotype-stratified immune/CSF single-cell dataset covering the chr1
   haplotype, with `GPR25`, `KIF21B`, and local-gene expression.
2. Orthogonal protein or surface-readout attempt for GPR25 where technically
   feasible.
3. Small perturbation panel in the cell state where genotype links GPR25 to the
   protective direction:
   - agonist or ligand candidate if available;
   - positive allosteric modulation if available;
   - CRISPRa/overexpression as a mechanistic restoration proxy.
4. Readouts tied to MS-relevant immune remodeling rather than generic viability.

## Decision Rule

GPR25 becomes "worth dedicated target workup" only if:

1. GPR25 is the best-supported causal gene for the relevant chr1 signal.
2. The protective direction is higher/restored GPR25 in an MS-relevant cell
   state.
3. A restoration/agonism perturbation moves the phenotype in the protective
   direction.
4. A plausible therapeutic modality can implement that direction.

If any element is missing, GPR25 remains a controlled-data handoff and should
not receive wet-lab target-prioritization budget as an MS therapeutic.
