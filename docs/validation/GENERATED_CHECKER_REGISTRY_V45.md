# Generated Checker Registry V45

Status: infrastructure navigation and documentation audit. No biological claim.

Script:

`scripts/v45_generated_checker_registry.py`

Purpose: map V45 scripts to documentation references, likely analysis output
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

- scripts indexed: `59`
- undocumented scripts: `0`
- scripts without detected output directories: `2`
- overall status: `PASS`

The two scripts without auto-detected output directories are documented
generators whose output directory names are shortened relative to the script
stem:

- `scripts/v45_followup_message_template_generator.py`
- `scripts/v45_route_arrival_packet_generator.py`

This is a navigation/discovery limitation, not a validation failure.
