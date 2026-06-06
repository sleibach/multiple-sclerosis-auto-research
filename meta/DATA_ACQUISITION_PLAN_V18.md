# DATA_ACQUISITION_PLAN_V18

Date: 2026-06-06

## Purpose

V18 addressed a data-source ceiling from V17: the MS-UC chr1 locus remains a
`GPR25` versus `KIF21B` causal-gene ambiguity. V18 did not attempt to make a
new therapeutic claim. It identified, acquired, and triaged data sources that
could resolve genotype-linked immune-cell expression or protein evidence.

## First-Action Verification

OpenGWAS access was verified with:

```bash
.venv/bin/python scripts/check_opengwas_access.py
```

Result:

- `/user`: HTTP 200.
- JWT valid until `2026-06-19 12:28 UTC`.
- POST `gwasinfo` for `ieu-b-18`: HTTP 200.
- POST `tophits` for `ieu-b-18`: HTTP 200.

No OpenGWAS GET-style calls were used.

## Tier 1 Acquired

All acquired files are under `data/raw/v18_source_triage/`; checksums are in
`analysis/v18_source_triage/acquired_sha256.tsv` and manifest rows are appended
to `data/manifest.tsv`.

### OneK1K

Source:

- Documentation/page: `https://onek1k.org/` (HTTP 200).
- Acquired file:
  `https://zenodo.org/records/18870747/files/OneK1K_TensorQTL_top_eQTL_summary.zip?download=1`.
- Local path:
  `data/raw/v18_source_triage/onek1k/OneK1K_TensorQTL_top_eQTL_summary.zip`.
- Size: `16,950,155` bytes.
- SHA-256:
  `a3100acf36aedfbb78ab7ddc1113b9dcb119170c9c4b863d37b99a0edee05d5d`.

Smoke test:

- Zip contains `617` entries.
- Target-gene scan found `14` OneK1K top-eQTL hits, all for `KIF21B`, across
  immune-cell subsets including monocytes, NK, CD8, plasma, DC, B, and CD4
  subsets.
- No `GPR25` or `CXCL17` top-eQTL hit was found in the acquired top-eQTL
  summaries.
- Fast overlap check against the V17 shared MS-UC credible set found no exact
  position match. The nearest OneK1K KIF21B hits were CD8_NC at `17,230 bp`
  and NK at `21,012 bp` from the nearest V17 credible-set variant; most were
  hundreds of kb away.

Relevance:

- Directly relevant genotype-linked immune eQTL source.
- Current public top-eQTL layer supports `KIF21B` more than `GPR25`.
- It does not resolve the full locus because top-eQTL summaries are not
  full-summary-statistics colocalization and do not provide protein/CITE-seq.

### DICE

Source:

- Documentation/downloads page: `https://dice-database.org/downloads`
  (HTTP 200).
- Acquired mean expression:
  `https://dice-database.org/download/mean_tpm_merged.csv`.
- Acquired significant eQTL VCF panel:
  - `B_CELL_NAIVE`
  - `MONOCYTES`
  - `M2`
  - `NK`
  - `CD4_NAIVE`
  - `CD4_STIM`
  - `CD8_NAIVE`
  - `CD8_STIM`
  - `TH1`
  - `TH17`
  - `TREG_NAIVE`
  - `TREG_MEM`
  - `TFH`

Local path:

- `data/raw/v18_source_triage/dice/`.

Smoke test:

- Mean TPM file uses Ensembl IDs.
- Target-expression summary:
  - `GPR25` (`ENSG00000170128`) is low but nonzero in selected T/NK subsets;
    max mean TPM `1.35495808486` in memory Treg.
  - `KIF21B` (`ENSG00000116852`) is high across immune subsets; max mean TPM
    `180.946938037` in memory Treg.
  - `CXCL17` (`ENSG00000189377`) is low/moderate; max mean TPM
    `0.656931673015` in naive B cells.
- Significant eQTL scan found one target hit:
  - DICE NK significant eQTL for `KIF21B`:
    `chr1:200076646:AACAG:A`, beta `0.81581214249`,
    p `1.49359908386e-05`.
- No significant DICE eQTL hit for `GPR25` or `CXCL17` was found in the
  acquired significant VCF panel.
