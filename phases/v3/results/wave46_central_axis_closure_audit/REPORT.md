# Wave46 Central Axis Closure Audit

## Result

The original central IFN/HLA-II/lysosomal antigen-processing axes remain biologically central but none is a promotable V3 therapeutic finding. Upstream IFN/JAK control is too generic/prior-arted; CD74/HLA-II is a biomarker state; CIITA/RFX5 is undruggable transcriptional machinery; IFI30 and CTSS are downstream lysosomal effectors whose modeled perturbation does not control the upstream transition, with IFI30 lacking mature chemical matter and CTSS blocked by prior art.

## Axis Calls

| candidate | final_call | central_conclusion | target_level_genetics_call | model_intervention | model_min_ifn_apc_log2fc | model_min_hla_cd74_log2fc | model_min_gilt_log2fc | primary_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IFNGR_JAK_STAT1_upstream_control | NO_GO_GENERIC_IFN_JAK_CONTROL | central_but_not_novel_or_selective | not_available_in_wave14_truth_table | ifngr_jak_70pct_suppression | -1.1225420423803392 | -0.6376888887217607 | -0.6350027796060569 | Upstream control is quantitatively real but collapses into broad JAK/IFN immunosuppression and prior-arted approved-class biology. |
| CD74_HLAII_receptor_APC_state_biomarker | NO_GO_BIOMARKER_NOT_TARGET | state_biomarker_not_intervention | no_go |  |  |  |  | Cell-state signal is strong, but CD74/HLA-II is better as a stratification readout than a selective therapeutic handle; direct CD74/MIF and HLA-II targeting are prior-arted and biologically broad. |
| CIITA_RFX5_HLAII_transcriptional_gate | NO_GO_HLAII_TF_GATE_UNDRUGGABLE | mechanistically_narrow_but_undruggable | no_go |  |  |  |  | Perturbation can narrow HLA-II output, but the practical targets are transcription-factor/enhanceosome machinery without a current selective clinical modality or target-level genetics. |
| IFI30_GILT_lysosomal_feedback_effector | NO_GO_IFI30_DOWNSTREAM_AND_UNTRACTABLE | downstream_effector_not_transition_controller | not_available_in_wave14_truth_table | ifi30_95pct_suppression | -0.1818996931239732 | -0.059897105215123 | -0.5575242293338812 | Even extreme modeled IFI30 suppression mostly changes the GILT/lysosomal readout and fails to shut down the upstream IFN/APC or HLA-II/CD74 transition; chemical matter is immature and prior art already covers broad IFI30/GILT autoimmunity. |
| CTSS_cathepsinS_lysosomal_effector | NO_GO_CTSS_PRIOR_ART_DOWNSTREAM_EFFECTOR | druggable_comparator_but_blocked | not_available_in_wave14_truth_table | ctss_70pct_suppression | -7.705985188157834e-09 | -4.541777100398571e-09 | -0.3064183217708471 | CTSS is druggable and mechanistically adjacent, but modeled downstream suppression does not control the transition and autoimmune cathepsin-S inhibitor prior art/clinical history undercuts novelty and feasibility. |

## DoD Gate Matrix

