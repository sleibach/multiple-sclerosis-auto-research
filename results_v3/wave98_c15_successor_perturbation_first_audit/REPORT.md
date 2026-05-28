# Wave98 C15 Successor Perturbation-First Audit

Random seed: `20260527`.

## Question

Can any novelty-open C15ORF48-state successor candidate be reopened after
requiring perturbation-direction evidence rather than residual co-state
alone?

## Verdict

`NO_REOPEN_C15_SUCCESSOR_TARGET`

## Call Counts

| wave98_call | n |
| --- | --- |
| NO_GO_C15_SUCCESSOR_PERTURBATION_FIRST | 2 |
| PARK_PERTURBATION_ORDERING_REQUIRED | 1 |
| NO_GO_CLOSE_PRIOR_OR_SAFETY_BLOCKED | 1 |

## Candidate Matrix

| gene | wave98_call | wave98_score | critical_gate_count | support_gate_count | mechanistic_direction | residual_case_positive_disease_count | median_residual_case_r | ms_delta_log2 | ms_p | wave68_remission_adjusted_delta | wave68_remission_adjusted_fdr | wave37_screen_call | wave37_contrast_fdr | wave18_recommendation | wave55_n_genetic_diseases_ge_0_25 | chembl_activity_count | modality_class | prior_status | wave98_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LITAF | PARK_PERTURBATION_ORDERING_REQUIRED | 8.717 | 2 | 1 | upstream_inflammatory_stress_generator | 3 | 0.4155 | 0.3084 | 0.1716 | -0.4507 | 0.03313 | UNRESOLVED | 0.9971 |  | 2 | 0 | no selective direct modality | novelty_open_but_generic_tnf_lps_prior | residual C15 co-state plus remission direction survive, but real perturbation or modality is missing; failed=gate_ms_strict;gate_real_perturbation_direction;gate_modality_selective;gate_model_perturbation_direction;gate_genetics |
| CASP4 | NO_GO_CLOSE_PRIOR_OR_SAFETY_BLOCKED | 7.892 | 2 | 1 | upstream_pyroptosis_danger_stress_generator | 2 | 0.3084 | 0.2067 | 0.4927 | -0.7246 | 0.02812 |  | 1 | do_not_promote | 0 | 61 | enzymatic but selectivity/host-defense risk | close_eae_caspase_and_inhibitor_prior | close prior-art/safety gate blocks therapeutic promotion; failed=gate_ms_strict;gate_real_perturbation_direction;gate_prior_not_blocking;gate_model_perturbation_direction;gate_genetics |
| PLEK2 | NO_GO_C15_SUCCESSOR_PERTURBATION_FIRST | 6.089 | 2 | 1 | cytoskeletal_state_marker_until_proven_controller | 1 | 0.3143 | 3.046 | 0.007379 |  | 1 | UNRESOLVED | 1 | do_not_promote | 0 | 0 | no selective direct modality | autoimmune_novelty_open | successor candidate lacks required MS/residual/perturbation/modality convergence; failed=gate_residual_c15_survives;gate_real_perturbation_direction;gate_modality_selective;gate_response_beneficial_for_inhibition;gate_model_perturbation_direction;gate_genetics |
| PIK3R2 | NO_GO_C15_SUCCESSOR_PERTURBATION_FIRST | 2.374 | 1 | 0 | generic_pi3k_autophagy_adjacency | 1 | 0.3979 | -0.03954 | 0.8468 |  | 1 | UNRESOLVED | 0.9966 |  | 0 | 1781 | PI3K-family chemistry exists but PIK3R2-specific selectivity is not established | pi3k_autoimmune_field_saturated | successor candidate lacks required MS/residual/perturbation/modality convergence; failed=gate_residual_c15_survives;gate_ms_strict;gate_real_perturbation_direction;gate_modality_selective;gate_response_beneficial_for_inhibition;gate_model_perturbation_direction;gate_genetics |

## Interpretation

`LITAF` is the strongest wet-lab ordering hypothesis because residual
C15 co-state and remission-direction support survive, but it lacks a
validated perturbation edge and a selective modality. `CASP4` has similar
biology but is close-prior/safety blocked. `PLEK2` is MS-anchored but
still marker-like. `PIK3R2` is broad PI3K adjacency without MS or C15
specificity. None is a therapeutic nomination.

## Output Files

- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_perturbation_first_rank.tsv`
- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_residual_context_tests.tsv`
- `results_v3/wave98_c15_successor_perturbation_first_audit/summary.json`
- `results_v3/wave98_c15_successor_perturbation_first_audit/REPORT.md`
