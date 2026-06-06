# CONVERGENCE_CHECK_V9_02

Timestamp: 2026-06-02 12:04 CEST

## What Changed Since Check 01

MS processed microbiome data were successfully exported and analyzed after
installing R `phyloseq`.

IBDMDB/HMP2 all-sample sensitivity completed:

- `1,360` MGX taxonomic profiles downloaded.
- `106` participants represented.
- Naive repeated-sample tests showed multiple FDR-significant effects.
- Participant-clustered inference removed FDR support.

Genetics source-manifest scaffold completed:

- `analysis/v9_genetics/source_manifest.tsv`
- `analysis/v9_genetics/SOURCE_MANIFEST_REPORT.md`
- `OPENGWAS_JWT` absent, so no harmonized LDSC claim is made.

## Microbiome Axis Decision

MS has a primary-data case-control microbiome signal:

- Bacteroides higher in MS, age/sex-adjusted FDR `0.00639`.
- Enterobacteriaceae/LPS proxy lower in MS, adjusted FDR `0.00510`.
- Faecalibacterium lower in MS, adjusted FDR `0.0341`.

IBD does not have V9-supported taxonomic-family evidence after
participant-aware inference:

- 106-profile independent-participant subset: no FDR `<0.10`.
- 1,360-profile all-sample sensitivity: naive significance disappears under
  participant-clustered inference.

Conclusion:

- Upgrade MS microbiome evidence from literature-only to primary-data-supported
  within one dataset.
- Do not upgrade MS/IBD microbiome-mediated proximity.
- Keep V8's MS/IBD proximity anchored in mucosal IFN/APC treatment-response and
  tissue-repair axes, not shared broad taxonomic dysbiosis.

## Mechanism / Intervention Consequence

The gut-barrier/metabolite/APC-plasticity hypothesis remains conditional and
should be narrowed:

- Supported: MS has stool taxonomic shifts, including lower Faecalibacterium
  after adjustment.
- Unsupported: MS and IBD share a broad taxonomic-family dysbiosis pattern.
- Next stronger test: microbial pathways/metabolites linked to APC plasticity,
  not genus/family-level overlap.

## Genetics Axis Decision

The genetics axis cannot be robustly upgraded from current local data.

- UC/Crohn retain the V8 LDSC-backed source.
- Other diseases remain checkpoint/provisional until harmonized LDSC/HDL or
  coloc/fine-mapping runs are performed.
- OpenGWAS automated download is access-blocked in this environment by missing
  `OPENGWAS_JWT`.

## Next Forcing Questions

1. Can V9 find independent MS microbiome replication or pathway/metabolite
   data that tests the Faecalibacterium/Bacteroides/Enterobacteriaceae pattern?
2. Can gut-microbiome feature shifts be linked to IFN/APC or APC plasticity in
   a paired immune dataset?
3. Is the MS/IBD map implication now sharper as "shared mucosal repair/APC
   response architecture, not shared broad dysbiosis"?
4. If genetics access becomes available, do MHC-excluded rg estimates preserve
   UC > Crohn proximity and clarify RA/SLE/T1D positions?
