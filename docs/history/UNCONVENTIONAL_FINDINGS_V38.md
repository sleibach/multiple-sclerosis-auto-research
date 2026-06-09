# Unconventional Findings V38

Block start UTC: 2026-06-08T20:30:23Z

Status: in progress.

V38 asks unconventional questions while keeping the evidence gate unchanged.
Model and RPT output are proposal sources only. Every claim below is grounded in
committed project data or explicitly marked blocked/inconclusive.

## Workstream B: Adversarial Self-Inversion

### B1. Inversion Of The Bounded V22/V23 Monitoring Signal

Status: **completed for first adversarial target**.

Question:

Could the project's strongest surviving lead, the bounded V22/V23 APC/HLA-II
early monitoring scalar, be better explained as an artifact than as a true
provisional validation lead?

Proposal sources:

- Claude and Gemini were prompted independently with a compact adversarial
  inversion prompt.
- Outputs:
  - `analysis/v38_adversarial_monitoring/claude_inversions.json`
  - `analysis/v38_adversarial_monitoring/gemini_inversions.json`
- Model output was used only to prioritize tests.

Grounding artifacts:

- Script: `scripts/v38_adversarial_monitoring_inversion.py`
- AUC set table:
  `analysis/v38_adversarial_monitoring/grounded_auc_sets.tsv`
- Inversion result table:
  `analysis/v38_adversarial_monitoring/grounded_inversion_results.tsv`
- Summary JSON:
  `analysis/v38_adversarial_monitoring/grounded_inversion_summary.json`

Grounded results:

| Inversion | Grounded result | Evidence | V38 delta |
|---|---|---|---|
| Bounded subset selection artifact | partially supported as scope limit | bounded DMF + exact tofacitinib AUC `0.811`, exact p `0.011`; primary locked all DMF + fingolimod + adalimumab AUC `0.547`; complement fingolimod + adalimumab AUC `0.557`, exact p `0.333` | Strengthens bounded-only wording; does not kill the bounded validation-lead status because V37 already scoped it as provisional and bounded. |
| Cross-disease exact tofacitinib drives the headline | supported as MS-specificity caveat | DMF-only AUC `0.720`, exact p `0.155`; exact tofacitinib-only AUC `0.950`, exact p `0.0159`; pooled bounded AUC `0.811` | Any MS-specific wording must be DMF-suggestive, not MS-validated. The Gafson DMF validation remains the decisive next step. |
| STAT1/metabolic/inflammatory tone explains independent APC specificity | partially supported | V32 broad immune-tone joint adjustment attenuates AUC to `0.656`, permutation p `0.163`; locked+confounders LOOCV AUC `0.733` still exceeds confounders-only `0.611` | Supports "immune-tone bounded" and "not APC/HLA-II-specific" wording; does not justify calling it a steroid or simple composition artifact. |
| Small-n winner's curse / family-wise fragility | partially supported for post-hoc extensions, not for the pre-locked scalar | V28 bounded scalar p `0.008`; Bonferroni across 9 V28 bounded methods would be `0.072`, but the scalar was locked before V28 method expansion | Reinforces no successor/post-hoc rule promotion. Does not invalidate the pre-locked scalar as a validation candidate. |
| Threshold calibration does not transfer across bounded cohorts | supported | DMF median threshold -> exact tofacitinib accuracy `0.667`; exact tofacitinib threshold -> DMF accuracy `0.600` | Blocks any clinical threshold claim. Keep as rank/direction monitoring candidate until fresh validation calibrates a threshold. |

Verdict:

The adversarial inversion **narrows but does not kill** the V37 claim. The
bounded monitoring scalar should be described as:

> bounded, small-n, partly immune-tone-conditioned, not MS-calibrated, not
> broad across therapies, and dependent on fresh DMF validation.

This is not a demotion relative to V37's honest framing. It is a useful stress
test that confirms the V37 wording should stay conservative and that the next
action remains frozen Gafson/DMF validation rather than building a successor
rule.

### B2. Inversion Of The Coupled APC Architecture

Status: **completed first immune-tone inversion**.

Question:

Could the V26 coupled HLA-II/IFN-APC/MIF-CD74 architecture be mostly generic
immune-tone covariance rather than a structured APC module dependency?

Grounding artifacts:

- Script: `scripts/v38_coupled_architecture_inversion.py`
- V26 module matrices:
  `analysis/v26_deep_structure/*module_matrix.tsv`
- Residual edge tests:
  `analysis/v38_coupled_architecture_inversion/coupled_edge_residual_tests.tsv`
- Global-tone tests:
  `analysis/v38_coupled_architecture_inversion/module_global_tone_tests.tsv`
