# V54 Progression Cohort Acquisition Specification

Status: operational data-request contract. This document adds no biological
finding and does not create a new discovery analysis. Any received package must
be quarantined, audited, and pre-registered before expression scores are viewed.

## Decision The Data Must Support

The north-star decision is whether a molecular state predicts or mediates
relapse-independent disability accumulation and whether it identifies a safe,
direction-matched intervention route. The held corpus cannot answer that
question because it has no transcriptomic dataset linking repeated molecular
measurements to repeated disability or adjudicated conversion.

The requested data must support three distinct roles. A package is never
silently promoted from one role to another:

| role | required question | minimum design identity | current blocker |
|---|---|---|---|
| `P1_longitudinal_progression` | Does a frozen state precede disability accumulation? | verified repeated subjects, molecular time, repeated disability/adjudicated progression, treatment and relapse context | zero held datasets have the complete link |
| `P2_compartment_localization` | Is an association CNS/CSF-enriched rather than a peripheral immune-tone proxy? | same subjects or harmonized phenotype in CNS/CSF and blood, formal compartment interaction, composition/source controls | zero eligible compartment pairs |
| `P3_functional_direction` | Does selective modulation improve a progression-relevant function without harmful collateral? | component-resolved perturbation in independent primary-human contexts with functional and safety readouts | zero direction-resolved selective control nodes |

## Package P1: Longitudinal Progression Cohort

### Required participants and timing

- Living participants with a verified MS diagnosis and recorded disease course
  (`RRMS`, `SPMS`, or `PPMS`) at each clinical visit.
- Stable subject identifier linking all samples, visits, imaging, outcomes, and
  treatment records.
- Molecular baseline before the outcome window and at least one repeated
  molecular timepoint. Collection date and days from baseline are required.
- Repeated clinical assessment over a pre-declared outcome window. At least
  baseline and two follow-up assessments are required to distinguish transient
  change from confirmed progression.
- Exact protocol definition and adjudication status for confirmed disability
  progression and/or PIRA. The project requires raw component measurements and
  does not accept an undocumented derived label alone.

### Required disability and activity fields

- EDSS value, assessment date, assessor/blinding status if available, and
  whether the change was subsequently confirmed;
- timed 25-foot walk and 9-hole peg test values where collected;
- relapse dates, relapse onset/recovery, and the protocol's relapse-exclusion
  window used for PIRA;
- corticosteroid dates/dose and acute infection dates;
- treatment name, start/stop dates, infusion/dose dates, switch reason, and
  adherence where available;
- MRI acquisition dates and protocol; new/enlarging T2 and enhancing lesions;
- if available, susceptibility/QSM/SWI-derived paramagnetic-rim or slowly
  expanding lesion identifiers, reader method, and longitudinal persistence.

Relapse count alone is not a progression endpoint. Cross-sectional PPMS versus
SPMS is not a progression rate. Lesion morphology without clinical time is not
disability accumulation.

### Required molecular package

- raw counts or documented normalized expression matrix;
- stable feature identifiers and gene annotation/version;
- sample-level QC, sequencing/array batch, processing date, site, lane/plate,
  library depth, mapping rate, RIN or equivalent;
- PBMC differential counts or single-cell cell-type counts sufficient to
  separate composition from within-cell state;
- enough coverage to score the frozen project modules without replacing absent
  genes post hoc;
- original files, checksums, data-use terms, and an immutable receipt manifest.

Preferred modality is single-cell RNA plus surface protein or sorted-cell
expression, because V54 could not separate broad state from component-specific
biology. Bulk blood remains useful only with measured or pre-specified cell
composition adjustment.

### Pre-data analysis requirement

Before any module score is viewed, the project must freeze:

1. one primary progression endpoint and exact outcome window;
2. one molecular baseline and one primary molecular change/timepoint;
3. event censoring, treatment-switch handling, relapse/steroid exclusion, and
   missing-data rules;
