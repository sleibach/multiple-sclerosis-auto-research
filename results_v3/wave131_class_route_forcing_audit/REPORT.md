# Wave131 Class-Route Forcing Audit

## Bottom Line

Branch call: `NO_CLASS_ROUTE_REOPENED_AFTER_WAVE130`.

This wave retested the least-bad post-Wave129 intervention classes after the
corrected Wave130 MS treatment-response audit. The test asks whether class-level
reachability plus any MS response rescue is enough to reopen a route for target
nomination.

## Decisions

| candidate | call | gate_pass | forced_question | required_ms_feature | wave130_ms_feature_call | reachable_modality | cross_disease_cellstate | ms_anchor_or_response_rescue | target_resolution_genetics | direct_perturbation_or_response | prior_not_blocked | safety_direction_clear | specificity_not_generic | critical_failures | source_call | primary_blocker | late_blocker | l1000_rows_matching_class | genetics_rows_matching_class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eicosanoid_receptors | NO_REOPEN_CLASS_ROUTE | 4/8 | Can a leukotriene/prostaglandin/eicosanoid intervention be narrowed to a selective lipid-lysosomal myeloid controller? | lipid_loader_repair | NO_CROSS_MS_REPLICATION | True | True | True | False | True | False | False | False | target_resolution_genetics;prior_not_blocked;safety_direction_clear;specificity_not_generic | NO_GO | Leukotriene/prostaglandin immunology is crowded, directionally contradictory, and not selective for the V3 APC state. | directionally contradictory leukotriene/prostaglandin biology and prior-art crowding | 0 | 0 |
| MED16_MEDIATOR_MODULE | NO_REOPEN_CLASS_ROUTE | 4/8 | Does the strong Med16 perturbation signal overcome the lack of MS anchor and broad transcriptional toxicity risk? | ifn_apc | REPRODUCES_DIRECTIONALLY_SMALL_N | True | False | False | False | True | True | False | True | cross_disease_cellstate;ms_anchor;target_resolution_genetics;safety_direction_clear | WETLAB_ONLY_MED16_SELECTIVE_NONDRUGGABLE_ROUTE | The real Med16_KO signal is strong, but the route lacks a target-specific MS anchor and a safe selective druggable handle; practical Mediator/CDK8/19 modulation risks broad transcriptional or oncology-like toxicity. | no safe selective druggable Mediator-module handle | 0 | 0 |
| GALC_LYSOSOMAL_SPHINGOLIPID | NO_REOPEN_CLASS_ROUTE | 4/8 | Does the genetics/lysosomal recurrence around GALC survive enough gates to become a sphingolipid intervention route? | lysosomal_apc | NO_CROSS_MS_REPLICATION | True | True | False | True | False | False | False | True | ms_anchor;direct_perturbation_or_response;prior_not_blocked;safety_direction_clear | NO_GO_LYSOSOMAL_MODEL_REOPENER | foundation_model_support; strict_ms_white_matter; module_specific_residual; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking | failed genetics-first reopening and unclear safe directionality | 0 | 1 |
| retinoid_vdr_rxr | NO_REOPEN_CLASS_ROUTE | 3/8 | Can retinoid/VDR/RXR differentiation biology be made tissue-selective enough to count as a druggable autoimmune repair controller? | lipid_loader_repair | NO_CROSS_MS_REPLICATION | True | True | True | False | False | False | False | False | target_resolution_genetics;direct_perturbation_or_response;prior_not_blocked;safety_direction_clear;specificity_not_generic | NO_GO | Vitamin D, retinoic-acid, and RXR/RAR immunomodulation are very crowded and pleiotropic. | vitamin D/retinoid/RXR autoimmune prior art and pleiotropic nuclear-receptor biology | 0 | 0 |

## Interpretation

No class is reopened unless it passes reachable modality, MS anchor or MS
response rescue, target-resolution genetics, direct perturbation or response,
prior-art freedom, direction/safety, and specificity gates. This prevents a
broad class such as eicosanoids, retinoids, or IFN/APC biology from becoming a
target claim merely because it is biologically plausible.

## Reproducibility

- Script: `scripts/v3_wave131_class_route_forcing_audit.py`
- Outputs: `results_v3/wave131_class_route_forcing_audit/`
- Seed: `20260527`