- V27 predictive constraint:
  `analysis/v38_coupled_architecture_inversion/v27_bounded_predictive_constraint.tsv`
- Summary:
  `analysis/v38_coupled_architecture_inversion/coupled_inversion_summary.json`

Method:

The adversarial control was row-wise module-mean residualization. For each V26
matrix, each context's module vector was centered by its own mean, then module
pair correlations were retested with 5,000 row-permutation nulls. If coupling
were only global immune tone, core APC edges should collapse after this
row-centering.

Results:

| Test | Result | Interpretation |
|---|---|---|
| Core modules vs global row mean | Core module median abs correlation with row mean `0.854`; non-core median `0.663` | The inversion is partly right: the coupled architecture is strongly tone-loaded. |
| Core APC edges before row-centering | `22/32` core edge tests had abs r >= `0.5` and p < `0.05`; median core abs r `0.788` | Reproduces V26's coupled-dependency signal. |
| Core APC edges after row-centering | `13/32` still had abs r >= `0.5` and p < `0.05`; `10/32` also had BH q < `0.10`; median core abs r `0.590` | Coupling is attenuated but not erased. It is not purely row-wise global tone. |
| Non-core edges after row-centering | `15` non-core edge tests also passed abs r/p criteria; `13` had q < `0.10` | Specificity is imperfect; row-centering can induce compositional anti-correlations and does not isolate APC-only biology cleanly. |
| Predictive successor constraint | V27 bounded AUC: scalar `0.811`, coupled projection `0.689`, V22-augmented `0.633`, coordination `0.733` | Coupling remains mechanistic context, not a better response-prediction rule. |

Verdict:

The adversarial inversion **partly succeeds but does not erase** the V26
architecture.

What survives:

- core APC module dependencies remain after a harsh global-tone residualization;
- several residual core edges remain strong, including HLA-II/MIF-CD74 and
  IFN/lysosomal relationships in treatment/cell-state matrices.

What weakens:

- the architecture is heavily immune-tone-loaded;
- specificity is not clean, because non-core residual edges also survive;
- V27 already showed the coupled representation does not improve prediction
  over the scalar.

V38 delta:

V26 should be framed as a **tone-loaded coupled APC architecture**, not as a
pure APC-specific invariant and not as a superior clinical rule. This is a
narrowing of interpretation, not a demotion of the V26 `supported` structural
grade, because the row-centered residual test still leaves core structure.

### B3. Inversion Of The MS-UC Genome-Wide Genetic Backdrop

Status: **completed against recorded V21 LDSC outputs**.

Question:

Could the V21 MS-UC genetic-correlation backdrop be mostly an MHC artifact,
sample-overlap artifact, or an interpretation unsupported outside the primary
LDSC run?

Grounding artifacts:

- Script: `scripts/v38_rg_backdrop_inversion.py`
- V21 LDSC table: `analysis/v21_ldsc_backdrop/ldsc_rg_results.tsv`
- V21 report: `docs/workups/genetics/GENETIC_CORRELATION_BACKDROP_V21.md`
- V38 inversion table:
  `analysis/v38_rg_backdrop_inversion/rg_backdrop_inversion_table.tsv`
- Summary:
  `analysis/v38_rg_backdrop_inversion/rg_backdrop_inversion_summary.json`

Results:

| Comparator | Full rg | p | MHC sensitivity | Intercept caveat | V38 inversion result |
|---|---:|---:|---|---|---|
| UC | `0.3342` | `4.8771e-14` | no-MHC rg identical (`0.3342`), valid SNPs identical | h2 intercept `1.0467`, gcov intercept `0.0844`; not strongly inflated | MHC/sample-overlap inversion not supported in the recorded LDSC frame. |
| Crohn | `0.1675` | `0.0015` | no-MHC rg identical (`0.1675`), valid SNPs identical | h2 intercept `1.0212`, gcov intercept `0.0789`; not strongly inflated | Same caveat; modest positive rg remains. |
| SLE | `0.2439` | `6.0712e-05` | no no-MHC run in V21 | h2 intercept `1.1998` | Remains caveated, as V21 already stated. |
| RA | `0.1692` | `0.0002` | no no-MHC run in V21 | h2 intercept `1.0553` | Modest positive rg remains within recorded frame. |

Critical caveat:

The MHC-excluded UC/Crohn runs were identical because V21 documented that the
active LDSC reference panel contains zero chr6:25-34 Mb SNPs. That means the
result is effectively MHC-free for that interval, but it is **not** an
independent sensitivity using an MHC-containing reference.

Verdict:

The adversarial inversion **does not demote** the V21 MS-UC backdrop. The
strongest supported statement remains:

> In the verified LDSC frame, UC is the strongest tested genome-wide inherited
> genetic comparator for MS, with Crohn materially weaker.

