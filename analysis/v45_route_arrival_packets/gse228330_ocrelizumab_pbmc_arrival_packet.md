# Arrival Command Packet: gse228330_ocrelizumab_pbmc

Status: route-specific operational packet. No scoring is authorized until
all required gates pass.

Role: `open_anti_cd20_pharmacodynamic_context_optional_label_request`
Access tier: `Tier1_open_data_optional_author_labels`
Current blocker: `public_response_labels_absent_and_subject_map_unverified`

## Hard Stop

Do not run module scoring, response metrics, or interpretation before the
route-specific receipt, checksum, terms, preflight, subject-map, label, and
addendum gates pass.

## First Actions

1. Place received files under `data/raw_v3/gse228330_ocrelizumab_outcomes/` and quarantine/staging under `data/quarantine/gse228330_ocrelizumab/`.
2. Capture non-sensitive data-use terms.
3. Write and verify checksums before opening analysis paths.
4. Run intake preflight:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check --root data/quarantine/gse228330_ocrelizumab --mode pharmacodynamic --metadata data/quarantine/gse228330_ocrelizumab/metadata/sample_metadata.tsv --expression data/quarantine/gse228330_ocrelizumab/processed/expression.tsv --outdir analysis/intake_preflight/gse228330_ocrelizumab --write-checksums
```

5. Run subject-map sanity if paired deltas or subject matching are required:

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check --metadata analysis/v45_gse228330_pharmacodynamic_runbook/gse228330_draft_pharmacodynamic_metadata_unverified.tsv --outdir analysis/subject_map_sanity/gse228330_public_draft --min-paired-subjects 2
```

6. Treat the route as pharmacodynamic/context-only unless outcome labels
   and a cohort-specific addendum are received and frozen first.
7. Do not use GSE228330 as response validation without that addendum.
