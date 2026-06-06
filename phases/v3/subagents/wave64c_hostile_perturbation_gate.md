# Wave64-C Hostile Perturbation-Gate Review

Status: completed.

Date: 2026-05-27.

Role: hostile perturbation-gate reviewer.

## Verdict

Default rule: **no perturbation-first or treatment-response route may be promoted
to a V3 therapeutic claim unless it demonstrates selective, directionally
correct repair of the lipid-lysosomal myeloid state in human disease-relevant
cells, with guardrails showing preserved repair, debris handling, and host
defense.**

Wave26 already showed that treatment-response signals are fragile after global
FDR, generic-inflammation adjustment, and independent replication. Wave63
already closed transition-controller intersections because they lacked direct
disease-relevant perturbation. The next branch must not re-open these routes by
renaming weak pharmacodynamic or module-score movements as mechanism.

This document defines minimum acceptance rules for local scripts. It does not
claim a finding.

## Core Principle

A perturbation-first V3 claim must satisfy three independent questions in the
same direction:

1. **Disease anchor:** is the candidate node active in the claimed disease-cell
   state after accounting for cell composition, batch, tissue damage, treatment,
   and generic inflammation?
2. **Perturbation anchor:** does modulating the node causally move that state in
   the intended direction in a relevant human cell or tissue system?
3. **Therapeutic guardrail:** does the perturbation preserve or improve repair,
   debris clearance, lysosomal function, cholesterol handling, viability, and
   host-defense competence?

If any answer is missing, the route is assay-design material only.

## Claim-Freeze Gate

Before scoring, scripts must freeze the exact claim in machine-readable fields:

- `target_node`
- `intervention_node`
- `intervention_direction`: `activate`, `inhibit`, `replace`, `degrade`,
  `agonize`, `antagonize`, or `unknown`
- `modality`: `small_molecule`, `antibody`, `enzyme_replacement`,
  `ASO_siRNA`, `cell_therapy`, `other`
- `lead_disease`
- `replication_diseases`
- `claimed_cell_type`
- `claimed_tissue`
- `claimed_state`
- `expected_module_direction`
- `expected_functional_guardrail_direction`
- `primary_readout`
- `heldout_readouts`
- `negative_controls`
- `prior_art_search_string`

Stop rule: if `intervention_direction == unknown`, `claimed_cell_type` is
missing, or `heldout_readouts` is empty, set `wave64c_call = NO_GO_UNFROZEN_CLAIM`.

## Minimum Promotion Gates

All gates below must pass for promotion. A partial pass is not a finding.

| Gate | Required implementation | Hard stop |
| --- | --- | --- |
| Human disease-cell anchor | Donor-level effect in claimed cell/tissue; FDR <= 0.10 in MS plus at least two non-MS autoimmune datasets; sign-stable after residualization. | `NO_GO_NO_HUMAN_DISEASE_ANCHOR` |
| Direct perturbation | Human primary myeloid, microglia-like, or disease-tissue explant perturbation; dose-response; target engagement; donor replication. | `NO_GO_NO_DIRECT_HUMAN_PERTURBATION` |
| Directionality | Perturbation direction matches disease direction and proposed intervention direction. | `NO_GO_WRONG_OR_UNKNOWN_DIRECTION` |
| Generic inflammation control | Effect survives residualization or matching against IFN, TNF/NF-kB, IL6/JAK/STAT, inflammasome, cell stress, and tissue-damage modules. | `NO_GO_GENERIC_INFLAMMATION_ONLY` |
| Cell-composition control | Within-cell-type pseudobulk or single-cell mixed model with donor as unit; composition covariates; unchanged conclusion after excluding abundance-shift-dominated compartments. | `NO_GO_CELL_COMPOSITION_CONFONDED` |
| Batch control | Dataset, donor, chemistry, run, site, timepoint, and treatment-arm covariates where available; no single-batch or single-donor drive. | `NO_GO_BATCH_OR_DONOR_DRIVEN` |
| Endpoint independence | Candidate selection module and validation module must be disjoint or leave-family-out; at least one protein, flow, functional, or spatial readout. | `NO_GO_ENDPOINT_CIRCULARITY` |
| Drug-class specificity | Compare against same-class and broad anti-inflammatory controls; candidate must outperform generic class effect on target state and guardrails. | `NO_GO_DRUG_CLASS_NONSPECIFIC` |
| Repair guardrail | Preserved or improved efferocytosis, myelin-debris or tissue-relevant debris clearance, lysosomal cargo handling, cholesterol efflux, and repair/resolution markers. | `NO_GO_REPAIR_GUARDRAIL_FAIL` |
| Host-defense guardrail | Preserved antiviral, antimicrobial, antigen-processing competence where relevant, viability, mitochondrial fitness, and non-cytotoxicity. | `NO_GO_HOST_DEFENSE_OR_TOXICITY_FAIL` |
| Cross-disease replication | Same direction in at least three autoimmune diseases, with at least two independent evidence channels beyond expression recurrence. | `NO_GO_NO_CROSS_DISEASE_REPLICATION` |
| Prior-art freeze | Literature, preprint, patent, trial, and pipeline search after exact claim freeze. | `NO_GO_PRIOR_ART_BLOCKED_OR_UNSEARCHED` |

