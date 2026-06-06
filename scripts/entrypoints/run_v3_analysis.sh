#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-./.venv_v3_py312/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="./.venv/bin/python"
fi

"$PYTHON_BIN" scripts/v3_download_foundation_outputs.py
"$PYTHON_BIN" scripts/v3_prioritize_module_nodes.py
"$PYTHON_BIN" scripts/v3_rank_axes_from_disease_evidence.py
"$PYTHON_BIN" scripts/v3_analyze_gse111972_microglia.py
"$PYTHON_BIN" scripts/v3_prior_art_intervention_audit.py
"$PYTHON_BIN" scripts/v3_druggability_audit.py
"$PYTHON_BIN" scripts/v3_l1000fwd_reversal.py
"$PYTHON_BIN" scripts/v3_pde4_camp_l1000_audit.py
"$PYTHON_BIN" scripts/v3_model_ifng_apc_feedback.py
if [[ -s data/raw_v3/gse253006/GSE253006_RAW.tar && -s data/raw_v3/gse253006/GSE253006_family.soft ]]; then
  "$PYTHON_BIN" scripts/v3_analyze_gse253006_tofacitinib_uc.py
  if [[ -d data/raw_v3/gse253006/raw ]]; then
    "$PYTHON_BIN" scripts/v3_analyze_gse253006_tofacitinib_marker_compartments.py
  else
    echo "Skipping GSE253006 marker-compartment tofacitinib analysis: extracted raw matrices not present"
  fi
else
  echo "Skipping GSE253006 tofacitinib UC analysis: raw tar or family SOFT metadata not present"
fi
if [[ -s data/raw_v3/mixscale/DE_results_all_pathway.zip ]]; then
  "$PYTHON_BIN" scripts/v3_analyze_mixscale_perturbseq.py
  "$PYTHON_BIN" scripts/v3_rank_mixscale_transition_controllers.py
else
  echo "Skipping Mixscale perturb-seq analysis: DE_results_all_pathway.zip not present"
fi
if [[ -s data/raw_v3/cell_state/ibd_human_10x.h5ad && -s data/raw_v3/cell_state/psoriasis_skin.h5ad ]]; then
  "$PYTHON_BIN" scripts/v3_analyze_direct_h5ad_cell_states.py
  "$PYTHON_BIN" scripts/v3_analyze_direct_h5ad_gene_replication.py
else
  echo "Skipping direct h5ad cell-state analysis: IBD and psoriasis h5ad files not present"
fi
if [[ "${RUN_SLE_CENSUS_TARGETED:-0}" == "1" ]]; then
  "$PYTHON_BIN" scripts/v3_analyze_sle_census_targeted.py
else
  echo "Skipping targeted SLE Census extraction: set RUN_SLE_CENSUS_TARGETED=1 to run the remote selected-gene path"
fi
"$PYTHON_BIN" scripts/v3_wave5_quant_osmr_complement.py
"$PYTHON_BIN" scripts/v3_analyze_osmr_complement_axes.py
"$PYTHON_BIN" scripts/v3_broad_h5ad_gene_discovery.py
"$PYTHON_BIN" scripts/v3_lgals3_glycan_checkpoint_analysis.py
"$PYTHON_BIN" scripts/v3_pivot_panel_triage.py
"$PYTHON_BIN" scripts/v3_unrestricted_survivor_scan.py
if [[ -s data/raw_v3/gse248205/processed/C1/C1_matrix.mtx.gz && -s data/raw_v3/gse248205/processed/HT1/HT1_matrix.mtx.gz ]]; then
  "$PYTHON_BIN" scripts/v3_analyze_gse248205_thyroid_spatial.py
else
  echo "Skipping GSE248205 thyroid spatial analysis: extracted processed Visium matrices not present"
fi
if [[ -s data/raw_v3/gse315138/GSE315138_RAW.tar && -s data/raw_v3/gse315138/raw/GSE315138_Celiac-a2_matrix.mtx.gz ]]; then
  "$PYTHON_BIN" scripts/v3_analyze_gse315138_celiac_marker_compartments.py
else
  echo "Skipping GSE315138 celiac marker-compartment analysis: raw matrices not present"
fi
if [[ -s data/raw_v3/gse227835/filelist.txt ]]; then
  "$PYTHON_BIN" scripts/v3_wave14_gse227835_myasthenia_marker.py
