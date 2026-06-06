# Wave15-B Perturbation and Drug-Response Evidence

Returned: 2026-05-27

## Scope

Search real perturbation/drug-response resources for interventions that reduce `CD74`/`CIITA`/HLA-II antigen presentation more selectively than generic IFN/JAK collapse. This worker does not assess novelty or make a therapeutic claim.

## Data Provenance

- `GSE281048` / Zenodo `14035992`: Mixscale pathway CRISPRi DE tables, local file `data/raw_v3/mixscale/DE_results_all_pathway.zip`.
- `GSE162463`: mouse macrophage MHCII/CD40/PD-L1 CRISPR-screen normalized sgRNA counts.
- `GSE162464`: mouse macrophage NTC/`Gsk3b`/`Med16` +/- IFN-gamma RNA-seq normalized counts.
- `GSE294918`: human macrophage IFN-gamma memory/ruxolitinib processed CPM table.
- L1000FWD/LINCS2020: module-signature API queries plus local `compoundinfo_beta.txt` metadata.

## Module Definition

- Target antigen-presentation module: `CD74, CIITA, RFX5, IFI30, CTSS, HLA-DRA, HLA-DRB1, HLA-DPA1, HLA-DPB1, HLA-DQA1, HLA-DQB1, HLA-DMA, HLA-DMB`.
- Generic IFN/JAK module: `STAT1, IRF1, CXCL10, GBP1, ISG15, IFIT1`.
- Stress/viability proxy module where available: `DDIT3, ATF4, HSPA1A, HSPA1B, HSP90AA1, DNAJB1, HMOX1, JUN, FOS, GADD45A, KLF6, BAX, CASP3`.

Selectivity score is target suppression minus generic IFN suppression, with a small stress penalty. It is a ranking heuristic; raw effect sizes are the evidence.

## Ranked Direct Perturbations

| within_direct_rank | source | dataset | pathway | perturbation | condition | target_module_effect | generic_ifn_effect | stress_module_effect | target_vs_ifn_margin | target_over_ifn_ratio | selectivity_score | evidence_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | mouse_macrophage_RNAseq | GSE162464 |  | Med16_KO | Med16_IFNg_vs_NTC_IFNg | -3.140 | -0.798 | -0.365 | 2.342 | 3.935 | 2.305 | selective_target_suppression |
| 2 | mouse_macrophage_RNAseq | GSE162464 |  | Gsk3b_KO | Gsk3b_IFNg_vs_NTC_IFNg | -1.622 | -0.795 | -0.492 | 0.827 | 2.040 | 0.778 | selective_target_suppression |
| 3 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | TNFA | TNFRSF1A | TNFA_pathway | -0.968 | -0.306 | 0.092 | 0.662 | 3.165 | 0.621 | selective_target_suppression |
| 4 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | IFNG | RFX5 | IFNG_pathway | -0.552 | 0.083 | 0.064 | 0.552 | 5.518 | 0.523 | weak_selective_target_suppression |
| 5 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | TNFA | CHUK | TNFA_pathway | -0.672 | -0.269 | 0.150 | 0.403 | 2.497 | 0.335 | weak_selective_target_suppression |
| 6 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | TNFA | SOX9 | TNFA_pathway | -0.304 | -0.129 | 0.043 | 0.174 | 2.349 | 0.155 | target_suppression_not_selective |
| 7 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | IFNG | JAK1 | IFNG_pathway | -1.032 | -0.873 | -0.071 | 0.159 | 1.182 | 0.152 | target_suppression_not_selective |
| 8 | human_macrophage_RNAseq_descriptive | GSE294918 |  | IFNG_8H | D0_IFNy_8H_vs_D0_unstim | -0.120 | 4.403 | -0.163 | 0.120 | 1.196 | 0.103 | null_or_wrong_direction |
| 9 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | IFNB | CEBPB | IFNB_pathway | -0.211 | -0.108 | -0.076 | 0.103 | 1.954 | 0.096 | null_or_wrong_direction |
| 10 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | TNFA | ZNF267 | TNFA_pathway | -0.136 | -0.046 | -0.004 | 0.090 | 1.359 | 0.090 | null_or_wrong_direction |
| 11 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | IFNG | IRF2 | IFNG_pathway | -0.161 | -0.060 | 0.066 | 0.100 | 1.606 | 0.071 | null_or_wrong_direction |
| 12 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | IFNG | JUN | IFNG_pathway | -0.088 | 0.016 | -0.194 | 0.088 | 0.880 | 0.069 | null_or_wrong_direction |
| 13 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | TNFA | MMP9 | TNFA_pathway | -0.071 | 0.051 | 0.019 | 0.071 | 0.712 | 0.062 | null_or_wrong_direction |
| 14 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | IFNG | PLEK | IFNG_pathway | -0.064 | 0.029 | -0.025 | 0.064 | 0.637 | 0.061 | null_or_wrong_direction |
| 15 | Mixscale_CRISPRi | GSE281048_Zenodo14035992 | TNFA | FADD | TNFA_pathway | -0.174 | -0.116 | -0.008 | 0.058 | 1.502 | 0.057 | null_or_wrong_direction |

