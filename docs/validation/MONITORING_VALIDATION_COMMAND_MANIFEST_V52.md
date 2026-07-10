# Monitoring Validation Command Manifest V52

Date: 2026-07-10

Status: operator command manifest. This document adds no analysis and changes no
validation rule. It restates the exact command order for a future complete
Gafson/Karolinska-style monitoring package, using the V45 runbook and V52
therapeutic framing.

## Interpreter Precheck

Use the repo virtual environment that imports the harness dependencies:

```bash
.venv/bin/python -c 'import numpy, pandas; print("venv_numpy_pandas_ok")'
```

V52 check result while writing this manifest: `.venv/bin/python` imported
`numpy` and `pandas` successfully. The default shell `python3` in this
environment did not, so operators should not substitute it without checking.

## Package Paths

Use a quarantined package path before any scoring:

```text
data/quarantine/<cohort_id>/
  raw/
  processed/expression.tsv
  metadata/sample_metadata.tsv
  metadata/outcome_label_dictionary.tsv
  governance/data_use_terms_summary.tsv
  SHA256_MANIFEST.tsv
```

Replace `<cohort_id>` with `gafson_dmf_2018`, `karolinska_dmf`, or another
stable cohort identifier. Do not commit private raw data or restricted terms.

## Command Order

| order | gate | command template | stop condition |
|---:|---|---|---|
| 0 | interpreter | `.venv/bin/python -c 'import numpy, pandas; print("venv_numpy_pandas_ok")'` | stop if dependencies fail |
| 1 | receipt/quarantine | record path, file sizes, checksums, and access terms in the local receipt log | stop if receipt is not auditable |
| 2 | checksum manifest | `.venv/bin/python scripts/v45_checksum_manifest_validator.py verify --root data/quarantine/<cohort_id> --manifest data/quarantine/<cohort_id>/SHA256_MANIFEST.tsv --outdir analysis/validation_command_runs/checksum_manifest/<cohort_id> --fail-on-error` | stop if checksum audit fails |
| 3 | outcome dictionary | validate `metadata/outcome_label_dictionary.tsv` with the V45 outcome dictionary validator | stop if NEDA/equivalent orientation or window is ambiguous |
| 4 | intake preflight | `.venv/bin/python scripts/v45_validation_intake_preflight.py check --root data/quarantine/<cohort_id> --mode primary --metadata data/quarantine/<cohort_id>/metadata/sample_metadata.tsv --expression data/quarantine/<cohort_id>/processed/expression.tsv --outdir analysis/validation_command_runs/intake_preflight/<cohort_id> --write-checksums` | stop if schema, quarantine, sample IDs, or label guard fails |
| 5 | module coverage | `.venv/bin/python scripts/v45_module_coverage_precheck.py check --expression data/quarantine/<cohort_id>/processed/expression.tsv --outdir analysis/validation_command_runs/module_coverage/<cohort_id> --fail-on-error` | stop if V22 modules are unscoreable |
| 6 | subject map | `.venv/bin/python scripts/v45_subject_map_sanity_check.py check --metadata data/quarantine/<cohort_id>/metadata/sample_metadata.tsv --outdir analysis/validation_command_runs/subject_map_sanity/<cohort_id> --min-paired-subjects 2 --fail-on-error` | stop if baseline/early pairing is not mechanical |
| 7 | preregistration confirmation | confirm `docs/validation/PREREGISTRATION_V42.md` applies exactly | stop if cohort role differs; write any needed addendum blind before scoring |
| 8 | harness self-test | `.venv/bin/python scripts/v42_gafson_validation_harness.py synthetic-check --outdir analysis/v42_harness_validation` | stop if null/planted mechanics fail |
| 9 | frozen primary harness | `.venv/bin/python scripts/v42_gafson_validation_harness.py run --expression data/quarantine/<cohort_id>/processed/expression.tsv --metadata data/quarantine/<cohort_id>/metadata/sample_metadata.tsv --outdir analysis/validation_runs/<cohort_id> --expression-type auto` | interpret only through V42/V52 decision tree |

## Required Outputs

For a completed primary harness run, retain:

- `validation_summary.json`
- `paired_module_deltas.tsv`
- `gene_mapping_coverage.tsv`
- `sample_attrition.tsv`
- `locked_rule_metrics.tsv`
- `confounder_adjustment_metrics.tsv`
- `joint_confounder_metrics.tsv`
- `batch_diagnostic_metrics.tsv`

Also retain all preflight and gate outputs under
`analysis/validation_command_runs/`.

## Interpretation Command Is Not A Command

After Step 9, do not run alternative analyses to rescue or improve the result.
Map the output to:

- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`

The result is one of:

- `PASS_CLEAN`
- `PASS_IMMUNE_TONE_BOUNDED`
- `PASS_NON_SPECIFIC`
- `INCONCLUSIVE_UNDERPOWERED`
- `FAIL_ADEQUATE_POWER`
- `UNSCOREABLE_DATA`

## Explicit Non-Commands

Do not run:

1. score tuning;
2. feature selection;
3. endpoint substitution;
4. timepoint window changes;
5. post-hoc batch correction of the locked score;
6. structural or genetics target analyses as a substitute for monitoring
   validation.

## Source Artifacts

- `docs/validation/GAFSON_ARRIVAL_RUNBOOK_V45.md`
- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`
- `scripts/v42_gafson_validation_harness.py`
- `scripts/v45_validation_intake_preflight.py`
