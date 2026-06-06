# Wave69-C Foundation-Model / Perturbation Feasibility Replacement Audit

Returned: 2026-05-27 16:00 CEST

## Scope

Task: inventory what can actually be run now in this workspace for cellular perturbation or regulatory/protein prediction relevant to the current parked gene/controller branch. The audit covers local packages, prior scripts/results, downloaded model assets, live API availability checks, blockers, and the next executable in-silico perturbation test. No model output is fabricated here; endpoint checks are availability checks only.

Current branch context from `results_v3/wave68_gse282122_unrestricted_gene_screen/summary.json`:

- Wave68 now has no promoted `REOPEN_GENE_LEVEL_TARGET_CANDIDATE`; calls are `DESCRIPTIVE_GENE_SIGNAL=66137` and `PARK_GENETIC_PERTURBATION_INTERSECTION=13`.
- Parked candidates with gene-level remission-associated signal plus cross-autoimmune genetic flags include `RGS14`, `CD274`, `LPP`, `ARHGAP31`, `TNFSF15`, `NCF1`, `CD80`, `FCGR2B`, `IL7R`, `STAT4`, `TNFRSF9`, `DCLRE1B`, and `FCGR2A`.
- `SP140` is not currently promotable: the integrated table marks it `DESCRIPTIVE_GENE_SIGNAL` with `wave68_posthoc_blocker=v3_sp140_prior_art_direction_conflict_ms_local_null` and `manual_or_prior_blocked=True`.

## Environment Facts Checked

Commanded imports in `.venv_v3_py312`:

| Package | Status |
| --- | --- |
| `numpy` | 2.4.6 |
| `pandas` | 2.3.3 |
| `scipy` | 1.17.1 |
| `statsmodels` | 0.14.6 |
| `sklearn` | 1.8.0 |
| `networkx` | 3.6.1 |
| `requests` | 2.34.2 |
| `anndata` | 0.12.16 |
| `scanpy` | 1.12.1 |
| `torch` | 2.12.0 |
| `transformers` | 5.9.0 |
| `scvi` | 1.4.3 |
| `Bio` | 1.87 |
| `h5py` | 3.16.0 |
| `geneformer` | missing |
| `cpa` | missing |
| `celloracle` | missing |
| `decoupler` | missing |
| `omnipath` | missing |
| `gseapy` | missing |
| `rdkit` | missing |
| `esm` | missing |
| `pyensembl` | missing |

Local relevant data/model assets:

- `tmp_v3/foundation_wave6/geneformer_assets/Geneformer-V2-104M/model.safetensors`: 417,571,156 bytes.
- Geneformer dictionaries present under `tmp_v3/foundation_wave6/geneformer_assets/geneformer/`.
- Existing lightweight Geneformer engine: `tmp_v3/foundation_wave6/geneformer_tiny_delete_screen.py`.
- StateParse CD14 files under `data/raw_v3/state_parse_split4/`; `adata_real.h5ad` now has the expected stored size, 9,112,404,896 bytes, and opens with shape `(1125352, 2000)`.
- Local single-cell h5ads available: IBD, psoriasis, Sjogren, T1D HPAP islet, RA blood, and GSE282122 myeloid (`data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`).
- Local LINCS metadata: `data/raw_v3/lincs2020/compoundinfo_beta.txt`.

## Runnable Now

### 1. Lightweight Geneformer V2-104M Token-Deletion Screen

Verdict: runnable now.

Evidence:

- Official Geneformer V2-104M weights and dictionaries are present locally.
- The workspace already ran custom bounded screens using `transformers.BertModel`, not the missing `geneformer` Python package.
- Prior outputs exist under:
  - `results_v3/geneformer_candidate_delete/`
  - `results_v3/geneformer_pivot_panel_delete/`
  - `results_v3/geneformer_unrestricted_survivor_delete/`
  - `results_v3/geneformer_broad_residual_delete/`
  - `results_v3/wave57_intervention_first_geneformer_screen/`
