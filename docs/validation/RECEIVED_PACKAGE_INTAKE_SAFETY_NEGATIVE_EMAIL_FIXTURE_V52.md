# Received-Package Intake Safety Negative Email Fixture V52

Date: 2026-07-10

Status: synthetic negative-control fixture. This document adds no biological
evidence, does not inspect raw package data, and does not alter any validation
rule or therapeutic verdict.

## Purpose

The received-package intake safety audit must reject committed intake metadata
that contains a non-placeholder email address. The production audit scans only
tracked files under `analysis/received_package_intake/`. For regression testing,
`scripts/v52_received_intake_safety_audit.py` also supports `--all-files`, which
lets a synthetic fixture directory be scanned before it is tracked in git.

## Fixture

- Fixture root:
  `analysis/v52_received_intake_safety_negative_email_fixture/`
- Fixture file:
  `analysis/v52_received_intake_safety_negative_email_fixture/manifest.tsv`
- Email used:
  `operator@example.com`

The email is intentionally from the reserved `example.com` documentation domain.
It is not a real contact address and is used only to confirm that the safety
audit detects any email not ending in `.invalid`.

## Verification Command

```bash
python3 scripts/v52_received_intake_safety_audit.py \
  --intake-root analysis/v52_received_intake_safety_negative_email_fixture \
  --out analysis/v52_received_intake_safety_negative_email/negative_email_audit.tsv \
  --all-files \
  --fail-on-error
```

Expected result: nonzero exit, because the synthetic manifest should fail the
`non_placeholder_email` check. The committed audit output is:

`analysis/v52_received_intake_safety_negative_email/negative_email_audit.tsv`

## Boundary

This is a method-behavior test only. It proves the intake safety audit detects a
non-placeholder email in a synthetic metadata fixture. It is not evidence about
MS, any cohort, or any real received package.
