# Primary Biliary Cholangitis Report: Goodall

Returned: 2026-05-26 19:13 UTC

## Verdict

PBC strongly fits the portal IFN/APC plus lysosomal antigen-processing part of
the V3 model, but does not cleanly support the full lipid-loader/repair plus
NAMPT/HIF version.

## Axis Read

- IFN/APC: strong. `CXCL9/CXCL10/CXCR3`, JAK-STAT/Th1-like inflammation,
  HLA-II genetics, and `CD74/MIF` portal interactions align.
- Lysosomal antigen processing: partial-strong. Best PBC evidence is
  `CTSS + HLA-II/CD74`; `IFI30` is plausible cross-autoimmune but PBC-specific
  evidence is sparse.
- Lipid-loader/repair: weak. Cholestasis/lipid biology matters clinically, but
  the V3 `SPP1/GPNMB/TREM2/APOE` repair macrophage module is not clearly
  supported.
- HIF/NAMPT: weak-partial. HIF has cholestatic/fibrotic portal macrophage
  support; `NAMPT` lacks strong PBC specificity and remains prior-arted.

## Useful Datasets

- `HRA008003` / `PRJCA027647`: open human scRNA-seq from normal and PBC
  liver/PBMCs, about 290k cells in the 2024 Nature Communications PBC
  Th1-like/JAK-STAT study.
- `CRA017680`: mouse liver scRNA companion dataset.
- `OMIX001122` / `HRA002347` / `PRJCA009122`: PBC liver/blood scRNA from the
  DUOX2+ACE2+ small cholangiocyte study; controlled access.
- `OMIX001127`: spatial transcriptomics from same cholangiocyte study.
- `GSE79850`: FFPE liver bulk, 7 low-risk PBC, 9 high-risk PBC, 8 controls.
- `GSE159676`, `GSE304352`, `GSE119600`: weak/exploratory liver or blood
  comparators.
- `GCST002774`: PBC GWAS meta-analysis.

## Candidate Nodes

- HLA-II/CD74: strongest disease fit; central APC-state marker/neighborhood.
- CTSS: strongest lysosomal protease candidate for PBC; prior work reports
  increased CTSS in PBC liver macrophages and reduced cytokine/antigen
  presentation activity with CTSS inhibition.
- CXCL10/CXCR3: strong IFN/APC biomarker axis, but direct CXCL10 neutralization
  in PBC reduced CXCL10 without improving ALP/biochemistry.
- JAK-STAT / IL-12 / TYK2: stronger PBC-specific intervention neighborhood than
  NAMPT; mouse injury alleviation reported in the 2024 scRNA study.
- IFI30: readout/co-marker; direct PBC evidence weak.

## Integration Decision

Keep PBC as partial support for the portal IFN/APC plus CTSS/CD74/HLA-II arm.
Do not use it to strengthen the full lipid-loader/repair module or NAMPT as a
central node.
