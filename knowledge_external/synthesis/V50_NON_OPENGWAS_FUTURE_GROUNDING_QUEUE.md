# V50 Non-OpenGWAS Future-Grounding Queue

Status: future-grounding queue only. These are executable routes, not findings.
HTTP/API reachability is not evidence, and no route below uses OpenGWAS.

## Purpose

V50 confirmed that several public APIs remain usable while the OpenGWAS JWT is
expired. This queue turns those routes into concrete future-grounding tasks with
clear acceptance gates, stop conditions, and evidence boundaries.

Primary inputs:

- `knowledge_external/synthesis/V50_NON_OPENGWAS_ROUTE_INVENTORY.md`
- `analysis/v50_non_opengwas_route_inventory/route_smoke_summary.tsv`
- `scripts/v50_check_non_opengwas_routes.py`
- `analysis/v50_non_opengwas_route_checks/route_check_results.tsv`

## Queue

| priority | route | task | acceptance gate | stop condition | output | boundary |
|---|---|---|---|---|---|---|
| high | GWAS Catalog REST | Allele-harmonize rs1250550, rs4613763, and rs7522462 against project disease/eQTL direction conventions. | Strand/orientation, phenotype mapping, and project effect convention all resolved. | Any unresolved allele orientation or phenotype ambiguity. | Direction-check manifest under `analysis/`; synthesis note under `knowledge_external/`. | Not direction evidence until harmonized. |
| high | Europe PMC REST | Search data-availability statements for exact V22/V32 treatment-response validation or contradiction sources. | Source has paired baseline/early-treatment data, response labels, module-gene coverage, and comparable endpoint definition. | Broad DMF/APC/steroid mention without frozen-score-compatible data. | Source-hit review packet or parking queue. | Literature hit is a candidate only. |
| high | NCBI E-utilities / GDS | Scout GEO/GDS for paired immune-remodeling/JAK-STAT treatment-response cohorts not already used. | Paired timing, labels, and module-gene coverage can be verified from metadata or safe package preview. | Missing labels, missing paired timing, or no module-gene coverage. | Cohort scout addendum; no expression import unless terms and quarantine are satisfied. | Metadata route only until cohort is verified. |
| high | EBI BioStudies API | Search BioStudies/ArrayExpress-style records for low-barrier treatment-response or postpartum MS immune datasets. | Accession has enough metadata to route to a preregistered harness or a validated scout. | Ambiguous access, no labels, or no MS-relevant paired structure. | Candidate-source packet with access tier and required data fields. | Study discovery only. |
| medium | ClinicalTrials.gov API v2 | Map trial endpoints and NEDA/response definitions for validation-readiness context. | Endpoint definition is useful for interpreting a preregistered validation plan. | Trial metadata cannot be mapped to a molecular validation endpoint. | Endpoint-context note. | Clinical metadata is not molecular validation. |
| medium | Open Targets GraphQL | Check target/tractability context for already closed or parked targets, especially PTGER4, GPR25, KIF21B, ZMIZ1, and NAMPT. | Context is source-specific and does not conflict with direction-matched project discipline. | Any output would imply target promotion without project-side direction evidence. | Target-context caution note. | Target-platform context is not a target nomination. |
| medium | ENA Portal API | Resolve raw sequence accession metadata for candidate studies after a paper/GEO/BioStudies route names a specific accession. | Accession is tied to a verified candidate study and terms/access are clear. | Broad keyword search only or no study-level candidate. | Accession metadata manifest; no bulk sequence download. | Raw sequence metadata only. |
| low | Crossref REST | Fill DOI/citation metadata for already accepted source candidates when publisher/PMC metadata is incomplete. | DOI metadata improves provenance for a source already accepted through another route. | Crossref is the only source for a biological claim. | Citation metadata patch. | Bibliographic fallback only. |

## Execution Rules

1. Run `scripts/v50_check_non_opengwas_routes.py check --fail-on-error` before
   starting route-heavy work.
2. Do not call OpenGWAS until the JWT is renewed and verified.
3. Do not count a cohort usable until paired timing, response labels, and
   module-gene coverage are verified.
4. Do not import bulk datasets during route scouting.
5. Store source hits under `knowledge_external/` until a project-grounding
   analysis is committed.
6. If a route produces a same-definition contradiction candidate, route it
   through `knowledge_external/synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md`
   before asserting a relationship.

## Immediate Next Tasks

1. Use GWAS Catalog REST plus the allele-harmonization prep table to resolve
   whether any rsid row is safe for project-direction comparison.
2. Use Europe PMC and NCBI GDS to search specifically for paired
   baseline/early-treatment DMF or immune-remodeling/JAK-STAT response cohorts.
3. Use BioStudies only for accession-level candidates surfaced by the paper/GEO
   route, not broad unsupervised harvesting.

## Provenance

Prepared from V50 route-smoke outputs and route inventory on 2026-06-28. This is
a work queue, not evidence about MS biology.
