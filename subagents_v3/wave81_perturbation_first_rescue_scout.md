# Wave81 Perturbation-First Rescue Scout

Returned: 2026-05-27

Role: hostile sidecar audit over existing V3 perturbation/model artifacts. This
report makes no finding claim and edits no code.

## Inputs Read

- `CONVERGENCE_CHECK_40.md`
- `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
- `subagents_v3/wave15_perturbation_drug_response.md`
- `subagents_v3/wave15_prior_art_feasibility.md`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/REPORT.md`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/candidate_gene_screen_scores.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/REPORT.md`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
- `results_v3/wave69d_gse282122_geneformer_remission_centroid/REPORT.md`
- `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_candidate_calls.tsv`
- `results_v3/wave62_opentargets_target_resolution/REPORT.md`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_gate_matrix.tsv`
- `results_v3/wave71_global_survivor_meta_rank/REPORT.md`
- `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`

## Hostile Bottom Line

No candidate in the specified artifacts has all four rescue properties:

1. real perturbation or foundation-model support;
2. cross-autoimmune and/or MS anchor;
3. non-conflicted therapeutic direction;
4. feasible modality.

The least-bad rescue candidate is `IL7R`, but only as a comparator or narrowly
bounded falsification lead. It combines Geneformer support and strong MS/cross-
autoimmune genetics, but the CD127 axis is prior-art blocked and directionally
nontrivial. `CXCR2` has model and druggability appeal but lacks an MS anchor.
`GSK3B` has the best druggable-ish direct perturbation signal but lacks
target-resolved autoimmune genetics and is too pleiotropic. `TNFRSF1A` has
direct perturbation plus MS genetics but is directionally unsafe for an MS
therapeutic claim. `RFX5` and `MED16` are useful mechanistic controls, not
therapeutic targets.

## Rescue Gate Matrix

| Candidate | Perturbation/model support | Cross-autoimmune/MS anchor | Direction | Modality | Hostile disposition |
|---|---:|---:|---:|---:|---|
| `IL7R` | PASS model | PASS genetics | FAIL/PARTIAL | PARTIAL | Least-bad, but prior-art and directionality blocked. |
| `CXCR2` | PASS model | PARTIAL, no MS | PARTIAL/FAIL | PASS | Park outside MS; chemokine recruitment is not a demonstrated transition-controller. |
| `GSK3B` | PASS direct perturbation | FAIL | FAIL/PARTIAL | PASS but broad | Keep as upstream controller scout only if substrate-selective route emerges. |
| `TNFRSF1A` | PASS direct perturbation | PASS MS genetics | FAIL | PASS | Do not rescue; MS paradox and TNF prior art dominate. |
| `RFX5` | PASS weak direct perturbation | FAIL | PARTIAL | FAIL | Readout/genetic-gate control, not druggable. |
| `MED16` | PASS strong direct perturbation | FAIL | PARTIAL | FAIL | Strong mouse comparator, not druggable. |
| `FCGR2A` | PASS model | PARTIAL, no MS | FAIL | PARTIAL | Fc directionality and safety block. |
| `NCF1` | PARTIAL model | FAIL/PARTIAL | FAIL | PARTIAL | NADPH oxidase host-defense/CGD direction risk. |
| `CD80` / `CD274` | PASS model | PARTIAL | FAIL | PASS | Costimulation/checkpoint biology is crowded and safety-conflicted. |
| `JAK1` / `JAK2` / `SYK` / `SRC` | PASS model for some | PARTIAL | FAIL | PASS | Broad established immunosuppression/comparator biology. |
| `PRKDC` / `BLK` | FAIL current model support | PARTIAL | UNKNOWN | PASS | Chemistry exists, but no rescue evidence in current artifacts. |
| `CTSB` / `ASAH1` | PARTIAL model | FAIL | PARTIAL/FAIL | PARTIAL | Lysosomal/cathepsin-family signals remain nonspecific and prior-art exposed. |

## Least-Bad Shortlist

### 1. `IL7R` / CD127

Why it survives longest:

- Wave57 reopened it as `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST`.
- Wave57 model metrics: one support context and one strong support context,
  best context `ra_myeloid_dendritic`, best cosine-shift z `0.529`,
  projection-minus-random `0.0318`, model priority score `7.25`.
- Wave69d independently marked it as model-supported in IBD remission geometry:
  `MODEL_SUPPORT_BUT_BLOCKED_COMPARATOR`, best context
  `GSE282122_DC_post_nonremission_to_remission_UC_only`, cosine-shift z
  `1.348`, projection-minus-random `0.0621`, priority score `7.5`.