- Provenance in `tmp_v3/foundation_wave6/geneformer_tiny_delete_screen/summary.json`: model `Geneformer V2-104M`, repo `ctheodoris/Geneformer`, revision `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`, `parameters_loaded_encoder=104365056`, seed `20260527`.

Limitations:

- This is not the official `InSilicoPerturberStats` workflow.
- Output is an embedding-state hypothesis: deleting a candidate token shifts disease-cell embeddings toward a defined reference centroid more than random-token deletion.
- It does not produce transcriptome log2FC and does not prove causality.
- Detection is limited to cells in which the candidate token appears in the top-ranked sequence.

Concrete command style already used:

```bash
.venv_v3_py312/bin/python scripts/v3_wave57_intervention_first_geneformer_screen.py
```

For Wave69, write a new narrow script rather than rerun old panels unchanged, because the current branch is GSE282122 remission/non-remission myeloid state, not the older cross-tissue disease/control contexts.

### 2. Arc State / ST-HVG-Parse Released Outputs

Verdict: calibration-grade only; blocked for named-gene candidate scoring.

Evidence:

- `data/raw_v3/state_parse_split4/adata_real.h5ad` is now complete and openable:
  - shape `(1125352, 2000)`
  - `var_names` are numeric strings `0..1999`
  - `var` has no columns
  - `uns` has no keys
- `tmp_v3/var_dims_split4.pkl` contains `gene_names` for 18,308 genes, but not the exact 2,000 HVG feature order used in the DE CSV columns.
- `results_v3/state_parse_cd14_de_with_gene_symbols.tsv` has 248,000 rows and 2,000 unique `gene` values, but all rows are numeric/feature identifiers. Checked named-gene counts are all zero for `SP140`, `STAT4`, `IL7R`, `CD274`, `TNFSF15`, `CD74`, `HLA-DRA`, `CTSS`, `IFI30`, and `STAT1`.

Important guardrail:

- `results_v3/state_parse_cd14_summary.json` currently reports `n_mapped_features=2000` and `gene_mapping_status=mapped_from_adata_real_var_names`, but this is misleading because the mapped values are numeric IDs, not gene symbols. The same summary correctly keeps `module_scoring_status=blocked_no_gene_symbols_for_feature_ids`. Do not use it for named-gene claims unless `scripts/v3_analyze_state_parse_cd14.py` is patched to reject numeric-only `var_names`.

Runnable contribution:

- Feature-agnostic State calibration across CD14 cytokine perturbations can still be used as a general model sanity check.
- It cannot answer whether perturbing `SP140`, `STAT4`, `IL7R`, `CD274`, `TNFSF15`, or `RGS14` moves autoimmune myeloid cells toward remission.

### 3. scVI / scanpy Latent Modeling

Verdict: runnable as a statistical comparator, not a foundation-model perturbation predictor.

Evidence:

- `scvi-tools 1.4.3`, `scanpy 1.12.1`, and `anndata 0.12.16` import successfully.
- No pretrained immune reference model or scArches weights were found locally.

Useful role:

- Fit a local scVI model on GSE282122 myeloid cells to test whether Wave68 candidates explain remission/non-remission state separation after patient/site/disease/batch covariates.
- Use as a robustness check for cell-state geometry and batch correction.

Not valid as:

- A causal perturbation prediction unless a trained perturbational model or explicit counterfactual model is introduced and validated.

### 4. Real Perturbation Datasets Already Integrated

Verdict: runnable/reusable and more trustworthy than weak model surrogates where candidate coverage exists.

Existing relevant outputs:

