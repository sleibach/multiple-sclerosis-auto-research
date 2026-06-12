# Sensitive Data Redaction Checklist V45

Status: data-governance checklist. No data received or analyzed.

Purpose: prevent private clinical, expression, agreement, credential, or
correspondence material from being committed or sent in collaborator-facing
handoffs.

Machine-readable checklist:

`docs/validation/input_schemas/V45_sensitive_data_redaction_checklist.tsv`

## Scope

Run this checklist before committing or sending:

- receipt summaries;
- request follow-ups;
- validation handoff bundles;
- gate-output bundles;
- result reports;
- external account appendices.

## Redaction Rules

| Risk | Required action |
|---|---|
| raw expression or assay files | keep outside git unless terms explicitly permit |
| sample-level clinical labels | keep outside git unless terms explicitly permit |
| signed agreements/contracts | never commit; summarize non-sensitive permission status only |
| credentials/tokens/private URLs | never commit or paste into docs |
| private email content | commit only sanitized sent-packet templates, not private replies |
| identifiable dates/IDs | replace with study IDs or aggregate summaries where terms require |
| screenshots of portals/accounts | do not commit |

## Allowed Commit Content

Allowed only when terms permit:

- non-sensitive data-use summary;
- checksums/manifests without private URLs;
- aggregate preflight status;
- schema compatibility summaries;
- frozen addendum text written before scoring;
- aggregate validation outputs from the frozen harness.

## Required Pre-Commit Commands

```bash
.venv/bin/python scripts/v45_no_raw_git_scanner.py
.venv/bin/python scripts/v45_precommit_readiness_check.py
```

If either fails, stop and repair before committing.

## Redaction Stamp

For any handoff artifact, add a short stamp:

```text
Redaction checked: [YYYY-MM-DDTHH:MM:SSZ]
Private raw data, credentials, signed agreements, and private correspondence
are excluded from this artifact.
```
