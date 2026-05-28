# Wave120 EPHX2/sEH Target-PD Coherence Closure

## Bottom Line

Branch call: `NO_REOPEN_EPHX2_TARGET_PD_COHERENCE`.

EPHX2/sEH remains biologically and pharmacologically interesting, but this V3
route cannot be promoted because the available local evidence does not connect
target-level EPHX2, paired epoxy-fatty-acid/diol pharmacodynamics,
cross-disease specificity, and treatment-response behavior in one coherent
chain.

## Strict Gates

| gate | pass | observed | required |
| --- | --- | --- | --- |
| direct_target_pd_ratio_available | False | direct_epoxide_diol_pairs=0; direct_ratio_supportive_tests=0 | same-study paired epoxide/diol ratio support |
| target_level_ephx2_support | False | 0 | expression/genetics/target-resolution support for EPHX2 itself |
| specificity_vs_generic_lipid_inflammation | False | 0 | EPHX2 axis beats generic lipid, inflammatory, and lysosomal APC comparators |
| independent_response_replication | False | 0 | treatment response or perturbation evidence in an independent dataset |
| cross_disease_specific_biochemistry | False | 1 | specific EPHX2 substrate/product class recurrence across diseases |
| prior_art_unblocked | False | BLOCKED_BY_PRIOR_ART | no blocking broad autoimmune/MS/IBD sEH prior art for the same use |

## Evidence Inventory

| source | rows | supportive_rows | path |
| --- | --- | --- | --- |
| direct_ratio_decision | 1 |  | results_v3/wave74_ephx2_direct_ratio_audit/ephx2_direct_ratio_decision.tsv |
| final_decision | 1 |  | results_v3/wave74_ephx2_oxylipin_specificity/final_decision.tsv |
| gene_evidence | 10 | 0 | results_v3/wave74_ephx2_oxylipin_specificity/ephx2_gene_evidence.tsv |
| module_specificity_margins | 23 |  | results_v3/wave74_ephx2_oxylipin_specificity/module_specificity_margins.tsv |
| metabolite_cross_disease_stats | 7 |  | results_v3/wave74_ephx2_oxylipin_specificity/metabolite_cross_disease_stats.tsv |

## Interpretation

This is a closure audit, not a claim that sEH biology is irrelevant to
autoimmunity. The rejected claim is narrower: the current V3 evidence is
insufficient for an EPHX2/sEH target nomination in the shared
lipid-lysosomal myeloid module, and prior art blocks broad autoimmune
repurposing without a new stratified or mechanistically distinct angle.

## Reproducibility

- Script: `scripts/v3_wave120_ephx2_target_pd_coherence_closure.py`
- Output: `results_v3/wave120_ephx2_target_pd_coherence_closure/ephx2_target_pd_gates.tsv`
- Seed: `20260527`
