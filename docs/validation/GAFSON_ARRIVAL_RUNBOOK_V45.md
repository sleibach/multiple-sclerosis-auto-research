# Gafson Arrival Runbook V45

Status: operator runbook for future received data. No Gafson data were read or
analyzed while writing this document.

Purpose: map the V45 command-runner handoff to the exact V42 preregistration
gates so a received Gafson/DMF/NEDA-4 package is handled mechanically.

Authoritative frozen documents:

- locked rule: `docs/locked_rules/LOCKED_RULE_V22.md`
- primary preregistration: `docs/validation/PREREGISTRATION_V42.md`
- outcome interpretation grid:
  `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- harness README: `docs/validation/VALIDATION_HARNESS_README_V45.md`
- command-runner checklist:
  `docs/validation/VALIDATION_COMMAND_RUNNER_V45.md`

## Non-Negotiable Operator Rules

1. Do not open or inspect expression/outcome relationships manually.
2. Do not edit the V22 locked rule, V42 preregistration, or interpretation grid.
3. Do not change endpoint, sign, timepoint window, module genes, thresholds, or
   confounder panels after seeing the data.
4. Any failed gate is an operational blocker, not a biological result.
5. If an OpenGWAS-adjacent check is unexpectedly required after
   `2026-06-19 12:28 UTC`, renew the JWT first. Expired auth is a blocker, not
   a null.

## Expected Package Layout

Place received files under:

```text
data/quarantine/gafson_dmf_2018/
  raw/
  processed/expression.tsv
  metadata/sample_metadata.tsv
  metadata/outcome_label_dictionary.tsv
  governance/data_use_terms_summary.tsv
  SHA256_MANIFEST.tsv
```

Restricted agreements, credentials, and private correspondence stay outside git.
Only non-sensitive summaries and manifests may be committed.

## Gate Map

| Order | Gate | Command/artifact | V42 preregistration section | Pass condition | If fail |
|---:|---|---|---|---|---|
| 0 | receipt log | update `docs/validation/RECEIVED_DATA_TRIAGE_STATUS_BOARD_V45.md` and local non-git receipt log | Blindness and quarantine | path, file sizes, checksums recorded before scoring | stop; complete receipt/quarantine record |
| 1 | data-use terms | fill `docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv`; save summary at `data/quarantine/gafson_dmf_2018/governance/data_use_terms_summary.tsv` | Required input package; blindness/quarantine | `status=approved_for_preflight` | stop; terms/permission blocker |
| 2 | checksum manifest | `.venv/bin/python scripts/v45_checksum_manifest_validator.py verify --root data/quarantine/gafson_dmf_2018 --manifest data/quarantine/gafson_dmf_2018/SHA256_MANIFEST.tsv --outdir analysis/validation_command_runs/checksum_manifest/gafson_dmf_2018 --fail-on-error` | Blindness and quarantine | `manifest_audit_summary.json overall_status=PASS` | stop; repair manifest or received package record |
| 3 | outcome dictionary | complete `docs/validation/input_schemas/V45_outcome_label_dictionary_template.tsv` as `metadata/outcome_label_dictionary.tsv` before scoring | Outcome mapping | NEDA-4 orientation, assessment window, missingness rules, and binary mapping frozen | stop; missing/ambiguous endpoint blocker |
| 4 | intake preflight | `.venv/bin/python scripts/v45_validation_intake_preflight.py check --root data/quarantine/gafson_dmf_2018 --mode primary --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv --expression data/quarantine/gafson_dmf_2018/processed/expression.tsv --outdir analysis/validation_command_runs/intake_preflight/gafson_dmf_2018 --write-checksums` | Required input package; subject and sample eligibility | `preflight_summary.json overall_status=PASS` | stop; schema/quarantine/sample-ID blocker |
| 5 | module coverage precheck | `.venv/bin/python scripts/v45_module_coverage_precheck.py check --expression data/quarantine/gafson_dmf_2018/processed/expression.tsv --outdir analysis/validation_command_runs/module_coverage/gafson_dmf_2018 --fail-on-error` | Expression preprocessing; frozen V22 modules | `module_coverage_precheck_summary.json overall_status=PASS` | stop; gene mapping or matrix blocker |
| 6 | subject-map sanity | `.venv/bin/python scripts/v45_subject_map_sanity_check.py check --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv --outdir analysis/validation_command_runs/subject_map_sanity/gafson_dmf_2018 --min-paired-subjects 2 --fail-on-error` | Subject and sample eligibility; early timepoint selection | `subject_map_summary.json overall_status=PASS` | stop; baseline/early pairing blocker |
| 7 | preregistration confirmation | confirm `docs/validation/PREREGISTRATION_V42.md` applies exactly and no addendum edits are needed | Frozen rule application; pass/fail criteria | committed preregistration already matches cohort role | stop; if role differs, write addendum blind before scoring |
| 8 | harness self-test | `.venv/bin/python scripts/v42_gafson_validation_harness.py synthetic-check --outdir analysis/v42_harness_validation` | Harness correctness, not a V42 biological gate | null synthetic fails; planted synthetic passes | stop; software regression blocker |
| 9 | frozen primary harness | `.venv/bin/python scripts/v42_gafson_validation_harness.py run --expression data/quarantine/gafson_dmf_2018/processed/expression.tsv --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv --outdir analysis/validation_runs/gafson_dmf_2018 --expression-type auto` | Primary metrics; confounder adjustment; batch guard | harness completes and writes all primary outputs | interpret only through V42 grid; do not rerun with altered parameters |

## Generated Command Plan

The standing command-runner can regenerate the base plan:

```bash
.venv/bin/python scripts/v45_validation_command_runner.py \
  --cohort-id gafson_dmf_2018 \
  --mode primary \
  --root data/quarantine/gafson_dmf_2018 \
  --outdir analysis/v45_validation_command_runner/gafson_primary_plan
