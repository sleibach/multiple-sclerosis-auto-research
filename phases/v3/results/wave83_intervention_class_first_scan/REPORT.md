# Wave83 Intervention-Class-First Scan

## Question

If we start from locally reachable intervention classes instead of residual
expression markers, does any target pass MS/cross-autoimmune module evidence and
directional perturbation gates?

## Verdict

`REOPEN_REACHABLE_INTERVENTION_CANDIDATE`: `0`.

This wave is a triage scan. A park is not a therapeutic claim.

## Call Counts

| call | n |
| --- | --- |
| NO_GO_NOT_REACHABLE_FIRST_CLASS | 662 |
| NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 63 |
| PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 10 |

## Top Reachable-First Candidates

| gene | intervention_class | wave83_call | total_score | reachability_score | cross_autoimmune_score | ms_score | perturbation_response_score | hard_failures | manual_closure_reason | positive_diseases | genetic_breadth_diseases | wave39_call | wave62_call | wave34a_call | wave68_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PTPN2 | kinase_or_phosphosignaling | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 16.61 | 8.562 | 11 | 0 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:restoration_needed_no_selective_intervention_route;no_high_confidence_directional_support | restoration_needed_no_selective_intervention_route | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | Celiac;Crohn;Psoriasis;RA;T1D | NO_GO_SURFACEOME_RESCUE | NO_GO_WAVE62_TARGET_RESOLUTION | DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION | DESCRIPTIVE_GENE_SIGNAL |
| STAT4 | receptor_or_ligand_axis | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 13.59 | 4.562 | 8 | 2 | 2 | manual_or_prior_blocker;prior_branch_closed:broad_tf_jak_stat_axis_prior_art_no_selective_target | broad_tf_jak_stat_axis_prior_art_no_selective_target | Crohn disease;ulcerative colitis | Celiac;Crohn;MS;PBC;RA;SLE;Sjogren;T1D |  | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION | PARK_GENETIC_PERTURBATION_INTERSECTION |
| PTGER4 | intracellular_other | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 13.51 | 7.5 | 7 | 2 | 0 | no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:ep4_directionality_prior_art_conflicted;no_high_confidence_directional_support | ep4_directionality_prior_art_conflicted | Crohn disease;type 1 diabetes mellitus | Crohn;MS;Psoriasis;T1D;UC |  | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | DEMOTE_NO_TARGET_LEVEL_GENETIC_PACKAGE | DESCRIPTIVE_GENE_SIGNAL |
| TYK2 | kinase_or_phosphosignaling | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 12.34 | 7.5 | 8 | 0 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:jak_tyk_prior_art_direction_and_selectivity_blocker;no_high_confidence_directional_support | jak_tyk_prior_art_direction_and_selectivity_blocker | psoriasis;type 1 diabetes mellitus | Crohn;PBC;Psoriasis;RA;SLE;T1D |  | NO_GO_WAVE62_TARGET_RESOLUTION | DEMOTE_PRIOR_ART_BLOCKED | DESCRIPTIVE_GENE_SIGNAL |
| PTPN22 | phosphatase_or_signaling_adaptor | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 12.17 | 9.125 | 5 | 1 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:restoration_direction_and_pleiotropy_blocker;no_high_confidence_directional_support | restoration_direction_and_pleiotropy_blocker | Sjogren syndrome | Crohn;RA;SLE;T1D |  | NO_GO_WAVE62_TARGET_RESOLUTION | PARK_DIRECTION_OR_MODALITY_UNRESOLVED | DESCRIPTIVE_GENE_SIGNAL |
| IL2RA | receptor_or_ligand_axis | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 11.72 | 5.5 | 4.5 | 2 | 2 | manual_or_prior_blocker;prior_branch_closed:cd25_axis_prior_art_and_treg_effector_direction_conflict | cd25_axis_prior_art_and_treg_effector_direction_conflict |  | Crohn;MS;Psoriasis;RA;T1D |  | PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW | DEMOTE_PRIOR_ART_BLOCKED | DESCRIPTIVE_GENE_SIGNAL |
| GPR65 | intracellular_other | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 10.79 | 6.5 | 5 | 2 | 0 | no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:acid_sensing_gpcr_prior_art_local_mismatch;no_high_confidence_directional_support | acid_sensing_gpcr_prior_art_local_mismatch | Sjogren syndrome | AS;MS |  | PARK_MS_TARGET_RESOLVED_NO_CROSS_DISEASE_MODULE | PARK_GENETIC_SIGNAL_LOCAL_CELLSTATE_MISMATCH | DESCRIPTIVE_GENE_SIGNAL |
| CXCR2 | intracellular_other | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 9.572 | 3.5 | 7 | 0 | 2.5 | no_strong_ms_anchor;manual_or_prior_blocker;prior_branch_closed:neutrophil_chemokine_axis_prior_art_and_safety | neutrophil_chemokine_axis_prior_art_and_safety | Crohn disease;psoriasis;ulcerative colitis | AS;Crohn;Psoriasis;RA;UC |  | NO_GO_WAVE62_TARGET_RESOLUTION |  | DESCRIPTIVE_GENE_SIGNAL |
| CD40 | intracellular_other | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 8.391 | 3 | 8 | 2 | 1.5 | no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:costimulation_axis_prior_art_and_systemic_safety;no_high_confidence_directional_support | costimulation_axis_prior_art_and_systemic_safety | Crohn disease;ulcerative colitis | RA |  | NO_GO_WAVE62_TARGET_RESOLUTION |  | DESCRIPTIVE_GENE_SIGNAL |
| CTLA4 | receptor_or_ligand_axis | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 7.618 | 5.5 | 4.5 | 0 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:checkpoint_axis_prior_art_systemic_immunosuppression;no_high_confidence_directional_support | checkpoint_axis_prior_art_systemic_immunosuppression |  | RA;T1D |  | NO_GO_WAVE62_TARGET_RESOLUTION | DEMOTE_PRIOR_ART_BLOCKED | DESCRIPTIVE_GENE_SIGNAL |
| IL23R | receptor_or_ligand_axis | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 13.79 | 7.5 | 5.5 | 0 | 2 | no_strong_ms_anchor;manual_or_prior_blocker |  |  | AS;Crohn;Psoriasis;RA;UC |  | NO_GO_WAVE62_TARGET_RESOLUTION | DEMOTE_PRIOR_ART_BLOCKED | DESCRIPTIVE_GENE_SIGNAL |
| MMP7 | surface_secreted_other | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 12.77 | 5 | 7 | 1 | 2 | no_strong_ms_anchor;manual_or_prior_blocker |  | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | PARK_REVIEW |  |  | DESCRIPTIVE_GENE_SIGNAL |
| IL10 | receptor_or_ligand_axis | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 12.38 | 7.5 | 6 | 0 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;no_high_confidence_directional_support |  |  | Crohn;T1D;UC |  | NO_GO_WAVE62_TARGET_RESOLUTION | PARK_PRIOR_ART_OR_CROWDING | DESCRIPTIVE_GENE_SIGNAL |
| FAP | enzyme | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 12.07 | 7.5 | 4.8 | 0 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;no_high_confidence_directional_support |  | type 1 diabetes mellitus;ulcerative colitis | Psoriasis |  | NO_GO_WAVE62_TARGET_RESOLUTION | PARK_DIRECTION_OR_MODALITY_UNRESOLVED | DESCRIPTIVE_GENE_SIGNAL |
| IFNGR2 | intracellular_other | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 11.62 | 5 | 6 | 2 | 0 | no_positive_perturbation_or_response_direction;manual_or_prior_blocker;no_high_confidence_directional_support |  | type 1 diabetes mellitus | Crohn;RA |  | NO_GO_WAVE62_TARGET_RESOLUTION |  | DESCRIPTIVE_GENE_SIGNAL |
| PTPRC | intracellular_other | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 11.05 | 4 | 6.1 | 0 | 2 | no_strong_ms_anchor |  | Crohn disease;Sjogren syndrome;ulcerative colitis | Crohn |  | NO_GO_WAVE62_TARGET_RESOLUTION |  | DESCRIPTIVE_GENE_SIGNAL |
| IL15 | receptor_or_ligand_axis | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 11 | 5 | 5 | 1 | 2 | no_strong_ms_anchor;manual_or_prior_blocker |  | Crohn disease;Sjogren syndrome;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | NO_GO_SURFACEOME_RESCUE |  |  | DESCRIPTIVE_GENE_SIGNAL |
| CASP4 | surface_secreted_other | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 10.73 | 4 | 6 | 0 | 2 | no_strong_ms_anchor |  | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | NO_GO_SURFACEOME_RESCUE |  |  | DESCRIPTIVE_GENE_SIGNAL |
| CCL20 | receptor_or_ligand_axis | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 10.41 | 3 | 8 | 1 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;no_high_confidence_directional_support |  | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | UC | PARK_REVIEW | NO_GO_WAVE62_TARGET_RESOLUTION |  | DESCRIPTIVE_GENE_SIGNAL |
| KCNJ2 | transporter_or_trafficking | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 10.38 | 4 | 6.7 | 0 | 2 | no_strong_ms_anchor;manual_or_prior_blocker |  | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | AITD | NO_GO_SURFACEOME_RESCUE | NO_GO_WAVE62_TARGET_RESOLUTION |  | DESCRIPTIVE_GENE_SIGNAL |
| ITPR3 | intracellular_other | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 10.11 | 4 | 6.5 | 0 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;no_high_confidence_directional_support |  | type 1 diabetes mellitus;ulcerative colitis | T1D |  | NO_GO_WAVE62_TARGET_RESOLUTION |  | DESCRIPTIVE_GENE_SIGNAL |
| HLA-DRB1 | receptor_or_ligand_axis | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 10 | 5 | 4 | 1 | 2 | no_strong_ms_anchor;manual_or_prior_blocker |  | Crohn disease;Sjogren syndrome;type 1 diabetes mellitus;ulcerative colitis |  | NO_GO_SURFACEOME_RESCUE |  |  | DESCRIPTIVE_GENE_SIGNAL |
| CD226 | receptor_or_ligand_axis | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 9.78 | 4.5 | 5.5 | 0 | 0 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;no_high_confidence_directional_support |  |  | Crohn;PBC;T1D |  | NO_GO_WAVE62_TARGET_RESOLUTION | DEMOTE_NO_TARGET_LEVEL_GENETIC_PACKAGE | DESCRIPTIVE_GENE_SIGNAL |
| TIMP1 | enzyme | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 9.772 | 3 | 7 | 0 | 2 | no_strong_ms_anchor;manual_or_prior_blocker |  | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis |  | NO_GO_SURFACEOME_RESCUE |  |  | DESCRIPTIVE_GENE_SIGNAL |
| FKBP1A | kinase_or_phosphosignaling | NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED | 9.718 | 5 | 4.7 | 0 | 2 | no_strong_ms_anchor;manual_or_prior_blocker |  | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | Sjogren | NO_GO_SURFACEOME_RESCUE | NO_GO_WAVE62_TARGET_RESOLUTION |  | DESCRIPTIVE_GENE_SIGNAL |

