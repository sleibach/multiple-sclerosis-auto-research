# TYK2

Status: demoted  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V5 Recalibration - Allosteric TYK2 / Deucravacitinib-Class Route

V5 question: can TYK2 re-enter Tier 0 specifically as an allosteric
deucravacitinib-class approach in MS, Sjogren's, or another autoimmune
indication where this modality has not been directly tested?

Verdict: **demotion holds for V5 Tier 0**.

This is not a `P0 target-invalidating` verdict. I did not find an equivalent
allosteric TYK2 intervention that failed mechanistically in MS with adequate
target engagement. The demotion holds because the V5 contribution is still not
specific enough and the local evidence does not add a new MS, subgroup,
pregnancy/postpartum, or lipid-lysosomal-cell-state anchor beyond generic
JAK/IFN/TYK2 biology.

### V5 Contribution Assessment

Potential V5 contribution considered:

- New modality: allosteric/JH2 TYK2 inhibition rather than pan-JAK inhibition.
- New indication: MS or other autoimmune indications not directly tested with
  deucravacitinib-class drugs.
- New subgroup: TYK2/IL-12/23/type-I-IFN-high patients, ideally separated from
  generic inflammatory burden and from HLA-II/IFN/APC modules.

Assessment:

- The modality contribution is weak because deucravacitinib-class allosteric
  TYK2 inhibition is already the defining clinical modality, not a new V5
  invention.
- The Sjogren's contribution is occupied by current clinical development:
  ClinicalTrials.gov query `deucravacitinib Sjogren` returned `NCT05946941`,
  a Phase 3 randomized placebo-controlled study in active Sjogren's syndrome,
  status `ACTIVE_NOT_RECRUITING`, enrollment `774`, last update posted
  `2026-04-01`.
- The MS contribution remains theoretically open but fails Tier 0 because V3/V4
  local evidence did not identify an MS-specific TYK2 cell-state, perturbation,
  pregnancy, postpartum, progressive-MS, or lipid-lysosomal-myeloid subgroup
  signal. Prior screens repeatedly classified TYK2 as a broad JAK/IFN positive
  control rather than a candidate with a new MS mechanism.
- Other untested autoimmune indications are not enough by themselves. Under the
  V4 prior-art standard, "not yet tested in disease X" is a possible opening,
  but Tier 0 still requires at least one supporting evidence channel beyond the
  V3 baseline. No such disease-specific contribution was identified in this
  recalibration.

### V5 Tier 0 Decision

Decision: **do not re-enter Tier 0 as an active V5 candidate**.

Reason: the only credible surviving claim is generic allosteric TYK2 inhibition
in autoimmune disease, and that is a crowded, clinically active class. The V5
standard would allow re-entry for a biomarker-defined subgroup or a new
disease-stage mechanism, but this audit found no local evidence supporting such
a subgroup in MS or in the current pregnancy/postpartum lead.

Prior-art grade: **P1 high crowding**, not `P0 target-invalidating`.

What would change this verdict:

- A dataset showing that baseline TYK2/IL-12/23/STAT4 activity predicts response
  or nonresponse to a TYK2/JAK-pathway perturbation after adjustment for generic
  IFN, HLA-II, TNF/NF-kB, and inflammatory-burden covariates.
- MS-specific longitudinal or natural-experiment evidence showing TYK2-axis
  activity temporally precedes relapse, postpartum flare, lesion expansion, or
  progression independently of the broad IFN/APC module.
- A treatment-by-biomarker result in MS, Sjogren's, SLE, psoriasis, IBD, or
  another autoimmune disease showing that a TYK2-high subgroup has a materially
  different therapeutic effect under allosteric TYK2 inhibition.

### V5 Verified Searches

Searches run on 2026-05-28:

- Local sparse RAG query:
  `./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "TYK2 deucravacitinib allosteric MS Sjogren V5 prior art recalibration" 12`.
  Top hits were this file, `meta/ROADMAP_V5.md`,
  `meta/CONVERGENCE_CHECK_V5_01.md`, `meta/CURRENT_STATUS.md`, and
  `phases/v3/subagents/wave11_genetics_prior_art_scout_report.md`.
- Local text search:
  `rg -n "TYK2|deucravacitinib|BMS-986165|Sotyktu|allosteric" knowledge meta subagents phases/v3/subagents phases/v3/results analysis results scripts`.
  This recovered the V3 genetics, perturbation, OpenTargets, and prior-art
  records summarized below.
- ClinicalTrials.gov API:
  `deucravacitinib multiple sclerosis` -> no returned studies.
- ClinicalTrials.gov API:
  `TYK2 multiple sclerosis` -> no returned studies.
- ClinicalTrials.gov API:
  `deucravacitinib Sjogren` -> `NCT05946941`, Phase 3 active Sjogren's
  syndrome trial.
- ClinicalTrials.gov API:
  `deucravacitinib` -> crowded class/program landscape including psoriasis,
  psoriatic arthritis, SLE, cutaneous lupus, ulcerative colitis, Crohn's
  disease, Sjogren's syndrome, vitiligo, hidradenitis suppurativa, alopecia
  areata, myositis/dermatomyositis, Takayasu arteritis, and other inflammatory
  skin or systemic conditions.
- PubMed ESearch:
  `deucravacitinib multiple sclerosis` -> 6 records, inspected by ESummary;
  titles were review/computational/comorbidity/EAE-adjacent rather than a
  clinical MS trial of deucravacitinib.
- PubMed ESearch:
  `deucravacitinib Sjogren` -> 4 records, review-level or broad JAK/TYK2
  material in the returned titles, not a completed Sjogren's efficacy result.