- `results_v3/wave15_perturbation_drug_response/` contains Mixscale/L1000/direct perturbation summaries.
- `results_v3/wave18_foundation_rescue/direct_perturbation_evidence_by_candidate.tsv` joins model screens to real perturbation evidence.
- `results_v3/wave35_resolution_perturbation/` contains public mouse perturbation readouts.
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/` contains CRISPR/efferocytosis screen outputs.
- `results_v3/wave64_slamf7_perturbation_audit/` contains a direct human macrophage SLAMF7 perturbation audit.

Useful role:

- Validate whether model-prioritized candidates have directionally aligned real perturbation evidence.
- Fail candidates when model support contradicts real perturbation data.

Limitation:

- Current parked genes (`RGS14`, `CD274`, `LPP`, `ARHGAP31`, `TNFSF15`, `NCF1`, `CD80`, `FCGR2B`, `STAT4`, `IL7R`) may not be directly perturbed in the most relevant public assays, so coverage must be checked per gene before claiming validation.

### 5. LINCS / L1000FWD

Verdict: runnable now as weak compound-signature evidence.

Evidence:

- Local files exist: `results_v3/l1000fwd_reversal_hits.tsv`, `results_v3/l1000fwd_compound_summary.tsv`, `results_v3/l1000fwd_summary.json`, and `data/raw_v3/lincs2020/compoundinfo_beta.txt`.
- L1000FWD API smoke test:
  - `POST https://maayanlab.cloud/L1000FWD/sig_search`
  - status `200`
  - returned a `result_id`
  - `GET /result/topn/{result_id}` status `200`

Use:

- Query disease/remission module signatures or candidate-adjacent signatures for compound reversers.
- Treat results as cell-line perturbation support only. Prior V3 hostile reviews already warned that L1000 alone overselects cytotoxic/stress/generic anti-inflammatory mechanisms.

### 6. Enrichr

Verdict: runnable now via API; no local package needed.

Evidence:

- `GET https://maayanlab.cloud/Enrichr/datasetStatistics` returned status `200`, JSON payload, 68,971 bytes.

Use:

- Enrich Wave68 remission-associated gene sets for TF targets, pathways, ligand/receptor programs, and drug signatures.
- Useful libraries for next run: ChEA/ENCODE TF targets, Reactome, KEGG/GO, kinase perturbation, and drug perturbation libraries.

Limitation:

- Enrichment is not perturbation prediction. Use it to nominate controllers, not to validate them.

### 7. OmniPath / Network Perturbation

Verdict: runnable now through raw HTTP API; local `omnipath` Python package is missing but not required.

Evidence:

- `GET https://omnipathdb.org/interactions?genesymbols=1&format=json&datasets=omnipath&sources=TNF` returned status `200`, JSON payload, 5,247 bytes.

Use:

- Pull signed directed interactions for candidate controllers and module genes.
- Run a simple network propagation or sign-consistency model with `networkx`.
- Score whether inhibiting/activating a candidate is expected to move Wave68 remission-associated modules in the observed direction.

Limitation:

- Network coverage will be uneven for nuclear factors (`SP140`, `RGS14`, `LPP`, `ARHGAP31`) and stronger for canonical immune nodes (`STAT4`, `CD274`, `CD80`, `TNFSF15`, `IL7R`).

## Blocked or Not Worth Running Now

| Tool / route | Status | Reason |
| --- | --- | --- |
| Arc State named-gene perturbation | Blocked | Complete AnnData opens, but feature IDs are numeric and no HVG gene map is exposed. |
| Arc Stack | Blocked | No local install, weights, or prior runnable script found. |
| Evo 2 | Blocked for this branch | No local install/weights; regulatory sequence prediction is not the immediate bottleneck for Wave68 remission-controller candidates. |
| ESM / protein language models | Blocked locally | `esm` missing, no local weights; protein prediction is secondary because most parked candidates are receptors/signaling/nuclear regulators with prior-art/druggability questions rather than structure-first enzyme pockets. |
| RDKit / docking | Blocked locally | `rdkit` missing; no current chemistry-first candidate requiring docking. |
| CPA | Missing | `cpa` not installed; no trained perturbation model available. |
| DoRothEA through `decoupler` | Package missing | Could be approximated by Enrichr/OmniPath API, but no local decoupler workflow is runnable now. |
| Official Geneformer package workflow | Missing package | The custom lightweight Geneformer engine is runnable; official `InSilicoPerturberStats` is not installed. |

## Recommended Next Test

Run a Wave69-D GSE282122 myeloid remission-centroid Geneformer deletion screen.

Rationale:

