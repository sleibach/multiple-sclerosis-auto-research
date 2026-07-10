# OpenGWAS Renewal Watch V52

Date: 2026-07-10

Status: operational guardrail. This note does not add genetics evidence.

## Current Token State

On 2026-07-10, `scripts/check_opengwas_access.py` loaded `.env` and verified
OpenGWAS API v4 POST-only access:

- `/gwasinfo` POST for `ieu-b-18`: HTTP 200;
- `/tophits` POST for `ieu-b-18`: HTTP 200;
- decoded JWT expiry: `2026-07-24 08:00 UTC`.

## Required Behavior

Before any OpenGWAS-dependent task:

```bash
python3 scripts/check_opengwas_access.py
```

If the checker returns HTTP 200, OpenGWAS may be used only for bounded,
pre-specified V52 genetics reruns:

- confirmed-locus SuSiE-coloc reruns;
- frozen chr1/ZMIZ1/PTGER4 direction or LD checks;
- no broad new discovery scan.

If the checker returns HTTP 401 or reports expiry:

1. Stop OpenGWAS-dependent work.
2. Route to non-OpenGWAS public sources where applicable.
3. Record the auth blocker as operational, not biological.
4. Request token renewal before any OpenGWAS-dependent interpretation.

## Renewal Deadline

The renewed token expires on `2026-07-24 08:00 UTC`. Any targeted genetics
reruns that depend on OpenGWAS should either finish before that timestamp or
start by renewing the token again.

## Evidence Boundary

Authentication status is not evidence. A failed OpenGWAS call after expiry must
never be reported as a null genetics result.
