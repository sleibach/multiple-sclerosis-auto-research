# Failure Structure And Exclusion Mapping V39

Status: **value-complete for Workstreams 1 and 2**.

This report treats the project's documented killed, closed, parked, and
decoupling items as a dataset. It does not introduce new biological
measurements. All pattern tests are computed from committed V37/V38 ledgers and
use exact small-n hypergeometric nulls to reduce the risk of narrating structure
into a small failure set.

## Inputs

- V37 scored findings: `docs/reports/FINDINGS_SCORES_V37.tsv`
- V38 failure annotations:
  `analysis/v38_failure_structure/failure_mode_table.tsv`
- V38 direction/modality labels:
  `analysis/v38_direction_modality_prefilter/direction_modality_annotated_failures.tsv`
- V38 exclusion ledger:
  `analysis/v38_exclusion_ledger/exclusion_nonreplication_ledger.tsv`
- V39 script: `scripts/v39_failure_structure_and_exclusion.py`
- V39 output directory: `analysis/v39_failure_structure_exclusion/`

## Workstream 1: Structure Of Failure

Failure frame: `20` V37/V38 killed, closed, parked, or
decoupling items.

### Verdict

There is **no single universal failure mechanism** across the project. The
strongest null-tested pattern is narrower:

- **Supported:** context/axis dependence is enriched in cross-axis transfer
  failures (`p=0.007224`).
- **Supported but sparse:** generic immune-tone collapse is enriched inside
  exploratory-module failures (`p=0.031579`) but appears in only `2` rows, so it
  is an audit panel, not a universal MS failure law.
- **Suggestive, not formally established:** direction/modality constraints are
  enriched in target-nomination-like leads (`4/6`, expected `2.1`,
  `p=0.077657`), and hard restoration/up-function constraints are similarly
  suggestive (`2/6`, expected `0.6`, `p=0.078947`).
- **Not supported as a specific enrichment:** evidence-resolution gaps are
  common, but not specifically enriched in genetics/target-like failures
  (`p=0.455108`).

Medical-team implication: future leads should be prefiltered by **axis/context,
direction/modality, and specificity/tone controls** before any wet-lab spend.
Only the first of these is formally enriched in this small frame; the others are
practical guardrails supported by repeated failures and suggestive null tests,
not universal laws.

### Pattern Family Counts

| pattern_family | count | fraction_of_failure_frame |
| --- | --- | --- |
| direction_or_modality_constraint | 7 | 0.35 |
| hard_restoration_or_up_function | 2 | 0.1 |
| context_or_axis_dependence | 7 | 0.35 |
| specificity_or_tone_constraint | 7 | 0.35 |
| generic_immune_tone_specific | 2 | 0.1 |
| evidence_resolution_gap | 6 | 0.3 |

### Exact Null Tests

| pattern | frame_n | pattern_count | subset | subset_n | observed_in_subset | expected_under_random_assignment | exact_hypergeom_tail_p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| direction_or_modality_constraints_enriched_in_target_nomination_like_leads | 20 | 7 | target_nomination_like | 6 | 4 | 2.1 | 0.077657 | suggestive_not_established |
| hard_restoration_or_up_function_enriched_in_target_nomination_like_leads | 20 | 2 | target_nomination_like | 6 | 2 | 0.6 | 0.078947 | suggestive_not_established |
| context_axis_dependence_enriched_in_cross_axis_transfer_rows | 20 | 7 | mechanism_level_cross_axis_transfer | 4 | 4 | 1.4 | 0.007224 | supported_enrichment |
| specificity_or_tone_constraints_enriched_in_exploratory_modules | 20 | 7 | mechanism_level_exploratory_module | 4 | 3 | 1.4 | 0.101135 | suggestive_not_established |
| generic_immune_tone_specific_constraints_enriched_in_exploratory_modules | 20 | 2 | mechanism_level_exploratory_module | 4 | 2 | 0.4 | 0.031579 | supported_enrichment |
| evidence_resolution_gaps_enriched_in_genetics_or_target_like_leads | 20 | 6 | genetics_or_target_like | 8 | 3 | 2.4 | 0.455108 | not_supported_as_statistical_regularity |

### Target-Nomination-Like Failures

| item | evidence_grade | mechanism_level | therapeutic_constraint | failure_modes |
| --- | --- | --- | --- | --- |
| chr1 KIF21B/GPR25 locus resolves to real biology but hard target | supported | genetics_to_target | restoration_or_up_function_required | hard_protective_direction;causal_gene_ambiguity;weak_modality_fit |
| MHC overlap is distinct-signal, not simple shared biology | negative-established | genetics_coloc | shared_region_not_shared_target | distinct_causal_variants;overlap_not_mechanism |
| GPR25 demoted from protected favorite | negative-established | genetics_to_target | agonism_or_restoration_required | causal_gene_ambiguity;weak_expression_support;hard_protective_direction;immature_chemical_matter |
| NAMPT/eNAMPT not reactivated as target | negative-established | target_nomination | covariate_not_target | marker_not_driver;weak_genetic_support;prior_art_not_enough |
| ZFP36L1 chr14 parked | provisional | genetics_coloc | no_direction_matched_target | subthreshold_coloc;missing_qtl_direction |
| REL/PUS10/USP34 chr2 closed | negative-established | genetics_coloc | no_shared_disease_signal | coloc_failure;expression_cannot_rescue |

