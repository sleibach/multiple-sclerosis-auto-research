# Manifest Metadata Versus Raw Data Git Policy V52

Date: 2026-07-10

Status: operational policy. This document adds no evidence, changes no
validation rule, and does not authorize data inspection. It distinguishes
metadata manifests that may be committed from raw or restricted package content
that must stay out of git.

## Commit-Eligible Metadata

A manifest or classifier output may be committed only when all of the following
are true:

1. allowed-use terms permit local storage in this repository;
2. the file contains package metadata, route fields, checksums, or classifier
   output only;
3. there are no patient identifiers, sample-level clinical values, genotype
   values, expression values, access tokens, signed URLs, or restricted raw data;
4. the file is small enough for normal git storage;
5. the package route can be interpreted without exposing restricted content.

Examples that may be commit-eligible after terms check:

- `manifest.tsv`
- `manifest_redacted.tsv`
- `route_classification.tsv`
- `receipt_blocker.md`

## Never Commit

Never commit:

1. raw expression matrices;
2. FASTQ/BAM/VCF/genotype dosage files;
3. patient-level outcomes or dates unless explicitly allowed and de-identified;
4. proprietary supplements or data-owner restricted files;
5. credentials, tokens, signed URLs, or access links;
6. any file larger than repository limits.

These belong in an ignored/quarantined location such as:

`data/raw/received_packages/<package_id>/`

## Operator Rule

If unsure whether a received file is metadata or raw/restricted content, treat it
as restricted. Record a receipt blocker and request clarification. Do not commit
first and decide later.

## Relationship To Other Controls

- Use `docs/validation/RECEIVED_PACKAGE_FILE_NAMING_POLICY_V52.md` for paths.
- Use `docs/validation/INCOMING_PACKAGE_MANIFEST_TEMPLATE_V52.tsv` for the safe
  manifest shape.
- Use `scripts/v52_package_route_classifier.py` only on a safe or redacted
  manifest.
