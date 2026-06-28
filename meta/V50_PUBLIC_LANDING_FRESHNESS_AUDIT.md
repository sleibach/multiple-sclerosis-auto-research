# V50 Public Landing Freshness Audit

Status: repository-navigation audit only. This file does not add a scientific
claim, change a locked rule, alter a pre-registration, or reclassify any
finding.

## Purpose

Task 51 checked whether the public GitHub landing path points readers to the
true current repository state after V45-V50. The concern was that stale
front-page wording could make the repository look less current, less governed,
or less push-ready than it is.

## Files Checked

- `README.md`
- `meta/CURRENT_STATUS.md`
- `meta/NEXT_ACTIONS.md`
- `knowledge_external/INDEX.md`
- `docs/reports/FINDINGS_REPORT_V37.md`
- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/POWER_MAP_V43.md`

## Findings

| file | freshness status | issue | public-reader risk | recommended fix |
|---|---|---|---|---|
| `README.md` | stale headline | The `Current Status` section says the current phase is `V43`, while the live work has advanced through V50. | High: a GitHub reader starts from a false current-phase label. | Replace the headline with a stable pointer to `meta/CURRENT_STATUS.md`, `meta/NEXT_ACTIONS.md`, and the newest `meta/V*_QUEUE.md` rather than hard-coding a phase number. |
| `README.md` | partially current body | The long phase history includes V40-V43 and some V49 post-purge notes, but does not summarize V44-V50 as the active frontier. | Medium: readers can see some later artifacts but not the actual latest operational state. | Add compact rows for V44-V50 in the phase ledger and a short "latest operational state" pointer. |
| `meta/CURRENT_STATUS.md` | stale canonical status | Last updated `2026-06-12 17:50 CEST`; it summarizes V44 but not V45-V50. | High: the canonical status file omits the 6-hour V45/V46 blocks, V47 segregation architecture, V48/V49/V50 convergence work, and current OpenGWAS expiry state. | Add a V45-V50 status block and mark OpenGWAS as expired until renewal. |
| `meta/NEXT_ACTIONS.md` | stale canonical actions | Last updated `2026-06-12 17:50 CEST`; first action path remains post-V44 acquisition/readiness. | High: future readers or agents may skip the V47-V50 provenance/push/public-knowledge state. | Add a current V50 next-action block: continue V50 active-time target, push every iteration, keep provenance gate passing, and route around expired OpenGWAS. |
| `knowledge_external/INDEX.md` | current for external layer | Includes V50 records, V50 public-reader path, V50 source prioritization, GWAS fetcher validation, and allele-harmonization prep. | Low: external layer is discoverable once a reader reaches it. | Keep using this as the external-knowledge landing index; do not move external records into grounded status files. |
| `docs/reports/FINDINGS_REPORT_V37.md` | appropriately historical | V37 is the scored findings report, not a live status file. | Low: stale only if misread as live status. | Link it as the authoritative synthesis report, not the current queue. |
| `docs/validation/PREREGISTRATION_V42.md` | appropriately frozen | The Gafson validation plan is intentionally frozen and should not be updated except blind additive diagnostics already committed. | Low: frozen is correct. | Keep immutable for the validation plan; point readers to later readiness/checkpoint files for operational changes. |
| `docs/validation/POWER_MAP_V43.md` | appropriately historical with V49 purge note | Contains the V43 power map and V49 post-purge sufficiency note. | Low: useful method-characterization artifact, not live status. | Link as method behavior, not current phase. |

## Freshness Verdict

The public landing path is **not fresh enough** for a GitHub reader starting at
`README.md`. The external-knowledge index is current, but the main README and
canonical status/action files still present V43/V44 as current. That creates a
navigation error, not a scientific error: the committed later artifacts exist
and are reachable if a reader already knows where to look.

## Minimal Safe Fix Plan

1. Update `README.md` so its `Current Status` section does not hard-code an old
   phase as current.
2. Add compact V44-V50 rows to the README phase ledger.
3. Refresh `meta/CURRENT_STATUS.md` with a V45-V50 operational summary:
   history purge/push reconciliation, returned-package handling, provenance
   segregation, convergence/contradiction content, sharper source records, and
   OpenGWAS-expired routing.
4. Refresh `meta/NEXT_ACTIONS.md` with the active V50 queue, push requirement,
   provenance gate, non-OpenGWAS routes, and pending OpenGWAS renewal.
5. Keep external-context records under `knowledge_external/`; do not copy those
   claims into grounded status prose.

## V50 Boundary

This audit does not itself edit the landing pages. It identifies the stale
public-facing pointers so a later content-cleanup task can update them without
changing any scientific result or evidence class.
