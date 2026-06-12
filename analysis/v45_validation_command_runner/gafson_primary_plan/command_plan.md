# V45 Validation Command Plan: gafson_dmf_2018

Mode: `primary`
Root: `data/quarantine/gafson_dmf_2018`

| Step | Gate | Required | Expected pass condition |
|---:|---|---:|---|
| 1 | `data_use_terms` | True | status=approved_for_preflight |
| 2 | `checksum_manifest` | True | manifest_audit_summary.json overall_status=PASS |
| 3 | `intake_preflight` | True | preflight_summary.json overall_status=PASS |
| 4 | `subject_map_sanity` | True | subject_map_summary.json overall_status=PASS |
| 5 | `preregistration_or_addendum` | True | committed preregistration/addendum exists; no rule or threshold edits |
| 6 | `frozen_harness_handoff` | False | execute only the matching frozen harness documented in VALIDATION_HARNESS_README_V45.md |

## Commands

### Step 1: data_use_terms

```bash
Fill docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv and save non-sensitive summary under data/quarantine/gafson_dmf_2018/governance/data_use_terms_summary.tsv
```

### Step 2: checksum_manifest

```bash
.venv/bin/python scripts/v45_checksum_manifest_validator.py verify --root data/quarantine/gafson_dmf_2018 --manifest data/quarantine/gafson_dmf_2018/SHA256_MANIFEST.tsv --outdir analysis/validation_command_runs/checksum_manifest/gafson_dmf_2018 --fail-on-error
```

### Step 3: intake_preflight

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check --root data/quarantine/gafson_dmf_2018 --mode primary --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv --expression data/quarantine/gafson_dmf_2018/processed/expression.tsv --outdir analysis/validation_command_runs/intake_preflight/gafson_dmf_2018 --write-checksums
```

### Step 4: subject_map_sanity

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv --outdir analysis/validation_command_runs/subject_map_sanity/gafson_dmf_2018 --min-paired-subjects 2 --fail-on-error
```

### Step 5: preregistration_or_addendum

```bash
Confirm the applicable frozen preregistration/addendum is already committed and matches this cohort role before scoring outcomes.
```

### Step 6: frozen_harness_handoff

```bash
Run V42 frozen primary harness only after preregistration, preflight, and subject-map sanity pass.
```
