# Generated Checker Registry V45

Status: infrastructure navigation and documentation audit. No biological claim.

Script:

`scripts/v45_generated_checker_registry.py`

Purpose: map V45/V46 scripts to documentation references, likely analysis output
directories, summary JSON files, and observed pass/fail/headline statuses. This
helps reviewers see which readiness/checker scripts are documented and where
their outputs live.

## Command

```bash
.venv/bin/python scripts/v45_generated_checker_registry.py \
  --outdir analysis/v45_generated_checker_registry
```

## Output

- `analysis/v45_generated_checker_registry/generated_checker_registry.tsv`
- `analysis/v45_generated_checker_registry/generated_checker_registry_summary.json`

The registry is best read as a navigation aid. A script with `REVIEW_NEEDED`
does not imply a biological problem; it means documentation or output discovery
should be checked.

## Current Result

- scripts indexed: `100`
- undocumented scripts: `0`
- scripts without detected output directories: `0`
- overall status: `PASS`

The generator-name shortening cases are handled by explicit registry
exceptions, so all currently indexed V45/V46 scripts have detected output
directories.
