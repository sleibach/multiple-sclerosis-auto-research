# V53 GSE301908 Low-Control Sensitivity

Verdict: **LOW_CONTROL_SENSITIVITY_NOT_SUPPORTED**.

The held object contributes `14` MS and only
`3` control donors (`25,036` deposited
Micro nuclei). Its RNA assay contains normalized `data` but no raw-count layer,
so the test averages deposited normalized expression per donor and applies the
unchanged CD44/CXCR4 z-score as a platform-mismatched sensitivity.

Disease beta after age, quadratic age, and sex adjustment is `0.438`
(HC3 CI `-1.546` to `2.422`, p `0.6653`).
The exact null enumerates `680` full-rank placements of three controls;
two-sided p is `0.4779`. Score/microglia-count Spearman rho is
`0.400`.

Regardless of direction, three controls cannot satisfy the frozen replication
definition or support a mechanism, stage claim, monitoring rule, intervention
direction, or target. The result is retained only as a low-control sensitivity.
