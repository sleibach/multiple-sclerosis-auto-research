# Blockers V3

This file records blockers without stopping the session.

## 2026-05-26 18:41 UTC

No terminal blocker yet.

Early feasibility risks:

- Arc State/Stack/Evo 2 may require package versions, operating system, GPU, or hosted credentials not present in this macOS CPU workspace.
- The current Python environment is minimal and lacks `torch`, `transformers`, `scanpy`, `anndata`, `requests`, `Bio`, `rdkit`, and `networkx`.
- V2 already blocked direct use of `GSE154609` T1D monocyte data because the platform annotation route required a multi-gigabyte `GPL17692` SOFT file; this can be revisited but must be documented if still blocked.

## 2026-05-26 18:45 UTC

Subagent concurrency blocker: active thread limit is six. Three old V2 agents were still open and blocked part of the first V3 dispatch. They were closed. First V3 wave is now running with six disease agents; remaining disease and modality agents must be batched as active agents return.

## 2026-05-26 18:52 UTC

Evo 2 local inference blocker: official repo requires Linux/WSL2, CUDA 12.1+, cuDNN 9.3+, Python 3.11/3.12, and GPU. This workspace is macOS ARM CPU; Docker exists but daemon is not running. Hosted NVIDIA API is mentioned in official docs but requires credentials not present in environment variables so far. Route: use Evo 2 only if a hosted key or compatible runtime becomes available; otherwise document as unavailable and do not fabricate genomic foundation-model output.

State/Stack package provisioning succeeded, but full checkpoint inference may still be compute-heavy. Official State released prediction/real DE files are available and have been downloaded for a CD14 monocyte benchmark.

## 2026-05-26 18:56 UTC

State released-output gene mapping blocker: `CD14_Mono_pred_de.csv` and `CD14_Mono_real_de.csv` expose numeric features `0..1999`, not gene symbols. The companion files that likely encode exact HVG order are `adata_real.h5ad` and `adata_pred.h5ad`, each `9,112,404,896` bytes. Downloading both would be about `18.2 GB`. Until the HVG order is recovered by a smaller metadata file or a justified download, gene-module scoring from these State outputs is blocked.

## 2026-05-26 19:03 UTC

Subagent context failure: myasthenia gravis disease-specialist subagent
`019e65a2-e27f-7c92-b6b9-b59b946469f8` failed with a context-window error.
This output is discarded and not counted toward disease breadth. A narrower
replacement was launched as `019e65ac-dd68-7b50-8f83-60e8051487a4`.

## 2026-05-26 19:08 UTC

State de novo inference blocker: `arcinstitute/ST-HVG-Parse` exposes the split
4 checkpoint and config, and the checkpoint size is manageable (~540 MB).
However, `state tx infer` requires real input AnnData with the trained
`X_hvg`/feature space plus perturbation, donor, batch, and cell type metadata.
Constructing a pseudo-AnnData from unrelated expression data would be a
synthetic proxy and cannot support the V3 foundation-model perturbation claim.
Route: use released State CD14 monocyte prediction/real DE files only for
feature-agnostic cytokine-response validation unless a compatible real AnnData
is downloaded or identified.

## 2026-05-26 19:20 UTC

Foundation-model perturbation blocker for the current lead: no valid de novo
State, Stack, or Evo2 perturbation prediction has been run for the
CD74/MIF/IFI30/IRF1 axis. The foundation route scout identified LINCS/CMap and
Mixscale/Perturb-seq as the correct next branch, with large but feasible
downloads. Until that branch is executed, the CD74/MIF-high progressive MS
concept remains a supported translational hypothesis, not a DoD-complete V3
finding.

## 2026-05-26 19:34 UTC

Zenodo API lookup for Mixscale pathway Perturb-seq record `14518762` failed
with DNS resolution error for `zenodo.org`. Hugging Face downloads remained
active at the same time, so this is logged as a transient route-specific network
blocker, not a general network outage. Route: continue State HVG recovery and
retry Zenodo/Perturb-seq later; do not claim Mixscale evidence until the data
are actually downloaded and analyzed.

## 2026-05-26 19:39 UTC

State `adata_real.h5ad` download from Hugging Face transferred about 1.1 GB of
9.1 GB and then failed with `curl: (18) transfer closed`. The partial file is
kept because the command used `-C -` and can resume. Route: prioritize the
smaller Mixscale `DE_results_all_pathway.zip` perturbation archive first, then
resume State if the perturbation branch still needs gene-specific foundation
model support.

## 2026-05-26 19:48 UTC

CELLxGENE Census mirror lookup failed transiently with DNS resolution error for
`census.cellxgene.cziscience.com`. Earlier Census queries succeeded and exposed
the public S3 URI `s3://cellxgene-census-public-us-west-2/cell-census/2025-11-17/soma/`.
Route: attempt direct S3 Census opening, and otherwise use direct CZI h5ad
downloads from Zeno's report.

