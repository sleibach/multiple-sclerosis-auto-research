# Wave53 Perturbation-First Pivot

Random seed: `20260527`.

## Verdict

- `MED16_MEDIATOR_MODULE`: `WETLAB_ONLY_MED16_SELECTIVE_NONDRUGGABLE_ROUTE`; 2/8 gates passed.
  - Primary blocker: The real Med16_KO signal is strong, but the route lacks a target-specific MS anchor and a safe selective druggable handle; practical Mediator/CDK8/19 modulation risks broad transcriptional or oncology-like toxicity.
  - Decisive reopen test: Perform graded MED16 or Mediator-module perturbation in human primary myeloid cells and MS lesion slice co-culture; require selective MHC-II/lipid-module reduction without loss of viability, housekeeping transcription, phagocytosis, or repair.
- `GSK3B_INHIBITION`: `NO_GO_GSK3B_REAL_PERTURBATION_PRIOR_ART_PLEIOTROPY`; 2/8 gates passed.
  - Primary blocker: Gsk3b_KO has real perturbation support but GSK3B is pleiotropic, prior-art crowded in neuroimmune disease, and locally lacks FDR-supported MS/cross-disease cell-state anchoring.
  - Decisive reopen test: Use isoform-selective, dose-graded GSK3B perturbation in primary human myeloid/MS lesion organoid systems; reopen only if antigen-processing suppression is separable from WNT/metabolic/neurotoxicity and replicates in MS tissue.
- `TNFRSF1A_DAMPING`: `NO_GO_PERTURBATION_FIRST_PIVOT`; 3/8 gates passed.
  - Primary blocker: TNFRSF1A/TNF perturbation is genetically broad but MS direction is unsafe because TNF blockade can worsen demyelinating biology; local MS expression is negative.
  - Decisive reopen test: Only a TNFR1-selective approach that improves MS lesion repair without worsening demyelination in humanized/ex vivo systems would reopen; broad anti-TNF-like effects remain no-go.
- `RFX5_MHCII_PARTIAL_SUPPRESSION`: `NO_GO_PERTURBATION_FIRST_PIVOT`; 2/8 gates passed.
  - Primary blocker: RFX5 is a direct antigen-presentation transcriptional node, but the whole HLA-II axis is already closed for host-defense and nonselective antigen-presentation suppression risk.
  - Decisive reopen test: Reopen only if tunable RFX5 modulation selectively reduces pathogenic antigen presentation while preserving antimicrobial MHC-II response in primary APCs.
- `CHUK_IKK_MODULATION`: `NO_GO_PERTURBATION_FIRST_PIVOT`; 2/8 gates passed.
  - Primary blocker: CHUK/IKK-alpha is weakly perturbation-positive but broad NF-kB biology lacks selectivity and novelty.
  - Decisive reopen test: Reopen only if a selective CHUK-biased intervention suppresses the disease module without broad NF-kB/host-defense loss across primary immune assays.

## Gate Matrix

