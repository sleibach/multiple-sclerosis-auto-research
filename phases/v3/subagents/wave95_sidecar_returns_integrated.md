# Wave95 Sidecar Returns Integrated

Timestamp integrated: 2026-05-27 20:50 CEST.

These sidecars were completed before a context interruption and were retrieved
from the still-open agent slots. They are preserved here because they affected
the post-Wave95 branch choice.

## CD300 Family

Agent: `019e6a0b-8503-7bd0-b101-ec603041af8b`.

Call: `PARK_WET_LAB_ONLY`; do not promote a broad CD300-family target claim.

Key verified blockers:

- `CD300F/CLM-1` has direct MS/EAE biology; CLM-1 deficiency worsened EAE
  (PMID `20038601`, DOI `10.1084/jem.20091508`).
- Genentech/Roche CD300F/CLM-1 agonist patent for MS/demyelinating disease:
  `EP2451843A1`.
- `CD300C` autoimmune/EAE/CIA patent: `US11952419B2`.
- Broad CD300LG autoimmune claims: `WO2008003748A2`.
- CD300A/CD300F receptor-specific direction is ambiguous across efferocytosis,
  mast-cell/eosinophil, EAE, lupus-like, IBD, and RA contexts.

Integration decision: CD300 remains a receptor-specific wet-lab kill-test
branch only; it is not a V3 computationally promotable central node.

## SEL1L3

Agent: `019e6a18-7aa6-7112-8dbd-f42060a94c51`.

Call: `PARK` as biomarker/accessibility-state marker; not a therapeutic target.

Key verified sources:

- NCBI Gene `23231`; UniProt `Q68CR1`.
- No exact ChEMBL target/activity and no ClinicalTrials.gov trials found.
- Auto-antigen/BCR lymphoma paper PMID `38671086`; MS PBMC relapse signature
  PMID `40597893`; RA biomarker-style papers PMIDs `35379209`, `36739468`.

Integration decision: SEL1L3 low prior art is not enough. Missing ligand,
receptor axis, enzymatic function, perturbation support, and safety logic block
promotion.

## NRCAM

Agent: `019e6a2c-d95b-7bb1-bf18-40a6e4f782af`.

Call: `PARK` as response/accessibility biomarker; close therapeutic route.

Key verified sources:

- UniProt `Q92823`; neural/node-of-Ranvier biology PMIDs `8947556`, `11728309`.
- MS CSF/brain injury-marker evidence PMCID `PMC10355830`.
- Graves CD4 T-cell transcriptional observation PMID `35220890`.
- No NRCAM ChEMBL target or ClinicalTrials.gov trials in this pass.
- Oncology/CAR-T patent activity exists (`WO2026064380`), adding translational
  caution without autoimmune target validation.

Integration decision: NRCAM is likely tissue injury/stromal/neural response
biology rather than an autoimmune intervention node.

## C15ORF48 / MOCCI

Agent: `019e6a2c-fafb-7942-9805-88ed76ea0b5d`.

Call: `PARK` as myeloid metabolic-state readout / perturbation assay marker;
do not promote as a target.

Key verified sources:

- MOCCI/C15ORF48 complex-IV remodeling and inflammation: PMID `33837217`,
  DOI `10.1038/s41467-021-22397-5`.
- Primary macrophage inflammation/remodeled cytochrome c oxidase: PMID
  `34878835`.
- Stress-independent autophagy/autoimmunity: PMID `38296961`.
- Gut epithelial `C15ORF48/miR-147-NDUFA4` axis: PMID `38917002`.
- miR147 mucosal healing: PMID `40956617`.
- RA miR-147 papers: PMIDs `33864383`, `31105830`.
- No clean C15ORF48/MOCCI therapeutic trials; patents found are biomarker or
  panel-style rather than selective modulation.

Integration decision: C15ORF48/MOCCI is mechanistically rich but directionally
likely adaptive/protective and not directly druggable. Use as readout axis for
upstream/downstream controller searches only.

## CD200 / CD200R1

Agent: `019e6a3a-6519-7043-819e-1b0173103894`.

Call: `PARK` comparator; close as V3 target due low novelty and weak local
receptor-state coupling.

Key verified sources:

- EAE CD200Fc agonism reduced severity/demyelination/axonal damage: PMID
  `20147531`.
- EAE CD200/CD200R1 dynamics: PMID `28522962`.
- Human MS lesion inhibitory signal reports: PMIDs `17879969`, `39175944`.
- Oncology antagonism trials: `NCT00648739`, `NCT05199272`.
- Agonist/patent crowding: `US20200087395A1`, `US11319370B2`,
  `WO2024248532A1`.

Integration decision: correct direction would be CD200R1 agonism/restoration,
but novelty and safety are poor and local receptor coupling remains weak.

## Hostile Integration

Agent: `019e6a3a-8615-76d2-b721-6a2a9520dddc`.

Call: no Wave95 branch merits promotion. Least-bad branch was receptor-specific
CD300 tuning, but only as a fail-fast wet-lab/mechanistic branch. C15ORF48 is
only an assay/readout axis. SEL1L3, CD200/CD200R1, and NRCAM should not be the
next computational branch unless new evidence solves cell source, direction,
and causal intervention coupling.

Orchestrator consequence: proceed to C15ORF48-proximal controller searches
instead of promoting any Wave95 candidate.
