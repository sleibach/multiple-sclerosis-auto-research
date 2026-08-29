# V57 Paired Myeloid Composition Probe: Frozen Plan

Status: **frozen before outcome analysis**

## Question

Does anti-TNF response in held paired single-cell data associate with a
relative redistribution of myeloid subtypes that cannot be represented by
the within-cell module-distribution probe?

This is a method-feasibility and cross-disease context probe in IBD. It is
not evidence of an MS mechanism and cannot validate the frozen V22 rule.

## Input and Unit of Inference

- Held non-quarantined GSE282122 myeloid single-cell object.
- Pre/post sample pairing is inherited from the audited Wave67 pair contract.
- Only same-batch pairs are eligible.
- Each pre and post sample must contain at least 100 annotated myeloid cells.
- The inferential unit is the patient. Multiple sites for one patient are
  collapsed by the median before outcome testing.

## Frozen Composition

- Categories are the complete observed `final_analysis` annotation levels;
  none are selected by outcome.
- Each sample receives a count vector over all categories.
- A fixed pseudocount of 0.5 is added to every category.
- Counts are closed to proportions and transformed to centered log ratios
  (CLR): log(category proportion / geometric mean of all category
  proportions).
- The primary feature is post-treatment CLR minus pretreatment CLR for each
  category.

## Primary Test

- Compare remission versus nonremission patient CLR changes.
- Preserve the number of remission labels separately within Crohn's disease
  and ulcerative colitis in every permutation.
- Use 200,000 patient-label permutations with seed 57021.
- Use the maximum absolute studentized statistic over the complete category
  family for family-wise error control.
- Report raw and max-T p-values, effect direction in each disease, and sample
  counts.

## Sensitivity Test

For each category, regress CLR change on these pre-outcome covariates without
using response labels:

- disease;
- log pre/post total-cell-count ratio;
- absolute change in the audited inflammation score; and
- baseline CLR abundance of the category.

Repeat the same disease-stratified max-T response-label test on residuals.

## Promotion Gate

A category is response-specific only if all conditions hold:

1. raw max-T p <= 0.10;
2. residualized max-T p <= 0.10;
3. raw and residualized effects have the same sign; and
4. Crohn's disease and ulcerative colitis effects are both estimable and have
   the pooled sign.

The exploratory 0.10 gate is deliberate for triage, but it remains
family-wise corrected. Anything weaker is recorded as not supported or
inconclusive, not promoted.

## Stability

Repeat with seeds 57022 and 57023 using 100,000 permutations each. The
verdict and passing-feature set must be unchanged.