What is narrowed:

- do not overstate this as a separately confirmed MHC-exclusion sensitivity;
- do not use SLE rg without the high-intercept caveat;
- do not infer locus-level transferability from global rg.

### B4. Inversion Of The Layer-Transfer Map

Status: **completed against V8-V12 matrix artifacts**.

Question:

Could the V10/V12 transfer-validity map be mostly narrative disease similarity
rather than evidence-grounded, axis-specific transfer logic?

Grounding artifacts:

- Script: `scripts/v38_layer_transfer_inversion.py`
- Placement matrix: `analysis/v8_map/placement_matrix.tsv`
- Disagreement matrix: `analysis/v11_matrix/disagreement_matrix.tsv`
- Axis heterogeneity table:
  `analysis/v38_layer_transfer_inversion/disease_axis_heterogeneity.tsv`
- Disagreement-cell specificity table:
  `analysis/v38_layer_transfer_inversion/disagreement_cell_axis_specificity.tsv`
- Summary:
  `analysis/v38_layer_transfer_inversion/layer_transfer_inversion_summary.json`

Results:

| Test | Result | Interpretation |
|---|---|---|
| Key comparator diseases with heterogeneous axis placements | `4/4` | UC, Crohn, RA, and Sjogren each change placement across biological layers; disease label alone is insufficient. |
| V11/V12 disagreement cells | `10` total: `4` intervention-derived, `4` biological, `2` artifact | Artifact accounting is explicit rather than hidden. |
| Non-artifact cells with axis-specific evidence | `8/8` | Every retained transfer/disagreement cell has placement difference plus compartment, causality, or axis-independence evidence. |
| Artifact cells | `2/10` | The map already downgraded overlapping or scope-confounded axes. |

Disease-level heterogeneity:

- Sjogren: `near` on IFN/APC, `far` on lipid-lysosomal.
- RA: `near` on pregnancy/hormonal axis, `far` on blood APC/treatment/repair
  axes.
- Crohn: `near` on IFN/APC and treatment/repair, `intermediate` on genetics.
- UC: `near` on IFN/APC/genetics/repair but `contradictory` on treatment
  response because baseline and dynamic treatment-response behave differently.

Verdict:

The narrative-disease-similarity inversion is **not supported**. The transfer
map is genuinely axis-specific in the committed matrix: the same disease can
transfer on one biological layer and fail on another, and artifact cells were
explicitly marked rather than promoted.

What remains limited:

- The map is a transfer-validity **warning framework**, not an intervention
  claim.
- Some V12 genetics cells were originally supported by triangulation rather
  than new in-process OpenGWAS/LDSC/coloc. V21 hardened the global rg backdrop
  but did not turn every V12 genetics transfer cell into robust locus-level
  colocalization.

Additional null:

- Script: `scripts/v38_layer_heterogeneity_null.py`
- Summary:
  `analysis/v38_layer_heterogeneity_null/layer_heterogeneity_null_summary.json`
- The simple statistic "4/4 key diseases have heterogeneous axis placements" is
  **not exceptional** under random reassignment of placement labels across the
  same key disease-axis table:
  - empirical p for `n_heterogeneous >= 4`: `0.276`;
  - empirical p for mean placement range >= observed: `0.147`.

This narrows the evidence basis: disease-level heterogeneity is a useful
description but not the proof. The transfer-map claim rests on the specific
V11/V12 disagreement cells, where `8/8` non-artifact cells carry
axis/compartment/causality evidence.

### B5. Tone-Stripped Residual Scalar Test

Status: **completed from model-lens proposal, grounded on V32 table**.

Proposal source:

- Claude proposed a "tone-stripped residual scalar" inversion in
  `analysis/v38_model_proposal_pass/claude_remaining_tests.json`.
- Gemini produced separate terse proposals in
  `analysis/v38_model_proposal_pass/gemini_remaining_tests.json`.
- Model output was used only to select a computable test.

Question:

Is the bounded V22/V23 scalar mostly a broad immune-tone proxy, or does response
signal remain after broad tone is removed?

Grounding artifacts:

- Script: `scripts/v38_tone_residual_scalar.py`
- Input: `analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv`
- AUC table: `analysis/v38_tone_residual_scalar/tone_residual_scalar_auc.tsv`
- Summary: `analysis/v38_tone_residual_scalar/tone_residual_scalar_summary.json`

Method:

The script used V32 bounded subject-level data (`n=19`). It fit a leave-one-out
linear model predicting the locked scalar from broad tone deltas:
general inflammatory tone, STAT1 axis, glycolysis, and HIF/NAMPT
immunometabolism. It then compared response AUCs for:

