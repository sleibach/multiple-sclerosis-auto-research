# Wave 6 Foundation Named-Gene Report

Returned: 2026-05-26 22:27 UTC

## Attempts

### 1. Arc State released-output gate

Checked the previously blocked State file:

```bash
stat -f '%N %z bytes' data/raw_v3/state_parse_split4/adata_real.h5ad
.venv_v3_py312/bin/python - <<'PY'
import anndata as ad
p = "data/raw_v3/state_parse_split4/adata_real.h5ad"
a = ad.read_h5ad(p, backed="r")
print(a.shape)
print(list(map(str, a.var_names[:30])))
print(list(map(str, a.var.columns)))
a.file.close()
PY
```

Result:

- `adata_real.h5ad` is now complete by stored EOF: `9,112,404,896` bytes.
- It opens successfully with `anndata.read_h5ad(..., backed="r")`.
- Shape: `(1,125,352, 2,000)`.
- `var_names` are numeric feature IDs: `0..1999`.
- `adata.var` has no columns.

Interpretation: State is still blocked for named-gene claims. The large AnnData being complete resolves the HDF5 truncation blocker but not the gene-mapping blocker. The released CD14 DE CSVs and `adata_real.h5ad` both expose anonymous features only. `tmp_v3/var_dims_split4.pkl` contains `gene_names` of length `18,308`, but it does not encode the 2,000-HVG output order. Mapping feature `0..1999` to the first 2,000 names would still be an unjustified guess.

I did not rerun `scripts/v3_analyze_state_parse_cd14.py` because this worker was scoped away from `results_v3`, and direct inspection already shows that a valid named-gene map is unavailable.

### 2. Geneformer V2-104M scratch route

Downloaded official Geneformer V2-104M assets into scratch:

```bash
.venv_v3_py312/bin/python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="ctheodoris/Geneformer",
    revision="04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5",
    local_dir="tmp_v3/foundation_wave6/geneformer_assets",
    allow_patterns=[
        "Geneformer-V2-104M/model.safetensors",
        "Geneformer-V2-104M/config.json",
        "Geneformer-V2-104M/generation_config.json",
        "geneformer/token_dictionary_gc104M.pkl",
        "geneformer/gene_median_dictionary_gc104M.pkl",
        "geneformer/gene_name_id_dict_gc104M.pkl",
        "geneformer/ensembl_mapping_dict_gc104M.pkl",
    ],
)
PY
```

Then ran a bounded real-cell deletion screen:

```bash
.venv_v3_py312/bin/python tmp_v3/foundation_wave6/geneformer_tiny_delete_screen.py
```

Output files:

- `tmp_v3/foundation_wave6/geneformer_tiny_delete_screen/summary.json`
- `tmp_v3/foundation_wave6/geneformer_tiny_delete_screen/geneformer_tiny_delete_metrics.tsv`

This route used `transformers.BertModel.from_pretrained(...)` directly, not the official Geneformer `InSilicoPerturberStats` package workflow. It is therefore valid only as a lightweight named-gene embedding perturbation screen.

## Model / Version / Weights

Model:

- Geneformer V2-104M
- Hugging Face repo: `ctheodoris/Geneformer`
- Revision: `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`
- Encoder parameters loaded: `104,365,056`
- Runtime: local macOS CPU, `.venv_v3_py312`
- Seed: `20260527`
- Max sequence length: `512`

Downloaded asset checksums:

```text
fff5cba29ddd8792991fa77b4872246fbe548a178cebda3775cdc72b67780e7f  Geneformer-V2-104M/model.safetensors
467d4492f0dd53b4d60afffe20812db484ca1cf9fdbeb6a6e060e93564f70859  Geneformer-V2-104M/config.json
67c445f4385127adfc48dcc072320cd65d6822829bf27dd38070e6e787bc597f  geneformer/token_dictionary_gc104M.pkl
```

Model-load caveat: loading as `BertModel` ignores the masked-LM head and initializes no pooler weights. That is acceptable for CLS/encoder embedding extraction, but it is not a full masked-LM or official Geneformer perturbation-statistics run.

