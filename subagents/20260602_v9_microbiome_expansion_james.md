# V9 Microbiome Primary-Data Expansion Scout

Timestamp: 2026-06-02 11:31 CEST

Scope: report-only recommendation for upgrading the V8 microbiome axis beyond
literature using primary or machine-readable data. I inspected
`DATA_SEARCH_V9.md`, `MAP_METHODOLOGY_V9.md`, the IBDMDB subset scripts, and
`analysis/v9_microbiome`. I did not edit shared indexes.

## Bottom Line

The most tractable immediate primary-data route is **scaling the existing
IBDMDB/HMP2 MGX taxonomic-profile analysis from 30 profiles to the available
matched tax-profile set**. The path is already proven locally, uses small BIOM
files, is pure Python, and directly satisfies the V9 requirement for a
machine-readable taxonomic relative-abundance table. It can upgrade the IBD
microbiome placement to `supported` only if the expanded analysis finds at
least two pre-specified feature-family effects with FDR `<0.10`, or if it
integrates longitudinal/treatment perturbation evidence from the same IBDMDB
metadata. The current 30-sample subset does **not** meet that bar.

The fastest secondary route is the downloaded MS phyloseq data from
`PRJEB44538` / `trocialba/Multiple_Sclerosis_Study`, but it is currently
dependency-blocked by missing R `phyloseq`. Once exported, it is small enough
to analyze quickly and would provide the MS side needed for disease-relative
placement rather than IBD-only evidence.

## Route 1: Expanded IBDMDB Tax-Profile Analysis

Recommendation: primary route.

Exact sources:

- Study / resource: HMP2 / iHMP IBDMDB.
- Publication URL: `https://www.nature.com/articles/s41586-019-1237-9`.
- Resource URL: `https://ibdmdb.org/results`.
- Local product-page source: `data/raw/v9_microbiome_ibd/products_MGX_2017-08-12.html`.
- Local metadata: `data/raw/v9_microbiome_ibd/hmp2_metadata_2018-08-20.csv`.
- Tax-profile URL pattern:
  `https://g-227ca.190ebd.75bc.data.globus.org/ibdmdb//products/HMP2/MGX/2018-05-04/tax_profiles/<PRODUCT_ID>_taxonomic_profile.biom`.
- Example verified profile URL:
  `https://g-227ca.190ebd.75bc.data.globus.org/ibdmdb//products/HMP2/MGX/2018-05-04/tax_profiles/CSM67UH7_taxonomic_profile.biom`.

Current local status:

- Metadata rows: `5533`.
- Candidate MGX rows after data-type filtering: `1360`.
- Unique tax-profile URLs parsed from product page: `1338`.
- MGX rows matching tax-profile product IDs: `1360`.
- Matched diagnosis rows: CD `605`, UC `381`, nonIBD `374`.
- Matched participants: `106`.
- Participants by diagnosis after first participant row: CD `50`, UC `30`,
  nonIBD `26`.
- Current pilot subset: 30 profiles, balanced 10 nonIBD / 10 UC / 10 CD.
- Current pilot result: no pre-specified feature family reached FDR `<0.10`.

Expected compute:

- Download size: current BIOM profiles are roughly `16-49 KB` each. Full
  1,338-profile download should be on the order of tens of MB, not GB.
- CPU/RAM: pure Python JSON/BIOM parsing and feature-family scoring should run
  comfortably on a laptop. Expected RAM under `1 GB`; likely minutes, not
  hours, after downloads.
- Network risk: moderate. URLs are Globus-hosted HTTPS endpoints; the 30-file
  subset downloaded successfully. If some product IDs fail, log missing profiles
  and continue, but do not infer missing data.

Required implementation changes:

- Reuse `scripts/v9_select_ibdmdb_subset.py` logic but add a full or stratified
  mode:
  - full one-sample-per-participant early-sample analysis;
  - larger balanced participant-level subset if full longitudinal handling is
    too noisy;
  - optional longitudinal mode using repeated samples and mixed models.
