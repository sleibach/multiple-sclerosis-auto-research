# From Interesting Thought To Testable Research Direction

Creative ideas are welcome. The hard step is converting an idea into a test
that can say **no**. The examples below are design illustrations, not new
scientific hypotheses or endorsements. They use only boundaries already
recorded in the [claim-source contract](CLAIM_SOURCE_MATRIX_V55.md).

For a blank version, use the
[copy-ready template](HOW_TO_CONTRIBUTE_IDEAS.md#copy-ready-idea-template).

## The Transformation In One Picture

| vague thought | add | testable direction |
|---|---|---|
| “Maybe method or mechanism X matters.” | Current boundary, changed prediction, reachable data, comparator/null, confounders, holdout, and drop rule | “Under fixed conditions, X predicts observable A rather than B; this test distinguishes them, and result C closes the direction.” |

The goal is not to make an idea sound more technical. It is to expose what
would make the idea wrong.

## Example 1: “Use AI To Improve The Monitoring Score”

### Interesting but not yet usable

> Train a deep model on all the expression data. It will probably outperform
> the simple APC/HLA-II score.

### Hidden problems

- The available internal evidence is tiny, so a flexible model can memorize
  folds or analytical choices.
- More flexible coupled-axis models already failed to improve the locked score
  under the existing checks. `[D02]`
- Reusing a validation cohort for optimization would destroy the frozen
  external test. `[A01]`

### Testable rewrite

**Question:** Can a prespecified flexible model improve transportability on a
future cohort without changing or tuning the locked score?

**Prediction:** A model trained only on designated historical cohorts and
frozen before access to a new cohort will improve a prespecified metric over
the locked scalar on that untouched cohort.

**Null/comparator:** The unchanged locked scalar, plus label-permuted training
and a complexity-matched null pipeline.

**Required data:** A genuinely independent cohort with paired timepoints,
compatible outcome labels, gene coverage, and adequate metadata.

**Drop rule:** Drop the improvement claim if the held-out interval includes no
improvement, if gains vanish after batch/source controls, or if any tuning used
the external outcomes.

**Status:** Data-gated method proposal, not a superior model. `[M03, A01]`

## Example 2: “GPR25 Is A GPCR, So It Must Be Druggable”

### Interesting but not yet usable

> GPR25 is a receptor and AlphaFold gives it a structure. Find an inhibitor.

### Hidden problems

- The chr1 causal gene remains uncertain.
- The protective direction appears more compatible with restoration or
  up-function, not default inhibition.
- Predicted geometry does not establish causal relevance or the needed
  pharmacological sign. `[G03, G05]`

### Testable rewrite

**Question:** Under a signal-specific causal model, does GPR25 rather than
KIF21B mediate the protective direction, and can a feasible modality reproduce
that direction in the relevant immune state?

**Prediction:** Perturbations that increase the causally implicated function
will move a prespecified downstream readout in the protective direction;
inhibition will not.

**Null/comparator:** Matched perturbations of KIF21B, non-targeting controls,
and both gain- and loss-direction interventions.

**Required data:** Signal-specific, cell-relevant QTL evidence plus a
directional functional assay in the implicated state.

**Drop rule:** Keep the route closed if causal assignment remains ambiguous,
the required sign cannot be reproduced, or the modality only supports the
opposite sign.

**Status:** A possible reopening test, not a reopened target. `[G03, G05]`

## Example 3: “Use A Brain Dataset To Find A Progression Marker”

### Interesting but not yet usable

> Compare progressive and relapsing brain samples and call the strongest gene a
> progression biomarker.

### Hidden problems

- Cross-sectional stage or tissue differences cannot show that an earlier
  state predicts later confirmed disability in the same people.
- Diagnosis, brain bank, site, and tissue source can be entangled.
- The held progression packages lack the complete longitudinal design.
  `[P01, P03, C02]`

### Testable rewrite

**Question:** Does a molecular state measured before outcome change predict
later confirmed disability beyond relapse activity, treatment, site/source,
and baseline disability?

**Prediction:** A score fixed in advance predicts repeated confirmed-disability
change in held-out people or sites while retaining direction after source and
clinical adjustment.

**Null/comparator:** Time-shuffled outcomes, source/site prediction, baseline-
only clinical prediction, and a negative-control molecular score.

**Required data:** Repeated molecular measurements, repeated confirmed-
disability outcomes, person/time mapping, treatment and relapse context, and
source provenance.

**Drop rule:** Do not call it progression prediction if molecular measurement
does not precede outcome, source predicts the score, or only cross-sectional
stage separation remains.

**Status:** Cohort-design direction; current data cannot run the decisive test.
`[P01-P05]`

## Example 4: “The APC Axis Means We Should Combine Several Drugs”

### Interesting but not yet usable

> HLA-II, IFN/APC, MIF/CD74, and lysosomal processing move together, so inhibit
> several nodes at once.

### Hidden problems

- Coupled expression can reflect shared upstream context rather than multiple
  causal control points.
- The architecture did not improve the monitoring score.
- Combination enthusiasm does not determine node direction, cell specificity,
  interaction, toxicity, or controllability. `[D01-D02]`

### Testable rewrite

**Question:** Which of several competing network explanations best predicts
the response to single-node and paired perturbations?

**Prediction:** A prespecified causal graph predicts distinct non-additive
readouts for a minimal perturbation panel, including an interaction that rival
graphs do not predict.

**Null/comparator:** Independent additive effects, a single common-upstream
driver, and label-preserving network randomizations.

**Required data:** Perturbation-by-node-by-dose measurements in a relevant APC
state, with viability and broad immune-tone readouts.

**Drop rule:** Drop the combination logic if interactions are additive,
non-specific, unstable across donors, or reproduced by a common-context null.

**Status:** Systems-identification proposal, not a multi-target treatment.
`[D01-D02]`

## Example 5: “AlphaFold Found A Pocket, So Test The Protein”

### Interesting but not yet usable

> The predicted structure has a pocket. That makes the protein a target.

### Hidden problems

- A structure prediction is not an experimental structure.
- Pocket confidence, residue confidence, conformational state, accessibility,
  and functional coupling are separate questions.
- A pocket says nothing by itself about causal gene or therapeutic direction.

### Testable rewrite

**Question:** Is a high-confidence predicted region experimentally folded and
ligandable, and would modulation at that site produce the genetically required
functional sign?

**Prediction:** Orthogonal structural or biophysical assays reproduce the local
geometry and binding changes the prespecified functional readout in the needed
direction.

**Null/comparator:** Low-confidence regions, inactive analogs, pocket-disrupting
mutations, and opposite-direction functional controls.

**Required data:** Confidence-resolved prediction, experimental structural or
biophysical assay, binding measurements, and a direction-matched functional
assay.

**Drop rule:** Treat the pocket as non-actionable if geometry is not
experimentally supported, binding does not alter function, or only the wrong
direction is feasible.

**Status:** Structure-informed assay proposal, not target evidence. `[G03-G04,
E02]`

## Example 6: “I Found A Longitudinal MS Dataset”

### Interesting but not yet usable

> This paper has before-and-after samples. Use it to validate the score.

### Hidden problems

“Longitudinal” does not guarantee that the same people are paired, the relevant
outcome is mapped to samples, the module genes are present, or use is permitted.
The existing scout found many near-matches that fail one of these requirements.
`[A04]`

### Testable rewrite

**Question:** Does the package meet the frozen validation input contract?

**Prediction:** A verified manifest resolves person IDs, baseline and early
timepoints, compatible outcome labels, required genes, normalization, batch,
and use terms without outcome-dependent repair.

**Null/comparator:** The preregistered rejection/abstention cases for missing
pairing, labels, gene coverage, provenance, or permission.

**Required data:** Accession, metadata dictionary, sample sheet, expression
matrix, outcome mapping, and explicit use conditions.

**Drop rule:** Classify it as not validation-ready if any mandatory field cannot
be verified. Do not infer labels from group names or paper prose.

**Status:** Access-verification task, not a validation result. `[A01, A04]`

## Example 7: “Adjust The Score Until It Works In Gafson”

### Interesting but not yet usable

> If the score misses, change the threshold or genes to fit the new cohort.

### Hidden problems

That would turn validation into model development after seeing the answer. It
could create an apparently successful result with no independent test left.

### Testable rewrite

**Question:** Does the unchanged rule pass the precommitted external test?

**Prediction:** The frozen score achieves the preregistered outcome under the
fixed ingestion, quality, confounder, and interpretation plan.

**Null/comparator:** The preregistered null distribution and all three declared
outcomes: pass, fail, or inconclusive.

**Required data:** A package that passes the frozen ingestion contract.

**Drop rule:** If it fails, report failure under the preregistered meaning. Any
later redesigned score is a new hypothesis requiring another untouched cohort.

**Status:** This is the existing validation plan, not a place for optimization.
`[A01]`

## Example 8: “Build A Green/Red Clinical Dashboard”

### Interesting but not yet usable

> Show green when the monitoring score predicts response and red otherwise.

### Hidden problems

The lead is provisional, is not a treatment selector, and may be inconclusive
or invalid on a particular input. A binary display would imply a clinical
decision the evidence does not support. `[M01, M05]`

### Testable rewrite

**Question:** Can an interface communicate a research result without causing
users to infer treatment advice or hide uncertainty?

**Prediction:** In a preregistered comprehension test, users correctly identify
pass, fail, inconclusive, and invalid-input states and state that none selects a
treatment or proves a target.

**Null/comparator:** A binary green/red design and a text-only baseline, with
predefined misunderstanding rates.

**Required data:** Synthetic interface cases only, clearly labeled as method
testing, plus participant responses. No patient-level clinical claims.

**Drop rule:** Reject the interface if users systematically infer efficacy,
treatment selection, or biological causality.

**Status:** Human-factors method proposal, not a clinical product. `[M01, M05,
A01]`

## Example 9: “Two AI Models Agree, So Ground It As A Finding”

### Interesting but not yet usable

> Claude and Gemini independently suggested the same mechanism. That
> convergence makes it likely to be true.

### Hidden problems

Models can share training sources, framing effects, or persuasive failure
modes. Agreement can order a testing queue, but it does not measure biological
truth. `[E03]`

### Testable rewrite

**Question:** What concrete observable prediction follows from the shared
proposal that differs from existing explanations?

**Prediction:** The proposal survives a fixed real-data test, negative controls,
multiplicity correction, and an independent holdout.

**Null/comparator:** Predictions from the current explanation, shuffled or
matched nulls, and a precommitted search budget.

**Required data:** Determined by the biological claim, not by model prose.

**Drop rule:** Record the proposal as unsupported if it lacks reachable data or
fails the grounded test, regardless of model confidence.

**Status:** Proposal-generation workflow only. `[E03]`

## Example 10: “A Null Means We Should Try More Variants”

### Interesting but not yet usable

> The primary result was null, so test related modules, thresholds, subgroups,
> and transformations until something appears.

### Hidden problems

An expanding search after seeing the outcome makes false positives likely and
erases the meaning of the original test.

### Testable rewrite

**Question:** What bounded information remains after the primary null?

**Prediction:** The prespecified effect interval or failure envelope can rule
out effects larger than a stated scope, or identify the sample/design needed for
a decisive future test.

**Null/comparator:** The original frozen null and multiplicity budget; any new
exploration is labeled exploratory and cannot rescue the tested claim.

**Required data:** Original outputs, uncertainty estimates, and the frozen
analysis record.

**Drop rule:** Close the tested version when its criterion fails. Register a
materially different follow-up as a new test before using another outcome.

**Status:** Honest inference after a null, not result shopping. `[D02-D05,
P02, P04]`

## A Five-Line Rewrite Pattern

When an idea is still vague, rewrite it in five lines:

1. **Boundary:** The project currently cannot distinguish ___ from ___.
2. **Prediction:** If my idea is useful, fixed measurement ___ will differ from
   comparator ___ in direction ___.
3. **Data:** The test requires ___, and the access path is ___.
4. **Protection:** The null, holdout, and main confounder are ___, ___, and ___.
5. **Drop rule:** I will abandon or narrow the idea if ___.

If line 3 cannot be completed, the next contribution is a precise data request.
If line 5 cannot be completed, the idea is not yet testable.