Promotion condition:

```text
promote =
  disease_anchor_pass
  and direct_perturbation_pass
  and directionality_pass
  and generic_inflammation_pass
  and cell_composition_pass
  and batch_pass
  and endpoint_independence_pass
  and drug_class_specificity_pass
  and repair_guardrail_pass
  and host_defense_guardrail_pass
  and cross_disease_replication_pass
  and prior_art_pass
```

Anything else is `NO_GO`, `PARK_ASSAY_DESIGN`, or `POSITIVE_CONTROL_ONLY`.

## Implementable Script Columns

Add these columns to any Wave64 perturbation/treatment-response table:

- `claim_frozen`
- `human_disease_anchor_fdr`
- `human_disease_anchor_disease_count`
- `human_disease_anchor_sign_stable`
- `residualized_generic_fdr`
- `residualized_generic_effect`
- `raw_target_effect`
- `generic_effect_max_abs`
- `target_to_generic_effect_ratio`
- `cell_composition_adjusted_effect`
- `cell_composition_sensitivity_call`
- `batch_sensitivity_call`
- `donor_n`
- `donor_min_group_n`
- `direct_human_perturbation`
- `dose_response`
- `target_engagement`
- `genetic_pharmacologic_concordance`
- `direction_matches_claim`
- `heldout_readout_pass`
- `protein_or_functional_validation`
- `same_class_control_margin`
- `broad_antiinflammatory_control_margin`
- `efferocytosis_guardrail`
- `debris_clearance_guardrail`
- `lysosome_function_guardrail`
- `cholesterol_efflux_guardrail`
- `repair_resolution_marker_guardrail`
- `antiviral_guardrail`
- `antimicrobial_guardrail`
- `viability_guardrail`
- `cytotoxicity_signature`
- `cross_disease_same_direction_count`
- `cross_disease_independent_channel_count`
- `prior_art_search_completed`
- `prior_art_blocker`
- `wave64c_failed_gates`
- `wave64c_call`

Recommended thresholds:

- `donor_n >= 20` total and `donor_min_group_n >= 8` for discovery; stricter
  claims should require independent replication, not larger p-value mining.
- `human_disease_anchor_fdr <= 0.10`.
- `residualized_generic_fdr <= 0.10`.
- `abs(target_to_generic_effect_ratio) >= 2.0` for a module-specific claim.
- `same_class_control_margin > 0` and
  `broad_antiinflammatory_control_margin > 0`.
- all guardrail fields must be `preserved`, `improved`, or `not_tested_blocking`;
  `not_tested_blocking` blocks promotion but permits assay-design parking.
