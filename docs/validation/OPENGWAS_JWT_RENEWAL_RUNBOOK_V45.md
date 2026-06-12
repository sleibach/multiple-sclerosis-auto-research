# OpenGWAS JWT Renewal Runbook V45

Status: operations guardrail. No biological claim.

Purpose: prevent OpenGWAS authentication expiry from being mistaken for a
genetics null in later runs. V45 itself is mostly OpenGWAS-independent, but
genetics-adjacent follow-up tasks still depend on a valid JWT.

## Current Verified Status

Checked at `2026-06-12 18:26 UTC` with:

```bash
set -a
source .env >/dev/null 2>&1
set +a
.venv/bin/python scripts/check_opengwas_access.py
```

Result:

```text
OPENGWAS_JWT loaded: true; length=548
jwt_valid_until=2026-06-19 12:28 UTC (decoded locally; no /user GET call)
gwasinfo_ieu_b_18: HTTP 200; id=ieu-b-18; trait=multiple sclerosis; sample_size=115803
tophits_ieu_b_18: HTTP 200; rows=72; first_rsid=rs3134603
OpenGWAS access check passed.
```

Renewal should be done before `2026-06-19 12:28 UTC`; operationally, renew by
`2026-06-18` if any OpenGWAS-dependent work is planned.

## POST-Only Checker

`scripts/check_opengwas_access.py` is now POST-only:

- JWT expiry is decoded locally from the token payload and not fetched through
  `/user`.
- HTTP access is verified through POST calls to `/gwasinfo` and `/tophits`.
- The token is never printed.

This matches the project rule: no OpenGWAS GET calls.

## Renewal Steps

Official OpenGWAS documentation says JWT authentication is required for most
API endpoints and that tokens are generated from the account/profile page and
are valid for a limited period. See:

- OpenGWAS API authentication page: <https://api.opengwas.io/api/>
- OpenGWAS profile/token page: <https://api.opengwas.io/profile/>

Human renewal procedure:

1. Sign in to <https://api.opengwas.io/profile/>.
2. Generate a new JWT.
3. Replace the local `.env` value:

   ```bash
   OPENGWAS_JWT=<new-token>
   ```

4. Do not commit `.env`, the token, screenshots, or copied profile-page text.
5. In a fresh shell, run:

   ```bash
   set -a
   source .env >/dev/null 2>&1
   set +a
   .venv/bin/python scripts/check_opengwas_access.py
   ```

6. Continue OpenGWAS-dependent work only if the checker reports HTTP 200 on the
   POST endpoints.

## Failure Routing

| Failure | Meaning | Allowed action |
|---|---|---|
| `OPENGWAS_JWT missing` | `.env` lacks token or was not loaded | add token to gitignored `.env`, rerun checker |
| decoded expiry is past/current | token expired or clock mismatch | generate new token before OpenGWAS work |
| HTTP 401/403 | token invalid, expired, or unauthorized | renew token; do not treat as a data null |
| timeout/5xx | service/network problem | retry later or route around OpenGWAS-dependent task |
| POST endpoint schema change | API changed | update checker using official docs before genetics work |

## Runbook Rule

If OpenGWAS access fails, the correct project status is:

```text
OpenGWAS-dependent task blocked on authentication/service availability.
No biological or genetic null was observed.
```

Do not run fallback queries through GET to recover convenience.
