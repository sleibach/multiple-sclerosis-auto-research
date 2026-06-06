# Wave100 cAMP-Restoration Intervention-Class Audit

## Bottom Line

Branch call: `NO_REOPEN_CAMP_RESTORATION_CLASS`.

The cAMP-restoration class remains a useful comparator but is not promoted as
a V3 therapeutic mechanism. The best biology clues split across incompatible
gates: `ADCY3` has nominal MS white-matter expression and broad genetics but
no selective activation modality or direction proof; `GPR65` and `PTGER4`
carry stronger GPCR/genetic tractability but are prior-art/directionality
blocked; `PDE4B/PDE4D` are pharmacologically reachable but have negative/weak
local L1000 support, no clean MS disease-high anchor, and class toxicity/prior
art.

## Candidate Ranking

| gene | route | wave100_call | wave100_priority_score | critical_gate_count | support_gate_count | ms_delta_log2 | ms_p | raw_positive_disease_count | raw_negative_disease_count | retained_positive_disease_count | wave55_n_genetic_diseases_ge_0_25 | wave62_strong_l2g_disease_count | wave62_strong_qtl_coloc_disease_count | wave62_ms_max_l2g_score | wave62_ms_max_relevant_qtl_h4 | wave37_screen_call | wave37_contrast_fdr | wave18_recommendation | class_l1000_top_hit_rows_matching_core_compounds | missing_critical_gates | manual_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADCY3 | ADCY3_positive_modulation | NO_GO_NO_SELECTIVE_ACTIONABLE_MODALITY | 14 | 3 | 4 | 0.9418 | 0.005839 | 0 | 1 | 0 | 5 | 2 | 2 | 0 | 0 | UNRESOLVED | 0.9971 |  | 0 | cross_disease_cellstate;target_resolved_breadth;ms_genetic_anchor;any_perturbation_or_model;actionable_modality;direction_clear | nominal MS expression and broad genetics make it a biology clue, but gene-high disease expression is not proof that activation is beneficial |
| HCAR3 | HCAR3_agonism | NO_GO_NO_SELECTIVE_ACTIONABLE_MODALITY | 11 | 3 | 3 | 0.171 | 0.7115 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |  | 1 |  | 0 | ms_expression_anchor;target_resolved_breadth;ms_genetic_anchor;any_perturbation_or_model;actionable_modality;direction_clear | less prior-crowded than HCAR2 but lacks disease-cell, MS, genetics, and perturbation support |
| PTGER4 | EP4_contextual_modulation | NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED | 13 | 4 | 5 | 0.2721 | 0.3034 | 2 | 3 | 0 | 9 | 5 | 3 | 0.5559 | 0.9292 | UNRESOLVED | 1 |  | 0 | ms_expression_anchor;cross_disease_cellstate;any_perturbation_or_model;prior_not_blocking;direction_clear | excellent genetics but prostaglandin direction is tissue-dependent and prior V3 marked EP4 direction/prior art as blocking |
| GPR65 | GPR65_acidic_tissue_cAMP_PAM | NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED | 9 | 3 | 4 | 0.09041 | 0.6241 | 1 | 3 | 0 | 5 | 2 | 1 | 0.6238 | 0.9823 | UNRESOLVED | 1 | do_not_promote | 0 | ms_expression_anchor;cross_disease_cellstate;target_resolved_breadth;any_perturbation_or_model;prior_not_blocking;direction_clear | prior V3 GPR65 audit found direct autoimmune/IBD prior art and weak or contradictory local disease-cell support |
| FFAR2 | FFAR2_SCFA_receptor_modulation | NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED | 8 | 3 | 4 | -0.2826 | 0.7481 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | UNRESOLVED | 0.9971 |  | 0 | ms_expression_anchor;target_resolved_breadth;ms_genetic_anchor;any_perturbation_or_model;prior_not_blocking;direction_clear | microbiome/SCFA autoimmunity is crowded and local target-level support is absent |
| PDE4B | PDE4B_selective_inhibition | NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED | 7 | 3 | 4 | -0.4295 | 0.2821 | 4 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | UNRESOLVED | 0.9971 |  | 0 | ms_expression_anchor;target_resolved_breadth;ms_genetic_anchor;any_perturbation_or_model;prior_not_blocking;safety_not_blocking | reachable pharmacology but class is crowded and local MS direction is not disease-high |
| PDE4D | PDE4D_selective_or_sparing_inhibition | NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED | 6 | 3 | 3 | 0.02496 | 0.973 | 4 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | UNRESOLVED | 1 |  | 0 | ms_expression_anchor;target_resolved_breadth;ms_genetic_anchor;any_perturbation_or_model;prior_not_blocking;safety_not_blocking | accessible but not supported by local MS/cross-disease signal and has known class liabilities |
| HCAR2 | HCAR2_agonism | NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED | 6 | 3 | 3 | -0.0849 | 0.8286 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | UNRESOLVED | 0.9971 |  | 0 | ms_expression_anchor;cross_disease_cellstate;target_resolved_breadth;ms_genetic_anchor;any_perturbation_or_model;prior_not_blocking | route is crowded by niacin/fumarate-adjacent MS and inflammatory literature and lacks local disease-state support |
| ADORA2A | A2A_adenosine_agonism | NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED | 0 | 2 | 2 | -0.8775 | 0.3604 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | UNRESOLVED | 1 |  | 0 | ms_expression_anchor;cross_disease_cellstate;target_resolved_breadth;ms_genetic_anchor;any_perturbation_or_model;prior_not_blocking;safety_not_blocking | anti-inflammatory logic is known but broad cardiovascular/CNS and immunosuppressive liabilities block a cross-autoimmune claim here |
| ADORA2B | A2B_adenosine_modulation | NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED | -3 | 1 | 1 | 0.2661 | 0.8047 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | UNRESOLVED | 1 |  | 0 | ms_expression_anchor;cross_disease_cellstate;target_resolved_breadth;ms_genetic_anchor;any_perturbation_or_model;prior_not_blocking;direction_clear;safety_not_blocking | A2B biology is context-dependent and not anchored in local MS/cross-disease signal |

