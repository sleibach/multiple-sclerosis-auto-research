# Arrival Command Packet: gafson_dmf_2018

Status: route-specific operational packet. No scoring is authorized until
all required gates pass.

Role: `primary_V22_V42_validation`
Access tier: `Tier2_low_barrier`
Current blocker: `data_not_local`

## Hard Stop

Do not run module scoring, response metrics, or interpretation before the
route-specific receipt, checksum, terms, preflight, subject-map, label, and
addendum gates pass.

## First Actions

1. Place received files under `data/raw_v3/gafson_dmf_2018/` and quarantine/staging under `data/quarantine/gafson_dmf_2018/`.
2. Capture non-sensitive data-use terms.
3. Write and verify checksums before opening analysis paths.
4. Run intake preflight:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check --root data/quarantine/gafson_dmf_2018 --mode primary --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv --expression data/quarantine/gafson_dmf_2018/processed/expression.tsv --outdir analysis/intake_preflight/gafson_dmf_2018 --write-checksums
```

5. Run subject-map sanity if paired deltas or subject matching are required:

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv --outdir analysis/subject_map_sanity/gafson_dmf_2018 --min-paired-subjects 2 --fail-on-error
```

6. If all V42/Gafson gates pass, run only the frozen V42 primary harness.
7. Interpret only under the V42 outcome grid.
