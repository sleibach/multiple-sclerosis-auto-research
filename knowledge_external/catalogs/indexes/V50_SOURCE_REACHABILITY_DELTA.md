# V50 Source Reachability Delta

Status: transport-maintenance summary only. HTTP status is not evidence for or
against any external claim.

Input table:
`knowledge_external/catalogs/indexes/external_source_url_reachability.tsv`.

## Summary

- V50-added source records checked: `24`
- direct reachable 2xx: `18`
- reachable redirected 2xx: `3`
- non-success maintenance warnings: `3`
- missing source URLs: `0`

## V50 Transport Warnings

| record | HTTP code | source | maintenance interpretation |
|---|---:|---|---|
| `claim.diebold_2022.dmf_high_dimensional_immune_monitoring_context.2026-06-28` | `403` | https://www.pnas.org/doi/10.1073/pnas.2205042119 | PNAS source blocks the checker transport path; source locator remains useful but should be manually checked before future reuse. |
| `claim.mult_scler_2017.dmf_response_lymphocyte_subsets_ms.2026-06-28` | `403` | https://journals.sagepub.com/doi/10.1177/1352458517703799 | SAGE source blocks the checker transport path; source locator remains useful but should be manually checked before future reuse. |
| `claim.hmg_2019.zmiz1_dendritic_vitamin_d_context.2026-06-28` | `403` | https://academic.oup.com/hmg/article/28/2/269/5115479 | Oxford Academic source blocks the checker transport path; source locator remains useful but should be manually checked before future reuse. |

## Interpretation

The three warnings are transport-level maintenance items, not claim-validity
problems and not contradictions. They should trigger manual source review before
future fuller reuse, but they do not change the V50 convergence/contradiction
matrix.

## Decision

No V50 record needs removal for reachability. Keep all three `403` rows in the
external layer with manual-recheck notes if they are reused in a future source
intake or grounding task.
