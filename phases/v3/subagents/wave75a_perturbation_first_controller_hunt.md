# Wave75-A Perturbation-First Controller Hunt

Timestamp: 2026-05-27 17:25 CEST

## Executive Call

No finding is claimed.

The local artifacts still support one hard statement: the recurrent IFN/APC plus lysosomal/APC myeloid state is perturbable, but most apparent intervention points collapse into broad IFN/JAK/TNF/NF-kB/Fc/host-defense biology, model-only support, expression recurrence, or prior-art/translation blockers.

Best bounded Wave75/76 tests are:

1. Use `MED16`/Mediator perturbation as a positive-control selectivity anchor, not as a therapeutic target.
2. Run a narrow LILRB-family directionality/response audit, led by `LILRB2`, `LILRB1`, and `LILRB4`, because they have cell-resolved anti-TNF remission-response signals and some model direction hints, but no direct target perturbation.
3. Optionally test `CD300A`/`INPP5D` only as efferocytosis-negative-regulator scouts, not as disease candidates.

Everything else below should remain closed unless a new target-specific perturbation dataset appears.

## Files Inspected

- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/REPORT.md`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/candidate_gene_screen_scores.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave38_crispr_state_druggability_rescue/summary.json`
- `results_v3/wave38_crispr_state_druggability_rescue/crispr_state_druggability_rescue_rank.tsv`
- `results_v3/wave41_l1000_external_unknown_deconvolution/REPORT.md`
- `results_v3/wave41_l1000_external_unknown_deconvolution/external_unknown_deconvolution.tsv`
- `results_v3/wave53_perturbation_first_pivot/REPORT.md`
- `results_v3/wave53_perturbation_first_pivot/decision_matrix.tsv`
- `results_v3/wave53_perturbation_first_pivot/perturbation_first_audit.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/REPORT.md`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/REPORT.md`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/wave65_gate_summary.tsv`
- `results_v3/wave67_gse282122_myeloid_pseudobulk/REPORT.md`
- `results_v3/wave67_gse282122_myeloid_pseudobulk/wave67_gate_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/REPORT.md`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave69d_gse282122_geneformer_remission_centroid/REPORT.md`
- `results_v3/wave69d_gse282122_geneformer_remission_candidate_calls.tsv`
- `results_v3/wave70_fc_ros_resolution_matrix/REPORT.md`
- `results_v3/wave70_fc_ros_resolution_matrix/fc_ros_resolution_candidate_matrix.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/REPORT.md`
- `results_v3/wave70b_fc_ros_computational_scout/integrated_fc_ros_candidate_scout.tsv`
- `results_v3/wave70c_inhibitory_receptor_geneformer_direction/REPORT.md`
- `results_v3/wave70c_inhibitory_receptor_geneformer_direction/geneformer_direction_candidate_calls.tsv`
- `results_v3/wave73_p2rx7_stratification_test/REPORT.md`
- `results_v3/wave73_p2rx7_stratification_test/p2rx7_stratification_decision.tsv`
- `results_v3/wave74_ephx2_direct_ratio_audit/REPORT.md`
- `results_v3/wave74_ephx2_direct_ratio_audit/ephx2_direct_ratio_decision.tsv`
- Geneformer outputs: `results_v3/wave57_intervention_first_geneformer_screen/*`, `results_v3/wave69d_gse282122_geneformer_remission_centroid/*`, `results_v3/wave70c_inhibitory_receptor_geneformer_direction/*`, plus older `results_v3/geneformer_*` file inventory.
- L1000/CMap-like outputs: `results_v3/wave15_perturbation_drug_response/summary.json`, `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`, `results_v3/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv`, `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_summary.json`, `results_v3/wave24_l1000_recurrent_reversal/*`, `results_v3/wave27_l1000_unknown_deconvolution/*`, `results_v3/wave41_l1000_external_unknown_deconvolution/*`.
- Checkpoint/run reports: `ORCHESTRATION_LOG_V3.md`, `LAB_NOTEBOOK_V3.md`, `BLOCKERS_V3.md`, `CONVERGENCE_CHECK_35.md`.

## Candidate Table

| Candidate | Evidence type | Perturbation/response signal | Decisive blocker | Recommended next test |
| --- | --- | --- | --- | --- |
| `MED16` / Mediator module | Real perturbation in primary mouse macrophage RNA-seq plus mouse CRISPR screen; Wave53/Wave15 selectivity anchor | `Med16_KO` had target/APC suppression `3.14`, selectivity `2.31`, target-vs-IFN margin `2.34`; strongest real perturbation signal found locally | Not a practical target: non-druggable/broad transcriptional Mediator biology; no strict MS anchor; no safe selective intervention | Use only as positive-control signature. Wave75/76 local test: re-score available perturbation/L1000/Geneformer tables for perturbations that phenocopy MED16 selectivity without broad transcription/stress, then require human myeloid validation before any target claim |
| `LILRB2` | Cell-resolved treatment-response association plus weak model direction; Wave70b | In GSE282122 DCs, remission association adjusted beta `-0.949`, adjusted FDR `0.019`; nominal MS down signal and 2 broad positive compartments | No direct target perturbation; no RA anti-TNF response replication; no Wave68/Wave62 cross-autoimmune genetic anchor; inhibitory-receptor directionality is unresolved | Bounded Wave75/76 audit: baseline and delta `LILRB2` against IFN/APC, HLA-II, lysosomal/APC, remission, and generic inflammation in GSE282122/RA/MS. Promote only to wet-lab test if baseline target level predicts module normalization beyond generic inflammation |
| `LILRB1` / `LILRB4` | Cell-resolved GSE282122 anti-TNF remission-response association; Wave70b | Mono/macrophage `LILRB1` adjusted beta `-1.075`, FDR `0.010`; `LILRB4` adjusted beta `-1.507`, FDR `0.017` | No RA response replication, weak/absent MS anchor, no direct perturbation, no local genetics anchor; model direction for `LILRB4` points toward possible restoration/agonism rather than simple antagonism | Same bounded LILRB audit as above. Keep family-level and direction-agnostic until direct agonism/antagonism perturbation exists |
| `CD300A` / `INPP5D` | Mouse BMDM CRISPR efferocytosis trends plus RA/gene hints | `CD300A` KO showed efferocytosis-enhancement trend (`median_efficient_minus_noneater_lfc=1.34`) but FDR high; `INPP5D` had RA anti-TNF paired down FDR `0.029` and efferocytosis trend | Wave37 CRISPR screen lacks transcriptomic/autoimmune readout; FDRs unresolved; no cross-disease disease-state convergence; no direct module perturbation | Low-priority bounded test only if LILRB audit fails: check whether baseline or treatment delta separates IFN/APC and lysosomal/APC modules beyond generic inflammation. Do not nominate from efferocytosis alone |
| `RFX5` | Direct Mixscale CRISPRi weak target suppression | Target module effect `-0.552`, selectivity `0.523`; direct MHC-II transcriptional node | Whole MHC-II suppression is host-defense blocked; weak signal from stimulated cancer-cell Perturb-seq, no MS/cross-disease anchor, no tractable selective modality | Keep as assay positive control for antigen-presentation suppression, not an intervention candidate |
| `CHUK` | Direct Mixscale CRISPRi weak target suppression | Target module effect `-0.672`, selectivity `0.335` | Broad NF-kB/IKK biology, host-defense risk, no selectivity/novelty | Closed except as broad NF-kB comparator |
| `GSK3B` | Real mouse macrophage perturbation | `Gsk3b_KO` target suppression `1.62`, selectivity `0.778`, target-vs-IFN margin `0.827` | Prior-art crowded, pleiotropic neuroimmune/metabolic biology, no strict MS/cross-disease anchor; Wave53 no-go | Keep closed. Reopen only with isoform/dose-selective human myeloid/MS lesion data separating APC suppression from WNT/metabolic/neurotoxicity |

## No-Go List

| Candidate/class | Why closed |
| --- | --- |
| `JAK1`, `JAK2`, `IFNGR1/2`, `IFNAR1/2`, `TYK2`, `STAT1`, ruxolitinib | Real perturbation exists, but it is broad IFN/JAK collapse, not selective lysosomal/APC modulation. Use only as positive controls. |
| Broad anti-TNF / `TNFRSF1A` damping | RA/IBD pharmacodynamic movement exists, but anti-TNF is broad and MS direction is unsafe; GSE282122 and RA audits do not isolate a myeloid target-specific controller. |
| `FCGR2A`, `FCGR2B`, `NCF1`, `NCF2`, `CYBB`, `CYBA`, `LYN`, `SYK`, `BTK`, `PIK3CD`, `PIK3CG` | Fc/ROS kinase and NOX biology is blocked by host-defense, immunodeficiency, broad signaling, prior art, or directionality. Geneformer support does not overcome blockers. |
| TAM route: `MERTK`, `AXL`, `TYRO3`, `GAS6`, `PROS1` | Efferocytosis/repair biology is plausible, but local recurrence is weak/contradictory and the likely useful direction is agonism/restoration while available pharmacology is often inhibition or pleiotropic TAM modulation. |
| L1000/CMap recurrent reversers and unknown BRD compounds | Cell-line reversal signatures are dominated by cytotoxic, HSP90/PLK/tubulin/steroid/NF-kB/JAK-like or unresolved compounds. Wave41 deconvolution closed BRD-A72180425/K784-3188 as an ML162-like cytotoxic probe analog. |
| Wave37/Wave38 CRISPR efferocytosis hits such as `LRRC61`, `FAM49B`, `HSPA9`, `CLEC7A`, `TREM2`, `CD300A` as standalone targets | Direct efferocytosis screen is useful biology but lacks transcriptomic autoimmune tissue readouts; Wave38 scanned 184 candidates and promoted 0. Most fail FDR, MS anchor, tractability, or prior-art gates. |
| `CXCR2`, `IL7R` | Wave57 reopened them only as model-supported intervention-first rows, but prior branches already demoted them; efferocytosis unresolved and no strict MS/local perturbation rescue. |
| `P2RX7` / purinergic inflammasome | Wave73 parked: broad purine/cell-state support exists, but specificity, MS, IBD response, RA response, and target-level gene anchors fail. |
| `EPHX2` | Wave74 no-go: no same-study same-site epoxide/diol pairs, so no direct soluble epoxide hydrolase activity ratio. Proxy DiHOME/DHET features cannot support target-level intervention. |
| `GPR183`, `ACSL1`, `NAMPT`, `NAAA`, mapped-gene/genetics/expression-only candidates | Prior branches demoted them. No local perturbation-response evidence inspected here reopens them. |
| `PRKDC`, `BLK`, `SP140`, `RGS14`, `STAT4`, `CD274`, `CD80`, `TNFSF15` from Wave68/69d | Mostly model, descriptive, mapped-genetic, or prior-art/broad biology signals; no direct disease-module perturbation response. |

## Recommended Wave75/76 Local Tests

1. **Mediator positive-control mining**

   Build a strict MED16-phenocopy score across existing perturbation tables only. Required pass criteria: APC/HLA/lysosomal module suppression greater than generic IFN/NF-kB/JAK/stress, no viability/stress induction, and no oncology-like broad transcription signature. Expected output should be a ranked comparator table, not a finding.

2. **LILRB response-direction audit**

   Test `LILRB1`, `LILRB2`, `LILRB4`, and optionally `LILRB3` in GSE282122 myeloid pseudobulk and RA GSE198520 for baseline predictor, paired delta, and responder interaction models adjusted for generic inflammation and baseline target/module level. Add MS GSE111972 and broad h5ad recurrence only as guardrails. Required pass: target-level signal predicts favorable movement of IFN/APC plus lysosomal/APC modules beyond generic inflammation and is directionally consistent across at least IBD plus one independent dataset.

3. **CD300A/INPP5D efferocytosis guardrail check**

   Do not retest as target nominations. Use them to ask whether efferocytosis-negative-regulator trends can coexist with lower IFN/APC and lysosomal/APC modules in patient data. Required pass: disease-response or target perturbation support, not mouse efferocytosis alone.

## Bottom Line

The perturbation-first hunt does not rescue a durable target yet. The strongest usable artifact is `MED16` as a non-druggable selectivity benchmark. The only target-family worth a bounded local Wave75/76 response-direction test is the LILRB inhibitory-receptor cluster, led by `LILRB2` and checked against `LILRB1/LILRB4`. All other branches should stay closed or comparator-only.
