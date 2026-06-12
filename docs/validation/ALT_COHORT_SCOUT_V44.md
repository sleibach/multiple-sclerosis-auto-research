# ALT_COHORT_SCOUT_V44: Alternative And Replication Cohort Scout

Date: 2026-06-12

Status: Workstream 1 value-complete pass. This is a data-discovery and
verification artifact, not a validation analysis. No locked rule was changed and
no quarantined or real Gafson data were read.

## Direct Answer

V44 did **not** find a fresh, public, ready-to-run Tier 1 primary validation
cohort that breaks dependence on Gafson.

The public/low-barrier state is now:

1. **Best primary validation target remains Gafson et al. 2018 DMF PBMC
   RNA-seq** (`PMID 30283812`): MS, dimethyl fumarate, baseline plus 6-week
   early treatment plus 15-month timepoint, NEDA-4 endpoint in the publication.
   It is still Tier 2 because processed expression plus sample-level labels are
   not publicly available in a verified accession.
2. **Best secondary MS cohort remains the Karolinska DMF ROS cohort
   (`GSE130478/GSE130491/GSE130494`)**: public longitudinal omics, but
   patient-level beneficial-response labels are absent from the public matrices.
   It needs a label request before it can validate anything.
3. **New useful open-but-not-validation cohort surfaced in V44:
   `GSE228330` anti-CD20/ocrelizumab PBMC expression**. It has baseline, 2-week,
   and 6-month PBMC expression around anti-CD20 initiation, but the GEO record
   does not provide responder/nonresponder or NEDA labels. It is useful for
   pharmacodynamic/context checks and batch-harness testing, not for response
   validation.
4. **Only open labeled fresh-ish dataset remains the caveated `GSE85034`
   methotrexate arm**, already noted by V24: psoriasis skin, week 16, same study
   source as the used adalimumab arm. It is a secondary stress test only, not
   independent MS validation.

Bottom line: V44 strengthens, rather than overturns, V24. The ready public well
for primary validation is dry; the low-barrier well is not. The next rational
move remains acquiring Gafson data and Karolinska label mappings, while treating
Gafson-sized evidence as potentially inconclusive under the V43 power map.

## Search Audit

Machine-readable outputs:

- `analysis/v44_alt_cohort_scout/search_counts.tsv`
- `analysis/v44_alt_cohort_scout/raw_search_hits.json`
- `analysis/v44_alt_cohort_scout/candidate_inventory.tsv`
- `analysis/v44_alt_cohort_scout/summary.json`

Search terms covered MS DMTs and bounded-domain cross-disease therapies:
dimethyl fumarate, Gafson/NEDA, fingolimod, ocrelizumab, natalizumab,
teriflunomide, cladribine, alemtuzumab, RA JAK inhibitors, IBD JAK inhibitors,
IBD biologics, and psoriasis response transcriptomics.

Repository/API coverage:

| Source | Queries | Status | Total raw hits | Interpretation |
|---|---:|---|---:|---|
| NCBI GEO DataSets | 11 | ok | 34 | Primary source for GEO accessions. |
| NCBI PubMed | 11 | ok | 162 | Published-paper mining source. |
| NCBI SRA | 11 | ok | 345 | Raw sequencing hit source; many non-specific. |
| Europe PMC | 11 | ok | 84 | Paper/data-availability mining source. |
| BioStudies/ArrayExpress | 11 | ok | 61 | EBI repository coverage; no ready MS validation cohort verified. |
| Zenodo | 11 | ok | 1 | No validation cohort verified. |
| Figshare | 11 | ok | 55 | Mostly supplementary PDFs/tables; no fresh ready cohort verified. |
| Dryad | 11 | ok | 779,933 | Broad API search is highly non-specific; used only as coverage signal, not candidate evidence. |
| ENA study search | 11 | blocked | 0 | API rejected broad free-text syntax with HTTP 400; not counted as a null. |
| OSF preprints | 11 | blocked | 0 | API returned HTTP 400 for these structured queries; not counted as a null. |

Important: raw hit counts are **not** candidate counts. V44 only counts a source
as usable if the record itself verifies paired/longitudinal samples, response
labels, and transcriptomic module feasibility.

## Verified Candidate Inventory

