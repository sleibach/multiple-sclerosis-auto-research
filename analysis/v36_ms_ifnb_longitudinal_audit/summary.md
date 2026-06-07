# V36 MS IFN-beta Longitudinal Audit

This uses the held `GSE24427` MS IFN-beta longitudinal artifact to test
whether a locked-style dynamic APC/HLA-II score behaves like an early
monitoring signal for 2-year relapse-free status.

| timepoint | feature | n | n_relapse_free | n_relapsed | auc_high_score_relapse_free | auc_permutation_p | permutation_mode | hedges_g_relapsefree_minus_relapsed | welch_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| month_1 | delta__cd74_alone | 25 | 16 | 9 | 0.7222 | 0.03696 | monte_carlo_50000 | 0.9276 | 0.0501 |
| month_1 | delta__hla_ii_without_cd74 | 25 | 16 | 9 | 0.75 | 0.02008 | monte_carlo_50000 | 1.009 | 0.02239 |
| month_1 | delta__ifn_apc | 25 | 16 | 9 | 0.6319 | 0.1513 | monte_carlo_50000 | -0.02223 | 0.9503 |
| month_1 | locked_style_score | 25 | 16 | 9 | 0.5764 | 0.2797 | monte_carlo_50000 | 0.3935 | 0.2676 |
| month_1 | negative_delta_ifn_apc | 25 | 16 | 9 | 0.3681 | 0.8627 | monte_carlo_50000 | 0.02223 | 0.9503 |
| month_1 | negative_delta_receptor | 25 | 16 | 9 | 0.4167 | 0.7577 | monte_carlo_50000 | -0.3742 | 0.4257 |
| month_24 | delta__cd74_alone | 25 | 16 | 9 | 0.6319 | 0.1491 | monte_carlo_50000 | 0.3498 | 0.3906 |
| month_24 | delta__hla_ii_without_cd74 | 25 | 16 | 9 | 0.4861 | 0.5577 | monte_carlo_50000 | 0.1843 | 0.6495 |
| month_24 | delta__ifn_apc | 25 | 16 | 9 | 0.3889 | 0.8218 | monte_carlo_50000 | -0.1209 | 0.7383 |
| month_24 | locked_style_score | 25 | 16 | 9 | 0.6042 | 0.2105 | monte_carlo_50000 | 0.1717 | 0.6566 |
| month_24 | negative_delta_ifn_apc | 25 | 16 | 9 | 0.6111 | 0.1926 | monte_carlo_50000 | 0.1209 | 0.7383 |
| month_24 | negative_delta_receptor | 25 | 16 | 9 | 0.3333 | 0.917 | monte_carlo_50000 | -0.5381 | 0.193 |
| second_injection | delta__cd74_alone | 25 | 16 | 9 | 0.6736 | 0.0852 | monte_carlo_50000 | 0.2491 | 0.5175 |
| second_injection | delta__hla_ii_without_cd74 | 25 | 16 | 9 | 0.6319 | 0.152 | monte_carlo_50000 | 0.114 | 0.7706 |
| second_injection | delta__ifn_apc | 25 | 16 | 9 | 0.7153 | 0.04206 | monte_carlo_50000 | 0.3362 | 0.3886 |
| second_injection | locked_style_score | 25 | 16 | 9 | 0.3333 | 0.9159 | monte_carlo_50000 | -0.4169 | 0.2782 |
| second_injection | negative_delta_ifn_apc | 25 | 16 | 9 | 0.2847 | 0.9631 | monte_carlo_50000 | -0.3362 | 0.3886 |
| second_injection | negative_delta_receptor | 25 | 16 | 9 | 0.4028 | 0.7873 | monte_carlo_50000 | -0.1343 | 0.7426 |

## Interpretation

This is an exploratory stress test on an older IFN-beta cohort. It can add
context about timing, but it does not edit the immutable V22 rule or create
a successor rule.
