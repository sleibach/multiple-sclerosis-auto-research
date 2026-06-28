# V50 Public Guard Status

Status: operational guard card. This file reports repository-publication and
route-health checks only. It is not biological evidence, does not validate any
project finding, and does not change any locked rule or pre-registration.

## Latest Guard Run

- checked UTC: `2026-06-28T18:52:14Z`
- wrapper command:
  `python3 scripts/v50_run_public_guards.py run --fail-on-error`
- wrapper status: `PASS`
- guard families: `2`
- failures: `0`
- OpenGWAS used: `false`

## Guard Families

| guard | status | checks | failures | output |
|---|---|---:|---:|---|
| status freshness | `PASS` | `16` | `0` | `analysis/v50_public_guards/status_freshness/status_freshness_lint.tsv` |
| non-OpenGWAS routes | `PASS` | `8` routes | `0` | `analysis/v50_public_guards/non_opengwas_routes/route_check_results.tsv` |

## Interpretation

The public landing/status files still point to V50, and the currently registered
non-OpenGWAS public metadata/API routes are reachable at transport/schema level.
This does not mean any route contains a usable validation cohort or evidence for
a biological claim. It only means the public guard wrapper is functioning and no
OpenGWAS endpoint was called while the JWT is expired.

## Required Push Guards

Before each V50 push, run:

```bash
python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error
python3 scripts/v48_public_index_crosslink_linter.py lint --fail-on-error
python3 scripts/v47_provenance_gate.py audit
python3 scripts/v50_status_freshness_linter.py lint --fail-on-error
python3 scripts/v50_check_non_opengwas_routes.py check --fail-on-error
python3 scripts/v50_run_public_guards.py run --fail-on-error
git ls-files -z | while IFS= read -r -d '' f; do [ -f "$f" ] || continue; size=$(wc -c < "$f"); if [ "$size" -gt 52428800 ]; then printf '%s\t%s\n' "$size" "$f"; fi; done
git ls-files | rg '(^|/)tmp/' || true
```

## Current Boundary

OpenGWAS remains disabled until token renewal and a passing POST-based access
check. Non-OpenGWAS route checks are transport/schema checks only and must not be
used as biological evidence. Source: `meta/NEXT_ACTIONS.md`;
`docs/knowledge/EPISTEMIC_CLASSES.md`.
