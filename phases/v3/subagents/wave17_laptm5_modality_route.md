# Wave17-B LAPTM5 Modality / Dependency Route

Returned: 2026-05-27

Ownership: LAPTM5 route only. I did not edit other candidate routes.

## Recommendation

**PARK LAPTM5 as an intervention target. PROMOTE LAPTM5 only as a biomarker / pharmacodynamic readout.**

LAPTM5 is credible as a recurrent lysosomal immune-state marker around the `CD74` / HLA-II / APC axis, but it is not yet credible as a direct chronic autoimmune intervention point. The local signal is real enough to keep in assays, yet the biology is directionally split by immune cell type and the modality path is weak.

## Local Wave15 Evidence

Local support is enough for a dependency hypothesis, not for a therapeutic target.

| evidence layer | LAPTM5 result | interpretation |
|---|---:|---|
| Wave15 surface/trafficking rank | `GO_SCOUT`, rank score `22.75` | Recurrent state-coupled lysosomal candidate, below CTSH/CTSS/LGALS9 and HLA-DM state controls. |
| Disease-control trend | 3 diseases: Hashimoto thyroiditis, Sjogren syndrome, ulcerative colitis | Breadth exists but is modest; only one FDR10-positive disease in the surface table. |
| Residual HLA/CD74-state coupling | 6 diseases: Crohn, Sjogren, celiac, psoriasis, T1D, UC | Strongest local reason to keep LAPTM5 in the readout panel. |
| Wave15 orchestrator | priority score `10.0`, residual support in 4 diseases | Kept as upper-mid candidate, not lead. |
| Geneformer deletion | 7 contexts, 32 disease cells, 1 support context, 0 strong contexts | Weak-positive only; does not rescue causality. |
| External gate | Open Targets gwas_credible_sets rows `0`; ClinicalTrials.gov hits `0` | Novelty is relatively clean, but genetics and clinical validation are absent. |

## Immune Cell Biology

LAPTM5 is a reviewed, 262-aa lysosomal multi-pass membrane protein. UniProt describes lysosomal membrane localization, ubiquitin binding, and preferential adult hematopoietic expression. NCBI Gene lists highest expression in bone marrow and lymph node, and GO annotations include Golgi-to-lysosome transport plus negative regulation of T-cell and B-cell activation / receptor signaling.

The immune biology is not one-directional:

- **B lineage:** pre-BCR signaling induces LAPTM5, which routes intracellular pre-BCR to lysosomes and limits surface pre-BCR supply (PMID `22949502`). A later B-cell tolerance paper reports a LAPTM5-WWP2-PTEN-AKT route supporting immature B-cell apoptosis/tolerance.
- **T lineage:** LAPTM5 promotes lysosomal degradation of intracellular CD3zeta and negatively regulates TCR expression/activation (PMID `24638062`).
- **Macrophages:** LAPTM5 has the opposite flavor in myeloid innate signaling. The macrophage JBC paper reports reduced NF-kB/MAPK activation and cytokine secretion after LAPTM5 loss (PMID `22733818`).
- **STING/inflammation:** a 2025 rosacea study reports LAPTM5 stabilizing STING and knockdown attenuating LL-37-induced rosacea-like inflammation in mice (PMID `41087666`).

This creates a hard therapeutic-direction problem. Increasing LAPTM5 might improve B/T receptor down-modulation or tolerance in some lymphocyte contexts, while decreasing LAPTM5 might suppress macrophage/STING inflammation. A systemic intervention could push beneficial and harmful axes simultaneously.

## Disease Genetics

No strong target-level autoimmune genetics anchor was found.

- Local Wave15 Open Targets `gwas_credible_sets` query returned **no LAPTM5 rows** for the selected autoimmune disease panel.
- The Open Targets target page resolves LAPTM5 (`ENSG00000162511`), but top platform associations from a live check were not the V3 autoimmune diseases and are low-scoring/non-specific.
- A Chinese SLE candidate-gene study reported lower LAPTM5 PBMC mRNA in SLE and lupus nephritis, but the assayed SNPs were not associated with SLE susceptibility (PMID `25998573`). That supports readout use more than target causality.
- Lupus nephritis and other bioinformatics papers repeatedly surface LAPTM5 as an immune-infiltration marker, which is compatible with a myeloid/APC abundance or activation readout.

Genetics call: **weak / negative for intervention.**

## Perturbation Evidence

Perturbation evidence is suggestive but not enough.

- Local Wave15 perturbation/drug-response outputs did not nominate LAPTM5 as a direct perturbation candidate.
- LAPTM5 shRNA/AAV evidence in rosacea-like inflammation supports that knockdown can affect a macrophage/STING inflammatory phenotype, but this is skin/LL-37/STING biology, not cross-autoimmune HLA-II dependency validation.
- Cancer-cell lysosomal integrity work shows LAPTM5 depletion can destabilize lysosomes (PMID `35091468`), which is a safety/liability signal for broad inhibition.

