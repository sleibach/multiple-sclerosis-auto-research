# V56 HERCULES Vivli Request And Frozen Analysis Sketch

Status: draft controlled-access request, not submitted and not approved.

Boundary: `external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://clinicaltrials.gov/study/NCT04411641.

## Why This Request

The project has no grounded progression treatment or progression biomarker. A
new V56 analysis of 10 rapid and 10 slow untreated SPMS blood profiles found no
family-wise-supported signal across nine frozen modules. A broad-rim lesion
analysis remains acquisition- and reconstruction-bounded. Another
cross-sectional scan is therefore not a defensible route to treatment impact.

- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://pubmed.ncbi.nlm.nih.gov/40202696/] HERCULES is a randomized, placebo-controlled progression-treatment trial with 1,131 participants and a positive 6-month confirmed-disability-progression primary result.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://download.open.fda.gov/crl/CRL_NDA219624_20251223.pdf] The FDA review identified substantial uncertainty about benefit across baseline inflammatory-activity and prior-treatment strata and a serious compound-level liver risk.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT04411641] The registry says qualified researchers may request anonymized participant-level data and related documents through Vivli.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/SAP_001.pdf] Public trial documents list baseline and longitudinal disability/MRI data, plasma NfL, serum CHI3L1, immunoglobulins, pharmacokinetics, and a lymphocyte-phenotyping subset; actual shared fields and timepoint completeness must be confirmed in the approved data dictionary.

The request is for transparent reproduction, a same-trial consistency audit of
prespecified effect modifiers, and parallel efficacy/safety uncertainty. It is
not a request to mine a new molecular target or declare a favorable-benefit
subgroup.

## Proposed Request Title

**Reproduction and same-trial consistency of prespecified clinical, MRI, and
biomarker effect modifiers in HERCULES**

## Research Questions

1. Can the published intention-to-treat treatment effect on 6-month confirmed
   disability progression be reproduced from shared participant-level data
   using the final public statistical analysis plan?
2. Are the prespecified baseline gadolinium-activity and prior-DMT interactions
   consistent across fixed 24-month absolute-effect, influence, bootstrap, and
   missing-data analyses within the same trial?
3. If baseline NfL and CHI3L1 are sufficiently complete, does either show a
   same-trial treatment interaction beyond the prespecified clinical/MRI
   covariates under one study-wide multiplicity family?
4. Can any apparent benefit stratum be described alongside, rather than
   separately from, the observed liver-safety burden without building an
   underpowered toxicity classifier?

## Requested Data And Documents

### Trial reproduction

- randomized arm, randomization date, region, age stratum, and analysis
  population flags;
- every EDSS assessment date and value, relapse dates/adjudication, 3- and
  6-month confirmation flags, death date/cause category, withdrawal, and last
  follow-up;
- final imputation flags and enough source fields to recreate the SAP-defined
  event/censoring algorithm;
- protocol, amendments, final SAP, annotated case-report form, data dictionary,
  dataset specifications, and clinical study report.

### Candidate effect modifiers

- baseline and historical gadolinium-enhancing activity, with MRI dates and
  explicit missingness reason;
- baseline EDSS, years from RRMS symptom onset, relapse history, and disease-
  course fields;
- every prior DMT, start/stop date, washout, and derived prior-therapy count;
- baseline plasma NfL and serum CHI3L1, assay batch, lower limit, units, and
  collection date;
- longitudinal NfL/CHI3L1 only with collection dates, to preserve temporal
  order in any landmark analysis;
- lymphocyte subsets, CD19-positive B cells, immunoglobulins, assay batch, and
  subset-selection mechanism;
- tolebrutinib and M2 pharmacokinetic fields and sampling times, if approved.

### Outcomes and safety

- T25FW, 9HPT, SDMT, CVLT-II, MSQoL-54, and their assessment dates;
- new/enlarging T2 lesions, baseline and serial gadolinium lesions, brain
  volume, and slowly expanding lesion outputs if shared;
- exposure, adherence, treatment interruption/discontinuation, crossover, and
  open-label timing;
- ALT, AST, bilirubin, alkaline phosphatase, laboratory upper limits, testing
  dates, adverse events, serious adverse events, Hy's-Law adjudication fields,
  and liver-monitoring intervention dates.

No RNA-expression or CSF field is assumed to exist in the standard clinical IPD
package. The public protocol separately describes the ToleDYNAMIC substudy;
omics and functional data require an explicit request under
`V56_TOLEDYNAMIC_ACCESS_AND_TEST_PLAN.md`. If that package is not approved, no
APC/HLA-II or other project module will be tested in HERCULES.

## Frozen Analysis Order

The following order is committed before participant outcomes are visible.

### Gate 0: package and temporal audit

1. Verify participant counts, randomized ratio, event count, follow-up range,
   missingness, open-label switches, and variable definitions against the CSR.
2. Produce no efficacy result if event timing or treatment assignment cannot be
   reproduced from source fields.
3. Confirm sponsor/Vivli disclosure thresholds before producing subgroup
   tables; analyses may run in the secure environment even when a small cell
   cannot be exported.
4. Exclude no participant beyond the SAP populations; report every discrepancy.

### Gate 1: exact primary reproduction

Reproduce the ITT treatment-policy estimand:

- endpoint: time from randomization to onset of 6-month EDSS-confirmed
  disability progression;
- model: robust-variance Cox regression with treatment, age stratum, region,
  baseline EDSS, and baseline gadolinium-enhancing T1 lesions;
- companion test: age/region-stratified log-rank;
- event/censoring and multiple-imputation handling: final SAP verbatim,
  including seed `16645`, `1,000` imputations, and Rubin pooling;
- pass criterion: randomized count and primary event count match the CSR, and
  the hazard ratio plus both 95% CI limits round to the published two decimal
  places. No undocumented transformation or analyst-selected tolerance can
  convert a mismatch into a pass.

Failure ends all effect-modifier analyses until the sponsor or data dictionary
reconciles the discrepancy. A transparent alternate endpoint may be reported
as a methods discrepancy, but it cannot unlock downstream treatment-selection
claims.

### Gate 2: two-factor clinical/MRI stability family

Only these two prespecified factors are tested:

1. baseline gadolinium-enhancing T1 lesions: present versus absent;
2. prior DMT count: `0`, `1`, or `>=2`, preserving the SAP categories.

The primary effect-modification estimand is fixed before access: the difference
between treatment-arm **24-month restricted mean progression-free time (RMST)
differences** across modifier levels. It is estimated with 24-month
pseudo-observations and an identity-link model containing treatment, modifier,
treatment-by-modifier, age stratum, region, and baseline EDSS, with robust
variance. For prior DMT, the interaction is one global two-df hypothesis;
pairwise estimates are descriptive.

For each factor, also add factor and treatment-by-factor terms to the Gate-1
Cox model as a SAP-aligned secondary analysis. Report:

- the 24-month RMST interaction contrast, robust 95% CI, nominal p, and
  study-wide Holm-adjusted p;
- Cox interaction coefficient and robust 95% CI as a model-dependent secondary
  quantity, without allowing it to override the RMST result;
- subgroup hazard ratios without interpreting within-subgroup significance as
  interaction;
- Kaplan-Meier 24-month risk and unadjusted RMST difference by arm and modifier
  level;
- cell counts/events, Schoenfeld proportional-hazards diagnostics at `p<0.05`,
  dfbeta influence, and `10,000` bootstraps resampled within treatment-by-age-
  stratum-by-region cells, with bootstrap Monte Carlo error reported;
- sensitivity using censor-at-last-EDSS and potential-onset-as-event definitions
  from the SAP.

This is a same-trial consistency audit, not validation. A factor is merely
flagged for independent replication if its study-wide Holm-adjusted RMST
interaction p is below `0.05`, its stratified-bootstrap interval excludes zero,
the sign survives both SAP missing-data sensitivities, and no single
participant reverses the sign. The permitted label is **same-trial candidate;
independent randomized replication required**.

### Gate 3: two-biomarker exploratory family

Run only if pre-randomization values and assay metadata are present for at least
`80%` of each arm, the standardized difference in the missingness indicator by
arm is below `0.10`, and no assay batch is perfectly nested within arm:

1. log2 plasma NfL, standardized using the pooled baseline distribution;
2. log2 serum CHI3L1, standardized identically.

Each is entered continuously into the same 24-month RMST pseudo-observation
model with a treatment-by-biomarker interaction. The Cox interaction is
secondary. No outcome-derived cutoff, dichotomization, spline search, or
alternative marker substitution is permitted. All four Gate-2/Gate-3
interactions share one Holm family; an unavailable biomarker receives `p=1`
rather than shrinking the family after access.

Complete-case and multiple-imputation results must agree in direction. Use
`50` imputations with seed `16645`; passively construct the treatment
interaction and include treatment, age stratum, region, baseline EDSS,
gadolinium activity, prior-DMT count, disease duration, site, assay batch, event
indicator, and Nelson-Aalen cumulative hazard. Before imputation, report a
fixed missingness model with those baseline predictors. Run a pattern-mixture
delta grid shifting missing biomarker values by `-1`, `-0.5`, `0`, `0.5`, and
`1` baseline SD independently in each arm. Perfect arm/batch nesting or failure
of the coverage/balance gate makes the marker descriptive only and fixes its
inferential p-value to `1`.

An exploratory marker is flagged only if the study-wide Holm p is below `0.05`,
the 10,000-replicate stratified-bootstrap interval excludes zero, every delta-
sensitivity result retains direction, and cross-validated 24-month absolute-
benefit calibration is not worse than the Gate-1 clinical model. The permitted
label is **same-trial exploratory candidate; independent randomized validation
and assay lock required**, never clinical readiness.

Lymphocyte phenotyping is descriptive because the SAP limits it to a subset of
up to 200. It is not used to select patients unless the selection mechanism is
documented, coverage supports the same predeclared gate, and a separate plan is
committed before those values are viewed.

### Gate 4: safety and benefit-risk description

Reproduce arm-level liver laboratory and serious-adverse-event summaries with
exact binomial 95% intervals. Fit no severe-DILI prediction model and make no
favorable-benefit subgroup claim: sparse same-trial safety counts cannot
establish absence of rare severe harm. For each Gate-2 stratum, report efficacy
estimates beside observed liver-event counts and intervals, subject to export
rules; do not combine them into an optimized utility score or choose a post hoc
benefit-risk threshold.

### Gate 5: descriptive landmark pharmacodynamics only

This gate is unavailable unless the approved dictionary contains a common
month-6 biomarker timepoint measured before progression onset, treatment
interruption, dose modification, or protocol-defined liver-monitoring action.
If available, describe month-6 change among participants alive, under
observation, progression-free, and still on uninterrupted assigned treatment
at the landmark. Report every pre-landmark progression, censoring, interruption,
and exclusion by arm. Run no inferential treatment-effect-modifier test; if only
end-of-study values exist, this gate is not run and no alternate landmark is
selected.

## Multiplicity And Analysis Budget

| family | inferential tests | correction |
|---|---:|---|
| Primary reproduction | 1 | reproduction criterion, not a new efficacy claim |
| All baseline modifier interactions | exactly 4, with unavailable tests fixed to p=1 | one study-wide Holm family-wise 0.05 |
| Safety | 0 confirmatory | descriptive intervals only |
| Landmark PD | 0 inferential | descriptive only if the fixed month-6 gate is met |

No other subgroup, molecule, module, cutoff, endpoint composite, or machine-
learning search is permitted in this request. A later question requires a new
time-stamped plan and cannot alter these verdicts.

## Interpretation Grid

| result | permitted interpretation |
|---|---|
| Primary does not reproduce | Shared-package or implementation discrepancy; no downstream result is interpretable |
| Primary reproduces, no flagged interaction | Average randomized effect reproduced; no project-supported selector |
| Clinical/MRI interaction passes consistency screen | Same-trial candidate requiring independent randomized replication; not a treatment rule |
| Biomarker interaction passes consistency screen | Same-trial exploratory candidate requiring independent randomized validation and assay lock |
| Biomarker adds no value | Do not promote molecular stratification from HERCULES |
| Any apparent high-benefit group | No favorable-benefit claim from this reanalysis; report sparse safety uncertainty side by side |

## Controlled-Data Handling

- Store approved data only in the Vivli secure environment or another location
  explicitly permitted by the data-use agreement.
- Commit no participant-level row, restricted document, screenshot, derived
  small cell, or reidentification-sensitive output to this public repository.
- Commit only approved aggregate exports, analysis code, exact environment,
  checksums for exportable artifacts, and a disclosure-safe run report.
- The repository's grounded status applies only after a rerunnable approved
  analysis is completed; this draft and the access statements remain external
  context.

## Human Submission Requirements

Submission requires a qualified researcher, institutional affiliation,
methodologically complete proposal, conflict/funding disclosures, and agreement
to Vivli/Sanofi data-use terms. The project can prepare code and the frozen plan;
an eligible human principal investigator must submit and accept controlled-
access obligations.
