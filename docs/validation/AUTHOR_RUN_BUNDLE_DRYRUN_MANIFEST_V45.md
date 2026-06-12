# Author-Run Bundle Dry-Run Manifest V45

Status: author-run fallback send-readiness guard. No biological claim.

Purpose: verify, before any collaborator packet is sent, that the author-run
fallback packet has its required committed files present, checksum-verified, and
connected to a passing command-plan consistency check and current-action route.

This manifest is read-only. It does not create an archive, transfer files,
inspect external data, or run validation.

## Commands

Live dry-run:

```bash
.venv/bin/python scripts/v45_author_run_bundle_dryrun_manifest.py \
  --outdir analysis/v45_author_run_bundle_dryrun_manifest/live \
  --expect-status PASS
```

Synthetic missing-required-file regression:

```bash
.venv/bin/python scripts/v45_author_run_bundle_dryrun_manifest.py \
  --synthetic-case missing_required \
  --outdir analysis/v45_author_run_bundle_dryrun_manifest/synthetic_missing_required \
  --expect-status FAIL
```

## Inputs

- `analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv`
- `analysis/v45_author_run_packet_checksums/write/author_run_packet_sha256_manifest.tsv`
- `analysis/v45_author_run_packet_checksums/verify/author_run_packet_checksum_verify.tsv`
- `analysis/v45_author_run_packet_checksums/write/author_run_packet_checksum_summary.json`
- `analysis/v45_author_run_packet_checksums/verify/author_run_packet_checksum_verify_summary.json`
- `analysis/v45_command_plan_consistency/command_plan_consistency_summary.json`
- `analysis/v45_current_action_card/current_action_card.tsv`

## Current Result

Current live status: `PASS`.

Current synthetic missing-required-file status: `FAIL`, as expected by
regression.

Machine-readable outputs:

- `analysis/v45_author_run_bundle_dryrun_manifest/live/author_run_bundle_dryrun_manifest.tsv`
- `analysis/v45_author_run_bundle_dryrun_manifest/live/author_run_bundle_dryrun_violations.tsv`
- `analysis/v45_author_run_bundle_dryrun_manifest/live/author_run_bundle_dryrun_summary.json`
- `analysis/v45_author_run_bundle_dryrun_manifest/synthetic_missing_required/author_run_bundle_dryrun_manifest.tsv`
- `analysis/v45_author_run_bundle_dryrun_manifest/synthetic_missing_required/author_run_bundle_dryrun_violations.tsv`
- `analysis/v45_author_run_bundle_dryrun_manifest/synthetic_missing_required/author_run_bundle_dryrun_summary.json`

## Interpretation Boundary

A live `PASS` means the author-run fallback packet is mechanically ready to
assemble from committed non-sensitive files, subject to human approval of the
external send. It does not mean:

- the packet was sent;
- any author accepted the route;
- any data or aggregate output was received;
- any validation was run.

The synthetic missing-required-file run is method behavior only. It proves the
guard catches an impossible packet manifest.
