# Received Package Intake Safety Audit V52

Date: 2026-07-10

Status: operational smoke audit. This document adds no biological evidence and
does not inspect raw received-package data.

## Purpose

The audit checks whether tracked files under `analysis/received_package_intake/`
remain consistent with the V52 intake boundary:

- safe file extensions only
- no oversized tracked intake artifacts
- no raw-data file extensions
- no non-placeholder email addresses
- no TSV headers that look like raw per-sample clinical or expression data

The audit is intentionally conservative. A failure means the file must be
reviewed before commit or push.

## Command

```bash
python3 scripts/v52_received_intake_safety_audit.py --fail-on-error
```

## Recorded Result

Recorded output:

`analysis/v52_received_intake_safety_audit/intake_safety_audit.tsv`

Current result: 3 tracked intake files, 14 checks, 0 failures.

## Boundary

This audit is a commit-safety check only. It does not certify that a future real
package may be analyzed. Route-specific analysis still requires the V52 package
ID check, access-term checklist, safe manifest, route classifier, and preflight
decision table.
