# V53 MIF/CD74 Grounded Re-Audit

Status: completed targeted re-examination on committed held-data outputs. This is not a new public-data discovery run.

## Verdict

**Not supported as a therapeutic target; retain only as a tone-loaded APC state readout.**

The mature audit confirms the earlier Tier-1 demotion. Project data support recurring CD74/HLA-II receptor-state coupling, but not MIF ligand causality, receptor-specific adjusted response, or a stable intervention direction.

## Evidence Ledger

| evidence_layer | test | effect | p | q_or_fdr | outcome | interpretation | source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MS_cross_sectional_microglia | mif_cd74_receptor_state | 0.6141257454613055 | 0.005473419155014 | 0.0191569670425492 | supported_state_association | observational state association; not causal or directional target evidence | phases/v3/results/cross_disease_cell_state_convergence.tsv |
| MS_cross_sectional_microglia | mif_ligand_axis | 0.2855714681357631 | 0.3368490652013122 | 0.4679881110726095 | not_supported | observational state association; not causal or directional target evidence | phases/v3/results/cross_disease_cell_state_convergence.tsv |
| cross_disease_IFN_residualization | all receptor-state residual tests | 0.0 |  | 0.4417003015587293 | not_supported | zero tests survived FDR<=0.10 | analysis/tier_0_triage/mif_cd74_stratification/residual_evidence.tsv |
| MS_lesion_component_residualization | immune CD74 after APC/size adjustment | 0.0 | 0.175586890848046 | 0.7419955642189386 | not_supported | no immune CD74 contrast survived multiplicity correction | analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk/component_residual_tests.tsv |
| component_resolved_treatment_response | receptor/CD74/full-state after IFN/APC adjustment | 0.0 | 0.0391412193993875 | 0.8997148480903072 | not_supported | zero adjusted receptor-specific tests survived FDR<=0.10 | analysis/tier_1_mechanism/mif_cd74_gse282122_component_response/component_remission_interaction.tsv |
| cross_modality_module_dependency | supported V26 dependencies involving receptor-state module | 9.0 | 0.0004997501249375 | 0.0014992503748125 | supported_coupling | module coupling is supported, but does not establish ligand causality or intervention direction | analysis/v26_deep_structure/workstream_b_module_dependencies.tsv |
| global_tone_loading | receptor-state module vs row-wise module mean | 5.0 | 0.0001999600079984 | 0.0232388304947706 | supported_confounding_context | tone association survives in 5/5 modalities | analysis/v38_coupled_architecture_inversion/module_global_tone_tests.tsv |
| therapy_direction_recurrence | collapsed delta_RECEPTOR sign consistency | 1.0 | 1.0 |  | not_supported | 1 positive, 1 negative, and 1 near-null therapy-cohort directions | analysis/v36_receptor_coupling_followup/receptor_recurrence_tests.tsv |
| module_definition_provenance | literal module definitions containing MIF | 3.0 |  |  | inconsistent_coverage | MIF present in 3/9 recovered literal definitions | committed analysis scripts listed in module_definition_audit.tsv |

## Module-Definition Audit

| source | definition_found | genes | n_genes | contains_MIF | contains_CD74 | contains_HLAII |
| --- | --- | --- | --- | --- | --- | --- |
| scripts/v3_analyze_direct_h5ad_cell_states.py | True | CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1 | 7 | False | True | True |
| scripts/v3_analyze_mixscale_perturbseq.py | True | CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1 | 7 | False | True | True |
| scripts/v3_analyze_gse253006_tofacitinib_uc.py | True | CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1 | 7 | False | True | True |
| scripts/v3_analyze_cellxgene_cross_autoimmune.py | True | CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1 | 7 | False | True | True |
| scripts/analyze_gse17410_ms_pregnancy_modules.py | True | CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1 | 7 | False | True | True |
| scripts/analyze_emt12260_ms_tcells.py | True | MIF;CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1 | 6 | True | True | True |
| scripts/analyze_gse108497_sle_pregnancy.py | True | MIF;CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1 | 6 | True | True | True |
| scripts/v10_sjogren_gse23117_bulk_replication.py | True | MIF;CD74;CD44;CXCR4;HLA-DRA;HLA-DPA1 | 6 | True | True | True |
| scripts/v3_analyze_gse111972_microglia.py | True | CD74;CD44;CXCR4;HLA-DRA;HLA-DRB1;HLA-DPA1;HLA-DPB1 | 7 | False | True | True |

The label `mif_cd74_receptor_state` is not a consistent MIF measurement. Several central V26/V36 source definitions omit `MIF` and combine CD74/CD44/CXCR4 with HLA-II genes.

## Therapy-Direction Null

| cohort_family | n_rows_collapsed | median_hedges_g | median_auc | direction |
| --- | --- | --- | --- | --- |
| GSE85034_MTX | 1 | -1.0918551066536035 | 0.1 | negative |
| GSE85034_ADA | 1 | 0.0719447565184434 | 0.5555555555555556 | near_null |
| GSE253006_TOF | 6 | 1.0515393143197533 | 0.775 | positive |

Collapsed therapy-cohort directions are 1 positive, 1 negative, and 1 near-null using |Hedges g| >= 0.2; exact majority-sign p = 1, empirical p = 1 (20000 seeded null draws).

## What Survives

- Supported: recurrent APC receptor-state coupling and observational MS microglial state association.
- Not supported: MIF-specific causality, receptor-specific adjusted treatment response, same-direction transfer across therapies, or target promotion.
- Needs data: an MS treatment or lesion dataset measuring MIF, CD74, CD44, CXCR4, HLA-II, cell composition, and clinical outcome together, followed by a pre-specified component-resolved test.

## Therapeutic Boundary

Structure may establish that MIF or CD74 is physically tractable, but cannot repair the missing causal and directional evidence. Any structure-first follow-up remains prediction-informed context and cannot reopen this target as a finding.
