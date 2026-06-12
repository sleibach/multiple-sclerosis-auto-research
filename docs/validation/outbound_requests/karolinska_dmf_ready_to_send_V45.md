# Karolinska DMF Label Request: Ready-To-Send Draft V45

Status: unsent draft. Send only if the medical team approves the external
contact. Save the exact sent text separately after sending.

To: Ewoud Ewing, `ewoud.ewing@ki.se`

Subject: `Request for response-label mapping for GSE130478/GSE130491 DMF MS cohort`

Attachments/references to mention if useful:

- `docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md`
- `docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md`
- `docs/validation/CLINICAL_DATA_DICTIONARY_CRF_V45.md`

## Email Body

```text
Dear Dr. Ewing and colleagues,

I am working on an independent, pre-specified validation-readiness project for
longitudinal treatment-response transcriptomic monitoring in multiple sclerosis.
Your Karolinska dimethyl fumarate cohort is one of the few public longitudinal
MS DMF datasets we identified that could provide a secondary validation or
stress-test path beyond a single PBMC RNA-seq cohort.

We have verified the public GEO records for GSE130494, GSE130478, and GSE130491
and the Nature Communications paper (PMID 31300673). The expression data in
GSE130478 appear to include 14 MS patients sampled at baseline and 6 months
after DMF treatment in CD4+ T cells. The public record also states that monocyte
counts and monocytic ROS distinguished beneficial responders from
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
- clinical definition and cutoff used for that label.

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
for early PBMC response validation. We can follow any data-use conditions you
require and can work with either a small mapping table for the public GEO
samples or a fuller metadata file.

Kind regards,

[Name / affiliation]
```

## If Data Are Received

Place files under:

```text
data/raw_v3/karolinska_dmf_ros_2019/
```

Required gates before analysis:

1. preserve original filenames and terms;
2. checksum all files;
3. finalize a Karolinska-specific preregistration addendum before module
   scoring, because platform/timepoint/cell type differ from Gafson;
4. run intake preflight;
5. treat the result as secondary unless the blinded addendum explicitly
   justifies a stronger role.
