# Foundation-Model Fallback Report

Returned: 2026-05-26

## Verdict

Use a conditional route:

1. **First choice if the download finishes cleanly: Arc State, released ST-HVG-Parse CD14 monocyte split 4.** This is the only route here that directly addresses cytokine perturbation of CD14 monocytes and can potentially produce gene-resolved IFN-gamma response predictions for the `HLA-II/CD74/IFI30/CTSS/TAP/B2M` transition. Current local status is **not valid yet** because `data/raw_v3/state_parse_split4/adata_real.h5ad` is still incomplete/truncated and cannot be opened by HDF5.
2. **Best CPU-feasible fallback: Geneformer V2-104M zero-shot in silico perturbation on real local h5ad cells.** This can produce traceable named-gene perturbation predictions as embedding/state-shift outputs. It is weaker than State and weaker than real Perturb-seq because it does not produce transcriptome log2FC by itself.
3. **Best substitute if a valid model route is required to produce expression-level evidence today: Mixscale real CRISPRi Perturb-seq, not a foundation model.** This is already in the workspace and is more defensible evidence than pseudo-AnnData or anonymous State features.

No synthetic pseudo-data should be used. Any Geneformer perturbation output must be labeled as **model hypothesis**, not experimental evidence, and compared against Mixscale where possible.

## Local Feasibility

Workspace: `/Users/soeren.leibach/Projects/ms-auto-research`

Runtime observed:

- macOS 26.5, Apple M4 Pro, 14 CPU cores, 48 GiB RAM.
- `.venv_v3_py312`: Python 3.12.10, `torch 2.12.0`, `transformers 5.9.0`, `anndata 0.12.16`, `scanpy 1.12.1`, `scvi-tools 1.4.3`.
- `geneformer` and `scgpt` are not installed in the current venv.
- The local direct h5ads already have Ensembl IDs as `var_names`; IBD and psoriasis need an added `obs["n_counts"]`, while Sjogren already has `n_counts`/`total_counts`.

## Route 1: State, Conditional Best Route

Source and weights:

- Code: `https://github.com/ArcInstitute/state`
- Released output/model repo: `https://huggingface.co/arcinstitute/ST-HVG-Parse`
- Repo SHA verified by HF API: `a69af46d5b8c6f8c036c489a8f71354f321d968b`
- Relevant files:
  - `fewshot/split_4/data_module.torch`
  - `fewshot/split_4/pert_onehot_map.pt`
  - `fewshot/split_4/var_dims.pkl`
  - `fewshot/split_4/checkpoints/best.ckpt` (~540 MB)
  - `fewshot/split_4/eval_best.ckpt/CD14_Mono_pred_de.csv`
  - `fewshot/split_4/eval_best.ckpt/CD14_Mono_real_de.csv`
  - `fewshot/split_4/eval_best.ckpt/adata_real.h5ad` (HDF5 stored EOF ~9.11 GB)

Current local blocker:

- Existing `results_v3/state_parse_cd14_summary.json` is feature-agnostic only.
- `scripts/v3_analyze_state_parse_cd14.py` correctly refuses gene-module conclusions unless the 2,000 HVG features can be mapped from `adata_real.h5ad`.
- Attempted open of the local `adata_real.h5ad` failed with HDF5 truncation: local EOF was below stored EOF `9112404896`.
- A background `curl -C -` download is currently resuming that file. Until `anndata.read_h5ad(..., backed="r")` succeeds, State is blocked for gene-resolved output.

Expected input format:

- Completed `adata_real.h5ad` with `n_vars == 2000` and `var_names` matching the released DE feature order.
- Released CD14 files already local:
  - `data/raw_v3/state_parse_split4/CD14_Mono_pred_de.csv`
  - `data/raw_v3/state_parse_split4/CD14_Mono_real_de.csv`
  - `tmp_v3/var_dims_split4.pkl`

Valid output:

- Rerun: `.venv_v3_py312/bin/python scripts/v3_analyze_state_parse_cd14.py`
- Valid only if:
  - `results_v3/state_parse_cd14_de_with_gene_symbols.tsv` has symbols such as `CD74`, `IFI30`, `CTSS`, `TAP1`, `TAP2`, `B2M`, `STAT1`, not `FEATURE_n`.
  - `results_v3/state_parse_cd14_summary.json` reports mapping from `adata_real.var_names`.
  - `module_scoring_status == "completed"`.
  - `results_v3/state_parse_cd14_transition_target_rank.tsv` is non-empty.
