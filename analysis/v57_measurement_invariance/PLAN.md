# V57 Cross-Environment Measurement-Invariance Plan

## Question

Do the frozen V22 modules have concordant internal gene-correlation architecture
in the two bounded environments, or does a shared gene list mask different
latent measurements across PBMC DMF and intestinal anti-TNF data?

## Frozen probe

- Use the same paired subject-level gene deltas and original loaders as the
  V22 gene-influence audit; no fresh or quarantined data.
- Primary module families: the seven-gene IFN/APC module and six-gene HLA-II
  module. The 12-gene union is exploratory.
- Within each cohort and module, compute the Spearman gene-by-gene correlation
  matrix over paired subject deltas.
- Primary concordance statistic: Pearson correlation between the off-diagonal
  edges of the two cohort matrices.
- Gene-identity null: permute gene labels in the second matrix. Enumerate all
  permutations for each primary module; use 200,000 seeded permutations for
  the 12-gene exploratory union.
- Patient uncertainty: independently bootstrap patients within each cohort
  10,000 times under each of three seeds; retain aggregate confidence intervals
  only.

## Gate

Cross-environment module measurement invariance requires **both** primary
modules to have:

1. edge concordance at least `0.50`;
2. gene-label permutation p below `0.025` (Bonferroni for two modules); and
3. bootstrap 95% lower confidence bound above zero under every seed.

The union cannot rescue a failed primary module. No threshold is changed after
seeing results.

## Boundary

Passing would support cross-environment measurement comparability, not response
association, mechanism, transportability, or clinical validation. Failing means
the pooled bounded result must remain an empirical score association and cannot
be elevated to a shared latent APC/HLA-II construct from these data alone.
