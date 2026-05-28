# Cross-Autoimmune Genetics Report: James

Returned: 2026-05-26 19:15 UTC

## Verdict

The strongest genetic anchor is not `NAMPT`; it is the antigen-presentation /
interferon-regulated antigen-processing axis.

Priority order from genetics:

1. HLA-II is the broadest cross-autoimmune GWAS anchor, but LD complexity makes
   it unsuitable as a clean target.
2. `IFI30` is the best candidate-specific lysosomal antigen-processing anchor
   for MS, with cis monocyte qTL colocalization to MS.
3. `IRF1` is the strongest non-MHC cross-disease regulatory anchor, especially
   IBD/psoriasis, with stimulated monocyte/macrophage qTL colocalization.
4. `MERTK` and `CTSB` have narrower but real genetics: MS for `MERTK`, T1D/SLE
   for `CTSB`.
5. `NAMPT`, `SPP1`, `TREM2`, `CTSD`, `LIPA`, `C1QBP`, and `SARM1` are weak as
   common-variant cross-autoimmune anchors.

## Key Validated Evidence From Subagent

- `IFI30`: GWAS Catalog MS hits in `GCST009597` and `GCST005531`; FinnGen R12
  `G6_MS`; OpenTargets reports monocyte influenza-stimulated eQTL and
  transcript-usage QTL colocalizations with MS (`H4` about 0.996 and 0.982).
- HLA-II: broad cross-autoimmune MHC signal across celiac, RA, T1D, AS, MS,
  psoriasis, Sjogren, thyroid disease, and PBC, but LD/haplotype complexity
  blocks target-specific interpretation.
- `IRF1`: GWAS and stimulated monocyte/macrophage qTL colocalization for IBD and
  psoriasis; strongest non-MHC regulatory anchor.
- `MERTK`: MS-specific GWAS plus qTL/MR support.
- `CTSB`: T1D/SLE locus plus T1D qTL colocalization.
- `CD74` and `SPP1`: mostly trans pQTL colocalization and should be treated as
  biomarker/protein consequences, not cis target genetics.

## Integration Decision

Promote `IFI30 + IRF1/HLA-II antigen-processing` as the best genetics-compatible
central axis. Keep `NAMPT/HIF1A/NAD` as an expression/perturbation hypothesis,
not a genetics-led anchor. Do not infer therapeutic direction from qTL
colocalization without directional validation.