- raw locked scalar;
- LOOCV broad-tone prediction of the scalar;
- tone-residual scalar.

Results:

| Feature | AUC | Exact p | Interpretation |
|---|---:|---:|---|
| Tone-residual scalar | `0.844` | `0.0101` | Residual after broad-tone prediction still separates responders. |
| Raw locked scalar | `0.811` | `0.0220` | Reproduces bounded scalar signal. |
| Broad-tone prediction of scalar | `0.589` | `0.549` | Tone-only prediction does not carry the response signal. |
| Delta glycolysis | `0.689` | `0.182` | Weak context signal only. |
| Delta STAT1 axis | `0.611` | `0.447` | Weak alone. |
| Delta inflammatory tone | `0.500` | `1.000` | Null alone. |

Verdict:

This test **weakens the strongest artifact version** of the immune-tone
inversion. The locked scalar is associated with broad tone in prior audits, but
the response signal is not simply reproduced by broad tone alone. In this held
table, the tone-residual scalar performs at least as well as the raw scalar.

Limits:

- This is still the same tiny bounded `n=19` table, not fresh validation.
- The residual scalar is not a new locked rule.
- V32's broader conclusion remains: the signal is immune-context-conditioned
  and must be audited with confounders in Gafson/DMF validation.

## Workstream A: Structure Of Failure

### A1. Failure-Mode Meta-Analysis Across V37 Negative/Closed Items

Status: **completed for V37 closed/negative item frame**.

Question:

Do the project's killed, closed, parked, and decoupling findings fail for a
common reason that itself reveals a constraint on MS biology or project
methodology?

Grounding artifacts:

- Script: `scripts/v38_failure_structure_meta.py`
- Input frame: `docs/reports/FINDINGS_SCORES_V37.tsv`
- Annotated failure table:
  `analysis/v38_failure_structure/failure_mode_table.tsv`
- Family counts:
  `analysis/v38_failure_structure/failure_family_counts.tsv`
- Mode counts:
  `analysis/v38_failure_structure/failure_mode_counts.tsv`
- Summary:
  `analysis/v38_failure_structure/failure_structure_summary.json`

Frame:

- V37 closed/negative/decoupling items analyzed: `20`.
- Categories included: `decoupling_negative` and `kills_closed`.
- Tags were explicit artifact-derived annotations, not model output.

Family-level results:

| Failure family | Items | Fraction | Interpretation |
|---|---:|---:|---|
| Evidence-resolution failure | `7` | `0.35` | The most common limit is not biological impossibility but insufficient causal resolution, full-QTL direction, held-out validation, or perturbation proof. |
| Context or axis dependence | `5` | `0.25` | Mechanisms often fail when moved across disease, tissue, therapy, baseline/dynamic state, or compartment. |
| Direction or modality constraint | `5` | `0.25` | Genetics and target leads often fail because the disease-protective direction is opposite, mixed, or requires hard restoration/up-function. |
| Specificity or control failure | `4` | `0.20` | Attractive broad module interpretations often fail under random controls, donor-aware tests, or distinct-causal-variant checks. |
| Complexity or modeling failure | `2` | `0.10` | More complex models or coupled successors fail to improve over simpler locked representations. |
| Marker-not-driver failure | `2` | `0.10` | Some attractive biology remains useful as covariate/readout, not as target. |

Most frequent individual tags:

- `module_specificity_failure`: `3` items.
- `transfer_invalid`, `hard_protective_direction`, `causal_gene_ambiguity`,
  `axis_mismatch`, `baseline_not_dynamic`, `compartment_mismatch`: `2` items
  each.

Verdict:

There is **no single universal failure mechanism**. The common structure is a
three-part constraint:

1. MS-adjacent mechanisms are highly context/axis dependent.
2. Therapeutic genetics often points toward hard directions: restoration,
   up-function, signal-specific modulation, or opposite disease directions.
3. Broad module stories collapse unless they survive specificity, donor-aware,
   full-QTL, or held-out validation gates.

This is decision-useful because it predicts where future leads should be
skeptically pre-filtered. A new lead should be penalized immediately if it
requires cross-axis transfer, restoration/up-function without modality, or broad
module interpretation without a matched specificity control.

### A2. Direction/Modality Constraint As A Future-Lead Prefilter

Status: **completed targeted follow-up**.

Question:

Was the chr1/KIF21B lesson, real biology but wrong or hard therapeutic
direction, an anecdote, or a recurring enough pattern to become a mandatory
prefilter for future leads?

Grounding artifacts:

- Script: `scripts/v38_direction_modality_prefilter.py`
- Input: `analysis/v38_failure_structure/failure_mode_table.tsv`
- Annotated table:
  `analysis/v38_direction_modality_prefilter/direction_modality_annotated_failures.tsv`