- Biologically useful output would be IFN-gamma predicted-vs-real signed effect for the transition genes/modules in CD14 monocytes. That would be a traceable State model prediction with matched real perturbation comparison.

Invalid output:

- Anonymous `FEATURE_n` effects.
- Mapping feature IDs by guessing from `var_dims.pkl`.
- De novo State inference using pseudo-AnnData not in the trained feature space.

## Route 2: Geneformer V2-104M, CPU Fallback

Recommendation:

Use Geneformer V2-104M for a small, donor-balanced, real-cell in silico perturbation screen. This is CPU-feasible on the local machine if capped to selected cells and genes.

Source and weights:

- Repo/model: `https://huggingface.co/ctheodoris/Geneformer`
- HF repo SHA verified: `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`
- License: Apache-2.0
- Use the smaller V2 model:
  - `Geneformer-V2-104M/model.safetensors`, 417,571,156 bytes
  - `Geneformer-V2-104M/config.json`
  - `Geneformer-V2-104M/generation_config.json`
  - `geneformer/token_dictionary_gc104M.pkl`
  - `geneformer/gene_median_dictionary_gc104M.pkl`
  - `geneformer/gene_name_id_dict_gc104M.pkl`
  - `geneformer/ensembl_mapping_dict_gc104M.pkl`
- Do not use V2-316M for this first pass; its weight file is 1,265,455,076 bytes and is less suitable for CPU iteration.

Install feasibility:

- Use a separate environment rather than mutating `.venv_v3_py312`.
- CPU-only install should avoid quantized/bitsandbytes paths on macOS.
- Practical pattern:

```bash
python3.12 -m venv .venv_geneformer_cpu
. .venv_geneformer_cpu/bin/activate
pip install --upgrade pip
pip install torch anndata scanpy datasets pyarrow scikit-learn scipy pandas numpy tqdm huggingface_hub
pip install --no-deps git+https://huggingface.co/ctheodoris/Geneformer@04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5
```

Expected input format:

- Raw-count scRNA-seq `.h5ad`, no feature selection.
- Required gene attribute: Ensembl ID. In the local CZI h5ads, Ensembl IDs are already `var_names`; create `adata.var["ensembl_id"] = adata.var_names`.
- Required cell attribute: `obs["n_counts"]`; compute as per-cell raw count sum for IBD and psoriasis before tokenization.
- Preserve metadata as tokenized dataset attributes: `disease`, `donor_id`, `cell_type`, `compartment`, and source dataset.
- Use only real cells from:
  - `data/raw_v3/cell_state/ibd_human_10x.h5ad`
  - `data/raw_v3/cell_state/psoriasis_skin.h5ad`
  - `data/raw_v3/cell_state/sjogren_salivary.h5ad`
- Recommended first pass: donor-balanced maximum of 100-250 disease cells and 100-250 control cells per compartment, not all cells.

Target perturbation set:

- Upstream/controller: `IFNGR1`, `IFNGR2`, `JAK1`, `JAK2`, `STAT1`, `IRF1`
- HLA-II gate/state: `CIITA`, `RFX5`, `CD74`, `HLA-DRA`, `HLA-DRB1`
- Lysosomal/TAP readout: `IFI30`, `CTSS`, `TAP1`, `TAP2`, `B2M`

Verified Ensembl IDs for key targets from Ensembl REST where available:

- `IFNG` `ENSG00000111537`
- `IFNGR1` `ENSG00000027697`
- `IFNGR2` `ENSG00000159128`
- `JAK1` `ENSG00000162434`
- `JAK2` `ENSG00000096968`
- `STAT1` `ENSG00000115415`
- `IRF1` `ENSG00000125347`
- `CIITA` `ENSG00000179583`
- `RFX5` `ENSG00000143390`
- `CD74` `ENSG00000019582`
- `IFI30` `ENSG00000216490`
- `CTSS` `ENSG00000163131`
- `HLA-DRA` `ENSG00000204287`
- `HLA-DRB1` `ENSG00000196126`
- `HLA-DPA1` `ENSG00000231389`
- `HLA-DPB1` `ENSG00000223865`

