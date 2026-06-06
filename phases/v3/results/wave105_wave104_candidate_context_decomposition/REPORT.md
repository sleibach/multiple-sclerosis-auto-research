# Wave105 Wave104 Candidate Context Decomposition

## Bottom Line

This wave decomposes the Wave104 genetics-first sidecar set by disease,
compartment, response state, and residual support. It does not nominate a
target by itself.

## Context Calls

```json
{
  "CONTROL_PRIOR_ART_OR_KNOWN_IMMUNE_AXIS": 2,
  "PARK_RAW_RECURRENCE_RESIDUAL_WEAK": 1,
  "PARK_STATE_SUPPORTED_BUT_ROUTE_BLOCKED": 2
}
```

## Candidate Summary

| gene | wave105_context_call | wave105_context_reason | wave104_call | wave104_missing_gates | positive_disease_count_broad | positive_diseases_broad | myeloid_positive_disease_count_broad | tissue_resident_positive_context_count_broad | retained_positive_disease_count | best_retained_residual_tests | nonresponse_high_contexts | ms_wm_delta_log2 | ms_wm_p | route_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IFI30 | PARK_STATE_SUPPORTED_BUT_ROUTE_BLOCKED | State evidence exists but prior, modality, or direction remains blocking. | PARK_GENETICS_STATE_DIRECTION_NO_MODALITY | reachable_modality;prior_or_safety | 3 | psoriasis;type 1 diabetes mellitus;ulcerative colitis | 2 | 0 | 1 | ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|myeloid_apc:delta=0.764,p=0.0366,fdr=0.503 | 4 | 0.2102 | 0.3799 | NO_GO_DIRECT_ANTIGEN_PROCESSING_HOST_DEFENSE_AND_POOR_DRUGGABILITY |
| IL7R | CONTROL_PRIOR_ART_OR_KNOWN_IMMUNE_AXIS | Useful comparator, not a novel target in this run. | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | prior_or_safety | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 2 | 0 | 2 | ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|myeloid_apc:delta=3.16,p=0.00115,fdr=0.293; ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|myeloid_apc:delta=2.96,p=0.00198,fdr=0.323; ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|myeloid_apc:delta=2.2,p=0.00255,fdr=0.329; ibd_uc_myeloid\|ulcerative colitis\|colon myeloid\|myeloid_apc:delta=3.12,p=0.00383,fdr=0.358; ibd_uc_stromal\|ulcerative colitis\|colon stromal\|tissue_resident:delta=2.03,p=0.00404,fdr=0.359; ibd_uc_stromal\|ulcerative colitis\|colon stromal\|tissue_resident:delta=2.17,p=0.0065,fdr=0.398 |  |  |  |  |
| SP140 | PARK_STATE_SUPPORTED_BUT_ROUTE_BLOCKED | State evidence exists but prior, modality, or direction remains blocking. | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | prior_or_safety | 4 | Crohn disease;Sjogren syndrome;psoriasis;ulcerative colitis | 2 | 0 | 1 | ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|myeloid_apc:delta=0.255,p=0.0146,fdr=0.439; ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|myeloid_apc:delta=0.284,p=0.0157,fdr=0.443; ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|myeloid_apc:delta=0.262,p=0.0251,fdr=0.477; ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|myeloid_apc:delta=0.24,p=0.0261,fdr=0.48; ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|myeloid_apc:delta=0.246,p=0.0289,fdr=0.488; ibd_crohn_myeloid\|Crohn disease\|colon myeloid\|myeloid_apc:delta=0.209,p=0.0463,fdr=0.53 |  |  |  |  |
| GALC | PARK_RAW_RECURRENCE_RESIDUAL_WEAK | Raw cross-disease recurrence exists but residual support is absent or weak. | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | directional_or_perturbation_support;prior_or_safety | 3 | psoriasis;type 1 diabetes mellitus;ulcerative colitis | 1 | 0 | 0 |  |  |  |  |  |
| CD58 | CONTROL_PRIOR_ART_OR_KNOWN_IMMUNE_AXIS | Useful comparator, not a novel target in this run. | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | directional_or_perturbation_support;reachable_modality;prior_or_safety | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 2 | 0 | 0 |  |  |  |  |  |

## Interpretation

- A target-resolved genetic signal is only useful here if it lands in the
  cross-disease lipid/myeloid disease state after compartment and residual
  checks.
- Raw recurrence without residual retention is treated as dispatch material,
  not as mechanism.
- Known immune axes are retained as calibration controls, not as novelty
  candidates.

## Reproducibility

- Script: `scripts/v3_wave105_wave104_candidate_context_decomposition.py`
- Summary: `results_v3/wave105_wave104_candidate_context_decomposition/wave104_candidate_context_summary.tsv`
- Seed: `20260527`
