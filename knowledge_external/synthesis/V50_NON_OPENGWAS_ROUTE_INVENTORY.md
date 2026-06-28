# V50 Non-OpenGWAS External API Route Inventory

Status: routing and transport/schema inventory only. This artifact does not add
external claims, does not validate any project finding, and does not use
OpenGWAS. It identifies public routes that remain executable while the OpenGWAS
JWT is expired.

## Why This Exists

OpenGWAS access is disabled in V50 because the JWT expired on
`2026-06-19T12:28:39Z`. Work that depends on OpenGWAS must wait for renewal.
This inventory lists public non-OpenGWAS routes that can still support source
discovery, metadata checks, external-record sharpening, and future grounding
preparation without producing false OpenGWAS nulls.

Machine-readable smoke summary:

- `analysis/v50_non_opengwas_route_inventory/route_smoke_summary.tsv`
- `analysis/v50_non_opengwas_route_inventory/summary.json`

## Smoke-Tested Routes

| route | service | method | status | V50-safe use | boundary |
|---|---|---|---|---|---|
| `gwas_catalog_association_by_rsid` | NHGRI-EBI GWAS Catalog REST | GET | ready | Fetch association metadata for queued rsids; already used by `scripts/v50_fetch_gwas_catalog_associations.py`. | Association metadata only until allele harmonization and project-side effect conventions are resolved. |
| `europe_pmc_search` | Europe PMC REST | GET | ready | Literature and data-availability mining. | Search hits are source candidates, not findings. |
| `ncbi_eutils_geo_search` | NCBI E-utilities GDS | GET | ready | GEO/GDS dataset discovery without importing expression data. | A dataset is not usable until paired structure, labels, and module-gene coverage are verified. |
| `biostudies_search` | EBI BioStudies API | GET | ready | BioStudies / ArrayExpress-style study discovery. | Metadata only until source terms and dataset structure are reviewed. |
| `clinicaltrials_v2_search` | ClinicalTrials.gov API v2 | GET | ready | Trial, endpoint, intervention, and cohort context. | Clinical trial metadata is context, not molecular validation. |
| `crossref_works_search` | Crossref REST | GET | ready | DOI and bibliographic fallback lookup. | Use publisher, PMC, or database source pages for actual source intake when possible. |
| `opentargets_graphql_search` | Open Targets Platform GraphQL | POST | ready with schema caution | Target/pathway context and tractability lookup. | Initial `query=` argument failed; use GraphQL `queryString`. Target context is not project evidence. |
| `ena_portal_study_search` | ENA Portal API | GET | ready with query-syntax caution | Raw sequence study discovery. | Broad quoted free-text query failed; fielded query works. Do not download bulk sequence data during route scouting. |

## Failed-Then-Corrected Checks

| service | first failure | correction |
|---|---|---|
| Open Targets GraphQL | HTTP `400`; `search` requires `queryString`, not `query`. | POST GraphQL body using `search(queryString: "multiple sclerosis")`. |
| ENA Portal API | HTTP `400`; broad quoted free-text query format invalid. | Use a fielded query such as `study_title="multiple sclerosis"`. |

## Priority Order While OpenGWAS Is Expired

1. GWAS Catalog REST for already queued rsid metadata routes.
2. Europe PMC plus NCBI E-utilities for published-paper and GEO/GDS cohort
   discovery.
3. BioStudies / ArrayExpress-style metadata search for study-level routes.
4. ClinicalTrials.gov for endpoint and cohort-context checks.
5. Open Targets for target/tractability context only.
6. ENA for raw sequence discovery only when a concrete accession route exists.
7. Crossref as a DOI fallback, not as a primary evidence source.

## Non-Actions

- Do not call OpenGWAS until the JWT is renewed.
- Do not treat HTTP `200` as evidence for any biological claim.
- Do not import large/bulk datasets during route scouting.
- Do not count a cohort usable until paired timing, response labels, and module
  gene coverage are verified.
- Do not treat target-platform context as direction-matched druggability.

## Provenance

Smoke checks were run on 2026-06-28 with lightweight public API calls and no
OpenGWAS endpoint use. Outputs are stored in:

- `analysis/v50_non_opengwas_route_inventory/summary.json`
- `analysis/v50_non_opengwas_route_inventory/route_smoke_summary.tsv`

Source locators checked:

- https://www.ebi.ac.uk/gwas/
- https://www.ebi.ac.uk/europepmc/
- https://eutils.ncbi.nlm.nih.gov/
- https://www.ebi.ac.uk/biostudies/
- https://clinicaltrials.gov/data-api/api
- https://api.crossref.org/
- https://api.platform.opentargets.org/api/v4/graphql
- https://www.ebi.ac.uk/ena/portal/api/
