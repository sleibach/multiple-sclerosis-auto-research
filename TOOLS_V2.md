# Tool Inventory V2

**Created:** 2026-05-26T17:47:25Z

## Local Runtime

- Python via `./.venv/bin/python`.
- R via `Rscript`; existing SeuratObject support is installed.
- Shell utilities: `rg`, `git`, `curl`, `tar`, checksum utilities.
- Existing repository entrypoints: `run_analysis.sh`, `run_therapeutic_analysis.sh`.

## Deepen Track Tools

| Tool/resource | Intended use | Constraint/downscope |
|---|---|---|
| AlphaFold DB | Retrieve verified ACSL family predicted structures and confidence metadata when available. | Do not claim new structure prediction unless actually run. |
| UniProt REST | ACSL isoform sequences, domain annotations, catalytic motifs. | Sequence-based selectivity is weaker than experimental enzymology. |
| RCSB PDB | Look for experimental structures or homolog templates for ACSL family. | If no human ACSL1 structure exists, use AlphaFold/homology cautiously. |
| ChEMBL / PubChem / DrugBank / DGIdb / OpenTargets | Known ligands, target tractability, disease associations. | Absence of selective clinical ACSL1 inhibitor is a major feasibility limitation. |
| RDKit | Ligand descriptors and simple CNS-likeness screens if ligands are retrieved. | Descriptors are not proof of CNS penetration. |
| AutoDock Vina / DiffDock / Boltz | Optional docking if installable and protein/ligand preparation is feasible. | Docking without family selectivity will not count as strong evidence. |
| networkx / scipy.integrate | ODE/Boolean/pathway dynamics models. | Simulations must expose assumptions and sensitivity, not masquerade as measured biology. |
| Mesa-like custom Python | Agent-based lesion/tissue dynamics. | Use transparent rules and fixed seeds; label as mechanistic simulation. |
| scipy/statsmodels | Trial simulation, power, sensitivity, mixed models. | Trial assumptions must be clearly marked as planning assumptions. |

## Broaden Track Tools

| Tool/resource | Intended use | Constraint/downscope |
|---|---|---|
| GEO / ArrayExpress | Public autoimmune expression datasets. | Prefer processed matrices; raw scRNA reprocessing only if small enough. |
| CZ CELLxGENE / cellxgene-census | Cross-tissue single-cell atlas search for disease/state/gene expression. | May be too large; downscope to targeted queries. |
| OpenTargets Genetics / Platform | Multi-indication genetics and target association evidence. | Target scores are evidence summaries, not colocalization. |
| GWAS Catalog / OpenGWAS / FinnGen / Pan-UKBB | Cross-disease locus and instrument search. | Full MR/colocalization requires accessible summary stats and instruments. |
| OpenAlex / PubMed / Europe PMC / bioRxiv / medRxiv | Literature and preprint novelty checks. | Verified citations only. |
| Google Patents / Espacenet | Patent prior art. | Search results are not freedom-to-operate opinions. |
| LINCS / CMap / Enrichr APIs | Perturbation signature reversal if accessible. | Do not count simple enrichment as CMap unless actual perturbation signatures are used. |
| iReceptor / VDJdb / McPAS-TCR | Immune repertoire cross-disease context. | Likely exploratory unless antigen-specific datasets are accessible. |
| Microbiome public cohorts | Cross-autoimmune lipid/metabolite context. | Only use if data access is practical. |

## Integration Tools

- `pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib` for reproducible summaries and simulations.
- `json.tool` and `git diff --check` for artifact integrity.
- Markdown logs: `ORCHESTRATION_LOG.md`, `LAB_NOTEBOOK_V2.md`, `CONVERGENCE_CHECK_*.md`, `CRITIQUE_V2.md`.