| Rank | Source | Access tier | Paired/longitudinal? | Response labels? | Module genes? | Verdict |
|---:|---|---|---|---|---|---|
| 1 | Gafson et al. 2018 DMF PBMC RNA-seq, `PMID 30283812` | Tier 2 low-barrier author/data request | Yes: baseline, 6 weeks, 15 months reported | Yes in publication; sample-level labels not public | Not verifiable until files are received | **Best next data request** |
| 2 | `GSE130478/GSE130491/GSE130494` Karolinska DMF ROS cohort | Tier 1 expression/methylation open; Tier 2 labels | Yes: baseline/3m/6m across CD4/CD14; expression mainly CD4 baseline/6m | Beneficial response described; patient-level mapping absent | Likely expression-compatible, but validation blocked by labels | **Low-barrier label request** |
| 3 | `GSE228330` anti-CD20/ocrelizumab PBMC expression | Tier 1 open | Yes: before, 2 weeks, 6 months after first infusion | No responder/NEDA labels found in GEO | Likely platform-compatible, not counted because labels absent | Open pharmacodynamic/context cohort only |
| 4 | `GSE85034` methotrexate arm | Tier 1 local/open | Yes: baseline/week16 lesional skin | Yes: PASI75 labels locally available | V24 verified 9 frozen genes represented | Caveated secondary stress test only |
| 5 | `GSE253495` RA upadacitinib CD14 monocytes | Tier 1 open | Yes: baseline and 3 months | No discriminating responder class; all improved in V24 review | RNA-seq likely covers genes | JAK pharmacodynamic only |
| 6 | Natalizumab pharmacogenomics, `PMID 39264442` | Publication open; not transcriptomic | Clinical response follow-up, not paired expression | Yes | Not applicable | Not usable for V22 module validation |
| 7 | `GSE235357` DMF | Tier 1 local/open | Yes | Yes | Yes | Exclude: already used in V22 |
| 8 | `GSE250453` fingolimod | Tier 1 local/open | Yes | Yes | Yes | Exclude: already used in V22 |

## Record-Level Verification Notes

### Gafson et al. 2018

V24 and V44 both identify Gafson as the strongest primary validation target.
The project still lacks the expression matrix and sample-level NEDA-4 metadata,
so V44 does not classify it as public-ready. It remains the highest-leverage
low-barrier human acquisition.

Required request:

- processed or raw gene-level PBMC RNA-seq for all timepoints;
- sample-to-subject map;
- baseline / 6-week / 15-month labels;
- NEDA-4 subject-level responder status;
- batch/covariate table, especially steroid exposure, sequencing batch, and
  collection date.

### Karolinska DMF ROS cohort

The GEO record for `GSE130491` states DMF treatment in RRMS, baseline/3m/6m
sampling, CD4 T cells and CD14 monocytes, and that monocyte counts/redox state
distinguished beneficial responders from nonresponders. The public metadata
does not provide a patient-level response-label mapping suitable for the frozen
harness. It is therefore a label request, not a ready validation cohort.

Required request:

- beneficial-response/nonresponder labels mapped to patient IDs;
- which expression samples belong to the transcriptomic subcohort;
- exact treatment-relative sampling times;
- batch/covariate metadata.

### GSE228330

`GSE228330` is new to the validation-scout inventory. The GEO record verifies
PBMC transcriptome profiling around anti-CD20 therapy in MS, with ocrelizumab
patients sampled before, 2 weeks, and 6 months after first infusion. It also
includes untreated and interferon-beta-treated MS groups and healthy controls.

Blocker: the GEO record does not provide response/remission/NEDA labels, so it
cannot validate the V22 response rule. It may still be useful for:

- testing whether the frozen V22 module genes are stable under anti-CD20
  pharmacodynamic shifts;
- exercising V42/V43 batch and timepoint diagnostics on an open longitudinal
  PBMC expression dataset;
- designing an ocrelizumab-specific future request if clinical outcomes can be
  linked elsewhere.

### GSE85034 Methotrexate Arm

V24 already verified this as the only immediately usable Tier 1 fresh labeled
subgroup, but it is not primary validation: psoriasis lesional skin, week 16,
same study source as the adalimumab arm already used, and outside the MS/DMF
early-monitoring target.

Use only as an explicitly caveated secondary stress test after a separate
pre-registration permits same-study, non-MS, late-tissue stress tests.

## What V44 Changes Relative To V24

V44 does **not** change the primary conclusion. It adds three durable updates:

1. Search coverage is now more auditable: NCBI GEO/PubMed/SRA, Europe PMC,
   BioStudies/ArrayExpress, Zenodo, Figshare, Dryad, plus exact API blockers for
   ENA/OSF are recorded in machine-readable files.
2. `GSE228330` is added as an open pharmacodynamic/context cohort. It does not
   solve validation because response labels are missing.
3. The V43 power result makes the acquisition priority sharper: a small Gafson
   validation may still be inconclusive, so the Karolinska label request should
   be pursued in parallel rather than after Gafson.

## Direct Medical-Team Answer

Is the project dependent on a single cohort?

For **primary validation**, yes for now: Gafson remains the only identified
near-ideal MS DMF paired transcriptomic response cohort. It is not public-ready,
and V43 shows it may be underpowered.

Can single-cohort dependence be reduced now?

Partially:

1. request Gafson data;
2. request Karolinska `GSE130478/GSE130491/GSE130494` response labels in
   parallel;
3. use `GSE228330` as open pharmacodynamic/batch-context material, not response
   validation;
4. reserve `GSE85034_MTX` as a caveated secondary stress test only.

## Next Actions

1. Send the Gafson request package from `docs/validation/GAFSON_DATA_REQUEST_V36.md`.
2. Send a second request to the Karolinska/GEO contact for patient-level
   beneficial-response labels and expression sample mapping.
3. Add `GSE228330` to the local open-data acquisition queue for
   pharmacodynamic and batch-diagnostic harness testing only.
4. Continue V44 with Workstream 2: blind batch-diagnostic hardening, because
   V43 showed response-correlated batch effects can produce null pass rates up
   to `0.40`.

