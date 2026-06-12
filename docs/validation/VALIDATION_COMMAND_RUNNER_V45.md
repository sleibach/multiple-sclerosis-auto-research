# V45 Validation Command-Runner Checklist

Status: plan-only infrastructure. It does not execute validation.

## Purpose

`scripts/v45_validation_command_runner.py` generates an ordered command plan for
a received cohort package. It reduces operator error by sequencing the V45
guardrails before any frozen harness can run.

The script writes plans only. It does not open quarantined data, compute module
scores, score outcomes, or run a harness.

## Supported Modes

| Mode | Intended package | Extra guard |
|---|---|---|
| `primary` | V42/Gafson-style paired response validation | subject-map sanity |
| `pharmacodynamic` | context-only longitudinal cohort | response-column audit + subject-map sanity |
| `postpartum` | secondary postpartum APC-arm subject table | secondary preregistration gate |
| `tb` | secondary T/B compartment subject table | secondary preregistration gate |

## Example Commands

Primary:

```bash
.venv/bin/python scripts/v45_validation_command_runner.py \
  --cohort-id gafson_dmf_2018 \
  --mode primary \
  --root data/quarantine/gafson_dmf_2018 \
  --outdir analysis/v45_validation_command_runner/gafson_primary_plan
```

Pharmacodynamic:

```bash
.venv/bin/python scripts/v45_validation_command_runner.py \
  --cohort-id gse228330_ocrelizumab \
  --mode pharmacodynamic \
  --root data/quarantine/gse228330_ocrelizumab \
  --outdir analysis/v45_validation_command_runner/gse228330_pharmacodynamic_plan
```

Outputs per plan:

- `command_plan.tsv`
- `command_plan.md`
- `command_plan_summary.json`

## Generated Example Results

| Example | Steps | Required gates |
|---|---:|---|
| Gafson primary plan | 6 | data-use terms, checksum manifest, intake preflight, subject-map sanity, preregistration/addendum |
| GSE228330 pharmacodynamic plan | 7 | data-use terms, checksum manifest, response-column audit, intake preflight, subject-map sanity, preregistration/addendum |

## Gate Order

The generated plans enforce this order:

1. data-use/terms capture;
2. checksum-manifest verification;
3. response-column audit when pharmacodynamic-only;
4. full intake preflight;
5. subject-map sanity when paired deltas are required;
6. preregistration/addendum confirmation;
7. matching frozen harness handoff.

## Guardrail

This checklist does not replace the underlying guards. It only assembles the
commands. A cohort remains blocked if any generated command fails or if the
applicable preregistration/addendum is not already committed.
