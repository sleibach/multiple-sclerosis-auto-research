# LXR / ABCA1 / ABCG1

Status: demoted  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

V3 explored lipid efflux and lipid-lysosomal myeloid biology but did not produce
a final LXR/ABCA1/ABCG1 therapeutic claim.

## V4 Recalibration Question

Is there a safe, tissue-targeted, or subgroup-specific lipid-efflux intervention
that avoids systemic LXR liabilities?

## Current V4 Contribution

None as an active therapeutic target nomination.

The V4 prior-art standard prevents a lazy kill based only on the fact that
LXR/PPAR/cholesterol-efflux biology is crowded. There is no local evidence that
an equivalent tissue-selective, non-lipogenic LXR/ABCA1/ABCG1 intervention
failed clinically in a repair-enriched MS or cross-autoimmune subgroup with
adequate target engagement.

The candidate still remains demoted because V3's failure was not merely a
prior-art problem. Local evidence showed mixed or negative single-gene
direction, weak genetics, broad nuclear-receptor pharmacology, lipogenesis and
systemic metabolic liabilities, and only context-limited perturbation support.
`ABCA1` and `ABCG1` are better retained as cholesterol-efflux/readout genes for
repair or LIPA/NPC/TAM/TREM2 comparator experiments, not as a V4 target claim.

## V4 Recalibration Verdict

Verdict 3: evidence-driven demotion holds.

Prior-art grade: P1 high crowding for generic LXR/PPAR/RXR and cholesterol
efflux activation in inflammatory/remyelination biology. Not P0
target-invalidating under V4 because the local archive does not document a
directly equivalent correct-direction autoimmune clinical failure with adequate
target engagement. The active blocker is evidence/direction/selectivity, not
only novelty.

## Evidence Ledger

- Sparse-index query before recalibration:
  `./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "LXR ABCA1 ABCG1 lipid efflux remyelination V4" 10`
  returned this candidate file first, followed by V3 Wave19/Wave32/Wave36
  lipid-efflux analyses and `meta/PRIOR_ART_RULEBOOK.md`.
- `subagents_v3/wave19_lysosomal_controller.md` and
  `results_v3/wave19_lysosomal_controller/decision_matrix.tsv`:
  `PPAR_LXR_cholesterol_efflux_activation` was `NO_GO`; V3 recorded
  mixed/negative local direction for `PPARG/NR1H3/ABCG1`, with `ABCA1`
  MS-positive but broad-negative, plus saturated autoimmune/metabolic claims and
  LXR lipogenesis liability.
- `results_v3/wave19_lysosomal_controller/external_evidence_matrix.tsv`:
  generic activation of `PPARG;NR1H3;NR1H2;ABCA1;ABCG1` had chemical matter and
  biological plausibility, but the route was broad, metabolically constrained,
  and locally mixed/negative.
- `results_v3/wave19_lysosomal_controller/source_log.tsv`: local prior-art
  anchors include LXR EAE prior art (PubMed `16955483`), LXR lipogenesis
  liability (PubMed `11090131`), and PPAR-gamma autoimmune trial anchors.
- `subagents_v3/wave13_genetics_prior_art_reopen.md`: scoped genetics found
  only weak `NR1H3` MS credible-set evidence; `ABCA1`/`SOAT1` lacked scoped
  support in that run. The route was called mechanistically relevant but weak
  on genetics and safety.
- `results_v3/wave32_resolution_rescue_audit/resolution_rescue_route_audit.tsv`:
  `LXR_ABCA1_CHOLESTEROL_EFFLUX` was
  `NO_GO_RESOLUTION_MARKER_OR_UNVALIDATED_ROUTE`; it had coherent biology and
  druggability, but no cross-disease coloc/MR/perturbation/foundation support
  and a blocking prior-art/safety profile.
- `subagents_v3/wave36a_gene_level_controller_rescue.md`: RXR/LXR agonism
  produced some favorable submodule movements in a bexarotene context, but only
  in one dataset; V3 did not find independent perturbation replication.
- `subagents_v3/wave36b_hostile_critique.md`: hostile review noted
  `Aged_BEX_vs_Aged_vehicle` had resolution +0.286, lipid/APC +0.024, IFN
  -0.094, stress -0.342; young and stroke-aged contexts did not replicate,
  leaving broad nuclear-receptor pharmacology, weak lipid/APC reduction, and
  age/context dependence.
- `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`
  and `results_v3/wave133_closure_hygiene_correction/wave122_corrected_rank.tsv`:
  `ABCA1`, `ABCG1`, `NR1H2`, and `NR1H3` were all
  `NO_GO_FRESH_SCAN`, lacking genetics, perturbation, foundation, and modality
  gates despite isolated expression trends.
- `results_v3/wave23_orchestrator_nonexpression_axis_triage/raw_api/chembl_search_NR1H3.json`,
  `chembl_search_NR1H2.json`, and ABCA1/NR1H activity files confirm available
  ChEMBL target/assay precedent, but this supports tractability rather than
  therapeutic specificity.

## Next Tier 0 Test

Do not reopen generic systemic LXR/RXR/PPAR agonism or generic
`ABCA1/ABCG1` induction.

Allowed future re-entry test:
- Define a tissue-restricted, non-lipogenic cholesterol-efflux route, preferably
  downstream of LIPA/NPC or lesion-local oxysterol handling rather than broad
  nuclear-receptor agonism.
- In MS lesion-relevant myeloid/microglial data, require target engagement to
  increase cholesterol efflux or myelin-debris lipid export while reducing
  lipid/APC and `HLA-II/CD74/CIITA` programs.
- Require replication in at least one independent autoimmune tissue or a
  natural-experiment/remission dataset.
- Require guardrails showing no `SREBF1/FASN/SCD` lipogenesis program, no
  generic stress response, and no macrophage-density-only explanation.

Pass threshold: at least one direct perturbation dataset plus one independent
autoimmune replication where efflux activation reduces lipid/APC inflammation
with a selectivity ratio at least 2x better than generic IFN/stress/lipogenesis
movement. Otherwise LXR/ABCA1/ABCG1 remains a readout/comparator axis only.
