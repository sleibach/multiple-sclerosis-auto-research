# Compute Capabilities

Last updated: 2026-05-28 12:23 CEST

## Known Working

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`.
- Shell: zsh.
- Python environment: `.venv_v3_py312`.
- Python version: 3.12.10.
- `curl` network downloads worked in V3 Wave170 for ChEMBL API artifacts.

## Known Limitations

- Python HTTPS via `urllib` failed with name-resolution errors under sandboxed
  execution during V3 Wave170.
- macOS `sysctl` hardware introspection failed under sandbox permissions.
- Foundation-model installation/runtime for Arc State/Stack/Evo 2 was not
  provisioned in V3.

## Operational Guidance

- Use saved raw artifacts for reproducibility when fetching with `curl`.
- Do not assume Python network access unless explicitly tested in the current
  run.
- Large model runs require an explicit compute feasibility check before being
  placed on a Tier 2+ critical path.
