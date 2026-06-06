# TREM2

Status: demoted  
V4/V5 tier: Tier 0 failed  
Last updated: 2026-05-28 20:45 CEST

## V3 History

V3 treated TREM2 as crowded microglia/neurodegeneration prior art and did not
fully separate agonism, shedding modulation, ligand biology, and stratification.

## V4 Recalibration Question

Can TREM2 be reframed as a remyelination/progressive-MS subgroup or modality
specific claim not equivalent to Alzheimer's-style microglial activation?

## Current V4 Contribution

None as an active therapeutic target nomination.

TREM2 remains useful as:
- a repair-biology comparator for microglial lipid/debris-clearance states,
- a possible CSF soluble TREM2 or lesion-rim stratification/readout axis,
- and a perturbation dataset source for testing repair-versus-activation
  directionality.

It does not re-enter Tier 0 as a V4 therapeutic candidate because V3's failure
was not merely a prior-art problem. The unresolved barriers are target-resolved
causal support, perturbation/foundation-model alignment, and separation of
beneficial repair from chronic lipid-loaded activation, shedding/sTREM2 biology,
and marker-only microglial abundance.

## V4 Recalibration Verdict

Verdict 3: evidence-driven demotion holds.

TREM2 is not `P0 target-invalidated`: locally cached AL002 Alzheimer trials and
TREM2 agonist precedent are different indications and do not equal a failed
progressive-MS/remyelination-enriched trial with adequate CNS target engagement.
But the candidate still fails V4 active status because the therapeutic claim is
not direction-resolved or causally anchored.

## Evidence Ledger

- `phases/v3/results/wave32_resolution_rescue_audit/resolution_rescue_route_audit.tsv`:
  `TREM2_APOE_LIPID_REPAIR` was the only parked downstream-resolution branch,
  but failed coupling, causal/perturbation, prior-art/nonblocking, and
  independent-validation gates.
- `phases/v3/results/wave32_resolution_rescue_audit/resolution_rescue_gate_matrix.tsv`:
  the route passed MS-anchor and modality-plausibility gates but failed
  causal/perturbational and independent-validation gates.
- `phases/v3/results/wave52_remaining_mechanistic_reopeners/decision_matrix.tsv`:
  passed cross-autoimmune breadth and cell-state replication but failed
  target-specific MS anchor, target-resolved genetics/coloc,
  perturbation/foundation alignment, safe direction, and novelty delta.
- `phases/v3/results/cross_disease_gene_convergence.tsv`: weak/null gene-level
  cross-disease signal; MS white-matter microglia delta 0.190, p 0.613, FDR
  0.793 in V3 output.
- `phases/v3/results/wave32b_dataset_availability_scan/candidate_dataset_matrix.tsv`:
  usable perturbation datasets exist (`GSE302857`, `GSE66926`, `GSE70475`,
  `GSE65067`), but V3 did not convert them into a validated direction-resolved
  target claim.
- `phases/v3/results/wave32c_resolution_prior_art_audit/raw_api/clinicaltrials__TREM2_agonism__AL002.json`:
  locally cached AL002 TREM2 agonist precedent, including `NCT03635047`,
  `NCT04592874`, and `NCT05744401`; crowding/modality context but not
  target-invalidating for MS under V4.

## Next Tier 0 Test

Do not reopen generic TREM2 agonism.

Allowed future re-entry test:
- Run a route-split perturbation audit using `GSE302857`, `GSE66926`, and
  `GSE70475`.
- Compare Trem2 loss versus WT during cuprizone demyelination/recovery for
  predefined modules: `repair_lipid_clearance`, `myelin_debris_phagocytosis`,
  `HLAII_APC`, `generic_IFN`, and `stress`.

Reopen only if Trem2 perturbation shows a consistent repair/lipid-clearance
effect in at least two datasets, with direction separable from generic
activation/stress and a measurable biomarker route such as CSF sTREM2 or
lesion-rim TREM2-high microglia.

## V5 Recalibration: TREM2 Agonism In MS

Requested scope: TREM2 agonism in MS specifically, treated as distinct from
Alzheimer's AL002 prior art.

### V5 Prior-Art Standard Applied

Prior-art grade: `P2 adjacent prior art`.

AL002/TREM2 agonist precedent is not target-invalidating for this V5 question.
The locally cached ClinicalTrials.gov artifact
`phases/v3/results/wave32c_resolution_prior_art_audit/raw_api/clinicaltrials__TREM2_agonism__AL002.json`
lists AL002 as a biological intervention in healthy volunteer/Alzheimer disease
contexts, including Alzheimer disease browse terms. That is not the same
indication, not the same patient subgroup, and not a progressive-MS or
remyelination-enriched trial with adequate CNS/lesion-rim target engagement.