## 2026-05-26 20:02 UTC

Direct CELLxGENE Census S3 access succeeded for metadata, but repeated
`get_anndata` expression materialization for selected gene subsets stalled for
minutes even on the small psoriasis APC subset and had to be interrupted.
This is a performance/tooling blocker for Census expression extraction in this
workspace, not a biological result. Route: use direct CZI/EBI h5ad downloads
for tractable disease atlases and retain Census metadata only for dataset
selection.

## 2026-05-26 21:24 UTC

RA synovium/macrophage direct h5ad `E-MTAB-8322.project.h5ad` was selected as
the best next tissue by the disease-breadth scout, but repeated HTTPS transfer
attempts to `ftp.ebi.ac.uk` timed out before receiving bytes. A directory-list
request to the same host also returned no content within the timeout. Route:
document the blocker, preserve the recommended accession for later, and switch
to the smaller autoimmune thyroid spatial backup `GSE248205` rather than
spending the hour-four window on a dead transfer.

## 2026-05-26 22:08 UTC

State `adata_real.h5ad` resume reached byte 5,619,356,404 of the expected
9,112,404,896 bytes and then failed again with `curl: (56) Recv failure:
Operation timed out`. This keeps State gene-resolved module scoring blocked.
Route: restarted `curl -L --fail --retry 20 --retry-delay 10 --connect-timeout
30 --speed-time 120 --speed-limit 1024 -C -` from the existing partial file.
Until `anndata.read_h5ad(..., backed="r")` succeeds, State outputs remain
feature-agnostic only and cannot be used as named-gene foundation-model
perturbation evidence.

## 2026-05-26 22:41 UTC

State transfer blocker resolved but replaced by feature-identity blocker:
`adata_real.h5ad` is now readable with `anndata.read_h5ad(..., backed="r")`,
shape `(1125352, 2000)`, but `adata.var_names` are numeric feature IDs and
`adata.var` has no gene-symbol column. Therefore State remains valid only for
feature-agnostic perturbation calibration in this run; it cannot support
named-gene module scoring or named-gene perturbation evidence unless an
official mapping from the 2,000 feature IDs to genes is recovered.

RA atlas route remains blocked: a retry of the EBI FTP/HTTPS directory listing
for `E-MTAB-8322` at 2026-05-26 22:35 UTC timed out during name resolution /
connection without receiving content. Treat as route-specific network blocker,
not as absence of RA biology.

## 2026-05-26 23:09 UTC

SNX10 IBD novelty blocker: after APOC1 failed Geneformer testing, SNX10 became
the strongest second-pass model-supported survivor. However, IBD target novelty
is blocked by existing literature and chemical matter:

- PubMed-indexed work already reports SNX10 in macrophage polarization and
  experimental mouse colitis.
- PubMed-indexed work reports SNX10 inhibition promoting intestinal mucosal
  healing through SREBP2-mediated stemness restoration.
- Reagent/vendor records list `DC-SX029` as an orally active SNX10-PIKFYVE PPI
  inhibitor with IBD research potential.

Route: keep SNX10 as a mechanistic comparator and possible cross-disease
extension clue. Do not promote it as a novel IBD therapeutic target.

## 2026-05-27 00:12 UTC

SLE targeted CELLxGENE Census expression extraction failed on the first attempt
despite successful metadata access. The selected-gene extractor sampled at most
70,000 cells, then failed during `get_anndata(..., X_name="raw")` with a
TileDB/S3 `curlCode: 28` timeout while reading a raw matrix fragment from
`s3://cellxgene-census-public-us-west-2/cell-census/2025-11-17/soma/`.

This is a remote object-store read blocker, not evidence against SLE biology.
Route-around implemented:

- `scripts/v3_analyze_sle_census_targeted.py` now exposes
  `SLE_MAX_CELLS_PER_DONOR_CELLTYPE` and `SLE_MAX_TOTAL_CELLS`.
- A smaller retry was started with 25 cells per donor/cell type and 8,000 total
  cells.
- If the reduced Census route still fails, continue with local downloadable GEO
  disease atlases rather than treating SLE as available evidence.

The full SLE source h5ad is reachable but 11.3 GB, so it remains a deliberate
resource tradeoff rather than the next default branch.

## 2026-05-27 00:25 UTC

The reduced SLE Census selected-gene retry was also stopped. With
`SLE_MAX_CELLS_PER_DONOR_CELLTYPE=25` and `SLE_MAX_TOTAL_CELLS=8000`, the
process ran for more than ten minutes, consumed several GB of memory, and
produced no output files under `results_v3/sle_census_targeted/`.

Decision: do not spend the current critical path on Census raw-matrix
materialization. The SLE metadata and source h5ad remain documented and
available for a later full-download or more robust SOMA extraction route, but
V3 continues through local GEO disease-atlas additions.
