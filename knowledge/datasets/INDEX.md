# Dataset Registry

Canonical manifest:
- `../../data/manifest.tsv`

## V3 Local Dataset Roots

- `../../data/raw_v3/`
- `../../data/derived_v3/`
- `../../phases/v3/results/`

## V4 Registry Rule

Every new dataset must be added to `../../data/manifest.tsv` with:

- accession or stable ID,
- URL/source,
- local path,
- size if known,
- SHA256 if feasible,
- last verified date,
- access status,
- notes.

## Priority Datasets To Register Next

- Pregnancy/postpartum autoimmune transcriptomic datasets.

## Pregnancy / Hormonal Natural Experiments

| Accession | Disease / system | Modality | Access status | V4 use |
|---|---|---|---|---|
| `GSE235508` | RA, SLE, healthy pregnancy | longitudinal blood bulk plus scRNA/cell-type-adjusted transcriptomics | SOFT metadata and mRNA count matrix downloaded; sample metadata parsed | highest-priority RA/SLE natural-experiment screen |
| `GSE17410` | MS pregnancy | PBMC expression array, before pregnancy vs ninth month | SOFT metadata downloaded and sample metadata parsed; raw CEL tar not downloaded | MS pregnancy Tier 0 screen |
| `GSE17449` | MS pregnancy-related superseries | expression array | public GEO, not yet downloaded | metadata/support; independence from `GSE17410` must be checked |
| `GSE153459` | healthy pregnancy reference | CD4 T-cell DNA methylation by trimester | public GEO, not yet downloaded | hormonal immune-regulation reference |
| `GSE122894` | pregnant vs non-pregnant EAE | mouse TCR-beta repertoire in Tcon/Treg | public GEO/SRA, not yet downloaded | cross-species mechanistic support |
- Longitudinal pre-disease cohorts or accessible summary artifacts.
- Failed-trial/post-hoc datasets.
- HMP2/MetaCardis/IBD multi-omics.
