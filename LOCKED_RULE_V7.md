# LOCKED RULE V7 - APC Response Architecture

Locked timestamp: 2026-05-28 21:31 CEST  
Status: immutable for V7 validation  
Derived from: `GSE282122`, `GSE138064`, `GSE24427` only  
Validation exclusion: `GSE282122`, `GSE138064`, and `GSE24427` must not be
counted as V7 independent validation cohorts.

## Scientific Question

Does pre-specified APC response architecture predict autoimmune treatment
response in held-out cohorts, without tuning the rule to those cohorts?

## Frozen Modules

Use gene symbols exactly as listed. A module is scoreable only if at least
`50%` of its genes are present after platform mapping.

### IFN/APC Module

`STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`

### HLA-II Module

`HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`, `HLA-DQB1`

### Receptor-Only Negative-Control Module

`CD74`, `CD44`, `CXCR4`

The receptor-only module is not part of the predictive rule. It is a specificity
control: a validation pass is weakened if receptor-only outperforms the locked
rule in the same cohort.

## Scoring

For bulk expression:

1. Map probes/transcripts to gene symbols.
2. Collapse multiple probes/transcripts per gene by arithmetic mean within
   sample.
3. Transform raw counts to `log2(CPM + 1)` when counts are available. Use the
   provided normalized log-expression values when the dataset already supplies
   normalized expression.
4. Z-score each gene across all analyzed samples in that cohort.
5. Module score = arithmetic mean of available z-scored module genes.

For single-cell expression:

1. Use annotated APC/myeloid/DC compartments when available.
2. Aggregate to patient-sample-cell-state pseudobulk before scoring.
3. Use the same gene-level scoring rule as bulk expression.
4. If no APC/myeloid/DC annotation is available, score whole-sample pseudobulk
   and mark the cohort as compartment-unresolved.

## Locked Therapy-Class Rule

The V7 rule is not a universal single-feature rule. It is a pre-specified
drug-mechanism-class rule:

### Class A - Inflammatory Input Blockade

Examples: anti-TNF, anti-IL-12/23, anti-IL-23, anti-IL-17, JAK inhibition when
the treatment is intended to reduce inflammatory cytokine signaling.

Primary locked feature:
- Early on-treatment delta IFN/APC, computed as first available on-treatment
  timepoint minus pretreatment baseline.

Predicted responder direction:
- Responders have lower delta IFN/APC than nonresponders.

If no early on-treatment sample exists:
- Use baseline IFN/APC.
- Predicted responder direction: responders have higher baseline IFN/APC than
  nonresponders, reflecting a suppressible inflammatory-input state.

Secondary expected direction, not part of pass/fail:
- HLA-II delta may increase during response, reflecting APC remodeling rather
  than broad suppression.

### Class B - Exogenous IFN / APC-Reprogramming Therapy

Examples: IFN-beta in MS and any therapy whose direct intended mechanism is
immune reprogramming rather than inflammatory-input blockade.

Primary locked feature:
- Early on-treatment delta HLA-II, computed as first available on-treatment
  timepoint minus pretreatment baseline.

Predicted responder direction:
- Responders have higher delta HLA-II than nonresponders.

If no early on-treatment sample exists:
- Use baseline HLA-II.
- Predicted responder direction: responders have higher baseline HLA-II than
  nonresponders, reflecting intact APC reprogrammability or competence.

### Class C - Cell Trafficking, Cell Depletion, or Non-APC-Primary Therapy

Examples: natalizumab, fingolimod, anti-CD20, S1P modulators, pure
cell-trafficking blockade, and therapies where APC state is not expected to be
the primary response axis.

Locked decision:
- These cohorts are out-of-scope for primary validation unless the dataset
  includes a clear APC-relevant pretreatment or early-treatment transcriptomic
  response hypothesis documented before analysis.
- They may be analyzed as exploratory Tier -1 falsification/context cohorts but
  cannot count toward V7 validation success.

## Locked Model

No coefficients are fitted on validation cohorts.

For each validation cohort:

- Compute the primary locked feature for its therapy class.
- The prediction score is the signed feature:
  - Class A early delta: `-1 * delta_IFN_APC`.
  - Class A baseline-only: `baseline_IFN_APC`.
  - Class B early delta: `delta_HLAII`.
  - Class B baseline-only: `baseline_HLAII`.
- Higher prediction score means more likely responder.
- Binary response labels are used as supplied by the cohort or publication.
  If multiple response endpoints exist, use the primary clinical response or
  remission label defined by the study authors.

## Pre-Specified Validation Metrics

Primary metric:
- ROC AUC of the locked prediction score for responder versus nonresponder.

Secondary metrics:
- Hedges g responder-minus-nonresponder in the signed prediction score.
- Welch p value for responder versus nonresponder score difference.
- Bootstrap 95% CI for AUC with `2000` resamples and random seed `20260528`.

## Validation Success Threshold

A cohort-level validation pass requires:

- AUC `>= 0.70`; and
- lower bootstrap 95% CI for AUC `> 0.55` when cohort has at least `30`
  labeled subjects; and
- signed Hedges g `>= 0.50`.

For small cohorts with fewer than `30` labeled subjects:

- AUC `>= 0.70`; and
- signed Hedges g `>= 0.50`; and
- effect direction consistent with the locked rule.

V7 breakthrough validation requires:

- at least `3` independent validation cohorts passing;
- at least `2` autoimmune diseases represented;
- at least `2` therapy classes represented;
- no more than one directly contradictory cohort with AUC `< 0.45` in a
  clearly in-scope therapy class.

## Failure / Kill Threshold

The predictive rule is killed if either condition is met:

- At least `3` independent in-scope validation cohorts fail, including at least
  `2` cohorts with AUC `< 0.55` or signed Hedges g `< 0.20`; or
- receptor-only CD74/CD44/CXCR4 outperforms the locked rule by AUC `>= 0.10` in
  at least `2` independent in-scope cohorts.

If killed, write `KILL_HYP_V6_006.md` and convert failure modes into Tier -1
hypotheses per V6 discipline.

## Causal Mechanism To Test

Locked mechanistic resolution hypothesis:

APC response architecture is causal through **APC plasticity**, not through
static CD74/MIF receptor signaling. Different drug classes reveal different
directions of the same plasticity axis:

- inflammatory-input blockade succeeds when a high inflammatory IFN/APC state
  can be downshifted;
- IFN/APC-reprogramming therapy succeeds when HLA-II/APC competence can be
  induced or maintained;
- receptor-only CD74/CD44/CXCR4 is a trafficking/state readout and should not
  be the dominant predictor.

V7 causal evidence must support at least one of:

- perturbation of IFN/APC or HLA-II regulators changes downstream APC
  architecture in the predicted direction;
- early APC-module change precedes later clinical response in a longitudinal
  validation cohort;
- genetic or pharmacogenetic instruments link APC architecture to response.

## Locked Exclusions

The following are derivation/refinement cohorts and cannot count as V7
independent validation:

- `GSE282122`
- `GSE138064`
- `GSE24427`

The following analyses are forbidden during V7 validation:

- changing module genes;
- changing feature direction;
- adding fitted coefficients to improve validation performance;
- selecting a different endpoint after seeing results;
- dropping an in-scope cohort because it fails.
