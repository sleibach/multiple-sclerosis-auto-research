# Wave104 Cross-Disease Cell-State Sidecar

Date: 2026-05-27

Role: local evidence sidecar for `IFI30`, `SP140`, `GALC`, `CD58`, and `IL7R`. This is an evidence map only. It does not claim a `FINDING_V3` result and does not promote a therapeutic target.

## Inputs Read

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/broad_residual_gate/broad_residual_residual_tests.tsv`
- `results_v3/broad_residual_gate/broad_residual_raw_tests.tsv`
- `results_v3/broad_residual_gate/broad_residual_gene_presence.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`
- `results_v3/wave91_lipid_neighborhood_controller_scan/lipid_neighborhood_controller_rank.tsv`
- `results_v3/wave94_accessible_state_rerank/*`
- Compartment/context checks in `direct_h5ad_gene_replication`, `direct_h5ad_cell_state`, `gse253006_tofacitinib_marker`, `gse315138_celiac_marker`, `wave79_targetability_shortlist_*`, and `wave104_genetics_first_lipid_state_convergence_audit`.

## Executive Call

No gene earns a `GO` as a cross-disease causal-state candidate from these local artifacts. `IL7R` has the strongest residualized expression signal, but it is IBD-heavy, not MS-supported, and confounded by known CD127/adaptive-immune biology. `IFI30` is the cleanest lipid-lysosomal/APC marker, not a controller. `SP140` is a genetics/mechanism comparator with local IBD signal but no lesion support. `CD58` is a stratification/comparator axis. `GALC` is the weakest local cell-state case and is treated as a tissue-specific lysosomal/sphingolipid artifact.

| Gene | Evidence classification | Breadth / MS | Residual support | Recommendation |
| --- | --- | --- | --- | --- |
| `IFI30` | Lipid-lysosomal/IFN antigen-processing marker; not causal-state controller | Broad h5ad: 4/17 positive compartments, 3 diseases, 0 FDR10; MS WM delta `0.210`, p `0.380`, FDR `0.914`; lipid-lysosomal neighborhood `True` | Retains only UC myeloid after one covariate adjustment; strict core residual `0` | `PARK` as marker/comparator; no target claim |
| `SP140` | Myeloid/chromatin genetics comparator; marker, not lipid-lysosomal state | Broad h5ad: 4/13 positive compartments, 4 diseases, 0 FDR10; MS WM delta `-0.087`, p `0.726`, FDR `0.968` | Retains Crohn myeloid only; strict core residual `0` | `PARK` as Crohn/SP140-loss comparator |
| `GALC` | Tissue-skewed lysosomal/sphingolipid marker/artifact | Broad h5ad: 3/17 positive compartments, 3 diseases, 0 FDR10; MS WM delta `0.190`, p `0.455`, FDR `0.923` | Not present in broad residual gate | `NO_GO` as causal-state candidate |
| `CD58` | Immune-synapse / adaptive-immune marker; stratification comparator | Broad h5ad: 3/17 positive compartments, 3 diseases, 0 FDR10; MS WM delta `0.180`, p `0.311`, FDR `0.910` | Not present in broad residual gate | `PARK` as comparator/stratification axis |
| `IL7R` | Generic cytokine/adaptive-immune axis with IBD residual support | Broad h5ad: 4/16 positive compartments, 3 diseases, 3 FDR10; MS WM delta `-0.654`, p `0.572`, FDR `0.943` | Retains 3 analyses / 2 IBD diseases; strict core residual 1 UC stromal analysis; non-IBD residual `0` | `PARK`; not a cross-disease cell-state finding |

## Cross-Artifacts Notes

- `wave94_accessible_state_rerank`: none of the five genes appears in `candidate_pool.tsv`, `accessible_state_candidate_rank.tsv`, `broad_candidate_summary.tsv`, `broad_candidate_context_rows.tsv`, `ms_candidate_rows.tsv`, response, genetics, or foundation outputs. Wave94 therefore contributes absence, not support.
- `wave91_lipid_neighborhood_controller_scan`: none of the five genes is ranked as a lipid-neighborhood controller.
- `wave91_lipid_lysosomal_module_intervention_rank`: only `IFI30` is present, and its call is `NO_GO_NO_MS_WHITE_MATTER_SINGLE_GENE_ANCHOR`.
- `broad_residual_gate`: only `IFI30`, `SP140`, and `IL7R` are present. `GALC` and `CD58` have no residual-gate row in this artifact.
- Compartment module tables include `IFI30` as a member of IFN/APC, lysosomal/APC, and IFNG-readout modules across direct h5ad, celiac marker, and tofacitinib marker contexts. That is marker/module coverage, not gene-level causal evidence.

## Per-Gene Evidence

### `IFI30`

Broad h5ad statistics:

- Tested compartments: `17`.
- Positive nominal compartments: `4`; negative nominal compartments: `0`; positive FDR10 compartments: `0`.
- Positive diseases: psoriasis, type 1 diabetes mellitus, ulcerative colitis.
- Top positive contexts: UC colon myeloid delta `1.10`, p `0.00999`, FDR `0.234`; T1D beta cell delta `0.812`, p `0.0152`, FDR `0.335`; psoriasis skin stromal delta `0.317`, p `0.0221`, FDR `0.548`; psoriasis skin APC delta `0.537`, p `0.0489`, FDR `0.730`.
- MS white matter: delta `0.210`, p `0.380`, FDR `0.914`; no MS expression anchor.
- Lipid-lysosomal myeloid neighborhood: `True`.

Residual support:

- Broad residual gate raw positive count: `1` analysis / `1` disease.
- Retained positive count: `1` analysis / `1` disease.
- Strict core covariate survivor: `0`.
- Retained residual row: UC colon myeloid after `c1q_phagocytic_myeloid` adjustment, residual delta `0.764`, p `0.0366`; raw delta `0.765`.
- Direct h5ad gene replication has only UC myeloid nominal support: detection fraction delta `0.188`, p `0.0188`, FDR `0.217`; mean z delta `0.765`, p `0.0365`, FDR `0.268`.

Wave91 / Wave94:

- Wave91 module row: modules `ifn_apc;lysosomal_apc`; direct positive p<0.05 disease count `1` (`ulcerative colitis`); IBD anti-TNF nonresponse anchor present; RA `NO_SUPPORT`; psoriasis `NONRESPONSE_HIGH_WEAK`; MS `MS_WM_NULL_OR_WEAK`; final call `NO_GO_NO_MS_WHITE_MATTER_SINGLE_GENE_ANCHOR`; module intervention score `4.5`.
- Wave94: absent from accessible-state rerank outputs.

Confounders:

- `IFI30` sits inside IFN/APC, HLA/antigen-processing, and lysosomal modules. The local signal reads as a downstream antigen-processing/lysosomal marker.
- Residual support is single-disease and single-compartment after covariate adjustment, with no strict residual core survivor.
- MS white matter is null and response evidence is not coherent enough to separate causal control from inflammatory APC state.

Recommendation: `PARK`. Use as a lipid-lysosomal/APC marker and comparator; do not label as causal-state candidate.

### `SP140`

Broad h5ad statistics:

- Tested compartments: `13`.
- Positive nominal compartments: `4`; negative nominal compartments: `0`; positive FDR10 compartments: `0`.
- Positive diseases: Crohn disease, Sjogren syndrome, psoriasis, ulcerative colitis.
- Top positive contexts: Crohn colon myeloid delta `2.44`, p `0.000990`, FDR `0.103`; UC colon myeloid delta `1.90`, p `0.00335`, FDR `0.155`; Sjogren gland epithelial delta `0.872`, p `0.0118`, FDR `0.844`; psoriasis keratinocyte delta `0.480`, p `0.0416`, FDR `0.402`.
- MS white matter: delta `-0.087`, p `0.726`, FDR `0.968`.
- Lipid-lysosomal myeloid neighborhood: `False`.

Residual support:

- Broad residual gate raw positive count: `1` analysis / `1` disease.
- Retained positive count: `1` analysis / `1` disease.
- Strict core covariate survivor: `0`.
- Retained residual rows are all Crohn colon myeloid and small in scale: after `hla_ii_apc` residual delta `0.255`, p `0.0146`; after `c1q_phagocytic_myeloid` residual delta `0.284`, p `0.0157`; after `complement_phagocytosis`, `complement_effector`, `lipid_loader_repair`, and `mif_cd74_receptor_state`, p remains nominal.

Wave91 / Wave94:

- Not ranked in Wave91 lipid-neighborhood controller scan or module-intervention rank.
- Absent from Wave94 accessible-state rerank outputs.

Confounders:

- The positive local signal is IBD-myeloid plus heterogeneous epithelial/keratinocyte/gland context. It is not a consistent lipid-lysosomal compartment signal.
- The local MS lesion/pseudobulk row is null despite strong genetic-context interest in other artifacts.
- Direction remains a blocker: genetic loss/splicing biology and direct inhibition are not the same therapeutic direction.

Recommendation: `PARK`. Keep as a Crohn/SP140-loss and genetics comparator; not a cross-disease causal-state candidate.

### `GALC`

Broad h5ad statistics:

- Tested compartments: `17`.
- Positive nominal compartments: `3`; negative nominal compartments: `0`; positive FDR10 compartments: `0`.
- Positive diseases: psoriasis, type 1 diabetes mellitus, ulcerative colitis.
- Top positive contexts: T1D ductal cell delta `0.532`, p `0.0127`, FDR `0.373`; psoriasis skin APC delta `0.870`, p `0.0139`, FDR `0.730`; UC colon epithelial delta `1.31`, p `0.0188`, FDR `0.238`.
- MS white matter: delta `0.190`, p `0.455`, FDR `0.923`.
- Lipid-lysosomal myeloid neighborhood: `False`.

Residual support:

- Not present in `broad_residual_gate` summary, raw, residual, or presence outputs.
- No strict residual support and no non-IBD residual support.

Wave91 / Wave94:

- Not ranked in Wave91 lipid-neighborhood controller scan or module-intervention rank.
- Absent from Wave94 accessible-state rerank outputs.

Confounders:

- The positive local contexts are ductal, skin APC, and UC epithelial. That is too compartment-scattered for a causal cell-state call.
- The known lysosomal/sphingolipid biology makes `GALC` a plausible pathway comparator, but the local evidence does not show disease-state control or direction.
- MS white matter is null; residualization is absent.

Recommendation: `NO_GO` as a causal-state candidate. At most keep as a sphingolipid/lysosomal comparator.

### `CD58`

Broad h5ad statistics:

- Tested compartments: `17`.
- Positive nominal compartments: `3`; negative nominal compartments: `0`; positive FDR10 compartments: `0`.
- Positive diseases: Crohn disease, type 1 diabetes mellitus, ulcerative colitis.
- Top positive contexts: UC colon myeloid delta `0.965`, p `0.00224`, FDR `0.138`; T1D acinar cell delta `0.770`, p `0.0140`, FDR `0.444`; Crohn colon myeloid delta `0.596`, p `0.0267`, FDR `0.323`.
- MS white matter: delta `0.180`, p `0.311`, FDR `0.910`.
- Lipid-lysosomal myeloid neighborhood: `False`.

Residual support:

- Not present in `broad_residual_gate` summary, raw, residual, or presence outputs.
- No strict residual support and no non-IBD residual support.

Wave91 / Wave94:

- Not ranked in Wave91 lipid-neighborhood controller scan or module-intervention rank.
- Absent from Wave94 accessible-state rerank outputs.

Other context:

- Wave79 targetability context has a `PARK_TARGETABILITY_SHORTLIST_NODE` row and MS target-resolution context, but the local expression package here does not show MS lesion support or residualized cross-disease state control.

Confounders:

- `CD58` is an immune-synapse/adaptive-immune axis. Local myeloid expression can reflect immune-cell abundance or APC/T-cell contact biology rather than a disease-intrinsic tissue state.
- The T1D positive context is acinar, which weakens compartment specificity.
- Prior branches already treat CD58/CD2 as a comparator/stratification axis rather than a new target-promotion path.

Recommendation: `PARK`. Use as immune-synapse/stratification comparator only; no causal-state or target claim.

### `IL7R`

Broad h5ad statistics:

- Tested compartments: `16`.
- Positive nominal compartments: `4`; negative nominal compartments: `0`; positive FDR10 compartments: `3`.
- Positive diseases: Crohn disease, type 1 diabetes mellitus, ulcerative colitis.
- Top positive contexts: UC colon myeloid delta `6.77`, p `4.39e-05`, FDR `0.030`; Crohn colon myeloid delta `5.71`, p `1.25e-04`, FDR `0.060`; UC colon stromal delta `4.43`, p `0.00135`, FDR `0.0947`; T1D stellate cell delta `2.44`, p `0.0266`, FDR `0.374`.
- MS white matter: delta `-0.654`, p `0.572`, FDR `0.943`.
- Lipid-lysosomal myeloid neighborhood: `False`.

Residual support:

- Broad residual gate raw positive count: `3` analyses / `2` diseases.
- Retained positive count: `3` analyses / `2` diseases.
- Non-IBD retained positive disease count: `0`.
- Strict core covariate survivor: `1` analysis / `1` disease, `ibd_uc_stromal`.
- Top retained residual tests include UC myeloid after `hla_ii_apc` adjustment, residual delta `3.16`, p `0.00115`; UC myeloid after `c1q_phagocytic_myeloid`, residual delta `2.96`, p `0.00198`; Crohn myeloid after `hla_ii_apc`, residual delta `2.20`, p `0.00255`; UC stromal after `complement_effector`, residual delta `2.03`, p `0.00404`; UC stromal after `inflammatory_nfkb`, residual delta `2.17`, p `0.00650`.

Wave91 / Wave94:

- Not ranked in Wave91 lipid-neighborhood controller scan or module-intervention rank.
- Absent from Wave94 accessible-state rerank outputs.

Confounders:

- This is the strongest residualized local signal among the five, but it is IBD-heavy and has no non-IBD residual survivor.
- The MS white-matter signal is negative/null despite genetic interest in context tables.
- `IL7R` is a known CD127/IL-7 immune-axis marker; local tissue signal can reflect lymphoid/APC admixture, inflammatory recruitment, or cytokine-response state rather than a cross-disease lipid-lysosomal causal state.

Recommendation: `PARK`. Use as a positive-control immune-axis / stratification comparator; do not call it a cross-disease causal-state candidate.

## Bottom Line

- `GO`: none.
- `PARK`: `IFI30`, `SP140`, `CD58`, `IL7R`.
- `NO_GO`: `GALC` as a causal-state candidate.

The sidecar supports marker/comparator use only. The strongest local residual evidence is `IL7R`, but its disease and compartment breadth are too narrow after residualization, and MS lesion support is absent. `IFI30` is useful for tracking IFN/lysosomal APC state, not as an upstream state controller. `SP140`, `CD58`, and `GALC` should not be used to claim a new cross-disease cell-state finding from the current local artifacts.
