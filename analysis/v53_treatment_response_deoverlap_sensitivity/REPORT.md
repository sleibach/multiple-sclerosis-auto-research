# V53 Treatment-Response De-overlap Sensitivity

Verdict: **TREATMENT_RESPONSE_HLA_MIF_EDGE_FAILS_DISJOINT_READOUT_GATE**.

Held RA counts and IBD single-cell pseudobulk inputs were reprocessed under original
and globally disjoint module definitions. The original 20-row V26 response matrix
reproduces to maximum absolute error `2.22e-16`.

HLA-II/APC versus receptor-state rho changes from
`0.878` to
`-0.059`. The unique-score global and
dataset/endpoint-stratified q-values are
`0.8068` and
`0.6707`.
This sensitivity does not alter the locked V22 rule.
