# V36 Updated Ranking After Multiplicity Stress Test

Status: **completed_false_positive_control_update**.

## Key Change

The V36 exact max-AUC null found that after scanning 76 generated features in
n=9, perfect feature AUCs are common under label permutation. Therefore:

- V36-derived perfect-AUC compartment/substate features are exploratory only.
- The pre-specified V22/V23 monitoring rule remains distinct from the V36
  post-hoc feature search, but it still needs external validation.

## Current Ranking

| Rank | Item | Status After Multiplicity Control |
|---:|---|---|
| 1 | Immutable V22/V23 bounded monitoring rule | Still the primary validation target because it was pre-specified/locked before V36 feature search; provisional pending external validation and V36 confounder/QC audits. |
| 2 | V36 early W8 broad IFN/APC/STAT1 treated-state readout | Useful mechanistic/interpretive refinement, but exploratory because it emerged from post-hoc feature searches in n=8-9. |
| 3 | T/B and B/plasma compartment readouts | Secondary readouts only; not independent mechanisms and vulnerable to composition/QC/STAT1-axis caveats. |
| 4 | B/plasma/plasma-like substate IFN/APC | Supports within-substate remodeling over simple fraction artifact, but exploratory and globally STAT1-axis dependent. |
| 5 | Glycolysis/metabolic coupling | Coupled context only; not independent after IFN/STAT residualization. |
| 6 | Postpartum APC-arm imbalance | Data-acquisition hypothesis; no MS postpartum validation. |

## Practical Consequence

The next human-facing ask should not be "validate the B/plasma feature." It
should be:

Validate the locked V22/V23 early-treatment monitoring rule in Gafson or another
fresh cohort, while pre-specifying V36 secondary audits for timing, STAT1-axis,
glycolysis, compartments, B/plasma substates, and QC/batch covariates.
