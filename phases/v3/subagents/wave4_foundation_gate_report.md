# Wave 4 Foundation-Model Gate Report

Returned: 2026-05-26 22:02 UTC

## State gate result

State is **blocked for named-gene module scoring** in this environment right now.

Checked file:

- `data/raw_v3/state_parse_split4/adata_real.h5ad`
- local size: `5,619,356,404` bytes
- HDF5 stored EOF from open attempt: `9,112,404,896` bytes
- missing bytes: `3,493,048,492`
- completion fraction: `61.67%`
- modification time: `2026-05-26T23:59:29+0200`
- no active `curl`/HF download process was detected by `pgrep -fl 'curl|huggingface|hf|adata_real'`

`anndata.read_h5ad(..., backed="r")` failed with:

```text
OSError: Unable to synchronously open file (truncated file: eof = 5619356404, sblock->base_addr = 0, stored_eof = 9112404896)
```

Therefore `scripts/v3_analyze_state_parse_cd14.py` cannot recover the exact 2,000-feature HVG order from `adata_real.var_names`, and State cannot currently produce valid named-gene predictions for `CD74`, `IFI30`, `CTSS`, `STAT1`, `TAP1`, `B2M`, `HLA-DRA`, or related modules.

## Commands run

Read required context:

```bash
sed -n '1,220p' TOOLS_V3.md
sed -n '1,240p' BLOCKERS_V3.md
sed -n '1,520p' scripts/v3_analyze_state_parse_cd14.py
./.venv_v3_py312/bin/python -m json.tool results_v3/state_parse_cd14_summary.json
sed -n '1,260p' subagents_v3/foundation_fallback_report.md
```

Gate checks:

```bash
ls -lh data/raw_v3/state_parse_split4/adata_real.h5ad \
  data/raw_v3/state_parse_split4/adata_pred.h5ad \
  data/raw_v3/state_parse_split4/CD14_Mono_pred_de.csv \
  data/raw_v3/state_parse_split4/CD14_Mono_real_de.csv \
  tmp_v3/var_dims_split4.pkl

stat -f '%N size_bytes=%z modified=%Sm' -t '%Y-%m-%dT%H:%M:%S%z' \
  data/raw_v3/state_parse_split4/adata_real.h5ad \
  data/raw_v3/state_parse_split4/adata_pred.h5ad

./.venv_v3_py312/bin/python - <<'PY'
from pathlib import Path
import pickle
p = Path('data/raw_v3/state_parse_split4/adata_real.h5ad')
print('path', p)
print('exists', p.exists())
if p.exists():
    print('size_bytes', p.stat().st_size)
with open('tmp_v3/var_dims_split4.pkl', 'rb') as fh:
    var = pickle.load(fh)
print('output_dim', var.get('output_dim'))
try:
    import anndata as ad
    a = ad.read_h5ad(p, backed='r')
    print('openable True')
    print('n_obs', a.n_obs, 'n_vars', a.n_vars)
    print('var_names_head', list(map(str, a.var_names[:20])))
    a.file.close()
except Exception as exc:
    print('openable False')
    print('error_type', type(exc).__name__)
    print('error', exc)
PY

./.venv_v3_py312/bin/python - <<'PY'
from pathlib import Path
size = Path('data/raw_v3/state_parse_split4/adata_real.h5ad').stat().st_size
stored = 9112404896
print('size_bytes', size)
print('stored_eof_bytes', stored)
print('missing_bytes', stored - size)
print('percent_complete', f'{100 * size / stored:.2f}%')
PY

pgrep -fl 'curl|huggingface|hf|adata_real' || true
```

Output-table validation:

```bash
head -n 5 results_v3/state_parse_cd14_de_with_gene_symbols.tsv
head -n 12 results_v3/state_parse_cd14_axis_scores.tsv
wc -l results_v3/state_parse_cd14_transition_target_rank.tsv

./.venv_v3_py312/bin/python - <<'PY'
import pandas as pd
p = 'results_v3/state_parse_cd14_de_with_gene_symbols.tsv'
df = pd.read_csv(p, sep='\t', usecols=['gene'])
print('n_rows', len(df))
print('n_unique_gene_values', df['gene'].nunique())
print('n_feature_placeholders', df['gene'].astype(str).str.startswith('FEATURE_').sum())
for g in ['CD74', 'IFI30', 'CTSS', 'STAT1', 'TAP1', 'B2M', 'HLA-DRA']:
    print(g, int((df['gene'].astype(str) == g).sum()))
PY
```

Note: `python -m json.tool ...` failed because `python` is not on PATH; all Python checks were rerun with `./.venv_v3_py312/bin/python`.

## Valid outputs or blocker

Valid current State-derived output is limited to **feature-agnostic perturbation validation** from the already downloaded released CSVs:

- `results_v3/state_parse_cd14_summary.json`
- `results_v3/state_parse_cd14_per_target_validation.tsv`
- `results_v3/state_parse_cd14_focused_per_target_validation.tsv`

The feature-agnostic summary reports:

- model repo: `arcinstitute/ST-HVG-Parse`
- model SHA: `a69af46d5b8c6f8c036c489a8f71354f321d968b`
- split: `fewshot/split_4`
- cell type: `CD14_Mono`
- perturbations: `62`
- output features: `2000`
- IFN-gamma feature-agnostic validation: Spearman `0.47930399664071527`, direction match `0.7086978898610397`, significant-feature recall `0.8173553719008264`, significant-feature precision `0.7397157816005984`

These are valid only as anonymous-feature model calibration. They do **not** support a named-gene autoimmune-module claim.

