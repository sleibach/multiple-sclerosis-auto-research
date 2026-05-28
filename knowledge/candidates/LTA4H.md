# LTA4H

Status: demoted  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

V3 treated leukotriene/lipid mediator routes as crowded or directionally
fragile and did not mature LTA4H.

## V4 Recalibration Question

Is the V4 contribution a new lipid-mediator balance mechanism, subgroup, or
combination rather than generic leukotriene blockade?

## Current V4 Contribution

None as an active V4 therapeutic target nomination.

LTA4H remains useful as a lipid-mediator comparator for inflammatory myeloid
and foamy-microglia biology, but V3 evidence does not support reopening it as a
candidate. The V4 prior-art rule removes "leukotriene biology is crowded" as a
standalone kill. The demotion still holds because LTA4H lacks target-resolved
genetics, perturbation/foundation support, and V4-specific evidence separating
an LTA4H intervention from generic LTB4/BLT inflammatory-lipid modulation.

## V4 Recalibration Verdict

Verdict 3: evidence-driven demotion holds.

Prior-art grade: P1 high crowding for leukotriene/LTB4 inflammatory-disease
biology and LTA4H/BLT pharmacology. Not P0 target-invalidating because the
local archive does not document an equivalent LTA4H intervention failed
clinically in the proposed autoimmune indication with adequate target
engagement for target-mechanistic reasons.

## Evidence Ledger

- Sparse-index query run before recalibration:
  `./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "LTA4H V4 prior art autoimmune lipid mediator subgroup" 10`.
- `subagents_v3/wave7_lipid_myeloid_target_scout_report.md`: LTA4H had local
  MS white-matter microglia delta 0.809, Hedges g 1.357, p 0.00636, plus
  MIMS2-like microglia effect 1.483, p 0.0108 and foamy proteomics effect
  0.169, p 0.0321, but was called no-go after Geneformer/prior-art demotion.
- `subagents_v3/wave8_candidate_breadth_report.md`: LTA4H had 4 token
  contexts, 6 disease cells with token, mean cosine shift -0.000289, mean
  projection shift -0.00278, and 0 support contexts in the Geneformer deletion
  summary; interpretation: negative by posthoc rule, keep demoted.
- `results_v3/wave20_unrestricted_survivor/wave20_local_evidence.tsv`:
  demoted with positive local signals in Crohn myeloid, UC myeloid, T1D
  acinar, and MS white matter, but no strict core survival and no model/real
  perturbation support.
- `results_v3/wave20_unrestricted_survivor/wave20_gate_matrix.tsv`: failed
  `FAIL_RETAINED_ONLY_NO_STRICT_CORE_SURVIVAL` and
  `FAIL_NO_MODEL_OR_REAL_PERTURBATION`; blocker noted direct EAE/MS and
  inflammatory-disease inhibitor prior art plus prior Geneformer veto.
- `results_v3/wave20_unrestricted_survivor/wave20_chembl_target_search.tsv`:
  ChEMBL target `CHEMBL4618`, 2863 activity records, confirming druggability
  but not V4 specificity.
- `results_v3/wave166_same_gene_genetics_cellstate_overlap/same_gene_genetics_cellstate_rank.tsv`:
  LTA4H had some cell-state support but no cross-disease genetic support, no
  MR/coloc, no perturbation/foundation support, and no druggability-derived
  V4 promotion signal.

## Next Tier 0 Test

Do not reopen generic LTA4H inhibition or generic LTB4/BLT blockade.

Allowed future re-entry test:
- Use lipidomics/metabolomics or treatment-resistance cohorts to test whether
  an LTA4H/LTB4-high inflammatory myeloid state predicts trajectory or
  treatment failure independently of neutrophil/myeloid abundance, TNF/NF-kB,
  and generic inflammatory burden.
- Require target-specific perturbation: LTA4H inhibition or BLT blockade must
  reduce the disease-relevant lipid-myeloid module without collapsing host
  defense or merely tracking cell abundance.
- Require one independent replication outside IBD.

Pass only if the contribution is a biomarker-defined lipid-mediator subgroup or
combination strategy that cannot be reduced to generic leukotriene blockade.

## V5 Recalibration: Lipid-Lysosomal Stratification

Requested scope: re-evaluate LTA4H with patient stratification by the
cross-autoimmune lipid-lysosomal myeloid module identified in V3/V4.

V5 prior-art standard:
- Leukotriene/LTB4/LTA4H prior art remains `P1 high crowding`, not `P0`
  target-invalidating. A biomarker-defined lipid-mediator subgroup or
  combination strategy would still be a valid V5 contribution if supported.

V5 verdict:
- Demotion holds at Tier 0 for evidence-driven reasons.
- The proposed stratification idea is conceptually valid but not yet evidenced.
  The local record contains expression/cell-state positives and ChEMBL
  tractability, but no lipidomics/metabolomics confirmation, no
  target-specific perturbation showing beneficial module movement, no
  independent non-IBD replication with causal direction, and no treatment-
  response subgroup where LTA4H/LTB4 adds predictive value beyond generic
  myeloid inflammation.

Searches and evidence used:
- Sparse-index query:
  `./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "LTA4H lipid lysosomal module stratification autoimmune MS V5" 12`.
- Top hit was this candidate file, followed by V3 lipid-myeloid scout reports
  and prior V4 decision material.
- No new internet search was used in this V5 check.

Re-entry criteria:
- LTA4H may re-enter Tier 0 only if a non-transcriptomic or perturbational
  channel appears: lipidomics showing LTB4/LTA4H-pathway enrichment in the
  lipid-lysosomal-high subgroup, or LTA4H/BLT perturbation reducing a disease-
  relevant inflammatory myeloid phenotype while preserving host-defense and
  repair modules.
- A transcriptomic LTA4H-high subgroup alone is insufficient because V3 already
  showed local expression positives without strict-core, genetics, or
  perturbation survival.
