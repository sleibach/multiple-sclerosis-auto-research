# V44 Self-Audit Weak-Leg Analysis

Date: 2026-06-12

## Scope

This analysis resolves the V43 self-audit tension: the APC/HLA/IFN monitoring signal looked strong by recurrence but only borderline by the V41 joint-inference gate.

This is method-characterization, not discovery. It does not change the locked V22 rule, the V42 preregistration, or any biological claim. It asks which existing evidence formulation is most defensible before external validation.

## Inputs

- V41 integrated evidence matrix: `analysis/v41_joint_inference/entity_modality_evidence_matrix.tsv`
- V41 joint inference results: `analysis/v41_joint_inference/joint_inference_entity_results.tsv`
- V41 recurrence meta-results: `analysis/v41_joint_inference/recurring_signal_meta_results.tsv`
- V41 train/held-out modality split: `analysis/v41_joint_inference/heldout_modality_split.json`
- V43 synthetic-null calibration values summarized in `docs/history/PIPELINE_SELF_AUDIT_V43.md`

Reproducible script and outputs:

- `scripts/v44_self_audit_weak_leg.py`
- `analysis/v44_self_audit_weak_leg/summary.json`
- `analysis/v44_self_audit_weak_leg/apc_hla_ifn_modality_contributions.tsv`
- `analysis/v44_self_audit_weak_leg/train_modality_top_z_entities.tsv`
- `analysis/v44_self_audit_weak_leg/joint_vs_recurrence_top_entities.tsv`

## Headline

The joint-gate result is borderline because the family-wise max-z null envelope is high, not because the APC/HLA/IFN signal is carried by a single fragile modality.

The recurrence result is the stronger formulation of the central claim: the APC/HLA/IFN monitoring entity has 78 positive source units versus a recurrence-null 95th-percentile max of 12, giving a 6.5x margin and empirical FWER `0.0001`.

## Quantitative Results

| Quantity | Value | Interpretation |
|---|---:|---|
| APC/HLA/IFN train joint z | `8.0548` | Strong absolute joint score |
| Joint-gate empirical FWER | `0.0684` | Borderline against family-wise max-z null |
| V41/V43 joint-null 95th percentile | `8.1547` | Null maximum is high enough to overlap the target |
| Joint z / null p95 | `0.9878` | Target sits just below the conservative null envelope |
| Positive source units | `78` | Broad repeated evidence across source units |
| Recurrence-null max p95 | `12` | Recurrence null rarely creates many repeated hits |
| Recurrence / null p95 | `6.5` | Large recurrence margin |
| Recurrence FWER | `0.0001` | Robust under the source-unit recurrence null |
| Training modalities with APC/HLA/IFN support | `8` | Broad but moderate support |
| Smallest leave-one joint z | `6.5359` | No single positive modality fully explains the signal |
| Largest leave-one delta | `0.6686` | Each top modality contributes, none dominates |

## Why The Joint Gate Is Borderline

The joint gate uses a family-wise maximum over many entities and modalities. In the V41 matrix, one single-modality genetics entity, `genetic_backdrop_ms_uc`, has support z `7.5352`. That extreme value raises the max-z null envelope. Against that conservative family-wise threshold, the APC/HLA/IFN joint z of `8.0548` is close but not cleanly beyond the null 95th percentile (`8.1547`).

This means the joint gate is doing what it was designed to do: it is conservative under a large search space. It should not be treated as a failure of the APC/HLA/IFN signal, but it should also not be presented as discovery-grade by itself.

## Modality Contribution Check

The APC/HLA/IFN signal is not a single-modality artifact. Removing the strongest positive modalities leaves the joint z above `6.5`.

| Modality | Support z | Leave-one joint z | Delta if removed |
|---|---:|---:|---:|
| perturbation | `3.1748` | `6.5359` | `0.6686` |
| perturbation_mixscale | `3.1748` | `6.5359` | `0.6686` |
| treatment_pharmacodynamic | `3.0904` | `6.5641` | `0.6404` |
| treatment_response_tests | `3.0235` | `6.5863` | `0.6181` |
| cell_state_h5ad | `2.6970` | `6.6952` | `0.5093` |
| exploratory | `2.6548` | `6.7093` | `0.4952` |
| deep_structure | `2.5760` | `6.7355` | `0.4690` |
| cross_disease_summary | `2.3912` | `6.7971` | `0.4074` |

Two modalities add no positive support in this formulation (`failure_structure`, `network_topology`). Removing either increases the joint z to `7.5942`, showing they dilute the Stouffer score rather than drive it.

## Verdict

Supported method conclusion:

1. The recurrence/cross-evidence formulation is the most defensible internal evidence for the APC/HLA-II/IFN monitoring lead.
2. The joint-z formulation is supportive but should be presented as conservative and borderline, not as the lead evidence.
3. The borderline joint FWER reflects a high family-wise max-z null from the broad search space and extreme single-modality signals, not collapse of the APC/HLA/IFN signal under leave-one-modality stress.
4. External validation remains required. This analysis strengthens the internal framing; it does not validate the clinical biomarker.

## Medical-Team Implication

Lead with the recurrence/convergence statement: the APC/HLA-II/IFN monitoring axis recurs across many independent project source units far beyond the synthetic-null recurrence envelope. Treat the V41 joint-inference score as a conservative secondary check. Do not overstate the joint-gate result as a standalone discovery.

