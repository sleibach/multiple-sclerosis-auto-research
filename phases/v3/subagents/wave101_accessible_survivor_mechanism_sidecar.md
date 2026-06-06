# Wave101 Sidecar: Accessible Survivor Mechanism and Directionality

Timestamp: 2026-05-27 Europe/Berlin

Scope: mechanism and directionality audit for `SEL1L3` versus `FXYD5`, with
`APOC1`, `CD82`, and `LAPTM5` as comparators. This sidecar does not claim a
finding.

## Inputs Read

- `results_v3/wave101_accessible_survivor_forcing_triage/accessible_survivor_forcing_rank.tsv`
- `results_v3/wave94_accessible_state_rerank/accessible_state_candidate_rank.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_candidate_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`

## Sidecar Verdict

Neither `SEL1L3` nor `FXYD5` currently has enough evidence to say it controls
the lipid-lysosomal inflammatory tissue state. `SEL1L3` is the cleaner forcing
candidate because it has the strongest Wave101 score and fewer directionality
contradictions, but its mechanism is mostly unknown and its support is still
expression-led. `FXYD5` has a more interpretable molecule-to-tissue hypothesis,
through adhesion and Na/K-ATPase coupling, but its Crohn negative context and
treatment-response direction conflict make it unsafe to pursue as a target
nomination. The immediate next step should be a residualized tissue-niche test,
not a new target claim.

## Candidate Mechanism Hypotheses

### SEL1L3

Local evidence:

- Wave101 call: `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR`.
- Wave101 score: `22.78`; gate count: `8`.
- MS white-matter signal: delta `0.9225`, p `0.01814`, FDR `0.8373`.
- Positive disease count in Wave101: `3`; positive diseases: Crohn disease,
  type 1 diabetes mellitus, ulcerative colitis.
- Best positive context: ulcerative-colitis stromal compartment, delta `2.09`,
  p `0.00104`.
- UniProt accessibility in local Wave101/W94 table: membrane, one
  transmembrane feature.
- Wave37 CRISPR efferocytosis screen: `UNRESOLVED`; contrast LFC `-0.1019`,
  FDR `1.0`.
- Wave18 foundation-model result: `do_not_promote_from_foundation_model`;
  one support context and one strong support context, model-only.
- Wave62 target-resolution result: `NO_GO_WAVE62_TARGET_RESOLUTION`; zero
  strong L2G diseases and zero strong QTL-colocalized diseases.

Molecule-to-cell-to-tissue hypothesis:

- Molecule: an undercharacterized membrane SEL1-repeat protein.
- Cell: disease-high stromal, endothelial, or epithelial niche cells may use
  `SEL1L3` as a surface scaffold or trafficking/quality-control-associated
  membrane factor.
- Tissue: if causal, `SEL1L3`-high tissue-resident cells would license local
  inflammatory retention or survival of lipid-handling myeloid cells, producing
  a secondary lipid-lysosomal inflammatory module.

Directionality prediction:

- Test non-depleting inhibition or knockdown first.
- Do not test agonism first; the disease-associated direction is increased
  expression in MS and several non-MS tissue contexts.
- Do not infer that antibody depletion is acceptable. The safety and cell-type
  specificity are unknown.

Strongest falsifying observation:

- After adjusting for lipid-lysosomal module score, IFN/NF-kB/stress modules,
  tissue damage, and donor/cell-compartment structure, the `SEL1L3` disease
  residual disappears in MS and the UC/T1D contexts; or target-specific
  perturbation of `SEL1L3` in disease-high stromal/endothelial cells fails to
  change macrophage lipid-lysosomal state in co-culture.

Sidecar decision:

- Keep `SEL1L3` for one focused residual/controller test. Do not promote.

### FXYD5

Local evidence:

- Wave101 call: `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR`.
- Wave101 score: `17.23`; gate count: `7`.
- MS white-matter signal: delta `0.3525`, p `0.05871`, FDR `0.8989`.
- Positive disease count in Wave101: `4`; negative disease count: `1`.
- Positive diseases: Crohn disease, psoriasis, type 1 diabetes mellitus,
  ulcerative colitis.
- Negative disease: Crohn disease.
- Best positive context: ulcerative-colitis epithelial compartment, delta
  `2.32`, p `0.0322`.
