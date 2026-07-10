# Receipt Blocker Template V52

Date: 2026-07-10

Status: operational template. This document adds no evidence, changes no
validation rule, and does not authorize analysis. Use it when a received package
cannot proceed past intake or preflight.

## Template

Copy this into:

`analysis/received_package_intake/<package_id>/receipt_blocker.md`

```markdown
# Receipt Blocker

Package ID: <package_id>
Detected UTC: <YYYY-MM-DDTHH:MM:SSZ>
Detected by: <operator>

## Blocker Type

Choose one:

- access terms unclear
- access terms forbid local analysis
- raw or restricted data received before permission
- required manifest missing
- manifest missing required classifier headers
- package route ambiguous
- required route fields missing
- file too large for git
- other: <describe>

## What Was Received

Describe only safe metadata. Do not paste patient-level data, raw expression,
genotype values, credentials, signed URLs, or restricted file contents.

## Why Analysis Stops

State which preflight or policy rule failed.

## Required Next Action

State exactly what the data owner, legal reviewer, or project operator must
provide before handling can resume.

## Allowed Interim Handling

State whether any safe metadata can be committed, whether raw files remain in
quarantine, and whether any classifier output is valid.
```

## Rule

Do not create a custom blocker format. Use this template so future package
handling can distinguish an operational blocker from a scientific null.