- `prior_art_blocker == False`.

## Confounder Attacks And Stop Rules

### Clinical Response Confounding

Response labels are downstream clinical outcomes, not clean mechanisms. Baseline
responder/nonresponder contrasts can reflect disease severity, prior therapy,
cell composition, concomitant medication, or regression to the mean.

Stop rules:

- If only responder/nonresponder baseline expression exists, require global FDR
  <= 0.10, generic-adjusted FDR <= 0.10, and independent same-direction
  replication. Otherwise `NO_GO_RESPONSE_CONFOUNDED`.
- If pharmacodynamic movement exists only in responders, do not claim mechanism
  unless the same movement appears in nonresponder target-engaged cells or is
  mediated by target engagement. Otherwise `NO_GO_RESPONSE_MEDIATED_ONLY`.
- Do not use clinical response as both selection endpoint and validation
  endpoint.

### Cell-Composition Confounding

The lipid-lysosomal myeloid module can increase because there are more myeloid
cells, more activated macrophages, more damaged tissue, or more plasma cells in
the sample. A bulk or marker-derived compartment score is insufficient.

Stop rules:

- If no within-cell-type analysis exists, `NO_GO_CELL_COMPOSITION_CONFONDED`.
- If the effect disappears after adjusting for cell-type abundance,
  `NO_GO_CELL_COMPOSITION_CONFONDED`.
- If the effect is present only in marker-derived compartments without
  single-cell donor-level support, at most `PARK_WEAK_COMPARTMENT_PROXY`.

### Generic Inflammation

JAK/TYK, TNF, IL-17/23, NF-kB, steroid, interferon, and stress-response
pathways will move many inflammatory modules. That is not sufficient.

Stop rules:

- If target-state reduction is not at least two-fold larger than the largest
  generic IFN/TNF/NF-kB/IL6-JAK/inflammasome/stress effect,
  `NO_GO_GENERIC_INFLAMMATION_ONLY`.
- If the only positive readouts are HLA-II, CD74, CXCL, ISG, S100, or cytokine
  genes selected into the query module, `NO_GO_ENDPOINT_CIRCULARITY`.
- If broad transcription, translation, heat-shock, apoptosis, or cell-cycle
  signatures dominate, `NO_GO_CYTOTOXIC_OR_STRESS_SIGNATURE`.

### Reverse Causation

A disease-associated cell state can be compensatory. Suppressing it may worsen
repair or host defense.

Stop rules:

- If disease direction and perturbation direction are not explicitly linked,
  `NO_GO_WRONG_OR_UNKNOWN_DIRECTION`.
- If a node is up in disease but perturbation evidence shows that inhibiting it
  impairs debris clearance or repair, `NO_GO_COMPENSATORY_REPAIR_NODE`.
- If genetics suggests protective upregulation but the proposed therapy inhibits
  the node, `NO_GO_GENETIC_DIRECTION_CONFLICT`.

### Batch, Site, And Donor Effects

Single-study perturbation signals are vulnerable to chemistry, site, library,
timepoint, and donor effects.

Stop rules:

- If one donor, one batch, one site, or one timepoint accounts for the effect,
  `NO_GO_BATCH_OR_DONOR_DRIVEN`.
- If train/test split is by cell rather than donor, do not count it as
  replication.
- If discovery and validation use the same accession and same endpoint family,
  count it as internal sensitivity only, not independent replication.

### Endpoint Circularity

The branch must not select a target because it reverses a module and validate it
by showing the same module moved.

Stop rules:

- If discovery genes overlap validation genes by Jaccard > 0.25 and no
  leave-family-out validation is provided, `NO_GO_ENDPOINT_CIRCULARITY`.
- If the target is part of the readout module and drives the score,
  recompute with target-family genes removed. If the result fails,
  `NO_GO_TARGET_IN_READOUT_CIRCULARITY`.