- Best negative context in Wave94: Crohn myeloid, delta `-0.979`, p `0.000214`.
- Treatment-response summary is direction-conflicted: IBD external anti-TNF
  signal g `-0.783`, p `0.014`; RA baseline synovium g `0.809`, p `0.0197`.
- UniProt accessibility in local Wave101/W94 table: basolateral cell membrane
  and cell membrane, one transmembrane feature.
- Wave37 CRISPR efferocytosis screen: `UNRESOLVED`; contrast LFC `-0.2179`,
  FDR `1.0`.
- Wave62 target-resolution fields in Wave101 are zero for strong L2G and QTL
  colocalization support.

Molecule-to-cell-to-tissue hypothesis:

- Molecule: FXYD-domain Na/K-ATPase regulator and adhesion-associated
  membrane protein.
- Cell: epithelial, endothelial, or stromal cells with high `FXYD5` may shift
  ion handling and adhesion/barrier state.
- Tissue: if causal, a high-`FXYD5` barrier or stromal state could increase
  tissue leak, matrix remodeling, or inflammatory licensing, indirectly
  feeding a lipid-lysosomal myeloid response.

Directionality prediction:

- If pursued at all, test non-depleting blockade or knockdown in barrier/stromal
  cells; avoid systemic Na/K-ATPase perturbation and avoid cytotoxic depletion.
- Direction must remain conditional: inhibition is plausible only if
  `FXYD5`-high states cause inflammatory licensing. If `FXYD5` is a repair or
  compensatory barrier response, inhibition could worsen tissue damage.

Strongest falsifying observation:

- The Crohn myeloid negative signal replicates in an independent dataset, or
  residualization shows `FXYD5` is only a barrier-damage/epithelial-composition
  marker; or `FXYD5` knockdown improves neither tissue inflammatory signals nor
  macrophage lipid-lysosomal state, or worsens barrier integrity.

Sidecar decision:

- Kill `FXYD5` as an immediate therapeutic nomination. Retain it only as a
  wet-lab kill-test comparator because its mechanistic story is testable.

### APOC1 Comparator

Local evidence:

- Wave101 call: `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR`.
- Wave101 score: `14.41`; gate count: `6`.
- MS white-matter signal: delta `0.8063`, p `0.03335`, FDR `0.8507`.
- Positive disease count: `3`; negative disease count: `1`.
- Positive diseases: Sjogren syndrome, type 1 diabetes mellitus, ulcerative
  colitis.
- Negative disease: ulcerative colitis.
- Wave37 CRISPR efferocytosis screen: `UNRESOLVED`; contrast LFC `0.2597`,
  FDR `1.0`.
- Wave18: `do_not_promote`.
- Wave62: `NO_GO_WAVE62_TARGET_RESOLUTION`.

Molecule-to-cell-to-tissue hypothesis:

- `APOC1` is best treated as a secreted lipid-state marker or confounder. It
  plausibly reports lipid transport/remodeling in diseased tissue, but the
  local evidence does not show target-specific control of lipid-lysosomal
  myeloid biology.

Directionality prediction:

- Avoid direct target deepening for now. Any intervention would need a
  compartment-specific route because systemic apolipoprotein modulation is not
  selective for autoimmune tissue.

Strongest falsifying observation:

- `APOC1` remains disease-high only before adjustment for tissue lipid state or
  cell composition, and perturbation fails to move the lipid-lysosomal module.

Sidecar decision:

- Kill `APOC1` immediately as an intervention branch. Keep it only as a
  lipid-state confounder comparator.

### CD82 Comparator

Local evidence:

- Wave101 call: `NO_GO_PRIOR_OR_CROWDED_ROUTE`.
- Wave101 score: `17.16`; gate count: `6`.
- MS white-matter signal: delta `0.5037`, p `0.1729`, FDR `0.8994`.
- Positive disease count: `5`; negative disease count: `0`.
- Best positive context: ulcerative-colitis stromal compartment, delta `1.51`,
  p `0.0136`.
- Wave94 response signal: IBD external anti-TNF g `-1.08`, p `5.867e-05`.
- UniProt annotation in local Wave94: cell membrane and cytoplasmic vesicle /
  phagosome; four transmembrane features.
