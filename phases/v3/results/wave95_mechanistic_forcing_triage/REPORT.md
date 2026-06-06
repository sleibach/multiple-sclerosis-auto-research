# Wave95 Mechanistic Forcing Triage

Random seed: `20260527`.

## Question

Do the Wave94 accessible/state-transition candidates survive stricter
mechanistic therapeutic gates: residualized state control, MS anchoring,
validated perturbation/model direction, modality, and non-blocking prior art?

## Verdict

`NO_MECHANISTIC_THERAPEUTIC_PROMOTION`

Candidates tested: `15`. Promoted candidates: `0`.

## Call Counts

| wave95_call | n |
| --- | --- |
| NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 8 |
| PARK_WETLAB_KILL_TEST_ONLY | 4 |
| NO_GO_PRIOR_ART_OR_SAFETY_BLOCKED | 3 |

## Top Ranked Rows

| candidate | candidate_type | wave95_call | critical_gate_count | support_gate_count | ms_delta_log2 | ms_p | broad_positive_disease_count | strict_core_residual_disease_count | w68_remission_adjusted_fdr | w37_screen_call | w18_foundation_recommendation | wave62_strong_qtl_coloc_disease_count | wave55_n_genetic_diseases_ge_0_25 | manual_prior_class | wave95_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEL1L3 | gene | NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 4 | 2 | 0.9225 | 0.01814 | 4 | 0 |  | UNRESOLVED | do_not_promote_from_foundation_model | 0 | 0 | undercharacterized_no_intervention_package | expression/response signal lacks residualized controller evidence and validated perturbation direction |
| C15ORF48 | gene | NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 4 | 1 | 1.223 | 0.003753 | 4 | 0 |  |  |  | 0 | 0 | mitochondrial_microprotein_no_direct_modality | expression/response signal lacks residualized controller evidence and validated perturbation direction |
| PLEK2 | gene | NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 4 | 1 | 3.046 | 0.007379 | 4 | 0 |  | UNRESOLVED | do_not_promote | 0 | 0 | intracellular_cytoskeletal_no_modality | expression/response signal lacks residualized controller evidence and validated perturbation direction |
| CHI3L1 | gene | NO_GO_PRIOR_ART_OR_SAFETY_BLOCKED | 3 | 2 | 2.007 | 0.004613 | 4 | 0 | 0.01278 |  | do_not_promote_from_foundation_model | 0 | 0 | secreted_biomarker_prior_saturation | prior-art/safety gate blocks therapeutic promotion |
| NRCAM | gene | NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 3 | 2 | 1.298 | 0.08125 | 3 | 0 |  | UNRESOLVED |  | 0 | 0 | neural_adhesion_safety_and_weak_genetics | expression/response signal lacks residualized controller evidence and validated perturbation direction |
| CD58 | gene | NO_GO_PRIOR_ART_OR_SAFETY_BLOCKED | 3 | 2 | 0.1798 | 0.3111 | 0 | 0 |  |  |  | 2 | 3 | blocked_generic_autoimmune_intervention | prior-art/safety gate blocks therapeutic promotion |
| MFGE8 | gene | PARK_WETLAB_KILL_TEST_ONLY | 3 | 2 | 0.5587 | 0.06863 | 0 | 0 | 0.02241 | UNRESOLVED |  | 0 | 0 | close_efferocytosis_prior_art_safety_unresolved | route can only be reopened by target-specific wet-lab perturbation/safety test |
| CD82 | gene | NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 3 | 2 | 0.5037 | 0.1729 | 5 | 0 | 0.01065 | UNRESOLVED |  | 0 | 0 | direction_actionability_blocked | expression/response signal lacks residualized controller evidence and validated perturbation direction |
| CD200 | gene | NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 3 | 1 | 1.838 | 0.09086 | 4 | 0 |  | UNRESOLVED |  | 0 | 2 | checkpoint_direction_receptor_side_unresolved | expression/response signal lacks residualized controller evidence and validated perturbation direction |
| FXYD5 | gene | PARK_WETLAB_KILL_TEST_ONLY | 3 | 1 | 0.3525 | 0.05871 | 4 | 0 |  | UNRESOLVED |  | 0 | 0 | novelty_not_blocked_safety_modality_unresolved | route can only be reopened by target-specific wet-lab perturbation/safety test |
| ROMO1 | gene | NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 3 | 1 | 0.4378 | 0.06607 | 3 | 0 |  | UNRESOLVED |  | 0 | 0 | mitochondrial_ros_no_selective_modality | expression/response signal lacks residualized controller evidence and validated perturbation direction |
| FPR2_ANXA1_BIASED_RESOLUTION | route | PARK_WETLAB_KILL_TEST_ONLY | 3 | 1 | -0.501 | 0.4607 | 3 | 0 |  |  |  | 0 | 0 | NOT_BLOCKED_BUT_IMMATURE | route can only be reopened by target-specific wet-lab perturbation/safety test |
| CD300_RECEPTOR_SPECIFIC_TUNING | route | PARK_WETLAB_KILL_TEST_ONLY | 3 | 1 | -0.394 | 0.2625 | 2 | 0 |  |  |  | 0 | 0 | NOT_BLOCKED_BUT_DIRECTION_AMBIGUOUS | route can only be reopened by target-specific wet-lab perturbation/safety test |
| P4HB | gene | NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT | 3 | 0 | -0.1078 | 0.5193 | 4 | 0 |  | UNRESOLVED |  | 0 | 0 | nonspecific_redox_er_biology | expression/response signal lacks residualized controller evidence and validated perturbation direction |

## Interpretation

The Wave94 branch selection survives as a useful forcing map, but no
candidate becomes a therapeutic nomination. `SEL1L3` remains the top
statistical survivor, yet it has no validated perturbation direction, no
strong target-resolved genetics, and no intervention package. `CD58/CD2`
has the best genetic/biological evidence but is prior-art and direction
blocked. `FXYD5`, `MFGE8`, and `CD300` are wet-lab kill-test routes, not
in-silico findings. `C15ORF48` is a mechanistic clue rather than a druggable
intervention point.

The next computational move should not be another accessible-marker rerank.
It should either (a) discover residualized transition controllers across
cell-resolved autoimmune tissues de novo, or (b) move into explicit wet-lab
assay design for the highest-ranked kill-test routes.

## Output Files

- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_candidate_rank.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_gate_audit.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_metric_long.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/summary.json`
- `results_v3/wave95_mechanistic_forcing_triage/REPORT.md`
