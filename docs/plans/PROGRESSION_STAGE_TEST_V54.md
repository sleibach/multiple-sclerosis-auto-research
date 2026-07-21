# V54 Cross-Sectional Progressive-Stage Test Plan

Status: frozen before running the V54 stage-test implementation. This plan is
targeted re-examination of pre-existing module scores, not open discovery.

## Question

Do any of five existing microglial module scores differ between SPMS and PPMS
after restricting the Macnair discovery package to source/tissue strata where
both stages are represented?

This is a cross-sectional disease-stage association. It cannot identify
RRMS-to-SPMS transition, progression rate, treatment response, causality, or a
means of halting progression.

## Cohort And Frozen Restrictions

- Input: the already-generated Macnair discovery sample scores and deposited
  source-family map.
- Include PPMS and SPMS only.
- Include only source families containing both stages: Amsterdam BB and UK MS
  Tissue Bank.
- Within Amsterdam, include white-matter samples only.
- Within UK, include grey-matter samples only.
- Exclude Edinburgh because it contains one SPMS donor and no PPMS donor.
- One inferential unit per donor after nuisance adjustment and donor averaging.

The tissue restriction prevents the UK grey-matter-heavy PPMS samples from
being compared with UK SPMS white-matter samples. Source-specific effects will
be reported separately; agreement is required for a portable stage claim.

## Frozen Module Family

1. `receptor_cd44_cxcr4` - primary progression-adjacent state from V53.
2. `hla_regulatory`.
3. `mif_ligand`.
4. `ifn_apc_unique`.
5. `lysosomal_unique`.

No genes or modules will be added because of the observed V54 result.

## Adjustment And Null

Within each source/tissue stratum and module, regress the sample score on the
deposited lesion-context label, age (linear and quadratic), sex, and log
microglial yield. Average residuals per donor, then standardize donor residuals
within source. Estimate the pooled SPMS-minus-PPMS coefficient with a source
fixed effect.

Use 100,000 donor-label permutations per seed, preserving the observed number
of PPMS and SPMS donors inside each source. Use three fixed seeds. Report:

- pooled standardized coefficient and HC3 confidence interval;
- aggregate and per-seed two-sided permutation p-values;
- Benjamini-Hochberg q-values across five modules;
- max-T family-wise p-values across the same five modules;
- Amsterdam-only and UK-only effects and directions.

## Calling Rule

A module supports a portable cross-sectional stage association only if all are
true:

- pooled direction is the same in Amsterdam and UK;
- HC3 95% confidence interval excludes zero;
- aggregate permutation p is at most 0.05;
- BH q is at most 0.10;
- max-T family-wise p is at most 0.10.

Anything else is not-supported or inconclusive. A passing association would
remain provisional and non-causal and would require independent,
source-balanced replication with disability outcomes before any progression or
therapeutic interpretation.