Use the Geneformer token dictionary as the final authority before running.

Valid output:

- A tokenized Geneformer `.dataset` derived from real local cells with retained source metadata.
- `InSilicoPerturber` raw pickle outputs from `perturb_type="delete"` or explicitly documented rank-shift perturbation, using `model_type="Pretrained"`, `model_version="V2"`, and `emb_mode="cell"` or `cls`.
- `InSilicoPerturberStats` CSV with at least:
  - `Gene_name`
  - `Ensembl_ID`
  - `N_Detections`
  - `Shift_to_goal_end`
  - `Goal_end_vs_random_pval`
  - `Goal_end_FDR`
  - optionally `Impact_component_percent`
- A valid biological read is: deleting/inhibiting a candidate gene in disease-state cells shifts the embedding toward matched normal/control cells more than random-gene perturbations, with FDR control and enough detections.

What it can and cannot claim:

- Can claim: a traceable Geneformer model hypothesis that a named gene changes the disease-to-control state geometry in real autoimmune cells.
- Cannot claim: expression log2FC, causal validation, or therapeutic efficacy.
- Must compare direction/rank against Mixscale. A credible model-fallback result should rank `IFNGR1/IFNGR2/JAK1/JAK2/STAT1` above downstream effectors for broad transition suppression, or explain why it does not.

Expected runtime:

- Tokenization: minutes to tens of minutes for the selected local subsets.
- V2-104M perturbation: feasible on CPU for tens of genes and hundreds to low-thousands of cells; expect hours, not seconds.
- Full all-cell/all-gene in silico perturbation is not CPU-feasible for this workspace.

## Weaker Comparators

### scGPT

Source and weights:

- HF repo: `https://huggingface.co/perturblab/scgpt-human`
- HF repo SHA verified: `571a0445d68fa48381f863ff75dd4f6d0eae3dfc`
- License: MIT
- Files: `best_model.pt` (205,385,258 bytes), `args.json`, `vocab.json`

Assessment:

- CPU loading is feasible.
- The documented perturbation workflow fine-tunes a model with perturbation data and uses `GEARS`-style loaders. That makes it a poor zero-shot fallback for local autoimmune h5ads unless a real perturbation training/reference set is included.
- Use only as an embedding/reference comparator. A scGPT embedding shift alone is weaker than Geneformer `InSilicoPerturberStats` and weaker than Mixscale.

### scVI / scArches

Current local install: `scvi-tools 1.4.3`.

Assessment:

- CPU-feasible for reference mapping and latent comparison.
- Not a foundation-model perturbation predictor unless using a pretrained reference with documented weights and matching genes.
- Valid outputs are latent embeddings, mapped cell states, and uncertainty/normalized expression estimates. These are useful comparators for disease-state separation, not perturbation evidence.

## Genomic/Protein Model Routes

### AlphaMissense

Source:

- `https://github.com/google-deepmind/alphamissense`
- Precomputed database: `AlphaMissense_hg38.tsv.gz`, `AlphaMissense_gene_hg38.tsv.gz`, `AlphaMissense_aa_substitutions.tsv.gz`

Assessment:

- CPU-feasible because it can be used as a precomputed lookup.
- Valid output: `am_pathogenicity` and `am_class` for a named missense variant in a candidate protein such as `IFI30`, `CTSS`, `CD74`, `IFNGR1`, or `STAT1`.
- Not relevant to the current transition unless the intervention question becomes a specific coding variant or protein engineering question. It will not predict HLA-II/CD74/GILT/TAP cell-state suppression.

### ESM2

Source:

- HF repo: `https://huggingface.co/facebook/esm2_t33_650M_UR50D`
- HF SHA verified: `08e4846e537177426273712802403f7ba8261b6c`
- License: MIT
- `model.safetensors`: 2,609,506,392 bytes

Assessment:

- CPU possible for small protein variant scoring, but slow.
- Less directly useful than AlphaMissense for human missense pathogenicity.
- Not a route for the IFN-gamma/HLA-II/CD74/GILT/TAP cellular transition unless a protein variant is explicitly selected.

