# Wave71-A Global Survivor Meta-Rank

Random seed: `20260527`. No new external data were fetched.

## Decision

No candidate meets the Wave71-A reopen threshold.

The threshold required non-blocked convergence across genetics, perturbation, and modality channels. Closed Fc/ROS, JAK/SYK/BTK/PI3K, checkpoint/costimulation, ACSL1, NAMPT, SP140, LILRB2, and INPP5D branches were explicitly blocked.

## Top 10 After Guardrails

|gene|wave71_call|meta_score|evidence_channel_count|genetics_channel_count|perturbation_channel_count|modality_channel_count|wave71_reason|
|---|---|---|---|---|---|---|---|
|CD58|NO_REOPEN_INSUFFICIENT_CONVERGENCE|3.787943|4|4|1|2|insufficient_independent_convergence_after_guardrails|
|CARMIL1|NO_REOPEN_INSUFFICIENT_CONVERGENCE|2.3844|2|2|0|2|insufficient_independent_convergence_after_guardrails|
|RAD51B|NO_REOPEN_INSUFFICIENT_CONVERGENCE|2.24585|2|2|0|2|insufficient_independent_convergence_after_guardrails|
|PARK7|NO_REOPEN_INSUFFICIENT_CONVERGENCE|1.79705|2|2|0|2|insufficient_independent_convergence_after_guardrails|
|ADCY3|NO_REOPEN_INSUFFICIENT_CONVERGENCE|1.5905|2|2|0|2|insufficient_independent_convergence_after_guardrails|
|FADS1|NO_REOPEN_INSUFFICIENT_CONVERGENCE|1.2898|1|1|0|1|insufficient_independent_convergence_after_guardrails|
|CCDC88B|NO_REOPEN_INSUFFICIENT_CONVERGENCE|1.2711|1|1|0|1|insufficient_independent_convergence_after_guardrails|
|PRR5L|NO_REOPEN_INSUFFICIENT_CONVERGENCE|1.2711|1|1|0|1|insufficient_independent_convergence_after_guardrails|
|YDJC|NO_REOPEN_INSUFFICIENT_CONVERGENCE|1.2711|1|1|0|1|insufficient_independent_convergence_after_guardrails|
|ARID5B|NO_REOPEN_INSUFFICIENT_CONVERGENCE|1.24645|1|1|0|1|insufficient_independent_convergence_after_guardrails|


## Top 10 Evidence And Blockers

|gene|evidence_channels|top_calls|blockers|
|---|---|---|---|
|CD58|external_genetics;genetics_expression_druggability;target_resolution;unrestricted_gene_screen|PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE; PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE; DESCRIPTIVE_GENE_SIGNAL; NO_G...|gate_druggable_surface; gate_perturbation_or_model; cross_disease_target_resolved; broad_genetic_support; strict_residual_or_ms...|
|CARMIL1|external_genetics;genetics_expression_druggability|PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE|gate_druggable_surface; gate_perturbation_or_model|
|RAD51B|external_genetics;genetics_expression_druggability|PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE|gate_druggable_surface; gate_perturbation_or_model|
|PARK7|external_genetics;genetics_expression_druggability|PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE|gate_druggable_surface; gate_perturbation_or_model|
|ADCY3|external_genetics;genetics_expression_druggability|PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE|gate_druggable_surface; gate_perturbation_or_model|
|FADS1|genetics_expression_druggability|PARK_GENETIC_DRUGGABLE_NEEDS_CELL_STATE|gate_local_cell_state; gate_perturbation_or_model|
|CCDC88B|genetics_expression_druggability|PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE|gate_druggable_surface; gate_perturbation_or_model|
|PRR5L|genetics_expression_druggability|PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE|gate_druggable_surface; gate_perturbation_or_model|
|YDJC|genetics_expression_druggability|PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE|gate_druggable_surface; gate_perturbation_or_model|
|ARID5B|genetics_expression_druggability|PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE|gate_druggable_surface; gate_perturbation_or_model|


## Inputs Used

|wave|channel|exists|rows_read|rows_used|path|
|---|---|---|---|---|---|
|wave21|residual_druggability|True|80|8|results_v3/wave21_residual_druggability_scan/wave21_residual_druggability_ranked_full.tsv|
|wave23|genetics_restoration|True|14|14|results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv|
|wave25|causal_proxy|True|206|192|results_v3/wave25_causal_genetics_module_proxy/causal_proxy_candidate_matrix.tsv|
|wave34|genetics_expression_druggability|True|5997|47|results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv|
|wave34a|genetics_first_target_rescue|True|23|5|results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv|
|wave38|crispr_state_druggability|True|184|184|results_v3/wave38_crispr_state_druggability_rescue/crispr_state_druggability_rescue_rank.tsv|
|wave39|surfaceome_rescue|True|224|6|results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv|
|wave48|resolution_reopener|True|2|7|results_v3/wave48_resolution_reopener_audit/route_reopener_audit.tsv|
|wave52|remaining_reopeners|True|4|13|results_v3/wave52_remaining_mechanistic_reopeners/remaining_reopeners_audit.tsv|
|wave55|external_genetics|True|3517|125|results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv|
|wave57|geneformer|True|26|2|results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv|
|wave60|circuit_coupling|True|276|120|results_v3/wave60_circuit_coupling_pivot/circuit_predictor_rank.tsv|
|wave61|perturbation_guardrail|True|395|33|results_v3/wave61_perturbation_first_guardrail/intervention_evidence_tiers.tsv|
|wave62|target_resolution|True|2028|1|results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv|
|wave63|transition_controller|True|55|61|results_v3/wave63_transition_controller_integrator/transition_controller_candidates.tsv|
|wave68|unrestricted_gene_screen|True|66150|16|results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv|
|wave70|fc_ros_resolution_closure|True|29|29|results_v3/wave70_fc_ros_resolution_matrix/fc_ros_resolution_candidate_matrix.tsv|
|wave70b|fc_ros_computational_closure|True|19|17|results_v3/wave70b_fc_ros_computational_scout/integrated_fc_ros_candidate_scout.tsv|
|wave70c|fc_ros_geneformer_direction_closure|True|29|29|results_v3/wave70c_inhibitory_receptor_geneformer_direction/geneformer_direction_candidate_calls.tsv|


## Output Files

- `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
- `results_v3/wave71_global_survivor_meta_rank/evidence_long.tsv`
- `results_v3/wave71_global_survivor_meta_rank/summary.json`
- `results_v3/wave71_global_survivor_meta_rank/REPORT.md`
- `subagents_v3/wave71a_global_survivor_meta_rank.md`
