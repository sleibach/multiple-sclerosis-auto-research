# Progression P1 Core Package Request V54

Status: ready-to-send generic draft. Replace recipient and sender placeholders;
save the exact sent text separately. This request does **not** assert that any
field exists or that a returned package will be eligible.

Subject: `Request for de-identified longitudinal MS molecular and confirmed-disability data package`

## Email Body

```text
Dear [study team / data custodian],

We are preparing a fully pre-specified analysis of whether a molecular state
measured before or during follow-up is associated with confirmed disability
accumulation in multiple sclerosis. To avoid post-hoc endpoint construction, we
need the raw linkage and adjudication fields rather than a response label alone.

Could you provide, where collected and shareable, a de-identified package with:

1. Linkage and molecular data
   - stable pseudonymous subject, sample, and visit identifiers;
   - sample collection date or study day, compartment/cell type, disease course;
   - expression matrix, scale/normalization description, feature annotation and
     identifier version;
   - collection site, processing batch, platform, sample QC, and cell counts.

2. Repeated disability and endpoint construction
   - raw EDSS values and dates plus T25FW/9HPT where collected;
   - the exact CDP and/or PIRA protocol definition and confirmation interval;
   - candidate worsening date, confirmation date, confirmation status, and the
     reason a candidate event was not confirmed;
   - whether outcome assessors were blinded to molecular measurements.

3. Follow-up and clinical context
   - every expected and observed visit, attendance status/reason, last-observed
     date, censoring date/reason, and death date/cause where applicable;
   - relapse onset/recovery, corticosteroid and infection dates;
   - complete DMT start/stop/dose history and treatment-switch reason;
   - MRI activity and paramagnetic-rim/slowly-expanding lesion fields where
     collected.

4. Package provenance
   - data dictionary, protocol/version references, file manifest, data-use
     terms, and SHA-256 checksums.

Please include all eligible participants rather than selecting them by outcome
or molecular result. The attached response template permits SUPPLIED,
NOT_COLLECTED, NOT_SHAREABLE, or UNKNOWN for every requested field; an explicit
absence is preferable to imputation or inference. Dates may be represented as
consistently shifted study days if required for de-identification, provided all
within-subject intervals remain valid and the transformation is documented.

We will quarantine the returned package, verify identifiers and terms, and
freeze the cohort-specific endpoint, censoring, treatment-switch, site, and
power plan before any molecular score is viewed. Receipt does not imply that
the package is powered or eligible, and no derived progression label will be
reconstructed from relapse, disease stage, or lesion morphology alone.

Kind regards,

[Name / affiliation]
```

## Response Attachment

Ask the provider to complete:

`docs/validation/input_schemas/V54_progression_p1_request_response_template.tsv`

Allowed `provider_status` values are `SUPPLIED`, `NOT_COLLECTED`,
`NOT_SHAREABLE`, and `UNKNOWN`. Placeholders are not treated as supplied. The
template covers all P1/all-role fields in the canonical acquisition contract,
the five immediate acquisition bundles, and endpoint-confirmation provenance.

## Internal Receipt Rule

On return, preserve original files and terms, checksum before transformation,
and quarantine before opening expression values. Run the existing package,
endpoint-semantic, event-time, site-score, treatment-switch, feasibility, and
information gates. Missing gate-critical fields fail closed; contextual fields
marked absent remain reported as absent. No real package is currently assumed
eligible.

Traceability bundle IDs:

- `p1_longitudinal_disability_link`
- `attendance_censoring_provenance`
- `site_batch_scale_identity`
- `balanced_event_yield`
- `pira_treatment_activity_context`