else
  echo "Skipping GSE227835 myasthenia marker-compartment analysis: GEO file list not present"
fi
"$PYTHON_BIN" scripts/v3_residualize_antigen_processing_vs_ifn.py
"$PYTHON_BIN" scripts/v3_residualize_lipa_vs_stress.py
"$PYTHON_BIN" scripts/v3_snx10_c15orf48_residual_gate.py
"$PYTHON_BIN" scripts/v3_broad_residual_gate.py
if [[ "${RUN_CELLXGENE_CENSUS:-0}" == "1" ]]; then
  "$PYTHON_BIN" scripts/v3_analyze_cellxgene_cross_autoimmune.py
else
  echo "Skipping CELLxGENE Census expression query: set RUN_CELLXGENE_CENSUS=1 to run the fragile remote path"
fi
if [[ -s data/raw_v3/state_parse_split4/CD14_Mono_pred_de.csv && -s data/raw_v3/state_parse_split4/CD14_Mono_real_de.csv && -s phases/v3/tmp/var_dims_split4.pkl ]]; then
  "$PYTHON_BIN" scripts/v3_analyze_state_parse_cd14.py
else
  echo "Skipping State CD14 analysis: released prediction/real files not present"
fi
if [[ -s phases/v3/tmp/foundation_wave6/geneformer_assets/Geneformer-V2-104M/model.safetensors ]]; then
  "$PYTHON_BIN" scripts/v3_geneformer_candidate_delete_screen.py
  "$PYTHON_BIN" scripts/v3_geneformer_phagolysosomal_matrix_screen.py
  "$PYTHON_BIN" scripts/v3_geneformer_pivot_panel_screen.py
  "$PYTHON_BIN" scripts/v3_geneformer_unrestricted_survivor_screen.py
  "$PYTHON_BIN" scripts/v3_geneformer_broad_residual_screen.py
  "$PYTHON_BIN" scripts/v3_wave14_geneformer_narrowed_candidate_screen.py
  "$PYTHON_BIN" scripts/v3_wave15_geneformer_loader_dependency_screen.py
  "$PYTHON_BIN" scripts/v3_pivot_panel_triage.py
  "$PYTHON_BIN" scripts/v3_unrestricted_survivor_scan.py
else
  echo "Skipping Geneformer candidate deletion screen: local Geneformer V2-104M weights not present"
