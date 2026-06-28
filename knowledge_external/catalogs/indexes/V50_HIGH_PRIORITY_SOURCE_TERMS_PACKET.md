# V50 High-Priority Source-Terms Follow-Up Packet

Status: source-terms review packet only. This artifact does not assert current
license terms, authorize reuse, add project evidence, or change any grounded
finding. It packages the five high-priority resource rows identified in
`knowledge_external/catalogs/indexes/V50_SOURCE_TERMS_GAP_AUDIT.md` for future
operator review.

## Scope

Task 46 found `31` optional source-terms metadata gaps, mostly older
resource-level catalog rows. V50 should not fill every optional gap. This packet
selects the five high-value resources whose terms/access metadata matters most
for near-term public navigation or future source routing.

## Review Packet

| priority | record_id | resource | current source locator | record file | current access tier | why review first | required review action | safe outcome labels | marker |
|---|---|---|---|---|---|---|---|---|---|
| high | `resource.gwas_catalog.ms.2026-06-13` | NHGRI-EBI GWAS Catalog | https://www.ebi.ac.uk/gwas/ | `knowledge_external/catalogs/resources/gwas_catalog_multiple_sclerosis.json` | `open` | Active non-OpenGWAS genetics route in V50; resource-level terms should be explicit before broader API reuse. | Locate official terms/licensing/API-use page; record citation guidance, redistribution boundary, and API/data-download reuse boundary. | `terms_added_metadata_only`, `needs_manual_terms_review`, `do_not_redistribute_bulk_data` | `NOT_PROJECT_GROUNDED` |
| high | `resource.msgd.database_commons.2026-06-13` | MSGD / Multiple Sclerosis Gene Database | https://ngdc.cncb.ac.cn/databasecommons/database/id/9285 | `knowledge_external/catalogs/resources/msgd_database_commons.json` | `open` | Closest public MS molecular knowledgebase comparator; deeper comparison needs explicit source-use boundary. | Locate MSGD/database terms or citation page; record whether entry-level metadata can be summarized and whether bulk extraction is allowed. | `terms_added_metadata_only`, `needs_manual_terms_review`, `park_bulk_reuse_until_terms_clear` | `NOT_PROJECT_GROUNDED` |
| high | `resource.msda.catalogue.2026-06-13` | MS Data Alliance Catalogue | https://msda.emif-catalogue.eu/ | `knowledge_external/catalogs/resources/msda_catalogue.json` | `registration` | High-value cohort-discovery route; future recommendations should separate public metadata browsing from dataset access. | Locate catalogue terms, account requirements, metadata reuse/citation rules, and data-access governance notes. | `terms_added_metadata_only`, `registration_required`, `dataset_access_not_granted_by_catalogue` | `NOT_PROJECT_GROUNDED` |
| high | `resource.msbase.registry.2026-06-13` | MSBase Registry | https://www.msbase.org/ | `knowledge_external/catalogs/resources/msbase_registry.json` | `application` | Clinically deep registry comparator; any future cohort-route language must not imply public data availability. | Locate access/application terms and publication/collaboration policy; record that registry analyses require external approval unless source states otherwise. | `terms_added_metadata_only`, `application_required`, `no_public_participant_data_reuse` | `NOT_PROJECT_GROUNDED` |
| high | `resource.narcoms.registry.2026-06-13` | NARCOMS Registry | https://www.narcoms.org/ | `knowledge_external/catalogs/resources/narcoms_registry.json` | `application` | Major patient-reported longitudinal registry comparator; terms matter before recommending any registry-derived route. | Locate researcher-access, data-use, citation, and participant-data governance terms. | `terms_added_metadata_only`, `application_required`, `no_public_participant_data_reuse` | `NOT_PROJECT_GROUNDED` |

## Operator Steps

For each row:

1. Open only the official resource domain or official documentation linked from
   the current source locator.
2. Find a terms, license, citation, API-use, access, or data-use page.
3. If terms are clear, add a conservative `source_terms` block to the resource
   JSON with:
   - `terms_url`
   - `checked_date`
   - `license_or_terms_label`
   - `allowed_project_use`
   - `redistribution_boundary`
   - `notes`
4. If terms are not clear, leave the resource JSON unchanged and record
   `needs_manual_terms_review` in a follow-up note.
5. Do not import participant-level data, bulk datasets, or large resource dumps
   as part of source-terms review.
6. Re-run the source-terms freshness and provenance gates after any metadata
   change.

## Explicit Non-Actions

- Do not treat open website reachability as data-reuse permission.
- Do not infer registry data access from public website access.
- Do not add source terms by guessing from the hosting institution.
- Do not move resource metadata into project-grounded trees.
- Do not use these resources as evidence for project findings unless a later
  committed grounding analysis tests a specific claim.

## Optional Next Tier

After the five high-priority resource rows are resolved, the next useful
source-terms follow-up is the shared Nature Communications MS-IBD source used by:

- `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14`
- `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14`

This is lower priority than the five resources above because V50 currently uses
the Nature source as citation-level context, not as a reusable data route.

## Provenance

- Primary input:
  `knowledge_external/catalogs/indexes/V50_SOURCE_TERMS_GAP_AUDIT.md`
- Prior packet:
  `knowledge_external/catalogs/indexes/HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md`
- Resource records:
  `knowledge_external/catalogs/resources/gwas_catalog_multiple_sclerosis.json`,
  `knowledge_external/catalogs/resources/msgd_database_commons.json`,
  `knowledge_external/catalogs/resources/msda_catalogue.json`,
  `knowledge_external/catalogs/resources/msbase_registry.json`,
  `knowledge_external/catalogs/resources/narcoms_registry.json`

Date prepared: 2026-06-28.
