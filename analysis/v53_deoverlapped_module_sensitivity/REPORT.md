# V53 De-overlapped APC Module Sensitivity

Verdict: **PERTURBATION_HLA_MIF_GLOBAL_ASSOCIATION_FAILS_STIMULUS_CONTROL_GLOBAL_STATUS_UNCHANGED**.

The gene-level rebuild matches the committed V26 perturbation matrix to a maximum
absolute error of `4.44e-16`. Every gene appearing in more than one
module was then removed before recomputing all 24 signatures.

For HLA-II/APC versus receptor-state, Spearman rho changes from
`0.798` to
`0.647`; the six-pair BH q-value is
`0.0099` under a global shuffle but
`0.7665` when labels are
shuffled only within cytokine stimuli. The paired-bootstrap attenuation interval
is `-0.413` to
`0.002`. The result is a sensitivity for the
perturbation modality only. It does not edit the modules or change the V26
multi-modality architecture by itself.