## Key Findings

- `RFX5` CRISPRi in IFN-gamma-stimulated Mixscale cells is the cleanest selective genetic gate: target module mean log2FC `-0.552`, generic IFN mean log2FC `0.083`, margin `0.552`. This is mechanistically coherent but not a druggable compound result.
- `Med16` KO in mouse macrophages is a strong non-druggable gate comparator: target module `-3.140`, generic IFN `-0.798`, margin `2.342`.
- `Gsk3b` KO in mouse macrophages remains the strongest druggable-ish controller evidence: target module `-1.622`, generic IFN `-0.795`, margin `0.827`, selectivity score `0.778`. It is still comparator evidence, not enough to nominate a drug, because GSK3 biology is broad and the support is mouse KO rather than selective human chemical perturbation.
- `ruxolitinib` is the expected broad-JAK positive control, not selective: in human macrophage CPM the LPS0 contrast has target module `-0.991` and generic IFN `-3.736`.

## L1000FWD Compound Signal

| pert_id | cmap_name | target | moa | target_antigen_presentation_best_rank | target_antigen_presentation_min_qval | target_antigen_presentation_max_reversal_strength | generic_ifn_jak_max_reversal_strength | l1000_target_minus_generic_reversal_strength | l1000_selectivity_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BRD-A39996500 | radicicol |  |  | 1.000 | 0.000 | 25.437 | 0.000 | 25.437 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K33583600 | BRD-K33583600 |  |  | 5.000 | 0.000 | 23.215 | 0.000 | 23.215 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K64890080 | BI-2536 | PLK1 | PLK inhibitor | 2.000 | 0.000 | 20.840 | 0.000 | 20.840 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K01436366 | XMD-1150 | LRRK2 | Leucine rich repeat kinase inhibitor | 4.000 | 0.000 | 20.268 | 0.000 | 20.268 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K82109576 | vincristine | TUBB | Tubulin inhibitor | 7.000 | 0.000 | 19.520 | 0.000 | 19.520 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K81473043 | tanespimycin | HSP90AA1 | HSP inhibitor | 8.000 | 0.000 | 19.455 | 0.000 | 19.455 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K30707190 | PNU-74654 | CTNNB1 | Beta-catenin inhibitor | 10.000 | 0.000 | 19.323 | 0.000 | 19.323 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K92301463 | BRD-K92301463 |  |  | 6.000 | 0.000 | 19.253 | 0.000 | 19.253 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K99530743 | BRD-K99530743 |  |  | 9.000 | 0.000 | 18.876 | 0.000 | 18.876 | target_opposite_hit_absent_from_generic_top50 |
| BRD-A56020723 | CA-074-Me | CTSB | Cathepsin inhibitor | 13.000 | 0.000 | 16.994 | 0.000 | 16.994 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K37865504 | LY-2183240 | FAAH | FAAH inhibitor | 19.000 | 0.000 | 16.384 | 0.000 | 16.384 | target_opposite_hit_absent_from_generic_top50 |
| BRD-K75999307 | BRD-K75999307 |  |  | 16.000 | 0.000 | 15.955 | 0.000 | 15.955 | target_opposite_hit_absent_from_generic_top50 |

L1000FWD is treated as weak supportive or negative evidence only: it is a LINCS cell-line signature search, not an antigen-presentation assay. No L1000 compound alone is strong enough for nomination.

## Candidate-Level Disposition

