# DATA_SEARCH_V9

Started: 2026-06-02 11:18 CEST

## Objective

Find primary or machine-readable data capable of upgrading V8's provisional
microbiome axis for MS, IBD, RA, and T1D. Literature-only evidence does not
upgrade placements under `MAP_METHODOLOGY_V9.md`.

## Searches And Sources

### Multiple Sclerosis

| Source | Status | Access / URL | Notes |
| --- | --- | --- | --- |
| iMSMS / Jangi MS gut microbiome cohort | accession verified | `PRJNA321051` | SRA search returned 210 runs. Raw read processing is likely too compute-heavy for this session unless processed abundance tables are found. |
| B-cell depletion MS gut microbiome study | processed RDS downloaded | `PRJEB44538`; GitHub `trocialba/Multiple_Sclerosis_Study` | ENA returns FASTQ runs. GitHub provides small `phyloseq` RDS objects for MS-vs-HC and before/after treatment analyses. |

Downloaded files:

| File | SHA256 | Source |
| --- | --- | --- |
| `data/raw/v9_microbiome_ms/ps_HMS.subset.stool.itm.rds` | `6d88e86fde81cd070769d8cfb4ed90ddf72e18a0b5eec350150be01ac65e35ec` | `https://raw.githubusercontent.com/trocialba/Multiple_Sclerosis_Study/main/MS.vs.HC/Data.Stool/ps_HMS.subset.stool.itm.rds` |
| `data/raw/v9_microbiome_ms/ps.ms.stool.rds` | `7c7589c8161de82a1441d36dc3c995e962409f494bb15ebefc13a58de48cf3fe` | `https://raw.githubusercontent.com/trocialba/Multiple_Sclerosis_Study/main/MS%20before%20vs%20after%20treatment/Data.Stool/ps.ms.stool.rds` |

Current blocker:

- The files are `phyloseq` RDS objects. Local R initially lacked `phyloseq` and
  `vegan`; installation was started on 2026-06-02.

MS primary-data result:

- Export: `scripts/v9_export_ms_phyloseq.R`.
- Analysis: `scripts/v9_analyze_ms_microbiome.py`.
- Output: `analysis/v9_microbiome/ms_primary_analysis/REPORT.md`.
- MS-vs-control stool cohort: `95` MS and `54` healthy controls, group column
  `Status`.
- Corrected signals:
  - Bacteroides higher in MS: Hedges g `0.716`, p `0.000180`, FDR `0.00108`.
  - Enterobacteriaceae/LPS proxy lower in MS: Hedges g `-0.569`, p `0.00279`,
    FDR `0.00836`.
  - Faecalibacterium/butyrate proxy lower in MS: Hedges g `-0.360`, p
    `0.0278`, FDR `0.0557` (near-threshold, not FDR `<0.05`).
- Age/sex-adjusted OLS sensitivity:
  - Bacteroides remained higher in MS: adjusted coefficient `0.0505`,
    p `0.00213`, FDR `0.00639`.
  - Enterobacteriaceae/LPS proxy remained lower in MS: adjusted coefficient
    `-0.0647`, p `0.000850`, FDR `0.00510`.
  - Faecalibacterium/butyrate proxy became FDR-supported after age/sex
    adjustment: adjusted coefficient `-0.0120`, p `0.0171`, FDR `0.0341`.
- Paired MS timepoint deltas were computed for the before/after object and the
  MS subset embedded in the combined object. No paired timepoint comparison
  reached FDR `<0.10`; the largest exploratory TP4-minus-TP1 signal was
  Enterobacteriaceae/LPS proxy increase, g about `0.70`, p about `0.032`, FDR
  about `0.458`, with only `11` pairs.
- Decision: MS now has a primary-data microbiome signal at pre-specified
  taxonomic-family level, but this is one processed dataset and therefore not
  robust by itself. It supports a V9 upgrade from literature-only to
  primary-data-supported within-MS microbiome evidence, but not a robust
  MS/IBD microbiome-mediated proximity claim.

### IBD

| Source | Status | Access / URL | Notes |
| --- | --- | --- | --- |
| HMP2 / iHMP IBDMDB | primary data subsets downloaded and analyzed | `https://www.nature.com/articles/s41586-019-1237-9`; `https://ibdmdb.org/results` | Metadata, product URLs, an initial 30-profile subset, and an expanded independent-participant subset were downloaded and analyzed. |

Downloaded IBD files:

| File | SHA256 | Notes |
| --- | --- | --- |
| `data/raw/v9_microbiome_ibd/hmp2_metadata_2018-08-20.csv` | `656b7bd97660ddb875548805e30bede31f2d1208293f7170d2d5755e33862ec9` | 5533 metadata rows. |
| `data/raw/v9_microbiome_ibd/products_MGX_2017-08-12.html` | `554efe1180df5d7a27f4da7347cff40c8d543248fddca5ad5b6ec894638c0644` | Product-page source for taxonomic BIOM URLs. |
| `data/raw/v9_microbiome_ibd/tax_profiles_subset/*.biom` | per-file hashes printed in shell output | 30 selected taxonomic profile BIOMs, 10 nonIBD / 10 UC / 10 CD. |
| `data/raw/v9_microbiome_ibd/tax_profiles_subset_50/*.biom` | `data/raw/v9_microbiome_ibd/tax_profiles_subset_50/download_manifest.tsv` | 106 independent-participant taxonomic profile BIOMs: 26 nonIBD / 30 UC / 50 CD. |

