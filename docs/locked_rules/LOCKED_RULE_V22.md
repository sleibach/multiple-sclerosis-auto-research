# LOCKED_RULE_V22 - Dynamic APC/HLA-II Treatment-Response Monitoring

Locked timestamp: 2026-06-06 13:49 CEST  
Status: immutable for V22 held-out validation  
Purpose: prospective-style validation of an early treatment-response monitoring
rule, not a baseline stratifier.

## Scientific Question

Does a pre-specified early on-treatment APC/HLA-II module change identify
clinical response in held-out treatment-response transcriptomic cohorts not used
in V6/V7 derivation, validation, or kill decisions?

## Frozen Modules

Gene symbols are frozen exactly as listed. A module is scoreable only if at
least `50%` of its genes are present after platform mapping.

### IFN/APC Module

`STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`

### HLA-II Module

`HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`, `HLA-DQB1`

### Receptor-Only Negative-Control Module

`CD74`, `CD44`, `CXCR4`

The receptor-only module is not part of the predictive rule. It is a
specificity control. A cohort-level pass is downgraded to "non-specific pass"
if receptor-only outperforms the locked score by AUC `>= 0.10`.

## Frozen Feature Type

V22 tests **early on-treatment change only**.

For each subject:

`delta_module = first_available_on_treatment_score - pretreatment_baseline_score`

Baseline-only cohorts are out of scope for V22 primary validation. They may be
listed as inaccessible/out-of-scope but cannot count as validation failures or
successes. This is a deliberate correction from V7, where baseline fallback
failed reproducibly.

Eligible early timepoints:

- Use the earliest post-treatment transcriptomic sample collected at least
  `24 hours` after treatment start and no later than `12 weeks`.
- If multiple eligible early timepoints exist, use the earliest one.
- If the first available post-treatment sample is collected after the primary
  clinical outcome assessment, the cohort is out of scope for causality and can
  only be analyzed as exploratory context.

## Therapy-Class Branching

No coefficients are fitted in validation cohorts.

### Class A - Inflammatory Input Blockade

Examples: anti-TNF, anti-IL-12/23, anti-IL-23, anti-IL-17, and JAK inhibition
when the intended treatment mechanism is suppression of inflammatory cytokine
signaling.

Locked feature:

- `signed_score = -1 * delta_IFN_APC`

Predicted responder direction:

- Responders show a larger decrease in IFN/APC module activity than
  nonresponders.

### Class B - Exogenous IFN / APC-Reprogramming Therapy

Examples: IFN-beta in MS.

Locked feature:

- `signed_score = delta_HLAII`

Predicted responder direction:

- Responders show a larger increase in HLA-II module activity than
  nonresponders.

### Class C - MS Non-IFN DMT / Cell-Trafficking / Cell-Depletion / Broad Immune Rebalancing

Examples: natalizumab, fingolimod/S1P modulators, dimethyl fumarate,
ocrelizumab/anti-CD20, and other MS DMTs whose mechanism is not exogenous IFN
and not direct inflammatory-cytokine blockade.

Locked feature:

- `signed_score = delta_HLAII - delta_IFN_APC`

Predicted responder direction:

- Responders show stronger APC remodeling: HLA-II competence/induction rises
  relative to inflammatory IFN/APC activation.

Rationale locked before validation:

- V6/V7 historical evidence supports early HLA-II induction for MS IFN-beta and
  early IFN/APC downshift for mucosal anti-TNF response. For non-IFN MS DMTs,
  the pre-specified unifying dynamic variable is the balance between HLA-II
  induction/maintenance and inflammatory IFN/APC suppression. This is a
  higher-risk generalization and must be interpreted separately from Class A
  and Class B.

## Scoring

For bulk expression:

1. Map probes/transcripts to official gene symbols.
2. Collapse multiple probes/transcripts per gene by arithmetic mean within
   sample.
3. Transform raw counts to `log2(CPM + 1)` when counts are available. Use
   provided normalized log-expression values when the dataset already supplies
   normalized expression.
