# Data That Would Actually Change The Answer

More data are not automatically better data. A package changes a project
verdict only when its people, timing, outcome, modality, metadata, provenance,
and independence match the question being asked.

This map distinguishes a **decisive package** from a useful near-match. A
near-match may add context; it cannot silently inherit a stronger evidence
role.

## The Short Priority List

| priority | current answer | minimum data that can change it |
|---:|---|---|
| 1 | The APC/HLA-II monitoring score is provisional. | Independent paired baseline/early-treatment expression with compatible response labels and frozen-rule gene coverage. `[M01, A01]` |
| 2 | Progression prediction is not identifiable in the held corpus. | Repeated molecular measurements **before** repeated confirmed-disability outcomes in the same people, with relapse/treatment/source context. `[P01-P05, A02]` |
| 3 | The CD44/CXCR4 microglia state is identity-only for progression. | A microglia-compatible longitudinal progression package; source-balanced donor replication is needed before stronger localization. `[P06, C01-C02]` |
| 4 | KIF21B/GPR25 and PTGER4 remain direction/causal-signal closed. | Signal-specific, cell-relevant causal evidence plus gain/loss functional direction and modality-fit assays. `[G03-G05]` |
| 5 | The coupled APC architecture is context, not a control strategy. | Component-resolved perturbations that discriminate competing causal graphs and directions. `[D01-D02]` |
| 6 | More unconstrained mining of the same corpus is not rational discovery. | Genuinely new people, modality, temporal design, or perturbation evidence with a precommitted held-out role. `[D04-D05]` |

## Package 1: External Monitoring Validation

### Decision it can change

Does the unchanged early-treatment APC/HLA-II score transport to an independent
MS dimethyl-fumarate cohort with the intended outcome? `[A01]`

### Mandatory package components

| component | minimum content | why it matters |
|---|---|---|
| Expression | Sample IDs, feature IDs, values, and feature-to-gene annotation. | Reproduce the frozen modules without outcome-guided replacement. |
| Pairing | Stable person ID, one pretreatment baseline, and an eligible early on-treatment sample. | Preserve within-person change. |
| Outcome | Person-level NEDA-4 label, assessment window, and source definition. | Test the preregistered primary endpoint. |
| Treatment/timing | DMF identity, treatment start, collection date or relative time. | Select the early sample without looking at response. |
| Gene coverage | At least the preregistered scoreability threshold for both frozen modules. | An absent module makes the primary test unscoreable, not negative. |
| Quality/provenance | QC flags, platform/normalization, sample manifest, checksums, and lawful use terms. | Make ingestion reproducible and fail closed. |
| Confound metadata | Batch/site/processing, depth/quality, cell counts, steroid and medication fields where available. | Report the predeclared immune-tone, composition, steroid, and technical audits. |

The full contract and exact timing/coverage rules are frozen in
[`PREREGISTRATION_V42.md`](../validation/PREREGISTRATION_V42.md).

### Near-matches that cannot substitute

- baseline-only expression;
- treatment samples from different people;
- no NEDA-4 mapping or only a paper-level group description;
- response labels inferred after inspecting expression;
- a late sample collected after the outcome window;
- a different therapy treated as the primary DMF validation;
- insufficient module-gene coverage;
- aggregate group means without person-level pairing; or
- a cohort used to tune genes, timing, threshold, or endpoint before being
  called validation.

### What each result changes

| frozen outcome | meaning |
|---|---|
| Clean pass | Stronger evidence for a bounded external monitoring association; clinical utility and target claims still require later work. |
| Raw pass, technical or immune-tone attenuation | A technically or biologically bounded monitor, reported with the attenuation rather than upgraded. |
| Clear fail | The external transport claim narrows or closes under the preregistered interpretation. |
| Inconclusive | Effect and interval inform a future powered cohort; the lead is neither rescued nor killed. |
| Unscoreable/invalid | The package cannot answer the question and is not reported as a biological null. |

Seeded simulations indicate that a very small cohort can remain inconclusive
unless separation is large and labels are clean. Those simulations describe
method behavior, not the effect expected in MS. `[A03]`

## Package 2: Longitudinal Progression Prediction (`P1`)

### Decision it can change

Does a molecular state measured first predict later relapse-independent,
confirmed disability accumulation? The held datasets cannot currently identify
that transition. `[P01, P03]`

### Mandatory design

- Stable participant IDs linking every sample, visit, outcome, treatment, and
  imaging record.
- Molecular baseline before the outcome window and at least one repeated
  molecular timepoint.
- Baseline plus at least two follow-up disability assessments, so transient
  change can be separated from confirmed progression.
- The exact confirmed-disability and/or PIRA definition, adjudication status,
  and raw component measurements rather than an undocumented label alone.
- EDSS dates/values and, where collected, timed-walk and peg-test values.
- Relapse, steroid, infection, treatment, switching, and adherence context.
- Sample-level source/site/batch/QC and measured cell composition or a
  preregistered adjustment path.
- Feature annotation, enough frozen-module coverage, receipt checksums, and
  permitted use.

The operational field contract is
[`PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md`](../validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md).

### Near-matches that cannot substitute

