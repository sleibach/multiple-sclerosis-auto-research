# Wave99 Endogenous Inflammasome Brake Audit

Random seed: `20260527`.

## Question

Can an endogenous brake below the LITAF/CASP4 inflammatory-stress branch
be promoted as a tractable cross-autoimmune intervention point?

## Verdict

`NO_REOPEN_ENDOGENOUS_INFLAMMASOME_BRAKE_TARGET`

## Call Counts

| wave99_call | n |
| --- | --- |
| NO_GO_PRIOR_OR_SAFETY_BLOCKED | 13 |
| NO_GO_COMPENSATORY_BRAKE_MARKER | 2 |
| NO_GO_LOCAL_EVIDENCE_WEAK | 2 |

## Candidate Matrix

| gene | wave99_call | wave99_score | hard_gate_count | support_gate_count | axis_role | broad_positive_disease_count | strict_core_covariate_surviving_disease_count | residual_case_positive_disease_count | c15_trend_positive_disease_count | ms_delta_log2 | ms_p | wave68_remission_adjusted_delta | wave68_remission_adjusted_fdr | wave37_screen_call | wave37_contrast_fdr | wave18_recommendation | wave55_n_genetic_diseases_ge_0_25 | chembl_activity_count | modality_class | wave99_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CARD16 | NO_GO_COMPENSATORY_BRAKE_MARKER | 10.46 | 3 | 3 | endogenous_inflammasome_brake | 5 | 0 | 1 | 4 | 0.4271 | 0.4948 | -0.7672 | 0.03392 |  | 1 |  | 0 | 0 | intracellular CARD-only protein; no established selective augmentation modality | endogenous brake-like marker is recurrent, but residual C15 coupling/perturbation/actionability gates fail; failed=gate_ms_strict;gate_c15_residual_costate;gate_real_perturbation_direction;gate_modality_ready;gate_genetics |
| SERPINB1 | NO_GO_COMPENSATORY_BRAKE_MARKER | 5.15 | 3 | 0 | endogenous_protease_inflammatory_brake | 3 | 0 | 1 | 2 | 0.02595 | 0.8686 |  | 1 |  | 1 |  | 0 | 0 | intracellular serpin; recombinant replacement/delivery to lesional myeloid cells is not established | endogenous brake-like marker is recurrent, but residual C15 coupling/perturbation/actionability gates fail; failed=gate_ms_strict;gate_c15_residual_costate;gate_real_perturbation_direction;gate_modality_ready;gate_genetics |
| CASP4 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 11.5 | 3 | 2 | noncanonical_pyroptosis_stress_generator | 4 | 0 | 2 | 3 | 0.2067 | 0.4927 | -0.7246 | 0.02812 |  | 1 | do_not_promote | 0 | 61 | cysteine protease; targetable but selectivity/host-defense risk | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_real_perturbation_direction;gate_prior_not_blocking;gate_safety_not_blocking;gate_genetics |
| GBP1 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 11.25 | 3 | 3 | ifn_induced_noncanonical_inflammasome_host_defense | 3 | 0 | 1 | 3 | 0.4914 | 0.06818 | -1.976 | 0.01712 |  | 1 |  | 0 | 0 | GTPase; no selective autoimmune-safe modality | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_real_perturbation_direction;gate_modality_ready;gate_safety_not_blocking;gate_genetics |
| GBP2 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 7.928 | 2 | 2 | ifn_induced_noncanonical_inflammasome_host_defense | 0 | 0 | 2 | 3 | 0.02596 | 0.9251 | -1.179 | 0.02241 | UNRESOLVED | 1 |  | 0 | 0 | GTPase; no selective autoimmune-safe modality | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_real_perturbation_direction;gate_modality_ready;gate_safety_not_blocking;gate_genetics |
| CASP1 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 6.746 | 2 | 1 | core_inflammasome_effector | 0 | 0 | 3 | 3 | -0.05687 | 0.8113 |  | 1 | UNRESOLVED | 0.9966 |  | 0 | 0 | cysteine protease; inhibitor chemistry exists but selectivity/safety are difficult | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_real_perturbation_direction;gate_prior_not_blocking;gate_safety_not_blocking;gate_genetics |
| IL1B | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 6.584 | 2 | 1 | proinflammatory_inflammasome_output | 0 | 0 | 2 | 2 | -0.4439 | 0.2707 |  | 1 | UNRESOLVED | 0.9966 |  | 0 | 0 | biologic neutralization exists | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_real_perturbation_direction;gate_prior_not_blocking;gate_safety_not_blocking;gate_genetics |
| CASP5 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 5.206 | 1 | 2 | noncanonical_pyroptosis_stress_generator | 0 | 0 | 0 | 2 | -1.242 | 0.2057 | -2.299 | 0.01447 |  | 1 |  | 0 | 0 | cysteine protease; targetable class but selectivity/host-defense risk | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_prior_not_blocking;gate_safety_not_blocking;gate_genetics |
| GBP5 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 3.731 | 1 | 2 | ifn_induced_noncanonical_inflammasome_host_defense | 0 | 0 | 0 | 2 | 0.5414 | 0.08384 |  | 1 | UNRESOLVED | 1 |  | 0 | 0 | GTPase; no selective autoimmune-safe modality | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_modality_ready;gate_safety_not_blocking;gate_genetics |
| NLRP3 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 3.628 | 1 | 1 | inflammasome_sensor | 1 | 0 | 0 | 2 | -0.2348 | 0.4767 |  | 1 | UNRESOLVED | 0.9966 |  | 0 | 0 | small-molecule NLRP3 inhibitors exist | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_prior_not_blocking;gate_safety_not_blocking;gate_genetics |
| IL18BP | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 2.9 | 2 | 0 | secreted_IL18_neutralizing_brake | 0 | 0 | 1 | 1 | 0.127 | 0.6187 |  | 1 | UNRESOLVED | 0.9971 |  | 0 | 0 | secreted soluble decoy; recombinant biologic modality exists in adjacent indications | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_prior_not_blocking;gate_genetics |
| GSDMD | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 2.01 | 1 | 0 | pyroptotic_pore_effector | 0 | 0 | 1 | 1 | -0.3297 | 0.0496 |  | 1 | UNRESOLVED | 1 |  | 0 | 0 | pore-forming effector; chemistry emerging but broad innate safety risk | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_prior_not_blocking;gate_safety_not_blocking;gate_genetics |
| IL18 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 1.9 | 1 | 0 | proinflammatory_inflammasome_output | 0 | 0 | 1 | 1 | 0.1841 | 0.2056 | 0.8362 | 0.03123 | UNRESOLVED | 0.92 |  | 0 | 0 | biologic neutralization/IL18BP route exists | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_prior_not_blocking;gate_safety_not_blocking;gate_genetics |
| CARD8 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 1.4 | 1 | 0 | inflammasome_sensor_regulator | 0 | 0 | 1 | 0 | -0.2941 | 0.02906 |  | 1 |  | 1 |  | 0 | 0 | NLR/CARD inflammasome regulator; target biology is not a clean brake | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_modality_ready;gate_safety_not_blocking;gate_genetics |
| NLRP6 | NO_GO_PRIOR_OR_SAFETY_BLOCKED | 1 | 1 | 0 | mucosal_inflammasome_context_regulator | 0 | 0 | 0 | 0 | -2.656 | 0.0381 |  | 1 | UNRESOLVED | 0.9971 |  | 0 | 0 | inflammasome sensor; no clean selective autoimmune modality | prior-art or safety gate blocks broad therapeutic promotion; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_modality_ready;gate_safety_not_blocking;gate_genetics |
| CARD17 | NO_GO_LOCAL_EVIDENCE_WEAK | 2.4 | 2 | 0 | endogenous_inflammasome_brake_like | 0 | 0 | 1 | 0 |  | 1 |  | 1 |  | 1 |  | 0 | 0 | intracellular CARD-only protein; no established selective augmentation modality | local MS/cross-disease evidence is insufficient; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_modality_ready;gate_genetics |
| CARD18 | NO_GO_LOCAL_EVIDENCE_WEAK | 2 | 2 | 0 | endogenous_inflammasome_brake_like | 0 | 0 | 0 | 0 |  | 1 |  | 1 |  | 1 |  | 1 | 0 | intracellular CARD-only protein; no established selective augmentation modality | local MS/cross-disease evidence is insufficient; failed=gate_ms_strict;gate_broad_cross_disease;gate_c15_residual_costate;gate_real_perturbation_direction;gate_modality_ready;gate_genetics |

## Interpretation

The endogenous-brake concept remains mechanistically useful but not
therapeutically promotable from current data. `CARD16` is the cleanest
biological brake clue, yet it lacks residual C15 co-state, MS anchoring,
real perturbation direction, and a selective augmentation modality. `IL18BP`
is the most druggable brake-like modality, but local MS/C15 evidence is weak
and the IL18 neutralization space is prior-art crowded. Core pyroptosis
nodes (`CASP1`, `CASP4`, `CASP5`, `GSDMD`, `NLRP3`, `IL1B`, `IL18`) are
actionable in principle but blocked by prior-art/safety and do not solve the
cross-autoimmune novelty problem. GBP-family signals are dominated by
generic interferon/host-defense biology.

## Output Files

- `results_v3/wave99_endogenous_inflammasome_brake_audit/inflammasome_brake_candidate_rank.tsv`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/inflammasome_brake_c15_residual_context_tests.tsv`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/inflammasome_brake_c15_residual_summary.tsv`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/inflammasome_brake_donor_covariate_scores.tsv`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/summary.json`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/REPORT.md`