- Reuse `scripts/v9_download_selected_tax_profiles.py` for the expanded URL
  table.
- Reuse `scripts/v9_analyze_ibdmdb_subset.py`, but strengthen it for V9:
  - participant-level independence or mixed model for repeated measures;
  - BH FDR within disease-vs-control feature tests;
  - signed feature-family vector for UC-vs-nonIBD and CD-vs-nonIBD;
  - optional longitudinal flare/nonflare or dysbiosis-state analysis if
    metadata fields support it.

Can it meet `MAP_METHODOLOGY_V9.md` supported-grade rules?

- **Yes, potentially for IBD**, because it provides primary taxonomic
  relative-abundance data and enough samples/participants to test the
  pre-specified families with FDR correction.
- It can reach `near/supported` relative to MS only if paired with an MS
  primary-data analysis showing same-direction overlap in at least two
  microbial functional/taxon families, or if a published corrected MS effect
  table is used.
- It can reach `robust` only if the longitudinal structure of IBDMDB is used
  as longitudinal evidence or if independent cross-platform replication is
  added. Cross-sectional IBDMDB alone cannot be robust under V9.

Best use:

1. Run expanded IBDMDB to produce an adequately powered IBD microbial feature
   vector.
2. Use it as the IBD side of the MS-relative comparison.
3. Pair with Route 2 MS phyloseq export or another processed MS abundance
   table before attempting any supported placement relative to MS.

## Route 2: Downloaded MS Phyloseq Data From PRJEB44538

Recommendation: fastest secondary route after dependency unblock.

Exact sources:

- Study accession: `PRJEB44538`.
- GitHub repository: `https://github.com/trocialba/Multiple_Sclerosis_Study`.
- Downloaded MS-vs-HC stool phyloseq object:
  `https://raw.githubusercontent.com/trocialba/Multiple_Sclerosis_Study/main/MS.vs.HC/Data.Stool/ps_HMS.subset.stool.itm.rds`.
- Downloaded before/after treatment stool phyloseq object:
  `https://raw.githubusercontent.com/trocialba/Multiple_Sclerosis_Study/main/MS%20before%20vs%20after%20treatment/Data.Stool/ps.ms.stool.rds`.
- Local files:
  - `data/raw/v9_microbiome_ms/ps_HMS.subset.stool.itm.rds`
  - `data/raw/v9_microbiome_ms/ps.ms.stool.rds`

Current blocker:

- The RDS files are `phyloseq` objects.
- Local R version is `4.6.0`.
- `vegan` is installed, but `phyloseq` is not installed.
- `readRDS()` identifies the class, but slot access/export fails without
  `phyloseq`.
- Existing scripts are already scaffolded:
  - `scripts/v9_export_ms_phyloseq.R`
  - `scripts/v9_analyze_ms_microbiome.py`

Expected compute:

- Data size: local RDS files are small: `334 KB` and `211 KB`.
- After installing/exporting `phyloseq`, table export and feature-family
  analysis should be trivial: seconds to minutes, RAM well under `1 GB`.
- Main cost is dependency installation, not computation.

Can it meet `MAP_METHODOLOGY_V9.md` supported-grade rules?

- **Potentially yes for MS primary-data support**, because it should expose
  taxonomic abundance and metadata tables.
- By itself, one MS dataset is not enough for robust placement.
- It can contribute to `near/supported` or `intermediate/supported` if its
  feature-family directions overlap with expanded IBDMDB or with another
  independent MS/IBD/RA/T1D quantitative dataset.
- The before/after treatment object may provide perturbation evidence; if the
  metadata contains treatment timing and paired subjects, this could help move
  from cross-sectional support toward robust, but only after actual export and
  corrected tests.

Best use:

1. Install or otherwise provide `phyloseq`.
2. Run `scripts/v9_export_ms_phyloseq.R`.
3. Run `scripts/v9_analyze_ms_microbiome.py`.
4. Compare signed MS feature-family effects with expanded IBDMDB effects.

