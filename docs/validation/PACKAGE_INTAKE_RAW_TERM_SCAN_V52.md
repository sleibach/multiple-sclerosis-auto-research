# Package Intake Raw-Term Scan V52

Date: 2026-07-10

Status: operational wording scan. This document adds no biological evidence and
does not inspect package data.

## Purpose

This scan checks package-intake operator documents for unsafe credential, token,
email, signed-URL, raw-data, or restricted-content wording. It hard-fails on
secret-like patterns and treats raw/restricted wording as acceptable only when
the surrounding Markdown context is a prohibition, quarantine, or policy
statement.

## Command

```bash
python3 scripts/v52_package_intake_raw_term_scanner.py --fail-on-error
```

## Recorded Result

Recorded output:

`analysis/v52_package_intake_raw_term_scanner/raw_term_scan.tsv`

Current result: 42 contextual wording checks, 0 hard failures, 0 warnings.

## Boundary

This scan is a text-safety smoke check. It does not certify future real package
contents, access terms, or route suitability.
