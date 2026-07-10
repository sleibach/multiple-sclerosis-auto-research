# Package ID Validation Note V52

Date: 2026-07-10

Status: operational note. This document adds no evidence, changes no validation
rule, and does not inspect real data. It defines how to check received-package
IDs before creating intake paths.

## Required Shape

Package IDs must match:

`YYYYMMDD_lowercase_alnum_underscore_segments`

Examples:

- `20260710_karolinska_dmf_manifest`
- `20260710_gafson_dmf_response`
- `20260710_chr1_collaborator_genotype_expression`

Do not include patient identifiers, emails, access tokens, signed URLs, or human
names.

## Command

```bash
python3 scripts/v52_validate_package_id.py 20260710_karolinska_dmf_manifest
```

Expected pass output includes:

`'status': 'PASS'`

## Synthetic Checks

Recorded checks:

`analysis/v52_package_id_validation/package_id_validation_checks.tsv`

## Boundary

The validator checks syntax only. It cannot detect whether a package ID embeds a
real person's name or sensitive identifier. Operators must still inspect the ID
semantically before using it.
