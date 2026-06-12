# Author-Run Frozen Harness Packet V45

Status: collaborator execution template. No external data are included.

Purpose: define the exact packet to send when a collaborator cannot share
individual-level expression or clinical labels but can run the frozen harness
locally and return non-sensitive aggregate outputs.

Machine-readable packet checklist:

`docs/validation/input_schemas/V45_author_run_frozen_harness_packet.tsv`

## Packet Contents

Include:

- locked rule and preregistration;
- input schema and data dictionary;
- frozen harness command;
- hash baseline and integrity commands;
- result report template;
- minimum non-sensitive output list;
- redaction rules.

Do not include any API keys, private URLs, or received third-party data.

## Primary Gafson-Style Author Command

```bash
.venv/bin/python scripts/v42_gafson_validation_harness.py run \
  --expression <local_expression.tsv> \
  --metadata <local_sample_metadata.tsv> \
  --outdir <local_output_dir> \
  --expression-type auto
```

Before running, author should confirm:

```bash
.venv/bin/python scripts/v45_module_coverage_precheck.py check \
  --expression <local_expression.tsv> \
  --outdir <local_gate_output_dir>/module_coverage \
  --fail-on-error
```

## Required Returned Outputs

The author-run output is usable only if it includes enough aggregate artifacts
to fill `docs/validation/VALIDATION_RESULT_REPORT_TEMPLATE_V45.md`, including:

- `validation_summary.json`
- `sample_attrition.tsv`
- `gene_mapping_coverage.tsv`
- `locked_rule_metrics.tsv`
- `confounder_adjustment_metrics.tsv`
- `joint_confounder_metrics.tsv`
- `batch_diagnostic_metrics.tsv`
- exact command run and software/version notes

The returned output must not include raw expression or private clinical labels
unless terms explicitly permit transfer.

## Guardrail

An author-run result is not acceptable if the collaborator changes module genes,
endpoint, score sign, thresholds, early timepoint rule, or pass/fail criteria.
Any modification converts the run to exploratory and it cannot validate V22.
