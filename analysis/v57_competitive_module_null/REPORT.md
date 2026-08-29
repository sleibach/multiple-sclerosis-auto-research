# V57 Competitive Matched-Module Null Result

## Result

- Competitive specificity gate: **PASS**.
- Intact V22 pooled cohort-percentile AUC: `0.822`.
- Null scale: 600,000 random module pairs over
  18,003 common, variable, measured genes.

| neighbors | seed | null median | null q95 | null q99 | null max | empirical p | pass |
|---:|---:|---:|---:|---:|---:|---:|---|
| 25 | 5721 | 0.600 | 0.800 | 0.844 | 0.956 | 0.031319 | True |
| 25 | 5722 | 0.600 | 0.800 | 0.844 | 1.000 | 0.030339 | True |
| 25 | 5723 | 0.600 | 0.800 | 0.844 | 0.956 | 0.030719 | True |
| 50 | 5721 | 0.600 | 0.800 | 0.844 | 1.000 | 0.032259 | True |
| 50 | 5722 | 0.600 | 0.800 | 0.867 | 1.000 | 0.033979 | True |
| 50 | 5723 | 0.600 | 0.800 | 0.867 | 1.000 | 0.033319 | True |
| 100 | 5721 | 0.600 | 0.778 | 0.844 | 0.978 | 0.028739 | True |
| 100 | 5722 | 0.622 | 0.778 | 0.844 | 0.978 | 0.029259 | True |
| 100 | 5723 | 0.622 | 0.800 | 0.844 | 0.978 | 0.031859 | True |
| 200 | 5721 | 0.600 | 0.778 | 0.844 | 0.956 | 0.020720 | True |
| 200 | 5722 | 0.600 | 0.778 | 0.844 | 1.000 | 0.020000 | True |
| 200 | 5723 | 0.600 | 0.778 | 0.844 | 0.978 | 0.019560 | True |

## Interpretation boundary

The null preserves module sizes, the shared-gene topology, therapy-class
formulas, and cross-cohort expression/variance neighborhoods. Random module
identities were deliberately not retained or mined. Passing would make an
arbitrary small matched module less plausible as a sufficient explanation for
the same-data association. It would not establish functional or mechanistic
specificity: the null is not matched on immune annotation, within-module
correlation, tissue role, or prior selection history. It also cannot repair the
failed cross-environment measurement-invariance and partial-conjunction gates.