## Workstream 2: Rigorous Exclusion / Non-Replication Mapping

Exclusions recorded: `16`.

Non-replication-like items recorded: `9`.

### Verdict

The exclusion map is a stop-spending instrument, not a claim that the biology is
irrelevant. Most rows mean a specific translational interpretation is not
supported: not a target, not a clinical threshold, not a broad response rule,
not a clean transfer locus, not EBV-specific, or not validated as a simulator.

### Exclusion List

| exclusion | scope | strength | decision_value |
| --- | --- | --- | --- |
| Baseline IFN/APC is not a valid general fallback stratifier | cross-disease treatment response | negative_established | Do not substitute baseline IFN/APC for early on-treatment delta. |
| V22 scalar is not a broad cross-therapy response rule | MS/autoimmune treatment response | negative_established | Do not transfer the rule to fingolimod, adalimumab, or arbitrary DMTs without direct validation. |
| V22 scalar is not a calibrated clinical threshold | clinical utility | negative_established | Use only rank/direction validation until a fresh cohort calibrates a threshold. |
| Glucocorticoid/steroid signature does not explain the bounded scalar | treatment-response confounding | supported_exclusion | Steroid control remains required, but current data do not justify killing the scalar as steroid artifact. |
| Simple marker-level cell-composition shift does not explain the bounded scalar | treatment-response confounding | supported_exclusion | Future validation still needs composition adjustment, but current data do not reduce the scalar to composition. |
| Receptor-only CD74/CD44/CXCR4 does not dominate the scalar | treatment-response mechanism | negative_established | Do not replace the scalar with receptor-only readout. |
| Coupled/dynamic/flexible ML variants do not improve over the scalar | treatment-response modeling | negative_established | Do not lock a successor rule from held data. |
| A broad immune-state simulator is not validated from current data | in-silico modeling | negative_established | Do not use the simulator for patient response, single-cell simulation, or genetics-direction claims. |
| No load-bearing invariant was established | deep structure | negative_established | Do not target a claimed invariant without new evidence. |
| PTGER4 is not a clean MS-UC transfer target | shared genetics target transfer | negative_established | Do not pursue naive PTGER4 agonist/antagonist transfer without signal-specific direction data. |
| MHC/HLA overlap is not simple shared causal biology | shared genetics interpretation | negative_established | Do not infer shared causal variant from HLA overlap alone. |
| EBV/IFN APC imprint is not EBV-specific in current data | infectious-trigger exploratory biology | negative_established | Do not revive without EBV-stratified B-cell/APC data beyond random-module controls. |
| Complement/lipid progressive axis is not supported as a combined axis | progressive/lesion biology | negative_established | Do not pursue without donor-aware lesion-rim spatial lipid/complement data. |
| NAMPT/eNAMPT is not reactivated as an MS target | target nomination | negative_established | Use NAMPT/HIF/glycolysis as covariate/context, not target nomination. |
| REL/PUS10/USP34 chr2 is not a current shared-locus lead | genetics colocalization | negative_established | Expression/QTL context cannot rescue a failed disease-coloc screen. |
| ZFP36L1 chr14 is not robust enough for lead status | genetics colocalization | data_gated_not_established | Park until robust disease coloc and allele-aligned QTL direction exist. |

### Non-Replication / Expected-Association Failure List

| exclusion | scope | strength | interpretation_type | decision_value |
| --- | --- | --- | --- | --- |
| Baseline IFN/APC is not a valid general fallback stratifier | cross-disease treatment response | negative_established | grounded_negative_or_discrepancy | Do not substitute baseline IFN/APC for early on-treatment delta. |
| V22 scalar is not a broad cross-therapy response rule | MS/autoimmune treatment response | negative_established | data_gated_or_power_limited | Do not transfer the rule to fingolimod, adalimumab, or arbitrary DMTs without direct validation. |
| Coupled/dynamic/flexible ML variants do not improve over the scalar | treatment-response modeling | negative_established | grounded_negative_or_discrepancy | Do not lock a successor rule from held data. |
| A broad immune-state simulator is not validated from current data | in-silico modeling | negative_established | grounded_negative_or_discrepancy | Do not use the simulator for patient response, single-cell simulation, or genetics-direction claims. |
| PTGER4 is not a clean MS-UC transfer target | shared genetics target transfer | negative_established | data_gated_or_power_limited | Do not pursue naive PTGER4 agonist/antagonist transfer without signal-specific direction data. |
| MHC/HLA overlap is not simple shared causal biology | shared genetics interpretation | negative_established | grounded_negative_or_discrepancy | Do not infer shared causal variant from HLA overlap alone. |
| EBV/IFN APC imprint is not EBV-specific in current data | infectious-trigger exploratory biology | negative_established | data_gated_or_power_limited | Do not revive without EBV-stratified B-cell/APC data beyond random-module controls. |
| Complement/lipid progressive axis is not supported as a combined axis | progressive/lesion biology | negative_established | data_gated_or_power_limited | Do not pursue without donor-aware lesion-rim spatial lipid/complement data. |
| REL/PUS10/USP34 chr2 is not a current shared-locus lead | genetics colocalization | negative_established | grounded_negative_or_discrepancy | Expression/QTL context cannot rescue a failed disease-coloc screen. |

