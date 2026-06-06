# Wave91 Lipid-Neighborhood Controller Scan

Question: after parking LPL, which lipid-loader neighborhood node has a better mix of MS anchoring, cross-disease support, response evidence, foundation-model availability, and druggability?

## Ranked Candidates

| gene | wave91_call | wave91_score | ms_wm_delta | ms_wm_p | direct_positive_contexts_p_lt_0_10 | direct_negative_contexts_p_lt_0_10 | nonresponse_high_contexts | ra_hedges_g_resp_minus_non | ra_p | pso_ada_hedges_g_resp_minus_non | pso_ada_p | geneformer_usable_rows | manual_druggability_0_4 | manual_prior_pressure_0_3 | intervention_route | wave91_failures |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FABP5 | PARK_CONTROLLER_FOR_DEEP_VALIDATION | 7.05 | 1.265 | 0.004142 | 2 | 1 | 2 | -0.4081 | 0.201 | -0.1782 | 0.7059 | 5 | 3 | 1 | fatty-acid binding protein inhibitor | case_control_negative_context_present;weak_or_inconsistent_response_direction |
| PPARG | PARK_MARKER_OR_WEAK_CONTROLLER | 4.55 | 1.339 | 0.002337 |  |  |  | -0.5574 | 0.09834 |  |  |  | 4 | 3 | PPAR-gamma agonism/modulation | weak_or_inconsistent_response_direction;no_usable_foundation_model_rows;manual_prior_or_class_pressure |
| LPL | PARK_MARKER_OR_WEAK_CONTROLLER | 4.35 | 1.76 | 0.000622 | 1 | 1 | 3 | -0.3946 | 0.1578 | -2.209 | 0.01111 | 0 | 1 | 1 | enzyme/extracellular lipid hydrolysis | case_control_negative_context_present;no_usable_foundation_model_rows;weak_direct_druggability;major_safety_or_selectivity_liability |
| GPNMB | PARK_MARKER_OR_WEAK_CONTROLLER | 4.1 | 1.434 | 0.00491 | 0 | 2 | 4 | 0.7697 | 0.01402 | 0.3127 | 0.5055 | 4 | 3 | 1 | surface/secreted glycoprotein; antibody/ADC precedent, agonism unresolved | case_control_negative_context_present;weak_or_inconsistent_response_direction |
| ABCG1 | NO_GO_LIPID_NEIGHBORHOOD_NODE | 3.35 | 0.8151 | 0.01407 |  |  |  | -0.08675 | 0.7895 |  |  |  | 1 | 1 | cholesterol efflux transporter, indirect activation | weak_or_inconsistent_response_direction;no_usable_foundation_model_rows;weak_direct_druggability |
| LIPA | NO_GO_LIPID_NEIGHBORHOOD_NODE | 3.35 | 0.458 | 0.2725 | 4 | 3 | 2 | 0.111 | 0.7229 | 0.29 | 0.6095 | 4 | 3 | 1 | lysosomal acid lipase replacement/activation | no_nominal_ms_wm_up_anchor;case_control_negative_context_present;weak_or_inconsistent_response_direction |
| ACSL1 | NO_GO_LIPID_NEIGHBORHOOD_NODE | 3.3 | 0.03355 | 0.9588 | 3 | 2 | 4 | 0.1801 | 0.5267 | 0.4198 | 0.3925 | 7 | 2 | 1 | long-chain acyl-CoA synthetase inhibition | no_nominal_ms_wm_up_anchor;case_control_negative_context_present;weak_or_inconsistent_response_direction |
| ABCA1 | NO_GO_LIPID_NEIGHBORHOOD_NODE | 3 | 0.6056 | 0.03449 |  |  |  | 0.5137 | 0.07379 |  |  |  | 1 | 1 | cholesterol efflux transporter, indirect activation | weak_or_inconsistent_response_direction;no_usable_foundation_model_rows;weak_direct_druggability |
| PLIN2 | NO_GO_LIPID_NEIGHBORHOOD_NODE | 2.2 | 0.6476 | 0.1084 | 0 | 0 | 3 | -0.2578 | 0.44 | -0.321 | 0.4718 | 5 | 0 | 0 | lipid droplet coat protein | no_nominal_ms_wm_up_anchor;weak_direct_druggability |
| NR1H2 | NO_GO_LIPID_NEIGHBORHOOD_NODE | 1.95 | 0.06462 | 0.8275 |  |  |  | -0.03952 | 0.9064 |  |  |  | 4 | 2 | LXR-beta nuclear receptor agonism/modulation | no_nominal_ms_wm_up_anchor;weak_or_inconsistent_response_direction;no_usable_foundation_model_rows;manual_prior_or_class_pressure |
| MSR1 | NO_GO_LIPID_NEIGHBORHOOD_NODE | 1.9 | 0.5659 | 0.03131 | 0 | 2 | 1 | 0.04908 | 0.8638 | -0.2609 | 0.65 | 1 | 2 | 1 | scavenger receptor modulation | case_control_negative_context_present;weak_or_inconsistent_response_direction;major_safety_or_selectivity_liability |
| NR1H3 | NO_GO_LIPID_NEIGHBORHOOD_NODE | 1.45 | 0.9212 | 0.2094 |  |  |  | -0.1647 | 0.5798 |  |  |  | 4 | 2 | LXR-alpha nuclear receptor agonism/modulation | no_nominal_ms_wm_up_anchor;weak_or_inconsistent_response_direction;no_usable_foundation_model_rows;manual_prior_or_class_pressure;major_safety_or_selectivity_liability |
| PPARD | NO_GO_LIPID_NEIGHBORHOOD_NODE | 1.1 | -0.3398 | 0.4029 |  |  |  | 0.05526 | 0.8688 |  |  |  | 4 | 2 | PPAR-delta agonism/modulation | no_nominal_ms_wm_up_anchor;weak_or_inconsistent_response_direction;no_usable_foundation_model_rows;manual_prior_or_class_pressure;major_safety_or_selectivity_liability |
| CD36 | NO_GO_LIPID_NEIGHBORHOOD_NODE | -0.05 | -0.9993 | 0.441 | 0 | 1 | 4 | -0.2374 | 0.4555 | -0.2317 | 0.6852 |  | 2 | 2 | fatty-acid/scavenger receptor inhibition/modulation | no_nominal_ms_wm_up_anchor;case_control_negative_context_present;no_usable_foundation_model_rows;manual_prior_or_class_pressure;major_safety_or_selectivity_liability |
| TREM2 | NO_GO_LIPID_NEIGHBORHOOD_NODE | -0.2 | 0.19 | 0.6127 | 0 | 1 | 2 | 0.03823 | 0.9103 | 0.3748 | 0.5767 |  | 3 | 2 | microglial/myeloid receptor agonism | no_nominal_ms_wm_up_anchor;case_control_negative_context_present;weak_or_inconsistent_response_direction;no_usable_foundation_model_rows;manual_prior_or_class_pressure |
| MERTK | NO_GO_LIPID_NEIGHBORHOOD_NODE | -0.35 | 0.2471 | 0.4293 | 0 | 2 | 3 | 0.1197 | 0.6642 | -0.7528 | 0.1267 | 1 | 3 | 2 | efferocytosis receptor tyrosine kinase agonism | no_nominal_ms_wm_up_anchor;case_control_negative_context_present;manual_prior_or_class_pressure;major_safety_or_selectivity_liability |
| APOE | NO_GO_LIPID_NEIGHBORHOOD_NODE | -0.95 | 0.3729 | 0.1202 | 0 | 2 | 3 | -0.2777 | 0.3508 | 0.7924 | 0.08558 | 7 | 1 | 2 | apolipoprotein/lipid transport state | no_nominal_ms_wm_up_anchor;case_control_negative_context_present;weak_direct_druggability;manual_prior_or_class_pressure |

## Interpretation

No candidate is promoted as a V3 therapeutic finding by this scan alone. The top rows are parked for deeper validation only if their failures are addressable.

The most important guardrail is that nuclear-receptor and scavenger-receptor routes are druggable but broad; marker strength does not equal safe intervention.
