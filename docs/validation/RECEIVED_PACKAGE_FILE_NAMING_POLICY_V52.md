# Received Package File Naming Policy V52

Date: 2026-07-10

Status: operational policy. This document adds no evidence, changes no
validation rule, and does not authorize inspection of restricted data. It defines
where received-package metadata, classifier outputs, and raw files may live.

## Package ID

Use a stable package ID before any analysis:

`YYYYMMDD_source_shortname_packagekind`

Examples:

- `20260710_karolinska_dmf_manifest`
- `20260710_gafson_dmf_response`
- `20260710_chr1_collaborator_genotype_expression`

Use only lowercase letters, numbers, and underscores. Do not include patient
identifiers, emails, accession tokens, or access credentials in the package ID.

## Paths

| content | path pattern | git status |
|---|---|---|
| restricted raw files | `data/raw/received_packages/<package_id>/` | ignored by `.gitignore`; never commit |
| safe metadata manifest | `analysis/received_package_intake/<package_id>/manifest.tsv` | commit only if access terms allow and no restricted content is present |
| redacted metadata manifest | `analysis/received_package_intake/<package_id>/manifest_redacted.tsv` | commit if it contains only non-restricted metadata |
| route-classifier output | `analysis/received_package_intake/<package_id>/route_classification.tsv` | commit if generated from a safe or redacted manifest |
| checksum summary | `analysis/received_package_intake/<package_id>/checksums.sha256` | commit only if filenames and hashes are allowed to be disclosed |
| receipt blocker note | `analysis/received_package_intake/<package_id>/receipt_blocker.md` | commit if needed to explain why analysis stopped |

## Classifier Command

```bash
python3 scripts/v52_package_route_classifier.py \
  --manifests analysis/received_package_intake/<package_id>/manifest.tsv \
  --out analysis/received_package_intake/<package_id>/route_classification.tsv
```

If only a redacted manifest is allowed:

```bash
python3 scripts/v52_package_route_classifier.py \
  --manifests analysis/received_package_intake/<package_id>/manifest_redacted.tsv \
  --out analysis/received_package_intake/<package_id>/route_classification.tsv
```

## Commit Rules

Commit only safe metadata, classifier outputs, and blocker notes. Never commit:

1. raw expression matrices from restricted packages;
2. genotype files;
3. patient-level clinical files if terms do not explicitly allow local storage
   in git;
4. files larger than repository limits;
5. access credentials or signed URLs.

If terms are unclear, record a receipt blocker and stop. Do not inspect or
classify restricted content by convenience.

## Boundary

This policy controls file placement and names only. It does not decide package
scoreability; the route classifier, preflight checklist, field dictionary, and
route-specific cards still decide that.
