# CTSS

Status: demoted  
V4/V5 tier: Tier 0 closed for direct therapeutic targeting  
Last updated: 2026-05-28

## V3 History

V3 demoted CTSS/cathepsin biology as antigen-processing prior art with
host-defense and selectivity concerns.

## V4 Recalibration Question

Is there a compartment-specific or subgroup-specific CTSS contribution that is
not equivalent to broad antigen-processing inhibition?

## Current V4 Contribution

None as a direct intervention target.

CTSS remains useful as:
- a mechanistic comparator for antigen-processing-high APC states,
- a pharmacodynamic readout for upstream CIITA/MHC-II/CD74 modulation,
- and a possible stratification component with `CD74`, HLA-II, `IFI30`, and
  generic IFN/JAK markers.

It does not re-enter Tier 0 as a therapeutic target under V4 because the
demotion is not merely prior-art crowding. It is a combined evidence-driven
failure:

1. Equivalent or near-equivalent cathepsin S inhibition has already been tested
   in autoimmune indications with target engagement but without convincing
   clinical efficacy.
2. V3 mechanistic modeling placed CTSS downstream of the central IFN/HLA-II/APC
   state: modeled 70% CTSS suppression was essentially null on `IFN/APC` and
   `HLA-II/CD74`, while affecting only the lysosomal readout.
3. V3 genetics scans found weak/non-decisive disease genetics for CTSS relative
   to stronger comparator axes.
4. The route carries host-defense and antigen-processing risk without a clear
   repair-preserving or subgroup-specific therapeutic direction.

## V4 Recalibration Verdict

Verdict 3: demotion was evidence-driven and V4 prior-art recalibration does not
save direct CTSS intervention.

The V4 rulebook prevents killing targets merely because they are known. CTSS is
different: clinical studies directly tested the same target/direction class in
autoimmune disease. RO5459072/petesicatib in primary Sjogren's syndrome did not
produce clinically meaningful benefit despite soluble-biomarker evidence of
target engagement, and a celiac gluten-challenge study did not meet its primary
endpoint. This is close enough to a direct target-mechanistic challenge that any
new CTSS claim would need a sharply different contribution: local delivery,
different disease compartment, or biomarker-defined subgroup with evidence that
CTSS is upstream in that subgroup. V3 did not provide that evidence.

## Evidence Ledger

- `phases/v3/subagents/wave11_genetics_prior_art_scout_report.md`: CTSS had weak or
  non-decisive Crohn genetics and no broad genetic anchor; report lists
  Sjogren, celiac, RA, and psoriasis/autoimmune cathepsin-S clinical prior art.
- `phases/v3/subagents/wave13_genetics_prior_art_reopen.md`: CTSS retained as a
  prior-art-blocked enzyme comparator, not promoted.
- `phases/v3/results/wave16_ctsh_chembl_feasibility/cathepsin_activity_summary.tsv`:
  CTSS is druggable (`CHEMBL2954`, 3,171 reported activities, 1,333 unique
  molecules in retained rows, median potency 206 nM, 594 sub-100 nM rows), so
  lack of chemistry is not the blocker.
- `phases/v3/results/wave46_central_axis_closure_audit/` and
  `docs/lab_notebooks/LAB_NOTEBOOK_V3.md`: `CTSS_cathepsinS_lysosomal_effector` closed as
  `NO_GO_CTSS_PRIOR_ART_DOWNSTREAM_EFFECTOR`; modeled 70% CTSS suppression was
  essentially null on upstream `IFN/APC` and `HLA-II/CD74`.
- PubMed/PMC verified celiac study: RO5459072 in 19 celiac participants under a
  gluten challenge did not meet the primary endpoint and concluded absence of
  clear effects, despite some pharmacodynamic hints
  (PMID 39739628, DOI 10.1111/cts.13901).
- PubMed/PMC verified Sjogren study: RO5459072 phase IIa in 75 participants
  showed no clinically relevant ESSDAI improvement and no secondary clinical
  benefit despite target engagement (ClinicalTrials.gov `NCT02701985`).

## Next Tier 0 Test

Do not run direct CTSS therapeutic Tier 0 unless a new V4 contribution is
defined first.

Allowed future use:
- biomarker/readout test: ask whether `CTSS` adds predictive value to
  `CD74/HLA-DRA/IFI30` and generic IFN/JAK markers in treatment-response or
  natural-experiment datasets;
- subgroup rescue test: reopen only if a dataset shows a CTSS-high subgroup
  where CTSS is upstream of tissue damage or treatment resistance after
  adjusting for broad APC/IFN state.

Advance criterion for any future reopening:
- at least one longitudinal, natural-experiment, or perturbation dataset showing
  CTSS-specific predictive or causal signal beyond the broader antigen-
  processing module;
- a delivery or modality distinction from systemic CTSS inhibition;
- and a clear reason why RO5459072 failures in Sjogren/celiac do not apply.

## V5 Recalibration - Selective Lysosomal-pH-Conditional CTSS Inhibition

Question: does a more selective lysosomal-pH-conditional CTSS inhibitor create a
new V5 contribution that should re-enter Tier 0?

Verdict: **demotion holds for direct CTSS therapeutic targeting**.

