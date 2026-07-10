# Structure-Aware No-Go / Reopen Table V52

Date: 2026-07-10

Status: synthesis and target-discipline control. This document uses AlphaFold
DB structural context to sharpen target triage, but predicted structures remain
context only and do not create project-grounded therapeutic evidence.

## Rule

Structure can answer "is there a structurally interpretable protein region?"
It cannot answer "is this the causal MS gene?", "which direction is protective?",
or "is the modality safe and disease-matched?"

Therefore a lead remains no-go if its blocker is genetics direction, causal-gene
uncertainty, missing cell-state support, or absent direction-matched modality.

## Table

| lead | structural context | why still no-go | reopen trigger |
|---|---|---|---|
| GPR25 | AlphaFold DB `AF-O00155-F1` v6: receptor-like core confidence is high; seven-transmembrane structural context is plausible. | Causal gene remains unresolved against KIF21B/local alternatives; MS cell-state support is weak; chemistry is immature; required direction is agonism/restoration, not generic antagonism. | Genotype-linked immune/CSF expression or protein data showing protective haplotype raises GPR25 in a relevant cell state, plus perturbation or ligand evidence that agonism/restoration moves an MS-relevant phenotype protectively. |
| KIF21B | AlphaFold DB `AF-O75037-F1` v6: full-length confidence is mixed but motor/binding-site regions are interpretable. | Genetics-facing direction requires restoration/up-function; conventional kinesin inhibition, degradation, ASO, or siRNA likely move wrong-direction. Causal-gene and cell-state support still need controlled data. | Genotype-linked data resolving KIF21B as causal in an MS-relevant cell state, plus a plausible restoration/up-function modality and perturbation evidence. |
| PTGER4 | AlphaFold DB `AF-P35408-F1` v6: receptor-core context is compatible with EP4/GPCR tractability; long C-terminal region is low-confidence. | PTGER4 closure is driven by mixed shared/distinct genetic signal and disease-direction conflict, not lack of a receptor fold. Structural tractability cannot rescue a wrong or ambiguous disease signal. | Signal-specific fine-mapping/QTL that separates shared and distinct components, resolves an MS-protective PTGER4 direction, and identifies a safe EP4 modulation direction. |
| ZMIZ1 | No V52 AlphaFold triage needed for target promotion. | The lead is an opposite-direction MS/Crohn transfer-warning locus and is not directly druggable on current evidence. Structure would not solve direction or modality. | MS-specific genotype-linked expression/protein direction, perturbation evidence, and a plausible modality. |

## Practical Interpretation

- **Do not promote by target class.** GPCR, motor-domain, or predicted-structure
  presence is insufficient.
- **Do not promote by external context.** Literature or database agreement can
  corroborate caution but cannot replace project-grounded direction evidence.
- **Do not promote by AlphaFold confidence.** High pLDDT regions can guide
  feasibility thinking; they cannot validate disease relevance.
- **Do promote only with direction-matched biology.** A tractable target is one
  where causal gene, cell state, protective direction, and modality all align.

## Consequence For V52 Therapeutic Path

The no-go table supports the V52 headline: the near-term actionable route is
validation of the monitoring/stratification lead. Target-level work should wait
for controlled genotype-linked and perturbation data, especially around chr1.
