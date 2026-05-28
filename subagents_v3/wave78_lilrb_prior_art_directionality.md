# Wave78 LILRB Prior-Art and Directionality Sidecar

Date: 2026-05-27

Scope: hostile scout for `LILRB1`/ILT2, `LILRB2`/ILT4, and `LILRB4`/ILT3 as autoimmune/MS intervention points. No code was edited. This report does not claim a finding.

## Executive Call

Do not promote the LILRB family as a V3 therapeutic intervention point from current evidence. The family is biologically real and antibody-druggable, but the intervention direction is not stable: autoimmune tolerance biology mostly points toward agonism/restoration of inhibitory signaling, while the strongest existing drug programs are oncology antagonists intended to activate myeloid/T-cell immunity. The local Wave70 evidence instead shows lower `LILRB1/2/4` expression in IBD anti-TNF remitters, which can be read as a response-state marker rather than proof that antagonism would resolve autoimmune inflammation.

If the local Wave78 audit is positive, the only member worth keeping as a bounded follow-up is `LILRB2`, and only as a target-level biomarker/falsification lead. It should not be promoted as a drug target unless direct agonist-vs-antagonist perturbation in primary human myeloid cells shows receptor-specific resolution of IFN/APC and lysosomal/APC programs beyond generic inflammation.

## Local Evidence Cross-Check

| target | local support | local blocker |
| --- | --- | --- |
| `LILRB2` | Strongest local signal: GSE282122 DC remission adjusted beta `-0.949`, FDR `0.0191`; Mono_macro beta `-0.891`, FDR `0.0760`; MS GSE111972 nominal down delta `-0.730`, p `0.00778`, FDR `0.834`; broad h5ad positives in Crohn/UC. | No RA anti-TNF replication (`FDR 0.278` paired; response FDR `0.894`), no direct perturbation, no local Wave62 cross-autoimmune target-resolution call, direction ambiguous. |
| `LILRB1` | GSE282122 Mono_macro remission adjusted beta `-1.075`, FDR `0.0104`; broad h5ad positives in Crohn/UC. Geneformer token deletion weakly moves UC Mono_macro cells toward remission. | MS null, RA null, expression-state signal only; widespread NK/T/B/myeloid expression makes systemic targeting high-risk. |
| `LILRB4` | GSE282122 Mono_macro remission adjusted beta `-1.507`, FDR `0.0167`; Geneformer direction weakly favors restoration/agonism; mouse efferocytosis screen shows KO-impairment trend (`median efficient-minus-noneater LFC -0.437`, unresolved). | MS null, RA null, broad h5ad only T1D hint; biology is bifurcated between tolerogenic APCs and pathogenic/tumor plasma-myeloid states. |

Wave62 pQTL colocalization rows exist for `LILRB4` in RA/psoriasis and `LILRB2` in Crohn/T1D, but Wave62 reported zero reopen calls and these rows do not provide an MS or cross-disease genetic anchor.

## Directionality Assessment

| target | agonism/restoration | inhibition/antagonism | sidecar call |
| --- | --- | --- | --- |
| `LILRB1` | Mechanistically plausible for tolerance through HLA-G/MHC-I inhibitory signaling, but not locally supported as a resolving expression direction. | Oncology blockers such as SAR444881/BND-22 are designed to restore antitumor immunity; that direction is conceptually hostile to autoimmune resolution. | `PARK_DIRECTIONALITY`; do not promote. |
| `LILRB2` | Best theoretical autoimmune direction is agonism/restoration of myeloid inhibitory signaling, but practical agonist pharmacology is immature and prior-art crowded. | Local Geneformer/decrease-in-remitters points toward suppression, but oncology literature interprets LILRB2 blockade as myeloid activation/reprogramming, not anti-inflammatory resolution. | Keep only as bounded biomarker/perturbation test if local audit is positive. |
| `LILRB4` | Strongest tolerogenic argument: ILT3/LILRB4 on DC/monocytes/macrophages can support immune tolerance and T-cell anergy. | LILRB4 blockade/depletion is active in AML/oncology, and lupus/plasma-cell literature creates a narrow but conflicted antagonist rationale. | `NO_PROMOTION`; too cell-context dependent and prior-art blocked for CNS/MS. |

