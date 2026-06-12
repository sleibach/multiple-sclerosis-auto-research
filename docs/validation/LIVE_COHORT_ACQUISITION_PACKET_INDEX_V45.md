# V45 Live-Cohort Acquisition Packet Index

## Purpose

This index connects every active validation/acquisition path to its request
packet, blocker, intended storage path, preflight command, and harness gate. It
reduces dependence on a single delayed Gafson transfer by making Gafson,
Karolinska, and GSE228330 operationally actionable without reopening discovery
or changing any locked rule.

Machine-readable index:

`analysis/v45_live_cohort_acquisition_index/live_cohort_acquisition_index.tsv`

## Operating Rule

No received cohort enters module scoring until all applicable intake gates pass:

1. files are placed in the specified raw/quarantine location;
2. checksums are written and audited;
3. metadata schema preflight passes;
4. longitudinal subject map sanity check passes when paired deltas are needed;
5. the cohort-specific preregistration/addendum is committed before any outcome
   label is scored;
6. the frozen harness is run mechanically, with no V22 rule edit and no
   threshold change.

## Active Cohort Paths

| Cohort | Role | Current status | Blocking item | Request packet |
|---|---|---|---|---|
| Gafson et al. 2018 DMF PBMC RNA-seq | best primary V22/V42 validation target | ready-to-send request | data not local: expression, sample map, NEDA-4 labels, covariates | `docs/validation/outbound_requests/gafson_dmf_ready_to_send_V45.md` |
| Karolinska DMF ROS / `GSE130478/GSE130491/GSE130494` | parallel secondary MS DMF path | ready-to-send label/map request | beneficial-response labels and GSM-to-patient/timepoint map absent from public GEO | `docs/validation/outbound_requests/karolinska_dmf_ready_to_send_V45.md` |
| `GSE228330` ocrelizumab PBMC | open anti-CD20 pharmacodynamic context; optional label request | public metadata audited, raw data reachable, no outcome labels | processed expression and verified subject map absent; response labels absent | `docs/validation/outbound_requests/gse228330_ocrelizumab_ready_to_send_V45.md` |

## Gafson DMF

Primary request artifact:

- `docs/validation/GAFSON_DATA_REQUEST_V36.md`
- `docs/validation/outbound_requests/gafson_dmf_ready_to_send_V45.md`

Expected receipt path:

- `data/raw_v3/gafson_dmf_2018/`
- use a quarantine mirror such as `data/quarantine/gafson_dmf_2018/` for
  preflight before frozen harness execution.

Required fields/files:

- expression matrix for baseline and early on-treatment PBMC samples;
- sample-to-patient map;
- NEDA-4 responder/nonresponder status and definition;
- timepoint labels;
- gene identifiers;
- batch/QC, steroid, cell-composition, and clinical covariates where available.

Preflight command template:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/gafson_dmf_2018 \
  --mode primary \
  --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv \
  --expression data/quarantine/gafson_dmf_2018/processed/expression.tsv \
  --outdir analysis/intake_preflight/gafson_dmf_2018 \
  --write-checksums
```

Subject-map sanity command:

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check \
  --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv \
  --outdir analysis/subject_map_sanity/gafson_dmf_2018 \
  --min-paired-subjects 2 \
  --fail-on-error
```

Harness gate:

- only after `PREREGISTRATION_V42.md`, intake preflight, and subject-map sanity
  all pass;
- run the frozen V42/Gafson harness exactly as documented in
  `docs/validation/VALIDATION_HARNESS_README_V45.md`;
- do not alter `LOCKED_RULE_V22.md` or any V42 threshold.

## Karolinska DMF

Primary request artifacts:

- `docs/validation/KAROLINSKA_DMF_LABEL_REQUEST_V45.md`
- `docs/validation/outbound_requests/karolinska_dmf_ready_to_send_V45.md`
- `docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md`

Expected receipt path:

