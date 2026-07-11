# V53 Pharmacodynamic De-overlap Sensitivity

Verdict: **PHARMACODYNAMIC_HLA_MIF_EDGE_PERSISTS_WITH_DISJOINT_READOUTS**.

All `24` V26 pharmacodynamic contexts were rebuilt from source inputs under
original and globally disjoint module definitions. Public downloads were cached in
memory across both passes. The original matrix reproduces to `2.22e-16`.

HLA-II/APC versus receptor-state rho changes from
`0.758` to
`0.535`. The disjoint global and
dataset-stratified q-values are `0.0150`
and `0.0231`.

The association criteria pass with complete coverage: all `24` contexts
and all `6` datasets retain both globally unique readouts.
The paired attenuation CI is
`[-0.512,
0.038]`, so attenuation is not
established. This layer is therefore suggestive but cannot rescue a claim of robust,
independently measured coupling across the full pharmacodynamic evidence set.