- The DICE NK KIF21B hit did not exactly match the V17 shared credible set and
  was `797,583 bp` from the nearest V17 credible-set variant.

Relevance:

- Directly relevant immune-cell eQTL/expression source.
- Supports KIF21B as the better transcript-visible candidate.
- Public significant files do not resolve whether GPR25 has weaker but real
  genotype-linked effects; controlled DICE individual-level data would be
  needed for custom tests.

### eQTL Catalogue / BLUEPRINT-style FTP-tabix Source

Source:

- API docs: `https://www.ebi.ac.uk/eqtl/api-docs/` (HTTP 200).
- REST smoke endpoint `https://www.ebi.ac.uk/eqtl/api/studies?size=5` returned
  HTTP 500 from `www.ebi.ac.uk`; no proxy `x-deny-reason`.
- Direct FTP/tabix source:
  `ftp://ftp.ebi.ac.uk/pub/databases/spot/eQTL/sumstats/QTS000002/QTD000021/QTD000021.all.tsv.gz`.
- Full source size: `2,991,536,954` bytes; full file not downloaded.
- `.tbi` index size: `1,935,109` bytes.

Acquired targeted extract:

- Local path:
  `data/raw/v18_source_triage/eqtl_catalogue/QTD000021_chr1_200000000_202000000_targets.tsv`.
- Size: `1,381,267` bytes.
- SHA-256:
  `5e1c4dc36cabd1f31531b7a1fa3b79b8cbb0675a11925f2c2d812e44a1aa0171`.

Smoke test:

- Remote tabix via `pysam` succeeded.
- Extracted `8,416` rows in chr1:200,000,000-202,000,000 for target gene IDs.
- Rows were all for `KIF21B`; no rows for `GPR25` or `CXCL17` were returned in
  this QTD000021 target extract.

Relevance:

- Useful as a direct full-summary-statistics-style targeted QTL source.
- The current QTD000021 extract supports KIF21B availability but does not
  resolve GPR25.
- REST metadata was unavailable due HTTP 500, so study/tissue metadata should
  be verified before publication-grade use.
- A proper next step would intersect QTD000021 variant IDs with the V17
  credible set and run formal QTL colocalization only after metadata is
  verified.

### IUPHAR / Guide to Pharmacology

Source:

- `https://www.guidetopharmacology.org/services/targets?name=GPR25`.

Local path:

- `data/raw/v18_source_triage/iuphar/gpr25_targets.json`.

Smoke test:

- JSON returned target ID `95`, type `GPCR`.

Relevance:

- GPR25 ligand/target annotation.
- Peripheral to causal-gene resolution; useful for agonist feasibility.

### GPCRdb

Source:

- `https://gpcrdb.org/services/protein/gpr25_human/`.

Local path:

- `data/raw/v18_source_triage/gpcrdb/gpr25_human.json`.

Smoke test:

- JSON returned `entry_name = gpr25_human`, accession `O00155`.

Relevance:

- GPCR structural/sequence context.
- Peripheral to causal-gene resolution; useful only if GPR25 remains causal.

## Tier 1 Blocked / Not Acquired

| Source | Status | Exact result | Human action |
|---|---|---|---|
| eQTL Catalogue REST API | Service error | `GET https://www.ebi.ac.uk/eqtl/api/studies?size=5` returned HTTP 500, host `www.ebi.ac.uk`, no `x-deny-reason`. | No allowlist needed; retry later or use FTP/tabix. |
| BLUEPRINT/eQTL Catalogue full QTD000021 file | Resource-heavy but reachable | FTP HEAD returned size `2,991,536,954` bytes; targeted remote tabix worked. | No immediate human action; full download not needed unless publication-grade broad scan is required. |
| OneK1K GEO raw tar `GSE196830_RAW.tar` | Resource-heavy but reachable | FTP HEAD returned size `13,459,619,840` bytes. | Download only if raw scRNA is needed; public top-eQTL summaries already acquired. |
| DICE unfiltered eQTL VCFs | Resource-heavy but reachable | Per-cell unfiltered files are ~3.3-3.4 GB each; significant VCF panel acquired instead. | Download only if custom non-significant eQTL testing is required and storage/time allow. |
| CELLxGENE Census / HCA | Open, not acquired | Docs reachable; not genotype-linked and less direct than OneK1K/DICE for this run. | Use later for expression-only context, not causal-gene resolution. |
| BLUEPRINT portal homepage | Stale URL | `https://blueprint-epigenome.eu/` returned HTTP 404. | Use eQTL Catalogue/FTP or IHEC/Ensembl mirrors instead of the stale homepage. |

