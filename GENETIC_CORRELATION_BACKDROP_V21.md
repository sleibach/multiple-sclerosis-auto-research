# GENETIC_CORRELATION_BACKDROP_V21

## Scope

V21 used the now-verified LDSC European LD-score reference panel to provide the
first genome-wide genetic-correlation backdrop for the MS-centered map. This
context was missing from prior locus-level colocalization work.

Inputs and tools:

- MS: OpenGWAS `ieu-b-18`, `n = 115803`.
- UC: OpenGWAS `ieu-a-32`, `n = 27432`.
- Crohn: OpenGWAS `ieu-a-30`, `n = 20883`.
- RA: OpenGWAS `ieu-a-832`, `n = 58284`.
- SLE: OpenGWAS `ebi-a-GCST003156`, `n = 14267`.
- Summary statistics were downloaded as local VCFs through OpenGWAS API v4
  POST `gwasinfo/files`, then converted to HapMap3 SNP TSVs.
- LDSC reference: `data/raw/ldsc_reference/eur_w_ld_chr/`, verified in
  `meta/LDSC_PANEL_STATUS.md`.
- Reproducible script: `scripts/v21_ldsc_core_backdrop.py`.

Important implementation note: initial munge attempts on gzip-compressed raw
TSVs failed with the LDSC Python 3 gzip text/binary issue. The successful
path used plain TSV input to `munge_sumstats.py`; the V21 script has been
patched to reproduce that path.

## Results

| Pair | Mode | rg | SE | z | p | Comparator h2 intercept | Genetic covariance intercept | Valid SNPs | Caveat |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| MS-UC | full | 0.3342 | 0.0444 | 7.5352 | 4.8771e-14 | 1.0467 | 0.0844 | 1,108,932 | strongest tested comparator |
| MS-UC | MHC-excluded raw | 0.3342 | 0.0444 | 7.5352 | 4.8771e-14 | 1.0467 | 0.0844 | 1,108,932 | identical after LDSC merge |
| MS-SLE | full | 0.2439 | 0.0608 | 4.0100 | 6.0712e-05 | 1.1998 | 0.0100 | 985,993 | high SLE h2 intercept; interpret cautiously |
| MS-RA | full | 0.1692 | 0.0453 | 3.7325 | 0.0002 | 1.0553 | 0.0423 | 932,380 | modest positive rg |
| MS-Crohn | full | 0.1675 | 0.0527 | 3.1775 | 0.0015 | 1.0212 | 0.0789 | 1,108,900 | modest positive rg |
| MS-Crohn | MHC-excluded raw | 0.1675 | 0.0527 | 3.1775 | 0.0015 | 1.0212 | 0.0789 | 1,108,900 | identical after LDSC merge |

The MS h2 intercepts in the paired runs were near 1.017 to 1.019. SLE is the
least stable of these estimates because the SLE h2 intercept was high
(`1.1998`), consistent with residual confounding, stratification, or
summary-statistic idiosyncrasy. The SLE positive rg is therefore treated as
supported but caveated, not robust.

## MHC Sensitivity

The requested MHC-excluded sensitivity was attempted for UC and Crohn by
removing raw HapMap3 SNPs in chr6:25-34 Mb before munge:

- MS raw HM3 rows removed: `2,733`.
- UC raw HM3 rows removed: `3,053`.
- Crohn raw HM3 rows removed: `3,065`.

After LDSC reference-panel merge, the estimates and valid-SNP counts were
identical. Direct inspection showed the active LDSC reference panel contains
zero SNPs in chr6:25-34 Mb, so the regression SNP set used here is already
effectively MHC-free for that interval. This is useful but should not be
overstated as an independent sensitivity using an MHC-containing reference.

## Interpretation

UC is the strongest tested genome-wide genetic comparator for MS
(`rg = 0.3342`, `p = 4.8771e-14`). Crohn is positive but materially weaker
(`rg = 0.1675`). This hardens the V8-V12 map claim that UC is the closer gut
comparator on inherited genetic architecture, while both UC and Crohn can still
share downstream mucosal/treatment-response analogies with MS.

RA is not genetically far from MS (`rg = 0.1692`), despite the repeated RA
divergence on blood APC treatment-response architecture. That supports the V10
axis-disagreement framing: RA divergence is axis- and compartment-specific,
not global.

SLE remains an MS-adjacent infectious-trigger/complement hypothesis space, but
the V21 genetic-correlation estimate is caveated by the high SLE intercept.
SLE should not be promoted on rg alone.

## Reproducibility Artifacts

- Raw converted sumstats: `analysis/v21_ldsc_backdrop/sumstats_raw/`.
- Munge logs: `analysis/v21_ldsc_backdrop/logs/munge_*_plain.log`.
- LDSC rg logs: `analysis/v21_ldsc_backdrop/rg/*_plain.log`.
- Parsed table: `analysis/v21_ldsc_backdrop/ldsc_rg_results.tsv`.
- Reproducible script: `scripts/v21_ldsc_core_backdrop.py`.

## Remaining Work

Extend the same LDSC pipeline to psoriasis, T1D, Sjogren's, celiac disease,
thyroid disease, and myasthenia gravis once the best OpenGWAS IDs are selected
and verified. Do not interpret any added rg without h2 intercept, genetic
covariance intercept, ancestry/source review, and the MHC-reference caveat.
