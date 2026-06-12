# V45 Checksum-Manifest Validator

Status: infrastructure guardrail. No biological claim.

## Purpose

`scripts/v45_checksum_manifest_validator.py` writes and verifies lightweight
SHA256 manifests for handoff packages that are not yet full validation intake
packages. This covers:

- outbound request packet bundles;
- small received metadata-only packages;
- acquisition handoff folders before full V45 intake preflight is assembled.

The full validation intake preflight remains the required gate before any frozen
harness runs.

## Commands

Write a manifest:

```bash
.venv/bin/python scripts/v45_checksum_manifest_validator.py write \
  --root docs/validation/outbound_requests \
  --manifest analysis/v45_checksum_manifest_validator/outbound_requests_manifest.tsv
```

Verify a manifest:

```bash
.venv/bin/python scripts/v45_checksum_manifest_validator.py verify \
  --root docs/validation/outbound_requests \
  --manifest analysis/v45_checksum_manifest_validator/outbound_requests_manifest.tsv \
  --outdir analysis/v45_checksum_manifest_validator/outbound_requests_verify \
  --fail-on-error
```

Outputs:

- manifest TSV with `relative_path`, `sha256`, and `bytes`;
- `manifest_audit.tsv`;
- `manifest_audit_summary.json`.

## Synthetic Verification

Command run:

```bash
.venv/bin/python scripts/v45_checksum_manifest_validator.py synthetic-check \
  --outdir analysis/v45_checksum_manifest_validator/synthetic_check
```

Result: `PASS`

| Fixture | Expected | Observed |
|---|---:|---:|
| unchanged synthetic package | pass | pass |
| modified file after manifest write | fail | fail |

## Outbound Request Packet Check

The validator wrote and verified:

`analysis/v45_checksum_manifest_validator/outbound_requests_manifest.tsv`

for:

`docs/validation/outbound_requests/`

Current result:

| Metric | Value |
|---|---:|
| manifest rows | 4 |
| audit rows | 4 |
| failures | 0 |
| warnings | 0 |
| overall status | `PASS` |

## Interpretation

This validator catches drift or tampering in small handoff bundles. It is not a
replacement for:

1. data-use/terms review;
2. quarantine placement;
3. full intake preflight;
4. subject-map sanity checks;
5. cohort-specific preregistration addenda.

It is additive and does not change any locked rule or frozen validation
threshold.