No proxy-blocked source with `x-deny-reason` was observed in V18.

## Tier 2

See `meta/DATA_TIER2_KEY_REQUESTS.md`.

Summary:

- No new simple API-key-gated source was promoted.
- OpenGWAS remains the only active key-gated source, already handled by
  `OPENGWAS_JWT` and `scripts/check_opengwas_access.py`.

## Tier 3

See `meta/DATA_TIER3_DOWNLOAD_INSTRUCTIONS.md`.

Highest-leverage controlled/manual sources:

1. OneK1K individual-level genotype/scRNA, if not fully public in `GSE196830`.
2. DICE controlled individual-level data through dbGaP `phs001703.v3.p1`.
3. MS PBMC/CSF single-cell plus genotype or CITE-seq controlled cohorts through
   dbGaP/EGA.
4. UK Biobank or other large biobank genotype/immune phenotype data.

## Ranked Relevance To GPR25-versus-KIF21B

| Rank | Source | Tier | Verdict |
|---:|---|---|---|
| 1 | MS PBMC/CSF genotype plus single-cell/CITE-seq cohorts | 3 | Directly resolves the ambiguity if GPR25 surface/transcript or KIF21B expression is genotype-linked in MS material. |
| 2 | OneK1K individual-level genotype/scRNA | 3 or resource-heavy Tier 1 | Best healthy-immune genotype-linked source for custom chr1 tests. |
| 3 | DICE controlled individual-level data | 3 | Lets the project test non-significant or subset-specific GPR25 effects missed by public significant VCFs. |
| 4 | OneK1K public top eQTL | 1 acquired | Supports KIF21B top-eQTL hits; no GPR25 top hit. |
| 5 | DICE public significant eQTL + mean expression | 1 acquired | Supports strong KIF21B expression and a KIF21B NK eQTL; no GPR25 significant eQTL hit. |
| 6 | eQTL Catalogue QTD000021 targeted extract | 1 acquired | KIF21B-only target extract in chr1 interval; useful but metadata needs verification. |
| 7 | IUPHAR/GPCRdb | 1 acquired | Supports GPR25 target/GPCR feasibility, not causality. |
| 8 | CELLxGENE/HCA expression-only data | 1 not acquired | Context only; no genotype-linked resolution. |

## What The Human Should Do Next

1. **Controlled MS PBMC/CSF data first.** Search/apply for MS PBMC/CSF
   genotype plus scRNA/CITE-seq cohorts through dbGaP/EGA. Place files under
   `data/raw/ms_csf_pbmc_genotype_sc/`.
2. **DICE controlled data second.** Apply for dbGaP `phs001703.v3.p1`; public
   DICE data already points toward KIF21B, but controlled data is needed for
   custom GPR25 non-significant tests.
3. **OneK1K raw/individual-level next.** Inspect/download `GSE196830_RAW.tar`
   only if it contains the individual-level data needed; otherwise follow the
   publication/GEO controlled-data instructions.
4. **No host allowlisting is currently needed.** V18 observed no proxy
   `x-deny-reason`; eQTL Catalogue REST failures are server/API-side.
5. **Do not spend effort on GPCR chemistry before causality.** IUPHAR/GPCRdb
   are acquired, but GPR25 should not receive agonist-program effort until
   protein/genotype-linked immune-cell evidence distinguishes it from KIF21B.

## Immediate Computational Next Action

Use the acquired Tier 1 files to run a bounded chr1 fine-mapping/eQTL overlap
check:

```bash
.venv/bin/python scripts/v18_smoke_test_acquired_sources.py
```

The OneK1K/DICE top/significant-hit overlap check has already been run:
`analysis/v18_source_triage/v18_hits_vs_v17_credible_set.tsv`. Next,
prioritize formal QTD000021/eQTL Catalogue intersection and colocalization only
if metadata is verified; otherwise move to controlled/protein-level data.