## Route 3: iMSMS / Jangi MS Gut Microbiome

Recommendation: not the next primary route unless processed tables are found.

Exact source:

- Accession: `PRJNA321051`.
- DATA_SEARCH_V9 note: SRA search returned `210` runs.

Current status:

- Raw reads appear available through SRA/ENA.
- No processed abundance table has been located locally.

Expected compute:

- Raw-read processing for 210 microbiome runs would exceed the intended V9
  single-session compute budget if done from scratch.
- Even a lightweight 16S pipeline would require download, QC, denoising or OTU
  assignment, taxonomy classification, and batch/metadata handling.

Can it meet `MAP_METHODOLOGY_V9.md` supported-grade rules?

- Yes in principle, because it is an MS primary dataset, but not tractable
  unless a processed abundance/effect table is found.
- Route around for now; do not attempt raw processing unless V9 explicitly
  allocates a raw-read pipeline budget.

## Route 4: RA Or T1D Primary Microbiome Datasets

Recommendation: scout later, not the immediate expansion route.

Candidate sources from `DATA_SEARCH_V9.md`:

- RA gut microbiome: literature identified only; no machine-readable abundance
  table or corrected effect table located locally.
- TEDDY/T1D microbiome:
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC6296767/`.

Current status:

- RA currently lacks a verified machine-readable table in the local V9 search.
- TEDDY is high-value and longitudinal, but access may be controlled or limited
  to supplementary published tables. It needs a dedicated access check.

Expected compute:

- If TEDDY supplementary feature tables are accessible: low to moderate.
- If controlled access or raw metagenomics are required: high administrative or
  compute blocker.

Can it meet `MAP_METHODOLOGY_V9.md` supported-grade rules?

- TEDDY could be extremely valuable because longitudinal evidence can support
  robust placement, but current access status is unresolved.
- RA cannot currently upgrade the axis without locating a primary table.

## Recommended Routing

1. **Expand IBDMDB now.** It is the only fully unblocked route with verified
   primary data, local metadata, URL inventory, and working analysis code.
2. **Unblock MS phyloseq next.** Install/export `phyloseq` or find another way
   to extract OTU/taxonomy/sample tables from the RDS objects. This gives the
   MS comparator required for an MS-relative microbiome placement.
3. **Only then attempt V9 supported-grade placement.** Under
   `MAP_METHODOLOGY_V9.md`, an IBD-only expanded result can support IBD
   primary-data evidence, but it cannot by itself upgrade disease similarity
   relative to MS.
4. **Keep iMSMS raw reads and TEDDY as second-wave routes.** They are valuable
   but not the fastest route to a V9 primary-data upgrade.

## Supported-Grade Feasibility Assessment

| Route | Data type | Current blocker | Compute | Supported-grade potential |
|---|---|---|---|---|
| Expanded IBDMDB tax profiles | primary taxonomic relative abundance | none beyond downloading more BIOMs | low/moderate; likely minutes and <1 GB RAM | yes for IBD primary evidence; needs MS comparator for MS-relative placement |
| MS PRJEB44538 phyloseq | processed primary taxonomic abundance | missing R `phyloseq` export dependency | low after dependency | yes as MS comparator; possibly treatment perturbation if paired metadata supports it |
| iMSMS / `PRJNA321051` | raw microbiome reads | raw-read processing burden; no processed table found | high | yes in principle, not tractable now |
| RA microbiome | unknown | no verified machine-readable table | unknown | not currently |
| TEDDY/T1D | likely longitudinal microbiome tables or controlled data | access unresolved | low if tables; high/blocker if controlled/raw only | high if accessible, but not immediate |

## Do Not Overclaim

The current IBDMDB pilot is negative under V9 correction: no tested feature
family reached FDR `<0.10` in the 30-profile subset. The route is recommended
because it is tractable and adequately scalable, not because it has already
produced a supported microbiome placement.

