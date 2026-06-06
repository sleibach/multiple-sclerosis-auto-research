# ROADMAP V7 - Causal Validation of APC Response Architecture

Started: 2026-05-28 21:31 CEST

## Objective

Advance or kill `HYP_V6_006`: APC response architecture as a cross-autoimmune
treatment-response stratifier.

V7 requires both:

- locked predictive validation on independent cohorts not used in V6;
- causal/mechanistic evidence resolving why anti-TNF points to IFN/APC
  downshift while IFN-beta points to HLA-II competence or induction.

## Locked Rule

The immutable rule is in `LOCKED_RULE_V7.md`. `GSE282122`, `GSE138064`, and
`GSE24427` are excluded from V7 validation because they informed the lock.

## Workplan

### Step 1 - Lock Complete

Files:
- `LOCKED_RULE_V7.md`
- `ROADMAP_V7.md`

### Step 2 - Validation Cohort Acquisition

Search/acquire independent cohorts:

- IBD anti-TNF baseline or longitudinal response transcriptomics.
- RA anti-TNF, JAK, abatacept, rituximab, or other biologic response cohorts.
- Psoriasis IL-23/IL-17/TNF biologic response cohorts, including `GSE228421` if
  processed data are usable.
- Additional MS DMT cohorts not `GSE138064` or `GSE24427`.

Each cohort goes into `VALIDATION_LEDGER.md` and `data/manifest.tsv`.

### Step 3 - Apply Locked Rule

For every acquired cohort:

- classify therapy class before analysis;
- apply `LOCKED_RULE_V7.md` exactly;
- record AUC, bootstrap CI, Hedges g, p value, and pass/fail;
- do not retune modules or directions.

### Step 4 - Conserved-Component Resolution

Test whether the consistent variable is:

- APC plasticity;
- therapy-class-specific IFN/APC downshift versus HLA-II induction;
- compartment-specific APC state;
- or a false pattern that fails validation.

### Step 5 - Causal Direction

Use at least one:

- perturbation data for APC regulators;
- longitudinal precedence in validation cohorts;
- genetic/pharmacogenetic evidence.

### Step 6 - Synthesis Or Kill

If breakthrough criteria are met, write `FINDING_V7.md`.

If validation fails and mechanism does not resolve, write
`KILL_HYP_V6_006.md`, then generate Tier -1 failure-mode hypotheses and continue
to the next candidate.

## First Cohort Targets

Priority order:

1. Additional IBD anti-TNF bulk or single-cell response cohorts.
2. RA anti-TNF or biologic response cohorts.
3. Psoriasis biologic response, especially IL-23 blockade.
4. Additional MS response cohorts excluding V6 derivation datasets.

## Logging

- `VALIDATION_LEDGER.md`: one row per cohort.
- `meta/CONVERGENCE_CHECK_V7_01.md`: due after first validation attempts.
- `meta/LAB_NOTEBOOK.md`: append every decision and failed route.
