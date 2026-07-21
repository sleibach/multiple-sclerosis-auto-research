# V54 Progression Transition Identifiability Plan

Status: frozen before execution.

## Question

Can any held MS dataset identify an RRMS-to-progressive transition or a
molecular state associated with longitudinal disability accumulation?

This is a semantic and coverage audit, not a biological association test.
Cross-sectional subtype differences, repeated treatment samples, relapse
outcomes, pregnancy timepoints, and multiple samples from one postmortem donor
must not be relabeled as progression-transition evidence.

## Required Transition Fields

A dataset is eligible only if all of the following are available and linked at
the subject level:

1. a verified subject identifier;
2. at least two chronologically ordered transcriptomic measurements;
3. MS subtype or transition status assessed at each relevant timepoint;
4. a repeated disability measure, or a prospectively adjudicated conversion
   event with its assessment time;
5. treatment and sampling context sufficient to separate transition from a
   pharmacodynamic change.

Failure of any requirement gives `NOT_IDENTIFIABLE`. Missingness is not a
negative biological result.

## Corpus Scope

The audit will inspect the held progression-adjacent and longitudinal MS
artifacts:

- Macnair discovery microglia;
- GSE180759 and GSE279972 postmortem lesion material;
- GSE228330 ocrelizumab PBMC;
- GSE24427 IFN-beta longitudinal blood;
- GSE17410 MS pregnancy PBMC;
- the held pre/post-ocrelizumab MS microbiome cohort.

For each dataset, the script will record the observed unit count, whether a
verified repeated-subject structure exists, which transition requirements are
present, the safe bounded use, and the exact blocker.

## Interpretation

- `IDENTIFIABLE`: all five requirements are met. A separate frozen statistical
  plan would still be required before testing a molecular association.
- `NOT_IDENTIFIABLE`: one or more required fields are absent. No transition,
  progression-rate, or halting-progression inference is permitted.

The audit cannot establish that no transition biology exists. It can establish
that a given held dataset cannot answer that question without additional
subject-level clinical data.
