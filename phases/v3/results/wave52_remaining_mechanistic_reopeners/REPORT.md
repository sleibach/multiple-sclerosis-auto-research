# Wave52 Remaining Mechanistic Reopeners

Random seed: `20260527`.

## Verdict

- `CCR6_TH17_TRAFFICKING`: `NO_GO_CROWDED_TRAFFICKING_NO_COLOC_LOCAL_SUPPORT`; 2/8 critical gates passed.
  - Primary blocker: Broad mapped-gene autoimmune signal is not target-resolved; local disease-cell-state and MS anchors are absent, and CCR6/CCL20/Th17 trafficking is crowded prior art with host-defense risk.
  - Decisive reopen test: Fine-map/colocalize the CCR6 locus with disease-tissue eQTLs and show CCR6 blockade prevents pathogenic Th17 entry in paired human inflamed-tissue organoids without suppressing protective mucosal recruitment.
- `TREM2_APOE_LIPID_REPAIR`: `NO_GO_TREM2_PRIOR_ART_MARKER_CONFOUNDER`; 3/8 critical gates passed.
  - Primary blocker: Route-level lipid repair biology is plausible, but target-specific causality is not established; TREM2 agonism is crowded in neurodegeneration and may mark phagocytic state rather than control it across autoimmune tissues.
  - Decisive reopen test: Use MS lesion slice or iPSC-microglia/oligodendrocyte debris co-culture with a selective TREM2 agonist and TREM2 loss control; require increased myelin-debris clearance plus preserved remyelination and reduced inflammatory lipid loading.
- `SQLE_STEROL_STROMAL`: `NO_GO_SQLE_FAILFAST_RECONFIRMED`; 2/8 critical gates passed.
  - Primary blocker: The previous SQLE fail-fast stands: cross-disease signal is mostly stromal/IBD-skewed, MS anchor is negative, foundation-model support is contradicted by real perturbation, and no novel autoimmune-use delta survives.
  - Decisive reopen test: Run selective SQLE perturbation in independent non-IBD autoimmune stromal/myeloid tissue and MS lesion models; reopen only if disease modules reverse and repair/barrier readouts are preserved.
- `LOCALIZED_IL10_RESTORATION`: `NO_GO_IL10_PRIOR_ART_SYSTEMIC_CYTOKINE_DELIVERY`; 2/8 critical gates passed.
  - Primary blocker: IL-10 restoration is biologically credible but not novel; systemic cytokine delivery has extensive prior art and local V3 artifacts do not define a compartment-specific subgroup or modality that solves selectivity.
  - Decisive reopen test: Engineer lesion/tissue-local IL-10 delivery and test in ex vivo autoimmune tissue explants; require local STAT3/Treg-like resolution without systemic immunosuppression or fibrotic/barrier impairment.

## Gate Matrix