- It directly tests the current parked gene/controller branch rather than reusing older disease/control contexts.
- It uses real local GSE282122 myeloid cells from the same dataset that generated Wave68.
- It uses actual model weights already downloaded and runnable through `transformers`.
- It produces quantitative per-gene embedding shifts with random-token deletion controls.
- It can be immediately cross-checked against Wave68 pseudobulk remission deltas, Wave62 genetics, and any candidate coverage in real perturbation datasets.

Design:

1. Input:
   - `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`
   - `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
   - Geneformer assets in `tmp_v3/foundation_wave6/geneformer_assets/`
2. Candidate panel:
   - Primary parked branch: `RGS14`, `CD274`, `LPP`, `ARHGAP31`, `TNFSF15`, `NCF1`, `CD80`, `FCGR2B`, `IL7R`, `STAT4`, `TNFRSF9`, `DCLRE1B`, `FCGR2A`.
   - Include blocked controls: `SP140` as a negative/prior-art-blocked comparator; `STAT1`, `IFNGR1`, `JAK1`, `JAK2`, `CD74` as known inflammatory/APC-axis controls if detected.
3. Contexts:
   - `Mono_macro` and `DC`, analyzed separately.
   - Use paired `Post` cells if enough cells exist; otherwise use all cells while preserving `Patient`, `Disease`, `Site`, `Treatment`, `Remission_status`, and `Batch`.
4. Goal geometry:
   - Disease-start cells: post-treatment non-remission cells, or pre-treatment cells from non-remitters if post-treatment counts are too low.
   - Goal centroid: post-treatment remission cells within the same broad state, with disease/site balancing where possible.
   - Positive model signal: deleting/inhibiting a candidate token moves start-cell embeddings toward the remission centroid more than random-token deletions and in the same direction as Wave68 remission-associated expression change.
5. Guardrails:
   - Require at least 10 candidate-expressing start cells per state; otherwise mark gene `not_testable_low_token_detection`.
   - Require random-token controls with fixed seed `20260527`.
   - Report both cosine shift and projection along the non-remission-to-remission axis.
   - No therapeutic claim from Geneformer alone; require alignment with real perturbation or network/druggability evidence.

Suggested entry point:

```bash
.venv_v3_py312/bin/python scripts/v3_wave69d_gse282122_geneformer_remission_delete.py
```

Recommended output files:

- `results_v3/wave69d_gse282122_geneformer_remission_delete/geneformer_remission_delete_metrics.tsv`
- `results_v3/wave69d_gse282122_geneformer_remission_delete/geneformer_remission_gene_summary.tsv`
- `results_v3/wave69d_gse282122_geneformer_remission_delete/summary.json`
- `results_v3/wave69d_gse282122_geneformer_remission_delete/REPORT.md`

Decision rule:

- Promote for further audit only if a candidate has:
  - at least one state with `n_start_cells_with_token >= 10`;
  - cosine shift toward remission greater than random mean;
  - projection toward remission greater than random mean;
  - z-score versus random deletion `> 0.5`;
  - no existing prior-art/directionality blocker; and
  - independent support from Wave62 genetics or real perturbation/network sign-consistency.
- Demote if the model shift is absent, opposite, low-detection, or only seen for blocked/prior-art candidates.

## Secondary Fast Test

In parallel or immediately after Wave69-D, run an OmniPath sign-consistency audit:

- Fetch directed signed interactions for candidates plus module genes.
- Build a small graph with `networkx`.
- Score whether candidate inhibition or activation predicts the observed Wave68 remission direction for HLA-II/APC, cytokine, lipid-lysosomal, Fc receptor, and TNF-superfamily genes.
- Use this as mechanistic plausibility filtering, not causal validation.

This is lower-value than the Geneformer remission-centroid test but faster and orthogonal.

## Verdict

The best replacement for unavailable State/Stack/Evo2 is not another bulk signature score. It is a narrow, cell-resolved Geneformer deletion test on GSE282122 myeloid remission geometry, backed by random-token controls and then filtered through real perturbation and OmniPath/network evidence. Arc State remains useful only as feature-agnostic cytokine-perturbation calibration until the 2,000 HVG feature IDs can be mapped to genes.