## Workstream 3: Cross-Domain Reframing

Status: **completed first grounded anomaly/control-system probe**.

Question: do responders form a more compact treated immune-tone attractor than
nonresponders in the bounded V22/V23 cohorts?

Grounding artifacts:

- Script: `scripts/v39_immune_tone_anomaly_reframing.py`
- Input: `analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv`
- Output table:
  `analysis/v39_immune_tone_anomaly/immune_tone_anomaly_spaces.tsv`
- Summary:
  `analysis/v39_immune_tone_anomaly/immune_tone_anomaly_summary.json`

Method:

Eight pre-defined baseline, delta, treated, broad-tone, and composition spaces
were z-scored and tested with exact label permutations preserving the `10/9`
responder/nonresponder split (`92,378` label assignments per space). The primary
cross-domain metric was responder within-class compactness versus
nonresponder within-class compactness; group-separation margin was also tested.
Bonferroni and BH correction were applied across the eight spaces.

Result:

| space | timing | responder_compactness_delta | exact_p_responder_more_compact | compactness_bonferroni_p | compactness_bh_q | separation_margin | exact_p_greater_group_separation | separation_bh_q |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| treated_broad_tone | treated | -1.4787975878552415 | 0.002673767847671 | 0.021390142781368 | 0.0119940679158683 | 0.0663386946295139 | 0.2496130072852055 | 0.6656346860938814 |
| delta_broad_tone | delta | -2.1535725477410903 | 0.002998516978967 | 0.0239881358317366 | 0.0119940679158683 | -0.0012285660260307 | 0.4026347979519155 | 0.805269595903831 |
| treated_composition | treated | -1.041125362365042 | 0.0130549150781021 | 0.1044393206248173 | 0.025443011939943 | 0.1278536526797959 | 0.1449247123263945 | 0.6551272475346128 |
| treated_core | treated | -1.5005192845377546 | 0.0135961636302622 | 0.1087693090420983 | 0.025443011939943 | 0.0887496876860867 | 0.1637818118836532 | 0.6551272475346128 |
| delta_core | delta | -1.5095279886010755 | 0.0159018824624644 | 0.1272150596997153 | 0.025443011939943 | -0.1284550299982965 | 0.7616016627155522 | 0.9381569404301844 |
| baseline_core | baseline | -0.888863603525829 | 0.190454540534104 | 1.0 | 0.2539393873788054 | -0.3932443017321323 | 0.8583877288128254 | 0.9381569404301844 |
| delta_composition | delta | -0.4175603721971166 | 0.2551986923434979 | 1.0 | 0.2916556483925691 | -0.0619293982976487 | 0.7492828456683879 | 0.9381569404301844 |
| baseline_composition | baseline | 0.6203971950939242 | 0.8524015198259345 | 1.0 | 0.8524015198259345 | -0.2381457647182507 | 0.9381569404301844 | 0.9381569404301844 |

Verdict:

The anomaly/control-system reframing is **supported only as exploratory
mechanistic framing**, not as a new rule. Responders are significantly more
compact in treated broad-tone space (`p=0.002674`, Bonferroni `0.02139`, BH
`0.01199`) and delta broad-tone space (`p=0.002999`, Bonferroni `0.02399`, BH
`0.01199`). However, group separation margins do not survive (`best separation
BH q=0.655`), so the result is better read as **responder convergence toward a
compact immune-tone treated state**, not as a deployable classifier or
replacement for the locked V22 scalar.

Medical-team implication: if Gafson/DMF arrives, measure treated/delta
broad-tone compactness as a secondary audit endpoint, but do not tune or replace
the locked scalar with it.


## Bottom Line

The project failures do contain structure, but not a simple one-line biological
law. The strongest supported structure is **axis/context dependence**. The
most important operational prefilter remains **direction/modality fit** for
target-like leads, even though its enrichment is suggestive rather than
formally significant in this 20-item frame. The cross-domain immune-tone probe
adds one exploratory but null-tested framing: responders converge into a compact
treated/delta broad-tone state, while group separation remains insufficient for
a classifier. The exclusion ledger gives the medical team a concrete list of
things not to spend on unless a new dataset directly overrides the named
blocker.