fi
"$PYTHON_BIN" scripts/v3_build_cross_disease_convergence_tables.py
"$PYTHON_BIN" scripts/v3_rank_central_and_intervention_candidates.py
"$PYTHON_BIN" scripts/v3_wave14_candidate_gate_matrix.py
"$PYTHON_BIN" scripts/v3_wave14_negative_regulator_feedback_test.py
"$PYTHON_BIN" scripts/v3_post_critique_candidate_status.py
"$PYTHON_BIN" scripts/v3_wave14_target_level_genetics.py
"$PYTHON_BIN" scripts/v3_wave15_surface_trafficking_dependency.py
"$PYTHON_BIN" scripts/v3_wave15_orchestrator_dependency_scan.py
"$PYTHON_BIN" scripts/v3_wave15_loader_external_gate.py
"$PYTHON_BIN" scripts/v3_wave15_perturbation_drug_response.py
"$PYTHON_BIN" scripts/v3_wave16_ctsh_chembl_feasibility.py
"$PYTHON_BIN" scripts/v3_wave16_ctsh_chemistry_selectivity.py
"$PYTHON_BIN" scripts/v3_wave17_mediator_route_gate.py
"$PYTHON_BIN" scripts/v3_wave18_accessible_target_rescue.py
"$PYTHON_BIN" scripts/v3_wave18_foundation_rescue.py
"$PYTHON_BIN" scripts/v3_wave18_treatment_response_scout.py
"$PYTHON_BIN" scripts/v3_wave19_tolerogenic_checkpoint.py
"$PYTHON_BIN" scripts/v3_wave19_lysosomal_controller.py
"$PYTHON_BIN" scripts/v3_wave19_orchestrator_controller_triage.py
"$PYTHON_BIN" scripts/v3_wave20_unrestricted_survivor.py
"$PYTHON_BIN" scripts/v3_wave20_genetic_druggable_altaxis.py
"$PYTHON_BIN" scripts/v3_wave20_orchestrator_unrestricted_triage.py
"$PYTHON_BIN" scripts/v3_wave20_c15orf48_ndufa4_switch.py
"$PYTHON_BIN" scripts/v3_wave21_residual_druggability_scan.py
"$PYTHON_BIN" scripts/v3_wave22_sqle_failfast.py
"$PYTHON_BIN" scripts/v3_wave23_orchestrator_nonexpression_axis_triage.py
"$PYTHON_BIN" scripts/v3_wave24_l1000_recurrent_reversal_triage.py
"$PYTHON_BIN" scripts/v3_wave25_causal_genetics_module_proxy.py
"$PYTHON_BIN" scripts/v3_wave26_treatment_response_strict_audit.py
"$PYTHON_BIN" scripts/v3_wave27_l1000_unknown_deconvolution.py
"$PYTHON_BIN" scripts/v3_wave28_target_first_rescue.py
"$PYTHON_BIN" scripts/v3_wave29_ptpn2_restoration_model.py
"$PYTHON_BIN" scripts/v3_wave30_niche_driver_audit.py
"$PYTHON_BIN" scripts/v3_wave31_dynamic_transition_controller_audit.py
"$PYTHON_BIN" scripts/v3_wave32_resolution_rescue_audit.py
"$PYTHON_BIN" scripts/v3_wave32c_resolution_prior_art_audit.py
"$PYTHON_BIN" scripts/v3_wave33_tolerance_costimulation_audit.py
"$PYTHON_BIN" scripts/v3_wave34_genetics_expression_druggability_scan.py
"$PYTHON_BIN" scripts/v3_wave34a_genetics_first_target_rescue.py
"$PYTHON_BIN" scripts/v3_wave35_resolution_perturbation_analysis.py
"$PYTHON_BIN" scripts/v3_wave36a_gene_level_controller_rescue.py
"$PYTHON_BIN" scripts/v3_wave37_gse212008_crispr_efferocytosis_screen.py
"$PYTHON_BIN" scripts/v3_wave38_crispr_state_druggability_rescue.py
"$PYTHON_BIN" scripts/v3_wave39_surfaceome_rescue_after_resolution_pivot.py
"$PYTHON_BIN" scripts/v3_wave40_parked_surface_failfast.py
"$PYTHON_BIN" scripts/v3_wave41_l1000_external_unknown_deconvolution.py
"$PYTHON_BIN" scripts/v3_wave42_fads_lipid_desaturation_axis.py
"$PYTHON_BIN" scripts/v3_wave43_genetic_druggable_failfast.py
"$PYTHON_BIN" scripts/v3_wave44_cfb_complement_stratification_audit.py
"$PYTHON_BIN" scripts/v3_wave45_regulatory_controller_audit.py
"$PYTHON_BIN" scripts/v3_wave46_central_axis_closure_audit.py
"$PYTHON_BIN" scripts/v3_wave47_late_stage_survivor_map.py
"$PYTHON_BIN" scripts/v3_wave48_resolution_reopener_audit.py
"$PYTHON_BIN" scripts/v3_wave49_ptpn22_directionality_audit.py
"$PYTHON_BIN" scripts/v3_wave50_gpr65_acid_sensing_gpcr_audit.py
"$PYTHON_BIN" scripts/v3_wave51_reachable_stromal_surface_audit.py
"$PYTHON_BIN" scripts/v3_wave52_remaining_mechanistic_reopeners.py
"$PYTHON_BIN" scripts/v3_wave53_perturbation_first_pivot.py
"$PYTHON_BIN" scripts/v3_wave54_mfge8_debris_opsonin_audit.py
"$PYTHON_BIN" scripts/v3_wave55_external_genetics_druggability_sweep.py
"$PYTHON_BIN" scripts/v3_wave56_sp140_targeted_reopener_audit.py
"$PYTHON_BIN" scripts/v3_wave56k_sp140_perturbation_druggability_audit.py
"$PYTHON_BIN" scripts/v3_wave57_intervention_first_geneformer_screen.py
"$PYTHON_BIN" scripts/v3_wave58_cxcr2_il7r_targeted_audit.py
"$PYTHON_BIN" scripts/v3_wave59_lysosomal_sphingolipid_model_reopener_audit.py
"$PYTHON_BIN" scripts/v3_wave60_circuit_coupling_pivot.py
"$PYTHON_BIN" scripts/v3_wave61_intervention_guardrail_scorer.py
"$PYTHON_BIN" scripts/v3_wave62_opentargets_target_resolution.py
"$PYTHON_BIN" scripts/v3_wave63_transition_controller_integrator.py
"$PYTHON_BIN" scripts/v3_wave64_slamf7_perturbation_audit.py
"$PYTHON_BIN" scripts/v3_wave65_gse198520_ra_synovium_antitnf_audit.py
"$PYTHON_BIN" scripts/v3_wave66_metabolomics_class_convergence.py
"$PYTHON_BIN" scripts/v3_wave67_gse282122_myeloid_pseudobulk.py
"$PYTHON_BIN" scripts/v3_wave68_gse282122_unrestricted_gene_screen.py
"$PYTHON_BIN" scripts/v3_wave69_parked_controller_rank.py
"$PYTHON_BIN" scripts/v3_wave69d_gse282122_geneformer_remission_centroid.py
"$PYTHON_BIN" scripts/v3_wave70_fc_ros_resolution_matrix.py
"$PYTHON_BIN" scripts/v3_wave70b_fc_ros_computational_scout.py
"$PYTHON_BIN" scripts/v3_wave70c_inhibitory_receptor_geneformer_direction.py
"$PYTHON_BIN" scripts/v3_wave71_global_survivor_meta_rank.py
"$PYTHON_BIN" scripts/v3_wave72_lipid_mediator_intervention_scout.py
"$PYTHON_BIN" scripts/v3_wave73_p2rx7_stratification_test.py
"$PYTHON_BIN" scripts/v3_wave74_gpr183_oxysterol_niche.py
"$PYTHON_BIN" scripts/v3_wave74_ephx2_direct_ratio_audit.py
"$PYTHON_BIN" scripts/v3_wave74_ephx2_oxylipin_specificity.py
"$PYTHON_BIN" scripts/v3_wave75_ets2_macrophage_program_audit.py
"$PYTHON_BIN" scripts/v3_wave75_response_state_stratification.py
"$PYTHON_BIN" scripts/v3_wave76_adjusted_response_specificity.py
"$PYTHON_BIN" scripts/v3_wave77_ets2_macrophage_axis_audit.py
"$PYTHON_BIN" scripts/v3_wave78_lilrb_family_target_audit.py
"$PYTHON_BIN" scripts/v3_wave78_lilrb_inhibitory_receptor_audit.py
"$PYTHON_BIN" scripts/v3_wave79_targetability_shortlist_audit.py
"$PYTHON_BIN" scripts/v3_wave79_targetability_shortlist_residual_audit.py
"$PYTHON_BIN" scripts/v3_wave80_cd58_cd2_axis_deepening.py
"$PYTHON_BIN" scripts/v3_wave80_cd58_synapse_closure.py
"$PYTHON_BIN" scripts/v3_wave81_perturbation_first_rescue.py
"$PYTHON_BIN" scripts/v3_wave82_parked_perturbation_intervention_audit.py
"$PYTHON_BIN" scripts/v3_wave82_parked_intervention_route_audit.py
"$PYTHON_BIN" scripts/v3_wave83_intervention_class_first_scan.py
"$PYTHON_BIN" scripts/v3_wave84_stratification_first_audit.py
"$PYTHON_BIN" scripts/v3_wave84_response_prediction_audit.py
"$PYTHON_BIN" scripts/v3_wave83_intervention_class_meta_rank.py
"$PYTHON_BIN" scripts/v3_wave85_external_geo_antitnf_validation.py
"$PYTHON_BIN" scripts/v3_wave86_external_geo_antitnf_gene_driver.py
"$PYTHON_BIN" scripts/v3_wave87_cross_system_antitnf_resistance_gene_check.py
"$PYTHON_BIN" scripts/v3_wave87_inflammatory_nonresponse_circuit_audit.py
"$PYTHON_BIN" scripts/v3_wave88_antitnf_nonresponse_covariate_falsification.py
"$PYTHON_BIN" scripts/v3_wave89_psoriasis_gse85034_response_validation.py
"$PYTHON_BIN" scripts/v3_wave90_lpl_cross_disease_audit.py
"$PYTHON_BIN" scripts/v3_wave91_lipid_lysosomal_module_intervention_rank.py
"$PYTHON_BIN" scripts/v3_wave92_lipid_state_controller_route_audit.py
"$PYTHON_BIN" scripts/v3_wave91_lipid_neighborhood_controller_scan.py
"$PYTHON_BIN" scripts/v3_wave92_fabp5_prior_art_audit.py
"$PYTHON_BIN" scripts/v3_wave93_gpr183_oxysterol_forcing_test.py
"$PYTHON_BIN" scripts/v3_wave94_accessible_state_rerank.py
"$PYTHON_BIN" scripts/v3_wave95_cd300_vs_accessible_top_forcing_triage.py
"$PYTHON_BIN" scripts/v3_wave95_mechanistic_forcing_triage.py
"$PYTHON_BIN" scripts/v3_wave96_c15orf48_controller_search.py
"$PYTHON_BIN" scripts/v3_wave97_c15_residual_costate_falsification.py
"$PYTHON_BIN" scripts/v3_wave98_c15_successor_perturbation_first_audit.py
"$PYTHON_BIN" scripts/v3_wave98_ccl20_ccr6_forcing_audit.py
"$PYTHON_BIN" scripts/v3_wave99_endogenous_inflammasome_brake_audit.py
"$PYTHON_BIN" scripts/v3_wave99_litaf_casp4_stress_generator_audit.py
"$PYTHON_BIN" scripts/v3_wave100_camp_restoration_class_audit.py
"$PYTHON_BIN" scripts/v3_wave101_accessible_survivor_forcing_triage.py
"$PYTHON_BIN" scripts/v3_wave102_accessible_survivor_residual_compartment_test.py
"$PYTHON_BIN" scripts/v3_wave103_fc_receptor_efferocytosis_route_audit.py
"$PYTHON_BIN" scripts/v3_wave104_accessible_survivor_niche_controller_test.py
"$PYTHON_BIN" scripts/v3_wave105_cd82_niche_robustness_audit.py
"$PYTHON_BIN" scripts/v3_wave106_cd82_specificity_confounder_audit.py
"$PYTHON_BIN" scripts/v3_wave107_cd82_multiplicity_disease_collapse_audit.py
"$PYTHON_BIN" scripts/v3_wave108_mfge8_debris_opsonin_safety_window_model.py
"$PYTHON_BIN" scripts/v3_wave109_mfge8_threshold_sensitivity_audit.py
"$PYTHON_BIN" scripts/v3_wave110_post_closure_intervention_route_map.py
"$PYTHON_BIN" scripts/v3_wave111_gpr183_spatial_proxy_forcing_test.py
"$PYTHON_BIN" scripts/v3_wave112_gpr183_compartment_contrast_fallback.py
"$PYTHON_BIN" scripts/v3_wave113_psap_recurrence_specificity_audit.py
"$PYTHON_BIN" scripts/v3_wave114_p2rx7_target_level_closure_audit.py
"$PYTHON_BIN" scripts/v3_wave115_spns1_controller_falsification_audit.py
"$PYTHON_BIN" scripts/v3_wave116_closure_aware_route_rerank.py
"$PYTHON_BIN" scripts/v3_wave117_park7_stress_route_forcing_test.py
"$PYTHON_BIN" scripts/v3_wave118_dab2_cd9_efferocytosis_directionality_audit.py
"$PYTHON_BIN" scripts/v3_wave119_wave110_remaining_survivor_prefilter.py
"$PYTHON_BIN" scripts/v3_wave120_ephx2_target_pd_coherence_closure.py
"$PYTHON_BIN" scripts/v3_wave121_final_wetlab_only_route_closure.py
"$PYTHON_BIN" scripts/v3_wave122_fresh_breadth_target_scan.py
"$PYTHON_BIN" scripts/v3_wave123_sidecar_candidate_kill_audit.py
"$PYTHON_BIN" scripts/v3_wave124_ncf2_nox2_strict_closure_audit.py
"$PYTHON_BIN" scripts/v3_wave125_mechanism_class_failure_map.py
"$PYTHON_BIN" scripts/v3_wave126_l1000_upstream_regulator_reopener.py
"$PYTHON_BIN" scripts/v3_wave128_genetics_first_reopener.py
"$PYTHON_BIN" scripts/v3_wave129_response_stratification_salvage.py
"$PYTHON_BIN" scripts/v3_wave102_sel1l3_fxyd5_target_specific_evidence_audit.py
"$PYTHON_BIN" scripts/v3_wave103_intervention_first_successor_triage.py
"$PYTHON_BIN" scripts/v3_wave102_sel1l3_fxyd5_residual_controller_test.py
"$PYTHON_BIN" scripts/v3_wave103_sender_to_myeloid_bridge_scan.py
"$PYTHON_BIN" scripts/v3_wave104_genetics_first_lipid_state_convergence_audit.py
"$PYTHON_BIN" scripts/v3_wave105_wave104_candidate_context_decomposition.py
"$PYTHON_BIN" scripts/v3_wave130_ms_treatment_response_audit.py
"$PYTHON_BIN" scripts/v3_wave131_class_route_forcing_audit.py
"$PYTHON_BIN" scripts/v3_wave132_gpr183_post_wave130_closure.py
"$PYTHON_BIN" scripts/v3_wave133_closure_hygiene_correction.py
"$PYTHON_BIN" scripts/v3_wave134_dap_strict_reopen_audit.py
"$PYTHON_BIN" scripts/v3_wave135_lipid_flux_ms_response_sensitivity.py
"$PYTHON_BIN" scripts/v3_wave136_leukotriene_axis_strict_route_audit.py
"$PYTHON_BIN" scripts/v3_wave137_gpr183_ligand_axis_fair_closure.py
"$PYTHON_BIN" scripts/v3_wave138_postcritique_residual_fresh_route_map.py
"$PYTHON_BIN" scripts/v3_wave139_residual_marker_falsification_integrator.py
"$PYTHON_BIN" scripts/v3_wave140_target_first_pivot_audit.py
"$PYTHON_BIN" scripts/v3_wave141_modality_first_successor_scan.py
"$PYTHON_BIN" scripts/v3_wave142_sender_bridge_strict_pivot_audit.py
"$PYTHON_BIN" scripts/v3_wave143_cd58_cd2_adaptive_synapse_forcing.py
"$PYTHON_BIN" scripts/v3_wave144_bcell_complement_architecture_audit.py
"$PYTHON_BIN" scripts/v3_wave145_strict_route_inventory.py
"$PYTHON_BIN" scripts/v3_wave146_architecture_first_barrier_retention_scan.py
"$PYTHON_BIN" scripts/v3_wave147_tagap_adaptive_genetics_benchmark.py
"$PYTHON_BIN" scripts/v3_wave148_tnfsf14_light_lymphoid_niche_audit.py
"$PYTHON_BIN" scripts/v3_wave149_metabolite_barrier_strict_reaudit.py
"$PYTHON_BIN" scripts/v3_wave150_repurposing_first_strict_audit.py
"$PYTHON_BIN" scripts/v3_wave151_interface_cell_perturbation_first_audit.py
"$PYTHON_BIN" scripts/v3_wave152_external_interface_perturbation_module_test.py
"$PYTHON_BIN" scripts/v3_wave153_gse129487_synovial_fibroblast_sirna_rescue.py
"$PYTHON_BIN" scripts/v3_wave154_cux1_consistency_guardrail.py
"$PYTHON_BIN" scripts/v3_wave155_cux1_gene_specificity_vs_stat.py
"$PYTHON_BIN" scripts/v3_wave156_elr_chemokine_intervention_audit.py
"$PYTHON_BIN" scripts/v3_wave157_elr_state_biomarker_responsiveness.py
"$PYTHON_BIN" scripts/v3_wave158_tnfil17_synergy_controller_closure.py
"$PYTHON_BIN" scripts/v3_wave159_tweak_fn14_interface_audit.py
"$PYTHON_BIN" scripts/v3_wave160_lifr_interface_rescue_guardrail.py
"$PYTHON_BIN" scripts/v3_wave161_post_interface_route_reprioritization.py
"$PYTHON_BIN" scripts/v3_wave162_fpr2_anxa1_response_state_killtest.py
"$PYTHON_BIN" scripts/v3_wave163_cd300_receptor_specific_closure.py
"$PYTHON_BIN" scripts/v3_wave164_genetics_first_survivor_audit.py
"$PYTHON_BIN" scripts/v3_wave165_inava_nod_ripk_neighbor_audit.py
"$PYTHON_BIN" scripts/v3_wave166_same_gene_genetics_cellstate_overlap.py
"$PYTHON_BIN" scripts/v3_wave167_shadow_no_label_overlap.py
"$PYTHON_BIN" scripts/v3_wave168_efferocytosis_state_controller_pivot.py
"$PYTHON_BIN" scripts/v3_wave169_l1000_repurposing_deconvolution_pivot.py
"$PYTHON_BIN" scripts/v3_wave170_external_chembl_target_quality.py
