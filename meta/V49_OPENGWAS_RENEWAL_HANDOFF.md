# V49 OpenGWAS Renewal Handoff

Status: operational auth handoff. This file records the current OpenGWAS JWT
state after V49 resumed on `2026-06-20`. It is not a biological result and
should not be used as evidence for any genetics null.

## Current State

- Latest V49 resume check: `2026-06-20T07:42:42Z`
- Check command:

```bash
set -a
source .env
set +a
python3 scripts/check_opengwas_access.py
```

- `OPENGWAS_JWT` was present in `.env`.
- Local decoded expiry: `2026-06-19 12:28 UTC`.
- API result on resume: `gwasinfo_ieu_b_18` returned HTTP `401`.
- Interpretation: token expired. Route around OpenGWAS-dependent work until a
  renewed token is placed in the gitignored `.env`.

## Required Human Step

Renew `OPENGWAS_JWT` in `.env` before any future OpenGWAS-dependent task. Do
not commit the token or any derived secret.

After renewal, run:

```bash
set -a
source .env
set +a
python3 scripts/check_opengwas_access.py
```

Expected healthy result:

- local decoded expiry is in the future;
- `gwasinfo_ieu_b_18` returns HTTP `200`;
- `tophits_ieu_b_18` returns HTTP `200`;
- the script prints `OpenGWAS access check passed.`

## Safe Routing Rule

Until renewal passes, future sessions must not:

- run OpenGWAS-dependent analyses;
- treat HTTP `401` or missing OpenGWAS output as a biological null;
- expand genetics conclusions from failed auth-dependent calls.

OpenGWAS-independent repository hygiene, external-layer provenance, validation
harness, and already-held-data work can continue.