- `CCR6_TH17_TRAFFICKING` / `cross_autoimmune_breadth`: PASS (`OT=0.0; support_union=0.0; local_pos=0.0; GWAS_traits=15.0; min_p=4e-47`) - requires evidence spanning at least five autoimmune diseases or strong genome-wide autoimmune breadth.
- `CCR6_TH17_TRAFFICKING` / `cross_dataset_cell_state_replication`: FAIL (`local_pos=0.0; local_neg=0.0; retained=0.0; support_union=0.0`) - requires repeated disease-state signal beyond one tissue or one disease.
- `CCR6_TH17_TRAFFICKING` / `target_specific_ms_anchor`: FAIL (`delta=0.2229856175356008; p=0.7784945025694487; fdr=0.9741955192514664; route_ms_anchor=False`) - requires target/intervention-specific MS support, not just route-level plausibility.
- `CCR6_TH17_TRAFFICKING` / `target_resolved_genetics_or_coloc`: FAIL (`absent in local V3 artifacts`) - mapped-gene or pathway genetics is insufficient for therapeutic promotion.
- `CCR6_TH17_TRAFFICKING` / `foundation_plus_real_perturbation_alignment`: FAIL (`foundation_contexts=0.0; strong=0.0; real_pass=False; contradicted=False; l1000=False`) - requires foundation-model prediction aligned with real disease-relevant perturbation.
- `CCR6_TH17_TRAFFICKING` / `tractable_intervention_point`: PASS (`chemical_matter=True; activity_rows=100; best_nM=594.0`) - requires at least a plausible biologic or small-molecule intervention point.
- `CCR6_TH17_TRAFFICKING` / `safe_selective_direction_resolved`: FAIL (`block CCR6/CCL20-dependent pathogenic Th17 tissue entry`) - requires a direction that is selective and unlikely to impair repair, barrier, or host defense.
- `CCR6_TH17_TRAFFICKING` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=895; ClinicalTrials=5; prior_block=True`) - requires a non-blocked novelty delta across the autoimmune cluster.
- `TREM2_APOE_LIPID_REPAIR` / `cross_autoimmune_breadth`: PASS (`OT=0.0; support_union=13.0; local_pos=4.0; GWAS_traits=2.0; min_p=7e-08`) - requires evidence spanning at least five autoimmune diseases or strong genome-wide autoimmune breadth.
- `TREM2_APOE_LIPID_REPAIR` / `cross_dataset_cell_state_replication`: PASS (`local_pos=4.0; local_neg=3.0; retained=1.0; support_union=13.0`) - requires repeated disease-state signal beyond one tissue or one disease.
- `TREM2_APOE_LIPID_REPAIR` / `target_specific_ms_anchor`: FAIL (`delta=1.7595984466157422; p=0.0006219963760009; fdr=0.7144250374746858; route_ms_anchor=True`) - requires target/intervention-specific MS support, not just route-level plausibility.
- `TREM2_APOE_LIPID_REPAIR` / `target_resolved_genetics_or_coloc`: FAIL (`absent in local V3 artifacts`) - mapped-gene or pathway genetics is insufficient for therapeutic promotion.
- `TREM2_APOE_LIPID_REPAIR` / `foundation_plus_real_perturbation_alignment`: FAIL (`foundation_contexts=0.0; strong=0.0; real_pass=False; contradicted=False; l1000=False`) - requires foundation-model prediction aligned with real disease-relevant perturbation.
- `TREM2_APOE_LIPID_REPAIR` / `tractable_intervention_point`: PASS (`chemical_matter=True; activity_rows=76; best_nM=0.7`) - requires at least a plausible biologic or small-molecule intervention point.
- `TREM2_APOE_LIPID_REPAIR` / `safe_selective_direction_resolved`: FAIL (`enhance lesion-local phagolysosomal lipid/debris repair without chronic inflammatory lipid loading`) - requires a direction that is selective and unlikely to impair repair, barrier, or host defense.
- `TREM2_APOE_LIPID_REPAIR` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=272; ClinicalTrials=2; prior_block=True`) - requires a non-blocked novelty delta across the autoimmune cluster.
- `SQLE_STEROL_STROMAL` / `cross_autoimmune_breadth`: FAIL (`OT=0.0; support_union=0.0; local_pos=4.0; GWAS_traits=0.0; min_p=1.0`) - requires evidence spanning at least five autoimmune diseases or strong genome-wide autoimmune breadth.
- `SQLE_STEROL_STROMAL` / `cross_dataset_cell_state_replication`: PASS (`local_pos=4.0; local_neg=0.0; retained=3.0; support_union=0.0`) - requires repeated disease-state signal beyond one tissue or one disease.
- `SQLE_STEROL_STROMAL` / `target_specific_ms_anchor`: FAIL (`delta=-0.3408177110309154; p=0.3307572199460259; fdr=0.9141270983319502; route_ms_anchor=False`) - requires target/intervention-specific MS support, not just route-level plausibility.
- `SQLE_STEROL_STROMAL` / `target_resolved_genetics_or_coloc`: FAIL (`absent in local V3 artifacts`) - mapped-gene or pathway genetics is insufficient for therapeutic promotion.
- `SQLE_STEROL_STROMAL` / `foundation_plus_real_perturbation_alignment`: FAIL (`foundation_contexts=3.0; strong=1.0; real_pass=False; contradicted=True; l1000=False`) - requires foundation-model prediction aligned with real disease-relevant perturbation.
- `SQLE_STEROL_STROMAL` / `tractable_intervention_point`: PASS (`chemical_matter=True; activity_rows=88; best_nM=20.0`) - requires at least a plausible biologic or small-molecule intervention point.
- `SQLE_STEROL_STROMAL` / `safe_selective_direction_resolved`: FAIL (`reduce pathological sterol/stromal stress state while preserving repair`) - requires a direction that is selective and unlikely to impair repair, barrier, or host defense.
- `SQLE_STEROL_STROMAL` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=61; ClinicalTrials=0; prior_block=True`) - requires a non-blocked novelty delta across the autoimmune cluster.
- `LOCALIZED_IL10_RESTORATION` / `cross_autoimmune_breadth`: PASS (`OT=7.0; support_union=2.0; local_pos=1.0; GWAS_traits=14.0; min_p=5e-55`) - requires evidence spanning at least five autoimmune diseases or strong genome-wide autoimmune breadth.
- `LOCALIZED_IL10_RESTORATION` / `cross_dataset_cell_state_replication`: FAIL (`local_pos=1.0; local_neg=1.0; retained=0.0; support_union=2.0`) - requires repeated disease-state signal beyond one tissue or one disease.
- `LOCALIZED_IL10_RESTORATION` / `target_specific_ms_anchor`: FAIL (`delta=0.5386340709389863; p=0.0920894843746553; fdr=0.8989378106274888; route_ms_anchor=True`) - requires target/intervention-specific MS support, not just route-level plausibility.
- `LOCALIZED_IL10_RESTORATION` / `target_resolved_genetics_or_coloc`: FAIL (`absent in local V3 artifacts`) - mapped-gene or pathway genetics is insufficient for therapeutic promotion.
- `LOCALIZED_IL10_RESTORATION` / `foundation_plus_real_perturbation_alignment`: FAIL (`foundation_contexts=0.0; strong=0.0; real_pass=False; contradicted=False; l1000=False`) - requires foundation-model prediction aligned with real disease-relevant perturbation.
- `LOCALIZED_IL10_RESTORATION` / `tractable_intervention_point`: PASS (`chemical_matter=False; activity_rows=0; best_nM=None`) - requires at least a plausible biologic or small-molecule intervention point.
- `LOCALIZED_IL10_RESTORATION` / `safe_selective_direction_resolved`: FAIL (`restore anti-inflammatory IL-10 signaling only in the disease compartment`) - requires a direction that is selective and unlikely to impair repair, barrier, or host defense.
- `LOCALIZED_IL10_RESTORATION` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=6240; ClinicalTrials=5; prior_block=True`) - requires a non-blocked novelty delta across the autoimmune cluster.
