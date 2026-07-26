# Confound Check: A Quick Reference

A confounder is a competing explanation that can move both the proposed signal
and the outcome. The safest time to detect one is before interpreting a
biological contrast.

This card translates the project's V32 immune-tone audit and V53 brain-bank
correction into a reusable workflow. It adds no new scientific claim.
`[M04, C01-C02]`

## The 60-Second Screen

Before running a model, ask:

1. **Who or what is the independent unit?** Person/donor, not thousands of
   cells from the same donor.
2. **Did outcome groups come from the same places and times?** Cross-tabulate
   outcome against site, source, bank, batch, platform, collection period, and
   processing route.
3. **Does every source contain both outcome groups?** If not, adjustment may
   not separate source from outcome.
4. **Was the signal measured before the outcome?** If not, direction is
   ambiguous.
5. **Could treatment, steroid exposure, inflammation, metabolism, cell mix, or
   technical quality move both variables?** Name the plausible alternatives
   before testing.
6. **Are the required metadata actually present?** A missing exposure field is
   not the same as a measured negative.

If any answer is unknown, record the gap before biological interpretation.

## The Confound Map

| competing explanation | first diagnostic | stronger check | unsafe shortcut |
|---|---|---|---|
| Source/site/brain bank | Outcome-by-source counts and association strength | Within-source effects, source-adjusted model, leave-one-source-out | “Include source as a covariate and move on.” |
| Batch/platform | Outcome-by-batch counts; score/batch plots | Blinded batch diagnostics and guarded sensitivity | Correct after choosing the favorable result. |
| Baseline state | Signal versus baseline module/state | Model early change beside baseline | Treat baseline difference as treatment response. |
| Steroid exposure | Recorded exposure timing and dose | Exposure-aware analysis plus expression signature sensitivity | Call a signature score measured steroid use. |
| Broad immune tone | Inflammatory, metabolic, IFN/STAT1 panels | Raw and adjusted signal, held-out or cross-validated comparison | Adjust away overlapping biology and call the residue “pure.” |
| Cell composition | Direct counts where available; marker panels otherwise | Measured proportions or validated deconvolution, within-compartment analysis | Call marker scores complete deconvolution. |
| Donor repetition | Cells/samples per donor | Donor pseudobulk, clustered uncertainty, within-donor contrasts | Count cells as independent people. |
| Timing/follow-up | Outcome and sampling timeline | Fixed eligible window and event-time logic | Pick the most favorable timepoint. |
| Missing attendance/censoring | Visit and dropout table | Sensitivity to informative observation | Assume missing visits are random without evidence. |

## Step 1: Detect Entanglement

### Build The Label-Source Table

For every outcome and candidate confounder, count independent units in each
cell:

```text
                 outcome A     outcome B
source 1              ?             ?
source 2              ?             ?
```

Empty or sparse cells mean the desired comparison may not exist. In the V53
Macnair discovery partition, one brain bank contributed 27 MS donors and no
controls, while another contributed 18 controls and one MS donor. Disease and
source association reached Cramer's V `0.773`. `[C02]`

That was a design warning, not an MS effect size.

### Draw The Timeline

Place baseline, exposure, treatment, early sample, outcome, relapse, steroid,
switch, missed visit, and censoring dates on one line. A variable measured
after the outcome cannot be treated as its predictor.

### Separate Measured From Proxied

State whether each confounder is:

- directly recorded;
- measured by a validated method;
- approximated by a marker or expression signature; or
- absent.

In V32, direct steroid-exposure metadata were absent. A glucocorticoid-response
expression signature was tested, but that is not the same measurement. `[M04]`

## Step 2: Test The Competing Explanation

Minimum reporting should include:

1. The confounder's association with the proposed signal.
2. The confounder's association with the outcome.
3. The unadjusted signal-outcome effect and uncertainty.
4. The adjusted effect and uncertainty.
5. A confounder-only versus confounder-plus-signal comparison using a
   small-sample-aware held-out or cross-validated route when predictive.
6. A permutation or other appropriate null under the design.
7. Within-source and leave-one-source-out direction when source is relevant.
8. Direct acknowledgement when overlap is too weak for adjustment to identify
   the intended effect.

Do not choose the adjustment set after seeing which one preserves the claim.

## Step 3: Use The Right Verdict

### Survives

The signal retains its pre-specified effect under the named adjustment and
uncertainty rule. This strengthens only that confound check; it does not prove
all confounding absent.

### Attenuates

The effect weakens materially but does not meet the rule for being explained
away. Report raw and adjusted results and narrow the interpretation.

The V22 monitor survived the tested steroid-response-signature and simple
cell-composition panels, but broad metabolic/inflammatory/STAT1 adjustment
attenuated it. It remains immune-tone bounded. `[M04]`

### Explained Away Under The Tested Model

The adjusted result crosses the pre-specified explained-away boundary. Report
that directly. Do not search for a favorable alternative model unless it was
precommitted as a sensitivity with its own correction.

### Source-Sensitive

The result depends materially on acquisition source. Preserve any independent
bounded support, but do not let a favorable pooled result override the
source-aware failure.

In V53, the score was positive before source adjustment and attenuated to wild
`p=0.245` with source fixed effects in the affected discovery partition.
The retained state association therefore requires source-balanced replication.
`[C01-C02]`

### Invalid Or Not Identifiable

Outcome and source lack enough overlap, timing is incompatible, metadata are
missing, or the design cannot distinguish the proposed effect. No biological
verdict is allowed.

## The Seven Fail-Closed Warnings

Stop or downgrade interpretation when:

1. One source nearly determines the outcome label.
2. There is no within-source comparison for a key group.
3. Cells, lesions, or repeated samples are counted as independent donors.
4. A proxy is described as direct exposure or measured composition.
5. Adjustment choices were selected after viewing outcome associations.
6. A favorable pooled result reverses or disappears across sources.
7. Missing timing or outcome data are silently treated as negative observations.

## What Adjustment Cannot Do

Adjustment cannot:

- create controls inside a source that supplied none;
- repair unknown sample swaps or undocumented processing;
- turn an expression signature into exposure metadata;
- prove the remaining association is causal;
- guarantee transport to another site or population; or
- rescue an analysis whose independent unit or time order is wrong.

The prospective design should remove the largest confounds by construction,
then use adjustment as a sensitivity rather than a substitute for overlap.

## A Copy-Ready Confound Plan

Complete this as a design plan before inspecting the outcome. Do not include
personal records, credentials, or private row-level data in a public issue.

```text
Independent unit:
Outcome and timing:
Candidate signal and measurement time:
Sources/sites/batches/platforms:
Outcome-by-source counts:
Directly measured confounders:
Proxy confounders and limitations:
Unadjusted model and null:
Adjusted model(s), frozen before outcomes:
Within-source / leave-source-out checks:
Decision rules: survives / attenuates / explained / source-sensitive / invalid
Condition that stops interpretation:
Safety check: no personal/private data or credentials in the public plan
Evidence limit: a plan is not a result; an invalid/data-blocked run has no biological grade
```

## Trace The Evidence

- [V32 monitoring-signal confounder audit](../workups/treatment_response/CONFOUNDER_AUDIT_V32.md)
- [V53 source-balance addendum](../validation/MS_MICROGLIA_SOURCE_BALANCE_ADDENDUM_V53.md)
- [Brain-bank confounding case study](CASE_STUDY_BRAIN_BANK_CONFOUND.md)
- [Claim-source contract](CLAIM_SOURCE_MATRIX_V55.md), rows `M04` and
  `C01-C02`