## Parked Candidates

| gene | intervention_class | wave83_call | total_score | hard_failures | manual_closure_reason | positive_diseases | ms_genetic_score | model_support_contexts | ibd_response_fdr10 | manual_prior_blocked | primary_route_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PTPN2 | kinase_or_phosphosignaling | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 16.61 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:restoration_needed_no_selective_intervention_route;no_high_confidence_directional_support | restoration_needed_no_selective_intervention_route | Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | 0 | 1 | insufficient_breadth; no_ms_anchor; prior_demoted_or_class_blocked; prior_art_or_trial_saturation; reachable protein class by UniProt location/features; ChEMBL exact target found; ChEMBL activity records: 1279 |
| STAT4 | receptor_or_ligand_axis | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 13.59 | manual_or_prior_blocker;prior_branch_closed:broad_tf_jak_stat_axis_prior_art_no_selective_target | broad_tf_jak_stat_axis_prior_art_no_selective_target | Crohn disease;ulcerative colitis | 0.8457 | 0 | 1 | 1 | Genetics may be broad, but current modality is absent or wrong-direction restoration. |
| PTGER4 | intracellular_other | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 13.51 | no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:ep4_directionality_prior_art_conflicted;no_high_confidence_directional_support | ep4_directionality_prior_art_conflicted | Crohn disease;type 1 diabetes mellitus | 0.5559 | 0 | 0 | 1 | No broad local credible-set/eQTL-backed genetic package; GWAS-only evidence is insufficient. |
| TYK2 | kinase_or_phosphosignaling | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 12.34 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:jak_tyk_prior_art_direction_and_selectivity_blocker;no_high_confidence_directional_support | jak_tyk_prior_art_direction_and_selectivity_blocker | psoriasis;type 1 diabetes mellitus | 0 | 0 | 0 | 1 | Direct clinical or therapeutic-class prior art blocks novelty. |
| PTPN22 | phosphatase_or_signaling_adaptor | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 12.17 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:restoration_direction_and_pleiotropy_blocker;no_high_confidence_directional_support | restoration_direction_and_pleiotropy_blocker | Sjogren syndrome | 0 | 0 | 0 | 1 | Genetic signal survives triage but direction/modality is not clean enough for promotion. |
| IL2RA | receptor_or_ligand_axis | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 11.72 | manual_or_prior_blocker;prior_branch_closed:cd25_axis_prior_art_and_treg_effector_direction_conflict | cd25_axis_prior_art_and_treg_effector_direction_conflict |  | 0.8341 | 0 | 1 | 1 | Direct clinical or therapeutic-class prior art blocks novelty. |
| GPR65 | intracellular_other | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 10.79 | no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:acid_sensing_gpcr_prior_art_local_mismatch;no_high_confidence_directional_support | acid_sensing_gpcr_prior_art_local_mismatch | Sjogren syndrome | 1 | 0 | 0 | 1 | Genetic signal is plausible but local expression/state support is contradictory. |
| CXCR2 | intracellular_other | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 9.572 | no_strong_ms_anchor;manual_or_prior_blocker;prior_branch_closed:neutrophil_chemokine_axis_prior_art_and_safety | neutrophil_chemokine_axis_prior_art_and_safety | Crohn disease;psoriasis;ulcerative colitis | 0 | 1 | 0 | 1 | prior_art_and_safety_saturated_neutrophil_axis |
| CD40 | intracellular_other | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 8.391 | no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:costimulation_axis_prior_art_and_systemic_safety;no_high_confidence_directional_support | costimulation_axis_prior_art_and_systemic_safety | Crohn disease;ulcerative colitis | 0.7293 | 1 | 0 | 1 | prior_art_saturated_costimulation |
| CTLA4 | receptor_or_ligand_axis | PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED | 7.618 | no_strong_ms_anchor;no_positive_perturbation_or_response_direction;manual_or_prior_blocker;prior_branch_closed:checkpoint_axis_prior_art_systemic_immunosuppression;no_high_confidence_directional_support | checkpoint_axis_prior_art_systemic_immunosuppression |  | 0 | 0 | 0 | 1 | Direct clinical or therapeutic-class prior art blocks novelty. |