Therefore the V3/V4 prior-art objection does not by itself demote TREM2
agonism under V5. The demotion must stand or fall on evidence and direction.

### Candidate V5 Contribution

The only defensible V5 contribution would be:

TREM2 receptor agonism, or agonist-biased enhancement of the TREM2-APOE lipid
repair state, for a biomarker-defined progressive-MS subgroup with high
lesion-rim lipid/debris-clearance demand and a measurable CSF or imaging
readout such as soluble TREM2, lesion-rim myeloid activity, or a
TREM2/APOE/LPL/GPNMB repair-state signature.

This contribution would be new relative to AL002 Alzheimer's prior art because
it changes indication, target tissue context, subgroup definition, and
therapeutic endpoint. It is not a generic "TREM2 is interesting in microglia"
claim.

### V5 Tier 0 Verdict

Verdict: **demotion holds at Tier 0 for evidence-driven reasons, not for
AL002/prior-art reasons.**

Reason:
- The V5 contribution is explicit, but no new V5 support channel has been added
  beyond the V3/V4 baseline.
- V3 local gates support TREM2/APOE lipid-repair biology broadly, but not a
  target-resolved MS therapeutic claim:
  `phases/v3/results/wave52_remaining_mechanistic_reopeners/decision_matrix.tsv`
  marked `TREM2_APOE_LIPID_REPAIR` as passing cross-autoimmune breadth and
  cross-dataset cell-state replication, while failing target-specific MS
  anchor, target-resolved genetics/coloc, foundation plus real perturbation
  alignment, and safe/selective direction resolution.
- The route-split V3 audit
  `phases/v3/results/wave32_resolution_rescue_audit/resolution_rescue_gate_matrix.tsv`
  called `TREM2_APOE_LIPID_REPAIR` `PARK_RESOLUTION_BIOLOGY_NO_CAUSAL_ANCHOR`.
  It passed MS-anchor and correct-direction-modality gates, but failed
  state-coupling-not-density-only, genetic-or-real-perturbation-anchor, and
  independent-validation gates.
- V5 Tier 0 requires at least one support channel beyond the V3 baseline. This
  recalibration found none locally.
- Correct-direction agonism remains biologically ambiguous: enhancing TREM2 may
  improve lipid/debris clearance and repair, but may also expand or preserve a
  chronic lipid-loaded activation state. The current local evidence does not
  separate repair-promoting agonism from abundance/state-marker behavior or
  generic microglial activation.

### Searches And Evidence Used

No new internet search was used for this V5 recalibration. The update used
local verified artifacts only:
- `meta/PRIOR_ART_RULEBOOK.md`
- `meta/TIERING_RULEBOOK.md`
- `meta/CURRENT_STATUS.md`
- `phases/v3/results/wave52_remaining_mechanistic_reopeners/decision_matrix.tsv`
- `phases/v3/results/wave32_resolution_rescue_audit/resolution_rescue_gate_matrix.tsv`
- `phases/v3/results/wave32b_dataset_availability_scan/candidate_dataset_matrix.tsv`
- `phases/v3/results/wave32c_resolution_prior_art_audit/raw_api/clinicaltrials__TREM2_agonism__AL002.json`

### Re-Entry Criteria

Do not reopen generic TREM2 agonism.

Re-enter Tier 0 only if at least one of the following is produced:
- A real perturbation analysis from `GSE302857`, `GSE66926`, or `GSE70475`
  showing that Trem2 loss specifically impairs lipid/debris-clearance or
  remyelination-repair modules while not simply lowering generic activation,
  stress, IFN, or HLA-II/APC modules.
- A progressive-MS lesion or CSF dataset showing TREM2-high biology predicts
  repair failure or progression after controlling for microglial/macrophage
  abundance and lesion stage.
- A modality-specific agonism rationale that separates productive TREM2
  signaling from shedding/sTREM2, TYROBP inflammatory amplification, and
  chronic lipid-loaded lesion-rim persistence.

If such evidence appears, the next Tier 1 test should be route-split rather
than gene-level: compare `repair_lipid_clearance`,
`myelin_debris_phagocytosis`, `TREM2_APOE_LPL`, `HLAII_APC`, `generic_IFN`,
and `stress` modules across Trem2 loss, recovery, and agonist-like contexts.
