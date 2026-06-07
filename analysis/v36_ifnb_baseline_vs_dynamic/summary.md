# V36 IFN-beta Baseline-vs-Dynamic Audit

This asks whether `GSE24427` IFN-beta response context is a baseline
stratifier or a month-1 dynamic monitoring readout.

| feature | n | n_relapse_free | n_relapsed | auc_high_score_relapse_free | permutation_p | hedges_g_relapsefree_minus_relapsed | welch_p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| month1_delta_hla_ii | 25 | 16 | 9 | 0.75 | 0.01952 | 1.009 | 0.02239 |
| month1_delta_cd74 | 25 | 16 | 9 | 0.7222 | 0.03594 | 0.9276 | 0.0501 |
| month1_delta_ifn_apc | 25 | 16 | 9 | 0.6319 | 0.151 | -0.02223 | 0.9503 |
| month1_locked_style | 25 | 16 | 9 | 0.5764 | 0.2802 | 0.3935 | 0.2676 |
| baseline__hla_ii_without_cd74 | 25 | 16 | 9 | 0.3611 | 0.8754 | -0.4094 | 0.3026 |
| baseline__ifn_apc | 25 | 16 | 9 | 0.3403 | 0.9049 | -0.1727 | 0.6303 |
| baseline__cd74_alone | 25 | 16 | 9 | 0.2917 | 0.9583 | -0.7825 | 0.07836 |
| baseline__receptor_only_cd74_cd44_cxcr4 | 25 | 16 | 9 | 0.25 | 0.9816 | -0.7234 | 0.08039 |

## Interpretation

In this cohort, month-1 HLA-II/CD74 dynamics outperform baseline HLA-II.
This complements `GSE138064`, where baseline HLA-II competence was strong.
The IFN-beta branch may therefore contain both baseline competence and
early induction, depending on cohort/timing.
