# KIF21B Restoration Modality Specification V52

Date: 2026-07-10

Status: future evidence gate. KIF21B remains a serious chr1 causal-biology
candidate but not an intervention-grade MS target.

## Current State

KIF21B has stronger direction-aware genetics than many closed leads, but the
therapeutic direction is hard:

- V17/V19 support KIF21B colocalization in chr1 follow-up.
- V19 QTD000021 exact shared credible-set direction indicates MS and UC risk
  alleles lower KIF21B expression in `11 / 11` exact shared SNPs.
- V52 AlphaFold context shows the motor/binding-site region is structurally
  interpretable.
- The likely protective direction is higher/restored KIF21B expression or
  function, not loss-of-function.

## Why Standard Targeting Is Wrong-Direction

The easy modalities are the wrong ones unless future data prove otherwise:

| modality | default V52 interpretation |
|---|---|
| Small-molecule motor inhibition | likely wrong-direction if protective biology requires more KIF21B function |
| Degrader | likely wrong-direction |
| ASO / siRNA knockdown | likely wrong-direction |
| Broad microtubule perturbation | too nonspecific for MS target work |
| Expression restoration / function rescue | direction-compatible in principle, but currently not demonstrated |

## Required Evidence

KIF21B can move toward target workup only if future data support:

| gate | required evidence | acceptable form |
|---|---|---|
| Causal-gene resolution | KIF21B must be the winning gene over GPR25/local alternatives. | Genotype-linked expression/protein or full QTL colocalization in MS-relevant cells. |
| Relevant cell state | The KIF21B genotype effect must appear in an immune, CSF, or CNS-adjacent state tied to MS biology. | Single-cell, sorted-cell, or protein data with genotype labels and covariates. |
| Protective direction | Protective alleles must increase or restore KIF21B state/function. | Allele-dosage effect on RNA/protein/function with harmonized direction. |
| Restoration feasibility | There must be a plausible way to raise or normalize KIF21B function safely. | CRISPRa/overexpression proof-of-concept, state-correction mechanism, or validated pathway modulation. |
| Phenotype readout | Restoring KIF21B must move an MS-relevant phenotype protectively. | Perturbation readout in relevant immune/CNS-adjacent cell context. |

## What Does Not Count

Do not reopen KIF21B based on:

- motor-domain pLDDT or binding-site confidence alone;
- generic kinesin ligandability;
- inhibitors, degraders, ASO, or siRNA without proof that lowering KIF21B is
  protective;
- peripheral blood eQTL direction without MS-relevant cell-state context;
- broad cytoskeletal phenotypes with no disease-layer link.

## Minimal Future Experiment

The most efficient future package:

1. Genotype-linked immune and, if possible, CSF single-cell expression/protein
   for the chr1 haplotype.
2. Cell-type-specific test of KIF21B RNA/protein direction versus GPR25 and
   local alternatives.
3. Direction-matched perturbation:
   - CRISPRa or overexpression as a restoration proxy;
   - pathway/state correction that increases KIF21B-associated function;
   - only test inhibition/knockdown as a negative or wrong-direction control.
4. Readouts tied to immune-cell migration, activation, antigen-presentation
   context, or another pre-specified MS-relevant phenotype.

## Decision Rule

KIF21B becomes "worth dedicated target workup" only if:

1. KIF21B is causally resolved over local alternatives.
2. The protective direction is higher/restored KIF21B state or function.
3. Restoration moves an MS-relevant phenotype in the protective direction.
4. A plausible restoration/up-function modality exists.

Until those hold, KIF21B should remain a controlled-data biology lead and a
direction-discipline example, not a wet-lab target program.
