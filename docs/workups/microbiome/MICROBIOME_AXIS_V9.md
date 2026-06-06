# MICROBIOME_AXIS_V9

Status: completed V9 microbiome-axis synthesis.

## Question

Does primary microbiome data support the V8 hypothesis that MS and gut diseases
are near each other on a gut-microbiome axis, and is the MS/IBD proximity
microbiome-mediated rather than primarily IFN/APC/tissue-repair mediated?

## Methodology Lock

V9 methodology was locked before V9 microbiome placement upgrades:

- `ROADMAP_V9.md`
- `MAP_METHODOLOGY_V9.md`
- Git commit `df7c7de`

Pre-specified feature families:

- Akkermansia / mucin barrier
- Prevotella
- Faecalibacterium / butyrate proxy
- Bacteroides
- Enterobacteriaceae / LPS proxy
- Butyrate-clostridia

Placement rule:

- Literature-only remains provisional.
- Primary-data support requires corrected statistics and traceable input data.
- MS/IBD proximity requires same-direction or mechanistically coherent
  cross-disease evidence, not separate within-disease dysbiosis claims.

## Primary Data Sources

### MS

Source:

- `PRJEB44538`-associated processed `phyloseq` objects from
  `trocialba/Multiple_Sclerosis_Study`.

Local files:

- `data/raw/v9_microbiome_ms/ps_HMS.subset.stool.itm.rds`
- `data/raw/v9_microbiome_ms/ps.ms.stool.rds`

Scripts:

- `scripts/v9_export_ms_phyloseq.R`
- `scripts/v9_analyze_ms_microbiome.py`

Outputs:

- `analysis/v9_microbiome/ms_primary_analysis/REPORT.md`
- `analysis/v9_microbiome/ms_primary_analysis/ms_feature_family_tests.tsv`
- `analysis/v9_microbiome/ms_primary_analysis/ms_feature_family_adjusted_tests.tsv`

### IBD

Source:

- HMP2 / IBDMDB MGX taxonomic profiles.

Local files:

- `data/raw/v9_microbiome_ibd/hmp2_metadata_2018-08-20.csv`
- `data/raw/v9_microbiome_ibd/products_MGX_2017-08-12.html`
- `data/raw/v9_microbiome_ibd/tax_profiles_subset_50/*.biom`

Scripts:

- `scripts/v9_select_ibdmdb_subset.py`
- `scripts/v9_download_selected_tax_profiles.py`
- `scripts/v9_analyze_ibdmdb_subset.py`

Outputs:

- `analysis/v9_microbiome/ibdmdb_subset_50_analysis/REPORT.md`
- `data/raw/v9_microbiome_ibd/tax_profiles_subset_50/download_manifest.tsv`

## Results

### MS Case-Control Signal

MS versus healthy control stool, `95` MS and `54` controls:

| Feature family | Direction in MS | Unadjusted result | Age/sex-adjusted result | Interpretation |
| --- | --- | --- | --- | --- |
| Bacteroides | higher | Hedges g `0.716`, FDR `0.00108` | coefficient `0.0505`, FDR `0.00639` | supported in this dataset |
| Enterobacteriaceae/LPS proxy | lower | Hedges g `-0.569`, FDR `0.00836` | coefficient `-0.0647`, FDR `0.00510` | supported in this dataset |
| Faecalibacterium/butyrate proxy | lower | Hedges g `-0.360`, FDR `0.0557` | coefficient `-0.0120`, FDR `0.0341` | supported after age/sex adjustment |
| Akkermansia/mucin barrier | lower | Hedges g `-0.074`, FDR `0.798` | FDR `0.651` | not supported |
| Prevotella | lower | Hedges g `-0.039`, FDR `0.813` | FDR `0.434` | not supported |
| Butyrate-clostridia | higher | Hedges g `0.161`, FDR `0.429` | FDR `0.477` | not supported |

Paired timepoint deltas in the MS before/after object:

- No TP2/TP3/TP4 minus TP1 feature reached FDR `<0.10`.
- The largest exploratory signal was TP4-minus-TP1 Enterobacteriaceae/LPS proxy
  increase, g about `0.70`, p about `0.032`, FDR about `0.458`, with only `11`
  pairs.

### IBD Independent-Participant Subset

IBDMDB/HMP2 independent-participant subset:

- `26` nonIBD, `30` UC, `50` CD.
- No pre-specified taxonomic feature family reached FDR `<0.10`; all FDR values
  were `>=0.7429`.
- Largest exploratory signal: UC butyrate-clostridia higher than nonIBD,
  Hedges g `0.409`, p `0.109`, FDR `0.743`.
- Akkermansia was lower in UC and CD, but unsupported.

### IBD All-Sample Sensitivity

Completed.

- Selected: `1,360` MGX profiles, `106` participants.
- Caveat: repeated samples are not independent. This sensitivity can detect
  whether the independent-participant negative was a precision issue, but it
  cannot by itself upgrade to robust-grade evidence.
