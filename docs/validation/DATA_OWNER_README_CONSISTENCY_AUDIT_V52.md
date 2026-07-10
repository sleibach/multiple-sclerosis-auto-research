# Data Owner README Consistency Audit V52

Date: 2026-07-10

Status: operational audit. This document adds no evidence, changes no validation
rule, and does not authorize any new analysis. It checks that the external-facing
data-owner package guide aligns with the V52 route classifier, field dictionary,
preflight checklist, and handoff bundle.

## Inputs

- Data-owner guide:
  `docs/validation/DATA_OWNER_PACKAGE_README_V52.md`
- Route classifier:
  `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv`
- Field dictionary:
  `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv`
- Preflight checklist:
  `docs/validation/INCOMING_PACKAGE_PREFLIGHT_CHECKLIST_V52.md`
- Handoff bundle:
  `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`

## Summary

The README lists eight human-facing package types. The route classifier lists
nine route classes. The difference is expected: `access_or_terms_blocked` is a
handling state, not a data package type a data owner should choose as a primary
submission category.

No blocking inconsistency was found between README package types and route
classifier classes. One non-blocking documentation gap remains: the
metadata/aggregate-only context route is present in the README and classifier,
but it has no corresponding field-dictionary row.

## Package-Type To Route Mapping

| README package type | README likely route | classifier route class | status |
|---|---|---|---|
| paired DMF-like PBMC response | monitoring validation | `monitoring_validation` | aligned |
| chr1 genotype-linked immune or CSF readout | chr1 target-resolution handoff | `chr1_target_resolution` | aligned |
| chr1 direction-matched perturbation | chr1 modality workup | `chr1_modality_workup` | aligned |
| postpartum MS relapse-window data | secondary biology validation | `postpartum_secondary_biology` | aligned |
| T/B compartment data | secondary monitoring validation | `TB_secondary_monitoring` | aligned |
| treatment-timed expression without response labels | pharmacodynamic context only | `pharmacodynamic_context_only` | aligned |
| protein structure or tractability file | feasibility context only | `structure_context_only` | aligned |
| aggregate paper table or plot | acquisition lead or context only | `metadata_only_or_aggregate_only` | aligned but field dictionary gap |

## Field-Dictionary Coverage

The field dictionary covers the scoreable or semi-scoreable route families:

- `paired_DMF_like_PBMC_response`
- `chr1_genotype_linked_immune_CSF`
- `chr1_direction_matched_perturbation`
- `postpartum_MS_relapse_window`
- `TB_compartment_monitoring`
- `pharmacodynamic_only_DMF_context`
- `structure_only_target_context`

The classifier route `metadata_only_or_aggregate_only` has minimum fields
(`source_description`, `available_fields`, `missing_sample_level_elements`) but
does not yet have a matching field-dictionary entry. This does not affect
scoreable validation because aggregate-only material is context-only or an
acquisition lead, but adding the row would make package intake more mechanical.

## Handoff References

All README "Files To Read Before Sending" references are present in the repo and
are also represented in the handoff-bundle flow:

- `docs/validation/INCOMING_PACKAGE_PREFLIGHT_CHECKLIST_V52.md`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv`
- `docs/validation/MONITORING_MINIMUM_VIABLE_PACKAGE_CHECKLIST_V52.md`
- `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`
- `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`

## Verdict

The data-owner README is operationally consistent with the V52 classifier and
handoff bundle. The only follow-up is to add a field-dictionary entry for the
metadata/aggregate-only route so context-only packages can be documented as
mechanically as scoreable packages.