| candidate | dod_gate | status | reason |
| --- | --- | --- | --- |
| IFNGR_JAK_STAT1_upstream_control | specific_cross_autoimmune_mechanism | pass_mechanistic_axis | The axis is biologically coherent and central enough to audit. |
| IFNGR_JAK_STAT1_upstream_control | breadth_coverage_and_cell_state | partial | Cell-state evidence exists for the module, but target-specific disease breadth is inconsistent or confounded. |
| IFNGR_JAK_STAT1_upstream_control | cross_disease_genetic_anchoring | fail | No target-resolved coloc/MR package across four diseases. |
| IFNGR_JAK_STAT1_upstream_control | foundation_or_real_perturbation | fail | upstream_suppression_reduces_all_three_readouts_but_is_generic |
| IFNGR_JAK_STAT1_upstream_control | intervention_druggability_selectivity | fail | Upstream control is quantitatively real but collapses into broad JAK/IFN immunosuppression and prior-arted approved-class biology. |
| IFNGR_JAK_STAT1_upstream_control | verified_novelty_or_prior_art | fail | Prior V3 novelty/prior-art gates blocked this route or reduced it to comparator/biomarker status. |
| IFNGR_JAK_STAT1_upstream_control | therapeutic_feasibility | fail | Upstream control is quantitatively real but collapses into broad JAK/IFN immunosuppression and prior-arted approved-class biology. |
| CD74_HLAII_receptor_APC_state_biomarker | specific_cross_autoimmune_mechanism | pass_mechanistic_axis | The axis is biologically coherent and central enough to audit. |
| CD74_HLAII_receptor_APC_state_biomarker | breadth_coverage_and_cell_state | partial | Cell-state evidence exists for the module, but target-specific disease breadth is inconsistent or confounded. |
| CD74_HLAII_receptor_APC_state_biomarker | cross_disease_genetic_anchoring | fail | no disease genetic locus evidence in supplied OT credible-set rows; GTEx cis-eQTL exists but full SNP-level eQTL summary stats were not downloaded; no paired disease GWAS summary stats and eQTL/pQTL summary files were available locally for multi-signal coloc; OpenGWAS endpoint returned auth barrier in this run; local GWAS Catalog parquet lacks an installed reader; candidate is close to HLA-II state biology but lacks target-level disease genetics |
| CD74_HLAII_receptor_APC_state_biomarker | foundation_or_real_perturbation | fail | not_directly_modeled |
| CD74_HLAII_receptor_APC_state_biomarker | intervention_druggability_selectivity | fail | Cell-state signal is strong, but CD74/HLA-II is better as a stratification readout than a selective therapeutic handle; direct CD74/MIF and HLA-II targeting are prior-arted and biologically broad. |
| CD74_HLAII_receptor_APC_state_biomarker | verified_novelty_or_prior_art | fail | Prior V3 novelty/prior-art gates blocked this route or reduced it to comparator/biomarker status. |
| CD74_HLAII_receptor_APC_state_biomarker | therapeutic_feasibility | fail | Cell-state signal is strong, but CD74/HLA-II is better as a stratification readout than a selective therapeutic handle; direct CD74/MIF and HLA-II targeting are prior-arted and biologically broad. |
| CIITA_RFX5_HLAII_transcriptional_gate | specific_cross_autoimmune_mechanism | pass_mechanistic_axis | The axis is biologically coherent and central enough to audit. |
| CIITA_RFX5_HLAII_transcriptional_gate | breadth_coverage_and_cell_state | partial | Cell-state evidence exists for the module, but target-specific disease breadth is inconsistent or confounded. |
| CIITA_RFX5_HLAII_transcriptional_gate | cross_disease_genetic_anchoring | fail | GWAS Catalog top associations were seen, but no supplied Open Targets credible-set support was present; GTEx cis-eQTL exists but full SNP-level eQTL summary stats were not downloaded; no paired disease GWAS summary stats and eQTL/pQTL summary files were available locally for multi-signal coloc; OpenGWAS endpoint returned auth barrier in this run; local GWAS Catalog parquet lacks an installed reader; candidate is close to HLA-II state biology but lacks target-level disease genetics \| no disease genetic locus evidence in supplied OT credible-set rows; GTEx cis-eQTL exists but full SNP-level eQTL summary stats were not downloaded; no paired disease GWAS summary stats and eQTL/pQTL summary files were available locally for multi-signal coloc; OpenGWAS endpoint returned auth barrier in this run; local GWAS Catalog parquet lacks an installed reader; candidate is close to HLA-II state biology but lacks target-level disease genetics |
| CIITA_RFX5_HLAII_transcriptional_gate | foundation_or_real_perturbation | fail | not_directly_modeled |
| CIITA_RFX5_HLAII_transcriptional_gate | intervention_druggability_selectivity | fail | Perturbation can narrow HLA-II output, but the practical targets are transcription-factor/enhanceosome machinery without a current selective clinical modality or target-level genetics. |
| CIITA_RFX5_HLAII_transcriptional_gate | verified_novelty_or_prior_art | fail | Prior V3 novelty/prior-art gates blocked this route or reduced it to comparator/biomarker status. |
| CIITA_RFX5_HLAII_transcriptional_gate | therapeutic_feasibility | fail | Perturbation can narrow HLA-II output, but the practical targets are transcription-factor/enhanceosome machinery without a current selective clinical modality or target-level genetics. |
| IFI30_GILT_lysosomal_feedback_effector | specific_cross_autoimmune_mechanism | pass_mechanistic_axis | The axis is biologically coherent and central enough to audit. |
| IFI30_GILT_lysosomal_feedback_effector | breadth_coverage_and_cell_state | partial | Cell-state evidence exists for the module, but target-specific disease breadth is inconsistent or confounded. |
| IFI30_GILT_lysosomal_feedback_effector | cross_disease_genetic_anchoring | fail | No target-resolved coloc/MR package across four diseases. |
| IFI30_GILT_lysosomal_feedback_effector | foundation_or_real_perturbation | fail | extreme_IFI30_suppression_is_mostly_lysosomal_and_weak_on_IFN_HLA_state |
| IFI30_GILT_lysosomal_feedback_effector | intervention_druggability_selectivity | fail | Even extreme modeled IFI30 suppression mostly changes the GILT/lysosomal readout and fails to shut down the upstream IFN/APC or HLA-II/CD74 transition; chemical matter is immature and prior art already covers broad IFI30/GILT autoimmunity. |
| IFI30_GILT_lysosomal_feedback_effector | verified_novelty_or_prior_art | fail | Prior V3 novelty/prior-art gates blocked this route or reduced it to comparator/biomarker status. |
| IFI30_GILT_lysosomal_feedback_effector | therapeutic_feasibility | fail | Even extreme modeled IFI30 suppression mostly changes the GILT/lysosomal readout and fails to shut down the upstream IFN/APC or HLA-II/CD74 transition; chemical matter is immature and prior art already covers broad IFI30/GILT autoimmunity. |
| CTSS_cathepsinS_lysosomal_effector | specific_cross_autoimmune_mechanism | pass_mechanistic_axis | The axis is biologically coherent and central enough to audit. |
| CTSS_cathepsinS_lysosomal_effector | breadth_coverage_and_cell_state | partial | Cell-state evidence exists for the module, but target-specific disease breadth is inconsistent or confounded. |
| CTSS_cathepsinS_lysosomal_effector | cross_disease_genetic_anchoring | fail | No target-resolved coloc/MR package across four diseases. |
| CTSS_cathepsinS_lysosomal_effector | foundation_or_real_perturbation | fail | CTSS_suppression_is_lysosomal_only_with_no_IFN_HLA_state_control |
| CTSS_cathepsinS_lysosomal_effector | intervention_druggability_selectivity | fail | CTSS is druggable and mechanistically adjacent, but modeled downstream suppression does not control the transition and autoimmune cathepsin-S inhibitor prior art/clinical history undercuts novelty and feasibility. |
| CTSS_cathepsinS_lysosomal_effector | verified_novelty_or_prior_art | fail | Prior V3 novelty/prior-art gates blocked this route or reduced it to comparator/biomarker status. |
| CTSS_cathepsinS_lysosomal_effector | therapeutic_feasibility | fail | CTSS is druggable and mechanistically adjacent, but modeled downstream suppression does not control the transition and autoimmune cathepsin-S inhibitor prior art/clinical history undercuts novelty and feasibility. |

