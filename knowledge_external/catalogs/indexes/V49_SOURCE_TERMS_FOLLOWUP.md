# V49 Source-Terms Follow-Up

Status: source-terms navigation only. This document crosschecks V49
source-domain review decisions against the V48 source-terms queue. It does not
authorize reuse beyond metadata-only cataloging.

Boundary: V48 `SOURCE_TERMS_REVIEW_QUEUE_V48.md` tracks records missing a
`source_terms` object. The eight V49-added records now have conservative
metadata-only `source_terms`, so they are not missing-object queue failures.
They still require row-specific review before fuller use of text, tables,
figures, datasets, detailed methods, or quantitative source fields.

## Summary

- V49 records checked: `8`
- missing `source_terms` object: `0`
- safe for current metadata-only use: `8`
- fuller-reuse terms review needed before tables/figures/extended text: `4`
- access/terms parking before fuller reuse: `1`
- no fuller-reuse action unless future work needs source details: `3`

## Follow-Up Table

| record | source domain | V48 queue status | V49 fuller-reuse decision | required follow-up before fuller reuse |
|---|---|---|---|---|
| `claim.science.ebv_ms_longitudinal_risk_context.2026-06-14` | `pubmed.ncbi.nlm.nih.gov` | Not in missing-object queue; has metadata-only terms. | `metadata_ok_no_parking` | None unless future grounding needs cohort-level source details. |
| `claim.nature.ms_ibd_gpr25_context.2026-06-14` | `pmc.ncbi.nlm.nih.gov` | Not in missing-object queue; has metadata-only terms. | `metadata_ok_terms_review_before_full_reuse` | Review source-specific PMC/license terms before copying tables, figures, or extended text. |
| `claim.frontiers.uc_tofacitinib_mhc_stat1_context.2026-06-14` | `pmc.ncbi.nlm.nih.gov` | Not in missing-object queue; has metadata-only terms. | `metadata_ok_terms_review_before_full_reuse` | Review source-specific PMC/license terms before copying tables, figures, or extended text. |
| `claim.probast_tripod.prediction_model_validation_context.2026-06-14` | `pubmed.ncbi.nlm.nih.gov` | Not in missing-object queue; has metadata-only terms. | `metadata_ok_no_parking` | None unless future governance text needs direct PROBAST/TRIPOD details. |
| `claim.open_targets.direction_tractability_context.2026-06-14` | `www.annualreviews.org` | Not in missing-object queue; has metadata-only terms. | `metadata_ok_access_terms_parking_before_full_reuse` | Park for access/terms review before full text, figures, tables, or detailed method extraction. |
| `claim.plos.ms_mhc_independent_effects_context.2026-06-14` | `pmc.ncbi.nlm.nih.gov` | Not in missing-object queue; has metadata-only terms. | `metadata_ok_terms_review_before_full_reuse` | Review source-specific PMC/license terms before copying tables, figures, or extended text. |
| `claim.cshperspect.ms_biomarker_heterogeneity_context.2026-06-14` | `pmc.ncbi.nlm.nih.gov` | Not in missing-object queue; has metadata-only terms. | `metadata_ok_terms_review_before_full_reuse` | Review source-specific PMC/license terms before copying tables, figures, or extended text. |
| `claim.ard.ra_sle_pregnancy_transcriptome_context.2026-06-14` | `pubmed.ncbi.nlm.nih.gov` | Not in missing-object queue; has metadata-only terms. | `metadata_ok_no_parking` | None unless future work imports the underlying dataset or extracts detailed protocol fields. |

## Decision

Do not add the V49 records back into the missing-object source-terms queue.
Their current metadata-only use is already conservatively marked. Instead, use
this follow-up table when a future session proposes deeper reuse.