V5 contribution assessed:

- **New modality proposed:** CTSS inhibition preferentially active in acidic
  lysosomal/APC compartments, potentially reducing extracellular or
  off-compartment cathepsin liabilities.
- **Potentially non-equivalent to prior art:** this could be chemically distinct
  from historical systemic CTSS inhibitors if it shows cellular lysosomal
  selectivity, disease-APC enrichment, and a safety window not achieved by
  RO5459072/petesicatib or RWJ-445380.
- **Why this does not rescue Tier 0 now:** the local project evidence does not
  show CTSS is upstream of the autoimmune lipid-lysosomal/APC state in MS or
  across the V5 target diseases. V3/V4 repeatedly classified CTSS as a
  downstream antigen-processing/lysosomal readout with weak MS white-matter
  anchoring and insufficient perturbation support.

This is not binary prior-art gating. The pH-conditional modality prevents the
older CTSS clinical failures from being fully target-invalidating (`P0`) by
itself. The demotion still holds because V5 Tier 0 requires a concrete
contribution plus at least one support channel beyond the V3 baseline. The
proposed modality supplies only the modality distinction. It does not supply new
disease biology, causal direction, subgroup definition, or perturbation
evidence.

Prior-art grade under V5:

- `P1/P2`: high crowding plus adjacent direct autoimmune clinical precedent.
  Prior CTSS inhibitors in Sjogren, celiac, and RA are not ignored, but they are
  not treated as a complete kill gate for a demonstrably different
  pH-conditional, subgroup-enriched, tissue-restricted strategy.
- No verified evidence in the local record that a directly equivalent
  lysosomal-pH-conditional CTSS inhibitor has failed in MS or a
  biomarker-defined CTSS-high autoimmune subgroup.

Evidence basis:

- `knowledge/decisions/0006_ctss_recalibration.md`: CTSS retained only as
  comparator/readout after V4 review.
- `phases/v3/results/wave91_lipid_lysosomal_module_intervention_rank/REPORT.md`:
  CTSS scored `4.5` with `NO_GO_NO_MS_WHITE_MATTER_SINGLE_GENE_ANCHOR`,
  `NO_GO_CATHEPSIN_S_PRIOR_AUDITED_HOST_DEFENSE_AND_PRIOR_ART`,
  `MS_WM_NULL_OR_WEAK`, direct positive signal only in Crohn disease and UC,
  no cross-disease genetic anchor, and `NO_GO_PERTURBATION_FIRST_BLOCKED`.
- `phases/v3/subagents/wave11_genetics_prior_art_scout_report.md`: CTSS had
  weak/non-decisive Crohn genetics and no broad genetic anchor; direct CTSS
  autoimmune prior art includes Sjogren, celiac, and RA.
- `phases/v3/subagents/wave15_prior_art_feasibility.md`: CTSS is chemically
  druggable but highly saturated; use as assay comparator unless a new
  subgroup/compartment/delivery mechanism is demonstrated.
- `phases/v3/results/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`:
  Ctss CRISPR/efferocytosis direction was unresolved, not a rescue signal.
- V4 pregnancy and V5 MIF/CD74 work continue to support antigen-processing
  module behavior, but not CTSS-specific causal control.

Tier 0 decision:

**Verdict 1: demotion holds.** The direct CTSS inhibitor program does not
re-enter the active V5 candidate queue. The modality idea is parked as a
possible chemistry rescue condition, not as a live therapeutic hypothesis.

What would promote CTSS to Tier 1:

1. A disease-relevant human dataset showing `CTSS` adds predictive or causal
   information beyond `CD74`, HLA-II, `IFI30`, IFN/JAK markers, and broad
   myeloid/APC abundance. Acceptable examples: progressive-MS lesion rim,
   postpartum-MS flare, treatment-resistance, or pre-diagnostic autoimmune
   samples.
2. A perturbation dataset in primary human APCs, microglia-like cells,
   macrophages, or tissue organoids showing selective CTSS inhibition moves a
   disease-relevant phenotype in the intended direction while preserving
   repair/efferocytosis. Required comparator controls: CTSS inactive analog,
   broader cathepsin inhibitor, CIITA/HLA-II perturbation, and IFI30/GILT
   perturbation.
3. Chemistry or chemical-biology evidence for the proposed V5 modality:
   lysosomal-pH-conditional activity, biochemical and cellular selectivity over
   CTSB/CTSL/CTSC/CTSH/CTSZ, and lysosomal target engagement in disease APCs at
   exposures below broad antigen-presentation suppression.
4. A subgroup definition that explains why prior systemic CTSS trials in
   Sjogren/celiac/RA do not apply. Minimal acceptable evidence: CTSS-high,
   HLA-II/CD74-adjusted subgroup with treatment-resistance or relapse-risk
   association in an independent dataset.

Until those conditions exist, CTSS should be used as:

- a pharmacodynamic readout for lysosomal antigen-processing state;
- a comparator against upstream APC-state interventions such as CIITA/Mediator
  kinase, MIF/CD74, IFI30/GILT, or macrophage lipid-handling programs;
- and a safety/selectivity counter-axis for any proposed lysosomal
  intervention.
