# V36 Generated Hypothesis Grounding

Model proposals consolidated: `16` (`8` Claude, `8` Gemini).

Grounded executable subset:

## tofa_treg_glycolytic_brake

- Source models: claude.
- Grounded result: **inconclusive_partial_context_only**.
- Test: GSE253006 exact all-cell V32 metabolic confounder scores; Treg-specific glycolysis is not available in held exact compartment matrix.
- Key numbers: `{"delta_glycolysis_auc_oriented": 0.95, "delta_glycolysis_exact_perm_p": 0.031746031746031744, "locked_signed_score_auc_oriented": 0.95, "locked_signed_score_exact_perm_p": 0.031746031746031744}`
- Interpretation: All-cell glycolysis delta can be scored, but it is not a Treg- or T-cell-specific brake test. The exact compartment matrix only carries the locked module genes, not glycolysis genes. The hypothesis remains a plausible mechanism proposal, not a grounded finding.
- Next test: Treg/effector-T sorted or single-cell paired treatment data with glycolysis genes and response labels.

## sterol_setpoint_lysosomal_coupling, pvm_lysosomal_blockade

- Source models: claude, gemini, rpt.
- Grounded result: **not_supported_as_coupled_bottleneck_with_current_data**.
- Test: Compare MS lesion-edge sterol/lysosomal cholesterol modules with V35 Mixscale lysosomal APC perturbation coupling.
- Key numbers: `{"lesion_edge_cholesterol_synthesis_hedges_g": 0.2686208742241309, "lesion_edge_cholesterol_synthesis_p": 4.962001971791353e-18, "lesion_edge_lysosomal_cholesterol_hedges_g": 0.0519834700966836, "lesion_edge_lysosomal_cholesterol_p": 0.4028382732728299, "mixscale_top_lysosomal_pair": "gilt_lysosomal_apc_vs_ifn_apc", "mixscale_top_perm_p": 9.999000099990002e-05, "mixscale_top_spearman_r": 0.9017391304347826}`
- Interpretation: The perturbation data strongly couples GILT/lysosomal APC to IFN/APC, and lesion-edge immune cells show cholesterol-synthesis context, but the lesion-edge lysosomal-cholesterol module itself is weak and non-significant. Current data do not support a unified sterol-lysosomal bottleneck.
- Next test: APC- or perivascular-macrophage-resolved lipid/lysosomal flux or HLA-peptidomics in MS lesions.

Non-grounded proposals remain proposals only. They are queued only if a
concrete held-data test can be specified without reading quarantined data.
