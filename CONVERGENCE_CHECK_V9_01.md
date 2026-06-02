# CONVERGENCE_CHECK_V9_01

Timestamp: 2026-06-02 11:35 CEST

## State

V9 is focused on upgrading the V8 microbiome gap with primary data and then
using the result to constrain the MS-centered mechanism/intervention map.

Methodology is locked:

- `ROADMAP_V9.md`
- `MAP_METHODOLOGY_V9.md`
- Git commit: `df7c7de` (`Lock V9 microbiome upgrade methodology`)

## Microbiome Axis

### IBDMDB / HMP2

Primary data were downloaded and analyzed from the HMP2 IBDMDB MGX taxonomic
profile products.

Outputs:

- `analysis/v9_microbiome/ibdmdb_subset_analysis/REPORT.md`
- `analysis/v9_microbiome/ibdmdb_subset_50_analysis/REPORT.md`
- `data/raw/v9_microbiome_ibd/tax_profiles_subset_50/download_manifest.tsv`

Result:

- Initial subset: 30 profiles, 10 nonIBD / 10 UC / 10 CD. No FDR `<0.10`.
- Expanded subset: 106 profiles, 26 nonIBD / 30 UC / 50 CD. No FDR `<0.10`.
- Expanded subset all FDR values were `>=0.7429`.
- Largest exploratory signal was UC butyrate-clostridia higher than nonIBD:
  Hedges g `0.409`, p `0.109`, FDR `0.743`.
- Akkermansia was lower in UC and CD but unsupported after correction.

Decision:

- Do **not** upgrade IBD microbiome placement using this taxonomic
  feature-family operationalization.
- This is not a broad IBD microbiome negative. It is a negative for the
  pre-specified crude taxonomic-family test in a resource-conscious subset.
- Next viable upgrade routes: full HMP2 mixed model, HUMAnN/pathway layer,
  metabolomics, or published harmonized effect tables.

### MS Microbiome

Processed MS `phyloseq` RDS files were downloaded:

- `data/raw/v9_microbiome_ms/ps_HMS.subset.stool.itm.rds`
- `data/raw/v9_microbiome_ms/ps.ms.stool.rds`

Export and analysis scripts are prepared:

- `scripts/v9_export_ms_phyloseq.R`
- `scripts/v9_analyze_ms_microbiome.py`

Blocker:

- R package `phyloseq` was not initially installed. Bioconductor installation
  is running; `vegan` is installed, but `phyloseq` was not yet available at
  this checkpoint.

Decision:

- Continue this route once `phyloseq` installs.
- If installation fails, document the blocker and route to another MS
  processed abundance table or raw-read-lightweight alternative.

## Mechanism / Intervention Convergence

Sidecar report:

- `subagents/20260602_v9_mechanism_intervention_nietzsche.md`

Current best hypothesis remains conditional:

> Gut-barrier or microbial-metabolite regulation of APC plasticity may define
> an MS subgroup or pharmacodynamic axis, but current V9 primary-data evidence
> does not yet support a microbiome upgrade.

This should not be written as a cure claim or target nomination. The strongest
defensible use is as a forcing hypothesis for additional primary-data tests.

## Convergence / Divergence

Converging:

- V8's IBD/MS proximity on mucosal IFN/APC dynamics remains intact because it
  came from treatment-response transcriptomic evidence, not microbiome data.
- V9's IBD taxonomic-family tests do not strengthen the microbiome-mediated
  explanation of that proximity.

Diverging:

- The simple expectation that pre-specified broad taxa families would show
  robust IBD case-control differences in a small-to-moderate HMP2 subset did
  not hold.
- This pushes V9 away from genus/family-level dysbiosis and toward pathway,
  metabolite, longitudinal, and compartment-resolved microbial-immune tests.

## Next Forcing Questions

1. Can the MS processed `phyloseq` data be exported and analyzed?
2. Does MS show any pre-specified family-level microbial signal, and is its
   direction consistent with the IBD exploratory effects?
3. If family-level microbiome remains weak, is the correct V9 upgrade route
   genetics, metabolomics/pathway microbiome, or dynamic APC compartment data?
4. Do the genetics and microbiome sidecar agents identify a feasible robust
   axis upgrade that avoids the crude-taxonomy limitation?
