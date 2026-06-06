# Wave98 CCL20/CCR6 Forcing Audit

Random seed: `20260527`.

## Question

Does the only Wave97 reopened candidate, `CCL20`, survive as a
CCL20/CCR6 cross-autoimmune therapeutic intervention axis rather than a
state marker or prior-art trap?

## Verdict

Analysis call: `NO_GO_CCL20_CCR6_PRIOR_ART_BLOCKED`.

Claim-grade gates passed: `1/7`.

Failed gates:

- `receptor_coupled_to_c15_state`
- `ms_claim_grade_anchor`
- `target_resolved_genetics_or_coloc`
- `directional_perturbation_or_foundation_support`
- `novelty_not_blocked`
- `therapeutic_feasibility_without_host_defense_penalty`

Interpretation: `CCL20` remains a credible inflammatory ligand-state
readout near the C15ORF48/MOCCI branch, but the actionable axis fails
because the receptor (`CCR6`) does not share the C15 state locally, MS
anchoring is not claim-grade, target-resolved genetics are insufficient,
perturbation/foundation support is absent, and direct autoimmune/MS
prior art blocks novelty.

## Axis Summary

| entity | role | wave97_call | c15_positive_disease_count | c15_state_pearson_r | residual_case_positive_disease_count | ms_delta_log2 | ms_p | ms_fdr | strong_qtl_coloc_disease_count | opentargets_like_genetic_disease_count | geneformer_strong_support_contexts | wave81_call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CCL20 | ligand | REOPEN_AFTER_RESIDUAL_COSTATE | 3 | 0.7105455631170888 | 1.0 | 1.1469018183892334 | 0.0611072952242856 | 0.8989378106274888 | 1.0 | 5.0 | 0.0 | NO_GO_NO_PERTURBATION_SUPPORT |
| CCR6 | receptor |  | 0 | 0.4005887115562238 | 0.0 | 0.2229856175356008 | 0.7784945025694487 | 0.9741955192514664 | 2.0 |  |  |  |

## Gate Matrix

| gate | status | evidence | failure_if_false |
| --- | --- | --- | --- |
| ligand_state_recurrence | True | CCL20 c15_positive_diseases=3; c15_state_r=0.7105; wave97_call=REOPEN_AFTER_RESIDUAL_COSTATE | ligand does not reproduce as a residual C15-proximal state marker |
| receptor_coupled_to_c15_state | False | CCR6 c15_positive_diseases=0; donor_case_positive_diseases=0; wave96_call=NO_GO_C15_CONTROLLER_SEARCH | ligand signal is not matched by disease-cell receptor-state coupling |
| ms_claim_grade_anchor | False | CCL20 MS white-matter delta=1.147; p=0.06111; fdr=0.8989 | MS evidence is nominal/trend-only rather than claim-grade |
| target_resolved_genetics_or_coloc | False | CCL20 strong_qtl_coloc_diseases=1; CCR6 strong_qtl_coloc_diseases=2; CCL20 OpenTargets-like disease count=5; CCR6 OpenTargets-like disease count= | mapped/associated-target evidence does not substitute for coloc-grade genetics |
| directional_perturbation_or_foundation_support | False | Geneformer strong_support_contexts=0; contexts_with_token_ge_3_cells=0; wave81_call=NO_GO_NO_PERTURBATION_SUPPORT | no real perturbation or usable foundation-model support for beneficial direction |
| novelty_not_blocked | False | Blocked by EAE/MS mechanistic prior (PMID:19305396), negative/compensability EAE prior (PMID:36527746), anti-CCL20 PsA clinical trial (NCT02671188), and anti-CCL20 autoimmune/MS patent claims (US8491901B2; WO2017064564A2). | direct prior art already covers CCL20/CCR6 autoimmune/MS therapeutic concept |
| therapeutic_feasibility_without_host_defense_penalty | False | CCL20 is secreted and antibody-druggable, but CCR6/CCL20 controls mucosal/skin immune cell trafficking and has an antimicrobial/mucosal-surface role; GSK3050002 reached a PsA study plan but no current efficacy-positive autoimmune program was found in local audit. | modality exists, but selectivity and host-defense/trafficking risk remain unresolved |

## Verified Prior-Art Sources

| source_id | kind | axis | claim_used | url | effect_on_wave98 |
| --- | --- | --- | --- | --- | --- |
| PMID:19305396 | literature | CCR6/CCL20 in EAE CNS entry | CCR6-regulated Th17 entry through choroid plexus is required for EAE initiation. | https://pubmed.ncbi.nlm.nih.gov/19305396/ | direct MS/EAE mechanistic prior art |
| PMID:36527746 | literature | CCR6/CCL20 in EAE | CCL20/CCR6 signaling reported not essential in an EAE model. | https://pubmed.ncbi.nlm.nih.gov/36527746/ | direction/necessity caution |
| NCT02671188 | clinical_trial | anti-CCL20 antibody in psoriatic arthritis | GSK3050002 is a humanized IgG monoclonal antibody that neutralizes human CCL20 in psoriatic arthritis. | https://clinicaltrials.gov/study/NCT02671188 | clinical/translational prior art |
| US8491901B2 | patent | neutralizing anti-CCL20 antibodies | Neutralizing anti-CCL20 antibodies are disclosed for inflammatory and autoimmune disorders, including multiple sclerosis in patent text. | https://patents.google.com/patent/US8491901B2/en | patent novelty blocker |
| WO2017064564A2 | patent | anti-CCL20/GSK3050002 psoriatic arthritis regimen | Anti-CCL20 antibody regimen around psoriatic arthritis. | https://patents.google.com/patent/WO2017064564A2/en | patent/translational prior art |
| UniProt:P78556 | target_biology | CCL20 ligand biology | CCL20 is a secreted ligand for CCR6 and recruits dendritic cells, effector/memory T cells, B cells, and Th17/Treg populations. | https://www.uniprot.org/uniprotkb/P78556/entry | tractability and host-defense/trafficking caution |

## Decision

Close `CCL20/CCR6` as a V3 therapeutic nomination. Keep it only as a
positive-control inflammatory trafficking axis in future perturbation
ordering experiments around `C15ORF48`/MOCCI.

## Output Files

- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccl20_ccr6_gate_matrix.tsv`
- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccl20_ccr6_axis_summary.tsv`
- `results_v3/wave98_ccl20_ccr6_forcing_audit/verified_prior_art_sources.tsv`
- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccl20_broad_context_rows.tsv`
- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccr6_broad_context_rows.tsv`
- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccl20_ccr6_response_meta.tsv`
- `results_v3/wave98_ccl20_ccr6_forcing_audit/summary.json`
- `results_v3/wave98_ccl20_ccr6_forcing_audit/REPORT.md`
