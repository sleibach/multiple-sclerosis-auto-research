# Type 1 Diabetes Report: Rawls

Returned: 2026-05-26 19:08 UTC

## Verdict

T1D supports an IFN-driven islet antigen-presentation/metabolic-stress program,
but not a proven full `IFI30 + CTSD/CTSB + HLA-II/CD74 + STAT1/IRF1 +
HIF1A/NAMPT` myeloid transition.

Blood monocyte datasets are mixed to negative for the complete module. The
strongest support is in islets and cytokine-treated human islets, where
`STAT1/IRF1`, HLA-II/CD74, `IFI30`, `HIF1A`, and `NAMPT` move together. The
lysosomal cathepsin arm is weaker and context-dependent. No lipid-droplet
narrative is needed.

## Useful Datasets

- `GSE33440`: recent-onset pediatric T1D CD14+ monocytes; 6 controls, 16 T1D.
- `GSE154609`: CD14+ monocytes, 12 controls and 12 T1D; local platform mapping
  remains blocked.
- `GSE232310`: purified monocytes from T1D families; 62 samples.
- `GSE239501`: related monocyte scRNA-seq; raw tar about 422 MB.
- `GSE148073`: HPAP human islet scRNA/multi-omics; 3 controls, 3
  autoantibody-positive, 4 T1D.
- `GSE205853`: primary human islet cytokine perturbation plus pooled
  CRISPR/single-cell screen.
- `GSE273594/GSE273597/GSE273598`: 2025 pancreas single-cell multiome/spatial
  T1D atlas; high-priority follow-up for myeloid-specific pancreas testing.

## Evidence Summary

- `GSE33440` recent-onset monocytes: supports `HIF1A` and `IRF1`; partial
  lysosomal/AP signal (`CTSD`, `HLA-DPB1`) in a severe subgroup; no coherent
  full transition for `CD74`, `STAT1`, `IFI30`, `NAMPT`, `CTSB`, and
  `HLA-DRB1`.
- `GSE232310` T1D-family monocytes: dominant signal is cytolytic (`KLRD1`,
  `NKG7`, `PRF1`, `GNLY`), not lysosomal antigen processing.
- `GSE148073` T1D islets: strong islet-intrinsic antigen-presentation/IFN
  signal with large `CD74`, HLA-II, `IRF1`, `STAT1`, and `CTSB` increases in
  endocrine populations, especially beta cells. `NAMPT` rises in several
  endocrine/stromal compartments.
- `GSE205853` cytokine-treated human islets: perturbational support for
  inflammatory induction of `IFI30`, HLA-II, `CD74`, `STAT1`, `IRF1`, `HIF1A`,
  `NAMPT`, and `CXCL10`; `CTSD`/`CTSB` not convincingly induced.

## Integration Decision

Count T1D as strong support for IFN/MHC-II/metabolic-stress biology in diseased
target tissue and cytokine perturbation, but not as a core myeloid-transition
validation disease unless pancreas myeloid-specific datasets confirm it.
