# Karolinska DMF Label Request Package V45

Date: 2026-06-12

Status: data-access preparation. This is not a validation analysis and does not
change any locked rule or preregistration.

## Why This Matters

V43 showed that a Gafson-sized cohort may be inconclusive, and V44 found no
fresh public ready-to-run Tier 1 primary validation cohort. The best parallel
low-barrier MS cohort is the Karolinska DMF ROS cohort:

- SuperSeries: `GSE130494`
- Expression subseries: `GSE130478`
- Methylation subseries: `GSE130491`
- Publication: PMID `31300673`, DOI `10.1038/s41467-019-11139-3`

The public data are not enough for validation because patient-level
beneficial-response labels and GSM-to-patient/timepoint mapping are not exposed
in the GEO metadata. V45 converts that blocker into a concrete request package.

## Verified Public Metadata

Machine-readable verification:

- `scripts/v45_karolinska_access_package.py`
- `analysis/v45_karolinska_access/karolinska_geo_series_summary.tsv`
- `analysis/v45_karolinska_access/karolinska_pubmed_summary.json`
- `analysis/v45_karolinska_access/karolinska_request_checklist.tsv`
- raw public GEO text snapshots:
  `analysis/v45_karolinska_access/raw_public_metadata/`

Verified fields from current public records:

| Accession | Role | Public status | Design | Samples | Contact |
|---|---|---|---|---:|---|
| `GSE130494` | SuperSeries | Public on 2019-07-31 | expression + methylation subseries | `110` | Ewoud Ewing, `ewoud.ewing@ki.se` |
| `GSE130478` | Expression | Public on 2019-07-31 | 14 MS patients, baseline/6 months after DMF, CD4+ T cells | `28` | Ewoud Ewing, `ewoud.ewing@ki.se` |
| `GSE130491` | Methylation | Public on 2019-07-31 | 19 MS patients, baseline/3m/6m after DMF, CD4+ T cells and CD14+ monocytes | `82` | Ewoud Ewing, `ewoud.ewing@ki.se` |

The expression series is public, but the labels and sample mapping needed for a
frozen response-rule test are not public in the GEO metadata.

## Validation Role

This cohort is a **secondary MS DMF validation / stress-test path**, not a
drop-in replacement for Gafson.

Reasons:

- the transcriptomic expression data are CD4+ T-cell array data, not PBMC RNA-seq;
- the expression timepoints are baseline and 6 months, not baseline and early
  6-week treatment;
- the project needs a response label definition and sample-level mapping before
  any frozen analysis can run.

If labels are obtained, the correct role is:

1. secondary DMF MS validation of directionality / effect-size consistency;
2. sensitivity to later-treatment transcriptomic timing;
3. bridge between the V22 APC/HLA-II rule and the Karolinska monocyte/ROS
   response biology;
4. not a primary clean validation unless a preregistered interpretation grid
   explicitly handles the platform/timepoint differences.

## Minimum Data To Request

| Priority | Needed item | Minimum acceptable |
|---:|---|---|
| 1 | patient-level beneficial-response labels | one response label per patient ID for the 14 `GSE130478` expression-paired subjects |
| 2 | GSM-to-patient/timepoint/cell-type map | `GSM`, `patient_id`, `timepoint`, `cell_type`, `platform` for all `GSE130478` samples |
| 3 | clinical outcome definition | the exact beneficial-response/nonresponder definition used in PMID `31300673`, including cutoffs |
| 4 | technical covariates | array batch/date/file, processing date, RNA quality or other available QC |
| 5 | monocyte count / ROS mapping | patient-level monocyte count and ROS summaries with timepoints, if shareable |

If the authors can share more, useful optional fields are:

- age, sex, disease duration, baseline disease activity, prior DMT;
- relapse/MRI/disability components if available;
- steroid exposure around each blood draw;
- blood counts or sorted-cell purity measures;
- NOX3 genotype / variant call used in the paper, if sample-level sharing is
  allowed.

## Suggested Email

Subject:

`Request for response-label mapping for GSE130478/GSE130491 DMF MS cohort`

Body:

```text
Dear Dr. Ewing and colleagues,

I am working on an independent, pre-specified validation of an early
treatment-response transcriptomic monitoring signal in multiple sclerosis. Your
Karolinska dimethyl fumarate cohort is one of the few public longitudinal MS DMF
datasets we have identified that could provide a secondary validation or
stress-test path beyond a single PBMC RNA-seq cohort.

We have verified the public GEO records for GSE130494, GSE130478, and GSE130491
and the Nature Communications paper (PMID 31300673). The expression data in
GSE130478 appear to include 14 MS patients sampled at baseline and 6 months
after DMF treatment in CD4+ T cells. The public record also states that
monocyte counts and monocytic ROS distinguished beneficial responders from
non-responders, but we could not find the patient-level response-label mapping
or the exact GSM-to-patient/timepoint map in the public GEO metadata.

Would you be willing to share the sample-level mapping needed to interpret the
public expression data?

The minimum useful fields would be:

- GSM accession;
- patient ID or pseudonymous subject ID;
- timepoint (baseline / 6 months, and 3 months where applicable);
- cell type;
- beneficial-response / nonresponder label;
- the clinical definition and cutoff used for that label.

If available, these additional fields would make the validation more
interpretable:

- array batch, processing date, RNA quality, or other technical QC fields;
- monocyte counts and ROS measurements by patient/timepoint;
- steroid exposure near sampling;
- age, sex, disease duration, prior DMT, and baseline disease activity;
- NOX3 genotype or variant call used in the publication, if shareable.

We would use the data only under a frozen, no-refitting analysis plan. Because
GSE130478 is CD4+ T-cell expression at baseline and 6 months, we would treat it
as a secondary DMF validation/stress-test rather than as a primary replacement
for early PBMC response validation.

We can follow any data-use conditions you require and can work with either a
small mapping table for the public GEO samples or a fuller metadata file.

Kind regards,

[Name / affiliation]
```

## Human Execution Steps

1. Send the email above to `ewoud.ewing@ki.se`.
2. If no response after 10 business days, send a brief follow-up and optionally
   include the corresponding/senior authors from PMID `31300673`.
3. If data are shared, place files under:

   `data/raw_v3/karolinska_dmf_ros_2019/`

4. Preserve the original filenames and add:

   - `README_source.txt`
   - `data_use_terms.txt` if provided
   - `received_files_manifest.tsv`

5. Before opening for analysis, quarantine and checksum:

   ```bash
   find data/raw_v3/karolinska_dmf_ros_2019 -type f -maxdepth 1 -print0 \
     | sort -z \
     | xargs -0 shasum -a 256 \
     > data/raw_v3/karolinska_dmf_ros_2019/SHA256SUMS
   ```

6. Update `data/manifest.tsv` and do **not** run analysis until a Karolinska-
   specific preregistered interpretation grid is written, because platform and
   timing differ from Gafson/V42.

## Pre-Analysis Gate Once Data Arrive

Before any module score is computed, verify:

- `GSE130478` expression samples can be paired within subject;
- response labels map to all or most paired expression subjects;
- the response-label definition is fixed before analysis;
- module-gene coverage is sufficient on `GPL17692`;
- technical covariates are present or explicitly absent;
- the interpretation plan treats this as secondary and later-timepoint, not
  primary early PBMC validation.

If these gates fail, the cohort remains pharmacodynamic/context material only.