## V3 History

V3 repeatedly ranked TYK2 highly by autoimmune genetics but demoted it as a
known/crowded autoimmune kinase axis without an MS-specific contribution.

## V4 Recalibration Question

Can TYK2 be rescued by subgroup, combination, dose/signal-bias, or progressive
MS mechanism rather than generic TYK2 inhibition?

## Current V4 Contribution

None as an active V4 therapeutic target nomination.

The V4 prior-art rule rescues TYK2 from a simplistic "known target" kill, but
it does not rescue the candidate as currently evidenced. Generic TYK2 inhibition
is a useful positive control for autoimmune genetics and druggability, not a V4
finding. A future TYK2 branch would need a sharply defined biomarker subgroup,
combination, dose/signal-bias, or disease-stage claim that is not equivalent to
approved/crowded systemic TYK2 inhibition.

## V4 Recalibration Verdict

Verdict 3: evidence-driven demotion holds.

Prior-art grade: P1 high crowding, not P0 target-invalidating. Locally cached
trial/prior-art files show extensive TYK2 autoimmune development, but no
equivalent progressive-MS or MS biomarker-subgroup TYK2 intervention with
adequate target engagement that failed for target-mechanistic reasons. The
candidate remains demoted because V3 evidence did not produce a cell-state,
perturbation, or MS-specific mechanistic contribution beyond broad JAK/IFN
pathway suppression.

## Evidence Ledger

- Sparse-index query run before recalibration:
  `./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "TYK2 V4 prior art subgroup combination autoimmune" 10`.
  Top hits were `knowledge/candidates/TYK2.md`,
  `knowledge/candidates/LRRK2.md`, `meta/PRIOR_ART_RULEBOOK.md`,
  `knowledge/candidates/LTA4H.md`, and `phases/v3/subagents/wave11_genetics_prior_art_scout_report.md`.
- `phases/v3/subagents/wave11_genetics_prior_art_scout_report.md`: TYK2 was called
  the strongest cross-autoimmune genetic comparator, with literature links for
  TYK2 coding/common variants across MS, SLE, Crohn, UC, psoriasis, RA, T1D,
  and IBD, but the hard call was "blocked positive control" rather than novel
  intervention.
- `phases/v3/results/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`:
  TYK2 ranked high in a genetics-first target scan (`genetics_first_score`
  19.65, 36 GWAS Catalog trait count, 7 OpenTargets diseases score >= 0.5:
  AITD, Crohn, PBC, psoriasis, RA, SLE, T1D), but was called
  `DEMOTE_PRIOR_ART_BLOCKED` and had no new local cell-state or perturbation
  delta.
- `phases/v3/results/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`:
  TYK2 was `PARK_GENETIC_DRUGGABLE_NEEDS_CELL_STATE`; failed
  `gate_local_cell_state`, `gate_perturbation_or_model`, and
  `gate_not_prior_art_blocked`; MS anchor was false.
- `phases/v3/results/wave62_opentargets_target_resolution/target_resolution_summary.tsv`:
  TYK2 had cross-disease L2G/QTL breadth but failed MS L2G, MS-relevant QTL,
  module-link, manual-blocker, and prior-context gates; call
  `NO_GO_WAVE62_TARGET_RESOLUTION`; blocker class
  `prior_art_autoimmune_kinase_class` / `generic_JAK_STAT_axis`.
- `phases/v3/results/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`:
  TYK2 was `NO_GO_PERTURBATION_FIRST_BLOCKED`, with support only in psoriasis
  and T1D, no MS positive disease count, and blocker
  `JAK/IFN broad immunosuppression/prior art`.
- `phases/v3/results/wave81_perturbation_first_rescue/perturbation_first_wave15_rows.tsv`:
  direct perturbation evidence classified TYK2 as
  `broad_ifn_jak_like_collapse` and `comparator_only_broad_ifn_jak_collapse`.
- `phases/v3/results/wave166_same_gene_genetics_cellstate_overlap/same_gene_genetics_cellstate_rank.tsv`:
  TYK2 failed same-gene genetics/cell-state overlap because of insufficient MS
  genetic anchor and prior/local no-go blocker.
- `phases/v3/results/wave34a_genetics_first_target_rescue/raw_api/clinicaltrials_TYK2.json`
  and `phases/v3/results/wave34a_genetics_first_target_rescue/raw_api/europepmc_TYK2.json`:
  local API cache records 17 ClinicalTrials.gov matches and 6839 Europe PMC
  hits for TYK2 autoimmune/MS-adjacent queries, documenting crowding but not a
  P0-equivalent MS subgroup failure.

## Next Tier 0 Test

Do not reopen generic TYK2 inhibition.

Allowed future re-entry test:
- Define a biomarker-specific TYK2 branch, for example high IL-12/23/TYK2/STAT4
  genetic-risk plus active Th1/Th17/APC state, and explicitly separate it from
  broad IFN/JAK suppression.
- Test whether baseline TYK2/IL-12/23/STAT4 axis activity predicts response or
  nonresponse in psoriasis, PsA, IBD, SLE, or MS trial/real-world cohorts where
  TYK2 or adjacent JAK-pathway treatment data are available.
- Require the TYK2 signal to add predictive value beyond generic IFN, HLA-II,
  TNF/NF-kB, and inflammatory burden covariates.
- Require at least one MS-relevant natural-experiment or longitudinal signal
  before any progressive-MS claim.

Pass Tier 0 only if a non-equivalent contribution emerges: a biomarker-defined
subgroup, combination partner, dose/signal-bias strategy, or disease-stage
claim with evidence not explained by generic JAK/IFN pathway inhibition.
