# GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17

Date: 2026-06-06

## Purpose

Resolve the MS-UC chr1 causal-gene ambiguity between `GPR25` and `KIF21B`.

Computational V17 evidence is not sufficient for an intervention-grade claim:

- `GPR25` has stronger eQTL signal in the disease-shared block and a plausible
  CXCL17-GPR25 ligand axis, but weak transcript-level cell-state support.
- `KIF21B` has better single-cell expression support but weak direct
  druggability.

## Experiment 1: Genotype-Linked Protein and Transcript Mapping

Samples:

- MS cases: `n = 60`, enriched for the chr1 shared-locus risk/protective
  genotype balance.
- Matched controls: `n = 60`.
- If available, add CSF immune cells or CNS-infiltrating lymphocyte material
  from `n >= 20` MS donors.

Cell populations:

- CD4 T cells.
- CD8 T cells, including tissue-residency markers where possible.
- B cells.
- Monocytes/dendritic cells.
- CSF lymphocytes if material is available.

Readouts:

- CITE-seq or flow cytometry for GPR25 surface protein.
- Targeted RNA or single-cell RNA for `GPR25` and `KIF21B`.
- Genotype at the chr1 shared credible-set variant or best proxy.

Primary decision rule:

- GPR25-supported outcome: protective genotype associates with higher GPR25
  surface protein or transcript in a defined immune/CSF subset with
  `|log2FC| >= 0.25` and FDR `< 0.10`.
- KIF21B-supported outcome: GPR25 has no genotype-linked expression, while
  KIF21B shows genotype-linked expression in the relevant immune subset with
  `|log2FC| >= 0.25` and FDR `< 0.10`.
- Unresolved outcome: neither gene shows genotype-linked expression in any
  accessible subset.

Stop-loss:

- If `n >= 20` genotype-balanced donors per group shows no GPR25 signal
  (`|log2FC| < 0.25`) and no KIF21B signal (`|log2FC| < 0.25`) in all tested
  immune subsets, do not continue public transcript mining. Seek tissue-specific
  QTL data or downgrade the locus to unresolved causal gene.

## Experiment 2: CXCL17-GPR25 Functional Assay

Only run if Experiment 1 identifies GPR25 protein or transcript in a subset.

Perturbations:

- CXCL17 stimulation.
- GPR25 blocking antibody or knockdown if a validated reagent is available.
- Optional GPR25 overexpression/restoration in risk-genotype cells.

Readouts:

- Chemotaxis or migration toward CXCL17.
- RhoA activation.
- Integrin activation/adhesion.
- Tissue-residency or trafficking marker induction.

Primary decision rule:

- GPR25 mechanism supported if protective-genotype or GPR25-high cells show a
  reproducible CXCL17-directed migration/RhoA/integrin phenotype with
  standardized effect size `>= 0.5`, and GPR25 perturbation reduces the effect
  by at least `30%`.

Falsification:

- GPR25 is detectable but CXCL17 responses are genotype-independent and
  GPR25-perturbation-insensitive.

## Experiment 3: KIF21B Functional Branch

Only run if Experiment 1 points to KIF21B or if GPR25 fails.

Perturbations:

- KIF21B knockdown or CRISPRi in the implicated immune subset.
- Include a microtubule/cytoskeletal positive-control perturbation.

Readouts:

- Cell migration and synapse/adhesion phenotypes.
- Antigen-presentation or activation-state markers if the subset is APC-like.
- Viability and proliferation, because broad cytoskeletal disruption can create
  non-specific toxicity.

Primary decision rule:

- KIF21B mechanism supported if perturbation shifts immune-cell migration,
  adhesion, or activation in the direction predicted by protective genotype
  without broad toxicity.

Translational implication:

- If KIF21B wins, the locus is likely mechanism/biomarker biology rather than a
  direct drug target unless a selective modality is identified.

## Current Project Decision

Do not claim a GPR25 intervention hypothesis before Experiment 1 and, ideally,
Experiment 2. The current V17 result is a prioritized experimental branch:

1. Test whether the protective genotype raises GPR25 protein in a real immune
   subset.
2. If yes, test whether GPR25 controls CXCL17-directed migration or residency.
3. If no, resolve whether KIF21B explains the locus despite weak direct
   druggability.