### Evo2

Source:

- HF repo: `https://huggingface.co/ArcInstitute/evo2_7b`
- HF SHA verified: `bda0089f92582d5baabf0f22d9fc85f3588f6b58`
- License: Apache-2.0
- `evo2_7b.pt`: 13,766,621,200 bytes

Assessment:

- Not CPU-feasible in this workspace. The local environment is macOS CPU; the Evo2 route is CUDA/Linux-oriented and the weight is large.
- It is also not the first model to use here unless a specific regulatory or coding variant near `IRF1`, `IFI30`, `CD74`, or HLA loci is nominated.

## Best Substitute Evidence

Use the existing Mixscale CRISPRi outputs as the evidence backbone:

- Source dataset: `GSE281048` / Zenodo `10.5281/zenodo.14035992`
- Local file: `data/raw_v3/mixscale/DE_results_all_pathway.zip`
- MD5: `f077cba680a1affc599f5153d99b0e45`
- Current output: `results_v3/mixscale/mixscale_transition_controller_rank.tsv`

Top IFN-gamma controllers already support the transition:

- `IFNGR1`: `ifn_apc=-1.492`, `hla_ii_apc=-1.605`, `mif_cd74_receptor_state=-0.534`, `gilt_lysosomal_apc=-0.266`
- `IFNGR2`: `ifn_apc=-1.451`, `hla_ii_apc=-1.546`, `mif_cd74_receptor_state=-0.515`
- `JAK2`: `ifn_apc=-1.149`, `hla_ii_apc=-1.251`
- `STAT1`: `ifn_apc=-1.253`, `hla_ii_apc=-1.107`
- `RFX5`: narrower `HLA-II/CD74` suppression, not broad IFN/APC suppression

This is not a foundation model, but it is named-gene, real perturbation evidence. It should outrank any Geneformer/scGPT/scVI-only output when making biological claims.

## Final Recommendation

Do **not** treat current State outputs as gene evidence until `adata_real.h5ad` opens and remaps the 2,000 features. If that gate passes, State split 4 CD14 is the strongest foundation-model route for IFN-gamma perturbation.

If the State gate remains blocked, use **Geneformer V2-104M** as the CPU-feasible fallback, capped to real local disease/control cells and the named transition genes. The only valid Geneformer claim is a traceable model-derived ranking of genes whose in silico perturbation shifts disease-state cells toward matched controls.

For evidence, keep **Mixscale CRISPRi** as the best substitute. It already supplies named-gene perturbation effects for the IFN-gamma to HLA-II/CD74/GILT/TAP transition and avoids synthetic pseudo-data.

## Sources Checked

- Arc State repo: `https://github.com/ArcInstitute/state`
- Arc ST-HVG-Parse model/output repo: `https://huggingface.co/arcinstitute/ST-HVG-Parse`
- Geneformer repo/model: `https://huggingface.co/ctheodoris/Geneformer`
- Geneformer tokenizer docs: `https://geneformer.readthedocs.io/en/latest/geneformer.tokenizer.html`
- Geneformer in silico perturber docs: `https://geneformer.readthedocs.io/en/latest/geneformer.in_silico_perturber.html`
- Geneformer perturbation stats docs: `https://geneformer.readthedocs.io/en/latest/geneformer.in_silico_perturber_stats.html`
- scGPT perturbation tutorial: `https://scgpt.readthedocs.io/en/stable/tutorial_perturbation.html`
- scGPT human checkpoint: `https://huggingface.co/perturblab/scgpt-human`
- scVI/scArches reference mapping docs: `https://docs.scvi-tools.org/en/stable/tutorials/notebooks/multimodal/scarches_scvi_tools.html`
- AlphaMissense publication/resource page: `https://deepmind.google/research/publications/21083/`
- AlphaMissense repo: `https://github.com/google-deepmind/alphamissense`
- ESM2 checkpoint: `https://huggingface.co/facebook/esm2_t33_650M_UR50D`
- Evo2 repo: `https://github.com/ArcInstitute/evo2`
- Evo2 7B checkpoint: `https://huggingface.co/ArcInstitute/evo2_7b`