- Require at least one held-out functional, protein, or spatial readout before
  any therapeutic promotion.

### Drug-Class Nonspecificity

Drug classes with known broad immunosuppressive effects should be positive
controls unless the new claim is more specific than the class.

Stop rules:

- If a candidate performs no better than steroids, JAK/TYK inhibition,
  anti-TNF, IL-17/23 blockade, NF-kB inhibition, or HSP90/cytotoxic controls,
  `NO_GO_DRUG_CLASS_NONSPECIFIC`.
- If the proposed intervention is simply a known successful autoimmune drug
  class applied to another autoimmune disease without a new stratification,
  delivery, or mechanism delta, `POSITIVE_CONTROL_ONLY`.

### Wrong Tissue Or Wrong Cell

The shared module is myeloid and tissue-shaped. PBMC or cancer-cell perturbation
alone is not enough for a tissue-compartment claim.

Stop rules:

- MS claim requires lesion, CSF, microglia-like, monocyte-derived macrophage
  with myelin challenge, or lesion-relevant explant support.
- IBD claim requires lamina propria, intestinal macrophage, epithelial-myeloid
  coculture, or gut explant support.
- RA claim requires synovial macrophage/fibroblast interaction support.
- Psoriasis claim requires lesional skin myeloid/keratinocyte axis support.
- If tissue support is absent, `PARK_WRONG_TISSUE_HYPOTHESIS_ONLY`.

### Missing Repair And Host-Defense Guardrails

The module cannot be treated as purely pathogenic. Phagolysosomal, APC, and
lipid-handling programs can be required for clearance, remyelination support,
antiviral defense, and antimicrobial defense.

Stop rules:

- If efferocytosis or debris clearance is reduced, `NO_GO_REPAIR_GUARDRAIL_FAIL`.
- If lysosomal acidification, cargo processing, or cholesterol efflux worsens,
  `NO_GO_LYSOSOME_OR_LIPID_GUARDRAIL_FAIL`.
- If antiviral or antimicrobial response is suppressed below positive-control
  safety margins, `NO_GO_HOST_DEFENSE_FAIL`.
- If no guardrail assay exists, `PARK_ASSAY_DESIGN_NOT_PROMOTION`.

### Prior-Art Leakage

Prior-art searches must occur after the exact claim is frozen. Searching broad
gene names before the intervention direction is fixed is not enough.

Stop rules:

- If direct literature, patent, clinical-trial, or pipeline precedent covers the
  same target, direction, disease family, and biomarker mechanism,
  `NO_GO_PRIOR_ART_BLOCKED`.
- If prior-art search did not include patents and trial registries,
  `NO_GO_PRIOR_ART_UNSEARCHED`.
- If the novelty delta is only "we use a different module score",
  `NO_GO_FALSE_NOVELTY`.

## Route-Specific Hostile Calls

