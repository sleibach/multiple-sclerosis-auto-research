# Autoimmune Thyroid Disease Report: Dirac

Returned: 2026-05-26 19:03 UTC

## Verdict

Autoimmune thyroid disease is a partial recurrence of the V3 IFN/APC axis, but
not a clean myeloid-dominant recurrence. Hashimoto thyroiditis has inflammatory
macrophage/DC and APC biology, and Graves/Graves orbitopathy has IFN, HLA-II,
CXCL10, hypoxia/glycolysis signals. The dominant disease architecture remains
thyroid epithelial autoantigen biology plus lymphoid/B-cell autoimmunity:
`TSHR`, `TG`, `TPO`, HLA, `CTLA4`, `PTPN22`, `CD40`, `IL2RA`, `IFIH1`.

## Useful Datasets

- `HRA001684` / CNGB `CNP0001494`: Hashimoto thyroid plus PBMC scRNA-seq; strong
  cell-state source but access needs validation.
- `GSE248205` / `PRJNA1042806`: AITD spatial transcriptomics; HT/GD/control
  Visium, processed data about 159 MB.
- `GSE285196` / `PRJNA1201778`: Graves PBMC and intrathyroidal mononuclear
  scRNA/BCR with thyroid autoantigen peptide stimulation.
- `GSE183576`: small Graves PBMC miRNA dataset.
- `GSE272832` / `PRJNA1137109`: Graves orbitopathy PBMC transcriptome/methylome.
- `GSE9340`: legacy bulk Graves thyroid/orbit comparator.

## Candidate Nodes

AITD supports `CXCL10`, `CXCL9`, `STAT1`, `IRF1`, HLA-II genes, `CD74`, `CD40`,
`ICAM1`, and `MIF`. Possible myeloid/APC recurrence genes include `IL1B`,
`TNF`, `NFKBIA`, `CCL2`, `CD14`, `CD68`, `CD163`, `C1QA/B/C`, `APOE`, `SPP1`,
`IFI30`, `CTSS`, `CTSB`, `CTSD`, `LAMP1`, and `TPP1`, but these are not
genetically anchored in AITD from this pass.

## Integration Decision

Count AITD as supportive for IFN/APC recurrence, not as evidence that the
IFN/HIF-licensed lysosomal antigen-processing myeloid state dominates.
