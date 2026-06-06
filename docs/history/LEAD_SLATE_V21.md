# LEAD_SLATE_V21

V21 updates the V20 next-tier slate with a genome-wide LDSC backdrop and
bounded SuSiE-coloc/QTL context for the two queued genetics regions. No new
locus clears the chr1 bar.

## Backdrop Summary

Genome-wide LDSC genetic correlation now provides the context missing from
earlier locus work:

- MS-UC: `rg = 0.3342`, `SE = 0.0444`, `p = 4.8771e-14`.
- MS-SLE: `rg = 0.2439`, `SE = 0.0608`, `p = 6.0712e-05`, caveated by high
  SLE h2 intercept `1.1998`.
- MS-RA: `rg = 0.1692`, `SE = 0.0453`, `p = 0.0002`.
- MS-Crohn: `rg = 0.1675`, `SE = 0.0527`, `p = 0.0015`.

The central V20/V21 interpretation is unchanged but better grounded: UC is the
stronger gut comparator for MS inherited risk, while Crohn still contributes
downstream mucosal and decoupling biology. RA is genetically modestly near MS
but remains divergent on blood APC treatment-response architecture.

## Lead Card: MS-Crohn chr14 `14:68710199-69753364`

Candidate region: `ZFP36L1` neighborhood.

Bounded SuSiE-coloc:

- SNPs used: `483`.
- Pairwise credible-set comparisons: `1`.
- max `PP.H4 = 0.687732800443124`.
- max `PP.H3 = 0.28112512912872`.
- Verdict: suggestive, not robust. It does not meet the high-H4 standard used
  to advance chr1 and chr10.

Immune-QTL context:

- OneK1K top-eQTL target hits for `ZFP36L1` in this region: `0`.
- DICE significant eQTL target hits: `30` for `ZFP36L1`, mostly M2 macrophage
  context.
- DICE mean expression supports broad immune expression, including activated T
  cells, monocytes, and B cells.
- No all-variant immune-QTL colocalization was run because the disease
  SuSiE-coloc did not reach robust grade and the available DICE data are
  significant-hit summaries, not full locus QTL summary statistics.

Direction and druggability:

- No allele-aligned therapeutic direction is established.
- `ZFP36L1` is an RNA-binding/post-transcriptional regulator. First-principles
  targetability is biologically plausible through RNA/protein-regulatory
  modalities but not a clean direction-matched small-molecule target from the
  current evidence.

Backdrop interpretation:

- MS-Crohn global rg is modest (`0.1675`). A robust shared chr14 locus would
  be a useful standout within a weaker global architecture, but V21 only
  supports a suggestive signal.

V21 verdict: **parked/suggestive**, not a promising next lead.

## Lead Card: MS-UC chr2 `2:60689469-61742410`

Candidate region: `REL` / `PUS10` / `USP34`.

Bounded SuSiE-coloc:

- SNPs used: `499`.
- Status: `no_cs`.
- Error: `coloc.susie returned no summary`.
- Verdict: does not survive the bounded multi-signal disease-coloc screen.

Immune-QTL context:

- OneK1K top-eQTL target hits for `REL`, `PUS10`, or `USP34` in this region:
  `0`.
- DICE significant eQTL target hits: `45` `REL`, `7` `USP34`, `5` `PUS10`.
- DICE expression strongly supports `REL` in activated CD4/CD8 T cells and B
  cells, but expression/QTL context cannot rescue a disease-coloc failure.

Direction and druggability:

- No shared disease causal signal is established, so no allele-aligned
  therapeutic direction is inferred.
- `REL`/NF-kB biology is druggable in a broad pathway sense but crowded and
  safety-limited. `PUS10` and `USP34` do not become target claims without a
  surviving shared disease signal and all-variant QTL colocalization.

Backdrop interpretation:

- MS-UC has the strongest global rg in V21 (`0.3342`). In that context, a
  moderate chr2 overlap can be part of broad shared architecture without being
  actionable. V21 finds no robust chr2 locus-level lead.

V21 verdict: **closed/not-now**.

## Does Either New Locus Clear the chr1 Bar?

No.

The chr1 bar requires a robust shared disease signal, credible causal-gene
evidence, allele-aligned effect direction, and a direction-matched tractable
modality. chr14 does not reach robust disease-coloc and lacks direction; chr2
does not produce a SuSiE-coloc summary. Neither should be surfaced to the
medical team as a therapeutic lead.

## Updated Slate Position

1. Dynamic APC/HLA-II treatment-response monitoring remains the top actionable
   lead, pending locked clinical-utility framing and held-out DMT testing.
2. chr1 `KIF21B`/`GPR25` remains real shared MS-UC genetics but not
   intervention-grade.
3. `ZMIZ1` remains a robust opposite-direction MS/Crohn decoupling finding,
   not a transfer target.
4. chr14 `ZFP36L1` is parked as suggestive genetics requiring stronger
   disease-coloc and full-QTL data.
5. chr2 `REL/PUS10/USP34` is closed as a V20 genetics follow-up unless new
   fine-mapped signal-specific data arrives.

## Reproducibility Artifacts

- Bounded SuSiE script: `scripts/v21_next_tier_locus_susie.py`.
- Locus outputs: `analysis/v21_next_tier_loci/`.
- Rollup: `analysis/v21_next_tier_loci/susie_coloc_rollup.tsv`.
- DICE target-hit context:
  `analysis/v21_next_tier_loci/dice_target_eqtl_hits.tsv`.