- Constraint counts:
  `analysis/v38_direction_modality_prefilter/direction_modality_constraint_counts.tsv`
- Summary:
  `analysis/v38_direction_modality_prefilter/direction_modality_prefilter_summary.json`

Results:

| Frame | Count | Interpretation |
|---|---:|---|
| All V37/V38 negative or closed items with a direction/modality constraint | `8/20` (`40%`) | Common, but not universal across all failure types. |
| Target-like genetics/nomination items with a direction/modality constraint | `5/6` (`83%`) | Strong enough to be a mandatory target-lead prefilter. |
| Hard restoration/up-function/agonism specifically | `2/20` | Not the whole failure structure, but decisive for chr1/GPR25-type target claims. |
| Opposite or invalid transfer direction | `2/20` | Captures ZMIZ1 and PTGER4-style transfer failures. |
| Direction unresolved or missing | `3/20` | A recurrent reason to park rather than promote genetics leads. |
| Modality or target-fit failure | `4/20` | Covers hard target fit and marker/covariate-not-driver cases. |

Verdict:

The hard-protective-direction problem is **not** a universal MS biology law.
It is, however, a strong project-level constraint for target-like leads.

Future genetics or target-nomination leads should be prefiltered before deep
work:

1. Is the protective direction allele-aligned and known?
2. Does the feasible modality move in that protective direction?
3. If the required action is restoration, up-function, or agonism, is there a
   realistic modality rather than class-precedent optimism?
4. Is the cross-disease direction same or opposite?

If any answer fails, the lead can still be important biology, but it should be
labeled hard-target/decoupling/data-gated immediately rather than entering the
medical-team lead slate as promising.

### A3. V36 Exploratory Fragility Map

Status: **completed across selected V36 machine-readable artifacts**.

Question:

When the project turned up the creativity dial in V36, what actually prevented
creative hypotheses from becoming findings?

Grounding artifacts:

- Script: `scripts/v38_v36_fragility_map.py`
- Item table: `analysis/v38_v36_fragility_map/v36_fragility_items.tsv`
- Family counts: `analysis/v38_v36_fragility_map/v36_fragility_family_counts.tsv`
- Summary: `analysis/v38_v36_fragility_map/v36_fragility_map_summary.json`

Results:

| Fragility family | Count | Representative grounded evidence |
|---|---:|---|
| Multiplicity / overfit | `2` | 76-feature search had observed max AUC `1.0` but empirical max-AUC p `0.5`; IFN/STAT four-gene subset top AUC `0.95` but empirical p `0.333`. |
| Composition / confounding | `2` | T/B gap remained positive after simple fraction adjustment (`0.158` -> `0.133`), but T-cell AUC attenuated `1.0` -> `0.65`; broader residualization had worst T-cell AUC `0.5`, B/plasma `0.6`. |
| Compartment-combination multiplicity | `1` | 31 compartment combinations; best single T-cell AUC `1.0`, B/plasma AUC `0.95`; no combo successor promoted. |
| Therapy-branch specificity | `1` | DMF AUC `0.72` and tofacitinib AUC `1.0`, but fingolimod `0.6`, adalimumab `0.511`; IFN-beta uses HLA-II/receptor branch rather than universal scalar. |
| Small-n power | `1` | Gafson-style validation needs roughly `30-40` per group for high p<0.05 power under the observed DMF effect. |
| Creative-generation data gate | `2` | Glycolysis and sterol/lysosomal variants looked plausible but lacked the compartment or flux data needed for promotion. |
| Missing decisive metadata/modality/QC | `3` | Postpartum lacks relapse-labeled MS postpartum samples; lysosomal/metabolic/EBV lack decisive stratified modality; QC structure cannot fully de-risk W8 features. |

Verdict:

V36's broad generation did not mainly fail because ideas were biologically
implausible. It failed to promote them because the evidence gate repeatedly
found the same practical blockers:

- too many post-hoc features for too few patients;
- composition/confounder sensitivity;
- therapy mechanism specificity;
- missing decisive metadata or assay modality;
- inadequate sample size for a validation claim.

The one narrow survivor remains **B/plasma-like IFN/APC remodeling** as the
most stable internal carrier, but it is still single-cohort and validation-gated.
This supports V38's broader failure-structure result: MS hypotheses tend to
become useful only when they are pre-bounded by mechanism, compartment,
direction, and data modality.

### A4. Failure-Map vs Fragility-Map Concordance

Status: **completed from model-lens proposal, grounded as gate-level comparison**.

Question:

Are the V38 failure-structure map and the V36 fragility map redundant, or do
they capture different project constraints?