- Naive repeated-sample tests produced many FDR-significant differences,
  including higher Bacteroides and higher Enterobacteriaceae/LPS proxy in UC
  and CD.
- Cluster-robust participant-level tests removed FDR support:
  - UC: no feature FDR `<0.10`; strongest uncorrected p values were
    Enterobacteriaceae p `0.115` and Akkermansia p `0.122`.
  - CD: no feature FDR `<0.10`; Enterobacteriaceae p `0.00989` but FDR
    `0.119`; Faecalibacterium p `0.0863`, FDR `0.292`.

Decision:

- The naive all-sample signals are treated as pseudo-replication-sensitive.
- The independent-participant and cluster-robust results govern the V9
  placement: IBD taxonomic-family evidence is not upgraded to supported.

## Cross-Disease Interpretation

The primary-data microbiome evidence does **not** currently support a simple
MS/IBD microbiome-mediated proximity claim at the tested taxonomic-family
level.

Reasons:

- MS has a corrected case-control signal, but it is a single processed dataset.
- IBD independent-participant data did not show corrected feature-family
  differences, and all-sample signals lose support under participant-clustered
  inference.
- The exploratory IBD directions are not a clean match to MS. MS shows
  Bacteroides higher and Enterobacteriaceae lower; IBD subset effects are weak
  and, where visible, Enterobacteriaceae trends higher in disease.

Therefore:

- V8's MS/IBD proximity remains strongest on mucosal IFN/APC
  treatment-response and tissue-repair / response-monitoring axes.
- V9 upgrades MS microbiome evidence from literature-only to primary-data
  supported within one dataset.
- V9 does not upgrade the MS/IBD microbiome-proximity cell to supported or
  robust.

## Mechanistic Implications

The gut-barrier/metabolite/APC-plasticity hypothesis remains alive but
conditional.

What V9 supports:

- MS has a measurable stool microbiome feature-family shift in a processed
  primary dataset.
- The shift includes lower Faecalibacterium after age/sex adjustment, compatible
  with a butyrate/metabolite hypothesis.

What V9 does not support:

- That MS and IBD share the same taxonomic-family dysbiosis profile.
- That microbiome explains the MS/IBD IFN/APC proximity.
- That a microbiome intervention would alter MS lesion biology.

Next stronger operationalization:

- pathway/metabolite features rather than genus/family-level taxa;
- full HMP2 longitudinal modeling;
- independent MS microbiome replication;
- paired immune readouts linking microbial features to APC plasticity.

## Placement Recommendation

For the V8/V9 map:

- MS microbiome axis: upgrade from literature-only provisional to
  primary-data-supported but single-dataset, confidence moderate-low.
- IBD microbiome axis relative to MS: keep provisional until full HMP2
  pathway/metabolite data, or independent disease-overlap evidence supports it.
  The V9 all-sample HMP2 sensitivity does not change this because
  cluster-robust inference removes FDR support.
- MS/IBD microbiome-mediated proximity: do not claim.

## Reproducibility

Entry points:

```bash
Rscript scripts/v9_export_ms_phyloseq.R
.venv/bin/python scripts/v9_analyze_ms_microbiome.py
.venv/bin/python scripts/v9_select_ibdmdb_subset.py --per-diagnosis 50 --out-dir analysis/v9_microbiome/ibdmdb_subset_50
.venv/bin/python scripts/v9_download_selected_tax_profiles.py --urls analysis/v9_microbiome/ibdmdb_subset_50/selected_tax_profile_urls.tsv --out-dir data/raw/v9_microbiome_ibd/tax_profiles_subset_50 --manifest data/raw/v9_microbiome_ibd/tax_profiles_subset_50/download_manifest.tsv
.venv/bin/python scripts/v9_analyze_ibdmdb_subset.py --subset analysis/v9_microbiome/ibdmdb_subset_50/selected_ibdmdb_samples.tsv --raw-dir data/raw/v9_microbiome_ibd/tax_profiles_subset_50 --out-dir analysis/v9_microbiome/ibdmdb_subset_50_analysis
.venv/bin/python scripts/v9_select_ibdmdb_subset.py --all-samples --out-dir analysis/v9_microbiome/ibdmdb_all_samples
.venv/bin/python scripts/v9_download_selected_tax_profiles.py --urls analysis/v9_microbiome/ibdmdb_all_samples/selected_tax_profile_urls.tsv --out-dir data/raw/v9_microbiome_ibd/tax_profiles_all_samples --manifest data/raw/v9_microbiome_ibd/tax_profiles_all_samples/download_manifest.tsv
.venv/bin/python scripts/v9_analyze_ibdmdb_subset.py --subset analysis/v9_microbiome/ibdmdb_all_samples/selected_ibdmdb_samples.tsv --raw-dir data/raw/v9_microbiome_ibd/tax_profiles_all_samples --out-dir analysis/v9_microbiome/ibdmdb_all_samples_analysis
```