## Prior Art and Program Blockers

`LILRB2` antagonist space is crowded. Verified examples include MK-4830 (`NCT03564691`), JTX-8064 (`NCT04669899`), IO-108 (`NCT05054348`), BMS/Five Prime ILT4 antibody patents including `US11401328B2`, and newer ILT4 antibody filings. These programs are immune-activating oncology programs, not autoimmune-resolution programs.

`LILRB1` antagonist space is also active: SAR444881/BND-22 is an anti-ILT2/LILRB1 antibody in advanced solid tumors (`NCT04717375`), and NGM707 is a dual ILT2/ILT4 antagonist (`NCT04913337`). Dual LILRB1/2 patents such as `WO2022187968A1` create freedom-to-operate pressure for generic LILRB1/2 biologics.

`LILRB4` is the most prior-art constrained for MS/CNS. IO-202 is an anti-LILRB4 antibody in AML/CMML and solid-tumor programs. `WO2024155891A2` explicitly claims anti-LILRB4 antibody or LILRB4-Fc approaches for neurological diseases including multiple sclerosis and microglial dysfunction. Older ILT3/LILRB4 tolerogenic/soluble receptor claims (`US9078858B2`, `US8901281B2`) also prefigure broad autoimmune agonism/soluble-ILT3 concepts.

Toxicity concern: systemic antagonism of these inhibitory receptors is intended to break immune suppression. In an autoimmune setting that raises a direct risk of worsening inflammatory myeloid activation, T-cell activation, loss of tolerance, and immune-related adverse events. Systemic agonism has the opposite risk: host-defense, vaccine-response, and tumor-surveillance suppression.

## Exact Blockers

1. Directionality is unresolved at receptor level. Local patient-response data point to lower expression in responders, but established receptor biology says inhibitory signaling is tolerogenic.
2. No direct human autoimmune myeloid perturbation separates LILRB agonism from antagonism.
3. No RA replication and no strong MS guardrail in current local evidence.
4. Existing oncology antibodies already occupy the clean antagonist route.
5. Broad autoimmune agonism/tolerogenic routes are prefigured by ILT3-Fc and targeted HLA-G/LILRB immunotolerance prior art.
6. `LILRB4` has direct CNS/MS patent prior art and SLE/plasma-cell vs DC directionality conflict.

## Suggested Pivot

If the local audit does not show receptor-specific resolution beyond generic inflammation, pivot away from LILRBs as targets. Treat `LILRB2` as a response-state biomarker comparator only, then test inhibitory axes with clearer MS lesion directionality and less oncology-antagonist conflict, especially CD200/CD200R or CD47/SIRPA restoration in MS lesion myeloid biology. A second practical pivot is the already shortlisted non-LILRB targetability set (`CD58`, `SPNS1`, `P4HB`, `SEL1L3`) under the same residualization and response-direction gates.

## Sources Checked

Local: `CONVERGENCE_CHECK_37.md`; `results_v3/wave70b_fc_ros_computational_scout/REPORT.md`; `results_v3/wave70c_inhibitory_receptor_geneformer_direction/REPORT.md`; `results_v3/wave62_opentargets_target_resolution/REPORT.md`; `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`; `subagents_v3/wave75a_perturbation_first_controller_hunt.md`; `subagents_v3/wave78a_lilrb_prior_art_feasibility.md`.

External verified sources: MK-4830 PubMed `34598945` / `NCT03564691`; JTX-8064 `NCT04669899`; IO-108 `NCT05054348`; SAR444881/BND-22 `NCT04717375`; NGM707 `NCT04913337`; IO-202 LILRB4 clinical report; LILRB4/FN lupus abstract at Journal of Immunology 2021 supplement; HLA-G/LILRB1/2 MS PLoS One article DOI `10.1371/journal.pone.0011296`; MS inhibitory molecule lesion paper PMID `17879969`; patents `US11401328B2`, `WO2024155891A2`, `US9078858B2`, `US8901281B2`, `WO2022187968A1`.
