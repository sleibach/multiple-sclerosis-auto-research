# Collaborator Package Path Resolver V45

Status: infrastructure governance check. No biological claim.

Script:

`scripts/v45_collaborator_package_path_resolver.py`

Purpose: verify that concrete artifact paths referenced by the V45 collaborator
package README and package manifests still exist after readiness updates.
Placeholders such as `<cohort>` are ignored because they are operator examples,
not committed artifacts.

## Checked Sources

Default live sources:

- `docs/validation/COLLABORATOR_VALIDATION_PACKAGE_README_V45.md`
- `docs/validation/AUTHOR_RUN_PACKET_BUNDLE_INDEX_V45.md`
- `analysis/v45_collaborator_package/collaborator_package_manifest.tsv`
- `analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv`

## Commands

Live check:

```bash
.venv/bin/python scripts/v45_collaborator_package_path_resolver.py check \
  --outdir analysis/v45_collaborator_path_resolver/live_sources \
  --fail-on-missing
```

Synthetic positive/negative regression:

```bash
.venv/bin/python scripts/v45_collaborator_package_path_resolver.py synthetic-check \
  --outdir analysis/v45_collaborator_path_resolver
```

Current verification:

- live collaborator sources: `PASS`, `164` concrete references resolved, `0` missing, `7` placeholders/directories ignored;
- synthetic broken source: `FAIL`, `1` missing synthetic reference, `1` ignored placeholder/directory example.

## Use

Run this after collaborator-package, author-run bundle, or validation-readiness
documentation changes. A missing concrete reference means the handoff package is
not reviewer-ready until the link is repaired or the referenced artifact is
restored.