## Candidate Genes Tested

All requested genes were present in the Geneformer token dictionary:

| Gene | Ensembl ID | Token |
|---|---:|---:|
| `OSM` | `ENSG00000099985` | `2136` |
| `OSMR` | `ENSG00000145623` | `8601` |
| `IL6ST` | `ENSG00000134352` | `6790` |
| `STAT3` | `ENSG00000168610` | `12179` |
| `SOCS3` | `ENSG00000184557` | `15093` |
| `C1QA` | `ENSG00000173372` | `13224` |
| `C1QB` | `ENSG00000173369` | `13223` |
| `C1QC` | `ENSG00000159189` | `10154` |
| `C3` | `ENSG00000125730` | `5626` |
| `C3AR1` | `ENSG00000171860` | `12911` |
| `C5AR1` | `ENSG00000197405` | `16472` |
| `CD74` | `ENSG00000019582` | `395` |
| `IFNGR1` | `ENSG00000027697` | `465` |
| `STAT1` | `ENSG00000115415` | `4387` |

Real-cell contexts:

| Context | Dataset | Disease cells | Control cells | Mean tokenized length |
|---|---|---:|---:|---:|
| `IBD_myeloid` | `data/raw_v3/cell_state/ibd_human_10x.h5ad` | 24 | 24 | 454.77 |
| `IBD_stromal` | `data/raw_v3/cell_state/ibd_human_10x.h5ad` | 24 | 24 | 512.00 |
| `psoriasis_keratinocyte` | `data/raw_v3/cell_state/psoriasis_skin.h5ad` | 24 | 24 | 512.00 |
| `sjogren_APC` | `data/raw_v3/cell_state/sjogren_salivary.h5ad` | 24 | 24 | 427.73 |

Disease cells were enriched for candidate-gene expression to make the feasibility screen informative. Controls were normal cells from the same compartment. This means effect sizes are not population estimates.

## Real Outputs

Metric: delete the candidate gene token from a real disease-cell Geneformer sequence, re-embed, and measure movement toward the matched normal/control centroid. Positive `mean_shift_to_control_cosine` or positive `mean_projection_to_control` means the perturbed disease-cell embedding moved toward control by that metric.

Aggregate across contexts with detected candidate tokens:

| Gene | Contexts with token | Disease cells with token | Mean cosine shift | Mean projection shift |
|---|---:|---:|---:|---:|
| `CD74` | 4 | 28 | `-0.000012` | `-0.007021` |
| `IFNGR1` | 4 | 18 | `-0.000118` | `-0.008495` |
| `STAT3` | 4 | 18 | `-0.000335` | `-0.010721` |
| `STAT1` | 3 | 17 | `-0.000003` | `0.002537` |
| `C3` | 2 | 4 | `0.000444` | `0.034535` |
| `C1QB` | 2 | 7 | `0.000196` | `-0.035143` |
| `C5AR1` | 2 | 11 | `0.000087` | `-0.021197` |
| `C3AR1` | 2 | 5 | `-0.000107` | `-0.032497` |
| `SOCS3` | 2 | 19 | `-0.000263` | `0.025294` |
| `IL6ST` | 2 | 11 | `-0.000430` | `-0.021453` |
| `OSM` | 2 | 6 | `-0.000696` | `-0.055166` |
| `C1QC` | 2 | 4 | `-0.000703` | `0.007644` |
| `C1QA` | 2 | 11 | `-0.000938` | `-0.012400` |
| `OSMR` | 1 | 2 | `0.000111` | `0.024087` |

Most informative context-gene rows:

