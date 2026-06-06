# Wave102 SEL1L3/FXYD5 Target-Specific Evidence Audit

## Bottom Line

Branch call: `NO_PROMOTABLE_SEL1L3_FXYD5_TARGET_SPECIFIC_EVIDENCE`.

Neither focal accessible survivor clears the minimum target-specific evidence
bar. `SEL1L3` has the cleaner raw tissue-resident expression signal, but it
does not survive as a cross-disease residualized controller and has no real
perturbation, validated model, selective modality, or strong target-resolved
genetic anchor. `FXYD5` has a clearer protein-biophysics story, but the route
is direction-conflicted, safety-limited by epithelial/barrier and Na-K-ATPase
biology, and lacks the same perturbation/genetic anchors.

## Target-Specific Ranking

| gene | wave102_call | wave102_target_score | wave102_gate_count | ms_delta_log2 | ms_p | raw_positive_disease_count | raw_negative_disease_count | residual_retained_positive_disease_count | residual_strict_core_disease_count | response_nonresponse_high_nominal | response_responder_high_nominal | wave81_direct_perturbation | foundation_total_strong_support_contexts | wave62_strong_l2g_disease_count | wave62_strong_qtl_coloc_disease_count | manual_modality_status | manual_direction_status | manual_route_blocker | wave102_missing_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEL1L3 | NO_GO_NO_TARGET_SPECIFIC_PERTURBATION_OR_VALIDATED_MODEL | 14 | 5 | 0.9225 | 0.01814 | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | immature | unknown_driver_vs_architecture_marker | no known ligand/catalytic function, no target-specific perturbation, and no strong autoimmune genetic anchor | residualized_cross_disease;response_direction_support;real_perturbation_or_validated_model;target_resolved_genetic_anchor;modality_ready |
| FXYD5 | NO_GO_NO_TARGET_SPECIFIC_PERTURBATION_OR_VALIDATED_MODEL | 10.75 | 4 | 0.3525 | 0.05871 | 4 | 1 | 2 | 0 | 3 | 1 | 0 | 0 | 0 | 0 | conceptual_but_safety_limited | direction_conflicted_across_response_systems | epithelial/barrier and Na-K-ATPase coupling create liability; Crohn myeloid negative signal conflicts with a pan-autoimmune target | residualized_cross_disease;response_direction_support;real_perturbation_or_validated_model;target_resolved_genetic_anchor;modality_ready;no_safety_blocker |
| CD82 | COMPARATOR_ONLY | 13.5 | 4 | 0.5037 | 0.1729 | 5 | 0 | 1 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | pleiotropic_surface_complex | unresolved | tetraspanin pleiotropy and prior demotion as marker without controller evidence | ms_nominal_anchor;residualized_cross_disease;real_perturbation_or_validated_model;target_resolved_genetic_anchor;modality_ready;no_safety_blocker |
| LAPTM5 | COMPARATOR_ONLY | 13 | 4 | 0.2727 | 0.1304 | 3 | 0 | 0 | 0 | 6 | 1 | 0 | 0 | 0 | 0 | poor_modality | unresolved | lysosomal membrane localization and absent causal perturbation | ms_nominal_anchor;residualized_cross_disease;response_direction_support;real_perturbation_or_validated_model;target_resolved_genetic_anchor;modality_ready |
| APOC1 | COMPARATOR_ONLY | 6.25 | 4 | 0.8063 | 0.03335 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | systemic_lipid_confounded | context_conflicted_lipid_state_marker | systemic lipid metabolism and contradictory tissue directions | residualized_cross_disease;response_direction_support;real_perturbation_or_validated_model;target_resolved_genetic_anchor;modality_ready;no_safety_blocker |

## Focal Raw Contexts

| analysis | disease_name | compartment | role | gene | delta_log2_cpm | hedges_g | p | fdr | positive_nominal | negative_nominal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t1d_endothelial_cell | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | FXYD5 | 0.8897 | 1.197 | 0.0008813 | 0.0955 | True | False |
| t1d_stellate_cell | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | FXYD5 | 0.7827 | 1.384 | 0.03059 | 0.3946 | True | False |
| ibd_uc_epithelial | ulcerative colitis | colon epithelial | tissue_resident | FXYD5 | 2.316 | 1.521 | 0.0322 | 0.2957 | True | False |
| t1d_acinar_cell | type 1 diabetes mellitus | pancreatic acinar cell | tissue_resident | FXYD5 | 1.254 | 0.86 | 0.03999 | 0.5425 | True | False |
| ibd_crohn_epithelial | Crohn disease | colon epithelial | tissue_resident | FXYD5 | 0.8308 | 1.281 | 0.04294 | 0.2734 | True | False |
| psoriasis_keratinocyte | psoriasis | skin keratinocyte | tissue_resident | FXYD5 | 1.398 | 2.948 | 0.0449 | 0.4068 | True | False |
| ibd_crohn_myeloid | Crohn disease | colon myeloid | myeloid_apc | FXYD5 | -0.9786 | -3.137 | 0.0002137 | 0.06523 | False | True |
| ibd_uc_stromal | ulcerative colitis | colon stromal | tissue_resident | SEL1L3 | 2.093 | 2.433 | 0.001037 | 0.08519 | True | False |
| ibd_crohn_stromal | Crohn disease | colon stromal | tissue_resident | SEL1L3 | 1.46 | 1.808 | 0.006965 | 0.4984 | True | False |
| t1d_endothelial_cell | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | SEL1L3 | 1.554 | 1.004 | 0.007568 | 0.2326 | True | False |

## Interpretation

- Raw expression is not the limiting issue. `SEL1L3` and `FXYD5` both recur
  across tissue-resident disease compartments.
- The limiting issue is non-expression anchoring. The residual gate collapses
  the apparent breadth to weak or narrow context support, and neither focal
  candidate has a target-specific perturbation that reverses the
  lipid-lysosomal/inflammatory state.
- Foundation-model rows are retained only as triage evidence. `SEL1L3` has a
  prior model-only supportive row, but it is explicitly marked
  `do_not_promote_from_foundation_model`, so it cannot satisfy perturbation.
- The accessible-survivor route should be closed unless a new wet-lab or public
  perturbation dataset directly perturbs `SEL1L3` or `FXYD5` in the relevant
  stromal/epithelial/endothelial context and shows disease-state reversal
  without barrier toxicity.

## Reproducibility

- Script: `scripts/v3_wave102_sel1l3_fxyd5_target_specific_evidence_audit.py`
- Rank table: `results_v3/wave102_sel1l3_fxyd5_target_specific_evidence_audit/target_specific_evidence_rank.tsv`
- Context rows: `results_v3/wave102_sel1l3_fxyd5_target_specific_evidence_audit/focal_context_rows.tsv`
- Summary: `results_v3/wave102_sel1l3_fxyd5_target_specific_evidence_audit/summary.json`
- Seed: `20260527`