IBD primary-data result:

- Script: `scripts/v9_select_ibdmdb_subset.py`.
- Script: `scripts/v9_download_selected_tax_profiles.py`.
- Script: `scripts/v9_analyze_ibdmdb_subset.py`.
- Output: `analysis/v9_microbiome/ibdmdb_subset_analysis/REPORT.md`.
- No pre-specified feature family reached FDR `<0.10` in the small subset.
- This is **not** evidence that IBD lacks microbiome involvement. It means the
  V9 small subset is insufficient to upgrade V8's IBD microbiome placement.

Expanded IBDMDB subset result:

- Selection: `scripts/v9_select_ibdmdb_subset.py --per-diagnosis 50 --out-dir analysis/v9_microbiome/ibdmdb_subset_50`.
- Download: `scripts/v9_download_selected_tax_profiles.py --urls analysis/v9_microbiome/ibdmdb_subset_50/selected_tax_profile_urls.tsv --out-dir data/raw/v9_microbiome_ibd/tax_profiles_subset_50 --manifest data/raw/v9_microbiome_ibd/tax_profiles_subset_50/download_manifest.tsv`.
- Analysis: `scripts/v9_analyze_ibdmdb_subset.py --subset analysis/v9_microbiome/ibdmdb_subset_50/selected_ibdmdb_samples.tsv --raw-dir data/raw/v9_microbiome_ibd/tax_profiles_subset_50 --out-dir analysis/v9_microbiome/ibdmdb_subset_50_analysis`.
- Usable profiles: `106`; missing profiles: `0`.
- Actual independent-participant counts were limited by available product files:
  `26` nonIBD, `30` UC, `50` CD.
- No pre-specified feature family reached FDR `<0.10`; all FDR values were
  `>=0.7429`.
- Largest exploratory effect: UC butyrate-clostridia higher than nonIBD,
  Hedges g `0.409`, p `0.109`, FDR `0.743`. Akkermansia was lower in UC
  (g `-0.386`) and CD (g `-0.353`) but not statistically supported.
- Decision: the expanded primary-data subset still does **not** upgrade the
  IBD microbiome placement under `MAP_METHODOLOGY_V9.md`. A full HMP2 analysis,
  pathway/metabolite layer, or published harmonized effect table is needed.

All-sample IBDMDB sensitivity:

- Selection: `scripts/v9_select_ibdmdb_subset.py --all-samples --out-dir analysis/v9_microbiome/ibdmdb_all_samples`.
- Download: `1,360` profiles, manifest
  `data/raw/v9_microbiome_ibd/tax_profiles_all_samples/download_manifest.tsv`.
- Analysis output:
  `analysis/v9_microbiome/ibdmdb_all_samples_analysis/REPORT.md`.
- Naive repeated-sample tests produced multiple FDR-significant taxonomic
  differences, including higher Bacteroides and Enterobacteriaceae/LPS proxy in
  both UC and CD.
- Because samples are repeated within only `106` participants, a
  participant-clustered OLS sensitivity was run and written to
  `analysis/v9_microbiome/ibdmdb_all_samples_analysis/ibdmdb_feature_family_cluster_robust_tests.tsv`.
- Cluster-robust result: no feature family reached FDR `<0.10`; CD
  Enterobacteriaceae had p `0.00989` but FDR `0.119`.
- Decision: all-sample signals are pseudo-replication-sensitive and do not
  override the independent-participant negative.

### Rheumatoid Arthritis

| Source | Status | Access / URL | Notes |
| --- | --- | --- | --- |
| RA gut microbiome studies | literature identified only | RA Prevotella/gut-joint reviews from V8 | Need machine-readable abundance table or published effect table. |

### Type 1 Diabetes

| Source | Status | Access / URL | Notes |
| --- | --- | --- | --- |
| TEDDY microbiome | identified | `https://pmc.ncbi.nlm.nih.gov/articles/PMC6296767/` | High-value longitudinal source; may require controlled access or published supplementary tables. Needs access check. |

## Decisions So Far

1. Raw-read pipelines are a fallback only. The V9 target is processed abundance,
   pathway, or effect tables because raw metagenomic processing would exceed a
   reasonable single-session compute budget.
2. MS processed data are immediately tractable if `phyloseq` can be installed
   or if the RDS can be exported with another method.
3. IBDMDB 30-profile, 106-profile independent-participant, and 1,360-profile
   all-sample/cluster-robust analyses do not support upgrading IBD microbiome
   placement using the pre-specified taxonomic feature families.
   Pathway/metabolite layers or better longitudinal mixed models would be
   needed.
4. No microbiome placement upgrade has been made yet.