```

Current generated base plan has six steps: data-use terms, checksum manifest,
intake preflight, subject-map sanity, preregistration confirmation, and frozen
harness handoff. This runbook adds two explicit operator gates around that base
plan: outcome-label dictionary freeze and module-coverage precheck. Item 62 in
the V45 queue will synchronize those additions into the command-runner output.

## Output Capture

After the frozen harness runs, archive these files under
`analysis/validation_runs/gafson_dmf_2018/`:

- `validation_summary.json`
- `paired_module_deltas.tsv`
- `gene_mapping_coverage.tsv`
- `sample_attrition.tsv`
- `locked_rule_metrics.tsv`
- `confounder_adjustment_metrics.tsv`
- `joint_confounder_metrics.tsv`
- `batch_diagnostic_metrics.tsv`

Also retain the gate outputs under `analysis/validation_command_runs/`.

## Interpretation Routing

Map the harness result to exactly one V42 grid class:

- `PASS_CLEAN`
- `PASS_IMMUNE_TONE_BOUNDED`
- `PASS_NON_SPECIFIC`
- `FAIL_ADEQUATE_POWER`
- `INCONCLUSIVE_UNDERPOWERED`
- `UNSCOREABLE_DATA`

Required report rule:

- raw locked-rule metrics are reported first;
- confounder and batch audits are interpretation modifiers only;
- adjusted analyses cannot turn a failed primary locked score into a pass;
- a single Gafson pass is not clinical utility and not a universal MS-DMT
  validation;
- an unscoreable package is a data-acquisition failure, not a negative biology
  result.

## Stop/Repair Decisions

| Blocker | Allowed repair before harness | Disallowed repair |
|---|---|---|
| missing checksums | request or generate manifest from received files before scoring | changing files silently after manifest verification |
| missing NEDA-4 dictionary | ask provider for label definition/orientation | reconstructing a different endpoint after seeing scores |
| expression sample mismatch | repair metadata/sample IDs from source documentation | dropping inconvenient samples based on score/outcome |
| failed module coverage | repair gene mapping under V42 rules or request processed matrix | changing module genes or lowering coverage threshold |
| failed subject-map sanity | request subject/timepoint map | inferring patient pairing from public sample order |
| batch warning | report and interpret via V42/V44 grid | batch-correcting the primary locked score post hoc |

## Ready-To-Run Criteria

The Gafson package is ready for the frozen harness only when all are true:

```text
terms approved
checksums pass
outcome dictionary frozen
intake preflight passes
module coverage precheck passes
subject-map sanity passes
V42 preregistration still applies exactly
synthetic harness self-test passes
```

Anything short of this is a named readiness blocker, not a validation result.
