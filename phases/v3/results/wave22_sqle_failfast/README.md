# Wave22 SQLE Fail-Fast

Decision: `NO_GO_SQLE_FAILFAST`.

Failed gates: `local_gate_pass;ms_anchor_pass;cross_disease_residual_specificity_pass;foundation_plus_real_gate_pass;real_perturbation_alignment_pass;l1000_disease_signature_reversal_pass;novel_autoimmune_delta_pass`.

Key observations:

- Broad local expression: SQLE is positive in 4 diseases, but the strict core-covariate residual signal survives in only 2 diseases: ibd_crohn_stromal:Crohn disease;ibd_uc_stromal:ulcerative colitis.
- MS anchor: `ms_wm_delta_log2=-0.3408177110309154`, `ms_wm_p=0.3307572199460259`.
- Foundation/perturbation: Geneformer triage is positive enough to inspect, but real perturbation alignment is `model_contradicted_by_gse162463_screen` with GSE162463 MHC-II direction `mhcii_low_enrichment_contradictory`.
- LINCS: 5 known SQLE-inhibitor names are present in compound metadata, but 0 SQLE-like rows appear in the existing disease-signature reversal outputs.
- Prior art/modality: Wave21 hostile review recommendation is `Only revisit if independent non-IBD residual and perturbation evidence show safe local suppression.` / `CONDITIONAL_NO`.

Interpretation: SQLE is a useful stress-test comparator for the residual/druggability pipeline, not a V3 therapeutic nomination.
