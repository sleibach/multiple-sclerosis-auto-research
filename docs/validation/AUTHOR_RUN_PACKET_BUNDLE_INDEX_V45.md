# Author-Run Packet Bundle Index V45

Status: collaborator packet index. No external data are included and no
validation has been run.

Purpose: define the exact committed, non-sensitive files that can be bundled for
a collaborator who cannot transfer individual-level expression or clinical data
but can run the frozen V22/V42 harness locally and return aggregate outputs.

Machine-readable index:

`analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv`

## When To Use This Packet

Use this path when an author or data controller says individual-level data
cannot leave their institution, but they are willing to run a frozen script and
return non-sensitive aggregate outputs.

Ready-to-send fallback request text:

`docs/validation/outbound_requests/author_run_fallback_ready_to_send_V45.md`

This packet is a fallback acquisition route. It does not change:

- `docs/locked_rules/LOCKED_RULE_V22.md`;
- `docs/validation/PREREGISTRATION_V42.md`;
- the V42 success/failure/inconclusive thresholds;
- the V42 outcome-interpretation grid.

## Packet Sections

| Section | Purpose |
|---|---|
| protocol | immutable rule, preregistration, and interpretation grid |
| operator README | human instructions for running and returning outputs |
| schemas | input/output formats, label dictionary, metadata/confounder dictionaries, redaction |
| scripts | frozen local commands to run |
| integrity | hash baseline and audit docs |
| reporting | required aggregate result templates |
| exclude | files that must not be sent |

## Required Send List

At minimum, include:

- `docs/locked_rules/LOCKED_RULE_V22.md`
- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/AUTHOR_RUN_FROZEN_HARNESS_PACKET_V45.md`
- `docs/validation/AUTHOR_RUN_MINIMUM_OUTPUT_SPEC_V45.md`
- `docs/validation/VALIDATION_HARNESS_README_V45.md`
- `docs/validation/MODULE_COVERAGE_PRECHECK_V45.md`
- `docs/validation/VALIDATION_RESULT_REPORT_TEMPLATE_V45.md`
- `docs/validation/SENSITIVE_DATA_REDACTION_CHECKLIST_V45.md`
- `docs/validation/VALIDATION_HANDOFF_BUNDLE_TEMPLATE_V45.md`
- `docs/validation/HANDOFF_COMPLETENESS_CHECK_V45.md`
- the primary input schemas under `docs/validation/input_schemas/`
- `scripts/v42_gafson_validation_harness.py`
- `scripts/v45_module_coverage_precheck.py`
- `scripts/v45_locked_artifact_hash_audit.py`
- `docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv`

## Collaborator Command Sequence

The collaborator should run, in order:

1. Prepare local expression and metadata files to match the supplied schemas.
2. Complete the outcome-label dictionary locally before scoring.
3. Run the module-coverage precheck:

```bash
.venv/bin/python scripts/v45_module_coverage_precheck.py check \
  --expression <local_expression.tsv> \
  --outdir <local_gate_output_dir>/module_coverage \
  --fail-on-error
```

4. If module coverage passes, run the frozen primary harness:

```bash
.venv/bin/python scripts/v42_gafson_validation_harness.py run \
  --expression <local_expression.tsv> \
  --metadata <local_sample_metadata.tsv> \
  --outdir <local_output_dir> \
  --expression-type auto
```

5. Return only the aggregate output package specified in
   `docs/validation/AUTHOR_RUN_MINIMUM_OUTPUT_SPEC_V45.md`.
6. Internally, check the returned package with
   `docs/validation/AUTHOR_RUN_OUTPUT_COMPLETENESS_CHECK_V45.md` before any
   result-report wording.

## Required Return Boundary

Return:

- frozen harness output tables and JSON summaries;
- aggregate attrition/group-size counts;
- module-coverage summary;
- confounder and batch diagnostic summaries;
- exact commands run and software/version notes;
- completed validation result report template if possible.

Do not return unless permitted by terms:

- raw expression matrices;
- individual-level clinical labels;
- private sample IDs or patient IDs;
- signed data-use agreements;
- screenshots containing private data;
- credentials or API keys.

## Internal Receipt Handling

When an author-run aggregate package returns:

1. record it in the received-data triage board as `author_run_aggregate`;
2. checksum the received aggregate files;
3. verify the returned command and hash evidence;
4. run or mirror `scripts/v45_handoff_completeness_check.py` against the returned
   bundle lifecycle state;
5. interpret only through the V42 outcome grid.

If the returned outputs are incomplete, classify the package as unscoreable or
blocked using `docs/validation/PREFLIGHT_FAILURE_TAXONOMY_V45.md`. Do not infer
missing metrics from prose.
