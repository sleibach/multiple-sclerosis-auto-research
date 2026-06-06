# CONVERGENCE_CHECK_46

Timestamp: 2026-05-27 18:49 CEST

## Forcing Question

After Wave85 demoted the residual lysosomal/APC endpoint, does the external
anti-TNF nonresponse signal decompose to a specific gene-level anchor, and does
that anchor generalize beyond IBD?

## Wave86 Result: IBD Gene-Level Decomposition

Script:

- `scripts/v3_wave86_external_geo_antitnf_gene_driver.py`

Inputs:

- Wave85 external GEO matrices and GPL570 annotation.

Primary independent contexts:

- `GSE12251_UC_ACT1_baseline`
- `GSE14580_UC_Leuven_baseline`
- `GSE16879_Crohn_colitis_Leuven_baseline`
- `GSE16879_Crohn_ileitis_Leuven_baseline`

Top nonresponse-high genes:

- `IL1B`
- `CXCL8`
- `TREM1`
- `CCL4`
- `CCL3`
- `CD44`
- `CCL2`
- `ACSL1`
- `IFI30`
- `OSM`

Key numbers:

- `45` module genes tested.
- `16` genes called `GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR`.
- Top gene `IL1B`:
  - nonresponse-high in `4/4` primary contexts.
  - nominal p<0.05 in `3/4` contexts.
  - FDR<0.10 in `3/4` contexts.
  - weighted mean Hedges g (responder minus nonresponder): `-1.695`.
  - median AUC for high score predicting nonresponse: `0.897`.
- `CXCL8` and `TREM1` are nearly tied with `IL1B`.

Interpretation:

- This is not a single-gene discovery yet. The top genes are a coherent
  inflammatory myeloid/neutrophil-chemokine resistance state.
- `IL1B`, `CXCL8`, `TREM1`, chemokines, and `OSM` are all likely
  prior-art-heavy in IBD anti-TNF resistance.

## Wave87 Result: RA Synovium Cross-System Check

Script:

- `scripts/v3_wave87_cross_system_antitnf_resistance_gene_check.py`

Inputs:

- `phases/v3/results/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`
- `phases/v3/results/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
- `phases/v3/results/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `phases/v3/results/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv`

Key result:

- `25` Wave86 anchor/park genes considered.
- `22` genes had usable RA synovium expression.
- Only `2` genes met the local cross-system directional criterion:
  - `LAMP3`: RA baseline responder-minus-nonresponder Hedges g `-0.927`,
    p `0.00238`, FDR `0.0261`, AUC high-score nonresponse `0.786`.
  - `IL1B`: RA baseline responder-minus-nonresponder Hedges g `-0.588`,
    p `0.0407`, FDR `0.0995`, AUC high-score nonresponse `0.701`.

Contradiction:

- `TREM1`, `CCL2`, `STAT1`, `CD44`, `NFKBIA`, and several other strong IBD
  nonresponse genes are higher in RA responders, not nonresponders.

## Integration

The current evidence does not support a broad pan-autoimmune anti-TNF
resistance mechanism built from the whole Wave86 inflammatory module. It does
support a narrower observation:

- `IL1B` is consistently anti-TNF nonresponse-high in external IBD mucosa and
  also directionally replicates in baseline RA synovium.
- `LAMP3` also cross-replicates, but it is a dendritic/lysosomal state marker
  rather than an obvious intervention point.

## Self-Critique

- RA synovium and IBD mucosa are different tissues with different responder
  definitions. A cross-system failure may reflect biology, not invalidation.
- IL1B is very likely too broad and prior-art saturated for novelty.
- LAMP3 is not currently a clean drug target. Promoting it would repeat the
  "marker mistaken for intervention" failure mode.
- The current branch may still yield a stratification biomarker, but the V3
  DoD asks for therapeutic relevance across autoimmune disease; this evidence
  is not enough.

## Decision

- Do not promote the full inflammatory/IFN module as a cross-autoimmune
  mechanism.
- Put `IL1B` and `LAMP3` through prior-art and intervention-feasibility
  pressure.
- If `IL1B` is prior-art blocked and `LAMP3` remains non-druggable, pivot again
  rather than forcing a biomarker-only claim.