| Context | Gene | Cells with token | Cosine shift | Projection shift | Read |
|---|---|---:|---:|---:|---|
| `sjogren_APC` | `C3` | 3 | `0.000797` | `0.038967` | weak positive model signal |
| `psoriasis_keratinocyte` | `OSMR` | 2 | `0.000111` | `0.024087` | very sparse weak positive model signal |
| `IBD_myeloid` | `STAT1` | 11 | `0.000094` | `0.014324` | weak positive in one context |
| `IBD_stromal` | `IFNGR1` | 3 | `0.000115` | `0.012657` | weak positive in one context |
| `IBD_myeloid` | `C5AR1` | 10 | `0.000313` | `-0.002834` | discordant metrics |
| `IBD_myeloid` | `CD74` | 15 | `-0.001012` | `-0.057563` | negative by both metrics |
| `IBD_myeloid` | `C1QA` | 6 | `-0.001090` | `-0.136349` | negative by both metrics |

Random non-candidate deletion controls had mean cosine shifts near zero and context SDs of about `0.00046-0.00101`. The candidate shifts are small and mostly within this scale. No formal p-value or FDR is claimed from this tiny run.

## Validation Against Real Perturbation Data

Existing Mixscale/Perturb-seq output remains stronger than the Geneformer tiny screen for the residual IFN baseline:

| Perturbation | Pathway | Transition suppression score | Modules suppressed | IFN/APC mean log2FC | HLA-II/APC mean log2FC | MIF-CD74 mean log2FC |
|---|---|---:|---:|---:|---:|---:|
| `IFNGR1` | `IFNG` | `2.485777` | 4/4 | `-1.491783` | `-1.604867` | `-0.534073` |
| `STAT1` | `IFNG` | `1.899942` | 4/4 | `-1.252608` | `-1.107283` | `-0.281576` |

Geneformer did not robustly recapitulate those strong IFN-axis perturbation effects: `IFNGR1` was detected in all four contexts but had aggregate mean cosine shift `-0.000118`; `STAT1` was near zero aggregate mean cosine shift `-0.000003`. Therefore the Geneformer tiny screen should not override Mixscale.

No real perturbation validation was found in the existing local Mixscale tables for `OSMR`, `OSM`, `IL6ST`, `SOCS3`, `C1QA`, `C1QB`, `C1QC`, `C3`, `C3AR1`, or `C5AR1` as perturbagens. Those axes remain model-only in this wave.

## Blockers

- **Arc State named genes:** still blocked. The completed `adata_real.h5ad` has only numeric feature IDs and empty `var` metadata.
- **State output order:** unresolved. `var_dims_split4.pkl` does not identify which 2,000 HVGs correspond to feature IDs `0..1999`.
- **Official Geneformer perturbation statistics:** not run. This wave used direct encoder embedding deletion to avoid mutating the shared environment. A full official `InSilicoPerturberStats` job would require installing `geneformer` and running a larger, slower workflow.
- **Candidate sparsity:** `OSMR` appeared in only 2 selected psoriasis keratinocyte disease cells; `C3` in only 4 disease cells across two contexts; several OSM/OSMR/complement genes were not detected in selected disease cells for some compartments.
- **Model-output strength:** embedding shifts are tiny and mostly within the scale of random deletion controls.
- **scGPT/scFoundation:** not attempted after Geneformer produced a real named-gene run. scGPT perturbation utilities generally require perturbation-trained/fine-tuned setup; a zero-shot embedding-only scGPT result would not be stronger than the Geneformer result above.

## Recommendation For Orchestrator

Real named-gene foundation-model inference is feasible in this environment via the Geneformer V2-104M scratch route. However, this wave does **not** provide strong foundation-model support for declaring `OSM/OSMR` or complement/C1q the central cross-autoimmune node.

Use this result as follows:

- Do **not** claim Arc State named-gene evidence.
- Treat Geneformer output as a weak model-hypothesis screen only.
- If the current central-axis choice needs foundation-model support, the most defensible next run is a larger official Geneformer `InSilicoPerturberStats` job focused on `C3/C3AR1/C5AR1` in Sjogren/IBD APC and `OSMR/IL6ST/STAT3/SOCS3` in psoriasis/IBD stromal-epithelial contexts, with `max_len >= 1024` and enough candidate-token detections for empirical null testing.
- For validated perturbation evidence today, keep Mixscale as the backbone for `IFNGR1/STAT1`; this wave found no comparable real perturbation support for `OSMR` or complement perturbagens.
