# Tools And Data Inventory V3

**Started:** 2026-05-26 18:41 UTC  
**Rule:** every claimed number must trace to code, public data, or verified source. Tool intent is broader than guaranteed availability.

## Local Baseline

- OS/runtime: macOS local workspace, Python `3.13.3`, R `4.6.0`.
- Current `.venv` has `numpy`, `pandas`, `scipy`, `statsmodels`.
- Missing at start: `requests`, `Bio`, `scikit-learn`, `anndata`, `scanpy`, `torch`, `transformers`, `huggingface_hub`, `rdkit`, `networkx`.
- Existing real data: MS lesion proteomics/RNA/spatial data under `data/raw`, autoimmune GEO matrices under `data/raw_v2`.
- Existing V2 entry point: `./scripts/entrypoints/run_v2_analysis.sh`.

## Foundation Models

### Arc Institute State

Use intent: single-cell/cellular perturbation prediction for candidate central nodes across immune cell contexts.

Provisioning plan:

- verify official repository, paper/model-card, license, install requirements, and weights;
- attempt CPU/macOS-compatible inference on a small expression panel first;
- if GPU/Linux-only or unavailable, document in `BLOCKERS_V3.md` and route to comparable models or real perturbation data.

Output requirement if used: model name/version, weight identifier, input gene set/cell state, command, output file, checksum.

### Arc Institute Stack

Use intent: if available, cross-modal or stackable cellular representation/perturbation inference.

Provisioning plan mirrors State. If Stack is not publicly installable or not relevant to single-cell perturbation, it will be marked as unavailable rather than substituted silently.

### Evo 2

Use intent: variant/regulatory sequence effect prediction around candidate genes or autoimmune GWAS loci.

Feasibility risk: likely CUDA/Linux and large-weight dependent. On this macOS CPU workspace, local full-weight Evo 2 inference may be impossible. Official APIs/containers will be checked. If unavailable, alternative traceable variant/regulatory sources will be used, but those alternatives do not count as Evo 2 output.

### Comparable Alternatives

Allowed only with actual installed weights and logged inference:

- `scGPT`
- `Geneformer`
- `scFoundation`
- `UCE`
- `CellPLM`
- `scVI`/`scArches` for latent-space perturbation or reference mapping, labeled as statistical model rather than foundation model unless pretrained weights are used.

## Cross-Disease Expression And Cell State

Existing local datasets:

- MS: `GSE279972`, `GSE301908`, `GSE284005`, `GSE180759`.
- RA: `GSE97779` macrophages.
- IBD: `GSE75214` mucosa.
- Psoriasis: `GSE13355` paired skin.
- Lupus nephritis: `GSE32591` kidney.
- SLE sorted immune subsets: `GSE10325`.
- Sjogren: `GSE23117`.
- T1D monocytes: `GSE154609` matrix present; platform annotation blocker from V2.

New data targets:

- Crohn's/UC single-cell lamina propria atlases from GEO/Single Cell Portal/cellxgene.
- RA synovium single-cell/spatial atlases.
- psoriasis lesional skin scRNA/spatial atlases.
- lupus nephritis kidney single-cell atlases.
- T1D islet/immune single-cell atlases.
- Sjogren salivary-gland scRNA/spatial.
- ankylosing spondylitis, myasthenia gravis, autoimmune thyroid disease, celiac disease, primary biliary cholangitis datasets where public matrices are tractable.

Analysis methods:

- disease/control or active/inactive contrasts;
- cell-type-aware pseudobulk where single-cell metadata and matrices are accessible;
- module decomposition into lipid handling, lysosomal antigen processing, complement/phagocytosis, interferon/chemokine, metabolic activation;
- cross-disease rank aggregation with tissue/cell-type quality weights;
- non-autoimmune inflammatory controls where accessible.

## Genetics

Target sources:

- GWAS Catalog
- OpenGWAS/MR-Base
- FinnGen endpoint summaries
- Pan-UK Biobank if accessible
- eQTL resources from GTEx/eQTL Catalogue/BLUEPRINT/DICE where accessible

Methods:

- validated cis-eQTL instrument extraction for candidate genes;
- MR only with instrument strength, harmonization, Steiger/pleiotropy checks where possible;
- colocalization/SuSiE only when full summary statistics and LD/reference can be obtained;
- if only GWAS Catalog overlap is available, label as locus evidence, not causal genetic anchoring.

## Perturbation

Sources:

- LINCS L1000 / CMap metadata and signatures where accessible;
- Perturb-seq resources from GEO/ArrayExpress/cellxgene;
- JUMP-CP only if target-relevant compounds and data access are tractable;
- public gene knockdown/CRISPR screens in macrophages, dendritic cells, microglia, intestinal macrophages, keratinocyte/immune co-culture, synovial macrophages.

Methods:

- disease-state signature reversal;
- candidate-gene perturbation effect on module axes;
- cell survival/proliferation confounder checks;
- compare model-predicted perturbation direction with real perturbation data.

## Drug And Target Resources

Sources:

- OpenTargets
- ChEMBL
- DGIdb
- Pharos
- Therapeutic Target Database
- DrugBank if available
- ClinicalTrials.gov
- PubChem
- UniProt/AlphaFold DB
- PDB where structures exist

Methods:

- target tractability and safety liabilities;
- existing chemical matter, potency, selectivity, modality precedent;
- CNS/tissue-delivery audit;
- family selectivity where target belongs to a protein family;
- no docking claim without structure, pocket, controls, and selectivity comparison.

## Literature, Trial, Patent, And Prior Art

Databases:

- PubMed
- Europe PMC
- bioRxiv
- medRxiv
- Google Scholar where accessible by web search
- ClinicalTrials.gov
- Google Patents
- Espacenet

Rule: patents and preprints count as prior art. Closest prior art must be listed before novelty is claimed.

## Simulation And Mechanistic Modeling

Tools:

- `scipy.integrate` for ODEs;
- lightweight agent-based simulation in Python if biologically justified;
- network diffusion/Boolean dynamics with `networkx` if installed;
- no complex PDE or docking workflow unless installation and inputs are tractable.

Model candidates:

- lipid/lysosomal inflammatory myeloid state transition;
- tissue-specific inflammatory positive feedback loops;
- intervention trial-feasibility model for lead indication.

## Reproducibility Targets

- `scripts/entrypoints/run_v3_analysis.sh` end-to-end entry point.
- `environment/requirements_v3.txt` and `environment/python_v3_freeze.txt`.
- fixed random seed `20260526`.
- manifest of data downloads/checksums under `data/derived_v3`.
- all subagent reports copied under `phases/v3/subagents`.
