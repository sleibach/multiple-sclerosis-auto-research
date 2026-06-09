# Dimension Scout V40

Status: **Phase 1 value-complete**.

Purpose: map computational dimensions the project has not seriously explored
but can plausibly probe with held or reachable data. This is a scout map, not
evidence. Model-lens suggestions, if used, are proposal sources only.

Model proposal files:

- Prompt: `analysis/v40_dimension_scout_prompt.md`
- Claude output: `analysis/v40_dimension_scout_claude.json`
- Gemini output: `analysis/v40_dimension_scout_gemini.json`

The model outputs were used only to widen the candidate list. The priority
ranking below is grounded in held project inventory and V39 prefilters, not in
model confidence.

## Tooling Health

| Tool / lens | V40 health | Use in V40 |
|---|---|---|
| OpenGWAS | HTTP 200 via `scripts/check_opengwas_access.py`; JWT valid until `2026-06-19 12:28 UTC` | Avoided for first probes because token is near-expiry and V40 can run on held data. |
| Claude via SAP AI Core | Smoke-passed: `anthropic--claude-4.7-opus`, deployment `def854013c7ac379` | Available for proposal generation / critique only. |
| Gemini via SAP AI Core | Smoke-passed: `gemini-2.5-pro`, deployment `d6dc532885507ac7` | Available for proposal generation / critique only. |
| SAP RPT | Not available in current Python client: `No implemented request schema for model: sap-rpt-1-large` | Do not claim RPT works. Either implement separately in a future engineering iteration or omit. |
| Local Python/scikit stack | Available | Primary grounding tool. |

## Held Data Families Relevant To New Dimensions

| Data family | Held examples | Under-explored angle |
|---|---|---|
| Treatment response | `analysis/v22_*`, `analysis/v23_*`, `analysis/v28_*`, `analysis/v32_*`, `data/raw_v3/wave96_ms_treatment/`, `data/raw_v3/gse253006/` | Outcome geometry, subgroup/resilience patterns, anomaly/state convergence, therapy-branch comparability. |
| Single-cell / h5ad atlases | `data/raw_v3/cell_state/*.h5ad`, `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`, `data/raw/GSE301908_sn_all.rds` | Cell-cell interaction inference, pseudotime/trajectory, subtype/stage state mapping. |
| Perturbation / CRISPR / Mixscale | `data/raw_v3/mixscale/`, `data/raw_v3/interface_perturbation_geo/`, `analysis/v26_deep_structure/*perturbation*` | Causal discovery / mediation over module responses, perturbation-network topology, regulator direction. |
| Immune-QTL / eQTL | `data/raw/v18_source_triage/`, `analysis/v18_source_triage/`, `analysis/v19_chr1_druggability/` | Protective/resilience eQTL rather than risk-first, cell-type-specific regulatory pleiotropy. |
| GWAS/LDSC summaries | `analysis/v21_ldsc_backdrop/`, `data/raw/opengwas_v21/`, `data/raw/ldsc_reference/` | Protective/resilience genetics, drug-target MR-style framing, subtype/sex/ancestry impossible unless source metadata exists. |
| Microbiome/metabolomics | `data/raw/v9_microbiome_*`, `data/raw/Processed_data_all_omics.xlsx`, `data/raw_v3/wave66_metabolomics_workbench/` | Cross-kingdom/metabolic axis, lipid/metabolite setpoint joins with immune-tone axes. |
| Structures / chemical caches | `data/raw_v3/structures/`, `data/raw_v3/wave82_api_cache/`, V19/V29 target ledgers | Structure-first target tractability independent of prior-art class labels. |
| Pregnancy / EBV / comparator datasets | `analysis/v35_*`, `data/raw_v35/ebv_gse162516/`, `data/raw/GSE17410/` | Natural-experiment timing, infection imprint specificity, stage-window biology. |

## Candidate Dimensions

Scores are `value x feasibility-on-held-data`, 1-5. `Priority` is the product.

