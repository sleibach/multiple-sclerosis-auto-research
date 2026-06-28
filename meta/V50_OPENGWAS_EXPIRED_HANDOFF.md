# V50 OpenGWAS Expired Handoff

Status: operational handoff. This file records the current OpenGWAS token state
and the safe routing rules until renewal.

## Current Status

- checked during V50: `2026-06-28`
- decoded JWT expiry: `2026-06-19T12:28:39Z`
- status: expired
- policy: do not call OpenGWAS endpoints until a renewed token is present
- allowed work while expired: non-OpenGWAS public APIs, local reruns, metadata
  scouts, validation-harness preparation, external-layer navigation, and
  already-downloaded project data

## Required Human Step

Renew `OPENGWAS_JWT` in the gitignored `.env` before any OpenGWAS-dependent
task runs.

After renewal, run:

```bash
python3 scripts/check_opengwas_access.py
```

Expected safe result: HTTP 200 using the project script. OpenGWAS API v4 calls
must remain POST-only.

## Route-Around Rules

Until renewal:

1. Do not call OpenGWAS directly or indirectly.
2. Do not treat a failed OpenGWAS request as a null result.
3. Mark every OpenGWAS-dependent task as blocked on token renewal.
4. Prefer non-OpenGWAS public routes when they answer a narrow operational
   question, for example the V50 GWAS Catalog allele-routing manifest.
5. Re-check this file before any future genetics task that might silently use
   OpenGWAS.

## Known Non-OpenGWAS Routes Created In V50

| route | artifact | use |
|---|---|---|
| GWAS Catalog rsid extraction | `knowledge_external/synthesis/V50_GWAS_CATALOG_ALLELE_ROUTING.md` | rs1250550, rs4613763, and rs7522462 route planning without OpenGWAS. |
| GSE255952 metadata scout | `knowledge_external/synthesis/V50_GSE255952_METADATA_SCOUT.md` | methylprednisolone B/T-cell metadata route for future steroid-panel testing. |
| Remaining source-search packet | `knowledge_external/synthesis/V50_REMAINING_SOURCE_SEARCH_PACKET.md` | literature/repository search routes that do not require OpenGWAS. |

## Decision

The OpenGWAS token expiry is an operational blocker, not a scientific finding.
Any result that depends on OpenGWAS must wait until renewal and a fresh access
check passes.
