# V36 T/B Readability Concordance

This grounds a Claude-proposed falsification test: if the V36 readout is
really readable in both T-like and B/plasma-like compartments, the same
patients should rank similarly across compartments.

| feature | n_patients | spearman_rho_t_vs_bplasma | spearman_exact_two_sided_p | pearson_r_t_vs_bplasma | sign_concordance | responder_mean_t | nonresponder_mean_t | responder_mean_bplasma | nonresponder_mean_bplasma |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| locked_signed_score | 9 | 0.8833 | 0.003075 | 0.6304 | 0.6667 | 1.037 | -0.08958 | 0.7852 | -1.026 |
| delta_IFN_APC | 9 | 0.8833 | 0.003075 | 0.6304 | 0.6667 | -1.037 | 0.08958 | -0.7852 | 1.026 |
| delta_HLAII | 9 | -0.01667 | 0.9816 | 0.001528 | 0.3333 | -0.6121 | -0.4377 | -0.6774 | 0.7457 |
| delta_RECEPTOR | 9 | 0.06667 | 0.8801 | -0.2069 | 0.5556 | 0.423 | 0.2189 | 0.5618 | -0.8517 |

Interpretation: positive concordance supports only the wording that the
broad IFN/APC/STAT1 response is T/B-readable. It does not make the
compartment readouts independent mechanisms and does not override the
multiplicity and single-cohort caveats.
