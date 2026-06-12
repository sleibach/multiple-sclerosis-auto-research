# V45 Validation Command Plan: gse228330_ocrelizumab

Mode: `pharmacodynamic`
Root: `data/quarantine/gse228330_ocrelizumab`

| Step | Gate | Required | Expected pass condition |
|---:|---|---:|---|
| 1 | `data_use_terms` | True | status=approved_for_preflight |
| 2 | `checksum_manifest` | True | manifest_audit_summary.json overall_status=PASS |
| 3 | `response_column_audit` | True | no response-like columns for pharmacodynamic-only mode |
| 4 | `intake_preflight` | True | preflight_summary.json overall_status=PASS |
| 5 | `subject_map_sanity` | True | subject_map_summary.json overall_status=PASS |
| 6 | `preregistration_or_addendum` | True | committed preregistration/addendum exists; no rule or threshold edits |
| 7 | `frozen_harness_handoff` | False | execute only the matching frozen harness documented in VALIDATION_HARNESS_README_V45.md |

## Commands

### Step 1: data_use_terms

```bash
Fill docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv and save non-sensitive summary under data/quarantine/gse228330_ocrelizumab/governance/data_use_terms_summary.tsv
```

### Step 2: checksum_manifest

```bash
.venv/bin/python scripts/v45_checksum_manifest_validator.py verify --root data/quarantine/gse228330_ocrelizumab --manifest data/quarantine/gse228330_ocrelizumab/SHA256_MANIFEST.tsv --outdir analysis/validation_command_runs/checksum_manifest/gse228330_ocrelizumab --fail-on-error
```

### Step 3: response_column_audit

```bash
.venv/bin/python scripts/v45_response_column_audit.py audit --metadata data/quarantine/gse228330_ocrelizumab/metadata/sample_metadata.tsv --outdir analysis/validation_command_runs/response_column_audit/gse228330_ocrelizumab --fail-on-response-like
```

### Step 4: intake_preflight

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check --root data/quarantine/gse228330_ocrelizumab --mode pharmacodynamic --metadata data/quarantine/gse228330_ocrelizumab/metadata/sample_metadata.tsv --expression data/quarantine/gse228330_ocrelizumab/processed/expression.tsv --outdir analysis/validation_command_runs/intake_preflight/gse228330_ocrelizumab --write-checksums
```

### Step 5: subject_map_sanity

```bash
.venv/bin/python scripts/v45_subject_map_sanity_check.py check --metadata data/quarantine/gse228330_ocrelizumab/metadata/sample_metadata.tsv --outdir analysis/validation_command_runs/subject_map_sanity/gse228330_ocrelizumab --min-paired-subjects 2 --fail-on-error
```

### Step 6: preregistration_or_addendum

```bash
Confirm the applicable frozen preregistration/addendum is already committed and matches this cohort role before scoring outcomes.
```

### Step 7: frozen_harness_handoff

```bash
Run pharmacodynamic-only context harness; no response-validation claim.
```
