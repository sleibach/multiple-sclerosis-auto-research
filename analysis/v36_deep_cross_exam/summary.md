# V36 Deep Cross-Exam Grounding

- Claude status: empty output file in this round.
- Gemini status: usable fenced JSON critique.

## patient bootstrap of raw locked T/B-minus-non-T/B AUC gap

- point_residualized_gap: `0.1333333333333333`
- bootstrap_raw_gap_mean: `0.14549838714828653`
- bootstrap_raw_gap_ci_low: `0.0`
- bootstrap_raw_gap_ci_high: `0.28517857142857045`
- bootstrap_p_gap_le_zero: `0.04024144869215292`
- n_bootstrap: `4970`

## B/plasma-only versus T-cell-only versus T/B mean locked score

- b_plasma_auc: `0.95`
- t_cell_auc: `1.0`
- tb_mean_auc: `0.95`
- interpretation: `B/plasma-only retains most of the T/B signal; combined T/B does not outperform the best single T/B component in n=9.`

## MS pregnancy-phase HLA-II and CD64 component separability

- spearman_hla_ii_vs_cd64_all_samples: `0.022058823529411766`
- n_samples: `17`
- interpretation: `The metric combines separable arms; it should be reported as component-wise HLA-II and CD64 plus the difference, not as a single opaque score.`

