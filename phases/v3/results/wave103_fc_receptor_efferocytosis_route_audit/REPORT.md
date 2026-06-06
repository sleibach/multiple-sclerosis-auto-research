# Wave103 Fc/FcRn/Efferocytosis Route Audit

## Bottom Line

Branch call: `NO_REOPEN_FC_EFFEROCYTOSIS_ROUTE`.

The Fc/FcRn/efferocytosis route has real perturbation and translational
interest, but no candidate currently combines MS anchoring, cross-disease
module anchoring, genetics, clear intervention direction, safety, and novelty.

## Candidate Ranking

| gene | wave103_call | wave103_score | wave103_gate_count | wave37_screen_call | wave37_contrast_lfc | ms_delta_log2 | ms_p | broad_positive_disease_count | broad_negative_disease_count | wave55_genetic_diseases_ge_0_25 | wave62_strong_qtl_coloc_disease_count | wave62_ms_max_l2g_score | modality | manual_safety_blocker | wave103_missing_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PDCD6IP | PARK_EFFEROCYTOSIS_ROUTE_NO_MS_ANCHOR | 10.22 | 4 | KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 1.217 | 0.05254 | 0.6289 | 1 | 0 | 0 | 0 | 0 | intracellular trafficking protein; no clean autoimmune modality | broad endosomal and exosome biology | ms_anchor;cross_disease_expression;genetic_breadth;modality_ready |
| FCGRT | PARK_EFFEROCYTOSIS_ROUTE_NO_MS_ANCHOR | 0.0489 | 3 | KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 1.049 | 0.02316 | 0.891 | 0 | 3 | 0 | 0 | 0 | approved/clinical biologics and Fc fragments exist for FcRn blockade | IgG lowering infection and humoral-immunity risk; MS/CNS compartment delivery uncertain | ms_anchor;cross_disease_expression;genetic_breadth;prior_not_blocked |
| DAB2 | PARK_EFFEROCYTOSIS_ROUTE_WEAK_CROSS_DISEASE_ANCHOR | 4.656 | 5 | KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0.6555 | 0.5379 | 0.01113 | 0 | 3 | 0 | 0 | 0 | intracellular adaptor; no clean selective modality | broad endocytosis, platelet, and tumor-biology liabilities | cross_disease_expression;genetic_breadth;modality_ready |
| FCGR2B | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | 9 | 4 | UNRESOLVED | -0.1232 | 0.3744 | 0.5996 | 0 | 1 | 0 | 4 | 0 | agonist biologic concept possible but receptor-family selectivity is difficult | Fc receptor balance and B-cell/myeloid immunosuppression risk | real_efferocytosis_perturbation;ms_anchor;cross_disease_expression;direction_clear |
| RYK | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | 8.059 | 3 | KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 1.059 | 0.08131 | 0.5201 | 2 | 0 | 0 | 0 | 0 | surface receptor but autoimmune direction and selectivity unclear | developmental/Wnt-pathway pleiotropy | ms_anchor;cross_disease_expression;genetic_breadth;direction_clear |
| FCGR2A | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | 5 | 2 |  |  | -0.1534 | 0.5827 | 1 | 1 | 0 | 7 | 0 | antibody-accessible receptor but activation/inhibition selectivity is difficult | activating Fc receptor host-defense and immune-complex safety blocker | real_efferocytosis_perturbation;ms_anchor;cross_disease_expression;direction_clear;prior_not_blocked |
| FCGR1A | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | 4 | 2 |  |  | -0.7574 | 0.05193 | 3 | 0 | 0 | 0 | 0 | antibody-accessible but high host-defense risk | macrophage activation and host-defense risk | real_efferocytosis_perturbation;ms_anchor;genetic_breadth;direction_clear;prior_not_blocked |
| CD9 | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | 3.747 | 4 | KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 0.7467 | 1.11 | 0.001969 | 0 | 2 | 0 | 0 | 0 | surface biologic possible but tetraspanin selectivity and direction are poor | ubiquitous tetraspanin and exosome biology | cross_disease_expression;genetic_breadth;direction_clear |
| FCGR3B | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | 1 | 1 |  |  | -0.8648 | 0.448 | 2 | 0 | 0 | 0 | 0 | antibody-accessible but neutrophil biology creates safety and selectivity blockers | neutrophil immune-complex clearance and infection risk | real_efferocytosis_perturbation;ms_anchor;cross_disease_expression;genetic_breadth;direction_clear;prior_not_blocked |
| FCGR3A | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | 0 | 1 |  |  | -0.4958 | 0.07317 | 1 | 0 | 0 | 0 | 0 | antibody-accessible but selective safe anti-inflammatory direction is unresolved | NK/myeloid effector biology and host-defense risk | real_efferocytosis_perturbation;ms_anchor;cross_disease_expression;genetic_breadth;direction_clear;prior_not_blocked |
| TSC1 | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | -0.8212 | 1 | KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR | 1.179 | 0.03642 | 0.7995 | 0 | 0 | 0 | 0 | 0 | pathway drugs exist but target-specific TSC1 modulation is not feasible | mTOR pathway pleiotropy and prior-art saturation | ms_anchor;cross_disease_expression;genetic_breadth;modality_ready;direction_clear;prior_not_blocked |
| FCER1G | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | -1.889 | 0 | UNRESOLVED | 0.1113 | 0.0326 | 0.8964 | 2 | 0 | 0 | 0 | 0 | intracellular adaptor; no selective tissue-safe modality | shared Fc receptor signaling adapter with broad innate immune effects | real_efferocytosis_perturbation;ms_anchor;cross_disease_expression;genetic_breadth;modality_ready;direction_clear;prior_not_blocked |
| MERTK | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | -3 | 2 | UNRESOLVED | -0.6589 | 0.2471 | 0.4293 | 0 | 2 | 0 | 0 | 0 | agonist antibody/ligand concepts possible; inhibitor precedent is opposite direction | oncology, immune tolerance, and receptor agonism-direction blockers | real_efferocytosis_perturbation;ms_anchor;cross_disease_expression;genetic_breadth;direction_clear;prior_not_blocked |
| TYROBP | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | -5 | 0 | UNRESOLVED | -0.6662 | 0.1685 | 0.2297 | 1 | 1 | 0 | 0 | 0 | intracellular adapter; no clean selective modality | shared innate immune signaling adapter | real_efferocytosis_perturbation;ms_anchor;cross_disease_expression;genetic_breadth;modality_ready;direction_clear;prior_not_blocked |
| AXL | NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED | -7 | 1 | UNRESOLVED | -0.4476 | 0.2437 | 0.2187 | 0 | 3 | 0 | 0 | 0 | small-molecule inhibitors exist but likely opposite of desired resolution direction | oncology/infection biology and wrong-direction inhibitor precedent | real_efferocytosis_perturbation;ms_anchor;cross_disease_expression;genetic_breadth;direction_clear;prior_not_blocked |