Minimum missing experiment before reconsideration: cell-type-restricted LAPTM5 knockdown/overexpression in primary human macrophages, dendritic cells, B cells, and tissue APC-like cells, with `CD74/HLA-DRA/HLA-DPA1/HLA-DMA/IFI30/CTSH/CTSS` readouts separated from viability, lysosomal membrane permeabilization, and generic myeloid abundance.

## Modality / Druggability

| modality | feasibility | call |
|---|---|---|
| Small molecule | No enzyme active site; no local ChEMBL/druggability row; Open Targets small-molecule tractability flags false for approved/clinical/high-quality ligand/pocket/druggable family. | **Poor** |
| ASO / siRNA | Plausible as a research perturbation. Chronic autoimmune therapy would need tissue- and cell-type-specific myeloid/APC or B-cell delivery. CNS microglia delivery for MS is an additional barrier. | **Tool only for now** |
| Antibody | LAPTM5 is primarily lysosomal membrane, not a clean extracellular/surface target. Open Targets antibody tractability has generic GO/TM hints, but no approved/clinical antibody flags. | **Poor** |
| PROTAC / molecular glue | No known binder; multi-pass lysosomal membrane topology is not a good conventional PROTAC substrate. Open Targets PR tractability lacks clinical/literature/small-molecule binder support. | **Poor** |
| Cell-type targeted nanoparticle / oligo | Could test macrophage/STING suppression or APC-state modulation ex vivo/in vivo. Therapeutic use would need strong selectivity to avoid broad lysosomal and lymphocyte receptor effects. | **Research-only** |

Therapeutic direction is also unresolved: **inhibit LAPTM5** may reduce macrophage/STING inflammatory amplification but could impair lysosomal integrity and alter lymphocyte receptor/tolerance biology; **increase LAPTM5** may suppress T/B receptor signaling but could amplify macrophage inflammatory signaling in some contexts.

## Novelty / Prior Art

LAPTM5 is less crowded than CTSS, CD74/MIF, LGALS3, or LGALS9 as a named autoimmune intervention target.

- Europe PMC query counts from Wave15: 325 LAPTM5-autoimmune disease-panel hits, 507 LAPTM5-antigen-presentation hits, and 1119 LAPTM5-therapeutic-word hits.
- ClinicalTrials.gov returned no LAPTM5 studies in the Wave15 API check and live spot check.
- Targeted Google Patents/Espacenet searches did not reveal a direct LAPTM5 autoimmune antigen-presentation intervention family.

This is **white space by absence**, not white space with a credible modality. The novelty is useful only if a later perturbation result creates a strong cell-type-specific causal claim.

## Decision

**PARK as direct intervention target.**

Do not spend the next wave trying to build a therapeutic claim around LAPTM5 unless new primary perturbation data show a separable, beneficial direction in a relevant human immune cell type. LAPTM5 is too context-dependent and poorly tractable for promotion as a standalone target.

**PROMOTE as readout / stratifier.**

Keep LAPTM5 in the HLA-II/APC-state pharmacodynamic panel alongside `CD74`, `HLA-DRA`, `HLA-DPA1`, `HLA-DMA/B`, `IFI30`, `CTSH`, `CTSS`, `LAMP3`, `TYROBP`, macrophage abundance markers, and lysosomal stress controls. Its best use is to indicate a lysosomal trafficking / immune receptor-routing facet of the CD74/HLA-II state, not to define the intervention.

## Source Links

- Local sources: `results_v3/wave15_surface_trafficking_dependency/candidate_ranked.tsv`, `results_v3/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv`, `results_v3/wave15_geneformer_loader_dependency_delete/wave15_geneformer_loader_dependency_gene_summary.tsv`, `results_v3/wave15_loader_external_gate/loader_external_gate_summary.tsv`.
- Source table created: `results_v3/wave17_laptm5_modality_route/evidence_sources.tsv`.
- UniProt: https://www.uniprot.org/uniprotkb/Q13571/entry
- NCBI Gene: https://www.ncbi.nlm.nih.gov/gene/7805
- Open Targets: https://platform.opentargets.org/target/ENSG00000162511
- ClinicalTrials.gov: https://clinicaltrials.gov/search?term=LAPTM5
- Europe PMC autoimmune query: https://europepmc.org/search?query=%28LAPTM5%29+AND+%28%22multiple+sclerosis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+Crohn+OR+%22ulcerative+colitis%22+OR+psoriasis+OR+%22type+1+diabetes%22+OR+Sjogren+OR+%22ankylosing+spondylitis%22+OR+celiac+OR+%22autoimmune+thyroid%22+OR+%22primary+biliary+cholangitis%22+OR+autoimmune%29
- PubMed: PMID `22949502`, `24638062`, `22733818`, `25998573`, `41087666`, `35091468`.
- Patents: https://patents.google.com/?q=LAPTM5+autoimmune+antigen+presentation
