# V56 Progressive-BTKI Cross-Trial Replication Plan

Status: pre-data controlled-access plan. No request is approved, no participant
data were read, and no treatment-selector claim is made.

Boundary: `external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://clinicaltrials.gov/study/NCT04411641,
https://clinicaltrials.gov/study/NCT04458051, and
https://clinicaltrials.gov/study/NCT04544449.

## Why Three Trials Are Needed

- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT04411641] HERCULES offers a placebo-controlled nrSPMS derivation setting with EDSS-confirmed progression and baseline NfL/CHI3L1 listed in public documents.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT04458051] PERSEUS offers an independent, placebo-controlled PPMS setting for the same compound and lists EDSS, composite progression, NfL, CHI3L1, MRI, and lymphocyte endpoints.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT04544449] FENtrepid offers an independent BTK inhibitor in PPMS with ocrelizumab as active comparator and lists composite progression, MRI, and blood NfL.

HERCULES alone can only generate a same-trial candidate. PERSEUS can falsify or
bound same-compound transport across disease phenotype. FENtrepid can test
independent-compound differential response relative to an active comparator.
Those are different estimands and must not be pooled as if interchangeable.

## Fixed Trial Roles

| trial | role | comparison | permitted conclusion |
|---|---|---|---|
| HERCULES | derivation and same-trial consistency | tolebrutinib vs placebo in nrSPMS | candidate modifier only |
| PERSEUS | independent same-compound phenotype test | tolebrutinib vs placebo in PPMS | replication, phenotype-specific failure, or inconclusive |
| FENtrepid | independent-compound active-comparator triangulation | fenebrutinib vs ocrelizumab in PPMS | differential comparative-response context only |

The trials are never combined until each reproduces its own primary analysis.

## Harmonized Endpoint

The cross-trial endpoint is fixed to **24-month EDSS-only 6-month confirmed
disability progression-free time** because it is the HERCULES primary endpoint
and a listed PERSEUS secondary endpoint. Composite progression remains each
PPMS trial's own primary context but is not substituted into the cross-trial
replication.

For FENtrepid, EDSS-only 24-week CDP is requested and used only if the approved
dictionary supports exact reconstruction. If not, FENtrepid cannot enter the
harmonized replication and remains a descriptive active-comparator context.

The effect scale is the 24-month treatment-arm difference in restricted mean
progression-free time. Hazard ratios are secondary because non-proportionality
and different comparator hazards can make them difficult to transport.

## Frozen Modifier Family

Exactly four baseline interactions are carried forward from the HERCULES plan:

1. baseline gadolinium-enhancing T1 lesion status;
2. prior-DMT count (`0`, `1`, `>=2`), only where categories have semantic and
   coverage equivalence;
3. log2 baseline plasma/blood NfL, continuously standardized within trial;
4. log2 baseline serum CHI3L1, continuously standardized within trial.

No alternate biomarker replaces an unavailable one. CHI3L1 is unavailable in
FENtrepid unless the controlled dictionary proves otherwise; its test is then
absent from that trial rather than substituted.

## Analysis Sequence

### 1. Trial-local reproduction

Reproduce each trial's randomized primary analysis under its own SAP. A trial
with a failed reproduction cannot contribute any modifier result.

### 2. HERCULES candidate flag

Apply the frozen V56 HERCULES plan. All four modifiers share one Holm family.
Only modifiers clearing the same-trial RMST consistency screen proceed, with
their model, coding, assay transform, and direction locked.

### 3. PERSEUS independent test

Apply the locked HERCULES modifier without coefficient refitting beyond the
trial-local baseline covariates needed for the prespecified 24-month RMST
interaction. The replication family contains only HERCULES-flagged modifiers,
but its alpha is `0.05 / 4 = 0.0125` per modifier regardless of how many were
flagged; this prevents derivation-based family shrinkage.

A modifier replicates only if:

- the interaction direction matches HERCULES;
- the PERSEUS 98.75% CI excludes zero on the 24-month RMST interaction scale;
- `10,000` randomization-stratified bootstraps retain direction in at least
  `95%` of replicates;
- missingness, assay-batch, influence, and fixed delta sensitivities pass; and
- the result is not driven solely by a disease-phenotype coding difference.

Failure is reported as `does_not_transport_to_PPMS`, not as proof the HERCULES
effect is false. A wide interval is `inconclusive`, never a directional rescue.

### 4. FENtrepid triangulation

Test only modifiers available with matching baseline semantics. The contrast is
fenebrutinib minus ocrelizumab, so a result cannot confirm placebo-controlled
BTK efficacy. A matching NfL interaction would support an independent-compound
comparative-response candidate; a null could reflect equal benefit in both
active arms and does not falsify BTK biology.

Use the same `0.0125` per-modifier threshold and 24-month RMST scale if an exact
EDSS-only endpoint is reconstructible. Otherwise report no harmonized
interaction.

### 5. Cross-trial heterogeneity

Only after trial-local results are frozen, estimate trial-by-treatment-by-
modifier interaction on the common endpoint. Lead with effect estimates and
intervals, not a pooled average. Do not pool across placebo and ocrelizumab
comparators. HERCULES-versus-PERSEUS heterogeneity answers phenotype
transportability; FENtrepid remains a separate active-comparator triangle.

## Safety Boundary

Tolebrutinib liver safety is analyzed jointly across HERCULES and PERSEUS only
as prespecified descriptive incidence with exact intervals and exposure time.
No rare-event subgroup classifier and no favorable-benefit threshold is fit.
Fenebrutinib safety is not pooled with tolebrutinib because compound-specific
chemistry and monitoring differ.

## Verdict Vocabulary

| result | allowed label |
|---|---|
| HERCULES only passes | same-trial candidate; not validated |
| HERCULES + PERSEUS pass | same-compound cross-phenotype replication candidate; still not a clinical rule |
| HERCULES passes, PERSEUS precise opposite/null | does not transport to PPMS |
| PERSEUS interval wide | independent trial inconclusive |
| FENtrepid agrees | independent-compound active-comparator triangulation |
| molecular variables absent | molecular route untestable; do not substitute |

## Access And Human Dependency

Both Sanofi trials state an IPD-sharing route through Vivli. FENtrepid points to
Roche's controlled sharing process. Eligibility, timing, actual field coverage,
and export rules must be confirmed by the sponsors/platforms. Submission
requires a qualified human principal investigator and institutional agreement;
controlled participant data must remain outside the public repository.

This plan creates a real falsification route for a treatment selector. It does
not make the selector exist before data access, and it does not turn trial
availability into evidence for a project mechanism.
