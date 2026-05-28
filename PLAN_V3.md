# Plan V3: Twelve-Hour Cross-Disease Synthesis

**Started:** 2026-05-26 18:41 UTC  
**Seed:** `20260526`

## Objective

Resolve whether the lipid-lysosomal inflammatory myeloid module is a cross-autoimmune causal mechanism, identify its strongest central node or state transition, test perturbation consequences with foundation models or documented alternatives, and nominate a tractable intervention point only if evidence converges.

## Workstreams

### Workstream 1: Breadth Screen

Inputs:

- existing V2 bulk/sorted datasets;
- new disease-specialist subagent reports;
- tractable additional public matrices.

Methods:

- decompose module into axes:
  - lipid uptake/droplet/efflux;
  - lysosome/antigen processing;
  - complement/phagocytosis;
  - interferon/chemokine;
  - metabolic inflammatory licensing;
  - repair/resolution.
- rank genes and regulators by disease breadth, direction consistency, and cell-type specificity;
- penalize broad pan-inflammation, tissue-injury-only, and myeloid-density-only signals.

Positive result:

- candidate central node/state appears in at least five autoimmune diseases with at least three independent channels in lead diseases.

Negative/pivot result:

- module reduces to generic tissue injury or macrophage density. Pivot to tissue-specific state transition or reject broad therapeutic claim.

### Workstream 2: MS Anchor

Inputs:

- `GSE279972`, `GSE301908`, `GSE284005`, `GSE180759`;
- existing MS outputs under `results/`.

Methods:

- compare candidate nodes against MS lesion proteomics, snRNA MIMS-like states, spatial MERFISH, and prior validation outputs;
- require donor-aware analyses;
- do not claim spatial cell-cell mechanism from bulk scores.

Positive result:

- lead candidate replicates across at least two MS modalities and adds mechanistic interpretation beyond `ACSL1` marker behavior.

Negative/pivot result:

- candidate is absent in MS or only tracks myeloid abundance. Pivot to another node.

### Workstream 3: Genetics

Inputs:

- GWAS Catalog/OpenGWAS/FinnGen/MR-Base/eQTL resources as accessible;
- subagent genetics report.

Methods:

- start with locus evidence for breadth;
- attempt cis-eQTL instruments for central genes;
- perform MR/colocalization only if summary-stat and eQTL data permit validated instruments.

Positive result:

- genetic anchoring for at least four autoimmune diseases with validated direction, or a clearly documented narrower genetic claim.

Negative/pivot result:

- no candidate-specific genetics. Continue only if cell-state/perturbation evidence is strong and label genetics as missing.

### Workstream 4: Foundation-Model / Perturbation

Inputs:

- State/Stack/Evo 2 official packages or model outputs;
- Perturb Sapiens if small relevant files can be accessed;
- real perturbation datasets from LINCS/Perturb-seq/GEO.

Methods:

- try actual State/Stack installation in Python 3.12 V3 environment;
- log versions and feasibility;
- run small test inference only if weights/checkpoints are available;
- compare predicted module reversal against real perturbation data where possible.

Positive result:

- foundation model predicts that perturbing candidate central node/intervention point reduces harmful module axes in relevant cell types without broad cytotoxic-state collapse, and at least one real perturbation dataset agrees in direction.

Negative/pivot result:

- model unavailable or prediction contradicts real perturbation. If unavailable, mark blocker and use real perturbation data without pretending it satisfies the foundation-model criterion.

### Workstream 5: Intervention-Point And Translation

Inputs:

- ChEMBL/OpenTargets/DGIdb/Pharos/ClinicalTrials.gov/patent/literature;
- structural resources from UniProt/AlphaFold/PDB where relevant.

Methods:

- identify central node, upstream regulator, downstream effector, or transition controller;
- evaluate druggability, selectivity, tissue delivery, safety liabilities, biomarker, trial design, and prior art.

Positive result:

- named intervention point with tractable modality and no blocking prior art for the specific autoimmune cluster/use.

Negative/pivot result:

- if the node is known/blocked/high-liability, search one edge upstream/downstream or reframe as biomarker only. Biomarker alone does not satisfy the requested therapeutic DoD unless it enables a failed/marginal therapy subgroup.

## Candidate Promotion Rules

Promote a candidate to lead only if:

- it is supported by at least three independent workstreams;
- at least one support channel is cell-state/spatial or perturbational, not only bulk expression;
- contradictory disease directions are biologically explainable and not dominant;
- prior art leaves room for the precise mechanism/modality/indication claim;
- falsification is feasible in a first wet-lab experiment.

## Candidate Demotion Rules

Demote if:

- adjusted analysis shows it is merely myeloid density or broad inflammation;
- perturbation predicts toxicity or failure to reverse the state;
- prior art already directly claims the intervention in the lead disease/cluster;
- no tissue-delivery path exists.

## Milestones

- Hour 2: six disease reports or documented misses; model feasibility; first convergence map.
- Hour 4: cross-disease shared genes/cell states and first central-node ranking.
- Hour 6: three to five central-node candidates plus critique round one.
- Hour 8: lead node selected or documented miss/pivot.
- Hour 10: intervention point selected or documented miss/pivot; critique round two.
- Hour 12: `FINDING_V3.md` if DoD survives; otherwise continue unless externally interrupted.

## Current Pivot Branches

1. If `IFI30`/lysosomal antigen processing dominates breadth and genetics: test GILT/antigen-processing intervention or upstream IFN/lysosomal regulator.
2. If `GPNMB`/`SPP1`/osteopontin tissue-remodeling state dominates: test receptor/ligand axis and macrophage transition controller, but prior art risk is high.
3. If `NAMPT`/metabolic licensing dominates: search for eNAMPT-specific or downstream NAD-sparing intervention; avoid generic FK866 claims.
4. If `LXR/TFEB/lipid efflux` dominates: test state-transition controller rather than individual lipid droplet enzyme.
5. If no single node dominates: sharpen to a named transition circuit and intervention point, or keep working until an integrated answer emerges.