## Interpretation

- `FCGRT` is the most intervention-ready node because FcRn blockade has human
  drug precedent and Wave37 CRISPR evidence suggests KO can enhance
  efferocytosis. It fails the V3 route here because local MS expression is
  null, broad h5ad expression is negative/contradictory, target-resolved
  autoimmune genetics are absent, and prior art is heavy.
- `DAB2` and `CD9` have MS white-matter expression anchors plus real
  efferocytosis-screen support, but lack target-resolved genetics and clean
  modality/direction.
- Activating Fc receptors (`FCGR2A`, `FCGR3A`, `FCGR3B`, `FCGR1A`) and shared
  adaptors (`FCER1G`, `TYROBP`) are blocked by direction and host-defense
  safety.
- TAM receptors (`MERTK`, `AXL`) remain biologically plausible resolution
  comparators, but local MS anchoring, agonist modality, and prior-art/direction
  issues block promotion.

## Reproducibility

- Script: `scripts/v3_wave103_fc_receptor_efferocytosis_route_audit.py`
- Rank table: `results_v3/wave103_fc_receptor_efferocytosis_route_audit/fc_efferocytosis_route_rank.tsv`
- Summary: `results_v3/wave103_fc_receptor_efferocytosis_route_audit/summary.json`
- Seed: `20260527`
