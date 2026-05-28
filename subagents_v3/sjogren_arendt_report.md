# Sjogren Disease Report: Arendt

Returned: 2026-05-26 19:03 UTC

## Verdict

Sjogren supports the `IFN -> STAT1/IRF1 -> CXCL10/HLA-II/CD74`
antigen-presentation arm. It does not yet cleanly support the full
IFN/HIF-licensed lysosomal myeloid state because local evidence is bulk salivary
gland and `NAMPT`/broad lysosomal genes are mixed or negative.

## Local Evidence

Local V2 Sjogren was `GSE23117`, bulk minor salivary gland, 10 SS vs 4 non-SS
controls, with only 2 advanced SS cases. Targeted read-only reanalysis by the
subagent reported:

- IFN/APC: `CXCL10` g=1.13 p=0.009, `STAT1` g=1.35 p=0.003, `IRF1` g=1.60
  p=0.001; IFN/APC module g=1.19 p=0.0069.
- HLA-II/CD74: `CD74` g=0.89 p=0.029, `HLA-DQA1` g=0.86 p=0.033; advanced
  samples show very large HLA-II effects but n=2.
- Lysosomal/AP: `IFI30` positive direction but non-significant; `LAMP3` positive
  g=1.33 p=0.0036; `CTSB` null; `CTSD` negative g=-1.64 p=0.004.
- Myeloid density: `ITGAM` g=1.07 p=0.015; myeloid-density module g=0.72
  p=0.066.
- HIF/NAMPT: `HIF1A` positive g=1.17 p=0.028, but `NAMPT` null and HIF/NAMPT
  module non-significant.

## Useful Datasets

- `GSE157278`: PBMC scRNA-seq, 57,288 PBMCs, 5 pSS/5 controls.
- `HRA003613` plus Zenodo `10884425`: salivary gland scRNA and SG/PBMC immune
  h5ad; processed immune h5ad about 644 MB, salivary gland h5ad about 3.1 GB.
- `GSE272409`: minor salivary gland scRNA-seq, TLS-focused Sjogren/Sicca cohort.
- `GSE272410`: matching bulk RNA-seq.
- `OMIX011039`: salivary gland spatial transcriptomics, 3 SjD/3 controls.
- `JGAS000773` / `hum0492-v1`: controlled multi-modal SjD data.

## Integration Decision

Count Sjogren as supportive for IFN/APC recurrence and blocked for
myeloid-specific and HIF/NAMPT-specific recurrence until cell-type/spatial
matrices are analyzed.