- Wave62 genetics are unusually strong: wave62 score `6.447`,
  max L2G `0.953` in PBC, strong L2G in `Crohn;MS;PBC;T1D`,
  MS L2G `0.945`, MS relevant QTL H4 `0.984`, local positive disease count
  `3`, residual-retained disease count `2`.

Why it still should not be promoted:

- Wave62 manual blocker is `prior_art_CD127_autoimmune_axis`.
- Wave69d manual blocker is also `prior_art_CD127_autoimmune_axis`.
- Wave71 demotes it as `PARK_PRIOR_ART_OR_HOST_DEFENSE_PENALIZED`, with
  blocker text including `prior_art_CD127_autoimmune_axis`.
- The current evidence is model/association heavy. No direct measured human
  CD127 perturbation in these artifacts shows selective normalization of the
  lipid-lysosomal myeloid module.
- Direction is not clean. CD127 modulation can affect effector T cells,
  memory T cells, and regulatory/tolerance compartments; the artifacts do not
  define whether inhibition, agonism, depletion, or cell-state stratification is
  the correct therapeutic move.

Disposition: retain only as a comparator and as a possible stratification/
falsification lead. Do not use as the V3 therapeutic target.

### 2. `CXCR2`

Why it survives:

- Wave57 reopened it as `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST`.
- Wave57 model metrics: one support context and one strong support context,
  best context `IBD_myeloid`, cosine-shift z `1.197`,
  projection-minus-random `0.0288`, model priority score `7.25`.
- Wave57 gives cross-disease genetics above threshold in
  `AS;Crohn;Psoriasis;RA;UC` and local positive diseases
  `Crohn disease;psoriasis;ulcerative colitis`.
- A receptor/chemokine axis is in principle more tractable than intracellular
  transcriptional controls.

Why it fails:

- MS anchor is absent in Wave57 (`ms_genetic_association` `0.0`) and Wave62
  (`ms_max_l2g_score` `0.0`, `ms_max_relevant_qtl_h4` `0.0`).
- Wave62 call is `NO_GO_WAVE62_TARGET_RESOLUTION`, despite local positive
  disease count `3`.
- MS white-matter expression is not significant in Wave57:
  delta `0.830`, p `0.378`, FDR `0.914`.
- Wave71 marks it `PARK_PRIOR_ART_OR_HOST_DEFENSE_PENALIZED`; blocker text says
  the chemokine recruitment route is not a demonstrated transition-controller
  and lacks V3 immune-cell selectivity.

Disposition: plausible non-MS inflammatory comparator; not an MS/cross-
autoimmune rescue target for V3.

### 3. `GSK3B`

Why it survives:

- Wave15 identifies `Gsk3b_KO` as the strongest druggable-ish direct
  perturbation comparator: target module suppression `1.622`, target-vs-IFN
  margin `0.827`, selectivity score `0.778`.
- Wave15 source support spans mouse macrophage CRISPR screen and mouse
  macrophage RNA-seq.
- Wave69d lists ChEMBL activity for `GSK3B` and a high controller score
  (`17.333`), so the target class is chemically reachable.

Why it fails:

- Wave15 itself calls it `candidate_evidence_not_enough_to_nominate_drug`.
- Wave69d call is `NO_GO_MODEL_REMISSION_SCREEN`; support contexts `0`,
  strong support contexts `0`, priority score `0.0`.
- Wave69d manual blocker is `GSK3_family_pleiotropic_neuroimmune_metabolic`.
- Wave71 reports no target-resolved coloc/MR, no supplied Open Targets disease
  locus evidence, and no broad genetics/module-state convergence; meta score
  `-2.9`.
- The direct perturbation is mouse KO, not selective human chemical
  perturbation with disease-response validation.

Disposition: keep as a mechanistic upstream-controller scout only if a future
analysis finds a substrate-, compartment-, or cell-delivery-selective modality.
Do not nominate pan-GSK3B modulation.

### 4. `TNFRSF1A`

Why it survives:

- Wave15 Mixscale CRISPRi gives selective target suppression: target module
  suppression `0.968`, target-vs-IFN margin `0.662`, selectivity score `0.621`.
- Wave62 gives very strong MS target-resolution genetics: MS L2G `0.954`,
  MS relevant QTL H4 `0.9998`, strong L2G diseases `AS;MS;PBC`.

Why it fails hard:

