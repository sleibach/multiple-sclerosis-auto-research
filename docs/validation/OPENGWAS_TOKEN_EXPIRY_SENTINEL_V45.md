# OpenGWAS Token Expiry Sentinel V45

Status: operations guardrail. No biological claim.

## Purpose

`scripts/v45_opengwas_token_expiry_sentinel.py` decodes the local
`OPENGWAS_JWT` expiry from `.env` without printing the token and writes a
machine-readable renewal status. It makes no OpenGWAS API calls. The POST-only
HTTP checker remains `scripts/check_opengwas_access.py`.

This prevents authentication expiry or shell-environment shadowing from being
mistaken for a genetic null.

## Command

```bash
.venv/bin/python scripts/v45_opengwas_token_expiry_sentinel.py \
  --outdir analysis/v45_opengwas_token_expiry_sentinel
```

Then, only when OpenGWAS access is actually needed:

```bash
.venv/bin/python scripts/check_opengwas_access.py
```

## Current Result

- renewal status: `RENEW_SOON`
- expiry: `2026-06-19 12:28:39 UTC`
- days remaining at sentinel run: about `6.6`
- `.env` present: `true`
- inherited environment token differed from `.env`: detected and routed around
  by using `.env` as the credential source of truth.

## Machine-Readable Outputs

- `analysis/v45_opengwas_token_expiry_sentinel/opengwas_token_expiry_sentinel_summary.json`
- `analysis/v45_opengwas_token_expiry_sentinel/opengwas_token_expiry_sentinel.tsv`

## Interpretation Boundary

`RENEW_SOON` means OpenGWAS-dependent work should be avoided or kept short until
the token is renewed. It does not affect V42/V45 validation readiness unless a
future step unexpectedly needs OpenGWAS. `EXPIRED`, `INVALID_FORMAT`, or
`MISSING` are authentication blockers, not data results.
