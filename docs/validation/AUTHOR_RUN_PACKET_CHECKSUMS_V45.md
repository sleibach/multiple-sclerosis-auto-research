# Author-Run Packet Checksums V45

Status: packet-integrity infrastructure. No biological claim.

Script:

`scripts/v45_author_run_packet_checksum_manifest.py`

Purpose: write and verify SHA-256 checksums for the committed, non-sensitive
files included in the author-run packet bundle. This supports integrity checks
after a collaborator packet is transferred.

## Commands

Write the manifest:

```bash
.venv/bin/python scripts/v45_author_run_packet_checksum_manifest.py write \
  --outdir analysis/v45_author_run_packet_checksums/write
```

Verify the manifest:

```bash
.venv/bin/python scripts/v45_author_run_packet_checksum_manifest.py verify \
  --manifest analysis/v45_author_run_packet_checksums/write/author_run_packet_sha256_manifest.tsv \
  --outdir analysis/v45_author_run_packet_checksums/verify \
  --fail-on-error
```

Synthetic regression:

```bash
.venv/bin/python scripts/v45_author_run_packet_checksum_manifest.py synthetic-check \
  --outdir analysis/v45_author_run_packet_checksums
```

Current verification:

- manifest write: `28` included packet files, `0` missing;
- manifest verify: `28/28` pass;
- synthetic corrupted manifest: `FAIL` with `1` hash mismatch.

## Scope

The manifest is built from:

`analysis/v45_author_run_packet_bundle/author_run_packet_bundle_index.tsv`

Only rows with `include_in_author_packet=yes` are hashed. Excluded raw,
quarantine, credential, and private-data paths are not hashed or transferred by
this packet.