- Wave62 manual blocker is `TNF_axis_prior_art_and_MS_paradox_risk`.
- Wave71 call is `PARK_PRIOR_ART_OR_HOST_DEFENSE_PENALIZED`; blocker text says
  TNF blockade is saturated and demyelination risk makes it unsuitable as an MS
  cure route.
- Wave62 local positive disease count is `0`, residual-retained disease count
  `0`; it is genetics/perturbation anchored but not locally aligned with the
  module.

Disposition: do not rescue. This is a warning signal, not a therapeutic lead.

### 5. `RFX5` and `MED16`

Why they matter:

- `RFX5` CRISPRi in Wave15 gives selective MHC-II/antigen-presentation
  suppression: target suppression `0.552`, margin `0.552`, selectivity score
  `0.523`.
- `Med16_KO` is the strongest direct perturbation control in Wave15:
  target suppression `3.140`, margin `2.342`, selectivity score `2.305`.

Why they fail:

- `RFX5` is a transcriptional MHC-II gate, not a realistic chronic therapeutic
  target from these artifacts.
- `MED16` is a strong mouse mechanistic comparator but not a druggable
  intervention point.
- Wave71 reports both as `NO_REOPEN_INSUFFICIENT_CONVERGENCE`, with missing
  target-resolved genetics, module-state convergence, and/or modality gates.

Disposition: use as assay positive controls for antigen-presentation
suppression. Do not nominate.

## Comparator Bucket: Model Support But Blocked

Wave69d contains several model-supported remission-direction candidates whose
main value is to stress-test the gate logic:

- `FCGR2A`: priority `9.75`, strong model context, but manual blocker
  `Fc_receptor_directionality_and_safety`; Wave62 has no MS anchor.
- `JAK1` and `JAK2`: model support and large ChEMBL activity counts, but
  `generic_JAK_STAT_axis_prior_art_host_defense`; Wave15 shows JAK/IFN collapse
  is not selective.
- `CD80` / `CD274`: model support, but costimulation/checkpoint direction and
  autoimmune safety are not clean.
- `NCF1`: three support contexts in Wave69d but no strong support; blocker is
  `NADPH_oxidase_host_defense_CGD_directionality_risk`.
- `SRC` / `SYK`: chemically tractable, but broad kinase/Fc signaling prior-art
  and safety blockers dominate.

None of these should be converted into a V3 finding without a new selective
modality and a non-conflicted disease-specific direction.

## Specific Non-Starters

- `PRKDC` and `BLK`: Wave69d keeps them only as
  `PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION`; both have zero
  support contexts and zero strong support contexts in the remission model
  table.
- `CTSB`: Wave57 has model signal in IBD/psoriasis contexts, but Wave62 is
  `NO_GO_WAVE62_TARGET_RESOLUTION`, MS L2G is `0.0`, and Wave37 efferocytosis
  evidence is `UNRESOLVED` with contrast FDR `0.920`.
- `ASAH1`: broad model contexts but no genetics block is even filled in the
  Wave57 row; negative diseases include Crohn and UC, so direction is not
  coherent.
- `SP140`, `GALC`, `STAT4`: genetics/state-interest candidates, but the
  specified perturbation/model outputs do not rescue them. Wave57 marks them
  `NO_GO_MODEL_SCREEN`.

## What Would Be Needed To Reopen A Candidate

Minimum reopener for `IL7R`:

- Direct human perturbation in disease-relevant APC/myeloid or T-cell context,
  not only Geneformer delete-token prediction.
- Direction-resolved readout showing whether CD127 blockade, agonism, or
  stratification normalizes the disease-associated state without erasing
  tolerance/repair programs.
- Prior-art delta that is narrower than generic CD127 autoimmunity.

Minimum reopener for `CXCR2`:

- MS-relevant genetic or lesion-cell-state anchor.
- Demonstration that CXCR2 perturbation alters a transition-controller state,
  not merely neutrophil/chemokine recruitment.

Minimum reopener for `GSK3B`:

- Human-cell chemical perturbation with a selective antigen-presentation or
  lipid-lysosomal rescue effect.
- Disease genetic or causal anchor, or a cell-targeted/substrate-specific
  modality that avoids pan-GSK3 biology.

Minimum reopener for `TNFRSF1A`:

- A non-TNF-blockade direction that resolves the MS paradox. Current artifacts
  do not supply one.

## Decision

No perturbation-first rescue candidate is promotable from the specified
artifacts. The next orchestrator branch should not spend another cycle on
expression-ranked targets unless a candidate first arrives with direct human
perturbation plus target-resolved autoimmune genetics and an explicit
directionality solution.
