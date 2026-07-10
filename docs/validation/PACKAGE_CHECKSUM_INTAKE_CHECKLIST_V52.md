# Package Checksum Intake Checklist V52

Date: 2026-07-10

Status: package-receipt checklist. This document adds no evidence, opens no
data, and changes no validation rule. It defines the minimum audit steps before
any incoming monitoring or target-development package can be analyzed.

## Entry Rule

No received package is analyzed until all receipt fields below are captured and
the package is classified as allowed by access terms. A package blocked by terms
or checksum failure remains quarantined and unread for analysis.

## Receipt Fields

| field | required value |
|---|---|
| package_id | stable lowercase ID, e.g. `gafson_dmf_2018`, `karolinska_dmf`, `chr1_genotype_package_YYYYMMDD` |
| receipt UTC | exact timestamp |
| received from | author, repository, collaborator, or data owner |
| access terms path | local terms summary path |
| access decision | approved / clarification needed / blocked |
| quarantine root | `data/quarantine/<package_id>/` or equivalent non-committed local path |
| raw file inventory | path to file list with sizes |
| checksum manifest | path to `SHA256_MANIFEST.tsv` |
| intended package type | monitoring validation / chr1 target-development / postpartum / T-B / pharmacodynamic context / other |
| operator | person or process recording receipt |

## Directory Shape

Recommended local, non-committed structure:

```text
data/quarantine/<package_id>/
  raw/
  processed/
  metadata/
  governance/
  SHA256_MANIFEST.tsv
```

Do not commit raw, restricted, or private package files.

## Required First Checks

| order | check | pass condition | stop condition |
|---:|---|---|---|
| 1 | access terms | terms permit the intended local analysis | terms absent, unclear, or restrictive |
| 2 | quarantine path | package is under a non-committed quarantine path | files are mixed into repo output trees |
| 3 | file inventory | all received files listed with size and timestamp | missing or unexplained files |
| 4 | checksum manifest | SHA256 recorded for every received file | missing checksum for any file |
| 5 | checksum verification | manifest verifies against local files | checksum mismatch |
| 6 | no raw git staging | no raw/private/quarantine file is tracked or staged | raw/private file appears in git |
| 7 | package type | package classified by V52 acceptance criteria | package type ambiguous |
| 8 | analysis eligibility | required fields for that package type present | missing required fields; classify partial/unscoreable |

## Command References

Use the repo virtual environment for validators that require project
dependencies:

```bash
.venv/bin/python -c 'import numpy, pandas; print("venv_numpy_pandas_ok")'
```

Checksum verification:

```bash
.venv/bin/python scripts/v45_checksum_manifest_validator.py verify \
  --root data/quarantine/<package_id> \
  --manifest data/quarantine/<package_id>/SHA256_MANIFEST.tsv \
  --outdir analysis/validation_command_runs/checksum_manifest/<package_id> \
  --fail-on-error
```

Primary monitoring intake preflight:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/<package_id> \
  --mode primary \
  --metadata data/quarantine/<package_id>/metadata/sample_metadata.tsv \
  --expression data/quarantine/<package_id>/processed/expression.tsv \
  --outdir analysis/validation_command_runs/intake_preflight/<package_id> \
  --write-checksums
```

No raw/private git staging check:

```bash
.venv/bin/python scripts/v45_no_raw_git_scanner.py
```

## Stop/Go Outcomes

| outcome | meaning | next action |
|---|---|---|
| `RECEIPT_APPROVED` | terms, quarantine, checksums, and type classification are complete | run package-specific preflight |
| `TERMS_BLOCKED` | access terms are missing, unclear, or restrictive | request clarification; do not analyze |
| `CHECKSUM_FAILED` | local file does not match recorded checksum | request retransmission or repair |
| `RAW_GIT_RISK` | raw/private/quarantine file is tracked or staged | unstage/remove before any commit |
| `PACKAGE_PARTIAL` | package is useful only for context or a subset of staged review | use communication template; do not overinterpret |
| `UNSCOREABLE` | package cannot answer the pre-specified question | request missing fields or replacement package |

## What Not To Do

- Do not open protected files for analysis before terms are approved.
- Do not infer a biological result from package absence, checksum failure, or
  unscoreability.
- Do not copy raw/private files into `docs/`, `analysis/`, or committed output
  trees.
- Do not tune a rule or endpoint to fit a partial package.
- Do not treat a target-development package as monitoring validation.

## Source Artifacts

- `docs/validation/VALIDATION_INTAKE_PREFLIGHT_V45.md`
- `docs/validation/VALIDATION_COMMAND_RUNNER_V45.md`
- `docs/validation/PREFLIGHT_FAILURE_TAXONOMY_V45.md`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv`
- `docs/validation/INCOMING_PACKAGE_COMMUNICATION_TEMPLATES_V52.md`
