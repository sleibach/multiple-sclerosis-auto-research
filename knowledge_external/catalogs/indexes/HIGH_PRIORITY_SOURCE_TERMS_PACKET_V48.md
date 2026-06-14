# V48 High-Priority Source-Terms Review Packet

Status: source-terms triage only. This packet does not grant reuse permission, validate external claims, or move any external source into the grounded project layer.

- high-priority records: `9`
- missing record paths: `0`
- missing NOT_PROJECT_GROUNDED markers: `0`

## Review Targets

| record | type | class | domain | review class | source | path | next step |
|---|---|---|---|---|---|---|---|
| `resource.disgenet.platform.2026-06-13` | `external_resource_catalog` | `external-unverifiable` | disgenet.com | `mixed_commercial_or_registration_access` | https://disgenet.com/ | `knowledge_external/catalogs/resources/disgenet_platform.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |
| `resource.ega.controlled_genomics.2026-06-13` | `external_resource_catalog` | `external-unverifiable` | ega-archive.org | `controlled_access_biomedical_archive` | https://ega-archive.org/ | `knowledge_external/catalogs/resources/ega_controlled_genomics.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |
| `resource.europe_pmc.literature.2026-06-13` | `external_resource_catalog` | `external-unverifiable` | europepmc.org | `manual_review_domain` | https://europepmc.org/ | `knowledge_external/catalogs/resources/europe_pmc_literature.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |
| `resource.imsgc.publications.2026-06-13` | `external_resource_catalog` | `external-unverifiable` | imsgc.net | `manual_review_domain` | https://imsgc.net/publications/ | `knowledge_external/catalogs/resources/imsgc_publications.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |
| `resource.msda.catalogue.2026-06-13` | `external_resource_catalog` | `external-unverifiable` | msda.emif-catalogue.eu | `registration_or_catalog_access` | https://msda.emif-catalogue.eu/ | `knowledge_external/catalogs/resources/msda_catalogue.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |
| `resource.msbase.registry.2026-06-13` | `external_resource_catalog` | `external-unverifiable` | www.msbase.org | `application_or_registry_access` | https://www.msbase.org/ | `knowledge_external/catalogs/resources/msbase_registry.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |
| `resource.narcoms.registry.2026-06-13` | `external_resource_catalog` | `external-unverifiable` | www.narcoms.org | `application_or_registry_access` | https://www.narcoms.org/ | `knowledge_external/catalogs/resources/narcoms_registry.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |
| `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` | `external_claim` | `external-unverifiable` | www.nature.com | `publisher_literature` | https://www.nature.com/articles/s41467-021-25768-0 | `knowledge_external/records/ms_ibd_treatment_transfer_caution_context.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |
| `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14` | `external_claim` | `external-unverifiable` | www.nature.com | `publisher_literature` | https://www.nature.com/articles/s41467-021-25768-0 | `knowledge_external/records/ms_uc_greater_genetic_correlation_context.json` | Check source terms URL and add conservative source_terms metadata, or leave missing_optional if terms cannot be stated safely. |

## Boundary

- Every row remains external-classed and `NOT_PROJECT_GROUNDED`.
- Add source_terms metadata only when terms can be stated conservatively from a source.
- If terms remain ambiguous, leave the record in review rather than inventing permission.
