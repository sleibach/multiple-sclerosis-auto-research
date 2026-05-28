# Wave54 MFGE8 Debris-Opsonin Audit

Random seed: `20260527`.

## Verdict

`MFGE8`: `PARK_EX_VIVO_ONLY_MFGE8_DEBRIS_OPSONIN`; 3/8 gates passed.

Primary blocker: MFGE8 has a coherent debris-opsonin/remyelination rationale, but local cross-autoimmune support is thin, MS evidence is nominal not FDR-supported, the efferocytosis CRISPR screen is unresolved, and bystander phagoptosis risk is not controlled.

Decisive reopen test: Test recombinant or engineered-local MFGE8 in human iPSC microglia/macrophage plus myelin-debris cultures with viable neuron and oligodendrocyte bystanders. Require increased myelin-debris uptake and repair-supportive lipid handling, no uptake of viable bystanders, no inflammatory cytokine amplification, and loss of effect with RGD/integrin-binding mutant or integrin blockade.

## Gate Matrix

- `cross_domain_mechanistic_anchor`: PASS (`remyelination_hits=62; autoimmunity_hits=294`) - requires public evidence tying MFGE8 to myelin/debris repair and autoimmunity biology.
- `local_cross_autoimmune_cell_state`: FAIL (`positive=1.0; negative=0.0; diseases=type 1 diabetes mellitus`) - requires local signal in at least three autoimmune diseases.
- `strict_ms_anchor`: FAIL (`delta=0.5586776922734735; p=0.0686336045013876; fdr=0.8989378106274888`) - requires FDR-supported MS lesion signal.
- `efferocytosis_screen_support`: FAIL (`lfc=0.1589236226146265; fdr=1.0; call=UNRESOLVED`) - requires direct screen support for efficient-vs-noneater phagocytosis.
- `tractable_modality`: PASS (`secreted_opsonin=True; chembl_activity_rows=0; trials=5`) - recombinant protein, engineered local delivery, or ex vivo assayable biologic modality is plausible.
- `safety_bystander_phagocytosis_resolved`: FAIL (`phagoptosis_query_hits=39`) - requires evidence that viable-neuron/oligodendrocyte bystander phagocytosis risk is controlled.
- `novelty_prior_art_unblocked`: PASS (`clinical_trial_hits=5; direct_therapeutic_trial=False; direct patents searched separately`) - requires no obvious direct clinical therapeutic crowding; patent search URLs are recorded but not treated as clearance.
- `promotion_grade_package`: FAIL (`local_and_screen_support_weak`) - requires all other major gates plus a disease-relevant perturbation package.
