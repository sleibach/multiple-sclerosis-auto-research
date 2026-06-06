# Wave 3 Genetics / Colocalization Report - Kierkegaard

Returned: 2026-05-26 21:16 UTC

Read-only. No files edited by subagent.

## Bottom Line

V3 has genetics-compatible pathway anchoring, but not clean single-gene
cross-autoimmune anchoring.

Go for: IFN-gamma-licensed antigen-processing/APC transition:

`IFNGR/JAK/STAT -> IRF1/CIITA/RFX5 -> HLA-II/CD74 + IFI30/CTSS`

No-go for: claiming that `IFI30`, `CD74`, `CTSS`, `STAT1`, `JAK1/2`, or
`IFNGR1/2` individually have true colocalized/MR-supported anchoring across four
or more scoped diseases.

## Strongest Anchors

| Tier | Evidence | Interpretation |
|---|---|---|
| Strong, broad, but not target-specific | HLA-II/MHC across MS, celiac, RA, SLE, Sjogren, PBC, IBD; psoriasis mostly MHC/HLA-C | Supports antigen-presentation biology, not a clean `CD74` or specific HLA-II gene target. MHC LD/haplotype complexity blocks simple MR/coloc. |
| Strong non-MHC regulatory | `IRF1`/`CARINH` 5q31 in IBD, psoriasis; OpenTargets local table also flags SLE and weak celiac | Best non-MHC cross-disease regulatory anchor, but the IBD causal locus is a `CARINH/IRF1` regulatory loop, not proven isolated `IRF1`. |
| Strong disease-specific effector | `IFI30` in MS | Best candidate-specific MS anchor: local genetics report records MS GWAS `GCST009597`, `GCST005531`, FinnGen `G6_MS`, and OpenTargets monocyte influenza-stimulated eQTL / transcript-usage QTL colocalizations with H4 about `0.996` and `0.982`. |
| Secondary, mechanistically useful | `IFNGR2` MS `rs9808753`; `JAK2` IBD `rs10758669` | Real locus/function evidence, but not enough for cross-disease target-level coloc. |

## Exact Loci

GRCh38 from Ensembl lookup:

| Gene/locus | Coordinates / variants |
|---|---|
| `IFNGR1` | chr6:137,197,483-137,219,449. No strong scoped autoimmune coloc found. |
| `IFNGR2` | chr21:33,403,369-33,479,348; MS coding risk SNP `rs9808753` at chr21:33,415,005. Functional B-cell IFN-gamma/STAT1 evidence exists, but true cross-disease coloc not established. |
| `JAK1` | chr1:64,833,223-65,067,754. Weak/non-specific autoimmune neighborhood evidence only. |
| `JAK2` | chr9:4,984,390-5,129,948; IBD SNP `rs10758669` at chr9:4,981,602. Supports IBD locus/QTL-function, not broad V3 genetic anchor. |
| `STAT1` | chr2:190,908,460-191,020,960. Many autoimmune signals are better read as adjacent `STAT4` locus, especially `rs7574865` at chr2:191,099,907. Do not claim STAT1-specific anchoring. |
| `IRF1` | chr5:132,440,440-132,508,719; IBD `rs2188962` at chr5:132,435,113 near `CARINH/IRF1`. Good regulatory-locus anchor. |
| `CIITA` | chr16:10,866,222-10,943,021; candidate promoter SNP `rs3087456` at chr16:10,877,045. Literature is mixed; no robust cross-disease coloc. |
| `RFX5` | chr1:151,340,640-151,347,339. No credible scoped autoimmune common-variant anchor found. |
| `IFI30` | chr19:18,173,162-18,178,121; MS SNP `rs11554159` at chr19:18,175,134. Strongest non-MHC MS-specific coloc anchor. |
| `CTSS` | chr1:150,730,079-150,765,957. Some pQTL/MR-style cathepsin literature exists, but not audited enough for V3 causal claim. |
| `CD74` | chr5:150,401,637-150,412,969. Expression/protein-state marker; no useful cis target genetics in scoped diseases. |
| HLA-II | chr6p21.32, roughly HLA-DRA/DRB/DQ/DP from chr6:32.44-33.09 Mb; OpenTargets excludes lead variants in MHC chr6:25,726,063-33,400,556 from standard credible-set handling. Treat as broad antigen-presentation anchor only. |

## Disease Readout

- MS: HLA-II, `IFI30`, and `IFNGR2` are the useful anchors. `IFI30` is the only
  local true coloc-grade candidate.
- Crohn/UC: `IRF1/CARINH` and `JAK2` loci support the IFN/APC axis; `IRF1` is
  stronger than `JAK2` for V3 cross-disease genetics.
- Psoriasis: MHC plus `IRF1` 5q31/TWAS/QTL support; not `IFI30`.
- Sjogren/PBC/celiac/RA/SLE: HLA and STAT4-like immune loci dominate. They
  support antigen-presentation/IFN biology, but not the named downstream genes
  as clean targets.

## Recommendation

Use genetics as supporting pathway evidence, not as the primary V3 target proof.
The defensible formulation is:

"Autoimmune risk genetics recurrently supports antigen presentation and
IFN-regulated immune control, with HLA-II as broad but non-specific anchoring,
`IRF1/CARINH` as the best non-MHC cross-disease regulatory locus, and `IFI30` as
an MS-specific colocalized effector candidate."

Do not claim supported MR/coloc for `CD74`, `CTSS`, `STAT1`, `CIITA`, `RFX5`,
`IFNGR1`, `JAK1`, or pan-disease `IFI30`.

Sources used: local `subagents_v3/genetics_james_report.md`, `MILESTONE_1.md`,
`results_v3/opentargets_candidate_disease_hits.tsv`, Open Targets credible-set
docs, eQTL Catalogue, OpenGWAS, FinnGen `G6_MS`, CARINH/IRF1 IBD paper, IFNGR2
MS paper, and JAK2 IBD functional genetics paper.