Direct output-table validation found:

- `results_v3/state_parse_cd14_de_with_gene_symbols.tsv`: `248,000` rows
- all `248,000` rows have `gene` values beginning with `FEATURE_`
- observed counts for named genes: `CD74=0`, `IFI30=0`, `CTSS=0`, `STAT1=0`, `TAP1=0`, `B2M=0`, `HLA-DRA=0`
- `results_v3/state_parse_cd14_axis_scores.tsv`: all module rows have `n_genes=0`
- `results_v3/state_parse_cd14_transition_target_rank.tsv`: one header line only; no ranked targets

The current `state_parse_cd14_summary.json` contains an internally inconsistent stale field, `n_mapped_features: 2000`, while the actual table contains only `FEATURE_n` placeholders. The valid interpretation is the table-level one: gene-resolved State scoring is blocked.

## Geneformer fallback command plan

Do not launch this as part of the gate. This is the CPU-feasible next-step plan if the orchestrator decides the session needs a model-derived named-gene hypothesis despite State being blocked.

Create an isolated environment:

```bash
python3.12 -m venv .venv_geneformer_cpu
. .venv_geneformer_cpu/bin/activate
pip install --upgrade pip
pip install torch anndata scanpy datasets pyarrow scikit-learn scipy pandas numpy tqdm huggingface_hub
pip install --no-deps git+https://huggingface.co/ctheodoris/Geneformer@04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5
```

Download only the V2-104M assets and dictionaries:

```bash
. .venv_geneformer_cpu/bin/activate
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='ctheodoris/Geneformer',
    revision='04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5',
    local_dir='data/raw_v3/geneformer',
    allow_patterns=[
        'Geneformer-V2-104M/model.safetensors',
        'Geneformer-V2-104M/config.json',
        'Geneformer-V2-104M/generation_config.json',
        'geneformer/token_dictionary_gc104M.pkl',
        'geneformer/gene_median_dictionary_gc104M.pkl',
        'geneformer/gene_name_id_dict_gc104M.pkl',
        'geneformer/ensembl_mapping_dict_gc104M.pkl',
    ],
)
PY
```

Prepare a capped real-cell input set before tokenization:

```bash
. .venv_geneformer_cpu/bin/activate
python scripts/v3_prepare_geneformer_autimmune_subset.py \
  --input-h5ads data/raw_v3/cell_state/ibd_human_10x.h5ad \
                data/raw_v3/cell_state/psoriasis_skin.h5ad \
                data/raw_v3/cell_state/sjogren_salivary.h5ad \
  --max-cells-per-disease-state 250 \
  --target-compartments myeloid epithelial apc \
  --var-ensembl-source var_names \
  --output-h5ad data/derived_v3/geneformer/autimmune_capped_real_cells.h5ad
```

Tokenize real cells only:

```bash
. .venv_geneformer_cpu/bin/activate
python scripts/v3_tokenize_geneformer_autimmune_subset.py \
  --input-h5ad data/derived_v3/geneformer/autimmune_capped_real_cells.h5ad \
  --model-dir data/raw_v3/geneformer \
  --output-dir data/derived_v3/geneformer/tokenized_autimmune_capped
```

Run a bounded perturbation job only after tokenization QC passes:

```bash
. .venv_geneformer_cpu/bin/activate
python scripts/v3_run_geneformer_perturbation_gate.py \
  --tokenized-dataset data/derived_v3/geneformer/tokenized_autimmune_capped \
  --model-dir data/raw_v3/geneformer/Geneformer-V2-104M \
  --genes IFNGR1 IFNGR2 JAK1 JAK2 STAT1 IRF1 CIITA RFX5 CD74 HLA-DRA HLA-DRB1 IFI30 CTSS TAP1 TAP2 B2M \
  --mode delete \
  --goal-state matched_control \
  --max-cells 1500 \
  --random-seed 20260526 \
  --output-dir results_v3/geneformer_gate
```

Expected valid output would be `InSilicoPerturber` raw pickle files plus `InSilicoPerturberStats` CSVs with named genes, Ensembl IDs, detection counts, shift-to-goal metrics, p-values, and FDR. This should be treated as a **model hypothesis**, not as expression log2FC or causal validation, and should be compared against Mixscale CRISPRi ranks.

## Invalid-output rules

Invalid for State:

- any claim using anonymous `FEATURE_n` values as genes
- any feature-to-gene mapping guessed from `var_dims.pkl["gene_names"]`
- any named-gene module score while `adata_real.h5ad` is truncated or unreadable
- de novo State inference using pseudo-AnnData outside the trained feature space
- treating the current `n_mapped_features: 2000` summary field as valid when output tables are all `FEATURE_n`

Invalid for Geneformer:

- launching full all-cell or all-gene perturbation on CPU and calling partial/stalled output valid
- using synthetic or pseudo-cells
- omitting donor/state metadata needed to define matched control goals
- claiming transcriptomic log2FC from embedding-shift outputs
- claiming therapeutic efficacy without comparison to real perturbation data
- using genes absent from the Geneformer token dictionary without reporting them as dropped

## Recommendation

State should **not** be used for named-gene foundation-model evidence until `adata_real.h5ad` is resumed to the full stored EOF and opens successfully with `anndata.read_h5ad(..., backed="r")`.

Given the current gate result, the V3 orchestrator should rely on **Mixscale CRISPRi** as the valid substitute perturbation evidence for named-gene transition control. Geneformer V2-104M is the next CPU-feasible foundation-model fallback, but it should be launched only as a bounded model-hypothesis job after a real-cell capped input set and tokenization QC are in place.
