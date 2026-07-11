# Macnair Discovery Frozen CD44/CXCR4 Test

Verdict: **FROZEN_PRIMARY_PASS_QUALITY_SENSITIVE**.

After deterministic cross-study donor de-duplication, the test includes `80` donors
(`54` MS, `26` controls),
`51677` annotated microglia, and the exact frozen score genes.
The adjusted disease beta is `0.510` (wild p `0.0046`,
HC3 95% CI `0.142` to `0.879`); the raw standardized
MS-control effect is `0.669`.

Study/batch association has p `1.0000` and Cramer's V `0.000`. Age SMD is
`-0.017`. The clean replication gate passes `8/9`
components. Secondary decoupling is not claimed unless both frozen contrasts pass BH q <= 0.10
after a clean primary replication.
The score-to-log-microglia-count correlation is `0.389`,
but count-adjusted disease beta is `0.341` (wild p
`0.0540`), and all executable thresholds in the transparent
post-result 1/10/25/50/100-cell sensitivity grid retain positive direction. The grid is a
conservative quality tightening, not part of the frozen primary; it addresses, but does not erase,
sparse-control-pseudobulk risk.

This is an independent public-cohort analysis, but it remains a state-association test. It cannot
establish causality, therapeutic direction, or target status.
