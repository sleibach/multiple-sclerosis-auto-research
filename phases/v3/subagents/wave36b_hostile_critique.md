# Wave36-B: Hostile Critique Of Corrected Resolution Perturbation Branch

Date: 2026-05-27  
Role: hostile critique after the corrected Wave35 perturbation rerun.  
Instruction honored: this report does not claim a finding.

## Verdict

Pivot away from active discovery on the resolution/efferocytosis branch.

The corrected Wave35 rerun fixed a real gene-mapping artifact, but the corrected
result is still negative: 10 datasets, 29 contrasts, 145 module rows, and 0
strict controller-like contrasts. The five "resolution without IFN collapse"
patterns are not therapeutic-controller evidence. They are lesion-state
comparisons, IL10-polarized phagocytic-fraction contrasts, or broad RXR
pharmacology.

The branch can remain as a biomarker/wet-lab comparator panel. It should not
consume more V3 target-discovery cycles unless a new external perturbation
dataset or experiment directly satisfies the gates below.

## Main Operationalization Failure Modes

1. **The mapping correction fixed coverage, not causality.**  
   Wave35 now recovers 28/28 resolution genes and most guardrail genes in the
   Ensembl-indexed mouse datasets. That makes the negative screen more credible,
   but it does not turn module-direction consistency into target causality.

2. **Several Ensembl-indexed count datasets are effectively 77-gene panels.**  
   `dataset_inventory.tsv` reports only 77 genes for `GSE253577`, `GSE325329`,
   `GSE274954`, and `GSE287142` after symbol mapping. For raw-count datasets
   using `log2cpm`, library size is then computed over the mapped module panel,
   not the full transcriptome. That makes the values partly compositional within
   the candidate panel. It is acceptable for a hostile negative screen, but it
   is not acceptable for promoting any subtle candidate or gene-level rescue.

3. **The "resolution" module is not a pure beneficial-resolution module.**  
   It mixes efferocytosis receptors, lipid handlers, complement, anti-
   inflammatory cytokines, tissue macrophage markers, and fibrosis-adjacent
   genes. `APOE`/`LPL` overlap with the lipid/APC module. `TGFB1` appears in
   the resolution and fibrosis guardrail modules. `C1QA/B/C` can mark injury
   burden as much as clearance. A positive module score can mean phagocyte
   abundance, lesion stage, cell selection, repair, fibrosis, or chronic damage.

4. **The contrast gate is direction-only.**  
   Controller calls use fixed thresholds: resolution `>0.25`, lipid/APC
   `<-0.25`, IFN `>-0.75`, stress `<0.50`, profibrosis `<0.50`. The final
   contrast call does not require p/FDR, replication across datasets, dose
   response, or on-target dependency. That would be a serious promotion flaw if
   any candidate passed. Since none passed, the right inference is negative, not
   "near miss."

5. **Most contrasts are not disease-relevant therapeutic perturbations.**  
   The screen mixes mouse BMDM/Hoxb8 macrophages, iPSC macrophages, peritoneal
   macrophages, plaque macrophages, cuprizone microglia, stroke/aged CNS
   myeloid cells, OxLDL, apoptotic Jurkat/cell cargo, and phagocytic fraction
   sorting. These are useful stress tests, not primary human autoimmune lesion
   rescue assays.

6. **Phagocytic-vs-nonphagocytic fraction comparisons are not intervention
   effects.**  
   The `GSE325329` IL10/IFNG contrasts compare sorted phagocytic fractions
   against nonphagocytic fractions inside a polarization condition. That tests
   post-hoc cell state associated with successful uptake, not whether IL10 is a
   safe controller of the disease module.

7. **Cuprizone positives are lesion-state positives, not controllers.**  
   `WT_CPZ_*_vs_WT_Basal` increases resolution together with lipid/APC and IFN.
   That is exactly the confounded lesion-state pattern the branch was supposed
   to escape.

## Candidate-by-Candidate Attack

