# V53 Pharmacodynamic Edge Robustness

Verdict: **PHARMACODYNAMIC_EDGE_NOT_PORTABLE_ACROSS_DATASET_SENSITIVITIES**.

The disjoint edge has global rho `0.535` and a dataset-stratified
permutation p-value of `0.0131`. After removing dataset
means, rho is `0.087` (`p=0.8077`); pooled
within-dataset ranks give rho `0.511` (`p=0.0281`).

The leave-one-dataset-out minimum global rho is `0.327`
and the minimum centered rho is `-0.130`. The dataset-cluster
bootstrap centered-rho interval is `[-0.617, 0.894]`.

This is a stability test of an existing pharmacodynamic relationship. It does
not establish causal direction, component specificity, treatment benefit, or a
therapeutic target, and it changes no frozen rule or validation threshold.