## Intervention-Class Summary

| intervention_class | n_candidates | n_parked | n_reopened | max_total_score | median_reachability_score | median_ms_score | median_perturbation_response_score | top_gene |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intracellular_other | 602 | 4 | 0 | 13.51 | 0 | 0 | 0 | PTGER4 |
| receptor_or_ligand_axis | 41 | 3 | 0 | 13.79 | 3 | 1 | 0 | STAT4 |
| kinase_or_phosphosignaling | 10 | 2 | 0 | 16.61 | 4.5 | 0 | 0 | PTPN2 |
| phosphatase_or_signaling_adaptor | 2 | 1 | 0 | 12.17 | 6.062 | 1.5 | 0 | PTPN22 |
| surface_secreted_other | 27 | 0 | 0 | 12.77 | 2 | 0 | 0 | MMP7 |
| enzyme | 14 | 0 | 0 | 12.07 | 2.5 | 0 | 0 | FAP |
| transporter_or_trafficking | 23 | 0 | 0 | 10.38 | 2 | 0 | 0 | KCNJ2 |
| nuclear_regulatory | 10 | 0 | 0 | 10.02 | 0 | 1 | 0 | SP140 |
| lysosomal_enzyme_or_trafficking | 6 | 0 | 0 | 9.15 | 2 | 0 | 2 | IFITM2 |

## Interpretation

This scan deliberately penalizes the pattern that failed in Wave82: a reachable
or recurrent marker is not enough without MS anchoring and directional
perturbation/response support. The ranked table should be used to choose the
next branch only if a parked candidate has a specific missing evidence gap that
can be resolved with an independent dataset or model.

## Outputs

- `reachable_intervention_rank.tsv`
- `reachable_intervention_class_summary.tsv`
- `summary.json`
