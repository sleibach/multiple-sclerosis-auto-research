# OpenGWAS Expiry-Day Runbook V52

Date: 2026-07-10

Status: operational runbook. This document adds no genetics evidence and does
not authorize broad discovery. It defines what to do as the renewed OpenGWAS
token approaches or passes `2026-07-24 08:00 UTC`.

## Current State

- Token verified active on 2026-07-10.
- Decoded expiry: `2026-07-24 08:00 UTC`.
- OpenGWAS use remains POST-only and bounded to pre-specified V52 commands.

## Daily Or Genetics-Session Start Check

Run:

```bash
python3 scripts/check_opengwas_access.py
```

Optional local expiry sentinel:

```bash
.venv/bin/python scripts/v45_opengwas_token_expiry_sentinel.py
```

If `.venv/bin/python` lacks dependencies on a future machine, use the
environment that can import `pandas`; this sentinel makes no OpenGWAS request.

## Status Routing

| status | action | interpretation |
|---|---|---|
| HTTP 200 and expiry outside 7 days | bounded POST-only OpenGWAS commands may run | operationally available |
| HTTP 200 but within 7 days | run only short bounded commands; request renewal before multi-day work | renewal soon, not biology |
| HTTP 200 but within 48 hours | renew before starting any queued genetics work unless the command is immediately necessary and bounded | urgent renewal |
| HTTP 401 or expired local JWT | stop OpenGWAS-dependent work and route around | auth blocker, not null |
| API unavailable or timeout | retry later or route around; record service blocker | service blocker, not null |
| renewed token added to `.env` | rerun `scripts/check_opengwas_access.py` before any interpretation | restored operational access |

## Allowed Before Expiry

Use only commands listed in:

`docs/workups/genetics/OPENGWAS_PRE_EXPIRY_BOUNDED_POLISH_COMMANDS_V52.md`

Priority order:

1. `python3 scripts/check_opengwas_access.py`
2. `python3 scripts/v14_susie_coloc_confirmed_loci.py`
3. `python3 scripts/v19_chr1_reanalysis.py`, only when chr1 handoff tables need
   refresh

## Forbidden On Expiry Day

Do not:

1. run new genome-wide scans;
2. run exploratory next-tier locus searches;
3. treat a failed request as a genetics null;
4. change V22/V42/V44 validation logic;
5. promote or reopen targets because an API route is temporarily available;
6. use OpenGWAS GET routes.

## If The Token Expires Mid-Run

1. Stop the OpenGWAS-dependent command family.
2. Record the exact command, timestamp, and auth/service status.
3. Mark the result as incomplete operationally.
4. Continue non-OpenGWAS tasks.
5. Request or install renewed token in `.env`.
6. Rerun `scripts/check_opengwas_access.py` after renewal before resuming.

## If A Renewed Token Is Provided

1. Save only to gitignored `.env`; never commit the token.
2. Confirm the `.env` override is active, not a stale process environment.
3. Run:

```bash
python3 scripts/check_opengwas_access.py
```

Expected successful state:

- decoded expiry prints a future timestamp;
- `gwasinfo_ieu_b_18` returns HTTP 200;
- `tophits_ieu_b_18` returns HTTP 200.

Only after that check may bounded OpenGWAS work resume.

## Queue Note Template

Use this wording in future queue files:

`OpenGWAS status: [VALID / RENEW_SOON / URGENT_RENEWAL / EXPIRED / SERVICE_BLOCKED].
Checked at [UTC timestamp]. Interpretation: operational status only; no
genetics null inferred. Next action: [bounded command / renew token / route
around].`

## Source Artifacts

- `meta/OPENGWAS_RENEWAL_WATCH_V52.md`
- `docs/workups/genetics/OPENGWAS_PRE_EXPIRY_BOUNDED_POLISH_COMMANDS_V52.md`
- `scripts/check_opengwas_access.py`
- `scripts/v45_opengwas_token_expiry_sentinel.py`