| Route | Default Wave64-C call | Promotion requirement beyond generic gates |
| --- | --- | --- |
| JAK/TYK | `POSITIVE_CONTROL_ONLY` | Must show a target-specific, non-broad repair transition not explained by known JAK/TYK anti-inflammatory action; prior-art barrier is high. |
| IL-17/23 | `POSITIVE_CONTROL_ONLY` | Must show direct lipid-lysosomal myeloid repair mechanism beyond known psoriasis/IBD axis and without merely tracking response. |
| Anti-TNF | `NO_GO_FOR_MS_THERAPEUTIC_DIRECTION` | MS/demyelination risk makes this a comparator or negative-control route unless the claim is outside MS and has disease-specific safety justification. |
| IL7R/CD127 | `NO_GO_PRIOR_ART_BLOCKED_UNLESS_NEW_DOWNSTREAM_NODE` | Must identify a downstream, cell-state-specific intervention distinct from CD127 blockade, with human perturbation and novelty. |
| SP140-to-topoisomerase rescue | `PARK_CROHN_COMPARATOR` | Requires non-genotoxic, non-cytotoxic rescue of SP140-loss myeloid chromatin phenotype and independent MS/cross-autoimmune relevance; topoisomerase inhibition itself is not acceptable as a therapeutic route. |
| Lysosomal enzymes/GALC | `PARK_DIRECTIONALITY_AND_DELIVERY_UNRESOLVED` | Must distinguish enzyme replacement, activation, inhibition, and substrate modulation; must prove preserved myelin-debris processing and no lysosomal stress. |
| IFI30/antigen processing | `NO_GO_HOST_DEFENSE_RISK_UNLESS_SELECTIVE_CONTEXT_CONTROL` | Requires preserving antimicrobial/antiviral antigen processing while reducing pathogenic APC state; MS-only target resolution is not enough. |
| Phagolysosomal modulators | `PARK_ASSAY_DESIGN` | Must provide functional phagocytosis/efferocytosis/debris-clearance assays, not just cathepsin or lysosome gene expression. |
| Lipid-handling nodes | `PARK_COMPENSATORY_STATE_RISK` | Must separate foam-cell/pathogenic lipid loading from reparative lipid export and resolution; require cholesterol efflux and repair-marker guardrails. |

## Local Script Stop-Rule Pseudocode

```python
failed = []

if not claim_frozen:
    failed.append("unfrozen_claim")
if not direct_human_perturbation:
    failed.append("no_direct_human_perturbation")
if not direction_matches_claim:
    failed.append("wrong_or_unknown_direction")
if human_disease_anchor_fdr > 0.10 or human_disease_anchor_disease_count < 3:
    failed.append("weak_human_disease_anchor")
if residualized_generic_fdr > 0.10:
    failed.append("generic_adjusted_not_significant")
if abs(target_to_generic_effect_ratio) < 2.0:
    failed.append("generic_inflammation_only")
if cell_composition_sensitivity_call != "robust":
    failed.append("cell_composition_confounding")
if batch_sensitivity_call != "robust":
    failed.append("batch_or_donor_driven")
if not heldout_readout_pass:
    failed.append("endpoint_circularity")
if same_class_control_margin <= 0 or broad_antiinflammatory_control_margin <= 0:
    failed.append("drug_class_nonspecific")
for guardrail in [
    efferocytosis_guardrail,
    debris_clearance_guardrail,
    lysosome_function_guardrail,
    cholesterol_efflux_guardrail,
    repair_resolution_marker_guardrail,
    antiviral_guardrail,
    antimicrobial_guardrail,
    viability_guardrail,
]:
    if guardrail not in {"preserved", "improved"}:
        failed.append("repair_or_host_defense_guardrail_missing_or_failed")
        break
if cytotoxicity_signature:
    failed.append("cytotoxicity_signature")
if cross_disease_same_direction_count < 3:
    failed.append("weak_cross_disease_replication")
if cross_disease_independent_channel_count < 2:
    failed.append("single_channel_only")
if not prior_art_search_completed:
    failed.append("prior_art_unsearched")
if prior_art_blocker:
    failed.append("prior_art_blocked")

if not failed:
    wave64c_call = "PROMOTION_ELIGIBLE_FOR_ORCHESTRATOR_REVIEW"
elif {"no_direct_human_perturbation", "repair_or_host_defense_guardrail_missing_or_failed"} & set(failed):
    wave64c_call = "PARK_ASSAY_DESIGN_NOT_PROMOTION"
else:
    wave64c_call = "NO_GO_" + ";".join(failed[:4])
```

## Final Instruction To The Orchestrator

Use perturbation and treatment-response data to falsify or design assays, not to
promote candidates by module-score movement. A candidate must survive
directionality, generic-inflammation, cell-composition, endpoint-independence,
repair, host-defense, and prior-art gates before it can be considered a V3
therapeutic claim. Known broad autoimmune mechanisms should be treated as
controls unless the local analysis proves a new, selective, tissue-relevant
intervention point.