| Candidate route | Corrected Wave35 result | Failure mode | Evidence required to continue |
|---|---|---|---|
| `FPR2/ANXA1` | No direct Wave35 FPR2/ANXA1 perturbation. Wave34-B already parks it: IBD/LN support, MS local `FPR2` and `ANXA1` negative. | Ligand-biased GPCR with sign risk; ANXA1/EAE context conflict; no MS lesion-local FPR2-dependent repair; no target-level genetics. | Biased agonist/ANXA1 perturbation in human Crohn/UC or LN macrophages plus MS myelin-loaded microglia, with FPR2 blockade/knockdown, >=30% cargo-clearance increase, lipid-inflammatory reduction, preserved IFN/HLA-II, no fibrosis. |
| RXR/LXR | `Aged_BEX_vs_Aged_vehicle`: resolution +0.286, lipid/APC +0.024, IFN -0.094, stress -0.342. Young and stroke-aged contexts do not replicate. LXR/ABCA1 remains prior-art/safety blocked in Wave32-C. | Broad nuclear-receptor pharmacology, no lipid/APC reduction, age/context dependence, saturated EAE/remyelination/metabolic prior art. | Tissue-restricted non-lipogenic RXR/LXR/efflux perturbation with replicated disease-myeloid lipid/APC reduction, target engagement, no systemic lipid/toxicity liability, and novelty beyond existing PPAR/RXR/LXR work. |
| `IL10` | `IL10_Treg_phago_vs_IL10_nonphago`: resolution +0.314 but lipid/APC +0.119 and IFN +0.169. `IL10_Tconv_phago`: resolution below gate (+0.202), lipid/APC +0.167, profibrosis +0.186. | Phagocytic-fraction association, not IL10 augmentation effect. Does not reduce lipid/APC. IL10 is broad immunosuppression/tolerance biology, not a selective resolution controller here. | Direct IL10-pathway augmentation in diseased human tissue macrophages showing cargo clearance gain, lipid/APC reduction, preserved host-defense response, no fibrosis/TGFB program, and a modality more selective than systemic IL10 biology. |
| `MERTK/TAM` | `GSE156234` is descriptive only with one pseudobulk sample per condition. WT efferocytosis decreases the resolution module. MERTK-dependent 2h interaction has resolution +0.023, IFN +2.000, profibrosis +1.275. 6h interaction has resolution -0.884 and profibrosis +1.088. | Strong mechanism but no replicated agonist perturbation; correct direction is agonism/restoration while drug space is inhibitor-heavy; fibrosis, tumor tolerance, infection, platelet/vascular risks remain. | Replicated human macrophage/microglia MERTK-selective agonism or engineered GAS6/PROS1 with pMERTK target engagement, cargo-clearance gain, lipid/APC reduction, no IFN collapse, no profibrotic/tumor-tolerance signature, and feasible delivery. |
| `GPNMB` | `GpnmbR150X` increases resolution but also lipid/APC and stress. Baseline mutant vs WT: resolution +0.476, lipid/APC +1.271, stress +0.595. OxLDL mutant vs WT: resolution +0.503, lipid/APC +0.511, stress +1.041. Interaction lowers lipid/APC (-0.760) but gives almost no resolution (+0.027) and profibrosis +0.763. | Mutation-state effects do not define a therapeutic direction. GPNMB remains a repair/injury marker or delivery handle; depletion/ADC is wrong-direction for repair. | Non-depleting GPNMB perturbation proving causal repair in human lesion myeloid cells, with reduced lipid-inflammatory state and no stress, plus evidence that targeting GPNMB+ cells will not remove beneficial repair cells. |
| `LIPA` | LIPA KO: lipid/APC -0.574 but resolution -0.043, stress +0.565, profibrosis +0.770. LipaOE peritoneal macrophages: resolution +0.106, lipid/APC +0.478, IFN +1.363. LipaOE plaque macrophages: resolution +0.096, lipid/APC -0.244, profibrosis +0.717. | Loss/gain results are directionally inconsistent; enzyme replacement/delivery does not solve tissue selectivity or CNS exposure; signal remains lipid-stress/readout-like. | Myeloid-specific LIPA enhancement in disease-relevant human cells with lipid-flux readouts, cargo-clearance gain, lipid/APC reduction, no stress/fibrosis, and a delivery route for the relevant tissue. |

## Gene-Level Rescue Attack

A gene-level rescue route is not supported by the current Wave35 outputs.

Failure modes:

- Wave35 does not produce per-gene differential tables, target-dependency
  statistics, or gene-level rescue scores.
- Four datasets are reduced to a mapped candidate panel, so they cannot support
  unrestricted gene-level discovery.
- Mean module scores can hide opposing genes, but that cuts both ways. It can
  hide a true controller, or it can hide that a "hit" is driven by one marker
  gene while guardrail biology worsens.
- Candidate genes inside the module are not automatically intervention points.
  `APOE`, `LPL`, `C1Q`, `GPNMB`, `LIPA`, `ANXA1`, `IL10`, and `MERTK` can be
  markers of cell abundance, lesion phase, cargo exposure, or repair attempt.
- Gene-level direction must be tied to function. A transcript increase in
  phagocytic cells is not evidence that agonizing the gene will clear disease
  tissue safely.

Minimum evidence for any gene-level rescue:

1. Re-run from full matrices or validated full-transcriptome normalization, not
   77-gene mapped panels.
2. Report per-gene effect size, p/FDR, and direction across all Wave35
   contrasts, including guardrail genes.
3. Require target perturbation, not only disease-state or sorted-fraction
   association.
4. Require on-target dependency: genetic knockdown/knockout/blockade/agonist
   reversal appropriate to the proposed direction.
5. Require cargo-resolved function: apoptotic-cell or myelin/lipid-debris
   clearance measured directly.
6. Require preservation of IFN antiviral response and antigen-presentation
   competence, not merely "IFN not collapsed" by a module threshold.
7. Require at least one human disease-tissue system and one independent
   replication context.
8. Require prior-art and modality differentiation before promotion.

If Wave36-A finds a nominal gene, treat it as a hypothesis generator only unless
it meets those gates.

## Decision For Orchestrator

Yes: pivot away from the resolution/efferocytosis branch as an active V3
therapeutic-discovery path.

Keep only these limited uses:

- biomarker/readout panel for lesion repair or lipid-debris handling;
- positive/negative controls in future perturbation assays;
- parked IBD/LN-first `FPR2/ANXA1` wet-lab branch, not an MS V3 target;
- comparator evidence for why generic RXR/LXR/PPAR, TAM, GPNMB, LIPA, and IL10
  routes fail promotion.

Stop doing additional route scoring inside this branch unless a new real
perturbation source appears that is disease-relevant, target-specific,
replicated, cargo-functional, and guardrail-clean.

## Changed Files

- `subagents_v3/wave36b_hostile_critique.md`