## Class-Level Perturbation Evidence

- LINCS metadata rows matching PDE4/cAMP terms: `85`.
- Unique LINCS perturbagen IDs matching PDE4/cAMP terms: `34`.
- Retrieved L1000FWD opposite-hit rows matching broad PDE4/cAMP terms:
  `2`.
- Retrieved opposite-hit rows matching core compounds
  (`apremilast`, `roflumilast`, `rolipram`, `cilomilast`, `ibudilast`,
  `piclamilast`, `forskolin`, `bucladesine`):
  `0`.

Interpretation: class perturbagens are present in the background LINCS
metadata, but core cAMP/PDE4 compounds are absent from the retrieved disease
signature reversal hits. This is not proof the biology is false; it is a
negative intervention-prioritization signal for the current V3 claim.

## Local Context Rows

Most significant context-level rows for cAMP-route genes:

| gene | disease_name | compartment | role | n_case_donors | n_control_donors | delta_log2_cpm | hedges_g | p | fdr | positive_nominal | negative_nominal | positive_fdr10 | negative_fdr10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADCY3 | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | 5 | 17 | -1.179 | -1.287 | 0.00227 | 0.1477 | False | True | False | False |
| ADCY3 | type 1 diabetes mellitus | pancreatic ductal cell | tissue_resident | 5 | 19 | -0.6354 | -0.8421 | 0.014 | 0.3818 | False | True | False | False |
| ADCY3 | type 1 diabetes mellitus | pancreatic acinar cell | tissue_resident | 5 | 18 | -0.8761 | -0.9475 | 0.06224 | 0.5707 | False | False | False | False |
| ADCY3 | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | 4 | 17 | -0.8828 | -1.103 | 0.06758 | 0.4981 | False | False | False | False |
| ADCY3 | ulcerative colitis | colon stromal | tissue_resident | 6 | 6 | -0.591 | -0.9268 | 0.1168 | 0.4959 | False | False | False | False |
| ADCY3 | psoriasis | skin keratinocyte | tissue_resident | 3 | 3 | 0.7612 | 1.506 | 0.126 | 0.4853 | False | False | False | False |
| ADCY3 | psoriasis | skin APC | myeloid_apc | 3 | 3 | -1.539 | -1.416 | 0.1312 | 0.7297 | False | False | False | False |
| ADCY3 | Crohn disease | colon epithelial | tissue_resident | 6 | 6 | 0.7488 | 0.8155 | 0.1675 | 0.4555 | False | False | False | False |
| ADCY3 | ulcerative colitis | colon myeloid | myeloid_apc | 6 | 6 | -0.9692 | -0.7972 | 0.1849 | 0.5729 | False | False | False | False |
| ADCY3 | psoriasis | skin stromal | tissue_resident | 3 | 3 | 0.7553 | 0.8635 | 0.2705 | 0.7099 | False | False | False | False |
| ADCY3 | Sjogren syndrome | salivary gland epithelial | tissue_resident | 11 | 14 | 0.4293 | 0.4388 | 0.279 | 0.8441 | False | False | False | False |
| ADCY3 | Crohn disease | colon stromal | tissue_resident | 6 | 6 | -0.3285 | -0.5461 | 0.3316 | 0.7744 | False | False | False | False |
| ADCY3 | Crohn disease | colon myeloid | myeloid_apc | 6 | 6 | -0.3516 | -0.5399 | 0.3374 | 0.7006 | False | False | False | False |
| ADCY3 | type 1 diabetes mellitus | pancreatic beta cell | tissue_resident | 3 | 19 | -0.2705 | -0.2854 | 0.5064 | 0.8819 | False | False | False | False |
| ADCY3 | Sjogren syndrome | salivary gland stromal/endothelial | tissue_resident | 10 | 14 | -0.1281 | -0.2175 | 0.6129 | 0.9459 | False | False | False | False |
| ADCY3 | ulcerative colitis | colon epithelial | tissue_resident | 6 | 6 | 0.4213 | 0.2709 | 0.6245 | 0.8429 | False | False | False | False |
| ADCY3 | Sjogren syndrome | salivary gland APC | myeloid_apc | 9 | 13 | 0.3385 | 0.1637 | 0.701 | 0.9878 | False | False | False | False |
| ADORA2A | psoriasis | skin stromal | tissue_resident | 3 | 3 | 0.182 | 2.782 | 0.04499 | 0.5792 | False | False | False | False |
| ADORA2A | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | 5 | 17 | 1.07 | 1.31 | 0.1783 | 0.5851 | False | False | False | False |
| ADORA2A | psoriasis | skin keratinocyte | tissue_resident | 3 | 3 | -0.02837 | -0.5461 | 0.4666 | 0.7304 | False | False | False | False |
| ADORA2A | psoriasis | skin APC | myeloid_apc | 3 | 3 | 0.2075 | 0.2322 | 0.7442 | 0.9266 | False | False | False | False |
| ADORA2B | ulcerative colitis | colon myeloid | myeloid_apc | 6 | 6 | 2.088 | 1.838 | 0.006866 | 0.2006 | True | False | False | False |
| ADORA2B | Crohn disease | colon myeloid | myeloid_apc | 6 | 6 | 1.853 | 1.646 | 0.01255 | 0.2447 | True | False | False | False |
| ADORA2B | ulcerative colitis | colon epithelial | tissue_resident | 6 | 6 | 0.8417 | 1.163 | 0.05408 | 0.3503 | False | False | False | False |
| ADORA2B | psoriasis | skin keratinocyte | tissue_resident | 3 | 3 | -0.846 | -1.518 | 0.0976 | 0.4514 | False | False | False | False |
| ADORA2B | ulcerative colitis | colon stromal | tissue_resident | 6 | 6 | 1.199 | 1.039 | 0.09809 | 0.4685 | False | False | False | False |
| ADORA2B | psoriasis | skin APC | myeloid_apc | 3 | 3 | -1.195 | -1.332 | 0.112 | 0.7297 | False | False | False | False |
| ADORA2B | Crohn disease | colon stromal | tissue_resident | 6 | 6 | 0.8517 | 0.7593 | 0.2025 | 0.7162 | False | False | False | False |
| ADORA2B | type 1 diabetes mellitus | pancreatic endothelial cell | tissue_resident | 5 | 17 | 0.746 | 0.8087 | 0.2158 | 0.6145 | False | False | False | False |
| ADORA2B | type 1 diabetes mellitus | pancreatic stellate cell | tissue_resident | 4 | 17 | 0.4454 | 0.342 | 0.3004 | 0.7251 | False | False | False | False |

## Gate Logic

Promotion required all of: MS expression anchor, cross-disease cell-state
support, target-resolved broad genetics, MS genetic anchor, real perturbation
or model/class reversal support, actionable modality, prior-art clearance,
clear direction, and safety not blocking. No route satisfied that combined
standard.

## Reproducibility

- Script: `scripts/v3_wave100_camp_restoration_class_audit.py`
- Rank table: `results_v3/wave100_camp_restoration_class_audit/camp_restoration_candidate_rank.tsv`
- Context rows: `results_v3/wave100_camp_restoration_class_audit/camp_candidate_context_rows.tsv`
- Summary JSON: `results_v3/wave100_camp_restoration_class_audit/summary.json`
- Seed: `20260527`
