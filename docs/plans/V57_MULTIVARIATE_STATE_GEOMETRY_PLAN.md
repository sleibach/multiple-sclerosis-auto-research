# V57 Multivariate Cell-State Geometry Probe: Frozen Plan

Status: **frozen before outcome analysis**

## Question

Can a treatment-response relationship appear in the joint distribution of
five APC/myeloid modules even though no individual module's one-dimensional
transport distance survived correction?

The held dataset is paired anti-TNF IBD single-cell data. This is a bounded
method probe and cross-disease context only, not an MS finding.

## Fixed Representation

- Input and audited pairs: the same GSE282122 object and pair contract as the
  V57 one-dimensional transport probe.
- Compartments: `DC` and `Mono_macro`.
- Modules: IFN/APC, HLA-II/APC, MIF/CD74 receptor state, lysosomal/APC, and
  inflammatory/NF-kB, with the fixed Wave67 gene sets.
- Cell scores: mean log1p counts per 10,000 over present module genes.
- Each module is scaled by the outcome-blind global median and IQR.
- At most 200 cells per sample/compartment are selected without replacement
  by a committed seed; smaller eligible groups use every cell.

## Primary Metric

For each paired sample and compartment:

1. median-center pre and post cell vectors separately in each module;
2. compute the biased multivariate energy distance using Euclidean cell-cell
   distances; and
3. collapse multiple sites to the patient median.

Separate median centering makes this a shape/dependence test rather than a
repeat of the module mean-delta analysis. Uncentered energy distance and the
norm of the mean shift are reported as diagnostics.

## Outcome Test

- Compare remission versus nonremission patient distances.
- Preserve remission counts within Crohn's disease and ulcerative colitis in
  every label permutation.
- Use 200,000 permutations, seed 57031.
- Correct the two-compartment family with the maximum absolute studentized
  statistic.

## Sensitivity

Residualize centered energy distance, without outcome labels, on disease,
technical-depth distribution distance, mean-shift norm, and absolute
inflammation-score change. Repeat the same max-T test on residuals.

Repeat the complete analysis with cell-subsampling/permutation seeds 57032
and 57033 using 100,000 permutations each.

## Promotion Gate

A compartment passes only when raw and residualized max-T p <= 0.10, effect
sign is unchanged, both diseases are estimable and direction-consistent, and
the pass recurs under both sensitivity seeds. Otherwise the result is
not-supported or inconclusive.
