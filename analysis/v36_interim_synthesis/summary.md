# V36 Interim Synthesis After Lead Refactoring

Status: **completed_interim_ranked_slate_update**.

## Main Evidence Shift

V36 started with the T/B compartment remodeling gate as the current top lead.
The resumed block sharpened and then partially demoted that framing:

1. B/plasma and T-cell readouts remain internally strong in `GSE253006`.
2. B/plasma IFN/APC is not explained by the W48 responder or one removable
   patient.
3. STAT1 and IFN/STAT downshift are not B/plasma-specific; they are broad across
   compartments.
4. B/plasma IFN/STAT loses signal after myeloid IFN/STAT residualization.
5. Compartment locked scores collapse after delta STAT1-axis residualization,
   but not after glucocorticoid residualization.
6. Baseline IFN/APC is weak/null; treated IFN/APC and delta dominate.
7. W8 is the only interpretable post-baseline timepoint in held data.
8. Lightweight B/plasma substate audit argues against simple B/plasma substate
   fraction artifact.

## Current Best Wording

The top V36 lead is now:

**An early W8 on-treatment IFN/APC/STAT1-axis monitoring state, broadly
cross-compartmental and readable in T/B compartments, not a baseline subtype,
not glucocorticoid-explained in held scores, not B/plasma-specific, and still
single-cohort/unreplicated.**

## Re-Ranked Slate

| Rank | Hypothesis | Current V36 status | What would move it forward |
|---:|---|---|---|
| 1 | Early W8 IFN/APC/STAT1-axis monitoring state | internally strongest; broad cross-compartment signal; T/B readouts useful but not mechanistically independent | independent paired response cohort with baseline + W8-like sample, response labels, steroid/STAT1/confounder panels, and compartment or cell-level readouts |
| 2 | B/plasma/plasma-like within-substate IFN/APC remodeling | supported as within-substate readout, not fraction artifact; not independent from global STAT1/myeloid axis | replicate within B/plasma substates in independent cohort and test myeloid residualization |
| 3 | T-cell IFN/APC readout | strongest raw AUC but composition-sensitive and STAT1-axis dependent | replicate with T-cell subset/fraction adjustment |
| 4 | Postpartum HLA-II/CD64 APC-arm imbalance | clinically anchored, but MS postpartum relapse-window data absent | postpartum MS blood/CSF cohort with relapse timing and confounder metadata |
| 5 | Metabolic/sterol and lysosomal APC variants | context/proposal only; no bottleneck or direction-matched intervention proof | APC/PVM lipid flux or HLA-peptidomics perturbation data |
| 6 | EBV/IFN APC imprint and complement/lipid progressive axis | not supported with held data | revive only with EBV-stratified B/APC data or donor-aware lesion-rim spatial lipid/complement data |

## Next Executable Items

1. Test whether W8 treated IFN/APC remains strong after subject-level
   confounder residualization, not only compartment locked-score residualization.
2. Compare broad treated IFN/APC against non-IFN modules from V32 in the exact
   tofacitinib cohort, to ensure W8 treated-state specificity.
3. Run a focused Claude/Gemini cross-exam on the new wording to identify any
   remaining executable falsification tests.