| Rank | Dimension | Data needed | Held / blocked | Fast probe | What it could reveal | V39 prefilter risk | Value | Feasibility | Priority | V40 action |
|---:|---|---|---|---|---|---|---:|---:|---:|---|
| 1 | Protective/resilience-direction genetics | Local GWAS VCFs, LDSC rg, coloc/eQTL summaries | Partly held; no individual-level genotypes | Re-orient known MS/comparator loci by protective allele and ask whether protective directions map to distinct modules/tractable modalities vs risk directions | A different question than risk-first target hunting: what biology resists MS rather than causes it | Direction/modality high; avoid target claim without aligned QTL | 5 | 4 | 20 | Probe. |
| 2 | Drug-target MR-style proxy screen | eQTLGen/eQTL Catalogue/DICE/OneK1K, OpenGWAS/local GWAS, V39 direction prefilter | Partly held, but full instruments incomplete | Fast screen of held target-like genes for expression-increasing/decreasing direction and modality match; report blockers | Whether any held expression target has right-direction tractability before wet-lab | High direction/modality and evidence-resolution risk | 5 | 3 | 15 | Scout/probe with held summaries only. |
| 3 | Treatment-response outcome geometry / responder attractors | V32 bounded subject scores, V22/V23 paired scores | Held | Already partially probed by V39; extend to patient-level leave-one-cohort-out geometry and anomaly metrics | Whether response is state convergence rather than scalar threshold | Small-n and therapy-context risk | 4 | 4 | 16 | Probe if time after genetics. |
| 4 | Cell-cell interaction / niche communication | h5ad atlases with cell labels and ligand-receptor gene sets | Held but large; no dedicated LR pipeline yet | Score ligand-receptor modules between APC/T/B/myeloid compartments in held h5ad summaries; null by permuted ligand sets | Non-cell-autonomous mechanism missed by gene/module scalar work | Context/axis and composition confounding | 5 | 3 | 15 | Candidate future run; fast module-level probe possible. |
| 5 | Pseudotime / trajectory state transitions | h5ad single-cell atlases; treatment/lesion/pregnancy stages | Held but requires scanpy/anndata health | Use existing module scores to order cells/samples along APC/HLA-II/CD64 or lesion-state trajectory; null by phase-label permutation | Disease-stage timing rather than static disease-vs-control | Stage metadata may be missing | 4 | 3 | 12 | Candidate future run. |
| 6 | Perturbation causal-discovery / module network | Mixscale module effects, CRISPR/KO perturbation matrices, V26 module matrices | Held summaries | Infer directed module graph from perturbation effect signs; null by perturbation-label shuffle | Which modules plausibly drive vs follow APC axis | Causality overclaim risk; perturbation contexts not MS | 4 | 4 | 16 | Probe. |
| 7 | Mediation analysis between QTL, expression, and response modules | eQTL hits, expression module matrices, treatment-response module scores | Partial; no same-individual genotype-expression-response | Negative/feasibility probe: identify joins impossible vs possible proxy joins | Prevents false mediation claims; maps exact data gap | Evidence-resolution risk | 3 | 5 | 15 | Map as blocked/partial. |
| 8 | Sex-stratified / hormonal dimension | Pregnancy datasets, metadata in treatment cohorts, sex fields where present | Partly held | Audit metadata coverage; if adequate, test module effects by sex/pregnancy phase with permutation | Sex/hormonal timing overlooked by target-centric analyses | Power and metadata missingness | 4 | 3 | 12 | Candidate probe if metadata sufficient. |
| 9 | Progressive-vs-relapsing subtype / lesion-stage structure | Chronic-active lesion data, MS single-cell/spatial, progressive lesion summaries | Partly held; labels fragmented | Test V35 complement/lipid and APC modules across lesion activity/stage labels with donor-aware nulls | Progressive MS dimension independent of relapsing treatment response | Donor/confounder risk already seen | 4 | 3 | 12 | Future run unless metadata readily joined. |
| 10 | Microbiome/metabolome to immune-tone join | IBD/MS microbiome files, metabolomics workbook, immune-tone module scores | Held but not harmonized | Correlate metabolite/microbial modules with immune-tone axes at cohort summary level; null by feature permutation | Cross-kingdom/metabolic context for immune-tone boundedness | Cross-cohort non-comparability | 3 | 3 | 9 | Lower priority. |
| 11 | Network topology / controllability of APC axis | V26 module dependency matrices, perturbation matrices | Held | Compute centrality/edge vulnerability and null by row/column permutation | Whether APC/HLA-II/MIF/CD74 is structurally controllable or just correlated | Static graph overclaim | 4 | 4 | 16 | Probe. |
| 12 | Rare-variant / burden angle | Individual-level sequencing or rare-variant summary stats | Not held | None without data | Could identify high-effect protective biology missed by common GWAS | Blocked by data absence | 4 | 1 | 4 | Blocked. |
| 13 | Ancestry-stratified transfer validity | Ancestry-specific GWAS/QTL and cohort metadata | Not held beyond EUR LDSC | None without data | Would test portability beyond EUR bias | Blocked by data absence | 4 | 1 | 4 | Blocked. |
| 14 | Splicing/sQTL and isoform direction | sQTL summaries or RNA-seq isoform quantification | Not clearly held | Inventory whether any raw RNA-seq supports isoform-level test | Could rescue targets where expression level is wrong abstraction | Data modality likely absent | 3 | 2 | 6 | Scout only. |
| 15 | Comorbidity structure mining | Clinical comorbidity metadata | Not held | None without data | Could define patient strata | Blocked by metadata | 3 | 1 | 3 | Blocked. |

## Immediate Probe Shortlist

1. **Protective/resilience-direction genetics**: highest priority and most
   orthogonal to risk-first genetics. Fast held-data probe: use V37/V38/V39
   genetics/target rows and local eQTL direction summaries to classify whether
   protective directions are tractable, hard restoration, opposite, unresolved,
   or closed by coloc.
2. **Perturbation causal-discovery / module network**: feasible on V26
   perturbation and module-dependency matrices. Fast probe: infer whether
   directed perturbation signatures put IFN/APC/HLA-II upstream, downstream, or
   confounded with lysosomal/MIF/CD74 modules; null by row/column permutation.
3. **Network topology / controllability of APC axis**: feasible on V26/V38
   module dependency matrices. Fast probe: centrality and edge-vulnerability
   with permutation null.
4. **Treatment-response outcome geometry**: already partly probed in V39; deepen
   only if the above do not yield new signal.

## Blocked Or Lower-Priority Dimensions

- Rare-variant/burden and ancestry-stratified analyses are blocked by absent
  individual-level or ancestry-specific data.
- Splicing/sQTL is not confirmed held and should start as inventory only.
- Comorbidity mining is blocked by metadata absence.
- Microbiome/metabolome joins are feasible but lower priority because
  cross-cohort comparability risk is high and V39 context-dependence prefilter
  makes unbounded transfer claims weak.
