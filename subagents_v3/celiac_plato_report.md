# Celiac Disease Report: Plato

Returned: 2026-05-26 19:11 UTC

## Verdict

Celiac disease gives partial support for the full V3 module. IFN/APC and antigen
processing are strong; lipid-loader/repair is weak; HIF/NAMPT/metabolic evidence
is partial and indirect.

## Useful Datasets

- `GSE277276`: duodenal scRNA-seq, 203,555 cells, 21 active CeD and 11 controls.
- `GSE252545`: 10x Visium spatial duodenal biopsies.
- FitzPatrick et al. 2025 scRNA/spatial resource: 86,442 cells, 35 participants,
  spatial transcriptomics in 20 participants.
- `GSE315138`: 2026 duodenal scRNA-seq, active CeD vs controls.
- `EGAS00001003751`: controlled-access CD45+ immune scRNA-seq.
- `GSE146190`, `GSE164883`, `GSE72625`: bulk/array duodenal datasets.
- `GCST000612` / OpenGWAS `ebi-a-GCST000612` and `GCST005523`: GWAS resources.

## Candidate Nodes

- `TGM2 -> LRP1 -> CD103+ DC -> HLA-DQ2/8`: celiac-specific strongest
  antigen-processing/intervention circuit.
- `IFNG/IFNGR1 -> STAT1/IRF1 -> HLA-II/CD74/CXCL10`: best match to V3 IFN/APC.
- `CXCL10/CXCR3`: strong but heavily prior-arted recruitment axis.
- `IL1B`: myeloid-derived epithelial/fibroblast reprogramming signal in active
  celiac.
- `IFI30`, `CTSS`, `CTSB`: good V3-compatible antigen-processing analytes, but
  require direct cell-type quantification before promotion.
- `NAMPT/HIF1A`: metabolic comparator, not celiac lead.

## Integration Decision

Use celiac as a positive-control disease for IFN/APC plus lysosomal antigen
processing, and as a warning that disease-specific antigen-entry circuits may be
stronger intervention points than generic lipid/repair macrophage markers.
