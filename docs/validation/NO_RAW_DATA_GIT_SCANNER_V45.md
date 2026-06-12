# V45 No-Raw-Data-In-Git Scanner

Status: commit-safety guardrail. No data analyzed.

## Purpose

`scripts/v45_no_raw_git_scanner.py` scans tracked and pending Git paths for
forbidden raw/quarantine data patterns before commits. It is designed for V45
validation-readiness work, where received clinical/individual-level data must
not be committed by accident.

## Command

```bash
.venv/bin/python scripts/v45_no_raw_git_scanner.py
```

Outputs:

- `analysis/v45_no_raw_git_scanner/no_raw_git_audit.tsv`
- `analysis/v45_no_raw_git_scanner/summary.json`

## Hard-Fail Rules

The scanner fails if Git-tracked or pending paths match:

- `data/quarantine/`
- `data/raw_v3/gafson_dmf_2018/`
- `data/raw_v3/karolinska_dmf_ros_2019/`
- `data/raw_v3/gse228330_ocrelizumab_outcomes/`
- restricted/agreement/credential-like filenames under `data/`
- individual-level assay extensions in live validation paths.

Hard failures must be resolved before committing.

## Warning Rules

The scanner warns on historical/public raw-data paths already tracked in the
repository. These warnings do not block the current V45 checkpoint, but they
remind future runs not to add new restricted validation data under those paths.

## Current Result

Overall status: `PASS`

| Metric | Value |
|---|---:|
| hard failures | 0 |
| warnings | 11 |

Current warnings are historical tracked public raw paths under `data/raw*`,
mainly the EBV V35 public raw files and `.gitkeep` placeholders. No V45 live
validation or quarantine raw data are committed.

## Guardrail

This scanner does not replace data-use review, checksums, or intake preflight.
It is a pre-commit safety check against accidentally committing restricted or
individual-level received validation data.