4. covariates and the analysis-count/multiple-testing budget;
5. a power simulation using the received sample count, event rate, missingness,
   and repeated-measures structure;
6. pass, fail, and inconclusive thresholds.

No universal powered sample size is asserted from the current corpus. Fewer
than 10 independent progression events is automatically descriptive-only; 10
or more events still requires the pre-data power simulation and does not imply
adequacy.

## Package P2: Paired Compartment Localization

The strongest design is paired blood and CSF from the same longitudinal P1
participants. Tissue from a separate postmortem cohort may provide pathology
context but cannot alone localize a living-person progression predictor.

Required:

- the same clinical phenotype and outcome window in both compartments;
- verified subject pairing and sample timing;
- at least 10 independent subjects in each compared stage/outcome group per
  compartment as the V54 eligibility floor, followed by a power analysis;
- source/site/batch, activity, treatment, age, sex, and cell-composition fields;
- frozen module coverage in both compartments;
- a pre-specified compartment-by-outcome interaction with uncertainty.

A significant blood result and a null CSF result, or vice versa, is not by
itself evidence of a compartment difference. An absent eligible comparator is
not a peripheral null and does not make a brain association CNS-intrinsic.

## Package P3: Functional Direction

Only a candidate that first passes a progression-specific association gate is
eligible for this package. The assay must include:

- a component-resolved, direction-matched perturbation rather than generic
  immune stimulation or suppression;
- at least two independent primary-human donor contexts;
- target engagement and the frozen molecular state;
- a progression-relevant functional readout such as myelin-debris clearance,
  remyelination support, neuroaxonal injury, or a justified cellular surrogate;
- viability, broad immune activation/suppression, antiviral/host-defense, and
  off-target readouts appropriate to the mechanism;
- dose-response, wrong-direction control, vehicle/non-targeting control, and
  blinded analysis;
- a direction-matched modality assessment only after the biological gates pass.

AlphaFold prediction context may inform the final modality assessment. It is
never causal, progression, or intervention evidence by itself.

## Intake Decision Table

| package state | safe action |
|---|---|
| P1 complete, outcome/event count power-eligible | freeze cohort-specific pre-registration while blinded, then run |
| P1 complete but underpowered | effect-size/CI planning only; no definitive progression claim |
| repeated expression but no repeated disability/adjudicated event | pharmacodynamic or temporal context only |
| disability label without raw components/protocol definition | request clarification; do not score progression |
| P2 complete | run formal compartment interaction under a frozen plan |
| unmatched CNS and blood phenotypes | context-only; no localization claim |
| P3 perturbation before progression association | mechanism context only; no target promotion |
| missing subject map, batch, treatment, relapse/steroid, or composition fields | fail closed or request addendum; never reinterpret as a null |

## Exact First Request

> Please provide a de-identified sample-to-subject and visit map linking raw or
> documented normalized expression to repeated EDSS and any T25FW/9HPT values,
> confirmed disability progression/PIRA labels with the exact protocol
> definition, relapse/steroid/infection dates, full DMT history, MRI timing and
> chronic-active/paramagnetic-rim lesion measures if available, cell counts,
> technical batch/QC, and paired CSF samples if collected. Please include raw
> outcome components even when derived labels are supplied.

## Traceability

This specification directly closes gaps established by:

- `analysis/v54_transition_identifiability/REPORT.md`;
- `analysis/v54_cns_peripheral_identifiability/REPORT.md`;
- `analysis/v54_progression_intervention_direction_map/REPORT.md`;
- `analysis/v54_progressive_stage_modules/REPORT.md`;
- `analysis/v54_progression_lesion_state/REPORT.md`;
- `analysis/v54_foamy_state_lesion_stratum_transport/REPORT.md`.

The machine-readable field contract is
`docs/validation/input_schemas/V54_progression_cohort_required_fields.tsv`.