Grounding artifacts:

- Script: `scripts/v38_failure_fragility_concordance.py`
- V38 failure families:
  `analysis/v38_failure_structure/failure_family_counts.tsv`
- V36 fragility families:
  `analysis/v38_v36_fragility_map/v36_fragility_family_counts.tsv`
- Gate comparison:
  `analysis/v38_failure_fragility_concordance/failure_fragility_gate_comparison.tsv`
- Summary:
  `analysis/v38_failure_fragility_concordance/failure_fragility_concordance_summary.json`

Important limitation:

The row units differ: V38 rows are failed/closed findings, while V36 rows are
analysis artifacts. V38 therefore uses a shared gate taxonomy, not a forced
item-level join.

Results:

| Gate | V38 failure fraction | V36 fragility fraction | Interpretation |
|---|---:|---:|---|
| Evidence resolution / data gap | `0.28` | `0.462` | Shared dominant constraint, stronger in V36 exploratory work. |
| Context / axis / therapy branch | `0.20` | `0.154` | Shared constraint. |
| Direction / modality | `0.20` | `0.000` | V38 target/lead failures capture this; V36 exploratory artifacts do not. |
| Specificity / control | `0.16` | `0.154` | Closely aligned. |
| Complexity / overfit | `0.08` | `0.231` | V36 captures this more strongly because it stress-tested many post-hoc features. |
| Marker not driver | `0.08` | `0.000` | V38 target-nomination failures capture this. |

Jensen-Shannon divergence between the gate distributions: `0.186` bits.

Verdict:

The maps are **complementary, not redundant**. V38 failure structure is better
for target/lead triage, especially direction/modality and marker-not-driver
problems. V36 fragility structure is better for analysis-design triage,
especially multiplicity, power, and technical/confounder fragility. Future work
needs both gates.

## Workstream E: RPT-Led Structural Mining

### E1. RPT Mining Over V37 Score Table And V38 Failure Annotations

Status: **completed for V37 score-table action-class probe**.

Question:

Does the tabular structure of the V37 scored findings table surface a pattern
or contradiction that the narrative synthesis missed?

Grounding artifacts:

- Script: `scripts/v38_rpt_structural_mining.py`
- Payload:
  `analysis/v38_rpt_structural_mining/v38_rpt_payload.json`
- Response:
  `analysis/v38_rpt_structural_mining/v38_rpt_response.json`
- Masked predictions:
  `analysis/v38_rpt_structural_mining/v38_rpt_masked_predictions.tsv`
- Grounded summary:
  `analysis/v38_rpt_structural_mining/v38_rpt_grounded_summary.json`

Method:

The table used V37 relevance, novelty, evidence grade, provisional/negative
flags, data-gap flags, transfer-warning flags, and V38 failure-table membership.
Six edge items were masked:

- bounded APC/HLA-II scalar;
- T/B-readable early IFN/APC/STAT1 state;
- postpartum HLA-II/CD64 APC-arm imbalance;
- ZMIZ1;
- PTGER4;
- V25 simulator negative.

Result:

- Masked rows: `6`.
- RPT predictions matching the artifact-derived V37 action class: `5/6`.
- Sole contradiction: the bounded APC/HLA-II scalar.
  - V37 true class: `external_validation_priority`.
  - RPT prediction: `data_gated_followup`, confidence `0.88`.

Interpretation:

RPT mostly rediscovered the V37 action taxonomy. The single contradiction is
useful: tabularly, the bounded scalar looks like other provisional,
data-gated follow-ups. Its "external validation priority" status is not earned
by generic table structure; it is earned by clinical relevance, pre-locking,
and the fact that a concrete Gafson/DMF validation path exists.

Verdict:

RPT does **not** demote the bounded scalar, because RPT output is not evidence.
It does sharpen the wording:

> The scalar is the top operational validation priority, not a structurally
> exceptional finding in the score table.

No V37 score changes are made.

### E2. Tool-Lens Contribution Ledger

Status: **completed**.

Artifacts:

- Script: `scripts/v38_tool_lens_ledger.py`
- Ledger: `analysis/v38_tool_lens_ledger/tool_lens_contribution_ledger.tsv`
- Summary: `analysis/v38_tool_lens_ledger/tool_lens_contribution_summary.json`

Verdict:

RPT, Claude, and Gemini added value as proposal/prioritization lenses, but none
provided evidence and none upgraded a finding by themselves. Evidence-bearing
V38 results all come from deterministic scripts over committed project data.

Specific contributions:

- RPT sharpened that the bounded scalar is operationally prioritized, not
  structurally exceptional.
- Claude proposed concrete adversarial tests; the tone-residual scalar test was
  grounded and weakened the broad-tone-artifact inversion.
