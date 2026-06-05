# V14 Bounded SuSiE-Coloc Follow-up

Timestamp: 2026-06-05 23:59 CEST

Prerequisite: `meta/PROVISIONING_REPORT.md` was written before this analysis. `coloc` and `susieR` passed real smoke tests before use.

## Scope

This run performed multi-signal SuSiE-coloc on the two V14 loci requested for immediate follow-up after provisioning:

- MS-UC chr1: `1:200375242-201375897`
- MS-Crohn chr10: `10:80542475-81559335`

It did not run LDSC/HDL genetic correlation, genome-wide correlation, eQTL/pQTL direction mapping, or intervention inference.

## Method

- Association input: cached OpenGWAS regional association JSON from `analysis/v13_genetics_coloc/raw/`.
- LD input: OpenGWAS `POST /ld/matrix`, population `EUR`.
- SNP selection: top `500` shared rsids per locus ranked by minimum p-value across the two traits.
- Allele handling: z-scores were aligned to the LD matrix allele order; variants whose alleles could not be aligned in both traits were excluded.
- Fine-mapping: `coloc::coloc.susie()` using `susieR::susie_rss()` through `coloc::runsusie()`, `L=10`, `coverage=0.95`, `min_abs_corr=0.1`, `max_iter=1000`, seed `20260605`.
- Code: `scripts/v14_susie_coloc_confirmed_loci.py`

## Results

| Locus | Shared SNPs available | LD SNPs returned | Allele-aligned SNPs used | SuSiE convergence | Pairwise CS rows | max PP.H3 | max PP.H4 |
|---|---:|---:|---:|---|---:|---:|---:|
| MS-UC chr1 `1:200375242-201375897` | 2397 | 500 | 485 | yes | 1 | 0.0406612726112663 | 0.959324545654259 |
| MS-Crohn chr10 `10:80542475-81559335` | 2322 | 500 | 492 | yes | 1 | 0.0418877620126776 | 0.958107919239886 |

Per-locus summary files:

- `analysis/v14_susie_coloc/MS_UC_chr1_200375242_201375897/coloc_susie_summary.tsv`
- `analysis/v14_susie_coloc/MS_Crohn_chr10_80542475_81559335/coloc_susie_summary.tsv`

## Interpretation

Both bounded SuSiE-coloc runs support shared causal signal structure in the analyzed SNP subsets:

- MS-UC chr1: `PP.H4.abf = 0.9593`, `PP.H3.abf = 0.0407`.
- MS-Crohn chr10: `PP.H4.abf = 0.9581`, `PP.H3.abf = 0.0419`.

This strengthens the V13 first-pass single-causal-variant result for these two loci. It does not by itself upgrade the genetics axis to full robust grade because:

1. The run used bounded top-500 SNP subsets, not every regional SNP.
2. The LD matrix came from OpenGWAS EUR reference LD rather than a study-matched LD panel.
3. Genome-wide LDSC/HDL with MHC exclusion and sample-overlap assessment remains unrun.
4. Causal-gene mapping and effect direction remain unresolved.

## Next Actions

1. Repeat or extend SuSiE-coloc for the remaining V14 high-H4 loci: UC chr5/PTGER4 and Crohn chr17/STAT3-STAT5.
2. Run explicit MHC PP.H3 negative-control SuSiE-coloc once LD matrix sizing is confirmed.
3. Provision reference LD-score panels before LDSC/HDL genetic correlation.
4. Do not make PTGER4 therapeutic-direction claims until effect-allele-aligned eQTL/pQTL direction is resolved.
