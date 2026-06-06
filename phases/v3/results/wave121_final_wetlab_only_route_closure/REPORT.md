# Wave121 Final Wet-Lab-Only Route Closure

## Bottom Line

Branch call: `NO_OPEN_ROUTE_AFTER_WETLAB_ONLY_AUDIT`.

After Wave116 hygiene fixes, only `FPR2_ANXA1_BIASED_RESOLUTION` and
`CD300_RECEPTOR_SPECIFIC_TUNING` remained open. Both are retained only as
wet-lab kill-test concepts, not computationally promotable target nominations.

## Route Decisions

| route | genes | call | passed_gates | gate_count | failed_gates | wave95_call | wave95_reason | route_ms_call | route_wave92_call | response_systems | nominal_response_systems | prior_art_close | direction_safe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FPR2_ANXA1_BIASED_RESOLUTION | FPR2;ANXA1 | NO_REOPEN_WETLAB_ONLY_ROUTE | 2 | 10 | ms_anchor_or_trend;cross_disease_residual;cell_resolved_response_or_transition;target_resolved_genetics_ge2;broad_genetics_ge4;real_perturbation_or_validated_model;prior_not_blocked;direction_safe | PARK_WETLAB_KILL_TEST_ONLY | route can only be reopened by target-specific wet-lab perturbation/safety test | MS_ROUTE_NULL_OR_WEAK | NO_GO_NO_MS_WHITE_MATTER_ROUTE_ANCHOR | 2 | 1 | True | False |
| CD300_RECEPTOR_SPECIFIC_TUNING | CD300A;CD300C;CD300E;CD300LF;CD300LG | NO_REOPEN_WETLAB_ONLY_ROUTE | 2 | 10 | ms_anchor_or_trend;cross_disease_residual;cell_resolved_response_or_transition;target_resolved_genetics_ge2;broad_genetics_ge4;real_perturbation_or_validated_model;prior_not_blocked;direction_safe | PARK_WETLAB_KILL_TEST_ONLY | route can only be reopened by target-specific wet-lab perturbation/safety test | MS_ROUTE_NULL_OR_WEAK | NO_GO_NO_MS_WHITE_MATTER_ROUTE_ANCHOR | 3 | 2 | True | False |

## Gene-Level Evidence

| route | gene | wave81_call | ms_delta_log2 | ms_p | wave71_call | wave37_screen_call | wave37_contrast_fdr |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FPR2_ANXA1_BIASED_RESOLUTION | FPR2 |  |  |  |  | UNRESOLVED | 0.92 |
| FPR2_ANXA1_BIASED_RESOLUTION | ANXA1 |  |  |  |  | UNRESOLVED | 0.92 |
| CD300_RECEPTOR_SPECIFIC_TUNING | CD300A | NO_GO_NO_PERTURBATION_SUPPORT | -0.3453 | 0.07661 | NO_REOPEN_INSUFFICIENT_CONVERGENCE | UNRESOLVED | 0.92 |
| CD300_RECEPTOR_SPECIFIC_TUNING | CD300C |  |  |  |  |  |  |
| CD300_RECEPTOR_SPECIFIC_TUNING | CD300E |  |  |  |  | UNRESOLVED | 0.9971 |
| CD300_RECEPTOR_SPECIFIC_TUNING | CD300LF | NO_GO_NO_PERTURBATION_SUPPORT | -0.09912 | 0.709 | NO_REOPEN_INSUFFICIENT_CONVERGENCE | UNRESOLVED | 0.9971 |
| CD300_RECEPTOR_SPECIFIC_TUNING | CD300LG |  |  |  |  | UNRESOLVED | 0.9971 |

## Interpretation

These routes have useful resolution-biology hypotheses, but the V3 claim needs
MS anchoring, target-resolved genetics or validated perturbation/model support,
directional safety, and novelty. The two routes fail that standard from
available local evidence. They should not keep consuming orchestration cycles
unless new wet-lab perturbation data are available.

## Reproducibility

- Script: `scripts/v3_wave121_final_wetlab_only_route_closure.py`
- Output: `results_v3/wave121_final_wetlab_only_route_closure/wetlab_only_route_decisions.tsv`
- Seed: `20260527`
