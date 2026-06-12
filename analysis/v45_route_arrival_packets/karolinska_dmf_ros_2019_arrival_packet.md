# Arrival Command Packet: karolinska_dmf_ros_2019

Status: route-specific operational packet. No scoring is authorized until
all required gates pass.

Role: `secondary_MS_DMF_label_path`
Access tier: `Tier1_open_data_plus_Tier2_labels`
Current blocker: `labels_and_subject_map_absent_publicly`

## Hard Stop

Do not run module scoring, response metrics, or interpretation before the
route-specific receipt, checksum, terms, preflight, subject-map, label, and
addendum gates pass.

## First Actions

1. Place received files under `data/raw_v3/karolinska_dmf_ros_2019/` and quarantine/staging under `data/quarantine/karolinska_dmf_ros_2019/`.
2. Capture non-sensitive data-use terms.
3. Write and verify checksums before opening analysis paths.
4. Run intake preflight:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check --root data/quarantine/karolinska_dmf_ros_2019 --mode primary --metadata data/quarantine/karolinska_dmf_ros_2019/metadata/sample_metadata.tsv --expression data/quarantine/karolinska_dmf_ros_2019/processed/expression.tsv --outdir analysis/intake_preflight/karolinska_dmf_ros_2019 --write-checksums
```

5. Run subject-map sanity if paired deltas or subject matching are required:

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check --metadata data/quarantine/karolinska_dmf_ros_2019/metadata/sample_metadata.tsv --outdir analysis/subject_map_sanity/karolinska_dmf_ros_2019 --min-paired-subjects 2 --fail-on-error
```

6. Before outcome scoring, finalize the Karolinska preregistration
   addendum blind to module scores and performance.
7. Only then run the secondary harness path declared in the addendum.
