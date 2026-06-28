# V50 Source-Terms Gap Audit

Status: source-terms navigation only. This audit reviews optional source-terms
metadata gaps and prioritizes only follow-ups that would change future
source-use decisions. It does not authorize data reuse, add external records,
or alter project findings.

Primary input:

- `knowledge_external/catalogs/indexes/source_terms_coverage_v48.tsv`

## Summary

| metric | count |
|---|---:|
| external records checked | `71` |
| records with source-terms metadata | `40` |
| records missing optional source-terms metadata | `31` |
| missing optional resource/catalog rows | `26` |
| missing optional claim rows | `5` |
| V50 sharper source-specific records missing optional terms | `0` |

Interpretation: the current V50 sharper-source layer is not blocked by
source-terms gaps. The remaining optional gaps are mostly older resource-level
catalog rows. Follow-up should focus on resources likely to be used for future
data retrieval or high-value public navigation.

## High-Value Follow-Ups

| priority | record | source | reason |
|---|---|---|---|
| high | `resource.gwas_catalog.ms.2026-06-13` | https://www.ebi.ac.uk/gwas/ | The public GWAS Catalog is now an active non-OpenGWAS route; resource-level terms should match the V50 claim-level GWAS API rows before broader reuse. |
| high | `resource.msgd.database_commons.2026-06-13` | https://ngdc.cncb.ac.cn/databasecommons/database/id/9285 | MSGD is the closest public MS molecular knowledgebase comparator; source terms matter for any future deeper comparison. |
| high | `resource.msda.catalogue.2026-06-13` | https://msda.emif-catalogue.eu/ | MSDA is a high-value cohort-discovery resource; terms/access review matters before using catalogue metadata beyond navigation. |
| high | `resource.msbase.registry.2026-06-13` | https://www.msbase.org/ | MSBase is clinically deep but application-gated; access/terms need explicit metadata if future cohort-routing work references it. |
| high | `resource.narcoms.registry.2026-06-13` | https://www.narcoms.org/ | NARCOMS is a major registry comparator; terms/access should be explicit before any future registry-route recommendation. |
| medium | `resource.arrayexpress_biostudies.functional_genomics.2026-06-13` | https://www.ebi.ac.uk/arrayexpress/ | Functional-genomics data retrieval route; terms review useful before future source acquisition. |
| medium | `resource.ena.sequence_archive.2026-06-13` | https://www.ebi.ac.uk/ena/browser/ | Raw sequence route; terms/access review useful before future download planning. |
| medium | `resource.europe_pmc.literature.2026-06-13` | https://europepmc.org/ | Literature-mining route; terms review useful for future automated source mining. |
| medium | `resource.open_targets.platform.2026-06-13` | https://platform-docs.opentargets.org/ | Target-knowledge route; terms review useful before fuller target-context reuse. |
| medium | `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` | https://www.nature.com/articles/s41467-021-25768-0 | This and the MS-UC row use the same Nature source; a single source-terms review can cover both V49 relationship rows. |
| medium | `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14` | https://www.nature.com/articles/s41467-021-25768-0 | Same shared Nature source as above; useful because it underpins the external MS-UC backdrop context. |

## Low-Value / Defer

| class | examples | reason to defer |
|---|---|---|
| General repositories not currently used for V50 routing | Dryad, Figshare, OSF, Zenodo | Useful catalog rows, but no immediate source-specific route depends on them. |
| Clinical guideline or patient-facing context rows | NICE, NHS England, National MS Society, MS Society UK, NINDS CDE | Important public context, but current usage is navigation only; terms review can wait until fuller quotation/reuse is needed. |
| Controlled or mixed resources with no active access path | EGA, DISGENET, IMSGC resource page | Terms review is less useful until a specific dataset/API route is selected. |
| Disease-course claim rows | RRMS/SPMS/PPMS context records | Low risk and low decision impact; keep as optional until public-reader clinical-context pages are expanded. |

## Current V50-Specific Status

All source-specific records added in V50 that are actively used for
convergence/contradiction, validation-context, or GWAS routing have at least
metadata-only source-terms metadata. Examples include:

- GWAS Catalog rsid claim rows;
- Gafson/GSE235357/DMF treatment-response context rows;
- steroid/glucocorticoid and composition context rows;
- coupled APC, EBV, Crohn, PTGER4, KIF21B, GPR25, and ZMIZ1 rows.

Therefore, no V50 relationship row needs to be downgraded for source-terms
coverage.

## Decision

Do not spend broad effort filling every optional source-terms gap. Prioritize
the five high-value resource rows first, then the shared Nature MS-IBD source if
future summaries quote or reuse it more deeply. Keep all other gaps as
`missing_optional` until a concrete future task depends on fuller reuse.
