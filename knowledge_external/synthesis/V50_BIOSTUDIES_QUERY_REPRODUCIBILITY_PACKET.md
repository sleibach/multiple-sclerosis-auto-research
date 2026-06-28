# V50 BioStudies Query Reproducibility Packet

Status: source-search reproducibility packet. This artifact records the exact
BioStudies / ArrayExpress-style metadata queries used in the V50 treatment-
response source search. It is navigation only, not biological evidence, and it
does not make any cohort usable without the V50 same-definition gates.

## Generated Outputs

| artifact | purpose |
|---|---|
| `analysis/v50_biostudies_query_reproducibility/biostudies_query_packet.tsv` | Exact query strings, encoded API URLs, recorded hit counts, top accessions, and manual-review outcomes by query. |
| `analysis/v50_biostudies_query_reproducibility/summary.json` | Machine-readable count summary for the query packet. |
| `scripts/v50_build_biostudies_query_packet.py` | Reproducible generator for the TSV/JSON packet. |

## Search Boundary

The packet records `8` BioStudies metadata queries against:

`https://www.ebi.ac.uk/biostudies/api/v1/search`

The V50 run recorded `80` raw hits, `56` deduplicated hits, `6` manual-review
rows, and `0` verified exact paired early-treatment V22/V32 validation cohort
candidates. The query packet is intended to prevent duplicated route-search
labor and to make future reruns comparable to the committed V50 result.

## Reuse Rule

Future source scouts should not rerun these queries merely to rediscover the
same near-misses. Rerun only if a release, source locator, access-terms change,
or new same-definition candidate appears. Any candidate then goes through:

- `knowledge_external/templates/V50_NON_OPENGWAS_SOURCE_HIT_REVIEW_TEMPLATE.md`
- `knowledge_external/templates/V50_SOURCE_HIT_NO_RECOUNT_CHECKER.md`

## Provenance

Prepared from committed V50 BioStudies metadata-search outputs. Source:
`docs/knowledge/EPISTEMIC_CLASSES.md`; API route:
`https://www.ebi.ac.uk/biostudies/api/v1/search`; source search artifact:
`knowledge_external/synthesis/V50_BIOSTUDIES_TREATMENT_RESPONSE_SEARCH.md`.
