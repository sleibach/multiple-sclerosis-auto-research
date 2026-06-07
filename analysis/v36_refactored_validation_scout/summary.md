# V36 Refactored Validation Scout

Status: **completed_from_existing_v24_inventory**.

Purpose: reinterpret V24 treatment-response cohort candidates under the stricter
V36 validation spec.

## V36 Validation Spec

The refactored lead now requires, ideally:

- baseline plus early on-treatment transcriptomics, preferably W8-like;
- response labels;
- IFN/APC, STAT1-axis, glycolysis, glucocorticoid, and composition modules;
- batch/lane/capture-date or processing metadata where available;
- raw-matrix QC metrics, including mitochondrial fraction and preferably ambient
  RNA estimates;
- compartment or cell-level readouts if possible.

## Candidate Re-Ranking

| Rank | Source | V36 fit | Access | Verdict |
|---:|---|---|---|---|
| 1 | Gafson et al. 2018 DMF PBMC RNA-seq, PMID `30283812` | Best fit: MS, DMF, baseline/6w/15m, NEDA-4 response. 6w is close to the V36 early-window requirement. Need batch/QC/steroid metadata in request. | Tier 2 author/data request | **Best next validation target**. |
| 2 | `GSE130478/GSE130491/GSE130494` Karolinska DMF ROS cohort | MS DMF and longitudinal, but expression is baseline/6m CD4 T-cell and response labels absent. Timing is less ideal than Gafson. | Public expression, Tier 2 labels | Secondary MS validation if labels obtained. |
| 3 | `GSE85034_MTX` unused methotrexate arm | Open/local and response-labeled, but psoriasis lesional skin, week16, same study family as used ADA arm. Poor V36 early-window and tissue fit. | Tier 1 local | Secondary stress test only, not primary validation. |
| 4 | `GSE253495` RA upadacitinib CD14 monocytes | JAK-class pharmacodynamic context and cell-type specific, but n=3 and all improved, no responder/nonresponder discrimination. | Tier 1 open | Mechanistic context only. |

## Updated Human Request For Gafson

Request processed and/or raw PBMC RNA-seq counts plus:

- sample-to-patient map for baseline, 6 weeks, and 15 months;
- NEDA-4 responder status and relapse/MRI/disability components if available;
- DMT timing and concomitant steroid/glucocorticoid exposure;
- batch/lane/library prep/run date or other processing metadata;
- QC metrics: library size, mapping rate, mitochondrial/ribosomal fractions if
  available;
- cell-count or deconvolution covariates if available.

## Bottom Line

Under V36, the validation target did not change, but the required metadata did.
Gafson remains the highest-leverage next dataset. Without batch/QC/steroid
metadata, it can still test the primary locked V22 score, but it cannot fully
resolve the strongest V36 caveats.
