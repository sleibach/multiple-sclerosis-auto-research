# Macnair Validation Frozen CD44/CXCR4 Test

Verdict: **REPLICATED_AND_DECOUPLED**.

After deterministic cross-study donor de-duplication, the test includes `31` donors
(`18` MS, `13` controls),
`11222` annotated microglia, and the exact frozen score genes.
The adjusted disease beta is `1.414` (wild p `0.0000`,
HC3 95% CI `0.806` to `2.022`); the raw standardized
MS-control effect is `2.212`.

Study/batch association has p `0.9423` and Cramer's V `0.062`. Age SMD is
`-0.723`. The clean replication gate passes `9/9`
components. Secondary decoupling is not claimed unless both frozen contrasts pass BH q <= 0.10
after a clean primary replication.
The score-to-log-microglia-count correlation is `0.666`,
but count-adjusted disease beta is `1.075` (wild p
`0.0048`), and all executable thresholds in the transparent
post-result 1/10/25/50/100-cell sensitivity grid retain positive direction. The grid is a
conservative quality tightening, not part of the frozen primary; it addresses, but does not erase,
sparse-control-pseudobulk risk.

This is an independent public-cohort analysis, but it remains a state-association test. It cannot
establish causality, therapeutic direction, or target status.
