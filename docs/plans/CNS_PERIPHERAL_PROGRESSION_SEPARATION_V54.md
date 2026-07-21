# V54 CNS-Versus-Peripheral Progression Separation Plan

Status: frozen before execution.

## Question

Can the held corpus distinguish a CNS-resident progression-associated state
from a peripheral immune-tone state?

This is an identifiability question before it is an expression question. A
brain association and a blood association can be compared only if they encode
the same clinical contrast with independently verified subjects and adequate
control of source, activity, treatment, and cell composition. Otherwise a
cross-compartment difference can be created by phenotype or design mismatch.

## Permitted Claims

Two nested claims are defined:

1. **Cross-sectional stage localization**: the same frozen module is associated
   with the same cross-sectional stage contrast in one compartment but not the
   other, with adequate precision and a formal compartment-by-stage test.
2. **Progression localization**: the same module predicts subsequent disability
   accumulation or adjudicated progression differently by compartment.

The second claim requires longitudinal disability or conversion outcomes. A
cross-sectional PPMS-versus-SPMS contrast, lesion morphology, relapse, and
treatment pharmacodynamics are not substituted for disability accumulation.

## Frozen Eligibility Contract

A compartment pair is eligible for a cross-sectional stage-localization test
only if all of the following hold before module scores are inspected:

1. The CNS and peripheral datasets encode the same stage contrast and compatible
   sampling semantics.
2. Each compartment has at least 10 verified independent subjects per stage.
3. A verified sample-to-subject map is available.
4. Processed expression and the frozen module genes are available.
5. Acquisition source or batch, inflammatory activity, and treatment are either
   balanced or explicitly modeled without rank deficiency.
6. Cell composition is measured or estimated with a pre-specified adjustment.
7. The test includes a formal compartment-by-stage interaction or an equivalent
   cross-cohort difference with uncertainty; a significant result in one cohort
   and a null in another is not a difference.

A progression-localization test additionally requires repeated disability or an
adjudicated conversion event linked to molecular measurements and treatment
context. No held dataset may receive a progression-localization label without
that endpoint.

The minimum of 10 subjects per stage is an eligibility floor, not a claim of
adequate power. Confidence intervals and null tests remain mandatory.

## Candidate Audit

The executable audit covers every held progression-adjacent compartment:

- Macnair source-restricted postmortem microglia PPMS versus SPMS;
- GSE180759 and GSE279972 postmortem lesion-state material;
- GSE228330 peripheral PBMC baseline RRMS versus SPMS metadata;
- GSE24427 longitudinal peripheral blood under IFN-beta.

For GSE228330, the baseline subtype-by-activity and subtype-by-sex tables are
computed directly from committed public metadata and tested with two-sided
Fisher exact tests. Public raw CEL/CHP availability does not repair a failed
clinical-design gate, so no large raw files are downloaded solely to manufacture
an ineligible comparison.

## Frozen Verdict Logic

- `ELIGIBLE_FOR_CROSS_SECTIONAL_SEPARATION`: at least one CNS/peripheral pair
  passes all seven cross-sectional requirements.
- `ELIGIBLE_FOR_PROGRESSION_SEPARATION`: a pair passes the cross-sectional gate
  and both compartments have the required progression outcome.
- `CNS_VS_PERIPHERAL_PROGRESSION_LOCALIZATION_NOT_IDENTIFIABLE`: no pair passes.

Failure of this gate is a coverage/design boundary. It is not evidence that a
CNS-specific state, peripheral state, or shared state is absent. In particular,
the absence of an eligible peripheral test cannot be reported as a peripheral
null, and brain pathology associations cannot be called CNS-intrinsic merely
because no comparable blood result exists.