| candidate | n_evidence_records | sources | best_direct_selectivity_score | best_direct_target_suppression | best_direct_target_vs_ifn_margin | direct_evidence_calls | gse162463_mhcii_low_gate_rank_if_available | nomination_strength | nomination_priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Med16_KO | 2 | mouse_macrophage_CRISPR_screen;mouse_macrophage_RNAseq | 2.305 | 3.140 | 2.342 | selective_target_suppression | 42.000 | strong_mechanistic_comparator_not_druggable | 1 |
| Gsk3b_KO | 2 | mouse_macrophage_CRISPR_screen;mouse_macrophage_RNAseq | 0.778 | 1.622 | 0.827 | selective_target_suppression | 39.000 | candidate_evidence_not_enough_to_nominate_drug | 2 |
| RFX5 | 1 | Mixscale_CRISPRi | 0.523 | 0.552 | 0.552 | weak_selective_target_suppression |  | weak_followup_only | 4 |
| CHUK | 1 | Mixscale_CRISPRi | 0.335 | 0.672 | 0.403 | weak_selective_target_suppression |  | weak_followup_only | 4 |
| JAK1 | 2 | Mixscale_CRISPRi | 0.152 | 1.032 | 0.159 | null_or_wrong_direction;target_suppression_not_selective |  | comparator_only_broad_ifn_jak_collapse | 5 |
| JAK2 | 1 | Mixscale_CRISPRi | -0.052 | 1.080 | -0.050 | broad_ifn_jak_like_collapse |  | comparator_only_broad_ifn_jak_collapse | 5 |
| IFNGR2 | 1 | Mixscale_CRISPRi | -0.101 | 1.331 | -0.099 | broad_ifn_jak_like_collapse |  | comparator_only_broad_ifn_jak_collapse | 5 |
| IFNGR1 | 1 | Mixscale_CRISPRi | -0.112 | 1.402 | -0.108 | broad_ifn_jak_like_collapse |  | comparator_only_broad_ifn_jak_collapse | 5 |
| STAT1 | 2 | Mixscale_CRISPRi | -0.401 | 1.012 | -0.396 | broad_ifn_jak_like_collapse;null_or_wrong_direction |  | comparator_only_broad_ifn_jak_collapse | 5 |
| TYK2 | 1 | Mixscale_CRISPRi | -0.405 | 0.641 | -0.380 | broad_ifn_jak_like_collapse |  | comparator_only_broad_ifn_jak_collapse | 5 |
| IFNAR2 | 1 | Mixscale_CRISPRi | -0.510 | 0.661 | -0.459 | broad_ifn_jak_like_collapse |  | comparator_only_broad_ifn_jak_collapse | 5 |
| IFNAR1 | 1 | Mixscale_CRISPRi | -0.659 | 0.351 | -0.659 | target_suppression_not_selective |  | comparator_only_broad_ifn_jak_collapse | 5 |
| ruxolitinib | 4 | human_macrophage_RNAseq_descriptive | -2.262 | 1.020 | -2.226 | broad_ifn_jak_like_collapse |  | comparator_only_broad_ifn_jak_collapse | 5 |
| TNFRSF1A | 1 | Mixscale_CRISPRi | 0.621 | 0.968 | 0.662 | selective_target_suppression |  | not_nominated | 6 |
| SOX9 | 1 | Mixscale_CRISPRi | 0.155 | 0.304 | 0.174 | target_suppression_not_selective |  | not_nominated | 6 |
| IFNG_8H | 1 | human_macrophage_RNAseq_descriptive | 0.103 | 0.120 | 0.120 | null_or_wrong_direction |  | not_nominated | 6 |
| CEBPB | 3 | Mixscale_CRISPRi | 0.096 | 0.211 | 0.103 | null_or_wrong_direction |  | not_nominated | 6 |
| ZNF267 | 2 | Mixscale_CRISPRi | 0.090 | 0.136 | 0.090 | null_or_wrong_direction |  | not_nominated | 6 |
| IRF2 | 1 | Mixscale_CRISPRi | 0.071 | 0.161 | 0.100 | null_or_wrong_direction |  | not_nominated | 6 |
| JUN | 3 | Mixscale_CRISPRi | 0.069 | 0.088 | 0.088 | null_or_wrong_direction |  | not_nominated | 6 |

## Verdict

No compound is strong enough to nominate from perturbation/drug-response data alone. The strongest direct selectivity signal is genetic gating of the CIITA/RFX5/MHC-II program (`RFX5` CRISPRi and `Med16` KO), with `Gsk3b` KO as the best druggable-ish upstream comparator. Broad JAK/IFNGR perturbations and ruxolitinib reduce the target module but fail the selectivity requirement because they collapse the generic IFN module. The appropriate use of this worker output is as comparator evidence for the orchestrator, not as a standalone therapeutic claim.

## Reproducibility

Command:

```bash
./.venv_v3_py312/bin/python scripts/v3_wave15_perturbation_drug_response.py
```

Outputs:
- `results_v3/wave15_perturbation_drug_response/mixscale_selectivity_by_perturbation.tsv`
- `results_v3/wave15_perturbation_drug_response/mixscale_selectivity_by_cell_type.tsv`
- `results_v3/wave15_perturbation_drug_response/mixscale_readout_gene_effects.tsv`
- `results_v3/wave15_perturbation_drug_response/gse162464_mouse_rna_selectivity.tsv`
- `results_v3/wave15_perturbation_drug_response/gse162464_mouse_rna_readout_gene_effects.tsv`
- `results_v3/wave15_perturbation_drug_response/gse162463_mouse_crispr_screen_gene_summary.tsv`
- `results_v3/wave15_perturbation_drug_response/gse162463_mouse_crispr_screen_sgrna_effects.tsv`
- `results_v3/wave15_perturbation_drug_response/gse294918_human_ruxolitinib_selectivity.tsv`
- `results_v3/wave15_perturbation_drug_response/gse294918_human_ruxolitinib_readout_gene_effects.tsv`
- `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_raw.json`
- `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_hits.tsv`
- `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_compound_rank.tsv`
- `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_summary.json`
- `results_v3/wave15_perturbation_drug_response/control_compound_metadata.tsv`
- `results_v3/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv`
- `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
- `results_v3/wave15_perturbation_drug_response/summary.json`
- `results_v3/wave15_perturbation_drug_response/run_log.tsv`
- `subagents_v3/wave15_perturbation_drug_response.md`