- Gemini converged on the failure/fragility comparison priority, but other
  proposals were too abstract for current tables.
- SAP AI Core spend was not exposed by the local client outputs; no open-ended
  cost was incurred from the repo side.

## Workstream C: Unpublishable-But-True Exclusions

### C1. Conservative Exclusion / Non-Replication Ledger

Status: **completed first ledger**.

Question:

What has the project established is **not** supported as a target, biomarker,
transfer rule, or modeling capability under current data?

Grounding artifacts:

- Script: `scripts/v38_exclusion_ledger.py`
- Ledger:
  `analysis/v38_exclusion_ledger/exclusion_nonreplication_ledger.tsv`
- Counts:
  `analysis/v38_exclusion_ledger/exclusion_counts.tsv`
- Summary:
  `analysis/v38_exclusion_ledger/exclusion_summary.json`

Result:

- Exclusions/non-replications recorded: `16`.
- Strength counts:
  - `negative_established`: `13`;
  - `supported_exclusion`: `2`;
  - `data_gated_not_established`: `1`.

Decision-useful exclusions:

1. Baseline IFN/APC is not a valid general fallback stratifier.
2. The V22 scalar is not a broad cross-therapy response rule.
3. The V22 scalar is not a calibrated clinical threshold.
4. Glucocorticoid/steroid signature does not explain the bounded scalar.
5. Simple marker-level cell composition does not explain the bounded scalar.
6. Receptor-only CD74/CD44/CXCR4 does not dominate the scalar.
7. Coupled/dynamic/flexible ML variants do not improve over the scalar.
8. A broad immune-state simulator is not validated from current data.
9. No load-bearing invariant was established.
10. PTGER4 is not a clean MS-UC transfer target.
11. MHC/HLA overlap is not simple shared causal biology.
12. EBV/IFN APC imprint is not EBV-specific in current data.
13. Complement/lipid progressive axis is not supported as a combined axis.
14. NAMPT/eNAMPT is not reactivated as an MS target.
15. REL/PUS10/USP34 chr2 is not a current shared-locus lead.
16. ZFP36L1 chr14 is not robust enough for lead status.

Verdict:

This is the most "unpublishable but true" V38 product so far. The project has
created a reliable stop-spending ledger. Most entries do not mean the biology is
irrelevant to MS; they mean a specific translational interpretation is not
supported:

- not a target;
- not a general rule;
- not a clinical threshold;
- not a clean transfer locus;
- not EBV-specific;
- not validated as a simulator;
- not robustly colocalized.

This ledger should be used before any future wet-lab or data-acquisition spend.
If a proposed experiment reopens one of these exclusions, it must name the exact
new evidence that would override the current ledger.

## Workstream D: Cross-Scale / Control-Systems Reframing

### D1. Baseline Load vs Dynamic Control Action vs Treated Set-Point

Status: **completed first control-systems probe**.

Question:

Is the bounded V22/V23 monitoring signal better read as a control-system
behavior: baseline immune load, early corrective action, or movement toward a
treated immune set-point?

Grounding artifacts:

- Script: `scripts/v38_control_system_reframing.py`
- Input table:
  `analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv`
- Feature tests:
  `analysis/v38_control_system/control_feature_tests.tsv`
- Family tests:
  `analysis/v38_control_system/control_feature_family_tests.tsv`
- Set-point tests:
  `analysis/v38_control_system/setpoint_distance_tests.tsv`
- Summary:
  `analysis/v38_control_system/control_system_summary.json`

Frame:

- Subjects: `19` bounded V22/V23 cases.
- Responders / non-responders: `10 / 9`.
- Cohorts: GSE235357 DMF (`10`) and exact-module GSE253006 tofacitinib (`9`).
- Tested scalar features: `54`.
- Feature-level tests used exact label permutations preserving responder count.
- Supervised set-point distances used fixed-seed Monte Carlo label permutation
  with the responder centroid recomputed on each permutation.

Results:

| Framing | Best grounded result | Multiplicity-aware interpretation |
|---|---|---|
| Early dynamic/control action | Locked signed score AUC `0.811`, exact p `0.022` | Strongest simple scalar, but within-family max-AUC p `0.190` over 14 early-delta features and all-feature BH q `0.397`. |
| Treated-state features | Treated IFN/APC AUC `0.811`, exact p `0.022`; treated proliferation AUC `0.811`, exact p `0.022` | Similar apparent signal, but within-family max-AUC p `0.196`; not a rule-level improvement over the locked scalar. |
| Baseline-load features | Best baseline feature AUC `0.667`, exact p `0.243` | Baseline load remains weak; no support for converting the monitoring signal into a baseline stratifier. |
| Negative-feedback features | Best feedback feature AUC `0.778`, exact p `0.043` | Does not survive within-family max-AUC correction (`p=0.402`). |
| Responder set-point proximity | Treated IFN/HLA-II/STAT1/metabolic proximity AUC `0.867`, Monte Carlo p `0.0098`; treated composition proximity AUC `0.833`, p `0.0286` | Interesting control-systems hypothesis, but supervised/in-sample: the responder centroid is learned from the same small cohorts. It is a candidate validation readout, not established evidence. |