- Wave37 CRISPR efferocytosis screen: `UNRESOLVED`; contrast LFC `-0.7754`,
  FDR `0.9971`.

Molecule-to-cell-to-tissue hypothesis:

- `CD82` is the most endolysosomal-looking accessible comparator because
  tetraspanin membrane domains can organize receptor signaling and trafficking.
  The problem is not biological plausibility; it is directionality and target
  actionability.

Directionality prediction:

- Do not choose a therapeutic direction from current data. Blockade, agonism,
  clustering, or cell-state marking could all fit different tetraspanin
  contexts.

Strongest falsifying observation:

- Target-specific perturbation does not alter phagosome/endolysosomal readouts
  or the disease signal disappears after residualization against generic
  inflammatory and tissue-compartment modules.

Sidecar decision:

- Keep as an endolysosomal comparator only. Do not reopen as a target branch.

### LAPTM5 Comparator

Local evidence:

- Wave101 call: `NO_GO_WEAK_MS_ANCHOR`.
- Wave101 score: `15.11`; gate count: `6`.
- MS white-matter signal: delta `0.2727`, p `0.1304`, FDR `0.8989`.
- Positive disease count: `3`; negative disease count: `0`.
- Best positive context: ulcerative-colitis stromal compartment, delta `2.76`,
  p `0.00326`.
- Wave94 records Wave15 residual support in six diseases and a previous
  `GO_SCOUT`, but Wave101 still lacks perturbation, genetics, and clean
  direction.
- Wave18: `do_not_promote`.

Molecule-to-cell-to-tissue hypothesis:

- `LAPTM5` is a hematopoietic lysosomal membrane state marker and may sit
  closer to the cell-intrinsic lipid-lysosomal program than `SEL1L3` or
  `FXYD5`. Its translational problem is that it is not an accessible,
  direction-resolved intervention point.

Directionality prediction:

- Avoid direct modulation until a perturbation test shows whether reducing or
  increasing `LAPTM5` resolves the inflammatory lysosomal state.

Strongest falsifying observation:

- Independent MS datasets fail to show a meaningful effect, or residualized
  analysis shows `LAPTM5` is only a hematopoietic cell-state marker with no
  disease-specific residual.

Sidecar decision:

- Keep as a lysosomal comparator and positive-control marker for the residual
  model. Do not promote.

## Candidate to Kill Immediately

Kill `APOC1` as an intervention branch. It is a secreted lipid-state signal with
systemic lipid biology, direction conflict, no useful Wave37 perturbation
support, no Wave18 promotion, and no Wave62 target-resolution support.

If forced to choose between only `SEL1L3` and `FXYD5`, kill `FXYD5` as a target
nomination now and retain it only as a mechanistic wet-lab comparator. Its
mechanism is more concrete than `SEL1L3`, but the current data already contain a
Crohn negative context plus treatment-response direction conflict.

## Recommended Local Next Test

Run a Wave102 residualized tissue-niche controller test before any more
target-ranking:

1. Inputs: direct h5ad donor-level compartment outputs plus MS white-matter
   evidence already used by Wave94/W101.
2. Candidates: `SEL1L3`, `FXYD5`, `APOC1`, `CD82`, `LAPTM5`.
3. Model each candidate's donor/compartment expression as a function of disease
   status after adjustment for:
   - lipid-lysosomal module score,
   - IFN/APC module score,
   - NF-kB/TNF/stress module score,
   - cell-type compartment and tissue role,
   - donor-level covariates available in the local h5ad metadata.
4. Ask whether the residual candidate signal predicts myeloid lipid-lysosomal
   module intensity in the same donor or tissue context.
5. Positive-for-deepening criterion:
   - residual disease effect remains in MS plus at least two non-MS tissues,
   - same-direction residual association with myeloid lipid-lysosomal module,
   - no replicated negative disease context,
   - effect is not explained by one tissue compartment alone.
6. Negative/closure criterion:
   - residual disease effect disappears, becomes direction-conflicted, or fails
     to predict myeloid module after adjustment. If this happens, close the
     accessible-survivor branch and pivot away from surface markers.

Preferred script name: `scripts/v3_wave102_sel1l3_fxyd5_residual_controller_test.py`.