- `MED16_MEDIATOR_MODULE` / `real_perturbation_selectivity`: PASS (`suppression=3.139501453617054; selectivity=2.3051173986620066; target_vs_ifn=2.3416465218333142`) - requires real perturbation that suppresses target readout more than generic IFN/stress.
- `MED16_MEDIATOR_MODULE` / `foundation_or_model_support`: FAIL (`rows=0; recommendations=`) - requires foundation/model support that is not explicitly do-not-promote.
- `MED16_MEDIATOR_MODULE` / `cross_disease_cell_state_support`: FAIL (`positive=4.0; negative=2.0; diseases=Crohn disease;psoriasis;type 1 diabetes mellitus;ulcerative colitis`) - requires signal in at least three diseases without contradiction.
- `MED16_MEDIATOR_MODULE` / `strict_ms_anchor`: FAIL (`delta=0.2872210471681988; p=0.1694354583767501; fdr=0.8989378106274888`) - requires FDR-supported target/intervention-specific MS signal.
- `MED16_MEDIATOR_MODULE` / `genetic_or_response_anchor`: FAIL (`GWAS_traits=1.0; min_p=7e-06; strict_response_claims=0`) - requires genetics or strict treatment-response anchoring.
- `MED16_MEDIATOR_MODULE` / `tractable_druggability`: PASS (`activity_rows=100; best_nM=1.4; clinical_trials=0`) - requires practical chemical/biologic modality.
- `MED16_MEDIATOR_MODULE` / `safe_selective_direction`: FAIL (`high_risk_broad_transcription`) - requires directionality that avoids host-defense, demyelination, and broad transcription toxicity.
- `MED16_MEDIATOR_MODULE` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=37; ClinicalTrials=0`) - requires a non-blocked novelty delta.
- `GSK3B_INHIBITION` / `real_perturbation_selectivity`: PASS (`suppression=1.6223580114004137; selectivity=0.7779563820432978; target_vs_ifn=0.8271572726202511`) - requires real perturbation that suppresses target readout more than generic IFN/stress.
- `GSK3B_INHIBITION` / `foundation_or_model_support`: PASS (`rows=1; recommendations=use_real_perturbation_not_foundation_model`) - requires foundation/model support that is not explicitly do-not-promote.
- `GSK3B_INHIBITION` / `cross_disease_cell_state_support`: FAIL (`positive=1.0; negative=0.0; diseases=Crohn disease`) - requires signal in at least three diseases without contradiction.
- `GSK3B_INHIBITION` / `strict_ms_anchor`: FAIL (`delta=-0.1319846584560178; p=0.4753109636188744; fdr=0.925497453503607`) - requires FDR-supported target/intervention-specific MS signal.
- `GSK3B_INHIBITION` / `genetic_or_response_anchor`: FAIL (`GWAS_traits=0.0; min_p=1.0; strict_response_claims=0`) - requires genetics or strict treatment-response anchoring.
- `GSK3B_INHIBITION` / `tractable_druggability`: FAIL (`activity_rows=4; best_nM=24.35; clinical_trials=0`) - requires practical chemical/biologic modality.
- `GSK3B_INHIBITION` / `safe_selective_direction`: FAIL (`pleiotropic_neuroimmune_metabolic`) - requires directionality that avoids host-defense, demyelination, and broad transcription toxicity.
- `GSK3B_INHIBITION` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=268; ClinicalTrials=0`) - requires a non-blocked novelty delta.
- `TNFRSF1A_DAMPING` / `real_perturbation_selectivity`: PASS (`suppression=0.9683862679530189; selectivity=0.6211601610564657; target_vs_ifn=0.6624135343272808`) - requires real perturbation that suppresses target readout more than generic IFN/stress.
- `TNFRSF1A_DAMPING` / `foundation_or_model_support`: FAIL (`rows=0; recommendations=`) - requires foundation/model support that is not explicitly do-not-promote.
- `TNFRSF1A_DAMPING` / `cross_disease_cell_state_support`: FAIL (`positive=0.0; negative=0.0; diseases=`) - requires signal in at least three diseases without contradiction.
- `TNFRSF1A_DAMPING` / `strict_ms_anchor`: FAIL (`delta=-0.1651855861386195; p=0.3190864538699107; fdr=0.9120391943246274`) - requires FDR-supported target/intervention-specific MS signal.
- `TNFRSF1A_DAMPING` / `genetic_or_response_anchor`: PASS (`GWAS_traits=7.0; min_p=2e-47; strict_response_claims=0`) - requires genetics or strict treatment-response anchoring.
- `TNFRSF1A_DAMPING` / `tractable_druggability`: PASS (`activity_rows=100; best_nM=210.0; clinical_trials=2`) - requires practical chemical/biologic modality.
- `TNFRSF1A_DAMPING` / `safe_selective_direction`: FAIL (`ms_directionally_unsafe`) - requires directionality that avoids host-defense, demyelination, and broad transcription toxicity.
- `TNFRSF1A_DAMPING` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=1068; ClinicalTrials=2`) - requires a non-blocked novelty delta.
- `RFX5_MHCII_PARTIAL_SUPPRESSION` / `real_perturbation_selectivity`: PASS (`suppression=0.5517938735080701; selectivity=0.5231987939104686; target_vs_ifn=0.5517938735080701`) - requires real perturbation that suppresses target readout more than generic IFN/stress.
- `RFX5_MHCII_PARTIAL_SUPPRESSION` / `foundation_or_model_support`: PASS (`rows=1; recommendations=use_real_perturbation_not_foundation_model`) - requires foundation/model support that is not explicitly do-not-promote.
- `RFX5_MHCII_PARTIAL_SUPPRESSION` / `cross_disease_cell_state_support`: FAIL (`positive=1.0; negative=1.0; diseases=type 1 diabetes mellitus`) - requires signal in at least three diseases without contradiction.
- `RFX5_MHCII_PARTIAL_SUPPRESSION` / `strict_ms_anchor`: FAIL (`delta=0.0043302351443461; p=0.9786885809467264; fdr=0.9982687727683835`) - requires FDR-supported target/intervention-specific MS signal.
- `RFX5_MHCII_PARTIAL_SUPPRESSION` / `genetic_or_response_anchor`: FAIL (`GWAS_traits=0.0; min_p=1.0; strict_response_claims=0`) - requires genetics or strict treatment-response anchoring.
- `RFX5_MHCII_PARTIAL_SUPPRESSION` / `tractable_druggability`: FAIL (`activity_rows=0; best_nM=None; clinical_trials=0`) - requires practical chemical/biologic modality.
- `RFX5_MHCII_PARTIAL_SUPPRESSION` / `safe_selective_direction`: FAIL (`antigen_presentation_host_defense`) - requires directionality that avoids host-defense, demyelination, and broad transcription toxicity.
- `RFX5_MHCII_PARTIAL_SUPPRESSION` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=103; ClinicalTrials=0`) - requires a non-blocked novelty delta.
- `CHUK_IKK_MODULATION` / `real_perturbation_selectivity`: PASS (`suppression=0.672021576511123; selectivity=0.3353338408117842; target_vs_ifn=0.402896081494298`) - requires real perturbation that suppresses target readout more than generic IFN/stress.
- `CHUK_IKK_MODULATION` / `foundation_or_model_support`: FAIL (`rows=0; recommendations=`) - requires foundation/model support that is not explicitly do-not-promote.
- `CHUK_IKK_MODULATION` / `cross_disease_cell_state_support`: FAIL (`positive=2.0; negative=0.0; diseases=Crohn disease;psoriasis`) - requires signal in at least three diseases without contradiction.
- `CHUK_IKK_MODULATION` / `strict_ms_anchor`: FAIL (`delta=0.2237878248965508; p=0.3211760938016935; fdr=0.9120391943246274`) - requires FDR-supported target/intervention-specific MS signal.
- `CHUK_IKK_MODULATION` / `genetic_or_response_anchor`: FAIL (`GWAS_traits=2.0; min_p=1e-09; strict_response_claims=0`) - requires genetics or strict treatment-response anchoring.
- `CHUK_IKK_MODULATION` / `tractable_druggability`: PASS (`activity_rows=100; best_nM=25.0; clinical_trials=3`) - requires practical chemical/biologic modality.
- `CHUK_IKK_MODULATION` / `safe_selective_direction`: FAIL (`broad_nfkb_host_defense`) - requires directionality that avoids host-defense, demyelination, and broad transcription toxicity.
- `CHUK_IKK_MODULATION` / `novelty_prior_art_unblocked`: FAIL (`EuropePMC=1082; ClinicalTrials=3`) - requires a non-blocked novelty delta.