Verdict:

The data support a **dynamic/treated-state interpretation over baseline load**,
but they do not justify a new rule or a demotion of the locked scalar. The
control-systems view is useful mainly as framing:

- responders look more like they move toward a treated immune set-point;
- baseline state alone is not sufficient;
- the apparent set-point signal needs fresh external validation because its
  centroid is learned from the same `n=19` bounded cases.

V38 delta:

The V37 conclusion is **strengthened in one narrow way**: the signal is still
dynamic, not baseline. It is also narrowed: any set-point/feedback wording must
be explicitly exploratory until tested on Gafson/DMF or another fresh cohort.

## V37-to-V38 Delta So Far

Structured ledger:

- Table: `analysis/v38_delta_ledger/v37_v38_delta_ledger.tsv`
- Summary: `analysis/v38_delta_ledger/v37_v38_delta_summary.json`
- Delta items: `8`.
- Demotions: `0`.

Strengthened:

- V37's conservative framing of the V22/V23 scalar survived direct adversarial
  inversion.
- The need for Gafson DMF validation is stronger, because the only MS-internal
  anchor is DMF-only AUC `0.720` with exact p `0.155`.
- V37's broad discipline is strengthened by the failure-structure result: most
  dead ends were not random; they cluster around context/axis transfer, evidence
  resolution, and direction/modality constraints.
- RPT independently treats the bounded scalar as data-gated rather than
  intrinsically exceptional, reinforcing that its priority is operational and
  clinical, not a reason to inflate evidence grade.
- The exclusion ledger strengthens the negative side of V37: the project now
  has an explicit "do not pursue without new evidence" list rather than a set of
  scattered closed-lead notes.
- The control-systems probe strengthens the dynamic-over-baseline reading of
  the monitoring lead: baseline-load features are weak, while early-delta and
  treated-state features carry the apparent signal.
- The coupled APC architecture withstands a direct global-tone inversion, but
  only as a tone-loaded structure rather than a pure APC-specific architecture.
- The MS-UC rg backdrop withstands an MHC/sample-overlap adversarial check in
  the recorded LDSC frame.
- Direction/modality constraints are now quantified as a recurring target-lead
  failure mode: `5/6` target-like closed/negative items carried them.
- The layer-transfer map withstands narrative-similarity inversion: `4/4` key
  diseases are heterogeneous across axes and `8/8` non-artifact disagreement
  cells are axis-specific.
- V36 creative-generation failures are now structured: promotion failed mostly
  at multiplicity, confounder/composition, therapy-branch, power, and
  missing-modality gates, not because the ideas were intrinsically incoherent.
- The tone-stripped scalar test weakens the broad-tone-artifact inversion: broad
  tone alone has AUC `0.589`, while the tone-residual scalar has AUC `0.844`.
- Failure-map and fragility-map concordance shows the two are complementary:
  V38 captures direction/modality target failures, while V36 captures
  multiplicity/power/technical fragility.

Weakened / narrowed:

- Any phrase implying "MS-validated" or "clinical threshold" is too strong.
- Any phrase implying APC/HLA-II specificity independent of broad
  STAT1/metabolic/inflammatory tone is too strong.
- Any phrase implying the scalar is merely a broad immune-tone proxy is now too
  strong; broad-tone prediction alone does not reproduce the response signal.
- Any phrase implying a validated immune set-point rule is too strong; the
  set-point result is supervised and in-sample.
- Any phrase implying the V26 coupled architecture is independent of broad
  immune tone or composition is too strong.
- Any phrase implying V21 provided an independent MHC-containing-reference
  sensitivity is too strong; the verified panel was already effectively
  MHC-free for chr6:25-34 Mb.
- Any phrase turning the transfer map into direct intervention transfer is too
  strong; V38 supports it as an axis-specific warning/triage framework.
- Any phrase treating "4/4 heterogeneous diseases" alone as statistical proof
  of axis-specific transfer is too strong; the permutation null shows that
  statistic is not exceptional by itself.

Demoted:

- No V37 item is demoted yet. The inversion supports V37's existing
  `provisional` grade for the bounded scalar.

## Pending Workstreams

- D. Additional cross-domain reframings if they yield concrete grounded tests.