- relapse count without confirmed disability;
- cross-sectional RRMS/SPMS/PPMS labels;
- one disability measurement;
- molecular measurement after the outcome;
- postmortem lesion morphology without living-person clinical time;
- a pharmacodynamic treatment response outcome;
- unmatched brain and blood cohorts; or
- a derived progression label without protocol and raw components.

Fewer than ten independent progression events is descriptive-only under the
current acquisition contract. Ten or more still requires a cohort-specific
power simulation; it is not automatic adequacy.

## Package 3: Compartment Localization (`P2`)

### Decision it can change

Is a progression association enriched in CNS/CSF rather than reflecting a
peripheral immune-tone or composition process? `[A02]`

### Minimum design

Paired blood and CSF from the same longitudinal participants is strongest. The
phenotype, outcome window, timing, treatment/activity context, module coverage,
and source/composition fields must align across compartments. The primary test
is a predeclared compartment-by-outcome interaction with uncertainty.

### What cannot substitute

- “significant in blood, not significant in CSF” without an interaction test;
- unmatched cohorts with different outcomes or stages;
- postmortem tissue alone as localization of a living-person predictor;
- absent comparator data treated as a peripheral null; or
- a PBMC proxy for the microglia-specific CD44/CXCR4 candidate. `[P06]`

## Package 4: Functional Direction (`P3`)

### Decision it can change

After a progression-specific association passes, does selective modulation in
the required direction improve a relevant function without unacceptable
collateral effects? `[P05]`

### Minimum design

- Component-resolved, direction-matched perturbation rather than generic immune
  stimulation or suppression.
- At least two independent primary-human donor contexts.
- Target engagement and the frozen molecular-state readout.
- A justified progression-relevant functional readout.
- Viability, broad immune activation/suppression, host-defense, and off-target
  controls appropriate to the mechanism.
- Dose response, wrong-direction, vehicle/non-targeting, and blinded analysis.

### What cannot substitute

- an AlphaFold pocket without causal and direction evidence;
- a generic inflammatory perturbation;
- one cell line or one donor;
- molecular movement with no functional or safety readout; or
- a perturbation performed before the progression association gate and then
  called a progression target.

Predicted structure may inform assay or modality design. It is not progression,
causal, or intervention evidence by itself.

## Reopening A Direction-Closed Genetics Route

### Decision it can change

Can a real associated region become a direction-resolved therapeutic route?

### Required chain

1. Separate causal signals rather than treating regional overlap as one event.
2. Assign the causal gene with uncertainty in a relevant cell/state.
3. Align alleles and establish whether protection requires decrease, increase,
   restoration, or context-specific modulation.
4. Compare gain and loss in a functional assay.
5. Show a feasible modality can deliver the required sign in the intended
   compartment.
6. Test on-target function and relevant collateral effects.

### What cannot substitute

A receptor family, approved ligand for another purpose, nearby-gene expression,
a literature mechanism, AlphaFold confidence, or model consensus cannot fill a
missing causal/directional link. `[G02-G05]`

## Resolving The Coupled APC Architecture

### Decision it can change

Is a node a controller, a readout, or one passenger in a common-context state?

### Required package

A minimal component-by-direction perturbation matrix in a relevant APC state,
with donor replication, dose, time, viability, broad immune-tone readouts, and
predictions fixed for at least two competing causal graphs.

### What cannot substitute

- correlation-network centrality;
- co-expression recurrence;
- adding coupled features to the same tiny outcome labels;
- a multi-drug story without a non-additive prediction; or
- one perturbation direction when the therapeutic sign is unresolved.

The current architecture remains useful context and assay design input, not a
validated multi-node target. `[D01-D02]`

## Strengthening The Microglia Candidate

Two distinct packages are needed:

1. **Source-balanced identity replication:** independent donors with diagnosis
   not entangled with brain bank/site, a compatible microglial compartment, and
   the exact CD44/CXCR4 identity. This tests whether the bounded MS association
   survives the known source issue. `[C01-C02]`
2. **Longitudinal progression test:** the P1 design above, in a compatible
   compartment, to ask whether that state precedes disability. Only score
   identity transfers; old thresholds, substitute genes, and blood proxies do
   not. `[P06]`

Passing the first does not pass the second.

## What Counts As Genuinely New Discovery Data

After the V41 joint search, a new file is not automatically new information.
Useful novelty could come from:

- new independent participants;
- a previously absent temporal progression design;
- a matched CNS/peripheral compartment pair;
- direction-resolved perturbation or functional readouts;
- new clinical outcomes linked at person and time level; or
- a truly held-out modality with its role declared before fitting.

Re-encoding the same labels, adding another flexible learner, or splitting one
cohort differently does not remove the corpus boundary. `[D04-D05]`

## Intake Questions For Any Proposed Package

1. Which exact decision above can this package change?
2. Are the unit, timing, outcome, modality, and compartment compatible?
3. Is person/sample/time mapping explicit?
4. Are source, batch, treatment, steroid, composition, and QC fields present?
5. Is the package independent of rule development?
6. Are access and use terms verified?
7. What makes the package invalid, unscoreable, or descriptive-only?
8. What result would change the current verdict?

If those questions cannot be answered from metadata, the next action is a
metadata or access request, not analysis.