- `data/raw_v3/karolinska_dmf_ros_2019/`
- use a quarantine mirror such as `data/quarantine/karolinska_dmf_ros_2019/`
  for intake before scoring.

Required fields/files:

- patient-level beneficial-response labels for the expression-paired subjects;
- GSM-to-patient/timepoint/cell-type/platform map;
- exact outcome definition and cutoff;
- array batch/date/file, processing date, RNA quality, and QC;
- ROS and monocyte metadata if shareable.

Preflight command template:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/karolinska_dmf_ros_2019 \
  --mode primary \
  --metadata data/quarantine/karolinska_dmf_ros_2019/metadata/sample_metadata.tsv \
  --expression data/quarantine/karolinska_dmf_ros_2019/processed/expression.tsv \
  --outdir analysis/intake_preflight/karolinska_dmf_ros_2019 \
  --write-checksums
```

Subject-map sanity command:

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check \
  --metadata data/quarantine/karolinska_dmf_ros_2019/metadata/sample_metadata.tsv \
  --outdir analysis/subject_map_sanity/karolinska_dmf_ros_2019 \
  --min-paired-subjects 2 \
  --fail-on-error
```

Harness gate:

- finalize a Karolinska-specific preregistration addendum first, blind to module
  scores and outcome performance;
- treat Karolinska as a secondary late-timepoint/platform stress test unless
  unexpectedly comparable early PBMC data are received;
- do not score outcomes until the addendum, intake preflight, and subject-map
  sanity all pass.

## GSE228330 Ocrelizumab

Primary artifacts:

- `docs/validation/GSE228330_OUTCOME_SCOUT_V45.md`
- `docs/validation/GSE228330_PHARMACODYNAMIC_RUNBOOK_V45.md`
- `docs/validation/outbound_requests/gse228330_ocrelizumab_ready_to_send_V45.md`

Current public status:

- open PBMC ocrelizumab longitudinal data are reachable;
- public annotation/probe table resolves;
- raw archive resolves but requires array reprocessing;
- the draft subject map is explicitly `inferred_unverified`;
- no sample-mapped response/NEDA/relapse/EDSS-change labels are public.

Current subject-map audit command:

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check \
  --metadata analysis/v45_gse228330_pharmacodynamic_runbook/gse228330_draft_pharmacodynamic_metadata_unverified.tsv \
  --outdir analysis/subject_map_sanity/gse228330_public_draft \
  --min-paired-subjects 2
```

Expected result for the current public draft: `FAIL`. That failure is a guardrail,
not a biological result.

If processed expression and a verified subject map are obtained, run context-only
preflight:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/gse228330_ocrelizumab \
  --mode pharmacodynamic \
  --metadata data/quarantine/gse228330_ocrelizumab/metadata/sample_metadata.tsv \
  --expression data/quarantine/gse228330_ocrelizumab/processed/expression.tsv \
  --outdir analysis/intake_preflight/gse228330_ocrelizumab \
  --write-checksums
```

Harness gate:

- if no response labels are received, run only the pharmacodynamic-only context
  harness from `PHARMACODYNAMIC_ONLY_HARNESS_V45.md`;
- if response labels are received, write a cohort-specific preregistration
  addendum before scoring any outcome;
- never use the current inferred public-order draft for paired-delta validation.

## Handoff Checklist

For each cohort after human send action:

1. Save the exact sent email as
   `docs/validation/outbound_requests/<cohort>_sent_YYYY-MM-DD.md`.
2. Update `analysis/v45_outbound_data_requests/request_tracker.tsv`.
3. Place received data under the specified raw/quarantine path.
4. Run intake preflight and subject-map sanity before any harness.
5. Commit a cohort-specific preregistration addendum if the cohort is not the
   exact V42 primary Gafson test.
6. Run only the matching frozen harness.

## Status

This artifact is operational and additive. It does not alter any locked rule,
pre-registration threshold, or validation outcome interpretation.
