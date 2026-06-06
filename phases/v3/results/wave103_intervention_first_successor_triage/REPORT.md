# Wave103 Intervention-First Successor Triage

## Bottom Line

Branch call: `NO_INTERVENTION_FIRST_SUCCESSOR_SURVIVES_ALL_GATES`.

This wave starts from non-expression anchors rather than marker recurrence. It
does not yet produce a therapeutic finding. It identifies candidates that are
worth route-specific sidecars only if they have perturbation/model/genetic or
druggability evidence before expression is considered.

## Reopened / Top Candidates

| gene | wave103_call | wave103_score | wave103_gate_count | has_direct_perturbation | has_foundation_support | ms_anchor | cross_disease_anchor | reachable_modality | prior_or_safety_blocked | wrong_direction_or_undruggable | intervention_class | positive_disease_count | genetic_breadth_disease_count | ms_expr_delta | ms_expr_p | ms_genetic_score | model_support_contexts_w57 | model_strong_contexts_w57 | direct_perturbation_detail | chembl_activity_count | manual_route | manual_blocker | wave103_missing_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CD9 | NO_GO_WRONG_DIRECTION_OR_UNDRUGGABLE | 7 | 3 | True | False | True | False | False | False | True |  | 0 | 0 | 1.11 | 0.001969 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 | surface tetraspanin; local CRISPR suggests knockout enhances efferocytosis | tetraspanin pleiotropy and unclear safe inhibition/agonism direction | cross_disease_anchor;reachable_modality |
| DAB2 | NO_GO_WRONG_DIRECTION_OR_UNDRUGGABLE | 7 | 3 | True | False | True | False | False | False | True |  | 0 | 0 | 0.5379 | 0.01113 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 | intracellular adaptor; DAB2 loss enhances macrophage efferocytosis in local CRISPR screen | not externally druggable; agonist/restoration route is unclear | cross_disease_anchor;reachable_modality |
| PARK7 | NO_GO_NO_MS_ANCHOR | 11.7 | 3 | False | True | False | True | False | False | False | intracellular_other | 3 | 5 | 0.171 | 0.4469 | 0 | 2 | 0 |  | 0 |  |  | ms_anchor;reachable_modality |
| BLK | NO_GO_NO_MS_ANCHOR | 11.4 | 3 | True | False | False | True | False | False | False | intracellular_other | 1 | 4 | 0 | 1 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;reachable_modality |
| LRRC61 | NO_GO_NO_MS_ANCHOR | 10.6 | 3 | True | False | False | True | False | False | False |  | 4 | 0 | 0.6971 | 0.582 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;reachable_modality |
| CLEC7A | NO_GO_NO_MS_ANCHOR | 10.2 | 3 | True | False | False | True | False | False | False |  | 3 | 0 | -0.3549 | 0.1287 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;reachable_modality |
| FAM49B | NO_GO_NO_MS_ANCHOR | 10.2 | 3 | True | False | False | True | False | False | False |  | 3 | 0 | 0.1048 | 0.3463 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;reachable_modality |
| ITPR3 | NO_GO_NO_MS_ANCHOR | 8.3 | 3 | False | False | False | True | True | False | False | intracellular_other | 2 | 5 | 0 | 0.4261 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support |
| NKD1 | NO_GO_NO_MS_ANCHOR | 7.8 | 2 | False | False | False | True | False | False | False | intracellular_other | 2 | 8 | 0 | 0.8167 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| TNFSF15 | NO_GO_NO_MS_ANCHOR | 7.8 | 2 | False | False | False | True | False | False | False | intracellular_other | 2 | 10 | 0.3944 | 0.7557 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| IFIH1 | NO_GO_NO_MS_ANCHOR | 7.4 | 2 | False | False | False | True | False | False | False | intracellular_other | 1 | 8 | 0.07624 | 0.8386 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| SMAD3 | NO_GO_NO_MS_ANCHOR | 7.4 | 2 | False | False | False | True | False | False | False | intracellular_other | 1 | 9 | 0.1728 | 0.3985 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| FUT2 | NO_GO_NO_MS_ANCHOR | 7.3 | 2 | False | False | False | True | False | False | False | intracellular_other | 2 | 7 | 0.1409 | 0.8797 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| IRF4 | NO_GO_NO_MS_ANCHOR | 7.3 | 2 | False | False | False | True | False | False | False | intracellular_other | 2 | 7 | 0.04445 | 0.9107 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| CARMIL1 | NO_GO_NO_MS_ANCHOR | 7.2 | 2 | False | False | False | True | False | False | False | intracellular_other | 3 | 6 | 0 | 1 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| PRDM1 | NO_GO_NO_MS_ANCHOR | 7.2 | 2 | False | False | False | True | False | False | False | intracellular_other | 3 | 6 | 0 | 0.9031 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| ADGRL2 | NO_GO_NO_MS_ANCHOR | 7 | 2 | False | False | False | True | False | False | False | intracellular_other | 0 | 9 | 0 | 0.3626 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| ANKRD30A | NO_GO_NO_MS_ANCHOR | 7 | 2 | False | False | False | True | False | False | False | intracellular_other | 0 | 8 | 0 | 1 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| FLT3 | NO_GO_NO_MS_ANCHOR | 7 | 3 | False | False | False | True | True | False | False | intracellular_other | 0 | 4 | 0 | 0.4934 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support |
| JAZF1 | NO_GO_NO_MS_ANCHOR | 7 | 2 | False | False | False | True | False | False | False | intracellular_other | 0 | 8 | 0 | 0.03951 | 0.4559 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| MUC19 | NO_GO_NO_MS_ANCHOR | 7 | 2 | False | False | False | True | False | False | False | intracellular_other | 0 | 8 | 0 | 1 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| NKX2-3 | NO_GO_NO_MS_ANCHOR | 7 | 2 | False | False | False | True | False | False | False | intracellular_other | 0 | 9 | 0 | 1 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| RASGRP1 | NO_GO_NO_MS_ANCHOR | 7 | 2 | False | False | False | True | False | False | False | intracellular_other | 0 | 8 | 0.5213 | 0.6479 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| UBASH3A | NO_GO_NO_MS_ANCHOR | 7 | 2 | False | False | False | True | False | False | False | intracellular_other | 0 | 8 | 0.2675 | 0.7746 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| PRKCB | NO_GO_NO_MS_ANCHOR | 6.9 | 2 | False | False | False | True | False | False | False | intracellular_other | 1 | 7 | 0.206 | 0.4904 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| SKAP2 | NO_GO_NO_MS_ANCHOR | 6.9 | 2 | False | False | False | True | False | False | False | intracellular_other | 1 | 7 | 0 | 0.638 | 0.1297 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| ABTB2 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | -0.1477 | 0.8826 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| BANK1 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | False | False | False | True | False | False | False | intracellular_other | 2 | 6 | 0 | 0.2391 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| CCDC121 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | 0.443 | 0.2381 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| CDKAL1 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | False | False | False | True | False | False | False | intracellular_other | 2 | 6 | 0 | 0.4021 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| CHST11 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | -0.2507 | 0.1533 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| CHUK | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | 0.2238 | 0.3212 | 0 | 0 | 0 | wave15:weak_selective_target_suppression:weak_followup_only | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| FBXO16 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | -999 | 1 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| MED16 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | -0.06015 | 0.8241 | 0 | 0 | 0 | wave15:selective_target_suppression:strong_mechanistic_comparator_not_druggable | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| RECQL4 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | -0.1913 | 0.8339 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| RYK | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | 0.08131 | 0.5201 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| SLC39A11 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | False | False | False | True | False | False | False | intracellular_other | 2 | 6 | 0.271 | 0.7607 | 0 | 0 | 0 |  | 0 |  |  | ms_anchor;direction_or_response_support;reachable_modality |
| TPX2 | NO_GO_NO_MS_ANCHOR | 6.8 | 2 | True | False | False | False | False | False | False |  | 2 | 0 | 0.3887 | 0.7566 | 0 | 0 | 0 | wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0 |  |  | ms_anchor;cross_disease_anchor;reachable_modality |
| APOL1 | NO_GO_NO_MS_ANCHOR | 6.6 | 3 | False | False | False | True | True | False | False | transporter_or_trafficking | 4 | 0 | 0 | 0.594 | 0 | 0 | 0 |  | 593 |  |  | ms_anchor;direction_or_response_support |
| CASP4 | NO_GO_NO_MS_ANCHOR | 6.6 | 3 | False | False | False | True | True | False | False | surface_secreted_other | 4 | 0 | 0.2067 | 0.4927 | 0 | 0 | 0 |  | 61 |  |  | ms_anchor;direction_or_response_support |

## Interpretation

- High-scoring prior-art-heavy nodes remain blocked even when genetics and
  druggability are strong. This prevents the run from rediscovering IL7R,
  CXCR2, TYK2, IL23R, PTPN2, or broad MHC/cytokine axes as supposedly novel.
- Direct perturbation-only candidates such as `DAB2` and `CD9` are useful
  biology, but they still fail as translational targets if modality and
  direction cannot be made plausible.
- Candidates reopened by this wave require sidecar validation. The score is a
  dispatch tool, not a claim.

## Dispatch Recommendation

No immediate route-specific sidecar candidate survived all gates.

## Reproducibility

- Script: `scripts/v3_wave103_intervention_first_successor_triage.py`
- Rank table: `results_v3/wave103_intervention_first_successor_triage/intervention_first_successor_rank.tsv`
- Summary: `results_v3/wave103_intervention_first_successor_triage/summary.json`
- Seed: `20260527`