4. Z-score each gene across all analyzed samples in the cohort before module
   scoring.
5. Module score = arithmetic mean of available z-scored module genes.
6. Pair baseline and early on-treatment samples by subject ID. Subjects without
   both samples are excluded from primary validation.

For single-cell expression:

1. Prefer annotated APC/myeloid/DC compartments when available.
2. Aggregate to subject-timepoint-cell-state pseudobulk before scoring.
3. If no APC/myeloid/DC annotation is available, score whole-sample pseudobulk
   and mark the cohort as compartment-unresolved.
4. Do not choose a cell state after seeing response association. If multiple
   APC-relevant cell states are present, use the union APC/myeloid/DC
   pseudobulk as the primary score and report cell-state components as
   exploratory only.

## Outcome

Use the primary clinical response, remission, relapse-free, NEDA, EULAR,
PASI75/90, Mayo, CDAI, or study-author-defined binary outcome supplied by the
cohort publication or metadata.

If multiple binary outcomes are supplied, use the primary outcome named by the
study authors. If no primary outcome is named, use the earliest objective
clinical response endpoint after the transcriptomic early timepoint. Do not
switch endpoints after seeing performance.

## Metrics

Primary metric:

- ROC AUC of the locked signed score for responder versus nonresponder.

Secondary metrics:

- Hedges g responder-minus-nonresponder in the signed score.
- Welch p value.
- Bootstrap 95% CI for AUC with `2000` resamples and random seed `20260606`.

## Validation Success Threshold

A cohort-level pass requires:

- AUC `>= 0.70`; and
- signed Hedges g `>= 0.50`; and
- for cohorts with at least `30` labeled paired subjects, lower bootstrap 95%
  CI for AUC `> 0.55`.

For cohorts with fewer than `30` labeled paired subjects:

- AUC `>= 0.70`; and
- signed Hedges g `>= 0.50`; and
- direction consistent with the locked rule.

V22 breakthrough validation requires:

- at least `3` independent held-out cohorts passing;
- at least `1` MS DMT cohort passing;
- at least `2` therapy classes represented among passing cohorts; and
- no more than one directly contradictory in-scope cohort with AUC `< 0.45`.

If the only passes are IBD mucosal Class A cohorts, the verdict is not an MS
breakthrough. It is a narrower mucosal pharmacodynamic monitoring result.

## Failure / Kill Threshold

The V22 rule is killed as a transferable APC/HLA-II treatment-response rule if:

- at least `3` independent in-scope held-out cohorts fail, including at least
  `2` with AUC `< 0.55` or signed Hedges g `< 0.20`; or
- every reachable MS DMT held-out cohort fails; or
- receptor-only `CD74/CD44/CXCR4` outperforms the locked score by AUC `>= 0.10`
  in at least `2` in-scope cohorts.

If killed, write `KILL_V22.md` and convert failure modes to Tier -1
hypotheses.

## Locked Exclusions

The following cohorts cannot count as V22 held-out validation because they were
used in V6/V7 derivation, validation, kill, or refinement:

- `GSE282122`
- `GSE138064`
- `GSE24427`
- `GSE16879`
- `GSE73661_IFX`
- `GSE73661_VDZ_W6_exploratory`
- `GSE8350`
- `GSE12051`
- `GSE12251`
- `GSE138746_CD14`

## Forbidden After Lock

- changing module genes;
- changing therapy-class assignment after seeing validation results;
- adding fitted coefficients;
- replacing early delta with baseline score;
- choosing a different endpoint after seeing validation results;
- dropping an in-scope cohort because it fails;
- counting derivation or V7 validation cohorts as V22 validation.

## Clinical Interpretation If Successful

V22 is a response-monitoring rule unless a held-out baseline-only analysis is
separately pre-registered in a future phase. A validated V22 pass would support
early switching or escalation decisions after initial treatment exposure, not
pretreatment patient selection.
